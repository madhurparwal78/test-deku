import { query, withTransaction } from './lib/db.js';
import { appendEntry } from './lib/record.js';
import { sha256 } from './lib/num.js';

export async function seedCore() {
  await withTransaction(async (c) => {
    // ---- sites ----
    await c.query(`insert into sites values ($1,$2,$3,$4,$5,$6,$7,$8)`, [
      'SITE-PILOT', 'Pilot', 'commissioned', 40000, 24000, '8000 hours per year, 0.90 availability, 0.80 yield', 'certified', '2026-06-30']);
    await c.query(`insert into sites values ($1,$2,$3,$4,$5,$6,$7,$8)`, [
      'SITE-DEMO', 'Demonstration', 'commissioned', 400000, 320000, '8000 hours per year, 0.90 availability, 0.80 yield', 'certified', '2026-06-30']);
    await c.query(`insert into sites values ($1,$2,$3,$4,$5,$6,$7,$8)`, [
      'SITE-COMM', 'Commercial', 'planned', 25000000, 26000000, '8000 hours per year, 0.90 availability, 0.80 yield', 'not_certified', '2026-06-30']);

    // ---- grants ----
    const grants: [string, string, string][] = [
      ['plant@example.com', 'plant_operator', 'SITE-DEMO'],
      ['plant@example.com', 'plant_operator', 'SITE-PILOT'],
      ['analyst@example.com', 'lab_analyst', 'SITE-DEMO'],
      ['analyst@example.com', 'lab_analyst', 'SITE-PILOT'],
      ['quality@example.com', 'quality_manager', 'SITE-DEMO'],
      ['quality@example.com', 'quality_manager', 'SITE-PILOT'],
      ['claims@example.com', 'claims_manager', 'SITE-DEMO'],
      ['claims@example.com', 'claims_manager', 'SITE-PILOT'],
      ['signer@example.com', 'certificate_signer', 'SITE-DEMO'],
      ['signer@example.com', 'certificate_signer', 'SITE-PILOT'],
      ['signer2@example.com', 'certificate_signer', 'SITE-PILOT'],
      ['auditor@example.com', 'auditor', 'SITE-DEMO'],
      ['auditor@example.com', 'auditor', 'SITE-PILOT'],
    ];
    for (const [email, role, site] of grants) {
      await c.query(`insert into grants(email, role, site, valid_to) values ($1,$2,$3,$4)`, [email, role, site, '2027-06-30']);
    }

    // ---- parties and collectors ----
    await c.query(`insert into parties values ('COL-ALDER','collector','Alder Reclaim')`);
    await c.query(`insert into parties values ('COL-BRINE','collector','Brine Circular Materials')`);
    await c.query(`insert into parties values ('COL-CINDER','collector','Cinder Industrial Offcuts')`);
    await c.query(`insert into parties values ('CUS-HELIOS','customer','Helios Textiles')`);
    await c.query(`insert into parties values ('CUS-VANTA','customer','Vanta Automotive Fabrics')`);
    await c.query(`insert into parties values ('RAVEL','producer','Ravel Materials SAS')`);
    await c.query(`insert into party_versions(party, name, effective_from) values ('COL-ALDER','Alder Reclaim','2026-01-01')`);
    await c.query(`insert into party_versions(party, name, effective_from) values ('COL-BRINE','Brine Textile Recovery','2026-01-01')`);
    await c.query(`insert into party_versions(party, name, effective_from) values ('COL-BRINE','Brine Circular Materials','2026-08-01')`);
    await c.query(`insert into party_versions(party, name, effective_from) values ('COL-CINDER','Cinder Industrial Offcuts','2026-01-01')`);

    await c.query(`insert into collectors values ($1,$2,$3,$4,$5,$6,$7,$8)`,
      ['COL-ALDER', 'Alder Reclaim', 'PT', 'WCR-PT-4471', '2027-03-31',
        JSON.stringify(['kerbside', 'retail_take_back']), JSON.stringify(['fishing_nets', 'carpet', 'textile_offcuts']), 'member']);
    await c.query(`insert into collectors values ($1,$2,$3,$4,$5,$6,$7,$8)`,
      ['COL-BRINE', 'Brine Textile Recovery', 'NL', 'WCR-NL-2208', '2027-01-31',
        JSON.stringify(['industrial_laundry']), JSON.stringify(['textile_offcuts']), 'member']);
    await c.query(`insert into collectors values ($1,$2,$3,$4,$5,$6,$7,$8)`,
      ['COL-CINDER', 'Cinder Industrial Offcuts', 'FR', 'WCR-FR-6613', '2026-12-31',
        JSON.stringify(['factory_offcut']), JSON.stringify(['coated_offcuts']), 'conditional']);

    await c.query(`insert into approval_periods(collector, state, valid_from, valid_to) values ('COL-ALDER','approved','2026-01-01','2026-12-31')`);
    await c.query(`insert into approval_periods(collector, state, valid_from, valid_to) values ('COL-BRINE','approved','2026-01-01','2026-06-30')`);
    await c.query(`insert into approval_periods(collector, state, valid_from, valid_to, condition, condition_closes_on)
      values ('COL-CINDER','conditional','2026-01-01','2026-12-31','Sampling plan for coated streams to be agreed','2026-10-31')`);

    await c.query(`insert into devices values ('WB-DEMO-01','SITE-DEMO','2026-05-01')`);
    await c.query(`insert into devices values ('WB-DEMO-02','SITE-DEMO','2025-02-01')`);

    // ---- findings ----
    await c.query(`insert into findings(collector, kind, detail, state, recorded_on) values ($1,$2,$3,'open','2026-03-01')`,
      ['COL-CINDER', 'declaration_departure',
        JSON.stringify({ batch: 'BATCH-1004', declared_fraction_bp: 9900, measured_fraction_bp: 9100, departure_bp: 800 })]);
    await c.query(`insert into findings(collector, kind, detail, state, recorded_on) values ($1,$2,$3,'open','2026-03-04')`,
      ['COL-CINDER', 'condition_unclosed', JSON.stringify({ condition: 'Sampling plan for coated streams to be agreed', closes_on: '2026-10-31' })]);
  });
  console.log('seed: sites, collectors, grants');
}

