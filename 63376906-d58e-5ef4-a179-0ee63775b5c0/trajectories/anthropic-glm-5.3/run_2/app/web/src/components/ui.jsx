import { useEffect, useRef } from 'preact/hooks';
import { Link } from '../lib/link.jsx';

/** One reveal component: one distance, one duration, readable before it finishes. */
export function Reveal({ as: Tag = 'div', children, delay = 0, ...rest }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.classList.add('settled');
      return;
    }
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          setTimeout(() => el.classList.add('in'), delay);
          io.unobserve(el);
        }
      }
    }, { threshold: 0.05 });
    io.observe(el);
    // Nothing governed by a reveal stays hidden if the reader never scrolls.
    setTimeout(() => el.classList.add('in'), 1600);
    return () => io.disconnect();
  }, [delay]);
  return <Tag ref={ref} class={'reveal ' + (rest.class ?? '')} {...rest}>{children}</Tag>;
}

export function Field({ label, hint, children }) {
  return (
    <label class="stack" style="gap:0.35rem">
      <span class="label">{label}</span>
      {children}
      {hint ? <span class="small" style="color:var(--muted)">{hint}</span> : null}
    </label>
  );
}

export function Empty({ children }) {
  return <p class="small" style="color:var(--muted);font-style:italic">{children}</p>;
}

export function Loading({ children = 'Loading…' }) {
  return <p class="small" style="color:var(--muted)">{children}</p>;
}

export function Banner({ title, children }) {
  return (
    <div class="banner" role="status">
      {title ? <strong class="label" style="display:block;margin-bottom:0.35rem">{title}</strong> : null}
      <div class="small">{children}</div>
    </div>
  );
}

export function StateWord({ children }) {
  return <span class="state-word">{children}</span>;
}

export function Ref({ value }) {
  return <span class="mono small">{value}</span>;
}

/** The three figures that never render alone. */
export function ContentFigure({ content_bp, claim_type, compact = false }) {
  const pct = content_bp === null || content_bp === undefined ? '—' : (Math.floor(content_bp / 100) + '.' + String(content_bp % 100).padStart(2, '0'));
  return (
    <span class={compact ? 'small' : ''}>
      <span class="mono">{pct} per cent</span>
      <span class="label"> {claim_type ? claim_type.replace(/_/g, ' ') : 'no claim type'}</span>
    </span>
  );
}

export function CarbonFigure({ value_mg_per_kg, boundary, method_version, uncertainty_bp, compact = false }) {
  return (
    <span class={compact ? 'small' : ''}>
      <span class="mono">{Number(value_mg_per_kg ?? 0).toLocaleString('en-GB')} mg CO2e/kg</span>
      <span class="label"> {boundary ?? 'no boundary'} · {method_version ?? 'no method version'} · ±{uncertainty_bp ?? '—'} bp</span>
    </span>
  );
}

export function CapacityFigure({ value_kg, confidence }) {
  return (
    <span>
      <span class="mono">{Number(value_kg ?? 0).toLocaleString('en-GB')} kg/yr</span>
      <span class="label"> {confidence ?? 'no confidence stated'}</span>
    </span>
  );
}

export function SiteHeader({ route, console: isConsole }) {
  return (
    <header class="site-header">
      <div class="inner">
        <Link href="/" class="wordmark">Ravel</Link>
        {isConsole ? (
          <nav class="nav" aria-label="Console">
            <Link href="/console" aria-current={route === '/console' ? 'page' : null}>Board</Link>
            <Link href="/console/intake" aria-current={route === '/console/intake' ? 'page' : null}>Intake</Link>
            <Link href="/console/record" aria-current={route.startsWith('/console/record') ? 'page' : null}>Record</Link>
            <Link href="/console/reconciliation" aria-current={route.startsWith('/console/reconciliation') ? 'page' : null}>Reconciliation</Link>
            <Link href="/console/certificates" aria-current={route.startsWith('/console/certificates') ? 'page' : null}>Certificates</Link>
            <Link href="/" >Public site</Link>
          </nav>
        ) : (
          <nav class="nav" aria-label="Public">
            <Link href="/product" aria-current={route === '/product' ? 'page' : null}>Product</Link>
            <Link href="/technology" aria-current={route === '/technology' ? 'page' : null}>Technology</Link>
            <Link href="/about" aria-current={route === '/about' ? 'page' : null}>About</Link>
            <Link href="/careers" aria-current={route === '/careers' ? 'page' : null}>Careers</Link>
            <Link href="/news" aria-current={route === '/news' ? 'page' : null}>News</Link>
            <Link href="/contact" aria-current={route === '/contact' ? 'page' : null}>Contact</Link>
            <Link href="/console">Console</Link>
          </nav>
        )}
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer class="site-footer">
      <div class="inner small">
        <div>
          <p class="label">Ravel Materials SAS</p>
          <p>14 quai des Célestins, 69002 Lyon, France</p>
        </div>
        <div>
          <p class="label">Verify a certificate</p>
          <p><Link href="/verify/CERT-PILOT-000001">ravel.example.com/verify/CERT-PILOT-000001</Link></p>
        </div>
        <div>
          <p class="label">Data protection</p>
          <p><Link href="/privacy">Privacy policy</Link> · privacy@example.com · security@example.com</p>
        </div>
      </div>
    </footer>
  );
}

/** Four inline interface marks, each with its text label. */
export function MarkLock() {
  return (
    <span class="mark label">
      <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">
        <rect x="3" y="7" width="10" height="7" fill="none" stroke="currentColor" stroke-width="1.4" />
        <path d="M5 7V5a3 3 0 0 1 6 0v2" fill="none" stroke="currentColor" stroke-width="1.4" />
      </svg>
      closed
    </span>
  );
}

export function MarkFlag() {
  return (
    <span class="mark label">
      <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">
        <path d="M4 2v12M4 3h8l-2 2.5L12 8H4" fill="none" stroke="currentColor" stroke-width="1.4" />
      </svg>
      flagged
    </span>
  );
}

export function MarkArrow({ label = 'traversal' }) {
  return (
    <span class="mark label">
      <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">
        <path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.4" />
      </svg>
      {label}
    </span>
  );
}

export function MarkWarning({ label = 'calibration lapsed' }) {
  return (
    <span class="mark label">
      <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">
        <path d="M8 2 15 14H1z" fill="none" stroke="currentColor" stroke-width="1.4" />
        <path d="M8 6v4M8 11.8v.4" stroke="currentColor" stroke-width="1.4" />
      </svg>
      {label}
    </span>
  );
}

export function setMeta(title, description, { noindex = false } = {}) {
  document.title = title;
  let m = document.querySelector('meta[name="description"]');
  if (!m) {
    m = document.createElement('meta');
    m.name = 'description';
    document.head.appendChild(m);
  }
  m.content = description;
  let r = document.querySelector('meta[name="robots"]');
  if (!r) {
    r = document.createElement('meta');
    r.name = 'robots';
    document.head.appendChild(r);
  }
  r.content = noindex ? 'noindex, nofollow' : 'index, follow';
}
