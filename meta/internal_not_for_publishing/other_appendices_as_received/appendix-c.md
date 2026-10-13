---
title: "Appendix C: Engineering Templates"
description: "User stories, DoD, capacity planning, PR reviews, ADRs, retrospectives, and AI records."
weight: 230
---

*OO Development and Agile Practices*  
*Designing, Testing and Evolving Software with AI Assistance*

## How to use this appendix

Professional software engineering requires structured, repeatable communication. In an Agile team, ambiguity regarding user requirements, untracked architectural decisions, informal code reviews, and undocumented AI interactions introduce technical debt and erode team velocity.

This appendix provides a standardized catalog of **Engineering Templates** used across the SE506 curriculum. In accordance with Blueprint Section 6, every template in this appendix contains three elements:
1. **Engineering Purpose:** Why the document exists, when it is authored, and what failure mode it prevents.
2. **Structural Schema:** A clean, reusable Markdown template ready to be copied into your team repository (under `.github/` or `docs/`).
3. **Concrete Filled Example:** A realistic, completed artifact drawn directly from the **Campus Equipment Lending System**.

* **Use Section C.1 and C.2** during iteration planning (Weeks 1 to 4) to formulate user stories and establish team quality standards.
* **Use Section C.3** during capacity planning sessions (Week 3 laboratory, Ground Rule G1).
* **Use Section C.4 and C.5** during day-to-day development to structure pull request reviews and document architectural decisions (ADRs).
* **Use Section C.6 and C.7** to facilitate sprint retrospectives and maintain the eight-part AI verification audit trail required by Chapter 15.
* **Use Section C.8** when compiling the final project handover dossier in Week 13.

---

## C.1 User Story and Acceptance Criteria Template

### Engineering Purpose
Captures user requirements in small, testable increments without prematurely dictating implementation mechanics or user interface layouts. The *Given-When-Then* acceptance criteria form the explicit behavioral contract from which automated acceptance and integration tests are derived.

### Structural Schema

```markdown
# User Story: [STORY-ID] [Concise Title]

### User Value Statement
* **As a** [specific role or persona],
* **I want to** [execute a specific domain action or capability],
* **So that** [achieve an identifiable business value or goal].

### Domain Context & Invariants
* **Preconditions:** [System state required prior to execution]
* **Boundary Rules:** [Specific limits, quotas, or temporal interval constraints]
* **Out of Scope:** [Explicitly excluded capabilities or edge cases deferred to later stories]

### Acceptance Criteria (Given-When-Then)

#### Scenario 1: [Normal / Happy Path]
* **Given** [pre-existing system state, entities, and configurations],
* **When** [the user or caller invokes the specific operation with valid inputs],
* **Then** [the system completes the state transition successfully],
* **And** [the expected confirmation, return value, or snapshot is produced].

#### Scenario 2: [Boundary / Rejection Condition]
* **Given** [system state at a defined limit or conflicting period],
* **When** [the user attempts the operation],
* **Then** [the system rejects the request safely with an explicit policy message],
* **And** [no internal state mutations, sequence increments, or side effects occur].
```

### Concrete Filled Example: Advance Reservation for Staff Loans

```markdown
# User Story: US-12 Advance Reservation for Staff Equipment Loans

### User Value Statement
* **As a** University Academic Staff Member,
* **I want to** reserve specialized laboratory equipment up to 60 days in advance for a maximum duration of 30 days,
* **So that** I can guarantee equipment availability for scheduled research experiments.

### Domain Context & Invariants
* **Preconditions:** Staff member has an active university account in good standing with zero overdue loans.
* **Boundary Rules:** 
  * Loan periods are strictly half-open: `[start, endExclusive)`.
  * Staff quota allows at most 5 active combined physical loans and future reservations.
* **Out of Scope:** Automatic recurring bookings (deferred to Epic 4).

### Acceptance Criteria (Given-When-Then)

#### Scenario 1: Valid Advance Reservation within Staff Quota
* **Given** Staff member "STAFF-401" has 2 active loans and 0 reservations (quota limit: 5),
* **And** Oscilloscope "ITEM-OSC-04" is available for `[2026-11-01, 2026-11-15)`,
* **When** "STAFF-401" requests a reservation for "ITEM-OSC-04" starting 2026-11-01 for 14 days,
* **Then** a confirmed reservation "R-1092" is created and stored,
* **And** inspecting coordinator reservations returns an unmodifiable list containing "R-1092",
* **And** the confirmation text contains identifier "R-1092", borrower "STAFF-401", and interval `[2026-11-01, 2026-11-15)`.

#### Scenario 2: Rejection Due to Quota Exhaustion
* **Given** Staff member "STAFF-401" currently holds 5 active equipment loans,
* **When** "STAFF-401" attempts to reserve any available equipment item,
* **Then** the reservation is rejected with message: "Policy violation: active loan quota (5) reached",
* **And** no reservation identifier is allocated,
* **And** the coordinator's stored reservations list remains unchanged.
```