export async function seedBatches() {
  const rows = [
    { reference: 'BATCH-1001', collector: 'COL-ALDER', site: 'SITE-DEMO', grade: 'N6', category: 'post_consumer',
      gross: 520000, tare: 20000, net: 500000, moisture: 1000, device: 'WB-DEMO-01', received: '2026-02-10',
      composition: [{ polymer: 'PA6', fraction_bp: 9200, basis: 'sampled', elastane_bp: 400, measured_fraction_bp: 9200 }],
      contamination: { non_nylon_bp: 500, elastane_bp: 400, coatings: 'none', colour_load: 'medium', foreign_matter: 'low' },
      omit: [] },
    { reference: 'BATCH-1002', collector: 'COL-ALDER', site: 'SITE-DEMO', grade: 'N6', category: 'pre_consumer',
      gross: 320000, tare: 20000, net: 300000, moisture: 0, device: 'WB-DEMO-01', received: '2026-02-12',
      composition: [{ polymer: 'PA6', fraction_bp: 9500, basis: 'declared' }],
      contamination: { non_nylon_bp: 300, elastane_bp: 0, coatings: 'none', colour_load: 'low', foreign_matter: 'none' },
      omit: [] },
    { reference: 'BATCH-1003', collector: 'COL-BRINE', site: 'SITE-DEMO', grade: 'N6', category: 'post_consumer',
      gross: 220000, tare: 20000, net: 200000, moisture: 500, device: 'WB-DEMO-01', received: '2026-07-05',
      composition: [{ polymer: 'PA6', fraction_bp: 9000, basis: 'declared' }],
      contamination: { non_nylon_bp: 800, elastane_bp: 200, coatings: 'partial', colour_load: 'high', foreign_matter: 'medium' },
      omit: [] },
    { reference: 'BATCH-1004', collector: 'COL-CINDER', site: 'SITE-DEMO', grade: 'N6', category: 'pre_consumer',
      gross: 140000, tare: 20000, net: 120000, moisture: 0, device: 'WB-DEMO-02', received: '2026-02-20',
      composition: [{ polymer: 'PA6', fraction_bp: 9900, basis: 'declared', measured_fraction_bp: 9100 }],
      contamination: { non_nylon_bp: 900, elastane_bp: 0, coatings: 'partial', colour_load: 'high', foreign_matter: 'low' },
      omit: [] },
    { reference: 'BATCH-1005', collector: 'COL-ALDER', site: 'SITE-DEMO', grade: 'N6', category: 'post_consumer',
      gross: 110000, tare: 10000, net: 100000, moisture: 0, device: 'WB-DEMO-01', received: '2026-03-02',
      composition: [{ polymer: 'PA6', fraction_bp: 9300, basis: 'declared' }],
      contamination: { non_nylon_bp: 400, elastane_bp: 300, coatings: 'none', colour_load: 'medium', foreign_matter: 'low' },
      omit: ['transport'] },
  ];
  await withTransaction(async (c) => {
    for (const b of rows) {
      await c.query(
        `insert into batches(reference, collector, site, grade, category, gross_g, tare_g, net_g, moisture_bp,
            moisture_method, device, received_on, composition, contamination, collector_name_snapshot)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9,'ISO 15512',$10,$11,$12,$13,$14)`,
        [b.reference, b.collector, b.site, b.grade, b.category, b.gross, b.tare, b.net, b.moisture,
         b.device, b.received, JSON.stringify(b.composition), JSON.stringify(b.contamination),
         b.collector === 'COL-BRINE' ? 'Brine Textile Recovery' : b.collector === 'COL-ALDER' ? 'Alder Reclaim' : 'Cinder Industrial Offcuts']);
      await custody(c, b.reference, b.omit, b.received);
    }
  });
  console.log('seed: batches');
}

async function custody(c: any, batch: string, omit: string[], received: string) {
  const kinds: [string, string][] = [
    ['collection_site', 'Nordic Net Depot'],
    ['collector', 'Alder Reclaim'],
    ['transport', 'Haulier BAS'],
    ['arrival', 'Ravel Demonstration'],
    ['weighing', 'Ravel Demonstration'],
    ['acceptance', 'Ravel Demonstration'],
  ];
  let pos = 0;
  for (const [kind, party] of kinds) {
    if (!omit.includes(kind)) {
      await c.query(`insert into custody_links(batch, kind, occurred_on, party, position) values ($1,$2,$3,$4,$5)`,
        [batch, kind, received, party, pos]);
    }
    pos++;
  }
}

