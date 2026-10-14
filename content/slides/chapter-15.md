---
title: "Chapter 15: AI as a Software Engineering Assistant"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 150
type: slides
layout: page
---

# Chapter 15: AI as a Software Engineering Assistant
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 2)

* **15.1 What an assistant gives you, and who stays accountable**
  * The six-step workflow behind every AI activity in the book.
* **15.2 Telling the assistant what you want: task and context**
  * A prompt is a work order, not a requirement.
* **15.3 Asking an assistant to explain: requirements and code**
  * Classify explanations claim by claim.
* **15.4 Candidate code and tests: a worked task**
  * The worked task: two rejected attempts and an accepted version.
* **15.5 Asking for a refactoring or a review**
* **15.6 How assistants fail: the patterns to recognise**

---

## Chapter Roadmap (2 of 2)

* **15.7 Privacy, dependencies and where work came from**
* **15.8 Writing down what you checked: verification records**
  * What evidence can and cannot show; a compact eight-part record.
* **15.9 Doing all of this without a live service**
* **15.10 AI habits that mislead**
* **15.11 Try it yourself: the lab and your own task**
* **15.12 Questions to think with, and a transfer challenge**
* **Summary and where to go next**
  * The appendices collect what the chapters point to.

---

## Learning Outcomes

After this chapter, you should be able to:

1. **Provide bounded context** for an AI-assisted task: what it is, what it may use, what it must not do, and what counts as done.
2. **Evaluate candidate explanations, code and tests** against evidence, claim by claim.
3. **Recognise** unsupported APIs, invented methods, unnecessary abstractions and tests that repeat the code's mistakes.
4. **Record useful provenance and verification evidence.**
5. **Complete an equivalent exercise without live AI access.**

---

## Where This Chapter Fits and Where You Start

* This is a **reference chapter that belongs to no teaching week**. It supports the module's outcomes wherever an assistant is used and adds **no separate assessed AI outcome**.
* It creates **no new deadlines, weights or marking rules**. Whether, and how, AI tools may be used in an assessment follows **the module leader's current rules**.
* **Entry version: none.** The worked example is a small separate project, **the lab**, that stands alone, compiles for Java 17 and needs only the pinned Maven toolchain of the earlier chapters.
* **The lending project is not changed:** its handover version 0.14.0 stays as Chapter 14 left it.
* The chapter is **vendor-neutral**. It does not teach prompt tricks, model internals, retrieval or agents.

---

## How to Use This Chapter

* **Core:** 15.1, 15.2, 15.4, 15.6 and 15.8.
* **Working knowledge:** 15.3, 15.5 and 15.7. **Learn the method; you do not need to memorise tools.**
* **What you must do:** **B1 to B4** (the book's project, the lab: running, tracing and diagnosis, everything supplied) and **T1 to T3** (your team's project: apply the method to your own work).
* These steps **consolidate** what the "AI in practice" activities of Chapters 1 to 14 already ask. Do B1 to B4 once, where you first need them: alongside the first AI activity, or before your final handover.
* **If you want more:** B5 to B7 and T4, the questions and the transfer challenge. **Nothing required depends on a paid account.**

---

## Opening Problem: The Confident Note

It is late. You ask an assistant for a small method, and it returns tidy code with a confident note: **"I tested this with Java 17 and it works."**

1. It compiles on your laptop. The tests it wrote pass. You commit.
2. The next morning **the pipeline fails to compile**: one call exists only from **Java 21**.
3. A reviewer asks **why the tests agree with the code** when your teammate's examples do not.
4. Another asks where a **dependency named in a `pom.xml` snippet** came from, because nobody can find it.

---

## What Was Missing

* **None of this needs a bad assistant.** Each needs only an ordinary one and a missing habit.
* The habit: treating the output as **a candidate that someone else's evidence must accept or reject**.
* This chapter collects that habit into a few workflows you have already practised in Chapters 1 to 14, shows them end to end on one small task, and says **what to write down** so the work can be reviewed.
* **AI-assisted development** (an assistant helps you build software) is the topic. Software that **contains** an AI component, such as the borrower directory, is treated where it arises and, for a model, in Appendix F.

---

## Before You Start: Five Rules (1 of 2)

1. **You are accountable.** The assistant proposes. **You decide, and you answer for what you commit.**
2. **The requirement is yours.** An assistant can ask good questions about it. It cannot decide what the equipment office wants.
3. **Keep the evidence independent.** Check the output against something the assistant did not write: the requirement, examples you wrote first, the compiler, a trace by hand. **Another assistant's opinion is not independent evidence.**

---

## Before You Start: Five Rules (2 of 2)

4. **Share the minimum.** No secrets and no personal data. Use **synthetic data**.
5. **Follow the current rules.** Whether a given tool may be used on coursework or in an assessment is decided by **the module leader's current rules, not by this book**.

---

# 15.1 What an Assistant Gives You, and Who Stays Accountable
### Candidates, not answers

---

## What an Assistant Gives You

* An assistant can explain code, suggest an implementation, propose tests, point out risks in a change and draft documents.
* Each is a **candidate contribution**: plausible text or code that **may or may not be right**.
* GitHub's documentation for one such tool says suggestions can **look valid and still be incorrect**, and the user must **review and validate** them before accepting. Users **assume the risks** of generated code: bugs, security flaws, intellectual-property questions.
* That is **one vendor's statement about one tool**. The discipline it describes is general.

---

## Where the Decisions Stay

| Question | Who answers it |
|---|---|
| What should the system do? | The **requirement owner**, with your questions. Not the assistant |
| Is this output correct? | **Evidence**: compiler, examples you wrote first, tests, a trace. Not the assistant's own claim |
| Is this the simplest design that works? | **You, in review** |
| May this tool be used for this work? | **The module leader's rules** and your institution's, not this book |
| What was accepted, and why? | **You, in a record** |

---

## The Assistant's Statement About Itself

* **"I tested it with Java 17" is a sentence, not a test.**
* The assistant's statement about itself is **a claim like any other**.
* Treat every such statement as **something to check**: an assistant that cannot run your build cannot have tested it under your settings, and one that can run something still ran **what it chose**.

---

## A Workflow in Six Steps

