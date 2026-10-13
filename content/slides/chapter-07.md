---
title: "Chapter 7: Testing as a Design Practice"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 70
type: slides
layout: page
---

# Chapter 7: Testing as a Design Practice
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **7.1 Behaviour and test evidence**
  * Executable availability examples; observe result and state together.
* **7.2 Test anatomy and Arrange-Act-Assert**
  * Assertions that can be wrong; fresh, small fixtures.
* **7.3 Red-green-refactor**
  * One recorded cycle, and why the first failure must be the intended one.
* **7.4 Boundaries, controlled time and a bounded lending flow**
  * Boundary values, a controlled clock, a bounded lending flow.

---

## Chapter Roadmap (2 of 3)

* **7.5 Dummies, stubs, fakes, spies and mocks**
  * Name the role a substitute plays, then add Mockito for one interaction.
* **7.6 Testability and design feedback**
* **7.7 Weak or brittle tests**
  * Coverage is not correctness; a mutation experiment; a mutant that survives.
* **7.8 Milestone 2 evidence**

---

## Chapter Roadmap (3 of 3)

* **7.9 AI in practice:** separate implementation from expected behaviour.
* **7.10 Common mistakes**
* **7.11 Practical activity**
  * Steps 1 to 9; steps 8 and 9 on your Team project.
* **7.12 Review questions and midterm practice**
  * A five-task practice set for Chapters 2 to 7.
* **Summary and next chapter**
  * Chapter 8: construction and compatibility patterns.

---

## Learning Outcomes (1 of 2)

By the end of this chapter, you should be able to:

1. **Translate acceptance examples** into focused tests with meaningful expected outcomes.
2. **Demonstrate red-green-refactor** and explain why the first failure is the intended one.
3. **Control data, time and collaborators** to make tests repeatable.

---

## Learning Outcomes (2 of 2)

4. **Choose a useful test double** and distinguish state checks from interaction checks.
5. **Diagnose weak or brittle tests** and explain the limits of passing evidence.
6. **Assemble MVP, testing, demonstration and retrospective evidence** for Milestone 2.

---

## Module Connection

* Supports **LO3**; **Milestone 2** preparation.
* The **midterm practice** near the end draws on Chapters 2 to 7 (Weeks 1 to 6).
* No new assessment weights, deadlines or marking rules.
* Readings: the testing chapter and "A Programming Episode" in Martin, and Part I of Beck.

---

## Milestone 2 Checklist: Use It From the Start (1 of 2)

Milestone 2 falls in this week. By your demonstration you need:

1. A **working MVP flow** that someone else can run from written instructions.
2. **Acceptance examples mapped to named tests.**
3. **One red-green-refactor sequence** recorded from your own code.
4. A short **rationale for your object-oriented and SOLID choices**.

* Start with items 1 and 3.

---

## Milestone 2 Checklist (2 of 2)

5. A **justified test double or controlled clock**.
6. A **build result** for the revision you demonstrate.
7. **Real review feedback** and a short retrospective with a next action.
8. A statement of **what the MVP does not do**.

* Section 7.8 explains each item.
* The checklist is preparation. **The module leader's approved Milestone 2 requirements remain authoritative.**

---

## Entry Checkpoint and Tools

* **Entry:** Chapter 6's Java 17 application, explicit collaborator construction, student and staff policies, local notification outputs. The earlier executable checks remain available.
* **New tools:** **Maven, JUnit Jupiter and Mockito**, with an explicitly versioned configuration in the companion.
* Core reading 7.1 to 7.8. Section 7.5 introduces **hand-written doubles before Mockito**.
* Lab: steps 1 to 6, 8 and 9. Steps 1 to 6 on the Book project; **steps 8 and 9 on your Team project**.

---

## Opening Scenario: A Green Build That Is Wrong

* A developer adds the availability enquiry and reports **the build is green**.
* At the demonstration the officer asks about a **reserved camera** and receives **"available"**.
* The test had checked only that the method **returned a boolean without throwing**.

---

## Three Plausible, Wrong Implementations

* One passes because the test only checks "no exception".
* Another **rejects every enquiry** and still passes the overlap example.
* A third **accepts adjacent dates incorrectly** because it treats the earlier reservation's end as inclusive.
* Each looks plausible when its tests **ask incomplete questions**.

---

## What Testing Is For

* Not to **accumulate green indicators**.
* To create **evidence about specific behaviour**, reveal misunderstandings and **support changes in design**.
* This chapter turns the availability examples of Chapters 3 and 4 into executable tests, demonstrates **a complete red-green-refactor cycle**, and uses controlled collaborators.

---

# 7.1 Behaviour and Test Evidence
### Start from a promise, not an implementation

---

## The Examples Are Now Implemented

* Chapter 3 proposed **US-02**: an officer inspects availability without creating a reservation.
* Chapter 4 refined five acceptance examples.
* Now they become **executable**.

---

## AQ Examples (1 of 2)

| Example | Setup and action | Required observation |
|---|---|---|
| AQ-01 | Empty schedule; enquire about CAM1 for a valid interval | Available; records and notifications unchanged |
| AQ-02 | CAM1 reserved `[20 Oct, 22 Oct)`; enquire `[21 Oct, 23 Oct)` | Unavailable; no side effects |
| AQ-03 | Same booking; enquire `[22 Oct, 23 Oct)` | Available because the end is exclusive |

---

## AQ Examples (2 of 2)

| Example | Setup and action | Required observation |
|---|---|---|
| AQ-04 | Same booking; enquire about MIC1 for the same interval | Available for the different fixture item |
| AQ-05 | Equal or reversed interval | Identifiable invalid-input outcome; no side effects |

* All dates are in 2026.

---

## The API Decision

* The selected Java API is **`isAvailable(itemId, start, endExclusive)`**, returning a boolean for a valid interval.
* **Blank or null item identifier:** `IllegalArgumentException`.
* **Equal or reversed dates:** `IllegalArgumentException`.
* **Null dates:** `NullPointerException` through `LoanPeriod`.
* These choices **settle the earlier open API question** for this teaching checkpoint.

---

## What Availability Means

* **No conflicting reservation** for the item and interval.
* It does **not** mean a particular borrower is eligible.
* The query accepts any positive interval, **including more than seven days**; student limits apply when a reservation is requested.
* It does not know whether an item is **physically on loan** or **present in a real catalogue**.

---

## Observe Result and State Together

* The overlap example checks: a **false** result, **unchanged reservations**, **unchanged recorded notifications**.
* An implementation that calls `reserve` and undoes it would **also send a notice**: the unchanged-notices check exposes it.
* One that adds a temporary record directly and removes it again leaves **nothing for a sequential test to see**.
* We **reject that design by reading it**, not by testing it.

---

## Choose Observations by the Promise

* For an immutable snapshot, **compare the before and after lists**: they expose replacement, deletion or reordering. Checking only the **count** misses changes to contents.
* Inspecting a private list through reflection **binds the test to representation** when a public snapshot already exposes the behaviour.
* A separate example confirms that an enquiry **does not consume the next reservation identifier**.

---

## The Expected Answer Must Be Independent

