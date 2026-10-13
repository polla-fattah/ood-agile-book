---
title: "Chapter 12: Measuring Progress, Flow and Technical Health"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 120
type: slides
layout: page
---

# Chapter 12: Measuring Progress, Flow and Technical Health
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 2)

* **12.1 What decision needs a measure?**
  * A measurement contract, and a synthetic issue history.
* **12.2 Estimation revisited**
* **12.3 Velocity and its limits**
  * Velocity versus throughput; conditional forecasts.
* **12.4 Burn-down and burn-up**
  * Reconciling scope additions and removals.
* **12.5 Lead time, cycle time, throughput and WIP**
  * And real repository evidence.

---

## Chapter Roadmap (2 of 2)

* **12.6 Technical health and metric misuse**
* **12.7 Changed requirement and impact analysis**
  * CR-12: visiting-researcher reservations.
* **12.8 AI in practice:** check the explanation, not its confidence.
* **12.9 Common mistakes**
* **12.10 Practical activity**
* **12.11 Review and transfer**
* **Summary and next chapter**
  * Chapter 13: implement CR-12 and deliver it.

---

## Learning Outcomes (1 of 2)

After this chapter, you should be able to:

1. **Define a measurement boundary** and calculate lead time, cycle time, throughput, work in progress and work-item age.
2. **Distinguish velocity from item throughput** and explain why neither ranks individual contribution.
3. **Reconcile burn-down and burn-up observations** with additions, removals and completed work.

---

## Learning Outcomes (2 of 2)

4. **Use a small body of evidence to frame a conditional forecast** and identify missing information.
5. **Evaluate a technical-health or debt claim** without confusing activity with quality or causation.
6. **Prepare acceptance examples, an impact analysis and an ordered response** to a changed requirement.

---

## Module Connection and Checkpoint

* Supports **LO5 and LO6**. Required reading: the descriptor's Martin (2002) planning review; recommended: selected chapters of *Accelerate*.
* The required practical activity includes **repository-metrics analysis**.
* The requirement change is **introduced in this chapter**, **implemented and verified in Chapter 13** (Milestone 4), and **evaluated during handover in Chapter 14**.
* The module leader releases your team's assessed variant. **The book's worked change does not replace it.**
* **Checkpoint:** Chapter 11's verified Java project. This chapter adds an isolated metrics exercise and planning records. **It does not implement the feature.**

---

## Reading Route

* **Core:** 12.1 to 12.7, with the measurement contract and the worked change specification.
* **Minimum lab:** reproduce the synthetic calculations; inspect **actual repository evidence**; challenge the AI summary; **preserve the pre-change checkpoint** with a change-impact note.
* **Working knowledge:** the supplied Java calculator and the repository extraction method.
* **Optional:** richer visualisation, larger cohorts, probabilistic forecasting (after obtaining suitable data).

---

## Opening Problem: The Line Went Up

* The lending team has completed several changes, yet **the remaining-work line has risen**.
* One item spent **two days waiting for a directory decision**. Another was **removed from scope**.
* A team member says **more commits prove the team is faster**. An AI summary says **the blocked item proves the architecture is poor**.
* The history is **synthetic teaching data**, not recovered history and **not evidence about a real student team**.

---

## And a New Request

* Visiting researchers should be able to reserve selected equipment **after sponsor approval**, with a **shorter loan limit**.
* Can the team finish it next iteration? **Which existing rules will it affect?** What evidence would justify starting immediately rather than resolving an uncertainty first?
* **A metric cannot make these decisions.** It can make part of the situation visible, if its **unit, boundary and limitations are clear**.

---

# 12.1 What Decision Needs a Measure?
### A contract before a number

---

## Begin With a Question That Could Change an Action

* "Collect more metrics" is a weak objective.
* **"Should we finish the two open items before pulling the sponsor-approval story?"** points to a decision.
* We need: which items remain, **how long they have been open**, whether they are **blocked**, how comparable they are with past work. A commit count cannot answer all that.

---

## State the Contract for Each Measure

* The **question**, **population**, **unit**, **time window**, **intended response**.
* Keep a note of the **source** and **extraction date**.
* If a number cannot influence a decision or test an assumption, **consider whether collecting it is useful**.
* For a small student project, **a clear table often teaches more than a dashboard of unexplained indicators**.
* Compare **definitions** before comparing numbers: other teams may choose different boundaries.

---

## The Measurement Contract (1 of 3)

| Field | Definition for the synthetic history |
|---|---|
| Unit | One uniquely identified backlog item; IDs A to H |
| Accepted | Item admitted to the tracked scope |
| Started | First transition into implementation |
| Done | Accepted against the team's Definition of Done, including required checks and review |
| Removed | Explicitly taken out of scope without completion |

---

## The Measurement Contract (2 of 3)

| Field | Definition for the synthetic history |
|---|---|
| Reporting interval | `[2026-10-01T00:00:00Z, 2026-10-11T00:00:00Z)` |
| Duration | Elapsed 24-hour days; waiting and weekends remain included |
| Snapshot | State immediately after events at the stated timestamp |
| Completion cohort | Items whose Done event falls within the reporting interval |

---

## The Measurement Contract (3 of 3)

| Field | Definition for the synthetic history |
|---|---|
| Exclusions | No reopened, split, merged or re-estimated items in this small fixture |

* The **half-open interval** includes completions at the starting instant and excludes the ending instant: adjacent windows **cannot count the same completion twice**.
* A **snapshot** is different: a completion exactly at its timestamp has **already left** work in progress.
* These are **reporting choices, not new reservation-period rules**.

---

## The Complete Issue History (1 of 2)

| ID | Illustrative work | Points | Accepted | Started | Done | Removed |
|---|---|---:|---:|---:|---:|---:|
| A | Reservation boundary examples | 3 | 01 | 01 | 03 | - |
| B | Directory mapping clarification | 5 | 01 | 02 | 06 | - |
| C | Confirmation wording | 2 | 01 | 03 | 04 | - |
| D | Command replay protection examples | 3 | 01 | 05 | 08 | - |

---

## The Complete Issue History (2 of 2)

