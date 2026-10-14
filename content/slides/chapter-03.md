---
title: "Chapter 3: Agile Development and the Nature of Change"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 30
type: slides
layout: page
---

# Chapter 3: Agile Development and the Nature of Change
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **3.1 What do we not know yet? Uncertainty and feedback**
  * Four kinds of uncertainty, and the evidence that reduces each.
* **3.2 What the Agile values mean for real project decisions**
  * Preferences, not prohibitions, applied to project decisions.
* **3.3 Iteration or increment? Two kinds of progress**
  * Related but different, and neither is a public release.
* **3.4 Scrum: who is accountable, what happens when, what it produces**
  * The November 2020 Scrum Guide, and what a classroom adapts.

---

## Chapter Roadmap (2 of 3)

* **3.5 Kanban: making the workflow visible**
  * A five-column board, a combined WIP limit, a provisional expectation.
* **3.6 From “manage equipment” to a story: epics, user stories and INVEST**
  * From "manage equipment" to a small, testable story and an ordered backlog.
* **3.7 Is the story finished? Acceptance criteria and Definition of Done**
  * Behaviour of one item versus the standard for every increment.
* **3.8 Estimating without pretending to know: relative estimation**
  * Story points as a conversation, not a guarantee.

---

## Chapter Roadmap (3 of 3)

* **3.9 Challenging a story with AI without letting it invent policy**
  * Seven suggestions: accept, reject for this story, or clarify.
* **3.10 Try it yourself: build a draft backlog**
  * Parts A to C on your team's project.
* **3.11 Habits that sound agile but are not** and **3.12 Questions to think with**
* **What to take away, and what comes next**
  * Into Chapter 4: from requirements to an iteration.

---

## Learning Outcomes (1 of 2)

After completing this chapter, you should be able to:

1. **Distinguish iterative development from incremental delivery.**
2. **Explain Agile values** through concrete project decisions.
3. **Compare Scrum's framework with Kanban's** attention to workflow and flow.

---

## Learning Outcomes (2 of 2)

4. **Develop small user stories** and evaluate them using INVEST.
5. **Write acceptance criteria** and distinguish them from a Definition of Done.
6. **Discuss relative estimates and uncertainty** without treating estimates as guarantees.

---

## How to Use This Chapter

* **Core reading:** Sections 3.1 to 3.9.
* **What you must do:** Parts A to C of Section 3.10, on your team's project.
  * The equipment-lending backlog in this chapter is the **worked model, not your evidence**.
  * Evidence needs no code or tools beyond a text editor or a board.
* **If you want more:** the plain-Java acceptance check at the end of 3.10, then the questions and the transfer challenge.

---

## Readings and Scope

* **Readings:** the Agile practices and planning chapters of Martin, the Scrum Guide, and selected chapters of Rubin.
* The chapter assumes Chapter 2's objects, date convention and basic review workflow.
* It needs **no project-management platform and no new Java framework**.
* The **companion** holds worked backlog items, board policies, exercise solutions and an optional executable bridge from acceptance examples to the existing Java.
* The running application **stays at Chapter 2's completed version**. This chapter plans future work; it does not claim features already exist.

---

## Opening Scenario: The Demonstration

* The team demonstrates the reservation coordinator from Chapter 2.
  * A student request succeeds.
  * A conflicting request is rejected.
  * A booking can begin on the exclusive end date of another.
* The program behaves as its developers expected.

---

## The Officer's Question

> Can I check whether a camera is available before I create a reservation?

* The team can inspect the stored list, but there is **no dedicated availability query**.
* The demonstration revealed a distinction: **checking a rule during a request** versus **supporting the officer's actual workflow**.

---

## More Requests Follow

* The next conversation raises:
  * **cancellation**,
  * **displaying one borrower's reservations**,
  * **rejecting an equipment identifier that does not exist**.
* The team cannot implement every suggestion immediately.
* It needs a way to **clarify requests, compare their value, expose uncertainty and decide what useful work to finish next**.

---

## What This Chapter Produces

* An **ordered backlog**.
* **Testable stories**.
* **Shared completion conditions**.
* A **visible workflow**.
* All developed on the same small codebase from Chapter 2.

---

# 3.1 What Do We Not Know Yet?
### Uncertainty and feedback

---

## Uncertainty Takes Several Forms

* We may not understand:
  * what a user needs,
  * how a rule should behave,
  * whether an integration is feasible,
  * how much work a change will require.
* Treating all of these as "requirements problems" **hides useful distinctions**.

---

## Four Uncertainties and Their Next Actions

| Uncertainty | Example in the equipment project | A useful next action |
|---|---|---|
| User need | Does the officer need an availability enquiry without reserving? | Discuss the workflow; demonstrate a small example |
| Domain rule | Can a borrower cancel after equipment has been issued? | Ask the responsible stakeholder; record the decision |
| Technical feasibility | Can the institution's catalogue be accessed? | A bounded investigation with a concrete result |
| Delivery | Can the team finish a reviewed query workflow next iteration? | Examine remaining work, capacity, assumptions |

---

## Different Questions Need Different Evidence

* A larger estimate will **not** determine the cancellation policy.
* More conversation will **not** prove that an unavailable service can be accessed.
* Naming the uncertainty helps the team choose an action **that can actually reduce it**.

---

## Feedback Also Varies

* A **user** can expose a missing workflow.
* A **compiler** can identify an invalid program.
* A **test** can show that an observed result differs from an expectation.
* A **reviewer** can identify a dependency that makes the next change harder.
* None of these observers has complete authority over every question.

---

## A Discovery Is Not Automatically a Defect

* The implementation currently **allows adjacent bookings**. That matches our rule invented for this book.
* If the officer asks for an **inspection day between loans**, the team has found a **possible policy change**, not a defect in the original comparison.
* Record: **who proposed it**, **why it matters**, and **which examples would differ** if it were adopted.

---

## What Short Feedback Cycles Do

* They make discoveries while there is **still a manageable amount of work to revise**.
* They do **not** make change free: tests, documentation and stored data may also need to change.
* The team should **expose those consequences** rather than accept every request without discussion.

---

# 3.2 What the Agile Values Mean for Real Project Decisions
### Preferences, not prohibitions

---

## The Manifesto, Paraphrased

* The Agile Manifesto gives greater emphasis to:
  * **human collaboration**,
  * **usable software**,
  * **ongoing customer involvement**,
  * **adaptation**,
* than to relying primarily on tools, exhaustive documents, contractual positions or a fixed plan.
* It **explicitly retains value** in those latter activities.

---

## Applying the Values to Our Project

| Project decision | Applying the values thoughtfully | A mistaken interpretation |
|---|---|---|
| Choosing a board | Select a tool that makes coordination easier | Assume installing a board creates collaboration |
| Recording the period convention | Keep a short, clear decision with examples | Discard documentation because the code exists |
| Handling a new borrowing rule | Discuss its purpose with the equipment officer | Let the team invent policy privately |
| Planning the next increment | Use current information; revise when needed | Stop planning because requirements may change |