* It must come from **an agreed example or rule**.
* Calculating it by calling **the same method under test is circular**.
* Copying the implementation's overlap expression into a test **reproduces its mistake**.
* Concrete dates with an independently understood boundary are a better starting point.

---

## Introduce a Runner Without Losing Earlier Evidence

* **JUnit** provides annotations, assertions and reporting. **Maven** compiles and runs it through the configured **Surefire** plugin.

```bash
mvn --batch-mode verify
```

* The existing `scripts/check.sh` now **delegates to that command**.
* A `LegacyRegressionTest` invokes the **four older `main` methods** from four JUnit tests. A class merely placed in a test directory would **not** run its `main`.

---

## Counts Are Not Interchangeable

* The wrapper reports **four JUnit cases**.
* Their internal output still reports: **34** Chapter 2 checks, **five** Chapter 3 example groups, **44** Chapter 5 checks, **28** Chapter 6 checks.
* Do not merge those counts as if they were identical units.
* The useful question: **which behaviours execute, and what failures reach the build?**

---

# 7.2 Test Anatomy and Arrange-Act-Assert
### A readable argument

---

## Arrange, Act, Assert

* **Arrange:** establish the relevant state.
* **Act:** perform the operation being examined.
* **Assert:** inspect the outcome.
* A reading aid, **not a requirement** of exactly one statement per phase.

---

## The First Availability Test

```java
boolean available = coordinator.isAvailable(
        "CAM1", start.plusDays(1), start.plusDays(3));

assertAll(
        () -> assertFalse(available, "An overlapping item must be unavailable"),
        () -> assertEquals(recordsBefore, coordinator.reservations()),
        () -> assertEquals(noticesBefore, inbox.received()));
```

* Arranged: a two-day CAM1 reservation, with snapshots of records and notices.

---

## A Name That Says What Broke

* `overlappingEnquiryIsUnavailableWithoutChangingRecordsOrNotifying`
* A precise name reduces the need to **reverse-engineer why a fixture contains particular values**.
* Avoid `test1` or `worksCorrectly`: when the test fails, the name **should tell another developer which promise was broken**.

---

## How Many Assertions?

* Several assertions can belong together when they **describe one outcome**.
* Splitting this test into three methods with identical setup may **obscure the relationship** between a query result and its non-mutation promise.
* One giant method for every query, loan and notification scenario is the opposite problem: **a failure is hard to locate**.

---

## Use Assertions That Can Be Wrong

* `assertTrue(true)` **cannot reject an implementation**.
* "No exception occurred" may be valuable for a specific promise, but it **does not establish availability**.
* A meaningful assertion must **distinguish the behaviour you want from a plausible defect**.

---

## Exceptional Outcomes

* Use `assertThrows` for a specified exceptional outcome, and **inspect state afterwards** when preservation matters.
* A catch block that **prints an error and continues** does not establish that the right exception occurred.
* Wrapping a test in a broad catch can **turn a failure into a false success**.

---

## Parameterised Tests

* Small tables of policy boundaries: each row states **category, count, days and expected decision**.
* The runner reports **individual invocations**, so a particular boundary failure is visible.
* The table is **authored from the rule**, not generated by evaluating the policy itself.

---

## The Policy Table (`BorrowingPolicyTest`)

| Category | Count | Days | Expected |
|---|---:|---:|---|
| STUDENT | 0 | 1 | true |
| STUDENT | 2 | 7 | true |
| STUDENT | 3 | 1 | false |
| STUDENT | 0 | 8 | false |
| STAFF | 4 | 14 | true |
| STAFF | 5 | 1 | false |
| STAFF | 0 | 15 | false |

* Plus three more rows: a negative count and two non-positive durations. **Ten rows** in all.

---

## Keep Setup Independent and Small

* Each scenario constructs **fresh mutable collaborators** unless sharing is part of the behaviour.
* A **static coordinator reused across tests** makes results depend on which test ran first: the same test may pass alone and fail in the suite.
* Prefer **the smallest fixture** that makes the scenario meaningful, using real simple domain objects.

---

# 7.3 Red-Green-Refactor
### Make the missing behaviour visible

---

## TDD in Short Cycles

* Express an expected behaviour.
* **Observe its failure.**
* Implement enough to satisfy it.
* **Improve structure while preserving the tests.**
* A development **sequence**, not a label for tests added after a complete feature.

---

## The Cycle and Its Decision Point

<!--svg:ch07-tdd-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 362" role="img" aria-label="Red, green, refactor: write a behaviour test and run it. If the intended assertion does not fail, inspect setup, test or existing behaviour and run again. If it fails, implement just enough to pass, confirm green, then refactor and run the regression tests. If they pass, take the next behaviour; if they fail, repair the refactoring." style="display:block;width:100%;height:calc(var(--u) * 36.20);margin:0 auto">
<defs><marker id="ch07-tdd-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-tdd-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-tdd-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-tdd-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-tdd-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="25.0" width="175.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="97.5" y="50.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Write a</text>
<text x="97.5" y="73.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">behaviour test</text>
<rect x="225.0" y="25.0" width="150.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="300.0" y="62.1" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Run the test</text>
<polygon points="532.5,8.0 640.0,56.0 532.5,104.0 425.0,56.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="532.5" y="51.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Intended assertion</text>
<text x="532.5" y="72.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">fails?</text>
<rect x="425.0" y="195.0" width="215.0" height="62.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="532.5" y="221.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Inspect setup, test or</text>
<text x="532.5" y="241.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">existing behaviour</text>
<rect x="690.0" y="25.0" width="170.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="775.0" y="51.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Implement enough</text>
<text x="775.0" y="72.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">to pass</text>
<rect x="690.0" y="140.0" width="170.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="775.0" y="171.1" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Confirm green</text>
<rect x="690.0" y="270.0" width="170.0" height="62.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="775.0" y="296.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">Refactor and run</text>
<text x="775.0" y="317.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">regression tests</text>
<path d="M185.0,56.0 L225.0,56.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-tdd-arr)"/>
<path d="M375.0,56.0 L425.0,56.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-tdd-arr)"/>
<path d="M640.0,56.0 L690.0,56.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-tdd-arr)"/>
<text x="665.0" y="44.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Yes</text>
<path d="M532.5,104.0 L532.5,195.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-tdd-arr)"/>
<text x="448.0" y="158.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">No</text>
<path d="M425.0,226.0 L300.0,226.0 L300.0,87.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-tdd-arr)"/>
<path d="M775.0,87.0 L775.0,140.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-tdd-arr)"/>
<path d="M775.0,190.0 L775.0,270.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-tdd-arr)"/>
<path d="M690.0,301.0 L97.0,301.0 L97.5,87.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-tdd-arr)"/>
<text x="330.0" y="292.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">tests pass: next behaviour</text>
<text x="745.0" y="354.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="middle" font-style="italic">tests fail: repair the refactoring</text>
</svg>
</div>
<!--/svg-->

---

## The Starting Point for Red

* The worked cycle begins with a compiling `isAvailable` that **validates its arguments but always returns true**.
* This supplies an API for the first test **without pretending to implement overlap detection**.

```bash
mvn --batch-mode -Dtest=AvailabilityTddTest test
```

---

## The Observed Red Result

