import crypto from 'node:crypto';
import { Hono } from 'hono';
import { query, withTransaction } from '../lib/db.js';
import { HttpError, requireSession, requireRole, idempotent, readBody, strField, refusePagination } from '../lib/http.js';
import { appendEntry, retentionFor, GENESIS } from '../lib/record.js';
import { sha256, stableStringify } from '../lib/num.js';
import { batchImpact } from '../lib/claims.js';

export const record = new Hono();

function entryView(e: any) {
  return {
    seq: Number(e.seq), act: e.act, person: e.person, site: e.site, object: e.object,
    digest: e.digest, prev_digest: e.prev_digest,
    event_at: e.event_at, recorded_at: e.recorded_at,
    correction_of: e.correction_of ?? null,
    legal_hold: e.legal_hold,
    content_deleted_on: e.content_deleted_on ?? null,
    content: e.content_deleted_on ? { deleted: true, note: `Content deleted under retention on ${e.content_deleted_on}.` } : e.content,
  };
}

record.get('/record', async (c) => {
  refusePagination(c);
  const rows = await query<any>(`select * from record_entries order by seq`);
  return c.json(rows.map(entryView));
});

record.get('/record/check', async (c) => {
  const rows = await query<any>(`select * from record_entries order by seq`);
  let prev = GENESIS;
  let holds = true;
  let firstFailure: number | null = null;
  let gapAt: number | null = null;
  let prevSeq: number | null = null;
  for (const e of rows) {
    if (prevSeq !== null && Number(e.seq) !== prevSeq + 1 && gapAt === null) {
      gapAt = Number(e.seq);
    }
    if (e.prev_digest !== prev && firstFailure === null) {
      firstFailure = Number(e.seq); holds = false;
    }
    const payload = JSON.stringify({
      act: e.act, person: e.person, site: e.site, object: e.object,
      content: JSON.parse(stableStringify(e.content ?? {})),
      correction_of: e.correction_of ?? null,
      prev_seq: prevSeq, prev_digest: e.prev_digest,
    });
    if (sha256(payload) !== e.digest && firstFailure === null) {
      firstFailure = Number(e.seq); holds = false;
    }
    prev = e.digest;
    prevSeq = Number(e.seq);
  }
  return c.json({
    holds, entries: rows.length, first_failure: firstFailure,
    gap_in_sequence: gapAt,
    note: 'A gap in the sequence and a digest that does not verify are both reportable conditions.',
  });
});

record.patch('/record/:seq', async (c) => {
  await requireSession(c);
  throw new HttpError(403, 'record_is_append_only', {
    rule: 'No entry is edited and no entry is removed. A correction is a new entry naming what it corrects.',
  });
});

record.delete('/record/:seq', async (c) => {
  await requireSession(c);
  throw new HttpError(403, 'record_is_append_only');
});

record.post('/record/:seq/corrections', async (c) => {
  const s = await requireSession(c);
  if (s.roles.includes('auditor')) throw new HttpError(403, 'auditor_reads_only');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const target = (await query<any>(`select * from record_entries where seq = $1`, [Number(c.req.param('seq'))]))[0];
    if (!target) throw new HttpError(404, 'not_found');
    const out = await withTransaction(async (cl) => {
      const e = await appendEntry(cl, {
        act: 'correction', person: s.email, site: target.site, object: target.object,
        correction_of: Number(target.seq), content: { corrects: Number(target.seq), note: body.note ?? '' },
      });
      return e;
    });
    return { status: 201, body: { reference: `ENT-${out.seq}`, seq: Number(out.seq), corrects: Number(target.seq), digest: out.digest } };
  }).then((r) => c.json(r.body, r.status as any));
});

record.get('/record/:seq/retention', async (c) => {
  const e = (await query<any>(`select * from record_entries where seq = $1`, [Number(c.req.param('seq'))]))[0];
  if (!e) throw new HttpError(404, 'not_found');
  const hold = (await query<any>(`select * from legal_holds where seq = $1 and lifted_on is null`, [Number(e.seq)]));
  const r = retentionFor(e);
  return c.json({ ...r, legal_hold: hold.length > 0 });
});

record.post('/record/:seq/legal-hold', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  const seq = Number(c.req.param('seq'));
  return idempotent(c, async () => {
    const e = (await query<any>(`select * from record_entries where seq = $1`, [seq]))[0];
    if (!e) throw new HttpError(404, 'not_found');
    const existing = (await query<any>(`select * from legal_holds where seq = $1 and lifted_on is null`, [seq]));
    if (existing.length) throw new HttpError(409, 'hold_already_stands');
    const ref = `HLD-${String((await query<any>(`select count(*)::int as n from legal_holds`))[0].n + 1).padStart(4, '0')}`;
    await withTransaction(async (cl) => {
      await cl.query(`update record_entries set legal_hold = true where seq = $1`, [seq]);
      await cl.query(`insert into legal_holds(reference, seq, placed_by) values ($1,$2,$3)`, [ref, seq, s.email]);
      await appendEntry(cl, { act: 'legal_hold_placed', person: s.email, object: ref,
        content: { reference: ref, seq } });
    });
    return { status: 201, body: { reference: ref, seq, legal_hold: true } };
  }).then((r) => c.json(r.body, r.status as any));
});

