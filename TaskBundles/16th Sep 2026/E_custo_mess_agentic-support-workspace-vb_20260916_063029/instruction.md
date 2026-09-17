# Agentic Support Workspace

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, sign in as the
administrator, invite a teammate to a role and a team, route a waiting customer
conversation into that team's inbox, and watch the automated agent answer a second
conversation from a published article and hand a third one to a person, without hitting an
error page. A different stranger signed in as a teammate must NOT be able to reach a
conversation belonging to a team they are not in, by any means, including a direct request
to the interface with a known identifier. The notification mail that leaves this product
must land in exactly one inbox: the invitation reaches the invited address and nobody
else, and the handover notice reaches the receiving team's lead and nobody else. A message
the app records as sent to itself does not count; the mail must exist as a real delivered
message in Mailpit, addressed to exactly that one recipient, with no carbon copy and no
blind carbon copy.

## Overview

This is the shared workspace a customer support organization lives in all day. Every
conversation a customer starts, on any channel, lands in one list that the whole team
works through together. A teammate picks a conversation up, replies, and closes it. An
automated agent called Auto Agent answers on its own from the workspace's own published
knowledge, shows its reasoning in the thread rather than behind it, and hands the
conversation to a named team when it cannot ground an answer or when an action would cross
the workspace's approval ceiling. Service level policies put a clock on the first response
and on resolution, and a manager reads a report that says how many conversations were
settled, by whom, and how many targets were met.

Two kinds of people use it and they need different things. A teammate needs speed:
hundreds of conversations a day, a queue that never loses their place, and a keyboard that
does everything. An administrator and a manager need reach and restraint: an administrator
owns the workspace's teammates, roles and teams, and a manager sees the teams they lead
and not the whole business. Customers never sign in here at all. They read the public help
surface, which is generated from the same articles the automated agent answers from.

The state-changing workflows are few and each one is worth naming: open, assign, route,
snooze, reopen and close a conversation; send a reply or a note on a channel; let the agent
answer and let it hand over; publish, unpublish and version a knowledge article; start,
pause, satisfy and breach a service level target; invite a teammate, accept the invitation
and change a role. Everything else in the product is reading.

The non-goals, stated so a build does not drift into them. There is no marketing site, no
trial, no plan, no invoice and no spend cap. There are no outbound campaigns, no proactive messages and no customer
satisfaction ratings. There is no separate ticket record with its own configurable state
machine; a conversation's own state carries the work. There are no attachments, no file
uploads, no translation, no conversation merging, no second factor and no federated
sign-in. There is no public interface for other systems to call and no integration
catalogue.

The genuinely hard part is that reach is a relationship rather than a rank: a manager
reaches the teams they lead, a teammate reaches the teams they belong to, and a record
outside somebody's reach must be reported as absent rather than refused, because a refusal
confirms the record exists.

## User roles

Signup is closed. There is no public registration route and no self-service account
creation. The four accounts below are seeded, and every other account is created only by
an administrator's invitation.

| Role | Can read | Can write |
|---|---|---|
| `admin` | every conversation, article, team, teammate and report in the workspace | reply, note, assign, route to a team, change state, run the agent, publish and unpublish articles, invite a teammate, change a teammate's role, create and edit teams, create and edit service level policies. **Cannot** assign a role at or above their own, and **cannot** demote or deactivate the last active administrator |
| `manager` | conversations, articles and reports for the teams they lead, plus every conversation assigned to them | reply, note, assign within the teams they lead, route within the teams they lead, change state, run the agent, edit the service level policies. **Cannot** read or act on a team they do not lead, **cannot** invite a teammate, **cannot** change anybody's role, and **cannot** create or archive a team |
| `teammate` | conversations in the teams they belong to, plus conversations assigned to them, plus every published article | reply, note, assign within their own teams, change state, run the agent. **Cannot** read a team they do not belong to, **cannot** route a conversation to a team they are not in, **cannot** invite a teammate, **cannot** change a role, **cannot** publish an article, and **cannot** open any settings screen |

Reach is computed from current membership on every request, not carried in the session. A
role change or a team change takes effect on the next request rather than on the next
sign-in, and an administrator who removes somebody from a team removes that team's
conversations from their reach immediately.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in
the UI is not authorization: a direct API call from a `teammate` session to any
`admin`-only endpoint must be rejected by the server (an unauthorized request is denied,
not served), leaving the protected state unchanged.

Reads are stricter than a denial. A request for a conversation, an article or a report
outside the reader's reach is answered as though the record does not exist, and the
interface renders the product's own not-found page. A refusal would confirm that the
record exists, which is itself a leak across the team boundary. The one exception is a
whole screen a role may never open: opening a settings screen as a `teammate` is refused
plainly, and the screen names the role that can grant access, because the existence of the
settings screen is not a secret.

Every seeded account uses the password `deku-demo-pw-2026`.

| Email | Name | Role | Teams |
|---|---|---|---|
| `admin@example.com` | Dana Whitfield | `admin` | none |
| `manager@example.com` | Priya Raghunath | `manager` | lead of `Billing Support` |
| `teammate@example.com` | Marco Ferraro | `teammate` | member of `Billing Support` |
| `teammate2@example.com` | Leah Okonkwo | `teammate` | member of `Technical Support` |

## Core features

### Auth

Email and password, with a bearer token issued on sign-in and presented on every request
except sign-in itself, the health route and the public help routes. Passwords are stored as a
memory-hard hash with a per-record salt and tuned parameters, never as a fast hash, never
in plain text and never reversibly. A token expires after 24 hours; a
request carrying an expired or unknown token is rejected as unauthorized, and the
interface returns the person to the sign-in screen without losing what they had typed into
a composer. The token carries identity only. It does not carry the role, the team list or
any reach, because a token that carries permission is a token that keeps permission after
it has been taken away.

1. Sign-in with a correct address and password returns a bearer token under the key
   `access_token`, together with the signed-in person's identity, role and teams.
2. Sign-in with a wrong password, or with an address that has no account, is rejected as
   invalid, and both cases produce the same message and take the same visible path, so the
   form cannot be used to find out which addresses exist.
3. There is no signup route, no password reset route and no invitation route other than
   accepting an invitation an administrator created. A request to create an account by any
   other means is rejected as invalid.
4. Signing out revokes the token. Revocation is immediate and irreversible: a request
   afterwards carrying that token is rejected as unauthorized, and there is no
   self-contained token that outlives its revocation. A session has an absolute lifetime of
   24 hours and an idle lifetime of 2 hours, refreshed on use, whichever ends first.
5. Invalidation of reach is immediate too. Removing somebody from a team, changing their
   role or deactivating them takes effect on the very next request they make, without
   waiting for them to sign out. Session state is never trusted to carry a permission,
   which is the whole reason reach is recomputed rather than cached into the token.
6. Sign-in resists enumeration. Neither the form, the wording, the timing nor the shape of
   the response says whether an address has an account, because a form that answers that
   question is a tool for finding out who works here. That information leakage is treated
   as a security defect, not as a convenience.

### The omnichannel inbox

One list holds every conversation, whatever channel it arrived on. The channel set is
fixed: `messenger`, `email`, `phone`, `social`. A conversation records the channel it
arrived on, and a reply is sent back on that channel.

Six views, each a saved query rather than a separate store:

| View | What it holds |
|---|---|
| `Your inbox` | conversations assigned to the signed-in person, in state `open` or `snoozed` |
| `Mentions` | conversations holding a note that mentions the signed-in person and that they have not read |
| `Created by you` | conversations the signed-in person opened |
| `All` | every conversation the signed-in person may read |
| `Unassigned` | conversations with no assignee, in a team the signed-in person may read |
| `Team inboxes` | one view per team the signed-in person may read, named for the team |