---

## Principles: Delivery and Technical Quality

* The accompanying principles connect **regular delivery** with **technical quality**, a **sustainable pace** and **reflection on team effectiveness**.
* In this course the connection matters because **poorly understood code makes a small request expensive**.
* The design and testing work from earlier chapters supports the team's ability to respond.

---

## "Check Availability" Is Two Different Requests

* Option 1: merely inspect the coordinator's **current in-memory records**. A small teaching increment.
* Option 2: include an **authoritative inventory and maintenance schedule**. Substantially more work.
* Calling both "check availability" does not make them equivalent.
* **Clarify which one is meant.**

---

## Agile Still Needs Commitments

* Agile work still needs **commitments, boundaries and evidence**.
* What changes is the expectation that **every detail can be settled correctly at the beginning**.
* We maintain an explicit record of:
  * what we **know**,
  * what we **intend to deliver**,
  * what still **needs a decision**.

---

# 3.3 Iteration or Increment?
### Two kinds of progress

---

## Definitions

* An **iteration** is a repeated cycle of work and feedback.
* An **increment** adds integrated, usable capability.
* The terms describe **related but different aspects** of development.

---

## One Example of Each

* The team revises its reservation messages after a demonstration: it has **iterated** on the implementation.
* It then adds an availability enquiry that works with the existing records and can be used through the agreed interface: it has added an **increment** of capability.

---

## Effort Is Not an Increment

* An isolated **database table** or a collection of **unfinished screens** may represent effort without a usable increment.
* Technical tasks can be necessary.
* The team should explain **how they contribute to a result someone can inspect and use**.

---

## A Small Route Through the Project

1. Make the current reservation flow **reproducible**.
2. Add an **enquiry that does not change records**.
3. Support a borrower's **list of active reservations**.
4. **Cancellation** follows once its policy and state transitions are understood.

* A proposed learning route, **not a new assessment schedule**.

---

## Each Addition Must Still Work With What Came Before

* If the enquiry answers correctly but **creates a reservation as a side effect**, it has not delivered the intended capability.
* If cancellation **removes an unrelated record**, a successful cancellation message is insufficient evidence.
* Check the **whole relevant state**, not only the message.

---

## An Increment Is Not a Public Release

* A bounded teaching application can be demonstrated to its intended reviewers while remaining **unsuitable for institutional deployment**.
* Its **scope and limitations must be explicit**.
* Releasing to real users involves further considerations beyond completing a classroom exercise.
* **Chapter 4** turns the selected work into an iteration plan.

---

# 3.4 Scrum
### Who is accountable, what happens when, what it produces

---

## Scrum Is a Framework With Defined Elements

* The **November 2020 Scrum Guide** is the formal reference used here.
* Basic structure: **accountabilities**, **events**, **artefacts**.
* Terminology should **clarify responsibilities and decisions**.
* User-story templates and story points are **optional practices, not required Scrum elements**.

---

## Accountabilities

| Element | Meaning |
|---|---|
| Product Owner | Accountable for product value and effective Product Backlog management |
| Developers | Create usable increments and plan their work |
| Scrum Master | Establishes Scrum and supports team effectiveness |

---

## The Sprint and Its Events (1 of 2)

| Element | Meaning |
|---|---|
| Sprint | A fixed-length event of one month or less containing the other events |
| Sprint Planning | Establishes why the Sprint matters, the selected work and an approach |
| Daily Scrum | Developers inspect progress toward the Sprint Goal and adapt their plan |

---

## The Sprint and Its Events (2 of 2)

| Element | Meaning |
|---|---|
| Sprint Review | Inspect the outcome with stakeholders and consider adaptations |
| Sprint Retrospective | Examine how the team worked and choose improvements |

---

## The Sprint Contains All the Events

<!--svg:ch03-sprint-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="A Sprint of one month or less contains Sprint Planning, the Daily Scrum, the Sprint Review and the Sprint Retrospective." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch03-sprint-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-sprint-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-sprint-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-sprint-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-sprint-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="8.0" y="44.0" width="854.0" height="232.0" rx="14" fill="#f1f5fa" stroke="#1d588c" stroke-width="2" stroke-dasharray="9 6"/>
<text x="24.0" y="34.0" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#1d588c" text-anchor="start">Sprint: a fixed length of one month or less, containing all the events</text>
<rect x="24.0" y="68.0" width="190.0" height="76.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="119.0" y="100.3" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Sprint</text>
<text x="119.0" y="125.3" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Planning</text>
<text x="119.0" y="178.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">why the Sprint matters,</text>
<text x="119.0" y="198.8" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">what is selected,</text>
<text x="119.0" y="219.6" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">and an approach</text>
<rect x="232.0" y="68.0" width="190.0" height="76.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="327.0" y="100.3" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Daily</text>
<text x="327.0" y="125.3" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Scrum</text>
<text x="327.0" y="178.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Developers inspect</text>
<text x="327.0" y="198.8" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">progress toward the</text>
<text x="327.0" y="219.6" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Sprint Goal and adapt</text>
<rect x="440.0" y="68.0" width="190.0" height="76.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="535.0" y="100.3" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Sprint</text>
<text x="535.0" y="125.3" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Review</text>
<text x="535.0" y="178.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">inspect the outcome</text>
<text x="535.0" y="198.8" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">with stakeholders;</text>
<text x="535.0" y="219.6" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">consider adaptations</text>
<rect x="648.0" y="68.0" width="190.0" height="76.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="743.0" y="100.3" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Sprint</text>
<text x="743.0" y="125.3" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Retrospective</text>
<text x="743.0" y="178.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">examine how the team</text>
<text x="743.0" y="198.8" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">worked; choose</text>
<text x="743.0" y="219.6" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">improvements</text>
<path d="M214.0,106.0 L232.0,106.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch03-sprint-arr)"/>
<path d="M422.0,106.0 L440.0,106.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch03-sprint-arr)"/>
<path d="M630.0,106.0 L648.0,106.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch03-sprint-arr)"/>
<text x="435.0" y="268.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Together they inspect progress and adapt: the Sprint Goal ties the selected work to one outcome.</text>
</svg>
</div>
<!--/svg-->

---

## Artefacts and Their Commitments

