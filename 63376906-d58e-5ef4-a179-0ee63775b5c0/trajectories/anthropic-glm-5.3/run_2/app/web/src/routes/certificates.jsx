import { useEffect, useState } from 'preact/hooks';
import { api, fmtGrams } from '../lib/api.js';
import { navigate } from '../lib/router.js';
import { Link } from '../lib/link.jsx';
import { Banner, Empty, Loading, Field, StateWord, ContentFigure, setMeta } from '../components/ui.jsx';

const CONDITION_LABELS = {
  lot_released: 'The lot is released',
  no_open_deviation: 'No deviation touching it is open',
  no_unreviewed_override: 'No override on it is unreviewed',
  period_closed: 'The bookkeeping period is closed',
  balance_invariant_holds: 'The balance invariant holds with the allocation applied',
  carbon_figure_complete: 'The carbon figure exists with all four components',
  signer_scope_valid: 'The signer holds signing scope for that site on the date of signing',
  signer_not_data_enterer: 'The signer did not enter the data',
};

function Conditions({ conditions }) {
  return (
    <ol class="stack" style="list-style:none;margin:0;padding:0;gap:0">
      {conditions.map((c) => (
        <li class="condition-row" key={c.condition}>
          <span class="label">{CONDITION_LABELS[c.condition] ?? c.condition}</span>
          <span class="small">
            {c.satisfied ? 'Satisfied. ' : <><span class="state-word">blocked</span>{' '}</>}
            {c.detail}
          </span>
          <span class="small">
            {c.satisfied ? null : (c.blocking_reference
              ? <Link href={resolveHref(c.condition, c.blocking_reference)}>resolve {c.blocking_reference}</Link>
              : null)}
          </span>
        </li>
      ))}
    </ol>
  );
}

function resolveHref(condition, ref) {
  if (condition === 'no_unreviewed_override') return '/console/record';
  if (condition === 'period_closed') return `/console/balance/${ref}`;
  if (condition === 'no_open_deviation') return '/console/record';
  if (condition === 'lot_released') return `/console/lots/${ref}`;
  if (condition === 'carbon_figure_complete') return `/console/lots/${ref}`;
  return '/console';
}