1. A view never grants access. Two people opening the same view see different rows, and
   the count shown beside the view name is computed after reach is applied, never before.
   A count computed before reach tells a teammate how many conversations exist in a team
   they cannot read, which is the leak this rule exists to close.
2. Every row shows a generated avatar, the contact's name, a one-line plain-text preview
   of the most recent part with any markup stripped and the text cut on a word boundary,
   the relative age of the conversation, the channel as a labelled glyph, the assignee
   when the view is not already scoped to one, and the service level state. Unread is
   carried by a marker as well as by weight.
3. Filtering, sorting and search are visible controls at the top of the list rather than
   settings buried somewhere. The filters are state, assignee (including Auto Agent, and
   including unassigned), team, channel, service level state, and a free-text search over
   the conversation subject and over the bodies of its parts. The sorting choices are
   newest, oldest and longest waiting, and every sort is deterministic: two conversations
   that tie on the sorted value are broken by their identifier, so the same list never
   comes back in two different orders. The applied filters and the sort are part of the
   address, so a filtered list is shareable, and opening that address restores exactly that
   list.
4. Search is scoped to the workspace and reach is applied before ranking, never after. A
   search that matches nothing echoes the query back, names the filters that are applied,
   and offers to clear each one.
5. Opening a conversation changes the address and keeps the list. Moving from one
   conversation to the next must not rebuild the list, lose its scroll position or lose
   the selection, because a teammate moves through a queue at speed all day.
6. A conversation that no longer matches the current view leaves the list after the
   current action has settled. It is never removed from under a click.
7. Three empty states, all distinct and none of them shared. A workspace that has never
   had a conversation reads exactly:
   `No conversations yet. Connect a channel to start receiving them.`
   A filter that matched nothing reads exactly `No conversations match these filters.`
   A queue that has genuinely been cleared reads exactly `You are all caught up.`
   Clearing a queue is an achievement and must not look like an error.
8. Presence is shown where two people could collide. Teammates currently looking at the
   same conversation appear on it by generated avatar, and a teammate who starts a reply
   while another teammate already has one in progress is warned before sending rather than
   after, which is the moment it is still fixable. The customer never sees any of this
   collaboration signal, and presence is never stored and never appears in any record.

### The conversation and the composer

A conversation is an ordered stream of typed parts, oldest first. The order is the
conversation's own sequence number, never a timestamp: two parts written in the same
instant still have one defined order, and a clock difference between two writers must
never reorder a thread.

The part kinds are fixed, and every one of them renders differently. An `assignment`, a
`state_change`, a `snooze` and an `sla_event` render as single-line system events at
reduced strength, so the thread reads as a record without the housekeeping shouting over
the messages. The kinds are: `customer_message`,
`teammate_reply`, `agent_reply`, `note`, `agent_reasoning`, `agent_tool_call`, `summary`,
`handover`, `assignment`, `state_change`, `sla_event`.

1. The composer has exactly two modes, `Reply` and `Note`, chosen with a labelled control
   and shown on different grounds. A note is internal and can never reach a customer.
   Switching from `Note` to `Reply` with content already typed asks for confirmation
   first, because sending an internal note to a customer is the accident this product
   exists to prevent.
2. The composer carries a discoverable shortcut hint beside its tools, stating in words how
   to reach the keyboard shortcut list without hunting for it, and its tools are macro
   insertion, article insertion and an assistance control.
3. The send control is a split control offering `Send`, `Send and close` and `Send and
   snooze`. Snoozing requires a wake time, and a customer message wakes a snoozed
   conversation immediately.
4. A part appears in the thread as soon as it is submitted, marked as sending, then as
   sent. A part that fails to send stays in the thread marked as failed, carries the
   reason, and offers a retry. It is never silently discarded, because a discarded reply
   leaves a teammate believing they answered somebody they did not.
5. Sending carries a key generated by the client for that attempt. Submitting the same
   attempt twice, whether by a double press or by a retry, appends exactly one part and
   never two.
6. An unsent draft is ephemeral state and belongs to the person who wrote it, per
   conversation. It survives navigating away, a reload and a crash, and it is kept locally
   first and then saved to the store. Reassigning a conversation away from somebody keeps
   their unsent draft attached to them and tells them; quietly discarding a half-written
   apology to a customer is the kind of loss people leave a product over.
7. A reply body accepts a small allowlist of formatting and nothing else. Anything
   outside the allowlist is stripped on the way in and the stored body is sanitised again
   on the way out, so a customer message can never inject markup into a teammate's screen.
   Every free-text field carries a visible length counter, has a length limit enforced at
   the server, is trimmed at its ends and never in its middle, and round-trips accented
   characters, emoji, combining marks and right-to-left text exactly as they were typed,
   in the list, in the thread and in every export.
8. No role may delete a conversation or a part, and the product offers no route that
   does. A conversation leaves the working views by being closed, and a part that should
   not have been written is superseded by a later part rather than removed, so the record
   of what happened stays whole.
9. A mention of a teammate inside a note adds the conversation to that person's `Mentions`
   view and grants nothing. If the mentioned person may not read the conversation, they
   are told they were mentioned in something they cannot open, and by whom.
10. A reply written by Auto Agent is always visibly a reply written by Auto Agent. It
   carries the agent's name and its own accent, and there is no configuration, no setting
   and no code path by which it is attributed to a person.
11. The conversation header carries the contact's name, which opens the contact in the
   details panel, a row of controls, and a `Close` action set apart from the rest because
   it is the one that feels irreversible.
12. The state machine is `open` to `snoozed` and back, and `open` or `snoozed` to `closed`
   and back to `open` when a customer replies. Closing records who closed it and when, and
   sets the resolver to `agent` when the last substantive reply was an `agent_reply` and
   to `human` otherwise. Reopening increments the reopen count.

### Auto Agent

Auto Agent is a principal in its own right, with a name, a version and its own reach. It
belongs to teams exactly as a person does, and everything it does is attributed to it in
the audit record. It never acts under a person's identity.

Running the agent on a conversation is a single action, available to any signed-in person
who may reply to that conversation. Each run proceeds in the same order, and each stage is
recorded as a step on the run:

1. **Admission.** The run proceeds only if the conversation is `open` and the person
   triggering it may reply to it. Otherwise it is rejected as invalid and no part is
   appended.
2. **Retrieval.** The run searches the workspace's `published` articles for the
   conversation's subject and for the words of the customer's most recent message. A
   `draft`, `in_review`, `unpublished` or `archived` article is never retrieved. An article
   in a collection whose audience is `internal` is never used to answer a customer, though
   it may be cited in a note.
3. **Reasoning.** The run appends one `agent_reasoning` part per step, each a single plain
   sentence saying what it is about to do and why. It is collapsed by default in the
   thread and titled with the agent's name and the step number, in the exact form
   `Auto Agent's thoughts (Step 1)`, the number counting from one within the run.
4. **Tool calls.** The run appends one `agent_tool_call` part per call, each carrying a
   short human-readable label and, expandable beside it, the exact arguments and a digest
   of the result. A teammate must be able to see the exact arguments and must never be
   shown only a friendly summary of something that touched a customer's account. Two tools
   exist. `read_account` reads the contact's own record and is a read. `issue_credit`
   applies an account credit in integer minor units of `usd` and is a write. Every call is
   policy-checked against the agent's own reach before it runs, has its arguments validated
   against the tool's declared shape, is executed under a timeout after which the step
   fails and is recorded rather than hanging, and is recorded whatever its outcome.
