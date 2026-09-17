# Checklist: deku/downhole-friction-catalogue-vb

Items: 371
Unpinned values flagged: 4
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

The coverage target extracted from `instruction.md` alone. Every later channel is
joined against these ids in both directions.

## C-OV Overview

- [ ] `C-OV-1` `capability` The product serves a public catalogue of downhole friction reduction hardware. `src: Overview`
- [ ] `C-OV-2` `capability` The product serves a public library of field evidence drawn from real wells. `src: Overview`
- [ ] `C-OV-3` `capability` The product describes a four step engineering service cycle. `src: Overview`
- [ ] `C-OV-4` `capability` The product carries a firm profile covering manufacture, material, history. `src: Overview`
- [ ] `C-OV-5` `capability` The product funnels visitors into one enquiry form that creates a modelling request. `src: Overview`
- [ ] `C-OV-6` `capability` A product detail route names every case that ran that family. `src: Overview`
- [ ] `C-OV-7` `capability` A case route names the product family that ran in that well. `src: Overview`
- [ ] `C-OV-8` `constraint` No cart exists anywhere in the product. `src: Overview`
- [ ] `C-OV-9` `constraint` No price is displayed anywhere in the product. `src: Overview`
- [ ] `C-OV-10` `constraint` A visitor never signs in to read any public route. `src: Overview`

## C-RL User roles

- [ ] `C-RL-1` `role` A Visitor reads every public route under both locales with no account. `src: User roles`
- [ ] `C-RL-2` `role` A Visitor submits a well data enquiry. `src: User roles`
- [ ] `C-RL-3` `role` A Visitor subscribes from the footer form. `src: User roles`
- [ ] `C-RL-4` `role` A Visitor is denied every read of any modelling request. `src: User roles`
- [ ] `C-RL-5` `role` A Visitor is denied every change to a request status. `src: User roles`
- [ ] `C-RL-6` `role` A Visitor is denied every change to a request assignment. `src: User roles`
- [ ] `C-RL-7` `role` An Engineer reads the modelling request queue after signing in. `src: User roles`
- [ ] `C-RL-8` `role` An Engineer changes the status of one modelling request. `src: User roles`
- [ ] `C-RL-9` `role` An Engineer assigns one modelling request to an engineer account. `src: User roles`
- [ ] `C-RL-10` `role` An Engineer adds a note to one modelling request. `src: User roles`
- [ ] `C-RL-11` `role` An Engineer is denied deletion of any modelling request. `src: User roles`
- [ ] `C-RL-12` `role` An Engineer is denied edits to the well data a visitor submitted. `src: User roles`
- [ ] `C-RL-13` `contract` Authorization is enforced server side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-14` `contract` A direct API call from a Visitor session to an Engineer only endpoint is denied. `src: User roles`
- [ ] `C-RL-15` `contract` A denied call from a Visitor session leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-16` `capability` Signup is open, so anyone registers an engineer account with an email plus a password. `src: User roles`
- [ ] `C-RL-17` `literal` The seeded engineer account `engineer@example.com` exists. `src: User roles`
- [ ] `C-RL-18` `literal` The second seeded engineer account `engineer2@example.com` exists. `src: User roles`

## C-CF Core features