* **One executed test, one failure, zero errors.**
* The assertion reports that an overlapping item was expected to be unavailable but the method **returned true**.
* The unchanged-state assertions **do not fail**.
* That makes the missing behaviour **precise**.

---

## Not Every Failure Is Red

* A missing library, a syntax error or an unresolved dependency is **not** this red result.
* Those failures **prevent or interrupt the experiment**.
* Fix the environment or compilation issue, then rerun until **the intended assertion exposes the missing behaviour**.

---

## Green: Implement the Required Decision

* Construct a `LoanPeriod`, inspect existing reservations, **return false if the same item has an overlapping period**, otherwise true.
* It does **not** call `reserve`, allocate an identifier or invoke the sender.
* The same test then passes: useful evidence for that example, **not permission to stop thinking**.

---

## An Always-False Method Passes Too

* An implementation that **always returned false** would also satisfy the first overlap test.
* More examples are needed to **distinguish overlap rejection from universal rejection**:
  * empty schedule,
  * adjacency,
  * different item,
  * invalid input,
  * identifier preservation,
  * eligibility distinction.

---

## Refactor: Share Conflict Detection

* The green query **duplicates conflict scanning** already in `reserve`.
* Extract a private `hasConflict(itemId, requestedPeriod)` used by both.
* `reserve` keeps its validation and eligibility order and still stores exactly one record.
* The query uses the same conflict meaning **without acquiring reservation's mutation or borrower-limit behaviour**.

---

## After the Extraction

* Rerun the TDD test and the legacy bridge.
* Observed: **five JUnit cases** (the new test and four legacy wrappers) **pass**.
* The extraction is justified **because both callers need the same meaning of a conflict**, not because duplicated text is forbidden.
* If one caller later needs stock or maintenance status, **do not force that meaning into the helper**.

---

## Preserve a Traceable Sequence

* The companion includes **red, green and refactored** coordinator snapshots with their commands and results.
* In a team repository, separate commits or a recorded diff sequence give equivalent evidence.
* Keep **the actual failing assertion and correction**, not just a screenshot saying tests passed.
* A wrong implementation supplied **after the fact** shows test sensitivity. It does not reconstruct a test-first history that never happened.

---

# 7.4 Boundaries, Controlled Time and a Bounded Lending Flow
### Edges that carry meaning, and time under control

---

## Test the Edges That Carry Meaning

* **Borrowing:** a student with two records may add a third; one with three may not. **Seven days** allowed, **eight** not. Staff: **five** records, **fourteen** days.
* **Overlap:** an enquiry beginning at the exclusive end is available; **equal start and end is invalid**; a different item does not conflict because dates match.
* Each example distinguishes **a plausible error in the rule**.

---

## Boundary Selection Is Reasoning

* It is **not** an exhaustive proof over every integer or date.
* Combine examples with **source inspection** and, where justified, broader techniques later.
* Do not introduce a **coverage target** as a substitute for an explanation of the risks.

---

## Control Time Where Behaviour Depends on Today

* Availability needs **no clock** in this checkpoint.
* The new **loan checkout** does: checkout is allowed only on a date **within the confirmed reservation's half-open period**.
* `LoanService` receives a Java **`Clock`** and uses `LocalDate.now(clock)`.
* Tests use **`Clock.fixed`**, or a small controlled clock when the scenario must advance.

---

## Instant and Zone

<!--svg:ch07-clock-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 270" role="img" aria-label="One instant, 19 October 22:30 UTC, gives the local date 19 October in the UTC zone and 20 October in the Asia/Baghdad zone, so a test must state both the instant and the zone." style="display:block;width:100%;height:calc(var(--u) * 27.00);margin:0 auto">
<defs><marker id="ch07-clock-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-clock-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-clock-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-clock-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-clock-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="95.0" width="250.0" height="80.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="135.0" y="129.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">Instant</text>
<text x="135.0" y="152.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">2026-10-19 22:30 UTC</text>
<rect x="420.0" y="25.0" width="250.0" height="80.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="545.0" y="59.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Zone UTC</text>
<text x="545.0" y="82.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">local date: 19 October</text>
<rect x="420.0" y="165.0" width="250.0" height="80.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="545.0" y="200.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Zone Asia/Baghdad (UTC+3)</text>
<text x="545.0" y="221.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">local date: 20 October</text>
<path d="M260.0,119.0 L340.0,119.0 L340.0,65.0 L420.0,65.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-clock-arr)"/>
<path d="M260.0,151.0 L340.0,151.0 L340.0,205.0 L420.0,205.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch07-clock-arr)"/>
<text x="765.0" y="70.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="600" fill="#1d588c" text-anchor="middle">LocalDate.now(clock)</text>
<text x="765.0" y="92.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">needs both</text>
</svg>
</div>
<!--/svg-->

---

## Why the Zone Matters

* A fixed UTC instant **does not define a local date without a zone**.
* One test uses **19 October 22:30 UTC** with **Asia/Baghdad** and expects the local checkout date **20 October**.
* A deliberate example of zone-sensitive conversion, **not reliance on the machine's default zone**.
* Do not wait until midnight or call `Thread.sleep`: **change the supplied clock.**

---

## A Bounded Lending Flow

* The MVP increment adds a small `LoanService` linked to one coordinator **in the same process**.
* It records checkout and return against a **confirmed reservation**.
* A `Loan` is a Java **record** with validated identifiers, a checkout date and an optional return date. **Null means one documented thing: the loan is active.**
* Records give concise value-oriented data, but **validation still has to be written**.

---

## The `Loan` Record

```java
public record Loan(String reservationId, String borrowerId, String itemId,
                   LocalDate borrowedOn, LocalDate returnedOn) {
    public Loan {
        if (reservationId == null || reservationId.isBlank()
                || borrowerId == null || borrowerId.isBlank()
                || itemId == null || itemId.isBlank()) {
            throw new IllegalArgumentException("Loan identifiers must not be blank.");
        }
        Objects.requireNonNull(borrowedOn, "borrowedOn");
        if (returnedOn != null && returnedOn.isBefore(borrowedOn)) {
            throw new IllegalArgumentException("Return cannot precede checkout.");
        }
    }
    public boolean active() { return returnedOn == null; }
}
```

---

## `LoanService.checkOut`

```java
LocalDate today = LocalDate.now(clock);
if (today.isBefore(reservation.period().start())
        || !today.isBefore(reservation.period().endExclusive())) {
    throw new IllegalStateException("Checkout must be within the reservation period.");
}
boolean itemAlreadyOut = loans.values().stream()
        .anyMatch(loan -> loan.active() && loan.itemId().equals(reservation.itemId()));
if (itemAlreadyOut) throw new IllegalStateException("Item is already on loan.");
```

---

## `LoanService.returnLoan`

```java
Loan current = loans.get(reservationId);
if (current == null || !current.active()) {
    throw new IllegalStateException("No active loan for this reservation.");
}
Loan returned = new Loan(current.reservationId(), current.borrowerId(),
        current.itemId(), current.borrowedOn(), LocalDate.now(clock));
loans.put(reservationId, returned);
```

* The service **replaces** an active loan value with a returned value instead of mutating earlier snapshots.

---

## The Lending Rules (1 of 2)

