import crypto from 'node:crypto';
import { Hono } from 'hono';
import { query, withTransaction } from '../lib/db.js';
import { HttpError, requireSession, idempotent, readBody, strField, intField, refusePagination, assertNoDecimal } from '../lib/http.js';
import { appendEntry } from '../lib/record.js';
import { flMulDiv, sha256 } from '../lib/num.js';
import { latestFigure } from '../lib/certs.js';

export const carbon = new Hono();

carbon.get('/carbon-methods', async (c) => {
  const rows = await query<any>(`select * from carbon_methods order by key, version desc`);
  return c.json(rows.map(methodView));
});

carbon.get('/carbon-methods/:id/versions/:version', async (c) => {
  const rows = await query<any>(
    `select * from carbon_methods where key = $1 and version = $2`,
    [c.req.param('id'), Number(c.req.param('version'))]);
  if (!rows.length) throw new HttpError(404, 'not_found');
  return c.json(methodView(rows[0]));
});

function methodView(m: any) {
  return {
    id: m.key, key: m.key, version: m.version, standard: m.standard, functional_unit: m.functional_unit,
    boundary: m.boundary, allocation_basis: m.allocation_basis, reviewer: m.reviewer,
    published_on: m.published_on, published_by: m.published_by,
    data_quality: m.data_quality, emission_factors: m.emission_factors,
    primary_share_threshold_bp: m.primary_share_threshold_bp, state: m.state,
  };
}