- [ ] `C-CF-1` `capability` Login with a seeded email plus the seeded password returns a bearer token. `src: Core features > Auth`
- [ ] `C-CF-2` `capability` Login with a seeded email returns the engineer display name. `src: Core features > Auth`
- [ ] `C-CF-3` `capability` Login with a wrong password is rejected as invalid. `src: Core features > Auth`
- [ ] `C-CF-4` `capability` Login with a wrong password returns no token. `src: Core features > Auth`
- [ ] `C-CF-5` `contract` The client sends the bearer token as an Authorization header on every desk request. `src: Core features > Auth`
- [ ] `C-CF-6` `contract` Passwords are stored hashed, never in plain text. `src: Core features > Auth`
- [ ] `C-CF-7` `contract` An expired token on a desk request is rejected. `src: Core features > Auth`
- [ ] `C-CF-8` `contract` An expired token on a desk request leaves the pending change unapplied. `src: Core features > Auth`
- [ ] `C-CF-9` `capability` Every public catalogue route is readable with no token. `src: Core features > Auth`
- [ ] `C-CF-10` `capability` Every public evidence route is readable with no token. `src: Core features > Auth`
- [ ] `C-CF-11` `constraint` No password reset exists in the product. `src: Core features > Auth`
- [ ] `C-CF-12` `capability` The enquiry band appears at the foot of every route except privacy, contacts. `src: Core features > The enquiry funnel`
- [ ] `C-CF-13` `literal` The enquiry band eyebrow reads `We reply within a day`. `src: Core features > The enquiry funnel`
- [ ] `C-CF-14` `literal` The enquiry band headline reads `Run the numbers on your well`. `src: Core features > The enquiry funnel`
- [ ] `C-CF-15` `capability` The contacts route promotes the enquiry form to be the main content of that page. `src: Core features > The enquiry funnel`
- [ ] `C-CF-16` `capability` The contacts route omits the enquiry band at the foot of the page. `src: Core features > The enquiry funnel`
- [ ] `C-CF-17` `data` The enquiry form carries a required first name field. `src: Core features > The enquiry funnel`
- [ ] `C-CF-18` `data` The enquiry form carries a required last name field. `src: Core features > The enquiry funnel`
- [ ] `C-CF-19` `data` The enquiry form carries a required email field. `src: Core features > The enquiry funnel`
- [ ] `C-CF-20` `data` The enquiry form carries an optional phone field. `src: Core features > The enquiry funnel`
- [ ] `C-CF-21` `data` The enquiry form carries an optional resizable message field. `src: Core features > The enquiry funnel`
- [ ] `C-CF-22` `data` The enquiry form carries a required consent checkbox. `src: Core features > The enquiry funnel`
- [ ] `C-CF-23` `ui` The consent label carries a real inline link to the privacy route. `src: Core features > The enquiry funnel`
- [ ] `C-CF-24` `ui` The submit control stays genuinely disabled until consent is ticked. `src: Core features > The enquiry funnel`
- [ ] `C-CF-25` `capability` The reason the submit control is disabled is announced, not only shown. `src: Core features > The enquiry funnel`
- [ ] `C-CF-26` `literal` The submit control label reads `Contact us`. `src: Core features > The enquiry funnel`
- [ ] `C-CF-27` `data` An enquiry submission carries the locale the visitor sent from. `src: Core features > The enquiry funnel`
- [ ] `C-CF-28` `data` An enquiry submission carries the route the visitor sent from. `src: Core features > The enquiry funnel`
- [ ] `C-CF-29` `capability` A successful submission creates exactly one modelling request. `src: Core features > The enquiry funnel`
- [ ] `C-CF-30` `ui` A successful submission reveals the success panel in place. `src: Core features > The enquiry funnel`
- [ ] `C-CF-31` `literal` The success panel title reads `Thank you!`. `src: Core features > The enquiry funnel`
- [ ] `C-CF-32` `capability` A successful submission shows the request reference to the visitor. `src: Core features > The enquiry funnel`
- [ ] `C-CF-33` `capability` A rejected submission reveals the failure panel in place. `src: Core features > The enquiry funnel`
- [ ] `C-CF-34` `literal` The failure panel title reads `Oops!`. `src: Core features > The enquiry funnel`
- [ ] `C-CF-35` `literal` The failure panel names the fallback mailbox `info@torq.tech`. `src: Core features > The enquiry funnel`
- [ ] `C-CF-36` `ui` Both feedback panels exist in the served markup at all times. `src: Core features > The enquiry funnel`
- [ ] `C-CF-37` `ui` Neither feedback panel is injected into the page after the response arrives. `src: Core features > The enquiry funnel`
- [ ] `C-CF-38` `capability` Submitting the same enquiry twice in immediate succession creates exactly one request. `src: Core features > The enquiry funnel`
- [ ] `C-CF-39` `capability` A repeated immediate submission returns the reference the first submission created. `src: Core features > The enquiry funnel`
- [ ] `C-CF-40` `capability` A repeated immediate submission does not write the stored row a second time. `src: Core features > The enquiry funnel`
- [ ] `C-CF-41` `capability` The submit control is disabled for the duration of an in flight request. `src: Core features > The enquiry funnel`
- [ ] `C-CF-42` `capability` A submission missing the first name is rejected inline with the field named. `src: Core features > The enquiry funnel`
- [ ] `C-CF-43` `capability` A submission missing the last name is rejected inline with the field named. `src: Core features > The enquiry funnel`
- [ ] `C-CF-44` `capability` A submission carrying a malformed email address is rejected inline. `src: Core features > The enquiry funnel`
- [ ] `C-CF-45` `capability` A submission without consent is rejected as a client error with a reason. `src: Core features > The enquiry funnel`
- [ ] `C-CF-46` `capability` A rejected submission writes nothing at all to the database. `src: Core features > The enquiry funnel`
- [ ] `C-CF-47` `capability` The footer subscribe form takes one email field plus one consent checkbox. `src: Core features > The enquiry funnel`
- [ ] `C-CF-48` `capability` Subscribing the same address twice leaves exactly one subscriber row. `src: Core features > The enquiry funnel`
- [ ] `C-CF-49` `ui` The subscribe consent copy is separate from the enquiry consent copy. `src: Core features > The enquiry funnel`
- [ ] `C-CF-50` `capability` An engineer signs in at the desk login route, landing on the queue. `src: Core features > The modelling request desk`
- [ ] `C-CF-51` `ui` The queue renders as a table ordered newest first. `src: Core features > The modelling request desk`
- [ ] `C-CF-52` `ui` The queue row shows the reference, the name, the email of one request. `src: Core features > The modelling request desk`
- [ ] `C-CF-53` `ui` The queue row shows the source route, the status, the assignee of one request. `src: Core features > The modelling request desk`
- [ ] `C-CF-54` `capability` Every stored request field reads back exactly as the visitor submitted. `src: Core features > The modelling request desk`
- [ ] `C-CF-55` `capability` A stored request survives an application restart unchanged. `src: Core features > The modelling request desk`
- [ ] `C-CF-56` `data` A request status is one of the five named values with exact casing. `src: Core features > The modelling request desk`
- [ ] `C-CF-57` `data` A newly created request starts at the status `new`. `src: Core features > The modelling request desk`
- [ ] `C-CF-58` `capability` A request status moves forward through the named order one step at a time. `src: Core features > The modelling request desk`
- [ ] `C-CF-59` `capability` The status `declined` is reachable from any other status. `src: Core features > The modelling request desk`
- [ ] `C-CF-60` `capability` A status transition outside the named order is denied as invalid with a reason. `src: Core features > The modelling request desk`
- [ ] `C-CF-61` `capability` A denied status transition leaves the stored status unchanged. `src: Core features > The modelling request desk`
- [ ] `C-CF-62` `ui` Status is changed inside the request row without leaving the queue. `src: Core features > The modelling request desk`
- [ ] `C-CF-63` `ui` Assignment is changed inside the request row without leaving the queue. `src: Core features > The modelling request desk`
- [ ] `C-CF-64` `ui` An edited row shows the new value at once. `src: Core features > The modelling request desk`
- [ ] `C-CF-65` `ui` A refused save returns the edited row to the previous value with the reason announced. `src: Core features > The modelling request desk`
- [ ] `C-CF-66` `capability` A request is assignable to either seeded engineer account. `src: Core features > The modelling request desk`
- [ ] `C-CF-67` `capability` A request is assignable to nobody. `src: Core features > The modelling request desk`
- [ ] `C-CF-68` `capability` An engineer adds a note to a request without overwriting the visitor words. `src: Core features > The modelling request desk`
- [ ] `C-CF-69` `literal` The seeded modelling request `REQ-1001` exists at status new, assigned to nobody. `src: Core features > The modelling request desk`
- [ ] `C-CF-70` `data` Five product families exist in the catalogue index. `src: Core features > The product catalogue`
- [ ] `C-CF-71` `literal` The product family `FRS` carries the class line Friction Reduction System. `src: Core features > The product catalogue`
- [ ] `C-CF-72` `literal` The product family `SVR` carries the class line Shock, Vibration Reducer. `src: Core features > The product catalogue`
- [ ] `C-CF-73` `literal` The product family `TRANSFER X1` carries the class line Transfer. `src: Core features > The product catalogue`
- [ ] `C-CF-74` `literal` The product family `TRANSFER X3` carries the class line Transfer. `src: Core features > The product catalogue`
- [ ] `C-CF-75` `literal` The product family `TRANSFER X6` carries the class line Transfer. `src: Core features > The product catalogue`
- [ ] `C-CF-76` `data` Ten size variants exist across the five families. `src: Core features > The product catalogue`
- [ ] `C-CF-77` `capability` Every size variant appears in the size table on the detail route of that family. `src: Core features > The product catalogue`
- [ ] `C-CF-78` `ui` A product card shows the class name in small type at the top left. `src: Core features > The product catalogue`
- [ ] `C-CF-79` `ui` A product card shows the family code in the largest type of the page. `src: Core features > The product catalogue`
- [ ] `C-CF-80` `ui` A product card shows a small side elevation render under the family code. `src: Core features > The product catalogue`
- [ ] `C-CF-81` `ui` A product card shows a hand broken two line description. `src: Core features > The product catalogue`
- [ ] `C-CF-82` `ui` A product card shows a row of size variants along the bottom left. `src: Core features > The product catalogue`
- [ ] `C-CF-83` `ui` A product card reveals a Learn more control in the bottom right on hover. `src: Core features > The product catalogue`
- [ ] `C-CF-84` `ui` A product detail banner opens with a bracketed eyebrow reading Products. `src: Core features > The product catalogue`
- [ ] `C-CF-85` `ui` A product detail banner carries the family code as one swept line. `src: Core features > The product catalogue`
- [ ] `C-CF-86` `ui` A product detail banner carries the class name as a second swept line. `src: Core features > The product catalogue`
- [ ] `C-CF-87` `ui` A dark band of result cards follows the product detail banner. `src: Core features > The product catalogue`
- [ ] `C-CF-88` `data` A result card carries a provenance annotation naming where the figure came from. `src: Core features > The product catalogue`
- [ ] `C-CF-89` `data` A result card carries the figure as a counting odometer. `src: Core features > The product catalogue`
- [ ] `C-CF-90` `data` A result card carries a label naming the quantity measured. `src: Core features > The product catalogue`
- [ ] `C-CF-91` `constraint` A provenance annotation is required on every figure, with no default. `src: Core features > The product catalogue`
- [ ] `C-CF-92` `data` The FRS route carries four result cards. `src: Core features > The product catalogue`
- [ ] `C-CF-93` `data` The TRANSFER X3 route carries three result cards. `src: Core features > The product catalogue`
- [ ] `C-CF-94` `ui` A mechanics numbered list follows the result band. `src: Core features > The product catalogue`
- [ ] `C-CF-95` `ui` A mechanics list entry carries a two digit index. `src: Core features > The product catalogue`
- [ ] `C-CF-96` `ui` A mechanics list entry carries a title plus a body. `src: Core features > The product catalogue`
- [ ] `C-CF-97` `ui` The FRS route carries four mechanics list entries. `src: Core features > The product catalogue`
- [ ] `C-CF-98` `ui` The TRANSFER X3 route carries three mechanics list entries. `src: Core features > The product catalogue`
- [ ] `C-CF-99` `capability` A material panel appears on the FRS route only. `src: Core features > The product catalogue`
- [ ] `C-CF-100` `literal` The material panel is titled `Polymer One`. `src: Core features > The product catalogue`
- [ ] `C-CF-101` `data` The material panel table carries five parameter rows. `src: Core features > The product catalogue`
- [ ] `C-CF-102` `literal` The material panel final row prints the value `None` against Steel frame. `src: Core features > The product catalogue`
- [ ] `C-CF-103` `ui` The size table is headed Sizes, running one column per variant. `src: Core features > The product catalogue`
- [ ] `C-CF-104` `data` The FRS size table carries four variant columns. `src: Core features > The product catalogue`
- [ ] `C-CF-105` `data` The FRS size table carries six parameter rows. `src: Core features > The product catalogue`
- [ ] `C-CF-106` `capability` An unmeasured size table cell prints a single dash character. `src: Core features > The product catalogue`
- [ ] `C-CF-107` `constraint` An unmeasured size table cell is never left blank. `src: Core features > The product catalogue`
- [ ] `C-CF-108` `constraint` An unmeasured size table cell never prints a zero. `src: Core features > The product catalogue`
- [ ] `C-CF-109` `data` The FRS-89 column of the FRS size table carries five unmeasured cells. `src: Core features > The product catalogue`
- [ ] `C-CF-110` `ui` A footnote below the FRS size table explains the pilot batch status. `src: Core features > The product catalogue`
- [ ] `C-CF-111` `data` The TRANSFER X3 size table carries three variant columns. `src: Core features > The product catalogue`
- [ ] `C-CF-112` `ui` A numbered application list closes every product detail route. `src: Core features > The product catalogue`
- [ ] `C-CF-113` `capability` The TRANSFER X1 route is built on the TRANSFER X3 template. `src: Core features > The product catalogue`
- [ ] `C-CF-114` `capability` The TRANSFER X6 route is built on the TRANSFER X3 template. `src: Core features > The product catalogue`
- [ ] `C-CF-115` `data` Ten case cards exist on the evidence index. `src: Core features > The field-evidence library`
- [ ] `C-CF-116` `capability` Case cards are ordered by run date descending. `src: Core features > The field-evidence library`
- [ ] `C-CF-117` `data` A case run date is a month plus a year, with no day. `src: Core features > The field-evidence library`
- [ ] `C-CF-118` `ui` A case card shows the well geometry with the region at the top left. `src: Core features > The field-evidence library`
- [ ] `C-CF-119` `ui` A case card shows the family code in the largest type, centred. `src: Core features > The field-evidence library`
- [ ] `C-CF-120` `ui` A case card shows two configuration lines under the family code. `src: Core features > The field-evidence library`
- [ ] `C-CF-121` `ui` The first configuration line takes an accent square marker. `src: Core features > The field-evidence library`
- [ ] `C-CF-122` `ui` The second configuration line takes a grey square marker. `src: Core features > The field-evidence library`
- [ ] `C-CF-123` `ui` A case card shows the measured result across one to three hand broken lines. `src: Core features > The field-evidence library`
- [ ] `C-CF-124` `ui` A case card shows the month with the year below the result lines. `src: Core features > The field-evidence library`
- [ ] `C-CF-125` `ui` A case card reveals a View case control at the bottom right on hover. `src: Core features > The field-evidence library`
- [ ] `C-CF-126` `capability` A case detail route is keyed by the well number rather than by a slug. `src: Core features > The field-evidence library`
- [ ] `C-CF-127` `capability` All ten case detail routes exist. `src: Core features > The field-evidence library`
- [ ] `C-CF-128` `ui` A case route opens with a bracketed eyebrow carrying the field name. `src: Core features > The field-evidence library`
- [ ] `C-CF-129` `ui` A case route sets the well number inside the bracket motif. `src: Core features > The field-evidence library`
- [ ] `C-CF-130` `ui` A dark metric bar of three headline figures follows the case hero. `src: Core features > The field-evidence library`
- [ ] `C-CF-131` `literal` The well 22061 metric bar shows a total depth of `4,025 m`. `src: Core features > The field-evidence library`
- [ ] `C-CF-132` `literal` The well 22061 metric bar shows a horizontal reach of `2,938 m`. `src: Core features > The field-evidence library`
- [ ] `C-CF-133` `literal` The well 22061 metric bar shows a tool count of `100`. `src: Core features > The field-evidence library`
- [ ] `C-CF-134` `ui` A thousands separator renders as static text between the digit strips. `src: Core features > The field-evidence library`
- [ ] `C-CF-135` `data` A well profile card carries a two line description naming the quantity. `src: Core features > The field-evidence library`
- [ ] `C-CF-136` `data` A well profile card description names the run the figure came from. `src: Core features > The field-evidence library`
- [ ] `C-CF-137` `data` The project goals list carries four goals written as imperatives. `src: Core features > The field-evidence library`
- [ ] `C-CF-138` `data` A technology panel carries the family code with a type badge. `src: Core features > The field-evidence library`
- [ ] `C-CF-139` `data` A technology panel repeats the first three mechanics entries of that family. `src: Core features > The field-evidence library`
- [ ] `C-CF-140` `data` The key results section carries three result cards. `src: Core features > The field-evidence library`
- [ ] `C-CF-141` `data` A key result annotation carries the before value with the after value. `src: Core features > The field-evidence library`
- [ ] `C-CF-142` `data` A conclusion restates one project goal with a badge plus per run figures. `src: Core features > The field-evidence library`
- [ ] `C-CF-143` `data` A neutral badge variant exists for an outcome neither met nor missed. `src: Core features > The field-evidence library`
- [ ] `C-CF-144` `data` Three tagged outcome cards follow the conclusions list. `src: Core features > The field-evidence library`
- [ ] `C-CF-145` `capability` Every case route closes on a single unattributed verdict paragraph. `src: Core features > The field-evidence library`
- [ ] `C-CF-146` `constraint` The verdict paragraph names how closely the forecast matched the actual outcome. `src: Core features > The field-evidence library`
- [ ] `C-CF-147` `ui` The engineering route carries four service cards on a dark ground. `src: Core features > The engineering service`
- [ ] `C-CF-148` `ui` A service card carries a two digit index, a title, a one line body. `src: Core features > The engineering service`
- [ ] `C-CF-149` `ui` A service card carries a drawn octagonal glyph above the title. `src: Core features > The engineering service`
- [ ] `C-CF-150` `ui` The fourth service card glyph is drawn with a dashed outline. `src: Core features > The engineering service`
- [ ] `C-CF-151` `capability` The same four steps are stated again at length as the process cycle. `src: Core features > The engineering service`
- [ ] `C-CF-152` `constraint` Both the service card list plus the process cycle list are present. `src: Core features > The engineering service`
- [ ] `C-CF-153` `ui` The process cycle first step offers modelling free for qualified candidates. `src: Core features > The engineering service`
- [ ] `C-CF-154` `ui` The qualification list carries four conditions. `src: Core features > The engineering service`
- [ ] `C-CF-155` `ui` A qualifying condition carries a printed threshold in the annotation slot. `src: Core features > The engineering service`
- [ ] `C-CF-156` `constraint` Every qualifying condition body is distinct from the other three. `src: Core features > The engineering service`
- [ ] `C-CF-157` `ui` Two case cards close the engineering route under Proven in the field. `src: Core features > The engineering service`
- [ ] `C-CF-158` `ui` The about banner is four hand broken lines opening on two very short lines. `src: Core features > The firm profile`
- [ ] `C-CF-159` `ui` A material note sits under the about banner as a footnote to that banner. `src: Core features > The firm profile`
- [ ] `C-CF-160` `capability` Two long statements brighten word by word as the reader scrolls through. `src: Core features > The firm profile`
- [ ] `C-CF-161` `constraint` The word brightening treatment is used on those two statements only. `src: Core features > The firm profile`
- [ ] `C-CF-162` `ui` Three pillar cards appear once on the about route. `src: Core features > The firm profile`
- [ ] `C-CF-163` `constraint` The third pillar body is distinct from the second pillar body. `src: Core features > The firm profile`
- [ ] `C-CF-164` `ui` Two technology cards appear on the about route. `src: Core features > The firm profile`
- [ ] `C-CF-165` `ui` The first technology card carries a three column comparison table. `src: Core features > The firm profile`
- [ ] `C-CF-166` `literal` The comparison table prints the word `baseline` in the steel reduction cell. `src: Core features > The firm profile`
- [ ] `C-CF-167` `ui` The second technology card lists four size values with a To equipment control. `src: Core features > The firm profile`
- [ ] `C-CF-168` `ui` The facts section carries two counting figures, each with a Fact badge. `src: Core features > The firm profile`
- [ ] `C-CF-169` `capability` Two locales are served, the default without a prefix. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-170` `literal` The English locale is served under the `/en` prefix. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-171` `constraint` The locale prefix is the only difference between the two route trees. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-172` `capability` Switching locale replaces the prefix, holding the rest of the path. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-173` `constraint` Switching locale never drops the visitor onto the home route. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-174` `capability` Every internal link on every public route resolves. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-175` `capability` An unknown address renders the product own not found page. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-176` `capability` An unknown address answers with a not found response. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-177` `ui` The not found page carries a control back to the locale home. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-178` `capability` A case number that does not exist renders the not found page. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-179` `capability` Navigation between routes does not full reload the document. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-180` `ui` The privacy route omits the enquiry band. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-181` `capability` The privacy route names the legal entity operating the product. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-182` `capability` The privacy route names the categories of personal data both forms collect. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-183` `constraint` The privacy categories match what the two forms actually send. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-184` `data` The footer carries four columns. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-185` `literal` The footer contact column carries the mailbox `info@torq.tech`. `src: Core features > Locale, routing and the site shell`
- [ ] `C-CF-186` `ui` A colophon row sits below the four footer columns. `src: Core features > Locale, routing and the site shell`

