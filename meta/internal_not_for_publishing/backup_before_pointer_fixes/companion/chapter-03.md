---
title: "Chapter 3 Companion: Code, Explanations and Solutions"
weight: 30
---

*Companion to Chapter 3: Agile Development and the Nature of Change*  
*OO Development and Agile Practices*

This chapter's main engineering artefacts are stories, acceptance examples, a backlog, completion conditions and workflow policies. This file provides worked versions and suggested answers, followed by an optional Java demonstration of how acceptance examples connect to the existing code.

The examples are proposals for the controlled teaching project. They do not establish new university assessment rules or claim that planned features have been built. Keep this file separate from the student chapter until learners have attempted its activities.

## 1 Project baseline and a proposed goal

Continue from the completed confirmation-extraction version of Chapter 2. The code supports the initial numeric student policy, sequential conflict checks, storing confirmed reservations in memory and returning a snapshot of all stored records. It does not provide a dedicated availability query, cancellation, catalogue validation or durable storage.

A suitable proposed Product Goal is:

> Enable an equipment officer, in a controlled demonstration, to create and inspect student reservations with clear eligibility decisions and no overlapping reservations for the same item within one coordinator.

This is a future outcome to work toward, not a declaration that the whole goal is achieved. It explicitly bounds the demonstration. A different goal is acceptable if the team explains its audience, benefit and scope.

A candidate next-iteration goal is “Let the officer inspect an item's availability without changing reservations.” This is an example for discussion; Chapter 4 will perform actual iteration planning. Neither statement chooses a new assessment date or fixes a Sprint duration.

## 2 A worked six-item backlog

The order below is one defensible teaching choice, not the only correct ordering. We review the inherited reservation flow first, then make an availability enquiry possible, and prepare repeatable checks before expanding the lifecycle.

| Order | ID | Item | Type | Current support and remaining work |
|---:|---|---|---|---|
| 1 | US-01 | Record an eligible, non-conflicting student reservation | User story | Core behaviour exists; clarify the user interaction and assess the complete delivery evidence before marking Done |
| 2 | US-02 | Inspect availability without reserving an item | User story | New query behaviour; must read current records without mutating them |
| 3 | EN-01 | Automate the existing build and checks | Technical enabler | Local commands exist; an automated workflow is planned for the kickoff work |
| 4 | US-03 | Inspect one borrower's active reservations | User story | An all-records snapshot exists; a defined borrower-focused interaction and filter are still needed |
| 5 | US-04 | Cancel a confirmed reservation under an agreed policy | User story | New lifecycle behaviour; cancellation authority and permitted states require clarification |
| 6 | US-05 | Reject unknown equipment identifiers using an agreed catalogue | User story | Current validation only checks non-blank text; catalogue source and failure policy remain open |

### Rationale and dependencies

US-01 prevents the team from building on a falsely reported baseline. Its remaining work should be recorded explicitly; do not recreate existing logic or claim it as newly developed. If the team verifies that it already meets the agreed delivery conditions, move it to completed history with evidence and select remaining work.

US-02 answers the workflow gap discovered at demonstration. It depends on understanding the existing records and period convention, but it need not wait for a production database. EN-01 supports reliable repeated work and should be coordinated with Chapter 4's kickoff requirements; its place here does not forbid parallel preparation when capacity permits.

US-03 may be a small useful improvement, although access rules matter outside the controlled officer-operated demonstration. US-04 changes the meaning of “active” and therefore affects counts and availability. US-05 matters before accepting arbitrary identifiers in a broader deployment. Its lower position assumes that early demonstrations use controlled fixture identifiers; change that ordering if real users or uncontrolled input enter scope.

The backlog order is not a calendar schedule. Some items need policy decisions, and the six items are not a promise that all can be completed in one Sprint.

## 3 Refined story cards

### 3.1 US-01 Record a reservation

**Actor and outcome:** as an equipment officer, I want to record an eligible, non-conflicting student reservation so that the selected item is allocated for the requested period.

