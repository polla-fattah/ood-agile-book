---
title: "Chapter 1: Developing Software That Can Change"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 10
type: slides
layout: page
---

# Chapter 1: Developing Software That Can Change
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **1.1 A working program meets a new requirement**
  * One small Java rule, and a change that the rule cannot absorb by editing numbers.
* **1.2 Behaviour, quality and maintenance**
  * What "it works" leaves out, and the kinds of change a team makes.
* **1.3 Object-oriented development and iterative delivery**
  * Responsibilities, iterations, increments, and how design meets process.
* **1.4 Testing, review and feedback**
  * Acceptance examples, regressions and the evidence a reviewer can use.

---

## Chapter Roadmap (2 of 3)

* **1.5 AI assistance and human judgement**
  * Activity 1A: separating the claims a code explanation gets right from the one it invents.
* **1.6 The running example and the semester route**
  * The Campus Equipment Lending System, its vocabulary and how the chapters build on each other.
* **1.7 How to study and read critically**
  * Predicting before running, keeping a learning record, reading advice as a claim.
* **1.8 Common mistakes**
  * Five mistakes, each exposed by a small counterexample.

---

## Chapter Roadmap (3 of 3)

* **1.9 Readiness diagnostic and practical task**
  * Tasks A, B and C: predict, find a fault, plan the staff change.
* **1.10 Review questions and a transfer challenge**
  * Six questions, then a room-booking change in a different domain.
* **1.11 Chapter summary**
  * What to carry into Chapter 2, which examines how objects protect their state.

---

## Learning Outcomes

After working through this chapter, you should be able to:

1. Explain why a functioning program may still be difficult to maintain.
2. Describe how object-oriented design, iterative delivery, testing and review contribute to a controlled change.
3. Read a small Java class and distinguish its actual behaviour from assumptions about the larger system.
4. Identify evidence needed to evaluate a proposed change or an AI-generated explanation.
5. Use the book's learning route and a readiness diagnostic to plan your study.

---

## Reading Route

* **Core reading:** Sections 1.1 to 1.8.
* **Minimum required lab:** Task A, Task B (the paper part), Task C and Activity 1A.
  * Together they produce every item in "What to produce".
  * Everything can be done by tracing the code on paper.
* **Optional extension:** run the program and the deliberate fault (needs a Java Development Kit), then answer the review questions and the transfer challenge.

---

## Prerequisites and Status of This Chapter

* **Prerequisites:** basic familiarity with variables, conditions, methods and classes.
* **Not needed yet:** design patterns, a testing framework or an Agile project-management tool.
* If Java syntax is unfamiliar, read the explanation beside each example, then the Java reading in the sources. Appendix A has a short Java refresher and a readiness diagnostic.
* This is an **orientation chapter**. It adds no teaching week and previews ideas that later chapters teach in full.
* Its code is a **Book project** orientation example: `ReservationRules` stays outside the cumulative Campus Equipment Lending code, which starts with the Chapter 2 starter.

---

## Opening Scenario: A Program That Works

* A university lends cameras, microphones and other equipment to students.
* Your team has written a small program that decides whether a student may request another reservation.
* It checks two things: the **number of active reservations** and the **requested duration**.
* The examples you tried produce the expected answers.
* So far, nothing is wrong.

---

## Then the Equipment Officer Asks for a Change

> Staff should also be able to borrow equipment, but their reservation limits will be different. The existing student limits should stay the same.

* The change sounds simple. Perhaps one more condition and two new numbers.

---

## The Questions the Change Raises

* **Where** do the current limits appear?
* **How** will the program know whether a borrower is a student or a staff member?
* **Which** existing behaviours must be preserved?
* **What evidence** will show that the new rule works?
* None of these can be answered by looking only at the new numbers.

---

## Why This Book Starts Here

* We will build software, and we will also examine how it is **understood, tested, reviewed and changed**.
* The goal is to make decisions that:
  * another developer can **inspect**, and
  * the team can **revise** when requirements develop.
* Every chapter returns to the same habit: state a claim, then name the check that could show it to be wrong.

---

# 1.1 A Working Program Meets a New Requirement
### One small rule and a change it cannot absorb

---

## The Initial Rules

The equipment office gives us three rules:

* A student may have **at most three** active reservations.
* A requested loan lasts from **one to seven days**, inclusive.
* A request is **rejected** if the supplied active-reservation count is negative.

These are fictional teaching rules for our project, not university policy.

---

## What the Count Means

* **Active reservation:** a confirmed reservation that has not been cancelled or completed.
* The count passed to the method is the count **before** the proposed reservation is added.
* The **caller** must obtain that count correctly.
* The method receives two integers. It never sees a borrower, an item or a calendar.

---

## The Class: `ReservationRules`

```java
public final class ReservationRules {
    public boolean mayRequest(int activeReservations, int requestedDays) {
        return activeReservations >= 0
                && activeReservations < 3
                && requestedDays >= 1
                && requestedDays <= 7;
    }
}
```

* A complete class: one method, two integer inputs, one Boolean result.

---

## Reading the Class

| Piece | What it does |
|---|---|
| `ReservationRules` | Groups a rule calculation under one name |
| `mayRequest` | Receives two integers, returns `true` or `false` |
| `&&` | Requires **all four** conditions to hold |
| `public` | Makes the class and method accessible to other code |
| `final` | Prevents the class from being subclassed |

* Neither `public` nor `final` proves that the rule is correct.

---

## One Boundary Deserves Attention

* `activeReservations < 3`: a borrower with **two** active reservations may request a third.
* A borrower who already has **three** may not request a fourth.
* Writing `<= 3` would allow **one reservation too many** if the successful request were then confirmed.
* The count is measured *before* adding the new reservation. That is why the test is "less than three".

---

## Five Calls, Traced