| Operation | Rule and state effect |
|---|---|
| Checkout | Reservation must exist; today's date must be within its period |
| Repeat checkout | One reservation can create at most one loan, including after return |
| Item already out | A second active loan for the same item is rejected |

---

## The Lending Rules (2 of 2)

| Operation | Rule and state effect |
|---|---|
| Return | Only an active loan can be returned; repeated return is rejected |
| Return date | Cannot precede the recorded checkout date |
| Observation | Loan snapshots are unmodifiable and contain immutable loan values |

---

## Do Not Invent Lifecycle Rules Silently

* Returning a loan does **not** delete or cancel its reservation.
* The reservation-count rule still counts **every stored reservation**; availability stays based on those records.
* An early return therefore **does not free a reserved interval or restore a borrower's allowance**.
* An explicit, tested **inherited limitation**. Changing it would disguise **a feature change as testing work**.

---

## A Bounded In-Memory Flow

* One coordinator and one loan service **for the session**.
* Multiple independent loan services have **independent loan maps**.
* No shared persistent or concurrent protection.
* **Not** a complete lending operation.

---

# 7.5 Dummies, Stubs, Fakes, Spies and Mocks
### Name the role a substitute plays

---

## Test Doubles (1 of 2)

| Role | Purpose | Example in this project |
|---|---|---|
| Dummy | Supplies an argument the scenario should not use | A sender passed to an immediately rejected request |
| Stub | Produces a controlled answer or failure | A sender that throws the expected notification exception |
| Fake | A working simplified substitute | An in-memory output standing in for external delivery |

---

## Test Doubles (2 of 2)

| Role | Purpose | Example in this project |
|---|---|---|
| Spy | Records calls for later inspection | The recorder, when a test examines received reservations |
| Mock | Supports verification of expected interactions | A Mockito sender checked for one call or no calls |

* The vocabulary follows Meszaros, summarised by Fowler. **Roles overlap**; the class name alone does not determine the role.

---

## Keep the Subject Real

* The coordinator is the **subject under test** in notification scenarios.
* Mocking its `reserve` method would **replace the behaviour we want to examine**.
* Keep the real coordinator, rules and small immutable values. Replace **the output boundary** that would otherwise complicate observation.
* A hand-written recorder is often **clearer than a framework**: its list makes the effect visible.

---

## Mockito for a Specific Interaction

```java
NotificationSender sender = mock(NotificationSender.class);
ReservationCoordinator c = ReservationApplication.create(sender);
c.reserve("B1", "CAM1", day, 2);
ArgumentCaptor<Reservation> captured = ArgumentCaptor.forClass(Reservation.class);
verify(sender).send(captured.capture());
Reservation sent = captured.getValue();
assertAll(() -> assertEquals("R1", sent.id()),
        () -> assertEquals("B1", sent.borrowerId()),
        () -> assertEquals("CAM1", sent.itemId()));
```

---

## Two More Mockito Tests

```java
// no notification after a rejection
assertEquals("Rejected: borrower limit or duration.", c.reserve("B1", "CAM1", day, 8));
assertTrue(c.reservations().isEmpty());
verifyNoInteractions(sender);

// expected failure: record retained, exactly one attempt
doThrow(new NotificationException("Expected test failure"))
        .when(sender).send(any(Reservation.class));
/* ... reserve ... */
verify(sender, times(1)).send(any(Reservation.class));
```

---

## Public Boundary, Not Private Helpers

* These checks concern **public boundary behaviour**.
* The exact number of invocations matters because the feature says **one attempt per acceptance and no automatic retry**.
* Counting how often a **private list** is inspected would be a brittle assertion of a different kind.

---

## Mockito Setup Notes

* The supplied setup uses its **interface-only proxy mock maker**: mocks are Java dynamic proxies, and **no class or static mocking** is needed.
* On newer JDKs, Mockito may still attach its ByteBuddy agent and the JVM prints **"A Java agent has been loaded dynamically"**. The tests still pass.
* Passing `-XX:+EnableDynamicAgentLoading` to the test JVM removed the message. The JVM says dynamic loading will be disallowed by default in a future release: **check Mockito's documentation** for your JDK.

---

## A Preview: Doubles for an Outside Data Source

```java
BorrowerDirectory knownStudent = id -> Optional.of(new Borrower(id, BorrowerCategory.STUDENT));
BorrowerDirectory nobody = id -> Optional.empty();
BorrowerDirectory offline = id -> { throw new DirectoryException("provider offline"); };
```

* The contract has **one method**, so a lambda is enough. Chapter 8 builds the real types.
* Compiled and run against Chapter 8's types, they print `STUDENT`, `false` and `failure: provider offline`.

---

## What Each Directory Double Answers

* `knownStudent`: a **stub with a fixed answer**: tests what the service does with a borrower it can trust.
* `nobody`: a stub saying **"absent or inactive"**: tests the ordinary rejection.
* `offline`: a **throwing stub**: tests that an outage is reported as an outage, **not as "not found"**.
* None needs a framework. **None proves that a real provider behaves this way.**

---

## Match the Double to the Question

* A **recorder** when you want to inspect accumulated notices.
* A **throwing stub** when you need a predictable output failure.
* An **interaction-verifying mock** when the contractual call itself is the observation.
* A **fixed clock** supplies controlled time; it does not prove the real system clock is correct.
* Neither recorder nor mock **proves that email is delivered**. Chapter 13 covers real adapters.

---

## Do Not Verify Everything

* A blanket "nothing else was called" assertion can make **harmless implementation changes fail**.
* Verify only absence or ordering that is **meaningful to the requirement**.
* "No notification after rejection" is meaningful.
* "Exactly three calls to the snapshot getter" is **not**.

---

# 7.6 Testability and Design Feedback
### Difficult tests as information

---

## Difficult Setup Can Reveal a Design Problem

* Chapter 6's constructor injection lets tests **choose a recorder, failing sender and policy mapping** without altering the coordinator.
* `LoanService` receives a **clock** for the same reason.
* A difficult test may expose hidden global configuration, mixed responsibilities or unclear results. It may also expose **a poorly chosen test**: is the scenario trying to inspect a private detail?

---

## The Query's Clear Contract

* The availability query **creates no records and has no notification side effects**: easy to test result and state separately.
* Implementing it by calling `reserve` would **entangle eligibility, identifiers and notifications**.
* Test difficulty would then be **useful feedback about the proposed design**.

---

## Use Real Simple Collaborators

* `LoanPeriod` is cheap, deterministic and central to the rule. **Mocking it to say "overlaps"** would prevent the tests from exercising real period semantics.
* An ordinary **list or map should usually remain real**: replacing it with a mock leads to assertions about `add`, `get` and ordering, not preserved records.
* A substitute should **remove an obstacle or expose a meaningful boundary**, not erase the behaviour under examination.

---

## Preserve Evidence During Migration

* Moving to JUnit does not require rewriting every old assertion at once.
* The bridge makes earlier runners visible to the new build; new tests are **focused methods with readable names**.
* The bridge is **transitional**: four coarse results give less precise reporting. Later migration can improve diagnosis **without changing expected behaviour**.
* Do not discard earlier checks because their syntax predates the framework.

