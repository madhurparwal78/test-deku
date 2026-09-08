import { query } from './lib/db.js';
const DDL = `
CREATE TABLE IF NOT EXISTS schema_version (version integer primary key, applied_on timestamptz not null default now());

CREATE TABLE IF NOT EXISTS sites (
  reference text primary key, name text not null, confidence text not null,
  nameplate_kg bigint not null, contracted_kg bigint not null, capacity_basis text not null,
  certification_state text not null, last_revised date not null
);

CREATE TABLE IF NOT EXISTS grants (
  email text not null, role text not null, site text not null references sites(reference),
  valid_to date not null
);

CREATE TABLE IF NOT EXISTS parties (
  reference text primary key, kind text not null, current_name text not null
);
CREATE TABLE IF NOT EXISTS party_versions (
  reference bigserial primary key, party text not null references parties(reference),
  name text not null, effective_from date not null, recorded_on date not null default current_date
);
CREATE UNIQUE INDEX IF NOT EXISTS party_versions_uq on party_versions(party, effective_from);

CREATE TABLE IF NOT EXISTS collectors (
  reference text primary key, name text not null, country text not null,
  registration text not null, registration_expiry date not null,
  site_types jsonb not null default '[]', streams jsonb not null default '[]', scheme_status text not null
);
CREATE TABLE IF NOT EXISTS approval_periods (
  reference bigserial primary key, collector text not null references collectors(reference),
  state text not null, valid_from date not null, valid_to date not null,
  condition text, condition_closes_on date, recorded_on date not null default current_date
);

CREATE TABLE IF NOT EXISTS devices (
  reference text primary key, site text not null references sites(reference), calibrated_on date not null
);

CREATE TABLE IF NOT EXISTS batches (
  reference text primary key, collector text not null references collectors(reference),
  site text not null references sites(reference), grade text not null default 'N6',
  category text not null, gross_g bigint not null, tare_g bigint not null, net_g bigint not null,
  moisture_bp integer not null, moisture_method text not null, device text not null references devices(reference),
  received_on date not null, composition jsonb not null default '[]', contamination jsonb not null default '{}',
  accepted_g bigint, rejected_g bigint, rejected_destination text, rejected_reason text,
  claimable_from date, collector_name_snapshot text, state text not null default 'accepted',
  created_at timestamptz not null default now()
);

CREATE TABLE IF NOT EXISTS custody_links (
  reference bigserial primary key, batch text not null references batches(reference),
  kind text not null, occurred_on date not null, party text not null, position integer not null,
  late_document boolean not null default false, arrived_on date
);

CREATE TABLE IF NOT EXISTS findings (
  reference bigserial primary key, collector text not null references collectors(reference),
  kind text not null, detail jsonb not null, state text not null default 'open', recorded_on date not null default current_date
);

CREATE TABLE IF NOT EXISTS runs (
  reference text primary key, run_type text not null, site text not null references sites(reference),
  grade text not null default 'N6', equipment text not null, recipe_version text not null,
  operator text not null, started_at timestamptz not null, closed_at timestamptz, opened_by text,
  losses_g bigint, within_tolerance boolean, set_points jsonb, annotation text, state text not null default 'open'
);
CREATE TABLE IF NOT EXISTS consumptions (
  reference text primary key, run text not null references runs(reference),
  input_kind text not null, input_reference text not null, mass_g bigint not null,
  effective_on date not null, recorded_at timestamptz not null default now(), event_at timestamptz not null default now(),
  recorded_by text
);
CREATE TABLE IF NOT EXISTS outputs (
  reference text primary key, run text not null references runs(reference), kind text not null,
  mass_g bigint not null, disposition text, grade text, created_at timestamptz not null default now()
);
CREATE TABLE IF NOT EXISTS lots (
  reference text primary key, run text not null references runs(reference), output text not null references outputs(reference),
  site text not null references sites(reference), grade text not null, mass_g bigint not null,
  disposition text not null default 'pending', claim_type text not null, blend_parents jsonb,
  created_at timestamptz not null default now()
);

CREATE TABLE IF NOT EXISTS test_results (
  reference text primary key, lot text references lots(reference), batch text references batches(reference),
  property text not null, method text not null, instrument text, analyst text not null,
  value text not null, unit text not null, uncertainty_bp integer, recorded_on date not null default current_date
);
CREATE TABLE IF NOT EXISTS deviations (
  reference text primary key, state text not null default 'open', runs text[] not null default '{}',
  lots text[] not null default '{}', raised_by text not null, raised_on date not null default current_date,
  outcome text, closed_on date, description text
);
CREATE TABLE IF NOT EXISTS overrides (
  reference text primary key, separation text not null, reason text not null, lot text not null references lots(reference),
  authorised_by text not null, authorised_on date not null default current_date,
  reviewed boolean not null default false, reviewed_by text, reviewed_on date
);

CREATE TABLE IF NOT EXISTS conversion_factors (
  reference text primary key, site text not null references sites(reference), factor_bp integer not null,
  derived_from date, derived_to date, derived_in_g bigint not null default 0, derived_out_g bigint not null default 0,
  provisional boolean not null default false, published_by text not null, published_on date not null default current_date
);

CREATE TABLE IF NOT EXISTS balance_periods (
  id text primary key, site text not null references sites(reference), grade text not null,
  period_from date not null, period_to date not null, state text not null default 'open',
  carry_over_limit_bp integer not null, closed_on date, cut_off date,
  allocation_basis text not null default 'mass', conversion_factor text references conversion_factors(reference),
  carried_forward_g jsonb, expired_g jsonb
);

CREATE TABLE IF NOT EXISTS credit_movements (
  reference text primary key, period text not null references balance_periods(id),
  kind text not null, category text not null, mass_g bigint not null,
  factor_version text, origin_site text, movement text, created_by text not null,
  lot text references lots(reference), effective_on date not null,
  event_at timestamptz not null default now(), recorded_at timestamptz not null default now(),
  decided_by text, favoured_over jsonb
);

CREATE TABLE IF NOT EXISTS carbon_methods (
  key text not null, version integer not null, standard text not null, functional_unit text not null,
  boundary text not null, allocation_basis text not null, reviewer text not null, published_on date not null,
  published_by text not null, data_quality jsonb not null default '{}', emission_factors jsonb not null default '[]',
  primary_share_threshold_bp integer not null default 5000, state text not null default 'current',
  primary key (key, version)
);
CREATE TABLE IF NOT EXISTS carbon_figures (
  id text primary key, lot text not null references lots(reference), method_key text not null, method_version integer not null,
  value_mg_per_kg bigint not null, uncertainty_bp integer not null, primary_share_bp integer not null,
  comparator jsonb not null, breakdown jsonb not null, energy_location_mg_per_kg bigint not null,
  energy_market_mg_per_kg bigint not null, metered_kwh bigint not null, retired_kwh bigint not null default 0,
  unmatched_kwh bigint not null default 0, computed_on date not null default current_date,
  computed_by text not null, cache_valid boolean not null default true, superseded_by text, reason text,
  primary_share_threshold_bp integer not null default 5000, boundary text not null default ''
);
CREATE TABLE IF NOT EXISTS period_energy (
  period text primary key, metered_kwh bigint not null
);
CREATE TABLE IF NOT EXISTS energy_instruments (
  reference text primary key, quantity_kwh bigint not null, vintage integer not null, region text not null,
  state text not null, period text references balance_periods(id)
);

CREATE TABLE IF NOT EXISTS specifications (
  grade text not null, version integer not null, issued_on date not null, state text not null default 'current',
  rows jsonb not null, virgin_reference jsonb not null, primary key (grade, version)
);
CREATE TABLE IF NOT EXISTS customers (
  reference text primary key, contact text not null, holds jsonb not null, application text not null,
  industry text not null, name text not null
);
CREATE TABLE IF NOT EXISTS conformances (
  reference bigserial primary key, customer text not null references customers(reference),
  specification text not null, spec_version integer not null, application text not null,
  trials jsonb not null default '[]', outcome text, opened_on date not null default current_date
);
CREATE TABLE IF NOT EXISTS change_notices (
  reference text primary key, description text not null, specifications_affected jsonb not null default '[]',
  customers_affected jsonb not null default '[]', qualifications_affected jsonb not null default '[]',
  notice_period_days integer not null default 30, proposed_on date not null default current_date,
  released_on date, raised_by text not null, qualification_relevant boolean not null default false,
  notifications jsonb not null default '[]'
);
CREATE TABLE IF NOT EXISTS contracts (
  id text primary key, customer text not null references customers(reference), site text not null references sites(reference),
  period text not null, committed_kg bigint not null, floor_bp integer not null, delivered_kg bigint not null default 0,
  shortfall_consequence text not null, state text not null default 'on_track', unreachable_on date
);
CREATE TABLE IF NOT EXISTS allocations (
  reference bigserial primary key, contract text not null references contracts(id), lot text not null references lots(reference),
  mass_g bigint not null, decided_by text not null, favoured_over jsonb not null default '[]',
  allocated_on date not null default current_date
);

CREATE TABLE IF NOT EXISTS certificates (
  number text primary key, version integer not null default 1, site text not null references sites(reference),
  recipient text not null, recipient_name text not null, signer text not null, signer_name text,
  signed_at timestamptz not null,
  state text not null default 'issued', lots jsonb not null, grade text not null, specification_version integer not null,
  specification text not null, claim_type text not null, content_bp integer not null, category_split jsonb not null,
  period text not null references balance_periods(id), carbon_figure text references carbon_figures(id),
  method_version text not null, boundary text not null, uncertainty_bp integer not null,
  primary_share_bp integer not null, scheme text not null, registration text not null,
  test_results jsonb not null default '[]', permitted_statement text not null, prohibited_statement text not null,
  conditions jsonb not null default '[]', provisional_factor boolean not null default false,
  withdrawn_by text, withdrawn_on date, withdrawal_reason text, derived_from text, void_statements jsonb,
  notified_recipients jsonb, input_versions jsonb not null default '{}', reissued_as text
);
CREATE TABLE IF NOT EXISTS cert_sequences (
  site text primary key, next_number integer not null default 1
);
CREATE TABLE IF NOT EXISTS restatements (
  reference text primary key, period text not null references balance_periods(id), reason text not null,
  opened_on date not null default current_date, opened_by text not null, state text not null default 'open',
  affected_certificates jsonb not null default '[]', content_movements jsonb, factor_reference text
);
CREATE TABLE IF NOT EXISTS resolutions (
  reference bigserial primary key, restatement text not null references restatements(reference),
  certificate text not null, outcome text not null, reason text not null,
  resolved_on date not null default current_date, resolved_by text not null
);
CREATE UNIQUE INDEX IF NOT EXISTS resolutions_uq on resolutions(restatement, certificate);

CREATE TABLE IF NOT EXISTS transfers (
  reference text primary key, from_period text not null references balance_periods(id),
  to_period text not null references balance_periods(id), mass_g bigint not null, category text not null,
  moved_on date not null default current_date, moved_by text not null
);

CREATE TABLE IF NOT EXISTS site_certifications (
  reference bigserial primary key, site text not null references sites(reference), state text not null,
  valid_from date not null, valid_to date, recorded_on date not null default current_date,
  lifted_on date, effective_from date not null, grade text
);

CREATE TABLE IF NOT EXISTS idempotency (
  key text not null, route text not null, body_hash text not null, status integer not null,
  response jsonb not null, created_at timestamptz not null default now(), primary key (key, route)
);

CREATE TABLE IF NOT EXISTS sessions (
  token text primary key, email text not null, roles jsonb not null, sites jsonb not null,
  name text not null, expires_at timestamptz not null, created_at timestamptz not null default now()
);

CREATE TABLE IF NOT EXISTS inbound_records (
  reference text primary key, source text not null, received_at timestamptz not null,
  payload_verbatim text not null, payload jsonb not null
);

CREATE TABLE IF NOT EXISTS record_entries (
  seq bigserial primary key, digest text not null, prev_digest text not null, act text not null,
  person text, site text, object text, content jsonb not null, correction_of bigint,
  event_at timestamptz not null default now(), recorded_at timestamptz not null default now(),
  legal_hold boolean not null default false, retain_until date, content_deleted_on date
);
CREATE INDEX IF NOT EXISTS record_entries_seq on record_entries(seq);

CREATE TABLE IF NOT EXISTS legal_holds (
  reference text primary key, seq bigint not null references record_entries(seq),
  placed_on date not null default current_date, placed_by text not null, lifted_on date, lifted_by text
);

CREATE TABLE IF NOT EXISTS exports (
  reference text primary key, scope jsonb not null, by text not null, exported_on date not null default current_date,
  entry_seq bigint, entry_count integer not null default 0, result jsonb
);

CREATE TABLE IF NOT EXISTS enquiries (
  reference text primary key, type text not null, name text not null, email text not null,
  message text not null, destination text not null, response_days integer not null,
  created_on date not null default current_date
);

CREATE TABLE IF NOT EXISTS positions (
  reference bigserial primary key, title text not null, location text not null, department text not null,
  contract_type text not null, closes_on date not null
);
CREATE TABLE IF NOT EXISTS news_items (
  reference bigserial primary key, title text not null, tag text not null, dated_on date not null,
  outlet text not null, link text not null, language text not null, coverage jsonb not null default '[]'
);
CREATE TABLE IF NOT EXISTS statistics (
  key text primary key, value text not null, source text not null, year text not null, geography text not null
);
CREATE TABLE IF NOT EXISTS claim_substantiation (
  reference bigserial primary key, claim text not null, route text not null, first_published_on date not null,
  evidence jsonb not null, method_version text not null, approver text not null, review_on date not null,
  withdrawn_on date
);

CREATE TABLE IF NOT EXISTS carbon_emission_factor_versions (
  id bigserial primary key, factor_key text not null, version integer not null, created_on date not null default current_date
);
`;
export async function migrate() {
    await query(DDL);
    await query(`INSERT INTO schema_version(version) VALUES (1) ON CONFLICT DO NOTHING`);
    console.log('migrations applied');
}
if (import.meta.url === `file://${process.argv[1]}`) {
    migrate().then(() => process.exit(0)).catch((e) => { console.error(e); process.exit(1); });
}
