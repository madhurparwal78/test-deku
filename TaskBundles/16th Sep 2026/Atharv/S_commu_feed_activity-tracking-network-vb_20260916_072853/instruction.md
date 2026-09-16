# Ridgeline

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
read the signup landing, open a public activity and a segment leaderboard, create an
account, sign in as an athlete, upload an activity file, and watch that upload move
from received through parsing and matching to ready, while the activity it produced
appears in the feeds of the athletes who follow the uploader and an effort appears on
every segment the track crossed, without hitting an error page. A different stranger,
holding only a session for an athlete who is blocked, must NOT be able to reach the
blocker's content by any path: not the profile, not the activity, not the feed, not
the segment leaderboard, not a club they share, not a challenge, not search, and not a
mutual follower's kudos list. And an athlete on the free plan must be refused every
subscriber capability by the server, whether or not the interface ever offered the
control.

## Overview

Ridgeline is a social network whose unit of content is a recorded athletic activity.
It is for runners and cyclists who want their training seen and compared.

An athlete uploads a file recorded by a watch or a phone. That upload is the
transaction the whole product exists to perform, and it is a fan-out across four
subsystems that must all agree. The numbers are derived from a noisy time-series
rather than believed from the device. The track is matched against every segment it
crosses. The resulting efforts enter ranked leaderboards and mint achievements. And
the activity lands in the feeds of everyone who follows the uploader, filtered by
what each of them is allowed to see.

The visible product is a feed of cards. Underneath it is a geospatial pipeline that
ingests time-series from consumer hardware of varying quality, derives physical
quantities from noisy signals, matches curves against a library of segments,
maintains ranked leaderboards that must stay stable and correct, and enforces a
privacy model on data that reveals where people live. Almost every hard problem is
invisible from the card.

This is not a fitness tracker with a feed bolted on. The comparison is the product:
the palette carries named tokens for first, second and third place, and you do not
define podium colours unless podiums are what your product is about. Alongside the
feed the product carries segment leaderboards, clubs and challenges, route planning,
and a subscription tier.

The second thing this product is, and it is not optional, is a custodian of location
data. This data says where a person lives, when they leave the house, and on what
schedule. Every one of the four subsystems above is a way to leak it: a feed that
fans out before it filters, a leaderboard that names an athlete who has hidden their
profile, a segment effort that starts in somebody's front garden. Visibility is
therefore a property the data layer holds and the interface only reports.

Five audiences arrive here and the product owes each of them something different: an
athlete recording, who came for the record and the streak; an athlete comparing, who came
for segments, leaderboards and achievements; an athlete socialising, who came for the
feed, kudos and clubs; a subscriber, who came for routes, analysis and the heatmap; and a
prospective athlete, who came to the signup landing and has seen nothing yet.

Three non-goals, stated so nobody builds them: there is no recording in the browser
and no live position sharing, so activities arrive only as uploaded files or as
manual entries; there is no payment capture, so the plan surface sells and does not
charge; and there is no machine-learning type detection, so an activity's type
arrives with the file and is corrected by hand.

The genuinely hard part is that the same leaderboard is a different list for
different viewers. An athlete who is private, or blocked, or whose activity is
followers-only, must be absent from what a viewer is shown, and the ranks that viewer
reads must run without a gap. A gap at rank three tells the viewer that a hidden
athlete exists and exactly where they stand, which is the leak. That single
requirement rules out one cached list per segment.

## User roles

One role, `athlete`. Signup is open and anyone may create an account. The permission
boundaries this product enforces are between athletes rather than between ranks of
staff, and there are three of them, composing in this fixed order.

| Boundary | Rule |
|---|---|
| Block | overrides everything below it, in both directions of reading |
| Activity visibility | `everyone`, `followers` or `only_you`, per activity, defaulted per athlete |
| Follow state | `followers` visibility is satisfied only by an `accepted` follow; a `pending` request grants nothing |

A second axis sits across the role and is **not** a role: `plan`, taking `free` or
`subscriber`. It gates a named set of capabilities.

| Capability | `free` | `subscriber` |
|---|---|---|
| The feed, activities, kudos, comments, clubs, challenges | yes | yes |
| Segment leaderboards, all-time and date-bounded scopes | yes | yes |
| The route builder and saving a route | no | yes |
| The heatmap | no | yes |
| Best-effort analysis across distance classes | no | yes |
| Leaderboard filtering by age group, weight class and sex | no | yes |

- A blocked athlete **cannot** read the blocker's profile, activities, feed
  contribution, leaderboard rows, club posts, challenge standings, search results or
  kudos entries, and the block applies in both directions and to logged-out reads of
  the same content.
- An athlete who is not an accepted follower **cannot** read a `followers` activity,
  and **cannot** infer its existence from a rank gap, a row count or a total.
- Nobody **can** read another athlete's `only_you` activity, at any plan, by any
  path.
- Nobody **can** read a privacy zone, including through a profile, an export or an
  activity the zone truncated.
- A `free` athlete **cannot** reach a gated capability by calling its endpoint
  directly with a valid session.

Authorization is enforced **server-side on every read and every mutating endpoint**.
Hiding a control in the interface is not authorization: a direct API call from a
blocked athlete's session, or from a free athlete's session to a subscriber-only
endpoint, must be rejected by the server (an unauthorized request is denied, not
served), leaving the protected state unchanged.

Signup is open, and seeded accounts exist so the product can be opened and read
immediately. Every seeded account uses the password `deku-demo-pw-2026`.

| Email | Name | Plan | Default visibility | Standing |
|---|---|---|---|---|
| `athlete@example.com` | Rowan Ellery | `free` | `everyone` | blocks Mira Halloran; first on the seeded segment |
| `athlete2@example.com` | Sena Okafor | `free` | `everyone` | follows Rowan, accepted; second |
| `athlete3@example.com` | Dorian Vance | `free` | `followers` | profile not discoverable; third |
| `athlete4@example.com` | Mira Halloran | `free` | `everyone` | blocked by Rowan; fourth |
| `athlete5@example.com` | Kit Bramwell | `subscriber` | `everyone` | fifth; owns the seeded route |

A new account created through signup is a `free` athlete with `everyone` as its
default visibility, following nobody, and its feed is empty until it follows
somebody.
## Core features

### Accounts and sign-in

Sign-in takes an email and a password and returns a bearer token the client sends on
every later request. Passwords are stored hashed, never in the clear. Tokens expire;
an expired token leaves the action unapplied and returns the person to sign-in with
their destination preserved. Identity is resolved from the session, never read from a
request body: a request carrying an athlete field is treated as though it did not.

1. Signup by email collects an address, a password and a display name, and nothing
   else. It is not a full profile form: units, timezone, weight and privacy defaults
   are set later in settings and each carries a working default.
2. A signup with an address already registered is refused in a way that does not
   confirm the address is registered, and the refusal is the same refusal an invalid
   address receives.
3. A sign-in with a seeded email and `deku-demo-pw-2026` succeeds and returns a
   token.
4. A sign-in with a correct email and a wrong password is denied and returns no
   token.
5. A sign-in against an address that was never registered is denied with the same
   status, the same body and inside the same response-time band as a wrong password.
   A response that differs between a known and an unknown address is an
   account-enumeration vector, and on a product that publishes where people run that
   is a safety failure rather than a privacy nicety.
6. If sign-in collects the address first and the password second, the address step
   discloses nothing about whether an account exists.
7. A request to any athlete-scoped endpoint with no bearer token is denied.
8. Repeated failed sign-ins for one address are refused for a period, and a
   legitimate athlete can get back in without an administrator.
9. Sign-in may also be federated. A federated identity returns a verified address and
   that address is not re-verified.
10. Two accounts must never be created for one person arriving by two providers with
    the same verified address. Signing up with one provider and later signing in with
    another using that address yields one account with the second identity linked to
    it. Two accounts means the athlete's history splits, their totals are lost, and
    merging afterwards is painful and lossy.
11. A remembered session is offered at sign-in and is on by default. Because this
    product holds location history, that default is paired with a list of live
    sessions in settings, each showing where and when it began, and each endable
    remotely.
12. Acceptance of the terms and privacy documents is recorded with the exact text
    that was shown at the time it was accepted.

### The social graph

13. A follow is directed. Following an athlete whose profile is discoverable takes
    effect immediately and its state is `accepted`.
14. Following an athlete whose profile is not discoverable creates a request at state
    `pending`. The followee accepts or declines it. A `pending` request grants no
    access to anything.
15. The follow control reads Follow, Requested or Following, and those are three
    distinct states rather than two.
16. Unfollowing removes the edge and, where the followee's activities are
    `followers`, removes their access immediately, including to activities the
    follower had already seen in their feed.
17. Blocking is directed but symmetric in effect. With a block in either direction
    between two athletes, neither reaches the other's content by any read path.
18. The read paths a block covers, exhaustively: the profile, the activity page, the
    following feed, a club feed they both belong to, a club roster, a challenge's
    standings, a segment leaderboard, search, the kudos list on a third athlete's
    activity, the comment list on a third athlete's activity, the public API, and a
    logged-out read of any of the same content.
19. Blocking is enforced at the data layer. Removing a row from a rendered list is
    not enforcement: the endpoint that would have returned it must not return it.
20. A block removes any existing follow edge in both directions, and neither athlete
    can re-follow the other while the block stands.
21. A blocked athlete is told nothing. The blocker's content returns the same
    not-found the product returns for content that does not exist, because a refusal
    confirms the thing exists.

### Upload and ingest

22. An upload accepts an activity file recorded by a device. It returns an upload
    identifier immediately; the activity is produced by processing that runs
    afterwards.
23. The raw file is retained, byte for byte, exactly as it arrived. Retaining it is
    what makes every later parser improvement possible, and it is the requirement a
    build skips to save storage. A parser fix must be re-runnable against it without
    asking the athlete to upload anything again.
