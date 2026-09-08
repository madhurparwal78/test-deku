import { useEffect, useState } from 'preact/hooks';
import { api, fmtGrams } from '../lib/api.js';
import { Link } from '../lib/link.jsx';
import { Banner, Empty, Loading, Field, StateWord, ContentFigure, MarkLock, setMeta } from '../components/ui.jsx';

export function BalancePeriod({ id }) {
  setMeta(`Ravel console — Balance ${id}`, 'Credits in, credits out and credits available, per category.');
  const [period, setPeriod] = useState(null);
  const [err, setErr] = useState(null);
  const [attempt, setAttempt] = useState({ phase: 'idle' });
  useEffect(() => { api(`/balance-periods/${id}`).then(setPeriod).catch((e) => setErr(e)); }, [id]);

  async function allocate(e) {
    e.preventDefault();
    const f = new FormData(e.target);
    setAttempt({ phase: 'sending' });
    try {
      const out = await api(`/balance-periods/${id}/allocations`, {
        method: 'POST',
        body: { lot: f.get('lot'), category: f.get('category'), mass_g: Number(f.get('mass_g')) },
      });
      setAttempt({ phase: 'done', out });
      const refreshed = await api(`/balance-periods/${id}`);
      setPeriod(refreshed);
    } catch (e2) {
      const refreshed = await api(`/balance-periods/${id}`).catch(() => period);
      setPeriod(refreshed);
      setAttempt({ phase: 'failed', err: e2 });
    }
  }

  if (err) return <div class="layout console" style="padding-top:2rem"><Banner title="No such period">{String(err.message)}</Banner></div>;
  if (!period) return <div class="layout console" style="padding-top:2rem"><Loading /></div>;
  const cats = ['post_consumer', 'pre_consumer'];
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <div class="spread">
        <h1 class="mono" style="font-size:var(--step-h3);line-height:var(--lh-h3)">{period.id}</h1>
        <p class="row">
          <StateWord>{period.state}</StateWord>
          {period.state === 'closed' ? <MarkLock /> : null}
        </p>
      </div>
      {period.state === 'closed' ? (
        <Banner title="This period is closed">Corrections require a restatement. Closed on {period.closed_on}, with a
          cut-off of {period.cut_off} after which a late event-time record no longer enters it.</Banner>
      ) : null}
      <div class="sheet table-scroll">
        <table>
          <caption class="label" style="text-align:left;padding-bottom:0.75rem">
            {period.site} · grade {period.grade} · {period.period} · allocation basis {period.allocation_basis}
          </caption>
          <thead><tr><th>Category</th><th class="num">Credits in, g</th><th class="num">Credits out, g</th><th class="num">Credits available, g</th></tr></thead>
          <tbody>
            {cats.map((c) => (
              <tr key={c}>
                <td>{c.replace(/_/g, ' ')}</td>
                <td class="mono num">{(period.credits_in_g[c] ?? 0).toLocaleString('en-GB')}</td>
                <td class="mono num">{(period.credits_out_g[c] ?? 0).toLocaleString('en-GB')}</td>
                <td class="mono num">{(period.credits_available_g[c] ?? 0).toLocaleString('en-GB')}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p class="small" style="color:var(--muted)">A balance is the sum of its movements and is never held as a total.
          Read at {period.derivation.read_at}. The two categories are never netted.</p>
      </div>
      {attempt.phase === 'done' ? (
        <Banner title={`Allocation ${attempt.out.reference} recorded`}>
          {fmtGrams(attempt.out.mass_g)} attached to {attempt.out.lot}. Content {attempt.out.content_bp / 100} per cent,
          claim type mass balance. Derivation: {attempt.out.derivation.formula}.
        </Banner>
      ) : null}
      {attempt.phase === 'failed' && attempt.err?.data?.error === 'insufficient_credits' ? (
        <Banner title="This allocation is refused">
          Available: {attempt.err.data.available_g.toLocaleString('en-GB')} g. Requested:{' '}
          {attempt.err.data.requested_g.toLocaleString('en-GB')} g. No credit has moved and the figures on this screen
          are unchanged.
        </Banner>
      ) : attempt.phase === 'failed' ? (
        <Banner title="The allocation was refused">{String(attempt.err?.data?.error ?? attempt.err?.message)}</Banner>
      ) : null}
      {period.state === 'open' ? (
        <form class="sheet stack" onSubmit={allocate} style="max-width:36rem">
          <p class="label">Attach claim to a lot</p>
          <div class="row" style="align-items:flex-end">
            <div style="flex:2;min-width:12rem"><Field label="Lot"><input name="lot" value="LOT-N6-0001" required /></Field></div>
            <div style="flex:1;min-width:10rem"><Field label="Category">
              <select name="category"><option value="post_consumer">post_consumer</option><option value="pre_consumer">pre_consumer</option></select>
            </Field></div>
            <div style="flex:1;min-width:9rem"><Field label="Mass, g"><input name="mass_g" type="number" step="1" required /></Field></div>
          </div>
          <div class="row"><button class="primary" type="submit" disabled={attempt.phase === 'sending'}>Allocate</button></div>
          <p class="small" style="color:var(--muted)">No route accepts a percentage. Every percentage is computed from
            the ledger, and an allocation that would breach the available credit is refused rather than warned about.</p>
        </form>
      ) : null}
      <div class="balance-grid">
        <div class="sheet">
          <p class="label">Conversion factors in force</p>
          {period.conversion_factors.map((f) => (
            <p class="small" key={f.reference}>
              <span class="mono">{f.reference}</span> at {f.factor_bp / 100} per cent{' '}
              {f.provisional ? <span class="state-word">provisional</span> : null} · window {f.derived_from ?? 'none'} to {f.derived_to ?? 'none'}
            </p>
          ))}
        </div>
        <div class="sheet">
          <p class="label">Three counts, none of them a badge</p>
          <p class="small">Overrides this period: {period.override_count}</p>
          <p class="small">Open restatements: {period.open_restatement_count}</p>
          <p class="small">Audit findings open: {period.open_finding_count}</p>
          <p class="small">Non-claimable input: {fmtGrams(period.non_claimable_input_g)}</p>
        </div>
        <div class="sheet">
          <p class="label">Inbound credits</p>
          {period.inbound_credits.length === 0 ? <Empty>No transfers into this period.</Empty> : period.inbound_credits.map((i) => (
            <p class="small" key={i.reference}>
              <span class="mono">{fmtGrams(i.mass_g)}</span> from {i.origin_site}, movement {i.movement}, fresh credit {String(i.fresh_credit)}
            </p>
          ))}
        </div>
      </div>
      {period.carried_forward_g ? (
        <div class="sheet">
          <p class="label">Closed with a carry-over</p>
          <p class="small">Carried forward: post-consumer {fmtGrams(period.carried_forward_g.post_consumer)}, pre-consumer {fmtGrams(period.carried_forward_g.pre_consumer)}.</p>
          <p class="small">Expired: post-consumer {fmtGrams(period.expired_g.post_consumer)}, pre-consumer {fmtGrams(period.expired_g.pre_consumer)}.</p>
        </div>
      ) : null}
    </div>
  );
}

export function BalanceList() {
  setMeta('Ravel console — Balance periods', 'The ledger, per site, grade and period.');
  const [rows, setRows] = useState(null);
  useEffect(() => { api('/balance-periods').then(setRows).catch(() => setRows([])); }, []);
  if (!rows) return <div class="layout console" style="padding-top:2rem"><Loading /></div>;
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">Balance periods</h1>
      {rows.length === 0 ? <Empty>There are no balance periods.</Empty> : (
        <div class="sheet table-scroll">
          <table>
            <thead><tr><th>Period</th><th>Site</th><th>Grade</th><th>State</th><th class="num">Post-consumer available, g</th><th class="num">Pre-consumer available, g</th></tr></thead>
            <tbody>
              {rows.map((p) => (
                <tr>
                  <td><Link class="mono" href={`/console/balance/${p.id}`}>{p.id}</Link></td>
                  <td class="mono">{p.site}</td><td>{p.grade}</td>
                  <td><StateWord>{p.state}</StateWord></td>
                  <td class="mono num">{(p.credits_available_g.post_consumer ?? 0).toLocaleString('en-GB')}</td>
                  <td class="mono num">{(p.credits_available_g.pre_consumer ?? 0).toLocaleString('en-GB')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