export function Certificates() {
  setMeta('Ravel console — Certificates', 'Issued certificates, with their states.');
  const [rows, setRows] = useState(null);
  useEffect(() => { api('/certificates').then(setRows).catch(() => setRows([])); }, []);
  if (!rows) return <div class="layout console" style="padding-top:2rem"><Loading /></div>;
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <div class="spread">
        <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">Certificates</h1>
        <Link class="button primary" href="/console/certificates/new/lot">Sign a certificate</Link>
      </div>
      {rows.length === 0 ? <Empty>There are no certificates.</Empty> : (
        <div class="sheet table-scroll">
          <table>
            <thead><tr><th>Number</th><th>Site</th><th>Lot</th><th>Recipient</th><th>Claim</th><th>State</th><th>Signed</th></tr></thead>
            <tbody>
              {rows.map((c) => (
                <tr key={c.number}>
                  <td><Link class="mono" href={`/console/certificates/${c.number}`}>{c.number}</Link></td>
                  <td class="mono">{c.site}</td>
                  <td class="mono small">{(c.lots ?? []).map((l) => l.reference).join(', ')}</td>
                  <td>{c.recipient_name}</td>
                  <td><ContentFigure content_bp={c.content_bp} claim_type={c.claim_type} compact /></td>
                  <td>
                    {c.state === 'withdrawn' ? <span><span class="state-word">withdrawn</span>{' '}</span> : null}
                    {c.state}
                    {c.provisional_factor ? <span class="state-word" style="margin-left:0.4rem">provisional factor</span> : null}
                  </td>
                  <td class="mono small">{String(c.signed_at).slice(0, 10)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export function CertDetail({ number }) {
  setMeta(`Ravel console — ${number}`, 'One certificate, every field derived.');
  const [cert, setCert] = useState(null);
  const [doc, setDoc] = useState(null);
  const [withdraw, setWithdraw] = useState({ phase: 'idle' });
  const [replay, setReplay] = useState(null);
  useEffect(() => {
    api(`/certificates/${number}`).then(setCert).catch(() => setCert(null));
    fetch(`/api/certificates/${number}/document`).then((r) => r.text()).then(setDoc).catch(() => setDoc(null));
  }, [number]);

  async function confirmWithdraw(e) {
    e.preventDefault();
    const f = new FormData(e.target);
    setWithdraw({ phase: 'sending' });
    try {
      const out = await api(`/certificates/${number}/withdraw`, { method: 'POST', body: { reason: f.get('reason') } });
      setWithdraw({ phase: 'done', out });
      const refreshed = await api(`/certificates/${number}`);
      setCert(refreshed);
    } catch (err) {
      setWithdraw({ phase: 'failed', err });
    }
  }

  async function runReplay() {
    try { setReplay(await api(`/certificates/${number}/replay`)); } catch (e) { setReplay({ error: e.data?.error ?? e.message }); }
  }

  if (!cert) return <div class="layout console" style="padding-top:2rem"><Loading /></div>;
  const blocking = cert.state !== 'withdrawn';
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <div class="spread">
        <h1 class="mono" style="font-size:var(--step-h3);line-height:var(--lh-h3)">{cert.number}</h1>
        <p>
          {cert.state === 'withdrawn' ? <span><span class="state-word">withdrawn</span>{' '}</span> : null}
          <StateWord>{cert.state}</StateWord>{cert.provisional_factor ? <span class="state-word">provisional factor</span> : null}
        </p>
      </div>
      {cert.state === 'withdrawn' ? (
        <Banner title="Withdrawn">
          This certificate was withdrawn on {cert.withdrawn_on}. Reason: {cert.withdrawal_reason}. The document stays
          readable at its address.
        </Banner>
      ) : null}
      <div class="sheet stack small">
        <div class="spread"><span class="label">Claim</span><span><ContentFigure content_bp={cert.content_bp} claim_type={cert.claim_type} /></span></div>
        <div class="spread"><span class="label">Site</span><span class="mono">{cert.site}</span></div>
        <div class="spread"><span class="label">Lots</span><span class="mono">{(cert.lots ?? []).map((l) => `${l.reference} ${l.mass_g} g`).join(', ')}</span></div>
        <div class="spread"><span class="label">Period</span><span class="mono">{cert.period}</span></div>
        <div class="spread"><span class="label">Carbon</span>
          <span>
            {cert.carbon ? <span class="mono">{Number(cert.carbon.value_mg_per_kg).toLocaleString('en-GB')} mg CO2e/kg</span> : '—'}
            {' '}<span class="label">{cert.carbon?.boundary} · {cert.method_version} · ±{cert.uncertainty_bp} bp</span>
          </span>
        </div>
        <div class="spread"><span class="label">Recipient</span><span>{cert.recipient_name}</span></div>
        <div class="spread"><span class="label">Verification address</span><Link class="mono" href={`/verify/${cert.number}`}>/verify/{cert.number}</Link></div>
        <div class="spread"><span class="label">Permitted statement</span><span>{cert.permitted_statement}</span></div>
        <div class="spread"><span class="label">Prohibited statement</span><span>{cert.prohibited_statement}</span></div>
      </div>
      <div class="row">
        <Link class="button" href={`/verify/${cert.number}`}>Public verification page</Link>
        <button onClick={runReplay}>Replay the figures</button>
      </div>
      {replay ? (
        <div class="sheet">
          <p class="label">Replay</p>
          <p class="small">
            Issued content {replay.issued.content_bp / 100} per cent; recomputed {replay.recomputed.content_bp / 100} per
            cent. {replay.agrees ? 'The figures agree.' : `The input that differs: ${replay.differing_input?.input}.`}
          </p>
          <p class="small">Input versions: conversion factor {replay.input_versions.conversion_factor ?? '—'}, method
            {replay.input_versions.carbon_method ?? '—'} v{replay.input_versions.carbon_method_version ?? '—'}.
            {replay.reproducible ? ' The figure is reproducible.' : ` Not reproducible: ${replay.reason}`}</p>
        </div>
      ) : null}
      {doc ? <div class="cert-document" aria-label="The certificate document, as plain text">{doc}</div> : null}
      {blocking && cert.state === 'issued' ? (
        <form class="sheet stack" onSubmit={confirmWithdraw} style="max-width:36rem">
          <p class="label">Withdraw this certificate</p>
          <p class="small">One action, five consequences:</p>
          <ol class="small" style="padding-left:1.25rem">
            <li>The state becomes withdrawn, with the reason, the person and the date.</li>
            <li>The recipient is notified through mail: <strong>{cert.recipient_name}</strong>.</li>
            <li>Every downstream statement the recipient was permitted to make becomes void.</li>
            <li>Every certificate derived from this one is identified and resolved.</li>
            <li>The reverse traversal of the underlying batches runs, so every other certificate touching them is enumerated.</li>
          </ol>
          <Field label="Reason"><input name="reason" required /></Field>
          <div class="row"><button type="submit" disabled={withdraw.phase === 'sending'}>{withdraw.phase === 'sending' ? 'Withdrawing…' : 'Confirm the withdrawal'}</button></div>
        </form>
      ) : null}
      {withdraw.phase === 'done' ? (
        <Banner title={`Certificate ${number} withdrawn`}>
          Recipients notified by name: {withdraw.out.notified_recipients.join(', ')}. Every downstream statement now void:
          <ul class="small" style="margin:0.5rem 0 0;padding-left:1.2rem">{withdraw.out.void_statements.map((s) => <li>{s}</li>)}</ul>
          <p class="small" style="margin-top:0.5rem">Certificates enumerated by the reverse traversal of the underlying
            batches: {withdraw.out.batch_traversal.length ? withdraw.out.batch_traversal.join(', ') : 'none besides this one'}.</p>
        </Banner>
      ) : null}
      {withdraw.phase === 'failed' ? <Banner title="The withdrawal was refused">{String(withdraw.err?.data?.error ?? withdraw.err?.message)}</Banner> : null}
    </div>
  );
}

const WIZARD_KEY = 'ravel.wizard';

function readWizard() { try { return JSON.parse(sessionStorage.getItem(WIZARD_KEY) ?? '{}'); } catch { return {}; } }
function writeWizard(w) { sessionStorage.setItem(WIZARD_KEY, JSON.stringify(w)); }

export function WizardStep({ step }) {
  setMeta('Ravel console — Sign a certificate', 'Four steps, four addresses, eight conditions.');
  const [lots, setLots] = useState(null);
  const [customers, setCustomers] = useState([]);
  const [preview, setPreview] = useState(null);
  const [sign, setSign] = useState({ phase: 'idle' });
  const [w, setW] = useState(readWizard());
  const me = (() => { try { return JSON.parse(sessionStorage.getItem('me') ?? 'null'); } catch { return null; } })();
  const steps = ['lot', 'claim', 'recipient', 'review'];
  const stepIndex = steps.indexOf(step);

  useEffect(() => {
    api('/lots').then(setLots).catch(() => setLots([]));
    api('/customers').then(setCustomers).catch(() => {});
  }, []);

  useEffect(() => {
    if (w.lot && w.recipient) {
      api('/certificates/preview', { method: 'POST', body: { lot: w.lot, recipient: w.recipient } })
        .then(setPreview).catch((e) => setPreview({ error: e.data?.error ?? e.message }));
    }
  }, [w.lot, w.recipient]);

  function set(patch) {
    const next = { ...w, ...patch };
    writeWizard(next);
    setW(next);
  }

  async function doSign(e) {
    e.preventDefault();
    const f = new FormData(e.target);
    setSign({ phase: 'signing' });
    try {
      const out = await api('/certificates', { method: 'POST', body: { lot: w.lot, recipient: w.recipient, password: f.get('password') } });
      setSign({ phase: 'done', out });
    } catch (err) {
      setSign({ phase: 'failed', err });
    }
  }

  if (sign.phase === 'done') {
    return (
      <div class="layout console stack" style="padding-top:2rem">
        <Banner title={`Certificate ${sign.out.number} signed`}>
          Version {sign.out.version} at site {sign.out.site}, claim type {sign.out.claim_type.replace(/_/g, ' ')},
          content {sign.out.content_bp / 100} per cent. The recipient files this document with their own regulator, and
          it resolves at <Link href={`/verify/${sign.out.number}`}>/verify/{sign.out.number}</Link>.
        </Banner>
        <Link class="button primary" href={`/console/certificates/${sign.out.number}`}>Open the certificate</Link>
      </div>
    );
  }

  return (
    <div class="layout console stack" style="padding-top:2rem">
      <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">Sign a certificate</h1>
      <ol class="row label" style="list-style:none;padding:0;margin:0">
        {steps.map((s, i) => (
          <li key={s}>
            <Link href={`/console/certificates/new/${s}`} style={{ 'font-weight': i === stepIndex ? 700 : 400 }}>
              {i + 1}. {s === 'lot' ? 'Choose the lot' : s === 'claim' ? 'The claim' : s === 'recipient' ? 'The recipient' : 'Review and sign'}
            </Link>
          </li>
        ))}
      </ol>

      {step === 'lot' ? (
        <div class="sheet stack">
          <p class="label">Step 1 — choose the lot</p>
          {lots === null ? <Loading /> : lots.length === 0 ? <Empty>There are no lots.</Empty> : (
            <table>
              <thead><tr><th>Lot</th><th>Site</th><th class="num">Mass</th><th>Disposition</th><th>Claim</th></tr></thead>
              <tbody>
                {lots.map((l) => (
                  <tr key={l.reference} style={{ cursor: 'pointer' }} onClick={() => { set({ lot: l.reference }); navigate('/console/certificates/new/claim'); }}>
                    <td class="mono">{l.reference}{w.lot === l.reference ? ' ✓' : ''}</td>
                    <td class="mono">{l.site}</td>
                    <td class="mono num">{l.mass_g.toLocaleString('en-GB')}</td>
                    <td>{l.disposition}</td>
                    <td><ContentFigure content_bp={l.content_bp} claim_type={l.claim_type} compact /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      ) : null}

      {step === 'claim' ? (
        <div class="sheet stack">
          <p class="label">Step 2 — the claim this certificate will carry</p>
          {lots === null ? <Loading /> : (
            (() => {
              const lot = lots.find((l) => l.reference === w.lot);
              return lot ? (
                <div class="stack small">
                  <div class="spread"><span class="label">Lot</span><span class="mono">{lot.reference}</span></div>
                  <div class="spread"><span class="label">Mass</span><span class="mono">{fmtGrams(lot.mass_g)}</span></div>
                  <div class="spread"><span class="label">Credit attached</span><span class="mono">{fmtGrams(lot.credit_attached_g)}</span></div>
                  <div class="spread"><span class="label">Recycled content, computed</span><span><ContentFigure content_bp={lot.content_bp} claim_type={lot.claim_type} /></span></div>
                  <div class="spread"><span class="label">Category split</span><span class="mono">{Object.entries(lot.category_split).map(([k, v]) => `${k} ${v / 100} %`).join(', ') || '—'}</span></div>
                  <div class="spread"><span class="label">Conversion factor</span><span class="mono">{lot.conversion_factor?.reference} at {lot.conversion_factor?.factor_bp / 100} %</span></div>
                  {lot.provisional_factor ? <Banner title="Provisional factor">A certificate issued on a provisional conversion factor carries provisional_factor true and says so.</Banner> : null}
                  {lot.overrides?.length ? (
                    <Banner title="Override on this lot">
                      Separation overridden by {lot.overrides[0].authorised_by} on {lot.overrides[0].authorised_on}.
                      This cannot be removed.
                    </Banner>
                  ) : null}
                </div>
              ) : <Empty>Choose a lot in step 1.</Empty>;
            })()
          )}
          <div class="row"><Link class="button primary" href="/console/certificates/new/recipient">Continue to the recipient</Link></div>
        </div>
      ) : null}

      {step === 'recipient' ? (
        <div class="sheet stack">
          <p class="label">Step 3 — the recipient</p>
          {customers.length === 0 ? <Loading /> : (
            <table>
              <thead><tr><th>Customer</th><th>Application</th><th>Industry</th><th>Holds specification</th></tr></thead>
              <tbody>
                {customers.map((cu) => (
                  <tr key={cu.reference} onClick={() => { set({ recipient: cu.reference }); navigate('/console/certificates/new/review'); }} style={{ cursor: 'pointer' }}>
                    <td class="mono">{cu.reference} — {cu.name}{w.recipient === cu.reference ? ' ✓' : ''}</td>
                    <td>{cu.application}</td><td>{cu.industry}</td>
                    <td class="mono small">{cu.holds_specification_version.specification} v{cu.holds_specification_version.version}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      ) : null}

      {step === 'review' ? (
        <div class="stack">
          <div class="sheet stack">
            <p class="label">Step 4 — the eight conditions as they stand</p>
            {preview === null ? <Loading /> : preview.error ? <Banner title="The preview was refused">{preview.error}</Banner> : (
              <>
                <Conditions conditions={preview.conditions} />
                <p class="small" style="color:var(--muted)">
                  None of the eight is waivable, no control on this screen dismisses one, and the same eight are
                  re-checked on the server at the moment of signing against the records as they stand then.
                </p>
                <p class="small">
                  {preview.blocking.length === 0
                    ? 'Every condition is satisfied.'
                    : `Blocked by: ${preview.blocking.join(', ')}. A lot whose conditions all held at a preview and which has since gained an open deviation is refused at signing, and the refusal names the condition that changed.`}
                </p>
              </>
            )}
          </div>
          {preview && !preview.error && preview.blocking.length === 0 ? (
            <form class="sheet stack" onSubmit={doSign} style="max-width:36rem">
              <p class="label">The document the recipient will read</p>
              <div class="cert-document small" style="max-height:18rem;overflow:auto">
                {`RAVEL MATERIALS — RECYCLED CONTENT CERTIFICATE\n\nCertificate: to be issued from the ${'SITE'} sequence\nLot: ${w.lot}\nRecipient: ${w.recipient}\nClaim type: mass balance\n\nThis material is claimed by mass balance. It is not physically segregated.\nYou may not state that this material physically contains recycled content.\n\nVerify this certificate at ravel.example.com/verify/{number}`}
              </div>
              <p class="small" style="color:var(--muted)">
                Signing is a separate, deliberate act. The recipient will file this document with their own regulator.
              </p>
              <Field label="Password (re-authentication for the signing act)">
                <input name="password" type="password" required />
              </Field>
              <div class="row"><button class="primary" type="submit" disabled={sign.phase === 'signing'}>{sign.phase === 'signing' ? 'Signing…' : 'Sign the certificate'}</button></div>
              {sign.phase === 'failed' ? (
                <Banner title="The signature was refused">
                  {String(sign.err?.data?.error ?? sign.err?.message)}
                  {sign.err?.data?.failing ? `. The condition that failed: ${sign.err.data.failing.join(', ')}.` : ''}
                </Banner>
              ) : null}
            </form>
          ) : null}
        </div>
      ) : null}

      {preview && !preview.error && step !== 'review' ? (
        <div class="sheet">
          <p class="label">The eight conditions so far</p>
          <Conditions conditions={preview.conditions} />
        </div>
      ) : null}
      <p class="small" style="color:var(--muted)">
        Signed in as {me?.email ?? 'unknown'} · sites {me?.sites?.join(', ')}
      </p>
    </div>
  );
}