<!--svg:ch15-workflow-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="Figure 15.1: the six-step workflow of every AI activity. 1 Requirement and acceptance examples (yours), 2 bounded task and context, 3 candidate output, 4 independent checks. If the checks fail, return to the task. If they pass, 5 human acceptance, then 6 record." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch15-workflow-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch15-workflow-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch15-workflow-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch15-workflow-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch15-workflow-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="0.0" y="56.0" width="190.0" height="84.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="95.0" y="84.8" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">1 Requirement and</text>
<text x="95.0" y="102.9" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">acceptance examples</text>
<text x="95.0" y="121.1" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">(yours)</text>
<rect x="226.0" y="56.0" width="190.0" height="84.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="321.0" y="93.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">2 Bounded task</text>
<text x="321.0" y="113.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">and context</text>
<rect x="452.0" y="56.0" width="190.0" height="84.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="547.0" y="93.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">3 Candidate</text>
<text x="547.0" y="113.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">output</text>
<rect x="678.0" y="56.0" width="190.0" height="84.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="773.0" y="93.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">4 Independent</text>
<text x="773.0" y="113.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">checks</text>
<rect x="678.0" y="206.0" width="190.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="773.0" y="236.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">5 Human</text>
<text x="773.0" y="256.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">acceptance</text>
<rect x="452.0" y="206.0" width="190.0" height="70.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="547.0" y="246.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">6 Record</text>
<path d="M190.0,98.0 L226.0,98.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-workflow-arr)"/>
<path d="M416.0,98.0 L452.0,98.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-workflow-arr)"/>
<path d="M642.0,98.0 L678.0,98.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-workflow-arr)"/>
<path d="M773.0,56.0 L773.0,28.0 L321.0,28.0 L321.0,56.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-workflow-arr)"/>
<text x="547.0" y="20.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">fails</text>
<path d="M773.0,140.0 L773.0,206.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-workflow-arr)"/>
<text x="811.0" y="176.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">passes</text>
<path d="M678.0,241.0 L642.0,241.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-workflow-arr)"/>
<text x="4.0" y="236.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">The loop from the checks back to the task</text>
<text x="4.0" y="256.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">is where most of the work happens.</text>
<text x="4.0" y="276.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">A failed candidate is information: keep it.</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 15.1

* The first box is **yours**: derived from the requirement, **before any candidate exists**, and it is the authority the checks refer to.
* The loop from the checks back to the task is where **most of the work happens**.
* **A candidate that fails is information. Keep it.**
* Every AI activity in this book has this shape.

---

## The Activities You Have Already Done (1 of 2)

| Chapter | What the candidate was | The independent check |
|---|---|---|
| 1 | An explanation of a small method | The code and a hand trace |
| 2 | An explanation of the coordinator | A trace and the supplied checks |
| 3 | Suggested story assumptions and criteria | The stated rules and scope |
| 4 | An iteration plan | Capacity arithmetic and the gate output |
| 5 | A "make this SOLID" proposal | Compilation and exact-output checks |
| 6 | A refactoring that claimed to decouple | The source: which classes are named? |
| 7 | A query and its tests | The reviewed examples and a wrong-boundary mutation |

---

## The Activities You Have Already Done (2 of 2)

| Chapter | What the candidate was | The independent check |
|---|---|---|
| 8 | Suggested structures | The source and tests for unknown codes, outage and order |
| 9 | Strategy or State | The transition table and tests |
| 10 | A dependency review | Actual imports and compiled dependencies |
| 11 | A refactoring patch | A hand trace, a scratch copy and the characterisation suite |
| 12 | An explanation of metrics | Recalculation |
| 13 | An integration test | Faults applied to the parser |
| 14 | A README | Running every command |

* **The checks vary, and none of them is "ask another assistant".**

---

# 15.2 Telling the Assistant What You Want
### Task and context

---

## A Prompt Is a Work Order

* A work order says **what to do, with what, within what limits and in what form**. It is useful, and **it is not a substitute for the requirement**.
* If the requirement is unclear, the assistant fills the gap **with a guess**, and a fluent guess looks like an answer.
* Keep the context **small**. More text is not more help, and every extra file is something the assistant may use and something **you may have shared that you should not have**.

---

## The Five Parts of a Work Order (1 of 2)

| Part | What to say | Example from the lab |
|---|---|---|
| Task | One sentence about what is wanted | Add `earliestStart(from, days, searchDays)` that returns the earliest start date the item could be reserved |
| Context | Only the code and facts the task needs | The source of `LoanPeriod`; the bookings arrive as a `List<LoanPeriod>` |
| Constraints | The baseline and what is forbidden | Java 17; standard library only; no new dependencies |

---

## The Five Parts of a Work Order (2 of 2)

| Part | What to say | Example from the lab |
|---|---|---|
| Output | The form of the answer | The complete `AvailabilityFinder.java` and nothing else |
| Scope | What it may touch, and what it may not | Do not change `LoanPeriod`; do not reserve anything |

---

## The First Prompt of the Lab

```markdown
You are helping with a small Java task in an existing project.

Task: add a class `AvailabilityFinder` in package `assist` with a method
`Optional<LocalDate> earliestStart(LocalDate from, int days, int searchDays)`. It returns
the earliest start date, on or after `from` and within `searchDays` days, on which an item
could be reserved for `days` days, given the periods for which the item is already booked.

Constraints: Java 17, standard library only, no new dependencies.
Output: the complete source of `AvailabilityFinder.java` and nothing else.
Scope: do not change `LoanPeriod`. Do not reserve anything.
```

---

## Derive the Examples From the Requirement First

* Before you prompt, write **concrete examples** of the behaviour you expect, with inputs and results. **Derive them from the requirement and not from any code.**
* In the lab they are **nine tests written before anything was requested**.
* What makes them independent evidence is **how they were derived, not whether the assistant saw them.**

---

## Should the Examples Be in the Prompt?

* A choice with a cost either way.
* **Sharing** reviewed examples clarifies the task and often improves the output; they remain useful acceptance checks. But **a pass on examples the assistant has seen shows only that it satisfied those examples**, not behaviour beyond them.
* In the lab the examples were **not shared**, so they could be used both ways: as acceptance checks, and to judge whether the code generalises.
* The point is **not that hiding examples is the rule**. It is that the examples came first, from the requirement.

---

## A Workable Practice in Three Parts

1. State the **requirement** precisely in the prompt. Share reviewed examples if they help.
2. Add **boundary cases or properties that you derived independently**, and keep some of them undisclosed when you want to judge whether the code generalises.
3. **Never derive the expected results and the implementation from the same unexamined assumption.** That is what happens when an assistant writes the code and then its tests from that code.

---

## Ambiguity Is Yours to Remove

* The lab's first prompt says the search is **"within `searchDays` days"**. That can mean:
  * "up to and including `from + searchDays`", or
  * "**`searchDays` candidate start dates, starting with `from`**".
* The developer meant the second. **The assistant chose the first, and its tests chose the same**, so the code and the tests agreed with each other and disagreed with the developer.
* The acceptance examples were the only thing that did not share the misreading. The requirement sentence was **rewritten afterwards**.
* When an assistant guesses wrong, **ask what in your requirement allowed the guess.**

---

# 15.3 Asking an Assistant to Explain
### Requirements and code

---

## Explanations Are Lists of Claims

* An assistant's explanation of code is a list of claims, some about what the code shows and some about things **the code does not show**.
* Break it into single claims and classify each:
  * **Supported:** the code, a test or a document shows it. **Name the evidence.**
  * **Contradicted:** the code shows the opposite. Name the evidence and **write the correct statement**.
  * **Not established:** the code does not say. **Say what would be needed.**
* A useful prompt asks for exactly that separation, **and it still needs checking**.

---

## A Constructed Explanation of `VisitorGate.rejection`

> `rejection` first checks the feature flag and returns the "not enabled" text if visitors are off. It then checks that the item is CAM1 or CAM2. If the number of days is below one it returns an empty result without asking anyone, because the count and duration policy will reject it. Otherwise it reads the clock once, asks the approval source for the exact request, and rejects unless the record found matches the request and is valid at that instant. **The gate caches the record for later requests and writes each rejection to the audit log. If the approval source throws, the gate returns the "no valid sponsor approval" rejection.**

