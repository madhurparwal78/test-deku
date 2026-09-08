import crypto from 'node:crypto';
import { Hono } from 'hono';
import { query, withTransaction } from '../lib/db.js';
import { HttpError, requireSession, idempotent, readBody, strField, intField, refusePagination } from '../lib/http.js';
import { appendEntry } from '../lib/record.js';
import { flMulDiv } from '../lib/num.js';
import { sendMail } from '../lib/mail.js';

export const commercial = new Hono();

commercial.get('/specifications/:grade/versions/:version', async (c) => {
  const rows = (await query<any>(
    `select * from specifications where grade = $1 and version = $2`,
    [c.req.param('grade'), Number(c.req.param('version'))]));
  if (!rows.length) throw new HttpError(404, 'not_found');
  const s = rows[0];
  return c.json({
    grade: s.grade, version: s.version, state: s.state, issued_on: s.issued_on,
    rows: s.rows, virgin_reference: s.virgin_reference,
    derivation: { note: 'A guaranteed limit is tested on every lot.' },
  });
});

commercial.get('/specifications', async (c) => {
  const rows = await query<any>(`select * from specifications order by grade, version desc`);
  return c.json(rows.map((s) => ({
    grade: s.grade, version: s.version, state: s.state, issued_on: s.issued_on,
    rows: s.rows, virgin_reference: s.virgin_reference,
  })));
});

commercial.post('/specifications/:grade/versions/:version/issue', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const customer = strField(body.customer, 'customer');
    const spec = (await query<any>(
      `select * from specifications where grade = $1 and version = $2`,
      [c.req.param('grade'), Number(c.req.param('version'))]))[0];
    if (!spec) throw new HttpError(404, 'not_found');
    const cust = (await query<any>(`select * from customers where reference = $1`, [customer]))[0];
    if (!cust) throw new HttpError(404, 'customer_not_found');
    const ref = 'SPEC-ISS-' + crypto.randomUUID().slice(0, 6).toUpperCase();
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into conformances(customer, specification, spec_version, application, outcome)
         values ($1,$2,$3,$4,'issued')`,
        [customer, spec.grade, spec.version, cust.application]);
      await appendEntry(cl, { act: 'specification_issued', person: s.email, object: ref,
        content: { reference: ref, specification: `${spec.grade} v${spec.version}`, customer } });
    });
    return { status: 201, body: { reference: ref, specification: `${spec.grade} v${spec.version}`, customer, issued_to: cust.name } };
  }).then((r) => c.json(r.body, r.status as any));
});

commercial.get('/customers', async (c) => {
  const rows = await query<any>(`select * from customers order by reference`);
  const conf = await query<any>(`select * from conformances`);
  return c.json(rows.map((x) => ({
    reference: x.reference, name: x.name, contact: x.contact, application: x.application,
    industry: x.industry, holds_specification_version: x.holds,
    conformance: conf.filter((cf) => cf.customer === x.reference).map((cf) => ({
      specification: cf.specification, specification_version: cf.spec_version,
      application: cf.application, trials: cf.trials, outcome: cf.outcome, opened_on: cf.opened_on,
    })),
  })));
});

commercial.get('/customers/:reference', async (c) => {
  const x = (await query<any>(`select * from customers where reference = $1`, [c.req.param('reference')]))[0];
  if (!x) throw new HttpError(404, 'not_found');
  const conf = await query<any>(`select * from conformances where customer = $1`, [x.reference]);
  return c.json({
    reference: x.reference, name: x.name, contact: x.contact, application: x.application,
    industry: x.industry, holds_specification_version: x.holds,
    conformance: conf.map((cf) => ({
      specification: cf.specification, specification_version: cf.spec_version,
      application: cf.application, trials: cf.trials, outcome: cf.outcome, opened_on: cf.opened_on,
    })),
  });
});

commercial.get('/change-notices', async (c) => {
  const rows = await query<any>(`select * from change_notices order by proposed_on desc`);
  return c.json(rows.map(changeNoticeView));
});

function changeNoticeView(n: any) {
  return {
    reference: n.reference, description: n.description,
    specifications_affected: n.specifications_affected, customers_affected: n.customers_affected,
    qualifications_affected: n.qualifications_affected, notice_period_days: n.notice_period_days,
    proposed_on: n.proposed_on, released_on: n.released_on ?? null, raised_by: n.raised_by,
    qualification_relevant: n.qualification_relevant,
    notifications: n.notifications,
    blocked: n.qualification_relevant && n.notifications.some((x: any) => !x.acknowledged && !x.waived),
  };
}

commercial.post('/change-notices', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.some((r) => ['quality_manager', 'claims_manager'].includes(r))) throw new HttpError(403, 'forbidden');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const description = strField(body.description, 'description');
    const customers = await query<any>(`select * from customers`);
    const specs = await query<any>(`select * from specifications where state = 'current'`);
    // Derive rather than assert who is affected.
    const specAffected = (body.specifications ?? specs.map((x) => `${x.grade} v${x.version}`));
    const qualificationRelevant = !!body.qualification_relevant;
    const customersAffected = qualificationRelevant
      ? customers.filter((x) => x.industry === 'automotive').map((x) => x.reference)
      : customers.map((x) => x.reference);
    const ref = `CHG-${String((await query<any>(`select count(*)::int as n from change_notices`))[0].n + 1).padStart(4, '0')}`;
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into change_notices(reference, description, specifications_affected, customers_affected,
            qualifications_affected, notice_period_days, raised_by, qualification_relevant, notifications)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9)`,
        [ref, description, JSON.stringify(specAffected), JSON.stringify(customersAffected),
         JSON.stringify(customersAffected), body.notice_period_days ?? 30, s.email, qualificationRelevant,
         JSON.stringify(customersAffected.map((cu: string) => ({ customer: cu, notified: false, acknowledged: false, waived: false })))]);
      await appendEntry(cl, { act: 'change_notice_raised', person: s.email, object: ref,
        content: { reference: ref, description, specifications_affected: specAffected, customers_affected: customersAffected } });
    });
    return { status: 201, body: { reference: ref, ...{ specifications_affected: specAffected, customers_affected: customersAffected, qualifications_affected: customersAffected, notice_period_days: body.notice_period_days ?? 30 } } };
  }).then((r) => c.json(r.body, r.status as any));
});

