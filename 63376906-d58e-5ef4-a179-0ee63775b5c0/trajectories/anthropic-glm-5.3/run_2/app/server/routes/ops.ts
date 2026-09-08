import crypto from 'node:crypto';
import { Hono } from 'hono';
import { query, withTransaction } from '../lib/db.js';
import { HttpError, requireSession, idempotent, readBody, strField, intField, dateField, refusePagination, assertNoDecimal } from '../lib/http.js';
import { batchView, decorateBatch, dryMass, missingCustody, genealogy, batchImpact, lotInheritedFlags } from '../lib/claims.js';
import { appendEntry } from '../lib/record.js';
import { flMulDiv } from '../lib/num.js';
import { periodForLot } from '../lib/certs.js';

export const ops = new Hono();

const WRITES = ['plant_operator', 'quality_manager', 'claims_manager', 'lab_analyst', 'certificate_signer'];

// ---------------- batches ----------------
ops.get('/batches', async (c) => {
  refusePagination(c);
  const rows = await query<any>(
    `select b.*, d.calibrated_on from batches b join devices d on d.reference = b.device order by b.received_on, b.reference`);
  const out = [];
  for (const r of rows) out.push(await decorateBatch(r));
  return c.json(out);
});

ops.get('/batches/:reference', async (c) => {
  const v = await batchView(c.req.param('reference'));
  if (!v) throw new HttpError(404, 'not_found');
  return c.json(v);
});

