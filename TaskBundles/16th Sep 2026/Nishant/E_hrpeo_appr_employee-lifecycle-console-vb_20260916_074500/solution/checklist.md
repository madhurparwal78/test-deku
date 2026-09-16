# Checklist: Cadrix Employee Lifecycle Console

Items: 614
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The application holds one record per employee from hire to exit. `src: Overview`
- [ ] `C-OV-02` `capability` Leave reads from the one employee record. `src: Overview`
- [ ] `C-OV-03` `capability` Attendance reads from the one employee record. `src: Overview`
- [ ] `C-OV-04` `capability` Claims read from the one employee record. `src: Overview`
- [ ] `C-OV-05` `capability` Statutory payroll reads from the one employee record. `src: Overview`
- [ ] `C-OV-06` `role` An `employee` reads their own record. `src: Overview`
- [ ] `C-OV-07` `role` A `manager` decides requests raised by their own direct reports. `src: Overview`
- [ ] `C-OV-08` `role` A `payroll` account works a monthly run through its lifecycle. `src: Overview`
- [ ] `C-OV-09` `constraint` Authority is a relationship rather than a role alone. `src: Overview`
- [ ] `C-OV-10` `constraint` A refused decision leaves the underlying row untouched. `src: Overview`
- [ ] `C-OV-11` `constraint` The approval queue is the only notification surface. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` The application has exactly three roles. `src: User roles`
- [ ] `C-RL-02` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-03` `role` An `employee` reads their own leave balances. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An `employee` reads their own leave ledger. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An `employee` reads their own attendance days. `src: User roles table row 1`
- [ ] `C-RL-06` `role` An `employee` reads their own payslips. `src: User roles table row 1`
- [ ] `C-RL-07` `role` An `employee` applies for leave. `src: User roles table row 1`
- [ ] `C-RL-08` `role` An `employee` requests a regularisation. `src: User roles table row 1`
- [ ] `C-RL-09` `role` An `employee` submits a claim. `src: User roles table row 1`
- [ ] `C-RL-10` `role` An `employee` cannot read another employee's record. `src: User roles table row 1`
- [ ] `C-RL-11` `role` An `employee` cannot read any salary figure. `src: User roles table row 1`
- [ ] `C-RL-12` `role` An `employee` cannot decide any request. `src: User roles table row 1`
- [ ] `C-RL-13` `role` A `manager` reads the record of their own direct reports. `src: User roles table row 2`
- [ ] `C-RL-14` `role` A `manager` reads the approval queue filtered to their own direct reports. `src: User roles table row 2`
- [ ] `C-RL-15` `role` A `manager` approves a request raised by one of their own direct reports. `src: User roles table row 2`
- [ ] `C-RL-16` `role` A `manager` rejects a request raised by one of their own direct reports. `src: User roles table row 2`
- [ ] `C-RL-17` `role` A `manager` cannot decide a request raised by somebody who does not report directly to them. `src: User roles table row 2`
- [ ] `C-RL-18` `role` A `manager` cannot decide a request raised by themselves. `src: User roles table row 2`
- [ ] `C-RL-19` `role` A `manager` cannot read any salary figure. `src: User roles table row 2`
- [ ] `C-RL-20` `role` A `manager` cannot work a payroll run through any transition. `src: User roles table row 2`
- [ ] `C-RL-21` `role` A `payroll` account reads every employee in a payroll group owned by that account. `src: User roles table row 3`
- [ ] `C-RL-22` `role` A `payroll` account reads salary structures. `src: User roles table row 3`
- [ ] `C-RL-23` `role` A `payroll` account reads the register. `src: User roles table row 3`
- [ ] `C-RL-24` `role` A `payroll` account opens, locks, computes, reviews a payroll run. `src: User roles table row 3`
- [ ] `C-RL-25` `role` A `payroll` account cannot decide a leave request. `src: User roles table row 3`
- [ ] `C-RL-26` `role` A `payroll` account cannot decide a claim. `src: User roles table row 3`
- [ ] `C-RL-27` `role` A `payroll` account cannot sign off a run moved into review by that same account. `src: User roles table row 3`
- [ ] `C-RL-28` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-29` `contract` A direct API call from an `employee` session to a `manager`-only endpoint is denied by the server. `src: User roles`
- [ ] `C-RL-30` `contract` A direct API call from an `employee` session to a `payroll`-only endpoint is denied by the server. `src: User roles`
- [ ] `C-RL-31` `contract` A denied call leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-32` `constraint` Signup is closed, with no registration route. `src: User roles`
- [ ] `C-RL-33` `constraint` The application creates no account of its own. `src: User roles`
- [ ] `C-RL-34` `literal` The seeded employee address is `employee@example.com`. `src: User roles`
- [ ] `C-RL-35` `literal` The second seeded employee address is `employee2@example.com`. `src: User roles`
- [ ] `C-RL-36` `literal` The third seeded employee address is `employee3@example.com`. `src: User roles`
- [ ] `C-RL-37` `literal` The seeded manager address is `manager@example.com`. `src: User roles`
- [ ] `C-RL-38` `literal` The seeded peer manager address is `manager2@example.com`. `src: User roles`
- [ ] `C-RL-39` `literal` The seeded payroll address is `payroll@example.com`. `src: User roles`
- [ ] `C-RL-40` `literal` The second seeded payroll address is `payroll2@example.com`. `src: User roles`
- [ ] `C-RL-41` `literal` The employee `E-1001` is named `Nadia Fernandes`. `src: User roles table row 4`
- [ ] `C-RL-42` `literal` The employee `E-1002` is named `Arjun Mehta`. `src: User roles table row 5`
- [ ] `C-RL-43` `literal` The employee `E-1003` is named `Sofia Ruiz`. `src: User roles table row 6`
- [ ] `C-RL-44` `literal` The manager `E-2001` is named `Priya Raman`. `src: User roles table row 7`
- [ ] `C-RL-45` `literal` The peer manager `E-2002` is named `Tomas Lindqvist`. `src: User roles table row 8`
- [ ] `C-RL-46` `literal` The payroll account `E-4001` is named `Daniel Okafor`. `src: User roles table row 9`
- [ ] `C-RL-47` `literal` The second payroll account `E-4002` is named `Helen Zhao`. `src: User roles table row 10`
- [ ] `C-RL-48` `literal` The fourth group employee `E-1004` is named `Marcus Bell`. `src: User roles`
- [ ] `C-RL-49` `data` The employee `E-1001` reports to the manager numbered `E-2001`. `src: User roles table row 4`
- [ ] `C-RL-50` `data` The employee `E-1002` reports to the manager numbered `E-2001`. `src: User roles table row 5`
- [ ] `C-RL-51` `data` The employee `E-1003` reports to the peer manager numbered `E-2002`. `src: User roles table row 6`

## C-CF Core features

