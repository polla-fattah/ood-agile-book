---
title: "Chapter 14: Responding to Change and Handing Over"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 140
type: slides
layout: page
---

# Chapter 14: Responding to Change and Handing Over
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **14.1 Did the design absorb the change? Reviewing the outcome**
  * Four questions, each with its own evidence.
* **14.2 Fix, defer or accept: scope control in the last week**
  * Fix, defer or accept, and freeze.
* **14.3 Writing it down: documents, decision records and release notes**
  * One document per question; the flag decision.
* **14.4 Keeping the evidence true: rehearsal and traceability**
  * A rehearsed flag removal; requirements traced to tests.

---

## Chapter Roadmap (2 of 3)

* **14.5 Setup and a demonstration that anyone can reproduce**
  * Follow your own instructions in a fresh copy.
* **14.6 Retrospective and individual reflection**
  * Evidence-based retrospectives; contribution as claims with links.
* **14.7 Getting ready for the final submission**
* **14.8 Validating an AI-drafted README** validate a README that an assistant drafted.

---

## Chapter Roadmap (3 of 3)

* **14.9 Handover habits that mislead**
* **14.10 Try it yourself: hand the project over**
* **14.11 Questions to think with, and a transfer challenge**
* **What to take away, and what comes next**
  * Chapter 15: the recurring assistance workflows and their verification records.

---

## Learning Outcomes (1 of 2)

After this chapter, you should be able to:

1. **Evaluate how a design accommodated a change**, using the affected responsibilities, the test failures, the revised assumptions and review feedback, and explain why **a small diff is not automatically a better design**.
2. **Prioritise remaining release work**, and choose between fixing, deferring and accepting a known issue.
3. **Produce reproducible handover instructions** and check them by following them in a fresh copy.

---

## Learning Outcomes (2 of 2)

4. **Trace requirements to implementation and tests**, and keep that trace true with a check.
5. **Support retrospective conclusions with evidence**, and write an individual reflection that explains your own contribution.
6. **Prepare a final submission** without claiming evidence that does not exist.

---

## Where This Chapter Fits and Where You Start

* Supports **all learning outcomes, LO1 to LO6**: the final sprint and retrospective. Required reading: Martin (2002), a review of the chapters relevant to your project.
* The descriptor says teams submit a **repository link, a technical report and an individual reflection**, give a **demonstration and presentation**, and that **marks are moderated by individual contribution**.
* This chapter creates **no new deadlines, weights or marking rules**; the approved final-project instructions decide what you submit.
* **Entry version:** the Chapter 13 version (the visitor change, version 0.13.1), or for your team's project a Milestone 4 outcome with its remaining defects named.
* **Completed version: version 0.14.0. Its production code is unchanged**: the companion lists only new and changed files.

---

## How to Use This Chapter

* **Core:** 14.1 to 14.5 and 14.7.
* **Working knowledge:** 14.6 on contribution evidence. **You are not asked to measure anyone**; you are asked to know what each kind of evidence can and cannot show.
* **What you must do:** **B1 to B4** (the book's project: running, tracing and diagnosis, the finished version is supplied) and **T1 to T5** (your team's project: your handover bundle, retrospective and individual reflection).
* **If you want more:** B5 to B8 (rehearse removing the flag, validate an AI-drafted README, read a synthetic contribution table, close the gap the one-line experiment found), the review questions, the transfer challenge.

---

## Opening Problem: The Morning of the Final Presentation

A classmate who was not on your team opens your repository link.

1. The README says to run **one command**. It fails: the classmate's machine has no `mvn` on its path, and the error says only **"command not found"**.
2. The README promises **one number of passing tests**; the build reports **another**.
3. The requirements table points at **a test that was renamed last week**.
4. A reviewer asks **which of the three of you wrote the approval-file adapter**; the commit log says the person with the most commits wrote it. **They did not.**

---

## The Defect Is in the Handover

* **None of these is a defect in the software.** Each is a defect in the **handover**: the material that lets someone else **set the project up, trust what it says, and understand who did what**.
* This chapter finishes the project the way Chapter 13 started the change: **with evidence**.
* It is **not a new feature sprint**. The change was implemented in Chapter 13. Here we add **no behaviour**.
* The one fix in the worked project is to **the setup and the demonstration**. Everything else is a decision, a document or a check.

---

# 14.1 Did the Design Absorb the Change?
### Reviewing the outcome

---

## "Did the Design Absorb the Change?" Is Too Vague

* Break it into **four questions**, each with its own evidence.
* Each evidence has a **weakness**; naming the weakness is part of the review.

---

## The Four Questions

| Question | Evidence | Weakness |
|---|---|---|
| Which responsibilities were affected? | Files changed and added, and what each does | Counts files and lines, **not the importance of a line** |
| What broke when the change started? | Test failures after the smallest edit that introduces the change | Shows what the tests cover, **not everything that depends on the code** |
| Which assumptions turned out wrong? | The assumptions written in earlier chapters, checked against the change | **Only the assumptions someone wrote down** |
| What did a reviewer say? | Actual review comments and the responses | **Only as good as the review** |

---

## Affected Responsibilities: The Numbers

Between the Chapter 11 and Chapter 13 versions, **23 files were added and 10 changed**.

| Group | Files | Lines |
|---|---:|---|
| New production files | 9 | **399** |
| Existing production files changed | 5 | **21 added, 3 removed** |
| New test files | 10 | 992 |
| Existing test files changed | 3 | 10 added, 4 removed |
| New scripts, workflow and record | 4 | 213 |
| README and POM changed | 2 | 14 added, 8 removed |

---

## The New Production Files

* Nine new production files hold **399 lines**: the visitor policy, the approval record and its status, the gate, the approval port and its exception, the file adapter, the HTTP client and the demonstration program.
* Line counts: `63 + 15 + 9 + 73 + 53 + 6 + 16 + 92 + 72`.
* **Five existing production files changed**, by a few lines each:

| Existing file | Change |
|---|---|
| `BorrowerCategory` | +1 −1 |
| `DirectoryReservationService` | +14 |
| `ReservationApplication` | +3 −1 |
| `LegacyDirectoryAdapter` | +1 |
| `LegacyDirectoryClient` | +2 −1 |

---

## Figure 14.1: The Footprint of the Visitor Change

<!--svg:ch14-footprint-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 335" role="img" aria-label="Figure 14.1: the footprint of the visitor change in production code. Five existing files changed (BorrowerCategory, DirectoryReservationService, ReservationApplication, LegacyDirectoryAdapter, LegacyDirectoryClient; 21 lines added and 3 removed). Nine new files hold 399 lines (VisitorReservationRules, VisitorGate, ApprovalRecord and ApprovalStatus, ApprovalSource and ApprovalSourceException, FileApprovalSource, HttpLegacyDirectoryClient, Chapter13Demo). DirectoryReservationService uses VisitorGate, ReservationApplication uses VisitorReservationRules, LegacyDirectoryClient is implemented by HttpLegacyDirectoryClient, VisitorGate uses ApprovalSource and ApprovalRecord, and FileApprovalSource implements ApprovalSource." style="display:block;width:100%;height:calc(var(--u) * 33.50);margin:0 auto">
<defs><marker id="ch14-footprint-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-footprint-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-footprint-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-footprint-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-footprint-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="2.0" y="2.0" width="266.0" height="331.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.6"/>
<rect x="400.0" y="2.0" width="468.0" height="331.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.6"/>
<text x="135.0" y="26.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="middle">Existing code changed</text>
<text x="135.0" y="44.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">5 files, +21 -3 lines</text>
<text x="634.0" y="26.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">New production code</text>
<text x="634.0" y="44.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">9 files, 399 lines</text>
<rect x="14.0" y="62.0" width="240.0" height="32.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="134.0" y="82.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">BorrowerCategory</text>
<rect x="14.0" y="120.0" width="240.0" height="32.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="134.0" y="140.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">DirectoryReservationService</text>
<rect x="14.0" y="178.0" width="240.0" height="32.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="134.0" y="198.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">ReservationApplication</text>
<rect x="14.0" y="236.0" width="240.0" height="32.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="134.0" y="256.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">LegacyDirectoryAdapter</text>
<rect x="14.0" y="294.0" width="240.0" height="32.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="134.0" y="314.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">LegacyDirectoryClient</text>
<rect x="415.0" y="62.0" width="210.0" height="32.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="520.0" y="82.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">ApprovalRecord, Status</text>
<rect x="415.0" y="120.0" width="210.0" height="32.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="520.0" y="140.8" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">VisitorGate</text>
<rect x="415.0" y="178.0" width="210.0" height="32.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="520.0" y="198.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">VisitorReservationRules</text>
<rect x="415.0" y="294.0" width="210.0" height="32.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="520.0" y="314.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">HttpLegacyDirectoryClient</text>
<rect x="655.0" y="120.0" width="200.0" height="32.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="755.0" y="140.4" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">ApprovalSource, Exception</text>
<rect x="655.0" y="178.0" width="200.0" height="32.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="755.0" y="198.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">FileApprovalSource</text>
<rect x="655.0" y="294.0" width="200.0" height="32.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="755.0" y="314.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Chapter13Demo</text>
<path d="M254.0,136.0 L415.0,136.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-footprint-arr)"/>
<path d="M254.0,194.0 L415.0,194.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-footprint-arr)"/>
<path d="M254.0,310.0 L415.0,310.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-footprint-arr)"/>
<path d="M520.0,120.0 L520.0,94.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-footprint-arr)"/>
<path d="M625.0,136.0 L655.0,136.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-footprint-arr)"/>
<path d="M755.0,178.0 L755.0,152.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-footprint-arr)"/>
<text x="330.0" y="282.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">implemented by</text>
</svg>
</div>
<!--/svg-->

