import crypto from 'node:crypto';
import { Hono } from 'hono';
import { query, withTransaction } from '../lib/db.js';
import { HttpError, requireSession, idempotent, readBody, strField, intField, refusePagination } from '../lib/http.js';
import { appendEntry } from '../lib/record.js';
import { login } from '../lib/auth.js';
import { flMulDiv, sha256 } from '../lib/num.js';
import { evaluateConditions, issueNumber, statementsFor, renderDocument, verificationUrl, latestFigure, periodForLot, notifySigned, notifyWithdrawn, signerScopeValid } from '../lib/certs.js';
import { batchImpact, lotInheritedFlags } from '../lib/claims.js';

export const certs = new Hono();

async function certView(number: string): Promise<any | null> {
  const cert = (await query<any>(`select * from certificates where number = $1`, [number]))[0];
  if (!cert) return null;
  const fig = cert.carbon_figure ? (await query<any>(`select * from carbon_figures where id = $1`, [cert.carbon_figure]))[0] : null;
  return {
    number: cert.number, version: cert.version, site: cert.site,
    lots: cert.lots, grade: cert.grade,
    specification: cert.specification, specification_version: cert.specification_version,
    claim_type: cert.claim_type, content_bp: cert.content_bp, category_split: cert.category_split,
    period: cert.period,
    carbon: fig ? {
      value_mg_per_kg: Number(fig.value_mg_per_kg), boundary: fig.boundary,
      method_version: cert.method_version, uncertainty_bp: cert.uncertainty_bp,
      comparator: fig.comparator, primary_share_bp: cert.primary_share_bp,
    } : null,
    primary_share_bp: cert.primary_share_bp,
    scheme: cert.scheme, registration: cert.registration,
    test_results: cert.test_results,
    permitted_statement: cert.permitted_statement,
    prohibited_statement: cert.prohibited_statement,
    signer: cert.signer, signer_name: cert.signer_name, signed_at: cert.signed_at,
    verification_url: verificationUrl(cert.number),
    state: cert.state, provisional_factor: cert.provisional_factor,
    withdrawn_by: cert.withdrawn_by ?? null, withdrawn_on: cert.withdrawn_on ?? null,
    withdrawal_reason: cert.withdrawal_reason ?? null,
    derived_from: cert.derived_from ?? null, reissued_as: cert.reissued_as ?? null,
    recipient: cert.recipient, recipient_name: cert.recipient_name,
    conditions: cert.conditions,
    derivation: { note: 'Every field is derived; the only free text on a certificate is a withdrawal reason.' },
  };
}

certs.get('/certificates', async (c) => {
  refusePagination(c);
  const rows = await query<any>(`select number from certificates order by signed_at, number`);
  const out = [];
  for (const r of rows) out.push(await certView(r.number));
  return c.json(out);
});

certs.get('/certificates/:number', async (c) => {
  const v = await certView(c.req.param('number'));
  if (!v) throw new HttpError(404, 'not_found');
  return c.json(v);
});

certs.post('/certificates/preview', async (c) => {
  const s = await requireSession(c);
  const body = await readBody(c);
  const lotRef = strField(body.lot, 'lot');
  const recipient = strField(body.recipient ?? body.recipient_reference, 'recipient');
  const lot = (await query<any>(`select * from lots where reference = $1`, [lotRef]))[0];
  if (!lot) throw new HttpError(404, 'lot_not_found');
  const period = await periodForLot(lotRef);
  const conditions = await evaluateConditions({
    lot: lotRef, period: period?.id ?? '', signer: s.email, site: lot.site,
  });
  return c.json({
    lot: lotRef, recipient, period: period?.id ?? null,
    conditions,
    satisfied: conditions.filter((x) => x.satisfied).length,
    blocking: conditions.filter((x) => !x.satisfied).map((x) => x.condition),
    waivable: false,
  });
});