---

# 7.7 Weak or Brittle Tests
### Executing code is not asking a question

---

## Coverage Is Not Correctness

* Coverage records **which code was exercised** under a particular measurement.
* It does **not** establish that the expected answer was correct or that the assertions would reject a defect.
* A test can execute **every line** of a method and accept **every result**.

---

## Compare Two Query Tests

* One only calls `isAvailable`.
* The other expects an overlapping interval to be **false** and **preserves the recorded state**: it distinguishes a meaningful defect.
* A further **adjacency example** distinguishes a different defect the overlap example would miss.

---

## A Targeted Mutation Experiment

* In a **separate copy**, change the second comparison in `LoanPeriod.overlaps`:

```java
other.start.isBefore(endExclusive)        // correct
!other.start.isAfter(endExclusive)        // deliberately wrong
```

```bash
mvn --batch-mode -Dtest=AvailabilityTest#adjacentPeriodAndDifferentItemAreAvailable test
```

---

## The Result

* **One failure, zero errors, nonzero build exit.** The assertion expects `true` and receives `false`.
* A **behavioural** failure in the adjacency example, not a missing tool or compile issue.
* **Restore** the original and rerun: the test passes.
* It supports one claim: **this test detects this fault**. It is not a mutation score.
* Never change the correct expected value to accommodate the mutant.

---

## Sixteen Single Faults

* Introduced **one at a time** into copies of the completed project; each run through `mvn test`.
* **Fifteen** were rejected by at least one named test.
* **One survived.**
* A surviving fault is **information to examine**, not always a defect in the tests.

---

## Which Test Caught Which Fault (1 of 4)

| Fault | Caught by |
|---|---|
| `isAvailable` always returns true | `AvailabilityTddTest` overlapping enquiry |
| `isAvailable` always returns false | `AvailabilityTest` empty-schedule, adjacency, eligibility examples |
| Conflict check ignores the item identifier | adjacency/different-item example and the Chapter 2 bridge |
| Inclusive end boundary in `LoanPeriod` | adjacency test and both older bridges |

---

## Which Test Caught Which Fault (2 of 4)

| Fault | Caught by |
|---|---|
| Checkout allowed on the exclusive end day | `checkoutOutsideHalfOpenPeriodIsRejected` |
| Checkout allowed before the start | the same test |
| One reservation checked out twice | `aReservationCannotBeCheckedOutTwiceEvenAfterReturn` |
| Item-already-on-loan check removed | `unreturnedItemBlocksTheNextAdjacentReservationUntilReturned` |

---

## Which Test Caught Which Fault (3 of 4)

| Fault | Caught by |
|---|---|
| Return of an inactive loan allowed | `checkoutAndReturnUseTheSuppliedClock` |
| Real system clock used instead of the supplied one | three `LoanServiceTest` methods |
| Clock zone ignored | `clockZoneDeterminesTheCheckoutDate` |
| Return date recorded as the checkout date | `checkoutAndReturnUseTheSuppliedClock` and the backward-clock test |

---

## Which Test Caught Which Fault (4 of 4)

| Fault | Caught by |
|---|---|
| `Loan` no longer rejects a return before checkout | `backwardClockCannotRecordReturnBeforeCheckout` |
| Sender called twice on success | `NotificationMockitoTest`, `Chapter06Checks`, an availability test |

---

## A Real Gap Found

* The rule table says **loan snapshots are unmodifiable**, but **no test checked it**.
* Replacing `List.copyOf(loans.values())` with a plain `ArrayList` passed the other tests.
* One assertion was added (in `checkoutAndReturnUseTheSuppliedClock`), which now rejects that fault.

---

## The Mutant That Survives

* An enquiry that **adds a temporary record and removes it again**.
* With identifiers derived from the list size, it leaves **no trace**: records, notices and next identifier end exactly as before.
* In a sequential program, **no test can tell it from the correct one**. Only a concurrent observer could.
* Response: **reject the design by reading it**; do not claim a test can catch it. The identifier example is still worth keeping.

---

## Do Not Let Tests Reproduce the Same Misunderstanding

* An AI-generated implementation and AI-generated tests may agree because **both assume inclusive end dates**. Agreement is **not independent evidence**.
* Check expected values against the human-reviewed convention and concrete examples.
* Avoid expected values derived from the result: an identifier equal to the identifier in the same returned object is **no independent fact**. For the first reservation, an explicit **R1** is meaningful.

---

## Avoid Unnecessary Implementation Coupling

* A test asserting the query calls private `hasConflict` exactly once **fails under a different correct structure**.
* The **public result and state contract** should survive refactoring.
* **Exact text assertions** are fine when text is part of the existing contract, but wording changes then require deliberate expectation updates.

---

## When a Test Fails, Classify the Failure

* A **requirement misunderstanding**.
* An **implementation defect**.
* An **outdated expectation**.
* An **environment or configuration problem**.
* **Test fragility**.
* A green build obtained by **suppressing the assertion's exit status** answers none of these.

---

# 7.8 Milestone 2 Evidence
### Demonstrate an outcome with its boundaries

---

## The Demonstration Journey

```text
Available before reservation: true
Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Available after reservation: false
Loan active after checkout: true
Loan active after return: false
Accepted-reservation notices: 1
```

* Fixed clock; one coordinator and loan service. **Checkout and return send no new notices**.

---

## What the Demonstration Is and Is Not

* A concrete example of **a bounded MVP increment**. Your assessed domain and scope may differ.
* No remote delivery, database or hosted execution.
* Another person should be able to **reproduce it and explain what remains outside its claim**.
* A hosted CI run is **separate evidence** from the local Maven runs.

---

## Milestone 2 Evidence (1 of 3)

| Evidence | What it should establish |
|---|---|
| Working MVP demonstration | A coherent user outcome runs from documented setup |
| Acceptance mapping | Selected examples connect to executed tests |
| TDD sequence | Intended failure, implementation and protected refactoring are visible |

---

## Milestone 2 Evidence (2 of 3)

| Evidence | What it should establish |
|---|---|
| OO/SOLID rationale | Collaborators and responsibilities have concrete reasons |
| Double choice | Controlled behaviour or interaction is justified |
| Build result | Actual tests ran against the intended revision |

---

## Milestone 2 Evidence (3 of 3)

| Evidence | What it should establish |
|---|---|
| Review and retrospective | Real feedback, a change in understanding and a next action are recorded |
| Limitations | In-memory storage, lifecycle boundaries and missing integrations are explicit |

* A test report is **not the whole milestone**.

---

## Make the Retrospective Useful

* Connect an **observation** to an **action**.
* Example (record it only if it happened): availability tests silently assumed the machine's current date, so **all time dependencies become explicit**.
* Avoid pre-filled success narratives: **"we collaborated well" explains nothing**.
* Distinguish a **proposed** improvement from one **already tested**.

---

# 7.9 AI in Practice: Implementation vs. Expected Behaviour
### Do not let outputs validate each other

---

## Use the Reviewed Examples as Authority

* Ask an AI assistant for a **candidate query implementation**.
* Separately ask for **omitted boundary cases**.
* **Evaluate both outputs** rather than letting them validate each other.
* Chapter 15 collects the recurring AI workflows. This activity is self-contained.

