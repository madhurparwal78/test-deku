import { useEffect, useState } from 'preact/hooks';
import { api } from '../lib/api.js';
import { Link } from '../lib/link.jsx';
import { Reveal, Empty, Loading, ContentFigure, CapacityFigure, setMeta } from '../components/ui.jsx';

export function Home() {
  setMeta("Ravel — Tomorrow's materials. Made from today's waste.",
    'Ravel produces low-carbon, virgin-quality recycled polymers, starting with nylon.');
  return (
    <div>
      <section class="hero layout">
        <Reveal as="h1" style="max-width:22ch">Tomorrow's materials.<br />Made from today's waste.</Reveal>
        <Reveal as="p" class="body-big measure" delay={80}>
          Ravel produces low-carbon, virgin-quality recycled polymers, starting with nylon.
        </Reveal>
        <Reveal delay={160} class="row">
          <Link class="button primary" href="/product">The material</Link>
          <Link class="button" href="/technology">How it is made</Link>
        </Reveal>
      </section>
      <section class="layout stack" style="padding-bottom:3rem">
        <Reveal as="h2">Nylon that goes on and on and on</Reveal>
        <Reveal as="p" class="measure">
          Nylon 6 is a polymer that can be returned to its monomer and rebuilt, which is why it goes on and on and on.
          The polymer survives its product; the product is what wears out. Ravel takes the product back and returns the
          polymer to the quality a converter specifies, without the oil.
        </Reveal>
        <Reveal as="h2">The power of green chemistry</Reveal>
        <Reveal as="p" class="measure">
          Dissolution, depolymerisation, purification and repolymerisation run at low temperature and low pressure,
          which is why the chemistry carries a smaller footprint than the incumbent route, and why the plant is safe to
          stand next to.
        </Reveal>
        <Reveal as="h2">We're closing the loop</Reveal>
        <Reveal as="p" class="measure">
          A loop is not a sentence on a website. It is a collector, a weighbridge, four process stages, a ledger and a
          certificate that stands up when somebody checks it. We publish the figures and the basis they rest on, and a
          claim we cannot substantiate comes off this site rather than staying on it.
        </Reveal>
      </section>
    </div>
  );
}