24. Parsing is tolerant. An unknown field is ignored rather than fatal, because
    device firmware invents fields. A file that parses partially produces an activity
    carrying whatever was recoverable plus a recorded warning, rather than failing
    whole.
25. The timestamps inside the file are the authority for the activity's start time.
    The moment of upload is not the start time.
26. The file's own timezone, where it carries one, is preferred over any inference
    from coordinates.
27. An upload moves through `received`, `parsing`, `matching` and `ready`, or
    terminates at `failed` or `duplicate_suspected`. The athlete sees the state it is
    in and a terminal state when it stops.
28. A `failed` upload is retryable from the retained raw file, without re-uploading
    the file.
29. Manual entry produces the same activity model with no streams. A manual entry
    cannot produce a segment effort, and it is visibly distinguished everywhere it
    appears, because an unverifiable manual entry sitting on a leaderboard is a
    cheating vector.
30. A partner integration, being another service pushing on the athlete's behalf,
    produces the same activity model as a device file.
31. Duplicate detection runs **before** segment matching. The naive arrangement, which
    is to deduplicate later or not at all, is the one to avoid. Athletes routinely record
    one activity twice, from a watch and a phone, or from a head unit and a watch, or
    from an automatic sync landing alongside a manual upload. A duplicate that
    reaches matching puts the same effort on a leaderboard twice, which looks like
    cheating and corrupts every total that segment feeds.
32. Duplicate detection checks the file's own unique identifier first, where the
    format provides one. Failing that it compares, for the same athlete, start time
    within a tolerance, duration within a tolerance and distance within a tolerance.
33. A suspected duplicate is flagged for the athlete to resolve and is never silently
    discarded. The athlete is shown both candidates and chooses which to keep, and
    the discarded one's efforts are removed.
34. Re-uploading bytes identical to an earlier upload by the same athlete returns the
    earlier upload and creates no second activity.
35. Photographs attached to an activity have their location metadata stripped on the
    server, on ingest, before storage. One photograph carrying intact coordinates
    defeats every other privacy control in this product.

### Streams and derived metrics

A stream is a time-series recorded alongside an activity. The types are `time`,
`latlng`, `distance`, `altitude`, `heartrate`, `cadence`, `watts`, `temp`, `moving`
and `grade_smooth`. `time` is the index the others align to.

36. Streams are stored separately from the activity row, by reference, and fetched on
    demand rather than joined into every read.
37. Every stream declares whether it was measured or derived, and a derived stream
    records the version of the algorithm that produced it. Algorithms improve, and
    knowing which activities were computed under which version is what makes
    recomputing years of history a decision rather than an accident.
38. Power may be measured or estimated, and the two are distinguished on the record
    and in the interface.
39. Streams are not necessarily the same length and not necessarily aligned. A watch
    may record heart rate every second, position every three seconds while it has a
    fix and not at all in a tunnel, and power only while a sensor is paired. The build
    aligns on the time index rather than on array position.
40. A gap is a gap. An average excludes the gap from both the numerator and the
    denominator, and the activity states the coverage the average was computed over.
    A heart-rate dropout treated as zeros halves the reported average, and athletes
    read that as a health signal.
41. Moving time and elapsed time are two different numbers on every activity.
    Elapsed is the whole duration; moving excludes stationary periods. A coffee stop
    makes a ride slow when they are one field, and every athlete notices on day one.
42. Average speed is distance divided by **moving** time.
43. Elevation gain is computed from a smoothed altitude series with a threshold, and
    never by summing every positive difference between consecutive raw samples.
    Summing raw differences reports thousands of metres of climbing that did not
    happen, and a flat route reports a mountain.
44. Two recordings of the same route by different devices report elevation gain
    within a small tolerance of each other, and a flat route reports at or near zero
    rather than several hundred metres.
45. Distance between coordinates is computed on a spheroid. Euclidean distance on
    latitude and longitude under-reports by roughly the cosine of the latitude, which
    in northern Europe is about a fifth of the answer.
46. Pace is inverse speed and the two are different quantity types with different
    formatting and different aggregation. An average pace is computed by averaging
    speed and inverting, never by averaging pace values: a run of one kilometre at
    four minutes and one kilometre at six minutes averages five minutes, being two
    kilometres in ten minutes, not the arithmetic mean of two pace strings.
47. Polylines are stored at several simplification levels, and the level is chosen by
    the zoom the surface needs. The feed reads the coarsest and fetches no stream at
    all.
48. Simplification preserves shape within a stated tolerance and never moves an
    endpoint.
49. Stored and returned coordinates are bounded at six decimal places. Beyond that is
    sensor noise, and it also helps identify a person.

### Segments and matching

A segment is a named stretch of road or trail, defined by a geometry with an activity
type, created by an athlete from a portion of their own activity. Any later activity
that traverses it produces an effort, which is timed and ranked.

50. **A segment match is a curve-similarity test, not a proximity test.** This is the
    single most consequential rule in the brief. Checking whether an activity passed
    near the segment's start point and near its end point produces false efforts for
    an athlete who rode past both ends by a different route, misses efforts when
    positional error puts a start point tens of metres off, credits efforts ridden in
    the wrong direction, and takes times from the nearest sample rather than the
    actual crossing.
51. Candidate segments are retrieved by a spatial index over the activity's bounding
    box and narrowed by each segment's own bounding box. Matching one activity
    against the library is never a scan; the candidate set is tens, not the whole
    library.
52. The index is over segment geometry rather than over start points. A segment whose
    start lies inside the activity's box may still not be traversed, and one whose
    start lies outside it may be irrelevant for a different reason.
53. For each candidate, the activity's polyline is tested for a sub-path that follows
    the segment's geometry within a tolerance, **in order and in the correct
    direction**.
54. The tolerance is a corridor width rather than a point radius, and it accounts for
    road width and typical positional error. A traverse carrying `25` metres of
    lateral drift is a match.
55. Effort start and end times are **interpolated between samples**, never snapped to
    the nearest one. At a `3` second sample rate, snapping introduces up to `3`
    seconds of error, and on a forty-second sprint segment that decides the
    leaderboard. This is the difference between a leaderboard athletes trust and one
    they do not.
56. An activity that traverses a segment several times produces several efforts.
57. A partial traversal produces no effort.
58. Matching is asynchronous and the activity exists before it finishes. The activity
    and its summary are visible immediately; efforts appear as they are computed.
59. While matching is running the interface says matching is in progress. **Showing
    zero segments while matching is still running is a defect**, because the athlete
    reads it as a fact about their ride.
60. Matching is idempotent and re-runnable, and a re-run replaces that activity's
    efforts atomically rather than duplicating them.
61. A segment's creator, or moderation, may rename it, mark it hazardous, edit its
    geometry or delete it.
62. Renaming a segment recomputes nothing.
63. Marking a segment hazardous suppresses its leaderboard and retains its efforts.
64. **Editing a segment's geometry recomputes every effort on it**, because those
    times were measured against the old geometry. A geometry edit that silently keeps
    the old efforts produces a leaderboard whose times were measured over different
    distances. No effort carrying a superseded geometry version stays ranked.
65. Deleting a segment follows one stated policy: its efforts are retained and
    detached, or they are removed. Pick one and apply it everywhere.
66. `activity.type` is not cosmetic. It drives which streams are expected, which
    derived metrics are computed, which segments are eligible for matching, which
    leaderboards an effort may enter, how the summary is formatted, and which
    achievements exist.
67. A run and a ride over the same road are not comparable and never share a
    leaderboard.
68. **Changing an activity's type re-runs segment matching, invalidates its efforts
    and achievements, and recomputes every affected leaderboard.** An activity
    uploaded as a run and corrected to a ride leaves no effort on any running
    leaderboard afterwards. A build that treats type as a label on a card lets a ride
    enter a running leaderboard the moment somebody fixes a mis-detected type.

### Leaderboards, efforts and achievements

69. A leaderboard is a ranking of efforts on one segment, filtered and scoped. Every
    scope is a different query and all of them are supported: all time across all
    athletes, date-bounded to this year, this month or today, social across the
    athletes a viewer follows, by club, by age group and weight class where the
    athlete has supplied them, and by sex where supplied.
70. One effort per athlete per leaderboard, being their best, except on a leaderboard
    that explicitly ranks every effort.
71. Ranking is on **elapsed** time for the effort, not moving time. Nobody gets to
    pause on a segment.
72. Ties break deterministically and stably, by effort timestamp, earliest first.
73. A flagged effort is excluded from a leaderboard rather than deleted, and it stays
    visible on its own activity.
74. **Ranks are computed over the set the viewer can see, and the ranks the viewer
    reads are contiguous from one.** An effort excluded because its athlete is hidden
    from this viewer consumes no rank number. If a private athlete holds third place,
    a viewer who cannot see them reads first, second, third, fourth with that athlete
    absent, never first, second, fourth, fifth. The gap is the leak: it tells the
    viewer a hidden athlete exists and exactly where they stand.
75. The row count and any total a viewer is shown counts only the rows that viewer
    can see, for the same reason.
76. Because ranks are per-viewer, a leaderboard cannot be one cached list. That single
    requirement rules out the obvious implementation, and the build must be honest
    about it from the start.
77. The leaderboard is a projection and is recomputed on effort insertion, on
    flagging, on a privacy change and on a segment geometry edit.
78. Achievements are computed at effort insertion. The kinds are an overall top-three
    place, a personal record on that segment, and a personal record over a distance
    class.
79. **An achievement is a historical fact, not a live query.** When an athlete is
    knocked off the podium a year later, the record that they held it survives. Each
    achievement stores the date it was earned and the date it was superseded, and the
    activity's own page still reports what it earned on the day. Recomputing the medal
    from the current standings rewrites the athlete's own history, which people find
    genuinely upsetting.