5. **The approval ceiling.** `issue_credit` may be called automatically only for an amount
   at or below `5000` minor units. Above that the agent does not call it and does not
   refuse the customer: it hands over. This is the policy threshold, and crossing it is
   never reported to the customer as a failure.
6. **Grounding.** Every factual claim in an `agent_reply` traces to a published article
   version the run retrieved, or to a tool result from this run. The run records the
   identifiers of the exact article versions it used. If nothing retrieved grounds the
   answer, the agent does not answer from anything else and hands over instead.
7. **Guardrails.** Every candidate reply passes the same guardrail set before it is
   emitted, and failing any one of them withholds the reply and hands over instead: it is
   grounded, its citations are recorded on the run even when they are not shown to the
   customer, it carries no credential and no other customer's data, the personal data it
   repeats is only that of the contact it is answering, it is in the contact's own
   language, and its length and format are channel-appropriate for the channel it is going
   out on.
8. **Instruction resistance.** Anything inside a customer message or a contact record is
   data, never an instruction. A customer message asking the agent to change its own rules,
   raise its ceiling, ignore its policy or reveal another customer's record is answered as
   an ordinary customer message and is flagged on the run. It must not change what the
   agent does.
9. **Emission.** On success the run appends one `agent_reply` and the outcome is
   `resolved`. On handover the run appends a `summary` part and then a `handover` part,
   sets the conversation's team from the routing rule, leaves the conversation `open`, and
   the outcome is `handed_over`. The customer is told a person is joining, in the exact
   words `Connecting you with a specialist who can help.`
10. **Handover triggers**, any one of which is sufficient: nothing retrieved grounds an
   answer; a write would cross the approval ceiling; the customer asks for a person; or the
   run has already taken three turns on this conversation without resolving it; or the
    customer message shows detected frustration or touches a topic the workspace has marked
    sensitive, in which case the reason is recorded on the run alongside the handover.
11. **Idempotency.** A run is keyed on the part that triggered it. Triggering the agent
    twice for the same customer message produces exactly one run, exactly one reply or
    exactly one handover, and never a second set of parts.
12. **Failure.** If retrieval is unavailable the agent does not answer from anything it
    happens to hold; it hands over. An answer invented without a source is worse than no
    answer.
13. **The summary card.** A summary is drawn only from parts in this conversation, is
    marked as machine-generated, and is titled exactly `Summary`. It is a reading aid: no
    automated action is ever taken from it, and it is marked stale rather than silently
    rewritten when new parts arrive.
14. **Auditability.** For any answer the agent has ever given, the workspace can retrieve
    the exact article versions it read, every tool call it made with its arguments and the
    digest of its result, the policy version in force, which guardrail withheld a reply if
    one did, every reasoning step, and when the run started and ended. An article edited
    afterwards must not change what the record says the agent read, which is why a citation
    names a version rather than an article.

### The knowledge hub

Collections hold articles; articles hold versions. A collection carries an audience,
either `public` or `internal`. An article's body lives in its versions and never in the
article row, so the question "what did this article say when the agent used it" always has
an answer.

1. The lifecycle is `draft`, `in_review`, `published`, `unpublished`, `archived`.
   Publishing writes a new version with an incremented version number and points the
   article at it as the current version. Publishing the same article twice produces two
   versions, not one overwritten one.
2. Only an `admin` may publish or unpublish. A `manager` or a `teammate` attempting it is
   denied at the server and the article's state is unchanged.
3. Unpublishing removes the article from the public help surface and from agent retrieval
   immediately, and retains every version.
4. An article in an `internal` collection never appears on the public help surface and is
   never used to answer a customer. Hiding a page from the public surface while leaving the
   agent free to quote it aloud is not a restriction at all.
5. The hub shows a gap queue. A gap has a kind, a priority badge reading `High`, `Medium`
   or `Low`, a title, a one-line rationale and an age in days. The three kinds are
   `content_gap` (customers ask something the knowledge base does not answer),
   `customer_data_gap` (answering needs a record the agent cannot reach) and `action_gap`
   (answering needs an action the agent cannot take). They are labelled in the interface
   exactly `CONTENT GAP`, `CUSTOMER DATA GAP` and `ACTION GAP`. A gap is created whenever
   an agent run hands over, carrying the handover reason as its rationale.
6. Each gap offers the one action that closes it. Dismissal carries a reason, and it feeds
   suppression: a dismissed gap does not come back for the same conversation.

### Service levels

A service level policy names a first-response target and a resolution target, both in
whole minutes.

1. A policy is matched to a conversation when the conversation is created, and the matched
   policy's identifier is recorded on the conversation along with the two due times
   computed from it. Editing a policy afterwards changes nothing about a conversation
   already in flight. A policy edit that rewrote history would make every past attainment
   figure a fiction.
2. The first-response clock starts on the customer's first message and stops on the first
   `teammate_reply` or `agent_reply`, whichever comes first. The moment of the first
   response is recorded once and is never rewritten by a later reply.
3. The resolution clock starts on the customer's first message and stops when the
   conversation is closed. The timer pauses while the conversation is `snoozed` and resumes
   on the customer's next message, and every elapsed duration is summed from the intervals
   the timer was actually running rather than subtracted from a wall-clock reading.
4. The service level state is one of `on_track`, `at_risk`, `breached` and `met`. It
   becomes `at_risk` once three quarters of the target has elapsed and `breached` at the
   target. All arithmetic is in UTC.
5. A breach is recorded exactly once per conversation per target. A sweep that runs again
   over the same overdue conversation appends no second `sla_event` part and produces no
   second breach record.
6. A breach appends an `sla_event` part to the thread naming which target was missed and
   when. It sends no mail. Service level state is surfaced in the product, not in an inbox.
7. A sweep looks for overdue conversations on a repeating interval, ordered by the
   soonest due time so the most overdue is handled first. Two copies of the app running at
   once must not both sweep the same conversation: the sweep takes a lease for its turn, and
   a second instance that cannot take it waits rather than duplicating the work. If it falls behind it works
   through the backlog oldest first and says so in the product; it never skips ahead to
   catch up, because a skipped backlog means the customer discovers the missed deadline
   before the team does.

### Teammates, roles and routing

This is the administrator's work, and it is the sequence the product is built around.

1. An `admin` invites a teammate by address, choosing a role and optionally a team, from a
   modal opened from the teammates screen. The role offered is bounded by the inviter's
   own: an `admin` may invite an `admin`, a `manager` or a `teammate`, and no route, form
   or direct request may create a role above the inviter's own.
2. An invitation creates a pending membership with status `invited` and a single-use
   token that expires in `7` days. At most one active invitation exists per address per
   workspace: inviting the same address again invalidates the previous invitation rather
   than creating a second. Inviting an address that already holds an active membership is
   refused as invalid with a clear message, and creates nothing.
3. Accepting an invitation collects a name and a password, activates the membership, adds
   the person to the chosen team, and consumes the token. Presenting the same token a
   second time is refused as invalid and changes nothing.
4. An `admin` changes a teammate's role from the teammates list. The control never offers
   a role at or above the actor's own, and a direct request that tries to elevate somebody
   to a role at or above the granter's own is denied at the server with the membership
   unchanged. The last active `admin` cannot be demoted or
   deactivated, and the control explains why.
5. An `admin` or a `manager` routes a conversation to a team inbox. Routing sets the
   conversation's team, clears any assignee, and appends an `assignment` part naming who
   routed it, from where and to where. A `manager` may route only within the teams they
   lead; a `teammate` may not route at all, and a direct request from either that names a
   team outside their reach is denied with the conversation unchanged.
6. Claiming an unassigned conversation is single winner under real concurrency. Two people
   pressing `Assign to me` on the same unassigned conversation at the same moment must not
   both succeed:
   exactly one becomes the assignee, the other is told the conversation has already been
   taken, and exactly one `assignment` part is appended. A failed claim leaves no partial
   state behind: no half-written assignment, no conversation left with two assignees, and
   no orphaned part.