| ID | Illustrative work | Points | Accepted | Started | Done | Removed |
|---|---|---:|---:|---:|---:|---:|
| E | Report failure investigation | 5 | 01 | 07 | - | - |
| F | Optional export format | 2 | 01 | - | - | 08 |
| G | Snapshot consistency checks | 3 | 04 | 06 | 10 | - |
| H | Review-notes improvement | 2 | 06 | 08 | - | - |

* Every date is October 2026 at 00:00 UTC. A **dash means the event has not occurred**, not a duration of zero.

---

## Reading the History as a Timeline

<!--svg:ch12-timeline-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 345" role="img" aria-label="Timeline of the eight synthetic items over 1 to 11 October: waiting before start, active time, B&#x27;s two-day block, F&#x27;s removal on day 8, and E and H still open at the end." style="display:block;width:100%;height:calc(var(--u) * 34.50);margin:0 auto">
<defs><marker id="ch12-timeline-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch12-timeline-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch12-timeline-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch12-timeline-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch12-timeline-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<text x="150.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">01</text>
<path d="M150.0,32.0 L150.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="210.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">02</text>
<path d="M210.0,32.0 L210.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="270.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">03</text>
<path d="M270.0,32.0 L270.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="330.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">04</text>
<path d="M330.0,32.0 L330.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="390.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">05</text>
<path d="M390.0,32.0 L390.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="450.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">06</text>
<path d="M450.0,32.0 L450.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="510.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">07</text>
<path d="M510.0,32.0 L510.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="570.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">08</text>
<path d="M570.0,32.0 L570.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="630.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">09</text>
<path d="M630.0,32.0 L630.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="690.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">10</text>
<path d="M690.0,32.0 L690.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="750.0" y="24.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">11</text>
<path d="M750.0,32.0 L750.0,292.0" fill="none" stroke="#c3cfdd" stroke-width="1.2"/>
<text x="12.0" y="61.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="start">A</text>
<text x="38.0" y="61.0" font-size="14" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="start">3 pts</text>
<rect x="150.0" y="49.0" width="120.0" height="18.0" rx="3" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="12.0" y="92.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="start">B</text>
<text x="38.0" y="92.0" font-size="14" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="start">5 pts</text>
<rect x="150.0" y="80.0" width="60.0" height="18.0" rx="3" fill="#f5f7fa" stroke="#46586d" stroke-width="1.4" stroke-dasharray="5 4"/>
<rect x="210.0" y="80.0" width="240.0" height="18.0" rx="3" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<rect x="270.0" y="84.0" width="120.0" height="10.0" rx="2" fill="#b4762e" stroke="#b4762e" stroke-width="1"/>
<text x="12.0" y="123.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="start">C</text>
<text x="38.0" y="123.0" font-size="14" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="start">2 pts</text>
<rect x="150.0" y="111.0" width="120.0" height="18.0" rx="3" fill="#f5f7fa" stroke="#46586d" stroke-width="1.4" stroke-dasharray="5 4"/>
<rect x="270.0" y="111.0" width="60.0" height="18.0" rx="3" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="12.0" y="154.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="start">D</text>
<text x="38.0" y="154.0" font-size="14" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="start">3 pts</text>
<rect x="150.0" y="142.0" width="240.0" height="18.0" rx="3" fill="#f5f7fa" stroke="#46586d" stroke-width="1.4" stroke-dasharray="5 4"/>
<rect x="390.0" y="142.0" width="180.0" height="18.0" rx="3" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="12.0" y="185.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="start">E</text>
<text x="38.0" y="185.0" font-size="14" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="start">5 pts</text>
<rect x="150.0" y="173.0" width="360.0" height="18.0" rx="3" fill="#f5f7fa" stroke="#46586d" stroke-width="1.4" stroke-dasharray="5 4"/>
<rect x="510.0" y="173.0" width="240.0" height="18.0" rx="3" fill="#7fa7cc" stroke="#1d588c" stroke-width="1.4"/>
<text x="758.0" y="187.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#b4762e" text-anchor="start" font-style="italic">open</text>
<text x="12.0" y="216.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="start">F</text>
<text x="38.0" y="216.0" font-size="14" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="start">2 pts</text>
<rect x="150.0" y="204.0" width="420.0" height="18.0" rx="3" fill="#f5f7fa" stroke="#46586d" stroke-width="1.4" stroke-dasharray="5 4"/>
<text x="584.0" y="220.0" font-size="22" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="middle">×</text>
<text x="600.0" y="218.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="start" font-style="italic">removed</text>
<text x="12.0" y="247.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="start">G</text>
<text x="38.0" y="247.0" font-size="14" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="start">3 pts</text>
<rect x="330.0" y="235.0" width="120.0" height="18.0" rx="3" fill="#f5f7fa" stroke="#46586d" stroke-width="1.4" stroke-dasharray="5 4"/>
<rect x="450.0" y="235.0" width="240.0" height="18.0" rx="3" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="12.0" y="278.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="start">H</text>
<text x="38.0" y="278.0" font-size="14" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="start">2 pts</text>
<rect x="450.0" y="266.0" width="120.0" height="18.0" rx="3" fill="#f5f7fa" stroke="#46586d" stroke-width="1.4" stroke-dasharray="5 4"/>
<rect x="570.0" y="266.0" width="180.0" height="18.0" rx="3" fill="#7fa7cc" stroke="#1d588c" stroke-width="1.4"/>
<text x="758.0" y="280.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#b4762e" text-anchor="start" font-style="italic">open</text>
<rect x="150.0" y="306.0" width="22.0" height="14.0" rx="3" fill="#f5f7fa" stroke="#46586d" stroke-width="1.4" stroke-dasharray="4 3"/>
<text x="178.0" y="318.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">accepted, waiting</text>
<rect x="330.0" y="306.0" width="22.0" height="14.0" rx="3" fill="#1d588c" stroke="#1d588c" stroke-width="1"/>
<text x="358.0" y="318.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">started to done</text>
<rect x="510.0" y="306.0" width="22.0" height="14.0" rx="3" fill="#b4762e" stroke="#b4762e" stroke-width="1"/>
<text x="538.0" y="318.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">B blocked, 03 to 05</text>
</svg>
</div>
<!--/svg-->

---

## Context and Caution