* Eight statements, mixed. **Three are wrong.** Which?

---

## Checking the Explanation (1 of 2)

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | The flag is checked first and the "not enabled" text returned | Supported | First statement of `rejection` |
| 2 | Then the item is checked against CAM1 or CAM2 | Supported | `ALLOWED_ITEMS = Set.of("CAM1", "CAM2")` |
| 3 | Fewer than one day returns empty without asking anyone | Supported | `ac4_...` asserts the register is not read |
| 4 | The clock is read once | Supported | `oneRequestReadsTheClockOnce` |

---

## Checking the Explanation (2 of 2)

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 5 | Exact request asked; rejected unless the record matches and is valid at that instant | Supported | `aSourceThatReturnsADifferentRequestDoesNotApprove`; `theWindowIncludesItsStartAndExcludesItsEnd` |
| 6 | The gate **caches** the record | **Contradicted** | No field holds a record; fields are the source, the clock and the flag |
| 7 | Each rejection is written to the **audit log** | **Contradicted** | No logger and no call that writes anywhere |
| 8 | If the source throws, the gate returns the "no valid sponsor approval" rejection | **Contradicted** | `anOperationalFailureOfTheSourceIsNotCaught` |

---

## Why the Wrong Claims Are the Dangerous Ones

* The incorrect ones are **the most believable**, because they describe things a gate like this might well do.
* The third would have produced **a wrong design decision about error handling**: it is the difference between a rejection and a failure that Chapters 12 and 13 insist on.
* Reading the code, a test and the class settles each in a minute.
* **Keep the accurate parts and correct the rest.** Do not throw away an explanation because one sentence is wrong.

---

## The Corrected Explanation

> `rejection` returns an empty result when the request may go on to the coordinator, and a rejection text otherwise. It checks the flag first, then the item, then returns empty for fewer than one day (the policy rejects it). Otherwise it reads the clock once, asks the source for the exact request and rejects unless the record matches and is valid at that instant. **It keeps no state and writes no log. If the source throws, the exception reaches the caller; nothing is reserved.**

---

## Requirements Work

* An assistant can help you **find gaps** in a requirement: what happens at the boundary, what is not said, which cases conflict.
* Use it to produce **questions**, and **take the questions to whoever owns the requirement**. Do not let it supply the rules.
* Chapter 3's exercise on a story and Chapter 11's suspected defects had the same shape: **the right output of an assistant was a question for an owner, not an answer.**

---

# 15.4 Candidate Code and Tests
### A worked task

---

## The Worked Task

* Given the periods for which an item is already booked, return the **earliest start date** on or after `from`, among **`searchDays` candidate start dates beginning with `from`**, on which it could be reserved for `days` days.
* **Periods are half-open:** a booking that ends on a date does not block a new one that starts on that date.
* **Nothing is reserved.** Invalid `days` or `searchDays` (below one) is an `IllegalArgumentException`; a null `from` or bookings list is a `NullPointerException`.
* The developer's **nine acceptance examples EX1 to EX9** were written before prompting.

---

## Acceptance Examples EX1 to EX5

Bookings: **20 to 22** and **24 to 26** October (half-open) unless stated.

| ID | Request | Result |
|---|---|---|
| EX1 | from 20, 2 days, window 10 | **22 October** (the end is exclusive) |
| EX2 | from 20, 3 days, window 10 | **26 October** (does not fit before the 24th) |
| EX3 | from 10, 2 days, window 10; and no bookings, from 10, 5 days, window 1 | 10 October |
| EX4 | from 20, 2 days, window 2 | **none** (the candidates are 20 and 21) |
| EX5 | from 20, 2 days, window 3 | **22 October** (the third candidate is included); window 2 gives none |

---

## Acceptance Examples EX6 to EX9

| ID | Request | Result |
|---|---|---|
| EX6 | booking 18 to 20 only; from 20, 2 days, window 1 | 20 October |
| EX7 | days 0, window 0, a null `from`, a null list | the exceptions above |
| EX8 | the caller's list gains a booking after construction | the finder is **unchanged** |
| EX9 | one booking covering 1 to 31 October; from 5, 1 day, window 10 | **none** |

---

## One Acceptance Example in Code

```java
/** CAM1 is booked for [20, 22) and [24, 26). */
private static AvailabilityFinder cam1() {
    return new AvailabilityFinder(List.of(period(20, 22), period(24, 26)));
}

@Test void ex4_theWindowCountsCandidateStartDatesAndNotDaysAfterFrom() {
    assertEquals(Optional.empty(), cam1().earliestStart(oct(20), 2, 2));
}

@Test void ex5_theLastCandidateInTheWindowIsIncluded() {
    assertEquals(Optional.of(oct(22)), cam1().earliestStart(oct(20), 2, 3));
    assertEquals(Optional.empty(), cam1().earliestStart(oct(20), 2, 2));
}
```

---

## Attempt 1: The Constructed Response

* **Author-written fictional AI output**, constructed to illustrate. Not a recording of a real model.
* The response claims: **"I tested it with Java 17 and it works"** and contains:

```java
List<LocalDate> free = from.datesUntil(from.plusDays(searchDays))
        .filter(start -> booked.stream()
                .noneMatch(b -> b.intersects(new LoanPeriod(start, start.plusDays(days)))))
        .toList();
return free.isEmpty() ? Optional.empty() : Optional.of(free.getFirst());
```

---

## Attempt 1: Rejected by the Compiler

Compiled with the project's baseline, `--release 17`, it fails with **two errors**:

```text
AvailabilityFinder.java:18: error: cannot find symbol
  symbol:   method intersects(LoanPeriod)
  location: variable b of type LoanPeriod
AvailabilityFinder.java:20: error: cannot find symbol
  symbol:   method getFirst()
  location: variable free of type List<LocalDate>
```

* Run it yourself: `bash scripts/try-attempt.sh 1`, or `javac --release 17` by hand.

---

## Two Different Failures

* **`intersects` is an invented method.** `LoanPeriod` has `overlaps`; `intersects` is what a similar class elsewhere might have.
* **`List.getFirst()` exists in Java 21 and not in Java 17.** It is an **API newer than the baseline**.
* Compiled with plain `javac` on a JDK 21 or later and **no `--release`**, the second one compiles. In the experiment plain `javac` reported **only the first error**; `javac --release 17` reported **both**.
* If your only JDK is 17, both commands report both errors: **the project's command is the one that matters, and it fails as it should.**

---

## What `--release` Changes

* `--release` restricts the **API as well as the language level** to the named release. `--source` and `--target` alone do not.
* The project's POM sets it to 17 through the compiler plugin's `release` parameter.
* The code "works on my machine" and **breaks on the baseline**.
* **The rule: compile and test with the project's own commands, never with the assistant's assurance or your own default settings.**

---

## Attempt 1 Under Different Settings

