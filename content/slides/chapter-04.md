---
title: "Chapter 4: From Requirements to an Iteration"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 40
type: slides
layout: page
---

# Chapter 4: From Requirements to an Iteration
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **4.1 What are we building? Vision, scope and constraints**
  * A bounded outcome, a visible boundary, small decision records.
* **4.2 Sketching the screens and walking through examples**
  * A wireframe is a question made visible.
* **4.3 Prioritisation and vertical slicing: what first, how thin?**
  * Slice by a user outcome, not by technical layer.
* **4.4 What can we really finish? Release outlook and iteration planning**
  * Capacity in person-hours, and why the total is not enough.

---

## Chapter Roadmap (2 of 3)

* **4.5 How the team works together: agreements and review**
  * How work moves, who reviews, what evidence a reviewer needs.
* **4.6 A starter build and CI you can run**
  * One meaningful command, Arrange-Act-Assert, a hosted workflow, a failure you can observe.
* **4.7 Getting ready for Milestone 1**
  * An evidence trail, rehearsed from another person's starting point.
* **4.8 Challenging an overambitious plan with AI**

---

## Chapter Roadmap (3 of 3)

* **4.9 Planning mistakes that look reasonable**
* **4.10 Try it yourself: prepare for the kickoff**
  * Eight steps on your team's project.
* **4.11 Questions to think with** and **4.12 A different setting: the transfer challenge**
  * A clinic appointment-slot system.
* **What to take away, and what comes next**
  * Chapter 5 examines responsibilities, extension and substitutability.

---

## Learning Outcomes (1 of 2)

By the end of this chapter, you should be able to:

1. **Define a project vision** with explicit scope, assumptions and constraints.
2. **Slice a feature** into a small increment that supports an observable user outcome.
3. **Form an iteration plan** that includes implementation, review, verification and realistic capacity.

---

## Learning Outcomes (2 of 2)

4. **Apply a shared repository workflow** with clear review responsibilities.
5. **Run a starter build and checks**, and demonstrate that the checking process detects a deliberate failure.
6. **Assemble traceable evidence** for the kickoff milestone.

---

## Module Connection

* The chapter prepares you for **Milestone 1** (the Week 3 kickoff). It supports LO5 and LO6.
* The descriptor's term **Sprint 0** is the local kickoff label. It is **not a formal Scrum event**.
* It supplies preparation guidance, **not new assessment weights, submission rules or approved module wording**.
* Readings: the planning and testing chapters of Martin, and the sprint-planning chapters of Rubin.

---

## Prerequisites and Route

* **Prerequisites:** the Chapter 2 Java version; Chapter 3's ordered backlog and Definition of Done; basic Git operations.
* **Tools:** a Java 17 JDK, Git and Bash. On Windows, use **Git Bash or WSL**.
* **Core reading:** 4.1 to 4.7, running the supplied checks while reading 4.6.
* **What you must do:** steps 1 to 8 of Section 4.10 on your team's project. Start steps 6 and 7 (hosted CI) early.
* **If you want more:** the AI activity, review questions, transfer challenge and extension.

---

## Opening Scenario: A Kickoff With Ideas but No Boundary

* The team arrives at kickoff with **six backlog items** and a working Java reservation coordinator.
* One member wants a **mobile interface**. Another proposes a **database**. A third wants to **complete every story before inviting feedback**.
* Everyone is busy.
* Yet nobody can describe **what an equipment officer will be able to demonstrate at the end of the next iteration**.

---

## The Difficulty Is Not a Shortage of Ideas

* It is the **absence of a shared boundary** and a **credible route from an idea to evidence**.
* A backlog tells the team what might be valuable.
* An iteration plan must also explain:
  * **what it will try to achieve**,
  * **what it can reasonably finish**,
  * **how another person will know that it worked**.

---

## What This Chapter Builds

* A bounded **project vision**.
* A thin **user journey**.
* A **capacity-aware plan**.
* A **repository that runs supplied checks**.
* The existing reservation behaviour is **preserved**. The availability enquiry (US-02) remains **proposed work**.
* Preparing delivery evidence is progress, but it must **not** be reported as newly implementing behaviour already in the starter.

---

# 4.1 What Are We Building?
### Vision, scope and constraints

---

## A Vision Explains Whose Problem and What Improvement

* It should **guide choices when time is limited**.
* "Build a complete equipment platform" provides little help: almost any proposed feature can be justified under it.
* A useful vision identifies **an actor**, **an observable improvement** and **the setting where the claim can be evaluated**.

---

## The Working Vision

> Help an equipment officer demonstrate clear reservation decisions for a small, controlled set of student borrowers and equipment, so that accepted requests can be inspected and conflicting requests do not create overlapping records within one running coordinator.

---

## What the Vision Does Not Promise

* It is deliberately narrower than a production service.
* It does **not** promise:
  * authentication,
  * a maintained inventory,
  * safe operation by several officers at once.
* The broader direction can include borrowing and returns later. The first evidence stays **small enough to inspect**.

---

## Product Goal, Iteration Goal, Sprint Backlog

* A **Product Goal** describes a future product state toward which the team works.
* An **iteration goal** gives the next period of work coherence.
* Neither is a list of every task.
* In Scrum, the **Sprint Backlog** combines the Sprint Goal, selected backlog items and an actionable delivery plan.
* Our worked plan uses that distinction **without assuming a classroom team has adopted every element of Scrum**.

---

## Make the Boundary Visible

* Scope is most useful when it **makes decisions easier**.
* Use a short table that distinguishes:
  * **present capability**,
  * **selected work**,
  * **deferred questions**.
* The next three slides show the table for the Chapter 4 version.

---

## Scope at the Chapter 4 Version (1 of 3)

| Area | At the version | Planning consequence |
|---|---|---|
| Reservation request | Existing Java accepts eligible, non-conflicting requests | Verify and demonstrate; do not rebuild it for credit |
| Availability enquiry | Proposed US-02; no query method or interface | Refine and plan a thin next slice |
| Storage | In-memory records in one coordinator | Restart loses records; demonstrate in one process |

---

## Scope at the Chapter 4 Version (2 of 3)

| Area | At the version | Planning consequence |
|---|---|---|
| Identity and equipment | Nonblank identifiers; synthetic examples | No claim of directory or catalogue validation |
| Loan period | Whole days; start inclusive, end exclusive | Label dates and test adjacency |
| Cancellation and completed loans | Not implemented; all stored reservations count as active | Clarify lifecycle before adding those stories |

---

## Scope at the Chapter 4 Version (3 of 3)

| Area | At the version | Planning consequence |
|---|---|---|
| User interface | Scripted console demonstration; proposed wireframes | No web or mobile implementation required for kickoff |
| Concurrent use | Sequential teaching example | No claim that a check prevents races across processes |

---

## Constraints, Assumptions, Open Questions

* **Constraint:** Java 17 compatibility is a chosen technical constraint for this starter.
* **Teaching boundary:** using synthetic borrower identifiers.
* **Assumption:** an officer can recognise a sample item (an assumption about the demonstration).
* **Open question:** the rule about past dates.
* Labelling all four as "requirements" hides their **different owners and consequences**.

---

## An Assumption Needs a Trigger

* Example: "For the controlled demo, the operator uses CAM1 and MIC1 from a supplied list of sample items."
* Trigger: "Before opening input to arbitrary equipment, clarify the catalogue authority and unknown-item behaviour."
* The trigger connects a **temporary simplification** to **the point at which it becomes inadequate**.

---

## A Small Decision Record