---

## C.2 Definition of Done (DoD) Template

### Engineering Purpose
Establishes a shared, non-negotiable quality contract between all team members. A work item is never moved to the "Done" column on the issue board simply because the code compiles on a developer's local laptop; it must satisfy every gate in the DoD to prevent hidden regression debt.

### Structural Schema

```markdown
# Definition of Done: [Team / Project Name]

### 1. Code Standards & Architecture
* [ ] Code adheres to project packaging conventions and architectural layering.
* [ ] All domain entities protect invariants; collection getters return unmodifiable snapshots (`List.copyOf`).
* [ ] No compiler warnings under `-Xlint:all` and target `--release 17`.
* [ ] Static analysis audit (e.g., PMD) introduces zero high-severity rule violations.

### 2. Testing & Verification Gates
* [ ] Automated unit tests written using the Arrange-Act-Assert (AAA) structure.
* [ ] Edge cases, rejections, and null arguments verified via targeted assertions.
* [ ] Full regression suite passes locally via clean build command (`mvn verify`).
* [ ] Single-fault test check executed: at least one deliberate boundary fault fails the test suite.

### 3. Continuous Integration & Version Control
* [ ] Work developed on a short-lived topic branch originating from `main`.
* [ ] Commits are atomic and formatted with descriptive messages.
* [ ] Branch cleanly rebased onto the latest `main` without merge conflicts.
* [ ] Automated CI pipeline passes all build, test, and package stages.

### 4. Peer Review & Handover
* [ ] Pull request reviewed and approved by at least one teammate.
* [ ] All review discussions and requested changes addressed and resolved.
* [ ] Issue board cards updated with links to merged commit SHAs and verified evidence.
```

### Concrete Filled Example: SE506 Team Lending Engine DoD

```markdown
# Definition of Done: SE506 Equipment Lending Mainline (Iteration Baseline)

### 1. Code Standards & Architecture
* [x] Code resides under `edu.se506.lending` and respects package dependency direction (no cycles).
* [x] Constructors use `Objects.requireNonNull` for mandatory fields; private fields are `final` where immutable.
* [x] No raw framework or infrastructure types leak into `domain` packages.
* [x] Compiles cleanly with `javac --release 17 -Xlint:all` with 0 warnings.

### 2. Testing & Verification Gates
* [x] Unit test methods follow explicit naming: `should[ExpectedBehavior]When[Condition]()`.
* [x] Test doubles for external gateways are hand-written in-memory fakes or interface-only mocks.
* [x] Surefire test invocations increased by the expected count with zero failures or errors.
* [x] Deliberate fault experiment: modifying half-open boundary `<` to `<=` causes at least one test to fail.

### 3. Continuous Integration & Version Control
* [x] Commit history contains no temporary files (`.class`, `target/`, `.DS_Store`).
* [x] Commit message begins with standard tag: `feat(reservation): add staff quota rule`.
* [x] Pull request passes clean execution of `mvn --batch-mode verify`.

### 4. Peer Review & Handover
* [x] Pull request reviewed by assigned peer; review verifies domain invariants and test coverage.
* [x] If requirement changed domain policies, an ADR or traceability row was updated under `docs/`.
```

---

## C.3 Iteration and Capacity Planning Template

### Engineering Purpose
Operationalizes the descriptor's Week 3 capacity planning requirement (Ground Rule G1). Prevents teams from overcommitting by explicitly calculating net engineering hours, adjusting for overhead, decomposing user stories into concrete tasks, and bounding sprint scope.