| Command | Result |
|---|---|
| `javac -d out1 *.java` (JDK 21 or later, no `--release`) | **One** error: `intersects` |
| `javac --release 17 -d out2 *.java` | **Two** errors: `intersects` and `getFirst` |
| After changing only `intersects` to `overlaps`: plain `javac` | **No error**: it compiles |
| After the same change: `javac --release 17` | One error: `getFirst()` |
| Maven (`maven.compiler.release` 17), `try-attempt.sh 1` | Two errors, at `[18,42]` and `[20,68]` |

* After the invented method is fixed, the code compiles where it was written and fails on the baseline.

---

## A Style Point, Not a Defect

* The code builds a list of **every** free date just to take the first one. It is correct in spirit and does more work than needed.
* That is a style point, not a defect, and it is **the reason to read candidate code and not just run it.**

---

## Attempt 2: Compiles, Passes Its Own Tests, Still Wrong

* The second work order names the two compiler findings and asks the assistant to **keep the solution small and to write tests**.
* The constructed response: *"The finder now delegates to an `AvailabilityRule`, so new rules can be added without changing it (open/closed principle). I added seven JUnit 5 tests and all of them pass. The behaviour matches your description."*
* It compiles. **Its seven tests pass.** Run the developer's acceptance examples:

```text
ex4_theWindowCountsCandidateStartDatesAndNotDaysAfterFrom: expected: <Optional.empty> but was: <Optional[2026-10-22]>
ex5_theLastCandidateInTheWindowIsIncluded: expected: <Optional.empty> but was: <Optional[2026-10-22]>
```

---

## The Loop Is One Step Too Far

* `for (int offset = 0; offset <= searchDays; offset++)`: the window examines **`searchDays + 1`** candidates.
* From the 20th with a window of 2 it examines **20, 21 and 22** and returns the 22nd.
* One of the assistant's own tests is called **`theSearchWindowIsInclusiveOfTheLastDay`** and asserts exactly that.
* Run it against the **correct** implementation and it **fails**.
* **The generated tests were written from the generated code, so they confirm what the code does and say nothing about what it should do.** "All tests pass" was true, and it was evidence about the wrong thing.

---

## Attempt 2, Step by Step

| Run | Result |
|---|---|
| Attempt 2 with its own seven generated tests | **7 pass** |
| Attempt 2 with the acceptance tests as written | **Does not compile**: `reference to AvailabilityFinder is ambiguous` at `new AvailabilityFinder(null)` in `ex7` |
| Attempt 2 with the acceptance tests after a one-line cast | 9 run, **2 fail**: `ex4_...` and `ex5_...` |
| The 7 generated tests against the **accepted** finder | **6 pass and 1 fails**: `theSearchWindowIsInclusiveOfTheLastDay` |

---

## An Abstraction Has a Price

* Attempt 2 has two constructors, one taking a `List` and one taking an `AvailabilityRule`, so a bare `null` fits both: **`new AvailabilityFinder(null)` became ambiguous**, and the developer's own test for a null argument **no longer compiled**.
* The one-line cast used to run the examples changes only the argument's type, not what the test asserts. **Editing a test to suit the code is the wrong direction in general**; here it is only so the logic failure can be seen. The right response is to remove the unneeded overload.

---

## Size of the Abstractions

* The interface has **one implementation**, built in **one place** by a factory called **once**. The task had **one rule**.
* The assistant called it the open/closed principle. Chapter 5 said when that principle earns its cost; **here nothing needs to be extended.**

| Version | Types | Lines | Documentation |
|---|---:|---:|---|
| Accepted finder | **1** | **38** (six of them documentation) | Yes |
| Attempt 2 (`AvailabilityFinder` 30, `AvailabilityRule` 6, `AvailabilityRules` 13) | **3** | **49** | None |

---

## Why the Acceptance Examples Were Independent

* They were **derived from the requirement before any candidate existed**, and not from code.
* They were also **not shared** with the assistant, which let them be used a second way: to judge whether the output **generalises**.
* Sharing them would have been legitimate. It would probably have produced a correct loop, and **the pass would then have shown only that the assistant satisfied those examples.**
* The prompts show the point: `prompt1.md` says "within `searchDays` days" and **nowhere says what that counts**; `prompt2.md` **asks for tests**, which is where the shared misreading gets locked in.

---

## Revision and Acceptance

* The developer wrote the final version **by hand**, using attempt 2 only as a reminder of the loop shape, and **rewrote the requirement sentence** that had allowed the misreading.
* The final class **validates its arguments**, **copies the bookings** so the caller's list cannot change it, and calls `LoanPeriod.overlaps`.
* It passes the **nine acceptance examples**. It does not reserve anything and does not touch the lending system.
* `mvn --batch-mode test` ends with `Tests run: 9, Failures: 0, Errors: 0, Skipped: 0`.

---

## The Accepted Finder

```java
public Optional<LocalDate> earliestStart(LocalDate from, int days, int searchDays) {
    Objects.requireNonNull(from, "from");
    if (days < 1) throw new IllegalArgumentException("days must be at least 1");
    if (searchDays < 1) throw new IllegalArgumentException("searchDays must be at least 1");
    for (int offset = 0; offset < searchDays; offset++) {
        LocalDate start = from.plusDays(offset);
        LoanPeriod wanted = new LoanPeriod(start, start.plusDays(days));
        if (booked.stream().noneMatch(wanted::overlaps)) return Optional.of(start);
    }
    return Optional.empty();
}
```

* The constructor does `List.copyOf(Objects.requireNonNull(booked, "booked"))`.

---

## Figure 15.2: The Worked Example

<!--svg:ch15-example-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 270" role="img" aria-label="Figure 15.2: the worked example. Prompt 1 gives attempt 1, which has an invented method and a Java 21 API and fails with 2 compile errors under release 17. Prompt 2 names the findings and asks for tests and gives attempt 2, which compiles and passes its 7 generated tests but fails acceptance examples EX4 and EX5. The developer&#x27;s version is one class with the window loop corrected, passes all 9 acceptance examples, and is accepted and recorded." style="display:block;width:100%;height:calc(var(--u) * 27.00);margin:0 auto">
<defs><marker id="ch15-example-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch15-example-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch15-example-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch15-example-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch15-example-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="0.0" y="20.0" width="210.0" height="78.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="105.0" y="46.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Prompt 1:</text>
<text x="105.0" y="63.8" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">task, context,</text>
<text x="105.0" y="81.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">constraints, scope</text>
<rect x="330.0" y="20.0" width="210.0" height="78.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="435.0" y="46.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Attempt 1:</text>
<text x="435.0" y="63.8" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">invented method,</text>
<text x="435.0" y="81.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Java 21 API</text>
<rect x="660.0" y="20.0" width="210.0" height="78.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="765.0" y="46.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Prompt 2:</text>
<text x="765.0" y="63.8" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">name the findings,</text>
<text x="765.0" y="81.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">ask for tests</text>
<rect x="660.0" y="172.0" width="210.0" height="78.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="765.0" y="198.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Attempt 2:</text>
<text x="765.0" y="215.8" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">compiles, 7 generated</text>
<text x="765.0" y="233.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">tests pass</text>
<rect x="330.0" y="172.0" width="210.0" height="78.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="435.0" y="198.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Developer's version:</text>
<text x="435.0" y="215.8" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">one class, window</text>
<text x="435.0" y="233.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">loop corrected</text>
<rect x="0.0" y="172.0" width="210.0" height="78.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="105.0" y="206.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Accepted</text>
<text x="105.0" y="225.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">and recorded</text>
<path d="M210.0,59.0 L330.0,59.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-example-arr)"/>
<path d="M540.0,59.0 L660.0,59.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-example-arr)"/>
<text x="600.0" y="52.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">2 compile errors</text>
<path d="M765.0,98.0 L765.0,172.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-example-arr)"/>
<path d="M660.0,211.0 L540.0,211.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-example-arr)"/>
<text x="600.0" y="204.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">EX4, EX5 fail</text>
<path d="M330.0,211.0 L210.0,211.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch15-example-arr)"/>
<text x="270.0" y="204.0" font-size="13" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">9 examples pass</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 15.2

