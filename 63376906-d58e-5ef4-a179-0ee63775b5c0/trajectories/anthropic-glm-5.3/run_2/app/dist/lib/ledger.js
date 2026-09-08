import crypto from 'node:crypto';
import { query, withTransaction } from './db.js';
import { flMulDiv } from './num.js';
import { HttpError } from './http.js';
import { appendEntry } from './record.js';
import { batchView } from './claims.js';
export async function periodMovements(period) {
    return query(`select * from credit_movements where period = $1 order by recorded_at, reference`, [period]);
}
export async function periodView(period) {
    const rows = await query(`select * from balance_periods where id = $1`, [period]);
    if (!rows.length)
        return null;
    return decoratePeriod(rows[0]);
}
export async function decoratePeriod(p) {
    const movements = await periodMovements(p.id);
    const factors = await query(`select * from conversion_factors where site = $1 order by published_on desc`, [p.site]);
    const overrides = await query(`select count(*)::int as n from overrides o join lots l on l.reference = o.lot
      where l.site = $1 and o.reviewed = false`, [p.site]);
    const restatements = await query(`select count(*)::int as n from restatements where period = $1 and state = 'open'`, [p.id]);
    const findings = await query(`select count(*)::int as n from findings where state = 'open'`);
    const consumed = await query(`select c.input_reference, c.mass_g from consumptions c
       join runs r on r.reference = c.run where r.site = $1`, [p.site]);
    let nonClaimableG = 0;
    for (const cm of consumed) {
        if (!cm.input_reference.startsWith('BATCH-'))
            continue;
        const bv = await batchView(cm.input_reference);
        if (bv && !bv.claimable)
            nonClaimableG += Number(cm.mass_g);
    }
    const inG = { post_consumer: 0, pre_consumer: 0 };
    const outG = { post_consumer: 0, pre_consumer: 0 };
    const inbound = [];
    const transferredIn = { post_consumer: 0, pre_consumer: 0 };
    for (const m of movements) {
        if (m.kind === 'in') {
            if (m.origin_site) {
                inbound.push({ reference: m.reference, mass_g: Number(m.mass_g), origin_site: m.origin_site, movement: m.movement, fresh_credit: false });
                transferredIn[m.category] = (transferredIn[m.category] ?? 0) + Number(m.mass_g);
            }
            else {
                inG[m.category] = (inG[m.category] ?? 0) + Number(m.mass_g);
            }
        }
        else if (m.kind === 'out')
            outG[m.category] = (outG[m.category] ?? 0) + Number(m.mass_g);
    }
    // Credits available includes credit that arrived by transfer, which is never a fresh credit.
    const available = {
        post_consumer: (inG.post_consumer ?? 0) + (transferredIn.post_consumer ?? 0) - (outG.post_consumer ?? 0),
        pre_consumer: (inG.pre_consumer ?? 0) + (transferredIn.pre_consumer ?? 0) - (outG.pre_consumer ?? 0),
    };
    const factorRows = factors.map((f) => ({
        reference: f.reference, factor_bp: f.factor_bp, derived_from: f.derived_from, derived_to: f.derived_to,
        derived_in_g: Number(f.derived_in_g), derived_out_g: Number(f.derived_out_g), provisional: f.provisional,
        version: f.reference,
    }));
    return {
        id: p.id, site: p.site, grade: p.grade,
        period: `${p.period_from} to ${p.period_to}`,
        period_from: p.period_from, period_to: p.period_to,
        state: p.state, carry_over_limit_bp: p.carry_over_limit_bp,
        closed_on: p.closed_on ?? null, cut_off: p.cut_off ?? null,
        allocation_basis: p.allocation_basis,
        conversion_factor: factorRows.find((f) => f.reference === p.conversion_factor) ?? factorRows[0] ?? null,
        credits_in_g: inG, credits_out_g: outG, credits_available_g: available,
        conversion_factors: factorRows,
        override_count: overrides[0].n,
        open_restatement_count: restatements[0].n,
        open_finding_count: findings[0].n,
        non_claimable_input_g: nonClaimableG,
        inbound_credits: inbound,
        carried_forward_g: p.carried_forward_g ?? null,
        expired_g: p.expired_g ?? null,
        derivation: {
            movements: `credit_movements for ${p.id}`,
            note: 'A balance is the sum of its movements and is never held as a total.',
            read_at: new Date().toISOString(),
        },
    };
}
/** Credit granted at a consumption: dry mass consumed times the site factor, floored. */
export function creditFor(dryMassG, factorBp) {
    return flMulDiv(dryMassG, factorBp, 10000);
}
/** Attach claim to a lot inside a serialisable transaction: one success, one refusal. */
export async function allocate(params) {
    return withTransaction(async (c) => {
        await c.query(`set transaction isolation level serializable`);
        const periodRow = (await c.query(`select * from balance_periods where id = $1 for update`, [params.period])).rows[0];
        if (!periodRow)
            throw new HttpError(404, 'not_found');
        if (periodRow.state === 'closed')
            throw new HttpError(409, 'period_closed', { closed_on: periodRow.closed_on });
        const lotRow = (await c.query(`select * from lots where reference = $1`, [params.lot])).rows[0];
        if (!lotRow)
            throw new HttpError(404, 'lot_not_found');
        if (lotRow.site !== periodRow.site)
            throw new HttpError(409, 'site_mismatch', { lot_site: lotRow.site, period_site: periodRow.site });
        const movs = (await c.query(`select * from credit_movements where period = $1 for update`, [params.period])).rows;
        let inG = 0, outG = 0;
        for (const m of movs) {
            if (m.category !== params.category)
                continue;
            if (m.kind === 'in')
                inG += Number(m.mass_g);
            if (m.kind === 'out')
                outG += Number(m.mass_g);
        }
        const available = inG - outG;
        if (params.mass_g > available) {
            const entry = await appendEntry(c, {
                act: 'allocation_refused', person: params.by, site: periodRow.site, object: params.lot,
                content: { period: params.period, lot: params.lot, category: params.category,
                    available_g: available, requested_g: params.mass_g, refused: true },
            });
            return {
                status: 409,
                body: {
                    error: 'insufficient_credits', available_g: available, requested_g: params.mass_g,
                    category: params.category, reference: null, entry_seq: entry.seq,
                },
            };
        }
        const ref = 'CRD-' + crypto.randomUUID().slice(0, 8).toUpperCase();
        const factorRow = (await c.query(`select * from conversion_factors where site = $1 order by (provisional), published_on desc limit 1`, [periodRow.site])).rows[0];
        await c.query(`insert into credit_movements(reference, period, kind, category, mass_g, factor_version, lot, created_by, effective_on, decided_by, favoured_over)
       values ($1,$2,'out',$3,$4,$5,$6,$7,$8,$9,$10)`, [ref, params.period, params.category, params.mass_g, factorRow?.reference ?? null, params.lot,
            params.by, new Date().toISOString().slice(0, 10), params.decided_by ?? params.by,
            JSON.stringify(params.favoured_over ?? [])]);
        const attached = (await c.query(`select coalesce(sum(mass_g),0)::bigint as n from credit_movements where lot = $1 and kind = 'out'`, [params.lot])).rows[0];
        const attachedG = Number(attached.n);
        const contentBp = flMulDiv(attachedG, 10000, Number(lotRow.mass_g));
        await appendEntry(c, {
            act: 'allocation_recorded', person: params.by, site: periodRow.site, object: params.lot,
            content: { period: params.period, lot: params.lot, category: params.category, mass_g: params.mass_g,
                factor_version: factorRow?.reference ?? null, credit_attached_g: attachedG, content_bp: contentBp },
        });
        return {
            status: 201,
            body: {
                reference: ref, period: params.period, lot: params.lot, category: params.category,
                mass_g: params.mass_g, credit_attached_g: attachedG, content_bp: contentBp,
                derivation: { formula: 'content_bp = credit_attached_g * 10000 / lot_mass_g, floored',
                    lot_mass_g: Number(lotRow.mass_g), movements: `credit_movements where lot = ${params.lot}` },
            },
        };
    });
}
export async function closePeriod(period, by) {
    return withTransaction(async (c) => {
        await c.query(`set transaction isolation level serializable`);
        const p = (await c.query(`select * from balance_periods where id = $1 for update`, [period])).rows[0];
        if (!p)
            throw new HttpError(404, 'not_found');
        if (p.state === 'closed')
            throw new HttpError(409, 'period_closed', { closed_on: p.closed_on });
        // Lots in the period are the lots carrying claim in it, plus any pending lot at the site.
        const openLots = (await c.query(`select reference from lots where site = $1 and disposition = 'pending'`, [p.site])).rows;
        const claimedLots = (await c.query(`select distinct lot from credit_movements where period = $1 and lot is not null`, [period])).rows.map((r) => r.lot);
        const openDevs = (await c.query(`select reference from deviations where state = 'open' and lots && $1::text[]`, [claimedLots])).rows;
        const movs = (await c.query(`select * from credit_movements where period = $1`, [period])).rows;
        const imbalance = movs.some((m) => m.kind === 'out' && Number(m.mass_g) > (movs.filter((x) => x.kind === 'in' && x.category === m.category).reduce((s, x) => s + Number(x.mass_g), 0)));
        const problems = [];
        if (openLots.length)
            problems.push('lot_without_disposition');
        if (openDevs.length)
            problems.push('open_deviation');
        if (imbalance)
            problems.push('balance_does_not_reconcile');
        if (problems.length) {
            await appendEntry(c, { act: 'period_close_refused', person: by, site: p.site, object: period,
                content: { period, problems, lots: openLots.map((l) => l.reference), deviations: openDevs.map((d) => d.reference) } });
            return { status: 409, body: { error: 'period_close_refused', problems, lots: openLots.map((l) => l.reference), deviations: openDevs.map((d) => d.reference) } };
        }
        // Settle the carry-over per category.
        const carried = {};
        const expired = {};
        for (const cat of ['post_consumer', 'pre_consumer']) {
            const inTotal = movs.filter((m) => m.kind === 'in' && m.category === cat).reduce((s, m) => s + Number(m.mass_g), 0);
            const outTotal = movs.filter((m) => m.kind === 'out' && m.category === cat).reduce((s, m) => s + Number(m.mass_g), 0);
            const availableCat = inTotal - outTotal;
            const limit = flMulDiv(inTotal, p.carry_over_limit_bp, 10000);
            const carry = Math.max(0, Math.min(availableCat, limit));
            carried[cat] = carry;
            expired[cat] = Math.max(0, availableCat - carry);
            if (carry > 0) {
                // The receiving period is the next period at the same site and grade, if one exists.
                const next = (await c.query(`select id from balance_periods where site = $1 and grade = $2 and period_from > $3 order by period_from limit 1`, [p.site, p.grade, p.period_from])).rows[0];
                if (next) {
                    await c.query(`insert into credit_movements(reference, period, kind, category, mass_g, origin_site, movement, created_by, effective_on)
             values ($1,$2,'in',$3,$4,$5,'carry_over',$6,$7)`, ['CRD-' + crypto.randomUUID().slice(0, 8).toUpperCase(), next.id, cat, carry, p.site, by, p.period_to]);
                }
            }
        }
        const closedOn = new Date().toISOString().slice(0, 10);
        const cutOff = closedOn;
        await c.query(`update balance_periods set state='closed', closed_on=$1, cut_off=$2, carried_forward_g=$3, expired_g=$4 where id=$5`, [closedOn, cutOff, JSON.stringify(carried), JSON.stringify(expired), period]);
        await appendEntry(c, { act: 'period_closed', person: by, site: p.site, object: period,
            content: { period, closed_on: closedOn, cut_off: cutOff, carried_forward_g: carried, expired_g: expired } });
        return { status: 200, body: { period, state: 'closed', closed_on: closedOn, cut_off: cutOff, carried_forward_g: carried, expired_g: expired } };
    });
}
export async function openRestatement(params) {
    return withTransaction(async (c) => {
        const p = (await c.query(`select * from balance_periods where id = $1`, [params.period])).rows[0];
        if (!p)
            throw new HttpError(404, 'not_found');
        const ref = 'RST-' + crypto.randomUUID().slice(0, 6).toUpperCase();
        const certs = (await c.query(`select * from certificates where period = $1 order by signed_at`, [params.period])).rows;
        const affected = certs.map((cert) => cert.number);
        let contentMovements = null;
        if (params.factor_reference && params.new_factor_bp !== undefined) {
            contentMovements = [];
            for (const cert of certs) {
                const lot = (cert.lots ?? [])[0];
                const lotRow = (await c.query(`select * from lots where reference = $1`, [lot.reference])).rows[0];
                if (!lotRow)
                    continue;
                const attached = (await c.query(`select coalesce(sum(mass_g),0)::bigint as n from credit_movements where lot = $1 and kind='out'`, [lot.reference])).rows[0];
                const oldFactor = (await c.query(`select factor_bp from conversion_factors where reference = $1`, [params.factor_reference])).rows[0];
                const oldBp = oldFactor ? Number(oldFactor.factor_bp) : params.new_factor_bp;
                contentMovements.push({
                    certificate: cert.number,
                    content_bp: cert.content_bp,
                    corrected_content_bp: recomputeContentBp(Number(attached.n), oldBp, params.new_factor_bp, Number(lotRow.mass_g)),
                });
            }
        }
        await c.query(`insert into restatements(reference, period, reason, opened_by, affected_certificates, content_movements, factor_reference)
       values ($1,$2,$3,$4,$5,$6,$7)`, [ref, params.period, params.reason, params.by, JSON.stringify(affected), contentMovements ? JSON.stringify(contentMovements) : null, params.factor_reference ?? null]);
        await appendEntry(c, { act: 'restatement_opened', person: params.by, site: p.site, object: ref,
            content: { period: params.period, reason: params.reason, affected_certificates: affected, content_movements: contentMovements } });
        return {
            status: 201,
            body: {
                reference: ref, period: params.period, reason: params.reason,
                affected_certificates: affected, content_movements: contentMovements,
                resolutions: [],
            },
        };
    });
}
/** Recompute content under a revised factor: credit scales with the factor ratio, floored. */
export function recomputeContentBp(attachedCreditG, oldFactorBp, newFactorBp, lotMassG) {
    const correctedCredit = flMulDiv(attachedCreditG, newFactorBp, oldFactorBp);
    return flMulDiv(correctedCredit, 10000, lotMassG);
}
