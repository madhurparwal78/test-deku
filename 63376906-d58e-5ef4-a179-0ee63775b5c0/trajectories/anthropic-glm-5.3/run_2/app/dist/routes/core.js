import crypto from 'node:crypto';
import { Hono } from 'hono';
import { query } from '../lib/db.js';
import { login, bearer, getSession } from '../lib/auth.js';
import { HttpError, requireSession, idempotent, readBody, strField, refusePagination, assertNoDecimal } from '../lib/http.js';
import { collectorNameOn } from '../lib/claims.js';
import { sendMail } from '../lib/mail.js';
import { appendEntry } from '../lib/record.js';
import { withTransaction } from '../lib/db.js';
export const core = new Hono();
core.get('/health', (c) => c.json({ status: 'ok', ready: true, now: new Date().toISOString() }));
core.post('/auth/login', async (c) => {
    const body = await readBody(c);
    const email = strField(body.email, 'email');
    const password = strField(body.password, 'password');
    const s = await login(email, password);
    if (!s)
        throw new HttpError(401, 'invalid_credentials');
    const rows = await query(`select token, expires_at from sessions where email = $1 order by created_at desc limit 1`, [email]);
    return c.json({ access_token: rows[0].token, token_type: 'Bearer', expires_at: rows[0].expires_at, email: s.email, name: s.name });
});
core.get('/auth/me', async (c) => {
    const s = await requireSession(c);
    const grants = await query(`select site, role, valid_to from grants where email = $1 order by site`, [s.email]);
    return c.json({
        email: s.email, name: s.name, roles: s.roles, sites: s.sites,
        grants: grants.map((g) => ({ site: g.site, role: g.role, valid_to: g.valid_to })),
    });
});
core.get('/sites', async (c) => {
    const rows = await query(`select * from sites order by reference`);
    return c.json(rows.map(siteView));
});
core.get('/sites/:reference', async (c) => {
    const rows = await query(`select * from sites where reference = $1`, [c.req.param('reference')]);
    if (!rows.length)
        throw new HttpError(404, 'not_found');
    return c.json(siteView(rows[0]));
});
function siteView(s) {
    return {
        reference: s.reference, name: s.name, confidence: s.confidence,
        certification_state: s.certification_state,
        nameplate_kg: Number(s.nameplate_kg), contracted_kg: Number(s.contracted_kg),
        uncommitted_kg: Number(s.nameplate_kg) - Number(s.contracted_kg),
        capacity_basis: s.capacity_basis, last_revised: s.last_revised,
    };
}
core.get('/sites/:reference/capacity', async (c) => {
    const rows = await query(`select * from sites where reference = $1`, [c.req.param('reference')]);
    if (!rows.length)
        throw new HttpError(404, 'not_found');
    const s = rows[0];
    return c.json({
        site: s.reference, nameplate_kg: Number(s.nameplate_kg), basis: s.capacity_basis,
        contracted_kg: Number(s.contracted_kg),
        uncommitted_kg: Number(s.nameplate_kg) - Number(s.contracted_kg),
        confidence: s.confidence, last_revised: s.last_revised,
    });
});
core.get('/parties/:reference/versions', async (c) => {
    refusePagination(c);
    const ref = c.req.param('reference');
    const rows = await query(`select pv.*, p.kind, p.current_name from party_versions pv join parties p on p.reference = pv.party
      where pv.party = $1 order by pv.effective_from`, [ref]);
    if (!rows.length)
        throw new HttpError(404, 'not_found');
    return c.json(rows.map((r) => ({
        party: r.party, kind: r.kind, name: r.name, effective_from: r.effective_from,
        recorded_on: r.recorded_on, current_name: r.current_name,
    })));
});
core.post('/parties/:reference/versions', async (c) => {
    const s = await requireSession(c);
    if (s.roles.includes('auditor'))
        throw new HttpError(403, 'auditor_reads_only');
    const ref = c.req.param('reference');
    return idempotent(c, async () => {
        const body = await readBody(c);
        assertNoDecimal(body);
        const name = strField(body.name, 'name');
        const effectiveFrom = strField(body.effective_from, 'effective_from');
        const out = await withTransaction(async (cl) => {
            const dupe = await cl.query(`select 1 from party_versions where party = $1 and effective_from = $2`, [ref, effectiveFrom]);
            if (dupe.rows.length)
                throw new HttpError(409, 'version_exists', { party: ref, effective_from: effectiveFrom });
            await cl.query(`update party_versions set name = name where party = $1`, [ref]);
            const ins = await cl.query(`insert into party_versions(party, name, effective_from) values ($1,$2,$3) returning *`, [ref, name, effectiveFrom]);
            await appendEntry(cl, { act: 'party_version_recorded', person: s.email, object: ref,
                content: { party: ref, name, effective_from: effectiveFrom } });
            return ins.rows[0];
        });
        await query(`update parties set current_name = $2 where reference = $1`, [ref, name]);
        return { status: 201, body: { reference: `${ref}@${effectiveFrom}`, party: ref, name, effective_from: effectiveFrom } };
    }).then((r) => c.json(r.body, r.status));
});
core.get('/collectors', async (c) => {
    refusePagination(c);
    const s = await getSession(bearer(c.req.raw));
    const rows = await query(`select * from collectors order by reference`);
    const out = [];
    for (const col of rows) {
        out.push(await collectorView(col));
    }
    if (s && s.roles.includes('collector'))
        return c.json(out.filter((x) => x.reference === s.email));
    return c.json(out);
});
core.get('/collectors/:reference', async (c) => {
    const rows = await query(`select * from collectors where reference = $1`, [c.req.param('reference')]);
    if (!rows.length)
        throw new HttpError(404, 'not_found');
    return c.json(await collectorView(rows[0]));
});
async function collectorView(col) {
    const periods = await query(`select * from approval_periods where collector = $1 order by valid_from`, [col.reference]);
    const findings = await query(`select * from findings where collector = $1 order by recorded_on desc`, [col.reference]);
    const today = new Date().toISOString().slice(0, 10);
    return {
        reference: col.reference, name: await collectorNameOn(col.reference, today), country: col.country,
        registration: col.registration, registration_expiry: col.registration_expiry,
        site_types: col.site_types, streams: col.streams, scheme_status: col.scheme_status,
        findings: findings.map((f) => ({ reference: 'FND-' + String(f.reference).padStart(4, '0'), kind: f.kind, detail: f.detail, state: f.state, recorded_on: f.recorded_on })),
        approval_periods: periods.map((p) => ({
            state: p.state, valid_from: p.valid_from, valid_to: p.valid_to,
            condition: p.condition ?? null, condition_closes_on: p.condition_closes_on ?? null,
            // A grant inside fourteen days of its expiry is reported as expiring.
            expiring: daysUntil(today, p.valid_to) <= 14 && daysUntil(today, p.valid_to) >= 0,
        })),
    };
}
function daysUntil(from, to) {
    return Math.round((new Date(to + 'T00:00:00Z').getTime() - new Date(from + 'T00:00:00Z').getTime()) / 86400000);
}
core.post('/collectors/:reference/approvals', async (c) => {
    const s = await requireSession(c);
    if (!s.roles.includes('quality_manager'))
        throw new HttpError(403, 'quality_manager_required');
    return idempotent(c, async () => {
        const body = await readBody(c);
        assertNoDecimal(body);
        const state = strField(body.state, 'state', ['approved', 'conditional', 'suspended', 'lapsed']);
        const validFrom = strField(body.valid_from, 'valid_from');
        const validTo = strField(body.valid_to, 'valid_to');
        const ref = c.req.param('reference');
        const out = await withTransaction(async (cl) => {
            const col = await cl.query(`select * from collectors where reference = $1`, [ref]);
            if (!col.rows.length)
                throw new HttpError(404, 'not_found');
            const ins = await cl.query(`insert into approval_periods(collector, state, valid_from, valid_to, condition, condition_closes_on)
         values ($1,$2,$3,$4,$5,$6) returning reference`, [ref, state, validFrom, validTo, body.condition ?? null, body.condition_closes_on ?? null]);
            await appendEntry(cl, { act: 'collector_approval_recorded', person: s.email, object: ref,
                content: { collector: ref, state, valid_from: validFrom, valid_to: validTo } });
            return ins.rows[0];
        });
        return { status: 201, body: { reference: 'APR-' + String(out.reference).padStart(4, '0'), collector: ref, state, valid_from: validFrom, valid_to: validTo } };
    }).then((r) => c.json(r.body, r.status));
});
// ---- public site content ----
core.get('/statistics', async (c) => c.json(await query(`select key, value, source, year, geography from statistics order by key`)));
core.get('/positions', async (c) => {
    const rows = await query(`select * from positions order by closes_on`);
    return c.json(rows.map((p) => ({
        reference: 'POS-' + String(p.reference).padStart(4, '0'), title: p.title, location: p.location,
        department: p.department, contract_type: p.contract_type, closes_on: p.closes_on,
    })));
});
core.get('/news', async (c) => {
    const rows = await query(`select * from news_items order by dated_on desc`);
    return c.json(rows.map((n) => ({
        reference: 'NEWS-' + String(n.reference).padStart(4, '0'), title: n.title, tag: n.tag,
        dated_on: n.dated_on, outlet: n.outlet, link: n.link, language: n.language, coverage: n.coverage,
    })));
});
core.get('/claim-register', async (c) => {
    const rows = await query(`select * from claim_substantiation order by first_published_on`);
    const today = new Date().toISOString().slice(0, 10);
    return c.json(rows.map((r) => ({
        reference: 'CLM-' + String(r.reference).padStart(4, '0'), claim: r.claim, route: r.route,
        first_published_on: r.first_published_on, evidence: r.evidence, method_version: r.method_version,
        approver: r.approver, review_on: r.review_on,
        evidence_expiring_before_review: evidenceExpiring(r.evidence, r.review_on),
        withdrawn_on: r.withdrawn_on ?? null,
    })));
});
const ENQUIRY_DESTINATIONS = {
    waste_supply: { destination: 'feedstock@example.com', response_days: 3 },
    polymer_purchase: { destination: 'sales@example.com', response_days: 2 },
    partnership: { destination: 'partners@example.com', response_days: 5 },
    press: { destination: 'press@example.com', response_days: 1 },
};
function evidenceExpiring(evidence, reviewOn) {
    if (!evidence || !reviewOn)
        return false;
    const until = evidence.valid_to ?? evidence.expires_on ?? null;
    return !!until && until < reviewOn;
}
core.post('/enquiries', async (c) => {
    return idempotent(c, async () => {
        const body = await readBody(c);
        const type = strField(body.type, 'type', Object.keys(ENQUIRY_DESTINATIONS));
        const name = strField(body.name, 'name');
        const email = strField(body.email, 'email');
        const message = strField(body.message, 'message');
        const dest = ENQUIRY_DESTINATIONS[type];
        const ref = 'ENQ-' + crypto.randomUUID().slice(0, 6).toUpperCase();
        await withTransaction(async (cl) => {
            await cl.query(`insert into enquiries(reference, type, name, email, message, destination, response_days)
         values ($1,$2,$3,$4,$5,$6,$7)`, [ref, type, name, email, message, dest.destination, dest.response_days]);
            if (type === 'waste_supply') {
                await cl.query(`insert into collectors(reference, name, country, registration, registration_expiry, scheme_status)
           values ($1,$2,$3,$4,$5,'unassessed') on conflict do nothing`, ['COL-' + ref.slice(4), name, body.country ?? 'XX', 'pending', '2999-12-31']);
            }
            if (type === 'polymer_purchase') {
                await cl.query(`insert into conformances(customer, specification, spec_version, application, outcome)
           values ($1, 'SPEC-N6', 3, 'pending assessment', 'pending')`, ['CUS-PENDING-' + ref]);
            }
            await appendEntry(cl, { act: 'enquiry_received', person: email, object: ref,
                content: { reference: ref, type, destination: dest.destination, response_days: dest.response_days } });
        });
        await sendMail(email, `Enquiry ${ref} received`, `Enquiry ${ref} received\n\nReference: ${ref}\nDestination: ${dest.destination}\nStated response time: ${dest.response_days} working days\n\n` +
            `Who receives this data: ${dest.destination}. Purpose: to answer your enquiry and, where you asked for it, to open a record. ` +
            `Retention: ${type === 'waste_supply' ? 36 : type === 'polymer_purchase' ? 36 : type === 'press' ? 12 : 24} months. ` +
            `To have it removed: privacy@example.com.\n`);
        return { status: 201, body: { reference: ref, destination: dest.destination, response_days: dest.response_days, deadline: type === 'press' ? body.deadline ?? null : null } };
    }).then((r) => c.json(r.body, r.status));
});
core.post('/sites/:reference/certification', async (c) => {
    const s = await requireSession(c);
    if (!s.roles.includes('quality_manager'))
        throw new HttpError(403, 'quality_manager_required');
    const ref = c.req.param('reference');
    return idempotent(c, async () => {
        const body = await readBody(c);
        const state = strField(body.state, 'state', ['certified', 'suspended', 'not_certified']);
        const effectiveFrom = strField(body.effective_from, 'effective_from');
        const validTo = body.valid_to ?? null;
        const out = await withTransaction(async (cl) => {
            const ins = await cl.query(`insert into site_certifications(site, state, valid_from, valid_to, effective_from, grade)
         values ($1,$2,$3,$4,$5,$6) returning reference`, [ref, state, effectiveFrom, validTo, effectiveFrom, body.grade ?? null]);
            let certs = [];
            if (state === 'suspended') {
                const rows = await cl.query(`select * from certificates where site = $1 and signed_at::date >= $2 and state = 'issued' order by signed_at`, [ref, effectiveFrom]);
                certs = rows.rows.map((r) => ({ number: r.number, state: r.state, resolution: null }));
            }
            await cl.query(`update sites set certification_state = $2 where reference = $1`, [ref, state === 'certified' ? 'certified' : 'not_certified']);
            await appendEntry(cl, { act: 'site_certification_recorded', person: s.email, site: ref, object: ref,
                content: { site: ref, state, effective_from: effectiveFrom, valid_to: validTo, certificates_in_window: certs } });
            return { reference: ins.rows[0].reference, certs };
        });
        return { status: 201, body: { reference: 'CRT-' + String(out.reference).padStart(4, '0'), site: ref, state, effective_from: effectiveFrom, valid_to: validTo, certificates_in_window: out.certs } };
    }).then((r) => c.json(r.body, r.status));
});
core.get('/sites/:reference/certification', async (c) => {
    const rows = await query(`select * from site_certifications where site = $1 order by effective_from`, [c.req.param('reference')]);
    return c.json(rows.map((r) => ({
        reference: 'CRT-' + String(r.reference).padStart(4, '0'), site: r.site, state: r.state,
        valid_from: r.valid_from, valid_to: r.valid_to, effective_from: r.effective_from, lifted_on: r.lifted_on,
    })));
});