**Scope:** one item per request, controlled non-blank fixture identifiers, whole-day durations and representable calendar dates. The initial student rules apply. Requests are processed sequentially by one coordinator. No real catalogue, identity provider, database, payment or email service is implied.

**Decisions carried from earlier chapters:** at most three active reservations; duration from one to seven days inclusive; start-inclusive/end-exclusive periods; all stored records remain active until a later lifecycle feature changes that assumption.

| Criterion | Example and expected observation |
|---|---|
| AC-01 | With no records, B1 requests CAM1 from 20 October 2026 for two days; one reservation is recorded and its confirmation returned |
| AC-02 | With that record present, B2 requests CAM1 from 21 October for one day; it is rejected, the count stays one, and B1's record is unchanged |
| AC-03 | B2 instead requests CAM1 from 22 October for one day; it is accepted because the earlier end is exclusive. A request from 19 to 20 October for the same item is also accepted, because it ends exactly where R1 begins |
| AC-04 | With three active reservations for B1 across different items, a fourth is rejected and the count remains three |
| AC-05 | One-day and seven-day requests can pass the duration rule; zero, negative and eight-day requests are rejected without adding records |

**Further clarification:** whether past start dates are allowed; what the agreed user interaction should be; how future cancellation affects the active count. The first two need explicit treatment when preparing a complete user-facing flow. Cancellation policy belongs to US-04 unless the stakeholder changes current scope.

**Existing evidence:** Chapter 2 contains checks for the core behaviour. Section 8 supplies an additional direct mapping from these acceptance examples to the current coordinator. Neither check set alone establishes that a peer review, shared integration or usable input interaction has happened.

### 3.2 US-02 Inspect availability

**Actor and outcome:** as an equipment officer, I want to inspect whether a known item is available for a proposed period without reserving it, so that I can discuss options with a borrower.

**Scope:** enquiry against the current coordinator's records for controlled known fixture identifiers. It does not promise that the physical item is operational, not under maintenance, or available in another application instance.

**Core distinction:** a successful enquiry never confirms a reservation and never guarantees that a later request will succeed. The later request must perform its own checks against its then-current state.

| Criterion | Given and when | Expected observations |
|---|---|---|
| AQ-01 | No stored reservations; inspect CAM1 for `[20 Oct, 22 Oct)` | Available within this record set; count and records unchanged |
| AQ-02 | CAM1 is reserved for `[20 Oct, 22 Oct)`; inspect it for `[21 Oct, 23 Oct)` | Unavailable; existing record unchanged |
| AQ-03 | The same existing reservation; inspect CAM1 for `[22 Oct, 23 Oct)` | Available under the current adjacency convention; records unchanged |
| AQ-04 | CAM1 is reserved; inspect a different known item MIC1 for the same period | Available if MIC1 has no conflict; records unchanged |
| AQ-05 | Inspect an invalid period with equal or reversed dates | An identifiable invalid-input outcome, rather than a valid availability answer; no records changed |

AQ-05 intentionally states the user-observable meaning without prescribing an exception class or interface design. The team must make that technical contract explicit during implementation. It must not silently return “available” for an invalid period.

**Unknowns:** the future behaviour for catalogue identifiers outside the controlled fixtures; maintenance rules; restrictions on past dates. Record these as questions or related work. Do not add a hidden maintenance buffer: the present interval convention allows adjacency.

**Status:** this query is not implemented by the Chapter 2 code. `reserve` cannot be reused as an enquiry by calling it and undoing the result; that would introduce a mutation and does not satisfy the story.

## 4 INVEST reasoning and completion conditions

### 4.1 INVEST applied to US-02

- **Independent:** the enquiry can be demonstrated with existing records without implementing cancellation. It still depends on the agreed period convention.
- **Negotiable:** the input mechanism and presentation can be discussed while preserving non-mutation and a clear result.
- **Valuable:** the officer can compare periods without creating speculative reservations.
- **Estimable:** a query against a controlled local list is sufficiently bounded for discussion. A live inventory integration would add uncertainty and belongs in separate scope.
- **Small:** one item and one period avoid a full multi-item scheduling interface.
- **Testable:** compare the result and the complete relevant record state before and after the enquiry.