export function Product() {
  const [spec, setSpec] = useState(null);
  useEffect(() => { api('/specifications/N6/versions/3').then(setSpec).catch(() => setSpec(null)); }, []);
  setMeta('Ravel — Same material. Better origin.',
    'We produce low-carbon, virgin-quality, recycled Nylon 6 and 6,6 for manufacturers who refuse to compromise.');
  return (
    <div class="layout stack" style="padding-top:3rem">
      <Reveal as="h1" style="max-width:20ch">Same material. Better origin.</Reveal>
      <Reveal as="p" class="body-big measure" delay={80}>
        We produce low-carbon, virgin-quality, recycled Nylon 6 and 6,6 for manufacturers who refuse to compromise.
      </Reveal>
      <Reveal as="h2" delay={140}>Two grades</Reveal>
      <div class="two-col">
        <Reveal class="sheet">
          <p class="label">Grade N6</p>
          <h3>Nylon 6</h3>
          <p class="small">Its limitation before Ravel: recycled Nylon 6 came almost entirely from one source, discarded
            fishing nets, and supply followed the tide rather than the order book.</p>
          <p class="small">Its claim now: <strong>recycled content credited by mass balance</strong>, under scheme
            RCS-2026, with the percentage stated beside the grade rather than above it.</p>
          <p><ContentFigure content_bp={9000} claim_type="mass_balance" compact /></p>
        </Reveal>
        <Reveal class="sheet" delay={80}>
          <p class="label">Grade N66</p>
          <h3>Nylon 6,6</h3>
          <p class="small">Its limitation before Ravel: Nylon 6,6 had no recycling solution at all, so every kilogram
            in use today began as virgin polymer.</p>
          <p class="small">Its claim now: <strong>recycled content credited by mass balance</strong>, under scheme
            RCS-2026, with the percentage stated beside the grade rather than above it.</p>
          <p><ContentFigure content_bp={0} claim_type="mass_balance" compact /></p>
        </Reveal>
      </div>
      <Reveal as="h2" delay={160}>Three features</Reveal>
      <Reveal as="h3">Nylon in any form</Reveal>
      <Reveal as="p" class="measure">Pellet, fibre, film or compound: the material is the incumbent, so it runs on the
        line you already have. Nylon in any form is what we make, and any form means any form.</Reveal>
      <Reveal as="h3" style="margin-top:1rem">Specified, not promised</Reveal>
      <Reveal as="p" class="measure">Every property below has a method beside it and a basis stated, and a guaranteed
        limit is tested on every lot we ship.</Reveal>
      <Reveal as="h3" style="margin-top:1rem">Origin a regulator can check</Reveal>
      <Reveal as="p" class="measure">Every certificate resolves at a public address, with its claim type, its
        percentage and its scheme. A certificate that is withdrawn says so, in the same place, forever.</Reveal>
      <Reveal as="h2" delay={200}>Six industries</Reveal>
      <Reveal as="p" class="measure">Textiles and apparel, automotive, electrical and electronics, consumer goods,
        industrial, construction.</Reveal>
      <Reveal as="h2">Specifications</Reveal>
      <div class="sheet table-scroll">
        {spec ? (
          <table>
            <caption class="label" style="text-align:left;padding:0 0 0.75rem">
              SPEC-N6 version 3, issued {spec.issued_on}
            </caption>
            <thead><tr><th>Property</th><th>Method</th><th>Limit</th><th>Unit</th><th>Basis</th></tr></thead>
            <tbody>
              {spec.rows.map((r) => (
                <tr>
                  <td class="mono">{r.property}</td>
                  <td>{r.method}</td>
                  <td class="mono num">{r.limit}</td>
                  <td>{r.unit}</td>
                  <td>{r.basis}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <Loading />}
        {spec?.virgin_reference ? (
          <p class="small" style="margin-top:1rem">
            Virgin-quality comparison against {spec.virgin_reference.reference}, source {spec.virgin_reference.source},
            dated {spec.virgin_reference.dated}.
          </p>
        ) : null}
      </div>
    </div>
  );
}

export function Technology() {
  const [sites, setSites] = useState(null);
  useEffect(() => { api('/sites').then(setSites).catch(() => setSites(null)); }, []);
  setMeta('Ravel — Technology',
    'Dissolution, depolymerisation, purification and repolymerisation, at low temperature and low pressure.');
  const stages = [
    ['Dissolution', 'The polymer is dissolved away from the contamination that came in with it. Mass in 600000 g, mass out 480000 g.'],
    ['Depolymerisation', 'The chain is broken back to its monomer. Mass in 850000 g, mass out 800000 g.'],
    ['Purification', 'The monomer stream is purified to polymerisation feed. Mass in 800000 g, mass out 760000 g.'],
    ['Repolymerisation', 'The monomer is rebuilt into pellet. Mass in 720000 g, mass out 700000 g.'],
  ];
  return (
    <div class="layout stack" style="padding-top:3rem">
      <Reveal as="h1">The four process steps</Reveal>
      {stages.map(([name, text], i) => (
        <Reveal class="sheet" delay={i * 60}>
          <p class="label">Stage {i + 1}</p>
          <h3>{name}</h3>
          <p class="small">{text}</p>
        </Reveal>
      ))}
      <Reveal as="figure" class="plant sheet" aria-label="Plant diagram, drawn from the four run types">
        <figcaption class="label" style="margin-bottom:0.75rem">Plant diagram, drawn from the four run types</figcaption>
        <svg viewBox="0 0 900 180" role="img" aria-label="Waste enters at dissolution, leaves repolymerisation as pellet; mass is named at every hop.">
          <g stroke="var(--ink)" fill="none" stroke-width="1.5" font-family="Archivo, sans-serif">
            {['Dissolution', 'Depolymerisation', 'Purification', 'Repolymerisation'].map((n, i) => (
              <g key={n}>
                <rect x={20 + i * 220} y="50" width="160" height="80" rx="8" />
                <text x={100 + i * 220} y="80" text-anchor="middle" font-size="13" fill="var(--ink)" stroke="none">{n}</text>
                <text x={100 + i * 220} y="102" text-anchor="middle" font-size="11" fill="var(--muted)" stroke="none">stage {i + 1}</text>
                {i < 3 ? <path d={`M180 ${0 + i * 0} h0 M180 90 h60`} marker-end="url(#ar)" /> : null}
              </g>
            ))}
            <defs>
              <marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
                <path d="M0 0 L8 4 L0 8 z" fill="var(--ink)" stroke="none" />
              </marker>
            </defs>
            <text x="100" y="30" text-anchor="middle" font-size="12" fill="var(--muted)" stroke="none">waste in</text>
            <text x="780" y="30" text-anchor="middle" font-size="12" fill="var(--muted)" stroke="none">pellet out</text>
          </g>
        </svg>
      </Reveal>
      <Reveal as="h2" delay={120}>Capacity</Reveal>
      <p class="small">Nameplate capacity is stated in tonnes of polymer per year. A year is 8000 hours of operation at
        0.90 availability and 0.80 yield, and the basis is identical on every row.</p>
      <div class="sheet table-scroll">
        {sites ? (
          <table>
            <thead><tr><th>Site</th><th class="num">Capacity, tonnes per year</th><th>Confidence</th></tr></thead>
            <tbody>
              {sites.map((s) => (
                <tr>
                  <td>{s.reference === 'SITE-PILOT' ? 'Pilot (2026)' : s.reference === 'SITE-DEMO' ? 'Demonstration (2027)' : 'Commercial Plant (2030+)'}</td>
                  <td class="mono num">{s.nameplate_kg >= 25000 ? `>25,000` : (s.nameplate_kg / 1000).toLocaleString('en-GB')}</td>
                  <td>
                    {s.confidence === 'planned' ? <span><span class="state-word">planned</span> </span> : null}
                    <CapacityFigure value_kg={s.nameplate_kg} confidence={s.confidence} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <Loading />}
      </div>
      <Reveal as="h2">Five attributes</Reveal>
      <ul class="measure">
        <li>Green chemicals & reagents — evidence: supplier EPDs held on file and named in the carbon method version.</li>
        <li>Low temperature &amp; pressure — evidence: the recipe set points published on every run record.</li>
        <li>Low carbon impact — evidence: ISO 14067, cradle-to-gate, method version CM-PA6 v2, uncertainty ±1200 bp.</li>
        <li>Dropped into the incumbent line — evidence: specification N6 v3 against a virgin reference.</li>
        <li>Traceable to a collector — evidence: the certificate and its verification address.</li>
      </ul>
    </div>
  );
}

export function About() {
  const [stats, setStats] = useState(null);
  useEffect(() => { api('/statistics').then(setStats).catch(() => setStats(null)); }, []);
  setMeta('Ravel — About', 'Three statistics under The hard facts, each with its source, year and geography.');
  return (
    <div class="layout stack" style="padding-top:3rem">
      <Reveal as="h1">The hard facts</Reveal>
      {stats === null ? <Loading /> : stats.length === 0 ? <Empty>There are no published figures.</Empty> : (
        <div class="two-col">
          {stats.map((s, i) => (
            <Reveal class="sheet" delay={i * 70}>
              <p class="stat-figure">{s.value}</p>
              <p class="label">Source: {s.source} · {s.year} · {s.geography}</p>
            </Reveal>
          ))}
        </div>
      )}
      <Reveal as="p" class="measure">
        Ravel Materials SAS operates a chemical recycling plant at Lyon, returning mixed polyamide waste to
        virgin-quality pellet. The company is registered in France and its scheme registration is REG-RAVEL-0042.
      </Reveal>
    </div>
  );
}

export function Careers() {
  const [positions, setPositions] = useState(null);
  useEffect(() => { api('/positions').then(setPositions).catch(() => setPositions(null)); }, []);
  setMeta('Ravel — Careers', 'Why this problem matters, and the positions we are hiring for.');
  return (
    <div class="layout stack" style="padding-top:3rem">
      <Reveal as="h1">Why this problem matters</Reveal>
      <Reveal as="p" class="measure" delay={80}>
        Less than one per cent of textiles are recycled into new materials. The rest is landfilled, incinerated or
        exported, and the polymer in it is lost. Polymer is expensive to make and cheap to throw away, which is a
        market failure rather than a technical one, and it is the one we chose.
      </Reveal>
      <Reveal as="h2" delay={140}>Open positions</Reveal>
      {positions === null ? <Loading /> : positions.length === 0 ? <Empty>There are no open positions.</Empty> : (
        <div class="sheet table-scroll">
          <p class="label" style="margin-bottom:0.75rem">{positions.length} open {positions.length === 1 ? 'position' : 'positions'}</p>
          <table>
            <thead><tr><th>Title</th><th>Location</th><th>Department</th><th>Contract</th><th>Closes</th></tr></thead>
            <tbody>
              {positions.map((p) => (
                <tr>
                  <td>{p.title}</td><td>{p.location}</td><td>{p.department}</td>
                  <td>{p.contract_type}</td><td class="mono">{p.closes_on}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export function News() {
  const [items, setItems] = useState(null);
  useEffect(() => { api('/news').then(setItems).catch(() => setItems(null)); }, []);
  setMeta('Ravel — News', 'Funding, partnership, technical and recognition coverage, listed once per event.');
  return (
    <div class="layout stack" style="padding-top:3rem">
      <Reveal as="h1">News</Reveal>
      <p class="small measure">Tags are a real taxonomy: funding, partnership, technical, recognition. An event is
        listed once with its coverage, and an item in another language says so before a reader clicks.</p>
      {items === null ? <Loading /> : items.length === 0 ? <Empty>There are no news items.</Empty> : (
        items.map((n, i) => (
          <Reveal class="sheet" delay={i * 60}>
            <p class="label">{n.tag}</p>
            <h3>{n.title}</h3>
            <p class="small">
              {n.outlet} · <span class="mono">{n.dated_on}</span> · {n.link}
              {n.language !== 'en' ? <span class="state-word" style="margin-left:0.5rem">in {n.language}</span> : null}
            </p>
          </Reveal>
        ))
      )}
    </div>
  );
}