| Existing | Days | Result | Reason |
|---:|---:|---|---|
| 2 | 7 | `true` | One more reaches the limit; seven days is allowed |
| 3 | 7 | `false` | Already at the reservation limit |
| 0 | 0 | `false` | A zero-day loan is outside the range |
| 0 | 8 | `false` | Eight days exceeds the duration limit |
| -1 | 2 | `false` | The supplied count is invalid |

---

## What `true` Does and Does Not Mean

| `true` establishes | `true` does not establish |
|---|---|
| The count is non-negative and below three | A borrower was identified |
| The duration is from one to seven days | The camera is available on those dates |
| Nothing more | A reservation was stored |

* A larger application must perform the other checks before confirming a reservation.

---

## The Risk of a Suggestive Name

* Method names can suggest more than their implementations establish.
* A developer who reads `true` as **"the reservation is confirmed"** may introduce a defect.
* The class itself behaves **exactly as written**. The defect lives in the reader's assumption.
* Habit for the whole book: state what a result does **and does not** establish.

---

## A Deliberate Simplification

* Returning `false` for a negative count treats an **impossible input** like an ordinary refusal.
* A caller bug can then look like a policy decision.
* We accept this here to keep the example small.
* Chapter 5 returns to **contracts**, and to how code should respond when a caller breaks them.

---

## The Changed Requirement, Clarified

> Students keep three active reservations and seven days. Staff may have up to five active reservations and request up to fourteen days.

* Students: **3** reservations, **7** days (unchanged).
* Staff: **5** reservations, **14** days (new).

---

## Why Editing the Numbers Fails

* Replacing `3` with `5` and `7` with `14` makes the method **more permissive for everyone**.
* A student with zero reservations requesting **eight days** is now accepted. That is a regression.
* Student with four reservations requesting one day: also accepted, and wrongly.
* The method receives **no borrower category**, so it cannot tell students from staff by its inputs.

---

## Before Editing: Three Questions

1. **How** is the borrower category established?
2. What should happen if the category is **missing or unknown**?
3. Which student behaviours must be **checked again** after the change?

* The answers come from the requirement, not from the original code.

---

## Do Not Guess the Unknown Case

* Do not silently decide that every unrecognised borrower receives the **staff** allowance.
* That is a **requirements decision**, not a fact we can infer from the original code.
* Related questions to raise with the equipment officer:
  * How is the category obtained?
  * What if someone holds both roles?
* Ask, and record the answer.

---

## Several Possible Implementations

| Approach | What it asks of the code |
|---|---|
| An explicit category and a small conditional | Direct, but repeated category tests may spread |
| A separately selected limit passed into the calculation | Moves selecting and validating limits to the caller |
| Give the policy its own responsibility | Worth considering as variations emerge |

* Each approach creates different obligations for callers and different places for mistakes.

---

## A Proportionate Choice

* At this stage we do **not** need to select a design pattern.
* We need to:
  * understand the rule,
  * **preserve student behaviour**, and
  * choose a proportionate implementation.
* Chapters 5 and 6 return to this kind of problem with more precise design tools.

---

## Discussion: What Would You Ask the Equipment Officer?

* Write down three questions before any code is changed.
* Prompts:
  * Where does the category come from, and can a caller simply claim it?
  * What happens to a request whose category is unknown?
  * Is there anyone who is both student and staff?
* Real callers must not grant privileges merely because a user **claims** a category.

---

# 1.2 Behaviour, Quality and Maintenance
### Does it work, and how hard will it be to change?

---

## "Does It Work?" Needs a Condition

* To answer usefully we must say **what behaviour is expected** and **under which conditions**.
* For the reservation rule: an expected result for a seven-day student request.
* For the complete application we also need expectations about:
  * equipment availability,
  * recording reservations,
  * reporting failures.
* A successful demonstration of one request does not answer all of those questions.

---

## Maintainability

* A further question: how difficult will the software be to change **correctly**?
* **Maintainability** is our ability to **understand, diagnose, test and modify** software over its useful life.
* In this book we look for **practical evidence** of that ability.
* It is not a label attached to a diagram.

---

## One Decision, Three Places

* The seven-day limit appears in:
  * a command-line screen,
  * a reservation service,
  * a report generator.
* A developer updates **two** locations and misses the third.
* Each expression may be easy to read, yet the system is difficult to change consistently.
* The problem lies in **how one decision is represented** across the codebase.

---

## The Codebase Is More Than Source Code

* A **codebase** is the body of source code and supporting material that the team maintains together.
* Its **tests, build instructions and configuration** affect whether another person can work with it.
* A clear method inside a project that no one else can build is only part of a maintainable solution.

---

## Making Quality Claims Concrete (1 of 2)

| Concern | Question to investigate | Useful evidence |
|---|---|---|
| Functional behaviour | Are the stated rules enforced? | Examples and tests linked to those rules |
| Modifiability | Can one policy change be made without unrelated edits? | A reviewed change and an explanation of affected responsibilities |
| Understandability | Can another developer say where the decision is made? | A walkthrough backed by accurate names |

---

## Making Quality Claims Concrete (2 of 2)

| Concern | Question to investigate | Useful evidence |
|---|---|---|
| Testability | Can the rule be checked with controlled inputs? | Repeatable checks that need no live university service |
| Failure handling | What happens when required information is unavailable? | Explicit expectations and checks for the failure path |

* These concerns **interact**.
* Moving a rule into its own component can ease testing; many tiny components can make navigation harder.
* Explain a design choice by the problem it solves **and the cost it introduces**.

---

## Kinds of Change

| Change | Nature |
|---|---|
| Correcting a wrong limit | Changes behaviour to **meet the requirement** |
| Adding staff borrowing | Introduces **new behaviour** |
| Improving internal organisation, same observable behaviour | **Refactoring** (the distinction follows Fowler) |

* Keeping these intentions separate makes review easier.
* A reviewer should know whether a changed result is **deliberate or accidental**.

---

## What Is Expected of You