* State: the **question**, the **chosen approach**, the **reason**, the **consequence** and the **review trigger**.
* It need not be a long report.
* "Use in-memory records for kickoff because the immediate question concerns reservation decisions; records disappear on restart; reconsider when a demonstration must survive restarting."

---

## "Database Later" Is Not a Decision

* It records **neither the current limitation nor the condition that will make the work necessary**.
* The team could postpone essential persistence **indefinitely**, or introduce it **immediately without a reason**.
* A clear trigger lets the plan change **when the evidence changes**.

---

## Do Not Settle Every Future Policy

* Resolve the questions that **determine the next slice's behaviour**.
* Keep other questions visible, each with **an owner and a decision point**.
* This supports progress while preventing a temporary assumption from **quietly becoming a permanent rule**.

---

# 4.2 Sketching the Screens and Walking Through Examples
### A wireframe is a question made visible

---

## What a Wireframe Is For

* A lightweight wireframe helps users and developers discuss **information, actions and outcomes** before spending time on presentation.
* It may be a **table, a sketch or a simple sequence of views**.
* Its value comes from **the questions it exposes**, not from visual polish.

---

## Questions a Journey Exposes

* What does the officer enter?
* Does "end date" **include that day**?
* What appears when equipment is unavailable?
* Does a failed request **leave a record**?
* Can the officer distinguish a **successful reservation** from an **availability observation**?
* The next slides are **proposed interface sketches**, not screenshots of implemented screens.

---

## View A: Request a Reservation

| Element | Example or behaviour |
|---|---|
| Borrower identifier | B1 |
| Equipment identifier | CAM1 |
| Start date | 2026-10-20 |
| Duration in days | 2 |
| Period explanation | Includes 20 and 21 October; ends before 22 October |
| Action | Request reservation |
| Scope note | Controlled demo; records last only for this session |

---

## View B: Request Outcome

| Outcome | Information shown |
|---|---|
| Confirmed | Reservation R1, B1, CAM1, `[2026-10-20, 2026-10-22)` |
| Item unavailable | Request rejected; no new reservation stored |
| Limit or duration failure | Request rejected; no new reservation stored |
| Malformed input | The proposed interface should explain the field to correct |

---

## View B: What Is Real and What Is Drawn

* The coordinator currently returns **confirmation or rejection strings** and throws exceptions for certain invalid arguments.
* A future interaction layer must **translate malformed input** into a useful response. Drawing it does not implement it.
* The coordinator **combines borrower-limit and duration failures in one message**.
* A sketch showing **two precise explanations** introduces new work the backlog should identify.

---

## View C: Availability Enquiry (Proposed US-02)

| Element | Example or behaviour |
|---|---|
| Equipment identifier | CAM1 from the controlled set of sample items |
| Start date | 2026-10-22 |
| End date, exclusive | 2026-10-23 |
| Action | Check availability |
| Result | Available, unavailable, or an identifiable invalid-period outcome |
| Explanation | An enquiry creates no reservation and does not guarantee a later request will succeed |

---

## Do Not Choose a Toolkit Yet

* A user can understand the sketch without agreeing to a particular toolkit.
* That leaves the team free to use a **thin console interaction** while learning about the domain.
* Choosing a web framework now would add configuration and presentation tasks **without resolving the date-boundary question**.

---

## Walk Through Concrete Examples

1. Begin with no reservations.
2. Submit B1, CAM1, 20 October, two days. **Expect one stored reservation ending exclusively on 22 October.**
3. Submit B2, CAM1, 21 October, one day. **Expect rejection and the original record preserved.**
4. Submit B2, CAM1, 22 October, one day. **Expect a second stored reservation.**

---

## Why the Last Step Matters

* Otherwise "no overlap" is ambiguous.
* If the officer expects collection on 22 October to **conflict** with the earlier booking, either the **period convention** or an **operational turnaround rule** needs discussion.
* Do **not** silently add a cleaning interval to the current rule.
* Record it as a **candidate requirement with examples**.

---

## For an Availability Enquiry, Record Two Things

* The **displayed answer**.
* The **unchanged state**.
* A program that says "available" after quietly creating a reservation has **not fulfilled the story**.
* An observation of availability is **not permission to reserve**: a borrower may already have three active records.
* The proposed query does **not** establish borrower eligibility.

---

## Three Descriptions of One Behaviour

* **Wireframes**, **examples** and **code** are three descriptions of the same intended behaviour.
* Disagreement among them is **useful evidence**.
* Resolve it **explicitly**, instead of selecting whichever description is easiest to implement.

---

# 4.3 Prioritisation and Vertical Slicing
### What first, how thin?

---

## Preserve the Backlog's History (1 of 2)

| Order | Item | Current interpretation |
|---|---|---|
| 1 | US-01: Record an eligible reservation | Core behaviour exists; confirm interaction and delivery evidence |
| 2 | US-02: Inspect availability without reserving | New user outcome to refine and forecast |
| 3 | EN-01: Automate build and checks | Enabling work supplied in this chapter; hosted evidence still required |

---

## Preserve the Backlog's History (2 of 2)

| Order | Item | Current interpretation |
|---|---|---|
| 4 | US-03: Inspect a borrower's active records | Filtering and interaction remain new work |
| 5 | US-04: Cancel a confirmed reservation | Authority, lifecycle and count effects need clarification |
| 6 | US-05: Reject unknown equipment identifiers | Depends on a catalogue source and failure policy |

---

## Order Is Judgement, Not a Rigid Instruction

* Order is not an instruction to finish every task of one item before examining another.
* **EN-01 supports reliable delivery of US-02**, so preparing automation during kickoff is reasonable. Explain that dependency openly.
* Do not quietly move **every technical improvement** ahead of user feedback.
* "Low priority" for catalogue validation is defensible **only within the controlled set of sample items**.

---

## Vertical Slice

* A **vertical slice** passes through the necessary parts of the system to deliver **one observable outcome**.
* It need **not** use a graphical interface, database or network.
* For this project, a console request that reaches the coordinator and displays a verified decision is a **thin journey through interaction, domain behaviour and storage**.

---

## Vertical vs. Horizontal

<!--svg:ch04-slicing-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 310" role="img" aria-label="Left: a horizontal split does all screens, then all services, then all storage, so nothing can be demonstrated until the end. Right: a vertical slice is a thin path through interaction, domain behaviour and storage that delivers one observable outcome." style="display:block;width:100%;height:calc(var(--u) * 31.00);margin:0 auto">
<defs><marker id="ch04-slicing-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-slicing-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-slicing-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-slicing-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-slicing-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<text x="215.0" y="24.0" font-size="21" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Horizontal split</text>
<text x="655.0" y="24.0" font-size="21" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Vertical slice</text>
<rect x="15.0" y="46.0" width="400.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="215.0" y="83.5" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">All screens first</text>
<rect x="15.0" y="124.0" width="400.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="215.0" y="161.5" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Then all services</text>
<rect x="15.0" y="202.0" width="400.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="215.0" y="239.5" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Then all storage</text>
<text x="215.0" y="296.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Work exists, but nothing is demonstrable until the end.</text>
<rect x="455.0" y="46.0" width="400.0" height="62.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="475.0" y="84.0" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="start">Interaction</text>
<rect x="455.0" y="124.0" width="400.0" height="62.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="475.0" y="162.0" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="start">Domain behaviour</text>
<rect x="455.0" y="202.0" width="400.0" height="62.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="475.0" y="240.0" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="start">Storage</text>
<rect x="745.0" y="38.0" width="90.0" height="232.0" rx="10" fill="#f6ead9" stroke="#b4762e" stroke-width="2.6"/>
<text x="790.0" y="160.0" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="middle">US-02</text>
<text x="655.0" y="296.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">A thin path through every layer: one observable outcome.</text>
</svg>
</div>
<!--/svg-->