---

## What the Footprint Shows

* The existing structure took the change **by extension**, which is what the abstractions of Chapters 5, 6 and 10 were for.
* A new borrowing rule was **one new class behind the policy contract**. A new source of approval was **one new port with an adapter**.
* Two things **do not show in a line count**:
  * the existing files that changed are **the ones every request passes through**;
  * nine new files are **nine more things to read**.

---

## What Broke First: Experiments E1 and E2

Start the change in the smallest possible way and see what the tests say.

| Experiment | Edit | Result |
|---|---|---|
| **E1** (Chapter 11 version, 159 invocations) | Add `VISITOR` to the enum only | **45 of 159 fail** (1 failure, 44 errors); 89 lines say `Missing policy: VISITOR` |
| **E2** (the same) | The enum, `VisitorReservationRules` and the composition root | **5 of 159 fail**, only in the three test files that build their own policy map; with four map entries added, **all 159 pass** |

---

## E1 and E2 in Detail

* **E1:** the one failure is `RepositoryBoundaryTest.coordinatorRequiresARepository`, which expects a `NullPointerException` and gets an `IllegalArgumentException`.
* **E2:** the five tests are in `LegacyRegressionTest.chapter06` (through `Chapter06Checks`), `BehaviourStrategyTest.injectedPolicyChangesDecisionWithoutChangingCoordinator` and three tests in `RepositoryBoundaryTest`.
* **No assertion changed.**
* Everything constructed through the composition root fails together when the policy is missing there: **one fix**. Tests that spell out their own map fail separately: **four fixes**.

---

## Is That Good or Bad?

* **Both.** The design tells you, **at construction time and with a precise message**, everywhere that lists every category.
* **A safety net:** the alternative would be a request that fails in production with a null policy.
* **A cost:** every test that spells out the full policy map must be edited when a category is added.
* **B1** in the practical activity runs it the other way: remove the visitor policy from the composition root of the finished version: **73 of 235 fail** (3 failures, 70 errors), in **14 test classes**; roughly three in ten tests.

---

## B1's Failures by Test Class

| Test class | Failing | Test class | Failing |
|---|---:|---|---:|
| `VisitorAcceptanceTest` | 19 | `NotificationPublisherTest` | 3 |
| `DirectoryOutageIntegrationTest` | 10 | `NotificationMockitoTest` | 3 |
| `LoanServiceTest` | 9 | `Chapter13JourneyE2ETest` | 3 |
| `AvailabilityTest` | 8 | `RepositoryBoundaryTest` | 1 |
| `ReserveEquipmentCommandTest` | 4 | `OverdueBridgeTest` | 1 |
| `LegacyRegressionTest` | 4 | `AvailabilityTddTest` | 1 |
| `DirectoryAdapterTest` | 4 | | |

* 146 lines of output say `Missing policy: VISITOR` (each failure is reported more than once).

---

## Revised Assumptions (1 of 2)

Chapters 5 to 11 made statements that the change tested.

| Assumption (where made) | What the change showed | Verdict |
|---|---|---|
| A policy answers a count and duration question and nothing else (Ch. 5, 6) | Approval needs borrower, item, period and time; widening the policy would give it hidden state, so a **separate gate** was added | **Held**, because the contract was not widened |
| Every category has a policy in one place (Ch. 6) | True in production, but four test setups also spelled out the map | **Held, with a cost** |
| The directory is a synthetic provider with no transport (Ch. 8) | Chapter 13 added a real HTTP client and the failures a transport brings, including a timeout that must cover the whole answer | **Contract held**; behaviour extended |

---

## Revised Assumptions (2 of 2)

| Assumption (where made) | What the change showed | Verdict |
|---|---|---|
| The count of retained reservations is the borrowing count (Ch. 7) | CR-12 preserved it on purpose; AC11 pins it | **Still open (SD-12)** |
| The overdue report knows two borrower kinds (Ch. 11) | A late visitor reaches the "any other kind" rule and is fined at a rate nobody chose | **Still open (SD-11-1)** |
| Notifications are one attempt, no retry (Ch. 6) | The directory client follows the same rule | **Held and extended** |

---

## A Small Diff Is Not Automatically a Better Design

* The cheapest possible "implementation" of visitors: the directory adapter maps kind code `V` to the existing **staff** category. **No gate, no register, no new policy. The diff is one line.**
* Experiment **E3** (Chapter 13 version, 232 invocations): **4 of 232 fail**, and **all 203 unit invocations pass**.
* What fails are the tests that cross the real boundary: the **three end-to-end journeys** and `DirectoryOutageIntegrationTest.aVisitorIsServedThroughTheRealDirectoryAndTheRealApprovalFile`.

---

## What E3 Shows in the Journey

* With the flag **off**, visitor V1 is **confirmed**: the flag is ignored.
* **V2 is rejected only because CAM2 is already taken**, with `Rejected: item unavailable.`, **not because it is unapproved**.
* A malformed register **no longer stops anyone**.
* It is a smaller diff, and **it does not implement the requirement**.

---

## Be Careful What E3 Shows

* It shows this suite has **a gap**: **no unit test checks the adapter's mapping of the visitor code**, so a one-line change to it passes the whole unit stage.
* It does **not** show that unit tests cannot see such a change. A focused unit test of the adapter would catch it, and so did the integration tests.
* **A passing unit stage is evidence only about what the unit tests cover.** A suite with a hole is found by **trying a change that goes through the hole**.
* **Neither the size of a diff nor a green unit stage is the measure of a design. The acceptance examples are.** B8 asks you to close the gap.

---

## The Opposite Case

* A change **larger than you expected** is not a failure if each added file has a **purpose the requirement needs**.
* It **is** a failure when the added files support code **nobody asked for**, or when existing files change in ways **the change did not require**.
* The footprint above has no such file: the three changes to existing test files **add an entry to a map, and nothing else**.

---

## Where the Design Bent

```java
if (borrower.category() == BorrowerCategory.VISITOR) {
    Optional<String> rejection = visitorGate.rejection(borrower.id(), itemId, start, days);
    if (rejection.isPresent()) return rejection.get();
}
```

* A **category-specific branch in the entry point**, in `DirectoryReservationService`.
* For **one** special category it is fine and easier to read than an abstraction. At a **second**, it becomes a smell: the next step is a **per-category pre-check chosen from a map**, introduced as a refactoring with its own tests.
* **Record it as a known issue with its trigger** (the second category), instead of fixing it now: **KI-14**.

---

## Review Feedback

* **Real review feedback is evidence; constructed feedback is not.** Use your team's actual review comments and the responses.
* the book's project has no team, so the companion supplies a short, **author-written, fictional** review of the visitor change, labelled as such.
* The task is to **check each comment against the code**, not to accept or reject it by tone.
* **No real peer review of this book's project has taken place.**

---

## The Constructed Review, Checked