<!--svg:ch03-commitments-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 290" role="img" aria-label="Scrum links each artefact to a commitment: the Product Backlog to the Product Goal, the Sprint Backlog to the Sprint Goal and the Increment to the Definition of Done." style="display:block;width:100%;height:calc(var(--u) * 29.00);margin:0 auto">
<defs><marker id="ch03-commitments-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-commitments-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-commitments-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-commitments-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-commitments-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="8.0" width="330.0" height="82.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="175.0" y="56.5" font-size="22" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Product Backlog</text>
<text x="175.0" y="78.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">an ordered, emergent list</text>
<rect x="530.0" y="8.0" width="330.0" height="82.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="695.0" y="56.5" font-size="22" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Product Goal</text>
<text x="695.0" y="78.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">the future state to work toward</text>
<path d="M340.0,49.0 L530.0,49.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch03-commitments-arr)"/>
<text x="435.0" y="44.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">commitment</text>
<rect x="10.0" y="100.0" width="330.0" height="82.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="175.0" y="148.5" font-size="22" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Sprint Backlog</text>
<text x="175.0" y="170.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">goal, selected work, plan</text>
<rect x="530.0" y="100.0" width="330.0" height="82.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="695.0" y="148.5" font-size="22" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Sprint Goal</text>
<text x="695.0" y="170.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">why this Sprint's work belongs together</text>
<path d="M340.0,141.0 L530.0,141.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch03-commitments-arr)"/>
<text x="435.0" y="136.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">commitment</text>
<rect x="10.0" y="192.0" width="330.0" height="82.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="175.0" y="240.5" font-size="22" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Increment</text>
<text x="175.0" y="262.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">a usable step toward the goal</text>
<rect x="530.0" y="192.0" width="330.0" height="82.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="695.0" y="240.5" font-size="22" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">Definition of Done</text>
<text x="695.0" y="262.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">the shared quality standard</text>
<path d="M340.0,233.0 L530.0,233.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch03-commitments-arr)"/>
<text x="435.0" y="228.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">commitment</text>
</svg>
</div>
<!--/svg-->

---

## The Sprint Backlog

* The Sprint Backlog includes **the goal, the selected work and the delivery plan**.
* Each artefact is tied to a commitment that makes its **purpose** explicit.
* The Definition of Done is the commitment for the **Increment**.

---

## A Product Goal

> Enable the equipment office to manage a small set of student reservations with visible rules and reliable records.

* It expresses a **useful future state**.
* It does **not** specify every screen or method.

---

## A Sprint Goal

* A possible Sprint Goal is narrower: **"Let the officer check availability without changing reservations."**
* It tells the team **why its selected work belongs together**.
* Compare: "Finish US-02, update the README and edit three classes" lists **work** but does not explain the **outcome that connects it**.

---

## A Daily Scrum Contribution

* A developer might say: "The enquiry works, but its result depends on a date convention we have not documented. I will pair with the reviewer to resolve that before adding another feature."
* This focuses on **the team's progress**.
* The Scrum Guide defines the Daily Scrum as a **15-minute event for the Developers** to inspect progress toward the Sprint Goal and adapt their plan.
* It is **not a status report to a supervisor**.

---

## A Sprint Review

* The equipment officer tries the enquiry and asks whether a **damaged item** should ever appear available.
* That discussion concerns **the product and possible next work**.
* The Scrum Guide describes the Sprint Review as a **working session**, not limited to a presentation.

---

## A Sprint Retrospective

* The team notices that reviews **consistently arrived too late**.
* It agrees to **request review when a small behaviour first works**, then inspects whether that agreement helps.
* The retrospective concerns increasing **quality and effectiveness**, including **how the team collaborated and verified work**.

---

## Classroom Adaptations Must Be Named

* The module leader may provide stakeholder answers; teams may rotate facilitation; reviews may happen within teaching sessions.
* These are **course arrangements**. They do not redefine Scrum's accountabilities or turn every classroom meeting into a formal Scrum event.
* An **academic submission date is not automatically a Sprint boundary**.

---

## "Sprint 0"

* The descriptor's later **"Sprint 0"** label refers to **kickoff work**.
* Treat it as a **local preparation convention**, not another formal Scrum event.
* Keep the distinction visible when you write reports about the process your team actually followed.

---

# 3.5 Kanban
### Making the workflow visible

---

## What Kanban Focuses On

* Kanban focuses on the **flow of value through work**.
* The May 2025 Kanban Guide describes:
  * **defining and visualising** a workflow,
  * **managing work within it**,
  * **improving** that workflow.

---

## What a Workflow Definition Includes

* Work items.
* **Start and finish points**.
* States.
* **Work-in-progress controls**.
* Movement policies.
* A **service-level expectation**: elapsed time combined with a probability. Historical evidence should inform it when available.

---

## Our Five Columns

| Column | Local meaning |
|---|---|
| Backlog | Candidate work, not yet selected to start |
| Ready | Small enough and clear enough to begin under the team's local policy |
| Building | Implementation and associated checks are under way |
| Review | Work is awaiting or receiving review and verification |
| Done | The agreed completion conditions have been met |

* These columns are **our example**, not mandatory names.

---

## Start, Finish and the Combined Limit

* **Start point:** entry into **Building**.
* **Finish point:** entry into **Done**.
* Limit the **combined** number of items in Building and Review to **two**.
* **Blocked work stays within that count.** An uncounted "Blocked" column would hide unfinished work rather than finish it.

---

## A Hypothetical Snapshot

<!--svg:ch03-board-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 350" role="img" aria-label="A five-column board: Backlog, Ready (US-03, US-04), Building (US-02), Review (EN-01, blocked) and Done (US-01). Building and Review share a combined work-in-progress limit of two, which is reached." style="display:block;width:100%;height:calc(var(--u) * 35.00);margin:0 auto">
<defs><marker id="ch03-board-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-board-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-board-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-board-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch03-board-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="15.0" y="38.0" width="160.0" height="232.0" rx="8" fill="#eef3f8" stroke="#c3cfdd" stroke-width="1.6"/>
<rect x="15.0" y="38.0" width="160.0" height="38.0" rx="8" fill="#1d588c" stroke="#1d588c" stroke-width="1.6"/>
<text x="95.0" y="63.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">Backlog</text>
<rect x="185.0" y="38.0" width="160.0" height="232.0" rx="8" fill="#eef3f8" stroke="#c3cfdd" stroke-width="1.6"/>
<rect x="185.0" y="38.0" width="160.0" height="38.0" rx="8" fill="#1d588c" stroke="#1d588c" stroke-width="1.6"/>
<text x="265.0" y="63.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">Ready</text>
<rect x="197.0" y="90.0" width="136.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="265.0" y="121.0" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">US-03</text>
<rect x="197.0" y="152.0" width="136.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="265.0" y="183.0" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">US-04</text>
<rect x="355.0" y="38.0" width="160.0" height="232.0" rx="8" fill="#eef3f8" stroke="#c3cfdd" stroke-width="1.6"/>
<rect x="355.0" y="38.0" width="160.0" height="38.0" rx="8" fill="#1d588c" stroke="#1d588c" stroke-width="1.6"/>
<text x="435.0" y="63.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">Building</text>
<rect x="367.0" y="90.0" width="136.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="435.0" y="121.0" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">US-02</text>
<rect x="525.0" y="38.0" width="160.0" height="232.0" rx="8" fill="#eef3f8" stroke="#c3cfdd" stroke-width="1.6"/>
<rect x="525.0" y="38.0" width="160.0" height="38.0" rx="8" fill="#1d588c" stroke="#1d588c" stroke-width="1.6"/>
<text x="605.0" y="63.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">Review</text>
<rect x="537.0" y="90.0" width="136.0" height="50.0" rx="6" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="605.0" y="112.0" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">EN-01</text>
<text x="605.0" y="131.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#b4762e" text-anchor="middle" font-style="italic">blocked</text>
<rect x="695.0" y="38.0" width="160.0" height="232.0" rx="8" fill="#eef3f8" stroke="#c3cfdd" stroke-width="1.6"/>
<rect x="695.0" y="38.0" width="160.0" height="38.0" rx="8" fill="#0c2238" stroke="#1d588c" stroke-width="1.6"/>
<text x="775.0" y="63.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">Done</text>
<rect x="707.0" y="90.0" width="136.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="775.0" y="121.0" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">US-01</text>
<text x="435.0" y="26.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">start point</text>
<text x="775.0" y="26.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">finish point</text>
<path d="M355.0,282.0 L355.0,298.0 L685.0,298.0 L685.0,282.0" fill="none" stroke="#b4762e" stroke-width="2.6"/>
<text x="520.0" y="326.0" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#b4762e" text-anchor="middle">WIP limit: 2 items in Building and Review combined</text>
<text x="95.0" y="296.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Hypothetical snapshot</text>
</svg>
</div>
<!--/svg-->