---

## Why Horizontal Splitting Hurts

* "All screens first, then all services, then all storage" can leave **substantial work without a demonstrable outcome**.
* Those activities may be implementation tasks.
* They do **not** become useful increments merely because they are separate tickets.

---

## A First Slice for US-02

> The officer supplies one sample item and a valid date interval, receives an availability answer based on current reservations, and can verify that the enquiry left every stored reservation unchanged.

---

## What the Slice Defers and What It Cannot

* **Can defer:** calendar styling, multiple-item search, live inventory integration, availability across several servers.
* **Cannot defer:** overlap semantics and state preservation. They determine **whether the promised outcome is true**.
* The slice also needs an identifiable response to an **equal or reversed interval**.

---

## Acceptance Examples for the Slice

| ID | Given and enquiry | Expected outcome |
|---|---|---|
| AQ-01 | Empty coordinator; CAM1 `[20 Oct, 22 Oct)` | Available; records unchanged |
| AQ-02 | CAM1 reserved `[20 Oct, 22 Oct)`; enquire `[21 Oct, 23 Oct)` | Unavailable; records unchanged |
| AQ-03 | Same reservation; enquire `[22 Oct, 23 Oct)` | Available; records unchanged |
| AQ-04 | Same reservation; example MIC1 for `[20 Oct, 22 Oct)` | Available; records unchanged |
| AQ-05 | Equal or reversed start and end | Identifiable invalid-input outcome; records unchanged |

---

## "Records Unchanged" Means Contents Too

* All dates are in 2026.
* "Unchanged" means preserving **contents as well as count**.
* A query that **replaces one reservation with another** can leave the same size and still be incorrect.
* The exact query API and invalid-input representation are **design choices to settle before implementation**. The existing `reserve` method is not a query implementation.

---

## When Is a Feature Small Enough?

* When the team can **understand and verify it within the iteration, including integration**.
* Making it smaller by removing meaningful rejection behaviour can produce **misleading success**.
* A reservation feature that accepts requests but **ignores conflicts** is not a safe reduction of this outcome.

---

## Necessary Work vs. Attractive Additions

* **Necessary for US-02:** interpreting the interval, inspecting relevant reservations, reporting the result, checking non-mutation.
* **Optional:** a calendar widget.
* A **persistent store** becomes necessary only when the selected outcome requires data to survive a restart.
* This lets the team negotiate scope **without treating quality as optional**.

---

## Epics Group Direction, Not Iteration Size

* "Reservation decisions" can contain US-01 and US-02.
* "Record lifecycle" can contain US-03 and US-04.
* EN-01 supports delivery across them.
* An epic does **not** require an architecture layer or a Java package with the same name.

---

# 4.4 What Can We Really Finish?
### Release outlook and iteration planning

---

## An Outlook Is Not a Commitment

* A **release outlook** communicates likely steps toward the product goal, and **should show uncertainty**.
* The book's teaching stages: **kickoff** makes the baseline reproducible; the **MVP stage** develops a small reservation and loan flow; **later stages** add integration boundaries and respond to a changed requirement.
* These are teaching stages, **not evidence that every team can deliver identical scope on identical dates**.

---

## Now, Next, Later

* Use a short outlook with **"now", "next" and "later"** if precise forecasts would be invented.
* Keep the module's official milestone schedule **unchanged**.
* A planning table **cannot create a new assessment deadline** or promise that a poorly understood story will fit a particular week.

---

## Two Different Goals

> **Kickoff goal:** Make the reservation baseline reproducible and reviewable, and prepare a bounded availability slice for the next iteration.

> **Candidate next iteration goal:** Let the officer inspect availability for one sample item and interval without changing reservations.

---

## What Chapter 4 Provides

* Chapter 4 provides the **first goal's** starter materials.
* It **plans** the second goal.
* It does **not** claim to have implemented US-02.

---

## Counting Capacity

<!--svg:ch04-capacity-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 262" role="img" aria-label="22 person-hours reported: 4 reserved for coordination, integration and administration, leaving an 18-hour planning budget. Selected work is 14 hours (2, 4, 3, 3 and 2), leaving 4 hours unallocated." style="display:block;width:100%;height:calc(var(--u) * 26.20);margin:0 auto">
<defs><marker id="ch04-capacity-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-capacity-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-capacity-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-capacity-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-capacity-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<text x="435.0" y="24.0" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#1d588c" text-anchor="middle">Four members report 6 + 6 + 5 + 5 = 22 person-hours</text>
<rect x="6.0" y="40.0" width="156.0" height="52.0" rx="4" fill="#c3cfdd" stroke="#1d588c" stroke-width="2"/>
<text x="84.0" y="74.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Reserved</text>
<text x="84.0" y="112.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">coordination,</text>
<text x="84.0" y="128.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">integration, admin</text>
<rect x="162.0" y="40.0" width="78.0" height="52.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="2"/>
<text x="201.0" y="74.0" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">2</text>
<text x="201.0" y="112.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">resolve the</text>
<text x="201.0" y="128.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">query contract</text>
<rect x="240.0" y="40.0" width="156.0" height="52.0" rx="4" fill="#2f78b3" stroke="#1d588c" stroke-width="2"/>
<text x="318.0" y="74.0" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">4</text>
<text x="318.0" y="112.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">implement the</text>
<text x="318.0" y="128.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">read-only query</text>
<rect x="396.0" y="40.0" width="117.0" height="52.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="2"/>
<text x="454.5" y="74.0" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">3</text>
<text x="454.5" y="112.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">thin interaction,</text>
<text x="454.5" y="128.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">invalid input</text>
<rect x="513.0" y="40.0" width="117.0" height="52.0" rx="4" fill="#2f78b3" stroke="#1d588c" stroke-width="2"/>
<text x="571.5" y="74.0" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">3</text>
<text x="571.5" y="112.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">query and</text>
<text x="571.5" y="128.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">regression checks</text>
<rect x="630.0" y="40.0" width="78.0" height="52.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="2"/>
<text x="669.0" y="74.0" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">2</text>
<text x="669.0" y="112.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">review, notes,</text>
<text x="669.0" y="128.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">rehearsal</text>
<rect x="708.0" y="40.0" width="156.0" height="52.0" rx="4" fill="#ffffff" stroke="#b4762e" stroke-width="2" stroke-dasharray="7 5"/>
<text x="786.0" y="74.0" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="middle">4</text>
<text x="786.0" y="112.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">unallocated:</text>
<text x="786.0" y="128.2" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle">room for uncertainty</text>
<path d="M162.0,160.0 L162.0,170.0 L708.0,170.0 L708.0,160.0" fill="none" stroke="#1d588c" stroke-width="2.4"/>
<text x="435.0" y="192.0" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#1d588c" text-anchor="middle">Selected work: 14 person-hours</text>
<path d="M162.0,208.0 L162.0,218.0 L864.0,218.0 L864.0,208.0" fill="none" stroke="#b4762e" stroke-width="2.4"/>
<text x="513.0" y="240.0" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#b4762e" text-anchor="middle">Planning budget: 18 person-hours</text>
</svg>
</div>
<!--/svg-->

---

## The Arithmetic

* These figures are **invented planning data**, not official contact hours or measured productivity.
* Four members report **6, 6, 5 and 5** person-hours: **22**.
* Reserve **four** for coordination, integration support and routine administration.
* The remaining planning budget is **18 person-hours**.