This reasoning is more useful than marking six boxes without explanation. A student can challenge the story's scope or dependency assumptions and still provide a strong answer.

### 4.2 A proposed Definition of Done

For the controlled teaching increment, the team proposes:

1. Applicable acceptance examples are verified, including important rejection paths and state effects.
2. Source compiles and executes using the documented environment and commands.
3. A peer review has occurred and findings that prevent acceptance are resolved.
4. Work is integrated into the shared codebase, and existing checks still pass.
5. Usage notes, domain decisions and known limitations are updated where needed.
6. Another team member can reproduce the intended demonstration within its stated scope.

This is an agreement to adopt or refine, not a claim that inherited work already satisfies all six items. Independent study can use a clearly labelled self-review for practice, but should not falsely record peer approval. A future CI gate must be introduced explicitly rather than claimed before it exists.

### 4.3 Distinguishing the three questions

| Kind of condition | Example | Question answered |
|---|---|---|
| Acceptance criterion | An enquiry leaves reservations unchanged | Does this behaviour satisfy the story? |
| Definition of Done | The integrated change has been reviewed and its relevant checks pass | Does the increment meet the shared quality standard? |
| Local Ready policy | Known scope, example inputs and identified blocking questions | Is the item sufficiently understood to begin? |

A Ready policy should help a conversation, not become a ritual that demands every detail months in advance. It is not a fourth Scrum artefact. Equally, no amount of formatting can make an unresolved cancellation-authority rule disappear.

## 5 A complete example workflow policy

**Work item:** a small user story or an explicitly identified technical enabler. Do not mix large epics and tiny subtasks into the same WIP count without explaining how they are treated.

**States:** Backlog, Ready, Building, Review and Done.

**Start and finish:** work starts on entering Building and finishes on entering Done. Ready items are not yet started. Building and Review both contribute to WIP.

**WIP control:** at most two items across Building and Review combined. This number is invented for the classroom exercise, not claimed to be optimal for every team.

**Movement rules:** an item enters Ready when its outcome, scope and useful examples are understood well enough to start. It enters Building when the team has capacity under the limit. It enters Review when the change and checking evidence can be inspected. It enters Done only when the applicable acceptance conditions and agreed DoD have been met. A failed review returns the item to Building and it remains within WIP.

**Blocked work:** retain the item in its actual workflow state, mark its blocker and who is investigating it, and keep it within WIP. Do not hide it in an excluded column or mark it Done to free capacity. If the team explicitly abandons an item, record that disposition separately from completed value and preserve the reason.

**Service-level expectation:** provisionally, 85% of these small work items within five working days from Building to Done. No historical evidence supports that number yet; it is a working hypothesis to revise, not a promise to users or a grading target. State how working days are counted before collecting timing data.

**Inspection:** when meeting to coordinate, first inspect blocked or waiting active work and agree a concrete next action. Later flow analysis should use consistent start/finish definitions. Detailed metrics and forecasting are deferred to Chapter 12.

### Board exercise solution

In the supplied hypothetical snapshot, US-02 is in Building and EN-01 is blocked in Review. Two items have started and neither has finished, so the limit is reached. The team should investigate the setup blocker, help review or complete the existing feature before pulling another ordinary item from Ready.

If the blocker genuinely prevents progress, discuss and record the trade-off instead of silently changing the count. A WIP policy can be revised deliberately, but an invisible exception destroys the information needed to evaluate it. US-01's Done position belongs only to the hypothetical board simulation; it is not an assertion about the actual project.

## 6 Relative estimation example

The following numbers are invented for a discussion; no empirical velocity or delivery forecast is being claimed.