### Notification

The app sends real mail over SMTP at `SMTP_HOST` and `SMTP_PORT`, authenticating with
`SMTP_USER` and `SMTP_PASS`. Mailpit is the mail server in this environment, it is already
running, and there is no third-party mail vendor and no API key.

Exactly two transitions send mail, and this is the rule the whole product turns on.

1. **The invitation.** When an administrator invites a teammate, one message is sent to
   the invited address and to no other address. There is no carbon copy and no blind
   carbon copy, and no copy goes to the inviter, to the team's lead, or to any other
   member of the workspace. The subject begins with `Support workspace invitation:`
   followed by a single space and then the workspace name, so an invitation into
   `Northwind Trading` carries the subject
   `Support workspace invitation: Northwind Trading`. The body names
   the workspace, names the role the person was invited to, and carries the acceptance
   link.
2. **The handover.** When an agent run ends in a handover, one message is sent to the lead
   of the receiving team and to no other address. There is no carbon copy and no blind
   carbon copy, and no copy goes to the customer, to the person who triggered the run, or
   to the other members of the team. The subject begins with `Handover needed:` followed by
   a single space and then the conversation's subject, so a handover on `Invoice shows the
   wrong tax rate` carries the subject
   `Handover needed: Invoice shows the wrong tax rate`. The body names the handover reason
   and carries the summary the run wrote. When the receiving team has no lead, the single
   recipient is the workspace's administrator instead, and still nobody else.
3. **Nothing else sends mail.** Replying, closing, reopening, snoozing, assigning,
   routing, publishing an article, changing a role, and breaching a service level target
   all send no message at all. If a message arrives for any of those, the product is
   wrong.
4. A message that cannot be delivered is recorded against the action with its reason and
   is retried on the next attempt. A failed delivery never rolls back the invitation or
   the handover, and it never produces a second delivered copy when it succeeds.

### First-run onboarding and the audit record

1. A first-run onboarding checklist sits above the inbox until it is dismissed for good.
   It lists what an empty workspace still needs: invite teammates, publish a first article,
   set a service level policy, and run the agent once. Each item's completion is derived
   from the state of the system rather than from a flag somebody set, so a checklist can
   never claim something is done that has since come undone.
2. The three seeded conversations and the seeded articles are marked as sample data. They
   are excluded from every reported figure and can be removed in one action. Without them
   an empty inbox is indistinguishable from a broken one.
3. Every write records the acting principal, its kind and the action, as an audit entry.
   Nothing is written unattributed, including a write made by the sweep, which acts as a
   named system principal. What is audited: sign-in, every conversation state change,
   assignment and routing, every agent run and every tool call it made, every article
   publish and unpublish, every invitation, acceptance and role change, and every refused
   attempt at any of those. The record is append only and the product offers no path that
   edits or removes an entry.

### Reporting

1. A report page states, for the reader's reach and for a chosen date range: the number of
   conversations resolved, the resolution rate split into agent-resolved and
   human-resolved, the service level attainment against each target, the number of
   conversations currently `at_risk`, and the number `breached`.
2. Reach applies to the report exactly as it applies to the inbox. A `manager` reads the
   teams they lead; an `admin` reads the whole workspace; a `teammate` reads only their
   own numbers and their own teams' totals. The same range read by the manager and by the
   administrator gives two different totals, and both are correct.
3. Response and resolution times are reported as the median and as the ninety-fifth
   percentile, never as a mean. A mean is dominated by a handful of week-old conversations
   and tells a manager nothing about what a typical customer experienced.
4. Every figure states the time zone it was computed in and the age of the data it was
   computed from. Freshness is stated rather than assumed, because the alternative is a
   manager acting on numbers that are twenty minutes stale without knowing it. A partial
   final period is marked as partial rather than plotted as a collapse, because a
   part-finished day drawn as a whole one looks like an outage that never happened.
5. Every chart has a table equivalent that is reachable rather than hidden, and no chart
   carries its meaning in colour alone.

### The public help surface

Published articles in a `public` collection are readable without a session, at a collection
index, a collection page and an article page.

1. The structure is collections, then articles, with breadcrumbs back up the collection on
   every article page and a short list of related articles from the same collection beneath
   it.
2. An article that is not `published`, or that lives in an `internal` collection, is
   absent from the public index, absent from public search, and answers not-found when
   requested directly rather than refusing. A refusal would confirm it exists.
2. Every public route declares its own title and its own description, and no two public
   routes share them.
3. An address that matches no route renders the product's own not-found page, on the
   product's own chrome, with a way back to the help index and to sign-in, and answers
   not-found rather than answering as though the page were found.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | sends a signed-in person to their inbox and everybody else to sign-in | none |
| `/signin` | email and password | none |
| `/invite/<token>` | accept an invitation: name and password | none |
| `/w/northwind/inbox` | the shared inbox at its default view | session |
| `/w/northwind/inbox/<view_id>` | a built-in view or a team inbox | session |
| `/w/northwind/inbox/c/<conversation_id>` | a conversation inside the list's context | session |
| `/w/northwind/knowledge` | collections, articles and the gap queue | session |
| `/w/northwind/knowledge/article/<article_id>` | one article and its versions | session |
| `/w/northwind/reports` | resolution and service level attainment | session |
| `/w/northwind/settings/teammates` | invite, change a role, add to a team | session, `admin` |
| `/w/northwind/settings/teams` | teams and their leads | session, `admin` |
| `/w/northwind/settings/sla` | service level policies | session, `admin` or `manager` |
| `/help` | the public collection index | none |
| `/help/<collection_slug>` | one public collection | none |
| `/help/<collection_slug>/<article_slug>` | one published public article | none |

**Entry and redirects.** An unauthenticated request for any workspace route lands on
`/signin`, and the address that was asked for is remembered and restored after a successful
sign-in. A successful sign-in lands on `/w/northwind/inbox`. Signing out clears the session
and returns to `/signin`, and going back afterwards does not restore a workspace screen. A
token that expires in the middle of an action leaves what was typed in the composer intact
and returns the person to `/signin`. A conversation identifier outside the reader's reach
renders the not-found page and answers not-found; it never renders a refusal. A `teammate`
opening `/w/northwind/settings/teammates` is refused at the server and sees a restricted
screen naming the role that can grant access.

**Journey one: the administrator invites a teammate and routes work to them.** Sign in as
`admin@example.com`. Open the teammates screen from the rail's settings control. Press
`Invite teammate`; a modal collects an address, a role and a team. Enter a new address,
choose `teammate` and choose `Billing Support`, and submit. An inline banner confirms the
invitation without leaving the screen, and a row appears with status `invited`. One message
arrives at that address and at no other. Open the link in it, set a name and a password,
and the membership becomes `active` with the person in `Billing Support`. Return to the
inbox, open `Invoice shows the wrong tax rate`, press `Route to team` and choose
`Billing Support`. An `assignment` part is appended to the thread, the conversation leaves
the unrouted state, and it now appears in that team's inbox view and in `Unassigned`.

**Journey two: a teammate works the queue.** Sign in as `teammate@example.com`. The
default view is `Your inbox`. Switch to `Unassigned` and open `Refund for duplicate
charge`. Press `Assign to me`; the row's assignee becomes Marco Ferraro. Type a reply in
`Reply` mode and press `Send and close`. The part appears as sending and then as sent, the
conversation's state becomes `closed`, its resolver becomes `human`, and the row leaves the
open views once the action has settled. Switch to `All` and try to open `Cannot reset my
password`, which belongs to `Technical Support`: the not-found page renders instead.

**Journey three: the agent answers, and then hands over.** Sign in as
`manager@example.com`. Open `Refund for duplicate charge` and press `Ask Auto Agent`. The
thread gains a collapsed reasoning disclosure titled `Auto Agent's thoughts (Step 1)`, a
tool-call row labelled for the record it read, and a reply grounded in the published
article `Refunds and duplicate charges`. Now open `Invoice shows the wrong tax rate` and
press `Ask Auto Agent`. Nothing published grounds it, so the run writes a `Summary` card
and a handover divider naming the reason and the receiving team, tells the customer
`Connecting you with a specialist who can help.`, and posts no other reply. One message
arrives at the lead of the receiving team and at no other address, and a `content_gap`
appears in the knowledge hub's gap queue.