* **B** is recorded as **blocked from 03 to 05 October** while a mapping question is answered: **supplied as synthetic context**, not inferred from inactivity in Git.
* **G and H** are scope additions; **F** is a removal.
* The labels describe an imagined iteration; they do not assert that earlier files were created on these dates.

---

## Data and Interpretation Are Different

* A **sound observation:** "B spent four elapsed days between Started and Done."
* A **possible explanation:** "waiting for the mapping decision contributed to B's delay."
* A **stronger claim** such as "the directory adapter caused all delays" **needs evidence this table does not contain**.

---

# 12.2 Estimation Revisited
### A judgement, not a measurement

---

## What an Estimate Is

* A **planning judgement made with incomplete knowledge**.
* Useful when it **exposes uncertainty** or supports a choice between smaller and larger slices.
* Misleading when treated as **a measured physical property of the work**.
* The points are **a local relative scale**: not hours, not an exchange rate between teams.

---

## Points Are Not Days

* B's five points and C's two express the team's **relative judgement before delivery**.
* B taking four days does **not** establish that one point equals 0.8 days: the duration **includes waiting**, and another item has different risks.
* **Do not rewrite old estimates** after seeing durations to make history look consistent. If a team genuinely revises one, **preserve the earlier value and record the event**.

---

## Split by Useful Behaviour

* For the approval change, start with a concrete example: **a recognised visitor requests CAM1 for two days with matching approval**.
* Compare that slice with the **failure case where the approval register is unavailable**: shared code, **a distinct delivery risk**.
* Splitting by useful behaviour makes uncertainty easier to discuss than "write classes, write tests, write documentation".

---

## When Estimates Differ

* Ask **what each person assumed**. One may expect an existing approval file; another a new sponsor-facing website.
* The solution is to **clarify scope, not average incompatible assumptions**. The worked change uses a small local approval register and excludes an approval-management interface.
* **Capacity** matters: a week with a midterm or an absent teammate is not interchangeable with an earlier week. Record the constraint **without turning people into point-producing units**.
* A time-bounded investigation should have an **output**: a sample approval record and a checked parsing/failure contract.

---

# 12.3 Velocity and Its Limits
### Two different units

---

## Velocity and Throughput

* **Velocity** (for a team using points): the sum of estimates of items completed within a defined iteration. A, B, C, D, G: `3 + 5 + 2 + 3 + 3 = 16 points`.
* **Throughput** counts completed **items**: **five items** in this ten-day interval.
* **Sixteen points and five items describe the same completions with different units.** Calling 16 "throughput" would confuse the comparison.

---

## What Does Not Count

* **E and H** contribute **no completed points yet**. Calling E "80% done" does not add four points.
* **F** contributes nothing: removing an optional item can be a sensible scope decision **without becoming delivery**.
* Discussing progress on E is fine, but is **not a reason to redefine Done**.

---

## Velocity Has Limits

* It can help **one team** inspect its own planning history when the **estimation scale, Definition of Done and work mix are consistent enough**.
* It **cannot fairly rank teams** that estimate differently.
* It **cannot reveal an individual's contribution**: reviewing a colleague's difficult change may raise team completion with no story or commit under the reviewer's name.
* A burn chart is **not a substitute for inspecting actual results**.

---

## Make Forecasts Conditional

* Two remaining items totalling seven points: `7 / 16 = 0.4375` iterations.
* That arithmetic does **not** establish a delivery date. It assumes **comparable work, capacity, dependencies, scope and completion behaviour**.
* One observed iteration says little about **variation**; unfinished work may be exactly **the work with unresolved risk**.

---

## A Defensible Planning Statement

> We have completed five items in ten elapsed days in this synthetic example. E and H remain open. We will inspect their blockers and size the approval slice before committing to a date.

* If later comparable history supports two to three items per five-day window, two remaining items **might fit one window under unchanged conditions**: a **scenario, not a calibrated probability or guarantee**.
* Preserve forecasts as **dated predictions** and compare them with outcomes. Do not fit a confident percentile to a tiny classroom sample.

---

# 12.4 Burn-Down and Burn-Up
### Scope moves too

---

## Definitions

* A **burn-down** shows **remaining work**.
* A **burn-up** shows **completed work**, normally alongside the **current scope total**.
* With points fixed and removed items never Done: **remaining = current scope − completed**.
* Initial scope **20** points. Adding G and H: **25**. Removing F: **23**. At the end **16 complete, 7 remain**.

---

## The Daily Snapshots (1 of 2)

| Snapshot day | Scope points | Completed points | Remaining points | WIP items |
|---|---:|---:|---:|---:|
| 01 | 20 | 0 | 20 | 1 |
| 02 | 20 | 0 | 20 | 2 |
| 03 | 20 | 3 | 17 | 2 |
| 04 | 23 | 5 | 18 | 1 |
| 05 | 23 | 5 | 18 | 2 |
| 06 | 25 | 10 | 15 | 2 |

---

## The Daily Snapshots (2 of 2)

| Snapshot day | Scope points | Completed points | Remaining points | WIP items |
|---|---:|---:|---:|---:|
| 07 | 25 | 10 | 15 | 3 |
| 08 | 23 | 13 | 10 | 3 |
| 09 | 23 | 13 | 10 | 3 |
| 10 | 23 | 16 | 7 | 2 |
| 11 | 23 | 16 | 7 | 2 |

---

## The Burn-Up