### Structural Schema

```markdown
# Iteration Planning Sheet: Sprint [N]
* **Sprint Window:** [Start Date] to [End Date]
* **Sprint Goal:** [Single sentence describing the primary architectural or business milestone]

### 1. Team Capacity Calculation
| Team Member | Gross Hours Available | Overhead / Commitments (hours) | Net Available Engineering Hours |
|---|---|---|---|
| [Member 1] | [Hours] | [Classes, other modules] | [Net] |
| [Member 2] | [Hours] | [Classes, other modules] | [Net] |
| [Member 3] | [Hours] | [Classes, other modules] | [Net] |
| **Total Team Capacity** | | | **[Total Net Hours]** |

### 2. Committed Backlog Items
| Story ID | Story Title | Estimated Effort (Hours / Story Points) | Assigned Lead | Priority |
|---|---|---|---|---|
| [US-XX] | [Title] | [Est] | [Name] | [High/Med] |
| [US-YY] | [Title] | [Est] | [Name] | [High/Med] |

### 3. Task Breakdown Structure (WBS)
* **[US-XX] [Story Title]**
  * Task 1: [Design & failing characterisation test] (Est: [X] hrs) - [Owner]
  * Task 2: [Domain class implementation] (Est: [Y] hrs) - [Owner]
  * Task 3: [Integration adapter & peer review] (Est: [Z] hrs) - [Owner]

### 4. Contingency & Buffer
* **Total Committed Task Hours:** [Sum of WBS tasks]
* **Load Factor:** (Total Committed Hours / Total Team Capacity) * 100 = [Target: 75-80%]
* **Buffer Allocation:** [Remaining 20-25% reserved for debugging, unexpected build issues, and code reviews]
```

### Concrete Filled Example: Sprint 4 Capacity Plan

```markdown
# Iteration Planning Sheet: Sprint 4 (Lending Engine Core)
* **Sprint Window:** 2026-10-27 to 2026-11-09
* **Sprint Goal:** Deliver Milestone 2 TDD MVP for student borrowing quotas and email notification gateway.

### 1. Team Capacity Calculation
| Team Member | Gross Hours Available | Overhead / Other Labs (hours) | Net Available Engineering Hours |
|---|---|---|---|
| Alice (Lead Dev) | 20 hrs | 6 hrs | 14 hrs |
| Bob (Dev/Test) | 20 hrs | 8 hrs | 12 hrs |
| Charlie (Dev/Docs) | 20 hrs | 6 hrs | 14 hrs |
| **Total Team Capacity** | **60 hrs** | **20 hrs** | **40 hrs** |

### 2. Committed Backlog Items
| Story ID | Story Title | Estimated Effort | Assigned Lead | Priority |
|---|---|---|---|---|
| US-03 | Student 2-item loan quota rule | 8 hrs | Alice | High |
| US-05 | Half-open overlap detection for loan periods | 6 hrs | Bob | High |
| US-08 | NotificationGateway double and integration | 10 hrs | Charlie | High |
| TECH-02 | Maven Surefire pipeline migration | 6 hrs | Bob | Medium |
| **Total Estimated Backlog Effort** | | **30 hrs** | | |

### 3. Task Breakdown Structure (WBS)
* **US-03 Student Loan Quota:**
  * Task 1: Write parameterised unit tests for student loan limits (AAA) (2 hrs) - Alice
  * Task 2: Implement `StudentReservationRules` strategy class (3 hrs) - Alice
  * Task 3: Wire into `ReservationCoordinator` and run fault check (3 hrs) - Alice
* **US-05 Overlap Detection:**
  * Task 1: Write property tests for `[start, endExclusive)` interval logic (2 hrs) - Bob
  * Task 2: Refactor `LoanPeriod#overlaps` with defensive null checks (2 hrs) - Bob
  * Task 3: Verify adjacent booking compatibility (2 hrs) - Bob
* **US-08 Notification Double:**
  * Task 1: Declare `NotificationGateway` interface in domain (2 hrs) - Charlie
  * Task 2: Implement `FakeNotificationGateway` with message capture (4 hrs) - Charlie
  * Task 3: Configure Mockito interface-only test double (4 hrs) - Charlie