80. A time-windowed achievement, such as a frequency or local-legend award, expires
    rather than standing forever.
81. A best effort over a distance class is a **sliding window over the distance
    stream**, found by a two-pointer scan: the pair of indices whose distance
    difference is at least the class and whose time difference is minimal. Measuring
    each successive five kilometres from the start misses the actual fastest five
    kilometres in almost every case. An activity whose fastest five kilometres begins
    at `3200` metres reports that window.
82. An effort may be flagged as not genuine: a ride recorded in a car, a run recorded
    on a bike, a device error producing an impossible speed. Automatic detection flags
    an implausible effort for review using speed, acceleration and activity-type
    plausibility.
83. An athlete flagging another athlete's effort is filing a report, not performing a
    removal.
84. Every flag and its disposition is recorded with a reason, and a flagged effort is
    appealable.
85. Leaderboards without integrity handling become worthless quickly. One
    car-assisted effort sitting at the top of a popular segment removes the point of
    the whole leaderboard for everybody below it.

### The feed

86. The following feed lists activities from the athletes a viewer follows and the
    clubs they have joined, newest activity start time first.
87. **Fan-out is hybrid.** Neither approach alone works. Pushing every activity into
    every follower's feed at upload is fast to read and catastrophic for an athlete
    with a million followers, who would generate a million writes per upload.
    Assembling the feed by querying followed athletes at read time is cheap to write
    and slow for an athlete following thousands. So: fan-out on write for ordinary
    accounts, fan-out on read for accounts above a follower threshold, merged at read
    time with ordering preserved. The threshold is configurable. This decision
    determines whether the product survives a popular athlete joining and it cannot be
    retrofitted cheaply, because it changes how feeds are stored.
88. Visibility is applied at the moment of the read, not only at the moment of the
    write. A feed row written when an activity was public is not returned after that
    activity is made `followers` or `only_you`, or after a block appears.
89. Feed items are not only activities. Club posts, challenge completions and
    achievements appear too.
90. **Grouping matters.** When several athletes ride together, their near-identical
    activities appear as one grouped item naming all of them, not as one card each.
    Grouping is detected by overlapping time and route among athletes who follow each
    other, and it is computed at read time.
91. The feed is **cursor-paginated on a stable sort key**. Offset pagination on a list
    that gains items while it is being read skips items and repeats items, and on an
    infinite scroll the reader never learns what they missed. Loading one page,
    having a followed athlete upload, then loading the next page yields no missing row
    and no repeated row.
92. A feed page fetches no stream. It reads summaries and the coarsest pre-simplified
    polyline. A page of `30` items that renders its route pictures from position
    streams fetches millions of points and makes the product unusable on the second
    screen.
93. Kudos are one per athlete per activity, toggleable and counted. Giving kudos
    twice does not count twice.
94. Comments carry an author and a time, support a mention, and are deletable by their
    author or by the activity's owner.
95. **Kudos notifications are batched.** An athlete receiving fifty kudos on one
    activity inside the configured window gets one notification carrying a count, not
    fifty notifications. Fifty notifications for one popular ride is how athletes turn
    notifications off and never come back.

### Privacy, visibility and safety

This is the section where a mistake hurts somebody rather than annoying them.

96. Every activity carries a visibility of `everyone`, `followers` or `only_you`.
    `everyone` is readable by a logged-out visitor; `followers` by accepted followers
    only; `only_you` by the athlete alone.
97. Each athlete carries a default visibility applied to new activities, and a
    separate control for whether the profile itself is discoverable.
98. **Visibility is enforced at every read path, and there are more of them than a
    build expects**: the feed, the profile, the activity page, segment leaderboards,
    club feeds, challenge standings, search, the public API and aggregate views.
99. An athlete defines a privacy zone around a place such as home or work, and the
    start and end of any activity inside it are hidden.
100. **The stored polyline is truncated, not merely hidden at render time.** A route
     that is drawn short but returned whole by an endpoint is not protected.
101. Truncation removes samples from **all** streams, not just position. A heart-rate
     trace that starts before the visible route reveals the duration that was removed.
102. The reported distance and time are those of the **full** activity, and the
     interface states that the map is partial. Otherwise the athlete's own numbers are
     wrong, which is a different harm.
103. **The truncation point is randomised within the zone rather than placed at its
     boundary.** Thirty activities all stopping exactly on a circle describe that
     circle, and a circle gives up its centre to anybody who can draw one. Generated
     from one home, the truncation points must not describe a circle.
104. **Segment efforts that begin or end inside a zone are suppressed.** If the route
     is hidden but the athlete's efforts still show them sprinting up the same road
     two streets from home every morning, the hiding achieved nothing. Privacy zones
     are defeated by aggregation rather than by inspection, and the build has to reason
     about the aggregate.
105. A privacy zone is returned by no read path, to anyone, ever.
106. Aggregate views such as a heatmap are built from many athletes' activities and a
     cell contributes only above a minimum distinct-athlete threshold. A heatmap built
     without one reveals an individual's routine in a sparsely populated area, and
     products of this kind have caused real harm that way. The threshold is the
     control, not a tuning parameter.
107. An activity with any non-public visibility is excluded from an aggregate
     entirely, rather than anonymised into it.
108. A privacy-zone-truncated portion of a track is excluded from every aggregate.
109. An athlete can opt out of aggregates independently of their activity visibility.
110. An athlete can export everything they have: activities, streams, efforts,
     achievements, kudos, comments, clubs and routes.
111. An athlete can delete their account. Deletion removes their activities, streams,
     efforts and photographs, recomputes the leaderboards those efforts were on, and
     rebuilds aggregates without them.
112. Kudos and comments the deleted athlete left on other athletes' activities are
     anonymised rather than removed, or the other athletes' pages develop holes.

### Clubs, challenges and routes

113. A club carries a name, a sport type, a description, a roster and a club feed.
     Membership is many-to-many and carries a role of `member` or `admin`.
114. Joining and leaving a club are both available, and a club's feed shows only the
     activities of its members that the viewer is permitted to see.
115. A challenge carries a metric of distance, elevation or activity count, a target,
     an activity type and a date window. An athlete enters it and their progress
     accumulates from their qualifying activities.
116. A challenge counts an activity by its **local** date at its start location, so an
     activity that crosses midnight counts on the day it started and an activity
     recorded abroad counts on the day it was recorded there.
117. Challenge standings respect visibility and blocking exactly as leaderboards do,
     including the contiguity rule.
118. The route builder produces a saved route with a geometry, a derived distance and
     a derived elevation gain, computed by the same code as an activity's, and it is a
     subscriber capability.
119. The heatmap renders aggregate popularity under the distinct-athlete threshold and
     is a subscriber capability.

### The subscription tier

120. **Every gated capability is gated at the data layer.** A route builder, a
     heatmap, a best-effort analysis or a demographic leaderboard filter hidden by a
     client-side check is available to anybody who looks, and on this product what
     they would be looking at is where people go.
121. Calling each gated endpoint directly, with a free athlete's valid session and no
     interface involved, is refused. Calling the same endpoint with a subscriber's
     session succeeds.
122. The plan surface states the price with its currency and its period, the renewal
     terms, and the route to cancel, all before purchase.
123. A gift purchase completes **logged out**. A gift is usually bought by somebody
     who does not use the product for somebody who does, and requiring the buyer to
     create an account first asks a non-customer to become a customer before they are
     allowed to give you money. The gift flow collects a recipient address, a plan and
     a duration, and issues a redemption code.

### The public surface and its errors

124. The feature, map, challenge and subscription content routes each describe a
     capability the product actually has, so each is a claim the rest of this brief
     has to deliver.
125. The not-found view carries its heading, its body denying the dead-end reading,
     and five options **ranked by likelihood**, beginning with the visitor's own typo
     and ending with a human. Leading with support is the usual arrangement and it is
     backwards: support is the least likely to help and the most expensive for
     everybody.
126. The server-error view is a **different page** from the not-found view. A server
     error is not a missing page, it carries different copy, and it must not tell the
     visitor to check their address, because their address is fine.
127. Every route carries its own title and description and no two routes share them.
128. A public activity, segment or profile page is rendered on the server, so a shared
     link opens with its content already in the document and is indexable. Each one
     declares a social preview title and a preview image, and the preview image
     resolves rather than pointing at nothing.
129. No link on any route leads to a missing page, and every internal link resolves.

### The public interface for other applications

130. An athlete may authorise another application with separately grantable scopes:
     read activity, write activity, read profile.
131. The athlete sees every connected application and revokes each one individually.
132. **An application's access to an activity is bounded by that activity's own
     visibility, not by whose account authorised it.** An application authorised by
     one athlete must not receive another athlete's followers-only activity merely
     because the authorising athlete can see it.
133. Webhooks are signed, delivered at least once, and carry the state of the resource
     rather than only its identifier.
134. Rate limits apply per application and per athlete, are documented, and state when
     they reset.
135. Upload, kudos, follow and join are idempotent, each by a key or by its own
     nature, so a retried write produces no second effect.
## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | the signup landing, three panels | none |
| `/login` | log in | none |
| `/signup` | create an account | none |
| `/features` | what the product does | none |
| `/maps` | route planning and the heatmap, described | none |
| `/challenges` | the public challenge index | none |
| `/subscription` | the plan comparison | none |
| `/gift` | buy a subscription for somebody else | none |
| `/stories` | community stories | none |
| `/help` | support | none |
| `/search` | find an activity, an athlete or a club | none |
| `/feed` | the following feed | athlete |
| `/upload` | the upload wizard | athlete |
| `/activities/<id>` | one activity, its route and its statistics | none when `everyone` |
| `/activities/<id>/edit` | rename, retype, change visibility | the owner |
| `/athletes/<id>` | an athlete profile | none when discoverable |
| `/athletes/<id>/following` | who they follow | none when discoverable |
| `/athletes/<id>/followers` | who follows them | none when discoverable |
| `/athletes/<id>/best-efforts` | best efforts by distance class | `subscriber` |
| `/segments` | segment explore | none |
| `/segments/<id>` | one segment and its leaderboard | none |
| `/clubs` | the club index | none |
| `/clubs/<slug>` | one club, its roster and its feed | none |
| `/challenges/<slug>` | one challenge and its standings | none |
| `/routes` | saved routes | `subscriber` |
| `/routes/new` | the route builder | `subscriber` |
| `/heatmap` | aggregate popularity | `subscriber` |
| `/settings` | account, units, notifications, sessions | athlete |
| `/settings/privacy` | visibility defaults, privacy zones, blocks | athlete |
| `/settings/applications` | connected applications | athlete |
| `/settings/export` | data export and account deletion | athlete |
| `/500` | the server-error view | none |
| `*` | the not-found view | none |

Navigation is a **single top bar carried on every surface**, with one item order and
one call to action: five content items, the first carrying a disclosure, and a right
cluster holding log-in and join. Two headers with different items on different routes
is a defect, not a variation.

### Entry and redirects

- An unauthenticated request for `/feed`, `/upload`, `/routes`, `/heatmap` or any
  `/settings` route redirects to `/login`, and a successful sign-in lands on the route
  that was asked for.
- A successful sign-in with no pending destination lands on `/feed`.
- Signing out returns to `/`, and any later athlete-only request redirects to
  `/login`.
- A logged-in visitor arriving at `/` or `/signup` is redirected to `/feed`.
- `/gift` is reachable and completable while logged out, and never redirects to
  `/login`.
- A request for an activity, a profile, a club or a challenge the viewer may not see
  returns the not-found view rather than a refusal.
- A `free` athlete requesting `/routes`, `/routes/new`, `/heatmap` or a best-efforts
  page is shown the subscription offer and stays signed in.

### Journeys

1. **A visitor signs up.** Open `/`. Three panels: a generated atmospheric panel left,
   the signup card in a white column centre, a generated panel with a device composite
   right. The card argues community-powered motivation, offers two federated controls
   first and the email control last with the emphasis on email, and carries a legal
   line. Sign up with an address, a password and a display name. Land on `/feed`, which
   is empty and says so with a next action.
2. **An athlete reads the feed.** Sign in as `athlete2@example.com` with
   `deku-demo-pw-2026`. `/feed` lists the activities of the athletes Sena Okafor
   follows, newest first, `30` to a page. Each card carries the athlete, the activity
   name, its type in text, a route picture drawn from the coarse polyline, and a
   statistic block of distance, moving time and elevation gain. Several athletes who
   rode together appear as one grouped card naming all of them. Reaching the end fetches
   the next page by cursor.
3. **Kudos and comments.** Give kudos on a card; the count rises by one. Press again;
   it falls back. Press a third time; it rises again and stops there. Leave a comment
   and it appears with its author and time.
4. **The leaderboard, and the privacy result.** Open `/segments`, then `Ridgeway
   Climb`. Signed in as Sena Okafor, who is not an accepted follower of Dorian Vance,
   the leaderboard reads first Rowan Ellery, second Sena Okafor, third Mira Halloran,
   fourth Kit Bramwell. The ranks run one, two, three, four with no gap, the count
   reads four, and Dorian Vance appears nowhere and is hinted at nowhere. Signed in as
   an athlete Dorian has accepted, the same board reads one through five with Dorian
   third.
5. **The block.** Sign in as `athlete4@example.com`, Mira Halloran, blocked by Rowan
   Ellery. Rowan's profile is not found. Rowan's activities are not found. Rowan is
   absent from the leaderboard Mira is shown, from the `Dawn Patrol` roster, from the
   `April Ascent` standings, from a search for the name, and from the kudos list of an
   activity they both reacted to. Every one is a separate read path and every one
   refuses.
6. **The upload, which is the transaction.** Sign in as `athlete@example.com` and open
   `/upload`. The wizard runs in ordered steps: choose the file, confirm the type and
   the name, set the visibility, submit. Submitting returns an upload identifier. The
   wizard shows `received`, then `parsing`, then `matching`, then `ready`. The activity
   is open-able as soon as its summary exists, while matching still runs, and its
   segment panel says matching is in progress rather than saying none. When matching
   finishes, an effort exists for every segment the track traversed in order and in
   direction, the leaderboards those efforts entered are correct, any achievement is
   stored with its earned date, and the activity is in the feeds of Sena Okafor and
   Kit Bramwell.
7. **The duplicate.** Upload the same file again. The upload reaches
   `duplicate_suspected` rather than `ready`. No second activity exists. No second
   effort exists on any segment. Both candidates are shown and one is chosen; the
   discarded one's efforts are gone.
8. **Retyping.** Open `/activities/<id>/edit` on an activity uploaded as `run` and
   change its type to `ride`. Every effort on a running segment is gone, efforts on
   riding segments have appeared, both leaderboards are correct, and no achievement
   from the old type survives.
9. **The privacy zone.** As Rowan Ellery, whose zone has a radius of `400` metres,
   open a public activity that started inside it from a logged-out browser. The drawn
   route begins away from the zone, the page says the map is partial, and the reported
   distance and time are those of the whole activity. No stream returned reaches past
   the drawn route. No effort on that activity begins or ends inside the zone. No
   endpoint returns the zone.
10. **The subscription gate.** As `athlete@example.com` on `free`, call the route-save
    endpoint, the heatmap endpoint, the best-efforts endpoint and the demographic
    leaderboard filter directly with a valid session. Each is refused. As
    `athlete5@example.com` on `subscriber`, each succeeds.
11. **Units.** Kit Bramwell prefers imperial and reads Rowan's ride in miles. Sena
    Okafor prefers metric and reads the same ride in kilometres. The stored value did
    not change and the recorder does not decide what either viewer reads.
12. **The gift.** From a logged-out browser, open the gift link in the footer, choose a
    plan and a duration, name a recipient, and complete. No sign-in was asked for and a
    redemption code was issued.

### States

Every list surface carries four states: loading, empty with a next action, populated,
and failed with a retry that does not lose the query or the filters.

The upload state machine is the one shown directly: `received` to `parsing` to
`matching` to `ready`, with `failed` and `duplicate_suspected` terminal and each
carrying a reason. `failed` offers a retry that re-processes the retained file.

A follow is three states, not two: not following, requested, following. Requested
grants nothing and says so.

## UI/UX notes

The direction is set by the supplied companion document, whose measured token layer
governs. Colour below is written as family, tone and shade because the builder chooses
the value; type is written exactly because it is an identity the builder cannot guess.

### The character, in four decisions

**One saturated hue.** A mid, vivid orange is the only saturated colour in the core
palette. It sits at the third step of a nine-step ramp rather than at the top, with
four darker steps above it: a deep, vivid orange, a deep, soft orange and a near-black,
muted orange among them. Lighter steps run out through two light, vivid oranges, a
light, soft orange and a near-white, muted orange. The ramp exists so the brand hue can
be used as text on a pale ground by stepping down rather than by darkening it by eye,
and the brand hue itself is not readable as body text on white.

**A palette that names product concepts.** Three named podium colours, for first,
second and third place. First is a mid, vivid orange read as gold. Second is a light
cool neutral rather than a plain grey, and that coolness is exactly what stops it
reading as a disabled control next to the first. Third is a mid, soft orange read as
bronze. A design system with named podium colours is a design system for a product
about ranking.

**One display family in two widths.** A standard width for prose and a condensed width
for numerals, three weights, with a true italic. The italic is load-bearing because the
wordmark is heavy italic capitals.

**One interface size.** `15px` on a `24px` line at weights `400`, `600` and `700`, and
that is nearly the whole interface. Fifteen is an unusual choice between the
conventional fourteen and sixteen, and the resulting ratio is generous for interface
text and correct for a product whose main surface is a scrolling feed of prose and
numbers. Weight `600` is a deliberate third step between body and emphasis rather than
a rounding.

### Palette by role

| Role | Colour |
|---|---|
| Brand, primary action, the live route line | mid, vivid orange |
| Brand as body text on a pale ground | deep, vivid orange, stepped down the ramp |
| Ink | near-black neutral |
| Page ground | near-white neutral |
| Card and panel grounds | two further near-white neutrals, one warmer |
| Dividers and disabled ink | light neutral |
| First place | mid, vivid orange |
| Second place | light cool neutral |
| Third place | mid, soft orange |
| Highlight and warning | mid, vivid amber |
| Accent | mid, vivid teal |
| Quiet secondary ground | a warm near-white neutral |
| Dark panels and the log-in card | near-black cool neutral |
| The alternative dark panel, bluer | a second near-black cool neutral |
| Deep accent, used sparingly | deep, soft red |

**The three podium colours are reserved for achievement and rank and are used for
nothing else.** The obvious temptation is to reach for the first-place colour as a
general warning or highlight, and doing so destroys the one signal this product most
needs to be unambiguous. A warning uses the amber. Third-party platform marks carry
their own colours and are the only colours in the system that are not the product's.

### Ramps, spacing, radius, borders, layering

Nine-step ramps per family: orange, blue, green, neutral and pink. The neutral ramp
carries an extra half-step between its fourth and fifth, which is the tell of a ramp
found to have a gap in practice and given one.

The spacing ladder is named rather than numbered and expressed in `rem`. It is
deliberately not a doubling series: it is dense at the small end and sparse at the
large end, which is right for an interface of dense data rows and generous section
breaks. Keep that shape rather than regularising it, and ship one token per value
rather than duplicates.

Radius runs none, extra-small, small, medium, large and extra-large. Controls take the
small step.

Ship four border styles: none, solid, dashed and dotted. A nine-style ladder carrying
groove, ridge, inset and outset is boilerplate generated from the property's full value
set rather than design, and those four have no place in a modern interface. Border
widths run a numbered ladder plus named thin, medium and thick. Dividers run four sizes
in three variants.