**Journey four: the manager reads the report.** Sign in as `manager@example.com` and open
the reports screen. It states the resolution rate for `Billing Support`, split into
agent-resolved and human-resolved, the attainment against the first-response and resolution
targets, and the age of the data. Sign in as `admin@example.com` and open the same screen:
the totals cover the whole workspace and differ from the manager's.

**States.** Every list draws skeleton rows at the true row height while it loads for the
first time, so nothing shifts when the data arrives. A list that is refreshing keeps the
data that is already on screen and stays usable. Every page has a loading state. A panel
that fails is replaced by an inline retry inside its own region and takes nothing else with
it. Errors never crash the app, never show a raw internal message, and always say what
failed and what to do next. When the list is known to be out of date it says so and offers
a refresh rather than silently showing stale rows.

## UI/UX notes

Somebody opening this should understand within a moment that it is a working queue owned by
a team, that every row in it is a person waiting, and that nothing here is hidden from the
people responsible for it. The goal is comprehension, not atmosphere. The register is an
operational tool, and that register is the tiebreak for every judgement below: quiet, dense
but organised, built for scanning and for the same action repeated several hundred times a day.
No oversized hero, no editorial composition, no decoration standing in for content. The
public help surface is the one exception and reads as reading matter rather than as an
instrument.

The workspace has to support speed and repetition, so it earns density, large hit areas,
positions that never move and minimal chrome. It also has to reassure at the two moments
that are irreversible for a customer, sending a reply and closing a conversation, so those
two moments get stillness, plain wording and nothing moving while the decision is made. The
public help surface has to guide, so it earns a strong hierarchy and one obvious primary
action per screen, visually distinct from every secondary one.

**Two surfaces, two climates.** The public help surface sits on a warm near-white neutral,
nearer paper than white, and its darkest text is a near-black warm neutral rather than
black. The workspace sits on a near-black cool neutral ground with panels one step off it, a
selected row one step brighter again, and text running from white through a light cool
neutral down to a mid cool neutral for metadata. Same product, deliberately different
climate, because staring at a bright field for a working day is unpleasant. Nothing in
either surface is a true grey: a cool grey placed next to the public surface reads as cold
and wrong.

**The token layer, first.** Before any screen is painted, declare the colours, the type
roles and the spacing once as named tokens in three layers, and let a component read only
the third: a primitive layer of raw values that mean nothing on their own, a semantic layer
that names a role, and a component layer that names a part. That is what stops the
fourteenth screen from being a slightly different shade of off-white from the first, and it
is what lets the workspace redefine the semantic layer for its own darker climate without a
single component being touched.

**Palette by role.** Name a role for every colour before painting anything, and let each
component read the role rather than the value. The roles this product needs, and nothing
beyond them: the page ground; a raised panel above it; a subtle fill for an inert block; an
alternating section band on the public surface; an inverted band and a dark band again for
a section that flips the climate; a selected row; a navigation hover fill; the fill an
open-state panel takes; card and cell borders; a default border and a stronger border for
the same edge when it must assert itself; a decorative rule and the dot grid; the ground a
pull quote sits on; primary text, supporting copy, and a quieter tone again for metadata
and captions; text on inverted surfaces; an active control, an inactive control and a
disabled control; an interface divider; and three badges, a success badge, a warning badge
and a negative badge. Interaction carries a mid, vivid blue, and it is the only colour a
person can press. The focus ring is that same blue, on every ground including the near-black
workspace. Product identity carries a second, deeper vivid blue a few steps away from the
interaction blue; the two are close enough that swapping them looks like nothing and reads
like a mistake, so identity never appears on a control and interaction never appears on a
badge. Auto Agent carries a mid, vivid orange, and that orange appears nowhere except where
the agent is the author or the subject. Three colours carry state and appear nowhere else:
a mid, vivid red for something that has gone wrong, a mid, vivid green for something that
worked, and a light, vivid amber for something still in progress, which is also the ground
of the summary card. A state that is none of the three borrows none of them. Negative
customer sentiment carries a light, soft red, kept distinct from the failure red so a bad
mood is not read as a broken system, and an automated sender that is not the agent carries
a deep, soft indigo. Three further accent pairs are reserved for surfaces this release does
not ship, named here so a later one does not invent them: a deep, vivid cyan with a
near-white, soft blue; a deep, muted teal with a light, vivid lime; and a light, vivid lime
with a mid, soft green. One decorative band exists on the public surface and is the only
place in the product where colour is decorative: it runs from a light, vivid magenta
through a light, vivid red, a light, soft red, a light, vivid orange, a mid, vivid lime and
a mid, vivid green. It must not become a system pattern. The exact shades are yours, so
long as every relationship and every exclusivity rule above holds.

**Type.** The interface, the navigation and every control are set in a geometric grotesque
with a tall x-height and near-vertical terminals, at a regular and a medium weight and
nothing heavier. Reading copy on the public help surface is set in a light transitional
serif, which inverts the usual editorial convention and is a large part of the tone. A
monospace is reserved for eyebrow labels, set uppercase with open tracking, and appears
nowhere else. The scale carries a heading role at several steps, a large body role, a body
role, a callout, a label role and two button roles, a larger and a smaller, and it is
declared once per width step rather than interpolated between them. Each family declares a
fallback whose metrics are adjusted so nothing jumps while a face is loading. At most three
font files ship, each subset to what the product actually uses and preloaded, and no other
binary asset is loaded at all. Headings carry real contrast against body copy in both size and
weight, and their tracking tightens as they grow rather than being interpolated from one
setting, so large type stays tight and small type stays readable. Figures line up in a
column wherever counts, ages and durations stack, which here is the whole conversation list
and every report.

**Shape, density and elevation.** Corners are barely softened and the system is nearly
square: controls and links take the smallest softening, popovers one step more, nested
panels one step beyond that, and the only fully round shape in the product is a person's
avatar. A build that rounds generously has changed the design. Nothing floats: elevation is
carried by a hairline border and a change of ground tone rather than by shade, and adding
card shadows changes the design. Spacing runs on one scale built from a single base unit,
and every gap, every inset and every stack is a step on it; the radius scale has a handful
of steps from barely softened to fully round and no value sits between them; and a
container scale caps how wide reading copy and a centred panel may grow, with the widest
step holding the content centred and the ground running on past it. Density is tight in the
workspace, with rows close enough that a full queue reads in one screen, and every gap is a
multiple of one base unit that is yours to choose and then hold everywhere. The public help surface is more generous, with the
gap between sections several times the gap beneath a heading and about halving on a narrow
screen. Space over dividers: sections read as separate at a glance without a rule between
them, and a rule appears only where the two decorative devices call for one. Those two
devices are built once as components rather than as one-offs: a dotted section rule of
evenly spaced marks, and a tiling dot grid painted behind the public help index and behind
the not-found page. Small square corner marks in the interaction blue sit at the corners of
a band. That is the entire decorative language.