ops.post('/batches', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.some((r) => ['plant_operator', 'quality_manager'].includes(r))) {
    throw new HttpError(403, 'plant_operator_required');
  }
  return idempotent(c, async () => {
    const body = await readBody(c);
    assertNoDecimal(body);
    const collector = strField(body.collector, 'collector');
    const site = strField(body.site, 'site');
    const category = strField(body.category, 'category', ['post_consumer', 'pre_consumer', 'industrial', 'ocean']);
    const grossG = intField(body.gross_g, 'gross_g', { min: 0 });
    const tareG = intField(body.tare_g, 'tare_g', { min: 0 });
    const netG = intField(body.net_g, 'net_g', { min: 0 });
    const moistureBp = intField(body.moisture_bp, 'moisture_bp', { min: 0, max: 10000 });
    const moistureMethod = strField(body.moisture_method, 'moisture_method');
    const device = strField(body.device, 'device');
    const receivedOn = dateField(body.received_on, 'received_on');
    if (grossG - tareG !== netG) throw new HttpError(400, 'mass_does_not_reconcile', { gross_g: grossG, tare_g: tareG, net_g: netG });
    const composition = Array.isArray(body.composition) ? body.composition : [];
    for (const comp of composition) {
      strField(comp.polymer, 'composition.polymer');
      intField(comp.fraction_bp, 'composition.fraction_bp', { min: 0, max: 10000 });
      strField(comp.basis, 'composition.basis', ['declared', 'sampled', 'assayed']);
    }
    const contamination = body.contamination ?? {};
    const custody = Array.isArray(body.custody) ? body.custody : [];
    for (const l of custody) strField(l.kind, 'custody.kind', ['collection_site', 'collector', 'transport', 'arrival', 'weighing', 'acceptance']);
    const ref = await nextBatchRef();
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into batches(reference, collector, site, grade, category, gross_g, tare_g, net_g, moisture_bp,
            moisture_method, device, received_on, composition, contamination, collector_name_snapshot)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)`,
        [ref, collector, site, body.grade ?? 'N6', category, grossG, tareG, netG, moistureBp, moistureMethod,
         device, receivedOn, JSON.stringify(composition), JSON.stringify(contamination),
         (await query<any>(`select name from collectors where reference=$1`, [collector]))[0]?.name ?? collector]);
      let pos = 0;
      for (const l of custody) {
        await cl.query(
          `insert into custody_links(batch, kind, occurred_on, party, position) values ($1,$2,$3,$4,$5)`,
          [ref, l.kind, dateField(l.date ?? l.occurred_on, 'custody.date'), strField(l.party, 'custody.party'), pos++]);
      }
      await appendEntry(cl, { act: 'batch_booked', person: s.email, site, object: ref,
        content: { reference: ref, collector, category, net_g: netG, moisture_bp: moistureBp, received_on: receivedOn, device } });
    });
    const v = await batchView(ref);
    return { status: 201, body: v };
  }).then((r) => c.json(r.body, r.status as any));
});

async function nextBatchRef(): Promise<string> {
  const r = await query<any>(`select count(*)::int as n from batches`);
  return `BATCH-${1001 + r[0].n}`;
}

ops.patch('/batches/:reference', async (c) => {
  const s = await requireSession(c);
  const ref = c.req.param('reference');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const row = (await query<any>(`select * from batches where reference = $1`, [ref]))[0];
    if (!row) throw new HttpError(404, 'not_found');
    if (body.category && body.category !== row.category) {
      throw new HttpError(409, 'category_immutable', {
        rule: 'A batch category cannot be changed after acceptance, by anybody, through any route.',
      });
    }
    const allowed = ['contamination', 'composition', 'annotation'];
    const keys = Object.keys(body).filter((k) => allowed.includes(k));
    if (!keys.length) throw new HttpError(400, 'no_writable_field', { writable: allowed });
    await withTransaction(async (cl) => {
      for (const k of keys) {
        await cl.query(`update batches set ${k} = $2 where reference = $1`, [ref, JSON.stringify(body[k])]);
      }
      await appendEntry(cl, { act: 'batch_amended', person: s.email, site: row.site, object: ref, content: body });
    });
    return { status: 200, body: await batchView(ref) };
  }).then((r) => c.json(r.body, r.status as any));
});

ops.post('/batches/:reference/reject', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('plant_operator')) throw new HttpError(403, 'plant_operator_required');
  const ref = c.req.param('reference');
  return idempotent(c, async () => {
    const body = await readBody(c);
    assertNoDecimal(body);
    const rejectedG = intField(body.rejected_g, 'rejected_g', { min: 0 });
    const reason = strField(body.reason, 'reason');
    const destination = strField(body.destination, 'destination');
    const row = (await query<any>(`select * from batches where reference = $1`, [ref]))[0];
    if (!row) throw new HttpError(404, 'not_found');
    const delivered = Number(row.net_g);
    const priorRejected = row.rejected_g === null ? 0 : Number(row.rejected_g);
    const acceptedG = delivered - rejectedG - priorRejected;
    if (acceptedG < 0 || acceptedG + rejectedG + priorRejected !== delivered) {
      throw new HttpError(400, 'rejection_does_not_sum', { delivered_g: delivered, accepted_g: acceptedG, rejected_g: rejectedG + priorRejected });
    }
    await withTransaction(async (cl) => {
      await cl.query(`update batches set accepted_g=$2, rejected_g=$3, rejected_destination=$4, rejected_reason=$5 where reference=$1`,
        [ref, acceptedG, rejectedG + priorRejected, destination, reason]);
      await appendEntry(cl, { act: 'batch_rejected', person: s.email, site: row.site, object: ref,
        content: { reference: ref, rejected_g: rejectedG, reason, destination, accepted_g: acceptedG } });
    });
    return { status: 200, body: await batchView(ref) };
  }).then((r) => c.json(r.body, r.status as any));
});

ops.post('/batches/:reference/custody', async (c) => {
  const s = await requireSession(c);
  const ref = c.req.param('reference');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const kind = strField(body.kind, 'kind', ['collection_site', 'collector', 'transport', 'arrival', 'weighing', 'acceptance']);
    const arrivedOn = dateField(body.arrived_on, 'arrived_on');
    const row = (await query<any>(`select * from batches where reference = $1`, [ref]))[0];
    if (!row) throw new HttpError(404, 'not_found');
    await withTransaction(async (cl) => {
      const pos = await cl.query(`select coalesce(max(position),0)+1 as p from custody_links where batch=$1`, [ref]);
      await cl.query(
        `insert into custody_links(batch, kind, occurred_on, party, position, late_document, arrived_on)
         values ($1,$2,$3,$4,$5,true,$6)`,
        [ref, kind, dateField(body.occurred_on ?? body.date ?? row.received_on, 'occurred_on'), strField(body.party, 'party'), pos.rows[0].p, arrivedOn]);
      await cl.query(`update batches set claimable_from=$2 where reference=$1`, [ref, arrivedOn]);
      await appendEntry(cl, { act: 'custody_late_document_attached', person: s.email, site: row.site, object: ref,
        content: { reference: ref, kind, arrived_on: arrivedOn } });
    });
    return { status: 200, body: await batchView(ref) };
  }).then((r) => c.json(r.body, r.status as any));
});

ops.get('/batches/:reference/impact', async (c) => {
  refusePagination(c);
  const out = await batchImpact(c.req.param('reference'));
  if (!out.lots.length && !out.certificates.length) {
    const exists = await query<any>(`select 1 from batches where reference=$1`, [c.req.param('reference')]);
    if (!exists.length) throw new HttpError(404, 'not_found');
  }
  return c.json(out);
});

// ---------------- runs ----------------
const RECIPES: Record<string, any> = {
  'RCP-DISS-2': { run_type: 'dissolution', set_points: { temperature_c: [160, 170], pressure_bar: [2, 4], residence_min: 90 }, reagents: [{ name: 'methanol', ratio_bp: 1200 }], released_by: 'quality@example.com' },
  'RCP-DEPO-4': { run_type: 'depolymerisation', set_points: { temperature_c: [240, 260], pressure_bar: [8, 12], residence_min: 180 }, reagents: [{ name: 'sodium hydroxide', ratio_bp: 800 }], released_by: 'quality@example.com' },
  'RCP-PURI-1': { run_type: 'purification', set_points: { temperature_c: [180, 195], pressure_bar: [4, 6], residence_min: 120 }, reagents: [{ name: 'activated carbon', ratio_bp: 300 }], released_by: 'quality@example.com' },
  'RCP-REPO-3': { run_type: 'repolymerisation', set_points: { temperature_c: [250, 270], pressure_bar: [1, 3], residence_min: 240 }, reagents: [{ name: 'caprolactam catalyst', ratio_bp: 150 }], released_by: 'quality@example.com' },
};

ops.get('/runs', async (c) => {
  refusePagination(c);
  const runs = await query<any>(`select * from runs order by started_at, reference`);
  const cons = await query<any>(`select * from consumptions`);
  const outs = await query<any>(`select * from outputs`);
  return c.json(runs.map((r) => {
    const inputs = cons.filter((x) => x.run === r.reference);
    const outputs = outs.filter((x) => x.run === r.reference);
    const massIn = inputs.reduce((s: number, x: any) => s + Number(x.mass_g), 0);
    const massOut = outputs.reduce((s: number, x: any) => s + Number(x.mass_g), 0);
    return {
      reference: r.reference, run_type: r.run_type, site: r.site, grade: r.grade, equipment: r.equipment,
      recipe_version: r.recipe_version, operator: r.operator, started_at: r.started_at, closed_at: r.closed_at,
      state: r.state, losses_g: r.losses_g === null ? null : Number(r.losses_g),
      mass_in_g: massIn, mass_out_g: massOut,
      within_tolerance: r.within_tolerance ?? null, set_points: r.set_points ?? null,
      inputs: inputs.map((x) => ({ reference: x.input_reference, kind: x.input_kind, mass_g: Number(x.mass_g) })),
      outputs: outputs.map((x) => ({ reference: x.reference, kind: x.kind, mass_g: Number(x.mass_g), disposition: x.disposition ?? null })),
      stage: r.run_type,
    };
  }));
});

ops.get('/runs/:reference', async (c) => {
  const r = (await query<any>(`select * from runs where reference = $1`, [c.req.param('reference')]))[0];
  if (!r) throw new HttpError(404, 'not_found');
  const cons = await query<any>(`select * from consumptions where run = $1`, [r.reference]);
  const outs = await query<any>(`select * from outputs where run = $1`, [r.reference]);
  const massIn = cons.reduce((s: number, x: any) => s + Number(x.mass_g), 0);
  const massOut = outs.reduce((s: number, x: any) => s + Number(x.mass_g), 0);
  const recipe = RECIPES[r.recipe_version] ?? null;
  return c.json({
    reference: r.reference, run_type: r.run_type, site: r.site, grade: r.grade, equipment: r.equipment,
    recipe_version: r.recipe_version, recipe: recipe, operator: r.operator,
    started_at: r.started_at, closed_at: r.closed_at, state: r.state,
    losses_g: r.losses_g === null ? (r.state === 'closed' ? massIn - massOut : null) : Number(r.losses_g),
    mass_in_g: massIn, mass_out_g: massOut,
    set_points_achieved: r.set_points ?? null,
    within_tolerance: r.within_tolerance ?? null,
    inputs: cons.map((x) => ({ reference: x.input_reference, kind: x.input_kind, mass_g: Number(x.mass_g), effective_on: x.effective_on })),
    outputs: outs.map((x) => ({ reference: x.reference, kind: x.kind, mass_g: Number(x.mass_g), disposition: x.disposition ?? null })),
    derivation: { losses: 'losses_g = mass in - mass out', mass_in_g: massIn, mass_out_g: massOut },
  });
});

ops.post('/runs', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('plant_operator')) throw new HttpError(403, 'plant_operator_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const runType = strField(body.run_type, 'run_type', ['dissolution', 'depolymerisation', 'purification', 'repolymerisation']);
    const site = strField(body.site, 'site');
    const equipment = strField(body.equipment, 'equipment');
    const recipeVersion = strField(body.recipe_version, 'recipe_version');
    const ref = await nextRunRef(runType[0].toUpperCase());
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into runs(reference, run_type, site, grade, equipment, recipe_version, operator, started_at, opened_by)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9)`,
        [ref, runType, site, body.grade ?? 'N6', equipment, recipeVersion, body.operator ?? s.email,
         body.started_at ?? new Date().toISOString(), s.email]);
      await appendEntry(cl, { act: 'run_started', person: s.email, site, object: ref,
        content: { reference: ref, run_type: runType, recipe_version: recipeVersion, equipment } });
    });
    return { status: 201, body: { reference: ref, run_type: runType, site, state: 'open' } };
  }).then((r) => c.json(r.body, r.status as any));
});