export async function seedRuns() {
  await withTransaction(async (c) => {
    const runRow = async (ref: string, type: string, site: string, equipment: string, recipe: string,
      started: string, closed: string, losses: number, within: boolean, setPoints: any) => {
      await c.query(
        `insert into runs(reference, run_type, site, grade, equipment, recipe_version, operator, started_at, closed_at,
            losses_g, within_tolerance, set_points, state, opened_by)
         values ($1,$2,$3,'N6',$4,$5,'plant@example.com',$6,$7,$8,$9,$10,'closed','plant@example.com')`,
        [ref, type, site, equipment, recipe, started, closed, losses, within, JSON.stringify(setPoints)]);
    };
    await runRow('RUN-D-0001', 'dissolution', 'SITE-DEMO', 'DISS-01', 'RCP-DISS-2', '2026-03-04T08:00:00Z', '2026-03-04T16:00:00Z', 120000, true, { temperature_c: 165, pressure_bar: 3, residence_min: 92 });
    await runRow('RUN-D-0002', 'dissolution', 'SITE-DEMO', 'DISS-01', 'RCP-DISS-2', '2026-03-11T08:00:00Z', '2026-03-11T16:00:00Z', 60000, true, { temperature_c: 166, pressure_bar: 3, residence_min: 90 });
    await runRow('RUN-D-0003', 'dissolution', 'SITE-DEMO', 'DISS-02', 'RCP-DISS-2', '2026-03-18T08:00:00Z', '2026-03-18T14:00:00Z', 30000, true, { temperature_c: 162, pressure_bar: 2, residence_min: 95 });
    await runRow('RUN-Y-0001', 'depolymerisation', 'SITE-DEMO', 'DEPO-01', 'RCP-DEPO-4', '2026-03-25T06:00:00Z', '2026-03-26T06:00:00Z', 50000, true, { temperature_c: 250, pressure_bar: 10, residence_min: 180 });
    await runRow('RUN-U-0001', 'purification', 'SITE-DEMO', 'PURI-01', 'RCP-PURI-1', '2026-04-02T06:00:00Z', '2026-04-03T06:00:00Z', 40000, true, { temperature_c: 188, pressure_bar: 5, residence_min: 122 });
    await runRow('RUN-R-0001', 'repolymerisation', 'SITE-DEMO', 'REPO-01', 'RCP-REPO-3', '2026-04-08T06:00:00Z', '2026-04-09T06:00:00Z', 20000, true, { temperature_c: 260, pressure_bar: 2, residence_min: 240 });

    const con = async (ref: string, run: string, kind: string, input: string, mass: number, eff: string) => {
      await c.query(
        `insert into consumptions(reference, run, input_kind, input_reference, mass_g, effective_on, recorded_by)
         values ($1,$2,$3,$4,$5,$6,'plant@example.com')`, [ref, run, kind, input, mass, eff]);
    };
    await con('CSM-D1-1', 'RUN-D-0001', 'batch', 'BATCH-1001', 300000, '2026-03-04');
    await con('CSM-D1-2', 'RUN-D-0001', 'batch', 'BATCH-1002', 300000, '2026-03-04');
    await con('CSM-D2-1', 'RUN-D-0002', 'batch', 'BATCH-1003', 190000, '2026-03-11');
    await con('CSM-D2-2', 'RUN-D-0002', 'batch', 'BATCH-1004', 120000, '2026-02-20');
    await con('CSM-D3-1', 'RUN-D-0003', 'batch', 'BATCH-1001', 150000, '2026-03-18');
    await con('CSM-Y1-1', 'RUN-Y-0001', 'intermediate', 'OUT-D-0001', 480000, '2026-03-25');
    await con('CSM-Y1-2', 'RUN-Y-0001', 'intermediate', 'OUT-D-0002', 250000, '2026-03-25');
    await con('CSM-Y1-3', 'RUN-Y-0001', 'intermediate', 'OUT-D-0003', 120000, '2026-03-25');
    await con('CSM-U1-1', 'RUN-U-0001', 'intermediate', 'OUT-Y-0001', 800000, '2026-04-02');
    await con('CSM-R1-1', 'RUN-R-0001', 'intermediate', 'OUT-U-0001', 720000, '2026-04-08');

    const out = async (ref: string, run: string, kind: string, mass: number, disposition: string | null) => {
      await c.query(`insert into outputs(reference, run, kind, mass_g, disposition, grade) values ($1,$2,$3,$4,$5,'N6')`,
        [ref, run, kind, mass, disposition]);
    };
    await out('OUT-D-0001', 'RUN-D-0001', 'intermediate', 480000, null);
    await out('OUT-D-0002', 'RUN-D-0002', 'intermediate', 250000, null);
    await out('OUT-D-0003', 'RUN-D-0003', 'intermediate', 120000, null);
    await out('OUT-Y-0001', 'RUN-Y-0001', 'intermediate', 800000, null);
    await out('OUT-U-0001', 'RUN-U-0001', 'intermediate', 720000, null);
    await out('OUT-U-0002', 'RUN-U-0001', 'byproduct', 40000, 'sold');
    await c.query(`insert into outputs(reference, run, kind, mass_g, disposition, grade) values ('OUT-R-0001','RUN-R-0001','lot',400000,null,'N6')`);
    await c.query(`insert into lots(reference, run, output, site, grade, mass_g, disposition, claim_type)
      values ('LOT-N6-0001','RUN-R-0001','OUT-R-0001','SITE-DEMO','N6',400000,'released','mass_balance')`);
    await c.query(`insert into outputs(reference, run, kind, mass_g, disposition, grade) values ('OUT-R-0002','RUN-R-0001','lot',300000,null,'N6')`);
    await c.query(`insert into lots(reference, run, output, site, grade, mass_g, disposition, claim_type)
      values ('LOT-N6-0002','RUN-R-0001','OUT-R-0002','SITE-DEMO','N6',300000,'quarantined','mass_balance')`);
    // The pilot lot, produced under a provisional factor.
    await c.query(`insert into runs(reference, run_type, site, grade, equipment, recipe_version, operator, started_at, closed_at,
        losses_g, within_tolerance, set_points, state, opened_by)
      values ('RUN-R-0002','repolymerisation','SITE-PILOT','N6','REPO-P1','RCP-REPO-3','plant@example.com','2026-03-01T06:00:00Z','2026-03-02T06:00:00Z',10000,true,$1,'closed','plant@example.com')`,
      [JSON.stringify({ temperature_c: 258, pressure_bar: 2, residence_min: 240 })]);
    await c.query(`insert into runs(reference, run_type, site, grade, equipment, recipe_version, operator, started_at, closed_at,
        losses_g, within_tolerance, set_points, state, opened_by)
      values ('RUN-P-0001','purification','SITE-PILOT','N6','PURI-P1','RCP-PURI-1','plant@example.com','2026-02-20T06:00:00Z','2026-02-21T06:00:00Z',10000,true,$1,'closed','plant@example.com')`,
      [JSON.stringify({ temperature_c: 185, pressure_bar: 5, residence_min: 120 })]);
    await c.query(`insert into outputs(reference, run, kind, mass_g, disposition, grade) values ('OUT-P-0000','RUN-P-0001','intermediate',210000,null,'N6')`);
    await c.query(`insert into consumptions(reference, run, input_kind, input_reference, mass_g, effective_on, recorded_by)
      values ('CSM-R2-1','RUN-R-0002','intermediate','OUT-P-0000',100000,'2026-03-01','plant@example.com')`);
    await c.query(`insert into outputs(reference, run, kind, mass_g, disposition, grade) values ('OUT-P-0001','RUN-R-0002','lot',200000,null,'N6')`);
    await c.query(`insert into lots(reference, run, output, site, grade, mass_g, disposition, claim_type)
      values ('LOT-N6-0003','RUN-R-0002','OUT-P-0001','SITE-PILOT','N6',200000,'released','mass_balance')`);
  });
  console.log('seed: runs and lots');
}