| # | Comment | Check | Verdict |
|---|---|---|---|
| R1 | "`DirectoryReservationService` now branches on `VISITOR`. Will that grow?" | One `if` on the category, delegating to the gate | **Valid**: KI-14, trigger a second category |
| R2 | "Where is the flag read in production?" | Only `Chapter13Demo` reads `lending.visitors` and passes a boolean to `VisitorGate`; no static state | No issue |
| R3 | "Is the old two-argument constructor safe for visitors?" | `ac12_...` builds one and asserts the disabled rejection | Covered |
| R4 | "The README says 230 tests. I count 233." | The count appeared in both README and HANDOVER | **Valid**: a number stated in two places rots |

* **R4 changed the version**: the README now states no number, and `handover-check.sh` checks the numbers in `HANDOVER.md`.

---

# 14.2 Fix, Defer or Accept
### Scope control in the last week

---

## Everything Looks Improvable

* In the final sprint every team sees things it could improve. Some are **real defects**. Some are **polish**. Many are **new features in disguise**.
* If you act on all of them, **you finish nothing and introduce faults close to the deadline**.
* Three questions sort them. Ask them **in this order**.

---

## Three Questions

1. **Does it block a requirement or the demonstration?** If yes, it is a **blocker**: fix it first or change the plan.
2. **Does fixing it need a decision that is not ours?** If yes, it is **deferred**: record the question, the owner and what would trigger the decision.
3. **Is the cost and risk of changing it now worth the benefit?** If not, it is **accepted**: say so in writing, as a limit, not as a secret.

---

## Figure 14.2: Triage of a Known Issue

<!--svg:ch14-triage-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 320" role="img" aria-label="Figure 14.2: triage of a known issue. If it blocks a requirement or the demonstration, fix it now with a check. Otherwise, if it needs a decision that is not ours, defer it and record the question, the owner and the trigger. Otherwise, if it is worth the cost and risk now, fix it now with a check; if not, accept it and state it as a limit." style="display:block;width:100%;height:calc(var(--u) * 32.00);margin:0 auto">
<defs><marker id="ch14-triage-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-triage-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-triage-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-triage-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-triage-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="0.0" y="118.0" width="100.0" height="58.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="50.0" y="142.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">A known</text>
<text x="50.0" y="161.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">issue</text>
<polygon points="225.0,95.0 325.0,147.0 225.0,199.0 125.0,147.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="225.0" y="143.3" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Blocks a requirement</text>
<text x="225.0" y="159.5" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">or the demonstration?</text>
<polygon points="455.0,95.0 555.0,147.0 455.0,199.0 355.0,147.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="455.0" y="143.3" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Needs a decision</text>
<text x="455.0" y="159.5" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">that is not ours?</text>
<polygon points="685.0,95.0 785.0,147.0 685.0,199.0 585.0,147.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="685.0" y="143.3" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Worth the cost</text>
<text x="685.0" y="159.5" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">and risk now?</text>
<rect x="255.0" y="6.0" width="195.0" height="58.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="352.5" y="30.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Fix now,</text>
<text x="352.5" y="49.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">with a check</text>
<rect x="330.0" y="246.0" width="250.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="455.0" y="272.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Defer: record the question,</text>
<text x="455.0" y="289.5" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">the owner and the trigger</text>
<rect x="600.0" y="246.0" width="170.0" height="60.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="685.0" y="272.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Accept: state it</text>
<text x="685.0" y="289.5" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">as a limit</text>
<path d="M100.0,147.0 L125.0,147.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-triage-arr)"/>
<path d="M325.0,147.0 L355.0,147.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-triage-arr)"/>
<text x="340.0" y="138.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">no</text>
<path d="M555.0,147.0 L585.0,147.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-triage-arr)"/>
<text x="570.0" y="138.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">no</text>
<path d="M225.0,95.0 L225.0,35.0 L255.0,35.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-triage-arr)"/>
<text x="203.0" y="75.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">yes</text>
<path d="M685.0,95.0 L685.0,35.0 L450.0,35.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-triage-arr)"/>
<text x="707.0" y="70.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">yes</text>
<path d="M455.0,199.0 L455.0,246.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-triage-arr)"/>
<text x="475.0" y="224.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">yes</text>
<path d="M685.0,199.0 L685.0,246.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-triage-arr)"/>
<text x="703.0" y="224.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">no</text>
</svg>
</div>
<!--/svg-->

---

## Reading the Triage

* **Every path ends in something written down.**
* **"Fix now" ends with a check**, so the fix is visible later.
* "Accepted" is **not "ignored"**: the team decided, with a reason, and a reader can find the reason.

---

## What the Project Did With Its Own List

* The visitor project has **fourteen known issues** (`docs/KNOWN-ISSUES.md`).
* **One was fixed.**
* **Seven are deferred:** five wait for an owner's decision, one for a JDK 17 and a hosted runner, one for the flag decision.
* **Six are accepted limits.**
* Every row has a **decision, a reason and a next step**.

---

## The Fixed One

* **KI-1:** the demonstration program needed a directory service that only the tests could start, so **a new reader could not run it**.
* That is a **blocker for a handover**: a reader who cannot run the system cannot check anything else about it.
* The fix added **no behaviour**. It added a small launcher (`DemoRun`) that starts the same test stub and runs the system twice, and a script, `scripts/demo.sh`.
* It is covered by the dry run in `scripts/handover-check.sh`.

---

## Deferred Issues (1 of 2)

| ID | Item | Why deferred |
|---|---|---|
| KI-2 (SD-11-1) | A kind other than student or staff is fined at 1.00 a day with no grace and no cap; **a late visitor now reaches it** (AC18 pins it) | Only the records office can say what the rate should be |
| KI-3 (SD-11-2) | A loan within the grace period is listed with fine 0.00 and counted as overdue | Needs the owner's answer to "should it appear at all?" |
| KI-4 (SD-11-3) | A null kind throws `NullPointerException`, only for an overdue unreturned loan | Ask whether the export can contain one |
| KI-5 (SD-11-4) | Amounts use the default locale (`0,50` under a German locale) | Owner decides whether the separator follows the machine or the office |

---

## Deferred Issues (2 of 2)

| ID | Item | Why deferred |
|---|---|---|
| KI-6 (SD-12) | The count rule counts every retained reservation, including returned ones | Preserved on purpose by CR-12 and pinned by AC11; owner decides |
| KI-12 | No Java 17 run and no hosted CI run; action versions not re-checked | Needs a JDK 17 and a hosted runner |
| KI-13 | The visitor flag is still in the code | Decided in ADR-014; removal rehearsed |

---

## Why Not Just Fix SD-11-1?

* It is tempting to "fix" it by giving visitors a sensible rate.
* But **nobody on the team knows the right rate. Only the records office does.**
* A guess would be **a new rule disguised as a bug fix**, and it would **hide the question** and change AC18.
* So it is deferred: **the question, the owner, and the test that will change when the answer arrives are all written down.**

---

## Accepted Issues (1 of 2)

| ID | Item | Why accepted |
|---|---|---|
| KI-7 | One bad row in the approval register rejects the whole register | A silent skip could hide a lost approval or a duplicate; revisit with real use |
| KI-8 | The directory wait defaults to **one second and was not measured**; it bounds the whole lookup, body included | A setting (`lending.directory.timeout.millis`); measure before changing. Stalled-body case tested on a newer JDK only |
| KI-9 | No retry and no cached answer after an outage | By design (ADR-013); revisit after measured outages |

---

## Accepted Issues (2 of 2)

| ID | Item | Why accepted |
|---|---|---|
| KI-10 | The directory stub and the approval file are stand-ins | Needs a provider contract test against a real service, which does not exist here |
| KI-11 | Concurrency (two writers of the register, simultaneous requests) was not considered | Out of scope; the register is a trusted sequential file |
| KI-14 | `DirectoryReservationService` branches on the visitor category | Fine for one special category; at a second, refactor with its own tests |

---

## Resist the Plausible Additions

| Tempting addition | Why not now |
|---|---|
| Retry the directory call after a timeout | Changes the one-attempt contract of earlier chapters; **nobody has measured an outage** |
| Replace the approval file with JSON or a database | Nothing in the requirement needs it; **adds a new boundary to test** |
| Remove the flag to "clean up" | **The conditions for removal do not hold** (14.3) |
| Give a visitor a late-fine rate | **A decision for the records office**, not the team |
| Add a second category of visitor | **A new requirement**: raise it as a change request, not as polish |

