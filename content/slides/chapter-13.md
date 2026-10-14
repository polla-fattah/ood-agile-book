---
title: "Chapter 13: Integration, Delivery and Feedback"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 130
type: slides
layout: page
---

# Chapter 13: Integration, Delivery and Feedback
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 2)

* **13.1 What can go wrong at a boundary? Risks and test scope**
  * Start from the risk, then pick the check.
* **13.2 Where our code meets the outside: integration and contract tests**
  * A real file, a controlled local service, an explicit failure policy.
* **13.3 A few end-to-end journeys**
  * The real boundary of a command-line program is the process.
* **13.4 Pipeline stages and quality gates**
  * A pipeline orders the checks by cost.
* **13.5 Delivery is not deployment**

---

## Chapter Roadmap (2 of 2)

* **13.6 Feature flags, configuration and rollback**
* **13.7 Did the change work? Verifying the changed behaviour**
  * The order of the visitor decision and the 18 acceptance examples.
* **13.8 Preparing the Milestone 4 evidence**
* **13.9 An integration test that mocks its boundary: judging an AI proposal** inspect an integration test that replaces its boundary.
* **13.10 Delivery habits that mislead**
* **13.11 Try it yourself: run the pipeline and deliver a flagged change**
* **13.12 Questions to think with, and a transfer challenge**
* **What to take away, and what comes next**
  * Chapter 14: review the design, hand over, decide the flag's removal.

---

## Learning Outcomes (1 of 2)

After this chapter, you should be able to:

1. **Choose unit, integration and end-to-end checks** for different risks, and say what each cannot show.
2. **Explain the scope of a contract test** and write one that several implementations must pass.
3. **Implement a changed requirement** with regression protection and a clear separation between expected rejections and operational failures.

---

## Learning Outcomes (2 of 2)

4. **Configure a modest delivery pipeline**, run it and read a failure in it.
5. **Distinguish continuous delivery from continuous deployment**, and label a simulated deployment as one.
6. **Evaluate a feature flag and a rollback plan**, including what rollback does not undo.

---

## Where This Chapter Fits and Where You Start

* Supports **LO3 and LO6** and **Milestone 4**: the change absorbed, with integration tests and CI/CD.
* Required reading: Martin (2002), *Testing* (review). Recommended: selected chapters of Humble and Farley, *Continuous Delivery*.
* The practical activity is an **automated build, test and integration pipeline**.
* This chapter creates **no new deadlines, weights or marking rules**; the approved Milestone 4 instructions decide what you submit.
* **Entry version:** the Chapter 11 project, Chapter 12's change specification **CR-12**, its acceptance matrix (**AC1 to AC18**) and its ordered backlog.
* **This chapter implements the change.** The companion lists only the files that are new or changed.

---

## How to Use This Chapter

* **Core:** 13.1 to 13.5 and 13.7 to 13.8.
* **Working knowledge:** 13.6, feature flags, configuration and rollback. **Learn to run one flag safely; you do not build a flag platform.**
* **What you must do:** steps **B1 to B4** (the book's project: running, tracing and diagnosis, nothing to rebuild) and **T1 to T5** (your team's project: your Milestone 4 evidence).
* **If you want more:** B5 to B7 (deliver and roll back a simulated release, the AI activity, break a boundary on purpose), the review questions, the transfer challenge.

---

## Opening Problem: Demonstration Morning

The visiting-researcher rule passes every unit test and works on the developer's laptop. On the morning of the Milestone 4 demonstration, three things go wrong:

1. The sponsor register exported by the office has a **stray column**, so a visitor request ends in an exception.
2. The borrower directory takes **eleven seconds** to answer, and the officer's screen freezes.
3. The new flag is **on for the demonstration but off in the build**: the build is green and the demonstration fails.

---

## What Went Wrong

* **None of these is a mistake in the rule.** Each lives at the **boundary** between our code and something it does not control: a file, a network service, a setting.
* A unit test that builds its own objects by hand **cannot see a boundary**, because the boundary is exactly what the test has replaced.
* This chapter checks **the places where our code meets something else**, orders those checks in a pipeline, and releases a change in a way that can be **undone**.
* The worked change is **CR-12**: visiting researchers, with sponsor approval, behind one flag. It is a **teaching contract, not an institutional policy**.

---

# 13.1 What Can Go Wrong at a Boundary?
### Risks and test scope

---

## Which Kind of Test Should I Write?

* That is the wrong **first** question.
* Ask: **what could go wrong** in this change, **where** it would go wrong, and **which check would notice**.
* Then choose **the cheapest check that can notice it**.
* The next two slides do that for CR-12.

---

## Risks and the Cheapest Check (1 of 2)

| What could go wrong | Where | Cheapest check that can notice |
|---|---|---|
| Validity window off by one at its edges | Approval record | Unit test with a controlled instant |
| A visitor served without a matching approval | Visitor gate and service | Acceptance examples with a controlled approval source |
| Stray column or a bad date in the register | File adapter | Integration test with a **real temporary file** |

---

## Risks and the Cheapest Check (2 of 2)

| What could go wrong | Where | Cheapest check that can notice |
|---|---|---|
| Directory slow, down or answering nonsense | HTTP client | Integration test against a **local stub service** |
| Flag read in the demonstration but not in the build | Whole program | End-to-end journey in a **separate process** |
| Old behaviour changed by accident | Existing code | The existing regression suite |

* Each check has a limit. Next: **what each one cannot show.**

---

## What Each Check Cannot Show

| Check | What it cannot show |
|---|---|
| Unit test with a controlled instant | That the register file is read correctly |
| Acceptance examples with a controlled source | That the real register has the shape the source expects |
| Integration test with a real temporary file | That the office's real export looks like the test file |
| Integration test against a local stub | That the real provider behaves like the stub |
| End-to-end journey in a separate process | Behaviour at scale, or with real users |
| Existing regression suite | Anything the old suite never covered |

---

## Three Names Used Throughout

* A **unit test** runs a small part of the system in memory, with everything it collaborates with **controlled**.
* An **integration test** runs our adapter against **the real mechanism it adapts**: a real file, a real HTTP client talking to a service under our control.
* An **end-to-end journey** starts **the whole program the way a user would**, in a separate process.

---

## Figure 13.1: The Two Boundaries Added by CR-12