- [ ] `C-CF-01` `data` An `employee_number` is unique across the organisation. `src: Core features, the employee record`
- [ ] `C-CF-02` `data` An `employee_number` is never reused. `src: Core features, the employee record`
- [ ] `C-CF-03` `ui` The employee record opens as tabs reading from one row. `src: Core features, the employee record rule 1`
- [ ] `C-CF-04` `ui` The record carries a Profile tab holding personal contact details. `src: Core features, the employee record rule 1`
- [ ] `C-CF-05` `ui` The record carries an Employment tab holding designation, department, location, manager. `src: Core features, the employee record rule 1`
- [ ] `C-CF-06` `ui` The record carries a Compensation tab holding the salary structure history. `src: Core features, the employee record rule 1`
- [ ] `C-CF-07` `ui` The record carries a Statutory tab holding national identifiers, provident fund, insurance numbers. `src: Core features, the employee record rule 1`
- [ ] `C-CF-08` `ui` The record carries a Bank tab never displayed in full after saving. `src: Core features, the employee record rule 1`
- [ ] `C-CF-09` `ui` The record carries Leave, Attendance, Claims tabs. `src: Core features, the employee record rule 1`
- [ ] `C-CF-10` `constraint` Every other surface reads the employee record rather than holding a copy. `src: Core features, the employee record rule 1`
- [ ] `C-CF-11` `data` A self-editable field is changed directly by the employee. `src: Core features, the employee record rule 2`
- [ ] `C-CF-12` `data` A requested field is proposed by the employee, confirmed by `payroll`. `src: Core features, the employee record rule 2`
- [ ] `C-CF-13` `data` Both versions of a requested field are kept. `src: Core features, the employee record rule 2`
- [ ] `C-CF-14` `constraint` A restricted field is never edited in place. `src: Core features, the employee record rule 2`
- [ ] `C-CF-15` `capability` A restricted field changes only as a dated change record. `src: Core features, the employee record rule 3`
- [ ] `C-CF-16` `data` A change record carries an effective date, an approver, a reason. `src: Core features, the employee record rule 3`
- [ ] `C-CF-17` `contract` An employee's state on any past date is reconstructable from the change history. `src: Core features, the employee record rule 3`
- [ ] `C-CF-18` `constraint` A direct edit of a restricted field is refused, naming the field. `src: Core features, the employee record rule 3`
- [ ] `C-CF-19` `constraint` An employee changing their own bank account without a second confirmation is refused. `src: Core features, the employee record rule 4`
- [ ] `C-CF-20` `capability` A bank proposal is held until a `payroll` account confirms. `src: Core features, the employee record rule 4`
- [ ] `C-CF-21` `data` A leave policy is data rather than code. `src: Core features, the leave policy engine`
- [ ] `C-CF-22` `data` A policy carries an accrual kind, an accrual rate, a cap. `src: Core features, the leave policy engine`
- [ ] `C-CF-23` `data` A policy carries a carry-forward allowance with an expiry date. `src: Core features, the leave policy engine`
- [ ] `C-CF-24` `data` A policy carries a minimum notice in days. `src: Core features, the leave policy engine`
- [ ] `C-CF-25` `data` A policy carries a maximum consecutive allowance. `src: Core features, the leave policy engine`
- [ ] `C-CF-26` `data` A policy carries the threshold above which a document is required. `src: Core features, the leave policy engine`
- [ ] `C-CF-27` `data` A policy carries whether half days are permitted. `src: Core features, the leave policy engine`
- [ ] `C-CF-28` `data` A policy carries how far a balance may go below zero. `src: Core features, the leave policy engine`
- [ ] `C-CF-29` `data` A policy carries a holiday calendar reference. `src: Core features, the leave policy engine`
- [ ] `C-CF-30` `data` A policy carries a number of approval levels. `src: Core features, the leave policy engine`
- [ ] `C-CF-31` `literal` The seeded annual policy code is `ANNUAL`. `src: Core features, the leave policy engine rule 1`
- [ ] `C-CF-32` `literal` The seeded sick policy code is `SICK`. `src: Core features, the leave policy engine rule 1`
- [ ] `C-CF-33` `literal` The seeded unpaid policy code is `UNPAID`. `src: Core features, the leave policy engine rule 1`
- [ ] `C-CF-34` `data` A holiday belongs to a calendar. `src: Core features, the leave policy engine rule 2`
- [ ] `C-CF-35` `data` A calendar belongs to a location. `src: Core features, the leave policy engine rule 2`
- [ ] `C-CF-36` `data` A weekend belongs to a calendar. `src: Core features, the leave policy engine rule 2`
- [ ] `C-CF-37` `contract` A leave day is stored as an integer count of half days. `src: Core features, the leave policy engine rule 3`
- [ ] `C-CF-38` `contract` A response reports `days` as the half-day count divided by two. `src: Core features, the leave policy engine rule 3`
- [ ] `C-CF-39` `ui` Applying for leave happens in a new row at the top of the request list. `src: Core features, applying for leave`
- [ ] `C-CF-40` `capability` Picking dates computes the half days deducted before submission. `src: Core features, applying for leave rule 1`
- [ ] `C-CF-41` `contract` The computed half days exclude the holidays of the employee's own calendar. `src: Core features, applying for leave rule 1`
- [ ] `C-CF-42` `contract` The computed half days exclude the weekends of the employee's own calendar. `src: Core features, applying for leave rule 1`
- [ ] `C-CF-43` `literal` A request from `2026-08-17` to `2026-08-21` under the seeded calendar is eight halves. `src: Core features, applying for leave rule 1`
- [ ] `C-CF-44` `ui` The balance is shown before submission rather than after. `src: Core features, applying for leave rule 2`
- [ ] `C-CF-45` `ui` The notice rule is shown before submission rather than after. `src: Core features, applying for leave rule 2`
- [ ] `C-CF-46` `ui` The consecutive-day rule is shown before submission rather than after. `src: Core features, applying for leave rule 2`
- [ ] `C-CF-47` `constraint` A request breaching the minimum notice is refused as invalid. `src: Core features, applying for leave rule 2`
- [ ] `C-CF-48` `constraint` A request breaching the minimum notice writes no row. `src: Core features, applying for leave rule 2`
- [ ] `C-CF-49` `ui` Teammates already away on the chosen dates are named before submission. `src: Core features, applying for leave rule 3`
- [ ] `C-CF-50` `capability` Submitting a request writes a pending ledger entry. `src: Core features, applying for leave rule 4`
- [ ] `C-CF-51` `capability` Submitting a request moves the request into the pending state. `src: Core features, applying for leave rule 4`
- [ ] `C-CF-52` `capability` Approval converts the pending ledger entry to an availed entry. `src: Core features, applying for leave rule 4`
- [ ] `C-CF-53` `capability` Rejection removes the pending ledger entry. `src: Core features, applying for leave rule 4`
- [ ] `C-CF-54` `contract` Rejection returns the balance to the figure held before submission. `src: Core features, applying for leave rule 4`
- [ ] `C-CF-55` `constraint` A request overlapping a date already approved for the same employee is refused as invalid. `src: Core features, applying for leave rule 5`
- [ ] `C-CF-56` `constraint` An overlapping request writes no row. `src: Core features, applying for leave rule 5`
- [ ] `C-CF-57` `data` A leave request carries one of eight named states. `src: Core features, applying for leave rule 6`
- [ ] `C-CF-58` `contract` The availed state is set by the requested date passing. `src: Core features, applying for leave rule 6`
- [ ] `C-CF-59` `contract` An availed day is what reaches the payroll run as an input. `src: Core features, applying for leave rule 6`
- [ ] `C-CF-60` `constraint` Cancelling after the dates have passed is refused for an `employee`. `src: Core features, applying for leave rule 7`
- [ ] `C-CF-61` `capability` Cancelling after the dates have passed is permitted for a `payroll` account. `src: Core features, applying for leave rule 7`
- [ ] `C-CF-62` `contract` A late cancellation writes a correction ledger entry carrying a reason. `src: Core features, applying for leave rule 7`
- [ ] `C-CF-63` `constraint` A leave balance is never a stored number anybody edits. `src: Core features, the balance is the ledger`
- [ ] `C-CF-64` `contract` The balance in half days is the signed sum of the ledger entries for one employee under one policy. `src: Core features, the balance is the ledger rule 1`
- [ ] `C-CF-65` `ui` Every balance shown expands into the ledger entries that produce the figure. `src: Core features, the balance is the ledger rule 2`
- [ ] `C-CF-66` `contract` The expanded ledger sums to the figure shown. `src: Core features, the balance is the ledger rule 2`
- [ ] `C-CF-67` `literal` The seeded annual balance of `E-1001` is `36` halves. `src: Core features, the balance is the ledger rule 3`
- [ ] `C-CF-68` `data` A punch carries the employee, the instant, a direction. `src: Core features, attendance rule 1`
- [ ] `C-CF-69` `data` A punch carries a source from six named values. `src: Core features, attendance rule 1`
- [ ] `C-CF-70` `data` A punch carries a device, a location, a confidence. `src: Core features, attendance rule 1`
- [ ] `C-CF-71` `data` A punch carries `raw_ref`, the source's own identifier. `src: Core features, attendance rule 1`
- [ ] `C-CF-72` `constraint` A punch row is never updated. `src: Core features, attendance rule 2`
- [ ] `C-CF-73` `constraint` A punch row is never deleted. `src: Core features, attendance rule 2`
- [ ] `C-CF-74` `contract` Posting a punch whose `raw_ref` already exists writes no second row. `src: Core features, attendance rule 3`
- [ ] `C-CF-75` `contract` Posting a repeated `raw_ref` leaves the computed day unchanged. `src: Core features, attendance rule 3`
- [ ] `C-CF-76` `contract` The response to a repeated `raw_ref` reports the punch already held. `src: Core features, attendance rule 3`
- [ ] `C-CF-77` `capability` A day is computed from the punches, the shift, the leave. `src: Core features, attendance rule 4`
- [ ] `C-CF-78` `data` A computed day carries worked minutes capped at the shift maximum. `src: Core features, attendance rule 4`
- [ ] `C-CF-79` `data` A computed day carries one of seven named statuses. `src: Core features, attendance rule 4`
- [ ] `C-CF-80` `data` A computed day carries minutes late, minutes early, overtime. `src: Core features, attendance rule 4`
- [ ] `C-CF-81` `contract` An `in` punch with no matching `out` punch produces the `unpaired` status. `src: Core features, attendance rule 5`
- [ ] `C-CF-82` `ui` An unpaired punch is surfaced on the month grid as a defect. `src: Core features, attendance rule 5`
- [ ] `C-CF-83` `constraint` An unpaired punch is never silently dropped. `src: Core features, attendance rule 5`
- [ ] `C-CF-84` `constraint` An unpaired punch is never paired with a neighbouring day's punch. `src: Core features, attendance rule 5`
- [ ] `C-CF-85` `capability` A correction is a regularisation requested by the employee with a reason. `src: Core features, attendance rule 6`
- [ ] `C-CF-86` `capability` A regularisation is decided by the requester's own manager. `src: Core features, attendance rule 6`
- [ ] `C-CF-87` `constraint` The original punches remain after a regularisation. `src: Core features, attendance rule 6`
- [ ] `C-CF-88` `contract` A regularised day reports the punched times beside the regularised times. `src: Core features, attendance rule 6`
- [ ] `C-CF-89` `ui` The month grid shows employees down the side, days across the top. `src: Core features, attendance rule 7`
- [ ] `C-CF-90` `ui` Each month-grid cell carries its state as a letter beside a colour. `src: Core features, attendance rule 7`
- [ ] `C-CF-91` `ui` The month grid carries the per-employee counts on the right. `src: Core features, attendance rule 7`
- [ ] `C-CF-92` `data` A claim carries a category from three named values. `src: Core features, claims`
- [ ] `C-CF-93` `data` A claim carries an amount in minor units with a currency. `src: Core features, claims`
- [ ] `C-CF-94` `data` A claim carries the date spent on. `src: Core features, claims`
- [ ] `C-CF-95` `literal` A receipt reference is required above `200000` minor units. `src: Core features, claims rule 1`
- [ ] `C-CF-96` `constraint` A claim above the receipt threshold with no receipt reference is refused as invalid. `src: Core features, claims rule 1`
- [ ] `C-CF-97` `literal` A `manager` approves a claim up to `1000000` minor units. `src: Core features, claims rule 2`
- [ ] `C-CF-98` `capability` A claim above the manager limit escalates to a `payroll` account. `src: Core features, claims rule 2`
- [ ] `C-CF-99` `ui` The claimant is told which role decides the claim at the moment of submission. `src: Core features, claims rule 2`
- [ ] `C-CF-100` `data` A claim carries one of six named states. `src: Core features, claims rule 3`
- [ ] `C-CF-101` `capability` An approved claim is paid through the payroll run as a non-taxable reimbursement line. `src: Core features, claims rule 4`
- [ ] `C-CF-102` `capability` An approved claim is paid through a separate payment batch. `src: Core features, claims rule 4`
- [ ] `C-CF-103` `literal` The seeded organisation setting `claim_payment_route` is `payroll`. `src: Core features, claims rule 4`
- [ ] `C-CF-104` `constraint` A claim already reimbursed through payroll cannot be added to a batch. `src: Core features, claims rule 4`
- [ ] `C-CF-105` `constraint` A claim is never paid through both routes. `src: Core features, claims rule 4`
- [ ] `C-CF-106` `ui` Leave requests, regularisations, claims arrive in one queue. `src: Core features, one approval queue`
- [ ] `C-CF-107` `ui` The queue carries a filter by kind. `src: Core features, one approval queue`
- [ ] `C-CF-108` `ui` A queue row carries the requester, the kind, a summary, an age in days, two actions. `src: Core features, one approval queue rule 1`
- [ ] `C-CF-109` `ui` Opening a leave row shows the balance beside who else is away. `src: Core features, one approval queue rule 1`
- [ ] `C-CF-110` `ui` Opening a claim row shows the receipt reference beside the category limit. `src: Core features, one approval queue rule 1`
- [ ] `C-CF-111` `ui` Opening a regularisation row shows the original punches. `src: Core features, one approval queue rule 1`
- [ ] `C-CF-112` `contract` A `manager` decides only a request whose requester reports directly to that manager. `src: Core features, one approval queue rule 2`
- [ ] `C-CF-113` `contract` A request from a peer manager's direct report is denied at the server. `src: Core features, one approval queue rule 2`
- [ ] `C-CF-114` `contract` A denied peer-manager decision leaves the request state unchanged. `src: Core features, one approval queue rule 2`
- [ ] `C-CF-115` `contract` A denied peer-manager decision leaves the request decider unchanged. `src: Core features, one approval queue rule 2`
- [ ] `C-CF-116` `contract` A `manager` deciding a request raised by themselves is denied at the server. `src: Core features, one approval queue rule 3`
- [ ] `C-CF-117` `contract` A denied self-decision leaves the request row unchanged. `src: Core features, one approval queue rule 3`
- [ ] `C-CF-118` `contract` A second decision on a request already carrying a decision is refused. `src: Core features, one approval queue rule 4`
- [ ] `C-CF-119` `ui` A refused second decision names the deciding account beside the decision time. `src: Core features, one approval queue rule 4`
- [ ] `C-CF-120` `contract` Two decisions submitted at the same moment produce exactly one accepted decision. `src: Core features, one approval queue rule 4`
- [ ] `C-CF-121` `contract` The loser of two simultaneous decisions is refused as already decided. `src: Core features, one approval queue rule 4`
- [ ] `C-CF-122` `contract` The leave ledger moves exactly once under two simultaneous decisions. `src: Core features, one approval queue rule 4`
- [ ] `C-CF-123` `data` An approval chain names a role relative to the requester rather than a person. `src: Core features, one approval queue rule 5`
- [ ] `C-CF-124` `data` The seeded annual chain carries one level. `src: Core features, one approval queue rule 5`
- [ ] `C-CF-125` `literal` A request unanswered for `3` days escalates to the next level. `src: Core features, one approval queue rule 6`
- [ ] `C-CF-126` `constraint` A timeout never decides a request. `src: Core features, one approval queue rule 6`
- [ ] `C-CF-127` `capability` Bulk approval acts across the filtered selection. `src: Core features, one approval queue rule 7`
- [ ] `C-CF-128` `capability` Bulk rejection acts across the filtered selection. `src: Core features, one approval queue rule 7`
- [ ] `C-CF-129` `literal` A bulk action can be undone within `10` seconds. `src: Core features, one approval queue rule 7`
- [ ] `C-CF-130` `constraint` A bulk rejection requires a reason. `src: Core features, one approval queue rule 7`
- [ ] `C-CF-131` `constraint` A bulk approval requires no reason. `src: Core features, one approval queue rule 7`
- [ ] `C-CF-132` `constraint` Exactly one payroll run exists per period per payroll group. `src: Core features, the payroll run`
- [ ] `C-CF-133` `constraint` A second attempt to open a run for a covered period is refused. `src: Core features, the payroll run`
- [ ] `C-CF-134` `data` A run carries one of eight named states. `src: Core features, the payroll run rule 1`
- [ ] `C-CF-135` `contract` Run states advance only in the declared order. `src: Core features, the payroll run rule 1`
- [ ] `C-CF-136` `contract` Locking freezes the attendance days of the period. `src: Core features, the payroll run rule 2`
- [ ] `C-CF-137` `contract` Locking freezes the leave without pay of the period. `src: Core features, the payroll run rule 2`
- [ ] `C-CF-138` `contract` Locking freezes the overtime of the period. `src: Core features, the payroll run rule 2`
- [ ] `C-CF-139` `contract` Locking freezes the claims marked for payroll. `src: Core features, the payroll run rule 2`
- [ ] `C-CF-140` `contract` Locking freezes the salary revisions effective in the period. `src: Core features, the payroll run rule 2`
- [ ] `C-CF-141` `contract` Anything arriving after the lock belongs to the next period. `src: Core features, the payroll run rule 2`
- [ ] `C-CF-142` `ui` The interface states the lock boundary at the moment of locking. `src: Core features, the payroll run rule 2`
- [ ] `C-CF-143` `capability` Computing produces one payslip per employee in the group. `src: Core features, the payroll run rule 3`
- [ ] `C-CF-144` `ui` The run reports progress per employee during the computation. `src: Core features, the payroll run rule 3`
- [ ] `C-CF-145` `constraint` A run completes for the whole group or for none of the group. `src: Core features, the payroll run rule 3`
- [ ] `C-CF-146` `constraint` A partial computation is never a run state. `src: Core features, the payroll run rule 3`
- [ ] `C-CF-147` `capability` A per-employee failure is raised as a blocking finding. `src: Core features, the payroll run rule 4`
- [ ] `C-CF-148` `constraint` Moving to review with a blocking finding outstanding is refused. `src: Core features, the payroll run rule 4`
- [ ] `C-CF-149` `data` A statutory rule set carries a jurisdiction, a state, a basis, a rate. `src: Core features, the payroll run rule 5`
- [ ] `C-CF-150` `data` A statutory rule set carries thresholds, caps, a rounding rule. `src: Core features, the payroll run rule 5`
- [ ] `C-CF-151` `literal` The seeded statutory rule set code is `IN-2026-04`. `src: Core features, the payroll run rule 5`
- [ ] `C-CF-152` `data` The seeded rule set carries five named statutory heads. `src: Core features, the payroll run rule 5`
- [ ] `C-CF-153` `constraint` No statutory rate is written into the application. `src: Core features, the payroll run rule 5`
- [ ] `C-CF-154` `contract` Every computed statutory line records the rule version that produced the line. `src: Core features, the payroll run rule 6`
- [ ] `C-CF-155` `ui` The register carries one row per employee, one column per component. `src: Core features, the payroll run rule 7`
- [ ] `C-CF-156` `ui` The register carries totals per column, subtotals per department, a grand total. `src: Core features, the payroll run rule 7`
- [ ] `C-CF-157` `contract` A filtered register shows the filtered department's totals labelled as filtered. `src: Core features, the payroll run rule 7`
- [ ] `C-CF-158` `contract` The account moving a run to review may not move the run to signed off. `src: Core features, sign-off`
- [ ] `C-CF-159` `contract` A same-account sign-off attempt is denied at the server. `src: Core features, sign-off rule 1`
- [ ] `C-CF-160` `contract` A denied sign-off leaves the run in the review state. `src: Core features, sign-off rule 1`
- [ ] `C-CF-161` `contract` A denied sign-off leaves the signing account empty. `src: Core features, sign-off rule 1`
- [ ] `C-CF-162` `ui` Sign-off presents the total gross, the total deductions, the total net, the headcount paid. `src: Core features, sign-off rule 2`
- [ ] `C-CF-163` `contract` Sign-off requires the exact total net in minor units typed back. `src: Core features, sign-off rule 2`
- [ ] `C-CF-164` `constraint` A mismatched total net is refused as invalid. `src: Core features, sign-off rule 2`
- [ ] `C-CF-165` `constraint` A refused sign-off leaves the run state unchanged. `src: Core features, sign-off rule 2`
- [ ] `C-CF-166` `constraint` A signed-off run's payslip figures never change. `src: Core features, sign-off rule 3`
- [ ] `C-CF-167` `constraint` Reopening a signed-off run is refused once payment has been initiated. `src: Core features, sign-off rule 3`
- [ ] `C-CF-168` `contract` Reopening before payment requires a reason. `src: Core features, sign-off rule 3`
- [ ] `C-CF-169` `contract` Reopening writes an audit entry. `src: Core features, sign-off rule 3`
- [ ] `C-CF-170` `capability` Payslips are published to the employee surface on close. `src: Core features, sign-off rule 4`
- [ ] `C-CF-171` `constraint` An employee reads only their own payslip. `src: Core features, sign-off rule 4`
- [ ] `C-CF-172` `ui` The employee surface carries balances per policy. `src: Core features, the employee surface`
- [ ] `C-CF-173` `ui` The employee surface carries the employee's own requests. `src: Core features, the employee surface`
- [ ] `C-CF-174` `ui` The employee surface carries the employee's own payslips. `src: Core features, the employee surface`
- [ ] `C-CF-175` `constraint` A payslip request for a period belonging to somebody else is denied. `src: Core features, the employee surface`
- [ ] `C-CF-176` `ui` An address matching no route renders the product's own not-found page. `src: Core features, the launch surface rule 1`
- [ ] `C-CF-177` `ui` The not-found page carries a way back into the console. `src: Core features, the launch surface rule 1`
- [ ] `C-CF-178` `contract` An address matching no route answers as not found rather than as success. `src: Core features, the launch surface rule 1`
- [ ] `C-CF-179` `contract` The application serves a favicon. `src: Core features, the launch surface rule 2`
- [ ] `C-CF-180` `ui` Every page declares the favicon in its document head. `src: Core features, the launch surface rule 2`
- [ ] `C-CF-181` `contract` Every internal link on every route resolves. `src: Core features, the launch surface rule 3`