---

## Activity Frame (1 of 2)

| Element | For this activity |
|---|---|
| Engineering objective | Separate a proposed implementation from the evidence that would accept or reject it |
| Input | AQ-01 to AQ-05 as reviewed, and Chapter 6's coordinator |
| Permitted scope | Evaluate the candidate implementation and its tests; do not treat either as proof of the other |

---

## Activity Frame (2 of 2)

| Element | For this activity |
|---|---|
| Independent checks | The reviewed examples, the labelled wrong-boundary mutation, the build result |
| Accept or reject | A verdict with independent evidence for each claim |
| No-account route | The fixture is sufficient |

---

## The Fixture

**Author-written fictional AI output.**

> An enquiry can call `reserve` and remove the temporary record. Treat the end date as inclusive so adjacent bookings conflict. A test is sufficient if the method returns without throwing. Since the implementation and generated tests agree, coverage will prove correctness. For time-sensitive loan tests, use the current date and wait until tomorrow to test the next state.

---

## Model Critique (1 of 2)

| Fixture claim | Verdict | Independent check or correction |
|---|---|---|
| Query by reserve-and-remove | Reject | `reserve` sends a notice and can be refused by limits; adding and removing directly leaves no trace sequential tests can see, so reject by reading |
| Inclusive end means adjacency conflicts | Reject | The agreed interval is half-open; `[20,22)` and `[22,23)` do not overlap |
| No exception is sufficient | Reject | An always-true or always-false method can return normally and be wrong |

---

## Model Critique (2 of 2)

| Fixture claim | Verdict | Independent check or correction |
|---|---|---|
| Implementation and tests mutually prove correctness | Reject | Both may share the same mistaken convention |
| Coverage proves correctness | Reject | Execution does not validate expected values or sensitivity to defects |
| Use the real date and wait for tomorrow | Reject | Supply a fixed or controlled clock and an explicit zone |

* The wrong-boundary experiment is a **concrete verification step**: no need to ask another AI whether the mutant is wrong.

---

# 7.10 Common Mistakes
### Eight to avoid

---

## Mistakes 1 to 3

| Mistake | Consequence | Better action |
|---|---|---|
| Count a dependency-download error as TDD red | Behaviour was never examined | Reach the intended assertion failure |
| Write expected values by calling the implementation | Reproduces the same mistake | Use independently reviewed examples |
| Mock the object under test | Replaces the behaviour being investigated | Keep the subject real |

---

## Mistakes 4 to 6

| Mistake | Consequence | Better action |
|---|---|---|
| Use real time for a deterministic date rule | Results change with date or zone | Inject an explicit clock |
| Treat every recorder as the same double role | Hides why it is used | Describe its role in the particular test |
| Verify private call counts | Breaks harmless refactoring | Observe public behaviour or meaningful boundary interactions |

---

## Mistakes 7 and 8

| Mistake | Consequence | Better action |
|---|---|---|
| Remove old checks during tool migration | Loses existing evidence | Bridge or migrate them explicitly |
| Call the bounded demo production-ready | Conceals lifecycle and integration gaps | State what the MVP actually demonstrates |

---

# 7.11 Practical Activity
### Test-first on your own code

---

## Input and Demonstration

* **Input:** Chapter 6's checkpoint, the reviewed query criteria, the new loan-flow rules and the companion's Maven/JUnit setup.
* **Demonstration:** run the labelled **red** stage, inspect the precise failure, apply the **green** implementation, extract conflict detection, rerun the new test **and** the legacy bridge.
* **Guided practice:** convert one **policy boundary table** into parameterised examples and discuss which incorrect result each row distinguishes. Compare a hand-written recorder with the Mockito interaction test.

---

## Independent Work: Steps 1 to 3

1. Reproduce the supplied TDD cycle, or conduct a small new one. **Record the actual sequence.**
2. Complete the remaining **query examples**, including side effects and adjacency.
3. Demonstrate the **loan flow** with controlled dates and rejection of an invalid return.

---

## Independent Work: Steps 4 to 6

4. Choose a **substitute** for one collaborator and justify its role.
5. Run the labelled **wrong-boundary implementation** in a separate copy, identify the failing assertion and restore the source.
6. Run the **full build** and map selected acceptance examples to named tests.

---

## Independent Work: Steps 7 to 9

7. **Rehearse the MVP demonstration** from documented instructions, obtain actual review feedback and write a short retrospective with a next action.
8. On your **Team project**, take one backlog behaviour and develop it **test-first**. Record the actual red failure, the green change and the refactoring. **Do not reconstruct a sequence afterwards.**
9. On your **Team project**, work through the **Milestone 2 checklist**: rehearse your own demo, get review feedback, write a retrospective. Record which items are complete, which are gaps and **who will close each one**.

---

## Expected Output and Completion

* **Output:** runnable source; focused tests; TDD and mutation evidence; double rationale; actual build result; demonstration notes; review and retrospective notes; explicit limitations; the step 8 and 9 records.
* **Complete when:** the failure is **behavioural and understood**; query results and state effects match the examples; time-sensitive tests **do not depend on the actual day**; the **whole regression suite executes**; the demo includes reservation, checkout and return.
* **Optional extension:** sketch how completed reservations should affect counts and early-return availability. Do **not** silently implement it.

---

## What the Build Establishes

* **35 JUnit invocations:** one TDD test, **eight** additional availability invocations, **ten** policy rows, **nine** loan invocations, **three** Mockito tests, **four** legacy wrappers.
* The expected output ends `Tests run: 35, Failures: 0, Errors: 0, Skipped: 0` and `BUILD SUCCESS`.
* An execution inventory, **not a claim of exhaustive correctness or a quality score**.

---

## Versions Pinned for This Chapter

| Tool | Tested selection | Role |
|---|---|---|
| Java | Java 17 language/API target | Application and test execution |
| Maven | 3.9.11 | Build and dependency resolution |
| Compiler Plugin | 3.14.1 | Java compilation |
| Surefire Plugin | 3.5.4 | JUnit Platform execution |
| JUnit Jupiter | 5.13.4 | Assertions, discovery, parameterised cases |
| Mockito | 5.20.0 | Interface mock, stubbing, verification |

---

## Acceptance Mapping (1 of 2)

| Requirement or risk | Executable evidence |
|---|---|
| AQ-01 empty schedule available | `emptyScheduleIsAvailableWithoutAnySideEffect` |
| AQ-02 overlap unavailable | `AvailabilityTddTest` overlapping enquiry |
| AQ-03 adjacent periods allowed | `adjacentPeriodAndDifferentItemAreAvailable` |
| AQ-04 different item | the same test checks MIC1 separately |
| AQ-05 equal or reversed interval | parameterised `invalidPeriodFailsWithoutChangingState` |

---

## Acceptance Mapping (2 of 2)

| Requirement or risk | Executable evidence |
|---|---|
| Enquiry does not allocate an ID | `queryDoesNotAllocateAnIdentifier` |
| Availability differs from eligibility | two tests: count limit and a thirty-day enquiry |
| Checkout window excludes its end | two invocations of `checkoutOutsideHalfOpenPeriodIsRejected` |
| Local date depends on clock zone | `clockZoneDeterminesTheCheckoutDate` |
| Backward time cannot predate checkout | `backwardClockCannotRecordReturnBeforeCheckout` |