<!--svg:ch12-burnup-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 335" role="img" aria-label="Burn-up of the synthetic iteration, daily from 1 to 11 October: scope points 20, 20, 20, 23, 23, 25, 25, 23, 23, 23, 23 and completed points 0, 0, 3, 5, 5, 10, 10, 13, 13, 16, 16." style="display:block;width:100%;height:calc(var(--u) * 33.50);margin:0 auto">
<defs><marker id="ch12-burnup-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch12-burnup-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch12-burnup-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch12-burnup-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch12-burnup-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<path d="M80.0,285.0 L800.0,285.0" fill="none" stroke="#c3cfdd" stroke-width="1.3"/>
<text x="70.0" y="290.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">0</text>
<path d="M80.0,234.0 L800.0,234.0" fill="none" stroke="#c3cfdd" stroke-width="1.3"/>
<text x="70.0" y="239.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">5</text>
<path d="M80.0,183.0 L800.0,183.0" fill="none" stroke="#c3cfdd" stroke-width="1.3"/>
<text x="70.0" y="188.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">10</text>
<path d="M80.0,132.0 L800.0,132.0" fill="none" stroke="#c3cfdd" stroke-width="1.3"/>
<text x="70.0" y="137.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">15</text>
<path d="M80.0,81.0 L800.0,81.0" fill="none" stroke="#c3cfdd" stroke-width="1.3"/>
<text x="70.0" y="86.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">20</text>
<path d="M80.0,30.0 L800.0,30.0" fill="none" stroke="#c3cfdd" stroke-width="1.3"/>
<text x="70.0" y="35.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">25</text>
<text x="80.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">01</text>
<text x="152.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">02</text>
<text x="224.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">03</text>
<text x="296.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">04</text>
<text x="368.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">05</text>
<text x="440.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">06</text>
<text x="512.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">07</text>
<text x="584.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">08</text>
<text x="656.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">09</text>
<text x="728.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">10</text>
<text x="800.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">11</text>
<path d="M80.0,81.0 L152.0,81.0 L224.0,81.0 L296.0,50.4 L368.0,50.4 L440.0,30.0 L512.0,30.0 L584.0,50.4 L656.0,50.4 L728.0,50.4 L800.0,50.4" fill="none" stroke="#b4762e" stroke-width="3.4"/>
<path d="M80.0,285.0 L152.0,285.0 L224.0,254.4 L296.0,234.0 L368.0,234.0 L440.0,183.0 L512.0,183.0 L584.0,152.4 L656.0,152.4 L728.0,121.8 L800.0,121.8" fill="none" stroke="#1d588c" stroke-width="3.4"/>
<circle cx="80.0" cy="81.0" r="4.5" fill="#b4762e"/>
<circle cx="152.0" cy="81.0" r="4.5" fill="#b4762e"/>
<circle cx="224.0" cy="81.0" r="4.5" fill="#b4762e"/>
<circle cx="296.0" cy="50.4" r="4.5" fill="#b4762e"/>
<circle cx="368.0" cy="50.4" r="4.5" fill="#b4762e"/>
<circle cx="440.0" cy="30.0" r="4.5" fill="#b4762e"/>
<circle cx="512.0" cy="30.0" r="4.5" fill="#b4762e"/>
<circle cx="584.0" cy="50.4" r="4.5" fill="#b4762e"/>
<circle cx="656.0" cy="50.4" r="4.5" fill="#b4762e"/>
<circle cx="728.0" cy="50.4" r="4.5" fill="#b4762e"/>
<circle cx="800.0" cy="50.4" r="4.5" fill="#b4762e"/>
<circle cx="80.0" cy="285.0" r="4.5" fill="#1d588c"/>
<circle cx="152.0" cy="285.0" r="4.5" fill="#1d588c"/>
<circle cx="224.0" cy="254.4" r="4.5" fill="#1d588c"/>
<circle cx="296.0" cy="234.0" r="4.5" fill="#1d588c"/>
<circle cx="368.0" cy="234.0" r="4.5" fill="#1d588c"/>
<circle cx="440.0" cy="183.0" r="4.5" fill="#1d588c"/>
<circle cx="512.0" cy="183.0" r="4.5" fill="#1d588c"/>
<circle cx="584.0" cy="152.4" r="4.5" fill="#1d588c"/>
<circle cx="656.0" cy="152.4" r="4.5" fill="#1d588c"/>
<circle cx="728.0" cy="121.8" r="4.5" fill="#1d588c"/>
<circle cx="800.0" cy="121.8" r="4.5" fill="#1d588c"/>
<text x="296.0" y="36.4" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="middle" font-style="italic">G added</text>
<text x="440.0" y="16.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="middle" font-style="italic">H added</text>
<text x="588.0" y="36.4" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="start" font-style="italic">F removed</text>
<text x="790.0" y="74.4" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="end">scope 23</text>
<text x="790.0" y="145.8" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#1d588c" text-anchor="end">done 16</text>
<text x="806.0" y="86.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">7 left</text>
<text x="440.0" y="328.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">October 2026 snapshot day</text>
</svg>
</div>
<!--/svg-->

---

## Read the Events, Not Only the Line

* **Day 04:** the remaining line **rises from 17 to 18** despite C's two-point completion: **three points arrived as G**.
* **Day 08:** it **falls by five**, but only **three came from D's completion**; **two came from removing F**.
* Without the scope events, both changes are **easy to misread**.
* The scope history must stay visible if we want to explain the line.

---

## Ideal Lines Are Not Evidence

* An **ideal diagonal burn-down** is a reference for a fixed initial scope. It is **not** evidence that real work should finish in equal daily increments.
* Review, integration and acceptance produce **uneven completions**.
* **Do not move Done timestamps** to make a curve attractive.
* Ask whether the team can **explain the change** and whether the remaining work still serves the goal.

---

# 12.5 Lead Time, Cycle Time, Throughput and WIP
### The completion cohort

---

## Definitions for This History

* **Lead time:** Accepted to Done.
* **Cycle time:** Started to Done.
* The difference is **the recorded wait before starting**.
* Neither measures **hands-on effort**.
* The calculations use **the completion cohort**, not every row in the backlog.

---

## The Finished Items

| Finished item | Lead days | Cycle days | Wait before start |
|---|---:|---:|---:|
| A | 2 | 2 | 0 |
| B | 5 | 4 | 1 |
| C | 3 | 1 | 2 |
| D | 7 | 3 | 4 |
| G | 6 | 4 | 2 |
| **Mean** | **4.6** | **2.8** | **1.8** |

---

## The Arithmetic

* Lead: `23 / 5 = 4.6` elapsed days. Cycle: `14 / 5 = 2.8`.
* Median cycle: sort `1, 2, 3, 4, 4` and take the middle: **three days**.
* Wait: `9 / 5 = 1.8`, consistent with `4.6 − 2.8`.
* **B's two blocked days stay inside its four-day cycle.** Subtracting them answers a different question (mean 2.4) and still **would not establish active coding time**.