Layering keeps a disciplined five-band scale. A layer value near the maximum
thirty-two-bit integer belongs to a consent vendor; do not adopt it.

An effects catalogue sits alongside, holding shadow and likewise transform presets, and it
follows the same rule as everything else here: one token per value.

Four token pairs in the measured layer are exact duplicates and only one of each ships.

| Pair | Keep |
|---|---|
| `--space-zero` and `--space-none`, both zero | one token |
| `--space-2xs` and `--space-base`, both the base step | one token, and it is the named base |
| `--border-radius-xs` and `--border-radius-base`, both the smallest step | one token |
| the brand orange declared as both `--color-coreo3` and `--color-extendedorangeo3` | one token, and it is the core one |

A colour declared twice under two names is the same defect as a spacing step declared
twice: two places to change and one of them will be missed.

### Typography

- Interface and body: a freely licensed grotesque at `400`, `600` and `700`, with the
  stack `"Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.
- Numerals in tables, leaderboards and statistic blocks: a condensed width **with
  tabular figures**, stack `"Roboto Condensed", "Inter", sans-serif`.

Tabular figures are not optional. Statistics align in columns, proportional digits
make a leaderboard unreadable, and numbers that change width as they change value make
the product look amateur. The condensed width is for numerals in constrained columns
and is never used for prose.

Sizes: `15px` on `24px` for the interface in three weights; `12px` on `14.4px` for the
smallest labels; `13px` on `18.85px` and `14px` on `18px` for secondary metadata;
`34px` on `41px` for a page heading. Ship three weights, not six, and subset the faces.
Fonts load with a swap strategy.

### Iconography

The mark is an elevation profile: two chevron forms, one nested inside and below the
other, read as an ascending trace, taller than wide, filled in the brand orange with no
stroke. For a product whose core artefact is a recorded route with a climb in it, the
logo is a picture of the data, and the product's name follows the same idea.

The disclosure chevron is a filled outline rather than a stroked line, so it holds its
weight at small sizes without a vector-effect declaration, and its apex is a rounded
join rather than a mitre.

The kudos glyph is a hand with an extended thumb and it renders one step below the text
beside it. An icon set at exactly the text size reads as too large; one step down reads
as level, and that rule governs every glyph paired with text.

The set to draw: activity-type glyphs for run, ride, swim, hike, ski and walk, plus map,
segment, trophy, crown, comment, share, lock, globe, group, calendar, chart, filter, a
chevron in four rotations, close and search. The activity-type glyphs are a closed,
extensible set keyed to the activity-type values, and a type with no glyph falls back to
a generic one rather than rendering nothing. Federated identity marks and platform marks
are third-party trademarks obtained under their own guidelines and never redrawn.

### Motion

The loading indicator is not a plain rotation. It has five stops, accelerating and then
easing, and near its end it has turned nearly two full revolutions before slowing. A
plain single-turn spinner reads as mechanical; this one reads as a wheel spun by hand,
which on a product about riding is a deliberate joke worth keeping.

Easing is shipped as named tokens rather than as loose curves. A system that names
fifteen spacing steps while leaving its curves unnamed accumulates one more that nobody
can identify as wrong.

Under a reduced-motion preference the indicator becomes a static or determinate one,
feed items appear without an entrance animation, map transitions cut rather than fly,
and an animated route replay is replaced by a static line with a play control. That last
is specific to this product and is not negotiable: an animated replay of a route on a
map is exactly the movement that makes some people ill, and it must never autoplay.

### Responsive, print and forced colours

Four breakpoints chosen for this product and expressed in `rem`, consistent with the
spacing ladder. Do not inherit a legacy grid framework's breakpoints. Write them
mobile-first, as `min-width` queries in one spelling rather than two, and do not mix
`min-width` and `max-width` families in the same ladder. Twenty media queries mixing the
two, which is what the measured reference carries, produce overlap defects nobody can
reproduce.

At a narrow viewport nothing overflows sideways and every navigation target stays
reachable: the feed, the activity page, the segment leaderboard and the upload wizard
each reflow into one column rather than scrolling the page horizontally.

**Print is required and is product-specific.** An activity page prints usefully: the
route, the summary statistics and the splits, without the feed chrome. Athletes print
activities for coaches and for race records.

**Forced colours are load-bearing here.** A product built on coloured route lines and
coloured podium badges loses its entire information channel when colour is stripped, so
a route line carries a non-colour distinction such as a dash pattern or a marker, and a
podium place is stated in text as well as coloured.

### Accessibility

One `h1` per route. A skip link. Landmarks for banner, navigation, main and contentinfo.
The consent bar is keyboard-operable and its reject path is one action. Federated
controls name their provider in their accessible name rather than saying sign-in alone.
Every statistic is announced with its unit.

| Surface | Requirement |
|---|---|
| The route map | never the only representation; the same route exists as text giving distance, elevation and location |
| The elevation chart | keyboard-navigable with values announced, or paired with a data table |
| Achievement rank | announced as a rank, never carried by podium colour alone |
| Segment leaderboards | a real table with headers, not a styled list |
| Kudos | an accessible name saying what it is, not a bare glyph |
| Activity type | in text; the glyph is decorative |

**The map requirement is the load-bearing one.** A screen-reader user must be able to
learn what an activity was without the map. A map that is the only carrier of the route
excludes them from the product entirely.

Contrast: the nine-step ramps exist so a darker step is always available. Two pairs need
checking. The brand orange on white fails at body size and steps down the ramp for text.
The second-place colour on a light ground is marginal, and it matters because it carries
a rank.
## Technical requirements

### Stack

Server-rendered routes with hydrated interactive regions. Each route arrives as HTML
from the server and only the parts that need behaviour hydrate in the browser. A shared
activity link, a segment page and a public profile therefore open with their content
already in the document, which is what makes them findable.

Run one interface framework, not two. A page that carries a modern framework alongside a
twelve-year-old one and its helper library makes every visitor download both, and it is
also how a product ends up with two different headers on two different routes.

### Services

| Slot | Provider | What the app reads |
|---|---|---|
| Database | PostgreSQL | `DATABASE_URL`, also exposed as `DB_URL` with the same value |
| Object store | MinIO, an S3-compatible store | `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` |
| App | - | `APP_PUBLIC_URL`, `APP_PUBLIC_PORT` |
| Feed | - | `FANOUT_FOLLOWER_THRESHOLD` |
| Notifications | - | `KUDOS_BATCH_WINDOW_SEC` |

Both backing services are already running and reachable at those variables. Do not
download, install, compile or start a copy of either.

### Object storage

The object store is where bytes live. Nothing is written to the container filesystem and
nothing is stored as a database blob.

Two prefixes and no others. The raw upload goes to
`uploads/{athlete_id}/{upload_id}/{sha256_of_bytes}.{ext}`  -  for athlete `7`, upload
`d41f`, a file whose bytes hash to `a3f1c8...` and whose name ended `.gpx`, that is
`uploads/7/d41f/a3f1c8....gpx`. Decoded series go to
`streams/{activity_id}/{stream_type}.json`.

The key is derived from the content, so identical bytes resolve to the same key and a
re-upload writes nothing new. The object read back from that key hashes to the same
value the application recorded: no re-encoding, no normalisation, no stripping of the
raw file.

Protected content is reached one way and one way only: an authenticated streaming
endpoint through the application, which applies the same visibility rules as every other
read path before it returns a byte. The bucket is never made public and no object URL is
handed to a browser that could be reused by somebody the activity is not visible to.

### Environment-injected behaviour

`KUDOS_BATCH_WINDOW_SEC` is the window inside which repeated kudos on one activity
collect into a single notification. `FANOUT_FOLLOWER_THRESHOLD` is the follower count
above which an athlete's activities stop being written into follower feed rows and are
merged at read time instead. Both are read from the environment on every use. A
hardcoded literal for either is a contract violation: the seams exist so the behaviour
can be exercised at a different scale without the application knowing.

### Asynchronous processing

Upload parsing, deduplication, metric derivation, segment matching, effort and
achievement computation, feed fan-out and leaderboard projection all run outside the
request that triggered them. There is no queue service in this environment; the work is
driven from the application's own process against rows it owns.

Every stage is idempotent. Running a stage twice produces the same result rather than a
second one, and a re-run of matching for one activity replaces that activity's efforts
in one step rather than adding to them.

An upload returns its identifier immediately and is polled. The activity becomes
readable as soon as its summary exists, before matching has finished.

### Units and quantities

Store in canonical SI: metres, seconds, metres per second, watts, degrees. Convert at
the presentation boundary and nowhere else. Mixed units in storage makes every aggregate
wrong and is expensive to unwind later.

**The viewer's preference governs, never the recorder's.** Pace and speed are separate
quantity types. Elevation, distance and temperature carry independent preferences,
because a runner may well want kilometres and feet.

### Time and place

Store the start instant in UTC. Store the **timezone identifier of the start location**,
resolved from the coordinates, not the athlete's home timezone. Store the derived local
date, because activities in March means local March.

An activity that crosses midnight belongs to its start date. An activity that crosses a
timezone boundary keeps its start timezone. Streams are offsets from the start instant,
never absolute timestamps.

An athlete who lives in one country and rides in another recorded an activity local to
where they rode. Formatting it in their home timezone shows a seven o'clock ride at six
and puts it on the wrong day for any challenge counting daily.

### Geometry

Distances are computed on a spheroid. Spatial queries are answered by a spatial index
over segment geometry rather than by a bounding-box scan written in application code.

### Idempotency

Idempotency is a property of every retryable write in this product. An upload carries the
hash of its own bytes, a kudos is naturally idempotent because one athlete gives at most
one, a follow and a club join are the same, and segment matching is re-runnable and
replaces in one step. A retried write therefore produces no second effect, which is what
makes the asynchronous stages above safe to repeat.

### The site's own backend

The public half of the site needs very little of its own: content for the feature and map
routes, the signup and log-in flows, the subscription surface, the gift flow that
completes logged out, and server-rendered public activity and segment pages so a shared
link is findable. Everything else is the platform behind the login, and that is where the
weight of this brief sits.

No mapping vendor is contacted for tiles, for geocoding or for routing. A route surface
renders a plain ground with the line drawn from the application's own coordinates, and
every geometry and matching requirement in this brief is satisfiable that way.

### Determinism and versioning

Every derived quantity records the version of the algorithm that produced it.
Recomputation is possible, is a deliberate operation, and states its scope. Two runs of
the same algorithm over the same streams produce identical results.

### Performance

| Surface | Budget |
|---|---|
| First contentful paint, the signup landing | under one and a half seconds |
| Total transferred, the signup landing | under nine hundred kilobytes |
| Script before first paint | under one hundred and fifty kilobytes compressed |
| Feed first render | under two seconds |
| An activity page with its route and charts | under three seconds |
| Route pan and zoom | one frame at sixty per second, sustained |
| A stream fetch for a four-hour activity | under eight hundred milliseconds at the ninety-fifth percentile |

The error views ship no application script. An error page is a heading, a drawing and
five links, and the condition it is reporting may be the application failing to start.
Map surfaces are never on the critical path. Streams are fetched separately from the
activity and progressively.

### Logging

Every log record is structured rather than prose and carries the athlete identifier
where a session exists, the activity or upload identifier where one applies, and a
correlation identifier that survives from the inbound request through every processing
stage. No coordinate pair, no privacy-zone centre, no access token and no password
appears in a log record.

### Health

`GET /api/health` returns `200` once the app is ready, the database answers and the
bucket is reachable.

## Data model

All timestamps are UTC. Money is integer minor units in `usd`. Measured quantities are
canonical SI.

### Entities

**athlete** - an account. Carries a display name, a plan, a unit preference, an
elevation preference, a timezone, an optional weight, an optional functional threshold
power, an optional maximum heart rate, a default visibility, whether the profile is
discoverable, and whether the athlete contributes to aggregates.

**athlete identity** - a federated identity linked to an athlete: a provider, the
provider's subject, and the verified address it returned. A provider and subject pair
identifies at most one athlete, and a verified address already belonging to an athlete
links to that athlete rather than producing another.

**athlete setting history** - a field, a value and the date it took effect. A
leaderboard scoped by weight class ranks an effort by what the athlete weighed on the
day of the effort, which is what this record is for.

**follow** - a follower, a followee and a state of `pending`, `accepted` or `blocked`.
At most one follow exists between one follower and one followee.

**block** - a blocker and a blocked athlete. At most one exists per ordered pair.

**upload** - an athlete, a source of `device_file`, `manual` or `partner`, the object
key of the retained raw file, the original filename, the hash of its bytes, its size, a
status, an error code and detail where it failed, the file's own identifier where the
format provided one, the activity it produced, and the activity it duplicates where it
is a suspected duplicate. One athlete never holds two uploads with the same byte hash.

**activity** - an athlete, the upload it came from, a type, a name, a description, a
visibility, the start instant in UTC, the start timezone identifier, the derived local
start date, the device name, whether it was entered by hand, whether it has streams,
whether its route was truncated by a privacy zone, and any parse warning.

**activity summary** - distance, moving time, elapsed time, elevation gain, average and
maximum speed, average and maximum heart rate, the coverage the heart-rate average was
computed over, average cadence, average power, whether power was measured or estimated,
and the version of the algorithm that produced them.

**stream** - an activity, a type, a sample rate, an encoding, the object key of the
series, its point count, whether it was measured or derived, and its algorithm version.
An activity holds at most one stream of each type.

**polyline** - an activity, a simplification level, the encoded line and the tolerance it
was simplified within. One per level.

**segment** - a name, an activity type, a geometry, a bounding box, a distance, an
elevation gain, an average grade, a hazardous flag, a private flag, its creator, and a
geometry version that changes whenever the geometry does.

**segment effort** - a segment, an activity, an athlete, the start and end sample
indices, the interpolated start instant, an elapsed time, a moving time, a flag state of
`clear`, `flagged` or `excluded`, the geometry version it was measured against, and when
it was computed. One activity produces at most one effort per segment per traversal.

**effort flag** - an effort, a reporter, a reason, a disposition of `open`, `upheld` or
`dismissed`, and when it was raised and resolved.

**best effort** - an activity, an athlete, a distance class, the distance at which the
window began, and the elapsed time across it. One per distance class per activity.

**achievement** - an athlete, an activity, an effort, a kind of `overall_top_three`,
`segment_pr` or `distance_pr`, a rank, the date it was earned and the date it was
superseded. The row survives being superseded.

**privacy zone** - an athlete, a centre, and a radius.

**kudos** - an activity and an athlete. One athlete gives at most one kudos to one
activity.

**comment** - an activity, an athlete, a body, a time and a deletion time.

**notification** - an athlete, a kind of `kudos`, `comment`, `follow_request` or
`achievement`, the activity it concerns, the number of actors it collects, when its
window opened, the most recent actor, and when it was read.

**feed entry** - an athlete and an activity, carrying the activity's start instant so the
feed orders without a join. One per athlete per activity, written by fan-out for athletes
below the follower threshold and absent by design for athletes above it.

**club** - a name, a slug, a sport type and a description. **club member** - a club, an
athlete and a role of `member` or `admin`. One membership per athlete per club.

**challenge** - a name, a slug, a metric of `distance`, `elevation` or `activity_count`,
a target, an activity type and a date window. **challenge entry** - a challenge, an
athlete, a progress value and a completion time. One entry per athlete per challenge.

**route** - an athlete, a name, a geometry, a derived distance, a derived elevation gain
and an activity type.

**api application** - an athlete, a name, its granted scopes, the hash of its token, and
when it was created and revoked. The token value is shown once, at creation, and never
again.

**plan** and **plan feature** - the subscription surface. **gift purchase** - a buyer
address that is a string rather than an account, a recipient address, a plan, a duration,
a message, a redemption code that is unique, and who redeemed it.

**page meta** - a route path, a title, a description and whether it is indexable. One per
route.

**audit event** - an actor address, an action, a subject, a time, and the value before
and after. Append only.

### Enumerations, exact casing

- plan: `free`, `subscriber`
- unit preference: `metric`, `imperial`
- elevation preference: `metres`, `feet`
- visibility: `everyone`, `followers`, `only_you`
- activity type: `run`, `ride`, `swim`, `hike`, `ski`, `walk`
- follow state: `pending`, `accepted`, `blocked`
- upload status: `received`, `parsing`, `matching`, `ready`, `failed`,
  `duplicate_suspected`
- upload source: `device_file`, `manual`, `partner`
- stream type: `time`, `latlng`, `distance`, `altitude`, `heartrate`, `cadence`,
  `watts`, `temp`, `moving`, `grade_smooth`
- effort flag state: `clear`, `flagged`, `excluded`
- achievement kind: `overall_top_three`, `segment_pr`, `distance_pr`
- flag disposition: `open`, `upheld`, `dismissed`
- club role: `member`, `admin`
- challenge metric: `distance`, `elevation`, `activity_count`
- notification kind: `kudos`, `comment`, `follow_request`, `achievement`

### Invariants

These hold as properties of the running system, whatever the storage arrangement.

1. With a block in either direction between two athletes, no read path returns either
   athlete's content to the other.
2. The ranks a viewer reads on any leaderboard or standings run without a gap from one,
   and any count or total that viewer is shown counts only what that viewer can see.
3. An achievement is never recomputed from present standings. Being beaten records the
   superseding date and leaves the rank, the kind and the earned date untouched.
4. Elapsed time is greater than or equal to moving time on every summary, and average
   speed is distance over moving time.
5. Re-submitting bytes identical to an earlier upload by the same athlete returns the
   original upload and produces no second activity.
6. An upload that has reached `duplicate_suspected` has produced no effort anywhere.
7. Re-running matching for one activity replaces its efforts rather than adding to them,
   so the number of efforts an activity holds on a segment does not grow from a re-run
   that found the same traversals.
8. Changing an activity's type removes every effort and achievement derived under the
   old type before any effort exists under the new one.
9. No effort measured against a superseded segment geometry appears on that segment's
   leaderboard.
10. No read path returns a privacy zone, and no stream or line returned for an activity
    extends past that activity's truncated route.
11. A free athlete is refused every gated capability at the endpoint, whether or not the
    interface offered the control.
12. A feed row is never returned to an athlete for an activity whose visibility excludes
    them at the moment of the read, even where it did not when the row was written.
13. One athlete's kudos on one activity counts once however many times it is submitted.

### Seed data

Seeding is idempotent: restarting the app must not duplicate rows.

Five athletes as listed under roles, all with the password `deku-demo-pw-2026`.

**Follows:** Sena Okafor follows Rowan Ellery, accepted. Kit Bramwell follows Rowan
Ellery, accepted. Rowan Ellery follows Sena Okafor, accepted. Sena Okafor follows Dorian
Vance, `pending`, because Dorian's profile is not discoverable.

**Blocks:** Rowan Ellery blocks Mira Halloran.

**Privacy zone:** one, Rowan Ellery's, radius `400` metres.

**Segment:** `Ridgeway Climb`, type `ride`, `1800` metres long, `95` metres of gain,
matched inside a corridor tolerance of `30` metres.

**Activities:** one per athlete on `Ridgeway Climb`, giving the five-row leaderboard,
plus Rowan Ellery's reference activity `Ridgeway long loop`, type `ride`, visibility
`everyone`, whose summary reads exactly:

| Field | Value |
|---|---|
| Elapsed time | `5400` seconds |
| Moving time | `4200` seconds, the difference being a `1200` second stationary period |
| Distance | `32000` metres |
| Elevation gain | `480` metres |

**Fixture tracks**, synthesised at a `3` second sample rate so a known answer exists:

| Fixture | Shape | Required outcome |
|---|---|---|
| A flat eastward track | `10000` metres due east at latitude `55` | measures `10000` metres, not roughly half of it |
| A flat route | no altitude change beyond sensor noise | elevation gain at or below `10` metres |
| A forward traverse | follows the segment end to end | one effort |
| An endpoints-only pass | reaches both ends by another road | no effort |
| A backward traverse | follows the geometry in reverse | no effort |
| A drifting traverse | follows it with `25` metres of lateral drift | one effort |
| A partial traverse | enters and leaves partway along | no effort |
| A two-kilometre pace run | `1` km at `4:00` then `1` km at `6:00` | average pace `5:00` |
| A long run | its fastest `5` kilometres begins at `3200` metres | the best effort reports that window |

**Club:** `Dawn Patrol` at the slug `dawn-patrol`, sport `ride`, with Rowan Ellery as
`admin` and Sena Okafor and Kit Bramwell as members.

**Challenge:** `April Ascent` at the slug `april-ascent`, metric `elevation`, target
`4000` metres, type `ride`, entered by Rowan Ellery and Kit Bramwell.

**Route:** `Loch Circuit`, owned by Kit Bramwell, `24000` metres and `310` metres of
gain. Kit is the subscriber, which is why the route exists at all.

**Plans:** `Free` and `Ridgeline Premium` at the slug `ridgeline-premium`, the second
at `1200` monthly and `8000` annual, in `usd`.

**Aggregates:** a cell contributes only above `3` distinct athletes, and the seed places
one cell above that line and one below it.

**Feed:** page size `30`, with enough seeded activity across the followed athletes that a
second page exists.
## Front-end specification

Everything below is normative. Copy given in backticks is carried verbatim.

### Global chrome

**Header.** One header on every surface, one item order, one call to action. The mark
sits left, then the wordmark. Five items sit centre: `Activities` carrying a disclosure
chevron, `Features`, `Maps`, `Challenges`, `Subscription`. The right cluster carries
`Log In` as an outlined control and `Join for Free` as the filled brand control, and a
signed-in athlete sees their own avatar and menu in that position instead.

The header's shadow sits at about two and a half percent alpha, which is barely visible
and is the point: it separates the header from white content beneath it without drawing
a line. Header controls declare `will-change` narrowly, for colour only, which is the
correct declaration for a control that only ever changes colour. Declared broadly it
promotes a layer that never needed promoting.

**Footer.** Four columns headed `Features`, `Subscription`, `Support`, `Privacy`. The
gift link lives in the footer and carries its campaign parameter into the gift route.

**Consent bar.** Bottom-anchored, full width, on a dark ground, heading `This website
uses cookies`, with the controls `Accept All`, `Customize`, `Reject Non-Essential` and
`Show details`. The reject control is present, is the same size as accept, and is
reachable in one action. The bar sits below the content rather than over it and is
keyboard-operable throughout. Its brand colour comes from the same token as every other
surface, never typed in by eye somewhere else.

**Skip link.** First in the document, visible on focus.

### Modules and component architecture

Ten modules build this product, and the brief names them so nobody invents an eleventh:
the token layer; the auth card, being one component in two modes; the header; the consent
bar; the activity card; the route surface; the statistic block; the segment effort row;
the leaderboard table; and the chart drawing pace, elevation and heart rate over distance
or time. The statistic block is the module that matters most, because every other surface
is made of them.

### The signup landing

The layout is a three-panel composition at the wide width, full-bleed to the viewport
edges.

| Panel | Contents |
|---|---|
| Left, roughly a third | a generated atmospheric panel standing in for a photograph of cyclists on a road |
| Centre | the signup card on white |
| Right, roughly a third | a second generated panel standing in for runners, with a generated device and watch composite over it |

The centre is not a bordered card; it is a white column between the two panels.

| Element | Copy |
|---|---|
| Heading | `Community-Powered Motivation` |
| Body | `Track your progress and cheer each other on. Join over 100 million active people on Ridgeline for free.` |
| Existing member | `Already a Member?` then `Log In` |
| Federated, first | `Sign Up With Google` |
| Federated, second | `Sign Up With Apple` |
| Primary | `Sign Up With Email` |
| Legal | `By continuing, you are agreeing to our Terms of Service and Privacy Policy.` |

**The order is federated first and email last, with the email control carrying the brand
orange and the two federated controls outlined.** That inverts the usual hierarchy: the
branded control is the fallback and the federated ones are offered first in plain
outlines. Keep the order and the treatment. Federated signup completes at a far higher
rate on a consumer product, and putting it first while leaving the emphasis on email is a
considered compromise between conversion and not depending on two identity providers.

The legal line links both documents and the acceptance is recorded with the text shown.

### Log in

The layout repeats the signup landing's three panels with two different generated panels,
and the centre column carries a **dark card** rather than sitting on white. The heading sits on a dark
header band.

| Element | Copy |
|---|---|
| Heading | `Log In` |
| Federated, first | `Sign In With Google` |
| Federated, second | `Sign In With Apple` |
| Divider | `or` |
| Field | label `Email`, placeholder `Your Email` |
| Checkbox | `Remember me`, checked by default |
| Primary | `Log In` |
| Secondary | `Create a New Account` |
| Legal | as on the signup landing |

**The field carries a real label above a placeholder**, which is the opposite of the
placeholder-as-label pattern and is correct. Keep it.

**Remember-me is checked by default.** On a product holding location history that is
defensible on a personal device and poor on a shared one, so it is paired with a list of
live sessions in settings, each endable remotely.

### The not-found view

| Element | Copy |
|---|---|
| Heading | `Sorry, this one stays red.` |
| Body | `The page you're looking for doesn't exist, but you're not at a dead end. Here are a few options:` |
| Option 1 | `Be sure you have the right url and try again` |
| Option 2 | `Sign up or log in at Ridgeline` |
| Option 3 | `See what the community's been up to at Ridgeline Stories` |
| Option 4 | `Search for a particular activity or club` |
| Option 5 | `Get a little help from Ridgeline Support` |