commercial.post('/change-notices/:reference/notify', async (c) => {
  const s = await requireSession(c);
  return idempotent(c, async () => {
    const body = await readBody(c);
    const customer = strField(body.customer, 'customer');
    const notice = (await query<any>(`select * from change_notices where reference = $1`, [c.req.param('reference')]))[0];
    if (!notice) throw new HttpError(404, 'not_found');
    const cust = (await query<any>(`select * from customers where reference = $1`, [customer]))[0];
    if (!cust) throw new HttpError(404, 'customer_not_found');
    const notifications = (notice.notifications ?? []).map((n: any) =>
      n.customer === customer ? { ...n, notified: true, notified_on: new Date().toISOString().slice(0, 10) } : n);
    await withTransaction(async (cl) => {
      await cl.query(`update change_notices set notifications = $2 where reference = $1`, [notice.reference, JSON.stringify(notifications)]);
      await appendEntry(cl, { act: 'change_notice_notified', person: s.email, object: notice.reference,
        content: { reference: notice.reference, customer } });
    });
    await sendMail(cust.contact, `Change notice ${notice.reference} requires acknowledgement`,
      `Change notice ${notice.reference} requires acknowledgement\n\n` +
      `The change: ${notice.description}\n` +
      `Specifications affected: ${(notice.specifications_affected ?? []).join(', ')}\n` +
      `Notice period: ${notice.notice_period_days} days\n`).catch(() => null);
    return { status: 200, body: { reference: notice.reference, customer, notified: true } };
  }).then((r) => c.json(r.body, r.status as any));
});

commercial.post('/change-notices/:reference/acknowledge', async (c) => {
  const s = await requireSession(c);
  return idempotent(c, async () => {
    const body = await readBody(c);
    const customer = strField(body.customer, 'customer');
    const waived = !!body.waived;
    const notice = (await query<any>(`select * from change_notices where reference = $1`, [c.req.param('reference')]))[0];
    if (!notice) throw new HttpError(404, 'not_found');
    const notifications = (notice.notifications ?? []).map((n: any) =>
      n.customer === customer ? { ...n, acknowledged: !waived, waived, acknowledged_on: new Date().toISOString().slice(0, 10) } : n);
    await withTransaction(async (cl) => {
      await cl.query(`update change_notices set notifications = $2 where reference = $1`, [notice.reference, JSON.stringify(notifications)]);
      await appendEntry(cl, { act: 'change_notice_acknowledged', person: s.email, object: notice.reference,
        content: { reference: notice.reference, customer, waived } });
    });
    return { status: 200, body: { reference: notice.reference, customer, acknowledged: !waived, waived } };
  }).then((r) => c.json(r.body, r.status as any));
});

