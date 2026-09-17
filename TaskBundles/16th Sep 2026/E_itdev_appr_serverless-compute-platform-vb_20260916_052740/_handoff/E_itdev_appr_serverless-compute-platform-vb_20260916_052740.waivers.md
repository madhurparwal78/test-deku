# G51 waivers: what the companion specifies that this bundle does not build

Source: `modal_prd.md`. Carriage before waivers: 298 of 374 topics and 1,589 of 1,964
enumerated items reached `instruction.md` by lexical footprint, and 76 of 76 colours
are described by family and tone. The groups below account for the remainder.

A waiver is a substring match against a dropped topic or item, so one token covers
every row on that subject. Every group below is passed to `source_lint.py` as
`--waive <token>`, and lands in the gate receipt.

## The marketing site beyond the home page and the privacy page

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `advisor`, `article`, `author`, `band`, `blog`, `brand`, `card-stat`, `card-subtitle`, `career`, `carousel`, `category`, `community`, `conference`, `contact`, `cta`, `deep-band`, `estimator`, `filters`, `founder`, `funding`, `headline`, `hero`, `index`, `investor`, `landing`, `logo`, `marketing`, `marquee`, `newsletter`, `office`, `podcast`, `press`, `price`, `pricing`, `quotation`, `rate`, `register`, `solution`, `standfirst`, `statistic`, `template`, `testimonial`, `wordmark`, `workload-card`

## The documentation application and its search vendor

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `breadcrumb`, `changelog`, `docsroot`, `documentation`, `footnote`, `guide`, `notebook`, `playground`, `referrer`, `release`, `search`, `tutorial`

## Federated sign-in, single sign-on, directory provisioning and the command-line handoff

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `assertion`, `authentication`, `certificate`, `challenge`, `claim`, `cli`, `command-line`, `domain`, `federation`, `github`, `google`, `handoff`, `issuer`, `method`, `misconfigured`, `provider`, `python`, `sdk`, `sign-up`, `sso`, `terms`

## The dimensional layer, the icon set and the zero-asset substitution guide

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `animation`, `arc`, `asset`, `audio`, `balance`, `commercial`, `cube`, `cycle`, `diagram`, `div`, `entrance`, `globe`, `glow`, `hemisphere`, `highlight`, `icon`, `illustration`, `keyframe`, `manifest`, `mark`, `material`, `noise`, `observer`, `parallax`, `parallelogram`, `path`, `rect`, `render`, `reveal`, `scroll`, `shader`, `sphere`, `substitution`, `svg`, `texture`, `translate`, `woff`, `zero-asset`

## Design token literals the kit's own number rule forbids in a brief

The brief carries colour as family, tone and shade and motion as words, never as a hex, a rem value, an easing curve or a keyframe body. That is the kit's settled number rule (prompts/generate_instruction.md S-4, tools/source_lint.py A5) and G43 additionally bans `cubic-bezier(` anywhere in the brief. Carrying these literally would fail one gate to satisfy another.

Tokens: `blur`, `breakpoint`, `color-`, `computed`, `cubic-bezier`, `ease-`, `fingerprint`, `font-`, `rem`, `rgb`, `selector`

## The capture-evidence register, the taxonomy and the acceptance apparatus

These are the PRD's own authoring apparatus, addressed to the person commissioning the build. They describe how the document was produced, not what the product does, and G44 forbids process disclosure in the brief.

Tokens: `acceptance`, `biggest`, `capture`, `checklist`, `deferred`, `depart`, `evidence`, `fidelity`, `gap`, `honesty`, `informational`, `ledger`, `measured`, `normative`, `observed`, `problem`, `reconstructed`, `taxonomy`, `tier`, `transcribed`

## The worker fleet, the scheduler, runtime isolation and capacity

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `admission`, `autoscaling`, `capacity`, `execution`, `fleet`, `game`, `gpu`, `kernel`, `multi-node`, `objective`, `pool`, `reserved`, `runtime`, `scheduler`, `shard`, `snapshot`, `worker`

## Platform observability, reliability, webhooks and integrations

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `aggregate`, `alert`, `alerting`, `allow-list`, `architecture`, `availability`, `backend`, `backoff`, `chain`, `chaos`, `circuit`, `collector`, `dead`, `degradation`, `delivery`, `efficient`, `encryption`, `error-reporting`, `errorreporterhost`, `failover`, `framing`, `frontend`, `granularity`, `incident`, `instrument`, `integration`, `invalidation`, `latency`, `machine-readable`, `measurement`, `module`, `observability`, `outbox`, `partition`, `percentile`, `performance`, `poison`, `polite-announcing`, `publish`, `reliability`, `replication`, `reporter`, `retry`, `span`, `telemetry`, `testing`, `time-serie`, `trace`, `webhook`

## The billing provider, invoicing and commitments

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `checkout`, `commitment`, `credit`, `forecasting`, `grain`, `invoice`, `metering`, `overage`, `payment`, `proration`, `reconcile`, `refund`, `reservation`, `rolled`, `subscription`, `tax`, `trend`

## Compliance, residency, retention beyond the console and support break-glass

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `abuse`, `advertising`, `analytics`, `break-glass`, `deletion`, `erasure`, `gdpr`, `governance`, `hipaa`, `legal`, `propagation`, `residency`, `soc`, `sub-processor`, `support`, `trust`

## The build order and platform services not built here

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `august`, `body`, `cards`, `consent`, `consistency`, `cookie`, `crashlooped`, `customer`, `deprecation`, `durable`, `empty`, `endpoint`, `foundation`, `header`, `image`, `logging`, `narrowly`, `organisation`, `pause`, `pet`, `primitive`, `result`, `schedule`, `seeing`, `stage`, `starts`, `symmetry`, `tail`, `thresholdreached`, `toast`, `versioning`, `vulnerability`

## The example model and workload catalogue

Out of scope for this bundle. The Task Order scopes the build to the governed console and the animated public product site over it; this subject belongs to the wider platform and is recorded in `## Constraints`.

Tokens: `binder`, `diffusion`, `embedding`, `evals`, `fine-tuning`, `folding`, `inference`, `llm`, `model`, `molecular`, `music`, `protein`, `question-answering`, `rag`, `reinforcement`, `slackbot`, `speech`, `trajectory`, `transcribe`, `video`, `webrtc`