---

## The Costs of a Feature Built Before It Is Needed

Fowler names four:

1. **The cost of building it.**
2. **The cost of the delay** it causes.
3. **The cost of carrying its complexity.**
4. **The cost of repairing it** if its assumptions were wrong.

* In the last week, **the delay and the repair cost are the ones that hurt.**

---

## A Release Is "Done" by a Definition, Not a Feeling

* The Scrum Guide defines a **Definition of Done** as the state an increment must reach to meet its quality measures; work that does not meet it **cannot be part of the increment**.
* Write yours for the handover version, as a short list **a check can confirm**:
  * the pipeline passes;
  * the handover check passes;
  * no test is skipped;
  * every number in a document matches a run;
  * every decision record has a true status;
  * every known issue has a decision.

---

# 14.3 Writing It Down
### Documents, decision records and release notes

---

## One Document per Question

* A new reader asks different questions at different times. One long document answers none of them well.
* The project has **six documents**, and **each is kept true in a different way**.
* Appendix C has forms for the requirements table and known-issues list (C.10), decision records (C.5) and release notes (C.11).

---

## The Six Documents (1 of 2)

| Document | Question it answers | How it is kept true |
|---|---|---|
| `README.md` | What is this, and where do I start? | Short; points to the others |
| `docs/HANDOVER.md` | How do I set it up, run it and understand it in an hour? | **`scripts/handover-check.sh` follows it in a fresh copy** |
| `docs/REQUIREMENTS-TO-EVIDENCE.md` | Which test checks each requirement? | **`TraceabilityTest` fails** if a named test or class is gone |

---

## The Six Documents (2 of 2)

| Document | Question it answers | How it is kept true |
|---|---|---|
| `docs/KNOWN-ISSUES.md` | What is wrong or missing, and what was decided? | A reviewer; every row has a decision |
| `docs/ADR-0NN-*.md` | Why is it built this way? | Never edited after acceptance except its status; **a new record supersedes it** |
| `docs/RELEASE-NOTES-*.md` | What changed in this version? | Written at release; one file per version |

* **The cheapest document to maintain is one that a check keeps true.** Wherever a statement can be checked by a script, write the script.

---

## Decision Records

* A record captures **a decision, not a description of the code**. Nygard proposes short records in the repository:
  * **title**, **context** (the forces at play), **decision**, **status** (proposed, accepted, or later superseded), **consequences**;
  * **numbered in order and never reused**; a reversed decision's old record stays and is marked **superseded**.
* This project's records add three parts that earn their place: **alternatives considered**, **how the decision was validated**, and **triggers for revisiting it**.

---

## ADR-014: Keep the Flag at Handover

ADR-013 set three conditions for removing the flag. ADR-014 **checks each one**:

| Condition from ADR-013 | State |
|---|---|
| The pipeline has run both settings | **True** |
| The visitor contract has been accepted by an owner | **Not yet** |
| A decision to keep visitors enabled is recorded | **Not yet** |

* **Decision: keep the flag, default off, and rehearse the removal** so the change is ready and its cost is known.
* It does **not** remove the flag and does **not** edit ADR-013. Status: a model decision by the book's author, **not an institutional decision**.

---

## ADR-014: Alternatives and Consequences