* You will **not** be expected to make the project ready for every possible future.
* You will be expected to:
  * **state its assumptions**, and
  * respond thoughtfully when a relevant assumption changes.

---

# 1.3 Object-Oriented Development and Iterative Delivery
### Where design and process meet

---

## Objects and Responsibilities

* Object-oriented development organises software around objects with **state, behaviour and responsibilities**.
* A **responsibility** is an obligation assigned to part of the system. For example:
  * representing a loan period,
  * deciding whether a borrower is eligible,
  * recording a confirmed reservation.

---

## A Class Is Not Automatically a Good Design

* Putting code inside a class does not create a useful design. A class can still:
  * contain **unrelated decisions**,
  * **expose information** that callers can misuse,
  * depend on details **scattered** through the application.
* Chapter 2 examines these problems through **encapsulation, cohesion and coupling**.

---

## Keeping Meanings Clear

* In the equipment-lending domain, an **equipment item** and a **reservation** are different things.
* The item is something the university **owns**.
* The reservation is an arrangement concerning that item **for a period**.
* Keeping these meanings clear helps the team discuss requirements before it decides which fields or methods are needed.

---

## Iteration and Increment

* An **iteration** is a repeated period of work and feedback.
* An **increment** adds usable capability to what already exists.
* A team can improve a reservation workflow over several iterations while delivering successive increments of functionality.
* One iteration might **refine** a flow without adding a new feature, so the terms are not interchangeable.

---

## Agile Principles in One Sentence

* The Agile principles connect **frequent delivery and adaptation** with continuing attention to **technical quality**.
* They also call for teams to **reflect and adjust** their way of working.
* The implication for our project is practical:
  * feedback should influence **what we build** and **how we build it**.
* This chapter does not yet teach a complete Agile framework (Chapter 3 does).

---

## A Demonstration Reveals a Mismatch

* Suppose an early demonstration shows that the equipment officer uses **"reservation"** to mean a confirmed allocation.
* The team has used it for an **unapproved request**.
* The feedback can change names, states and user messages.
* Found in a **small working increment**, the mismatch gives a concrete example and a bounded amount of code to revise.

---

## Design and Process Meet at the Change

* **Planning** decides which behaviour the team intends to deliver.
* **Design** decides where its decisions belong.
* **Tests and review** help determine whether the implementation matches those intentions.
* **Feedback** may revise the intentions, or reveal a weakness in the structure.

---

## Figure 1.1: A Change Moves Through a Cycle

<!--svg:ch01-cycle-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 350" role="img" aria-label="Figure 1.1: clarify the change, choose a small implementation, run checks and review, then ask whether the evidence supports acceptance. No: inspect the mismatch and return to clarify. Yes: demonstrate the increment, gather user feedback and return to clarify." style="display:block;width:100%;height:calc(var(--u) * 35.00);margin:0 auto">
<defs><marker id="ch01-cycle-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch01-cycle-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch01-cycle-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch01-cycle-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch01-cycle-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="20.0" width="230.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="125.0" y="49.6" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Clarify the</text>
<text x="125.0" y="73.3" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">requested change</text>
<rect x="300.0" y="20.0" width="230.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="415.0" y="49.6" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Choose a small</text>
<text x="415.0" y="73.3" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">implementation</text>
<rect x="590.0" y="20.0" width="230.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="705.0" y="49.6" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Run checks</text>
<text x="705.0" y="73.3" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">and review</text>
<polygon points="705.0,150.0 825.0,200.0 705.0,250.0 585.0,200.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="705.0" y="195.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Evidence supports</text>
<text x="705.0" y="216.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">acceptance?</text>
<rect x="300.0" y="175.0" width="230.0" height="50.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="415.0" y="206.1" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Inspect the mismatch</text>
<rect x="585.0" y="288.0" width="240.0" height="56.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="705.0" y="311.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Demonstrate</text>
<text x="705.0" y="332.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">the increment</text>
<rect x="300.0" y="288.0" width="230.0" height="56.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="415.0" y="311.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Gather</text>
<text x="415.0" y="332.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">user feedback</text>
<path d="M240.0,55.0 L300.0,55.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch01-cycle-arr)"/>
<path d="M530.0,55.0 L590.0,55.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch01-cycle-arr)"/>
<path d="M705.0,90.0 L705.0,150.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch01-cycle-arr)"/>
<path d="M585.0,200.0 L530.0,200.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch01-cycle-arr)"/>
<text x="557.0" y="192.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">No</text>
<path d="M300.0,200.0 L171.0,200.0 L171.0,90.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch01-cycle-arr)"/>
<path d="M705.0,250.0 L705.0,288.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch01-cycle-arr)"/>
<text x="738.0" y="276.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Yes</text>
<path d="M585.0,316.0 L530.0,316.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch01-cycle-arr)"/>
<path d="M300.0,316.0 L67.5,316.0 L67.5,90.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch01-cycle-arr)"/>
</svg>
</div>
<!--/svg-->

---

## Reading the Figure

* A mismatch may reveal a **defect**, a **mistaken expectation** or an **unclear requirement**.
* User feedback can begin another cycle after the increment is accepted.
* The diagram is a **learning model**, not a mandatory sequence where each activity happens once.
* In practice a developer may clarify a detail while writing a test, or revisit design during review.

---

# 1.4 Testing, Review and Feedback
### What would make us willing to accept the change?

---

## Acceptance Examples

* **Acceptance examples** are concrete situations with expected outcomes, agreed from the requirement.
* Examples are agreed **before** the change is trusted.
* They make the **distinction between categories** visible.
* They stop us validating the change using only staff cases and forgetting existing student behaviour.

---

## Acceptance Examples for the Staff Change

| Borrower | Existing count | Days | Eligible under the numeric rules? |
|---|---:|---:|---|
| Student | 2 | 7 | Yes |
| Student | 3 | any | No |
| Staff | 4 | 14 | Yes |
| Staff | 5 | any | No |