`url` is lowercase in option one, as given. The five options stay in that order, ranked
by likelihood, beginning with the visitor's own typo and ending with a human.

The illustration is drawn rather than shipped: route lines with waypoint dots in the
secondary palette rather than the brand orange, a single orange node at the junction, and
a traffic light showing red. Strokes, circles and three filled discs, all procedural.

**The server-error view is a separate page** with its own copy. It does not tell the
visitor to check their address. It ships no application script.

### The statistic block

The component this product lives or dies by, because every activity, every segment and
every profile is made of them.

| Requirement | Detail |
|---|---|
| Receives a canonical value plus a quantity type | never a pre-formatted string |
| Formats to the viewer's preference | not the recorder's |
| Pace and speed are different quantity types | different formatting, different aggregation |
| Numerals use the condensed width with tabular figures | so columns align |
| Performs no arithmetic | derived values arrive from the server |
| A missing value renders as absent | a ride with no power meter has no power, which is not nothing |

The last row is the one that produces support tickets. A null rendered as zero tells an
athlete something false about their own ride.

### The activity card

The feed unit. It carries the athlete's name and avatar, the activity name as a link, the
activity type in text with its glyph decorative beside it, the local start date, a route
picture drawn from the coarse line, a statistic block of distance, moving time and
elevation gain, a kudos control with its count, and a comment count.