---

## The Limit Is Reached: What Now?

* One item is in Building and another is waiting in Review.
* Before starting a third, investigate **what would help an existing item finish**:
  * review together,
  * resolve a question,
  * make a smaller change.
* A limit is useful **only when it affects decisions**.

---

## A Board Alone Is Incomplete

* A team also needs **workflow policies, active management and evidence for improvement**.
* For practice: provisionally expect **85% of small items to finish within five working days** after starting.
* Without historical data that is an **explicitly unvalidated hypothesis**, not a measured promise.
* Chapter 12 develops flow measures and forecasting. We do not derive a delivery guarantee from an invented example.

---

## Comparing Scrum and Kanban (1 of 2)

| Question | Scrum emphasis | Kanban emphasis |
|---|---|---|
| What structures the work? | Goals, Sprints, defined accountabilities and events | Explicit workflow and control of work in progress |
| What is inspected? | Product outcomes and progress toward goals | How work moves, waits and finishes |

---

## Comparing Scrum and Kanban (2 of 2)

| Question | Scrum emphasis | Kanban emphasis |
|---|---|---|
| Can a board help? | Yes, to make selected work visible | Yes, to visualise the workflow and its policies |
| Can they be used together? | A Scrum team can also manage flow explicitly | Flow practices can operate within a Sprint cadence |

* Not: "Scrum has meetings; Kanban has none". Not: "Scrum is planned; Kanban is unplanned."
* The chosen approach should help the team **make decisions**, not merely supply labels.

---

# 3.6 From “Manage Equipment” to a Story
### Epics, user stories and INVEST

---

## "Manage Equipment" Is Too Broad

* It may refer to **stock records, borrowing, maintenance, losses, reporting or purchasing**.
* To guide the next implementation we must identify **a particular actor, outcome and reason**.

---

## Epic and User Story

* An **epic** is a label for a large area of work that needs further division.
  * Here: "Manage student equipment reservations".
* A **user story** expresses a smaller user-centred need.

> As an equipment officer, I want to record an eligible, non-conflicting reservation so that the selected item is allocated for the borrower's requested period.

---

## A Story Opens a Discussion

* The sentence does **not** define eligibility, conflicts, dates or failure behaviour by itself.
* Ron Jeffries connects a short written reminder with **conversation and confirmation**.
* We keep a **card**, record the **relevant decisions** and attach **observable examples**.

---

## Stories and Implementation Tasks

* "Create a `HashMap`" names an **implementation task**. It does not explain the outcome a user needs.
* A story can lead to tasks (data structures, checks, interface work), but they should **remain connected to the outcome**.
* Not all backlog work needs a fictional user-story sentence.

---

## Technical Enablers

* A build-check task can be labelled a **technical enabler**, justified by the delivery problem it addresses.
* Our convention: `US-` for stories and `EN-` for enablers.
* These prefixes are **local identifiers, not Agile rules**.

---

## INVEST as Questions (1 of 2)

| Quality | Question to ask about this story |
|---|---|
| Independent | Can it provide an identifiable outcome without another unfinished story? If not, what is the dependency? |
| Negotiable | Which implementation details can still be discussed while preserving the need? |
| Valuable | Who benefits from this behaviour, and how? |

---

## INVEST as Questions (2 of 2)

| Quality | Question to ask about this story |
|---|---|
| Estimable | Is the team clear enough about scope and uncertainty to discuss its size? |
| Small | Can the team implement and verify a useful version within its intended work period? |
| Testable | Can we describe observations that distinguish success from failure? |

* Bill Wake introduced INVEST to prompt useful qualities in stories.

---

## INVEST Is a Reasoning Aid

* It is **not a six-point score** that certifies a story.
* Real dependencies should be recorded. "Independent" should not make us pretend cancellation needs no existing reservation.
* "Negotiable" should not mean ignoring an agreed safety or domain rule.

---

## A Small Version of the Availability Story

* Inspect the coordinator's **current records** for **one known item** and **one period**, leaving records unchanged.
* Adding **live inventory, maintenance calendars, permissions and email delivery at the same time** would make it harder to identify what is being delivered.

---

## A Backlog Is Ordered Work

* The Scrum Guide describes the Product Backlog as an **emergent, ordered list**.
* **Refinement** is the ongoing work of breaking items into smaller, more precise ones.
* Ordering and refinement together make upcoming work understandable.
* We record **current support** as well as remaining work, because the team inherits code from Chapter 2.

---

## The Beginning of a Draft Backlog

| Order | ID | Outcome or purpose | Relationship to existing code |
|---:|---|---|---|
| 1 | US-01 | Record an eligible, non-conflicting student reservation | Core behaviour exists; delivery and completion evidence must be reviewed |
| 2 | US-02 | Inspect an item's availability without reserving it | No dedicated query operation exists yet |
| 3 | EN-01 | Make the existing checks reproducible in an automated build workflow | Planned enabler for the kickoff work in Chapter 4 |

---

## Not a Delivery Report

* This is the beginning of a **draft backlog**, not a report that three items have been delivered.
* **Review inherited capability** instead of pretending to implement it again.
* When a story's conditions are met, retain the evidence in **completed history** rather than counting it again as new work.

---

# 3.7 Is the Story Finished?
### Acceptance criteria and Definition of Done

---

## Two Different Questions

* **Acceptance criteria** describe the behaviour expected for **a particular item**.
  * Specific enough that **a second team** can tell whether an implementation meets them.