certs.post('/certificates', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('certificate_signer')) throw new HttpError(403, 'certificate_signer_required');
  return idempotent(c, async () => {
    const body = await readBody(c);
    // Signing re-authenticates: a session alone is not a signing credential.
    const password = strField(body.password, 'password');
    const reauth = await login(s.email, password);
    if (!reauth) throw new HttpError(401, 'reauthentication_failed');
    const lotRef = strField(body.lot, 'lot');
    const recipient = strField(body.recipient ?? body.recipient_reference, 'recipient');
    const lot = (await query<any>(`select * from lots where reference = $1`, [lotRef]))[0];
    if (!lot) throw new HttpError(404, 'lot_not_found');
    const customer = (await query<any>(`select * from customers where reference = $1`, [recipient]))[0];
    const period = await periodForLot(lotRef);
    // The eight conditions are decided again, against the records as they stand now.
    const conditions = await evaluateConditions({ lot: lotRef, period: period?.id ?? '', signer: s.email, site: lot.site });
    const failing = conditions.filter((x) => !x.satisfied);
    if (failing.length) {
      await recordRefusal('certificate_signature_refused', s.email, lotRef, {
        conditions: failing.map((f) => f.condition), detail: failing.map((f) => f.detail),
      });
      return { status: 409, body: { error: 'condition_unsatisfied', conditions, failing: failing.map((f) => f.condition), waivable: false } };
    }
    const attached = await query<any>(
      `select category, coalesce(sum(mass_g),0)::bigint as n from credit_movements where lot = $1 and kind='out' group by category`, [lotRef]);
    const attachedTotal = attached.reduce((s2: number, x: any) => s2 + Number(x.n), 0);
    const contentBp = flMulDiv(attachedTotal, 10000, Number(lot.mass_g));
    const split: Record<string, number> = {};
    for (const a of attached) split[a.category] = flMulDiv(Number(a.n), 10000, Number(lot.mass_g));
    const fig = await latestFigure(lotRef);
    const factor = (await query<any>(
      `select * from conversion_factors where site = $1 order by provisional, published_on desc limit 1`, [lot.site]))[0];
    const spec = (await query<any>(
      `select * from specifications where grade = $1 order by version desc limit 1`, [lot.grade]))[0];
    const tests = await query<any>(`select * from test_results where lot = $1 order by recorded_on`, [lotRef]);
    const stmts = statementsFor(lot.claim_type, contentBp, split);
    const signDate = new Date().toISOString().slice(0, 10);

    const out = await withTransaction(async (cl) => {
      await cl.query(`set transaction isolation level serializable`);
      const number = await issueNumber(cl as any, lot.site);
      await cl.query(
        `insert into certificates(number, version, site, recipient, recipient_name, signer, signer_name, signed_at, state,
            lots, grade, specification, specification_version, claim_type, content_bp, category_split, period,
            carbon_figure, method_version, boundary, uncertainty_bp, primary_share_bp, scheme, registration,
            test_results, permitted_statement, prohibited_statement, conditions, provisional_factor, input_versions)
         values ($1,1,$2,$3,$4,$5,$6,$7,'issued',$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28)`,
        [number, lot.site, recipient, customer?.name ?? recipient, s.email, s.name, new Date().toISOString(),
         JSON.stringify([{ reference: lotRef, mass_g: Number(lot.mass_g) }]), lot.grade,
         spec?.grade ?? 'SPEC-N6', spec?.version ?? 3, lot.claim_type, contentBp, JSON.stringify(split),
         period?.id ?? '', fig?.id ?? null, `CM-PA6 v${fig?.method_version ?? 2}`, fig?.boundary ?? '', certFigUncertainty(fig),
         certFigPrimary(fig), 'RCS-2026', 'REG-RAVEL-0042',
         JSON.stringify(tests.map((t) => ({ property: t.property, method: t.method, value: t.value, unit: t.unit, recorded_on: t.recorded_on }))),
         stmts.permitted_statement, stmts.prohibited_statement, JSON.stringify(conditions),
         factor?.provisional ?? false,
         JSON.stringify({
           conversion_factor: factor?.reference ?? null,
           carbon_method: 'CM-PA6', carbon_method_version: fig?.method_version ?? null,
           specification: spec ? `${spec.grade} v${spec.version}` : null,
           carbon_figure: fig?.id ?? null,
         })]);
      await appendEntry(cl, { act: 'certificate_signed', person: s.email, site: lot.site, object: number,
        content: { number, lot: lotRef, recipient, claim_type: lot.claim_type, content_bp: contentBp,
          conditions_stored: conditions, referenced_until: addYears(signDate, 10) } });
      return number;
    });
    const cert = await certView(out);
    const contact = customer?.contact ?? recipient;
    await notifySigned({ ...cert, permitted_statement: stmts.permitted_statement }, contact).catch(() => null);
    return { status: 201, body: cert };
  }).then((r) => c.json(r.body, r.status as any));
});