### 4. Contingency & Buffer
* **Total Committed Hours:** 30 hrs
* **Team Net Capacity:** 40 hrs
* **Load Factor:** (30 / 40) * 100 = 75.0%
* **Buffer:** 10 hours (25%) reserved for PR review dialogue, PMD smell resolution, and buffer.
```

---

## C.4 Pull Request and Peer Review Description Template

### Engineering Purpose
Directs reviewer attention to critical architectural boundaries, changes in domain invariants, and verification evidence. Prevents superficial "looks good to me" approvals by requiring authors to supply exact reproduction commands and self-review checklists.

### Structural Schema

```markdown
## Pull Request: [PR-ID] [Concise Summary of Change]

### 1. Context & Motivation
* **Linked Story / Issue:** Closes #[Issue Number]
* **Problem Addressed:** [Why this change is needed; what was missing or flawed previously]

### 2. Summary of Changes
* [Extracted method / new class / altered interface]
* [Tests added or modified]
* [Configuration or documentation changes]

### 3. Invariants & Architectural Impact
* **Domain Invariants Affected:** [Any changes to validation, null handling, or period logic]
* **Package Boundaries:** [List packages modified; verify no illegal dependency cycles]
* **Breaking Changes:** [None / List deprecated signatures or configuration keys]

### 4. Verification Evidence
* **Local Build Command:** `mvn clean verify`
* **Test Results:** [X] passing tests across [Y] test classes (0 failures, 0 errors).
* **Deliberate Fault Test:** [Describe one fault introduced and which test detected it]

### 5. Author Self-Review Checklist
* [ ] I have verified that all collection getters return unmodifiable snapshots.
* [ ] I have added no unpinned third-party library dependencies.
* [ ] I have run static analysis and confirmed zero new PMD warnings.
* [ ] My commit history is rebased and free of merge commits.
```

### Concrete Filled Example: PR-47 Reservation Protection

```markdown
## Pull Request: PR-47 Encapsulate Confirmation Formatting and Protect Reservations List

### 1. Context & Motivation
* **Linked Story / Issue:** Closes #38
* **Problem Addressed:** `ReservationCoordinator` previously exposed its private mutable `List<Reservation>` directly to external callers via `reservations()`, allowing external callers to bypass domain rules by calling `.clear()`. Additionally, confirmation message formatting was tightly coupled inside the main `reserve()` method.

### 2. Summary of Changes
* Extracted private `confirmationFor(Reservation)` helper method inside `ReservationCoordinator`.
* Updated `reservations()` accessor to return `List.copyOf(this.reservations)`, providing an unmodifiable structural snapshot.
* Added `ReservationCoordinatorTest#shouldPreventExternalCallersFromMutatingStoredReservations()` asserting `UnsupportedOperationException` when calling `.add()` or `.clear()` on the returned list.

### 3. Invariants & Architectural Impact
* **Domain Invariants Affected:** Internal list integrity is now defended against external caller mutation.
* **Package Boundaries:** All changes contained within `edu.se506.lending.application`.
* **Breaking Changes:** None. Public API method signatures remain identical.

### 4. Verification Evidence
* **Local Build Command:** `mvn --batch-mode verify`
* **Test Results:** 34 passing test invocations (0 failures, 0 errors) in 1.4 seconds.
* **Deliberate Fault Test:** Reverting `List.copyOf(reservations)` to `reservations` causes `shouldPreventExternalCallersFromMutatingStoredReservations` to fail immediately.

### 5. Author Self-Review Checklist
* [x] I have verified that all collection getters return unmodifiable snapshots.
* [x] I have added no unpinned third-party library dependencies.
* [x] I have run static analysis and confirmed zero new PMD warnings.
* [x] My commit history is rebased and free of merge commits.
```

---

## C.5 Architecture Decision Record (ADR) Template

### Engineering Purpose
Captures significant architectural choices in lightweight, version-controlled Markdown files stored under `docs/`. Preserves institutional memory by documenting the problem context, competing options considered, explicit trade-offs, and consequences.

### Structural Schema

```markdown
# ADR-[NUMBER]: [Short Title of Architectural Decision]