A grouped card names every athlete in the group and carries one route picture and one
statistic block, and it says how many athletes it collects.

A card for a manual entry is visibly distinguished and carries no route picture.

An activity whose route was truncated by a privacy zone says the map is partial, and its
statistic block still reports the whole activity.

### The activity page

The route at a finer simplification level, the full statistic set, an elevation chart, a
splits table, the segment efforts the activity produced with each effort's rank and any
achievement it earned, the kudos list, the comment list, and the athlete's own controls
where they own it.

While matching is running, the segment panel says matching is in progress. It does not
say none.

The elevation chart is keyboard-navigable with its values announced, or is paired with a
data table carrying the same numbers.

### The segment page and its leaderboard

The segment's name, type, distance, elevation gain and average grade; its geometry drawn;
its scope controls; and the leaderboard as **a real table with headers**, one row per
athlete, carrying rank, athlete, elapsed time and date.

Rank is stated in text in the row, not only carried by the podium colour. The first three
rows carry the podium colours and nothing else in the product does.

A hazardous segment shows no leaderboard and says why.

### The upload wizard

Ordered steps, one decision per step: choose the file; confirm the type and name; set the
visibility; submit. The step the athlete is on is stated, the steps behind are
revisitable, and the step ahead is not reachable until the current one is complete.

After submitting, the wizard shows the upload's state and moves through it without the
athlete reloading. A terminal state carries its reason and, for a failure, a retry.

A suspected duplicate shows both candidates side by side with their distinguishing
numbers and asks which to keep.

### Feedback

Feedback on an action arrives as a transient message anchored to one corner, carrying
what happened and, where the action can be undone, a control to undo it. It does not
block the surface behind it and it does not steal focus, but it is announced.

An error that prevents an action is reported in the same place with the reason, and the
action stays unapplied.

### Empty states

The feed of an athlete following nobody says so and offers the next action, which is to
find athletes. A segment with no efforts says so. A club with no posts says so. A search
with no results says so and keeps the query. None of them renders as a blank region.

### Assets, and the zero-asset substitution guide

Nothing binary ships. There is no image file, no video file and no font file in the build
tree. The imagery is substituted rather than omitted, and each substitution is stated.