record.delete('/record/:seq/legal-hold', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  const seq = Number(c.req.param('seq'));
  const key = c.req.header('idempotency-key') ?? 'hold-lift-' + seq;
  return idempotent(c, async () => {
    const hold = (await query<any>(`select * from legal_holds where seq = $1 and lifted_on is null`, [seq]))[0];
    if (!hold) throw new HttpError(404, 'no_hold_stands');
    await withTransaction(async (cl) => {
      await cl.query(`update legal_holds set lifted_on = current_date, lifted_by = $2 where reference = $1`, [hold.reference, s.email]);
      const remaining = await cl.query(`select 1 from legal_holds where seq = $1 and lifted_on is null`, [seq]);
      if (!remaining.rows.length) await cl.query(`update record_entries set legal_hold = false where seq = $1`, [seq]);
      await appendEntry(cl, { act: 'legal_hold_lifted', person: s.email, object: hold.reference,
        content: { reference: hold.reference, seq } });
    });
    return { status: 200, body: { seq, legal_hold: false } };
  }).then((r) => c.json(r.body, r.status as any));
});

record.post('/record/:seq/expire', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('quality_manager')) throw new HttpError(403, 'quality_manager_required');
  const seq = Number(c.req.param('seq'));
  return idempotent(c, async () => {
    const e = (await query<any>(`select * from record_entries where seq = $1`, [seq]))[0];
    if (!e) throw new HttpError(404, 'not_found');
    if (e.content_deleted_on) throw new HttpError(409, 'already_expired');
    const hold = (await query<any>(`select 1 from legal_holds where seq = $1 and lifted_on is null`, [seq]));
    if (hold.length) throw new HttpError(409, 'legal_hold_refuses_deletion');
    const r = retentionFor(e);
    const today = new Date().toISOString().slice(0, 10);
    if (today < r.retain_until) {
      throw new HttpError(409, 'retention_not_elapsed', { retain_until: r.retain_until });
    }
    // A certificate existed: that one fact is never deleted.
    const isCertificate = e.act === 'certificate_signed' || e.act === 'certificate_withdrawn';
    if (isCertificate) throw new HttpError(403, 'certificate_existence_never_deleted');
    await withTransaction(async (cl) => {
      await cl.query(
        `update record_entries set content = $2, content_deleted_on = current_date where seq = $1`,
        [seq, JSON.stringify({ deleted: true })]);
      await appendEntry(cl, { act: 'record_content_expired', person: s.email, object: `ENT-${seq}`,
        content: { seq, deleted_on: today, note: 'Position and digest survive so the chain still verifies.' } });
    });
    return { status: 200, body: { seq, content_deleted_on: today, digest_kept: e.digest, prev_digest_kept: e.prev_digest } };
  }).then((r) => c.json(r.body, r.status as any));
});