**Iconography.** Every glyph is drawn in the build from its own geometry. There is no icon
font, no icon image file and no external icon package, and no third-party mark is
reproduced anywhere. Two menu weights exist and are not interchangeable: a stroked pair in
the workspace shell and a filled pair on the public surface, whose middle bar is
deliberately longer than the outer two. A chevron rotates between its closed and its open
position on a disclosure. The wordmark is set as type rather than traced. Every icon-only
control carries a text label that is always available to assistive technology and revealed
on pointing.

**Motion.** The character is measured rather than expressive: everything eases, entrances
and exits alike, and nothing overshoots or bounces. One curve and one speed govern
everything a pointer causes, quick enough not to be waited for and slow enough to be seen;
anything entering the view is slower than that, and nothing that responds to input is
slower than half a beat. Transform, scale and rotation animate as one group so a compound
move does not tear. The named moments are these, and each is a thing a person can see. The
link underline: point at any link and a hairline grows out beneath it from left to right,
drawn so that it never shifts the layout and clips correctly across a line break, and only
its width changes; this is the dominant interaction in the whole system and is built once as
a primitive, in three semantic variants, the default on navigation and footer links, the
product accent on inline links in body copy, and a softened one on secondary inline links.
The gradient sweep: behind the primary action on the public surface, a wide band of colour
stretches out and back continuously, on its own, never waiting to be pointed at. The scroll
progress indicator: a hairline at the top of a public page fills across as the reader moves
down and empties as they move back, driven from the reader's position rather than from a
timed sequence, so it runs backwards when they do, and it is kept out of the accessibility
tree. The settle: an element in the opening of a public page arrives soft and slightly out
of focus and sharpens as it lands. The panel enter: a disclosure rises a short distance into
place while fading in, on the same pair of properties at every width. The image entry:
imagery fades in only, with no travel. The refused move: a card a rule will not accept
returns to where it came from with a visible movement rather than vanishing. The primary
hover: the primary control's ground changes from near-black to the product identity blue,
which is a change of colour rather than a darkening and is one of the most recognisable
moments in the system. Under a reduced-motion preference the sweep stops and that ground
goes flat, the scroll progress indicator is removed rather than slowed, the settle resolves
immediately to its final state, any automatic advance stops entirely, and every marquee
stops; the link underlines, the focus rings and the state changes all stay, because they
inform rather than decorate and removing them removes information. That distinction is the
whole point, and a build that strips every transition under the preference has failed it.

**Components and their states.** One primary action style and one quieter alternative, both
carrying resting, pointed-at, pressed, focused and unavailable states, and unavailable is
never signalled by colour alone. An unavailable control stays focusable and says why it is
unavailable rather than being removed from the tab order. Escape closes every layer, at
every depth of nesting, and returns focus to whatever opened it. A destructive action that
can be undone offers an undo instead of a confirmation, because a confirmation taxes
everybody who was right in order to catch the rare person who was wrong; an irreversible
narrow one names the thing it will destroy; an irreversible wide one asks for the name to be
typed. Forms validate first when a field is left rather than on every keystroke, then on
every change once a field has been marked invalid, so the error clears the moment it is
fixed. Submitting validates everything, moves focus to the first invalid field and announces
how many failed. The submit control is never disabled until the form is valid: a dead
control does not say why it is dead. Every message says what is wrong and what to do about
it, is authored per field and per rule, and never exposes an internal field name; a message
reading only that the input was invalid is treated as a defect.

**The seven states.** Every surface that carries data implements all seven: nothing
requested yet, loading with nothing to show, loading with data already on screen, loaded and
empty, loaded and partly failed, failed, and known to be out of date. The two loading states
are never collapsed into one, because replacing a screen somebody is reading with a spinner
because a background refresh started is the defect that makes a tool exhausting. Skeletons
are drawn at the true dimensions of what is coming. Nothing shows a spinner for a wait
shorter than a blink. There are four kinds of empty and they do not look alike: a screen
nobody has used yet, a filter that matched nothing, a queue genuinely cleared, and something
the reader is not allowed to see. The cleared one is a good day and says so.

**Layout.** The workspace is a narrow permanent icon rail down the left, a resizable
contextual list beside it, then the working area, which itself splits into the thread and a
collapsible details panel. The rail never changes width and never reorders itself by
frequency, because people who live in this tool find things by position rather than by
reading, and a navigation that rearranges itself destroys that. The list's width and the
details panel's collapsed state are set by dragging and by folding, not in a settings
screen, and where somebody leaves them is where they stay. The public help surface uses a
top navigation bar and a footer instead of the rail.

**Responsive behaviour.** There are three named width steps, a phone step, a tablet step and
a desktop step, with two further refinement breakpoints above the last that widen the
container and the gutters without changing the type scale. Where each breakpoint falls is
yours, so long as the layout holds between them. The collapse order is fixed and every step
is designed rather than squeezed: the view list becomes a control, then the details panel becomes a
slide-over, then the list and the conversation become separate screens with a back control,
and finally the rail becomes a bar along the bottom where a thumb can reach it. The layout
holds at every width between those steps, and at a narrow viewport nothing overflows
sideways and every navigation target stays reachable. Four rules survive every width: a
conversation is always reachable by a direct link, the composer is visible without
scrolling whenever a conversation is open, the send control is never hidden by the
on-screen keyboard, and going back returns to the list at the position it was left. Touch
targets are at least 44 by 44 pixels wherever the pointer is coarse, every hover-only
affordance has a tap equivalent, and a disclosure opens on the first tap rather than
navigating.

**Accessibility.** Contrast meets WCAG 2.1 level AA on both palettes: at least 4.5 to 1 for
body text and at least 3 to 1 for large text, on every ground including the near-black
workspace ground, and the focus ring is checked against every ground it lands on. The focus
ring carries a visible thickness and sits at a small offset from the control it marks, so
it reads as a ring around the control rather than as a change to the control itself. The
document structure carries the meaning: one first-level heading per page, headings in order
without skipping, lists marked as lists, landmark regions everywhere, and the workspace's three panes labelled as regions so that somebody working by
keyboard can move between them directly rather than tabbing through a queue to reach the
composer. A skip link is the first focusable element on every page and becomes visible when
it takes focus; the workspace offers three skip destinations rather than one. Full keyboard
navigation reaches every control, with a visible focus ring, no positive tab order, focus
moving into a panel when it opens and back to its trigger when it closes, and focus never
lost to the page body after an action. Every icon-only control has an accessible name that
matches its visible label. Meaning is never carried by colour alone: unread carries a marker
as well as weight, service level state carries a word as well as a colour, and the agent's
replies carry its name as well as its accent. An arriving message, a send that succeeded,
loading starting and finishing, and a search result count are each announced politely as
an ordinary announcement; only a failed send and a service level breach announce
assertively, because a tool that shouts every arrival over what somebody is listening to is
a tool they cannot work in. These bars are a property of the finished product rather than
a matter of intention, so each journey above must be completable using the keyboard alone,
and must remain completable at twice the text size and at the narrowest supported width.
Verification of that is what the bars mean; an automated check alone settles perhaps a
third of them. Every content image carries alternative text
saying what it conveys, and an image that is purely decorative declares itself decorative so
it is skipped rather than described. Text scales to twice its size without losing content or
function, which the fixed-height list rows must survive.

**What this must not look like.** Not a marketing page wearing a working interface. No page
dominated by a single hue family with no second signal. No decoration standing in for
content. No panel lifted off the page by a shadow where a hairline and a change of ground
would do the same work. No oversized heading inside the workspace. Nothing borrowed from a
template that has never had to hold a queue of two thousand rows.

## Technical requirements