* They do **not** resolve an unknown borrower category. That still needs clarification.

---

## Automated Tests and Regressions

* An **automated test** performs a check repeatedly and compares observed behaviour with an expected result.
* A **regression** is an unintended loss or alteration of behaviour that previously worked.
* Regression checks help reveal such changes.
* Their usefulness depends on **what they examine** and **whether their expectations are correct**.

---

## A Test That Misses the Boundary

```java
// original
&& requestedDays <= 7;

// accidental change
&& requestedDays < 7;
```

* A test of a **two-day** request passes with both versions.
* A **seven-day** request exposes the difference: `true` becomes `false`.
* Both versions compile.

---

## Compiling Is Not Checking Policy

* The compiler checks **language rules**.
* It does not know that the equipment office permits seven days.
* So a successful compile tells us the source is well formed, nothing more.
* Which brings us to the question: what **evidence** do we have?

---

## Several Kinds of Evidence (1 of 2)

| Evidence | Can help establish | Does not establish by itself |
|---|---|---|
| Successful compilation | The source satisfies the compiler's checks | The program implements the requested policy |
| Passing behavioural tests | The tested cases match their expected results | All relevant cases were identified correctly |
| Code review | Another person examined decisions, changes and risks | Every defect was discovered |

---

## Several Kinds of Evidence (2 of 2)

| Evidence | Can help establish | Does not establish by itself |
|---|---|---|
| User demonstration | The workflow can be inspected against user expectations | Untested failure paths work correctly |
| Version history | The team can see what changed and why | Each recorded change was necessary or correct |

* No row is a guarantee beyond its **scope**.
* Strong decisions combine several kinds.

---

## A Review Connects the Evidence

* A reviewer might ask:
  * Why is the staff category trusted?
  * Does the student boundary remain covered?
  * Does the explanation match the **actual diff**?
* A **diff** is a comparison showing changes between versions of files.
* It gives the discussion a concrete object: precisely what is being proposed.

---

## Useful Feedback

| Weak feedback | Useful feedback |
|---|---|
| "This is bad design." | "The fourteen-day limit is repeated in two places, so the next change could leave them inconsistent." |

* Feedback should lead to an **action** or a **justified decision**.
* Good feedback names a **problem and its consequence**.

---

## How the Evidence Will Grow

* **Chapter 7** develops automated testing and test-driven development.
* **Chapter 11** examines safe changes to unfamiliar code.
* **Chapter 13** checks interactions between components and introduces delivery pipelines.
* Here the essential habit is: **match each claim with a check that could reveal it to be wrong**.

---

# 1.5 AI Assistance and Human Judgement
### Candidate contributions to examine

---

## AI Output Is a Candidate Contribution

* An AI coding assistant may:
  * offer an explanation,
  * suggest an implementation,
  * propose test cases,
  * review a change.
* These are useful **candidates to examine**.
* They do not automatically settle what the system should do, or whether an answer is correct.

---

## What a Vendor's Own Documentation Says

* GitHub's documentation for Copilot inline suggestions warns that a suggestion can **look valid and still be incorrect**.
* It says users are responsible for **reviewing and validating** suggestions before accepting them.
* This is guidance about **one tool**, not evidence that every model behaves identically.
* In this book we apply the same review discipline to **any** candidate output.

---

## Activity 1A: Evaluate a Candidate Explanation (1 of 2)

| Element | For this activity |
|---|---|
| Engineering objective | Decide which statements the code actually supports |
| Input | The class in Section 1.1 and its three stated rules |
| Permitted scope | Judge this one method; do not rewrite it |

---

## Activity 1A: Evaluate a Candidate Explanation (2 of 2)

| Element | For this activity |
|---|---|
| Independent checks | The code, a hand trace of two inputs, the stated rules |
| Accept or reject | Accept what evidence supports, reject what it contradicts, mark the rest undetermined |
| No-account route | The candidate output is all you need |

---

## What Kind of Output Is This?

* The candidate output on the next slide is an **author-written teaching example** of a plausible AI response.
* It was **constructed for this exercise**. It is not a recorded output from a particular model.
* Do not present it as evidence about any real model's performance.

---

## The Candidate Output

> The method permits a request only when the active-reservation count is non-negative and below three, and the requested duration is between one and seven days inclusive. It returns a Boolean result. Before returning true, it consults the equipment database to confirm that the requested item is available.

---

## Break It into Claims

For each claim, record:

1. Whether the code **supports** it, **contradicts** it, or provides **insufficient information**.
2. The **expression, input or operation** that justifies your decision.
3. Any further information needed to make a **broader claim** about the application.

* Then write a corrected explanation in two or three sentences.
* Preserve the accurate parts. Do not reject everything because one part is wrong.

---

## Worked Answer: Claim Classification

| Claim | Verdict | Evidence |
|---|---|---|
| Count non-negative and below three | Supported | `activeReservations >= 0 && activeReservations < 3` |
| Duration from one to seven days, inclusive | Supported | `requestedDays >= 1 && requestedDays <= 7` |
| Returns a Boolean result | Supported | Return type `boolean` |
| Consults the equipment database | **Contradicted** | The body has only comparisons and a `return` |

---

## Why the Database Claim Fails

* The method receives **neither an item identifier nor a period**.
* It performs **no call** to any database or availability service.
* The larger application's availability behaviour is **unknown** from this class.
* Keep the scope precise:
  * "this method does not query a database" is **true**;
  * "the whole application never queries a database" is **not established**.

---

## A Corrected Explanation

> The method returns true when the supplied count is non-negative and below three, and the requested duration is from one to seven days inclusive. It does not change state or create a reservation. Availability and the accuracy of the supplied count must be handled elsewhere.

---

## The Key Skill Is Locating Evidence