export async function seedLedger() {
  await withTransaction(async (c) => {
    await c.query(`insert into conversion_factors(reference, site, factor_bp, derived_from, derived_to, derived_in_g, derived_out_g, provisional, published_by, published_on)
      values ('CF-DEMO-1','SITE-DEMO',8000,'2026-01-01','2026-03-31',1000000,800000,false,'claims@example.com','2026-04-05')`);
    await c.query(`insert into conversion_factors(reference, site, factor_bp, derived_from, derived_to, derived_in_g, derived_out_g, provisional, published_by, published_on)
      values ('CF-PILOT-1','SITE-PILOT',7500,null,null,0,0,true,'claims@example.com','2026-01-05')`);

    await c.query(`insert into balance_periods(id, site, grade, period_from, period_to, state, carry_over_limit_bp, closed_on, cut_off, allocation_basis, conversion_factor)
      values ('BP-DEMO-N6-2025H2','SITE-DEMO','N6','2025-07-01','2025-12-31','closed',2000,'2026-01-15','2026-01-10','mass','CF-DEMO-1')`);
    await c.query(`insert into balance_periods(id, site, grade, period_from, period_to, state, carry_over_limit_bp, allocation_basis, conversion_factor)
      values ('BP-DEMO-N6-2026H1','SITE-DEMO','N6','2026-01-01','2026-06-30','open',2000,'mass','CF-DEMO-1')`);
    await c.query(`insert into balance_periods(id, site, grade, period_from, period_to, state, carry_over_limit_bp, allocation_basis, conversion_factor)
      values ('BP-PILOT-N6-2026H1','SITE-PILOT','N6','2026-01-01','2026-06-30','open',2000,'mass','CF-PILOT-1')`);

    // Credits granted at consumption: dry mass times the site factor, floored.
    const credit = async (ref: string, period: string, category: string, mass: number, eff: string, factor: string) => {
      await c.query(
        `insert into credit_movements(reference, period, kind, category, mass_g, factor_version, created_by, effective_on)
         values ($1,$2,'in',$3,$4,$5,'plant@example.com',$6)`, [ref, period, category, mass, factor, eff]);
    };
    await credit('CRD-SEED-1', 'BP-DEMO-N6-2026H1', 'post_consumer', 360000, '2026-03-04', 'CF-DEMO-1');
    await credit('CRD-SEED-2', 'BP-DEMO-N6-2026H1', 'pre_consumer', 240000, '2026-03-04', 'CF-DEMO-1');
    await credit('CRD-SEED-3', 'BP-DEMO-N6-2026H1', 'pre_consumer', 96000, '2026-02-20', 'CF-DEMO-1');

    await credit('CRD-SEED-4', 'BP-PILOT-N6-2026H1', 'pre_consumer', 75000, '2026-03-01', 'CF-PILOT-1');

    // The transfer: 50000 g from the pilot period into the demo period.
    await c.query(`insert into transfers(reference, from_period, to_period, mass_g, category, moved_on, moved_by)
      values ('TRF-0001','BP-PILOT-N6-2026H1','BP-DEMO-N6-2026H1',50000,'pre_consumer','2026-05-12','claims@example.com')`);
    await c.query(
      `insert into credit_movements(reference, period, kind, category, mass_g, factor_version, origin_site, movement, created_by, effective_on)
       values ('CRD-TRF-OUT','BP-PILOT-N6-2026H1','out','pre_consumer',50000,'CF-PILOT-1','SITE-DEMO','transfer','claims@example.com','2026-05-12')`);
    await c.query(
      `insert into credit_movements(reference, period, kind, category, mass_g, factor_version, origin_site, movement, created_by, effective_on)
       values ('CRD-TRF-IN','BP-DEMO-N6-2026H1','in','pre_consumer',50000,null,'SITE-PILOT','transfer','claims@example.com','2026-05-12')`);
  });
  console.log('seed: ledger');
}

export async function seedQuality() {
  await withTransaction(async (c) => {
    await c.query(`insert into deviations(reference, state, runs, lots, raised_by, raised_on, outcome, closed_on, description)
      values ('DEV-0001','open',$1,$2,'quality@example.com','2026-04-10',null,null,'Purity excursion held against the purification stage output.')`,
      [['RUN-U-0001'], ['LOT-N6-0002']]);
    await c.query(`insert into deviations(reference, state, runs, lots, raised_by, raised_on, outcome, closed_on, description)
      values ('DEV-0002','closed',$1,$2,'quality@example.com','2026-03-12','cause_not_established','2026-04-01','Off-spec dissolution batch, cause not established.')`,
      [['RUN-D-0002'], []]);
    await c.query(
      `insert into overrides(reference, separation, reason, lot, authorised_by, authorised_on, reviewed)
       values ('OVR-0001','analyst_not_dispositioner',$1,'LOT-N6-0001','quality@example.com','2026-03-18',false)`,
      ['Night shift analyst dispositioned the lot because no second qualified person was on site']);
  });
  console.log('seed: quality');
}