---

## Forecast Work for the Next Iteration

| Forecast work | Person-hours |
|---|---:|
| Resolve the query contract and update examples | 2 |
| Implement the read-only enquiry behaviour | 4 |
| Add the thin interaction and invalid-input response | 3 |
| Add and run query checks alongside regression checks | 3 |
| Review, integrate, update notes and rehearse the demonstration | 2 |
| **Selected work** | **14** |
| **Unallocated capacity within the 18-hour budget** | **4** |

---

## How to Read the Estimates

* They are discussion inputs, **independently expressed in person-hours**.
* They are **not converted from Chapter 3's story points**.
* Two people pairing for one hour consume **two** person-hours.
* Review and correction must fit in the budget. Calling them "after development" **does not make them free**.

---

## The Four Unallocated Hours

* They provide **room for uncertainty**.
* They are **not** a promise to pull in another feature.
* If the query needs an unexpected policy decision, use the capacity to **resolve that risk while protecting the goal**.
* If things finish early, **improve evidence** or select additional work deliberately.

---

## 18 Hours Does Not Establish Feasibility

* Suppose the **only person who can explain the coordinator** is unavailable until the last day, while the **reviewer is free only at the beginning**.
* The work cannot flow as the arithmetic suggests.
* Ask **when collaboration can occur** and whether knowledge must be shared earlier.

---

## Ownership Without Specialists

* A task owner ensures that **progress and questions remain visible**.
* It does **not** mean nobody else may help.
* Agree an **early pairing session** on the query contract and a **review window** before the final demonstration.
* A little coordination prevents the **entire slice waiting at the end**.

---

## When the Evidence Changes

* If four hours of implementation become nine, **discuss the forecast and remaining scope**.
* Do not hide the overrun by **postponing checks** or declaring the interaction "almost done".
* In Scrum, scope can be clarified and renegotiated with the Product Owner while **protecting the Sprint Goal**.
* A classroom adaptation should **make its decisions visible**.

---

## Replanning Example

* Implementation revised from **4 to 9** hours after a contract ambiguity.
* Selected work becomes **19 hours**: already above the **18-hour** budget.
* Do **not** preserve the status by removing checks.
* Revisit the ambiguity and reduce an optional part of the interaction, or **revise the forecast transparently**.
* If no coherent verified slice fits, report the outcome as **at risk** and renegotiate the selected work.

---

## The Practical Replanning Question

> What complete, still useful outcome can we verify with the capacity left?

* Sometimes the answer is a **smaller interface**.
* Sometimes unresolved behaviour means the item **cannot responsibly be called complete**.
* **Honest incompleteness is more useful than a green status that conceals unfinished work.**

---

# 4.5 How the Team Works Together
### Agreements and review

---

## Agree How Work Moves

* Keep Chapter 3's board: **Backlog, Ready, Building, Review, Done**.
* Combined **WIP limit of two** across Building and Review.
* A blocked item **still occupies a slot**. If review is blocked, helping it finish is usually better than starting a third item.

---

## What a Team Agreement Answers

* **Where** do requirements live?
* **How** are questions raised?
* **Who** reviews a change?
* **What evidence** do reviewers need?
* **How** is unfinished work reported?
* The board tool is interchangeable. A **shared Markdown table** can work if updates are visible and ownership is clear.

---

## Start From What You Decided Earlier

* The **issue board and branch policy** from Chapter 2 Part D.
* The **Definition of Done** from Chapter 3.
* Your **process note** naming which Scrum elements you use as defined and which you adapt.
* Revise them where experience shows a problem, and **record why**.

---

## Small, Short-Lived Branches

* One branch should contain **a coherent change another person can understand**.
* "Set up every tool and rewrite the coordinator" is hard to review: **functional and workflow changes become entangled**.
* A branch that adds the checking script and its documentation has a **clearer purpose**.

---

## The Review Loop

<!--svg:ch04-review-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="Team policy: a small change and local checks go to review and CI. If there is a blocking finding, correct and rerun, then return to review. If not, integrate and verify the shared branch." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch04-review-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-review-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-review-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-review-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-review-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="110.0" width="200.0" height="80.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="110.0" y="144.6" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Small change</text>
<text x="110.0" y="168.3" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">and local checks</text>
<rect x="270.0" y="110.0" width="200.0" height="80.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="370.0" y="156.5" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Review and CI</text>
<polygon points="605.0,95.0 680.0,150.0 605.0,205.0 530.0,150.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="605.0" y="144.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Blocking</text>
<text x="605.0" y="167.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">finding?</text>
<rect x="520.0" y="235.0" width="170.0" height="50.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="605.0" y="266.1" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Correct and rerun</text>
<rect x="730.0" y="110.0" width="135.0" height="80.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="797.5" y="135.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">Integrate and</text>
<text x="797.5" y="155.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">verify the</text>
<text x="797.5" y="175.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">shared branch</text>
<path d="M210.0,150.0 L270.0,150.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-review-arr)"/>
<path d="M470.0,150.0 L530.0,150.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-review-arr)"/>
<path d="M680.0,150.0 L730.0,150.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-review-arr)"/>
<text x="705.0" y="138.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">No</text>
<path d="M605.0,205.0 L605.0,235.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-review-arr)"/>
<text x="627.0" y="224.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Yes</text>
<path d="M520.0,260.0 L370.0,260.0 L370.0,190.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-review-arr)"/>
<text x="370.0" y="20.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">A team policy: git does not enforce review by itself.</text>
</svg>
</div>
<!--/svg-->

---

## A Policy, Not a Guarantee

* This describes the chapter's **team policy**. A repository does not enforce review **because the README requests it**.
* Where supported, configure the shared branch to **require the agreed check and review**.
* If enforcement is unavailable, **state that the team follows a manual policy** and retain its review evidence.

---

## Review the Claim, the Change and the Evidence

* Start with the **intended behaviour**.
* Trace the relevant code or documentation.
* Ask whether the **evidence supports the claim**.
* "Looks good" alone does not say **which risk was examined**.

---

## What to Ask About a CI Change

* Does a **compilation failure stop the job**?
* Do the check programs **actually execute**?
* Does a **failed assertion reach the job result**?
* For US-02 later: does the query **mutate state**, or depend on a borrower's eligibility?
* A code-style comment should not distract from a **behavioural defect**.

---

## Author and Reviewer Duties

* The author **resolves blocking findings** and **reruns affected checks**.
* The reviewer **inspects the correction**.
* Retain the **actual feedback and response**. Do not invent a review exchange to fill a template.
* Working alone permits a **documented self-review** for practice. It is **not independent review** and should be labelled so.

---

## Extending the Definition of Done

* Carry forward Chapter 3: checked examples, reproducible execution, actual review, integrated code, updated notes, repeatable demonstration.
* **Add:** the agreed automated check has **passed on the integrated revision** and the team can **locate its result**.
* Acceptance criteria stay specific to a story. A passing pipeline is **one part** of the DoD.
* It does not establish that a wireframe was understood or a useful outcome delivered.

---

## Forms in Appendix C

* **C.6:** the iteration plan of Section 4.4.
* **C.7:** a team agreement.
* **C.8:** a pull-request description.
* **C.9:** the evidence note of this chapter's companion.
* Each form comes with a worked example.

---

# 4.6 A Starter Build and CI You Can Run
### One command that means something

---

## Make One Command Meaningful

