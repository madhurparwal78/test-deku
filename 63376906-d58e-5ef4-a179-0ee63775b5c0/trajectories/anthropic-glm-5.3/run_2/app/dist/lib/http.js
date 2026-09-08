import { query } from './db.js';
import { getSession } from './auth.js';
import { bodyHash } from './num.js';
export class HttpError extends Error {
    status;
    code;
    extra;
    constructor(status, code, extra = {}) {
        super(code);
        this.status = status;
        this.code = code;
        this.extra = extra;
    }
}
export function json(c, body, status = 200) {
    return c.json(body, status);
}
export async function requireSession(c) {
    const h = c.req.header('authorization') ?? '';
    const m = /^Bearer\s+(.+)$/i.exec(h);
    const s = await getSession(m ? m[1].trim() : undefined);
    if (!s)
        throw new HttpError(401, 'unauthenticated');
    return s;
}
export async function requireRole(c, ...roles) {
    const s = await requireSession(c);
    if (!s.roles.some((r) => roles.includes(r)))
        throw new HttpError(403, 'forbidden', { roles_required: roles });
    return s;
}
export async function requireAuditor(c) {
    return requireRole(c, 'auditor');
}
/** Auditor may read everything in scope and write nothing. */
export function assertNotAuditor(s) {
    if (s.roles.includes('auditor'))
        throw new HttpError(403, 'auditor_reads_only');
}
export async function readBody(c) {
    const raw = await c.req.raw.clone().text();
    if (!raw.trim())
        throw new HttpError(400, 'empty_body');
    try {
        return JSON.parse(raw);
    }
    catch {
        throw new HttpError(400, 'invalid_json');
    }
}
/**
 * Every write requires an Idempotency-Key scoped to the route and body.
 * Returns the stored response when the key repeats with the same body, and
 * raises idempotency_key_reuse when the body differs.
 */
export async function idempotent(c, create) {
    const key = c.req.header('idempotency-key');
    if (!key)
        throw new HttpError(400, 'idempotency_key_required');
    const route = c.req.path;
    const body = await c.req.raw.clone().json().catch(() => null);
    const hash = bodyHash(body);
    const existing = await query(`select status, response, body_hash from idempotency where key = $1 and route = $2`, [key, route]);
    if (existing.length) {
        if (existing[0].body_hash !== hash) {
            throw new HttpError(409, 'idempotency_key_reuse', { route });
        }
        return { status: existing[0].status, body: existing[0].response };
    }
    const out = await create();
    await query(`insert into idempotency(key, route, body_hash, status, response) values ($1,$2,$3,$4,$5)`, [key, route, hash, out.status, JSON.stringify(out.body)]);
    return out;
}
/** The four complete-set queries refuse pagination outright. */
export function refusePagination(c) {
    for (const p of ['page', 'limit', 'offset', 'cursor']) {
        if (c.req.query(p) !== undefined)
            throw new HttpError(400, 'pagination_refused', { parameter: p });
    }
}
export function intField(v, name, { min = -(2 ** 52), max = 2 ** 52 } = {}) {
    if (typeof v !== 'number' || !Number.isInteger(v))
        throw new HttpError(400, 'invalid_field', { field: name, expected: 'integer' });
    if (v < min || v > max)
        throw new HttpError(400, 'invalid_field', { field: name, range: [min, max] });
    return v;
}
export function strField(v, name, values) {
    if (typeof v !== 'string' || !v.trim())
        throw new HttpError(400, 'invalid_field', { field: name, expected: typeof values === 'undefined' ? 'string' : 'enum' });
    if (values && !values.includes(v))
        throw new HttpError(400, 'invalid_field', { field: name, expected: values });
    return v;
}
export function dateField(v, name) {
    if (typeof v !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(v))
        throw new HttpError(400, 'invalid_field', { field: name, expected: 'YYYY-MM-DD' });
    return v;
}
/** No figure crosses the wire as a decimal: mass, proportion, carbon, energy are integers. */
export function assertNoDecimal(body, path = '') {
    if (body === null || typeof body !== 'object')
        return;
    for (const [k, v] of Object.entries(body)) {
        const p = path ? `${path}.${k}` : k;
        if (typeof v === 'number' && !Number.isInteger(v)) {
            throw new HttpError(400, 'decimal_refused', { field: p });
        }
        if (v && typeof v === 'object')
            assertNoDecimal(v, p);
    }
}