export async function seedCarbon() {
  await withTransaction(async (c) => {
    const breakdown = [
      { line: 'collection_and_transport', mg_per_kg: 310000, tag: 'primary' },
      { line: 'process_energy', mg_per_kg: 1850000, tag: 'primary' },
      { line: 'reagents', mg_per_kg: 1180000, tag: 'supplier_specific' },
      { line: 'water_and_effluent', mg_per_kg: 240000, tag: 'primary' },
      { line: 'waste_and_residues', mg_per_kg: 330000, tag: 'secondary' },
      { line: 'outbound_transport', mg_per_kg: 410000, tag: 'secondary' },
      { line: 'byproduct_credit', mg_per_kg: -60000, tag: 'primary' },
    ];
    const comparator = { material: 'virgin PA6', dataset: 'EcoBase 2025', dataset_year: '2025', region: 'EU-27' };
    await c.query(
      `insert into carbon_methods(key, version, standard, functional_unit, boundary, allocation_basis, reviewer, published_on, published_by,
          data_quality, emission_factors, primary_share_threshold_bp, state)
       values ('CM-PA6',2,'ISO 14067','1 kg of pellet','cradle-to-gate','mass','Ilse Grootveld','2026-01-20','quality@example.com',$1,$2,5000,'current')`,
      [JSON.stringify({ threshold_bp: 5000, rules: ['Primary data required for energy and feedstock', 'Secondary datasets no older than three years'] }),
       JSON.stringify([{ line: 'collection_and_transport', source: 'EcoBase 2025', year: '2025' },
         { line: 'process_energy', source: 'site meter, SITE-DEMO', year: '2026' },
         { line: 'reagents', source: 'supplier EPD', year: '2025' },
         { line: 'water_and_effluent', source: 'site meter, SITE-DEMO', year: '2026' },
         { line: 'waste_and_residues', source: 'EcoBase 2025', year: '2025' },
         { line: 'outbound_transport', source: 'EcoBase 2025', year: '2025' },
         { line: 'byproduct_credit', source: 'site meter, SITE-DEMO', year: '2026' }])]);
    await c.query(
      `insert into carbon_methods(key, version, standard, functional_unit, boundary, allocation_basis, reviewer, published_on, published_by,
          data_quality, emission_factors, primary_share_threshold_bp, state)
       values ('CM-PA6',1,'ISO 14067','1 kg of pellet','cradle-to-gate','mass','Ilse Grootveld','2025-06-01','quality@example.com',$1,$2,5000,'superseded')`,
      [JSON.stringify({ threshold_bp: 5000, rules: ['Primary data required for energy'] }),
       JSON.stringify([{ line: 'process_energy', source: 'site meter, SITE-DEMO', year: '2025' }])]);
    await c.query(
      `insert into carbon_figures(id, lot, method_key, method_version, value_mg_per_kg, uncertainty_bp, primary_share_bp, comparator, breakdown,
          energy_location_mg_per_kg, energy_market_mg_per_kg, metered_kwh, retired_kwh, unmatched_kwh, computed_on, computed_by, primary_share_threshold_bp, boundary)
       values ('FIG-LOT-0001','LOT-N6-0001','CM-PA6',2,4260000,1200,6500,$1,$2,1850000,620000,300000,250000,50000,'2026-04-12','quality@example.com',5000,'cradle-to-gate')`,
      [JSON.stringify(comparator), JSON.stringify(breakdown)]);
    await c.query(`insert into period_energy(period, metered_kwh) values ('BP-DEMO-N6-2026H1', 300000)`);
    await c.query(`insert into energy_instruments(reference, quantity_kwh, vintage, region, state, period)
      values ('EAC-2026-0007',250000,2026,'EU-27','retired','BP-DEMO-N6-2026H1')`);
    await c.query(`insert into energy_instruments(reference, quantity_kwh, vintage, region, state)
      values ('EAC-2025-0031',100000,2025,'EU-27','held')`);
  });
  console.log('seed: carbon');
}

export async function seedCommercial() {
  await withTransaction(async (c) => {
    const specRows = [
      { property: 'relative_viscosity', method: 'ISO 307', limit: '2.40', unit: 'ratio', basis: 'guaranteed' },
      { property: 'moisture', method: 'ISO 15512', limit: '0.10', unit: 'percent', basis: 'guaranteed' },
      { property: 'yellowness_index', method: 'ASTM E313', limit: '8.0', unit: 'index', basis: 'typical' },
      { property: 'ash_content', method: 'ISO 3451-1', limit: '0.30', unit: 'percent', basis: 'informational' },
    ];
    const virgin = { reference: 'virgin PA6 at relative viscosity 2.42', source: 'EcoBase 2025', dated: '2025-11-30' };
    await c.query(`insert into specifications(grade, version, issued_on, state, rows, virgin_reference) values ('N6',3,'2026-02-01','current',$1,$2)`,
      [JSON.stringify(specRows), JSON.stringify(virgin)]);
    await c.query(`insert into specifications(grade, version, issued_on, state, rows, virgin_reference) values ('N6',2,'2025-09-01','superseded',$1,$2)`,
      [JSON.stringify(specRows.map((r) => ({ ...r, limit: r.property === 'relative_viscosity' ? '2.45' : r.limit }))), JSON.stringify(virgin)]);

    await c.query(`insert into customers(reference, name, contact, holds, application, industry) values
      ('CUS-HELIOS','Helios Textiles','helios@example.com',$1,'technical apparel yarn','textiles')`,
      [JSON.stringify({ specification: 'SPEC-N6', version: 3 })]);
    await c.query(`insert into customers(reference, name, contact, holds, application, industry) values
      ('CUS-VANTA','Vanta Automotive Fabrics','vanta@example.com',$1,'airbag fabric','automotive')`,
      [JSON.stringify({ specification: 'SPEC-N6', version: 2 })]);
    await c.query(`insert into conformances(customer, specification, spec_version, application, trials, outcome) values
      ('CUS-HELIOS','N6',3,'technical apparel yarn',$1,'passed')`,
      [JSON.stringify([{ trial: 'spin trial ST-114', date: '2026-02-20', outcome: 'passed' }])]);
    await c.query(`insert into conformances(customer, specification, spec_version, application, trials, outcome) values
      ('CUS-VANTA','N6',2,'airbag fabric',$1,'in_progress')`,
      [JSON.stringify([{ trial: 'weave trial WT-031', date: '2026-03-05', outcome: 'passed' }])]);

    await c.query(`insert into contracts(id, customer, site, period, committed_kg, floor_bp, delivered_kg, shortfall_consequence, state)
      values ('CON-HELIOS-1','CUS-HELIOS','SITE-DEMO','2026-H1',200,5000,0,'a make-good volume in the following period','on_track')`);
    await c.query(`insert into contracts(id, customer, site, period, committed_kg, floor_bp, delivered_kg, shortfall_consequence, state)
      values ('CON-VANTA-1','CUS-VANTA','SITE-COMM','2029-H1',1000,3000,0,'a make-good volume in the following period','on_track')`);

    await c.query(`insert into inbound_records(reference, source, received_at, payload_verbatim, payload) values
      ('INB-SEED-1','weighbridge','2026-02-20T06:14:00Z',$1,$2)`,
      [JSON.stringify({ ticket: 'WB-DEMO-02', batch: 'BATCH-1004', gross_g: 140000, tare_g: 20000, calibration: 'lapsed' }),
       JSON.stringify({ ticket: 'WB-DEMO-02', batch: 'BATCH-1004', gross_g: 140000, tare_g: 20000, calibration: 'lapsed' })]);
    await c.query(`insert into inbound_records(reference, source, received_at, payload_verbatim, payload) values
      ('INB-SEED-2','control_system','2026-03-04T22:41:00Z',$1,$2)`,
      [JSON.stringify({ run: 'RUN-D-0001', temperature_c: 165, pressure_bar: 3, residence_min: 92 }),
       JSON.stringify({ run: 'RUN-D-0001', temperature_c: 165, pressure_bar: 3, residence_min: 92 })]);
    await c.query(`insert into inbound_records(reference, source, received_at, payload_verbatim, payload) values
      ('INB-SEED-3','laboratory','2026-03-06T09:02:00Z',$1,$2)`,
      [JSON.stringify({ lot: 'LOT-N6-0001', property: 'relative_viscosity', method: 'ISO 307', value: '2.41' }),
       JSON.stringify({ lot: 'LOT-N6-0001', property: 'relative_viscosity', method: 'ISO 307', value: '2.41' })]);
    await c.query(`insert into test_results(reference, lot, property, method, instrument, analyst, value, unit, uncertainty_bp, recorded_on) values
      ('TST-SEED-1','LOT-N6-0001','relative_viscosity','ISO 307','VISC-02','analyst@example.com','2.41','ratio',300,'2026-03-06')`);
  });
  console.log('seed: commercial');
}