async function nextRunRef(letter: string): Promise<string> {
  const r = await query<any>(`select count(*)::int as n from runs where run_type like $1`, [`${letter}%`]);
  const map: Record<string, string> = { D: 'RUN-D', Y: 'RUN-Y', U: 'RUN-U', R: 'RUN-R', P: 'RUN-P' };
  void map;
  return `RUN-${letter}-${String(1 + r[0].n).padStart(4, '0')}`;
}

ops.post('/runs/:reference/consumptions', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('plant_operator')) throw new HttpError(403, 'plant_operator_required');
  const runRef = c.req.param('reference');
  return idempotent<any>(c, async () => {
    const body = await readBody(c);
    assertNoDecimal(body);
    const inputRef = strField(body.input, 'input');
    const massG = intField(body.mass_g, 'mass_g', { min: 0 });
    const run = (await query<any>(`select * from runs where reference = $1`, [runRef]))[0];
    if (!run) throw new HttpError(404, 'run_not_found');
    if (run.state === 'closed') throw new HttpError(409, 'run_closed');
    const kind = inputRef.startsWith('BATCH-') ? 'batch' : 'intermediate';
    let dryG = massG;
    if (kind === 'batch') {
      const bv = await batchView(inputRef);
      if (!bv) throw new HttpError(404, 'batch_not_found');
      const moistureBp = bv.moisture_bp;
      dryG = dryMass(massG, moistureBp);
    }
    const effectiveOn = dateField(body.effective_on ?? run.started_at.slice(0, 10), 'effective_on');
    const ref = 'CSM-' + crypto.randomUUID().slice(0, 8).toUpperCase();
    // A consumption whose effective date falls in a closed period is refused as a write into it.
    const periods = await query<any>(
      `select * from balance_periods where site = $1 and grade = $2 and $3 between period_from and period_to`,
      [run.site, run.grade, effectiveOn]);
    const period = periods[0];
    if (period?.state === 'closed') {
      return {
        status: 409,
        body: { error: 'period_closed', period: period.id, closed_on: period.closed_on, remedy: 'open a restatement' },
      };
    }
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into consumptions(reference, run, input_kind, input_reference, mass_g, effective_on, recorded_by)
         values ($1,$2,$3,$4,$5,$6,$7)`,
        [ref, runRef, kind, inputRef, massG, effectiveOn, s.email]);
      if (period && kind === 'batch') {
        const bv = await batchView(inputRef);
        if (bv?.claimable) {
          const factor = (await cl.query(
            `select * from conversion_factors where site = $1 order by provisional, published_on desc limit 1`, [run.site])).rows[0];
          const credit = flMulDiv(dryG, Number(factor.factor_bp), 10000);
          await cl.query(
            `insert into credit_movements(reference, period, kind, category, mass_g, factor_version, created_by, effective_on)
             values ($1,$2,'in',$3,$4,$5,$6,$7)`,
            ['CRD-' + crypto.randomUUID().slice(0, 8).toUpperCase(), period.id, bv.category, credit,
             factor.reference, s.email, effectiveOn]);
        }
      }
      await appendEntry(cl, { act: 'consumption_recorded', person: s.email, site: run.site, object: runRef,
        content: { reference: ref, run: runRef, input: inputRef, mass_g: massG, dry_mass_g: dryG, effective_on: effectiveOn } });
    });
    return { status: 201, body: { reference: ref, run: runRef, input: inputRef, mass_g: massG, dry_mass_g: dryG } };
  }).then((r) => c.json(r.body, r.status as any));
});

ops.post('/runs/:reference/outputs', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('plant_operator')) throw new HttpError(403, 'plant_operator_required');
  const runRef = c.req.param('reference');
  return idempotent(c, async () => {
    const body = await readBody(c);
    assertNoDecimal(body);
    const kind = strField(body.kind, 'kind', ['intermediate', 'lot', 'byproduct']);
    const massG = intField(body.mass_g, 'mass_g', { min: 0 });
    const run = (await query<any>(`select * from runs where reference = $1`, [runRef]))[0];
    if (!run) throw new HttpError(404, 'run_not_found');
    if (run.state === 'closed') throw new HttpError(409, 'run_closed');
    const prefix = runTypePrefix(run.run_type);
    const count = (await query<any>(`select count(*)::int as n from outputs where run = $1`, [runRef]))[0].n;
    const ref = `OUT-${prefix}-${String(count + 1).padStart(4, '0')}`;
    let lotRef: string | null = null;
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into outputs(reference, run, kind, mass_g, disposition, grade) values ($1,$2,$3,$4,$5,$6)`,
        [ref, runRef, kind, massG, kind === 'byproduct' ? strField(body.disposition, 'disposition', ['sold', 'disposed']) : null, run.grade]);
      if (kind === 'lot') {
        const lotCount = (await cl.query(`select count(*)::int as n from lots where grade = $1`, [run.grade])).rows[0].n;
        lotRef = `LOT-${run.grade}-${String(lotCount + 1).padStart(4, '0')}`;
        await cl.query(
          `insert into lots(reference, run, output, site, grade, mass_g, claim_type) values ($1,$2,$3,$4,$5,$6,$7)`,
          [lotRef, runRef, ref, run.site, run.grade, massG, body.claim_type ?? 'mass_balance']);
      }
      await appendEntry(cl, { act: 'output_recorded', person: s.email, site: run.site, object: ref,
        content: { reference: ref, run: runRef, kind, mass_g: massG, lot: lotRef } });
    });
    return { status: 201, body: { reference: ref, run: runRef, kind, mass_g: massG, lot: lotRef } };
  }).then((r) => c.json(r.body, r.status as any));
});