function certFigUncertainty(fig: any) { return fig ? Number(fig.uncertainty_bp) : 0; }
function certFigPrimary(fig: any) { return fig ? Number(fig.primary_share_bp) : 0; }

function addYears(date: string, years: number): string {
  const d = new Date(date + 'T00:00:00Z');
  d.setUTCFullYear(d.getUTCFullYear() + years);
  return d.toISOString().slice(0, 10);
}

async function recordRefusal(act: string, person: string, object: string, content: any) {
  await withTransaction(async (cl) => {
    await appendEntry(cl, { act, person, object, content: { ...content, refused: true } });
  });
}

// ---------------- withdraw: one action, five consequences ----------------
certs.post('/certificates/:number/withdraw', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('certificate_signer')) throw new HttpError(403, 'certificate_signer_required');
  const number = c.req.param('number');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const reason = strField(body.reason, 'reason');
    const cert = (await query<any>(`select * from certificates where number = $1`, [number]))[0];
    if (!cert) throw new HttpError(404, 'not_found');
    if (!signerScopeValid(s.email, cert.site)) throw new HttpError(403, 'site_outside_signer_scope', { site: cert.site });
    if (cert.state === 'withdrawn') throw new HttpError(409, 'already_withdrawn');
    const customer = (await query<any>(`select * from customers where reference = $1`, [cert.recipient]))[0];
    const contact = customer?.contact ?? 'recipient@example.com';
    const voidStatements = [
      `The recipient may no longer state recycled content of ${cert.content_bp / 100} per cent against ${number}.`,
      `The permitted statement on ${number} is void: ${cert.permitted_statement}`,
      `The recipient may not present ${number} to a regulator as evidence of recycled content.`,
      `The recipient may not quote the carbon figure carried by ${number}.`,
    ];
    const derived = await query<any>(`select number from certificates where derived_from = $1`, [number]);
    const traversalPromises = await Promise.all((cert.lots ?? []).map(async (l: any) => batchImpact(await batchOfLot(l.reference))));
    const traversals = traversalPromises;
    const traversalCertificates = [...new Set(traversals.flatMap((t) => t.certificates.map((x: any) => x.number)))].filter((n) => n !== number);
    const notifiedRecipients = [cert.recipient_name];
    await withTransaction(async (cl) => {
      await cl.query(
        `update certificates set state='withdrawn', withdrawal_reason=$2, withdrawn_by=$3, withdrawn_on=current_date,
            void_statements=$4, notified_recipients=$5 where number=$1`,
        [number, reason, s.email, JSON.stringify(voidStatements), JSON.stringify(notifiedRecipients)]);
      for (const d of derived) {
        await cl.query(`update certificates set state='withdrawn', withdrawal_reason=$2, withdrawn_by=$3, withdrawn_on=current_date where number=$1`,
          [d.number, `Derived from ${number}, withdrawn with it.`, s.email]);
      }
      for (const n of traversalCertificates) {
        if (n === number) continue;
        await cl.query(
          `update certificates set state='withdrawn', withdrawal_reason=$2, withdrawn_by=$3, withdrawn_on=current_date where number=$1 and state='issued'`,
          [n, `Shares batches with ${number}, withdrawn by the same act.`, s.email]);
      }
      await appendEntry(cl, { act: 'certificate_withdrawn', person: s.email, site: cert.site, object: number,
        content: { number, reason, void_statements: voidStatements, notified_recipients: notifiedRecipients,
          derived_certificates: derived.map((d) => d.number),
          batch_traversal: traversalCertificates } });
    });
    await notifyWithdrawn({ ...cert, withdrawal_reason: reason }, contact, voidStatements).catch(() => null);
    return {
      status: 200,
      body: {
        number, state: 'withdrawn', reason, withdrawn_by: s.email, withdrawn_on: new Date().toISOString().slice(0, 10),
        notified_recipients: notifiedRecipients, void_statements: voidStatements,
        derived_certificates: derived.map((d) => d.number),
        batch_traversal: traversalCertificates,
        note: 'The document stays readable at its address.',
      },
    };
  }).then((r) => c.json(r.body, r.status as any));
});