* The presence of a database elsewhere in a real application would **not** establish that this method consults it.
* A missing database call in this class would **not** prove that no other component ever checks availability.
* Strong answers separate **local behaviour** from **system assumptions**.

---

## Optional: Using a Live Assistant

* The supplied example is sufficient. If live AI use is permitted and available, an optional prompt is:

> Explain only the behaviour visible in this Java class. Identify its inputs, returned result and any state changes. Separate facts visible in the code from assumptions about its caller. Do not invent surrounding services or rewrite the program.

---

## Checking a Live Response

* Provide the class and compare the response with **your own trace**.
* A confident explanation still needs checking.
* A careful prompt does **not** guarantee a correct answer.
* Record:
  * the **tool** used,
  * the **claim** you accepted or rejected,
  * the **evidence** behind that decision.

---

## The Shared-Misunderstanding Danger

* If the same misunderstood requirement influences **both an implementation and its tests**, they may agree with each other.
* They can then **both disagree with the intended policy**.
* Reviewing expected results against a **clarified requirement** is necessary even when all generated tests pass.

---

## Rules for AI Use in This Book

* Use **synthetic project data**.
* Follow the module leader's current rules for permitted AI use in assessments.
* Every AI exercise has a route that **does not require a paid service**.
* Chapter 15 collects the recurring workflows and is meant to be consulted alongside any chapter.
* This chapter's activity is **self-contained**.

---

# 1.6 The Running Example and the Semester Route
### The Campus Equipment Lending System

---

## The Running Example

* Throughout the book we develop the **Campus Equipment Lending System** in Java.
* The first useful system supports a small set of activities:
  1. inspect availability,
  2. request a reservation,
  3. confirm an eligible request,
  4. issue the equipment,
  5. record its return.

---

## Starting Simple

* We begin with a simple interface and data held **in memory**.
* This keeps early examples focused on **domain behaviour**.
* Later chapters introduce the boundaries needed to work with storage and external services.
* The opening `ReservationRules` is a small orientation example, **not** the completed application and not a promise that its structure will remain unchanged.

---

## Orientation Code vs. the Cumulative Project

* `ReservationRules` is a **separate teaching example**.
* The cumulative project begins with the **Chapter 2 starter**.
* Each later chapter states whether its code **joins that project** or stays on a **separate teaching branch**.
* Appendix D lists, for every chapter:
  * where the project stands,
  * which count a build should report,
  * the rules of the domain.

---

## Domain Vocabulary

| Term | Meaning in the book |
|---|---|
| Borrower | A person seeking permission to borrow equipment |
| Equipment item | One individually identifiable piece of equipment |
| Reservation | A recorded arrangement for an item over a period, whose status matters |
| Loan | The actual issue of an item to a borrower, followed by its return |
| Loan period | The intended interval during which the item is borrowed |

---

## Reservation vs. Loan

* A reservation and a loan are **related but distinct**.
* A confirmed reservation can exist **before** the borrower collects the equipment.
* **Cancelling** a reservation is different from **returning** an item already issued.
* Confusing the two is the kind of mismatch a demonstration should expose early.

---

## Initial Scope

* One item per reservation.
* Explicit periods.
* Synthetic borrowers.
* Once we represent actual dates and times, we must define:
  * **when periods overlap**, and
  * whether one period can **begin exactly when another ends**.
* The integer duration in Section 1.1 does not settle those calendar rules.

---

## Invariants

* We will preserve **invariants**: conditions the domain requires to remain true during valid operation.
* Examples:
  * a valid loan period,
  * no conflicting confirmed reservations for the same item and period,
  * no return operation on an inactive loan.
* These guide the evolving implementation. The small rule class has **not** already implemented all of them.

---

## How the Chapters Build on One Another (1 of 2)

| Reading | Main development in your understanding |
|---|---|
| Chapters 2 to 4 | Objects and responsibilities; a backlog; a shared delivery workflow |
| Chapters 5 to 7 | Improve responsibilities and dependencies; develop behaviour with useful automated tests |
| Chapters 8 to 10 | Evaluate recurring design solutions; organise a modest application |

---

## How the Chapters Build on One Another (2 of 2)

| Reading | Main development in your understanding |
|---|---|
| Chapters 11 to 13 | Improve unfamiliar code; interpret project evidence; implement a changed requirement across integration boundaries |
| Chapter 14 | Evaluate the result, document decisions, prepare a reproducible handover |
| Chapter 15 | Consult AI-assisted engineering methods alongside the relevant chapters |

---

## Project Checkpoints

* Chapters 2 to 14 follow the thirteen teaching weeks. This introduction and Chapter 15 add none.
* Checkpoints for the team project:
  * **Week 3:** kickoff.
  * **Week 6:** a minimum viable product.
  * **Week 9:** patterns and application structure.
  * **Week 12:** a verified response to changed requirements.
* The later assessment change is introduced in **Week 11**.

---

## Book Project and Team Project

* The book's worked system provides **shared examples**.
* Each practical activity says whether it runs on the **Book project** or on your **Team project**.
* Teams choose a domain the module provides. Equipment lending and an ML model-serving tool are examples.
* If your team uses another domain its change requests will differ, so each chapter ends with a **transfer note**.

---

## Transfer, Not Copying

* Learn the reasoning well enough to apply it elsewhere.
* Copying an equipment-related class name into another project does **not** establish that the responsibility belongs there.
* The question to ask each time: **what problem made this structure useful?**

---

## AI and Data Components

* The module aims to prepare you to build **reliable software around AI and data components**.
* The running project reflects that. It does **not** require training a model.
* The book takes the data-backed route. Its collaborator is the **equipment directory**.
* The directory answers: *"who is this borrower, and which category are they in?"* from outside the application.
* The domain code depends on it only through a **contract**.

---

## Meeting the Equipment Directory in Steps

| Chapter | What happens to the directory |
|---|---|
| 6 | Previews the contract |
| 7 | Shows how a test substitutes it |
| 8 | Builds the adapter that translates the provider's codes |
| 10 | Places it in the application structure |
| 13 | Adds what a real provider needs: timeouts and an explicit fallback-or-failure policy |