* **Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
* **Deciders:** [Names of team members / architect]
* **Date:** [YYYY-MM-DD]

### 1. Context and Problem Statement
[Describe the technical dilemma, changing requirement, or architectural friction. What forces are in conflict (e.g., testability vs. runtime complexity, flexibility vs. cognitive load)?]

### 2. Decision Drivers
* [Driver 1: e.g., Need to test external service without network dependencies]
* [Driver 2: e.g., Backwards compatibility for existing student accounts]
* [Driver 3: e.g., Execution speed in automated CI pipeline]

### 3. Options Considered
* **Option 1:** [Description of option]
  * *Pros:* [Advantages]
  * *Cons:* [Disadvantages]
* **Option 2:** [Description of option]
  * *Pros:* [Advantages]
  * *Cons:* [Disadvantages]

### 4. Decision Outcome
**Chosen Option:** [Option X], because [primary justification grounded in SOLID, testability, or delivery principles].

### 5. Consequences & Trade-offs
* **Positive Consequences:** [What improves: e.g., test isolation, decoupling]
* **Negative Consequences / Technical Debt:** [What becomes harder: e.g., additional indirection, manual double maintenance]
* **Removal / Evolution Condition:** [Under what future condition will this decision be re-evaluated or retired?]
```

### Concrete Filled Example: ADR-013 Feature Flag for Visiting Researchers

```markdown
# ADR-013: Introducing VisitorGate Feature Flag for Visiting Researcher Workflows

* **Status:** Accepted
* **Deciders:** Alice, Bob, Charlie (SE506 Team Lending)
* **Date:** 2026-11-12

### 1. Context and Problem Statement
In Iteration 6 (Chapter 13), the university requested a new requirement (CR-12): allow visiting researchers to borrow specialized equipment subject to faculty sponsor verification. However, the university directory service API is undergoing maintenance and will not be stable in production until December. We need to implement and test the complete visiting researcher feature set without risking regressions or outages in current student borrowing workflows.

### 2. Decision Drivers
* Allow continuous delivery of student borrowing enhancements without branch divergence.
* Test both enabled and disabled paths in automated CI suites.
* Provide an immediate operational kill-switch if the external directory service fails.

### 3. Options Considered
* **Option 1: Long-Lived Feature Branch.** Maintain visitor code on a separate Git branch until the directory service is ready.
  * *Pros:* Zero risk to production code on `main`.
  * *Cons:* Severe merge conflict risk; violates Continuous Integration principles; blocks automated contract testing.
* **Option 2: Runtime Feature Flag (`VisitorGate`).** Merge code into `main` behind an in-memory Boolean flag defaulting to `false`.
  * *Pros:* Single branch flow; both paths verified in CI; instant operational control via configuration.
  * *Cons:* Introduces temporary branching logic; creates technical debt that must be cleaned up later.

### 4. Decision Outcome
**Chosen Option:** Option 2 (`VisitorGate`). The gate wraps the coordinator check: if the flag is disabled, visitor requests are rejected immediately with a friendly policy explanation.

### 5. Consequences & Trade-offs
* **Positive Consequences:** Both paths are fully tested in Surefire unit and integration suites (232 passing invocations). Integration pipeline remains green.
* **Negative Consequences / Technical Debt:** The coordinator contains a conditional check that must be removed once the feature is universally active.
* **Removal Condition:** Per Chapter 14 roadmap, `VisitorGate` will be deleted in release `v0.15.0` once the live directory client achieves 99.9% uptime over two consecutive sprints.
```

---

## C.6 Sprint Retrospective and Action Note Template

### Engineering Purpose
Operationalizes the team reflection practices from Chapter 14. Transforms vague complaints into actionable, auditable improvement cards on the team issue board, linking qualitative team experience to measurable flow metrics.

### Structural Schema

```markdown
# Sprint Retrospective: Sprint [N]
* **Date:** [YYYY-MM-DD]
* **Facilitator:** [Name (rotated each sprint)]
* **Participants:** [Team members present]

### 1. Delivery & Flow Metrics Snapshot
* **Planned Stories:** [X] | **Completed Stories:** [Y]
* **Throughput:** [Z] pull requests merged
* **Average PR Cycle Time:** [Hours / Days from open to merge]
* **Build Health:** [Number of broken CI builds encountered during sprint]