---

## Open Items Have Ages

* At the final snapshot **E and H** are started but unfinished: **WIP is two**.
* Their **ages are four and three days**. They have **no completed cycle time yet**.
* Excluding them from the mean is correct for a completed-item statistic, but **forgetting them in the interpretation creates a misleadingly favourable account**.
* Report **the completed cohort alongside open-item age**.

---

## Throughput by Window

* `[01, 06)`: **two** items, A and C.
* `[06, 11)`: **three**, B, D and G.
* **B belongs only to the second window**, because it completes exactly at that window's starting instant.
* These are five-day windows, **not claims about official Sprints**.
* Whole interval: **five items in ten days**, or 0.5 per elapsed day.

---

## Equal Throughput, Different Delay

* Two five-day periods, each finishing two items.
* In one, both started **one day** before completion; in the other, both started **seven days** before and were carried in.
* **Throughput is two in both**; completed cycle times are **one and seven days**.
* Counting completions **does not reveal how long recipients waited**.

---

## Use Actual Repository Events Carefully

* The lab supplements the fixture with **real issue or PR history**, using **Repository Metrics Method RM-12 v1.0**, exact timestamps and the supplied Java 17 calculator.
* In the PR route: **Started = PR opened; Done = merged; unit = a PR**. Call the result **PR open-to-merge elapsed time**.
* It is **not** issue cycle time, developer effort, deployment lead time or time since coding began.

---

## Choose the Population Before the Result

* For throughput, **enumerate every qualifying merge** in the chosen repository, target branch and interval, **including all result pages**.
* **A convenient sample of five PRs supports a sample-duration description**, not the repository's throughput.
* Include PRs **already open at the start**; record **open PRs at the final snapshot** if reporting WIP.
* State the **inclusion rule** for bots and dependency updates.

---

## Keep Provenance

* Keep **URLs or IDs, original timestamps and the extraction date**.
* Local Git can cross-check commit identity, but **author and committer dates are not substitutes** for PR-open or server merge events; squashing and rebasing change the relationship.
* If only Git history is available, **report what it actually measures** and obtain real PR/issue timestamps.
* **Synthetic rehearsal alone does not complete this part of the lab.**

---

## The Calculator

```bash
mkdir -p out
javac --release 17 -d out FlowMetrics.java FlowMetricsChecks.java
java -cp out FlowMetricsChecks
java -cp out FlowMetrics issues.tsv 2026-10-01T00:00:00Z 2026-10-11T00:00:00Z --scope
```

```text
Completions in [from, until): 5
Completed points: 16
Mean lead days: 4.60
Mean cycle days: 2.80
Median cycle days: 3.00
WIP at until (after events at that instant): 2
Age E: 4.00 days
Age H: 3.00 days
```

---

## RM-12 Route A: PR Open-to-Merge Duration

1. **Choose a source and rule:** repository URL, target branch, fixed UTC interval, extraction timestamp, inclusion rule. Select the **first five qualifying merged PRs** by merge time and then PR number.
2. **Keep provenance** for each PR: URL or ID, opened timestamp, merged timestamp, branch. **Do not guess midnight** if the UI shows only relative dates.
3. **Map the data:** `accepted` and `started` both to the PR opened instant; `done` to the merged instant; leave `points` and `removed` blank.
4. **Calculate**, then **manually verify the longest duration**.
5. **Interpret and review**: coding may begin **before** a PR opens; draft and review waiting stay in.

---

## RM-12 Route B: Throughput and Open Work

* Enumerate **all** qualifying merged PRs in `[from, until)`; check pagination and filters; record counts and exclusions.
* **Do not filter by opened date**: that loses carried-in work.
* For WIP at `until`, also include **every qualifying PR opened by then that had neither merged nor closed**. A PR merged after `until` **was still open at `until`**.
* A PR **closed without merging** maps to `removed`, not `done`.
* Only a **complete population** supports full-window claims.

---

# 12.6 Technical Health and Metric Misuse
### Evidence, not activity

---

## Combine a Risk, Evidence and a Response

* "There are 159 passing tests in the Chapter 11 checkpoint" records **a build result**.
* It does **not** say every rule is correct, every important boundary has a test, or more tests would produce a better design.
* Chapter 11 supports **one narrow claim**: the selected tests detect a deliberately changed equality boundary.
* A high **line-coverage** percentage can identify unexecuted areas but **cannot tell whether assertions distinguish correct from incorrect outcomes**.

---

## Debt Needs an Expected Future Cost

* The report's duplicated selection rule had a **plausible maintenance cost**; the refactoring removed the duplication.
* **We have not measured** hours saved or production defects avoided.
* The sequential snapshot join may matter if concurrency enters scope, but **a feature deliberately excluded from a teaching application is not automatically debt**.
* Use the debt idea to examine **why a design decision was made**, not to label all untidy code alike.

---

## Claims and Cautious Responses (1 of 2)

| Claim | Evidence to seek | Cautious response |
|---|---|---|
| Approval changes will touch many unrelated classes | Trace actual category, directory, wiring and reservation references | Review the boundary before estimating |
| Reports are unreliable | Reproduce a specific wrong or unavailable report | Distinguish SD-11 policy uncertainty from an implementation failure |

---

## Claims and Cautious Responses (2 of 2)

| Claim | Evidence to seek | Cautious response |
|---|---|---|
| Builds are slowing feedback | Timed comparable builds, environment, wait causes | Try one targeted improvement and observe later runs |
| A package is difficult to change | Dependency evidence and affected responsibilities | Refer to Chapter 10; **do not use instability as a quality score** |

---

## Goodhart's Law

* **Pressure to maximise a proxy can weaken its connection to the goal.**
* A target for **commit counts** can encourage unnecessary splitting; a target for **velocity** can encourage inflated estimates.
* Neither improves the borrower's experience by itself.
* Research on developer productivity warns against reducing it to **a single activity measure**.

---

## Use Measures for Learning

* **Team learning and system improvement, not individual rankings.**
* A review, a careful deletion or help given to another person may be valuable **without increasing the chosen count**.
* Pair numbers with **a short account of what happened**.
* **Investigate suspicious numbers without assuming misconduct**, and do not present a tiny correlation as a causal explanation.