| Class | Substitution |
|---|---|
| The hero photography of cyclists and of runners | generated atmospheric panels at the measured proportions, in the secondary palette |
| The device and watch composite | generated: a rounded device frame, a route line in the brand orange on a light ground, and a statistic block built from the live tokens |
| The error illustration | generated: route strokes, waypoint circles and three filled discs |
| Route tiles | a plain drawn ground with the line rendered from the application's own coordinates |
| The lettering | a freely licensed grotesque and a condensed width for numerals, from a system stack |

Two of those are better generated than shipped. The device composite is the product
drawing itself, so it is always more current than a photograph and can never show an old
version of the interface. The error illustration is strokes, circles and discs, which the
code draws.

**One is a real loss and this brief says so rather than hiding it.** The signup landing's
argument is people exercising together, and the measured surface makes that argument with
commissioned photographs of cyclists and of runners. A generated wash cannot make it.
Hero photography is the line item to commission before launch, and until it exists the
panels are a placeholder that holds the composition and carries none of its meaning.

The panels, the device composite, the error illustration, avatars, route surfaces
and elevation charts are all drawn from the application's own data or generated as vector
geometry. Fonts come from a system stack with a swap strategy. Every generated region
carries intrinsic dimensions so nothing shifts as the page settles.

## Constraints

- One installation. There is no organisation above an athlete and no federation between
  installations.
- Signup is open, but there is no email of any kind: no verification mail, no password
  reset mail, no notification mail. There is no mail service in this environment.
- No payment capture and no billing integration. The plan surface sells and the gift
  surface issues a code; neither charges anybody.
- No third-party analytics, consent vendor, error reporter, feature-flag service, map
  tile vendor or content delivery vendor, and no outbound call to any of them at run
  time.
- No second database, cache, queue, object store or identity provider beyond the two
  named.
- No recording in the browser, no device pairing, no live position sharing.
- No native application, no desktop client, no browser extension.
- No real-time collaborative editing. One athlete edits their own activity at a time.
- No machine-learning type detection. Type arrives with the file and is corrected by
  hand.
- No binary asset ships with the build: no image file, no video file, no font file
  fetched from anywhere.
- The app must stay responsive with 5 seeded athletes, 2 clubs, 2 challenges, 20
  segments and up to 500 activities each carrying up to 10 streams and 5 efforts.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment;
  never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root,
  empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the
  shell. An ordinary background job dies with its shell, and the app will not be running
  when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of
  them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{"email", "password", "display_name"}` | `{"access_token"}` |
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token"}` |
| `POST /api/auth/link` | `{"provider", "provider_subject", "verified_email"}` | `{"athlete_id", "linked"}` |
| `GET /api/auth/sessions` | - | a top-level array of `{"id", "started_at", "user_agent", "current"}` |
| `DELETE /api/auth/sessions/{id}` | - | `{"id", "ended"}` |
| `GET /api/me` | - | `{"id", "email", "display_name", "plan", "unit_preference", "default_visibility", "profile_discoverable"}` |
| `PATCH /api/me` | any subset of the settable preference fields | the updated athlete |
| `GET /api/health` | - | `{"status"}` |
| `POST /api/uploads` | a file part plus `{"activity_type", "name", "visibility"}` | `{"upload_id", "status"}` |
| `GET /api/uploads/{id}` | - | `{"id", "status", "error_code", "activity_id", "duplicate_of_activity_id"}` |
| `POST /api/uploads/{id}/retry` | - | `{"id", "status"}` |
| `POST /api/uploads/{id}/resolve` | `{"keep"}` where keep is `new` or `existing` | `{"id", "status", "activity_id"}` |
| `GET /api/feed` | `?cursor=<opaque>&limit=<n>` | `{"items", "next_cursor"}` |
| `GET /api/activities/{id}` | - | the activity, its summary, its coarse line, its efforts and its achievements |
| `PATCH /api/activities/{id}` | `{"name", "description", "type", "visibility"}` | the updated activity |
| `DELETE /api/activities/{id}` | - | `{"id", "deleted"}` |
| `GET /api/activities/{id}/streams` | `?types=<csv>` | a top-level array of `{"type", "measured", "algorithm_version", "data"}` |
| `GET /api/activities/{id}/best-efforts` | - | a top-level array of `{"distance_class_m", "start_distance_m", "elapsed_time_s"}` |
| `POST /api/activities/{id}/kudos` | - | `{"activity_id", "kudos_count", "given"}` |
| `DELETE /api/activities/{id}/kudos` | - | `{"activity_id", "kudos_count", "given"}` |
| `GET /api/activities/{id}/comments` | - | a top-level array of comments |
| `POST /api/activities/{id}/comments` | `{"body"}` | the created comment |
| `GET /api/athletes/{id}` | - | `{"id", "display_name", "plan", "follower_count", "following_count", "follow_state"}` |
| `GET /api/athletes/{id}/activities` | `?cursor=&limit=` | `{"items", "next_cursor"}` |
| `POST /api/athletes/{id}/follow` | - | `{"followee_id", "state"}` |
| `DELETE /api/athletes/{id}/follow` | - | `{"followee_id", "state"}` |
| `POST /api/athletes/{id}/follow/respond` | `{"decision"}` where decision is `accepted` or `declined` | `{"follower_id", "state"}` |
| `POST /api/athletes/{id}/block` | - | `{"blocked_id", "blocked"}` |
| `DELETE /api/athletes/{id}/block` | - | `{"blocked_id", "blocked"}` |
| `GET /api/segments` | `?q=&type=&bbox=&cursor=` | `{"items", "next_cursor"}` |
| `GET /api/segments/{id}` | - | `{"id", "name", "activity_type", "distance_m", "elevation_gain_m", "average_grade_pct", "hazardous", "geometry_version"}` |
| `GET /api/segments/{id}/leaderboard` | `?scope=all\|year\|month\|today\|following\|club&club_id=&age_group=&weight_class=&sex=` | `{"total", "entries"}` where each entry is `{"rank", "athlete_id", "display_name", "elapsed_time_s", "start_time_utc"}` |
| `PATCH /api/segments/{id}` | `{"name", "geometry", "hazardous"}` | the updated segment |
| `POST /api/segments/{id}/efforts/{effort_id}/flag` | `{"reason"}` | `{"effort_id", "flag_state", "disposition"}` |
| `GET /api/clubs` | - | a top-level array of clubs |
| `GET /api/clubs/{slug}` | - | the club, its roster and its feed |
| `POST /api/clubs/{slug}/members` | - | `{"club_id", "joined"}` |
| `DELETE /api/clubs/{slug}/members` | - | `{"club_id", "joined"}` |
| `GET /api/challenges` | - | a top-level array of challenges |
| `GET /api/challenges/{slug}` | - | the challenge and its standings, ranks contiguous for the viewer |
| `POST /api/challenges/{slug}/entries` | - | `{"challenge_id", "entered", "progress_value"}` |
| `GET /api/routes` | - | a top-level array of routes, `subscriber` only |
| `POST /api/routes` | `{"name", "geometry", "activity_type"}` | the created route with its derived distance and gain, `subscriber` only |
| `GET /api/heatmap` | `?bbox=` | `{"cells", "minimum_athletes"}`, `subscriber` only |
| `GET /api/privacy-zones` | - | a top-level array of `{"id", "radius_m"}` and never a centre |
| `POST /api/privacy-zones` | `{"centre_lat", "centre_lng", "radius_m"}` | `{"id", "radius_m"}` |
| `DELETE /api/privacy-zones/{id}` | - | `{"id", "deleted"}` |
| `GET /api/notifications` | - | a top-level array of `{"id", "kind", "subject_activity_id", "actor_count", "window_started_at", "read_at"}` |
| `GET /api/applications` | - | a top-level array of `{"id", "name", "scopes", "created_at", "revoked_at"}` |
| `POST /api/applications` | `{"name", "scopes"}` | the application and its token, once |
| `DELETE /api/applications/{id}` | - | `{"id", "revoked"}` |
| `GET /api/export` | - | the athlete's own data as one document |
| `DELETE /api/me` | - | `{"deleted"}` |
| `GET /api/plans` | - | a top-level array of plans with their features |
| `POST /api/gifts` | `{"buyer_email", "recipient_email", "plan_slug", "months", "message"}` | `{"redemption_code"}`, and it accepts no bearer token |
| `GET /api/search` | `?q=&kind=activity\|athlete\|club` | a top-level array of matches |

Bearer auth is carried on everything except health, signup, login, the gift endpoint, the
plan list, and public reads of an `everyone` activity, a segment, a discoverable profile,
a club and a challenge. A successful call returns the named resource or shape; an invalid
or unauthorized call is rejected as a client error, never as a server error and never as
a silent success. List endpoints marked above return a top-level JSON array.

### No mocks

The named provider is where the data actually lives. Every one of these is a contract
violation however good the interface looks: an in-memory list of activities that
disappears when the process restarts; a hardcoded leaderboard payload the app returns to
itself; athletes held in a module-level dictionary rather than in PostgreSQL; a raw
upload written to the container filesystem or held as a database blob rather than put in
the object store; a sign-in comparing a password against a literal in the source rather
than against a stored hash; an upload whose status is only ever a value in a browser tab.
The named provider is the fact; the app's own interface can reflect what lives there and
can never substitute for it.

## Definition of done

A stranger can open the signup landing, read a public activity and a segment leaderboard,
and create an account without being asked for anything but an address, a password and a
name. An athlete can sign in, upload an activity file, and watch that upload move from
received through parsing and matching to ready, while the activity it produced appears in
their followers' feeds and an effort appears on every segment the track crossed in order
and in direction. A viewer who cannot see a hidden athlete reads that segment's
leaderboard with contiguous ranks and no sign that anybody is missing. A blocked athlete
reaches the blocker's content by no path at all. And an athlete on the free plan is
refused every subscriber capability by the server, with the interface control gone or
present.
