import { sha256, stableStringify } from './num.js';
export const GENESIS = '0'.repeat(64);
/** Appends an entry to the hash-chained record, inside the caller's transaction. */
export async function appendEntry(c, e) {
    const prev = await c.query(`select seq, digest from record_entries order by seq desc limit 1`);
    const prevSeq = prev.rows.length ? Number(prev.rows[0].seq) : null;
    const prevDigest = prev.rows.length ? prev.rows[0].digest : GENESIS;
    const content = e.content ?? {};
    // Digest over a canonical form, so a reader recomputing it from the stored row agrees.
    const payload = JSON.stringify({
        act: e.act, person: e.person ?? null, site: e.site ?? null, object: e.object ?? null,
        content: JSON.parse(stableStringify(content)), correction_of: e.correction_of ?? null,
        prev_seq: prevSeq, prev_digest: prevDigest,
    });
    const digest = sha256(payload);
    const ins = await c.query(`insert into record_entries(act, person, site, object, content, correction_of, digest, prev_digest, event_at)
     values ($1,$2,$3,$4,$5,$6,$7,$8, coalesce($9, now())) returning seq, digest, prev_digest`, [e.act, e.person ?? null, e.site ?? null, e.object ?? null, JSON.stringify(content),
        e.correction_of ?? null, digest, prevDigest, e.event_at ?? null]);
    return ins.rows[0];
}
/** Retention basis, shared by the retention route and the expire route. */
export function retentionFor(entry) {
    const schemeMonths = 120;
    const statutoryMonths = 84;
    const eventAt = new Date(entry.event_at ?? entry.recorded_at);
    const addMonths = (d, m) => {
        const out = new Date(d.getTime());
        out.setUTCMonth(out.getUTCMonth() + m);
        return out.toISOString().slice(0, 10);
    };
    const schemeUntil = addMonths(eventAt, schemeMonths);
    const statutoryUntil = addMonths(eventAt, statutoryMonths);
    let referencedUntil = null;
    const referenced = entry?.content?.referenced_until;
    if (typeof referenced === 'string')
        referencedUntil = referenced;
    const candidates = [schemeUntil, statutoryUntil, referencedUntil].filter(Boolean);
    const retainUntil = candidates.sort().at(-1);
    return { scheme_months: schemeMonths, statutory_months: statutoryMonths, referenced_until: referencedUntil, retain_until: retainUntil };
}