---

# 12.7 Changed Requirement and Impact Analysis
### CR-12: visiting-researcher reservations

---

## From Metrics to a Changed Requirement

* The first six sections taught how to **read evidence** about a team's work.
* Now the **same habits** go to a new request: say what it must do, **what it touches** and **what evidence will show it works**.
* It is the visiting-researcher change from the opening problem: **Chapter 13 implements it and Chapter 14 reviews it**.

---

## The Book Exercise Contract

> A recognised visiting researcher may request CAM1 or CAM2 for one to three calendar days when a trusted sponsor-approval record matches that borrower, item and exact loan period and is still valid at request time. Missing, rejected, mismatched, expired or unavailable approval must not create a reservation or send a confirmation. Student and staff behaviour must remain unchanged.

---

## What CR-12 Is and Is Not

* A **precise book exercise**, chosen for teaching. **Not an approved institutional policy.** Teams apply their own released requirement variant.
* Approval comes from a **local read-only data register**, not a sponsor website. In Chapter 13 it becomes **a genuine file-reading boundary**, tested with temporary files as well as doubles.
* **Training a model, predicting trust and calling a live approval service are outside the exercise.**
* It gives the project another concrete contract and failure boundary.

---

## Trace the Change Through the Design

* `BorrowerCategory` has STUDENT and STAFF; the directory knows `S` and `T`; the coordinator **requires a policy for every enum value**.
* Adding a category affects **more than one enum**: directory mapping, composition, exhaustive test fixtures and the visitor path **must agree**.
* `BorrowingPolicy.mayRequest(count, days)` answers **only count and duration**: no identity, item, approval or clock.
* Passing approval data through **hidden global state** would defeat that contract.

---

## An Inherited Convention to Preserve

* The coordinator counts **every retained reservation** for a borrower, despite the variable name `activeCount`. **Returning a loan does not remove its reservation.**
* CR-12 **preserves** this convention. The companion records it as a separate question, **SD-12**.
* **Do not silently replace it** with an active-loan count while adding visitors.

---

## Planned Impact (1 of 2)

| Area | Planned impact | Evidence needed in Chapter 13 |
|---|---|---|
| Borrower and directory | Add a visitor category and explicit external mapping | Known visitor, unknown code and existing category cases |
| Request orchestration | Validate a matching approval before a visitor reservation | Success; denied, expired, mismatched and unavailable outcomes |
| Data boundary | Parse the read-only approval register | Real temporary-file parsing and failure checks |

---

## Planned Impact (2 of 2)

| Area | Planned impact | Evidence needed in Chapter 13 |
|---|---|---|
| Policies and wiring | Add the three-day limit and all required collaborators | Boundary tests and composition that includes every category |
| Existing reservation, loan and report behaviour | Retain old results and SD-11 status | Existing regression suite plus targeted old-path examples |
| Delivery configuration | One visitor-enablement flag | Both settings, failure behaviour and removal plan |

---

## Rejection vs. Operational Failure

* A **missing approval is an expected rejection**.
* An **unreadable or malformed register is an operational failure**.
* Both prevent a new visitor reservation, but the response **should not falsely say a sponsor rejected something when no valid decision could be read**.
* Keep these outcomes **visible in the application contract**.

---

## The Behaviour and Data Decisions (1 of 3)

| ID | Book contract |
|---|---|
| CR12-1 | A recognised `VISITOR` category; legacy directory code `V` maps to it; existing `S`/`T`, inactive and unknown-code behaviour stays; **unknown codes never default to STUDENT** |
| CR12-2 | Visitors may request only **CAM1 or CAM2**, for **one, two or three calendar days**; existing half-open period; zero, negative or four or more days rejected |
| CR12-3 | Reuse the student count limit: **fewer than three retained reservations** (the existing convention) |

---

## The Behaviour and Data Decisions (2 of 3)

| ID | Book contract |
|---|---|
| CR12-4 | One matching trusted approval for the **exact tuple (borrowerId, itemId, start, endExclusive)**, nonblank sponsor, status APPROVED |
| CR12-5 | One request-time instant from an injected `Clock`; valid when `validFrom <= now < validUntil`; **equality at expiry is invalid** |
| CR12-6 | Missing match, DENIED, or out-of-window: **expected rejection**; no reservation, no confirmation |
| CR12-7 | Unreadable register, malformed row, duplicate key, unknown status, invalid interval: **operational failure**, distinguishable from sponsor rejection; **no fallback approval** |

---

## The Behaviour and Data Decisions (3 of 3)

| ID | Book contract |
|---|---|
| CR12-8 | Once approval and existing checks succeed, create the reservation with existing confirmation behaviour; an expected notification failure leaves the reservation in place |
| CR12-9 | One flag `visitingResearchersEnabled`, **default false**; disabled visitor requests are rejected **without reading the register**; student and staff requests never need approval |
| CR12-10 | Approval checked **at reservation time only**; later expiry or disabling does not cancel an existing reservation |

* The category-taking entry points are **trusted teaching APIs, not authentication**.

---

## The Approval Register

```text
borrowerId  itemId  start  endExclusive  sponsorId  status  validFrom  validUntil
V1  CAM1  2026-10-20  2026-10-22  S1  APPROVED  2026-10-18T00:00:00Z  2026-10-20T00:00:00Z
```

* A local UTF-8 **TSV with eight columns**, tab-separated. Status exactly APPROVED or DENIED.
* Require `start < endExclusive` and `validFrom < validUntil`. **A malformed register is rejected as a whole**; do not silently skip bad rows. Request keys unique per read.
* At `2026-10-19T12:00:00Z` this approves V1's CAM1 request; at `2026-10-20T00:00:00Z` it **has expired**.

---

## The Acceptance Matrix (1 of 3)

| Example | Input difference | Expected observation |
|---|---|---|
| AC1 | CAM1, two days, matching approval valid at request time | One reservation; existing confirmation; one notice |
| AC2 | CAM2, three days, its own matching record | Allowed; upper boundary |
| AC3 | Four days | Reject; no state or notice change |
| AC4 | Zero or negative days | Reject; no state or notice change |
| AC5 | MIC1 with matching approval | Reject: outside the visitor allowlist |
| AC6 | Missing approval or DENIED | Expected rejection; no change |