commercial.post('/change-notices/:reference/release', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  return idempotent(c, async () => {
    const notice = (await query<any>(`select * from change_notices where reference = $1`, [c.req.param('reference')]))[0];
    if (!notice) throw new HttpError(404, 'not_found');
    if (notice.released_on) throw new HttpError(409, 'already_released');
    const owed = (notice.notifications ?? []).filter((n: any) => !n.notified && !n.waived);
    if (owed.length) {
      throw new HttpError(409, 'customers_owed_notice', {
        customers: owed.map((n: any) => n.customer),
        rule: 'Every customer owed notice must be notified or have waived it in a recorded act.',
      });
    }
    const unacknowledged = (notice.notifications ?? []).filter((n: any) => !n.acknowledged && !n.waived);
    if (notice.qualification_relevant && unacknowledged.length) {
      throw new HttpError(409, 'qualification_relevant_blocks_release', {
        customers: unacknowledged.map((n: any) => n.customer),
        rule: 'A change touching a qualification-relevant parameter for an automotive customer blocks rather than warns.',
      });
    }
    await withTransaction(async (cl) => {
      await cl.query(`update change_notices set released_on = current_date where reference = $1`, [notice.reference]);
      await appendEntry(cl, { act: 'change_notice_released', person: s.email, object: notice.reference,
        content: { reference: notice.reference } });
    });
    return { status: 200, body: { reference: notice.reference, released_on: new Date().toISOString().slice(0, 10) } };
  }).then((r) => c.json(r.body, r.status as any));
});

// ---------------- contracts ----------------
commercial.get('/contracts', async (c) => {
  const rows = await query<any>(`select * from contracts order by id`);
  const out = [];
  for (const r of rows) out.push(await contractView(r));
  return c.json(out);
});

commercial.get('/contracts/:id/projection', async (c) => {
  const row = (await query<any>(`select * from contracts where id = $1`, [c.req.param('id')]))[0];
  if (!row) throw new HttpError(404, 'not_found');
  return c.json(await contractView(row));
});

async function contractView(ct: any) {
  const site = (await query<any>(`select * from sites where reference = $1`, [ct.site]))[0];
  const allocations = await query<any>(`select * from allocations where contract = $1 order by allocated_on`, [ct.id]);
  const deliveredKg = allocations.reduce((s: number, a: any) => s + Math.floor(Number(a.mass_g) / 1000), 0);
  const committedKg = Number(ct.committed_kg);
  const runningContentBp = allocations.length
    ? flMulDiv(allocations.reduce((s: number, a: any) => s + Number(a.mass_g), 0) * 10000, 1, 1)
    : 0;
  // Running weighted content across allocated lots.
  let weighted = 0, totalG = 0;
  for (const a of allocations) {
    const lot = (await query<any>(`select * from lots where reference = $1`, [a.lot]))[0];
    if (!lot) continue;
    const attached = await query<any>(
      `select coalesce(sum(mass_g),0)::bigint as n from credit_movements where lot = $1 and kind='out'`, [a.lot]);
    weighted += flMulDiv(Number(attached[0].n), 10000, Number(lot.mass_g)) * Number(a.mass_g);
    totalG += Number(a.mass_g);
  }
  const runningBp = totalG > 0 ? flMulDiv(weighted, 1, totalG) : 0;
  const floorBp = Number(ct.floor_bp);
  const remainingKg = Math.max(0, committedKg - deliveredKg);
  const requiredRemainingBp = remainingKg > 0
    ? Math.max(0, flMulDiv(floorBp * committedKg * 1000 - runningBp * deliveredKg * 1000, 1, remainingKg * 1000))
    : floorBp;
  const unreachable = runningBp < floorBp && requiredRemainingBp > 10000;
  return {
    id: ct.id, customer: ct.customer, site: ct.site, period: ct.period,
    delivered_kg: deliveredKg, committed_kg: committedKg,
    running_content_bp: runningBp || runningContentBp && 0, floor_bp: floorBp,
    required_remaining_bp: requiredRemainingBp,
    state: unreachable ? 'unreachable' : 'on_track',
    unreachable_on: unreachable ? ct.unreachable_on ?? new Date().toISOString().slice(0, 10) : null,
    allocation_that_made_it_so: allocations.at(-1)?.reference ?? null,
    planned_site_flag: site?.confidence === 'planned',
    flag_dismissible: false,
    shortfall_consequence: ct.shortfall_consequence,
    allocations: allocations.map((a) => ({
      reference: 'ALLOC-' + String(a.reference).padStart(4, '0'), lot: a.lot, mass_g: Number(a.mass_g),
      decided_by: a.decided_by, favoured_over: a.favoured_over, allocated_on: a.allocated_on,
    })),
    derivation: {
      delivered_kg: 'sum of allocated lots, in whole kilograms',
      required_remaining_bp: 'the average the remaining volume must reach for the floor to hold',
    },
  };
}