function runTypePrefix(t: string): string {
  return { dissolution: 'D', depolymerisation: 'Y', purification: 'U', repolymerisation: 'R' }[t] ?? 'X';
}

ops.post('/runs/:reference/close', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('plant_operator')) throw new HttpError(403, 'plant_operator_required');
  const runRef = c.req.param('reference');
  return idempotent(c, async () => {
    const run = (await query<any>(`select * from runs where reference = $1`, [runRef]))[0];
    if (!run) throw new HttpError(404, 'run_not_found');
    if (run.state === 'closed') {
      await withTransaction(async (cl) => {
        await appendEntry(cl, { act: 'run_close_attempt_on_closed', person: s.email, site: run.site, object: runRef,
          content: { reference: runRef, refused: true, reason: 'already closed' } });
      });
      throw new HttpError(409, 'already_closed', { closed_at: run.closed_at });
    }
    const cons = await query<any>(`select * from consumptions where run = $1`, [runRef]);
    const outs = await query<any>(`select * from outputs where run = $1`, [runRef]);
    const massIn = cons.reduce((s2: number, x: any) => s2 + Number(x.mass_g), 0);
    const massOut = outs.reduce((s2: number, x: any) => s2 + Number(x.mass_g), 0);
    const losses = massIn - massOut;
    const achieved = (await readBody(c).catch(() => ({}))) ?? {};
    const recipe = RECIPES[run.recipe_version];
    let within: boolean | null = null;
    if (recipe && achieved.set_points) {
      within = Object.entries(recipe.set_points).every(([k, range]) => {
        const got = (achieved.set_points as any)[k];
        if (typeof got !== 'number') return true;
        const [lo, hi] = range as [number, number];
        return got >= lo && got <= hi;
      });
    }
    await withTransaction(async (cl) => {
      await cl.query(
        `update runs set state='closed', closed_at=now(), losses_g=$2, within_tolerance=$3, set_points=$4 where reference=$1`,
        [runRef, losses, within, JSON.stringify(achieved.set_points ?? null)]);
      await appendEntry(cl, { act: 'run_closed', person: s.email, site: run.site, object: runRef,
        content: { reference: runRef, mass_in_g: massIn, mass_out_g: massOut, losses_g: losses, within_tolerance: within } });
      // A run outside its recipe tolerance raises a deviation whether or not its output passed its tests.
      if (within === false) {
        const n = (await cl.query(`select count(*)::int as n from deviations`)).rows[0].n;
        await cl.query(
          `insert into deviations(reference, state, runs, lots, raised_by, description)
           values ($1,'open',$2,$3,$4,$5)`,
          [`DEV-${String(n + 1).padStart(4, '0')}`, [runRef], outs.filter((o: any) => o.kind === 'lot').map((o: any) => o.reference),
           s.email, `Run ${runRef} recorded set points outside recipe ${run.recipe_version} tolerance.`]);
      }
    });
    return { status: 200, body: { reference: runRef, state: 'closed', losses_g: losses, mass_in_g: massIn, mass_out_g: massOut, within_tolerance: within, derivation: 'losses_g = mass in - mass out' } };
  }).then((r) => c.json(r.body, r.status as any));
});

