import { useState } from 'preact/hooks';
import { api, setToken } from '../lib/api.js';
import { navigate } from '../lib/router.js';
import { Link } from '../lib/link.jsx';
import { Banner, Field, setMeta } from '../components/ui.jsx';

const ACCOUNTS = [
  ['plant@example.com', 'Plant operator', 'Ines Bekele'],
  ['analyst@example.com', 'Laboratory analyst', 'Tomas Vlach'],
  ['quality@example.com', 'Quality manager', 'Marit Solheim'],
  ['claims@example.com', 'Claims manager', 'Osei Danquah'],
  ['signer@example.com', 'Certificate signer', 'Hana Ferreira'],
  ['signer2@example.com', 'Second certificate signer', 'Pavel Ostrowski'],
  ['auditor@example.com', 'Auditor', 'Ruth Lindqvist'],
];

export function Login() {
  setMeta('Ravel — Sign in', 'Sign in to the Ravel console.');
  const [state, setState] = useState({ phase: 'idle' });

  async function submit(e) {
    e.preventDefault();
    const f = new FormData(e.target);
    setState({ phase: 'sending' });
    try {
      const out = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'idempotency-key': crypto.randomUUID() },
        body: JSON.stringify({ email: f.get('email'), password: f.get('password') }),
      }).then((r) => r.json());
      if (!out.access_token) throw new Error('The credentials were refused.');
      setToken(out.access_token);
      sessionStorage.setItem('token', out.access_token);
      const me = await api('/auth/me');
      sessionStorage.setItem('me', JSON.stringify(me));
      setState({ phase: 'done' });
      navigate('/console');
    } catch (err) {
      setState({ phase: 'failed', err });
    }
  }

  return (
    <div class="layout stack" style="padding-top:4rem;max-width:36rem">
      <p class="eyebrow">Ravel console</p>
      <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">Sign in</h1>
      <p class="small" style="color:var(--muted)">Signup is closed. The seven seeded accounts are the only accounts, and
        every one authenticates at the identity provider. A session expires twelve hours after issue.</p>
      {state.phase === 'failed' ? (
        <Banner title="The sign-in was refused">
          {String(state.err?.message)}. Check the address and password, or ask an administrator whether your grant has
          ended.
        </Banner>
      ) : null}
      <form class="sheet stack" onSubmit={submit}>
        <Field label="Email"><input name="email" type="email" defaultValue="claims@example.com" required /></Field>
        <Field label="Password"><input name="password" type="password" defaultValue="deku-demo-pw-2026" required /></Field>
        <div class="row">
          <button class="primary" type="submit" disabled={state.phase === 'sending'}>
            {state.phase === 'sending' ? 'Signing in…' : 'Sign in'}
          </button>
          <Link class="button" href="/">Back to the public site</Link>
        </div>
      </form>
      <div class="sheet">
        <p class="label">The seeded accounts</p>
        <table>
          <thead><tr><th>Email</th><th>Role</th><th>Name</th></tr></thead>
          <tbody>{ACCOUNTS.map(([e, r, n]) => <tr key={e}><td class="mono small">{e}</td><td>{r}</td><td>{n}</td></tr>)}</tbody>
        </table>
      </div>
    </div>
  );
}
