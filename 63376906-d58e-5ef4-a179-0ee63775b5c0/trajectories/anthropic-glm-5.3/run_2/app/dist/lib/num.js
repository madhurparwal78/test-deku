import crypto from 'node:crypto';
/** Floor a rational to an integer. Never rounds, never carries at half. */
export function fl(n) {
    return n >= 0 ? Math.floor(n) : -Math.floor(-n);
}
/** Floor of (a * b) / c over integers, exact via BigInt. */
export function flMulDiv(a, b, c) {
    return Number((BigInt(Math.trunc(a)) * BigInt(Math.trunc(b))) / BigInt(Math.trunc(c)));
}
export function sha256(s) {
    return crypto.createHash('sha256').update(s).digest('hex');
}
export function newReference(prefix) {
    return prefix + '-' + crypto.randomBytes(6).toString('hex').toUpperCase();
}
export function bodyHash(body) {
    return sha256(stableStringify(body));
}
export function stableStringify(v) {
    if (v === null || typeof v !== 'object')
        return JSON.stringify(v) ?? 'null';
    if (Array.isArray(v))
        return '[' + v.map(stableStringify).join(',') + ']';
    const keys = Object.keys(v).sort();
    return '{' + keys.map((k) => JSON.stringify(k) + ':' + stableStringify(v[k])).join(',') + '}';
}