---

## The Acceptance Matrix (2 of 3)

| Example | Input difference | Expected observation |
|---|---|---|
| AC7 | Approval for V2, CAM2 or a different end date | Does not authorise this tuple |
| AC8 | `now == validFrom` | Valid if all else holds |
| AC9 | `now == validUntil`, or before `validFrom` | Rejected |
| AC10 | Unreadable file, malformed row or duplicate key | **Operational failure**; no change |
| AC11 | Three retained reservations exist | Reject the count limit even if loans were returned |
| AC12 | Visitor feature disabled | Explicit disabled result; **approval source not called** |

---

## The Acceptance Matrix (3 of 3)

| Example | Input difference | Expected observation |
|---|---|---|
| AC13 | Existing student or staff request, either flag setting | Existing behaviour; approval source not called |
| AC14 | Approved item overlaps an existing reservation | Existing availability rejection |
| AC15 | Valid visitor, expected notification failure | Reservation retained |
| AC16 | Reservation created, then approval expires or flag turns off | Checkout and return stay available |
| AC17 | Unknown directory code or inactive visitor | Existing semantics; never default to student |
| AC18 | Report generated after a visitor loan exists | Existing mapping and SD-11 retained |

---

## Plan the Smallest Checked Response

* **Preserve the passing Chapter 11 checkpoint** first.
* Record the requirement, accepted examples, assumptions and affected files.
* Order: a **thin valid visitor path**; the **genuine register boundary and failure paths**; **old-path regression**; delivery and demo evidence.
* Each item gets **an observable exit condition**. Resolve the approval-record format early. **Do not copy the synthetic history's points** onto these tasks.

---

## The Ordered Backlog (1 of 2)

| ID | Ordered work | Exit evidence |
|---|---|---|
| C12-1 | Preserve baseline and confirm CR12/SD12 examples | Passing baseline; retained revision; reviewed contract |
| C12-2 | Add recognised visitor path, policies and explicit wiring | Valid visitor with a controlled approval source; old categories unchanged |
| C12-3 | Implement and test the actual approval-file adapter | Temporary-file success and malformed, missing, duplicate failures; **no mock replacing the reader under test** |

---

## The Ordered Backlog (2 of 2)

| ID | Ordered work | Exit evidence |
|---|---|---|
| C12-4 | Complete matching, time and failure protection | AC boundary and operational-failure evidence |
| C12-5 | One flag; integrate CLI and demo | Both settings; old path; existing reservations usable after disable |
| C12-6 | Full regression, real boundary checks, delivery workflow | Observed gate; repeatable demo; retrospective |

* **C12-2 to C12-6 are planned, not implemented.** A design note is not a delivered capability, and **a green pre-change build is not evidence that the new rule works**.

---

## Preserve the Pre-Change Checkpoint

```text
Baseline: Chapter 11 cumulative project
Source revision or complete-copy location:
Uncommitted/untracked source accounted for:
Java and Maven versions:
Command and actual result:
SD-11: due-today inclusion preserved; policy unresolved
SD-12: retained-reservation count preserved; policy unresolved
CR-12: specified; implementation pending
Reviewer or explicitly labelled solo review:
```

* A commit ID suffices **only if the intended files are committed**; otherwise keep a complete copy such as `pre-change-ch12`.

---

# 12.8 AI in Practice: Check the Explanation
### Not its confidence

---

## The Task

* **Input:** the eight-row history, the blocked interval, the measurement contract and the chart table.
* **Task:** verify **every arithmetic or causal claim independently**.
* **Permitted scope:** explain the data and identify questions; **do not change timestamps, estimates or requirements to fit the explanation.**
* Mark each claim **supported, contradicted or not established**.

---

## The Fixture

**Author-written fictional AI output.**

> The team delivered six items and 18 points because F left the backlog. Mean cycle time is two days after subtracting B's blocked days. The rise on 4 October proves productivity declined, while the fall on 8 October proves five points were delivered. The legacy architecture caused the waiting. At 16 points per iteration, the remaining seven points will definitely finish in 0.44 iterations. Rank team members by commits to remove the bottleneck.

---

## Verdicts (1 of 2)

| Candidate claim | Judgement |
|---|---|
| Six items and 18 points delivered | **Contradicted**: F is removed, not Done. Five items and 16 points |
| Mean cycle is two after subtracting blocking | **Contradicted**: the defined mean is 2.8; subtracting would give 2.4, a different measure |
| The day 04 rise proves productivity declined | **Not established**: G adds three while C completes two; the line rises by one |
| The day 08 fall proves five points delivered | **Contradicted**: D completes three; F removes two |

---

## Verdicts (2 of 2)

| Candidate claim | Judgement |
|---|---|
| Legacy architecture caused the waiting | **Not established**: one mapping clarification is recorded |
| Remaining work will definitely finish in 0.44 iterations | **Unsupported forecast**: the division is roughly right; comparability, capacity and uncertainty are missing |
| Rank members by commits | **Reject**: commits do not measure individual value or identify the cause of delay |

* A good next step: **inspect E's unresolved problem and settle the approval data contract**. Another AI opinion is **not verification**.

---

# 12.9 Common Mistakes
### Seven to avoid

---

## Mistakes 1 to 4

| Mistake | Consequence | Correction |
|---|---|---|
| Treat removed work as Done | Inflates delivery and hides scope decisions | Retain a separate removal event |
| Divide by all accepted items when averaging completed duration | Treats unfinished cases as if their duration were known | Use the completed cohort; report open ages separately |
| Drop waiting from cycle time without saying so | Changes the question; delay disappears | Keep elapsed time; define any extra measure separately |
| Infer work-item completion from commits | Counts workflow artefacts as delivered value | Match the unit and event to the evidence |

---

## Mistakes 5 to 7

| Mistake | Consequence | Correction |
|---|---|---|
| Use an incomplete PR sample as repository throughput | Understates or selectively counts completions | Enumerate the full interval or label a sample |
| Convert one velocity observation into a deadline | Hides variation, new scope and uncertainty | State conditional assumptions; revisit with new evidence |
| Add visitors by defaulting unknown categories to students | Bypasses the explicit new rule | Preserve rejection of unknown categories; test mapping |