// ---------------- lots, genealogy, yield, blend ----------------
ops.get('/lots', async (c) => {
  refusePagination(c);
  const rows = await query<any>(`select * from lots order by reference`);
  const out = [];
  for (const l of rows) {
    out.push(await lotView(l.reference));
  }
  return c.json(out);
});

export async function lotView(ref: string): Promise<any> {
  const l = (await query<any>(`select * from lots where reference = $1`, [ref]))[0];
  if (!l) return null;
  const attached = await query<any>(
    `select category, coalesce(sum(mass_g),0)::bigint as n from credit_movements where lot = $1 and kind = 'out' group by category`, [ref]);
  const attachedTotal = attached.reduce((s: number, x: any) => s + Number(x.n), 0);
  const contentBp = Number(l.mass_g) > 0 ? flMulDiv(attachedTotal, 10000, Number(l.mass_g)) : 0;
  const split: Record<string, number> = {};
  for (const a of attached) split[a.category] = flMulDiv(Number(a.n), 10000, Number(l.mass_g));
  const overrides = await query<any>(`select * from overrides where lot = $1`, [ref]);
  const devs = await query<any>(`select * from deviations where state = 'open' and lots && $1::text[]`, [[ref]]);
  const factor = (await query<any>(
    `select * from conversion_factors where site = $1 order by provisional, published_on desc limit 1`, [l.site]))[0];
  return {
    reference: l.reference, grade: l.grade, site: l.site, mass_g: Number(l.mass_g),
    disposition: l.disposition, claim_type: l.claim_type,
    run: l.run, output: l.output,
    credit_attached_g: attachedTotal,
    content_bp: contentBp,
    category_split: split,
    flags: await lotInheritedFlags(ref),
    overrides: overrides.map((o) => ({
      reference: o.reference, separation: o.separation, reason: o.reason, authorised_by: o.authorised_by,
      authorised_on: o.authorised_on, reviewed: o.reviewed,
    })),
    open_deviations: devs.map((d) => d.reference),
    conversion_factor: factor ? { reference: factor.reference, factor_bp: factor.factor_bp, provisional: factor.provisional } : null,
    provisional_factor: factor?.provisional ?? false,
    blend_parents: l.blend_parents ?? null,
    derivation: {
      content_bp: 'credit_attached_g * 10000 / lot_mass_g, floored',
      credit_attached_g: attachedTotal, lot_mass_g: Number(l.mass_g),
      conversion_factor: factor?.reference ?? null,
    },
  };
}