* **Definition of Done** describes the **shared quality conditions** required for an increment.
  * Scrum makes that definition the **commitment associated with the Increment**.

---

## US-01 Criteria: Conventions

* All counts are measured **before** adding the new reservation.
* All stored reservations are currently **active**.
* Dates use the **exclusive-end convention** from Chapter 2.
* The next slides list AC-01 to AC-05.

---

## US-01 Acceptance Criteria

| Criterion | Required observable behaviour |
|---|---|
| AC-01 | An eligible request for an available item creates one stored reservation and returns its confirmation |
| AC-02 | A request overlapping an existing reservation for the same item is rejected without changing stored records |
| AC-03 | A request that begins at an existing reservation's exclusive end, or ends exactly where one begins, is permitted when the other rules hold |
| AC-04 | A borrower with three active reservations cannot add a fourth, even for another item |
| AC-05 | One through seven whole days are allowed; zero, negative and eight-day requests are rejected without adding records |

---

## What the Criteria Do Not Establish

* They describe a **controlled demonstration** using non-blank, agreed sample identifiers and representable dates.
* They do **not** establish catalogue membership, authentication, persistence or concurrency safety.
* Those omissions must **remain visible** when judging what kind of product the story represents.

---

## Turn AC-02 into an Example

```text
Given CAM1 is reserved for B1 from 20 October to 22 October,
using a start-inclusive, end-exclusive period,
when B2 requests CAM1 from 21 October for one day,
then the request is rejected as unavailable,
and the original reservation remains the only stored record.
```

* The format separates **context, action and observations**.
* It is plain text here, not an executable framework.

---

## Both Observations Matter

* The **rejection**, and
* the **unchanged state**.
* A program that prints the correct rejection but **still adds a reservation** has not met the criterion.
* This introduces **traceability** between an example and behaviour. It is not yet a complete TDD or BDD method.

---

## A Working Definition of Done (1 of 2)

**DoD version 0.1 for the controlled teaching increment:**

1. Relevant acceptance examples have been checked, including important **rejection paths**.
2. The code **compiles and runs** using the documented commands in the agreed environment.
3. The change has been **reviewed** and acceptance-blocking findings resolved.

---

## A Working Definition of Done (2 of 2)

4. The work is **integrated** with the team's shared codebase and existing checks still pass.
5. Necessary **usage notes, domain decisions and known limitations** are current.
6. The increment can be **reproduced and demonstrated** within its explicitly stated scope.

* A proposed team agreement, **not a university grading policy**.

---

## Do Not Pretend a Pipeline Exists

* The DoD uses checks **available now**. Automated CI gates can be added when the infrastructure is introduced.
* Do **not** claim a pipeline has passed before it exists.
* Do **not** weaken the agreed standard merely to move a card to Done.

---

## Story Criteria and Shared Completion

* AC-03 belongs to the reservation story because it **defines date behaviour**.
* **Reproducible setup** belongs to the shared completion agreement.
* Passing a story's examples while leaving an **unreviewed, unintegrated change** does not meet this DoD.
* Appendix C has blank forms, each with a worked example, for a **story card (C.2)**, an **acceptance example (C.3)** and a **Definition of Done (C.4)**.

---

## "Ready" Has a Different Purpose

* "Ready" records whether a team considers an item **sufficiently understood to start**.
* Our Ready-column policy is a **local agreement**, not an additional formal Scrum artefact or event.
* It should help a conversation, not become a ritual that demands every detail months in advance.

---

## Distinguishing the Three Conditions

| Kind of condition | Example | Question answered |
|---|---|---|
| Acceptance criterion | An enquiry leaves reservations unchanged | Does this behaviour satisfy the story? |
| Definition of Done | The integrated change is reviewed and its checks pass | Does the increment meet the shared standard? |
| Local Ready policy | Known scope, example inputs, identified blocking questions | Is the item understood enough to begin? |

---

## From Criterion to Code: A Plain-Java Bridge

```java
// AC-02: an overlapping request changes no records.
String conflict = coordinator.reserve("B2", "CAM1", day.plusDays(1), 1);
require(conflict.equals("Rejected: item unavailable."), "AC-02 rejection");
require(coordinator.reservations().size() == 1, "AC-02 unchanged count");
require(coordinator.reservations().get(0).borrowerId().equals("B1"),
        "AC-02 original borrower preserved");
System.out.println("AC-02 passed");
```

* The companion's `Chapter03AcceptanceExamples` runs AC-01 to AC-05 against the **completed Chapter 2 coordinator**.

---

## Running the Bridge

```sh
javac --release 17 -d out ReservationRules.java LoanPeriod.java \
    Reservation.java ReservationCoordinator.java \
    Chapter03AcceptanceExamples.java
java -cp out Chapter03AcceptanceExamples
```

```text
AC-01 passed
AC-02 passed
AC-03 passed
AC-04 passed
AC-05 passed
All 5 acceptance examples passed.
```

---

## What the Bridge Shows

* Each labelled group corresponds to a criterion: **setup, action, observations**.
* AC-04 uses **different item identifiers**, so the fourth refusal comes from the borrower's total count, not an item conflict.
* AC-05 stays **below the count limit**, so the duration rule is the reason for rejection.
* A passing run does **not** satisfy the Definition of Done by itself: review, integration and reproducibility still matter.

---

## Do the Examples Detect Faults?

| Change to `LoanPeriod` or `ReservationRules` | Chapter 3 runner |
|---|---|
| Original | All 5 acceptance examples passed |
| First overlap comparison to `!start.isAfter(other.endExclusive)` | Failed at `AC-03 request ending at an existing start` |
| Second overlap comparison to `!other.start.isAfter(endExclusive)` | Failed at `AC-03 adjacent confirmation` |
| `activeReservations < 3` to `<= 3` | Failed at `AC-04 fourth rejected` |
| `requestedDays <= 7` to `< 7` | Failed at `AC-05 seven days` |

---

## Why AC-03 Has Two Requests

* If AC-03 contained **only** a request starting at an existing end, the first overlap change would pass every Chapter 3 example.
* The extra request, one that **ends exactly where an existing reservation begins**, closes that gap.
* Chapter 2's `adjacency symmetric` check also caught that change.
* Lesson: choose example sets to **expose specific faults**, not merely to be numerous.

---

# 3.8 Estimating Without Pretending to Know
### Relative estimation

---

## What an Estimate Is For

* An estimate helps a team **discuss and forecast** work.
* It is **not a guarantee** that a specific person will finish at a precise time.
* Before estimating, establish **what is included**: implementation alone, or also review, checking and documentation needed to meet Done?

---

## Story Points as a Local Scale

* **Story points** are an optional local relative scale.
* A team might use **1, 2, 3, 5 and 8** to compare work considering effort, complexity and uncertainty.
* These numbers are **not hours**.
* The same number in two teams need not represent equivalent work.

---

## Two Estimates That Disagree