## C-UF User flow

- [ ] `C-UF-01` `ui` The route `/login` serves sign-in, unauthenticated. `src: User flow route table`
- [ ] `C-UF-02` `ui` The route `/me` serves own balances, own requests, own payslips, to any role. `src: User flow route table`
- [ ] `C-UF-03` `ui` The route `/me/leave` serves leave application in a new row, to any role. `src: User flow route table`
- [ ] `C-UF-04` `ui` The route `/me/claims` serves claim submission in a new row, to any role. `src: User flow route table`
- [ ] `C-UF-05` `ui` The route `/people` serves the employee directory to a `manager`. `src: User flow route table`
- [ ] `C-UF-06` `ui` The route `/people/E-1001` serves one tabbed employee record. `src: User flow route table`
- [ ] `C-UF-07` `ui` The route `/approvals` serves the one queue to a `manager`. `src: User flow route table`
- [ ] `C-UF-08` `ui` The route `/approvals/1` serves one request with the deciding context. `src: User flow route table`
- [ ] `C-UF-09` `ui` The route `/attendance` serves the month grid for the caller's own line. `src: User flow route table`
- [ ] `C-UF-10` `ui` The route `/payroll` serves the runs list to a `payroll` account. `src: User flow route table`
- [ ] `C-UF-11` `ui` The route `/payroll/2026-07` serves one run with its lifecycle. `src: User flow route table`
- [ ] `C-UF-12` `ui` The route `/payroll/2026-07/register` serves the register. `src: User flow route table`
- [ ] `C-UF-13` `contract` A signed-out request for a protected route goes to the sign-in route. `src: User flow, entry and redirects`
- [ ] `C-UF-14` `contract` Sign-in returns to the route asked for before the redirect. `src: User flow, entry and redirects`
- [ ] `C-UF-15` `contract` Sign-in with no stored destination lands on the own-surface route. `src: User flow, entry and redirects`
- [ ] `C-UF-16` `contract` Signing out returns to the sign-in route. `src: User flow, entry and redirects`
- [ ] `C-UF-17` `contract` A token expiring mid-action keeps the typed values on the page. `src: User flow, entry and redirects`
- [ ] `C-UF-18` `ui` A token expiring mid-action offers a fresh sign-in. `src: User flow, entry and redirects`
- [ ] `C-UF-19` `contract` A role reaching a route the role does not hold is refused with a reason. `src: User flow, entry and redirects`
- [ ] `C-UF-20` `contract` A refused route leaves everything unchanged. `src: User flow, entry and redirects`
- [ ] `C-UF-21` `ui` A manager opens the queue, reads the balance beside the roster, approves a request. `src: User flow journey 1`
- [ ] `C-UF-22` `ui` An approved row leaves the queue before the response lands. `src: User flow journey 1`
- [ ] `C-UF-23` `ui` An employee opens a new row, picks dates, reads the halves before submitting. `src: User flow journey 2`
- [ ] `C-UF-24` `ui` A submitted request moves the balance into pending on the employee surface. `src: User flow journey 2`
- [ ] `C-UF-25` `ui` A peer manager opening the request by address is refused both actions. `src: User flow journey 3`
- [ ] `C-UF-26` `ui` A refused peer-manager decision leaves the request pending with no decider. `src: User flow journey 3`
- [ ] `C-UF-27` `ui` A payroll account locks, computes, reviews the open run. `src: User flow journey 4`
- [ ] `C-UF-28` `ui` A sign-off attempted from the same payroll session that moved the run to review is refused as the same actor. `src: User flow journey 4`
- [ ] `C-UF-29` `literal` The seeded open run grand total net is `13075000`. `src: User flow journey 5`
- [ ] `C-UF-30` `ui` The second payroll account types the grand total net, signs the run off. `src: User flow journey 5`
- [ ] `C-UF-31` `ui` An unknown address lands on the product's own not-found page with a way back. `src: User flow journey 6`
- [ ] `C-UF-32` `ui` Every list carries an empty state naming the next action. `src: User flow, states`
- [ ] `C-UF-33` `ui` Every route carries a loading state during resolution. `src: User flow, states`
- [ ] `C-UF-34` `ui` A refusal raises an inline banner above the surface raising the refusal. `src: User flow, states`
- [ ] `C-UF-35` `ui` A refusal banner names what was refused beside why. `src: User flow, states`
- [ ] `C-UF-36` `constraint` No route becomes an error page. `src: User flow, states`
- [ ] `C-UF-37` `ui` Every request row carries its state as a word beside its colour. `src: User flow, states`
- [ ] `C-UF-38` `ui` Every attendance cell carries its state as a word beside its colour. `src: User flow, states`
- [ ] `C-UF-39` `ui` Every run state is carried as a word beside its colour. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The north star is comprehension rather than atmosphere. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The register is operational: quiet, dense, built for scanning. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` No surface carries an oversized hero. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` No surface carries an editorial composition. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The page ground is a near-white neutral. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Headings take a near-black neutral. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Body copy takes a deep neutral. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Captions take a mid neutral. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The brand colour is a mid, vivid violet on the wordmark, on emphasis words, on links. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` The one primary action per screen sits on a deep, soft indigo ground. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` The primary action takes a light, vivid violet on hover. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` No secondary control wears the primary ground. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Each screen leads with exactly one primary action, visually distinct from every secondary one. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Approved, present, paid take a mid, vivid green. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Pending, awaiting approval take a mid, vivid orange. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Rejected, absent, failed take a mid, vivid red. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Informational takes a mid, vivid blue. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Draft, not applicable take a mid cool neutral. `src: UI/UX notes`
- [ ] `C-UX-19` `contract` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Every state pill carries its state as a word. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` Type is one variable sans family for the interface. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Every amount, balance, count, duration renders with tabular figures. `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Density is compact on the directory, the register, the queue, the attendance grid. `src: UI/UX notes`
- [ ] `C-UX-24` `ui` The employee surface is comfortable by default. `src: UI/UX notes`
- [ ] `C-UX-25` `ui` Shape is soft: fully rounded pills, gently rounded cards, less on panels. `src: UI/UX notes`
- [ ] `C-UX-26` `ui` Elevation belongs only to floating surfaces. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` Motion is confined to four named moments. `src: UI/UX notes`
- [ ] `C-UX-28` `ui` A panel opens on a long decelerate. `src: UI/UX notes`
- [ ] `C-UX-29` `ui` A row changes state on the house ease. `src: UI/UX notes`
- [ ] `C-UX-30` `ui` A skeleton holds during a list load. `src: UI/UX notes`
- [ ] `C-UX-31` `ui` A progress indicator runs during a payroll computation. `src: UI/UX notes`
- [ ] `C-UX-32` `contract` A reduced-motion preference removes panel travel. `src: UI/UX notes`
- [ ] `C-UX-33` `contract` A reduced-motion preference holds a skeleton on its first frame. `src: UI/UX notes`
- [ ] `C-UX-34` `contract` A reduced-motion preference keeps the payroll progress indicator running. `src: UI/UX notes`
- [ ] `C-UX-35` `ui` A control carries resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes`
- [ ] `C-UX-36` `ui` Escape closes a layer, returning focus to whatever opened the layer. `src: UI/UX notes`
- [ ] `C-UX-37` `ui` A destructive action confirms first. `src: UI/UX notes`
- [ ] `C-UX-38` `ui` Unavailable is never signalled by colour alone. `src: UI/UX notes`
- [ ] `C-UX-39` `contract` Each screen carries exactly one `h1`. `src: UI/UX notes`
- [ ] `C-UX-40` `contract` Contrast meets WCAG AA. `src: UI/UX notes`
- [ ] `C-UX-41` `contract` Every command has a keyboard navigation route with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-42` `contract` Tables are real tables with header associations. `src: UI/UX notes`
- [ ] `C-UX-43` `contract` Icon-only controls carry labels. `src: UI/UX notes`
- [ ] `C-UX-44` `contract` The month grid declares its dimensions. `src: UI/UX notes`
- [ ] `C-UX-45` `contract` The month grid announces the state of its focused cell as text. `src: UI/UX notes`
- [ ] `C-UX-46` `contract` Dialogs trap focus, returning focus on close. `src: UI/UX notes`
- [ ] `C-UX-47` `contract` Every amount is announced with its currency. `src: UI/UX notes`
- [ ] `C-UX-48` `contract` Every date is announced in full rather than abbreviated. `src: UI/UX notes`
- [ ] `C-UX-49` `contract` Responsive behaviour holds at every width between the named tiers. `src: UI/UX notes`
- [ ] `C-UX-50` `ui` The layout floors on the smallest viewport. `src: UI/UX notes`
- [ ] `C-UX-51` `ui` The employee surface is designed for the narrowest width first. `src: UI/UX notes`
- [ ] `C-UX-52` `ui` The approval queue is designed for the narrowest width first. `src: UI/UX notes`
- [ ] `C-UX-53` `constraint` No page is dominated by one hue family with no second signal. `src: UI/UX notes`
- [ ] `C-UX-54` `constraint` No decoration stands in for content. `src: UI/UX notes`
- [ ] `C-UX-55` `ui` The product commits to light, designed fully for that mode. `src: UI/UX notes`
- [ ] `C-UX-56` `constraint` A dark mode is optional, never the default. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Every route's HTML is produced on the server. `src: Technical requirements`
- [ ] `C-TR-02` `contract` Every route's HTML arrives complete on first paint. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The queue, the month grid, the register still list rows with scripting disabled. `src: Technical requirements`
- [ ] `C-TR-04` `contract` The JSON API is a Hono application under the `/api` prefix on the same origin. `src: Technical requirements`
- [ ] `C-TR-05` `contract` One process serves the pages beside the API. `src: Technical requirements`
- [ ] `C-TR-06` `contract` Storage is PostgreSQL. `src: Technical requirements`
- [ ] `C-TR-07` `contract` Identity is Keycloak. `src: Technical requirements`
- [ ] `C-TR-08` `literal` The health endpoint `GET /api/health` returns `200` with no credential. `src: Technical requirements`
- [ ] `C-TR-09` `contract` The health endpoint answers only once seeding has finished. `src: Technical requirements`
- [ ] `C-TR-10` `literal` PostgreSQL is read from `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-11` `literal` Keycloak is read from `AUTH_ISSUER_URL`. `src: Technical requirements`
- [ ] `C-TR-12` `literal` The client identifier is read from `AUTH_CLIENT_ID`. `src: Technical requirements`
- [ ] `C-TR-13` `literal` The client secret is read from `AUTH_CLIENT_SECRET`. `src: Technical requirements`
- [ ] `C-TR-14` `literal` The application address is read from `APP_PUBLIC_URL`. `src: Technical requirements`
- [ ] `C-TR-15` `literal` The outside port is read from `APP_PUBLIC_PORT`. `src: Technical requirements`
- [ ] `C-TR-16` `constraint` No host or port is hardcoded. `src: Technical requirements`
- [ ] `C-TR-17` `constraint` Neither backing service is downloaded, installed, compiled, started. `src: Technical requirements`
- [ ] `C-TR-18` `capability` The application exchanges an email plus the seeded password for a token at Keycloak. `src: Technical requirements`
- [ ] `C-TR-19` `contract` The token signature is validated on every request. `src: Technical requirements`
- [ ] `C-TR-20` `contract` The realm role is validated on every request. `src: Technical requirements`
- [ ] `C-TR-21` `contract` The caller's own employee record is resolved from the token subject. `src: Technical requirements`
- [ ] `C-TR-22` `constraint` The application creates no realm, no role, no user. `src: Technical requirements`
- [ ] `C-TR-23` `constraint` The application holds no administrative credential for Keycloak. `src: Technical requirements`
- [ ] `C-TR-24` `constraint` A role read from a request body is never authority. `src: Technical requirements`
- [ ] `C-TR-25` `contract` Every read is narrowed by the relationship the record carries. `src: Technical requirements`
- [ ] `C-TR-26` `contract` Every write is narrowed by the relationship the record carries. `src: Technical requirements`
- [ ] `C-TR-27` `contract` A manager's reach is the set of employees reporting directly to that manager. `src: Technical requirements`
- [ ] `C-TR-28` `contract` A payroll account's reach is the payroll groups owned by that account. `src: Technical requirements`
- [ ] `C-TR-29` `contract` A request passing the role check but failing the relationship check is refused. `src: Technical requirements`
- [ ] `C-TR-30` `contract` Leave balances are computed on the server once. `src: Technical requirements`
- [ ] `C-TR-31` `contract` Attendance days are computed on the server once. `src: Technical requirements`
- [ ] `C-TR-32` `contract` Payroll components are computed on the server once. `src: Technical requirements`
- [ ] `C-TR-33` `constraint` No server-computed figure is recomputed in the browser for display. `src: Technical requirements`
- [ ] `C-TR-34` `constraint` Nothing the browser downloads carries a credential. `src: Technical requirements`
- [ ] `C-TR-35` `constraint` Nothing the browser downloads carries an API key. `src: Technical requirements`
- [ ] `C-TR-36` `constraint` The client secret stays on the server. `src: Technical requirements`
- [ ] `C-TR-37` `constraint` The database connection string stays on the server. `src: Technical requirements`
- [ ] `C-TR-38` `contract` Every collection endpoint pages by opaque cursor rather than an offset. `src: Technical requirements`
- [ ] `C-TR-39` `literal` A page carries `50` rows by default. `src: Technical requirements`
- [ ] `C-TR-40` `literal` A page carries `500` rows at most. `src: Technical requirements`
- [ ] `C-TR-41` `literal` The next cursor is returned in the `X-Next-Cursor` response header. `src: Technical requirements`
- [ ] `C-TR-42` `contract` The cursor header is absent on the last page. `src: Technical requirements`
- [ ] `C-TR-43` `contract` A paging session over the directory repeats no row. `src: Technical requirements`
- [ ] `C-TR-44` `contract` A paging session over the register skips no row. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `contract` A calendar day is decided by server-side UTC. `src: Data model`
- [ ] `C-DM-02` `literal` Every seeded account signs in with `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-03` `contract` The seeded password is written into `/app/USER_README.md` beside each account. `src: Data model`
- [ ] `C-DM-04` `contract` Money is an integer in the currency's minor unit. `src: Data model`
- [ ] `C-DM-05` `literal` The currency throughout is `inr`. `src: Data model`
- [ ] `C-DM-06` `constraint` No money value is a floating-point number. `src: Data model`
- [ ] `C-DM-07` `data` The `employee` table carries the columns named in the brief. `src: Data model`
- [ ] `C-DM-08` `data` An employee state is one of five named values. `src: Data model`
- [ ] `C-DM-09` `constraint` A reporting line closing a cycle is refused, naming the cycle. `src: Data model`
- [ ] `C-DM-10` `data` The `employment_change` table carries the field, the previous value, the new value. `src: Data model`
- [ ] `C-DM-11` `contract` A value on a past date is the latest change effective on or before that date. `src: Data model`
- [ ] `C-DM-12` `data` The `salary_structure` table carries an effective date, a gross in minor units, a currency. `src: Data model`
- [ ] `C-DM-13` `data` A salary component carries one of four named kinds. `src: Data model`
- [ ] `C-DM-14` `data` A salary component carries one of three named formula kinds. `src: Data model`
- [ ] `C-DM-15` `contract` Components compute in their declared order. `src: Data model`
- [ ] `C-DM-16` `constraint` A structure whose component order refers back on itself is refused at save. `src: Data model`
- [ ] `C-DM-17` `data` A holiday calendar carries a code, a location, the weekend days. `src: Data model`
- [ ] `C-DM-18` `data` A leave policy carries the fourteen columns named in the brief. `src: Data model`
- [ ] `C-DM-19` `data` A leave ledger entry carries one of seven named kinds. `src: Data model`
- [ ] `C-DM-20` `contract` A leave balance is never stored as a column. `src: Data model`
- [ ] `C-DM-21` `contract` Two approved requests for one employee never cover the same date. `src: Data model`
- [ ] `C-DM-22` `contract` The `raw_ref` column is unique across punches. `src: Data model`
- [ ] `C-DM-23` `contract` An attendance day is recomputed rather than edited. `src: Data model`
- [ ] `C-DM-24` `data` A shift carries a start, an end, a grace, a break, a night flag. `src: Data model`
- [ ] `C-DM-25` `data` A claim never carries both payment states across its lifetime. `src: Data model`
- [ ] `C-DM-26` `data` An approval carries one of three named kinds. `src: Data model`
- [ ] `C-DM-27` `contract` An approval row already carrying a decider accepts no second decision. `src: Data model`
- [ ] `C-DM-28` `literal` A run period is written as `YYYY-MM`. `src: Data model`
- [ ] `C-DM-29` `contract` The signing account is never equal to the reviewing account. `src: Data model`
- [ ] `C-DM-30` `data` A payslip carries a gross, a deductions total, a net, the leave-without-pay days. `src: Data model`
- [ ] `C-DM-31` `data` A payslip line carries a code, a kind, an amount, a rule version, an order. `src: Data model`
- [ ] `C-DM-32` `constraint` No payslip figure changes once its run reaches the signed-off state. `src: Data model`
- [ ] `C-DM-33` `data` A statutory rule carries a code, a state, a basis, a rate, a threshold, a cap, a rounding. `src: Data model`
- [ ] `C-DM-34` `contract` Every statutory payslip line records the rule set version. `src: Data model`
- [ ] `C-DM-35` `contract` A privileged action commits together with its audit entry. `src: Data model`
- [ ] `C-DM-36` `contract` Pagination is by cursor at `50` by default. `src: Data model`
- [ ] `C-DM-37` `contract` Idempotency is required on punches by the source reference. `src: Data model`
- [ ] `C-DM-38` `contract` Idempotency is required on every run transition. `src: Data model`
- [ ] `C-DM-39` `data` An error body carries a code, a message, an optional field. `src: Data model`
- [ ] `C-DM-40` `contract` A component marked prorated is scaled for a part-month. `src: Data model`
- [ ] `C-DM-41` `contract` Proration applies to the gross before any statutory line is computed. `src: Data model`
- [ ] `C-DM-42` `literal` The basic component is `40` percent of the prorated gross. `src: Data model`
- [ ] `C-DM-43` `literal` The house rent component is `20` percent of the prorated gross. `src: Data model`
- [ ] `C-DM-44` `contract` The special component is the remainder of the prorated gross. `src: Data model`
- [ ] `C-DM-45` `literal` Provident fund is `12` percent of basic with the base capped at `1500000` minor units. `src: Data model`
- [ ] `C-DM-46` `literal` State insurance is zero above a prorated gross of `2100000` minor units. `src: Data model`
- [ ] `C-DM-47` `literal` Professional tax in the seeded state is `20000` minor units above a prorated gross of `1500000`. `src: Data model`
- [ ] `C-DM-48` `literal` Welfare fund in the seeded state is `2000` minor units, in June, in December. `src: Data model`
- [ ] `C-DM-49` `literal` Deducted tax is zero up to an annualised taxable gross of `30000000` minor units. `src: Data model`
- [ ] `C-DM-50` `literal` The employee `E-1002` carries a gross of `5000000` minor units. `src: Data model`
- [ ] `C-DM-51` `literal` The employee `E-1002` carries a net of `4675000` minor units for the open period. `src: Data model`
- [ ] `C-DM-52` `literal` The employee `E-1001` carries a gross of `3100000` minor units. `src: Data model`
- [ ] `C-DM-53` `literal` The employee `E-1001` carries a net of `2806000` minor units for the open period. `src: Data model`
- [ ] `C-DM-54` `contract` The employer provident fund contribution never reduces net pay. `src: Data model`
- [ ] `C-DM-55` `literal` The seeded organisation is named `Cadrix`. `src: Data model`
- [ ] `C-DM-56` `literal` The seeded holiday calendars are `KA-2026` plus `MH-2026`. `src: Data model`
- [ ] `C-DM-57` `literal` The seeded holiday on `2026-08-19` is named `Independence Observance`. `src: Data model`
- [ ] `C-DM-58` `literal` The seeded organisation holds `120` employees. `src: Data model`
- [ ] `C-DM-59` `data` The seeded employees span four named departments. `src: Data model`
- [ ] `C-DM-60` `literal` The seeded core payroll group is `MONTHLY-CORE`. `src: Data model`
- [ ] `C-DM-61` `literal` The seeded second payroll group is `MONTHLY-OPS`. `src: Data model`
- [ ] `C-DM-62` `data` The core payroll group holds four named employees. `src: Data model`
- [ ] `C-DM-63` `literal` The employee `E-1003` carries a gross of `2000000` minor units. `src: Data model`
- [ ] `C-DM-64` `literal` The employee `E-1004` carries a gross of `4000000` minor units. `src: Data model`
- [ ] `C-DM-65` `literal` The annual policy accrues `4` halves monthly. `src: Data model`
- [ ] `C-DM-66` `literal` The annual policy caps the balance at `60` halves. `src: Data model`
- [ ] `C-DM-67` `literal` The annual policy carries `10` halves forward. `src: Data model`
- [ ] `C-DM-68` `literal` The annual policy requires `2` days notice. `src: Data model`
- [ ] `C-DM-69` `literal` The sick policy accrues `24` halves yearly. `src: Data model`
- [ ] `C-DM-70` `literal` The unpaid policy allows a negative balance of `20` halves. `src: Data model`
- [ ] `C-DM-71` `literal` The seed carries `31` days of attendance for the core group. `src: Data model`
- [ ] `C-DM-72` `data` The seeded attendance carries four unpaired days. `src: Data model`
- [ ] `C-DM-73` `data` The seeded attendance carries two pending regularisations. `src: Data model`
- [ ] `C-DM-74` `literal` The seed carries `12` claims across every claim state. `src: Data model`
- [ ] `C-DM-75` `literal` One seeded claim is submitted at `2500000` minor units. `src: Data model`
- [ ] `C-DM-76` `data` Two closed payroll runs are seeded with registers plus published payslips. `src: Data model`
- [ ] `C-DM-77` `literal` The open payroll run covers the period `2026-07`. `src: Data model`
- [ ] `C-DM-78` `literal` The open run computes a total gross of `14000000` minor units. `src: Data model`
- [ ] `C-DM-79` `literal` The open run computes total deductions of `925000` minor units. `src: Data model`
- [ ] `C-DM-80` `literal` The open run computes a total net of `13075000` minor units. `src: Data model`
- [ ] `C-DM-81` `literal` The open run pays a headcount of `4`. `src: Data model`
- [ ] `C-DM-82` `literal` A third seeded run covers the period `2026-08` at the open state. `src: Data model`
- [ ] `C-DM-83` `data` Both seeded payroll accounts own both payroll groups. `src: Data model`
- [ ] `C-DM-84` `contract` Seeding is idempotent, so restarting duplicates no row. `src: Data model`
- [ ] `C-DM-85` `data` A pending annual leave request from `E-1001` waits on `E-2001` at first start. `src: Data model`
- [ ] `C-DM-86` `data` A pending annual leave request from `E-1003` waits on `E-2002` at first start. `src: Data model`
- [ ] `C-DM-87` `data` The submitted claim above the manager limit waits on a `payroll` account. `src: Data model`
- [ ] `C-DM-88` `data` Each pending seeded request carries an approval row with no decider. `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The console carries twelve routes. `src: Front-end specification`
- [ ] `C-FE-02` `ui` The public surface is the sign-in route plus the not-found page. `src: Front-end specification, information architecture`
- [ ] `C-FE-03` `ui` Navigation is a left rail carrying the modules in a fixed order. `src: Front-end specification, information architecture`
- [ ] `C-FE-04` `ui` The rail carries the account control at its foot. `src: Front-end specification, information architecture`
- [ ] `C-FE-05` `ui` The work surface is a queue list with the filter above the rows. `src: Front-end specification, information architecture`
- [ ] `C-FE-06` `ui` The deciding context opens in place rather than on another route. `src: Front-end specification, information architecture`
- [ ] `C-FE-07` `ui` Creating a request opens a new row at the top of the list. `src: Front-end specification, information architecture`
- [ ] `C-FE-08` `ui` The row updates the moment the action is taken. `src: Front-end specification, information architecture`
- [ ] `C-FE-09` `ui` Hairlines are a near-white neutral one step below the ground. `src: Front-end specification, the ground`
- [ ] `C-FE-10` `ui` Table rules are a near-white neutral one step darker again. `src: Front-end specification, the ground`
- [ ] `C-FE-11` `ui` A table header takes a near-white neutral sunk ground. `src: Front-end specification, the ground`
- [ ] `C-FE-12` `constraint` No border appears where a luminance step will do. `src: Front-end specification, the ground`
- [ ] `C-FE-13` `ui` The footer ground is the deep, soft indigo of the primary button. `src: Front-end specification, the brand`
- [ ] `C-FE-14` `ui` The brand on a dark ground is a light, soft violet. `src: Front-end specification, the brand`
- [ ] `C-FE-15` `ui` The announcement bar ground is a near-white neutral with a violet cast. `src: Front-end specification, the brand`
- [ ] `C-FE-16` `ui` The eyebrow pill is a light, soft orange. `src: Front-end specification, the brand`
- [ ] `C-FE-17` `ui` Four pastel grounds carry the four summary tiles in a fixed order. `src: Front-end specification, the four summary tiles`
- [ ] `C-FE-18` `ui` The countries tile takes a near-white neutral with a mint cast. `src: Front-end specification, the four summary tiles`
- [ ] `C-FE-19` `ui` The companies tile takes a near-white cool neutral. `src: Front-end specification, the four summary tiles`
- [ ] `C-FE-20` `ui` The employees tile takes a near-white warm neutral. `src: Front-end specification, the four summary tiles`
- [ ] `C-FE-21` `ui` The products tile takes a near-white neutral with a violet cast. `src: Front-end specification, the four summary tiles`
- [ ] `C-FE-22` `ui` Approved status sits on a near-white neutral ground. `src: Front-end specification, semantic colour`
- [ ] `C-FE-23` `ui` Pending status sits on a near-white warm neutral ground. `src: Front-end specification, semantic colour`
- [ ] `C-FE-24` `ui` Rejected status sits on a near-white warm neutral ground. `src: Front-end specification, semantic colour`
- [ ] `C-FE-25` `ui` Informational status sits on a near-white cool neutral ground. `src: Front-end specification, semantic colour`
- [ ] `C-FE-26` `literal` Display type is `56px` on `64px` at `700`. `src: Front-end specification, type`
- [ ] `C-FE-27` `literal` A page title is `32px` on `40px` at `700`. `src: Front-end specification, type`
- [ ] `C-FE-28` `literal` A section heading is `24px` on `32px` at `600`. `src: Front-end specification, type`
- [ ] `C-FE-29` `literal` A card title is `18px` on `26px` at `600`. `src: Front-end specification, type`
- [ ] `C-FE-30` `literal` Body type is `16px` on `24px` at `400`. `src: Front-end specification, type`
- [ ] `C-FE-31` `literal` Secondary type is `14px` on `20px` at `400`. `src: Front-end specification, type`
- [ ] `C-FE-32` `literal` A label is `13px` on `18px` at `600`. `src: Front-end specification, type`
- [ ] `C-FE-33` `literal` Micro type is `11px` on `16px` at `600`. `src: Front-end specification, type`
- [ ] `C-FE-34` `literal` A tabular figure is `24px` on `32px` at `700`. `src: Front-end specification, type`
- [ ] `C-FE-35` `ui` Pills, buttons, the announcement bar are fully rounded. `src: Front-end specification, radius`
- [ ] `C-FE-36` `ui` Swatches are barely rounded. `src: Front-end specification, radius`
- [ ] `C-FE-37` `ui` Borders are a single hairline. `src: Front-end specification, radius`
- [ ] `C-FE-38` `ui` The wordmark is a lowercase word in the brand violet with a raised dot. `src: Front-end specification, iconography`
- [ ] `C-FE-39` `ui` The wordmark carries a small two-letter suffix below the baseline. `src: Front-end specification, iconography`
- [ ] `C-FE-40` `ui` Interface glyphs share a single consistent stroke weighting. `src: Front-end specification, iconography`
- [ ] `C-FE-41` `ui` Illustration is generated, flat, built from the palette. `src: Front-end specification, iconography`
- [ ] `C-FE-42` `constraint` No illustration carries a photograph of a person. `src: Front-end specification, iconography`
- [ ] `C-FE-43` `constraint` No illustration carries a third-party mark. `src: Front-end specification, iconography`
- [ ] `C-FE-44` `contract` Every content image carries alternative text. `src: Front-end specification, iconography`
- [ ] `C-FE-45` `contract` A decorative image declares itself decorative. `src: Front-end specification, iconography`
- [ ] `C-FE-46` `constraint` No certification badge is downloaded. `src: Front-end specification, iconography`
- [ ] `C-FE-47` `contract` Fonts are self-hosted with no font service called at run time. `src: Front-end specification, iconography`
- [ ] `C-FE-48` `ui` An announcement bar sits above the header, dismissible for the session. `src: Front-end specification, global chrome`
- [ ] `C-FE-49` `ui` The header carries the wordmark, the primary navigation, the account control. `src: Front-end specification, global chrome`
- [ ] `C-FE-50` `ui` Buttons come in a primary, a secondary, a quiet variant. `src: Front-end specification, global chrome`
- [ ] `C-FE-51` `ui` The product shell rail collapses to icons, then to a sheet, as the window narrows. `src: Front-end specification, global chrome`
- [ ] `C-FE-52` `ui` Every console surface defines the same five states. `src: Front-end specification, the five states`
- [ ] `C-FE-53` `ui` The loading state holds a skeleton. `src: Front-end specification, the five states`
- [ ] `C-FE-54` `ui` The empty state names the next action. `src: Front-end specification, the five states`
- [ ] `C-FE-55` `ui` The error state names what failed, offering the retry. `src: Front-end specification, the five states`
- [ ] `C-FE-56` `ui` The refused state names what was refused beside why. `src: Front-end specification, the five states`
- [ ] `C-FE-57` `ui` Search is one field over people, requests, runs. `src: Front-end specification, the five states`
- [ ] `C-FE-58` `contract` A search result is reflected in the address so the result can be linked. `src: Front-end specification, the five states`
- [ ] `C-FE-59` `ui` A mega-menu opens on a pointer, on a click without one. `src: Front-end specification, motion`
- [ ] `C-FE-60` `ui` A mega-menu translates up as the menu fades in. `src: Front-end specification, motion`
- [ ] `C-FE-61` `ui` A mega-menu waits a beat before closing. `src: Front-end specification, motion`
- [ ] `C-FE-62` `ui` The announcement pill overshoots slightly, settling. `src: Front-end specification, motion`
- [ ] `C-FE-63` `ui` On the narrowest width the rail becomes a sheet. `src: Front-end specification, responsive`
- [ ] `C-FE-64` `ui` On the narrowest width the directory becomes cards carrying name, designation, status. `src: Front-end specification, responsive`
- [ ] `C-FE-65` `ui` On the narrowest width the month grid shows one employee with the days down. `src: Front-end specification, responsive`
- [ ] `C-FE-66` `ui` At the middle width the month grid shows seven days across with paging. `src: Front-end specification, responsive`
- [ ] `C-FE-67` `ui` On the narrowest width the register is refused with an explanation. `src: Front-end specification, responsive`
- [ ] `C-FE-68` `ui` The refused register offers the export instead. `src: Front-end specification, responsive`
- [ ] `C-FE-69` `ui` At the middle width the register scrolls horizontally with a frozen first column. `src: Front-end specification, responsive`
- [ ] `C-FE-70` `literal` The empty directory reads `No people yet`. `src: Front-end specification, copy`
- [ ] `C-FE-71` `literal` The empty queue reads `Nothing waiting`. `src: Front-end specification, copy`
- [ ] `C-FE-72` `literal` A peer manager refused a decision reads `Not your report`. `src: Front-end specification, copy`
- [ ] `C-FE-73` `literal` A self-decision refusal reads `You cannot decide your own request`. `src: Front-end specification, copy`
- [ ] `C-FE-74` `literal` A second decision refusal reads `Already decided`. `src: Front-end specification, copy`
- [ ] `C-FE-75` `literal` A same-actor sign-off refusal reads `Sign-off needs a second pair of eyes`. `src: Front-end specification, copy`
- [ ] `C-FE-76` `literal` A mistyped total reads `That total does not match the run`. `src: Front-end specification, copy`
- [ ] `C-FE-77` `literal` The narrow register copy reads `The register needs a wider window`. `src: Front-end specification, copy`
- [ ] `C-FE-78` `literal` The not-found page reads `That page does not exist`. `src: Front-end specification, copy`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` There is one organisation with no second tenant. `src: Constraints`
- [ ] `C-CN-02` `constraint` No payment is initiated. `src: Constraints`
- [ ] `C-CN-03` `constraint` No bank file is produced. `src: Constraints`
- [ ] `C-CN-04` `constraint` No external financial call is made at run time. `src: Constraints`
- [ ] `C-CN-05` `constraint` No onboarding, exit, clearance, settlement workflow is built. `src: Constraints`
- [ ] `C-CN-06` `constraint` No typed assistant is built. `src: Constraints`
- [ ] `C-CN-07` `constraint` No report builder, scheduling, export delivery is built. `src: Constraints`
- [ ] `C-CN-08` `constraint` No approval delegation is built. `src: Constraints`
- [ ] `C-CN-09` `constraint` No support impersonation is built. `src: Constraints`
- [ ] `C-CN-10` `constraint` No billing, plan, invoice, metering surface is built. `src: Constraints`
- [ ] `C-CN-11` `constraint` No integration, webhook, public API key is built. `src: Constraints`
- [ ] `C-CN-12` `constraint` No document generation, letter, certificate is built. `src: Constraints`
- [ ] `C-CN-13` `constraint` No outbound email, SMS, push notification is sent. `src: Constraints`
- [ ] `C-CN-14` `constraint` No second factor, password reset, self-service signup is built. `src: Constraints`
- [ ] `C-CN-15` `constraint` No native or mobile application is built. `src: Constraints`
- [ ] `C-CN-16` `constraint` No marketing route, pricing page, public website is built. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The application is reachable at the public address variable. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `literal` The container-internal port is `4173`. `src: Deployment contract`
- [ ] `C-DC-04` `constraint` Neither the port nor the address is hardcoded. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-06` `contract` The health route returns `200` once the application is ready. `src: Deployment contract`
- [ ] `C-DC-07` `contract` The application starts from the environment image with no manual step. `src: Deployment contract`
- [ ] `C-DC-08` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-09` `literal` A reserved `.browser_screenshots/` directory exists at the application root, empty. `src: Deployment contract`
- [ ] `C-DC-10` `literal` A reserved `.downloads/` directory exists at the application root, empty. `src: Deployment contract`
- [ ] `C-DC-11` `contract` A production build is served behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No dev server is served. `src: Deployment contract`
- [ ] `C-DC-13` `contract` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-14` `constraint` The server is never a child of the shell. `src: Deployment contract`
- [ ] `C-DC-15` `literal` The listener binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-16` `constraint` The listener never binds a loopback address. `src: Deployment contract`
- [ ] `C-DC-17` `constraint` Neither backing service is downloaded, installed, compiled, started by the application. `src: Deployment contract`
- [ ] `C-DC-18` `constraint` Only the providers named in the brief are used. `src: Deployment contract`
- [ ] `C-DC-19` `literal` Sign-in is `POST /api/auth/login` taking an email plus a password. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `literal` The caller identity is `GET /api/me`. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `literal` The directory is `GET /api/employees`. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `literal` The balance endpoint is `GET /api/leave-balances`. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `literal` The ledger endpoint is `GET /api/leave-ledger`. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `literal` Leave application is `POST /api/leave-requests`. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `literal` The queue is `GET /api/approvals`. `src: Deployment contract, API shapes`
- [ ] `C-DC-26` `literal` A decision is `POST /api/approvals/{id}/decide`. `src: Deployment contract, API shapes`
- [ ] `C-DC-27` `literal` A punch is `POST /api/attendance/punches`. `src: Deployment contract, API shapes`
- [ ] `C-DC-28` `literal` Attendance days are `GET /api/attendance/days`. `src: Deployment contract, API shapes`
- [ ] `C-DC-29` `literal` A claim is `POST /api/claims`. `src: Deployment contract, API shapes`
- [ ] `C-DC-30` `literal` The run lock is `POST /api/payroll-runs/{period}/lock`. `src: Deployment contract, API shapes`
- [ ] `C-DC-31` `literal` The run computation is `POST /api/payroll-runs/{period}/compute`. `src: Deployment contract, API shapes`
- [ ] `C-DC-32` `literal` The run review is `POST /api/payroll-runs/{period}/review`. `src: Deployment contract, API shapes`
- [ ] `C-DC-33` `literal` The run sign-off is `POST /api/payroll-runs/{period}/signoff`. `src: Deployment contract, API shapes`
- [ ] `C-DC-34` `literal` The register is `GET /api/payroll-runs/{period}/register`. `src: Deployment contract, API shapes`
- [ ] `C-DC-35` `literal` A payslip is `GET /api/me/payslips/{period}`. `src: Deployment contract, API shapes`
- [ ] `C-DC-36` `contract` Every list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-37` `contract` Field names in a response are exact. `src: Deployment contract, API shapes`
- [ ] `C-DC-38` `contract` Bearer authentication is required on everything except the health route, the sign-in route. `src: Deployment contract, API shapes`
- [ ] `C-DC-39` `contract` An invalid call is rejected as a client error. `src: Deployment contract, API shapes`
- [ ] `C-DC-40` `contract` An unauthorized call is rejected as a client error. `src: Deployment contract, API shapes`
- [ ] `C-DC-41` `constraint` A rejected call never answers with a server error. `src: Deployment contract, API shapes`
- [ ] `C-DC-42` `constraint` A rejected call never answers with a silent success. `src: Deployment contract, API shapes`
- [ ] `C-DC-43` `constraint` An in-memory employees dictionary is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-44` `constraint` A users table beside the Keycloak realm is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-45` `constraint` A hardcoded approval response the application returns to itself is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-46` `constraint` A balance column the application increments is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-47` `constraint` A register served from a fixture file is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-48` `contract` The named provider is the only place the data actually lives. `src: Deployment contract, no mocks`
- [ ] `C-DC-49` `literal` The sign-in token field is named `access_token`. `src: Deployment contract, API shapes`
- [ ] `C-DC-50` `contract` The punch endpoint accepts a device key, also a signed-in caller's bearer credential. `src: Deployment contract, API shapes`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | Every seeded account uses the password deku-demo-pw-2026 | `C-RL-02` |
| `employee@example.com` | The seeded employee address is employee@example.com | `C-RL-34` |
| `employee2@example.com` | The second seeded employee address is employee2@example.com | `C-RL-35` |
| `employee3@example.com` | The third seeded employee address is employee3@example.com | `C-RL-36` |
| `manager@example.com` | The seeded manager address is manager@example.com | `C-RL-37` |
| `manager2@example.com` | The seeded peer manager address is manager2@example.com | `C-RL-38` |
| `payroll@example.com` | The seeded payroll address is payroll@example.com | `C-RL-39` |
| `payroll2@example.com` | The second seeded payroll address is payroll2@example.com | `C-RL-40` |
| `E-1001` | The employee E-1001 is named Nadia Fernandes | `C-RL-41` |
| `Nadia Fernandes` | The employee E-1001 is named Nadia Fernandes | `C-RL-41` |
| `E-1002` | The employee E-1002 is named Arjun Mehta | `C-RL-42` |
| `Arjun Mehta` | The employee E-1002 is named Arjun Mehta | `C-RL-42` |
| `E-1003` | The employee E-1003 is named Sofia Ruiz | `C-RL-43` |
| `Sofia Ruiz` | The employee E-1003 is named Sofia Ruiz | `C-RL-43` |
| `E-2001` | The manager E-2001 is named Priya Raman | `C-RL-44` |
| `Priya Raman` | The manager E-2001 is named Priya Raman | `C-RL-44` |
| `E-2002` | The peer manager E-2002 is named Tomas Lindqvist | `C-RL-45` |
| `Tomas Lindqvist` | The peer manager E-2002 is named Tomas Lindqvist | `C-RL-45` |
| `E-4001` | The payroll account E-4001 is named Daniel Okafor | `C-RL-46` |
| `Daniel Okafor` | The payroll account E-4001 is named Daniel Okafor | `C-RL-46` |
| `E-4002` | The second payroll account E-4002 is named Helen Zhao | `C-RL-47` |
| `Helen Zhao` | The second payroll account E-4002 is named Helen Zhao | `C-RL-47` |
| `E-1004` | The fourth group employee E-1004 is named Marcus Bell | `C-RL-48` |
| `Marcus Bell` | The fourth group employee E-1004 is named Marcus Bell | `C-RL-48` |
| `ANNUAL` | The seeded annual policy code is ANNUAL | `C-CF-31` |
| `SICK` | The seeded sick policy code is SICK | `C-CF-32` |
| `UNPAID` | The seeded unpaid policy code is UNPAID | `C-CF-33` |
| `2026-08-17` | A request from 2026-08-17 to 2026-08-21 under the seeded calendar is eight halves | `C-CF-43` |
| `2026-08-21` | A request from 2026-08-17 to 2026-08-21 under the seeded calendar is eight halves | `C-CF-43` |
| `36` | The seeded annual balance of E-1001 is 36 halves | `C-CF-67` |
| `200000` | A receipt reference is required above 200000 minor units | `C-CF-95` |
| `manager` | A manager approves a claim up to 1000000 minor units | `C-CF-97` |
| `1000000` | A manager approves a claim up to 1000000 minor units | `C-CF-97` |
| `claim_payment_route` | The seeded organisation setting claim_payment_route is payroll | `C-CF-103` |
| `payroll` | The seeded organisation setting claim_payment_route is payroll | `C-CF-103` |
| `3` | A request unanswered for 3 days escalates to the next level | `C-CF-125` |
| `10` | A bulk action can be undone within 10 seconds | `C-CF-129` |
| `IN-2026-04` | The seeded statutory rule set code is IN-2026-04 | `C-CF-151` |
| `13075000` | The seeded open run grand total net is 13075000 | `C-UF-29` |
| `GET /api/health` | The health endpoint GET /api/health returns 200 with no credential | `C-TR-08` |
| `200` | The health endpoint GET /api/health returns 200 with no credential | `C-TR-08` |
| `DATABASE_URL` | PostgreSQL is read from DATABASE_URL | `C-TR-10` |
| `AUTH_ISSUER_URL` | Keycloak is read from AUTH_ISSUER_URL | `C-TR-11` |
| `AUTH_CLIENT_ID` | The client identifier is read from AUTH_CLIENT_ID | `C-TR-12` |
| `AUTH_CLIENT_SECRET` | The client secret is read from AUTH_CLIENT_SECRET | `C-TR-13` |
| `APP_PUBLIC_URL` | The application address is read from APP_PUBLIC_URL | `C-TR-14` |
| `APP_PUBLIC_PORT` | The outside port is read from APP_PUBLIC_PORT | `C-TR-15` |
| `50` | A page carries 50 rows by default | `C-TR-39` |
| `500` | A page carries 500 rows at most | `C-TR-40` |
| `X-Next-Cursor` | The next cursor is returned in the X-Next-Cursor response header | `C-TR-41` |
| `inr` | The currency throughout is inr | `C-DM-05` |
| `YYYY-MM` | A run period is written as YYYY-MM | `C-DM-28` |
| `40` | The basic component is 40 percent of the prorated gross | `C-DM-42` |
| `20` | The house rent component is 20 percent of the prorated gross | `C-DM-43` |
| `12` | Provident fund is 12 percent of basic with the base capped at 1500000 minor units | `C-DM-45` |
| `1500000` | Provident fund is 12 percent of basic with the base capped at 1500000 minor units | `C-DM-45` |
| `2100000` | State insurance is zero above a prorated gross of 2100000 minor units | `C-DM-46` |
| `20000` | Professional tax in the seeded state is 20000 minor units above a prorated gross of 1500000 | `C-DM-47` |
| `2000` | Welfare fund in the seeded state is 2000 minor units, in June, in December | `C-DM-48` |
| `30000000` | Deducted tax is zero up to an annualised taxable gross of 30000000 minor units | `C-DM-49` |
| `5000000` | The employee E-1002 carries a gross of 5000000 minor units | `C-DM-50` |
| `4675000` | The employee E-1002 carries a net of 4675000 minor units for the open period | `C-DM-51` |
| `3100000` | The employee E-1001 carries a gross of 3100000 minor units | `C-DM-52` |
| `2806000` | The employee E-1001 carries a net of 2806000 minor units for the open period | `C-DM-53` |
| `Cadrix` | The seeded organisation is named Cadrix | `C-DM-55` |
| `KA-2026` | The seeded holiday calendars are KA-2026 plus MH-2026 | `C-DM-56` |
| `MH-2026` | The seeded holiday calendars are KA-2026 plus MH-2026 | `C-DM-56` |
| `2026-08-19` | The seeded holiday on 2026-08-19 is named Independence Observance | `C-DM-57` |
| `Independence Observance` | The seeded holiday on 2026-08-19 is named Independence Observance | `C-DM-57` |
| `120` | The seeded organisation holds 120 employees | `C-DM-58` |
| `MONTHLY-CORE` | The seeded core payroll group is MONTHLY-CORE | `C-DM-60` |
| `MONTHLY-OPS` | The seeded second payroll group is MONTHLY-OPS | `C-DM-61` |
| `2000000` | The employee E-1003 carries a gross of 2000000 minor units | `C-DM-63` |
| `4000000` | The employee E-1004 carries a gross of 4000000 minor units | `C-DM-64` |
| `4` | The annual policy accrues 4 halves monthly | `C-DM-65` |
| `60` | The annual policy caps the balance at 60 halves | `C-DM-66` |
| `2` | The annual policy requires 2 days notice | `C-DM-68` |
| `24` | The sick policy accrues 24 halves yearly | `C-DM-69` |
| `31` | The seed carries 31 days of attendance for the core group | `C-DM-71` |
| `2500000` | One seeded claim is submitted at 2500000 minor units | `C-DM-75` |
| `2026-07` | The open payroll run covers the period 2026-07 | `C-DM-77` |
| `14000000` | The open run computes a total gross of 14000000 minor units | `C-DM-78` |
| `925000` | The open run computes total deductions of 925000 minor units | `C-DM-79` |
| `2026-08` | A third seeded run covers the period 2026-08 at the open state | `C-DM-82` |
| `56px` | Display type is 56px on 64px at 700 | `C-FE-26` |
| `64px` | Display type is 56px on 64px at 700 | `C-FE-26` |
| `700` | Display type is 56px on 64px at 700 | `C-FE-26` |
| `32px` | A page title is 32px on 40px at 700 | `C-FE-27` |
| `40px` | A page title is 32px on 40px at 700 | `C-FE-27` |
| `24px` | A section heading is 24px on 32px at 600 | `C-FE-28` |
| `600` | A section heading is 24px on 32px at 600 | `C-FE-28` |
| `18px` | A card title is 18px on 26px at 600 | `C-FE-29` |
| `26px` | A card title is 18px on 26px at 600 | `C-FE-29` |
| `16px` | Body type is 16px on 24px at 400 | `C-FE-30` |
| `400` | Body type is 16px on 24px at 400 | `C-FE-30` |
| `14px` | Secondary type is 14px on 20px at 400 | `C-FE-31` |
| `20px` | Secondary type is 14px on 20px at 400 | `C-FE-31` |
| `13px` | A label is 13px on 18px at 600 | `C-FE-32` |
| `11px` | Micro type is 11px on 16px at 600 | `C-FE-33` |
| `No people yet` | The empty directory reads No people yet | `C-FE-70` |
| `Nothing waiting` | The empty queue reads Nothing waiting | `C-FE-71` |
| `Not your report` | A peer manager refused a decision reads Not your report | `C-FE-72` |
| `You cannot decide your own request` | A self-decision refusal reads You cannot decide your own request | `C-FE-73` |
| `Already decided` | A second decision refusal reads Already decided | `C-FE-74` |
| `Sign-off needs a second pair of eyes` | A same-actor sign-off refusal reads Sign-off needs a second pair of eyes | `C-FE-75` |
| `That total does not match the run` | A mistyped total reads That total does not match the run | `C-FE-76` |
| `The register needs a wider window` | The narrow register copy reads The register needs a wider window | `C-FE-77` |
| `That page does not exist` | The not-found page reads That page does not exist | `C-FE-78` |
| `${APP_PUBLIC_PORT}:4173` | The port mapping is ${APP_PUBLIC_PORT}:4173 | `C-DC-02` |
| `4173` | The container-internal port is 4173 | `C-DC-03` |
| `/app/USER_README.md` | Login credentials are written to /app/USER_README.md | `C-DC-08` |
| `.browser_screenshots/` | A reserved .browser_screenshots/ directory exists at the application root, empty | `C-DC-09` |
| `.downloads/` | A reserved .downloads/ directory exists at the application root, empty | `C-DC-10` |
| `0.0.0.0` | The listener binds 0.0.0.0 | `C-DC-15` |
| `POST /api/auth/login` | Sign-in is POST /api/auth/login taking an email plus a password | `C-DC-19` |
| `GET /api/me` | The caller identity is GET /api/me | `C-DC-20` |
| `GET /api/employees` | The directory is GET /api/employees | `C-DC-21` |
| `GET /api/leave-balances` | The balance endpoint is GET /api/leave-balances | `C-DC-22` |
| `GET /api/leave-ledger` | The ledger endpoint is GET /api/leave-ledger | `C-DC-23` |
| `POST /api/leave-requests` | Leave application is POST /api/leave-requests | `C-DC-24` |
| `GET /api/approvals` | The queue is GET /api/approvals | `C-DC-25` |
| `POST /api/approvals/{id}/decide` | A decision is POST /api/approvals/{id}/decide | `C-DC-26` |
| `POST /api/attendance/punches` | A punch is POST /api/attendance/punches | `C-DC-27` |
| `GET /api/attendance/days` | Attendance days are GET /api/attendance/days | `C-DC-28` |
| `POST /api/claims` | A claim is POST /api/claims | `C-DC-29` |
| `POST /api/payroll-runs/{period}/lock` | The run lock is POST /api/payroll-runs/{period}/lock | `C-DC-30` |
| `POST /api/payroll-runs/{period}/compute` | The run computation is POST /api/payroll-runs/{period}/compute | `C-DC-31` |
| `POST /api/payroll-runs/{period}/review` | The run review is POST /api/payroll-runs/{period}/review | `C-DC-32` |
| `POST /api/payroll-runs/{period}/signoff` | The run sign-off is POST /api/payroll-runs/{period}/signoff | `C-DC-33` |
| `GET /api/payroll-runs/{period}/register` | The register is GET /api/payroll-runs/{period}/register | `C-DC-34` |
| `GET /api/me/payslips/{period}` | A payslip is GET /api/me/payslips/{period} | `C-DC-35` |
| `access_token` | The sign-in token field is named access_token | `C-DC-49` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the bearer token lifetime | `C-TR-24` |
| the shift maximum worked minutes | `C-CF-83` |
| the escalation notification wording | `C-CF-140` |
| the export format of the register | `C-FE-68` |
| the statutory period of the jurisdiction | `C-DM-42` |
| the exact slab boundaries above the first band | `C-DM-53` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 0 | 11 |
| User roles | 2 | 51 |
| Core features | 10 | 181 |
| User flow | 3 | 39 |
| UI and UX notes | 5 | 56 |
| Technical requirements | 5 | 44 |
| Data model | 9 | 88 |
| Front-end specification | 2 | 78 |
| Constraints | 0 | 16 |
| Deployment contract | 10 | 50 |