export async function seedCertificates() {
  const stmts = {
    permitted: 'The recipient may state that the material is credited as containing recycled content under a mass-balance chain of custody at 75 per cent recycled content by mass (75 per cent post-consumer). The recipient may quote the figure 75 at the same weight as the certificate, and may not round it upward.',
    prohibited: 'The recipient may not state that this material physically contains recycled content. This material is claimed by mass balance. It is not physically segregated.',
  };
  const conditions = [
    { condition: 'lot_released', satisfied: true, blocking_reference: null, detail: 'Lot LOT-N6-0003 is released.' },
    { condition: 'no_open_deviation', satisfied: true, blocking_reference: null, detail: 'No open deviation touches this lot.' },
    { condition: 'no_unreviewed_override', satisfied: true, blocking_reference: null, detail: 'Every override on this lot has been reviewed.' },
    { condition: 'period_closed', satisfied: true, blocking_reference: null, detail: 'Bookkeeping period BP-PILOT-N6-2026H1 is closed.' },
    { condition: 'balance_invariant_holds', satisfied: true, blocking_reference: null, detail: 'Credits attached do not exceed credits available.' },
    { condition: 'carbon_figure_complete', satisfied: true, blocking_reference: null, detail: 'A carbon figure exists with all four components.' },
    { condition: 'signer_scope_valid', satisfied: true, blocking_reference: null, detail: 'The signer holds signing scope for SITE-PILOT on this date.' },
    { condition: 'signer_not_data_enterer', satisfied: true, blocking_reference: null, detail: 'The signer entered no data recorded against this lot.' },
  ];
  const base = {
    version: 1, site: 'SITE-PILOT',
    lots: [{ reference: 'LOT-N6-0003', mass_g: 200000 }], grade: 'N6',
    specification: 'N6', specification_version: 3, claim_type: 'mass_balance',
    content_bp: 7500, category_split: { post_consumer: 7500 }, period: 'BP-PILOT-N6-2026H1',
    method_version: 'CM-PA6 v2', boundary: 'cradle-to-gate', uncertainty_bp: 1200, primary_share_bp: 6500,
    scheme: 'RCS-2026', registration: 'REG-RAVEL-0042',
    permitted_statement: stmts.permitted, prohibited_statement: stmts.prohibited,
    conditions: JSON.stringify(conditions), provisional_factor: true,
    input_versions: JSON.stringify({ conversion_factor: 'CF-PILOT-1', carbon_method: 'CM-PA6', carbon_method_version: 2, specification: 'N6 v3', carbon_figure: null }),
  };
  await withTransaction(async (c) => {
    await c.query(
      `insert into certificates(number, version, site, recipient, recipient_name, signer, signer_name, signed_at, state,
          lots, grade, specification, specification_version, claim_type, content_bp, category_split, period,
          method_version, boundary, uncertainty_bp, primary_share_bp, scheme, registration,
          permitted_statement, prohibited_statement, conditions, provisional_factor, input_versions,
          withdrawn_by, withdrawn_on, withdrawal_reason, void_statements, notified_recipients)
       values ('CERT-PILOT-000001',$1,$2,'CUS-HELIOS','Helios Textiles','signer2@example.com','Pavel Ostrowski','2026-03-02T10:00:00Z','withdrawn',
          $3,'N6','N6',3,'mass_balance',7500,$4,'BP-PILOT-N6-2026H1','CM-PA6 v2','cradle-to-gate',1200,6500,'RCS-2026','REG-RAVEL-0042',
          $5,$6,$7,true,$8,'signer2@example.com','2026-04-18','A collector category was corrected after acceptance',$9,$10)`,
      [base.version, base.site, JSON.stringify(base.lots), JSON.stringify(base.category_split),
       base.permitted_statement, base.prohibited_statement, base.conditions, base.input_versions,
       JSON.stringify(['The recipient may no longer state recycled content of 75 per cent against CERT-PILOT-000001.',
         'The permitted statement on CERT-PILOT-000001 is void.']),
       JSON.stringify(['Helios Textiles'])]);
    await c.query(
      `insert into certificates(number, version, site, recipient, recipient_name, signer, signer_name, signed_at, state,
          lots, grade, specification, specification_version, claim_type, content_bp, category_split, period,
          method_version, boundary, uncertainty_bp, primary_share_bp, scheme, registration,
          permitted_statement, prohibited_statement, conditions, provisional_factor, input_versions)
       values ('CERT-PILOT-000002',$1,$2,'CUS-VANTA','Vanta Automotive Fabrics','signer2@example.com','Pavel Ostrowski','2026-03-02T14:00:00Z','issued',
          $3,'N6','N6',3,'mass_balance',7500,$4,'BP-PILOT-N6-2026H1','CM-PA6 v2','cradle-to-gate',1200,6500,'RCS-2026','REG-RAVEL-0042',
          $5,$6,$7,true,$8)`,
      [base.version, base.site, JSON.stringify(base.lots), JSON.stringify(base.category_split),
       base.permitted_statement, base.prohibited_statement, base.conditions, base.input_versions]);
    await c.query(`insert into cert_sequences(site, next_number) values ('SITE-PILOT', 3) on conflict do nothing`);
    await c.query(`insert into cert_sequences(site, next_number) values ('SITE-DEMO', 1) on conflict do nothing`);
    await c.query(`insert into site_certifications(site, state, valid_from, valid_to, effective_from)
      values ('SITE-PILOT','certified','2026-01-01','2026-12-31','2026-01-01')`);
    await c.query(`insert into site_certifications(site, state, valid_from, valid_to, effective_from)
      values ('SITE-DEMO','certified','2026-01-01','2026-12-31','2026-01-01')`);
  });
  console.log('seed: certificates');
}