---

## Suggested Evidence Packet (1 of 2)

| Artefact | Useful content |
|---|---|
| Scope note | Selected query and loan rules; synthetic inputs; lifecycle limitations |
| TDD record | Actual red message, same test at green, refactoring diff, regression result |
| Acceptance mapping | Named tests tied to concrete examples |
| Double rationale | Which collaborator is replaced, why, and what observation it enables |

---

## Suggested Evidence Packet (2 of 2)

| Artefact | Useful content |
|---|---|
| Mutation record | Isolated faulty comparison, selected failure and restored pass |
| Build result | Executed revision, tool versions, actual report |
| Demonstration | Reproducible steps from empty state through reserve, checkout, return |
| Review and retrospective | Actual observations, corrective action, a next-iteration experiment |

* A copied sample table is **not evidence** that a team ran the tests or conducted a review.

---

# 7.12 Review Questions and Midterm Practice
### Concept, diagnosis, transfer, and the practice set

---

## Concept Questions

1. Why is "the method did not throw" insufficient evidence for an availability query?
2. What distinguishes the red stage of the worked cycle from a missing-dependency failure?
3. When does the notification recorder act as a spy, and why can a framework mock serve a similar purpose?
4. Why do both the instant and zone matter when testing a local-date checkout rule?

---

## Diagnosis Questions

5. A test calculates its expected availability by calling the same overlap helper used by production code. Both treat adjacency as overlap. Explain why the green result is weak and replace it with an independent example.
6. A loan test passes alone but fails after another test, and both use a static shared loan service. Diagnose the likely cause and propose a fixture strategy that still allows intentional multi-step scenarios.

---

## Guidance: Questions 1 and 2

1. A valid query must **distinguish available from conflicting intervals and preserve state**. Always-true returns normally but fails AQ-02; always-false fails AQ-01 and AQ-03.
2. The worked red run **discovered and executed the named test, reached the assertion** and reported `false` expected but `true` actual. A dependency-resolution failure never establishes application behaviour.

---

## Guidance: Questions 3 and 4

3. When the test examines its received records, the recorder provides **observed interaction history**: a spy. A Mockito mock can record and verify too. The classification depends on **the test's purpose and observation**.
4. One instant gives **different dates in different zones**. The test must state both when the rule concerns a local date. The Baghdad example fixes the interpretation.

---

## Guidance: Questions 5 and 6

5. The test derives its expectation from **the same faulty rule**, so the two agree without independent validation. Book `[2026-10-20, 2026-10-22)`, enquire `[2026-10-22, 2026-10-23)`, **explicitly expect true**, and run the mutant to show this rejects the inclusive comparison.
6. Earlier tests may have inserted or returned loans that **alter later tests' starting state**. Use a **fresh coordinator, sender and loan service per independent scenario**. A multi-step lifecycle test may share its own service while advancing a controlled clock.

---

## Transfer Challenge: Room Booking

A room-booking service permits availability enquiry and check-in only during the booked interval.

* Design **three acceptance examples**, **one clock-controlled test** and **one collaborator substitute**.
* Explain which expectations **transfer from equipment lending** and which rules need **stakeholder clarification**, such as cleaning time or late check-in.

---

## Transfer Guidance

* Examples: an empty schedule is available; an overlapping booking makes an enquiry unavailable without adding a booking; an enquiry starting at the previous exclusive end is available if no turnaround rule applies.
* **Check-in:** fixed clock at the booking start: accept; at the exclusive end: reject if that is the agreed policy. A **recorder** observes one check-in notice.
* Clarify **cleaning intervals, early arrival, late check-in, no-show expiry, who authorises entry**.
* Represent the **time zone** and choose an appropriate time type. Do not copy `LocalDate` merely because the earlier project used whole days.

---

## Midterm Practice Set: What It Covers

* The midterm covers **Chapters 2 to 7** (Weeks 1 to 6).
* According to the module descriptor, it asks you to:
  * **model a scenario with UML class diagrams**,
  * **identify SOLID violations and smells** in supplied code,
  * **refactor** short snippets by introducing interfaces and dependency injection,
  * **write unit tests** with test doubles for a small component.
* Do **not** add Chapter 8's patterns. Whether Mockito is allowed in the exam is the module leader's decision; **hand-written doubles work anywhere**.

---

## Task 1: UML

Draw a class diagram. Include multiplicities, **one composition, one interface realisation and one dependency**, and write down **one rule your diagram cannot express**.

* A library lends laptops. Each laptop has an **asset tag and a model**.
* A **loan links one borrower to one laptop** and records a start date and a due date.
* A borrower and a laptop can **each appear in many loans** over time.
* A loan can be **renewed any number of times**; a renewal records a new due date and **has no meaning without its loan**.
* When a loan is **overdue**, a notice is delivered through a **channel**: email today, other channels later.

---

## Task 1: One Model

<!--svg:ch07-laptop-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 345" role="img" aria-label="Midterm practice task 1, one model: a Borrower and a Laptop each link to zero or more Loans; a Loan owns zero or more Renewals (composition); a Loan depends on the NoticeChannel interface, which EmailChannel implements." style="display:block;width:100%;height:calc(var(--u) * 34.50);margin:0 auto">
<defs><marker id="ch07-laptop-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-laptop-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-laptop-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-laptop-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch07-laptop-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="10.0" width="170.0" height="71.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,46.0 L12.0,16.0 Q12.0,12.0 16.0,12.0 L174.0,12.0 Q178.0,12.0 178.0,16.0 L178.0,46.0 Z" fill="#e6eef6"/>
<text x="95.0" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Borrower</text>
<line x1="10.0" y1="46.0" x2="180.0" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String name</text>
<rect x="10.0" y="205.0" width="190.0" height="94.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,241.0 L12.0,211.0 Q12.0,207.0 16.0,207.0 L194.0,207.0 Q198.0,207.0 198.0,211.0 L198.0,241.0 Z" fill="#e6eef6"/>
<text x="105.0" y="230.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Laptop</text>
<line x1="10.0" y1="241.0" x2="200.0" y2="241.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="263.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String assetTag</text>
<text x="22.0" y="286.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String model</text>
<rect x="310.0" y="10.0" width="250.0" height="152.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M312.0,46.0 L312.0,16.0 Q312.0,12.0 316.0,12.0 L554.0,12.0 Q558.0,12.0 558.0,16.0 L558.0,46.0 Z" fill="#e6eef6"/>
<text x="435.0" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Loan</text>
<line x1="310.0" y1="46.0" x2="560.0" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="322.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-LocalDate startedOn</text>
<text x="322.0" y="91.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-LocalDate dueOn</text>
<line x1="310.0" y1="104.0" x2="560.0" y2="104.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="322.0" y="126.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+notify(NoticeChannel</text>
<text x="322.0" y="149.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">   channel) void</text>
<rect x="420.0" y="265.0" width="200.0" height="71.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M422.0,301.0 L422.0,271.0 Q422.0,267.0 426.0,267.0 L614.0,267.0 Q618.0,267.0 618.0,271.0 L618.0,301.0 Z" fill="#e6eef6"/>
<text x="520.0" y="290.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Renewal</text>
<line x1="420.0" y1="301.0" x2="620.0" y2="301.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="432.0" y="323.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-LocalDate newDueOn</text>
<rect x="650.0" y="10.0" width="210.0" height="114.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M652.0,66.0 L652.0,16.0 Q652.0,12.0 656.0,12.0 L854.0,12.0 Q858.0,12.0 858.0,16.0 L858.0,66.0 Z" fill="#e6eef6"/>
<text x="755.0" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="755.0" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">NoticeChannel</text>
<line x1="650.0" y1="66.0" x2="860.0" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="662.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+deliver(String</text>
<text x="662.0" y="111.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">   message) void</text>
<rect x="650.0" y="215.0" width="210.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M652.0,251.0 L652.0,221.0 Q652.0,217.0 656.0,217.0 L854.0,217.0 Q858.0,217.0 858.0,221.0 L858.0,251.0 Z" fill="#e6eef6"/>
<text x="755.0" y="240.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">EmailChannel</text>
<path d="M180.0,45.0 L310.0,45.0" fill="none" stroke="#1d588c" stroke-width="2.2"/>
<text x="207.0" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="283.0" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="245.0" y="31.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">borrows</text>
<path d="M200.0,250.0 L350.0,250.0 L350.0,162.0" fill="none" stroke="#1d588c" stroke-width="2.2"/>
<text x="227.0" y="271.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="366.0" y="194.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="332.0" y="211.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="end" font-style="italic">is lent in</text>
<path d="M500.0,162.0 L500.0,265.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch07-laptop-diaf)"/>
<text x="484.0" y="194.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="484.0" y="243.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="518.0" y="218.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">has</text>
<path d="M560.0,70.0 L650.0,70.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch07-laptop-open)"/>
<text x="605.0" y="56.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">notices</text>
<path d="M755.0,215.0 L755.0,124.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch07-laptop-tri)"/>
<text x="737.0" y="174.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="end" font-style="italic">implements</text>
</svg>
</div>
<!--/svg-->