ops.get('/lots/:reference', async (c) => {
  const v = await lotView(c.req.param('reference'));
  if (!v) throw new HttpError(404, 'not_found');
  return c.json(v);
});

ops.get('/lots/:reference/genealogy', async (c) => {
  refusePagination(c);
  const g = await genealogy(c.req.param('reference'));
  if (!g) throw new HttpError(404, 'not_found');
  return c.json(g);
});

ops.get('/lots/:reference/yield', async (c) => {
  const s = await requireSession(c);
  if (s.roles.includes('collector') || s.roles.includes('converter')) throw new HttpError(403, 'yield_not_for_recipient');
  const ref = c.req.param('reference');
  const l = (await query<any>(`select * from lots where reference = $1`, [ref]))[0];
  if (!l) throw new HttpError(404, 'not_found');
  const g = await genealogy(ref);
  const batchNodes = g.nodes.filter((n: any) => n.kind === 'batch');
  const inputG = batchNodes.reduce((s2: number, n: any) => s2 + n.mass_g, 0);
  return c.json({
    lot: ref, input_mass_g: inputG, lot_mass_g: Number(l.mass_g),
    yield_bp: inputG > 0 ? flMulDiv(Number(l.mass_g), 10000, inputG) : null,
    derivation: { formula: 'yield_bp = lot_mass_g * 10000 / input_mass_g, floored', inputs: batchNodes.map((n: any) => n.reference) },
  });
});

ops.post('/lots/:reference/blend', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.some((r) => ['plant_operator', 'quality_manager', 'claims_manager'].includes(r))) {
    throw new HttpError(403, 'forbidden');
  }
  const ref = c.req.param('reference');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const other = strField(body.lot, 'lot');
    const a = (await query<any>(`select * from lots where reference = $1`, [ref]))[0];
    const b = (await query<any>(`select * from lots where reference = $1`, [other]))[0];
    if (!a || !b) throw new HttpError(404, 'not_found');
    if (ref === other) throw new HttpError(400, 'cannot_blend_with_itself');
    const va = await lotView(ref);
    const vb = await lotView(other);
    const massA = Number(a.mass_g), massB = Number(b.mass_g);
    const blendedMass = massA + massB;
    const contentA = va.content_bp, contentB = vb.content_bp;
    const blendedBp = flMulDiv(massA * contentA + massB * contentB, 1, blendedMass);
    const weakerType = claimWeaker(va.claim_type, vb.claim_type);
    const sites = [...new Set([a.site, b.site])];
    const weakerProvisional = va.provisional_factor || vb.provisional_factor;
    const blendedRef = `LOT-${a.grade}-${String((await query<any>(`select count(*)::int as n from lots`))[0].n + 1).padStart(4, '0')}`;
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into lots(reference, run, output, site, grade, mass_g, claim_type, blend_parents)
         values ($1,$2,$3,$4,$5,$6,$7,$8)`,
        [blendedRef, a.run, a.output, a.site, a.grade, blendedMass, weakerType,
         JSON.stringify([{ reference: ref, mass_g: massA }, { reference: other, mass_g: massB }])]);
      await appendEntry(cl, { act: 'lot_blended', person: s.email, site: a.site, object: blendedRef,
        content: { reference: blendedRef, parents: [ref, other], mass_g: blendedMass, content_bp: blendedBp } });
    });
    return {
      status: 201,
      body: {
        reference: blendedRef, mass_g: blendedMass, content_bp: blendedBp, claim_type: weakerType,
        sites, provisional_factor: weakerProvisional,
        derivation: {
          formula: '(mass_a * content_a + mass_b * content_b) / (mass_a + mass_b), floored',
          inputs: [{ lot: ref, mass_g: massA, content_bp: contentA }, { lot: other, mass_g: massB, content_bp: contentB }],
        },
      },
    };
  }).then((r) => c.json(r.body, r.status as any));
});

function claimWeaker(a: string, b: string): string {
  const order = ['physically_segregated', 'controlled_blending', 'mass_balance'];
  return order.indexOf(a) >= order.indexOf(b) ? a : b;
}

// ---------------- test results, dispositions, deviations, overrides ----------------
ops.post('/test-results', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.some((r) => ['lab_analyst', 'quality_manager'].includes(r))) throw new HttpError(403, 'lab_analyst_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const property = strField(body.property, 'property');
    const method = strField(body.method, 'method');
    const analyst = s.email;
    const value = typeof body.value === 'number' ? String(body.value) : strField(body.value, 'value');
    const unit = strField(body.unit, 'unit');
    const spec = await specificationFor(body.lot, body.batch);
    const methodMismatch = spec ? !spec.rows.some((r: any) => r.property === property && r.method === method) : false;
    const ref = 'TST-' + crypto.randomUUID().slice(0, 8).toUpperCase();
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into test_results(reference, lot, batch, property, method, instrument, analyst, value, unit, uncertainty_bp)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)`,
        [ref, body.lot ?? null, body.batch ?? null, property, method, body.instrument ?? null, analyst,
         value, unit, body.uncertainty_bp ?? null]);
      await appendEntry(cl, { act: 'test_result_recorded', person: s.email, object: ref,
        content: { reference: ref, lot: body.lot ?? null, batch: body.batch ?? null, property, method, value, unit } });
    });
    return {
      status: 201,
      body: {
        reference: ref, lot: body.lot ?? null, batch: body.batch ?? null, property, method,
        instrument: body.instrument ?? null, analyst, value, unit, uncertainty_bp: body.uncertainty_bp ?? null,
        method_mismatch: methodMismatch,
        usable_for_release: !methodMismatch,
      },
    };
  }).then((r) => c.json(r.body, r.status as any));
});