* **Remove the flag now:** rejected. It would turn an **unaccepted teaching contract into permanent behaviour** and remove the one switch that stops new visitor reservations without a new build.
* **Keep the flag with no removal plan:** rejected. **An owner-less flag is a permanent branch.**
* **Replace the flag by run-time configuration:** not adopted; outside the scope of the module.
* **Consequence:** both paths stay tested (AC12, the flag-off journey, the gate's disabled tests). A visitor can never be served unless someone sets the property to `true`.

---

## Release Notes

* A changelog is for people. **Keep a Changelog** groups changes as **Added, Changed, Deprecated, Removed, Fixed and Security**, gives each version its own dated entry and puts the **newest first**.
* The notes for version 0.14.0 use three of those headings and add two of their own that a handover needs: **"Behaviour you should know about"** and **"Not verified"**.
* The first line says **no production behaviour changed**: a statement a reader can check, and it was checked. **Every file under `src/main` is byte for byte as in 0.13.1.**

---

# 14.4 Keeping the Evidence True
### Rehearsal and traceability

---

## Rehearse a Risky Removal

* Removing a flag looks like deleting an `if`. **Rehearsed in a scratch copy, it touched eleven files**, with **87 lines added and 131 removed**.
* The flag was a constructor parameter, a result text, a factory for the old two-argument constructor, a system property in the demonstration, **AC12 which exists only for the flag**, two other acceptance examples that mention it, a journey that tests the flag off, and two documents that explain it.
* After the rehearsal: the full build **233 invocations, 0 failures**, the pipeline passed, the handover check passed. The patch is stored in `rehearsal/` and **not applied**.

---

## The Eleven Files of the Rehearsal

| File | Change |
|---|---|
| `VisitorGate.java` | Removes `DISABLED`, the flag and the `disabled()` factory; adds `noApprovals()` |
| `DirectoryReservationService.java` | Two-argument constructor uses `VisitorGate.noApprovals()` |
| `Chapter13Demo.java`, `DemoRun.java` | No `lending.visitors` property; the demo runs once |
| `VisitorGateTest.java`, `VisitorAcceptanceTest.java` | Flag argument dropped; AC12 becomes "no register approves no visitor"; AC13 and AC16 renamed |
| `Chapter13JourneyE2ETest.java` | Removes the flag-off journey, two remain |
| `DirectoryOutageIntegrationTest.java` | `disabled()` becomes `noApprovals()` |
| Requirements table, `HANDOVER.md`, `handover-check.sh` | Names and counts: 233 total, 205, 26 and 2 |

---

## What the Rehearsal Also Taught

* **Retiring AC12 means a requirement in the specification disappears with the flag**: "a disabled flag rejects explicitly" has no meaning without a flag. That is **a change to the specification**, and it needs a decision, not just a patch.
* `TraceabilityTest` is why the table edits are in the patch: without them the build fails on the first stale test name, **the check doing its job**.
* **Prose is not edited by the patch:** `README.md`, the rest of `HANDOVER.md` and ADR-013 still say the flag exists.
* After removal, **the rollback is a redelivery of the previous release**, because there is no longer a switch.

---

## Requirements to Evidence

* **Traceability** is the chain from a requirement to **the code that decides it** and **the test that checks it**.
* In a small project a table is enough: ten contract clauses and eighteen acceptance examples, each traced to a deciding class and a test, plus **five known gaps** (requirements with no evidence here).
* The last link of the chain is the one that **stops the table rotting**.

---

## Figure 14.3: The Chain

<!--svg:ch14-chain-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="Figure 14.3: the chain that the requirements-to-evidence table records. A requirement or example leads to the class that decides it and to the test that checks it. The test leads to the pipeline stage that runs it. Both the class and the test are checked by TraceabilityTest, which asks whether the name still exists." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch14-chain-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-chain-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-chain-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-chain-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch14-chain-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="124.0" width="180.0" height="62.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="100.0" y="150.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Requirement</text>
<text x="100.0" y="170.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">or example</text>
<rect x="290.0" y="28.0" width="190.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="385.0" y="53.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Class that</text>
<text x="385.0" y="73.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">decides it</text>
<rect x="290.0" y="220.0" width="190.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="385.0" y="245.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Test that</text>
<text x="385.0" y="265.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">checks it</text>
<rect x="600.0" y="118.0" width="250.0" height="74.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="725.0" y="141.3" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">TraceabilityTest:</text>
<text x="725.0" y="160.1" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">does the name</text>
<text x="725.0" y="178.8" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">still exist?</text>
<rect x="600.0" y="222.0" width="250.0" height="56.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="725.0" y="245.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Pipeline stage</text>
<text x="725.0" y="264.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">that runs it</text>
<path d="M100.0,124.0 L100.0,58.0 L290.0,58.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-chain-arr)"/>
<path d="M100.0,186.0 L100.0,250.0 L290.0,250.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-chain-arr)"/>
<path d="M480.0,58.0 L725.0,58.0 L725.0,118.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-chain-arr)"/>
<path d="M440.0,220.0 L440.0,155.0 L600.0,155.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-chain-arr)"/>
<path d="M480.0,250.0 L600.0,250.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch14-chain-arr)"/>
</svg>
</div>
<!--/svg-->

---

## What TraceabilityTest Checks

| Check | Method |
|---|---|
| Every test named in the Evidence column exists as a method | `everyTestNamedInTheTableStillExists` (also requires **at least 29** named tests, so a deleted row cannot hide) |
| Every class named in the Decided by column exists under `src/main` | `everyClassNamedAsDecidingStillExists` |
| AC1 to AC18 each have **exactly one row**, and every `ac<N>_` test appears in the table | `everyAcceptanceExampleHasExactlyOneRowAndEveryAcceptanceTestIsInTheTable` |
| That a named test is **the right evidence** | **Not checked: a reviewer decides** |

---

## Does the Traceability Check Detect Faults?

| Fault | Result |
|---|---|
| A named test is renamed | **Caught**: two of three methods fail |
| An acceptance example loses its row | **Caught**: two of three methods fail |
| A deciding class is renamed in the table (`VisitorGuard`) | **Caught** |
| An acceptance test is added that no row mentions | **Caught** |
| A row names an extra test that exists | **Not caught**; harmless |
| AC3 is pointed at the AC1 test, which exists | **Not caught**: a wrong mapping only a reviewer finds |

* **A script can check that a name exists. Only a reviewer can check that a name is the right evidence.** Say so in the document.

---

# 14.5 Setup and a Demonstration That Anyone Can Reproduce
### Write for someone who is not you

---

## Write for Someone Who Is Not You

* Your own machine has things installed that you have forgotten about. **The only way to find them is to try the instructions somewhere else.**
* The handover document begins with **what you need**: a full JDK 17 or later with the `jdk.jdeps` module, Maven 3.9.11, a POSIX shell, network access for the first build.
* Then **three commands with their expected output**, then how to see the system working.

---

## A Script Can Follow the Document for You

* `scripts/handover-check.sh` copies the project, **without build output**, into a new folder, runs the pipeline and the demonstration there, and **compares what they print with what the document promises**.
* It ends with `HANDOVER CHECK PASSED` after **twelve `ok` lines**.
* If a test is added and nobody updates the document, **the script fails**. It also fails if the document is edited to a number the run does not give.

---

## Does the Handover Check Detect Faults?

| Fault | Output |
|---|---|
| A test added | `FAIL stage 2 ran 206 invocations`: stage 2 shows 207; one problem |
| A word changed in the demonstration output | `FAIL an outage is reported as unavailable`; the pipeline fails too, because the journeys check the same line: three problems |
| `HANDOVER.md` edited to promise 232 invocations | `FAIL HANDOVER.md promises 235 invocations in total`; one problem |

* All three were caught. These are a few faults chosen by the author; they show the check notices **a document that disagrees with a run**, not one that is wrong in a way **the script cannot see**.

---

## The Test Counts the Document Promises

| Stage | Chapter 13 | Chapter 14 |
|---|---:|---:|
| 2 Unit tests and architecture checks | 203 | **206** (adds `TraceabilityTest`, 3) |
| 3 Integration | 26 | 26 |
| 4 End-to-end | 3 | 3 |
| **Total** | 232 | **235** |

* `mvn --batch-mode verify` ends with `Tests run: 235, Failures: 0, Errors: 0, Skipped: 0` and `BUILD SUCCESS`.

---

## What the Dry Run Found (1 of 2)

Following the handover in a fresh folder found **four things before any reader did**.

| Finding | Effect on a new reader | Change |
|---|---|---|
| **D1.** The setup assumed `mvn` was on the PATH; on the test machine it was not, and the failure said only `command not found` | The reader **stops at step 1** | The document starts with a tool check; scripts print a clear message and exit with status 2 |
| **D2.** On a recent JDK, Maven 3.9.11 prints `WARNING` lines about `sun.misc.Unsafe`, and the mocking library prints a dynamic-agent warning | A reader may think the build is broken | The document lists **"things you may see that are not errors"** |

---

## What the Dry Run Found (2 of 2)

| Finding | Effect on a new reader | Change |
|---|---|---|
| **D3.** The demonstration needed a directory service that only the tests could start (KI-1) | The reader **could not see the system work** | `DemoRun` and `scripts/demo.sh` |
| **D4.** The new clear message **rejected a valid Maven path on Windows** (a `.cmd` file that is not executable in the shell sense) | The check meant to help would have blocked a correct setup | Also accept a file that exists |

* **D4 was a fault in a fix written during this very exercise**, found only because the fix was run in the setting it was meant to protect.
* **A document you have not followed is a guess about what it says.**

---

## What Did Not Break

* A folder name **with spaces** was also tried, and worked.
* That is **a result, not a finding**: say what you tried that did not break.

---

## The Demonstration

* A short, repeatable story with **a fixed clock and fixed data**.
* `scripts/demo.sh` compiles, starts the local directory stub in one process, writes a small approval register, and runs the system **twice: visitors disabled, then enabled**.
* The viewer sees **the same requests produce different results**, and **an unreachable directory reported as unavailable, not as a missing borrower**.
* The handover suggests an outline of about ten minutes. **Your instructions decide the length and format** of your own demonstration.

---

## Expected Demonstration Output

```text
== visitors disabled ==
Visitors enabled: false
Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Visitor V1: Rejected: visitor reservations are not enabled.
Visitor V2: Rejected: visitor reservations are not enabled.
Unknown U9: Rejected: borrower not found or inactive.
Outage BROKEN: Unavailable: Borrower directory unavailable
Reservations: 1
Notices: 1
```

* The second run (`== visitors enabled ==`) confirms V1 as **R2 on CAM2**, rejects V2 with **no valid sponsor approval**, and ends with **Reservations: 2, Notices: 2**.

---

## What the Dry Run Cannot Show

* It ran on **one operating system with one JDK** and a local Maven repository that already held the dependencies.
* It cannot show a **first build over a slow network**, a **Java 17 runtime**, a **different shell**, or **a reader who misreads a sentence you thought was clear**.
* To cover the last, **ask a real person from outside your team to follow the document while you watch and say nothing**. Write down every place they hesitate. **That is the test.**

---

# 14.6 Retrospective and Individual Reflection
### Evidence, not mood

---

## A Retrospective Is Evidence-Based or It Is a Mood

* The Scrum Guide's purpose for the Retrospective: plan ways to **increase quality and effectiveness**; inspect individuals, interactions, processes, tools and the Definition of Done; discuss what went well and wrong; identify the **most helpful changes**.
* **Kerth's Prime Directive** asks the team to assume everyone did the best they could, given what they knew and the resources they had.
* Together: **look at the work and the process, not at blame.**

---

## Bring the Records

* Make it evidence-based by bringing **the sprint's records**: the board, the pipeline runs (passing and failing), the review comments, the defect list, the time between starting and finishing items (Chapter 12).
* For each thing the team wants to say, ask: **what record shows it?**
* **Keep the number of actions small.** Two actions with owners that are done beat ten that are not.

---

## From Observation to Action

| Observation | Evidence | Action | Owner and date |
|---|---|---|---|
| "Reviews were slow" | Two pull requests waited more than two days (board timestamps) | Review before starting a new item | Named person, next sprint |
| "The pipeline was flaky" | One of ten runs failed with no code change (run list) | Fix or quarantine the unstable test | Named person |
| "We rushed the end" | Seven items moved to Done on the last day | Plan a smaller scope and a freeze | Whole team |

---

## The Process Note, Revisited

* Chapter 3 asked each team to say which parts of Scrum it used **as defined** and which it **adapted** for the course.
* Now say **what the evidence shows about each adaptation**. For example: the course's sprints end at milestone weeks and not at a fixed calendar interval; a student team is not a full-time team; the Product Owner is usually a teaching role.
* For each adaptation: **did it help, did it hurt, what would you change?**
* This is **the closing of an earlier commitment**. It needs no new terms.

---

## Individual Contribution Is Evidence of Three Kinds

* The descriptor assesses individual contribution through **commits, pull-request reviews and peer evaluation**, and says team marks are **moderated by individual contribution**.
* **Each of these is an input. None is the answer.**
* Next: what each can and cannot show.

---

## What Each Kind of Evidence Can Show

| Evidence | What it can show | What it cannot show |
|---|---|---|
| **Commits** | That a change was made, by which author identity, when, and what it touched | **Effort, difficulty or importance.** Commit size is a habit; pair work is recorded under one author unless named in a `Co-authored-by` line; formatting and regenerated files inflate counts; squash merges turn many commits into one |
| **Pull-request reviews** | That someone read a change and what they said (comment, approval, request for changes) | **Whether the review was careful**; an approval says the changes look ready to merge, nothing about how thoroughly it was checked |
| **Peer evaluation** | How teammates experienced each other's work, including things no tool records | **Objectivity**: affected by friendship, conflict and what people happened to see |

---

## How Little a Count Can Be Trusted

* GitHub's account of its contribution graph: a commit counts **only when its author email is linked to the account**, and **only when it is on the default branch** or reaches it through a merged pull request; **commits made in a fork do not count until merged**.
* A person whose commits use the wrong email **appears to have done nothing.**

---

## A Constructed Example (Synthetic)

A team of three finished its last sprint with these counts.

| | Commits | Formatting only | Lines changed | PR reviews given | Requested changes |
|---|---:|---:|---:|---:|---:|
| P1 | 38 | 17 | 410 | 4 | 1 |
| P2 | 9 | 0 | 1,150 | 11 | 5 |
| P3 | 24 | 3 | 620 | 7 | 0 |

* Team total: **71 commits and 2,180 changed lines**.

---

## Four Rankings, Three Orders

| Measure | Order | Share |
|---|---|---|
| Commits | P1, P3, P2 | P1 has **38 of 71**, more than half |
| Lines changed | P2, P3, P1 | P1 has 410 of 2,180: **19%** |
| Reviews given | P2, P3, P1 | |
| Reviews requesting changes | P2, P1, P3 | |

* **Those numbers describe habits, not contributions.**
* The underlying facts, which only people and the work itself can supply, might be: P1's commits include seventeen formatting-only commits and several that undo each other, and P1 built the pipeline; P2 wrote the approval-file adapter in nine substantial commits and found two defects in review; P3 wrote the demonstration and the documents and did four pair sessions with P1, only two recorded.

---

## No Ranking Is Offered, and None Could Be

* The honest use of counts is **as a pointer to the work to read**.
* **"Why did P2 have so few commits?"** is a question to ask; the answer is in **the diff and the review**.
* A flawed alternative to avoid: `Contribution: P1 54%, P3 34%, P2 13% (by commits)`. **Habits are not contributions**, and the same team has three other orders by other counts.

---

## Write Your Contribution as Claims With Evidence

* An individual reflection does not say "I did a lot". It says **what you did, where to see it, what you learned from it and what you would do differently**.
* These are **prompts for thinking, not a rubric**: your approved instructions say what the reflection must contain.

| Part | Prompts |
|---|---|
| What I did | Three to five specific pieces of work, each with a **link or path** |
| What I decided | A design or process decision, the alternatives and why |
| What went wrong | A real fault or misjudgement, how it was found, the fix, what changed |

---

## The Reflection Prompts, Continued

| Part | Prompts |
|---|---|
| How I used AI | Where, with what input, what you accepted or rejected, how you verified it |
| What I did not do | **Honest limits**: work started and not finished, work you relied on others for |
| What I would change | One thing about your own practice |

* Appendix C has templates for the retrospective (C.12) and decision records (C.5). **Appendix E** gives a fuller guide to contribution evidence (E.4), the final handover (E.5) and the reflection (E.6). This chapter stands on its own without them.

---

# 14.7 Getting Ready for the Final Submission
### What is submitted, and what it must show

---

## What the Submission Must Show

* The descriptor says teams submit **the complete system built across the sprints**, a **short technical report** and an **individual reflection**, through a repository link, and give a **demonstration and presentation followed by questions**.
* It also names five things the submission must show. Use them as **the headings of an evidence index**:
  1. clean object-oriented design;
  2. justified use of design patterns and architecture;
  3. automated tests with continuous integration;
  4. evidence of safe refactoring;
  5. adaptability to the injected change in requirements.

---

## An Evidence Index for the Book's Project (1 of 2)

| Must show | Evidence | What it does not show |
|---|---|---|
| Clean OO design | Responsibilities and dependencies of Chapters 2, 5, 6, 10; the architecture tests | That it is the best design, or that anyone else reviewed it |
| Justified patterns and architecture | Chapters 9 and 10; ADR-010 | Any pattern the design does not use |
| Automated tests with CI | The test suite; the five-stage pipeline; the workflow file | **A hosted CI run: the workflow has never run** |

---

## An Evidence Index for the Book's Project (2 of 2)

| Must show | Evidence | What it does not show |
|---|---|---|
| Safe refactoring | Chapter 11: characterisation tests, stage-by-stage refactoring, probe | Behaviour on inputs the generator did not produce |
| Adaptability to the change | Chapter 13 footprint and tests; the requirements table; the rehearsed flag removal | **Whether the visitor rule is the right policy** |

---

## A Short Sequence

1. **Finish.** The final sprint and workshop feedback are for finishing.
2. **Freeze.** Decide a time after which **only fixes to the handover and blockers** are allowed.
3. **Run the handover check** on the frozen version.
4. **Review independently.** Use the free time before the demonstration to read the whole bundle **as a stranger**, fix what the dry run finds, and ask someone outside the team to follow it.
5. **Prepare** the demonstration and the report from the evidence index, and write your reflection **from your own work**.

---

## A Preparation Checklist (Not a Rubric) (1 of 2)

* The repository link **opens for a person who is not on the team**, and the default branch is the version you mean.
* A fresh copy **builds with the documented commands and prints the documented numbers**.
* The pipeline has run, and you can show **one passing run and one failing run you have read**.
* **Every number in a document matches a run. Every claim names the evidence.**

---

## A Preparation Checklist (Not a Rubric) (2 of 2)

* **Every decision record has a true status. Every known issue has a decision.**
* The limits statement says **what was not run**: for the book's project, a Java 17 runtime, a hosted CI run and any independent review.
* **Each person can say, with links, what they did.**
* The demonstration works **from a fresh checkout with only the documented setup**.
* **Do not claim a hosted run, a public deployment or a peer review that did not happen.** A local run is evidence of a local run.

---

# 14.8 Validating an AI-drafted README
### Validate a README that an assistant drafted

---

## The Activity

| | For this activity |
|---|---|
| Your goal | Decide which statements in an AI-drafted README are supported by the submitted version, and correct the rest |
| You start with | The README draft and the project at version 0.14.0 |
| What is in bounds | Verify every command, every feature claim and every limitation; **edit only the draft** |
| How to check | **Run each command**; read the code, tests and decision records each claim depends on |
| How to decide | A verdict on each statement, and a corrected README |

---

## The Ready-Made Example (1 of 2)

**Author-written fictional AI output**, asked to "write a README for the project":

```markdown
# Campus Equipment Lending System

A Java 11 application for reserving campus equipment, with support for students, staff and visiting researchers.

## Quick start

1. Build: `mvn package`
2. Run: `java -jar target/equipment-lending.jar`
3. Check everything: `mvn verify` runs all 230 tests, which pass in under 30 seconds.
```

---

## The Ready-Made Example (2 of 2)

```markdown
## Features

- Visiting researchers are enabled by default. Set `-Dlending.visitors=false` to turn them off.
- Visitors may reserve CAM1 or CAM2 for one to three days when a sponsor approval matches.
- Sponsor approvals are read from a CSV file. The file is cached in memory for speed.
- If the borrower directory does not answer within one second, the system retries three
  times and then treats the borrower as a student.
- `scripts/pipeline.sh` runs five stages and deploys the application to the staging server.
- Architecture rules are enforced by `DependencyRulesTest`.
- The system is production-ready and safe for concurrent use.

## Demonstration

Run `bash scripts/demo.sh` to see visitors rejected and then approved.
```

---

## The Task

* Split it into **separate statements**. For each decide:
  * **supported** (name the evidence);
  * **contradicted** (name the evidence and write the correct statement);
  * **not established** (say what would be needed).
* **Run every command; do not decide from the text.**
* A statement that is plausible is not a statement that is true. **A README that is partly right is more dangerous than one that is obviously wrong, because the reader stops checking.**

---

## Verdicts: Statements 1 to 6

| # | Statement | Verdict | Evidence |
|---|---|---|---|
| 1 | A Java 11 application | **Contradicted** | `release` is 17; `javac --release 11` fails at `LifecycleExamples.java`: switch rules not supported |
| 2 | Supports students, staff and visiting researchers | Supported | `BorrowerCategory`, ADR-013 |
| 3 | Build: `mvn package` | Supported | Produces `target/equipment-lending-0.14.0.jar` |
| 4 | Run: `java -jar target/equipment-lending.jar` | **Contradicted** | `Unable to access jarfile`; with the right name: `no main manifest attribute`. Run `java -cp target/classes edu.se506.lending.bootstrap.ReservationApplication` |
| 5 | `mvn verify` runs all 230 tests | **Contradicted** | 233 at the time of checking |
| 6 | ...under 30 seconds | Not established | About 21 seconds on one machine with cached dependencies: do not promise a time |

---

## Verdicts: Statements 7 to 11

| # | Statement | Verdict | Evidence |
|---|---|---|---|
| 7 | Visitors enabled by default; `-Dlending.visitors=false` turns them off | **Contradicted** | Default is `false`; the demo prints `Visitors enabled: false` |
| 8 | CAM1 or CAM2, one to three days, matching approval | Supported | C2, C3, C4 of the requirements table |
| 9 | Approvals are read from a CSV file | **Contradicted** | Tab-separated, fixed header, eight columns |
| 10 | The file is cached in memory | **Contradicted** | `theFileIsReadAfreshOnEveryCall` |
| 11 | One second, retries three times, then treats the borrower as a student | **Contradicted** (the one-second default is right) | One attempt, no retry, no fallback; `...IsNotRetried` asserts one request |

---

## Verdicts: Statements 12 to 16

| # | Statement | Verdict | Evidence |
|---|---|---|---|
| 12 | `pipeline.sh` runs five stages | Supported | Compile, unit and architecture, integration, end-to-end, package |
| 13 | ...and deploys to the staging server | **Contradicted** | Stage 5 only packages; the simulation copies a jar into a local folder |
| 14 | Rules enforced by `DependencyRulesTest` | Partly supported | Checks dependency direction (a separate test checks cycles), **not every rule** |
| 15 | Production-ready and safe for concurrent use | **Not established, contradicted by the project's own limits** | KI-10 and KI-11 |
| 16 | `bash scripts/demo.sh` shows visitors rejected then approved | Supported | The expected output above |

---

## Count the Verdicts

* Of **sixteen statements**: **six** are supported or partly supported as written, **eight are contradicted** and **two are not established**.
* Statements 5 and 6 split one sentence: this counts statements, not sentences.
* The corrected README is `ai-activity/README-corrected.md`. **Each command in it was run.**

---

## What Reading Reveals, and What Only a Run Does

* A reader who knows the project notices **the default of the flag** and **the CSV**.
* **Nobody notices that `java -jar` fails without running it**, because the sentence is exactly what a README usually says.
* **A draft in which half of the statements are contradicted reads as fluently as one that is right.**
* Notice also that the draft says **nothing about limitations**, and the corrected README adds them. **Do not use a generated README to approve generated code.**

---

# 14.9 Handover Habits That Mislead
### Ten to avoid

---

## Mistakes 1 to 5

| Mistake | Consequence | Better action |
|---|---|---|
| The last week as a chance to add a feature | Late faults; a handover describing a system that no longer exists | Triage as fix, defer or accept; freeze |
| "Fixing" a suspected defect that needs an owner's answer | A guess becomes a rule; the question is lost | Defer with the question, the owner and the test that will change |
| Judging a change by the size of its diff | A tiny diff that fails the requirement looks good | Judge against the acceptance examples and across all stages |
| A README written from memory | Counts, commands and defaults that were once true | Follow it in a fresh copy; let a script check what it can |
| Documents nobody checks | They rot, and a reader trusts them anyway | A check or a reviewer for each |

---

## Mistakes 6 to 10

| Mistake | Consequence | Better action |
|---|---|---|
| Editing an old decision record to match what happened | The reasons for the decision are lost | A new record that supersedes or applies it |
| Removing a flag as tidy-up | The specification changes silently, and so does rollback | Rehearse, decide, update the examples that mention the flag |
| Ranking teammates by commit counts | Habits mistaken for contribution | Counts point to the work; read the work |
| "I contributed a lot" | Nothing can be checked | Claims with links, and honest limits |
| Claiming a hosted run, a review or a Java 17 run that did not happen | The submission loses credibility, and so do the true claims | Say what was not run |

---

## Diagnostic Alternative: A Number Stated in Two Places

```text
README.md:    "The build executes 230 JUnit invocations ..."
HANDOVER.md:  "Expected: Tests run: 233 ..."
```

* One is stale the moment a test is added, and **a reader cannot tell which**. **State a number once, and have a script check it.**

---

## Diagnostic Alternatives: Edited Record and Guess

```markdown
# ADR-013 ...
Status: Accepted
- Introduce one flag ... (edited on 20 October: the flag was removed)
```

```java
// WRONG for a handover sprint: nobody knows the visitor rate.
private static final FinePolicy VISITOR = new FinePolicy(2, 0.50, 10.00);
```

* The edit **loses the reasons the team had at the time**: write a new record. The constant looks like a repair of SD-11-1; it is **a new rule, hides the question and changes AC18**.
* A claim that did not happen: `CI: passing on GitHub Actions`. The workflow has never run: say **"workflow file written, not run"**.

---

# 14.10 Try It Yourself
### Hand the project over

---

## What You Start With, and the Demonstration

* **You start with:** the Chapter 14 version (version 0.14.0) with the companion's files, the Chapter 13 material, and your team's repository. **B1 to B8** use the book's project; **T1 to T5** use your team's project.
* **Instructor demonstration:** run `scripts/handover-check.sh` and read it. **Break one thing** (add a test, or rename a word in the demonstration output) and run it again. Run `TraceabilityTest` after renaming a named test. **Show the one-line adapter change that passes the unit stage and fails the integration stage.**
* **Guided practice:** classify four known issues of your choice as blocker, deferred or accepted, and say what evidence each decision rests on. Find the row of the requirements table **you trust least**.

---

## The Book's Project: B1 and B2

* **B1. Predict and measure what breaks.** In a scratch copy, remove the visitor policy from the map in `ReservationApplication.create`. **Predict** how many invocations fail, in how many classes, and what the message says. Run, compare, say what it shows. Restore the original.
  * Good answer: most of the suite fails (**73 of 235, 14 classes**), every message names the missing policy; the design **fails fast and precisely, and the cost is breadth**. It does **not** show the code is correct.
* **B2. Triage.** Take **five items** from `docs/KNOWN-ISSUES.md`; check each decision against the three questions and say whether you agree. **Add one item you find yourself**, with a decision.

---

## B2: A Good Answer

| Item | Decision | Reason |
|---|---|---|
| KI-2 (SD-11-1, visitor late-fine rate) | Defer | Needs the records office; any rate would be a guess |
| KI-7 (whole-file rejection of the register) | Accept | A silent skip could hide a lost approval or a duplicate |
| KI-8 (one-second wait, not measured) | Accept | A setting; measure before changing |
| KI-12 (no Java 17 or hosted CI run) | Defer | Needs a JDK 17 and a hosted runner |
| KI-14 (the `VISITOR` branch) | Accept | Fine for one category; refactor at the second |

* **A good new item** comes from reading the project: `DemoRun` fixes the clock, so the demonstration **cannot show an approval that expires**.

---

## The Book's Project: B3 and B4

* **B3. Follow the handover.** Run `scripts/handover-check.sh`. Then follow `docs/HANDOVER.md` **by hand** from a new folder, and list **every place where you had to guess** or where the text was wrong for your setup. Likely: where the project directory is, how to set `CHAPTER_MVN`, what the warnings mean, how long the build takes.
* **B4. Trace and break a row.** Choose one contract clause, one acceptance example and one known gap. For each, **open the named test** and say whether it checks what the row claims. **Rename one named test** in a scratch copy, run `TraceabilityTest`, read the failure. Then name **something the check cannot catch**.
  * Example: C5 is checked by `VisitorGateTest.theWindowIncludesItsStartAndExcludesItsEnd`, which tests exactly the two edges and one instant before the start.

---

## Your Team's Project: T1 and T2

* **T1. Review your change.** Fill in the four questions of 14.1 **with real evidence**: files and responsibilities affected, what failed when you started, the assumptions overturned, **the review comments you actually received**. Say **where the design did not absorb the change cleanly**.
* **T2. Triage your open items.** A known-issues list with a **decision for each item** (fix, defer, accept), a reason, and **an owner for the deferred ones**. **Fix only blockers. Freeze.**

---

## Your Team's Project: T3 to T5

* **T3. Build the handover bundle.** Setup instructions, a usage example, known limitations, test instructions, a requirements-to-evidence table and a demonstration outline. **Dry run in a fresh copy, then have someone outside your team follow it while you watch.** Record what they struggled with and fix it.
* **T4. Decide and record.** At least **two decision records**: one about your flag or change (keep, remove or replace, with the conditions) and one other. Give each **a true status**.
* **T5. Retrospective, reflection and checklist.** An evidence-based retrospective with **at most three actions**. Your individual reflection as **claims with links**. Complete the 14.6 checklist, **marking each item complete or a gap**.

---

## If You Want More: B5 to B7

* **B5. Rehearse the removal.** In a scratch copy apply `rehearsal/remove-visitor-flag.patch` (`patch -p1`), run the build (233 invocations) and the handover check; **list the documents whose prose the patch does not edit**: `README.md`, `HANDOVER.md` section 6, ADR-013, `KNOWN-ISSUES.md` (KI-13), and the descriptions in the requirements table.
* **B6. AI activity.** Complete 14.8.
* **B7. Read a synthetic contribution table.** Using the synthetic table, **write two questions you would ask each team member** and what you would read to answer each. Say what you would **not** conclude from the counts.

---

## B8: Close the Gap That E3 Found

* Write the **focused unit test of `LegacyDirectoryAdapter`** that fails when kind `V` is mapped to staff.
* Use an in-memory client (no network) and check at least:
  * a row with kind `V` and status `Y` maps to `BorrowerCategory.VISITOR`, **not staff or student**;
  * a row with kind `V` and status `N` gives an empty result;
  * an unknown kind code **throws `DirectoryException` and is never defaulted**.
* Then apply the **one-line change** and show that **the unit stage now fails**.
* **A weak answer** adds a test that passes against the changed adapter too. The new tests raise the stage-2 count, so `handover-check.sh` and `HANDOVER.md` need their numbers updated: **the handover check doing its job**.

---

## What You Should End Up With, and When You Are Done

* **What you should end up with:** B1 to B4; for your team's project, the change review, the triage list, the handover bundle with its dry-run record, the decision records, the retrospective with its actions, the individual reflection and the completed checklist.
* **Acceptance:** every number in a document **matches a run**; the handover has been **followed by someone other than its author in a fresh copy**; every known issue has a **decision**; **no feature added in the final sprint** to fix an issue that needs an owner; every decision record has a **true status**; contribution is described with **claims and links, not ranked by counts**; the limits statement says **what was not run**.
* **Optional:** write a second handover for a different reader, such as the person who will operate the system.

---

# 14.11 Questions to Think with, and a Transfer Challenge
### Concept, diagnosis, transfer

---

## Concept Questions

1. Name the four questions of a change review and what each one's evidence cannot show.
2. A one-line change passes every unit test and fails four integration and end-to-end tests. What does that tell you about the change, and what does it tell you about the unit tests?
3. What is the difference between deferring an issue and accepting it? Give an example of each from the project.
4. What can a requirements-to-evidence check confirm, and what can it not?

---

## Diagnosis Questions

5. A teammate has 40 commits and another has 8. Name **three questions** you would ask before saying anything about their contributions, and something you would read for each.
6. Your handover says "run `mvn verify`; expect a stated number of tests" and a colleague adds a test. List **two things that could have noticed** and the cost of each.

---

## Guidance: Questions 1 to 4

1. **Responsibilities** (counts do not show importance); **what broke first** (shows only what tests cover); **assumptions** (only those written down); **reviewer comments** (only as good as the review).
2. The change is **smaller than the requirement**: it does not implement the flag, the register check or the failure behaviour. The unit tests cannot say so because **none goes through the adapter with a real visitor**. The stage that crosses the real boundary does: **that is the reason to have it**.
3. **Deferred** waits for a decision that is not ours, so it carries an **owner and a trigger** (SD-11-1). **Accepted** is a limit we decided to live with, so it carries **a reason and a statement** (the unmeasured one-second wait; no retry).
4. It can confirm a named test or class **exists** and each example has **exactly one row**. It cannot confirm that **the named test is the right evidence**: a reviewer does.

---

## Guidance: Questions 5 and 6

5. Are most of the 40 **formatting, generated or reverted**? (read the commit list.) **What are the eight?** (diffs and pull requests.) **Who reviewed whom, and what did the reviews find?** (review comments.) **Was there pair work recorded as one author?** (commit trailers, retrospective.) **Say nothing about contribution until the artefacts are read.**
6. **`scripts/handover-check.sh`** compares the pipeline's stage counts with what the handover promises; the cost is running the whole pipeline in a fresh copy, about a minute. **A reviewer** reading the pull request who knows the number is stated; the cost is attention and memory. **The script is cheaper to repeat.**

---

## Transfer Challenge: ML Model Serving

A small team has built an ML model-serving service. Its final sprint ends in a week. Plan its handover:

* a **README for a stranger**, the **tool check** and what the first run prints;
* a **demonstration** with a fixed model and fixed data;
* a **requirements-to-evidence table**;
* a **known-issues list** that includes what the team **did not evaluate about the model**;
* a **decision record** for the one flag that gates a model version;
* what you would put in the **limits statement**.
* Use synthetic model identifiers: no model needs to be trained.

---

## Transfer Guidance (1 of 2)

| Item | Content |
|---|---|
| README for a stranger | What the service does; what it needs (runtime, build tool, a model file or **a synthetic stand-in**); **three commands with expected output**; where the decisions are |
| Tool check | Runtime and tool versions with the output they should print; what to do if one is missing; **the warnings that are not errors** |
| Demonstration | A fixed model identifier, fixed synthetic data, a fixed clock if time matters, and a script that runs the same requests **with the gate off and on** |
| Requirements to evidence | Each rule (only approved versions served externally) to the class that decides it and the test, plus **a check that the names exist** |

---

## Transfer Guidance (2 of 2)

| Item | Content |
|---|---|
| Known issues | Including what was **not** evaluated about the model: **accuracy, fairness, drift**, behaviour on data unlike the synthetic data |
| Decision record | The flag that gates a model version: conditions for removal, the owner, and **what rollback does not undo** (responses already served) |
| Limits statement | No real model evaluated; synthetic identifiers; no load test; **no hosted run if none was made** |

---

# What to Take Away, and What Comes Next
### What to carry forward

---

## Summary

* A change is finished when **someone else can see what it did, trust what the documents say, and run it**.
* **Review the change with evidence, not feelings:** responsibilities affected, failures caused, assumptions overturned, feedback received.
* Sort what remains into **fix, defer and accept**; leave deferred questions **with their owners**.
* Write the few documents a stranger needs; give each **a check or a reviewer**.
* **Follow your own instructions in a fresh copy**, and let someone else follow them too.
* Describe each person's work as **claims with links**, never ranked by counts. **Say what you did not run.**

---

## Where the Project Stands

* The visitor project is handed over at **version 0.14.0**: its flag decided, its removal rehearsed, **fourteen known issues with decisions**, and **two unresolved questions for an owner**: **SD-11-1** (the late-fine rate) and **SD-12** (the count rule).
* **Chapter 15** collects the assistance workflows that recur through the book and the verification records that make them reviewable.

---

## Sources and Further Reading

1. **Nygard:** *Documenting Architecture Decisions* (2011). **Keep a Changelog 1.1.0.**
2. **Schwaber and Sutherland:** *The Scrum Guide* (2020). **Kerth:** *The Retrospective Prime Directive*.
3. **Fowler:** *Yagni*. **Hodgson:** *Feature Toggles (aka Feature Flags)*.
4. **GitHub:** documentation on contribution graphs, commits with multiple authors and pull request reviews.
5. **Martin:** *Agile Software Development* (2002).

* Full references and links are in the chapter text.
