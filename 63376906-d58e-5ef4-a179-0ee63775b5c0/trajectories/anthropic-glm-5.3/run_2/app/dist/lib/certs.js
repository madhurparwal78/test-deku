import { query } from './db.js';
import { sendMail } from './mail.js';
export const CLAIM_COPY = {
    mass_balance: {
        permitted: 'may state that the material is credited as containing recycled content under a mass-balance chain of custody',
        prohibited: 'may not state that this material physically contains recycled content',
    },
    controlled_blending: {
        permitted: 'may state that the material is produced under controlled blending and carries recycled content allocated by mass',
        prohibited: 'may not state that this material is physically segregated recycled content',
    },
    physically_segregated: {
        permitted: 'may state that the material is physically segregated recycled content',
        prohibited: 'may not state a recycled-content percentage above the measured figure',
    },
};
export function statementsFor(claimType, contentBp, split) {
    const copy = CLAIM_COPY[claimType] ?? CLAIM_COPY.mass_balance;
    const pct = describeBp(contentBp);
    const cats = Object.entries(split).map(([k, v]) => `${describeBp(Number(v))} ${k.replace('_', '-')}`).join(' and ');
    return {
        permitted_statement: `The recipient ${copy.permitted} at ${pct} recycled content by mass (${cats}). ` +
            `The recipient may quote the figure ${pct} at the same weight as the certificate, and may not round it upward.`,
        prohibited_statement: `The recipient ${copy.prohibited}. ${claimType === 'mass_balance' ? 'This material is claimed by mass balance. It is not physically segregated.' : ''}`,
    };
}
export function describeBp(bp) {
    const whole = Math.floor(bp / 100);
    const frac = bp % 100;
    return frac === 0 ? `${whole}` : `${whole}.${String(frac).padStart(2, '0')}`;
}
export const CERT_CONDITIONS = [
    'lot_released',
    'no_open_deviation',
    'no_unreviewed_override',
    'period_closed',
    'balance_invariant_holds',
    'carbon_figure_complete',
    'signer_scope_valid',
    'signer_not_data_enterer',
];
/** The eight conditions, decided against the records as they stand now. */
export async function evaluateConditions(params) {
    const lot = (await query(`select * from lots where reference = $1`, [params.lot]))[0];
    const period = (await query(`select * from balance_periods where id = $1`, [params.period]))[0];
    const out = [];
    const released = lot?.disposition === 'released';
    out.push({ condition: 'lot_released', satisfied: released, blocking_reference: released ? null : params.lot,
        detail: released ? `Lot ${params.lot} is released.` : `Lot ${params.lot} is ${lot?.disposition ?? 'unknown'} and must be released before a certificate may be signed.` });
    const openDev = (await query(`select reference from deviations where state = 'open' and lots && $1::text[] limit 1`, [[params.lot]]))[0];
    out.push({ condition: 'no_open_deviation', satisfied: !openDev, blocking_reference: openDev?.reference ?? null,
        detail: openDev ? `Deviation ${openDev.reference} is open and touches this lot.` : `No open deviation touches this lot.` });
    const ovr = (await query(`select reference from overrides where lot = $1 and reviewed = false limit 1`, [params.lot]))[0];
    out.push({ condition: 'no_unreviewed_override', satisfied: !ovr, blocking_reference: ovr?.reference ?? null,
        detail: ovr ? `Override ${ovr.reference} on this lot is unreviewed. A second person must review it before signing.` : `Every override on this lot has been reviewed.` });
    const closed = period?.state === 'closed';
    out.push({ condition: 'period_closed', satisfied: closed, blocking_reference: closed ? null : params.period,
        detail: closed ? `Bookkeeping period ${params.period} is closed.` : `Bookkeeping period ${params.period} is open. The period must be closed before signing.` });
    const invariant = await balanceInvariant(params.period, params.lot);
    out.push({ condition: 'balance_invariant_holds', satisfied: invariant.ok, blocking_reference: invariant.ok ? null : params.period,
        detail: invariant.ok
            ? `Credits attached to lots in this period do not exceed credits available.`
            : `Attaching this lot's claim would exceed the credits available in ${params.period}.` });
    const figure = await latestFigure(params.lot);
    const carbonOk = !!figure && figure.value_mg_per_kg !== null && figure.boundary && figure.method_version && figure.uncertainty_bp !== null;
    out.push({ condition: 'carbon_figure_complete', satisfied: carbonOk, blocking_reference: carbonOk ? null : params.lot,
        detail: carbonOk
            ? `A carbon figure exists with its boundary, method version and uncertainty.`
            : `No carbon figure with all four components exists for this lot.` });
    const scopeOk = await signerScopeValid(params.signer, params.site);
    out.push({ condition: 'signer_scope_valid', satisfied: scopeOk, blocking_reference: params.signer,
        detail: scopeOk
            ? `The signer holds signing scope for ${params.site} on this date.`
            : `The signer does not hold signing scope for ${params.site}.` });
    const entered = await signerEnteredData(params.signer, params.lot);
    out.push({ condition: 'signer_not_data_enterer', satisfied: !entered, blocking_reference: entered ? params.signer : null,
        detail: entered
            ? `The signer entered data recorded against this lot and may not sign it.`
            : `The signer entered no data recorded against this lot.` });
    return out;
}
export async function latestFigure(lot) {
    const rows = await query(`select * from carbon_figures where lot = $1 and superseded_by is null order by computed_on desc, id desc limit 1`, [lot]);
    return rows[0] ?? null;
}
export async function signerScopeValid(signer, site, on) {
    const day = on ?? new Date().toISOString().slice(0, 10);
    const rows = await query(`select 1 from grants where email = $1 and site = $2 and role = 'certificate_signer' and $3 <= valid_to`, [signer, site, day]);
    return rows.length > 0;
}
export async function rolesOf(email) {
    const rows = await query(`select distinct role from grants where email = $1`, [email]);
    return rows.map((r) => r.role);
}
export async function signerEnteredData(signer, lot) {
    const t = await query(`select 1 from test_results where lot = $1 and analyst = $2 limit 1`, [lot, signer]);
    if (t.length)
        return true;
    const cons = await query(`select 1 from consumptions c join runs r on r.reference = c.run where r.site = (select site from lots where reference = $1)
       and c.recorded_by = $2 limit 1`, [lot, signer]);
    void cons;
    const allocs = await query(`select 1 from credit_movements where lot = $1 and created_by = $2 limit 1`, [lot, signer]);
    return allocs.length > 0;
}
/** Credits attached never exceed credits available, with this lot's allocation applied. */
export async function balanceInvariant(period, lot) {
    const movs = await query(`select * from credit_movements where period = $1`, [period]);
    const attached = movs.filter((m) => m.kind === 'out' && m.lot === lot);
    if (!attached.length)
        return { ok: true, margin_g: 0 };
    let ok = true;
    let worst = Number.MAX_SAFE_INTEGER;
    for (const cat of ['post_consumer', 'pre_consumer']) {
        const inG = movs.filter((m) => m.kind === 'in' && m.category === cat && !m.origin_site).reduce((s, m) => s + Number(m.mass_g), 0);
        const outG = movs.filter((m) => m.kind === 'out' && m.category === cat).reduce((s, m) => s + Number(m.mass_g), 0);
        const margin = inG - outG;
        if (outG > inG)
            ok = false;
        worst = Math.min(worst, margin);
    }
    return { ok, margin_g: worst === Number.MAX_SAFE_INTEGER ? 0 : worst };
}
/** The bookkeeping period a lot belongs to, decided by its site, grade and creation date. */
export async function periodForLot(lotRef) {
    const l = (await query(`select * from lots where reference = $1`, [lotRef]))[0];
    if (!l)
        return null;
    const rows = await query(`select * from balance_periods where site = $1 and grade = $2 and $3 between period_from and period_to`, [l.site, l.grade, new Date(l.created_at).toISOString().slice(0, 10)]);
    if (rows.length)
        return rows[0];
    const anyP = await query(`select * from balance_periods where site = $1 and grade = $2 order by period_from desc limit 1`, [l.site, l.grade]);
    return anyP[0] ?? null;
}
export async function issueNumber(c, site) {
    await c.query(`insert into cert_sequences(site, next_number) values ($1, 2) on conflict (site) do nothing`, [site]);
    const row = await c.query(`update cert_sequences set next_number = next_number + 1 where site = $1 returning next_number - 1 as issued`, [site]);
    const n = Number(row.rows[0].issued);
    return `CERT-${site.replace('SITE-', '')}-${String(n).padStart(6, '0')}`;
}
export function verificationUrl(number) {
    const base = process.env.APP_PUBLIC_URL?.replace(/\/$/, '') ?? 'https://ravel.example.com';
    return `${base.replace(/\/$/, '')}/verify/${number}`;
}
export async function notifySigned(cert, to) {
    await sendMail(to, `Certificate ${cert.number} issued`, `Certificate ${cert.number} issued\n\n` +
        `Number: ${cert.number}\n` +
        `Claim type: ${cert.claim_type}\n` +
        `Recycled content: ${describeBp(cert.content_bp)} per cent\n` +
        `Permitted statement: ${cert.permitted_statement}\n`);
}
export async function notifyWithdrawn(cert, to, voidStatements) {
    await sendMail(to, `Certificate ${cert.number} withdrawn`, `Certificate ${cert.number} withdrawn\n\n` +
        `Number: ${cert.number}\n` +
        `Reason: ${cert.withdrawal_reason}\n` +
        `Every statement now void:\n` + voidStatements.map((s) => `- ${s}`).join('\n') + '\n');
}
/** Byte-stable plain-text document for a certificate version. */
export function renderDocument(cert, extra = {}) {
    const L = [];
    L.push('RAVEL MATERIALS — RECYCLED CONTENT CERTIFICATE');
    L.push('');
    L.push(`Certificate number: ${cert.number}`);
    L.push(`Version: ${cert.version}`);
    if (cert.state === 'withdrawn') {
        L.push(`State: WITHDRAWN`);
        L.push(`Withdrawn on: ${cert.withdrawn_on}. Reason: ${cert.withdrawal_reason}.`);
    }
    else {
        L.push(`State: ${cert.state}`);
    }
    L.push(`Site: ${cert.site}`);
    L.push(`Grade: ${cert.grade}`);
    L.push(`Specification: ${cert.specification} version ${cert.specification_version}`);
    L.push(`Claim type: ${cert.claim_type}`);
    L.push(`Recycled content: ${describeBp(cert.content_bp)} per cent by mass`);
    L.push(`Category split: ${Object.entries(cert.category_split ?? {}).map(([k, v]) => `${k} ${describeBp(Number(v))} per cent`).join(', ')}`);
    L.push(`Bookkeeping period: ${cert.period}`);
    L.push('');
    L.push('CARBON FOOTPRINT');
    L.push(`Value: ${cert.value_mg_per_kg} mg CO2e per kg of product`);
    L.push(`Boundary: ${cert.boundary}`);
    L.push(`Method version: ${cert.method_version}`);
    L.push(`Uncertainty: ${describeBp(cert.uncertainty_bp)} per cent`);
    L.push(`Comparator: ${cert.comparator?.material} — dataset ${cert.comparator?.dataset} ${cert.comparator?.dataset_year}, region ${cert.comparator?.region}`);
    L.push(`Primary data share: ${describeBp(cert.primary_share_bp)} per cent`);
    L.push('');
    L.push('PERMITTED STATEMENT');
    L.push(cert.permitted_statement);
    L.push('');
    L.push('PROHIBITED STATEMENT');
    L.push(cert.prohibited_statement);
    L.push('');
    L.push('CERTIFIED LOTS');
    for (const l of cert.lots ?? [])
        L.push(`- ${l.reference} ${l.mass_g} g`);
    L.push('');
    L.push(`Scheme: ${cert.scheme}`);
    L.push(`Registration: ${cert.registration}`);
    L.push(`Recipient: ${cert.recipient_name} (${cert.recipient})`);
    L.push(`Signed by: ${cert.signer_name ?? cert.signer} on ${String(cert.signed_at).slice(0, 10)}`);
    if (cert.provisional_factor) {
        L.push('');
        L.push('This certificate rests on a provisional conversion factor and says so.');
    }
    L.push('');
    L.push(`Verify this certificate at ravel.example.com/verify/${cert.number}`);
    for (const [k, v] of Object.entries(extra))
        L.push(`${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}`);
    return L.join('\n') + '\n';
}