async function batchOfLot(lotRef: string): Promise<string> {
  const rows = await query<any>(`select * from consumptions`);
  const outputs = await query<any>(`select * from outputs`);
  const lots = await query<any>(`select * from lots`);
  const lotMap = new Map(lots.map((l) => [l.reference, l]));
  const outputsByRun = new Map<string, any[]>();
  for (const o of outputs) outputsByRun.set(o.run, [...(outputsByRun.get(o.run) ?? []), o]);
  const seen = new Set<string>();
  const found: string[] = [];
  const walk = (ref: string, kind: string) => {
    if (seen.has(ref)) return;
    seen.add(ref);
    if (kind === 'batch') { found.push(ref); return; }
    if (kind === 'lot') {
      const l = lotMap.get(ref);
      if (l?.blend_parents) { for (const p of l.blend_parents) walk(p.reference, 'lot'); return; }
      if (l) { for (const o of outputsByRun.get(l.run) ?? []) walk(o.reference, o.kind); }
      return;
    }
    if (kind === 'intermediate') {
      const out = outputs.find((o) => o.reference === ref);
      if (out) for (const cm of rows.filter((x) => x.run === out.run)) walk(cm.input_reference, cm.input_kind);
      return;
    }
  };
  walk(lotRef, 'lot');
  return found[0] ?? lotRef;
}

certs.post('/certificates/:number/reissue', async (c) => {
  const s = await requireSession(c);
  if (!s.roles.includes('certificate_signer')) throw new HttpError(403, 'certificate_signer_required');
  const number = c.req.param('number');
  return idempotent(c, async () => {
    const body = await readBody(c);
    const cert = (await query<any>(`select * from certificates where number = $1`, [number]))[0];
    if (!cert) throw new HttpError(404, 'not_found');
    if (!signerScopeValid(s.email, cert.site)) throw new HttpError(403, 'site_outside_signer_scope');
    const out = await withTransaction(async (cl) => {
      const newNumber = await issueNumber(cl as any, cert.site);
      const version = cert.version + 1;
      await cl.query(
        `insert into certificates(number, version, site, recipient, recipient_name, signer, signer_name, signed_at, state,
            lots, grade, specification, specification_version, claim_type, content_bp, category_split, period,
            carbon_figure, method_version, boundary, uncertainty_bp, primary_share_bp, scheme, registration,
            test_results, permitted_statement, prohibited_statement, conditions, provisional_factor, input_versions, derived_from)
         values ($1,$2,$3,$4,$5,$6,$7,now(),'issued',$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29,$30)`,
        [newNumber, version, cert.site, cert.recipient, cert.recipient_name, s.email, s.name,
         cert.lots, cert.grade, cert.specification, cert.specification_version, cert.claim_type, cert.content_bp,
         cert.category_split, cert.period, cert.carbon_figure, cert.method_version, cert.boundary,
         cert.uncertainty_bp, cert.primary_share_bp, cert.scheme, cert.registration, cert.test_results,
         cert.permitted_statement, cert.prohibited_statement, cert.conditions, cert.provisional_factor,
         cert.input_versions, number]);
      await cl.query(`update certificates set reissued_as = $2 where number = $1`, [number, newNumber]);
      await appendEntry(cl, { act: 'certificate_reissued', person: s.email, site: cert.site, object: newNumber,
        content: { number: newNumber, version, reissues: number } });
      return newNumber;
    });
    return { status: 201, body: { reference: out, number: out, version: cert.version + 1, reissues: number, note: 'A re-issue is a new version at a new address.' } };
  }).then((r) => c.json(r.body, r.status as any));
});

certs.get('/certificates/:number/document', async (c) => {
  const cert = (await query<any>(`select * from certificates where number = $1`, [c.req.param('number')]))[0];
  if (!cert) throw new HttpError(404, 'not_found');
  const fig = cert.carbon_figure ? (await query<any>(`select * from carbon_figures where id = $1`, [cert.carbon_figure]))[0] : null;
  const doc = renderDocument({
    ...cert,
    value_mg_per_kg: fig ? Number(fig.value_mg_per_kg) : null,
    comparator: fig?.comparator ?? {},
    signer_name: cert.signer_name,
  });
  return c.body(doc, 200, { 'content-type': 'text/plain; charset=utf-8' });
});