| Item or remaining work | Example estimate | Assumption or uncertainty |
|---|---:|---|
| US-02 local availability enquiry | 3 points | Known fixture identifiers, existing date convention, no external catalogue, narrow agreed interaction |
| US-03 inspect one borrower's active records | 2 points | Current definition of active remains unchanged; officer-operated controlled demonstration |
| US-04 cancellation | Not yet estimated | Authority, permitted lifecycle states and consequences for counts remain unresolved |

Include implementation, meaningful checking, review and needed documentation in the estimate. Different values are acceptable when assumptions and comparison logic are clear. These numbers must not be converted to hours or used to rank students.

A useful investigation for US-05 would ask whether an authorised read-only sample catalogue can be obtained and what identifier fields it contains. Specify a bounded effort and a written result, including failure to obtain access. Do not claim such access already exists or ask students to probe systems without authorisation.

### Critiquing the two process recommendations

Advice A tries to avoid ambiguity but assumes that all relevant detail can be known before implementation. In this project, the availability enquiry itself emerged from demonstration. Freezing every detail could prevent useful learning or preserve a mistaken assumption.

Advice B tries to encourage fast feedback but leaves the team unable to distinguish successful behaviour from a persuasive demonstration. Without prior examples, a query that mutates state might look acceptable.

A stronger agreement is to clarify the next small outcome and its key examples before implementation, then revise the backlog and decisions as new evidence appears. Keep later work less detailed until it approaches selection. This does not mean ignoring major dependencies or domain rules.

## 7 AI activity decision log

The student chapter words the suggestions with “refused” and “specify” so that they do not echo the classification labels (accept, reject for this story, clarify).

| Suggestion | Disposition | Reason and next action |
|---|---|---|
| Refuse a request for the same item and an identical period | Accept | An identical period overlaps; this is a useful special case of AC-02 |
| Refuse a request beginning exactly when an earlier period ends | Reject for this story | Contradicts the current exclusive-end convention and AC-03 |
| Email every confirmation within thirty seconds | Reject for this story | Adds delivery infrastructure and a timing requirement not agreed in the scope; retain as a candidate only if a stakeholder wants it |
| A refused request leaves stored records unchanged | Accept | Matches existing state-preservation expectations, including AC-02 and AC-05 |
| Specify how past start dates are treated | Clarify | The current policy does not establish a past-date restriction; do not invent one. Ask the stakeholder |
| Take a deposit payment before confirming | Reject for this story | Introduces a new business process and unapproved scope |
| Specify whether cancelled reservations count toward the limit | Clarify and link to US-04 | Cancellation is not implemented; the future rule matters when that lifecycle is introduced, but does not automatically block today's bounded demonstration |

No suggestion becomes a rule merely because AI produced it. The correction may be to preserve an accurate observation, narrow its claim, record a question or keep a possible future feature outside the current story.

A sufficient student record gives the suggestion, classification, relevant source of authority and next action. “AI is wrong” without identifying the conflicting rule is not enough.

## 8 Java bridge from acceptance examples to code

### 8.1 Purpose and prerequisites

The full source below runs AC-01 through AC-05 against the **completed Chapter 2 coordinator**. It introduces no new application behaviour and makes no claim to implement US-02. Plain Java checks are used so the relation between an example and an observation remains visible before formal testing techniques in Chapter 7.

Copy these four inherited files from the Chapter 2 code-and-solutions file: `ReservationRules.java`, `LoanPeriod.java`, `Reservation.java`, and the completed `ReservationCoordinator.java`. Put them in one directory with the new file below. Preserve their content; the fixture rules and message contract have not changed.

**Filename: `Chapter03AcceptanceExamples.java`**