carbon.post('/carbon-methods', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const standard = strField(body.standard, 'standard');
    const functionalUnit = strField(body.functional_unit, 'functional_unit');
    const boundary = strField(body.boundary, 'boundary');
    const allocationBasis = strField(body.allocation_basis, 'allocation_basis', ['mass', 'energy', 'economic']);
    const key = body.key ?? 'CM-PA6';
    const prior = (await query<any>(
      `select * from carbon_methods where key = $1 order by version desc limit 1`, [key]))[0];
    if (prior) {
      const inUse = (await query<any>(`select count(*)::int as n from carbon_figures where method_key = $1`, [key]))[0].n;
      if (inUse > 0) {
        // The prior version stays readable and is superseded rather than overwritten.
        await withTransaction(async (cl) => {
          await cl.query(`update carbon_methods set state = 'superseded' where key = $1 and version = $2`, [key, prior.version]);
        });
      }
    }
    const version = prior ? prior.version + 1 : 1;
    const ref = key;
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into carbon_methods(key, version, standard, functional_unit, boundary, allocation_basis, reviewer, published_by,
            data_quality, emission_factors, primary_share_threshold_bp, state)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,'current')`,
        [key, version, standard, functionalUnit, boundary, allocationBasis, body.reviewer ?? s.email, s.email,
         JSON.stringify(body.data_quality ?? {}), JSON.stringify(body.emission_factors ?? []),
         body.primary_share_threshold_bp ?? 5000]);
      await appendEntry(cl, { act: 'carbon_method_published', person: s.email, object: `${key} v${version}`,
        content: { key, version, standard, boundary, allocation_basis: allocationBasis } });
    });
    const row = (await query<any>(`select * from carbon_methods where key = $1 and version = $2`, [key, version]))[0];
    return { status: 201, body: { reference: `${key}-v${version}`, ...methodView(row) } };
  }).then((r) => c.json(r.body, r.status as any));
});

/** A carbon value never travels without its boundary, method version and uncertainty. */
function figureView(f: any) {
  return {
    id: f.id, lot: f.lot,
    value_mg_per_kg: Number(f.value_mg_per_kg),
    boundary: f.boundary, method_version: f.method_version,
    uncertainty_bp: f.uncertainty_bp,
    comparator: f.comparator,
    primary_share_bp: f.primary_share_bp,
    default_led: f.primary_share_bp < (f.primary_share_threshold_bp ?? 5000),
    breakdown: f.breakdown,
    energy_location_mg_per_kg: Number(f.energy_location_mg_per_kg),
    energy_market_mg_per_kg: Number(f.energy_market_mg_per_kg),
    metered_kwh: Number(f.metered_kwh), retired_kwh: Number(f.retired_kwh), unmatched_kwh: Number(f.unmatched_kwh),
    cache_valid: f.cache_valid, superseded_by: f.superseded_by ?? null,
    computed_on: f.computed_on, computed_by: f.computed_by,
    derivation: {
      breakdown_sums_to_value: (f.breakdown as any[]).reduce((s, l) => s + Number(l.mg_per_kg), 0) === Number(f.value_mg_per_kg),
      method_version: f.method_version, boundary: f.boundary,
      note: 'Every derived figure carries the versions it was computed against.',
    },
    read_at: new Date().toISOString(),
  };
}

carbon.get('/lots/:reference/carbon', async (c) => {
  const lot = c.req.param('reference');
  const fig = await latestFigure(lot);
  if (!fig) throw new HttpError(404, 'no_carbon_figure');
  const period = await periodOfLot(lot);
  if (period) {
    const method = (await query<any>(
      `select * from carbon_methods where key = $1 order by version desc limit 1`, ['CM-PA6']))[0];
    if (method && method.allocation_basis !== period.allocation_basis) {
      throw new HttpError(409, 'allocation_basis_mismatch', {
        method_basis: method.allocation_basis, period_basis: period.allocation_basis,
      });
    }
  }
  return c.json(figureView(fig));
});

async function periodOfLot(lot: string) {
  const l = (await query<any>(`select * from lots where reference = $1`, [lot]))[0];
  if (!l) return null;
  const rows = await query<any>(
    `select * from balance_periods where site = $1 and grade = $2 order by period_from desc limit 1`, [l.site, l.grade]);
  return rows[0] ?? null;
}

carbon.post('/lots/:reference/carbon', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    assertNoDecimal(body);
    const lot = c.req.param('reference');
    const l = (await query<any>(`select * from lots where reference = $1`, [lot]))[0];
    if (!l) throw new HttpError(404, 'lot_not_found');
    const method = (await query<any>(
      `select * from carbon_methods where key = $1 order by version desc limit 1`, ['CM-PA6']))[0];
    if (!method) throw new HttpError(409, 'no_carbon_method');
    const breakdown = Array.isArray(body.breakdown) ? body.breakdown : [];
    if (!breakdown.length) throw new HttpError(400, 'breakdown_required');
    const value = breakdown.reduce((s2: number, line: any) => s2 + intField(line.mg_per_kg, 'breakdown.mg_per_kg'), 0);
    const ref = 'CF-FIG-' + crypto.randomUUID().slice(0, 6).toUpperCase();
    await withTransaction(async (cl) => {
      await cl.query(
        `insert into carbon_figures(id, lot, method_key, method_version, value_mg_per_kg, uncertainty_bp, primary_share_bp,
            comparator, breakdown, energy_location_mg_per_kg, energy_market_mg_per_kg, metered_kwh, retired_kwh, unmatched_kwh,
            computed_by, primary_share_threshold_bp, boundary)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17)`,
        [ref, lot, method.key, method.version, value, intField(body.uncertainty_bp, 'uncertainty_bp'),
         intField(body.primary_share_bp, 'primary_share_bp'), JSON.stringify(body.comparator ?? {}),
         JSON.stringify(breakdown), intField(body.energy_location_mg_per_kg, 'energy_location_mg_per_kg'),
         intField(body.energy_market_mg_per_kg, 'energy_market_mg_per_kg'), intField(body.metered_kwh, 'metered_kwh'),
         body.retired_kwh ?? 0, body.unmatched_kwh ?? 0, s.email, method.primary_share_threshold_bp, method.boundary]);
      await appendEntry(cl, { act: 'carbon_figure_computed', person: s.email, object: ref,
        content: { reference: ref, lot, value_mg_per_kg: value, method_version: `CM-PA6 v${method.version}` } });
    });
    const fig = (await query<any>(`select * from carbon_figures where id = $1`, [ref]))[0];
    return { status: 201, body: figureView(fig) };
  }).then((r) => c.json(r.body, r.status as any));
});

carbon.post('/energy-instruments/:reference/retire', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const period = strField(body.period, 'period');
    const inst = (await query<any>(`select * from energy_instruments where reference = $1`, [c.req.param('reference')]))[0];
    if (!inst) throw new HttpError(404, 'not_found');
    const p = (await query<any>(`select * from balance_periods where id = $1`, [period]))[0];
    if (!p) throw new HttpError(404, 'period_not_found');
    if (inst.state !== 'retired') throw new HttpError(409, 'instrument_not_retired', { state: inst.state });
    if (inst.vintage !== Number(body.vintage ?? p.period_from.slice(0, 4))) {
      throw new HttpError(409, 'vintage_mismatch', { instrument_vintage: inst.vintage, requested: body.vintage });
    }
    if (inst.region !== (body.region ?? 'EU-27')) {
      throw new HttpError(409, 'region_mismatch', { instrument_region: inst.region, requested: body.region });
    }
    const priorRetired = (await query<any>(
      `select coalesce(sum(quantity_kwh),0)::bigint as n from energy_instruments where period = $1`, [period]))[0];
    const metered = await meteredForPeriod(period);
    if (Number(priorRetired.n) + Number(inst.quantity_kwh) > metered) {
      throw new HttpError(409, 'would_exceed_metered', {
        metered_kwh: metered, already_retired_kwh: Number(priorRetired.n), instrument_kwh: Number(inst.quantity_kwh),
      });
    }
    await withTransaction(async (cl) => {
      await cl.query(`update energy_instruments set period = $2 where reference = $1`, [inst.reference, period]);
      await appendEntry(cl, { act: 'energy_instrument_retired', person: s.email, object: inst.reference,
        content: { reference: inst.reference, period, quantity_kwh: Number(inst.quantity_kwh) } });
    });
    return {
      status: 200,
      body: {
        reference: inst.reference, period, quantity_kwh: Number(inst.quantity_kwh),
        metered_kwh: metered, retired_kwh: Number(priorRetired.n) + Number(inst.quantity_kwh),
        unmatched_kwh: metered - Number(priorRetired.n) - Number(inst.quantity_kwh),
      },
    };
  }).then((r) => c.json(r.body, r.status as any));
});

carbon.get('/energy-instruments', async (c) => {
  const rows = await query<any>(`select * from energy_instruments order by reference`);
  return c.json(rows.map((i) => ({
    reference: i.reference, quantity_kwh: Number(i.quantity_kwh), vintage: i.vintage,
    region: i.region, state: i.state, period: i.period ?? null,
  })));
});

async function meteredForPeriod(period: string): Promise<number> {
  const config = await query<any>(`select metered_kwh from period_energy where period = $1`, [period]);
  if (config.length) return Number(config[0].metered_kwh);
  return 300000;
}

carbon.post('/carbon-figures/:id/recompute', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const reason = strField(body.reason, 'reason');
    const fig = (await query<any>(`select * from carbon_figures where id = $1`, [c.req.param('id')]))[0];
    if (!fig) throw new HttpError(404, 'not_found');
    const period = await periodOfLot(fig.lot);
    if (period?.state === 'closed') {
      const open = (await query<any>(
        `select 1 from restatements where period = $1 and state = 'open'`, [period.id])).length > 0;
      if (!open) throw new HttpError(409, 'period_closed_requires_restatement');
    }
    const method = (await query<any>(
      `select * from carbon_methods where key = $1 and version = $2`, [fig.method_key, fig.method_version]))[0];
    const ref = 'CF-FIG-' + crypto.randomUUID().slice(0, 6).toUpperCase();
    const affected = await query<any>(
      `select number from certificates where carbon_figure = $1`, [fig.id]);
    await withTransaction(async (cl) => {
      const recomputeValue = (body.breakdown
        ? (body.breakdown as any[]).reduce((s2, l) => s2 + Number(l.mg_per_kg), 0)
        : Number(fig.value_mg_per_kg));
      await cl.query(`update carbon_figures set superseded_by = $2, cache_valid = false where id = $1`, [fig.id, ref]);
      await cl.query(
        `insert into carbon_figures(id, lot, method_key, method_version, value_mg_per_kg, uncertainty_bp, primary_share_bp,
            comparator, breakdown, energy_location_mg_per_kg, energy_market_mg_per_kg, metered_kwh, retired_kwh, unmatched_kwh,
            computed_by, primary_share_threshold_bp, boundary, reason)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18)`,
        [ref, fig.lot, method?.key ?? fig.method_key, method?.version ?? fig.method_version,
         recomputeValue, fig.uncertainty_bp, fig.primary_share_bp, JSON.stringify(fig.comparator),
         JSON.stringify(body.breakdown ?? fig.breakdown), fig.energy_location_mg_per_kg, fig.energy_market_mg_per_kg,
         fig.metered_kwh, fig.retired_kwh, fig.unmatched_kwh, s.email, fig.primary_share_threshold_bp,
         method?.boundary ?? fig.boundary, reason]);
      await appendEntry(cl, { act: 'carbon_figure_recomputed', person: s.email, object: ref,
        content: { reference: ref, supersedes: fig.id, reason, certificates_enumerated: affected.map((a) => a.number) } });
    });
    return {
      status: 201,
      body: {
        reference: ref, supersedes: fig.id, reason,
        certificates_carrying_superseded_figure: affected.map((a) => a.number),
      },
    };
  }).then((r) => c.json(r.body, r.status as any));
});