* A familiar display adjustment is the reference item at **two** points.
* A small availability query may seem larger: a non-mutating operation, several date examples and a new interaction.
* One learner estimates **three**, another **eight**.
* Averaging them immediately would **discard the most useful information: why they disagree**.

---

## Expose the Assumption

* The second learner may be assuming the query includes **maintenance schedules**.
* Once exposed, the team can **narrow the story** or record a separate requirement.
* If the uncertainty is an **external catalogue with an unknown interface**, a short investigation may be more useful than a larger number.

---

## A Bounded Investigation

* Good: "Determine whether a read-only sample catalogue can be accessed and record the fields it provides."
* Bad: an unlimited task called "research the system".
* A bounded investigation has **a question** and **an output**, including the result "access not obtained".
* Do not probe systems without authorisation.

---

## Practising Estimation

* Estimate **only clarified items** and write the **assumption** behind each estimate.
* Leave an item **unestimated** when a material question remains.
* Different reasoned estimates are acceptable. **Claiming certainty without evidence is not.**

---

## Estimates Are Not Productivity Measures

* Do **not** rank students by points completed.
* Do **not** convert points into individual productivity targets.
* Do **not** assume that doubling team size doubles delivery.
* Chapter 4 combines selected work with actual capacity; Chapter 12 examines measured progress and flow.

---

## An Example of Estimates With Assumptions

| Item | Estimate | Assumption or uncertainty |
|---|---:|---|
| US-02 local availability enquiry | 3 points | Known sample identifiers, existing date convention, no external catalogue |
| US-03 one borrower's active records | 2 points | "Active" unchanged; officer-operated controlled demonstration |
| US-04 cancellation | Not yet estimated | Authority, permitted lifecycle states and effect on counts unresolved |

* Invented numbers for discussion. No velocity or forecast is claimed.

---

# 3.9 Challenging a Story with AI Without Letting It Invent Policy
### Without inventing policy

---

## What AI Can and Cannot Do Here

* An AI assistant can **suggest missing assumptions and candidate criteria**.
* It has **no authority to decide the equipment office's rules**.
* The exercise is to **evaluate its proposals against the agreed context**.
* Chapter 15 collects the recurring AI workflows. This activity is self-contained.

---

## Ground Rules for the Activity (1 of 2)

| | For this activity |
|---|---|
| Your goal | Decide which suggestions belong in the story, which do not and which need a stakeholder |
| You start with | US-01, AC-01 through AC-05, and Chapter 2's scope |
| What is in bounds | Classify the suggestions; do not change the policy, the code or the story's scope on your own |

---

## Ground Rules for the Activity (2 of 2)

| | For this activity |
|---|---|
| How to check | The stated rules, the Chapter 2 code and checks, the story's scope |
| How to decide | **Accept**, **reject for this story**, or **clarify** with a named person or decision |
| No AI account? | The ready-made example is enough |

---

## The Ready-Made Example (1 of 2)

An **ready-made example written by the author**, not a captured response from a real model.

1. A request for the same item and an identical period must be refused.
2. A request that begins exactly when an existing period ends must be refused.
3. Every confirmation must be emailed within thirty seconds.
4. A refused request must leave stored reservations unchanged.

---

## The Ready-Made Example (2 of 2)

5. Specify how start dates that are already in the past are treated.
6. A deposit payment must be taken before any reservation can be confirmed.
7. Specify whether cancelled reservations count toward the borrower's limit.

* Classify each suggestion **with a reason**.
* "Reject" can mean the proposal contradicts a rule or introduces unapproved scope. It need not mean the idea could never be useful.

---

## Decision Log (1 of 2)

| Suggestion | Disposition | Reason |
|---|---|---|
| 1. Refuse the same item and an identical period | Accept | An identical period overlaps; a useful special case of AC-02 |
| 2. Refuse a request beginning exactly when another ends | Reject for this story | Contradicts the exclusive-end convention and AC-03 |
| 3. Email every confirmation within thirty seconds | Reject for this story | Adds delivery infrastructure and a timing requirement not agreed |
| 4. A refused request leaves records unchanged | Accept | Matches the state-preservation expectations of AC-02 and AC-05 |

---

## Decision Log (2 of 2)

| Suggestion | Disposition | Reason |
|---|---|---|
| 5. Specify how past start dates are treated | Clarify | The policy sets no past-date restriction; do not invent one |
| 6. Take a deposit before confirming | Reject for this story | A new business process and unapproved scope |
| 7. Do cancelled reservations count toward the limit? | Clarify, link to US-04 | Cancellation is not implemented; it matters when that lifecycle arrives |

---

## What a Sufficient Record Contains

* The **suggestion**.
* The **classification**.
* The **source of authority** (rule, code or stakeholder).
* The **next action**.
* "AI is wrong" without naming the conflicting rule is **not enough**.
* No suggestion becomes a rule merely because AI produced it.

---

## Optional Live Prompt

> Review this story against the supplied policy and current project scope. Suggest missing assumptions, edge cases and candidate acceptance criteria. Label each suggestion as derived from a stated rule, an open question or a possible scope extension. Do not silently change the policy or claim a feature is already implemented.

* Refer to the **rule or code evidence**, not the assistant's confidence.

---

# 3.10 Try It Yourself
### Build a draft backlog

---

## Context

* The activity runs on your team's project.
* Equipment lending teams start from the Chapter 2 coordinator, the three backlog entries in 3.6 and the rule invented for this books.
* Another provided domain? Apply the same steps to that domain's starter codebase and its first user-visible capability.
* For an ML model-serving tool, for example: "as an analyst, I want a prediction for a supplied record so that I can check the result".
* It is preparation for the Week 3 kickoff and does not change assessment dates or weights.

---

## Part A: Define and Refine

* Write a short proposed **Product Goal**.
* Extend the draft backlog to **six items**, considering a borrower's active-reservation list, cancellation and catalogue-identifier validation.
* Use **stable IDs**; identify **dependencies** and **unresolved decisions**.
* **Order** the items and explain the first two positions.

---

## Part A: Be Honest About the Baseline

* Record which behaviours are **already supported in code**, which **need new implementation**, and which **cannot yet be judged**.
* Do **not** label an inherited feature Done solely because a demonstration prints the desired text.
* Refine **US-02** into a small story with **at least four acceptance examples**.
* State that asking about availability **must not create or remove reservations**.

---

## A Proposed Product Goal

> Enable an equipment officer, in a controlled demonstration, to create and inspect student reservations with clear eligibility decisions and no overlapping reservations for the same item within one coordinator.

* A **future outcome**, explicitly bounded; not a claim that it is achieved.
* A next-iteration candidate: inspect availability without changing reservations.

---

## A Worked Six-Item Backlog (1 of 2)

| Order | ID | Item | Type |
|---:|---|---|---|
| 1 | US-01 | Record an eligible, non-conflicting student reservation | User story |
| 2 | US-02 | Inspect availability without reserving an item | User story |
| 3 | EN-01 | Automate the existing build and checks | Technical enabler |

