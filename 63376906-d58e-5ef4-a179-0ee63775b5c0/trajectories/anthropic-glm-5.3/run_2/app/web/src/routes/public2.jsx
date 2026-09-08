import { useEffect, useState } from 'preact/hooks';
import { Reveal, Banner, Empty, Field, setMeta } from '../components/ui.jsx';

const TYPES = [
  ['waste_supply', 'Waste supply', 'feedstock@example.com', 3],
  ['polymer_purchase', 'Polymer purchase', 'sales@example.com', 2],
  ['partnership', 'Partnership', 'partners@example.com', 5],
  ['press', 'Press', 'press@example.com', 1],
];

export function Contact() {
  setMeta('Ravel — Contact', 'Four enquiry types, four destinations, four stated response times.');
  const [type, setType] = useState('waste_supply');
  const [state, setState] = useState({ phase: 'idle' });
  const dest = TYPES.find((t) => t[0] === type);

  async function submit(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    setState({ phase: 'sending' });
    try {
      const out = await api('/enquiries', {
        method: 'POST',
        body: {
          type,
          name: String(form.get('name') ?? ''),
          email: String(form.get('email') ?? ''),
          message: String(form.get('message') ?? ''),
        },
      });
      setState({ phase: 'done', out });
    } catch (err) {
      setState({ phase: 'failed', err });
    }
  }

  return (
    <div class="layout stack" style="padding-top:3rem">
      <Reveal as="h1">Contact</Reveal>
      <Reveal as="p" class="measure" delay={60}>
        Four enquiry types, four destinations, four stated response times. Whoever receives your data is named below,
        with what it is used for, how long it is kept and how to have it removed.
      </Reveal>
      <div class="sheet table-scroll">
        <table>
          <thead><tr><th>Type</th><th>Destination</th><th class="num">Response time, working days</th></tr></thead>
          <tbody>
            {TYPES.map(([key, label, destination, days]) => (
              <tr><td>{label}</td><td class="mono">{destination}</td><td class="mono num">{days}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <Reveal as="h2">Send an enquiry</Reveal>
      {state.phase === 'done' ? (
        <Banner title={`Enquiry ${state.out.reference} received`}>
          Your enquiry is with {state.out.destination}, who answer within {state.out.response_days} working days. You
          will receive one mail confirming the reference. Retention for this enquiry type is{' '}
          {type === 'waste_supply' ? 36 : type === 'polymer_purchase' ? 36 : type === 'press' ? 12 : 24} months, and
          you can ask for its removal at privacy@example.com.
        </Banner>
      ) : null}
      {state.phase === 'failed' ? (
        <Banner title="The enquiry could not be sent">
          What failed: the server refused the form ({String(state.err?.data?.error ?? state.err?.message)}). What you
          can do: check the fields and try again, or write to {dest[2]} directly — that address does not depend on this
          form working.
        </Banner>
      ) : null}
      <form class="sheet stack" onSubmit={submit} style="max-width:34rem">
        <Field label="Type">
          <select name="type" value={type} onChange={(e) => setType(e.target.value)}>
            {TYPES.map(([key, label]) => <option value={key}>{label}</option>)}
          </select>
        </Field>
        <Field label="Name"><input name="name" required /></Field>
        <Field label="Email"><input name="email" type="email" required /></Field>
        <Field label="Message"><textarea name="message" rows="4" required></textarea></Field>
        <p class="small" style="color:var(--muted)">
          Who receives this data: {dest[2]}. What it is used for: answering your enquiry and, where you asked for it,
          opening a record. How long it is kept: {type === 'waste_supply' ? 36 : type === 'polymer_purchase' ? 36 : type === 'press' ? 12 : 24} months.
          How to have it removed: privacy@example.com.
        </p>
        <div class="row">
          <button class="primary" type="submit" disabled={state.phase === 'sending'}>
            {state.phase === 'sending' ? 'Sending…' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
}

export function Privacy() {
  setMeta('Ravel — Privacy policy', 'Ravel Materials SAS is the controller. Retention is stated in months for every purpose.');
  return (
    <div class="layout stack measure" style="padding-top:3rem">
      <Reveal as="h1">Privacy policy</Reveal>
      <p>Ravel Materials SAS, 14 quai des Célestins, 69002 Lyon, France, is the controller for the data described
        below. A rights request goes to <span class="mono">privacy@example.com</span>. A disclosure goes to
        <span class="mono"> security@example.com</span>.</p>
      <h2>Retention, by purpose</h2>
      <div class="sheet table-scroll">
        <table>
          <thead><tr><th>Purpose</th><th class="num">Retention, months</th></tr></thead>
          <tbody>
            <tr><td>An enquiry</td><td class="mono num">24</td></tr>
            <tr><td>A waste-supply enquiry</td><td class="mono num">36</td></tr>
            <tr><td>A polymer enquiry</td><td class="mono num">36</td></tr>
            <tr><td>A press enquiry</td><td class="mono num">12</td></tr>
            <tr><td>An account and its acts</td><td class="mono num">120</td></tr>
            <tr><td>The record</td><td class="mono num">180</td></tr>
          </tbody>
        </table>
      </div>
      <h2>The operational record</h2>
      <p>The operational record names individuals — who booked a batch, who signed a certificate, who authorised an
        override. It is retained under a legal and scheme obligation, and it is not erased on request. A former
        employee's contact detail is.</p>
      <h2>Printing</h2>
      <p>This policy prints on A4 and on US Letter with no page break inside the retention table.</p>
    </div>
  );
}

export function Verify({ number }) {
  setMeta(`Ravel — Verify ${number}`, 'The public verification answer for a Ravel certificate.', { noindex: true });
  const [state, setState] = useState({ phase: 'loading' });
  useEffect(() => {
    let live = true;
    fetch(`/api/verify/${encodeURIComponent(number)}`)
      .then((res) => res.json())
      .then((data) => { if (live) setState({ phase: 'done', data }); })
      .catch((err) => { if (live) setState({ phase: 'failed', err }); });
    return () => { live = false; };
  }, [number]);
  if (state.phase !== 'done') {
    return (
      <div class="layout" style="padding-top:3rem">
        <p class="small">Loading the verification answer…</p>
      </div>
    );
  }
  const d = state.data;
  return (
    <div class="layout stack measure" style="padding-top:3rem">
      <p class="eyebrow">Certificate verification</p>
      <h1 class="mono" style="font-size:var(--step-h3);line-height:var(--lh-h3)">{number}</h1>
      {!d.found ? (
        <Banner title="There is no such certificate">
          No certificate with the number {number} has been issued by Ravel. This page does not list recipients, and it
          cannot be used to find one.
        </Banner>
      ) : (
        <div class="sheet stack">
          {d.state === 'withdrawn' ? (
            <Banner title="Withdrawn">
              This certificate was withdrawn on {d.withdrawn_on}. Reason: {d.withdrawal_reason}.
            </Banner>
          ) : null}
          <dl class="stack" style="gap:0.5rem;margin:0">
            <div class="spread"><dt class="label">State</dt><dd class="mono" style="margin:0">{d.state}</dd></div>
            <div class="spread"><dt class="label">Issued on</dt><dd class="mono" style="margin:0">{d.issued_on}</dd></div>
            {d.state === 'withdrawn' ? (
              <div class="spread"><dt class="label">Withdrawn on</dt><dd class="mono" style="margin:0">{d.withdrawn_on}</dd></div>
            ) : null}
            <div class="spread"><dt class="label">Site</dt><dd class="mono" style="margin:0">{d.site}</dd></div>
            <div class="spread"><dt class="label">Grade</dt><dd class="mono" style="margin:0">{d.grade}</dd></div>
            <div class="spread"><dt class="label">Claim type</dt><dd style="margin:0">{d.claim_type.replace(/_/g, ' ')}</dd></div>
            <div class="spread"><dt class="label">Recipient</dt><dd style="margin:0">{d.recipient_name}</dd></div>
          </dl>
          <p class="small" style="color:var(--muted)">
            A mass-balance certificate states that the material may not be described as physically containing recycled
            content. This page carries no yield, no collector, no genealogy and no carbon breakdown.
          </p>
        </div>
      )}
    </div>
  );
}
