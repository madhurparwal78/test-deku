import crypto from 'node:crypto';
import { Hono } from 'hono';
import { query, withTransaction } from '../lib/db.js';
import { HttpError, requireSession, idempotent, readBody, strField, intField, refusePagination, assertNoDecimal } from '../lib/http.js';
import { periodView, allocate, closePeriod, openRestatement } from '../lib/ledger.js';
import { appendEntry } from '../lib/record.js';
import { flMulDiv } from '../lib/num.js';
import { decorateBatch } from '../lib/claims.js';
export const ledger = new Hono();
ledger.get('/balance-periods', async (c) => {
    refusePagination(c);
    const rows = await query(`select * from balance_periods order by period_from, site`);
    const out = [];
    for (const r of rows)
        out.push(await periodView(r.id));
    return c.json(out);
});
ledger.get('/balance-periods/:id', async (c) => {
    refusePagination(c);
    const v = await periodView(c.req.param('id'));
    if (!v)
        throw new HttpError(404, 'not_found');
    return c.json(v);
});
ledger.post('/balance-periods/:id/allocations', async (c) => {
    const s = await requireSession(c);
    if (!s.roles.includes('claims_manager'))
        throw new HttpError(403, 'claims_manager_required');
    const period = c.req.param('id');
    return idempotent(c, async () => {
        const body = await readBody(c);
        assertNoDecimal(body);
        const lot = strField(body.lot, 'lot');
        const category = strField(body.category, 'category', ['post_consumer', 'pre_consumer']);
        const massG = intField(body.mass_g, 'mass_g', { min: 1 });
        const out = await allocate({
            period, lot, category, mass_g: massG, by: s.email,
            decided_by: body.decided_by, favoured_over: body.favoured_over,
        });
        return out;
    }).then((r) => c.json(r.body, r.status));
});
ledger.post('/balance-periods/:id/transfers', async (c) => {
    const s = await requireSession(c);
    if (!s.roles.includes('claims_manager'))
        throw new HttpError(403, 'claims_manager_required');
    const fromPeriod = c.req.param('id');
    return idempotent(c, async () => {
        const body = await readBody(c);
        assertNoDecimal(body);
        const toPeriod = strField(body.to_period, 'to_period');
        const massG = intField(body.mass_g, 'mass_g', { min: 1 });
        const category = strField(body.category, 'category', ['post_consumer', 'pre_consumer']);
        const from = (await query(`select * from balance_periods where id = $1`, [fromPeriod]))[0];
        const to = (await query(`select * from balance_periods where id = $1`, [toPeriod]))[0];
        if (!from || !to)
            throw new HttpError(404, 'not_found');
        if (to.state === 'closed')
            throw new HttpError(409, 'period_closed');
        const ref = `TRF-${String((await query(`select count(*)::int as n from transfers`))[0].n + 1).padStart(4, '0')}`;
        await withTransaction(async (cl) => {
            await cl.query(`insert into transfers(reference, from_period, to_period, mass_g, category, moved_by) values ($1,$2,$3,$4,$5,$6)`, [ref, fromPeriod, toPeriod, massG, category, s.email]);
            await cl.query(`insert into credit_movements(reference, period, kind, category, mass_g, origin_site, movement, created_by, effective_on)
         values ($1,$2,'out',$3,$4,$5,'transfer',$6,$7)`, ['CRD-' + crypto.randomUUID().slice(0, 8).toUpperCase(), fromPeriod, category, massG, to.site, s.email, new Date().toISOString().slice(0, 10)]);
            await cl.query(`insert into credit_movements(reference, period, kind, category, mass_g, origin_site, movement, created_by, effective_on)
         values ($1,$2,'in',$3,$4,$5,'transfer',$6,$7)`, ['CRD-' + crypto.randomUUID().slice(0, 8).toUpperCase(), toPeriod, category, massG, from.site, s.email, new Date().toISOString().slice(0, 10)]);
            await appendEntry(cl, { act: 'transfer_recorded', person: s.email, site: from.site, object: ref,
                content: { reference: ref, from_period: fromPeriod, to_period: toPeriod, mass_g: massG, category } });
        });
        const receiving = await periodView(toPeriod);
        return {
            status: 201,
            body: {
                reference: ref, from_period: fromPeriod, to_period: toPeriod, mass_g: massG, category,
                inbound_credits: receiving?.inbound_credits ?? [],
                note: 'A transfer is never a fresh credit; the total credit across the two periods is unchanged.',
            },
        };
    }).then((r) => c.json(r.body, r.status));
});
ledger.post('/balance-periods/:id/close', async (c) => {
    const s = await requireSession(c);
    if (!s.roles.includes('claims_manager'))
        throw new HttpError(403, 'claims_manager_required');
    const period = c.req.param('id');
    // Whoever published the carbon method version the period applies does not close it.
    const p = (await query(`select * from balance_periods where id = $1`, [period]))[0];
    if (!p)
        throw new HttpError(404, 'not_found');
    const methods = await query(`select published_by from carbon_methods where key = $1 order by version desc limit 1`, ['CM-PA6']);
    if (methods.length && methods[0].published_by === s.email) {
        throw new HttpError(403, 'method_publisher_may_not_close_period', { published_by: methods[0].published_by });
    }
    return idempotent(c, async () => {
        const body = await readBody(c).catch(() => ({}));
        return closePeriod(period, s.email);
    }).then((r) => c.json(r.body, r.status));
});
ledger.post('/balance-periods/:id/restatements', async (c) => {
    const s = await requireSession(c);
    if (!s.roles.includes('claims_manager'))
        throw new HttpError(403, 'claims_manager_required');
    const period = c.req.param('id');
    return idempotent(c, async () => {
        const body = await readBody(c);
        const reason = strField(body.reason, 'reason');
        return openRestatement({
            period, reason, by: s.email,
            factor_reference: body.factor_reference, new_factor_bp: body.new_factor_bp,
        });
    }).then((r) => c.json(r.body, r.status));
});
ledger.get('/restatements', async (c) => {
    const rows = await query(`select * from restatements order by opened_on desc`);
    const res = await query(`select * from resolutions order by resolved_on`);
    return c.json(rows.map((r) => ({
        reference: r.reference, period: r.period, reason: r.reason, opened_on: r.opened_on, opened_by: r.opened_by,
        state: r.state, affected_certificates: r.affected_certificates, content_movements: r.content_movements,
        resolutions: res.filter((x) => x.restatement === r.reference).map((x) => ({
            certificate: x.certificate, outcome: x.outcome, reason: x.reason, resolved_on: x.resolved_on, resolved_by: x.resolved_by,
        })),
    })));
});
ledger.post('/restatements/:reference/resolutions', async (c) => {
    const s = await requireSession(c);
    if (!s.roles.includes('claims_manager'))
        throw new HttpError(403, 'claims_manager_required');
    return idempotent(c, async () => {
        const body = await readBody(c);
        const certificate = strField(body.certificate, 'certificate');
        const outcome = strField(body.outcome, 'outcome', ['reissued', 'withdrawn', 'unaffected']);
        const reason = strField(body.reason, 'reason');
        const rst = (await query(`select * from restatements where reference = $1`, [c.req.param('reference')]))[0];
        if (!rst)
            throw new HttpError(404, 'not_found');
        if (!rst.affected_certificates.includes(certificate)) {
            throw new HttpError(409, 'certificate_not_in_restatement', { certificate, affected: rst.affected_certificates });
        }
        const existing = (await query(`select 1 from resolutions where restatement = $1 and certificate = $2`, [rst.reference, certificate])).length > 0;
        if (existing)
            throw new HttpError(409, 'already_resolved', { certificate });
        await withTransaction(async (cl) => {
            await cl.query(`insert into resolutions(restatement, certificate, outcome, reason, resolved_by) values ($1,$2,$3,$4,$5)`, [rst.reference, certificate, outcome, reason, s.email]);
            await appendEntry(cl, { act: 'restatement_resolved', person: s.email, object: rst.reference,
                content: { restatement: rst.reference, certificate, outcome, reason } });
        });
        return { status: 201, body: { reference: `RES-${rst.reference}-${certificate}`, restatement: rst.reference, certificate, outcome, reason } };
    }).then((r) => c.json(r.body, r.status));
});
// ---------------- conversion factors ----------------
ledger.get('/conversion-factors', async (c) => {
    const rows = await query(`select * from conversion_factors order by site, published_on desc`);
    return c.json(rows.map(factorView));
});
function factorView(f) {
    return {
        reference: f.reference, site: f.site, factor_bp: f.factor_bp,
        derived_from: f.derived_from, derived_to: f.derived_to,
        derived_in_g: Number(f.derived_in_g), derived_out_g: Number(f.derived_out_g),
        provisional: f.provisional, published_by: f.published_by, published_on: f.published_on,
        derivation: {
            formula: 'factor_bp = derived_out_g * 10000 / derived_in_g, floored',
            check: Number(f.derived_in_g) > 0 ? flMulDiv(Number(f.derived_out_g), 10000, Number(f.derived_in_g)) : null,
            note: f.provisional ? 'No derivation window: provisional by declaration.' : 'Derived from a stated window.',
        },
    };
}
ledger.post('/conversion-factors', async (c) => {
    const s = await requireSession(c);
    if (!s.roles.includes('claims_manager'))
        throw new HttpError(403, 'claims_manager_required');
    return idempotent(c, async () => {
        const body = await readBody(c);
        assertNoDecimal(body);
        const site = strField(body.site, 'site');
        const factorBp = intField(body.factor_bp, 'factor_bp', { min: 0, max: 10000 });
        const derivedIn = intField(body.derived_in_g ?? 0, 'derived_in_g', { min: 0 });
        const derivedOut = intField(body.derived_out_g ?? 0, 'derived_out_g', { min: 0 });
        const provisional = derivedIn === 0;
        if (!provisional) {
            const implied = flMulDiv(derivedOut, 10000, derivedIn);
            if (implied !== factorBp) {
                throw new HttpError(409, 'factor_not_derived', {
                    factor_bp: factorBp, derived_from_window: implied,
                    rule: 'factor_bp must equal derived_out_g * 10000 / derived_in_g, floored.',
                });
            }
        }
        const siteRow = (await query(`select * from sites where reference = $1`, [site]))[0];
        if (!siteRow)
            throw new HttpError(404, 'site_not_found');
        const short = site.replace('SITE-', '');
        const n = (await query(`select count(*)::int as n from conversion_factors where site = $1`, [site]))[0].n;
        const ref = `CF-${short}-${n + 1}`;
        await withTransaction(async (cl) => {
            await cl.query(`insert into conversion_factors(reference, site, factor_bp, derived_from, derived_to, derived_in_g, derived_out_g, provisional, published_by)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9)`, [ref, site, factorBp, body.derived_from ?? null, body.derived_to ?? null, derivedIn, derivedOut, provisional, s.email]);
            await appendEntry(cl, { act: 'conversion_factor_published', person: s.email, site, object: ref,
                content: { reference: ref, site, factor_bp: factorBp, derived_in_g: derivedIn, derived_out_g: derivedOut } });
        });
        const row = (await query(`select * from conversion_factors where reference = $1`, [ref]))[0];
        return { status: 201, body: factorView(row) };
    }).then((r) => c.json(r.body, r.status));
});
// ---------------- reconciliation ----------------
ledger.get('/reconciliation', async (c) => {
    const runs = await query(`select * from runs`);
    const cons = await query(`select * from consumptions`);
    const outs = await query(`select * from outputs`);
    const batches = await query(`select b.*, d.calibrated_on from batches b join devices d on d.reference = b.device`);
    const certs = await query(`select * from certificates`);
    const inbound = await query(`select source, max(received_at) as last from inbound_records group by source`);
    let massIn = 0, massOut = 0;
    for (const r of runs) {
        const ins = cons.filter((x) => x.run === r.reference).reduce((s, x) => s + Number(x.mass_g), 0);
        const os = outs.filter((x) => x.run === r.reference).reduce((s, x) => s + Number(x.mass_g), 0);
        massIn += ins;
        massOut += os;
    }
    const creditMargin = await totalCreditMargin();
    const brokenCustody = [];
    for (const b of batches) {
        const v = await decorateBatch(b);
        if (!v.custody_complete)
            brokenCustody.push(b.reference);
    }
    void certs;
    const ages = {
        weighbridge: null, control_system: null, laboratory: null, customer_reporting: null,
    };
    const now = Date.now();
    for (const row of inbound)
        ages[row.source] = Math.floor((now - new Date(row.last).getTime()) / 3600000);
    return c.json({
        read_at: new Date().toISOString(),
        mass_balance_residual_g: massIn - massOut,
        credit_margin_g: creditMargin,
        consumptions_on_open_runs: cons.filter((x) => runs.find((r) => r.reference === x.run)?.state === 'open').length,
        batches_with_broken_custody: brokenCustody,
        certificates_with_superseded_figures: await supersededFigureCertificates(),
        integration_ages: ages,
        derivation: {
            mass_balance_residual_g: 'sum(runs mass in) - sum(runs mass out)',
            credit_margin_g: 'sum(credits in) - sum(credits out) across every period',
            integration_ages: 'hours since the most recent inbound record per source; null when never sent',
        },
    });
});
async function totalCreditMargin() {
    const movs = await query(`select * from credit_movements`);
    let margin = 0;
    for (const cat of ['post_consumer', 'pre_consumer']) {
        const inG = movs.filter((m) => m.kind === 'in' && m.category === cat && !m.origin_site).reduce((s, m) => s + Number(m.mass_g), 0);
        const outG = movs.filter((m) => m.kind === 'out' && m.category === cat).reduce((s, m) => s + Number(m.mass_g), 0);
        margin += inG - outG;
    }
    return margin;
}
async function supersededFigureCertificates() {
    const rows = await query(`select c.number from certificates c join carbon_figures f on f.id = c.carbon_figure
      where f.superseded_by is not null`);
    return rows.map((r) => r.number);
}