export async function seedPublic() {
  await withTransaction(async (c) => {
    await c.query(`insert into statistics(key, value, source, year, geography) values
      ('textiles_recycled','Less than 1 per cent of textiles are recycled into new materials','Textile Flow Monitor','2024','Global')`);
    await c.query(`insert into statistics(key, value, source, year, geography) values
      ('plastics_emissions','1.8 gigatonnes of carbon dioxide equivalent a year from plastics production','Global Materials Emissions Panel','2023','Global')`);
    await c.query(`insert into statistics(key, value, source, year, geography) values
      ('textile_incineration','More than 8 per cent of textile waste is incinerated each year','Textile Flow Monitor','2024','EU-27')`);
    await c.query(`insert into positions(title, location, department, contract_type, closes_on)
      values ('Process Engineer','Lyon, France','Operations','Permanent','2026-11-30')`);
    await c.query(`insert into news_items(title, tag, dated_on, outlet, link, language, coverage) values
      ('Series A closes at 40 million euros','funding','2026-01-22','Materials Weekly','https://ravel.example.com/news/series-a','en','[]')`);
    await c.query(`insert into news_items(title, tag, dated_on, outlet, link, language, coverage) values
      ('Offtake agreement signed for demonstration output','partnership','2026-03-11','Fibre Report','https://ravel.example.com/news/offtake','en','[]')`);
    await c.query(`insert into news_items(title, tag, dated_on, outlet, link, language, coverage) values
      ('Depolymerisation yield published','technical','2026-05-06','Chimie Circulaire','https://ravel.example.com/news/yield','fr','[]')`);
    await c.query(`insert into claim_substantiation(claim, route, first_published_on, evidence, method_version, approver, review_on) values
      ('virgin-quality recycled Nylon 6','/product','2026-01-15',$1,'CM-PA6 v2','Marit Solheim','2027-01-15')`,
      [JSON.stringify({ specification: 'N6 v3', trials: ['spin trial ST-114'], valid_to: '2027-01-01' })]);
    await c.query(`insert into claim_substantiation(claim, route, first_published_on, evidence, method_version, approver, review_on) values
      ('low-carbon polymer production','/technology','2026-01-20',$1,'CM-PA6 v2','Marit Solheim','2026-10-20')`,
      [JSON.stringify({ figure: '4260000 mg CO2e/kg', comparator: 'virgin PA6, EcoBase 2025', valid_to: '2026-09-30' })]);
  });
  console.log('seed: public');
}