* CI needs a check that can run **without relying on one developer's open IDE**.
* The starter uses **Java 17, Bash and the supplied executable Java checks**. No external Java dependencies.
* Maven and JUnit remain the planned tools for the fuller testing stage. This version **keeps the plain-Java checks** so kickoff does not need a test framework first.
* On Windows, run the script from **Git Bash or WSL**. PowerShell cannot interpret it.

---

## From the Flat Directory to a Conventional Layout

* Continuing from the flat Chapter 2 directory, the move is **mechanical**:
  * application classes go to `src/main/java`,
  * check classes go to `src/test/java`,
  * their contents **do not change**.
* The classes stay in the **unnamed package**: a layout change only.
* It is the layout Maven expects, so a later move changes the build file and the checks, **not where the sources live**.

---

## The Repository Files (1 of 2)

| Relative path | Purpose |
|---|---|
| `src/main/java/ReservationRules.java` | Existing borrower-count and duration rule |
| `src/main/java/LoanPeriod.java` | Existing immutable interval and overlap behaviour |
| `src/main/java/Reservation.java` | Existing immutable reservation data |
| `src/main/java/ReservationCoordinator.java` | Existing sequential, in-memory reservation operation |
| `src/main/java/Chapter04Demo.java` | Fixed three-request demonstration |

---

## The Repository Files (2 of 2)

| Relative path | Purpose |
|---|---|
| `src/test/java/Chapter02Checks.java` | Existing 34 regression checks |
| `src/test/java/Chapter03AcceptanceExamples.java` | Existing five acceptance example groups |
| `scripts/check.sh` | Compile and execute the agreed gate |
| `.github/workflows/java-check.yml` | Hosted CI template |
| `.gitignore`, `.gitattributes`, `README.md` | Exclusions, LF endings, setup and scope |

---

## The Gate Script

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p build/classes
find build/classes -type f -name '*.class' -delete

