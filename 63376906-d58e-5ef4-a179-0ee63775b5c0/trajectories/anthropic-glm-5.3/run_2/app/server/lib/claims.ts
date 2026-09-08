import { query } from './db.js';
import { flMulDiv } from './num.js';

export type GraphNode = {
  kind: string; reference: string; mass_g: number; category_split: Record<string, number>; flags: string[];
};
export type GraphEdge = { from: string; to: string; mass_g: number };

const REQUIRED_CUSTODY = ['collection_site', 'collector', 'transport', 'arrival', 'weighing', 'acceptance'];

export function dryMass(net_g: number, moisture_bp: number): number {
  return flMulDiv(net_g, 10000 - moisture_bp, 10000);
}

export function missingCustody(links: any[]): string[] {
  const present = new Set((links ?? []).map((l) => l.kind));
  return REQUIRED_CUSTODY.filter((k) => !present.has(k));
}

export function monthsBetween(from: string, to: string): number {
  const a = new Date(from + 'T00:00:00Z'), b = new Date(to + 'T00:00:00Z');
  return (b.getUTCFullYear() - a.getUTCFullYear()) * 12 + (b.getUTCMonth() - a.getUTCMonth());
}

/** True when the calibration date is more than twelve months before the receipt. */
export function calibrationLapsed(calibratedOn: string, receivedOn: string): boolean {
  const limit = new Date(calibratedOn + 'T00:00:00Z');
  limit.setUTCMonth(limit.getUTCMonth() + 12);
  return limit.getTime() <= new Date(receivedOn + 'T00:00:00Z').getTime();
}

/** The approval state in force on a date, never a current flag. */
export async function approvalInForce(collector: string, on: string): Promise<any | null> {
  const rows = await query<any>(
    `select * from approval_periods
      where collector = $1 and valid_from <= $2 and valid_to >= $2
      order by valid_from desc limit 1`, [collector, on]);
  return rows[0] ?? null;
}

export async function collectorNameOn(collector: string, on: string): Promise<string> {
  const rows = await query<any>(
    `select name from party_versions where party = $1 and effective_from <= $2 order by effective_from desc limit 1`,
    [collector, on]);
  if (rows.length) return rows[0].name;
  const c = await query<any>(`select name from collectors where reference = $1`, [collector]);
  return c.length ? c[0].name : collector;
}

export async function decorateBatch(b: any): Promise<any> {
  const approval = await approvalInForce(b.collector, b.received_on);
  const custody = b.custody_links ?? (await query<any>(
    `select kind, occurred_on as date, party from custody_links where batch = $1 order by position`, [b.reference]));
  const missing = missingCustody(custody);
  const lapsed = calibrationLapsed(b.calibrated_on, b.received_on);
  let claimable = true, reason: string | null = null;
  if (!approval || !['approved', 'conditional'].includes(approval.state)) {
    claimable = false; reason = 'collector_approval_lapsed';
  } else if (missing.length) {
    claimable = false; reason = 'custody_link_missing';
  }
  const flags: string[] = [];
  if (lapsed) flags.push('lapsed_calibration');
  const accepted = b.accepted_g === null ? Number(b.net_g) : Number(b.accepted_g);
  const rejected = b.rejected_g === null ? 0 : Number(b.rejected_g);
  if (rejected > 0) flags.push('partial_rejection');
  return {
    reference: b.reference, collector: b.collector,
    collector_name: await collectorNameOn(b.collector, b.received_on),
    site: b.site, grade: b.grade, category: b.category,
    gross_g: Number(b.gross_g), tare_g: Number(b.tare_g), net_g: Number(b.net_g),
    moisture_bp: b.moisture_bp, moisture_method: b.moisture_method, device: b.device,
    device_calibrated_on: b.calibrated_on,
    received_on: b.received_on,
    dry_mass_g: dryMass(Number(b.net_g), b.moisture_bp),
    accepted_g: accepted, rejected_g: rejected,
    rejected_reason: b.rejected_reason ?? null, rejected_destination: b.rejected_destination ?? null,
    claimable, claimable_reason: reason,
    claimable_from: b.claimable_from ?? null,
    custody_complete: missing.length === 0, missing_custody_kinds: missing,
    custody,
    composition: b.composition ?? [], contamination: b.contamination ?? {},
    flags, state: b.state,
  };
}

export async function batchView(reference: string): Promise<any | null> {
  const rows = await query<any>(
    `select b.*, d.calibrated_on from batches b join devices d on d.reference = b.device
      where b.reference = $1`, [reference]);
  if (!rows.length) return null;
  return decorateBatch(rows[0]);
}

function runFlags(run: any): string[] {
  const f: string[] = [];
  if (run.state === 'closed' && run.within_tolerance === false) f.push('outside_tolerance');
  return f;
}