### 2. Qualitative Observations
#### What Went Well (Strengths to Preserve)
* [Specific practice, tool, or collaboration technique that worked effectively]

#### What Caused Friction or Blockers (Pains & Bottlenecks)
* [Specific delay, tooling obstacle, or communication breakdown]

### 3. Root Cause Diagnosis (5 Whys)
* **Observed Problem:** [e.g., Pull requests remained unmerged for an average of 3 days]
  1. *Why?* Teammates only reviewed code on Sunday evenings.
  2. *Why?* Developers were focused entirely on writing their own story tasks.
  3. *Why?* The team had no agreed policy on review priority.
  4. *Why?* The Definition of Done did not include review turnaround expectations.
  5. *Root Cause:* Absence of an explicit team Working Agreement on pull request review SLAs.

### 4. Actionable Improvement Items (Max 2-3 per sprint)
| Action Item | Issue Board Card | Assignee | Target Completion Date | Success Criteria |
|---|---|---|---|---|
| [Actionable task] | #[Card ID] | [Name] | [Date] | [Measurable result] |
```

### Concrete Filled Example: Sprint 3 Retrospective Note

```markdown
# Sprint Retrospective: Sprint 3 (SE506 Lending Team)
* **Date:** 2026-11-05
* **Facilitator:** Charlie
* **Participants:** Alice, Bob, Charlie

### 1. Delivery & Flow Metrics Snapshot
* **Planned Stories:** 4 | **Completed Stories:** 3 (US-08 carried over)
* **Throughput:** 6 pull requests merged
* **Average PR Cycle Time:** 38 hours
* **Build Health:** 2 CI build failures (both caused by unpinned plugin versions)

### 2. Qualitative Observations
#### What Went Well
* Extracting `LoanPeriod` into an immutable record eliminated three date-handling bugs.
* Pair programming between Alice and Bob accelerated test double setup in Chapter 7.

#### What Caused Friction
* PR reviews stalled because pull requests contained both formatting changes and domain logic.
* CI failed intermittently on Windows due to shell script line endings (CRLF vs LF).

### 3. Root Cause Diagnosis (5 Whys)
* **Observed Problem:** CI scripts failed with `invalid option: set -euo pipefail`.
  1. *Why?* The shell script contained Windows CRLF line endings.
  2. *Why?* Git checked out files on Windows using default auto-crlf settings.
  3. *Why?* The repository lacked a `.gitattributes` configuration file.
  4. *Why?* Setup was performed manually across different machines without a shared baseline.
  5. *Root Cause:* Missing version-controlled line-ending normalization in repository root.

### 4. Actionable Improvement Items
| Action Item | Issue Board Card | Assignee | Target Completion | Success Criteria |
|---|---|---|---|---|
| Add `.gitattributes` with `*.sh text eol=lf` | #52 | Bob | 2026-11-06 | Clean checkout passes `scripts/check-setup.sh` on all machines |
| Split PRs: zero formatting changes in feature PRs | #53 | Alice | 2026-11-08 | Average PR review turnaround drops below 24 hours |
```

---

## C.7 AI Assistance Verification Record Template

### Engineering Purpose
Directly fulfills the eight-part audit trail required by Chapter 15 Section 15.8 and Ground Rule G4/G11. Proves human engineering accountability by documenting task scope, prompts, rejected candidate outputs, manual fixes, and independent test evidence.

### Structural Schema

```markdown
# AI Verification Record: [AI-REC-ID] [Task Title]

* **Date:** [YYYY-MM-DD]
* **Engineer:** [Name]
* **Task Owner / Approved Story:** [User Story ID / Task Reference]

### 1. Task Definition & Scope
* **Objective:** [Precise implementation or refactoring goal]
* **Permitted Scope:** [Exact boundaries: what classes may be touched and what is forbidden]

### 2. Tool, Model & Environment
* **Tool / Interface:** [e.g., Local CLI / IDE extension / Browser portal]
* **Model Version:** [e.g., Anthropic Claude 3.5 Sonnet / OpenAI GPT-4o / Constructed Fixture]
* **Baseline Settings:** [e.g., Temperature 0.0, target Java 17 LTS]