## C-UF User flow

- [ ] `C-UF-1` `contract` The home route resolves under the default locale. `src: User flow`
- [ ] `C-UF-2` `contract` The products index route resolves. `src: User flow`
- [ ] `C-UF-3` `contract` Each of the five product detail routes resolves. `src: User flow`
- [ ] `C-UF-4` `contract` The cases index route resolves. `src: User flow`
- [ ] `C-UF-5` `contract` Each of the ten case detail routes resolves. `src: User flow`
- [ ] `C-UF-6` `contract` The engineering route resolves. `src: User flow`
- [ ] `C-UF-7` `contract` The about route resolves. `src: User flow`
- [ ] `C-UF-8` `contract` The contacts route resolves. `src: User flow`
- [ ] `C-UF-9` `contract` The privacy route resolves. `src: User flow`
- [ ] `C-UF-10` `contract` The desk login route resolves with no session. `src: User flow`
- [ ] `C-UF-11` `contract` The desk queue route requires an engineer session. `src: User flow`
- [ ] `C-UF-12` `ui` An anonymous visitor opening the desk queue lands on the desk login route. `src: User flow`
- [ ] `C-UF-13` `capability` The held destination is served after the engineer signs in. `src: User flow`
- [ ] `C-UF-14` `capability` Signing in lands the engineer on the desk queue. `src: User flow`
- [ ] `C-UF-15` `capability` Signing out returns the engineer to the locale home. `src: User flow`
- [ ] `C-UF-16` `capability` A token expiring mid action lands the engineer on the desk login route. `src: User flow`
- [ ] `C-UF-17` `ui` Every list renders an empty state in words rather than an empty table. `src: User flow`
- [ ] `C-UF-18` `ui` Every route renders a loading state. `src: User flow`
- [ ] `C-UF-19` `capability` A failure never navigates the visitor away from the current route. `src: User flow`
- [ ] `C-UF-20` `capability` An unreachable form service shows the failure panel in place. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-1` `ui` The page ground is a near white neutral field divided by hairline rules into cells. `src: UI/UX notes`
- [ ] `C-UX-2` `ui` The hairline rules continue across section boundaries rather than stopping at them. `src: UI/UX notes`
- [ ] `C-UX-3` `ui` Individual bands invert to a near black neutral against the light page ground. `src: UI/UX notes`
- [ ] `C-UX-4` `ui` The header recolours against whichever band sits behind the header. `src: UI/UX notes`
- [ ] `C-UX-5` `ui` The accent colour is a light vivid red used as a marker before a list number. `src: UI/UX notes`
- [ ] `C-UX-6` `ui` The accent colour appears nowhere that is not an action or an index. `src: UI/UX notes`
- [ ] `C-UX-7` `ui` Every eyebrow label is wrapped in a drawn bracket pair. `src: UI/UX notes`
- [ ] `C-UX-8` `ui` Every button, tag, card preview, contact mark carries chamfered corners. `src: UI/UX notes`
- [ ] `C-UX-9` `ui` The status badge on a case conclusion is the only rounded element in the body. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Every headline figure spins up from a strip of digits on entering the window. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Body copy is a deep neutral, the most used colour of the product. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The primary action is the only element on a page wearing the accent colour. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` A disabled control is never signalled by colour alone. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The palette is built in three layers, components referencing the semantic layer only. `src: UI/UX notes`
- [ ] `C-UX-15` `literal` The type family is `Monument Grotesk`, a variable grotesque. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Headlines are hand broken, with the breaks preserved rather than rewrapped. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Six easing roles exist, with no seventh added. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` A revealed block fades into place with no rise, no scale. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` A revealed block stays revealed once the reveal has run. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` A page banner title is swept by one marker bar per line. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` An interactive element carries two copies of the label, reversing cleanly on exit. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` A press compresses the control more in height than in width. `src: UI/UX notes`
- [ ] `C-UX-23` `constraint` Under a reduced motion preference every effect is present, finished from the start. `src: UI/UX notes`
- [ ] `C-UX-24` `constraint` Hover effects are gated on the device carrying a fine pointer. `src: UI/UX notes`
- [ ] `C-UX-25` `ui` The public routes carry one persistent top navigation with no breadcrumb. `src: UI/UX notes`
- [ ] `C-UX-26` `ui` Each page leads with exactly one primary action, distinct from every secondary one. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` The desk carries a persistent sidebar beside a table first queue. `src: UI/UX notes`
- [ ] `C-UX-28` `constraint` Text meets the WCAG AA contrast bar in the light scheme, in the dark bands. `src: UI/UX notes`
- [ ] `C-UX-29` `constraint` Full keyboard navigation is available with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-30` `constraint` Every content image carries alternative text saying what the image shows. `src: UI/UX notes`
- [ ] `C-UX-31` `ui` Every decorative image declares the decorative role. `src: UI/UX notes`
- [ ] `C-UX-32` `constraint` A counting figure digit strip is marked presentational. `src: UI/UX notes`
- [ ] `C-UX-33` `constraint` The target value of a counting figure is exposed once as text. `src: UI/UX notes`
- [ ] `C-UX-34` `constraint` Every form field carries a real label behind the placeholder. `src: UI/UX notes`
- [ ] `C-UX-35` `constraint` At the narrow width nothing on the page overflows sideways. `src: UI/UX notes`
- [ ] `C-UX-36` `constraint` At the narrow width every navigation target stays reachable. `src: UI/UX notes`
- [ ] `C-UX-37` `ui` A specification table scrolls inside the own cell rather than scrolling the document. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` Storage is PostgreSQL, reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-2` `contract` Auth is app implemented email plus password with bearer tokens. `src: Technical requirements`
- [ ] `C-TR-3` `capability` Every catalogue route arrives as complete markup before any script runs. `src: Technical requirements`
- [ ] `C-TR-4` `capability` Every evidence route arrives as complete markup before any script runs. `src: Technical requirements`
- [ ] `C-TR-5` `constraint` No binary asset ships with the product. `src: Technical requirements`
- [ ] `C-TR-6` `capability` Every icon is inline vector geometry inheriting the surrounding colour. `src: Technical requirements`
- [ ] `C-TR-7` `capability` Every texture field is a generated repeating pattern rather than a tiled image. `src: Technical requirements`
- [ ] `C-TR-8` `capability` Every client mark in the partner grid is a generated placeholder plate. `src: Technical requirements`
- [ ] `C-TR-9` `constraint` No generated face ships anywhere in the product. `src: Technical requirements`
- [ ] `C-TR-10` `capability` The well profile is drawn as inline vector geometry from the case record. `src: Technical requirements`
- [ ] `C-TR-11` `capability` One font file ships, subset to the character sets the two locales need. `src: Technical requirements`
- [ ] `C-TR-12` `constraint` The largest element painted on first load is the hero headline. `src: Technical requirements`
- [ ] `C-TR-13` `constraint` No third party script is loaded from anywhere. `src: Technical requirements`
- [ ] `C-TR-14` `capability` Every response carries a title, a description no other route shares. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-1` `data` Nine tables exist in the schema. `src: Data model`
- [ ] `C-DM-2` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-3` `contract` The seeded password literal works at login. `src: Data model`
- [ ] `C-DM-4` `data` The engineer table carries a unique email column. `src: Data model`
- [ ] `C-DM-5` `data` The product family table carries a unique code column. `src: Data model`
- [ ] `C-DM-6` `data` The product variant label is unique within one family. `src: Data model`
- [ ] `C-DM-7` `data` A spec row cell without a measured value stores a single dash character. `src: Data model`
- [ ] `C-DM-8` `data` The well case table carries a unique well number column. `src: Data model`
- [ ] `C-DM-9` `data` A case metric carries a required provenance value. `src: Data model`
- [ ] `C-DM-10` `data` A case metric stores the before value rather than deriving from the delta. `src: Data model`
- [ ] `C-DM-11` `data` A case metric stores the after value rather than deriving from the delta. `src: Data model`
- [ ] `C-DM-12` `data` The case product join table resolves the cross link in both directions. `src: Data model`
- [ ] `C-DM-13` `data` The modelling request table carries a unique request reference column. `src: Data model`
- [ ] `C-DM-14` `data` The modelling request table carries a source route column. `src: Data model`
- [ ] `C-DM-15` `data` The subscriber table carries a unique email column. `src: Data model`
- [ ] `C-DM-16` `capability` A modelling request exists only where consent was given. `src: Data model`
- [ ] `C-DM-17` `capability` A case metric without a provenance value does not render. `src: Data model`
- [ ] `C-DM-18` `capability` Every product variant appears in exactly one size table column set. `src: Data model`
- [ ] `C-DM-19` `capability` Every case joins at least one product variant. `src: Data model`
- [ ] `C-DM-20` `constraint` No stored well data a visitor submitted is ever edited afterwards. `src: Data model`
- [ ] `C-DM-21` `constraint` No modelling request row is ever removed. `src: Data model`
- [ ] `C-DM-22` `data` Two engineer accounts are seeded. `src: Data model`
- [ ] `C-DM-23` `data` Ten well cases are seeded. `src: Data model`
- [ ] `C-DM-24` `data` The well 22061 case is seeded complete with metrics, results, conclusions. `src: Data model`
- [ ] `C-DM-25` `constraint` Seeding is idempotent, so a restart never duplicates rows. `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-1` `ui` Twelve public routes exist, with no thirteenth added. `src: Front-end specification`
- [ ] `C-FE-2` `ui` The rendered descent layer sits behind the document rather than in front. `src: Front-end specification`
- [ ] `C-FE-3` `ui` Type is sized as a fraction of the window rather than in fixed units. `src: Front-end specification`
- [ ] `C-FE-4` `ui` A preloader guard puts the hero headline into the final state immediately. `src: Front-end specification`
- [ ] `C-FE-5` `ui` The header is fixed to the top of the window on every route. `src: Front-end specification`
- [ ] `C-FE-6` `ui` The header is built as a row of cells with a hairline between each cell. `src: Front-end specification`
- [ ] `C-FE-7` `ui` The header centre carries five navigation items. `src: Front-end specification`
- [ ] `C-FE-8` `ui` The header left gutter is a real cell rather than padding. `src: Front-end specification`
- [ ] `C-FE-9` `ui` The active navigation item cell takes a lighter fill. `src: Front-end specification`
- [ ] `C-FE-10` `ui` Five stacked blurred layers sit behind the header, each blurring twice the last. `src: Front-end specification`
- [ ] `C-FE-11` `ui` At the tablet break the five centre items collapse behind a Menu toggle. `src: Front-end specification`
- [ ] `C-FE-12` `ui` The handset menu panel is chamfered on the bottom two corners only. `src: Front-end specification`
- [ ] `C-FE-13` `ui` The wordmark is one monochrome inline vector surviving colour inversion. `src: Front-end specification`
- [ ] `C-FE-14` `ui` The eyebrow bracket right member is the left member rotated. `src: Front-end specification`
- [ ] `C-FE-15` `ui` Fifteen inline vectors carry the iconography of the product. `src: Front-end specification`
- [ ] `C-FE-16` `ui` The chamfer cuts all eight corners of an element. `src: Front-end specification`
- [ ] `C-FE-17` `ui` The tapered band above the footer narrows on each side as the band descends. `src: Front-end specification`
- [ ] `C-FE-18` `ui` Button padding is asymmetric, carrying more room on the trailing side. `src: Front-end specification`
- [ ] `C-FE-19` `ui` Eleven section types compose every route, with no twelfth added. `src: Front-end specification`
- [ ] `C-FE-20` `ui` The home route carries ten bands in a fixed order. `src: Front-end specification`
- [ ] `C-FE-21` `literal` The hero headline reads `Pushing the limits of drilling`. `src: Front-end specification`
- [ ] `C-FE-22` `ui` A by the numbers annotation carries the before value with the after value. `src: Front-end specification`
- [ ] `C-FE-23` `ui` The descent captions are served in the markup rather than injected. `src: Front-end specification`
- [ ] `C-FE-24` `ui` The skip control is the first focusable control inside the descent band. `src: Front-end specification`
- [ ] `C-FE-25` `ui` The skip control releases the pin on the descent sequence. `src: Front-end specification`
- [ ] `C-FE-26` `capability` A rendered layer that fails to start releases the pin immediately. `src: Front-end specification`
- [ ] `C-FE-27` `ui` A family name in the equipment showcase is prefixed with a literal double slash. `src: Front-end specification`
- [ ] `C-FE-28` `ui` The product card family code is the largest type, with a small render below. `src: Front-end specification`
- [ ] `C-FE-29` `ui` A case card result line rises into place from behind the line above. `src: Front-end specification`
- [ ] `C-FE-30` `ui` An odometer strip carries the digits zero through nine twice over. `src: Front-end specification`
- [ ] `C-FE-31` `ui` An odometer sign, separator, unit sit as static text between the strips. `src: Front-end specification`
- [ ] `C-FE-32` `ui` The depth readout tracks scroll position in both directions. `src: Front-end specification`
- [ ] `C-FE-33` `ui` One reveal observer serves every revealing element on a route. `src: Front-end specification`
- [ ] `C-FE-34` `ui` The reveal observer stops observing an element permanently after firing. `src: Front-end specification`
- [ ] `C-FE-35` `ui` The reveal stagger is a build time class rather than a runtime computed value. `src: Front-end specification`
- [ ] `C-FE-36` `ui` Effects driven from scroll position reverse when the visitor scrolls back up. `src: Front-end specification`
- [ ] `C-FE-37` `ui` Effects triggered once on entry do not reverse. `src: Front-end specification`
- [ ] `C-FE-38` `ui` The footer is revealed by the document sliding off the footer. `src: Front-end specification`
- [ ] `C-FE-39` `ui` Twenty three decorative shapes drift behind the content at four different rates. `src: Front-end specification`
- [ ] `C-FE-40` `constraint` Scroll smoothing never breaks the browser own paging keys. `src: Front-end specification`
- [ ] `C-FE-41` `ui` Six generated lighting lookups light the drawn tool renders. `src: Front-end specification`
- [ ] `C-FE-42` `ui` Card grids render two columns at the laptop width, one at the handset width. `src: Front-end specification`
- [ ] `C-FE-43` `ui` The metric bar three cells stack at the handset width. `src: Front-end specification`
- [ ] `C-FE-44` `ui` The footer columns stack at the handset width. `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` No public route requires a session. `src: Constraints`
- [ ] `C-CN-2` `constraint` No search field exists on the evidence library. `src: Constraints`
- [ ] `C-CN-3` `constraint` No filter, facet, sort control exists on the evidence library. `src: Constraints`
- [ ] `C-CN-4` `constraint` No pagination exists on the evidence library. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The application is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-2` `contract` The port mapping exposes container port 4173 at `APP_PUBLIC_PORT`. `src: Deployment contract`
- [ ] `C-DC-3` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-4` `contract` `GET /api/health` returns 200 once the application is ready. `src: Deployment contract`
- [ ] `C-DC-5` `contract` The application starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-6` `contract` A production build is served behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-7` `contract` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-8` `contract` The server is not a child of the shell. `src: Deployment contract`
- [ ] `C-DC-9` `contract` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract`
- [ ] `C-DC-10` `contract` A list endpoint returns a top level JSON array. `src: Deployment contract`
- [ ] `C-DC-11` `contract` An invalid call is rejected as a client error with a reason. `src: Deployment contract`
- [ ] `C-DC-12` `contract` An unauthorized call is rejected as a client error rather than served. `src: Deployment contract`
- [ ] `C-DC-13` `contract` Bearer auth is required on every endpoint except the public ones named. `src: Deployment contract`
## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the corpus seeded password | `C-DM-2` |
| `engineer@example.com` | the first seeded engineer account | `C-RL-17` |
| `engineer2@example.com` | the second seeded engineer account | `C-RL-18` |
| `REQ-1001` | the seeded modelling request reference | `C-CF-69` |
| `/en` | the English locale prefix | `C-CF-170` |
| `DATABASE_URL` | the PostgreSQL connection variable | `C-TR-1` |
| `APP_PUBLIC_URL` | the public application address | `C-DC-1` |
| `APP_PUBLIC_PORT` | the published port variable | `C-DC-2` |
| `GET /api/health` | the health endpoint | `C-DC-4` |
| `/api` | the API prefix | `C-DC-3` |
| `/app/USER_README.md` | the credential file | `` |
| `.browser_screenshots/` | the reserved screenshot directory | `` |
| `.downloads/` | the reserved download directory | `` |
| `0.0.0.0` | the bind address | `C-DC-9` |
| `FRS` | the first product family code | `C-CF-71` |
| `SVR` | the second product family code | `C-CF-72` |
| `TRANSFER X1` | the third product family code | `C-CF-73` |
| `TRANSFER X3` | the fourth product family code | `C-CF-74` |
| `TRANSFER X6` | the fifth product family code | `C-CF-75` |
| `Polymer One` | the in-house composite material | `C-CF-100` |
| `None` | the steel frame cell value | `C-CF-102` |
| `4,025 m` | the well 22061 total depth | `C-CF-131` |
| `2,938 m` | the well 22061 horizontal reach | `C-CF-132` |
| `100` | the well 22061 tool count | `C-CF-133` |
| `info@torq.tech` | the fallback mailbox | `C-CF-35` |
| `We reply within a day` | the enquiry band eyebrow | `C-CF-13` |
| `Run the numbers on your well` | the enquiry band headline | `C-CF-14` |
| `Contact us` | the submit control label | `C-CF-26` |
| `Thank you!` | the success panel title | `C-CF-31` |
| `Oops!` | the failure panel title | `C-CF-34` |
| `baseline` | the steel comparison cell value | `C-CF-166` |
| `Monument Grotesk` | the type family | `C-UX-15` |
| `Pushing the limits of drilling` | the hero headline | `C-FE-21` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact colour values behind every named role (left to the builder; the brief pins family, tone, shade only) | `` |
| the exact easing curves behind the six named roles (left to the builder; the brief pins character only) | `` |
| the exact pixel widths of the three responsive tiers (left to the builder; the brief pins behaviour only) | `` |
| the token expiry period (left to the builder; the brief pins the rejection outcome only) | `` |

## Coverage ledger

| Section | sentences | items |
|---|---|---|
| Overview | 5 | 10 |
| User roles | 1 | 18 |
| Core features | 17 | 186 |
| User flow | 6 | 20 |
| UI and UX notes | 9 | 37 |
| Technical requirements | 3 | 14 |
| Data model | 4 | 25 |
| Front-end specification | 13 | 44 |
| Constraints | 2 | 4 |
| Deployment contract | 10 | 13 |

## Declared but ungraded

Obligations `instruction.md` states that no channel can observe. Recorded here
rather than given a fabricated citation or dropped in silence (stage-3-checklist.md,
OPEN-DECISIONS D-H). Each stays a requirement of the product; none moves the score.

| Obligation | why: |
|---|---|
| The frontend is Astro with interactive islands. | the stack is named in the brief but G10 bars any reward-bearing check from reading the agent's source, so no channel may confirm it |
| The backend is FastAPI. | same as the frontend: naming the runtime is a build instruction, and confirming it would require reading the source G10 holds out |
| Only the libraries named in the brief plus direct dependencies are used. | a dependency tree is source, not behaviour; G10 bars a reward-bearing check from reading it |
| No second database, cache, queue, object store, identity provider is introduced. | only one backing service is declared, so a second one would be invisible from outside the container |
| PostgreSQL is never downloaded, installed, compiled, started by the application. | the grader reaches the same database either way, so a self-started copy is externally indistinguishable |
| No host is hardcoded; every host is read from the environment. | the grader supplies one environment, so a hardcoded value that happens to match reads identically |
| All timestamps are stored in UTC. | the brief pins no timestamp to a value, so a stored offset cannot be told from a correct one without a second clock |
| The seeded password is written into `/app/USER_README.md` beside each account. | same filesystem path as above |
| The product is single tenant, carrying no organisation boundary. | an absence: there is no second tenant to attempt a crossing from |
| No checkout, no currency, no payment exists anywhere. | an absence with no surface to probe; no payments slot is declared |
| No third party vector map is loaded. | an absence of a network call the runtime environment already forbids |
| No map provider token is required by the product. | an absence of a configuration value; nothing renders differently either way |
| No rendered three dimensional scene ships. | an absence of an asset class, indistinguishable from a scene that simply fails to start |
| No video ships anywhere in the product. | an absence of an asset class; a page that loads none is identical to a page that ships none |
| No map, office photograph, staff list appears on the contacts route. | an absence of content; a judge grades what is present, and nothing distinguishes a missing staff list from a page that never had one |
| No comment, no like, no message thread exists. | an absence of features with no route to probe |
| No file upload, no export, no print view exists. | an absence of features with no route to probe |
| No email is sent by the product. | no email slot is declared, so the corpus has no inbox to interrogate for the absence |
| No external network call is made at runtime. | the environment has no runtime network, so the absence is enforced rather than observed |
| No native application ships. | an absence outside the web surface entirely |
| The product stays responsive with a request queue of low thousands of rows. | a load characteristic; J.5 bars an assertion whose outcome differs between two identical runs |
| Login credentials are written to `/app/USER_README.md`. | a path on the agent container filesystem, which no black-box channel opens |
| The reserved `.browser_screenshots/` directory exists at the application root, empty. | a filesystem obligation the harness consumes directly; no HTTP or browser observation reaches it |
| The reserved `.downloads/` directory exists at the application root, empty. | same filesystem obligation as `.browser_screenshots/` |
| No edge function is used. | a deployment-topology absence the harness owns; nothing inside the trial can observe it |
| No persistent volume, fixed container name, custom network is declared. | a compose-level absence validated by G2 against task.toml, not by any runtime channel |