---

# 12.10 Practical Activity
### Measure, interpret and prepare the change

---

## Input and Demonstration

* **Supplied:** synthetic issue history and blocked-event note; Java calculator and checks; **RM-12 v1.0**; **CR-12** contract and examples; backlog and impact templates; the Chapter 11 checkpoint.
* **Demonstration:** calculate **B's lead and cycle time**; explain **day 08's five-point drop**; trace the count/duration policy boundary in the current code.
* **Guided practice:** pairs **reconcile the final scope** and trace the interval-edge completion.

---

## Steps 1 and 2: Calculate and Interpret

1. **Book project: calculate.** Reproduce the duration table, completed count and points, final WIP and ages. Run the Java exercise and **explain one boundary check**.
2. **Book project: interpret.** Explain the scope additions and removal. Write a **cautious forecast paragraph** and reject the unsupported AI claims.

---

## Steps 3 to 5

3. **Team project: required repository lab.** Apply RM-12 to **real PR or issue timestamps**, or an instructor-supplied real export. Produce an auditable duration result and, if the population is complete, throughput. **State missing evidence honestly.** The synthetic table is rehearsal.
4. **Book project: preserve and plan.** Retain the pre-change checkpoint; review CR-12's matrix; order a small backlog for Chapter 13. **Do not implement the feature.**
5. **Team project: transfer.** Apply the impact method to your released variant. Record **one dependency or policy question** and how its answer would change the plan.

---

## Expected Artefacts and Completion Checks

* **Artefacts:** calculations; source and contract; cautious interpretation; reviewed AI claims; checkpoint reference; updated backlog; change-impact note. Keep **real repository evidence separate** from the synthetic sample.
* **Complete when:** the arithmetic reconciles; **event boundaries and population are explicit**; open items and removals stay visible; repository results have **traceable real sources**; **no individual ranking**; new behaviour has acceptance examples; old behaviour and unresolved defects have a preservation plan.
* **Optional:** compare two complete intervals with the same inclusion rule, or add reopened-item support with a **clearly revised data model**.

---

# 12.11 Review and Transfer
### Concept, diagnosis, transfer

---

## Concept Questions

1. How do lead time and cycle time differ under this chapter's contract? Why must the boundaries travel with the reported number?
2. How can a burn-down fall without an equivalent amount of work being delivered?
3. Why can equal throughput coexist with different cycle times and different customer experiences?
4. Why does a passing regression suite support preserving old behaviour without proving the new approval requirement?

---

## Diagnosis Questions

5. A dashboard calculates average cycle time only for items both started and finished this week, then claims it represents every item finished this week. What is wrong with the cohort, and which carried-in work could disappear?
6. A developer adds VISITOR to the enum and passes sponsor approval through a static Boolean read by `BorrowingPolicy`. Identify the contract, test isolation and request-matching risks; propose a clearer boundary without implementing it.

---

## Guidance: Questions 1 to 4

1. **Lead** (Accepted to Done) includes the pre-start queue; **cycle** (Started to Done) does not. B: lead five, cycle four. Another team's lead time may start at a customer request: **the number cannot travel without its event definition**.
2. **Removing F** reduces remaining scope by two while delivering nothing; re-estimation could also move a line. Keep a **scope event record**; use a burn-up.
3. A carried-in **seven-day** item and a newly completed **one-day** item count equally. Recipients **experience different waiting**.
4. The old tests describe **existing contracts**; they contain no sponsor-approval requirement. Keep them; **add new acceptance, unit and integration checks**.

---

## Guidance: Questions 5 and 6

5. Filtering on **both start and finish within the week** excludes long-running carried-in work that finished this week. **Define the cohort by the finish event**, compute durations from actual start timestamps, and report unfinished-item age separately.
6. Approval belongs to **a specific borrower, item and period at a specific time**. A static flag **loses that identity and leaks across requests and tests**, and violates the count/duration contract. Obtain **a typed approval decision through an application boundary**; validate match and time with explicit inputs before creating the reservation.

---

## Transfer Challenge: ML Model Serving

An ML model-serving team: **only approved model versions may be served to external callers**. Its dashboard counts successful builds and reports "all requested releases are complete."

* Define a **useful unit and Done event**.
* Identify the **missing approval and serving evidence**.
* Plan a narrow change **with an unavailable-registry case**.
* Explain why **model accuracy, build success and release approval are different observations**.
* Synthetic model identifiers only.

---

## Transfer Guidance

* **Unit:** one requested release of a named model version to a stated serving environment. **Done:** the approved version is **demonstrably served** at that boundary with required checks, **not a successful build**.
* Keep **build, approval and activation timestamps separate**. **An unavailable approval registry must not be treated as permission to serve.**
* Plan a valid activation path; mismatched, expired or denied approval; registry failure. Test the **genuine registry boundary** separately from orchestration doubles.
* **Accuracy** concerns predictive behaviour; **build success** construction checks; **approval** a governance decision. **None substitutes for another.**

---

# Summary and Next Chapter
### What to carry forward

---

## Summary

* A measurement is useful **when its definition supports a concrete decision**.
* The synthetic history shows why **scope, elapsed time, unfinished work and completion counts must be read together**.
* Repository evidence adds **traceability** but does not reveal every cause of delay or every valuable contribution.

---

## Where the Project Stands

* The application remains at the **pre-change checkpoint**.
* **CR-12** and the ordered backlog give a precise basis for **Chapter 13**: implementation, genuine boundary tests and delivery evidence.

---

## Sources and Further Reading

1. **Kanban Guides:** *The Kanban Guide*, May 2025.
2. **Schwaber and Sutherland:** *The Scrum Guide*, November 2020.
3. **Fowler:** *Technical Debt Quadrant* (2009).
4. **Forsgren et al.:** *The SPACE of Developer Productivity*, ACM Queue 19(1), 2021.
5. **Git Project:** `git-log` documentation. **Oracle:** Java SE 17 `Duration`.
6. **Martin:** *Agile Software Development* (2002). **Forsgren, Humble, Kim:** *Accelerate* (2018).

* Full references and links are in the chapter text.