/** Forward genealogy: graph and nested text equivalent over the consumption records. */
export async function genealogy(lotRef: string): Promise<any> {
  const lots = await query<any>(`select * from lots`);
  const lotMap = new Map(lots.map((l) => [l.reference, l]));
  const target = lotMap.get(lotRef);
  if (!target) return null;

  const runs = await query<any>(`select * from runs`);
  const runMap = new Map(runs.map((r) => [r.reference, r]));
  const consumptions = await query<any>(`select * from consumptions`);
  const outputs = await query<any>(`select * from outputs`);
  const batches = await query<any>(
    `select b.*, d.calibrated_on from batches b join devices d on d.reference = b.device`);
  const outputsByRun = new Map<string, any[]>();
  for (const o of outputs) outputsByRun.set(o.run, [...(outputsByRun.get(o.run) ?? []), o]);
  const runProducing = new Map<string, any>();
  for (const o of outputs) runProducing.set(o.reference, runMap.get(o.run));

  const nodes = new Map<string, GraphNode>();
  const edges: GraphEdge[] = [];

  const addNode = (n: GraphNode) => {
    const existing = nodes.get(n.reference);
    if (!existing) { nodes.set(n.reference, n); return; }
    if (n.kind === 'batch') existing.mass_g = Math.max(existing.mass_g, n.mass_g);
  };
  const addEdge = (from: string, to: string, mass_g: number) => {
    const prior = edges.find((e) => e.from === from && e.to === to);
    if (prior) { prior.mass_g += mass_g; return; }
    edges.push({ from, to, mass_g });
  };

  const visitLot = async (ref: string) => {
    const l = lotMap.get(ref);
    if (!l) return;
    addNode({ kind: 'lot', reference: ref, mass_g: Number(l.mass_g), category_split: {}, flags: await lotInheritedFlags(ref) });
    if (l.blend_parents?.length) {
      for (const p of l.blend_parents) {
        addEdge(p.reference, ref, Number(p.mass_g));
        if (lotMap.has(p.reference)) await visitLot(p.reference);
        else await visitBatch(p.reference);
      }
      return;
    }
    const run = runMap.get(l.run);
    if (!run) return;
    addEdge(run.reference, ref, Number(l.mass_g));
    await visitRun(run.reference);
  };

  const visitRun = async (ref: string) => {
    const run = runMap.get(ref);
    if (!run) return;
    const ins = consumptions.filter((c) => c.run === ref);
    const totalIn = ins.reduce((s, c) => s + Number(c.mass_g), 0);
    addNode({ kind: 'run', reference: ref, mass_g: totalIn, category_split: {}, flags: runFlags(run) });
    for (const c of ins) {
      addEdge(c.input_reference, ref, Number(c.mass_g));
      if (c.input_kind === 'batch') await visitBatch(c.input_reference);
      else await visitOutput(c.input_reference);
    }
  };

  const visitOutput = async (ref: string) => {
    const out = outputs.find((o) => o.reference === ref);
    if (!out) return;
    addNode({
      kind: out.kind, reference: ref, mass_g: Number(out.mass_g), category_split: {},
      flags: out.kind === 'byproduct' ? ['byproduct_' + (out.disposition ?? 'unspecified')] : [],
    });
    const producer = runProducing.get(ref);
    if (producer) {
      addEdge(producer.reference, ref, Number(out.mass_g));
      await visitRun(producer.reference);
    }
  };

  const visitBatch = async (ref: string) => {
    const b = batches.find((x) => x.reference === ref);
    if (!b) return;
    const d = await decorateBatch(b);
    addNode({
      kind: 'batch', reference: ref, mass_g: d.dry_mass_g,
      category_split: d.claimable ? { [d.category]: d.dry_mass_g } : {},
      flags: [...d.flags, ...(d.claimable ? [] : ['non_claimable'])],
    });
  };

  await visitLot(lotRef);
  const nodeList = [...nodes.values()];
  const flagged = nodeList.some((n) => n.flags.length > 0);
  return {
    lot: lotRef,
    nodes: nodeList,
    edges,
    flagged,
    text_equivalent: textEquivalent(nodeList, edges, lotRef),
  };
}