The application is server-rendered with interactive islands. SvelteKit produces the HTML
for the workspace and for the public help surface on the server and hydrates only the
regions that need to be interactive, so the browser receives rendered markup on first
paint rather than an empty root element. Express serves the JSON interface under the `/api`
prefix on the same origin. Both run on Node 20. The store is PostgreSQL, reached at
`DATABASE_URL`. Mail goes out over SMTP to Mailpit at `SMTP_HOST` and `SMTP_PORT` with
`SMTP_USER` and `SMTP_PASS`. The public address and port are read from `APP_PUBLIC_URL` and
`APP_PUBLIC_PORT`. No host, port, address or credential is written into the source; every
one is read from the environment.

Authentication is email and password implemented by the application, with a bearer token
presented on every request except sign-in, the health route and the public help routes.
Passwords are stored hashed. The token carries identity, and the role, the team list and
the reach that follows from them are resolved per request from current state.

`GET /api/health` returns `200` once the app is ready. Requests are logged to standard
output as structured records carrying the method, the route, the outcome and a request
identifier, and no password, token or other credential ever appears in a log line.

Performance and failure handling are properties of the finished product rather than a later
pass. Rendering the inbox list at the seeded size must not make the reader wait, and a slow
or failing dependency degrades one region rather than the whole screen: a failed panel
carries its own inline retry, an error boundary around every routed region keeps a
rendering failure inside that region, and the application shell never blanks. Security is
enforced at the server and nowhere else: every mutating request is authorized there, and a
denial changes nothing. Nothing the browser downloads contains a credential, an interface
key or an administrative token. The app serves a favicon and declares it in the document head of every route. Every
public route declares a social preview title and a preview image, and that image resolves
to a real response rather than to a missing file.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and Mailpit, and reaching for
anything else is a contract violation.

## Data model

Fifteen tables. All timestamps are UTC. Money is integer minor units with an explicit
currency and never a floating-point number. Identifiers are non-sequential, so a count
cannot be inferred from one and a neighbouring record cannot be guessed from one. Every
enumeration below is a constrained set of
values at the database rather than a free string, so a value outside it cannot be stored by
any path, including a migration or a background job. Schema changes arrive as reversible
migrations applied on start, and seeding is one of them.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must be
written into `/app/USER_README.md` alongside each account so a grader can sign in.

`workspace` holds `id`, `name`, `slug` (unique), `reporting_timezone`, `created_at`.

`app_user` holds `id`, `email` (unique, compared case-insensitively), `name`, `avatar_seed`,
`locale`, `password_hash`, `status`, `last_seen_at`, `created_at`. An `avatar_seed` rather
than an image: identity pictures are generated from the seed, so the product needs no image
file and no upload path.

`membership` holds `id`, `workspace_id`, `user_id`, `role`, `status`, `invited_by`,
`invited_at`, `accepted_at`, `deactivated_at`, and is unique on `workspace_id` with
`user_id`. `role` is one of `admin`, `manager`, `teammate`; `status` is one of `invited`,
`active`, `deactivated`.

`team` holds `id`, `workspace_id`, `name`, `slug`, `archived_at`, and is unique on
`workspace_id` with `slug`. `team_member` holds `id`, `team_id`, `user_id`, `is_lead`,
`joined_at`, and is unique on `team_id` with `user_id`.

`invitation` holds `id`, `workspace_id`, `email`, `role`, `team_id`, `token`, `invited_by`,
`created_at`, `expires_at`, `accepted_at`, `revoked_at`. At most one invitation per
workspace and address may be unaccepted and unrevoked at a time.

`contact` holds `id`, `workspace_id`, `name`, `email`, `avatar_seed`, `locale`,
`created_at`. A contact is a customer and is a different kind of record from a user; a
contact never signs in to the workspace.

`conversation` holds `id`, `workspace_id`, `contact_id`, `channel`, `subject`, `state`,
`priority`, `team_id`, `assignee_id`, `assignee_kind`, `created_at`, `first_response_at`,
`last_customer_at`, `waiting_since`, `snoozed_until`, `closed_at`, `reopened_count`,
`resolved_by`, `sla_policy_id`, `sla_state`, `first_response_due_at`,
`resolution_due_at`, `is_sample`. `channel` is one of `messenger`, `email`, `phone`,
`social`; `state` is one of `open`, `snoozed`, `closed`; `priority` is one of `normal`,
`high`; `assignee_kind` is one of `user`, `agent`, `none`; `resolved_by` is one of `agent`,
`human`, `none`; `sla_state` is one of `on_track`, `at_risk`, `breached`, `met`. The
relative age shown in the list is derived on read from `waiting_since` and is not stored.

`conversation_part` holds `id`, `workspace_id`, `conversation_id`, `seq`, `kind`,
`author_kind`, `author_id`, `body`, `delivery_state`, `created_at`, and is unique on
`conversation_id` with `seq`. `seq` counts from one within its conversation and is
allocated by the store rather than by the application, so two parts written at the same
instant still have one defined order and a clock difference between two writers can never
reorder a thread. `kind` is one of `customer_message`, `teammate_reply`, `agent_reply`,
`note`, `agent_reasoning`, `agent_tool_call`, `summary`, `handover`, `assignment`,
`state_change`, `sla_event`; `author_kind` is one of `contact`, `user`, `agent`, `system`;
`delivery_state` is one of `pending`, `sent`, `failed`.

`collection` holds `id`, `workspace_id`, `name`, `slug`, `audience`, `archived_at`, with
`audience` one of `public`, `internal`.

`article` holds `id`, `workspace_id`, `collection_id`, `title`, `slug`, `state`,
`current_version_id`, `owner_id`, `agent_eligible`, `help_center_visible`, `review_due_at`,
`archived_at`, with `state` one of `draft`, `in_review`, `published`, `unpublished`,
`archived`. `article_version` holds `id`, `workspace_id`, `article_id`, `version`, `title`,
`body`, `change_note`, `author_id`, `published_at`, and is unique on `article_id` with
`version`. The body lives only in the version.

`knowledge_gap` holds `id`, `workspace_id`, `kind`, `priority`, `title`, `rationale`,
`conversation_id`, `created_at`, `dismissed_at`, `dismissed_reason`, with `kind` one of
`content_gap`, `customer_data_gap`, `action_gap` and `priority` one of `high`, `medium`,
`low`.

`sla_policy` holds `id`, `workspace_id`, `name`, `first_response_minutes`,
`resolution_minutes`, `priority`.

`agent_run` holds `id`, `workspace_id`, `conversation_id`, `trigger_part_id`, `outcome`,
`handover_reason`, `policy_version`, `started_at`, `ended_at`, `idempotency_key`, with
`outcome` one of `resolved`, `handed_over`, `failed` and `idempotency_key` unique.
`agent_step` holds `id`, `workspace_id`, `agent_run_id`, `seq`, `kind`, `statement`,
`tool_name`, `tool_args`, `tool_result_digest`, `citation_article_version_ids`,
`created_at`. The citations name exact article versions rather than articles, so an article
edited afterwards does not change what the record says the agent read.

`audit_entry` holds `id`, `workspace_id`, `actor_kind`, `actor_id`, `action`,
`resource_kind`, `resource_id`, `detail`, `occurred_at`. It is append only: the application
has no path that updates or removes a row in it.

Every table above except `workspace` and `app_user` carries `workspace_id`, and it is not
nullable. A read that does not constrain on it is a read that can return another
workspace's rows.

**Invariants, each a property of the running system.**

1. Two people claiming the same unassigned conversation at the same moment: exactly one
   becomes the assignee, the other is refused, and exactly one `assignment` part exists
   afterwards. The refused attempt leaves nothing behind.
