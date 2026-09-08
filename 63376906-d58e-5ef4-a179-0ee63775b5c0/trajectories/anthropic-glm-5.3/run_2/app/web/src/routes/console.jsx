import { useEffect, useState } from 'preact/hooks';
import { api, fmtGrams, fmtBp } from '../lib/api.js';
import { navigate } from '../lib/router.js';
import { Link } from '../lib/link.jsx';
import { Reveal, Banner, Empty, Loading, Field, StateWord, ContentFigure, MarkLock, MarkFlag, MarkArrow, MarkWarning, setMeta } from '../components/ui.jsx';

const STAGES = ['dissolution', 'depolymerisation', 'purification', 'repolymerisation'];

export function ConsoleBoard() {
  setMeta('Ravel console — Run board', 'One column per process stage and one card per run.');
  const [runs, setRuns] = useState(null);
  const [err, setErr] = useState(null);
  useEffect(() => { api('/runs').then(setRuns).catch((e) => setErr(e)); }, []);
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <div class="spread">
        <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">Run board</h1>
        <p class="small" style="color:var(--muted)">The console reads what a run did, after the run.</p>
      </div>
      {err ? <Banner title="The board could not be read">{String(err.message)}</Banner> : null}
      {runs === null ? <Loading /> : runs.length === 0 ? <Empty>There are no runs.</Empty> : (
        <div class="board">
          {STAGES.map((stage) => (
            <section aria-label={stage}>
              <p class="label" style="margin-bottom:0.75rem">{stage}</p>
              <div class="stack" style="gap:0.75rem">
                {runs.filter((r) => r.run_type === stage).length === 0
                  ? <Empty>No runs at this stage.</Empty>
                  : runs.filter((r) => r.run_type === stage).map((r) => (
                    <Link href={`/console/runs/${r.reference}`} class="run-card" style="text-decoration:none;display:block">
                      <p class="mono" style="margin:0 0 0.25rem">{r.reference}</p>
                      <p class="small" style="margin:0">{fmtGrams(r.mass_in_g)} in · {fmtGrams(r.mass_out_g)} out</p>
                      <p class="small" style="margin:0.25rem 0 0">
                        <span class="state-word">{r.state}</span>{' '}
                        {r.losses_g !== null ? <span class="mono small">losses {fmtGrams(r.losses_g)}</span> : null}
                      </p>
                      <p class="label" style="margin:0.5rem 0 0">stage: {r.run_type}</p>
                    </Link>
                  ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}

export function Intake() {
  setMeta('Ravel console — Feedstock intake', 'Book in a batch, record mass, contamination and custody.');
  const [batches, setBatches] = useState(null);
  const [state, setState] = useState({ phase: 'idle' });
  const [collectors, setCollectors] = useState([]);
  const load = () => api('/batches').then(setBatches).catch(() => setBatches([]));
  useEffect(() => { load(); api('/collectors').then(setCollectors).catch(() => {}); }, []);

  async function submit(e) {
    e.preventDefault();
    const f = new FormData(e.target);
    const body = {
      collector: f.get('collector'), site: f.get('site'), category: f.get('category'),
      gross_g: Number(f.get('gross_g')), tare_g: Number(f.get('tare_g')), net_g: Number(f.get('net_g')),
      moisture_bp: Number(f.get('moisture_bp')), moisture_method: f.get('moisture_method'),
      device: f.get('device'), received_on: f.get('received_on'),
      composition: [{ polymer: f.get('polymer'), fraction_bp: Number(f.get('fraction_bp')), basis: 'declared' }],
      contamination: { non_nylon_bp: Number(f.get('non_nylon_bp')), elastane_bp: Number(f.get('elastane_bp')), coatings: f.get('coatings'), colour_load: f.get('colour_load'), foreign_matter: f.get('foreign_matter') },
      custody: [
        { kind: 'collection_site', date: f.get('received_on'), party: f.get('collector') },
        { kind: 'collector', date: f.get('received_on'), party: f.get('collector') },
        { kind: 'transport', date: f.get('received_on'), party: f.get('collector') },
        { kind: 'arrival', date: f.get('received_on'), party: f.get('site') },
        { kind: 'weighing', date: f.get('received_on'), party: f.get('device') },
        { kind: 'acceptance', date: f.get('received_on'), party: f.get('site') },
      ],
    };
    setState({ phase: 'sending' });
    try {
      const out = await api('/batches', { method: 'POST', body });
      setState({ phase: 'done', out });
      load();
    } catch (err) {
      setState({ phase: 'failed', err });
    }
  }

  return (
    <div class="layout console stack" style="padding-top:2rem">
      <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">Feedstock intake</h1>
      <p class="small measure" style="color:var(--muted)">Category is required at intake, has no default, and can never
        be changed after acceptance. Every figure is computed on dry mass.</p>
      {state.phase === 'done' ? <Banner title={`Batch ${state.out.reference} booked in`}>Dry mass {fmtGrams(state.out.dry_mass_g)}. Claimable: {String(state.out.claimable)}. {state.out.claimable_reason ? `Reason: ${state.out.claimable_reason}.` : ''}</Banner> : null}
      {state.phase === 'failed' ? <Banner title="The batch was refused">{String(state.err?.data?.error ?? state.err?.message)} — {state.err?.data?.rule ?? 'correct the fields named in the refusal and submit again.'}</Banner> : null}
      <form class="sheet stack" onSubmit={submit} style="max-width:40rem">
        <div class="row" style="align-items:flex-end">
          <div style="flex:1;min-width:12rem"><Field label="Collector">
            <select name="collector">{collectors.map((c) => <option value={c.reference}>{c.reference} — {c.name}</option>)}</select>
          </Field></div>
          <div style="flex:1;min-width:10rem"><Field label="Site">
            <select name="site"><option value="SITE-DEMO">SITE-DEMO</option><option value="SITE-PILOT">SITE-PILOT</option></select>
          </Field></div>
          <div style="flex:1;min-width:10rem"><Field label="Category (no default)">
            <select name="category" required><option value="">choose a category</option><option value="post_consumer">post_consumer</option><option value="pre_consumer">pre_consumer</option></select>
          </Field></div>
        </div>
        <div class="row">
          <div style="flex:1"><Field label="Gross, g"><input name="gross_g" type="number" step="1" required /></Field></div>
          <div style="flex:1"><Field label="Tare, g"><input name="tare_g" type="number" step="1" required /></Field></div>
          <div style="flex:1"><Field label="Net, g"><input name="net_g" type="number" step="1" required /></Field></div>
          <div style="flex:1"><Field label="Moisture, bp"><input name="moisture_bp" type="number" step="1" required /></Field></div>
        </div>
        <div class="row">
          <div style="flex:1"><Field label="Moisture method"><input name="moisture_method" value="ISO 15512" /></Field></div>
          <div style="flex:1"><Field label="Device"><select name="device"><option>WB-DEMO-01</option><option>WB-DEMO-02</option></select></Field></div>
          <div style="flex:1"><Field label="Received on"><input name="received_on" type="date" required /></Field></div>
        </div>
        <div class="row">
          <div style="flex:1"><Field label="Polymer"><input name="polymer" value="PA6" /></Field></div>
          <div style="flex:1"><Field label="Declared fraction, bp"><input name="fraction_bp" type="number" step="1" value="9200" /></Field></div>
        </div>
        <div class="row">
          <div style="flex:1"><Field label="Non-nylon, bp"><input name="non_nylon_bp" type="number" step="1" value="500" /></Field></div>
          <div style="flex:1"><Field label="Elastane, bp"><input name="elastane_bp" type="number" step="1" value="300" /></Field></div>
          <div style="flex:1"><Field label="Coatings"><input name="coatings" value="none" /></Field></div>
          <div style="flex:1"><Field label="Colour load"><input name="colour_load" value="medium" /></Field></div>
          <div style="flex:1"><Field label="Foreign matter"><input name="foreign_matter" value="low" /></Field></div>
        </div>
        <div class="row"><button class="primary" type="submit" disabled={state.phase === 'sending'}>{state.phase === 'sending' ? 'Booking…' : 'Book in the batch'}</button></div>
      </form>
      <h2>Batch register</h2>
      {batches === null ? <Loading /> : batches.length === 0 ? <Empty>There are no batches.</Empty> : (
        <div class="sheet table-scroll">
          <table>
            <thead><tr><th>Batch</th><th>Collector</th><th>Category</th><th class="num">Received</th><th class="num">Dry mass</th><th>Claimable</th><th>Flags</th></tr></thead>
            <tbody>
              {batches.map((b) => (
                <tr>
                  <td class="mono">{b.reference}</td>
                  <td>{b.collector_name}</td>
                  <td>{b.category.replace(/_/g, ' ')}</td>
                  <td class="mono num">{b.received_on}</td>
                  <td class="mono num">{b.dry_mass_g.toLocaleString('en-GB')}</td>
                  <td>{b.claimable ? 'claimable' : <span><span class="state-word">non-claimable</span> {b.claimable_reason}</span>}</td>
                  <td>{b.flags.length ? <MarkWarning label={b.flags.join(', ')} /> : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export function RunDetail({ reference }) {
  setMeta(`Ravel console — ${reference}`, 'The operational record of one run.');
  const [run, setRun] = useState(null);
  const [err, setErr] = useState(null);
  useEffect(() => { api(`/runs/${reference}`).then(setRun).catch((e) => setErr(e)); }, [reference]);
  if (err) return <div class="layout console" style="padding-top:2rem"><Banner title="No such run">{String(err.message)}</Banner></div>;
  if (!run) return <div class="layout console" style="padding-top:2rem"><Loading /></div>;
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <div class="spread">
        <h1 class="mono" style="font-size:var(--step-h3);line-height:var(--lh-h3)">{run.reference}</h1>
        <p class="label">stage: {run.run_type}</p>
      </div>
      <div class="sheet stack">
        <div class="spread"><span class="label">State</span><StateWord>{run.state}</StateWord></div>
        <div class="spread"><span class="label">Site</span><span class="mono">{run.site}</span></div>
        <div class="spread"><span class="label">Equipment</span><span class="mono">{run.equipment}</span></div>
        <div class="spread"><span class="label">Recipe version</span><span class="mono">{run.recipe_version}</span></div>
        <div class="spread"><span class="label">Mass in</span><span class="mono">{fmtGrams(run.mass_in_g)}</span></div>
        <div class="spread"><span class="label">Mass out</span><span class="mono">{fmtGrams(run.mass_out_g)}</span></div>
        <div class="spread"><span class="label">Losses (computed)</span><span class="mono">{fmtGrams(run.losses_g)}</span></div>
        <div class="spread"><span class="label">Within tolerance</span><span>{run.within_tolerance === null ? 'not recorded' : String(run.within_tolerance)}</span></div>
        {run.recipe ? (
          <div>
            <p class="label">Recipe set points</p>
            <ul class="small mono" style="margin:0.25rem 0 0;padding-left:1.2rem">
              {Object.entries(run.recipe.set_points).map(([k, v]) => <li>{k}: {v[0]}–{v[1]}</li>)}
            </ul>
          </div>
        ) : null}
        {run.set_points_achieved ? (
          <div>
            <p class="label">Set points achieved</p>
            <ul class="small mono" style="margin:0.25rem 0 0;padding-left:1.2rem">
              {Object.entries(run.set_points_achieved).map(([k, v]) => <li>{k}: {v}</li>)}
            </ul>
          </div>
        ) : null}
      </div>
      <p class="small" style="color:var(--muted)">Losses reduce the claim: material that disappears in processing does
        not carry its claim forward.</p>
      <div class="two-col">
        <div class="sheet">
          <p class="label">Inputs</p>
          {run.inputs.length === 0 ? <Empty>No inputs recorded.</Empty> : (
            <table><thead><tr><th>Input</th><th class="num">Mass</th></tr></thead>
              <tbody>{run.inputs.map((i) => <tr><td class="mono">{i.reference}</td><td class="mono num">{i.mass_g.toLocaleString('en-GB')}</td></tr>)}</tbody>
            </table>
          )}
        </div>
        <div class="sheet">
          <p class="label">Outputs</p>
          {run.outputs.length === 0 ? <Empty>No outputs recorded.</Empty> : (
            <table><thead><tr><th>Output</th><th>Kind</th><th class="num">Mass</th></tr></thead>
              <tbody>{run.outputs.map((o) => (
                <tr><td class="mono">{o.kind === 'lot' ? <Link href={`/console/lots/${o.reference}`}>{o.reference}</Link> : o.reference}</td>
                  <td>{o.kind}{o.disposition ? ` (${o.disposition})` : ''}</td>
                  <td class="mono num">{o.mass_g.toLocaleString('en-GB')}</td></tr>
              ))}</tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export function Genealogy({ reference }) {
  setMeta(`Ravel console — Genealogy of ${reference}`, 'The same facts as a graph and as a nested list.');
  const [g, setG] = useState(null);
  const [err, setErr] = useState(null);
  const [exported, setExported] = useState(null);
  const [list, setList] = useState(false);
  const me = (() => { try { return JSON.parse(sessionStorage.getItem('me') ?? 'null'); } catch { return null; } })();
  useEffect(() => { api(`/lots/${reference}/genealogy`).then(setG).catch((e) => setErr(e)); }, [reference]);

  async function doExport() {
    try {
      const out = await api('/exports', { method: 'POST', body: { scope: { site: null, certificates: null, period: null } } });
      setExported(out);
    } catch (e) {
      setExported({ error: e.data?.error ?? e.message });
    }
  }

  if (err) return <div class="layout console" style="padding-top:2rem"><Banner title="No such lot">{String(err.message)}</Banner></div>;
  if (!g) return <div class="layout console" style="padding-top:2rem"><Loading /></div>;
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <div class="spread">
        <h1 class="mono" style="font-size:var(--step-h3);line-height:var(--lh-h3)">{reference}</h1>
        <p class="label">genealogy <MarkArrow /></p>
      </div>
      <div class="row">
        <span>{g.flagged ? <><MarkFlag /> a flag sits somewhere in this graph</> : 'nothing in this graph is flagged'}</span>
        <button onClick={() => setList(!list)}>{list ? 'Show the graph' : 'Show the nested list'}</button>
        {me?.roles?.includes('auditor') ? <button onClick={doExport}>Export the record</button> : null}
      </div>
      {exported ? (
        <Banner title={exported.error ? 'The export was refused' : `Export ${exported.reference} recorded`}>
          {exported.error ? exported.error : `${exported.entry_count} entries in scope, digest ${exported.digest.slice(0, 16)}… The export is itself an entry.`}
        </Banner>
      ) : null}
      {!list ? (
        <div class="sheet table-scroll">
          <table>
            <thead><tr><th>Node</th><th>Kind</th><th class="num">Mass, g</th><th>Category split</th><th>Flags</th></tr></thead>
            <tbody>
              {g.nodes.map((n) => (
                <tr>
                  <td class="mono">{n.reference}</td>
                  <td>{n.kind}</td>
                  <td class="mono num">{n.mass_g.toLocaleString('en-GB')}</td>
                  <td class="mono small">{Object.entries(n.category_split).map(([k, v]) => `${k} ${v.toLocaleString('en-GB')} g`).join(', ') || '—'}</td>
                  <td>{n.flags.length ? <MarkWarning label={n.flags.join(', ')} /> : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div class="sheet">
          <NestedList nodes={g.text_equivalent} />
        </div>
      )}
      <p class="small" style="color:var(--muted)">Edges carry mass, never a percentage, because percentages of
        percentages across four hops compound into a figure nobody can reconcile.</p>
    </div>
  );
}

function NestedList({ nodes }) {
  if (!nodes) return null;
  return (
    <ul class="genealogy-list small">
      {nodes.map((n) => (
        <li key={n.reference}>
          <span class="mono">{n.reference}</span> <span class="label">{n.kind}</span>{' '}
          <span class="mono">{n.mass_g.toLocaleString('en-GB')} g</span>
          {n.flags?.length ? <MarkWarning label={n.flags.join(', ')} /> : null}
          {n.contributes?.length ? <NestedList nodes={n.contributes} /> : null}
        </li>
      ))}
    </ul>
  );
}

export function RecordScreen() {
  setMeta('Ravel console — The record', 'Every act is an entry, chained by digest.');
  const [entries, setEntries] = useState(null);
  const [check, setCheck] = useState(null);
  const [queries, setQueries] = useState(null);
  useEffect(() => {
    api('/record').then(setEntries).catch(() => setEntries([]));
    api('/record/check').then(setCheck).catch(() => setCheck(null));
  }, []);
  const me = (() => { try { return JSON.parse(sessionStorage.getItem('me') ?? 'null'); } catch { return null; } })();
  const QUERY_NAMES = ['lots_from_batch', 'certificates_on_period', 'certificates_under_method_version',
    'lots_released_under_unreviewed_override', 'allocations_in_final_fortnight', 'refused_allocations',
    'collector_declaration_departures', 'acts_by_person', 'exports_by_auditor'];
  async function runQuery(name) {
    try {
      const out = await api(`/record/queries/${name}`);
      setQueries({ name, out });
    } catch (e) {
      setQueries({ name, error: e.data?.error ?? e.message });
    }
  }
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">The record</h1>
      {check ? (
        <Banner title={check.holds ? 'The chain verifies' : `The chain breaks at position ${check.first_failure}`}>
          {check.holds ? `${check.entries} entries, each digest computed over its own content and the previous entry's digest.` :
            `A digest that does not verify is a reportable condition. Position ${check.first_failure} fails.`}
        </Banner>
      ) : null}
      <div class="row no-print">
        <span class="label">Record queries</span>
        {QUERY_NAMES.map((q) => <button key={q} onClick={() => runQuery(q)}>{q.replace(/_/g, ' ')}</button>)}
      </div>
      {queries ? (
        <div class="sheet table-scroll">
          <p class="label">{queries.name}</p>
          {queries.error ? <Banner title="The query was refused">{queries.error}</Banner> : (
            <pre class="mono small" style="white-space:pre-wrap;max-height:22rem;overflow:auto">{JSON.stringify(queries.out, null, 1)}</pre>
          )}
        </div>
      ) : null}
      <h2>Entries</h2>
      {entries === null ? <Loading /> : entries.length === 0 ? <Empty>There are no entries.</Empty> : (
        <div class="sheet table-scroll">
          <table>
            <thead><tr><th class="num">Seq</th><th>Act</th><th>Person</th><th>Object</th><th>Digest</th><th>Hold</th></tr></thead>
            <tbody>
              {entries.map((e) => (
                <tr>
                  <td class="mono num">{e.seq}</td>
                  <td>{e.act}</td>
                  <td class="mono small">{e.person ?? '—'}</td>
                  <td class="mono small">{e.object ?? '—'}</td>
                  <td class="mono small">{e.digest.slice(0, 12)}…</td>
                  <td>{e.legal_hold ? <span class="state-word">legal hold</span> : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export function Reconciliation() {
  setMeta('Ravel console — Reconciliation', 'Six figures, none of them a verdict.');
  const [r, setR] = useState(null);
  useEffect(() => {
    const load = () => api('/reconciliation').then(setR).catch(() => setR(null));
    load();
    const t = setInterval(load, 30000);
    return () => clearInterval(t);
  }, []);
  if (!r) return <div class="layout console" style="padding-top:2rem"><Loading /></div>;
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">Reconciliation</h1>
      <div class="sheet">
        <p class="label">Mass balance residual</p>
        <p class="stat-figure mono">{r.mass_balance_residual_g.toLocaleString('en-GB')} g</p>
        <p class="small" style="color:var(--muted)">{r.derivation.mass_balance_residual_g}. Read at {r.read_at}.</p>
      </div>
      <div class="balance-grid">
        <div class="sheet"><p class="label">Credit margin</p><p class="mono">{r.credit_margin_g.toLocaleString('en-GB')} g</p></div>
        <div class="sheet"><p class="label">Consumptions on open runs</p><p class="mono">{r.consumptions_on_open_runs}</p></div>
        <div class="sheet"><p class="label">Batches with broken custody</p>
          {r.batches_with_broken_custody.length === 0 ? <Empty>None.</Empty> : (
            <ul class="mono small" style="margin:0;padding-left:1.2rem">{r.batches_with_broken_custody.map((b) => <li>{b}</li>)}</ul>
          )}
        </div>
        <div class="sheet"><p class="label">Certificates with superseded figures</p>
          {r.certificates_with_superseded_figures.length === 0 ? <Empty>None.</Empty> : (
            <ul class="mono small" style="margin:0;padding-left:1.2rem">{r.certificates_with_superseded_figures.map((b) => <li>{b}</li>)}</ul>
          )}
        </div>
      </div>
      <div class="sheet">
        <p class="label">Integration ages, hours since last record</p>
        <table>
          <thead><tr><th>Source</th><th class="num">Age, hours</th></tr></thead>
          <tbody>
            {Object.entries(r.integration_ages).map(([k, v]) => (
              <tr><td>{k.replace(/_/g, ' ')}</td><td class="mono num">{v === null ? 'null' : v}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="small" style="color:var(--muted)">A source that has never sent reports null rather than zero.</p>
      </div>
    </div>
  );
}

export function LotDetail({ reference }) {
  setMeta(`Ravel console — ${reference}`, 'One lot, its claim and the records behind it.');
  const [lot, setLot] = useState(null);
  const [carbon, setCarbon] = useState(null);
  const [err, setErr] = useState(null);
  useEffect(() => {
    api(`/lots/${reference}`).then(setLot).catch((e) => setErr(e));
    api(`/lots/${reference}/carbon`).then(setCarbon).catch(() => setCarbon(null));
  }, [reference]);
  if (err) return <div class="layout console" style="padding-top:2rem"><Banner title="No such lot">{String(err.message)}</Banner></div>;
  if (!lot) return <div class="layout console" style="padding-top:2rem"><Loading /></div>;
  return (
    <div class="layout console stack" style="padding-top:2rem">
      <div class="spread">
        <h1 class="mono" style="font-size:var(--step-h3);line-height:var(--lh-h3)">{lot.reference}</h1>
        <Link class="button" href={`/console/lots/${lot.reference}/genealogy`}>Genealogy</Link>
      </div>
      <div class="sheet stack small">
        <div class="spread"><span class="label">Site</span><span class="mono">{lot.site}</span></div>
        <div class="spread"><span class="label">Grade</span><span class="mono">{lot.grade}</span></div>
        <div class="spread"><span class="label">Mass</span><span class="mono">{fmtGrams(lot.mass_g)}</span></div>
        <div class="spread"><span class="label">Disposition</span><StateWord>{lot.disposition}</StateWord></div>
        <div class="spread"><span class="label">Claim</span><span><ContentFigure content_bp={lot.content_bp} claim_type={lot.claim_type} /></span></div>
        <div class="spread"><span class="label">Credit attached</span><span class="mono">{fmtGrams(lot.credit_attached_g)}</span></div>
        <div class="spread"><span class="label">Category split</span><span class="mono">{Object.entries(lot.category_split).map(([k, v]) => `${k} ${v / 100} %`).join(', ') || '—'}</span></div>
        {lot.flags.length ? <div class="spread"><span class="label">Flags</span><span>{lot.flags.join(', ')}</span></div> : null}
        {lot.overrides.length ? (
          <div>
            <p class="label">Overrides</p>
            {lot.overrides.map((o) => (
              <p class="small" key={o.reference}>
                {o.reviewed ? 'reviewed' : <span class="state-word">unreviewed</span>} · Separation overridden by
                {' '}{o.authorised_by} on {o.authorised_on}. This cannot be removed.
              </p>
            ))}
          </div>
        ) : null}
      </div>
      {carbon ? (
        <div class="sheet stack small">
          <div class="spread"><span class="label">Carbon</span>
            <span>
              <span class="mono">{Number(carbon.value_mg_per_kg).toLocaleString('en-GB')} mg CO2e/kg</span>
              <span class="label"> {carbon.boundary} · {carbon.method_version} · ±{carbon.uncertainty_bp} bp</span>
            </span>
          </div>
          <div class="spread"><span class="label">Lower than its comparator</span>
            <span class="small">The figure is lower than {carbon.comparator?.material} from dataset {carbon.comparator?.dataset} ({carbon.comparator?.dataset_year}, {carbon.comparator?.region}).</span>
          </div>
          <div class="spread"><span class="label">Energy, location and market together</span>
            <span class="mono">{Number(carbon.energy_location_mg_per_kg).toLocaleString('en-GB')} / {Number(carbon.energy_market_mg_per_kg).toLocaleString('en-GB')} mg CO2e/kg</span>
          </div>
          <div class="spread"><span class="label">Metered / retired / unmatched</span>
            <span class="mono">{carbon.metered_kwh.toLocaleString('en-GB')} / {carbon.retired_kwh.toLocaleString('en-GB')} / {carbon.unmatched_kwh.toLocaleString('en-GB')} kWh</span>
          </div>
        </div>
      ) : null}
    </div>
  );
}