---

## What the Book Is Not

* If your project uses a model-serving domain, the same questions apply to **the component that calls the model**.
* Using **AI to help write software** is a different topic. Chapter 15 covers it.
* Neither turns this book into a machine-learning implementation course.

---

# 1.7 How to Study and Read Critically
### Predict, record, evaluate

---

## Predict Before You Execute

1. Select one **ordinary** case and one case **near a limit**.
2. Trace the decisions.
3. Write the expected result.
4. Only then compare it with the program's output.

* A mismatch is an opportunity to find out whether your **understanding**, the **code** or the **requirement** needs correction.

---

## Reading a Worked Design

* Ask what **problem** made the additional structure useful.
* If the chapter introduces a **new class**, identify the responsibility it receives.
* If it introduces an **interface**, identify the caller that benefits from it.
* If you cannot name the benefit, **reread the problem** before copying the solution.

---

## Keep a Learning Record

For each practical session, three entries:

1. The **decision** you made.
2. The **evidence** you used.
3. The **uncertainty** that remains.

| Describes an action | Explains intent and evidence |
|---|---|
| "I changed the condition." | "I retained the student limit and checked requests at two and three existing reservations." |

---

## Reading Software-Engineering Advice

* Technical books recommend practices for **particular circumstances**.
* Read recommendations as **claims to understand and evaluate**.
* Hypothetical statement: *"Give every class an interface."* Ask:
  * Which callers need interchangeable behaviour?
  * What coupling does the interface reduce?
  * Does the extra file make this example easier to understand?
* Criticise the **strongest reasonable interpretation**, not an exaggerated version.

---

## The Reading Record (1 of 2)

| Entry | Question |
|---|---|
| Claim and location | What exactly does the author recommend, and where? |
| Context | What problem and assumptions surround the advice? |
| Supporting example | How does the example demonstrate the claimed benefit? |

---

## The Reading Record (2 of 2)

| Entry | Question |
|---|---|
| Limitation | Under what conditions might the cost outweigh the benefit? |
| Project application | What would change if we applied it to our system? |
| Further evidence | Which independently checked source or experiment helps evaluate it? |

---

## The Critical Review Assignment

* The module includes an **individual critical review** of a book from the approved software-design and Agile-engineering list, **due in Week 8**.
* It asks you to:
  * evaluate the book's principles and examples,
  * discuss their trade-offs and limits,
  * consider how they apply to engineering **AI-enabled systems**, supported by additional sources.
* Follow the current assignment brief for exact requirements. Appendix E develops the review method.

---

## What This Textbook Does Not Replace

* This textbook does **not** replace the book you select.
* An **AI summary of a book you have not read is not evidence about it**.
* Begin reading early.
* The reading record above is enough to start a useful record now.

---

# 1.8 Common Mistakes
### Each exposed by a small counterexample

---

## Mistake 1: Reading `true` as "Confirmed"

* **Mistake:** reading `true` as "the reservation is confirmed".
* **Counterexample:** `mayRequest(0, 1)` returns `true` even if the camera is already reserved for that day.
* **Better habit:** state what a result does and does not establish.

---

## Mistake 2: Changing the Numbers

* **Mistake:** changing the numbers to add the new behaviour.
* **Counterexample:** replacing `3` and `7` with `5` and `14` accepts a student request for eight days.
* **Better habit:** preserve existing cases while adding the new ones.

---

## Mistake 3: Treating Passing Tests as Proof

* **Mistake:** treating passing tests as proof.
* **Counterexample:** a test that expects students to borrow for fourteen days passes beside an implementation with the same error.
* **Better habit:** check expected results against the clarified requirement.

---

## Mistake 4: Trusting a Fluent Explanation

* **Mistake:** trusting a fluent explanation.
* **Counterexample:** Activity 1A's explanation mixes accurate claims with an invented database call.
* **Better habit:** locate the code or requirement behind each claim.

---

## Mistake 5: Assuming the Edit Is Local

* **Mistake:** assuming the edit is local.
* **Counterexample:** the seven-day limit may also appear in a screen and a report.
* **Better habit:** search for where each decision is represented before editing.

---

# 1.9 Readiness Diagnostic and Practical Task
### Tasks A, B and C

---

## What the Diagnostic Is

* It helps identify what you need to **practise**.
* It is **not** a new graded assessment.
* It runs on the **Book project**: the Java class in Section 1.1, its stated rules and the staff change are your materials.
* No team code is needed.

---

## Task A: Predict the Results

Without running the code, predict each result and name the condition that explains it.

| Call | Your predicted result | Your reason |
|---|---|---|
| `mayRequest(0, 1)` |  |  |
| `mayRequest(2, 7)` |  |  |
| `mayRequest(3, 1)` |  |  |
| `mayRequest(1, 8)` |  |  |
| `mayRequest(-1, 1)` |  |  |
| `mayRequest(1, 0)` |  |  |

---

## Task A: Also Identify

* The **class name**, **method name**, **parameter types** and **return type**.
* Whether a call **modifies a reservation count** or **records a new reservation**.
* If a keyword is unfamiliar, distinguish that **syntax gap** from a difficulty understanding the **rule**.

---

## Task A: Answers

| Call | Result | Reason |
|---|---|---|
| `mayRequest(0, 1)` | `true` | Count and duration are within range |
| `mayRequest(2, 7)` | `true` | One more is allowed; seven days is inclusive |
| `mayRequest(3, 1)` | `false` | Three existing already reach the limit |
| `mayRequest(1, 8)` | `false` | Eight days exceeds the student limit |
| `mayRequest(-1, 1)` | `false` | A negative count is explicitly rejected |
| `mayRequest(1, 0)` | `false` | Duration must be at least one day |

---

## Task A: Reading the Class