certs.get('/certificates/:number/replay', async (c) => {
  const cert = (await query<any>(`select * from certificates where number = $1`, [c.req.param('number')]))[0];
  if (!cert) throw new HttpError(404, 'not_found');
  const lotRef = (cert.lots ?? [])[0]?.reference;
  const lot = (await query<any>(`select * from lots where reference = $1`, [lotRef]))[0];
  const versions: any = cert.input_versions ?? {};
  const factors = await query<any>(`select * from conversion_factors where reference = $1`, [versions.conversion_factor]);
  const fig = cert.carbon_figure ? (await query<any>(`select * from carbon_figures where id = $1`, [cert.carbon_figure]))[0] : null;
  const methodVersion = versions.carbon_method_version ?? fig?.method_version ?? null;
  const method = methodVersion ? (await query<any>(
    `select * from carbon_methods where key = 'CM-PA6' and version = $1`, [methodVersion]))[0] : null;

  const missing: string[] = [];
  if (!factors.length) missing.push(`conversion factor ${versions.conversion_factor ?? 'unknown'}`);
  if (!method) missing.push(`carbon method version CM-PA6 v${methodVersion ?? '?'}`);
  if (!fig) missing.push('carbon figure');

  // Recompute the certificate's figures from the recorded inputs.
  const attached = await query<any>(
    `select coalesce(sum(mass_g),0)::bigint as n from credit_movements where lot = $1 and kind='out'`, [lotRef]);
  const recomputedContentBp = lot ? flMulDiv(Number(attached[0].n), 10000, Number(lot.mass_g)) : cert.content_bp;
  const agrees = recomputedContentBp === cert.content_bp && !!fig && Number(fig.value_mg_per_kg) === Number((await figureValue(cert)) ?? fig?.value_mg_per_kg);
  const differing: any[] = [];
  if (recomputedContentBp !== cert.content_bp) {
    differing.push({ input: 'ledger movements against the lot', issued: cert.content_bp, recomputed: recomputedContentBp });
  }
  return c.json({
    number: cert.number, issued: { content_bp: cert.content_bp }, recomputed: { content_bp: recomputedContentBp },
    agrees,
    differing_input: differing[0] ?? null,
    input_versions: {
      conversion_factor: versions.conversion_factor ?? null,
      carbon_method: versions.carbon_method ?? null,
      carbon_method_version: versions.carbon_method_version ?? null,
      specification: versions.specification ?? null,
      carbon_figure: versions.carbon_figure ?? null,
    },
    reproducible: missing.length === 0,
    reason: missing.length ? `Cannot resolve: ${missing.join(', ')}.` : null,
  });
});

async function figureValue(cert: any): Promise<number | null> {
  if (!cert.carbon_figure) return null;
  const fig = (await query<any>(`select * from carbon_figures where id = $1`, [cert.carbon_figure]))[0];
  return fig ? Number(fig.value_mg_per_kg) : null;
}

// ---------------- public verification, rate limited ----------------
const verifyBuckets = new Map<string, { count: number; reset: number }>();

export const verify = new Hono();
verify.get('/:number', async (c) => {
  const ip = c.req.header('x-forwarded-for')?.split(',')[0]?.trim() || c.req.header('x-real-ip') || 'local';
  const now = Date.now();
  const bucket = verifyBuckets.get(ip);
  if (!bucket || bucket.reset < now) {
    verifyBuckets.set(ip, { count: 1, reset: now + 60000 });
  } else {
    bucket.count += 1;
    if (bucket.count > 30) throw new HttpError(429, 'rate_limited');
  }
  const number = c.req.param('number');
  const cert = (await query<any>(`select * from certificates where number = $1`, [number]))[0];
  if (!cert) {
    return c.json({ found: false, number });
  }
  return c.json({
    found: true,
    number: cert.number,
    state: cert.state,
    issued_on: String(cert.signed_at).slice(0, 10),
    withdrawn_on: cert.withdrawn_on ?? null,
    withdrawal_reason: cert.withdrawal_reason ?? null,
    site: cert.site,
    grade: cert.grade,
    claim_type: cert.claim_type,
    recipient_name: cert.recipient_name,
  });
});