/** The seeded record: one entry per seeded act, in the order the acts happened. */
export async function seedRecord() {
  const acts: [string, string | null, string | null, string | null, Record<string, any>, string][] = [
    ['collector_approval_recorded', 'quality@example.com', 'SITE-DEMO', 'COL-ALDER', { collector: 'COL-ALDER', state: 'approved' }, '2026-01-01T09:00:00Z'],
    ['collector_approval_recorded', 'quality@example.com', 'SITE-DEMO', 'COL-BRINE', { collector: 'COL-BRINE', state: 'approved' }, '2026-01-01T09:05:00Z'],
    ['collector_approval_recorded', 'quality@example.com', 'SITE-DEMO', 'COL-CINDER', { collector: 'COL-CINDER', state: 'conditional' }, '2026-01-01T09:10:00Z'],
    ['conversion_factor_published', 'claims@example.com', 'SITE-PILOT', 'CF-PILOT-1', { site: 'SITE-PILOT', factor_bp: 7500, provisional: true }, '2026-01-05T10:00:00Z'],
    ['carbon_method_published', 'quality@example.com', 'SITE-DEMO', 'CM-PA6 v2', { version: 2, standard: 'ISO 14067' }, '2026-01-20T11:00:00Z'],
    ['party_version_recorded', 'claims@example.com', null, 'COL-BRINE', { party: 'COL-BRINE', name: 'Brine Circular Materials', effective_from: '2026-08-01' }, '2026-02-01T09:00:00Z'],
    ['batch_booked', 'plant@example.com', 'SITE-DEMO', 'BATCH-1001', { reference: 'BATCH-1001', collector: 'COL-ALDER', net_g: 500000, moisture_bp: 1000 }, '2026-02-10T07:30:00Z'],
    ['batch_booked', 'plant@example.com', 'SITE-DEMO', 'BATCH-1002', { reference: 'BATCH-1002', collector: 'COL-ALDER', net_g: 300000, moisture_bp: 0 }, '2026-02-12T07:20:00Z'],
    ['batch_booked', 'plant@example.com', 'SITE-DEMO', 'BATCH-1004', { reference: 'BATCH-1004', collector: 'COL-CINDER', net_g: 120000, moisture_bp: 0, device: 'WB-DEMO-02' }, '2026-02-20T06:14:00Z'],
    ['inbound_record_stored', 'system:weighbridge', 'SITE-DEMO', 'INB-SEED-1', { source: 'weighbridge', bytes: 96 }, '2026-02-20T06:14:00Z'],
    ['test_result_recorded', 'analyst@example.com', null, 'TST-SEED-1', { lot: 'LOT-N6-0001', property: 'relative_viscosity', value: '2.41' }, '2026-03-02T08:00:00Z'],
    ['certificate_signed', 'signer2@example.com', 'SITE-PILOT', 'CERT-PILOT-000001', { number: 'CERT-PILOT-000001', lot: 'LOT-N6-0003', content_bp: 7500 }, '2026-03-02T10:00:00Z'],
    ['batch_booked', 'plant@example.com', 'SITE-DEMO', 'BATCH-1005', { reference: 'BATCH-1005', collector: 'COL-ALDER', net_g: 100000, missing_custody: ['transport'] }, '2026-03-02T11:00:00Z'],
    ['certificate_signed', 'signer2@example.com', 'SITE-PILOT', 'CERT-PILOT-000002', { number: 'CERT-PILOT-000002', lot: 'LOT-N6-0003', content_bp: 7500 }, '2026-03-02T14:00:00Z'],
    ['run_started', 'plant@example.com', 'SITE-DEMO', 'RUN-D-0001', { run_type: 'dissolution', recipe_version: 'RCP-DISS-2' }, '2026-03-04T08:00:00Z'],
    ['consumption_recorded', 'plant@example.com', 'SITE-DEMO', 'CSM-D1-1', { run: 'RUN-D-0001', input: 'BATCH-1001', mass_g: 300000, dry_mass_g: 297000, credit_g: 237600 }, '2026-03-04T09:00:00Z'],
    ['consumption_recorded', 'plant@example.com', 'SITE-DEMO', 'CSM-D1-2', { run: 'RUN-D-0001', input: 'BATCH-1002', mass_g: 300000, dry_mass_g: 300000, credit_g: 240000 }, '2026-03-04T09:10:00Z'],
    ['inbound_record_stored', 'system:control_system', 'SITE-DEMO', 'INB-SEED-2', { source: 'control_system', bytes: 84 }, '2026-03-04T22:41:00Z'],
    ['run_closed', 'plant@example.com', 'SITE-DEMO', 'RUN-D-0001', { losses_g: 120000, within_tolerance: true }, '2026-03-04T16:00:00Z'],
    ['deviation_raised', 'quality@example.com', 'SITE-DEMO', 'DEV-0002', { runs: ['RUN-D-0002'] }, '2026-03-12T09:00:00Z'],
    ['run_started', 'plant@example.com', 'SITE-DEMO', 'RUN-D-0003', { run_type: 'dissolution' }, '2026-03-18T08:00:00Z'],
    ['override_recorded', 'quality@example.com', 'SITE-DEMO', 'OVR-0001', { separation: 'analyst_not_dispositioner', lot: 'LOT-N6-0001', authorised_by: 'quality@example.com' }, '2026-03-18T15:00:00Z'],
    ['inbound_record_stored', 'system:laboratory', 'SITE-DEMO', 'INB-SEED-3', { source: 'laboratory', bytes: 92 }, '2026-03-06T09:02:00Z'],
    ['deviation_closed', 'quality@example.com', 'SITE-DEMO', 'DEV-0002', { outcome: 'cause_not_established' }, '2026-04-01T10:00:00Z'],
    ['conversion_factor_published', 'claims@example.com', 'SITE-DEMO', 'CF-DEMO-1', { site: 'SITE-DEMO', factor_bp: 8000, derived_in_g: 1000000, derived_out_g: 800000 }, '2026-04-05T09:00:00Z'],
    ['run_closed', 'plant@example.com', 'SITE-DEMO', 'RUN-R-0001', { losses_g: 20000 }, '2026-04-09T06:00:00Z'],
    ['deviation_raised', 'quality@example.com', 'SITE-DEMO', 'DEV-0001', { runs: ['RUN-U-0001'], lots: ['LOT-N6-0002'] }, '2026-04-10T09:00:00Z'],
    ['carbon_figure_computed', 'quality@example.com', 'SITE-DEMO', 'FIG-LOT-0001', { lot: 'LOT-N6-0001', value_mg_per_kg: 4260000, method_version: 'CM-PA6 v2' }, '2026-04-12T09:00:00Z'],
    ['certificate_withdrawn', 'signer2@example.com', 'SITE-PILOT', 'CERT-PILOT-000001', { number: 'CERT-PILOT-000001', reason: 'A collector category was corrected after acceptance' }, '2026-04-18T10:00:00Z'],
    ['batch_booked', 'plant@example.com', 'SITE-DEMO', 'BATCH-1003', { reference: 'BATCH-1003', collector: 'COL-BRINE', net_g: 200000, moisture_bp: 500 }, '2026-07-05T07:40:00Z'],
  ];
  await withTransaction(async (c) => {
    for (const [act, person, site, object, content, at] of acts) {
      await appendEntry(c, { act, person, site, object, content, event_at: at });
    }
    // The seeded legal hold stands on the signing of CERT-PILOT-000001.
    const signing = (await c.query(
      `select seq from record_entries where act = 'certificate_signed' and object = 'CERT-PILOT-000001'`)).rows[0];
    await c.query(`insert into legal_holds(reference, seq, placed_by, placed_on) values ('HLD-0001',$1,'quality@example.com','2026-04-18')`,
      [signing.seq]);
    await c.query(`update record_entries set legal_hold = true where seq = $1`, [signing.seq]);
    const holdEntry = await appendEntry(c, {
      act: 'legal_hold_placed', person: 'quality@example.com', object: 'HLD-0001',
      content: { reference: 'HLD-0001', seq: Number(signing.seq) }, event_at: '2026-04-18T10:30:00Z',
    });
    void holdEntry;
  });
  console.log('seed: record chain');
}



export async function seedAll() {
  await seedCore();
  await seedBatches();
  await seedRuns();
  await seedLedger();
  await seedQuality();
  await seedCarbon();
  await seedCommercial();
  await seedCertificates();
  await seedPublic();
  await seedRecord();
  console.log('seed complete');
}

const isMain = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/^.*\//, ''));
if (process.env.SEED_STANDALONE === '1' || false) {
  seedAll().then(() => process.exit(0)).catch((e) => { console.error(e); process.exit(1); });
}