---

## A Worked Six-Item Backlog (2 of 2)

| Order | ID | Item | Type |
|---:|---|---|---|
| 4 | US-03 | Inspect one borrower's active reservations | User story |
| 5 | US-04 | Cancel a confirmed reservation under an agreed policy | User story |
| 6 | US-05 | Reject unknown equipment identifiers using an agreed catalogue | User story |

* The order is **one defensible teaching choice**, not a calendar and not a promise that all six fit one Sprint.

---

## Rationale and Dependencies

* **US-01** prevents building on a falsely reported baseline. Verify, then move to completed history with evidence.
* **US-02** answers the workflow gap found at demonstration. It need not wait for a production database.
* **EN-01** supports reliable repeated work; coordinate with Chapter 4's kickoff.
* **US-04** changes the meaning of "active", so it affects counts and availability.
* **US-05** sits lower because early demonstrations use controlled sample identifiers. Reorder if real users or uncontrolled input enter scope.

---

## US-02 Refined: The Card

* **Actor and outcome:** as an equipment officer, I want to inspect whether a **known item** is available for a **proposed period** without reserving it, so that I can discuss options with a borrower.
* **Scope:** the current coordinator's records, controlled sample identifiers.
* It does **not** promise the item is operational, not under maintenance, or available in another application instance.
* A successful enquiry never confirms a reservation and **never guarantees a later request will succeed**.

---

## US-02: Acceptance Examples (1 of 2)

| ID | Given and when | Expected observations |
|---|---|---|
| AQ-01 | No stored reservations; inspect CAM1 for `[20 Oct, 22 Oct)` | Available within this record set; records unchanged |
| AQ-02 | CAM1 reserved for `[20 Oct, 22 Oct)`; inspect `[21 Oct, 23 Oct)` | Unavailable; existing record unchanged |
| AQ-03 | Same reservation; inspect CAM1 for `[22 Oct, 23 Oct)` | Available under the adjacency convention; records unchanged |

---

## US-02: Acceptance Examples (2 of 2)

| ID | Given and when | Expected observations |
|---|---|---|
| AQ-04 | CAM1 reserved; inspect a different known item MIC1 for the same period | Available if MIC1 has no conflict; records unchanged |
| AQ-05 | Inspect an invalid period with equal or reversed dates | An identifiable invalid-input outcome, not a valid availability answer; no records changed |

* AQ-05 states the user-observable meaning **without prescribing an exception class**. It must **not** silently return "available".

---

## US-02: Unknowns and Status

* **Unknowns:** catalogue identifiers outside the controlled examples; maintenance rules; restrictions on past dates. Record them as questions.
* Do **not** add a hidden maintenance buffer: the interval convention allows adjacency.
* **Status:** the query is **not implemented** by the Chapter 2 code.
* `reserve` cannot be reused by calling it and undoing the result: that introduces a mutation and fails the story.

---

## INVEST Applied to US-02

* **Independent:** demonstrable with existing records, without cancellation. Depends on the period convention.
* **Negotiable:** input mechanism and presentation, while preserving non-mutation.
* **Valuable:** compare periods without speculative reservations.
* **Estimable:** a query against a controlled local list is bounded.
* **Small:** one item and one period.
* **Testable:** compare the result and the complete relevant state before and after.

---

## Part B: Agree Completion and Workflow

* Propose a **Definition of Done** and explain how it differs from your story criteria.
* Draw a **board**: the five example columns or a justified alternative.
* Define **start and finish points**, **movement policies**, **WIP control** and **handling of blocked work**.
* Record the **service-level expectation as provisional** if you lack data.

---

## Part B: The Process Note

* Write a short process note naming:
  * which Scrum elements your team uses **as the Guide defines them**,
  * which it **adapts for the course**,
  * which **optional practices** (stories, points, a board) it adopts.
* Any honest statement is acceptable. Using stories, points and a board but no designated Scrum Master is a **legitimate adaptation**.
* Calling an academic deadline a Sprint **without naming that adaptation** is not.

---

## A Complete Example Workflow Policy (1 of 2)

* **Work item:** a small user story or an explicitly identified enabler.
* **States:** Backlog, Ready, Building, Review, Done.
* **Start and finish:** start on entering Building; finish on entering Done. Building and Review both count toward WIP.
* **WIP control:** at most **two** items across Building and Review combined (invented for the classroom).

---

## A Complete Example Workflow Policy (2 of 2)

* **Movement:** Ready when outcome, scope and examples are understood; Building when capacity allows; Review when change and evidence can be inspected; Done only when acceptance conditions **and** the DoD are met. A **failed review returns to Building** and stays within WIP.
* **Blocked work:** keep it in its actual state, mark the blocker and who is investigating it, keep it within WIP. If abandoned, record that separately.
* **Inspection:** first look at blocked or waiting active work and agree a concrete next action.

---

## Board Exercise (Hypothetical)

| Ready | Building | Review | Done |
|---|---|---|---|
| US-03, US-04 | US-02 | EN-01, blocked by a setup problem | US-01 |

* The combined Building-plus-Review limit is **two**.
* Decide what to investigate next, and explain why moving the blocked card outside the counted area **misrepresents its work**.

---

## Board Exercise: Solution

* US-02 is in Building and EN-01 is blocked in Review: **two items started, none finished, limit reached**.
* Investigate the setup blocker, help review or complete the existing feature **before pulling another ordinary item from Ready**.
* If the blocker truly prevents progress, discuss and **record the trade-off** rather than silently changing the count.
* A WIP policy can be revised deliberately. An **invisible exception** destroys the information needed to evaluate it.
* US-01's Done position belongs only to the simulation.

---

## Part C: Estimate and Critique

* Choose **two clarified items** and propose relative estimates **with assumptions**.
* Identify **one item that needs clarification or investigation** before sizing.
* Complete the AI activity and record the **disposition of each suggestion**.

---

## Compare Two Invented Recommendations

> Advice A: Freeze every detailed story before any implementation begins.

> Advice B: Start implementation immediately and leave acceptance conditions until the demonstration.

* For each: the **problem it tries to solve**, its **risk in this project**, and a **more defensible working agreement**.

---

## Critique of Advice A and B

* **Advice A** avoids ambiguity but assumes all detail is known up front. The availability enquiry itself **emerged from a demonstration**.
* **Advice B** encourages fast feedback but cannot tell success from a **persuasive demonstration**: a query that mutates state might look acceptable.
* **Stronger agreement:** clarify the next small outcome and its **key examples** before implementation; revise as evidence appears; keep later work less detailed until it nears selection.

---

## Evidence and Completion Check