<!--svg:ch13-boundaries-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 330" role="img" aria-label="Figure 13.1: the two boundaries added by CR-12. The officer&#x27;s command-line demo calls DirectoryReservationService, which calls LegacyDirectoryAdapter, then HttpLegacyDirectoryClient, which reaches the directory service over HTTP with a bounded wait. The service also calls VisitorGate, then FileApprovalSource, which reads approvals.tsv on every call, and ReservationCoordinator." style="display:block;width:100%;height:calc(var(--u) * 33.00);margin:0 auto">
<defs><marker id="ch13-boundaries-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-boundaries-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-boundaries-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-boundaries-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-boundaries-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="5.0" y="128.0" width="120.0" height="64.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="65.0" y="146.8" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Officer:</text>
<text x="65.0" y="164.9" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">command-line</text>
<text x="65.0" y="183.1" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">demo</text>
<rect x="160.0" y="128.0" width="200.0" height="64.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="260.0" y="155.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Directory</text>
<text x="260.0" y="174.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">ReservationService</text>
<rect x="300.0" y="10.0" width="150.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="375.0" y="35.9" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Legacy</text>
<text x="375.0" y="54.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">DirectoryAdapter</text>
<rect x="490.0" y="10.0" width="175.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="577.5" y="35.9" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">HttpLegacy</text>
<text x="577.5" y="54.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">DirectoryClient</text>
<rect x="715.0" y="10.0" width="145.0" height="60.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="787.5" y="36.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Directory service</text>
<text x="787.5" y="53.5" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">(stub in tests)</text>
<rect x="300.0" y="250.0" width="165.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="382.5" y="276.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">VisitorGate</text>
<text x="382.5" y="293.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">flag, allowlist, window</text>
<rect x="505.0" y="250.0" width="160.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="585.0" y="275.9" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">FileApproval</text>
<text x="585.0" y="294.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Source</text>
<rect x="715.0" y="250.0" width="145.0" height="60.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="787.5" y="284.9" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">approvals.tsv</text>
<rect x="490.0" y="128.0" width="175.0" height="64.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="577.5" y="155.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Reservation</text>
<text x="577.5" y="174.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Coordinator</text>
<path d="M125.0,160.0 L160.0,160.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-boundaries-arr)"/>
<path d="M260.0,128.0 L260.0,40.0 L300.0,40.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-boundaries-arr)"/>
<path d="M450.0,40.0 L490.0,40.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-boundaries-arr)"/>
<path d="M665.0,40.0 L715.0,40.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-boundaries-arr)"/>
<path d="M360.0,160.0 L490.0,160.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-boundaries-arr)"/>
<path d="M260.0,192.0 L260.0,280.0 L300.0,280.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-boundaries-arr)"/>
<path d="M465.0,280.0 L505.0,280.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-boundaries-arr)"/>
<path d="M665.0,280.0 L715.0,280.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-boundaries-arr)"/>
<text x="690.0" y="94.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">HTTP, bounded wait</text>
<text x="690.0" y="238.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">reads on every call</text>
</svg>
</div>
<!--/svg-->

---

## Reading the Figure

* **Solid boxes are our code**; the two outer boxes (the directory service and the register file) are what we **do not control**.
* **Unit tests stop at the adapters.**
* **Integration tests cross the labelled arrows** with the real mechanism.
* **An end-to-end journey runs the whole picture** in a separate process.

---

## Narrow Checks First