/** Flags a lot inherits from every batch it descends from. */
export async function lotInheritedFlags(lotRef: string): Promise<string[]> {
  const consumptions = await query<any>(`select * from consumptions`);
  const outputs = await query<any>(`select * from outputs`);
  const lots = await query<any>(`select * from lots`);
  const lotMap = new Map(lots.map((l) => [l.reference, l]));
  const outputsByRun = new Map<string, any[]>();
  for (const o of outputs) outputsByRun.set(o.run, [...(outputsByRun.get(o.run) ?? []), o]);
  const seen = new Set<string>();
  const walk = (ref: string, kind: string) => {
    if (seen.has(ref)) return;
    seen.add(ref);
    if (kind === 'lot') {
      const l = lotMap.get(ref);
      if (!l) return;
      if (l.blend_parents?.length) {
        for (const p of l.blend_parents) walk(p.reference, lotMap.has(p.reference) ? 'lot' : 'batch');
        return;
      }
      for (const c of consumptions.filter((x) => x.run === l.run)) walk(c.input_reference, c.input_kind);
      return;
    }
    if (kind === 'intermediate' || kind === 'byproduct') {
      for (const c of consumptions.filter((x) => x.input_reference === ref)) walk(c.run, 'run');
      return;
    }
    if (kind === 'run') {
      for (const o of outputsByRun.get(ref) ?? []) walk(o.reference, o.kind);
    }
  };
  walk(lotRef, 'lot');
  const flags = new Set<string>();
  for (const ref of [...seen].filter((r) => r.startsWith('BATCH-'))) {
    const b = await batchView(ref);
    if (!b) continue;
    if (!b.claimable) {
      flags.add('non_claimable');
      if (b.claimable_reason === 'custody_link_missing') for (const k of b.missing_custody_kinds) flags.add('custody_missing_' + k);
    }
    for (const f of b.flags) flags.add(f);
  }
  return [...flags];
}

export function textEquivalent(nodes: GraphNode[], edges: GraphEdge[], root: string): any {
  const byRef = new Map(nodes.map((n) => [n.reference, n]));
  // The list descends upstream: for each node, the records that fed it.
  const incoming = new Map<string, GraphEdge[]>();
  for (const e of edges) incoming.set(e.to, [...(incoming.get(e.to) ?? []), e]);
  const seen = new Set<string>();
  const build = (ref: string): any => {
    const n = byRef.get(ref);
    const children = (incoming.get(ref) ?? [])
      .filter((e) => !seen.has(`${ref}<${e.from}`))
      .map((e) => {
        seen.add(`${ref}<${e.from}`);
        return { edge_mass_g: e.mass_g, ...(build(e.from) ?? {}) };
      });
    return n ? { kind: n.kind, reference: n.reference, mass_g: n.mass_g, category_split: n.category_split, flags: n.flags, contributes: children } : null;
  };
  return [build(root)];
}

/** Reverse traversal: every lot containing any of the batch, every certificate, every recipient. */
export async function batchImpact(batchRef: string): Promise<any> {
  const consumptions = await query<any>(`select * from consumptions`);
  const outputs = await query<any>(`select * from outputs`);
  const lots = await query<any>(`select * from lots`);
  const certs = await query<any>(`select * from certificates`);

  const outputsByRun = new Map<string, any[]>();
  for (const o of outputs) outputsByRun.set(o.run, [...(outputsByRun.get(o.run) ?? []), o]);
  const runsConsumingInput = new Map<string, string[]>();
  for (const c of consumptions) runsConsumingInput.set(c.input_reference, [...(runsConsumingInput.get(c.input_reference) ?? []), c.run]);

  const lotsReached = new Set<string>();
  const seen = new Set<string>();
  const walk = (ref: string, kind: string) => {
    if (seen.has(ref + kind)) return;
    seen.add(ref + kind);
    if (kind === 'batch') {
      for (const c of consumptions.filter((x) => x.input_reference === ref)) walk(c.run, 'run');
      return;
    }
    if (kind === 'lot') {
      // A lot output is addressed by its output reference; resolve the lot it became.
      const lot = lots.find((x) => x.reference === ref) ?? lots.find((x) => x.output === ref);
      if (lot) lotsReached.add(lot.reference);
      for (const l of lots.filter((x) => x.blend_parents?.some((p: any) => p.reference === ref))) walk(l.reference, 'lot');
      return;
    }
    if (kind === 'intermediate' || kind === 'byproduct') {
      for (const r of runsConsumingInput.get(ref) ?? []) walk(r, 'run');
      return;
    }
    if (kind === 'run') {
      for (const o of outputsByRun.get(ref) ?? []) walk(o.reference, o.kind);
    }
  };
  walk(batchRef, 'batch');

  const certRows = certs.filter((c) => (c.lots ?? []).some((l: any) => lotsReached.has(l.reference)));
  return {
    batch: batchRef,
    lots: lots.filter((l) => lotsReached.has(l.reference)).map((l) => ({
      reference: l.reference, mass_g: Number(l.mass_g), site: l.site, grade: l.grade, disposition: l.disposition,
    })),
    certificates: certRows.map((c) => ({
      number: c.number, version: c.version, site: c.site, state: c.state, claim_type: c.claim_type,
      content_bp: c.content_bp, recipient: c.recipient, recipient_name: c.recipient_name, signed_at: c.signed_at,
    })),
    recipients: [...new Set(certRows.map((c) => c.recipient_name))],
    read_at: new Date().toISOString(),
  };
}