```java
import java.time.LocalDate;

public class Chapter03AcceptanceExamples {
    public static void main(String[] args) {
        LocalDate day = LocalDate.of(2026, 10, 20);
        ReservationCoordinator coordinator = new ReservationCoordinator();

        // AC-01: an eligible request is stored once and confirmed.
        String accepted = coordinator.reserve("B1", "CAM1", day, 2);
        require(accepted.equals(
                "Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)."),
                "AC-01 confirmation");
        require(coordinator.reservations().size() == 1, "AC-01 one record");
        System.out.println("AC-01 passed");

        // AC-02: an overlapping request for the same item changes no records.
        String conflict = coordinator.reserve("B2", "CAM1", day.plusDays(1), 1);
        require(conflict.equals("Rejected: item unavailable."), "AC-02 rejection");
        require(coordinator.reservations().size() == 1, "AC-02 unchanged count");
        require(coordinator.reservations().get(0).borrowerId().equals("B1"),
                "AC-02 original borrower preserved");
        System.out.println("AC-02 passed");

        // AC-03: a booking may start at an existing exclusive end,
        // or end exactly where an existing booking starts.
        String adjacent = coordinator.reserve("B2", "CAM1", day.plusDays(2), 1);
        require(adjacent.equals(
                "Confirmed: R2 for B2 on CAM1 [2026-10-22, 2026-10-23)."),
                "AC-03 adjacent confirmation");
        require(coordinator.reservations().size() == 2, "AC-03 second record");
        String before = coordinator.reserve("B3", "CAM1", day.minusDays(1), 1);
        require(before.equals(
                "Confirmed: R3 for B3 on CAM1 [2026-10-19, 2026-10-20)."),
                "AC-03 request ending at an existing start");
        require(coordinator.reservations().size() == 3, "AC-03 third record");
        System.out.println("AC-03 passed");

        // AC-04: count limits span items, not just one equipment item.
        ReservationCoordinator limits = new ReservationCoordinator();
        for (String item : new String[] {"CAM1", "MIC1", "TRI1"}) {
            require(limits.reserve("B1", item, day, 1).startsWith("Confirmed:"),
                    "AC-04 establish three valid reservations");
        }
        require(limits.reserve("B1", "CAM2", day, 1).equals(
                "Rejected: borrower limit or duration."), "AC-04 fourth rejected");
        require(limits.reservations().size() == 3, "AC-04 unchanged count");
        System.out.println("AC-04 passed");

        // AC-05: one and seven days are allowed; zero, negative and eight are not.
        ReservationCoordinator durations = new ReservationCoordinator();
        require(durations.reserve("B1", "CAM1", day, 1).startsWith("Confirmed:"),
                "AC-05 one day");
        require(durations.reserve("B1", "MIC1", day, 7).startsWith("Confirmed:"),
                "AC-05 seven days");
        for (int days : new int[] {0, -1, 8}) {
            require(durations.reserve("B1", "TRI1", day, days).equals(
                    "Rejected: borrower limit or duration."), "AC-05 invalid duration");
            require(durations.reservations().size() == 2, "AC-05 unchanged count");
        }
        System.out.println("AC-05 passed");
        System.out.println("All 5 acceptance examples passed.");
    }

    private static void require(boolean condition, String description) {
        if (!condition) {
            throw new AssertionError(description);
        }
    }
}
```

### 8.2 Compile and run

Use the same Java 17 language/API baseline as Chapter 2:

```sh
javac --release 17 -d out ReservationRules.java LoanPeriod.java Reservation.java ReservationCoordinator.java Chapter03AcceptanceExamples.java
java -cp out Chapter03AcceptanceExamples
```

Expected output:

```text
AC-01 passed
AC-02 passed
AC-03 passed
AC-04 passed
AC-05 passed
All 5 acceptance examples passed.
```

### 8.3 What the code demonstrates

Each labelled group corresponds to a criterion, with setup, action and observations. AC-01 through AC-03 intentionally use one coordinator to inspect a sequence. AC-04 and AC-05 use fresh coordinators so existing state from another scenario does not accidentally decide their outcomes.

AC-04 uses different item identifiers, ensuring that the fourth refusal comes from the borrower's total count rather than a conflict on one item. AC-05 uses two valid requests and then invalid durations while the borrower remains below the count limit. That makes the duration rule the relevant reason for rejection.

The `require` helper throws `AssertionError` on a mismatch. It does not depend on the JVM's optional assertion flag. Some observations compare exact strings because the current public method returns strings. This couples those checks to the current message contract; a later typed outcome could separate a business decision from its wording. Do not redesign that API merely to complete this planning chapter.