* Class: `ReservationRules`. Method: `mayRequest`.
* Both parameters are `int`; the return type is `boolean`.
* There are **no fields**, no assignments to shared state, no storage calls and no reservation creation.
* Calling the method neither increments a count nor reserves equipment.
* Its result is **narrower** than overall eligibility or confirmation.

---

## A Caution About `final`

* Do not teach that `final` makes all Java objects immutable.
* Here it only **prevents subclassing**.
* The relevant absence of state changes is explained by the **absence of mutable state** and by the body of the method.

---

## Task B: Examine One Small Fault

* A developer changes `requestedDays <= 7` to `requestedDays < 7`.
* Provide **one input** that distinguishes the original and the modified version.
* State **both results**.
* Explain which result agrees with the initial requirement.

---

## Task B: Answer

* `mayRequest(2, 7)` distinguishes them.
* Original: `true`. Faulty `< 7` version: `false`.
* The original agrees with the explicit **inclusive maximum of seven days**.
* Any input with seven days and a valid count from zero to two works as a counterexample.

---

## Optional Execution: The Demo Class

```java
public class Chapter01Demo {
    public static void main(String[] args) {
        ReservationRules rules = new ReservationRules();
        System.out.println(rules.mayRequest(2, 7));
        System.out.println(rules.mayRequest(3, 7));
    }
}
```

* Save the rule as `ReservationRules.java` and this as `Chapter01Demo.java`.
* `new ReservationRules()` creates the object on which the method is called.

---

## Compile and Run

```sh
javac ReservationRules.java Chapter01Demo.java
java Chapter01Demo
```

```text
true
false
```

* Run from the directory containing both files, using a Java Development Kit.
* Appendix B gives a full, reproducible development setup. Installing tools is **not** required for the paper diagnostic.

---

## Each Call Evaluates Only Its Arguments

* The first call does **not** increase any count.
* Calling `mayRequest(2, 7)` repeatedly returns the **same result**.
* The complete application would have to **update its reservation records separately**.
* Printing the returned values makes the difference visible without building a user interface.

---

## Repeatable Checks: The Runner

```java
for (int[] example : cases) {
    boolean expected = example[2] == 1;
    boolean actual = rules.mayRequest(example[0], example[1]);
    if (actual != expected) {
        throw new AssertionError("mayRequest(" + example[0]
            + ", " + example[1] + ") expected " + expected
            + " but got " + actual);
    }
}
```

---

## Repeatable Checks: The Data

```java
int[][] cases = {
    {0, 1, 1}, {2, 7, 1}, {3, 1, 0}, {1, 8, 0},
    {-1, 1, 0}, {1, 0, 0}, {3, 7, 0}, {0, 7, 1},
    {2, 1, 1}, {4, 2, 0}, {1, -1, 0}, {0, 14, 0}
};
```

* Each row: existing count, requested days, expected result (`1` means `true`).
* The conversion to Boolean is a convenience for the example, not a modelling recommendation.
* Expected output: `All 12 chapter checks passed.`

---

## Running the Checks Needs No Library

* `AssertionError` is thrown explicitly, so it works **without enabling** Java's optional `assert` statements.
* The runner stops at the **first mismatch**.
* It is not meant to teach the full testing approach. That is Chapter 7.
* The 12 checks cover the diagnostic cases and several nearby boundaries.

---

## Two Deliberate Faults, Two Failure Messages

| Edit | First failing check |
|---|---|
| `requestedDays <= 7` becomes `requestedDays < 7` | `mayRequest(2, 7) expected true but got false` |
| `activeReservations < 3` becomes `activeReservations <= 3` | `mayRequest(3, 1) expected false but got true` |

* The `(3, 7)` case would also fail, but `(3, 1)` appears earlier in the table.
* Make a temporary copy first, and **restore the original expression afterwards**.

---

## Task C: Plan the Staff Change

Write a short **change note** (no complete redesign). Include:

* The behaviour that must **remain unchanged** for students.
* The **new staff behaviour** and the extra information needed to select it.
* **One unresolved question** to clarify rather than guess.
* **At least four acceptance examples** covering both categories and their limits.
* One simple **implementation approach** and one **trade-off**.
* An **evidence statement** of two or three sentences.

---

## Task C: Suggested Acceptance Examples

| Category | Existing count | Days | Decision |
|---|---:|---:|---|
| Student | 2 | 7 | Allow |
| Student | 3 | 1 | Reject |
| Student | 0 | 8 | Reject |
| Staff | 4 | 14 | Allow |
| Staff | 5 | 1 | Reject |
| Staff | 0 | 15 | Reject |

---

## Task C: What the Examples Leave Open

* Four well-chosen examples are enough. They must cover **both categories** and **meaningful limits**.
* Negative counts and non-positive durations stay **invalid for both**.
* None of these decisions establishes **availability**.
* Counts are measured **before** the new reservation is added.

---

## Task C: A Strong Evidence Statement

> I would need the six acceptance examples to give the expected results, the original student checks to still pass unchanged, and a reviewer to confirm from the diff that student limits were not edited. This would not show that the category is trustworthy, that availability is checked, or that the examples match the equipment officer's intent.

---

## Task C: What Makes a Weak Answer

* Weak answers say only that "the code works" or that "all tests pass".
* A good evidence statement names checks that **could fail**.
* It also says what the evidence **would still not show**.

---

## Task C: Choosing an Implementation Approach

* A **small conditional with an explicit category** is an acceptable initial approach.
  * Advantage: directness.
  * Cost: repeated category conditions may spread if more policy decisions appear.
* **Passing limits into a shared calculation** can also be reasonable.
  * It moves the obligation to select and validate limits to a caller.
* Accept either with a coherent rationale. Do not reward an early interface hierarchy just for using patterns.

---

## What to Produce

Submit or retain, as your instructor directs:

