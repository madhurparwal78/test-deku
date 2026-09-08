let token = null;

export function setToken(t) { token = t; }
export function hasToken() { return !!token; }

export async function api(path, { method = 'GET', body, key } = {}) {
  const headers = {};
  if (token) headers.authorization = `Bearer ${token}`;
  if (method !== 'GET') {
    if (!key) key = crypto.randomUUID();
    headers['idempotency-key'] = key;
    headers['content-type'] = 'application/json';
  }
  const res = await fetch('/api' + path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  if (!res.ok) {
    const err = new Error(data?.error ?? res.statusText);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

export function fmtGrams(n) {
  if (n === null || n === undefined) return '—';
  return Number(n).toLocaleString('en-GB') + ' g';
}

export function fmtBp(bp) {
  if (bp === null || bp === undefined) return '—';
  return (Math.floor(Number(bp) / 100)) + '.' + String(Number(bp) % 100).padStart(2, '0') + ' %';
}

export function id(x) { return x; }