// ---------------- the nine record queries ----------------
record.get('/record/queries/:name', async (c) => {
  refusePagination(c);
  const name = c.req.param('name');
  const lots = await query<any>(`select * from lots`);
  const lotMap = new Map(lots.map((l) => [l.reference, l]));
  const cons = await query<any>(`select * from consumptions`);
  const outs = await query<any>(`select * from outputs`);
  const outputsByRun = new Map<string, any[]>();
  for (const o of outs) outputsByRun.set(o.run, [...(outputsByRun.get(o.run) ?? []), o]);
  const runsConsuming = new Map<string, string[]>();
  for (const cm of cons) runsConsuming.set(cm.input_reference, [...(runsConsuming.get(cm.input_reference) ?? []), cm.run]);
  const lotsFromBatch = (batch: string) => {
    const reached = new Set<string>();
    const seen = new Set<string>();
    const walk = (ref: string, kind: string) => {
      if (seen.has(ref + kind)) return;
      seen.add(ref + kind);
      if (kind === 'lot') { reached.add(ref); return; }
      if (kind === 'intermediate' || kind === 'byproduct') {
        for (const r of runsConsuming.get(ref) ?? []) walk(r, 'run');
        return;
      }
      if (kind === 'run') { for (const o of outputsByRun.get(ref) ?? []) walk(o.reference, o.kind); }
    };
    walk(batch, 'batch');
    return [...reached];
  };

  switch (name) {
    case 'lots_from_batch': {
      const batches = await query<any>(`select reference from batches order by reference`);
      const out: any[] = [];
      for (const b of batches) out.push({ batch: b.reference, lots: lotsFromBatch(b.reference) });
      return c.json(out);
    }
    case 'certificates_on_period': {
      const periods = await query<any>(`select id from balance_periods order by period_from`);
      const out: any[] = [];
      for (const p of periods) {
        const rows = await query<any>(`select number from certificates where period = $1 order by signed_at`, [p.id]);
        out.push({ period: p.id, certificates: rows.map((r) => r.number) });
      }
      return c.json(out);
    }
    case 'certificates_under_method_version': {
      const rows = await query<any>(`select * from certificates order by signed_at`);
      return c.json(rows.map((r) => ({
        certificate: r.number, method_version: r.method_version, carbon_figure: r.carbon_figure,
      })));
    }
    case 'lots_released_under_unreviewed_override': {
      const ovr = await query<any>(`select * from overrides where reviewed = false`);
      const out = ovr.filter((o) => lotMap.get(o.lot)?.disposition === 'released')
        .map((o) => ({ lot: o.lot, override: o.reference, disposition: lotMap.get(o.lot)?.disposition }));
      return c.json(out);
    }
    case 'allocations_in_final_fortnight': {
      const rows = await query<any>(`select * from balance_periods`);
      const out: any[] = [];
      for (const p of rows) {
        const from = new Date(p.period_to + 'T00:00:00Z');
        from.setUTCDate(from.getUTCDate() - 14);
        const start = from.toISOString().slice(0, 10);
        const movs = await query<any>(
          `select * from credit_movements where period = $1 and kind = 'out' and effective_on between $2 and $3`,
          [p.id, start, p.period_to]);
        for (const m of movs) out.push({ period: p.id, reference: m.reference, lot: m.lot, mass_g: Number(m.mass_g), effective_on: m.effective_on });
      }
      return c.json(out);
    }
    case 'refused_allocations': {
      const rows = await query<any>(
        `select * from record_entries where act = 'allocation_refused' order by seq`);
      return c.json(rows.map((r) => ({
        seq: Number(r.seq), lot: r.content?.lot, period: r.content?.period,
        available_g: r.content?.available_g, requested_g: r.content?.requested_g, person: r.person,
      })));
    }
    case 'collector_declaration_departures': {
      const rows = await query<any>(`select * from findings where kind = 'declaration_departure' order by recorded_on`);
      return c.json(rows.map((f) => ({ collector: f.collector, detail: f.detail, state: f.state, recorded_on: f.recorded_on })));
    }
    case 'acts_by_person': {
      const rows = await query<any>(`select person, count(*)::int as n from record_entries where person is not null group by person order by person`);
      return c.json(rows.map((r) => ({ person: r.person, acts: r.n })));
    }
    case 'exports_by_auditor': {
      const rows = await query<any>(`select * from exports order by exported_on desc`);
      return c.json(rows.map((x) => ({
        reference: x.reference, by: x.by, exported_on: x.exported_on, scope: x.scope,
        entry_count: x.entry_count, returned_nothing: x.entry_count === 0,
      })));
    }
    default:
      throw new HttpError(404, 'unknown_query', {
        known: ['lots_from_batch', 'certificates_on_period', 'certificates_under_method_version',
          'lots_released_under_unreviewed_override', 'allocations_in_final_fortnight', 'refused_allocations',
          'collector_declaration_departures', 'acts_by_person', 'exports_by_auditor'],
      });
  }
});

// ---------------- exports ----------------
record.post('/exports', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('auditor')) throw new HttpError(403, 'auditor_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const scope = body.scope ?? {};
    const ref = 'EXP-' + crypto.randomUUID().slice(0, 6).toUpperCase();
    // Read the entries in scope, then record the scope before returning.
    const entries = await query<any>(`select * from record_entries order by seq`);
    const inScope = entries.filter((e) => {
      if (scope.site && e.site !== scope.site) return false;
      if (scope.period && e.content?.period !== scope.period) return false;
      if (Array.isArray(scope.certificates) && scope.certificates.length && !(scope.certificates as string[]).includes(String(e.object))) return false;
      return true;
    });
    const anchors = inScope.slice(0, 50).map((e) => ({ seq: Number(e.seq), digest: e.digest }));
    const result = {
      reference: ref,
      scope,
      exported_on: new Date().toISOString(),
      entries: inScope.map((e) => ({ seq: Number(e.seq), act: e.act, digest: e.digest, prev_digest: e.prev_digest })),
      anchor_references: anchors,
      digest: sha256(JSON.stringify(inScope.map((e) => e.digest))),
      derivation: 'Every entry carries its digest and the previous entry\'s digest, so integrity can be established without this system.',
    };
    const entry = await withTransaction(async (cl) => {
      const e = await appendEntry(cl, { act: 'export', person: s.email, site: scope.site ?? null, object: ref,
        content: { reference: ref, scope, entry_count: inScope.length } });
      await cl.query(
        `insert into exports(reference, scope, by, entry_seq, entry_count, result) values ($1,$2,$3,$4,$5,$6)`,
        [ref, JSON.stringify(scope), s.email, Number(e.seq), inScope.length, JSON.stringify({ digest: result.digest })]);
      return e;
    });
    return { status: 201, body: { ...result, entry_seq: Number(entry.seq), reference: ref } };
  }).then((r) => c.json(r.body, r.status as any));
});

record.get('/exports', async (c) => {
  const rows = await query<any>(`select * from exports order by exported_on desc`);
  return c.json(rows.map((x) => ({
    reference: x.reference, scope: x.scope, by: x.by, exported_on: x.exported_on,
    entry_seq: Number(x.entry_seq), entry_count: x.entry_count,
  })));
});