* your completed **prediction table**,
* your **fault-revealing input**,
* the short **change note** with its evidence statement,
* the **AI claim analysis**,
* the **readiness checklist**.

If you run the program, include the observed result and say which version produced it.

---

## The Task Is Complete When

* Your predictions **follow the code**.
* Your proposed change **preserves the original student rule**.
* Your acceptance examples **could reveal a boundary error**.
* Your evidence statement names checks that **could show the change to be wrong**.
* You can explain why the method alone **cannot confirm equipment availability**.

---

## Readiness Checklist

| Readiness question | Confident | Need practice |
|---|---|---|
| I can trace a Boolean expression with several conditions. | ☐ | ☐ |
| I can distinguish a method's inputs, returned result and state changes. | ☐ | ☐ |
| I can identify a case at the edge of an allowed range. | ☐ | ☐ |
| I can separate a confirmed requirement from an assumption. | ☐ | ☐ |
| I can explain what evidence supports a code explanation. | ☐ | ☐ |
| I can describe a small change and the behaviour it must preserve. | ☐ | ☐ |

---

## Choose Your Next Action

Pick one item marked "Need practice" and state your next action:

* **Syntax:** use the relevant Java tutorial (Appendix A has a refresher).
* **Tracing:** work through another input with a partner.
* **Requirements:** rewrite the rule as concrete examples and identify what remains unanswered.
* Optional extension: once your team has chosen its domain, repeat Task C for **one numeric limit** in that domain.

---

# 1.10 Review Questions and a Transfer Challenge
### Concept, diagnosis, transfer

---

## Concept Questions

1. Give an example of software that produces the expected result today but is difficult to maintain. What makes the next change risky?
2. Explain the difference between an iteration and an increment using the equipment-lending project.
3. Why does passing a set of tests provide useful but limited evidence? Include an example of an incorrect expectation.
4. Distinguish a behaviour change from a refactoring. Why should a reviewer know which one is intended?

---

## Diagnosis Questions

5. A developer replaces the student limits of three reservations and seven days with five and fourteen. Staff examples now pass. Explain why this is insufficient evidence that the requested change is correct, and give a student example that exposes the problem.
6. An AI assistant writes a method and tests for it. Every test passes, so the team accepts the change without comparing it with the equipment officer's rules. Identify the gap in the reasoning and propose a check that addresses it.

---

## Guidance: Questions 1 and 2

1. A rule duplicated across several screens and services may pass today's examples yet need **coordinated edits** tomorrow. Name the risk of **inconsistent copies**, not just "ugly code".
2. An **iteration** is a repeated period of development and feedback. An **increment** adds usable capability, such as a reservation flow. An iteration might refine a flow without adding a feature, so the terms are not interchangeable.

---

## Guidance: Questions 3 and 4

3. Tests cover **selected expectations**. A test that wrongly expects students to borrow for fourteen days can pass beside an equally wrong implementation. Compare expectations with the clarified policy.
4. Allowing staff fourteen days **adds behaviour**. Reorganising the same rule without changing outcomes is **refactoring**. Knowing the intention helps a reviewer decide whether a changed result is a defect or a feature.

---

## Guidance: Questions 5 and 6

5. A student with **zero** active reservations requesting **eight days** should still be rejected. Replacing all limits with staff limits would accept it. Staff-only checks do not protect student behaviour.
6. Tests and implementation may share the **same misunderstood requirement**. Review expected results independently against agreed examples, especially category distinctions and boundaries, then execute the relevant checks.

---

## Transfer Challenge: Room Booking

A room-booking application allows each student society up to **two** active bookings, each lasting at most **two hours**. University departments now need up to **four** active bookings, each at most **three hours**. The society rules stay unchanged.

* Prepare a change note using the method from Task C.
* State assumptions about duration values and booking status.
* Give one example that must **remain rejected** for a society but is **allowed** for a department.
* Identify one fact about room availability that these numeric rules **cannot establish**.

---

## Transfer Challenge: Guidance

* One acceptable assumption: durations are positive whole hours, and counts refer to active confirmed bookings **before** adding another.
* Raise the policy for **unknown groups** and define what "active" means.
* A society with two active bookings requesting **one hour** is rejected. A department with the same count and duration may be allowed.
* Checking a room needs a **room identity** and a **requested time interval**. Count and duration alone cannot establish that a room is free.

---

# 1.11 Chapter Summary
### What to carry forward

---

## Summary: A Working Program Is a Starting Point

* To change a program responsibly we need to:
  * understand the **requested behaviour**,
  * locate the **decisions** that implement it,
  * identify what **must remain true**.
* In the reservation example, the new requirement could not be met by editing numbers.

---

## Summary: Design, Delivery and Evidence

* **Object-oriented design** helps organise responsibilities.
* **Iterative delivery** creates opportunities to inspect useful increments and revise understanding.
* **Tests, reviews, demonstrations and version history** each contribute a different kind of evidence.
* None should be mistaken for a guarantee beyond its scope.

---

## Summary: AI-Assisted Work Needs Judgement

* A plausible explanation can combine **accurate observations** with an **invented operation**.
* Evaluate **individual claims** against the code and the requirements.
* Record **why** a contribution was accepted or rejected.

---

## Next: Chapter 2

* **Chapter 2: Object-Oriented Development Beyond Syntax.**
* How objects **protect their state**.
* How **responsibilities** are assigned.
* How **cohesion and coupling** affect the changes we make.
* The equipment-lending project gives those ideas a concrete setting, starting from the Chapter 2 starter.

---

## Sources and Further Reading

1. **Dev.java.** *Classes and Objects.* Official Java learning material on classes, methods, constructors and objects.
2. **Authors of the Agile Manifesto.** *Principles behind the Agile Manifesto*, 2001.
3. **Fowler, Martin.** *Definition of Refactoring*, 2004.
4. **GitHub Docs.** *Application card: GitHub Copilot inline suggestions.*

* Full references and links are in the chapter text.