commercial.post('/contracts/:id/allocations', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('claims_manager')) throw new HttpError(403, 'claims_manager_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const lot = strField(body.lot, 'lot');
    const massG = intField(body.mass_g, 'mass_g', { min: 1 });
    const decidedBy = strField(body.decided_by ?? s.email, 'decided_by');
    const favouredOver = Array.isArray(body.favoured_over) ? body.favoured_over : [];
    const ct = (await query<any>(`select * from contracts where id = $1`, [c.req.param('id')]))[0];
    if (!ct) throw new HttpError(404, 'not_found');
    const existing = (await query<any>(
      `select 1 from allocations a join contracts c2 on c2.id = a.contract where a.lot = $1 and c2.customer = (select customer from contracts where id = $2)`,
      [lot, ct.id])).length > 0;
    if (existing) throw new HttpError(409, 'lot_already_allocated', { lot });
    const ref = (await query<any>(`select count(*)::int as n from allocations`))[0].n + 1;
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into allocations(contract, lot, mass_g, decided_by, favoured_over) values ($1,$2,$3,$4,$5)`,
        [ct.id, lot, massG, decidedBy, JSON.stringify(favouredOver)]);
      await appendEntry(cl, { act: 'contract_allocation', person: s.email, site: ct.site, object: ct.id,
        content: { contract: ct.id, lot, mass_g: massG, decided_by: decidedBy, favoured_over: favouredOver } });
    });
    return {
      status: 201,
      body: {
        reference: 'ALLOC-' + String(ref).padStart(4, '0'), contract: ct.id, lot, mass_g: massG,
        decided_by: decidedBy, favoured_over: favouredOver,
      },
    };
  }).then((r) => c.json(r.body, r.status as any));
});

// ---------------- inbound ----------------
const SOURCES = ['weighbridge', 'control_system', 'laboratory', 'customer_reporting'];

commercial.post('/inbound/:source', async (c) => {
  await requireSession(c);
  const source = c.req.param('source');
  if (!SOURCES.includes(source)) throw new HttpError(400, 'unknown_source', { sources: SOURCES });
  return idempotent(c, async () => {
    const raw = await c.req.raw.clone().text();
    let body: any;
    try { body = JSON.parse(raw); } catch { throw new HttpError(400, 'invalid_json'); }
    const ref = 'INB-' + crypto.randomUUID().slice(0, 8).toUpperCase();
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into inbound_records(reference, source, received_at, payload_verbatim, payload) values ($1,$2,$3,$4,$5)`,
        [ref, source, body.received_at ?? new Date().toISOString(), raw, JSON.stringify(body.payload ?? body)]);
      await appendEntry(cl, { act: 'inbound_record_stored', person: 'system:' + source, object: ref,
        content: { reference: ref, source, bytes: raw.length } });
    });
    return { status: 201, body: { reference: ref, source, received_at: body.received_at ?? new Date().toISOString() } };
  }).then((r) => c.json(r.body, r.status as any));
});

commercial.get('/inbound', async (c) => {
  refusePagination(c);
  const rows = await query<any>(`select * from inbound_records order by received_at`);
  return c.json(rows.map((r) => ({
    reference: r.reference, source: r.source, received_at: r.received_at,
    payload_verbatim: r.payload_verbatim, payload: r.payload,
  })));
});