* Retain: the **proposed goal**, **ordered six-item backlog**, **two refined story cards**, acceptance examples, **Definition of Done**, **workflow policy**, **process note**, **estimates with assumptions**, **AI decision log**.
* **Exchange the top story with another team.**
* Complete when the other team can **explain the outcome, select meaningful inputs and predict observable results without inventing essential policy**.
* Record any question they could not answer, then revise the story or **explicitly defer** the decision.

---

## If You Want More

* Write a plain-Java check for your top story's examples, in the style of `Chapter03AcceptanceExamples`.
* Confirm that it **fails when you introduce a deliberate fault**.
* Peer story review: ask another team to describe the outcome, pick an ordinary and a failure case, and state the expected state afterwards.

---

# 3.11 Habits That Sound Agile but Are Not
### Seven mistakes and their corrections

---

## Mistakes 1 to 3

| Mistake | Consequence | Correction |
|---|---|---|
| Treating Agile as the absence of planning | Dependencies and deadlines remain invisible | Plan at useful detail; revise from evidence |
| Treating a story template as the full requirement | Eligibility and failure behaviour remain ambiguous | Add discussion, decisions and examples |
| Calling every item highest priority | The team has no usable order | Explain why one outcome precedes another |

---

## Mistakes 4 and 5

| Mistake | Consequence | Correction |
|---|---|---|
| Treating acceptance criteria as the whole DoD | Correct examples hide unreviewed or unintegrated work | Check behaviour and shared quality conditions |
| Starting new work whenever review is blocked | Unfinished work accumulates | Make the blockage visible; help existing work finish |

---

## Mistakes 6 and 7

| Mistake | Consequence | Correction |
|---|---|---|
| Treating AI suggestions as stakeholder decisions | Scope or policy changes without agreement | Classify each proposal and justify its disposition |
| Counting inherited working code as newly delivered work | Progress becomes misleading | Record the baseline and the remaining work honestly |

---

# 3.12 Questions to Think with
### Concept, diagnosis, transfer

---

## Concept Questions

1. Explain how an iteration can improve an existing feature and how an increment adds usable capability. Give an equipment-lending example of each.
2. Choose one Agile value and explain a decision that respects both sides of its preference rather than discarding one side.
3. Distinguish Sprint Review, Sprint Retrospective and Daily Scrum using the decisions each helps the team make.
4. Explain the difference between acceptance criteria, Definition of Done and the local Ready-column policy.

---

## Diagnosis Questions

5. A team marks an availability story Done because its method returns a correct answer for one date. The enquiry also adds a reservation, and the change has not been reviewed. Identify two separate completion failures and the evidence needed to investigate them.
6. Two items already occupy the team's limited active workflow. One is blocked in Review. A developer moves it to an uncounted column and starts a third item, claiming the WIP limit is still respected. Explain what the board now hides and propose a useful next action.

---

## Guidance: Questions 1 and 2

1. Revising the reservation messages after feedback is an **iteration** on an existing capability. Adding an integrated, usable enquiry that leaves records untouched is an **increment**. A cycle can produce an increment, but the words do not mean the same.
2. Favouring usable software over exhaustive documents still permits a **short written period convention**. The documentation supports the outcome; it does not substitute for examining it.

---

## Guidance: Questions 3 and 4

3. A **Review** examines outcomes with stakeholders and influences product choices. A **Retrospective** selects improvements in how the team works. A **Daily Scrum** helps Developers adapt their near-term plan toward the Sprint Goal.
4. **Acceptance criteria** are item-specific behavioural expectations. The **DoD** is the shared quality standard for the increment. **Ready** is this team's local policy for starting work, not a formal Scrum artefact.

---

## Guidance: Questions 5 and 6

5. The enquiry violates its **non-mutation acceptance condition**, and missing review violates the **example DoD**. Inspect records before and after, repeat the relevant examples, and obtain an actual review. One correct date is insufficient evidence for either.
6. The blocked item **remains unfinished**, so a third item exceeds the combined limit. Investigate or resolve the blockage and finish existing work. If policy must change, **record the change and its reason**.

---

## Transfer Challenge: Laboratory Room Booking

A laboratory room-booking team receives the request **"Make booking easier."**

* Develop **two small user stories** and **one justified technical enabler**.
* Give one story **four acceptance examples**, including a failure case and an observation about **unchanged state**.
* Propose a shared **Definition of Done** and a simple **WIP policy**.
* Identify one question for a **stakeholder** and one technical uncertainty that might need an **investigation**.
* Explain how to obtain feedback without pretending every rule is known.

---

## Transfer Challenge: Sample Answer

* **RB-01:** as a laboratory coordinator, I want to inspect availability for one known room and period without booking it, so that I can offer an appropriate slot.
* **RB-02:** confirm an eligible, non-conflicting booking.
* **RE-01 (enabler):** make the existing build and checks reproducible in the shared workflow.
* RB-01 examples: no booking, available, nothing created; booking 10:00 to 11:00 and enquiry 10:30 to 11:30, unavailable and unchanged; enquiry starting at 11:00 may be available; end before start gives an invalid-input result.

---

## Transfer Challenge: Completion and Uncertainty

* A reasonable DoD: checked examples, reproducible build, actual review, integration, updated decisions or notes.
* WIP: combined Building and Review limited to two, blocked work counted.
* **Stakeholder question:** does room capacity or organiser authority restrict booking?
* **Technical uncertainty:** can an approved read-only room catalogue be obtained? Investigate with a bounded task. Do not invent an API.
* Confirm whether a cleaning buffer is required before accepting adjacency for a real system.

---

# What to Take Away, and What Comes Next
### What to carry forward

---

## Summary: Learning and Quality

* Agile combines a **willingness to learn** with **visible work** and **explicit quality expectations**.
* Short cycles help when feedback changes what the team understands.
* Careful design and checks help it make the resulting changes **safely**.

---

## Summary: Scrum, Kanban and Our Result

* Scrum and Kanban are **different ways to organise** work.
* A board, meeting or estimate has little value if the team **cannot explain how it affects the next action**.
* Our result: a draft backlog with **clear stories, observable examples, shared completion conditions and a workflow**.
* It **distinguishes inherited capability from new work** and records open decisions.

---

## Next: Chapter 4

* **Chapter 4: From Requirements to an Iteration.**
* Use these documents to **define project scope** and **slice features**.
* Prepare the **kickoff milestone**.
* Establish a **reproducible repository** and an **initial CI workflow**.

---

## Sources and Further Reading

1. **Agile Manifesto authors:** *Manifesto for Agile Software Development* and *Principles behind the Agile Manifesto*, 2001.
2. **Schwaber and Sutherland:** *The Scrum Guide*, November 2020.
3. **Kanban Guides contributors:** *The Kanban Guide*, May 2025.
4. **Jeffries:** *Essential XP: Card, Conversation, Confirmation*, 2001.
5. **Wake:** *INVEST in Good Stories, and SMART Tasks*, 2003.
6. **Martin:** *Agile Software Development*, 2002. **Rubin:** *Essential Scrum*, 2012.

* Full references and links are in the chapter text.