* **Both rejected attempts are kept in the record, with the reason for each.**
* Attempt 1 failed **to compile**; attempt 2 compiled and **passed its own tests** but failed independent examples.
* The route that worked: the developer's version, informed by the failures, checked by examples written beforehand.

---

## Do the Tests Detect Faults?

* Ten single faults were applied to the accepted finder. Each was run against the developer's acceptance examples and, separately, against the assistant's generated tests.

| | Caught | Survived |
|---|---|---|
| Acceptance examples (9 tests) | **8 of 10** | 2, both **equivalent** |
| Generated tests (6 that pass on correct code) | **4 of 10** | **6** |

---

## The Ten Faults (1 of 2)

| Fault | Acceptance examples | Generated tests |
|---|---|---|
| Loop runs one step too far (attempt 2's own fault) | Caught: EX4, EX5 | **Survived** |
| Loop stops one step early | Caught: EX3, EX5, EX6 | **Survived** |
| A stay of `days` occupies `days - 1` days | Caught: EX2, EX9 | Caught |
| The search skips `from` itself | Caught: EX3 to EX6 | Caught |
| `noneMatch` becomes `allMatch` | Caught: seven examples | Caught: three tests |

---

## The Ten Faults (2 of 2)

| Fault | Acceptance examples | Generated tests |
|---|---|---|
| Overlap treats an end date as occupied | Caught: five examples | Caught |
| `days = 0` is accepted | **Survived** (equivalent) | **Survived** |
| `searchDays = 0` is accepted | Caught: EX7 | **Survived** |
| The caller's list is kept, not copied | Caught: EX8 | **Survived** |
| A null `from` is not rejected early | **Survived** (equivalent) | **Survived** |

---

## Why Two Faults Survive

* With `days = 0` the finder's own check is gone, but **`LoanPeriod`'s constructor throws `IllegalArgumentException`** on a period that does not begin before it ends.
* With a null `from` the early check is gone, but **`from.plusDays` throws `NullPointerException`**.
* Each example asserts only the exception type. The faults change **where** the exception is raised and not **what a caller sees**: they are **equivalent**, and cannot be told apart from correct code by any test of the exception type.
* **The generated tests miss the very fault the assistant made**, a window one step too long, because they were built to agree with it.
* **Ten faults chosen by the author on one small class** say nothing about assistants in general.

---

# 15.5 Asking for a Refactoring or a Review
### Questions, not verdicts

---

## Ask for a Review as Questions

* Assistants are good at producing **a list of things worth looking at**. They are poor at telling you **which of them matters here**, and a review that ends "looks good" settles nothing.
* Ask for questions and risks, and **decide for yourself**:

> List the behaviours of this method that a caller could depend on, and the inputs for which the behaviour is not obvious from the code. Do not suggest changes.

---

## A Refactoring Must Say What Must Not Change

* Chapter 11: a refactoring **preserves intended observable behaviour**.
* A prompt for a refactoring should say so, **name the boundaries that matter** and keep the tests out of its reach: **"do not change the tests; if a test fails, report it and do not edit it"**.
* When a patch arrives, **apply its claims one at a time** in a scratch copy and run the suite after each.
* A patch that makes three claims and fails one test does not tell you which claim was wrong. **Applied piece by piece, it does.** Chapter 11's patch changed a boundary, a lookup order and a default at once.

---

## What a Review Can Check

* A reviewer can check that **a dependency points the right way** (the compiled dependencies of Chapter 10), that **a boundary is covered** (Chapter 13), that **a number in a document matches a run** (Chapter 14), or that **an explanation is consistent with the code**.
* These are checks **someone can repeat**.
* **"The assistant reviewed it and found no issues" is not one of them.**

---

# 15.6 How Assistants Fail
### The patterns to recognise

---

## The Failures This Book Has Met

* These are failures the book has met, with where. **Recognising the pattern is quicker than diagnosing each instance.**
* Eleven patterns follow, each with **a check that exposes it**.

---

## Failure Modes (1 of 3)

| Failure mode | What it looks like | Seen in | A check that exposes it |
|---|---|---|---|
| Invented method or class | A call to something that does not exist, named plausibly | Lab attempt 1 | The compiler |
| API newer than the baseline | Compiles on your default JDK, fails on the project's | Lab attempt 1 | Compile with the project's `--release` |
| Invented or wrong dependency | A coordinate that does not exist, or a real library you did not need | 15.7 | Look it up; read the build |
| Plausible but wrong boundary | A comparison one step off | Chapters 7, 11, 13; attempt 2 | Examples that sit on the boundary |

---

## Failure Modes (2 of 3)

| Failure mode | What it looks like | Seen in | A check that exposes it |
|---|---|---|---|
| Tests that repeat the code | Tests derived from the implementation agree with its mistakes | Chapters 7, 13; attempt 2 | Examples written beforehand; fault experiments |
| Unnecessary abstraction | An interface with one implementation, patterns for their own sake | Chapters 5, 6, 8, 10; attempt 2 | Ask what change it makes easier |
| Silent policy change | A requirement decided inside a "tidy-up" | Chapters 3, 11 | Diff the behaviour, not the text |
| Unsupported causal claim | "Proves", "caused", "will definitely" | Chapter 12 | Ask what evidence would show it |

---

## Failure Modes (3 of 3)

| Failure mode | What it looks like | Seen in | A check that exposes it |
|---|---|---|---|
| Confident description of unseen code | Behaviour that the code does not have | Chapters 1, 2; 15.3 | Read the code; trace |
| Self-reported verification | "I tested it and it works" | Lab attempts 1 and 2 | **Run it yourself, under the project's settings** |
| Stale knowledge | A deprecated or removed API; an old configuration | Anywhere | Official documentation for your version |

---

## Two Worth a Sentence More

* **Silent policy change** is dangerous because **the code can be better, and the commit is no longer a refactoring**: reviewers cannot tell which failures were intended.
* **Self-reported verification** is a special case of confident wrongness. An assistant that cannot run your build cannot have tested it under your settings, and one that can run something **still ran what it chose**.

---

# 15.7 Privacy, Dependencies and Where Work Came from
### What not to send; what not to trust

---

## What Not to Send

* With a **remotely hosted tool**, a prompt leaves your machine. Whether and how the service keeps or uses it is in **its own terms**, which differ and change: **read them, do not assume**.
* A tool that runs **locally** may keep everything on your machine, but check how it is actually deployed: a local front end may still call a remote service.
* A rule that works everywhere: **send the minimum**. No passwords, keys, tokens, personal data, real student or borrower records, or other people's confidential material. **Replace identifiers with invented ones.**
* Whether a tool may be used with course material is **for the module leader's rules** and your institution's policy.
* OWASP's list of risks for language-model applications names **sensitive information disclosure**.

---

## A Prompt That Should Not Be Sent

> Our reservation service is failing for Layla Hassan (student ID 2023-48817, layla.hassan@example.edu). Here is the config that fails; the directory password is in it: `lending.directory.url=http://10.20.30.40:8080/borrowers`, `lending.directory.password=not-a-real-password-just-an-example`. And here are the last 200 lines of our production log, which include other borrowers' names. What is wrong?

* **Constructed example: all names, identifiers and the key are invented.**

---

## What the Prompt Discloses

| In the first prompt | Why it should not be sent |
|---|---|
| A student's name, student ID and email | **Personal data** about a real borrower |
| A configuration file with a password | **A credential.** Anything secret in real life must not be pasted |
| An internal address and path | **Information about your infrastructure** |
| 200 lines of production log with other borrowers' names | **More personal data**, far more than the question needs |
| "What is wrong?" | No hypothesis, no limit on scope |

---

## The Same Task, With the Minimum Context

> A Java client calls `GET <base>/borrowers/<key>` and sometimes throws `HttpTimeoutException` after 1000 ms. Here is the method (no secrets, no real URL). Here are the three log lines that show the exception, with borrower keys replaced by `B1`, `B2`, `B3`. **What are the possible causes? List them without choosing one.**

* It is **smaller, safer and more useful**: it names what is wrong and nothing else.
* It states the symptom precisely (a timeout after 1000 ms) and asks for **causes you will check**, not for a verdict.

---

## Verify Every Dependency

* An assistant may suggest a library that **does not exist**. Researchers who tested sixteen code-generating models on **576,000 samples** found hallucinated package names averaged **at least 5.2% for the commercial models** and **21.7% for the open-source models** they tested, and noted that **an attacker could register such a name** with malicious code.
* **The percentages describe that study and its models, not yours. The habit is what matters.**

---

## The Dependency Checks (1 of 2)

| Check | How, for the book's toolchain | What it does not show |
|---|---|---|
| The coordinate exists | Ask Maven Central for the artifact's page and read the status | That it is the library you meant, or safe |
| It is the project you think it is | The group ID belongs to the project's own site; compare with its documentation | That the version has no defects |
| The version exists and is pinned | The exact version's POM returns 200; the project pins versions | Compatibility with your other dependencies |

---

## The Dependency Checks (2 of 2)

| Check | How | What it does not show |
|---|---|---|
| You need it | Can the standard library or an existing dependency do the job? | |
| It is allowed | Its licence, and your team's rules | Anything about legal certainty |

* **A status of 200 shows only that something is published under that name.**

---

## A Constructed Dependency Suggestion

> Add these to your `pom.xml` and use `Mocks.firstOf(list)`: `org.mockito:mockito-fluent:5.20.0` and `com.google.guava:guava:33.0.0-jre`, both with scope `test`.

* Task given: "Add a test helper that asserts the first element of a list."
* Status codes read from Maven Central on 13 October 2026. **Nothing was downloaded.**

| Coordinate | Status |
|---|---:|
| `mockito-core`, `mockito-junit-jupiter` | 200 |
| **`mockito-fluent`** | **404** |
| `mockito-core:5.20.0` (the `.pom`) | 200 |
| `mockito-core:9.9.9` | 404 |
| `guava`, `guava:33.0.0-jre` | 200 |

---

## The Decisions

* **`mockito-fluent`: reject.** It does not exist under that group, and **a plausible name is not a reason to search for a similar one**. Even a real mocking library would be wrong: a helper that asserts the first element of a list does not need mocking.
* **`guava:33.0.0-jre`: reject.** It exists, and **nothing in the task needs it**: `list.get(0)` and `assertEquals` do the job.
* **One suggestion was invented, and one was real and unnecessary. Both are failures, of different kinds.**

---

## Provenance and Disclosure

* **Provenance** is where a piece of work came from. For AI-assisted work: **that an assistant was used, what for, what you gave it, what you took from it and what you changed.**
* It matters because **a reviewer or a successor needs it to judge the work**, and because your institution may require it.
* Say so plainly and follow the module leader's rules and your team agreement. **Whatever the rules, keep a record of tasks that mattered.**
* Questions of **licence and ownership** of generated code are unsettled and depend on the tool, the jurisdiction and the terms. **This book gives no legal advice.**

---

# 15.8 Writing Down What You Checked
### Verification records

---

## What Evidence Can Show (1 of 2)

| Evidence | What it can show | What it cannot |
|---|---|---|
| Requirement and examples written beforehand | What was intended | That your reading of the requirement is right |
| Hand trace on selected inputs | The code behaves as you think on those inputs | Behaviour elsewhere |
| Compiler and type checker, under the project's settings | Syntax, types, the API available at the baseline | Meaning |
| Tests | Behaviour on the cases tested | Cases not tested, or that the tests are good |

---

## What Evidence Can Show (2 of 2)

| Evidence | What it can show | What it cannot |
|---|---|---|
| Fault experiments on the tests | That the tests notice those faults | Others; equivalent faults cannot be noticed |
| Traced dependencies (`jdeps`, the build's own listing) | What the code actually references | Whether those references are wise |
| Human review | Judgement that tools lack | Thoroughness, unless it is recorded |

* **Do not use one assistant to approve another's work and call the result verification.** It is a second candidate opinion with the same weaknesses.

---

## A Compact Record: Eight Parts (1 of 2)

| Part | Contents |
|---|---|
| Task | What was asked and **who owns the requirement** |
| Tool and model | The tool and model, or **"none: constructed example"**, and the date |
| Context given | What the assistant saw, and **what was left out and why** |
| Output received | Each candidate in order, with accepted or rejected. **Keep the rejected ones** |

---

## A Compact Record: Eight Parts (2 of 2)

| Part | Contents |
|---|---|
| Decision | What was accepted or rejected, and why |
| Changes made | What you changed by hand |
| Verification | The checks, the commands, the results and the date; **which checks are independent of the assistant** |
| Limits | What the checks do not show and **what was not run** |

* The lab holds a template, a filled example, and `scripts/check-record.sh` that checks every heading is **present and not empty**. It cannot tell whether what is written is true: **a reviewer must**. Appendix C (C.13) has the blank record and a worked example.

---

## A Useful Record, Not a Ritual

* The ritual version says **"reviewed and verified"** and nothing else.
* The useful one says:
  * attempt 1 **failed to compile under `--release 17` with two errors**;
  * attempt 2's **seven generated tests passed while two acceptance examples failed**;
  * **ten faults were applied**.
* **Write the record while you remember, and write it for someone who was not there.**

---

## The Filled Record: Task, Tool, Context

* **Task:** add `AvailabilityFinder.earliestStart(from, days, searchDays)`. The requirement and its **nine acceptance examples** were written by the developer before any prompt. The developer owns the requirement.
* **Tool and model:** *None: constructed example* (author-written, not a recorded service response), 13 October 2026.
* **Context given:** prompt 1 (task sentence, `LoanPeriod` source, constraints, output format, scope); prompt 2 (the two compiler findings, the request to keep it small and add tests). **Not shared: the acceptance examples.**

---

## The Filled Record: Output and Decision

* **Output received:**
  1. Attempt 1: **rejected**. It did not compile: `LoanPeriod.intersects` does not exist and `List.getFirst()` exists only from Java 21.
  2. Attempt 2: **rejected**. It compiled and its seven generated tests passed, but it added an interface and helper class the task did not need, its loop examined one candidate too many, one generated test asserted that behaviour, and it made `new AvailabilityFinder(null)` ambiguous.
* **Decision:** neither attempt accepted. The developer wrote the final version by hand, using attempt 2 only as a reminder of the loop shape.

---

## The Filled Record: Changes, Verification, Limits

* **Changes made:** removed the interface and helper; fixed the loop to `offset < searchDays`; validated arguments; copied the list; discarded the generated tests; **rewrote the requirement sentence**.
* **Verification:** `javac --release 17` on attempt 1: two errors; attempt 2 with its own tests: 7 pass, with the acceptance tests: EX4 and EX5 fail; final version: 9 pass; ten faults: eight caught, two equivalent. **Independent of the assistant's claims: the compiler, the acceptance examples written beforehand, the fault experiment.**
* **Limits:** the examples are the developer's reading of the requirement; compiled with `--release 17` but run on a newer JDK, **so no Java 17 runtime run is claimed**; not connected to the lending system.

---

# 15.9 Doing All of This Without a Live Service
### No live service required

---

## Every AI Activity Can Be Done Without a Live Service

* **The supplied candidate.** Each activity includes a constructed candidate output, labelled as such. The lab's two attempts, the `VisitorGate` explanation, the privacy example and the dependency suggestion are all supplied.
* **Swap with a classmate.** Each of you writes a plausible candidate for the same small task, **deliberately including one or two flaws of the kinds in 15.6**, and keeps a private list. Swap, find the flaws, compare lists. **A flaw you did not find is as instructive as one you did.**

---

## More Offline Routes

* **Write both sides.** Write the acceptance examples first, then a **quick, careless implementation as if you were the assistant**. Run the examples. This shows how an implementation that looks right can fail on a boundary.
* **Use a live assistant if you may and can.** Only synthetic data and files you may share. **Keep the actual output, including the attempts you reject.** Treat its account of itself as a claim. Follow the module leader's rules on assessments.
* **Constructed output is not a recording of a real model.** It is written to illustrate a failure mode and should be **labelled** each time. Where a real transcript is captured, record the **tool, the model and the date**.

---

# 15.10 AI Habits That Mislead
### Ten to avoid

---

## Mistakes 1 to 5

| Mistake | Consequence | Better action |
|---|---|---|
| Writing the requirement in the prompt and nowhere else | The prompt becomes the only record; the assistant's reading becomes the requirement | Write requirement and acceptance examples first, separately |
| Asking for code and tests together | The tests agree with the code's mistakes | Examples first; tests from the requirement; fault experiments |
| Accepting "I tested it" | A claim stands in for a run | Run it under the project's settings |
| Compiling with your default settings | A newer API slips through | Use the project's `--release` and build commands |
| Adding a suggested dependency without looking | Invented, unnecessary or hostile libraries | Look it up, ask whether you need it, pin it |

---

## Mistakes 6 to 10

| Mistake | Consequence | Better action |
|---|---|---|
| Pasting real data or secrets | May leave your machine, and stay in your history either way | Synthetic data; the minimum context |
| Using another assistant to check the first | The same weaknesses twice | Independent evidence |
| Throwing away a whole explanation for one wrong sentence | The correct parts are lost | Classify claim by claim and correct |
| Keeping only the accepted answer | A reviewer cannot see what was rejected, or why | Keep rejected attempts in the record |
| Writing "AI-assisted" and no more | Nobody can judge the work | A record: what, with what, what changed, what was checked |

---

## Diagnostic Alternatives

* **"Reviewed by another assistant"** under *Verification*: a second candidate opinion, not independent evidence.
* **Accepting it because it compiled:** attempt 1's second error showed compiling is not enough, and attempt 2 compiled and was still wrong.
* **Tests derived from the implementation:** `theSearchWindowIsInclusiveOfTheLastDay` agrees with the code and fails on correct code.
* **A record that says nothing:** headings present, *Verification* reading "reviewed and verified", *Limits* empty: the script flags empty headings, and **a reviewer must flag empty claims**.
* **A prompt that carries the requirement and the secrets:** the privacy example.

---

# 15.11 Try It Yourself
### The lab and your own task

---

## What You Start With, and the Demonstration

* **You start with:** the lab (Companion, Section 3), with its prompts, two constructed attempts, acceptance tests and record. **B1 to B7** use the book's project (the lab); **T1 to T4** use your team's project.
* **Instructor demonstration:** compile attempt 1 with `javac --release 17` and, if a JDK 21 or later is available, once more with plain `javac`; ask the class **why the results differ**. Then run attempt 2 against its own tests, and against the acceptance examples.
* **Guided practice:** take one claim from the constructed `VisitorGate` explanation and classify it, naming the evidence. Take one statement an assistant has made about itself and say **how you would check it**.

---

## The Book's Project: B1 and B2

* **B1. Reject attempt 1.** Run `bash scripts/try-attempt.sh 1`. Compile by hand with `javac --release 17`, read both errors; with a JDK 21 or later, compile once more without `--release` and compare. **List each defect and its category from 15.6**, and say what the claim "I tested it with Java 17" **can and cannot mean**.
* **B2. Diagnose attempt 2.** Run its own tests (`try-attempt.sh 2 generated`), then the acceptance examples (`try-attempt.sh 2 adapted`). Find the failing line, **name the shared misunderstanding** between the code and its tests, and explain why the acceptance examples were independent evidence. Run the generated tests against the accepted finder and say **what the one failure shows**.

---

## Expected Output of the Lab Scripts

| Command | Expected |
|---|---|
| `mvn --batch-mode test` | `Tests run: 9, Failures: 0, Errors: 0, Skipped: 0` and `BUILD SUCCESS` |
| `try-attempt.sh 1` | `BUILD FAILURE`: two `cannot find symbol` errors at lines 18 and 20 |
| `try-attempt.sh 2 generated` | `Tests run: 7, Failures: 0` |
| `try-attempt.sh 2` (acceptance) | `BUILD FAILURE`: `reference to AvailabilityFinder is ambiguous` |
| `try-attempt.sh 2 adapted` | `Tests run: 9, Failures: 2`: `ex4_...` and `ex5_...` |
| `check-record.sh` | `RECORD CHECK PASSED` |
| `check-record.sh`, only the template exists | `RECORD CHECK FAILED: nothing was checked`, exit status 1 |

---

## The Book's Project: B3 and B4

* **B3. Make the tests bite.** Apply **three faults** of your choice to the accepted finder in a scratch copy. **Predict** which acceptance examples fail, run them, compare. Find **one fault that survives** and say why.
  * Examples: `offset < searchDays - 1`, `start.plusDays(days - 1)`, `allMatch`.
* **B4. Fill in a record.** For a **different, very small task of your own** (a method you ask an assistant, or a constructed candidate from a classmate), complete a record using the template and run the checker.
  * A good record uses **all eight headings**, keeps rejected output, names **at least one independent check** and **at least one limit**. A weak one says "reviewed and verified" under *Verification*.

---

## Your Team's Project: T1 to T3

* **T1. Define one AI-assisted task before you prompt.** A small, real task in your project: the requirement, the **acceptance examples (derived from the requirement, before any candidate)**, the constraints and the scope. **Decide which examples you will share and which you will keep undisclosed, and why.**
* **T2. Run it and keep everything.** A live assistant if the rules allow, or an offline route (15.9). **Keep each attempt, including the ones you reject.** Compile and test with the project's own commands.
* **T3. Record it.** Fill in the record, including the independent checks and the limits, put it **with the change**, and run the record checker.

---

## If You Want More: B5 to B7 and T4

* **B5. Repeat the lab task with a live assistant**, if you may. Which failure modes did it show? **An assistant that gets it right the first time is a valid result:** record that and the checks that showed it.
* **B6. Verify two dependencies.** Look up the constructed suggestion's coordinates, report the status of each and decide what to do about each.
* **B7. Swap and find.** The classmate exercise of 15.9. **Missing a flaw of the invented-method kind is common and instructive.**
* **T4. Agree your team's practice.** A short note: which tools may be used (following the module leader's rules), what may be shared with them, how work is **disclosed and recorded**, and **who reviews AI-assisted changes**.

---

## What You Should End Up With, and When You Are Done

* **What you should end up with:** B1 to B4; for your team's project, one defined task with its acceptance examples, the attempts, a record, and a team note if you did T4.
* **Acceptance:**
  * the acceptance examples were **written before the candidate was requested**;
  * every claim the assistant made about itself was **checked or marked unchecked**;
  * the check used **the project's own compiler settings**;
  * a **rejected attempt is in the record with its reason**;
  * the record's limits say **what was not run**;
  * **no secrets or personal data** were shared;
  * **no live tool was used where the rules forbid it**.
* **Optional:** do the same task twice, once with the acceptance examples in the prompt and once without, and compare.

---

# 15.12 Questions to Think with, and a Transfer Challenge
### Concept, diagnosis, transfer

---

## Concept Questions

1. Why is "I tested it with Java 17" not evidence? Name two checks that would be.
2. An assistant writes a function and its tests, and they pass. Why does that not establish that the function is right, and what would?
3. What does the `--release` option change that `--source` and `--target` alone do not?
4. A dependency suggested by an assistant exists on Maven Central. What have you learned and what have you not?

---

## Diagnosis Questions

5. An explanation of a method says "the method caches the result." The code has no field. What are your options for settling it, and what would you write down?
6. A refactoring patch makes four claims and one test fails. How do you find which claim caused it, and why is the patch's own summary not the way?

---

## Guidance: Questions 1 to 4

1. It is a sentence from a system that **did not run your build** and names no command or result. Evidence: compile and test with the **project's own command** (`mvn --batch-mode test`, which sets `release` 17); run `javac --release 17` on the file.
2. Tests derived from the code **agree with it, including where it is wrong**: `theSearchWindowIsInclusiveOfTheLastDay` passes on attempt 2 and fails on correct code. **Examples written from the requirement beforehand**, and a **fault experiment on the tests**, would show it.
3. `--source`/`--target` set the language level and class-file target. **`--release` also restricts the API** to the one that release defines, and cannot be combined with them.
4. You have learned that **something is published under that coordinate**. Not that it is the library you meant, safe or licensed for your use, suited to your build, or **needed**.

---

## Guidance: Questions 5 and 6

5. **Options:** read the class for a field that holds a result (there is none); look for a test that depends on caching, and one that depends on its absence (`theFileIsReadAfreshOnEveryCall`); trace two calls by hand. **Write down the claim, the evidence and the verdict**: contradicted, with the line or test.
6. **Apply the claims one at a time** in scratch copies and run the suite after each: the failing claim is the one whose copy fails. **The patch's summary is a claim of the same kind as the code** and cannot tell you which of its own claims was the cause.

---

## Transfer Challenge: ML Model Serving

A team building an ML model-serving service wants an assistant to write a **data-validation function and its tests**. Plan the task:

* the **requirement and acceptance examples** (synthetic records);
* the **context to share and not to share**;
* what the **independent checks** are;
* how you would **check any suggested dependency**;
* what the **record** would say about what the checks **do not show about the model**;
* what is different about AI **in** the product, such as the model itself, and **why this chapter does not cover it**.

---

## Transfer Guidance (1 of 2)

| Item | Content |
|---|---|
| Requirement and examples | The validation rule stated precisely (what counts as missing, which ranges, what happens to a bad record). **Examples on the boundaries, with synthetic records. Written first** |
| Context to share | The function signature, the record type, the constraints. **Synthetic records only** |
| Not to share | Real records, keys, tokens, the registry's address, any real model or customer identifiers |
| Independent checks | The compiler under the project's settings; the examples; a fault experiment on the tests; a trace on selected inputs |

---

## Transfer Guidance (2 of 2)

| Item | Content |
|---|---|
| Dependencies | Look up any suggested library; ask whether the standard library already does it; **pin the version** |
| Record | Task, tool and model, context, each attempt, decision, changes, verification, limits |
| What it does not show about the model | **Nothing here evaluates the model**: accuracy, fairness, drift, behaviour on data unlike the synthetic data. **Validating the data a model receives is not validating the model** |
| AI in the product | The model is **a component with its own failure modes, contracts and tests**: a different topic. In this book it is the borrower directory: Chapters 6, 7, 8 and 13 |

---

# What to Take Away, and What Comes Next
### What to carry forward

---

## Summary

* An assistant gives you **candidates**. Your job:
  * **define the task**;
  * **keep the requirement and the examples yours**;
  * **check the output against evidence the assistant did not write**;
  * **record what you accepted and why.**
* The failures are familiar: **invented methods, APIs newer than the baseline, dependencies that do not exist, boundaries one step off, tests that repeat the code, abstractions nobody needs, policy changed in passing, claims of testing that nobody ran.**
* **Each has an inexpensive check. None of them requires a live service to practise.**

---

## Where to Go Next

* This is the **last chapter of the book's main sequence**.
* The appendices that follow collect material the chapters point to: **notation and a programming refresher, tools and reproducible setup, engineering templates, project versions and a glossary, and a guide to critical reading and project evidence.**

---

## Sources and Further Reading

1. **GitHub Docs:** *Application card: GitHub Copilot inline suggestions* (one vendor's account of one tool).
2. **Oracle:** `List` (Java SE 21 and 17); `javac` (Java SE 17).
3. **Apache Maven:** *maven-compiler-plugin: compile mojo* (the `release` parameter).
4. **OWASP:** *Top 10 for LLM Applications* (2025 edition).
5. **Spracklen et al.:** *We Have a Package for You!*, arXiv 2406.10279.

* Full references and links are in the chapter text.
