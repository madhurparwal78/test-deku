import crypto from 'node:crypto';
import { query } from './db.js';
export const ACCOUNT_NAMES = {
    'plant@example.com': 'Ines Bekele',
    'analyst@example.com': 'Tomas Vlach',
    'quality@example.com': 'Marit Solheim',
    'claims@example.com': 'Osei Danquah',
    'signer@example.com': 'Hana Ferreira',
    'signer2@example.com': 'Pavel Ostrowski',
    'auditor@example.com': 'Ruth Lindqvist',
};
export const PUBLIC_ROLE_ROUTES = {};
export async function login(email, password) {
    const issuer = process.env.AUTH_ISSUER_URL;
    const body = new URLSearchParams({
        grant_type: 'password',
        client_id: process.env.AUTH_CLIENT_ID,
        client_secret: process.env.AUTH_CLIENT_SECRET,
        username: email,
        password,
    });
    let token;
    try {
        const res = await fetch(issuer.replace(/\/$/, '') + '/protocol/openid-connect/token', {
            method: 'POST',
            headers: { 'content-type': 'application/x-www-form-urlencoded' },
            body,
            signal: AbortSignal.timeout(8000),
        });
        if (!res.ok)
            return null;
        token = await res.json();
    }
    catch {
        return null;
    }
    // Roles come from the realm token; sites come from our own grant table.
    let realmRoles = [];
    try {
        const payload = JSON.parse(Buffer.from(token.access_token.split('.')[1], 'base64').toString('utf8'));
        realmRoles = payload?.realm_access?.roles ?? [];
    }
    catch { /* leave empty */ }
    const grants = await query(`select site, valid_to from grants where email = $1 order by site`, [email]);
    const today = new Date().toISOString().slice(0, 10);
    const sites = grants.filter((g) => g.valid_to >= today).map((g) => g.site);
    const roles = realmRoles.length ? realmRoles : roleFor(email);
    const s = { email, name: ACCOUNT_NAMES[email] ?? email, roles, sites };
    const tok = crypto.randomBytes(24).toString('hex');
    const expires = new Date(Date.now() + 12 * 3600 * 1000);
    await query(`insert into sessions(token, email, roles, sites, name, expires_at) values ($1,$2,$3,$4,$5,$6)`, [tok, s.email, JSON.stringify(s.roles), JSON.stringify(s.sites), s.name, expires.toISOString()]);
    return s;
}
function roleFor(email) {
    const map = {
        'plant@example.com': 'plant_operator',
        'analyst@example.com': 'lab_analyst',
        'quality@example.com': 'quality_manager',
        'claims@example.com': 'claims_manager',
        'signer@example.com': 'certificate_signer',
        'signer2@example.com': 'certificate_signer',
        'auditor@example.com': 'auditor',
    };
    const r = map[email];
    return r ? [r] : [];
}
export async function getSession(token) {
    if (!token)
        return null;
    const rows = await query(`select email, roles, sites, name, expires_at from sessions where token = $1`, [token]);
    if (!rows.length)
        return null;
    const r = rows[0];
    if (new Date(r.expires_at).getTime() < Date.now()) {
        await query(`delete from sessions where token = $1`, [token]);
        return null;
    }
    // A role change or an expired grant never validates retroactively: re-read grants.
    const grants = await query(`select site, valid_to from grants where email = $1 order by site`, [r.email]);
    const today = new Date().toISOString().slice(0, 10);
    const sites = grants.filter((g) => g.valid_to >= today).map((g) => g.site);
    return { email: r.email, name: r.name, roles: r.roles, sites };
}
export function bearer(req) {
    const h = req.headers.get('authorization') ?? '';
    const m = /^Bearer\s+(.+)$/i.exec(h);
    return m ? m[1].trim() : undefined;
}