2. Triggering the agent twice on the same customer message produces exactly one
   `agent_run`, and exactly one reply or exactly one handover. A second trigger for the
   same message is a no-op that returns the first run.
3. Inviting the same address twice leaves exactly one unaccepted invitation for that
   address in that workspace, and the earlier token no longer works. Inviting an address
   that already holds an active membership creates nothing.
4. Accepting an invitation twice activates one membership. The second attempt is refused as
   invalid and changes nothing.
5. `first_response_at` is written once and never rewritten by a later reply.
6. A breach is recorded once per conversation per target, however many times the sweep
   passes over it, and appends exactly one `sla_event` part.
7. Publishing an article twice produces two `article_version` rows with consecutive version
   numbers and exactly one current version.
8. A role may never be created or changed to a role at or above the actor's own, and the
   last active `admin` membership can be neither demoted nor deactivated.
9. Removal is a state change on the record, and a cascade is never the mechanism that
   removes anything. Deactivating a teammate keeps their record so that every part they
   wrote still resolves to a name, and returns their assigned conversations to their team's
   queue. The one place rows do follow their parent is a row with no independent meaning,
   such as a step belonging to an agent run.

**Seed data**, applied on first start. Seeding must be idempotent: restarting the app must
not duplicate rows.

Workspace `Northwind Trading`, slug `northwind`, reporting zone UTC.

Teams `Billing Support` (slug `billing-support`) and `Technical Support` (slug
`technical-support`). `manager@example.com` is the lead of `Billing Support`.
`teammate@example.com` is a member of `Billing Support`. `teammate2@example.com` is a member
of `Technical Support`. `Technical Support` has no lead, so a handover routed to it names
the administrator as the recipient.

Contacts `Alina Sokolova`, `Tomas Berg` and `Rafael Mendes`.

One service level policy, `Standard support`: first response `60` minutes, resolution `480`
minutes. It matches every conversation.

Three conversations, all in state `open`:

| Subject | Channel | Contact | Team | Assignee |
|---|---|---|---|---|
| `Refund for duplicate charge` | `email` | Alina Sokolova | `Billing Support` | none |
| `Cannot reset my password` | `messenger` | Tomas Berg | `Technical Support` | `teammate2@example.com` |
| `Invoice shows the wrong tax rate` | `phone` | Rafael Mendes | none | none |

The third is the boundary case: it is unrouted, and no published article answers it.

Collections `Billing` (audience `public`), `Accounts` (audience `public`) and
`Internal runbooks` (audience `internal`).

Articles: `Refunds and duplicate charges`, `published` in `Billing`;
`Resetting your password`, `published` in `Accounts`; `Tax rates on invoices`, `draft` in
`Billing` and never published; `Escalation runbook`, `published` in `Internal runbooks`.

Auto Agent's automatic approval ceiling is `5000` minor units of `usd`, which is `$50.00`.
`$50.00` is `5000`, not `50.00` and not `50`.

## Constraints

One workspace, `Northwind Trading`. There is no workspace switcher, no second tenant and no
cross-workspace anything, but every tenant-scoped read is still constrained on the
workspace so that adding a second one later does not require rewriting every query.

Absent by design: signup, password reset, second factors, federated sign-in and directory
provisioning; billing of any kind, including trials, plans, invoices and spend caps;
outbound campaigns and proactive messages; conversation ratings; conversation merging;
translation; attachments and any file upload; a separate ticket record with its own
configurable state machine, and trackers; a public interface for other systems, webhooks,
apps and an integration catalogue; data residency, export and erasure; a marketing site.

No live connection. The interface refreshes when somebody navigates and when an action
completes, not by pushing changes to an idle screen.

No external network calls at run time. Everything the product needs is PostgreSQL and
Mailpit, both already running in this environment.

No native application. The product is a web application and nothing else.

The app must stay responsive with `2000` conversations in the workspace, each holding up to
`50` parts, and `25` teammates. The inbox list must open at that size without the reader
waiting on it.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array. A
successful call returns the named resource or shape; an invalid or unauthorized call is
rejected as a client error, never as a server error and never as a silent success. Bearer
auth is required on everything except `POST /api/auth/login`, `GET /api/health` and the
public help routes.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "access_token", "user": { "id", "email", "name", "role", "teams" } }` |
| `POST /api/auth/logout` | none | the revoked token's identifier |
| `GET /api/me` | none | the signed-in person with `role` and `teams` |
| `GET /api/conversations` | `view`, `state`, `assignee`, `team`, `channel`, `sla_state`, `q`, `sort` | an array of conversation summaries, each with `id`, `subject`, `channel`, `state`, `team_id`, `assignee_id`, `sla_state`, `waiting_since`, `preview` |
| `GET /api/conversations/:id` | none | the conversation with its `parts` array ordered by `seq` |
| `POST /api/conversations/:id/parts` | `{ "kind", "body", "client_key" }` | the created part with its `seq` and `delivery_state` |
| `POST /api/conversations/:id/assign` | `{ "assignee_id" }` or `{ "assignee_kind": "none" }` | the conversation with its new assignee |
| `POST /api/conversations/:id/route` | `{ "team_id" }` | the conversation with its new team and a cleared assignee |
| `POST /api/conversations/:id/state` | `{ "state", "snoozed_until" }` | the conversation with its new state and `resolved_by` |
| `POST /api/conversations/:id/agent-run` | none | `{ "run_id", "outcome", "handover_reason", "parts" }` |
| `GET /api/teams` | none | an array of teams with their members and leads |
| `GET /api/teammates` | none | an array of memberships with `email`, `name`, `role`, `status`, `teams` |
| `POST /api/teammates/invitations` | `{ "email", "role", "team_id" }` | the invitation with its `status` and `expires_at` |
| `POST /api/invitations/:token/accept` | `{ "name", "password" }` | the activated membership |
| `PATCH /api/teammates/:id` | `{ "role" }` | the updated membership |
| `GET /api/articles` | `state`, `collection_id` | an array of articles with their current version |
| `POST /api/articles/:id/publish` | `{ "change_note" }` | the article with its new `current_version_id` and `version` |
| `POST /api/articles/:id/unpublish` | none | the article in state `unpublished` |
| `GET /api/sla-policies` | none | an array of policies |
| `GET /api/reports/resolution` | `from`, `to`, `team_id` | `{ "resolved_total", "resolved_by_agent", "resolved_by_human", "resolution_rate", "attainment_first_response", "attainment_resolution", "at_risk", "breached", "timezone", "data_age_seconds", "final_period_partial" }` |
| `GET /api/help/collections` | none | an array of public collections with their published articles |
| `GET /api/help/articles/:slug` | none | one published public article |

**No mocks.** Mail must leave the application over SMTP and exist as a real delivered
message in Mailpit. An in-memory `sent` array, a log line announcing a send, a
`{"status":"sent"}` response the app returns to itself, a message written to the app's own
filesystem, or a delivery recorded in the app's own tables without a corresponding message
in Mailpit are each a contract violation, however correct the screen looks. Likewise, every
conversation, part, membership, invitation, article version and audit entry must live in
PostgreSQL: an in-memory store, a file on the app container's disk, or a store the app
itself controls in place of the named one is a contract violation. The named provider is the
fact - the app's UI and its own tables can only reflect what lives in the provider, never
substitute for it.

## Definition of done

A support teammate can open the app, work a shared queue, reply to a customer and close the
conversation, and the automated agent settles a second conversation from a published
article while handing a third to a named team with a written summary. An administrator can
invite somebody to a role and a team, and only that person receives the invitation. A
teammate cannot reach a conversation outside their teams by any route, and a manager's
resolution figures cover only the teams they lead.