* Fowler distinguishes **narrow** integration tests (our service's code that talks to another service, with that service replaced by a double) from **broad** ones (live versions of everything).
* Narrow checks are **small, fast and resilient**, so most boundary evidence in this chapter is narrow.
* A few **broad** checks remain worth having, because **only they show the pieces are joined correctly**.
* **Rule of thumb: many narrow checks, a few broad ones, and a reason for each.**

---

## A Boundary Is Where We Stop Controlling the Answer

* Our own classes answer the same way every time. A file may be missing today. A call may not return. A setting may differ between the machine that built the program and the one that runs it.
* Each boundary needs two kinds of evidence: **what happens when the other side behaves** and **what happens when it does not**.
* The most important design decision in the change is **how a failure at a boundary is reported**.

---

# 13.2 Where Our Code Meets the Outside
### Integration and contract tests

---

## The File Boundary: Use a Real File

* CR-12 keeps sponsor approvals in a **tab-separated register with eight columns**.
* `FileApprovalSource` reads it, **rejects it as a whole** if any row is invalid or any request key repeats, and returns the record for **one exact request**.
* Its tests **write real files into a temporary directory** and read them back through the real adapter.
* Nothing replaces the file system or the parser, **because those are the boundary under test**.

---

## One Bad Row Rejects the Whole Register

```java
@Test void oneBadRowRejectsTheWholeRegisterEvenWhenTheRequestMatchesAGoodRow() throws IOException {
    failureOf(register(HEADER, GOOD,
            "V9\tCAM2\tnot-a-date\t2026-10-22\tS1\tAPPROVED\t2026-10-18T00:00:00Z\t2026-10-20T00:00:00Z"));
}
```

* The suite also tests: a **missing file**, a **wrong header**, a **wrong column count**, an **unknown status**, a **bad date or instant**, a **blank sponsor**, an **invalid interval**, a **duplicate key**, **text that is not UTF-8**, and a **file that changes between two calls**.

---

## Expected Result vs Operational Failure

* A **missing record** is an expected result: the source **returns empty**.
* An **unreadable or untrustworthy file** is a failure: the source **throws**.
* **They must never be confused:**
  * the first means **"no sponsor approved this"**;
  * the second means **"we could not find out"**.

---

## The Network Boundary: A Controlled Local Service

* The directory used to be an in-memory example. It is now reachable **over HTTP**.
* `HttpLegacyDirectoryClient` asks `GET /borrowers/<key>` and understands **one line**: the provider's kind and status, separated by a tab.
* To test it we need a service **we control**: the JDK includes a simple HTTP server API for embedded servers, enough for a stub that answers known keys, returns an error, **never answers**, or sends **nonsense**.
* A real service on the network would make tests **slow and dependent on someone else's availability**.

---

## The Stub Is a Stand-In, Not the Provider

* `DirectoryStub` is a JDK `HttpServer` on the loopback address with an ephemeral port.
* It answers keys **B1, T1, V1, V2, VOFF, ODD and GARBAGE** with prepared bodies, **BROKEN** with status 500, **SLOW** by not answering until the test releases it, and **SLOWBODY** by sending headers and one byte, then holding the rest.
* Closing the stub **releases any waiting request**, so a test never leaves a thread hanging.
* Every test that uses it shows how **our client** behaves when a service behaves in these ways. It does **not** show that the real service does.

---

## An Explicit Policy for the Failure Case

* A client that can **wait for ever**, **retry silently** or answer **"not found" when it cannot reach the service** has made an **unreviewed policy decision**.
* The decision is written down instead, as a table of **what the client sees** and **what it does**.
* Each row has a test.

---

## The Directory Failure Policy (1 of 2)

| What the client sees | What the client does |
|---|---|
| 200 with one line, kind and status | Returns the row |
| 404 | Returns no row: the borrower is absent |
| 500 or any other status | **Fails**: the directory could not answer |
| No complete answer within the bounded wait, even if the headers arrived | **Fails with a timeout** |

---

## The Directory Failure Policy (2 of 2)

| What the client sees | What the client does |
|---|---|
| Connection refused | **Fails** |
| A body that is not exactly two fields | **Fails**: a guess is worse than a failure |
| An unknown kind code | **Fails** at the adapter; never defaulted to student or staff |

> **Policy: one attempt, a bounded wait, no retry and no fallback answer.**

---

## What the Policy Means

* A failure becomes a `DirectoryException` in the adapter and **stops the request**: no reservation is made and nobody is notified.
* **An outage must never look like a missing borrower**, because that would tell a real borrower that they do not exist.
* **No borrower is given a category the provider did not state.**
* A **retry** would repeat a slow call while a person waits; a **cached answer** would grant a category the provider is not currently stating. Both could be justified later by measured outages; **neither is assumed now.**

---

## Which Test Pins Which Row

| Policy row | Test |
|---|---|
| Ordinary request | `anOrdinaryStudentRequestWorksThroughTheRealHttpClient` |
| 404 | `aMissingRowIsAnOrdinaryRejection` |
| 500 | `aServerErrorIsAnOutageNotANotFoundAndIsNotRetried` |
| Slow provider | `aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest` |
| Stalled body | `aStalledBodyIsAFailureWithinTheOverallWait` |

---

## Which Test Pins Which Row (continued)

| Policy row | Test |
|---|---|
| Connection refused | `aRefusedConnectionIsAnOutage` |
| Malformed body | `aMalformedAnswerIsAnOutageNotAGuess` |
| Unknown kind code | `anUnknownCategoryCodeIsNeverDefaultedToStaffOrStudent` |

* The wait is **a constructor argument**; the demonstration passes its own `lending.directory.timeout.millis`.

---

## A Timeout That Covers Less Than You Think

* The JDK HTTP client lets a request carry a timeout. The documentation says that if the response is **not received within it**, the call throws `HttpTimeoutException`, and that without a timeout the call **can wait for ever**.
* It does **not** say whether a response whose **headers have arrived and whose body has not** is covered.
* A client relying on that timeout alone, tested with a stub that waits **before** sending anything, **passes**. That is the only case the test imagines.

---

## The Experiment

* A server sends the **headers and the first byte** at once, then holds the rest for **1,600 milliseconds**; the client's timeout is **300**.
* The lookup **succeeds after about 1,700 milliseconds**.
* The policy said "a bounded wait" and the client **did not keep it**: the timeout bounded the wait for the headers, **not the whole answer**.

---

## The Fix: A Deadline on the Whole Lookup

* The client sends the request **asynchronously** and waits for the result for **at most the configured time**.
* If the time runs out it **asks the client to drop the exchange** and fails the lookup.
* **Asking is all it can do:** cancelling the future attempts to cancel the exchange, which is **not guaranteed** to be prompt or to take effect at all. The caller does not depend on it, because it has already stopped waiting.
* The **header timeout stays** as well.

---

## What the New Test Shows

* New stub scenario **SLOWBODY**. The test asserts the **outcome**, a failure and not a result, with a generous outer deadline so a defect shows as a **failed test, not a hang**.
* Against a client relying on the request timeout alone it fails with `execution timed out after 5000 ms`.
* Against this chapter's client the lookup **fails after about 330 milliseconds**: `Directory did not answer within 300 ms.`
* Removing the **overall deadline** is caught by the new test. Removing the **header timeout alone cannot be detected** by any test: the fault experiment records it as an **equivalent change**.

---

## The Lesson Is Wider Than HTTP

> A test of a failure path covers the failure you imagined, so try a different one.

* A second reader, or a **fault experiment that applies a different fault**, can find what you could not.
* Before the stalled-body test existed, no fault in the experiment concerned the **body** of the response, so the experiment **could not have found** the problem.

---

## Contract Tests: Two Meanings, One Limit

* **Interface contract.** `DirectoryClientContract` is written **once** and run against **every** implementation of `LegacyDirectoryClient`:
  * a known key returns its row;
  * an unknown key returns nothing and is **not** a failure;
  * a provider that cannot answer **fails** and never returns an empty answer.
* It runs against the **in-memory example** and against the **real HTTP client talking to the stub**. Two implementations pass the same test, so a caller can swap one for the other.

---

## Provider Contract Tests and the Limit

* A **provider contract test** (Fowler) is a separate suite, run **periodically against the real external service**, checking that your test doubles still return what the real service returns.
* It checks **structure rather than exact data** and follows the provider's rate of change, so it is **not part of every pipeline run**.
* **This book has no real provider, so no such suite exists.** The stub's fidelity to the real directory is an **assumption**, written in the decision record and tested only when someone has a real service to test against.
* That is a limit to **record, not hide**.

---

# 13.3 A Few End-To-End Journeys
### The real boundary is the process

---

## Find the Real Boundary of a Command-Line Program

* A web application has a browser and a server. This program has none of them.
* Its boundary is the **process**: how it is started, which settings it reads, what it prints, how it exits, and the network and files it touches.
* A journey therefore starts `Chapter13Demo` **as a separate Java process**, with a directory service on the loopback address and a real approval file, and checks **what the user sees**.

---

## Settings and What Journeys Check

* Settings are **system properties**: the directory address, the approval file, the flag `lending.visitors` (**default false**), a fixed time for the test, and the directory timeout.
* Journeys check what **no in-process test can**:
  * that the flag is **actually read**;
  * that the pieces are **wired together**;
  * that the **classpath is complete**.

---

## Journey 1: Flag Off

```text
Visitors enabled: false
Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Visitor V1: Rejected: visitor reservations are not enabled.
Visitor V2: Rejected: visitor reservations are not enabled.
Unknown U9: Rejected: borrower not found or inactive.
Outage BROKEN: Unavailable: Borrower directory unavailable
Reservations: 1
Notices: 1
```

* The **first line prints the effective setting**: a reason to read it before every demonstration.

---

## Journey 2: Flag On

```text
Visitors enabled: true
Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Visitor V1: Confirmed: R2 for V1 on CAM2 [2026-10-20, 2026-10-22).
Visitor V2: Rejected: no valid sponsor approval.
Unknown U9: Rejected: borrower not found or inactive.
Outage BROKEN: Unavailable: Borrower directory unavailable
Reservations: 2
Notices: 2
```

* An **approved visitor is served and an unapproved one refused**.

---

## Journey 3 and Keeping Journeys Few

* **Journey 3** corrupts the register: only the **visitor requests fail**, reported as an **unavailable register** and not as a sponsor's rejection, while the **student is still served**.
* Journeys are **slow** (they start a process) and **brittle** (they check output text). Keep the number small.
* Check the lines that **carry the meaning**; **fix the clock and the ports** so a run is repeatable; let narrower tests carry the detail.
* A journey that duplicates every unit test is **cost without evidence**.

---

# 13.4 Pipeline Stages and Quality Gates
### Order the checks by cost

---

## A Pipeline Orders the Checks by Cost

* A deployment pipeline splits an automated build into **stages**. Early stages give **fast feedback**; later stages add **slower, broader checks**.
* If a stage fails, **later stages should not run**: there is no point starting a process when the code does not compile.

---

## The Five Stages (1 of 2)

| Stage | What runs | Why here |
|---|---|---|
| 1 Compile | `mvn compile` | Nothing else can run without it |
| 2 Unit tests and architecture checks | Everything not tagged `integration` or `e2e` | Fast, controlled, no outside resources |
| 3 Integration tests | Tests tagged `integration` | Real file system, real HTTP client, local stub |

---

## The Five Stages (2 of 2)

| Stage | What runs | Why here |
|---|---|---|
| 4 End-to-end journeys | Tests tagged `e2e` | Needs compiled classes and a free port |
| 5 Package | `mvn package`, tests skipped because stages 2 to 4 passed | Produces the release candidate |

---

## What a Failure Means at Each Stage

| Stage | If it fails |
|---|---|
| 1 Compile | The code does not build |
| 2 Unit and architecture | A rule or a boundary in **our own code** is wrong |
| 3 Integration | **An adapter does not meet its boundary** |
| 4 End-to-end | **The pieces are not joined correctly**, or a setting is not read |
| 5 Package | The package cannot be built |

---

## Figure 13.2: The Pipeline of This Chapter

<!--svg:ch13-pipeline-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="Figure 13.2: the five-stage pipeline. Compile, then unit tests and architecture checks, then integration tests, then end-to-end journeys, then package a release candidate. Each arrow means only if the previous stage passed. A failure in stage 2, 3 or 4 stops the run and later stages do not run." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch13-pipeline-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-pipeline-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-pipeline-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-pipeline-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-pipeline-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="9.0" y="14.0" width="148.0" height="92.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="83.0" y="65.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">1 Compile</text>
<rect x="185.0" y="14.0" width="148.0" height="92.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="259.0" y="45.9" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">2 Unit tests and</text>
<text x="259.0" y="65.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">architecture</text>
<text x="259.0" y="84.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">checks</text>
<rect x="361.0" y="14.0" width="148.0" height="92.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="435.0" y="55.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">3 Integration</text>
<text x="435.0" y="75.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">tests</text>
<rect x="537.0" y="14.0" width="148.0" height="92.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="611.0" y="55.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">4 End-to-end</text>
<text x="611.0" y="75.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">journeys</text>
<rect x="713.0" y="14.0" width="148.0" height="92.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="787.0" y="45.9" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">5 Package:</text>
<text x="787.0" y="65.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">release</text>
<text x="787.0" y="84.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">candidate</text>
<path d="M157.0,60.0 L185.0,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-pipeline-arr)"/>
<path d="M333.0,60.0 L361.0,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-pipeline-arr)"/>
<path d="M509.0,60.0 L537.0,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-pipeline-arr)"/>
<path d="M685.0,60.0 L713.0,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-pipeline-arr)"/>
<rect x="300.0" y="196.0" width="270.0" height="64.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="435.0" y="223.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Stop: later stages</text>
<text x="435.0" y="243.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">do not run</text>
<path d="M259.0,106.0 L259.0,228.0 L300.0,228.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-pipeline-arr)"/>
<text x="285.0" y="168.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">fails</text>
<path d="M435.0,106.0 L435.0,196.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-pipeline-arr)"/>
<text x="463.0" y="160.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">fails</text>
<path d="M611.0,106.0 L611.0,228.0 L570.0,228.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-pipeline-arr)"/>
<text x="637.0" y="168.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">fails</text>
<text x="435.0" y="288.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Each arrow means: only if the previous stage passed.</text>
</svg>
</div>
<!--/svg-->

---

## Selecting Stages With Tags

* Stages are selected with **JUnit tags**: `@Tag("integration")` and `@Tag("e2e")` on the test classes, and **Surefire's `groups` and `excludedGroups`** parameters, given on the command line as `-Dgroups` and `-DexcludedGroups`.
* Surefire's page documents the parameters **in the POM**, not the command-line form: **the pipeline run in the companion is the evidence** for that form.

```bash
mvn test -DexcludedGroups=integration,e2e     # stage 2
mvn test -Dgroups=integration                 # stage 3
mvn test -Dgroups=e2e                         # stage 4
mvn test -Dtest=VisitorAcceptanceTest         # one class
```

---

## The Script and the Workflow

* `scripts/pipeline.sh` runs the five stages in order and **stops at the first failure**, printing a banner at the start and end of each stage.
* The same chain is a **GitHub Actions** workflow, where `needs` makes jobs run one after another.
* **The workflow file has not been run, and no hosted run is claimed.**

---

## A Passing Run

```text
=== STAGE: 1 compile
=== PASSED: 1 compile (4 s)
=== STAGE: 2 unit tests and architecture checks
[INFO] Tests run: 203, Failures: 0, Errors: 0, Skipped: 0
=== STAGE: 3 integration tests ...
[INFO] Tests run: 26, Failures: 0, Errors: 0, Skipped: 0
=== STAGE: 4 end-to-end journeys (separate process)
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
PIPELINE PASSED
```

* **Read the counts, not the seconds.**

---

## Where the Test Counts Come From

| Stage | Invocations | Contents |
|---|---|---|
| 2 Unit and architecture | **203** | The 159 inherited invocations, the 41 visitor tests and the 3 example contract invocations |
| 3 Integration | **26** | `FileApprovalSourceIntegrationTest` (13), `DirectoryOutageIntegrationTest` (10), `HttpDirectoryClientContractTest` (3) |
| 4 End-to-end | **3** | `Chapter13JourneyE2ETest` |

* Total **232** invocations: **159 inherited and 73 new** (41 + 3 + 26 + 3).

---

## Quality Gates Decide What Blocks a Release

* A **gate** is a rule that stops the pipeline. Here: every selected test passes, the **architecture checks of Chapter 10** pass, and **a stage that selects no tests fails** instead of passing silently.
* The last rule matters: a **mistyped tag** would otherwise give a green stage that checked nothing.
* `mvn test -Dgroups=nosuchtag` ends with `No tests were executed!` and `BUILD FAILURE`, because the POM sets `failIfNoTests` to true.
* A pipeline is evidence about **the checks it contains**. It does not establish that the program is secure, that every rule is right, or that real users will be served.

---

## Read a Failure: The Deliberate Fault

* The register parser's **header check was removed**, so a file with a wrong header is accepted.
* The comparison `lines.isEmpty() || !HEADER.equals(lines.get(0))` became `lines.isEmpty()`.

```text
=== PASSED: 2 unit tests and architecture checks (11 s)
=== STAGE: 3 integration tests ...
[ERROR] ...FileApprovalSourceIntegrationTest.aWrongOrMissingHeaderIsAFailure <<< FAILURE!
Expected ...ApprovalSourceException to be thrown, but nothing was thrown.
[ERROR] Tests run: 26, Failures: 1, Errors: 0, Skipped: 0
```

* Exit status 1 after stage 3. **Stages 4 and 5 never started.**

---

## Three Habits for Reading a Failing Pipeline

1. **Find the first failing stage** and ignore everything after it.
2. **Read the name of the first failing test before the stack trace**: the name says what the test promised.
3. **Ask whether the earlier stages should have caught it.** Here they could not: no unit test reads the real file, and that is correct for their purpose. **That is the reason stage 3 exists.**

* The other **25 integration tests passed**, so the fault is local to the header.

---

# 13.5 Delivery Is Not Deployment
### A release candidate is not a release

---

## Delivery vs Deployment

* **Continuous delivery:** software is built so that it **can be released to production at any time**.
* **Continuous deployment** goes further: **every change that passes the pipeline is put into production automatically**.
* You can do delivery without deployment, and you **must** do delivery to do deployment.
* Our pipeline ends with a **release candidate**, a jar that has passed every stage. **That is delivery. Nothing here deploys it to production.**

---

## The Simulation

* The course needs an understanding of delivery, not a public deployment, so the companion supplies a **simulation**: `scripts/simulate-release.sh`.
  1. Builds the jar.
  2. Copies it into a local `build/staging` folder as the **current** release.
  3. Runs the end-to-end journeys against that **copied jar** as a smoke test.
* A second delivery moves the old release to **previous**; `rollback` makes it current again and smoke-tests it.

```bash
RELEASE_LABEL=v1 bash scripts/simulate-release.sh
RELEASE_LABEL=v2 bash scripts/simulate-release.sh
bash scripts/simulate-release.sh rollback
```

---

## Two Limits of the Simulation

* The script packages with the tests skipped and then runs only the end-to-end journeys, so it **assumes the pipeline already passed** for the same candidate and **does not enforce the other gates**.
* Rollback assumes the **same version-derived jar name** in both releases, so the two releases are **two labels for one build**, not a tested rollback between different versions.
* This is a **simulation**: no server, no network deployment and no production.
* A real deployment would add **environment-specific settings, secrets, a health check and monitoring**, which are outside the module.

---

# 13.6 Feature Flags, Configuration and Rollback
### One flag, two paths

---

## One Flag, Two Paths

* A **feature flag** lets you ship code without turning the behaviour on.
* CR-12 has exactly one: **`visitingResearchersEnabled`, default off**.
* **Off:** a visitor request is rejected **explicitly** and the **approval register is not read**.
* **On:** the new path.
* **Student and staff requests behave the same under both settings** and never depend on the flag.
* It is a **release toggle**: it hides unfinished or unproven behaviour, and release toggles should be **short-lived**.

---

## Test Both Paths, But Few

* Both paths are tested: in the **acceptance examples**, the **end-to-end journeys** and the **service tests**.
* Testing both settings is cheap with **one** flag and becomes expensive with **many**, because each toggle state may go live.
* Test **the configuration you expect in production** and **the fallback with the new behaviour off**.
* An "off" that means legacy behaviour and an "on" that means the new behaviour **keeps that simple**.

---

## A Removal Plan Is Part of the Flag

* A flag nobody removes becomes **a permanent branch**.
* The decision record sets the conditions:
  1. the released variant is **accepted**;
  2. **both settings have passed** in the pipeline for the release candidate;
  3. a decision to keep visitors enabled is **recorded**.
* Then **the flag, the disabled path and its tests are deleted together, in one commit.**
* Review the flag at the handover in **Chapter 14**. Flags are **inventory**, and inventory has a carrying cost.

---

## Configuration Is Not a Flag

* The **directory address**, the **timeout** and the **register path** are *configuration*: they differ between machines and are not decisions about releasing behaviour.
* **A flag chooses between behaviours; configuration chooses between places and values.** Mixing them gives a program nobody can reason about.
* Caution: the demonstration reads the flag with `Boolean.parseBoolean`, which treats any text other than "true" as **false**, so a mistyped value silently means **off**.
* That is the safe direction, and a reason to **print the effective setting**, which the program does on its first line.

---

## Rollback, and What It Does Not Undo

* To stop new visitor reservations, **turn the flag off**.
* To go back to an earlier build, **redeliver the previous release**.
* Neither **removes a reservation that already exists**, **undoes a notice already sent**, or **restores a decision a person already made** on the strength of it.
* **AC16** pins one consequence: a visitor reservation made before the flag was switched off **can still be checked out and returned**.
* **A rollback plan is only a plan when it says what stays behind.**

---

# 13.7 Did the Change Work?
### Verifying the changed behaviour

---

## Figure 13.3: The Order of the Visitor Decision

<!--svg:ch13-decision-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 335" role="img" aria-label="Figure 13.3: the order of the visitor decision. Flag off: rejected, register not read. Item not CAM1 or CAM2: rejected. Fewer than one day: the gate steps aside and the coordinator rejects it, register not read. Otherwise read the clock once and the register once: unreadable or malformed is a failure with nothing reserved or sent; no valid matching approval is a rejection; valid at the request instant goes to the coordinator&#x27;s count and duration rules, which either reject or pass to the availability, reservation and notice steps." style="display:block;width:100%;height:calc(var(--u) * 33.50);margin:0 auto">
<defs><marker id="ch13-decision-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-decision-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-decision-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-decision-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch13-decision-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="0.0" y="104.0" width="100.0" height="66.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="50.0" y="124.7" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Visitor</text>
<text x="50.0" y="141.6" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">request</text>
<text x="50.0" y="158.5" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">(VISITOR)</text>
<polygon points="187.5,95.0 240.0,137.0 187.5,179.0 135.0,137.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="187.5" y="141.8" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Flag on?</text>
<polygon points="331.0,95.0 390.0,137.0 331.0,179.0 272.0,137.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="331.0" y="133.3" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Item CAM1</text>
<text x="331.0" y="149.5" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">or CAM2?</text>
<polygon points="481.0,95.0 540.0,137.0 481.0,179.0 422.0,137.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="481.0" y="133.3" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Fewer than</text>
<text x="481.0" y="149.5" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">one day?</text>
<rect x="575.0" y="104.0" width="125.0" height="66.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="637.5" y="125.2" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Read clock once</text>
<text x="637.5" y="141.4" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">and register</text>
<text x="637.5" y="157.7" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">once</text>
<rect x="732.0" y="104.0" width="136.0" height="66.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="800.0" y="125.2" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">FAILURE:</text>
<text x="800.0" y="141.4" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">nothing reserved</text>
<text x="800.0" y="157.7" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">or sent</text>
<rect x="105.0" y="8.0" width="135.0" height="52.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="172.5" y="30.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Rejected:</text>
<text x="172.5" y="47.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">not enabled</text>
<rect x="255.0" y="8.0" width="135.0" height="52.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="322.5" y="30.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Rejected:</text>
<text x="322.5" y="47.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">item not allowed</text>
<rect x="542.5" y="8.0" width="190.0" height="52.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="637.5" y="30.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Rejected: no valid</text>
<text x="637.5" y="47.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">sponsor approval</text>
<rect x="432.0" y="232.0" width="200.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="532.0" y="258.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Coordinator:</text>
<text x="532.0" y="275.5" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">count and duration rules</text>
<rect x="150.0" y="232.0" width="200.0" height="60.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="250.0" y="258.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Rejected: borrower</text>
<text x="250.0" y="275.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">limit or duration</text>
<rect x="712.0" y="232.0" width="156.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="790.0" y="258.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Availability,</text>
<text x="790.0" y="275.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">reservation, notice</text>
<path d="M100.0,137.0 L135.0,137.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<path d="M240.0,137.0 L272.0,137.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<text x="256.0" y="138.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">yes</text>
<path d="M390.0,137.0 L422.0,137.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<text x="406.0" y="138.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">yes</text>
<path d="M540.0,137.0 L575.0,137.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<text x="558.0" y="138.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">no</text>
<path d="M700.0,137.0 L732.0,137.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<path d="M187.5,95.0 L172.5,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<text x="203.5" y="80.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">no</text>
<path d="M331.0,95.0 L322.5,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<text x="347.0" y="80.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">no</text>
<path d="M637.5,104.0 L637.5,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<path d="M481.0,179.0 L481.0,232.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<text x="500.0" y="205.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">yes</text>
<path d="M657.5,170.0 L657.5,200.0 L600.0,200.0 L600.0,232.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<path d="M432.0,262.0 L350.0,262.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<text x="391.0" y="252.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">violated</text>
<path d="M632.0,262.0 L712.0,262.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch13-decision-arr)"/>
<text x="672.0" y="252.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">met</text>
<text x="645.5" y="90.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">no match</text>
<text x="667.5" y="188.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">valid at the</text>
<text x="667.5" y="203.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">request instant</text>
<text x="800.0" y="190.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">unreadable or</text>
<text x="800.0" y="205.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">malformed</text>
</svg>
</div>
<!--/svg-->

---

## Reading the Decision Order

* Rectangles are **results**; the one marked FAILURE is an **exception that nothing on the request path catches**.
* **Every rejection is an ordinary return value.**
* The **gate runs first**; the coordinator's **count and duration rules run last**.
* Inside the gate: **flag, item, duration, one clock read, one register read**, then an exact-request re-check and the validity window.

---

## The Order Is Observable

* A **four-day** visitor request with an **unreadable register** does **not** get the duration rejection: it **fails with the register's error**, because the gate reads the register before the coordinator applies the duration rule.
* A **zero-day** request is the opposite: the gate leaves it alone, the register is **not read**, and the coordinator rejects it.
* `precedence_theRegisterIsReadBeforeTheCountAndDurationRulesApply` pins both ends. It is **not one of the eighteen acceptance examples**.
* A different precedence (duration before register) is a change to **the contract, the implementation and the tests together**, not to the picture.

---

## Why the Gate Sits in Front of the Coordinator

* `BorrowingPolicy.mayRequest(count, days)` answers **a count and duration question and nothing else**. Approval needs the **borrower, item, period and time**.
* Passing those through a flag or a static would give the policy **hidden state** and make it untestable for identity and time.
* So the policy stays small (`VisitorReservationRules`), and the request-specific decision lives in `VisitorGate` in the **application layer**, called by `DirectoryReservationService` **before** the coordinator.
* **Student and staff requests never reach the gate.**

---

## The Exact-Request Re-Check

* The gate re-checks that the record returned **matches the exact request**, though the source was already asked for it.
* It looks redundant. It is there because the source is a **boundary**: a source that returns the wrong record (a bug, or a register changed underneath) **must not approve**.
* `aSourceThatReturnsADifferentRequestDoesNotApprove` and the fault experiment test it.

---

## One Acceptance Example in Code

```java
@Test void ac9_theRequestInstantAtValidUntilOrBeforeValidFromIsRejected() {
    var atExpiry = new World(true, UNTIL).approve("V1", "CAM1", START, 2);
    assertEquals(VisitorGate.NOT_APPROVED, atExpiry.service.reserve("V1", "CAM1", START, 2));
    var early = new World(true, FROM.minusSeconds(1)).approve("V1", "CAM1", START, 2);
    assertEquals(VisitorGate.NOT_APPROVED, early.service.reserve("V1", "CAM1", START, 2));
    assertNothingChanged(atExpiry);
    assertNothingChanged(early);
}
```

* **Every example builds its own setup**, so one failure cannot hide another.

---

## Acceptance Examples by Group

| Group | Examples | What they establish |
|---|---|---|
| Success path | AC1 | One matching, valid approval gives one reservation in the existing confirmation format and one notice |
| Duration and item | AC2 to AC5 | Upper boundary of three days, no zero or negative days, the two-item allowlist |
| Approval matching | AC6 to AC9 | Missing, denied, mismatched and expired approvals; equality at both ends of the window |
| Failure and flag | AC10, AC12 | Unreadable register is a failure, not a rejection; a disabled flag never reads the register |
| Existing behaviour | AC11, AC13 to AC18 | Count rule, students and staff under both settings, availability, notification failure, lifecycle, directory semantics, the report |

---

## Evidence for AC1 to AC6

| Example | Test in `VisitorAcceptanceTest` |
|---|---|
| AC1 | `ac1_aVisitorWithAMatchingApprovalReservesCam1ForTwoDays` |
| AC2 | `ac2_cam2ForThreeDaysNeedsItsOwnRecordAndIsAllowed` |
| AC3 | `ac3_fourDaysIsRejectedEvenWithAMatchingRecord` |
| AC4 | `ac4_zeroOrNegativeDaysIsRejectedWithoutReadingTheRegister` |
| AC5 | `ac5_anItemOutsideTheAllowlistIsRejectedEvenWithAMatchingRecord` |
| AC6 | `ac6_aMissingOrDeniedApprovalIsAnExpectedRejection` |

---

## Evidence for AC7 to AC12

| Example | Test in `VisitorAcceptanceTest` |
|---|---|
| AC7 | `ac7_anApprovalForAnotherBorrowerItemOrPeriodDoesNotAuthorise` |
| AC8 | `ac8_theRequestInstantEqualToValidFromIsValid` |
| AC9 | `ac9_theRequestInstantAtValidUntilOrBeforeValidFromIsRejected` |
| AC10 | `ac10_anUnreadableApprovalRegisterIsAnOperationalFailureNotARejection` |
| AC11 | `ac11_threeRetainedReservationsBlockAFourthEvenAfterLoansAreReturned` |
| AC12 | `ac12_aDisabledFlagRejectsExplicitlyWithoutReadingTheRegister` |

---

## Evidence for AC13 to AC18

| Example | Test in `VisitorAcceptanceTest` |
|---|---|
| AC13 | `ac13_studentAndStaffBehaviourIsUnchangedUnderEitherSettingAndNeverReadsTheRegister` |
| AC14 | `ac14_anOverlapWithAnExistingReservationIsRejectedByTheExistingRule` |
| AC15 | `ac15_anExpectedNotificationFailureLeavesTheVisitorReservationInPlace` |
| AC16 | `ac16_aVisitorReservationStaysUsableAfterTheApprovalExpiresAndTheFlagIsOff` |
| AC17 | `ac17_anInactiveOrUnknownBorrowerIsRejectedAsBefore` |
| AC18 | `ac18_aVisitorLoanInTheOverdueReportKeepsTheExistingKindRuleSd11_1` |

---

## What the Regression Suite Shows

* Adding `VISITOR` to the category enum has a deliberate consequence: the coordinator **requires a policy for every category**, so every test that builds a coordinator with a complete policy map needed **one more entry**.
* That was **four constructions in three test files**. **No assertion changed.** The inherited Chapter 11 tests passed unchanged afterwards.
* A regression suite that passes shows that **the old behaviours it covers are intact**. It says **nothing** about behaviour the old suite never covered, and **nothing** about whether the new rule is right.

---

## Unresolved Items Keep Their Names

* **AC18:** a visitor who returns a loan late appears in the overdue report, which knows only student and staff kinds, so it applies its "any other kind" rule: **one unit a day, no grace, no cap.**
* That is the suspected defect **SD-11-1** from Chapter 11. It now has a **real consequence**. The change does **not** fix it: only the records office can say what a visitor's late fine should be.
* The count rule **SD-12** also stays as it is.
* **Naming these items, and showing in a test what each does today, is more useful than silently resolving them.**

---

## Do the Tests Detect Faults?

* Thirty faults were run **one at a time** in a copy of the project. **Twenty-nine were caught. One survived, and it is an equivalent change** (removing the header timeout while the overall deadline stays).
* Examples caught: duration check removed; flag ignored; allowlist also admits MIC1; expiry instant valid; start instant invalid; DENIED also approves; unknown status becomes DENIED; duplicate keys allowed; register cached; 404 treated as outage.
* Some faults were first noticed by an **end-to-end journey**: that is a reason to keep a few journeys.
* **These counts come from one fault set on one small change, chosen by the author.** They do not show the suite catches every fault.

---

# 13.8 Preparing the Milestone 4 Evidence
### Preparation, not a rubric

---

## What You Should Be Able to Show (1 of 2)

By your demonstration you should show, on your team's project:

1. Your released requirement change, implemented from the **smallest vertical slice outwards**, behind **one flag**, with acceptance examples.
2. **Regression evidence** from your existing suite, with any necessary changes to test setups **disclosed**.
3. **Integration evidence** for at least one genuine boundary, including its failure cases.
4. **An observed pipeline run, and a failing run that you have read.**

---

## What You Should Be Able to Show (2 of 2)

5. A **delivery step**, simulated or real, with a smoke test and a rollback.
6. **Flag evidence:** both settings tested and a removal plan.
7. A **demonstration and a retrospective** with a next action.
8. **A statement of what your evidence does not show.**

* The approved Milestone 4 instructions decide what is submitted; **this list is preparation, not a rubric.**

---

## The Evidence Table

| Item | What to produce | What it should establish |
|---|---|---|
| 1 | Change record and acceptance examples | Requirement and each example traceable to a test |
| 2 | Regression result | Old behaviour intact; changed test setups listed |
| 3 | Boundary tests | Real file, service or store used; both outcomes checked |
| 4 | Pipeline output | Which stage ran which checks; one real failure read correctly |
| 5 | Delivery record | Candidate smoke-tested; a rollback tried |
| 6 | Flag evidence | Both paths tested; a named condition for removal |
| 7 | Retrospective | What worked, what did not, one next action |
| 8 | Limits statement | E.g. hosted CI not run, real provider not tested, concurrency not addressed |

---

## Do Not Claim What Did Not Happen

* **Do not claim** a hosted pipeline run, a public deployment or a peer review that did not happen.
* **A local pipeline run is evidence of a local run.**
* What this chapter's own evidence does **not** show: behaviour against a real directory or approval workflow, **concurrency** (two writers of the register, two simultaneous requests), **authentication**, behaviour under load, a hosted run, and that **SD-11-1 and SD-12 are acceptable**.

---

# 13.9 An Integration Test That Mocks Its Boundary
### Judging an AI proposal

---

## The Activity

| | For this activity |
|---|---|
| Your goal | Decide what a proposed integration test actually verifies, and repair it so it verifies what its name claims |
| You start with | The approval adapter, the visitor gate and the integration tests of 13.2 |
| What is in bounds | Judge and repair the proposed test; **do not weaken the adapter or its other tests** |
| How to check | Introduce one fault into the parser in a scratch copy and see which tests notice |
| How to decide | A verdict, a repaired test, and an explanation of what each verifies |

---

## The Ready-Made Example

**Author-written fictional AI output.**

> I added an integration test for the approval register. It builds a visitor approval, makes the register return it, and checks that the gate accepts the visitor and that the register was consulted.

```java
@Tag("integration")
class ProposedRegisterIntegrationTest {
    @Test void anApprovedVisitorIsAcceptedFromTheRegister() {
        ApprovalSource register = mock(ApprovalSource.class);
        ApprovalRecord record = new ApprovalRecord("V1", "CAM1", start, end, "S1", APPROVED, from, until);
        when(register.find("V1", "CAM1", start, end)).thenReturn(Optional.of(record));
        VisitorGate gate = new VisitorGate(register, clock, true);
        assertEquals(Optional.empty(), gate.rejection("V1", "CAM1", start, 2));
        verify(register).find("V1", "CAM1", start, end);
    }
}
```

---

## Questions to Answer

* Run it. It passes. Now introduce a fault into `FileApprovalSource` in a scratch copy: read the two instant columns the wrong way round, or skip a broken row instead of rejecting the file. Run it again.
* **Which part of the system does this test touch?**
* **Is there a file anywhere in it?**
* **What would it still say after you delete the parser?**
* **What does `@Tag("integration")` promise that the body does not deliver?**

---

## The Answers

| Question | Answer |
|---|---|
| Which part does it touch? | `VisitorGate` and `ApprovalRecord`. Nothing else |
| Is there a file in it? | No. `mock(ApprovalSource.class)` replaces the register; the parser and file system are not in the test |
| After the parser is deleted? | The same: it **passes** |
| What does the tag promise? | A test of a real boundary. It puts the test in stage 3, adding time and **a false sense of cover** |
| What does `verify(...)` establish? | That the gate asked the mock for the exact request: a fact about **the gate**, not the register |

---

## Run Both Tests Against Two Faults

| Run | Proposed test | Repaired test |
|---|---|---|
| No fault | Passes | Passes |
| Fault A: `validFrom` and `validUntil` columns read the wrong way round | **Passes** | **Fails**: `ApprovalSourceException: Row 2 is not a valid approval record.` |
| Fault B: a broken row skipped instead of rejecting the file | **Passes** | **Fails**: expected `ApprovalSourceException`, nothing was thrown |

---

## The Repair, and What the Original Is Still Good For

* **Repair:** write a real register into a temporary directory, read it with the real `FileApprovalSource`, pass that source to the real gate. **Add the failure case:** a broken row appended to the file makes the gate **throw the register's exception**, not reject politely.
* The repaired test is **deliberately small**. A **header fault would pass it**: `FileApprovalSourceIntegrationTest` covers the header.
* **The original is a fair unit test of the gate's decision logic** with a controlled source. It belongs in the unit stage under an honest name.
* **Accept it as a unit test; reject it as an integration test.** Do not use a generated test to approve generated code.

---

# 13.10 Delivery Habits That Mislead
### Eleven to avoid

---

## Mistakes 1 to 4

| Mistake | Consequence | Better action |
|---|---|---|
| Mock the boundary and call the test an integration test | Passes whatever the real adapter does | Use the real file or a controlled local service, and fault-test it |
| Test only the successful response | An outage or bad data is found in the demonstration | Test missing, slow, malformed and refused answers |
| Report an unreachable service as "not found" | A real borrower is told they do not exist | Fail the request; say the service could not answer |
| Add a timeout without deciding what happens next | Waits less long and still behaves unpredictably | Write the policy: one attempt, no retry, no fallback |

---

## Mistakes 5 to 8

| Mistake | Consequence | Better action |
|---|---|---|
| Default an unknown category to the nearest known one | A visitor becomes a student without anyone deciding it | Treat an unknown code as a failure |
| Let an end-to-end journey check everything | Slow, brittle, duplicates other tests | Check the lines that carry the journey's meaning |
| Use real clocks, ports or paths in tests | Runs differ by day, machine or luck | Inject the clock, take a free port, use a temporary directory |
| Assume a timeout covers the whole call | A trickling response holds the caller as long as the server likes | Bound the whole operation; test the stall you did not think of |

---

## Mistakes 9 to 11

| Mistake | Consequence | Better action |
|---|---|---|
| A stage that can select no tests | A mistyped tag gives a green stage that checked nothing | Fail a stage that runs nothing |
| Treat a green pipeline as proof | Security and unseen behaviour are not examined | State what the stages check and what they do not |
| Switch a flag on by default, or never remove it | The old path rots and the code keeps both | Default off, test both paths, name a removal condition |

---

## Diagnostic Alternatives: Flawed Code

```java
// WRONG: a failure of the provider is reported as an absent borrower.
try { return fetch(key); }
catch (IOException | InterruptedException failure) { return null; }

// WRONG: an unknown kind is given the nearest known category.
default -> BorrowerCategory.STUDENT;

// WRONG: no timeout; the request waits for ever.
HttpRequest request = HttpRequest.newBuilder(uri).GET().build();
```

* Caught by `aRefusedConnectionIsAnOutage`, `anUnknownCategoryCodeIsNeverDefaultedToStaffOrStudent` and `aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest`.

---

## Diagnostic Alternatives: Flag, Mock and Stage

```java
// WRONG: a flag with no owner, on by default, global and mutable.
public static boolean visitingResearchersEnabled = true;
```

```bash
mvn test -Dgroups=integraton   # misspelt: no test has this tag
```

* The global flag **cannot be tested for both settings in one process** without cleaning up and has **no removal plan**. This chapter's flag is a **constructor argument, default off**.
* Without `failIfNoTests`, a stage that runs zero tests **passes**. With it: `No tests were executed!`.

---

# 13.11 Try It Yourself
### Run the pipeline and deliver a flagged change

---

## What You Start With, and the Demonstration

* **You start with:** the Chapter 11 version with the Chapter 13 files from the companion, Chapter 12's CR-12 specification, and your team's repository.
* Steps **B1 to B7** use the book's project; steps **T1 to T5** use your team's project.
* **Instructor demonstration:** run `scripts/pipeline.sh` and read each stage. **Break the register parser on purpose** and run it again to show which stage notices. Run the flag-off and flag-on journeys.
* **Guided practice:** classify four risks of your choice as unit, integration or end-to-end, and say what each cannot show. Predict the outcome for a response the **directory policy table does not list**.

---

## The Book's Project: B1 and B2

* **B1. Run the pipeline.** Run `scripts/pipeline.sh` or the five Maven commands in it. Record **each stage, the number of tests it ran and its time**. Say what a failure in each stage would mean.
* **B2. Trace three acceptance examples.** Choose AC8 or AC9 (window boundary), **AC10** (operational failure) and **AC12** (the flag). For each, name **the test, the production class that decides the outcome and the observable result**, and say which stage runs it.

---

## B2: A Good Answer

| Example | Deciding production code | Observable result | Stage |
|---|---|---|---|
| AC9 (expiry boundary) | `ApprovalRecord.validAt`, called from `VisitorGate.rejection` | `Rejected: no valid sponsor approval.` at `validUntil`; no reservation | 2 |
| AC10 (operational failure) | `FileApprovalSource.readAll` throws; nothing catches it on the request path | `ApprovalSourceException`; no reservation or notice | 2 and 4 |
| AC12 (the flag) | `VisitorGate.rejection`, the first check | `Rejected: visitor reservations are not enabled.`; register not read | 2 and 4 |

---

## The Book's Project: B3 and B4

* **B3. Make a test bite.** In a scratch copy, introduce **one fault** into `FileApprovalSource` or `HttpLegacyDirectoryClient`. **Predict which stage fails first**, run the pipeline, compare. Restore the original.
  * Example: an unknown status becomes `DENIED`. Prediction: stage 2 passes (no unit test reads the real file); stage 3 fails at `anUnknownStatusIsAFailureNotADenial`.
* **B4. Complete the evidence table.** For the whole change, in the form of 13.1: the risk, the check that covers it, the test's name, and what it cannot show. **Mark at least one risk nothing here covers**: the real directory's behaviour, two concurrent writers of the register, a sponsor revoked after a reservation, the effect of an unusual time zone on the request instant.

---

## Your Team's Project: T1 to T3

* **T1. Implement your released change.** Start with the **thinnest vertical slice** that behaves correctly, behind **one flag that defaults to off**, and record the acceptance examples. Keep **expected rejections apart from operational failures**.
* **T2. Test one genuine boundary.** A file, a service or a store in your project, **without replacing it**: a real temporary file, a local stub service or a throw-away database. Cover **at least one failure case**.
* **T3. Protect the old behaviour and both flag settings.** Run your existing suite, **disclose any test setup you had to change**, and add tests for the flag on and off.

---

## Your Team's Project: T4 and T5

* **T4. Build and read a pipeline.** At least **three stages** (for example compile and unit, integration, and a smoke or end-to-end stage). Capture **one observed run and one failing run**, and read the failing one: first failing stage, first failing test, and why earlier stages could not have caught it.
* **T5. Prepare the Milestone 4 evidence.** Record a **flag removal plan and a rollback step**, run your demonstration, write the retrospective with **one next action**, and complete the eight items of 13.8, **marking each complete or a gap**.

---

## If You Want More: B5 to B7

* **B5. Deliver and roll back.** Run `simulate-release.sh` twice with different `RELEASE_LABEL` values, then `rollback`. Record which release is **current** after each step: after the second delivery v2 is current and v1 previous; after rollback v1 is current and nothing is previous. **The rollback changes a folder, not any data.**
* **B6. AI activity.** Complete 13.9.
* **B7. Break a boundary on purpose.** Make the directory timeout **twenty seconds** in a scratch copy and run the slow-provider test. It **fails after 20.03 seconds** with `the call must give up after its timeout, but took 20015 ms`; the class takes 20.58 seconds instead of 1.01. A test of a timeout should use a **short, injected timeout**; a pipeline that waits for the real timeout of every failure case is **itself a problem**.

---

## What You Should End Up With, and When You Are Done

* **What you should end up with:** B1 to B4; for your team's project, the implemented change with its acceptance examples, the boundary tests, the pipeline output (**one passing and one failing**), the delivery and rollback record, the flag evidence, and the Milestone 4 checklist. A pull request is a good vehicle where your course workflow permits it.
* **Acceptance:** change behind a flag that **defaults to off**; rejections and failures **distinguishable**; one boundary tested **without being replaced**, with its failure cases; old behaviour protected and changed test setups **disclosed**; a stage that selects no tests **fails**; delivery **labelled a simulation** unless real; **limits statement** says what was not run.

---

# 13.12 Questions to Think with, and a Transfer Challenge
### Concept, diagnosis, transfer

---

## Concept Questions

1. Why can a unit test not show that a file adapter parses the real register? What does it show instead?
2. What does the directory contract test say, and what can it never show about the real provider?
3. Why is "not found" the wrong answer when the directory times out? Name two other defaults the policy refuses.
4. What is the difference between continuous delivery and continuous deployment, and which does `simulate-release.sh` imitate?

---

## Diagnosis Questions

5. A teammate replaces the file reader with a mock "so that the test is repeatable" and keeps the name `FileApprovalSourceIntegrationTest`. Which risk is no longer covered? How would you keep repeatability without replacing the reader?
6. The pipeline is green and the demonstration fails because the flag was off. Name two checks, one in the pipeline and one in the process of delivering, that would have noticed.
7. A client sets a request timeout of two seconds and the officer's screen still freezes for forty. The server sends its headers at once, then the body a few bytes at a time. What does the timeout cover, what does it not, and what would you change and test?

---

## Guidance: Questions 1 to 4

1. A unit test **controls everything the unit collaborates with**, so it cannot show the real parser reads the real file: the file system, encoding, line endings and parser are exactly what it replaced. It shows that **the logic that consumes a parsed record** is right.
2. A known key returns its row; an unknown key returns nothing and is not a failure; a provider that cannot answer **fails**. Two implementations pass. It **can never show how the real provider behaves**: the stub's answers are the author's assumption.
3. After a timeout we do not know the borrower is absent. Two other refused defaults: **an unknown kind code treated as student or staff**, and **a cached or earlier answer when the provider is down**.
4. Delivery keeps software **releasable at any time**; deployment **releases every passing change automatically**. The script imitates **delivery** only.

---

## Guidance: Questions 5 to 7

5. The **parse of the real register** is no longer covered: header, columns, dates, encoding, duplicate keys. Keep repeatability with a **temporary directory**: write the file inside the test, read it with the real adapter, delete it afterwards. **Repeatable and real are not opposites.**
6. **Pipeline:** an end-to-end journey with the flag **on**, starting the program with the demonstration's setting. **Delivery:** a smoke test of the packaged jar with the target's settings and a **printed first line stating the effective setting**. Both check **configuration**, not logic.
7. The timeout covers the wait for the **response to be received**; it does **not** cover a body that trickles in. **Bound the whole operation** with an overall deadline, and add a stub scenario that sends headers and a byte, then stalls.

---

## Transfer Challenge: ML Model Serving

An ML model-serving team: **only approved model versions may be served to external callers.** The approval list is a file produced by another team; the model registry is queried over the network.

* Which risks are **unit, integration or end-to-end** checks?
* How is a **registry timeout** handled, and what must it **not default to**?
* What does the **one flag** do, and what does the **rollback not undo**?
* Name one thing your evidence **would not show about the model's accuracy**.
* Synthetic model identifiers only: no model needs to be trained.

---

## Transfer Guidance (1 of 2)

| Risk | Check |
|---|---|
| Approval rule: only approved versions served externally | **Unit** tests with a controlled approval source: approved, not approved, expired, a different version, the validity-window boundary |
| Approval list file has a stray column or duplicate | **Integration** test with a real temporary file and each failure case; a whole-file rule or skip rule, chosen and written down |
| Registry times out or returns nonsense | **Integration** test against a local stub with a bounded wait: the request fails and the version is **not** served; an unknown version is **never** defaulted to the latest approved one |

---

## Transfer Guidance (2 of 2)

| Risk | Check |
|---|---|
| Flag on in the demonstration and off in the build | One **end-to-end** journey that starts the serving process with each setting |
| Old behaviour changed | The existing suite |

* **The flag** enables the rule for external callers. **Rollback** turns it off, but does **not** recall a response already served or revoke an approval a person already acted on.
* **The evidence would not show** the model's **accuracy, fairness or drift**: nothing here evaluates the model, only the gate in front of it.

---

# What to Take Away, and What Comes Next
### What to carry forward

---

## Summary

* A change is only as safe as the checks **at the places where our code meets something else**.
* Test **the real file and a controlled service** without replacing them; **write down what happens when they fail**.
* **Order the checks in a pipeline from cheap to broad**, release behind a flag that **defaults to off**, and say what a **rollback cannot undo**.
* **A green pipeline is evidence about the checks it contains and nothing more.**

---

## Where the Project Stands

* The visiting-researcher change is **implemented and verified**, with two unresolved items still **named**: **SD-11-1**, which a visitor's late fine now exposes, and **SD-12**, the count rule.
* **Chapter 14** reviews how the design accommodated the change, prepares the handover, and decides the flag's removal.

---

## Sources and Further Reading

1. **Fowler:** *Integration Test*; *Contract Test*; *Deployment Pipeline*; *Continuous Delivery*.
2. **Hodgson:** *Feature Toggles (aka Feature Flags)*.
3. **GitHub:** *Workflow syntax for GitHub Actions*. **Maven:** *Using JUnit 5 Platform in Surefire*.
4. **Oracle:** `HttpRequest.Builder`, `HttpClient`, `com.sun.net.httpserver` (Java SE 17). **JUnit:** *User Guide 5.13.4*.
5. **Martin:** *Agile Software Development* (2002). **Humble and Farley:** *Continuous Delivery* (2010).

* Full references and links are in the chapter text.