java -version
"${CHAPTER_JAVAC:-javac}" --release 17 -encoding UTF-8 -d build/classes \
  src/main/java/*.java src/test/java/*.java
java -cp build/classes Chapter02Checks
java -cp build/classes Chapter03AcceptanceExamples
echo "BUILD AND CHECKS PASSED"
```

---

## What the Script Does

* Clears **generated class files**, then compiles the listed source directories.
* Runs Chapter 2's **34 checks** and Chapter 3's **five acceptance example groups**, then prints a completion message.
* Compilation targets Java 17 through `--release 17`; generated classes go into a **separate output directory**.
* The script **must stop** when compilation or either checking program fails. The final message is reached **only after success**.

---

## Why the Gate Is Built This Way

* It changes to the **project root relative to its own location**: independent of the caller's directory.
* `set -euo pipefail` stops on a failing command, rejects unset variables and propagates pipeline failures.
* There is **no `|| true`**, no catch-and-ignore handler, no success message issued before checking.
* Adding another check class also requires **adding its run command**: compiling does not run a `main` method.

---

## The Gate as a Picture

<!--svg:ch04-gate-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 330" role="img" aria-label="The gate: scripts/check.sh compiles with --release 17, runs Chapter02Checks and then Chapter03AcceptanceExamples, and only then prints BUILD AND CHECKS PASSED. Any failing step stops the script with a nonzero exit. The hosted workflow checks out the repository, installs Temurin Java 17 and runs the same script." style="display:block;width:100%;height:calc(var(--u) * 33.00);margin:0 auto">
<defs><marker id="ch04-gate-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-gate-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-gate-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-gate-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch04-gate-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="20.0" width="190.0" height="84.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="105.0" y="57.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Compile</text>
<text x="105.0" y="78.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">javac --release 17</text>
<rect x="230.0" y="20.0" width="190.0" height="84.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="325.0" y="57.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Chapter02Checks</text>
<text x="325.0" y="78.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">34 checks</text>
<rect x="450.0" y="20.0" width="190.0" height="84.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="545.0" y="46.5" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Chapter03</text>
<text x="545.0" y="67.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">AcceptanceExamples</text>
<text x="545.0" y="89.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">5 groups</text>
<rect x="670.0" y="20.0" width="190.0" height="84.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="765.0" y="57.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">BUILD AND</text>
<text x="765.0" y="78.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">CHECKS PASSED</text>
<path d="M200.0,62.0 L230.0,62.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-gate-arr)"/>
<path d="M420.0,62.0 L450.0,62.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-gate-arr)"/>
<path d="M640.0,62.0 L670.0,62.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-gate-arr)"/>
<path d="M105.0,104.0 L105.0,150.0" fill="none" stroke="#b4762e" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch04-gate-arr)"/>
<path d="M325.0,104.0 L325.0,150.0" fill="none" stroke="#b4762e" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch04-gate-arr)"/>
<path d="M545.0,104.0 L545.0,150.0" fill="none" stroke="#b4762e" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch04-gate-arr)"/>
<rect x="10.0" y="150.0" width="630.0" height="40.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="325.0" y="177.0" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">any failure stops the script: nonzero exit, no success line</text>
<text x="10.0" y="232.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#1d588c" text-anchor="start">Hosted workflow (GitHub Actions template):</text>
<rect x="10.0" y="248.0" width="250.0" height="64.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="135.0" y="285.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">actions/checkout</text>
<rect x="290.0" y="248.0" width="250.0" height="64.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="415.0" y="275.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">actions/setup-java</text>
<text x="415.0" y="295.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Temurin 17</text>
<rect x="570.0" y="248.0" width="250.0" height="64.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="695.0" y="275.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">bash scripts/check.sh</text>
<text x="695.0" y="295.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">the same gate</text>
<path d="M260.0,280.0 L290.0,280.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-gate-arr)"/>
<path d="M540.0,280.0 L570.0,280.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch04-gate-arr)"/>
</svg>
</div>
<!--/svg-->

---

## What a Passing Run Prints

```text
All 34 chapter checks passed.
AC-01 passed
AC-02 passed
AC-03 passed
AC-04 passed
AC-05 passed
All 5 acceptance examples passed.
BUILD AND CHECKS PASSED
```

* The five groups contain multiple assertions. Do **not** add 34 and 5 and call it 39 individual assertions.

---

## What a Pass Establishes

* The five acceptance examples cover: eligible reservation, overlap rejection, adjacency, borrower limit, duration boundaries.
* They do **not** test US-02, because that feature is not implemented.
* A pass establishes something **bounded**: the supplied reservation checks passed against **this revision in the recorded environment**.
* It is **not** a claim of complete correctness.

---

## Run the Scripted Journey

```bash
java -cp build/classes Chapter04Demo
```

```text
Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Rejected: item unavailable.
Confirmed: R2 for B2 on CAM1 [2026-10-22, 2026-10-23).
Stored reservations: 2
```

* Fixed synthetic examples. **Not interactive.** The second request neither consumes an identifier nor creates a record.

---

## Line Endings Can Break the Script

* Git on Windows may convert **LF to CRLF** on checkout.
* A CRLF script fails under WSL or Linux with an error such as `set: pipefail: invalid option name`.
* The repository includes a `.gitattributes` file containing `*.sh text eol=lf`.
* **Check that it is committed** before a teammate tries a fresh clone.

---

## Read a Check as Arrange, Act, Assert

```java
// Arrange: the coordinator already holds B1's reservation of CAM1.
// Act: B2 asks for CAM1 on an overlapping day.
String conflict = coordinator.reserve("B2", "CAM1", day.plusDays(1), 1);
// Assert: the request is refused, and nothing new was stored.
require(conflict.equals("Rejected: item unavailable."), "AC-02 rejection");
require(coordinator.reservations().size() == 1, "AC-02 unchanged count");
```

---

## The Three Steps

* **Arrange** builds the situation.
* **Act** performs the one operation under test.
* **Assert** states what must be observed, **including what must not have changed**.
* A check asserting only the message would pass for a request that was refused **but still stored**.
* Chapter 7 names this structure Arrange-Act-Assert and builds on it.

---

## The Hosted Workflow: Triggers

```yaml
name: Java starter checks
on:
  push:
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
```

* Runs on **pushes, pull requests and manual dispatch**, with **read-only** access to the repository contents.

---

## The Hosted Workflow: The Job

```yaml
jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: '17'
      - name: Compile and check
        run: bash scripts/check.sh
```

---

## Reading the Workflow

* Stored under `.github/workflows`.
* A hosted Ubuntu runner; Temurin Java 17; the **same gate**; a five-minute timeout.
* A push tied to a pull request may produce both kinds of run. The simple template accepts that duplication.
* A passing workflow does **not** configure merge requirements automatically.

---

## GitHub Actions Is One Route

* An institution's alternative CI service is suitable if it **checks the intended revision, runs the agreed command and preserves inspectable results**.
* A badge or YAML file alone is **not a passing run**.
* Confirm that the workflow **actually starts** and that its compilation and checking steps **execute**.

---

## Record the Run

* The **revision**.
* The **environment**.
* The **command**.
* The **result**, with a **link or exported log**.
* For a pull request, identify the tested revision. After integration, retain the **shared branch's** passing result too.
* A branch check can become **stale** after another change is integrated.

---

## Version Selectors Can Move

* The example uses a Java major version and **action major tags** for readability.
* Those selectors can resolve to updated releases, so **record the resolved versions** in evidence.
* Stronger dependency pinning, wider environment coverage and delivery stages belong in **Chapter 13**.

---

## Prove That a Failure Is Observable

1. Begin with a **passing run**.
2. On a **disposable branch or copy**, change one acceptance check to expect **two** records after the first successful reservation.
3. That expectation is intentionally wrong: valid behaviour stores exactly **one**.
4. Run the same gate and expect a **nonzero result identifying AC-01**.

---

## The Deliberate Failure

```java
// original
require(coordinator.reservations().size() == 1, "AC-01 one record");
// intentionally wrong, on a practice branch only
require(coordinator.reservations().size() == 2, "AC-01 one record");
```

```text
All 34 chapter checks passed.
Exception in thread "main" java.lang.AssertionError: AC-01 one record
```

* The author run returned exit status `1`. `BUILD AND CHECKS PASSED` must be **absent**.

---

## Restore and Retain Evidence

* **Restore** the correct expectation and run again.
* On a hosted practice branch, retain the **failed run** and the **restored passing run**.
* **Never merge the deliberate defect** into the shared baseline.
* A local copy proves local failure propagation but **not hosted CI**. Report the distinction.

---

## Environment Failure vs. Assertion Failure

* A **failed download or missing JDK** does not prove failure propagation. It shows an environment failure **before the assertion was reached**.
* Read the log and identify the **actual failed step**.
* Replacing a test command with `echo passed` makes a green workflow that **checks nothing**.

---

## Author Verification Boundary

* Executed locally by the author: compilation, the 34 checks, the five acceptance groups, the demonstration and the failing-check experiment.
* The GitHub Actions workflow is **supplied for learners to run**.
* **No hosted execution or independent team review is claimed.**
* Completing the milestone's hosted CI evidence requires **an observed run in the team's repository**.

---

# 4.7 Getting Ready for Milestone 1
### An evidence trail that agrees with itself

---

## Assemble an Evidence Trail

* Milestone 1 connects the project direction to an **executable starting point**.
* The documents should **agree with one another**.
* A vision promising live inventory, a backlog assuming sample identifiers and a demo using invented equipment without explanation leave a reviewer **unable to interpret success**.
* The preparation map is a **navigation aid**, not an extra assessment rubric.

---

## The Preparation Map (1 of 3)

| Evidence | Question it should answer |
|---|---|
| Vision and scope | Whose outcome matters, and under which boundaries? |
| Epics, stories and ordered backlog | What is supported, what is next, what is uncertain? |
| Wireframes and acceptance examples | What will the officer do, see and change? |

---

## The Preparation Map (2 of 3)

| Evidence | Question it should answer |
|---|---|
| Capacity and iteration plan | Why is the selected work plausible, including verification and review? |
| Team agreement and review record | How will changes be inspected and integrated? |
| Repository and README | Can another person obtain the intended revision and run it? |

---

## The Preparation Map (3 of 3)

| Evidence | Question it should answer |
|---|---|
| Passing CI result | Did the configured service execute the gate successfully? |
| Deliberate failure and restored pass | Does a failed check produce failure, and is the baseline healthy again? |
| Decision and limitation notes | Which assumptions restrict the claims being made? |

---

## Trace a Few Meaningful Links

* Story to **acceptance examples**.
* Examples to the **checking program**.
* Change to **review**.
* Revision to **CI result**.
* Links are useful when they let another person **answer a question**.
* A large spreadsheet of repeated identifiers adds little if the linked check **does not exercise the promised behaviour**.

---

## Rehearse From Another Person's Starting Point

* Ask a teammate to follow the **README from a fresh checkout**. Watch where they need undocumented help.
* Does the command assume a **shell they do not have**?
* Is the JDK a **development kit** or only a runtime?
* Does the demo require **records created in an earlier session**?
* Correct the instructions and **repeat the affected step**.

---

## Transparent Gaps

* Do not report an unrun command as verified because it looks familiar.
* If the hosted service is unavailable, **preserve the local evidence and name the missing hosted result as a gap**.
* A transparent gap gives the team **a concrete next action**.
* The exit version: **a bounded plan, inspectable sketches and a repeatable baseline with a delivery gate**.

---

# 4.8 Challenging an Overambitious Plan with AI
### Verdicts, not vibes

---

## Ground Rules for the Activity (1 of 2)

| | For this activity |
|---|---|
| Your goal | Evaluate a proposed iteration plan against scope, capacity, behaviour and delivery evidence |
| You start with | The Chapter 3 backlog, the capacity figures in 4.4 and the Chapter 4 starter |
| What is in bounds | Review and replace the plan; do not implement any feature |

---

## Ground Rules for the Activity (2 of 2)

| | For this activity |
|---|---|
| How to check | Your capacity arithmetic; the code (is there a query method? does `reserve` change state?); the actual gate output |
| How to decide | A verdict and reason for each distinct proposal, then a bounded replacement plan |
| No AI account? | The ready-made example is enough |

* Chapter 15 collects the recurring AI workflows. This activity is self-contained.

---

## The Ready-Made Example (1 of 3)

**Author-written fictional AI output**, constructed for this offline exercise. Not a record of an actual model conversation.

> Four students have 22 person-hours, so plan 22 hours of features. Deliver US-02, cancellation, a mobile app, a database and email confirmations. Assign one student to each layer and integrate on the final evening.

---

## The Ready-Made Example (2 of 3)

> Convert the three-point availability story into three hours. Show "available" by calling `reserve` and deleting its record afterwards. Skip failure cases until next sprint.

---

## The Ready-Made Example (3 of 3)

> Mark EN-01 complete when the YAML file is committed; a green badge proves the whole story works.

* Create a review table: **a verdict and a reason for each distinct proposal**.
* Replace the plan with a bounded goal, a selected slice, a capacity calculation and explicit evidence.
* Find **at least one** domain error, one estimation error, one integration risk and one unsupported completion claim.

---

## Model Critique (1 of 3)

| Proposal | Verdict | Reason and correction |
|---|---|---|
| Allocate all 22 hours to features | Reject | Coordination, review and uncertainty consume capacity; use the explicit budget |
| Deliver query, cancellation, mobile, database and email together | Reject | The selected goal is one query slice; the additions lack agreed requirements |
| One layer per member; integrate at the end | Revise | Ownership can help; final-day integration delays learning |

---

## Model Critique (2 of 3)

| Proposal | Verdict | Reason and correction |
|---|---|---|
| Convert three story points into three hours | Reject | No valid conversion was established; estimate tasks from real understanding |
| Call `reserve`, then delete the record | Reject | A query must not change state; deletion is not even a supplied operation; eligibility differs |
| Defer failure cases | Reject | Invalid intervals and non-mutation are part of this outcome's acceptance |

---

## Model Critique (3 of 3)

| Proposal | Verdict | Reason and correction |
|---|---|---|
| Mark EN-01 complete when YAML is committed | Reject | Configuration must execute successfully and detect the intended failure |
| A green badge proves the whole story | Reject | The gate checks only executed conditions; current checks cover reservation, not US-02 |

* A corrected response states the **availability goal, AQ-01 to AQ-05, the 18-hour budget and 14-hour forecast**, plus review and observed CI evidence.

---

## Independent Verification

* Trace `reserve` to its `reservations.add` call.
* Observe the **absence of a query method**.
* Check the **arithmetic**.
* Inspect the **actual check output**.
* Asking a second AI model whether the first plan is good does **not** replace those observations.
* An AI-use record names: the prompt or example, claims examined, decisions, evidence, remaining uncertainty.

---

# 4.9 Planning Mistakes That Look Reasonable
### Eight to avoid

---

## Mistakes 1 to 3

| Mistake | Why it fails | Better action |
|---|---|---|
| Count starter behaviour as newly delivered | Hides the actual change | Separate existing capability from new evidence or functionality |
| Slice only by technical layers | No usable end-to-end result | Select one observable journey and its necessary tasks |
| Fill all nominal capacity with features | Review, coordination and uncertainty go unfunded | Budget those activities explicitly |

---

## Mistakes 4 to 6

| Mistake | Why it fails | Better action |
|---|---|---|
| Use a wireframe as proof of implementation | Confuses an agreed sketch with working behaviour | Label proposal and implementation separately |
| Treat an availability answer as a reservation | Omits eligibility and later state changes | Keep query and command outcomes distinct |
| Create CI configuration without running it | No evidence the gate executes | Inspect an actual run against the intended revision |

---

## Mistakes 7 and 8

| Mistake | Why it fails | Better action |
|---|---|---|
| "Fix" a red job by ignoring its exit status | Conceals the defect | Correct the cause; preserve failure propagation |
| Invent review or meeting evidence | Makes the project state misleading | Report actual observations and remaining gaps |

---

# 4.10 Try It Yourself
### Prepare for the kickoff

---

## Project and Input

* The activity runs on your team's project.
* Equipment lending: the supplied listings are your **starting repository**.
* Another provided domain: apply each step to **that domain's starter codebase**, using the supplied files as the model for layout, script and workflow.
* **You start with:** the Chapter 3 backlog, the current Java baseline and the Chapter 4 repository listings.
* Do not change domain without following the module's arrangements.

---

## Instructor Demonstration and Guided Practice

* **Demonstration:** walk through the three reservation requests, then compare an ordinary passing run with the **deliberately wrong acceptance check**. Ask what each result **establishes**.
* **Guided practice:** create a **one-page scope statement and wireframe**. Have another pair **explain the journey back to you**. Resolve one discrepancy between their interpretation and your intended behaviour.

---

## Independent Team Work (1 of 2)

1. Write the **vision, boundaries, assumptions and two decision records** with review triggers.
2. Group the backlog into **epics**, preserve story identifiers, and distinguish **existing capability from new work**.
3. Refine **US-02** (or an equivalent thin slice) with normal, boundary and rejection examples, **including state effects**.
4. Create an **iteration goal and capacity plan** using your actual availability, with coordination, review and uncertainty shown.

---

## Independent Team Work (2 of 2)

5. Agree **ownership, review and board policies**. Apply them to one small repository change.
6. Create the **starter files**, run the gate and reproduce the scripted demonstration.
7. Enable the **hosted workflow**. Retain a **passing run**, a **deliberate assertion-failure run** on a practice branch, and a **restored passing run**. Record the integrated baseline's result.
8. Assemble the **evidence map**; ask another team member to follow the README from a fresh checkout.

---

## Expected Output

* Vision and scope notes.
* Ordered backlog and selected story.
* Wireframes.
* Capacity plan.
* Team agreement and review record.
* Repository instructions.
* Verification evidence.
* Unresolved questions **with owners**.

---

## Completion Checks

* Another person can explain the **chosen outcome**.
* They can distinguish **implemented and planned behaviour**.
* They can **run the baseline** and **locate the actual CI results**.
* They can trace **at least one acceptance example to an executed check**.
* A missing hosted run remains an **explicit gap**.
* Use the module leader's submission requirements for the assessed hand-in.

---

## Model Document: Vision and Scope

* **Working vision:** help an equipment officer demonstrate clear reservation decisions for a controlled set of student borrowers and equipment, and inspect accepted records without overlapping reservations for the same item in one coordinator.
* **In scope:** one item per request; inclusive start, exclusive end; the student rules; deterministic synthetic examples; sequential calls in one process.
* **Outside:** persistent storage, real catalogue validation, cancellation, returns, email, concurrency, a polished interface.

---

## Model Document: Open Questions

* Treatment of **past dates**.
* **Operational turnaround** between loans.
* **Authority to cancel**.
* What "**active**" means after cancellation or completion.
* The **catalogue source** and its failure behaviour.
* Resolve only those that **block the selected next outcome**. Attach an owner and a review trigger to the others.

---

## Model Decision Record D-01: Storage

* **Question:** must kickoff preserve records across restarts?
* **Decision:** keep one in-memory coordinator.
* **Reason:** the demonstration evaluates reservation decisions in one session.
* **Consequence:** a restart loses records and the identifier sequence restarts.
* **Review trigger:** a selected outcome requires a session to survive restart.
* **Status:** the existing teaching baseline.

---

## Model Decision Record D-02: Query Interaction

* **Question:** what input expresses the query interval?
* **Proposed decision:** a start and an **explicitly labelled exclusive end**.
* **Reason:** it makes the half-open interval visible in discussion.
* **Consequence:** the officer needs clear date guidance; equal or reversed bounds must be reported.
* **Review trigger:** a walkthrough shows persistent confusion or a preference for duration.
* **Status:** proposed; obtain team agreement first.

---

## Model Document: The US-02 Contract

* **Story:** as an equipment officer, I want to inspect whether one sample item is available for a stated interval, so I can discuss a possible reservation without creating one.
* **Acceptance:** AQ-01 to AQ-04 report availability for empty state, overlap, adjacency and a different item; AQ-05 reports an identifiable invalid-period outcome; **every enquiry leaves all reservation contents unchanged**.
* **Still to decide:** the invalid-input representation. Do not present two as simultaneously implemented.

---

## Review Trap: Availability Is Not Eligibility

* If B1 already holds three active reservations, an unreserved item can be **available** even though B1 **cannot reserve it**.
* Reusing `reserve` as the enquiry **mixes those questions and changes state**.
* **Necessary tasks:** agree the contract; add a read-only operation; add the thin interaction; test results and non-mutation; review and integrate; update instructions; demonstrate.

---

## Model Team Agreement

* Keep stories and acceptance examples in shared project notes; **preserve identifiers** when refining wording.
* Backlog, Ready, Building, Review, Done; **Building plus Review limited to two; blocked items count**.
* Branches small enough for a reviewer to explain.
* Authors **run the gate before review and after corrections**. Reviewers inspect behaviour, state effects and evidence.
* Record the shared branch's check result after integration. **Mark missing evidence as a gap; never manufacture it.**

---

## The Evidence Note (Blank Template) (1 of 2)

| Field | Team entry |
|---|---|
| Repository and baseline revision | The actual repository and commit |
| Implemented behaviour | Only the behaviour present at that revision |
| Local environment and command | Java version, shell, command |
| Local check result | Observed exit status and relevant output |
| Hosted passing run | Run URL or retained log, tested revision, date |

---

## The Evidence Note (Blank Template) (2 of 2)

| Field | Team entry |
|---|---|
| Deliberate failure | Practice revision, failed assertion, failed run |
| Restored pass | Restored revision and passing run |
| Independent review | Actual reviewer, finding, correction, follow-up |
| Unresolved questions | Owner, impact, next decision point |
| Known limitations | Scope boundaries relevant to interpreting the demo |

* A template, **not completed evidence**.

---

## Feedback Questions (Not Document Counts)

| Dimension | Useful feedback question |
|---|---|
| Scope | Can the team explain the conditions under which its claim is valid? |
| Slice | Does the result support one observable outcome, including necessary failures? |
| Planning | Is review and uncertainty accounted for, and can people collaborate when needed? |
| Traceability | Does the cited check actually exercise the criterion? |
| Workflow | Is there real evidence of review, corrections and the integrated result? |
| Honesty | Are proposed features, local checks and hosted runs labelled accurately? |

---

## If You Want More

* Review whether the query slice should use **duration** or an **exclusive end date** at its interaction boundary.
* Compare the **input errors** each choice creates. Update the sketch and examples.
* **Do not** implement a second interface solely for this extension.
* A suggested solution: duration matches the current reservation input and suits "two days"; an exclusive end makes boundaries explicit but may be **misread as an inclusive last day**.
* The choice should follow a **user walkthrough**.

---

# 4.11 Questions to Think with
### Concept and diagnosis

---

## Concept Questions

1. How do a vision, an iteration goal and an implementation task differ? Use the equipment project for each.
2. Why can a console-based journey be a vertical slice even when it has no database?
3. Why is total available person-time insufficient to establish a feasible iteration plan?
4. What does a passing starter check establish, and what does it leave unproven?

---

## Diagnosis Questions

5. A team reports the availability story done because the screen says "available". Its implementation calls `reserve`, then removes the new record. Identify the violated requirement and the state evidence you would inspect.
6. A CI job compiles successfully, runs `java -cp build/classes Chapter03AcceptanceExamples || true`, then prints "all checks passed". Explain how this can report success after an assertion failure and how you would verify the correction.

---

## Guidance: Questions 1 and 2

1. The **vision** describes the officer's improved ability to make clear reservation decisions. The **iteration goal** concerns inspecting availability without changing records. A read-only operation is one **task** supporting it. A list of technical tasks alone does not express the user outcome.
2. A slice is complete **relative to its promised outcome** when input reaches the relevant behaviour and storage decision and produces an inspectable result. A **console** can support that. A database or graphical interface is needed only if the outcome requires it.

---

## Guidance: Questions 3 and 4

3. Summed hours omit **dependencies, calendar overlap, skill availability and review timing**. Four people available on different days may be unable to pair or review when needed. Check the **sequence and collaboration windows**.
4. The particular checks executed successfully against the compiled revision **in the recorded environment**. Unproven: untested cases, unspecified rules, hosted execution if only run locally, independent review, concurrency safety, user acceptance. It does **not** certify that US-02 exists.

---

## Guidance: Questions 5 and 6

5. Calling `reserve` **violates the read-only requirement** before any cleanup: a success appends a record, and eligibility can reject the request even when the item is free. Inspect **before-and-after record identifiers, borrower/item identifiers and period bounds**, not only the count.
6. `|| true` turns the failing Java command into a **successful shell list**. Remove the suppression, rerun with the deliberately wrong AC-01 expectation, and verify **nonzero exit and no final success marker**. Restore, and verify a pass.

---

# 4.12 A Different Setting
### The transfer challenge

---

## Transfer Challenge: Clinic Appointments

A small clinic wants reception staff to inspect appointment-slot availability and make bookings. It has one supplied in-memory booking routine, a draft backlog and a **four-person student team with uneven availability**.

* Create a **bounded first-iteration goal**, a **wireframe** and a **capacity-aware plan**.
* Identify **two assumptions** to revisit before real use.
* Give **one adjacency example**, and explain why equipment-lending date rules **cannot simply be copied** into a time-based domain.
* Show what the **first automated gate would establish** and what **still needs human review**.
* Use **synthetic appointment data** only.

---

## Transfer Guidance (1 of 2)

* **Goal:** let reception demonstrate an availability enquiry for **one synthetic slot** without creating or altering bookings, within one running coordinator.
* **Sketch:** practitioner or resource identifier, date, start time, duration, a Check action, and a result that **distinguishes availability from a confirmed booking**. Show the agreed time zone.
* **Assumptions to revisit:** one known synthetic resource and a **single agreed scheduling zone**; no real appointment authority, patient identity or clinical workflow.

---

## Transfer Guidance (2 of 2)

* **Boundary example:** one appointment occupies `[09:00, 09:30)` and another requests `[09:30, 10:00)`. They do **not** overlap under that interval model. A **preparation interval** could still make the second invalid, so clarify it.
* The equipment starter uses whole dates. Do not paste `LocalDate.plusDays` into a **minute-based** rule.
* **Gate evidence:** compile, run checks for the agreed booking semantics, prove assertion failure propagates.
* **Human evidence:** a walkthrough that reception understands the result and time labels; stakeholder discussion of authority and assumptions.

---

# What to Take Away, and What Comes Next
### What to carry forward

---

## Summary: A Credible Iteration

* A credible iteration connects a **bounded outcome**, a **thin journey**, a **feasible plan** and **inspectable evidence**.
* **Scope notes** expose assumptions; **wireframes** reveal interaction questions; **acceptance examples** make behaviour testable.
* **Review and automation** help the team preserve a shared baseline while learning what to build next.

---

## Summary: What Changed in the Code

* The Chapter 4 application behaviour **remains the Chapter 2 to 3 reservation version**.
* Additions: **repository organisation**, a **repeatable checking command**, a **scripted demonstration** and a **hosted-workflow template**.
* **US-02 remains planned.**

---

## Next: Chapter 5

* **Responsibilities, Extension and Substitutability.**
* Use this protected starting point to examine **reasons for change**.
* Make **small, protected design improvements**.
* Comprehensive CI/CD, deployment and integration-testing choices remain for **Chapter 13**.

---

## Sources and Further Reading

1. **Schwaber and Sutherland:** *The Scrum Guide*, November 2020.
2. **Oracle:** *The `javac` command, Java SE 17.*
3. **GitHub Docs:** *Building and testing Java with Maven* (context for CI; this starter runs a Bash gate).
4. **GitHub Actions:** `setup-java` and `checkout`.
5. **Martin:** *Agile Software Development*, 2002. **Rubin:** *Essential Scrum*, 2012.

* Full references and links are in the chapter text.