---

## Task 1: Reading the Model

* A borrower and a laptop each link to **any number of loans over time**: `0..*` at the loan side.
* A renewal cannot exist without its loan: **composition**.
* The channel is an **interface** because other channels are expected; `Loan` depends on the **interface**, not on `EmailChannel`.
* A rule such as "a laptop is on at most one active loan" **cannot be expressed by multiplicity**: write it as a note or invariant.
* Penalise inheritance for "has", a solid line for realisation, a composition diamond between `Borrower` and `Loan`.

---

## Task 2: Diagnose This Class

```java
public class OverdueReminder {
    public boolean remind(String borrowerEmail, LocalDate dueDate, String itemName) {
        if (LocalDate.now().isAfter(dueDate)) {
            MailClient client = new MailClient("smtp.campus.example", 25);
            client.send(borrowerEmail, "Overdue: " + itemName,
                        "Please return " + itemName + ".");
            System.out.println("Reminder sent to " + borrowerEmail);
            return true;
        }
        return false;
    }
}
```

* `MailClient` opens a real network connection: assume you cannot call it from a test.

---

## Task 2: A Strong Diagnosis

* **Three jobs mixed:** deciding overdue, building and sending the message, reporting to the console (single responsibility).
* **Reads the system clock directly:** the result depends on the date the test runs.
* **Constructs `MailClient` with a hard-coded host and port:** a concrete provider it cannot swap (dependency inversion), and **untestable without a mail server**.
* The boolean does not distinguish "not overdue" from "sent".
* Connect each defect to a **consequence**: "the overdue path cannot run in a test; here it throws `IllegalStateException` from `MailClient`".

---

## Task 3: Refactor It

```java
public interface ReminderSender {
    void send(String to, String subject, String body);
}

public final class OverdueReminder {
    private final Clock clock;
    private final ReminderSender sender;

    public OverdueReminder(Clock clock, ReminderSender sender) { /* null checks */ }

    public boolean remind(String borrowerEmail, LocalDate dueDate, String itemName) {
        if (!LocalDate.now(clock).isAfter(dueDate)) return false;
        sender.send(borrowerEmail, "Overdue: " + itemName, "Please return " + itemName + ".");
        return true;
    }
}
```

---

## Task 3: What Was Preserved

* A `MailReminderSender` **adapts the supplied `MailClient`** and keeps the console message, so behaviour is preserved.
* The composition root would call `new OverdueReminder(Clock.systemDefaultZone(), new MailReminderSender(new MailClient("smtp.campus.example", 25)))`.
* The **constructor is a deliberate API change**; the observable behaviour of `remind` is preserved.
* No credit for adding an interface to `MailClient` (you do not own it) or for a factory nobody needs.

---

## Task 4: Tests With a Double

```java
@Test void noReminderOnTheDueDateItself() {
    assertFalse(reminderOn("2026-10-20T23:00:00Z").remind("a@example.org", DUE, "CAM1"));
    assertTrue(sender.calls.isEmpty());
}
@Test void exactlyOneReminderTheDayAfterTheDueDate() {
    assertTrue(reminderOn("2026-10-21T00:00:00Z").remind("a@example.org", DUE, "CAM1"));
    assertEquals(List.of("a@example.org|Overdue: CAM1|Please return CAM1."), sender.calls);
}
```

* A hand-written **spy** records calls; the **clock is fixed**; expected values come from the scenario.
* Also test an earlier date. State which **role** your double plays.

---

## Task 5: Trace a Rejected Reservation

* Trace, in order: **argument validation, borrower count, policy decision, conflict checking**.
* A rejection occurs **before storage and notification**.
* Choose observations that show it: the rejection outcome, **unchanged records**, **no sender interaction**.
* Identify the role of the **injected sender**.
* A good answer **connects design, behaviour and evidence** rather than listing acronyms.

---

# Summary and Next Chapter
### What to carry forward

---

## Summary

* Meaningful tests **distinguish intended behaviour from plausible mistakes**.
* The worked cycle makes one missing rule **fail visibly**, implements it and protects the following structural change.
* **Controlled collaborators and clocks** make outcomes reproducible; **carefully chosen assertions** keep tests useful during refactoring.

---

## Where the Checkpoint Stands

* Reservation **availability enquiry**.
* A bounded **checkout and return flow**.
* Lifecycle and integration limits remain **explicit**.

---

## Next: Chapter 8

* **Construction and compatibility patterns.**
* They build on these tests, rather than replacing design judgement with pattern names.

---

## Sources and Further Reading

1. **JUnit Team:** *JUnit 5 User Guide*, 5.13.4.
2. **Apache Maven:** Surefire with the JUnit Platform; Maven 3.9.11; Compiler Plugin.
3. **Fowler:** *Test Driven Development*; *Test Double* (2006).
4. **Oracle:** Java SE 17 `Clock`; Record Classes.
5. **Mockito Team:** API documentation; Mockito 5.20.0.
6. **Martin:** *Agile Software Development* (2002). **Beck:** *Test-Driven Development: By Example* (2002).

* Full references and links are in the chapter text.