async function specificationFor(lot?: string, batch?: string): Promise<any | null> {
  let grade = 'N6';
  if (lot) {
    const l = (await query<any>(`select grade from lots where reference = $1`, [lot]))[0];
    if (l) grade = l.grade;
  }
  const rows = (await query<any>(
    `select * from specifications where grade = $1 and state = 'current' order by version desc limit 1`, [grade]))[0];
  return rows ?? null;
}

ops.get('/test-results', async (c) => {
  refusePagination(c);
  const rows = await query<any>(`select * from test_results order by reference desc`);
  return c.json(rows.map((t) => ({
    reference: t.reference, lot: t.lot, batch: t.batch, property: t.property, method: t.method,
    instrument: t.instrument, analyst: t.analyst, value: t.value, unit: t.unit,
    uncertainty_bp: t.uncertainty_bp ?? null, recorded_on: t.recorded_on,
  })));
});

ops.post('/lots/:reference/disposition', async (c) => {
  const s = await requireSession(c);
  const ref = c.req.param('reference');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const disposition = strField(body.disposition, 'disposition', ['pending', 'released', 'quarantined', 'rejected']);
    if (!s.roles.includes('quality_manager')) {
      await recordRefusal('disposition_refused', s.email, ref, { reason: 'quality_manager_required' });
      throw new HttpError(403, 'quality_manager_required');
    }
    const entered = (await query<any>(`select 1 from test_results where lot = $1 and analyst = $2`, [ref, s.email])).length > 0;
    if (entered) {
      await recordRefusal('disposition_refused', s.email, ref, { reason: 'analyst_may_not_disposition_own_result' });
      throw new HttpError(403, 'analyst_may_not_disposition_own_result');
    }
    const openDev = (await query<any>(
      `select reference from deviations where state = 'open' and lots && $1::text[] limit 1`, [[ref]]))[0];
    if (openDev) {
      await recordRefusal('disposition_refused', s.email, ref, { reason: 'open_deviation', deviation: openDev.reference });
      throw new HttpError(409, 'open_deviation', { deviation: openDev.reference });
    }
    await withTransaction(async (cl) => {
      await cl.query(`update lots set disposition = $2 where reference = $1`, [ref, disposition]);
      await appendEntry(cl, { act: 'disposition_set', person: s.email, object: ref,
        content: { reference: ref, disposition } });
    });
    return { status: 200, body: await lotView(ref) };
  }).then((r) => c.json(r.body, r.status as any));
});

async function recordRefusal(act: string, person: string, object: string, content: any) {
  await withTransaction(async (cl) => {
    await appendEntry(cl, { act, person, object, content: { ...content, refused: true } });
  });
}

ops.get('/deviations', async (c) => {
  const rows = await query<any>(`select * from deviations order by reference`);
  return c.json(rows.map(deviationView));
});

function deviationView(d: any) {
  return {
    reference: d.reference, state: d.state, runs: d.runs, lots: d.lots, raised_by: d.raised_by,
    raised_on: d.raised_on, outcome: d.outcome ?? null, closed_on: d.closed_on ?? null, description: d.description ?? null,
  };
}