### 3. Context Provided
* **Files / Snippets Provided:** [List exact files or interfaces shared in prompt]
* **Omissions & Privacy Safeguards:** [What was withheld (e.g., credentials, institutional IDs) and why]

### 4. Candidate Output Received
#### Attempt 1: [Status: REJECTED | ACCEPTED WITH MODIFICATIONS]
[Paste candidate code or test snippet]

#### Attempt 2 (if applicable): [Status: REJECTED | ACCEPTED]
[Paste revised candidate snippet]

### 5. Decision & Rejection Rationale
* **Attempt 1 Evaluation:** [Identify hallucinated methods, broken boundary conditions, or violated invariants]
* **Specific Flaws Found:** [e.g., Used Java 21 `List#getFirst()` instead of Java 17; missed null check]

### 6. Manual Modifications Made
[Explain exact manual edits made by the engineer before committing]

### 7. Independent Verification Executed
* **Compiler Check:** `javac --release 17 -Xlint:all` (Result: [Pass/Fail])
* **Automated Test Run:** `mvn test -Dtest=[TestClass]` (Result: [X] invocations passed)
* **Single-Fault Verification:** [Describe deliberate fault injected to confirm test sensitivity]

### 8. Limitations & Boundary Statement
[State what the tests do not prove: e.g., thread safety unverified; assumes single-node in-memory storage]
```

### Concrete Filled Example: AI Verification for AvailabilityFinder

```markdown
# AI Verification Record: AI-REC-004 AvailabilityFinder Extraction

* **Date:** 2026-10-13
* **Engineer:** Alice
* **Task Owner / Approved Story:** US-05 Equipment Availability Query

### 1. Task Definition & Scope
* **Objective:** Generate a cohesive query helper `AvailabilityFinder` that filters overlapping reservations for a specified item and target period.
* **Permitted Scope:** New package-private helper class in `edu.se506.lending.domain`. No changes to `Reservation` or `LoanPeriod` signatures.

### 2. Tool, Model & Environment
* **Tool / Interface:** Constructed Teaching Fixture (per Blueprint G11 offline protocol)
* **Model Version:** `constructed-to-illustrate-v1`
* **Baseline Settings:** Java 17 LTS target, zero external dependencies.

### 3. Context Provided
* **Files Provided:** `Reservation.java`, `LoanPeriod.java` interface, and interval definition `[start, endExclusive)`.
* **Omissions:** Omitted database infrastructure and user identifiers to minimize context size.

### 4. Candidate Output Received
#### Attempt 1: [Status: REJECTED]
```java
public class AvailabilityFinder {
    public boolean isAvailable(List<Reservation> list, String itemId, LocalDate start, LocalDate end) {
        return list.stream()
            .filter(r -> r.itemId().equals(itemId))
            .noneMatch(r -> r.period().start().isBefore(end) && r.period().endExclusive().isAfter(start));
    }
}
```

### 5. Decision & Rejection Rationale
* **Attempt 1 Rejected Because:**
  1. Failed to validate inputs: missing `Objects.requireNonNull` for `itemId`, `start`, `end`.
  2. Boundary Error: The stream condition uses `start.isBefore(end)` which assumes `end` is inclusive, violating the domain's strict end-exclusive half-open interval rule.
  3. Leaked Types: Takes raw `LocalDate` pairs rather than accepting a cohesive `LoanPeriod` value object.

### 6. Manual Modifications Made
* Refactored signature to accept `(List<Reservation> existing, String itemId, LoanPeriod requestedPeriod)`.
* Replaced raw boolean math with domain delegation: `r.period().overlaps(requestedPeriod)`.
* Added constructor defensive null checks.

### 7. Independent Verification Executed
* **Compiler Check:** `javac --release 17 -Xlint:all` passed with 0 warnings.
* **Automated Test Run:** `mvn test -Dtest=AvailabilityFinderTest` (6 invocations passed in 0.12s).
* **Fault Injection:** Changing `overlaps` to permit identical start/end dates caused 2 tests to fail immediately.