AC-03 includes a request that ends exactly where an existing reservation begins because verification showed a gap without it. Changing the first overlap comparison in `LoanPeriod` from `start.isBefore(other.endExclusive)` to `!start.isAfter(other.endExclusive)` passed all five groups when AC-03 covered only a request starting at an existing end. Chapter 2's `adjacency symmetric` check caught that change, which is a useful illustration of why example sets are chosen to expose specific faults, not merely to be numerous.

These five groups are examples, not exhaustive proofs. They do not check catalogue membership, concurrent access, durable storage or a real user's entire interaction. A passing run does not automatically satisfy the team's Definition of Done: review, integration, reproducibility and the agreed delivery scope still matter.

## 9 Review-question solutions

1. **Iteration and increment:** revising the reservation messages after feedback is an iteration on an existing capability. Adding an integrated, usable enquiry that leaves records untouched is an increment. A cycle can produce an increment, but the words do not mean the same thing.
2. **Agile values:** favouring usable software over exhaustive documents still permits a short written period convention. The documentation makes behaviour and tests understandable; it should support the outcome rather than become a substitute for examining it. Equivalent reasoned examples are acceptable.
3. **Events:** a Review examines product outcomes with stakeholders and influences next product choices. A Retrospective selects improvements in how the team works. A Daily Scrum helps Developers adapt their near-term plan toward the Sprint Goal. A status report to the lecturer does not automatically fulfil all of those purposes.
4. **Conditions:** acceptance criteria are item-specific behavioural expectations; DoD is the shared quality standard for the increment; Ready is this team's local policy for starting work. The latter is not another formal Scrum artefact.
5. **False Done claim:** the enquiry violates its non-mutation acceptance condition, and missing review violates the example DoD. Inspect records before and after the enquiry, repeat relevant examples, and obtain an actual review. A correct answer for one date is insufficient evidence for either issue.
6. **Hidden WIP:** the blocked review item remains unfinished, so starting a third item exceeds the stated combined limit. Help investigate or resolve the blockage and finish existing work. If changing policy is necessary, record the change and its reason rather than relabelling the item to hide it.

## 10 Transfer-challenge solution

### Candidate stories and enabler

**RB-01:** as a laboratory coordinator, I want to inspect availability for one known room and period without booking it, so that I can offer an appropriate slot.

**RB-02:** as a laboratory coordinator, I want to confirm an eligible, non-conflicting booking, so that the room is allocated for an agreed session.

**RE-01:** make the room-booking project's existing build and checks reproducible in its shared workflow, reducing dependence on one developer's environment. This is a justified enabler, not a fictional room user's request for a build tool.

### RB-01 acceptance examples

For the exercise, assume known fixture room identifiers and a declared start-inclusive/end-exclusive convention:

- With no existing booking, a valid enquiry reports available and creates no booking.
- With a booking from 10:00 to 11:00, an enquiry for the same room from 10:30 to 11:30 reports unavailable and preserves the existing record.
- An enquiry starting at 11:00 may report available when there is no other conflict, and it changes no records.
- An invalid interval with end before start produces an identifiable invalid-input result and does not change records.

These are proposed teaching rules, not a claim about institutional room policy. Confirm whether a cleaning or preparation buffer is required before accepting adjacency for a real system.

### Completion, flow and uncertainty

A reasonable DoD includes checked acceptance examples, a reproducible build, actual review, integration and updated decisions or usage notes. A simple workflow can limit the combined Building and Review states to two items, counting blocked work until it is finished or explicitly withdrawn.

A stakeholder question is whether room capacity or organiser authority restricts booking. A technical question is whether an approved read-only room catalogue can be obtained. Investigate the latter with a bounded task; do not invent an API.

A small demonstration with synthetic room records can elicit feedback before these wider integrations exist. Present the limitations explicitly and ask the stakeholder to examine the intended interaction, not to assume a production service is already operating.