ops.post('/deviations', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.some((r) => ['quality_manager', 'plant_operator', 'lab_analyst'].includes(r))) {
    throw new HttpError(403, 'forbidden');
  }
  return idempotent(c, async () => {
    const body = await readBody(c);
    const runs = Array.isArray(body.runs) ? body.runs : [];
    const lots = Array.isArray(body.lots) ? body.lots : [];
    if (!runs.length && !lots.length) throw new HttpError(400, 'deviation_needs_object');
    const n = (await query<any>(`select count(*)::int as n from deviations`))[0].n;
    const ref = `DEV-${String(n + 1).padStart(4, '0')}`;
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into deviations(reference, state, runs, lots, raised_by, description) values ($1,'open',$2,$3,$4,$5)`,
        [ref, runs, lots, s.email, body.description ?? null]);
      await appendEntry(cl, { act: 'deviation_raised', person: s.email, object: ref,
        content: { reference: ref, runs, lots, description: body.description ?? null } });
    });
    return { status: 201, body: { reference: ref, state: 'open', runs, lots } };
  }).then((r) => c.json(r.body, r.status as any));
});

ops.post('/deviations/:reference/close', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const outcome = strField(body.outcome, 'outcome', ['root_cause_found', 'cause_not_established']);
    const d = (await query<any>(`select * from deviations where reference = $1`, [c.req.param('reference')]))[0];
    if (!d) throw new HttpError(404, 'not_found');
    if (d.state === 'closed') throw new HttpError(409, 'already_closed');
    await withTransaction(async (cl) => {
      await cl.query(`update deviations set state='closed', outcome=$2, closed_on=current_date where reference=$1`,
        [d.reference, outcome]);
      await appendEntry(cl, { act: 'deviation_closed', person: s.email, object: d.reference,
        content: { reference: d.reference, outcome } });
    });
    return { status: 200, body: { reference: d.reference, state: 'closed', outcome } };
  }).then((r) => c.json(r.body, r.status as any));
});

ops.get('/overrides', async (c) => {
  const rows = await query<any>(`select * from overrides order by reference`);
  return c.json(rows.map(overrideView));
});

function overrideView(o: any) {
  return {
    reference: o.reference, separation: o.separation, reason: o.reason, lot: o.lot,
    authorised_by: o.authorised_by, authorised_on: o.authorised_on,
    reviewed: o.reviewed, reviewed_by: o.reviewed_by ?? null, reviewed_on: o.reviewed_on ?? null,
  };
}

ops.post('/overrides', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.some((r) => ['quality_manager', 'claims_manager'].includes(r))) throw new HttpError(403, 'forbidden');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const separation = strField(body.separation, 'separation');
    const reason = strField(body.reason, 'reason');
    if (reason.trim().length < 40) throw new HttpError(400, 'reason_too_short', { minimum_characters: 40 });
    const lot = strField(body.lot, 'lot');
    const authorisedBy = strField(body.authorised_by, 'authorised_by');
    const n = (await query<any>(`select count(*)::int as n from overrides`))[0].n;
    const ref = `OVR-${String(n + 1).padStart(4, '0')}`;
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into overrides(reference, separation, reason, lot, authorised_by) values ($1,$2,$3,$4,$5)`,
        [ref, separation, reason, lot, authorisedBy]);
      await appendEntry(cl, { act: 'override_recorded', person: s.email, object: ref,
        content: { reference: ref, separation, lot, authorised_by: authorisedBy } });
    });
    return { status: 201, body: { reference: ref, separation, lot, authorised_by: authorisedBy, reviewed: false, permanent: true } };
  }).then((r) => c.json(r.body, r.status as any));
});

ops.post('/overrides/:reference/review', async (c) => {
  const s = await requireSession(c);
  const ref = c.req.param('reference');
  return idempotent(c, async () => {
    const o = (await query<any>(`select * from overrides where reference = $1`, [ref]))[0];
    if (!o) throw new HttpError(404, 'not_found');
    if (o.reviewed) throw new HttpError(409, 'already_reviewed');
    if (o.authorised_by === s.email) {
      await recordRefusal('override_review_refused', s.email, ref, { reason: 'authoriser_may_not_review' });
      throw new HttpError(403, 'authoriser_may_not_review');
    }
    if (!s.roles.some((r) => ['quality_manager', 'claims_manager'].includes(r))) {
      await recordRefusal('override_review_refused', s.email, ref, { reason: 'quality_or_claims_manager_required' });
      throw new HttpError(403, 'quality_or_claims_manager_required');
    }
    await withTransaction(async (cl) => {
      await cl.query(`update overrides set reviewed = true, reviewed_by = $2, reviewed_on = current_date where reference = $1`,
        [ref, s.email]);
      await appendEntry(cl, { act: 'override_reviewed', person: s.email, object: ref,
        content: { reference: ref, reviewed_by: s.email } });
    });
    return { status: 200, body: { reference: ref, reviewed: true, reviewed_by: s.email, note: 'A review sets reviewed true and removes nothing.' } };
  }).then((r) => c.json(r.body, r.status as any));
});