### 8. Limitations & Boundary Statement
Verification confirms single-thread collection filtering. Does not prove thread safety under concurrent modifications; assumes the provided list is an unmodifiable snapshot.
```

---

## C.8 Known Issues and Technical Debt Register Template

### Engineering Purpose
Fulfills the handover requirement in Chapter 14 Section 14.5 and Appendix E. Prevents teams from concealing defects by maintaining an honest, auditable catalog of deferred work, legacy discrepancies, and architectural compromises.

### Structural Schema

```markdown
# Known Issues and Technical Debt Register: [Project Name]

### [ISSUE-ID]: [Short Descriptive Title]
* **Severity / Priority:** [Low | Medium | High | Blocker]
* **Affected Component:** [Class name, package, or script path]
* **Observed Anomaly / Defect:** [Clear explanation of incorrect or surprising behavior]
* **Root Cause & Context:** [Why this behavior occurs in the code]
* **Reason for Deferral:** [Why it was not fixed in the current milestone: e.g., backwards compatibility, time box]
* **Safety / Characterisation Guardrail:** [The specific automated test that prevents further regression]
* **Remediation Plan:** [Concrete strategy and planned future release for complete remediation]
```

### Concrete Filled Example: SE506 Handover Debt Register

```markdown
# Known Issues and Technical Debt Register: Campus Equipment Lending System (Release v0.14.0)

### KI-01: Legacy Fine Calculation Category Discrepancy (SD-11-1)
* **Severity / Priority:** Medium
* **Affected Component:** `edu.se506.lending.legacy.LegacyOverdueReporter`
* **Observed Anomaly:** The legacy overdue report calculates fines for overdue visitor accounts using the fallback "other category" rate ($2.00/day) instead of the updated policy rate ($1.50/day).
* **Root Cause & Context:** An unrefactored conditional block in the legacy reporting routine was written prior to the introduction of the `VISITOR` borrower enum.
* **Reason for Deferral:** Deferred to preserve backwards compatibility with historical financial exports and existing characterisation tests.
* **Safety Guardrail:** Protected by `LegacyOverdueReporterTest#shouldPreserveHistoricalVisitorCalculationQuirk()`.
* **Remediation Plan:** Scheduled for extraction into polymorphic fee calculators in Milestone 5 under Issue #78.

### KI-02: Reservation Count Evaluates Archived Loans (SD-12)
* **Severity / Priority:** Low
* **Affected Component:** `edu.se506.lending.application.ReservationCoordinator`
* **Observed Anomaly:** Borrowers who have returned equipment still have those records counted against their active loan quota until a manual system restart occurs.
* **Root Cause & Context:** The coordinator currently stores all records in an in-memory list without an explicit archiving or pruning seam.
* **Reason for Deferral:** In-memory storage is an educational simplification; true lifecycle archiving depends on database repository introduction.
* **Safety Guardrail:** Verified by `ReservationCoordinatorTest#quotaCountsAllRetainedRecords()`.
* **Remediation Plan:** Implement `ArchivedLoanFilter` when persistent database adapters are added.
```

---

## C.9 Primary Sources and Standards

The engineering templates in this appendix reflect standard software engineering methodologies and industry literature:

1. **Nygard, Michael.** "Documenting Architecture Decisions." *Cognitect Blog*, 2011. The original Architecture Decision Record (ADR) format.
2. **Rubin, Kenneth S.** *Essential Scrum: A Practical Guide to the Most Popular Agile Process.* Addison-Wesley, 2012. Reference authority for Definitions of Done, story decomposition, and capacity planning.
3. **Fowler, Martin.** *Refactoring: Improving the Design of Existing Code.* 2nd ed., Addison-Wesley, 2018. Rationale for self-documenting code, small commits, and characterisation testing.
4. **Beck, Kent.** *Test-Driven Development: By Example.* Addison-Wesley, 2002. Standards for Arrange-Act-Assert structure and executable specifications.
5. **Humble, Jez, and David Farley.** *Continuous Delivery.* Addison-Wesley, 2010. Foundations for feature flags, deployment pipelines, and pull request hygiene.
6. **Martin, Robert C.** *Clean Code: A Handbook of Agile Software Craftsmanship.* Prentice Hall, 2008. Conventions for meaningful naming, small functions, and clear team agreements.