## 11 Reusable working templates

### Story card

| Field | What to record |
|---|---|
| ID and title | Stable identifier and a short outcome |
| Actor and value | Who needs it and why |
| Scope | What this item includes and the boundaries of the demonstration |
| Rules and assumptions | Confirmed decisions separated from temporary assumptions |
| Acceptance examples | Inputs, action, expected result and relevant state effects |
| Current support | Existing code or evidence, if any |
| Dependencies and questions | Blocking decisions, related items and responsible follow-up |
| Estimate | Optional local relative size, assumptions and date of discussion |
| Completion evidence | Links or notes for checks, review, integration and demonstration |

### Decision record for a proposed criterion

| Proposal | Accept, reject or clarify | Reason and evidence | Follow-up or related item |
|---|---|---|---|
| Write the proposed behaviour | Choose one | Identify the rule, scope boundary or missing decision | Record the next action |

### Peer story review

Ask another team to describe the story's outcome, choose an ordinary case and a failure case, and identify the expected state afterwards. If they must invent a cancellation policy, duration convention or catalogue assumption, refine the story or explicitly defer the missing decision. Record the actual reviewer and questions; a template is not evidence that review occurred.

## 12 Instructor guidance

Start with the equipment officer's enquiry request. Ask students to find the exact difference between the current `reserve` operation and a non-mutating question. This connects process work to a real behaviour gap rather than beginning with meeting names.

Use a short role-play to clarify the story: one learner represents the officer, another asks about boundaries, and another records examples and open questions. Label this as a classroom arrangement, not a redefinition of Scrum accountabilities. Keep the critical-reading exercise focused on assumptions and consequences instead of choosing a slogan.

The six backlog items, top-story criteria, board snapshot and AI classifications are consistent with the student chapter. Proposed or hypothetical states are identified; no claim is made that US-02 through US-05 or EN-01 are implemented. The period convention and numeric rules match Chapter 2, and the example DoD does not pretend that an automated pipeline already exists.

### 12.1 Do the acceptance examples detect faults?

Each change below was made on its own to a copy of `LoanPeriod` or `ReservationRules`, and the Chapter 3 acceptance runner was run. Where the Chapter 2 runner is named, it was run as well.

| Version of `LoanPeriod` or `ReservationRules` | Chapter 3 runner | Chapter 2 runner |
|---|---|---|
| Original | All 5 acceptance examples passed | All 34 checks passed |
| First overlap comparison changed to `!start.isAfter(other.endExclusive)` | Failed at `AC-03 request ending at an existing start` | Failed at `adjacency symmetric` |
| Second overlap comparison changed to `!other.start.isAfter(endExclusive)` | Failed at `AC-03 adjacent confirmation` | Not run |
| `activeReservations < 3` changed to `<= 3` | Failed at `AC-04 fourth rejected` | Not run |
| `requestedDays <= 7` changed to `< 7` | Failed at `AC-05 seven days` | Not run |

Suppose AC-03 contained only a request that starts at an existing end. The first change would then pass every Chapter 3 acceptance example. The extra request in AC-03, one that ends exactly where an existing reservation begins, closes that gap.

Martin (2002) and Rubin (2012) are cited in the student chapter; this book treats Agile practices and Scrum in Chapter 3 and sprint planning in Chapter 4.

The practical activity runs on the Team project, with the lending backlog as the worked model and a transfer note for other provided domains. The process note asks teams to separate Scrum as defined from classroom adaptations and optional practices. When marking the process note, accept any honest statement. A team that uses stories, points and a board but no designated Scrum Master has described a legitimate adaptation, whereas a team that calls an academic deadline a Sprint without naming that adaptation has not.

This chapter adds planning and acceptance-example artefacts. The cumulative application code remains at the completed Chapter 2 checkpoint. Keep these backlog decisions available for Chapter 4's kickoff planning, and revise them explicitly when stakeholder answers arrive.

Authoritative concept references are provided in the student chapter. All worked project material and suggested solutions here are original examples.