---
title: "Chapter 11: Refactoring and Legacy Code"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 110
type: slides
layout: page
---

# Chapter 11: Refactoring and Legacy Code
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **11.1 Working with unfamiliar code**
  * Observe, seam, pin, reshape, then change behaviour.
* **11.2 Smells as investigation prompts**
  * A smell is only worth acting on when it blocks a change.
* **11.3 Characterisation and regression tests**
  * Record what the code does, even when it looks wrong.
* **11.4 Seams and dependency isolation**
  * Clock, locale and standard output.

---

## Chapter Roadmap (2 of 3)

* **11.5 Extract Method, Extract Class, Move Method and Rename**
  * Four stages of one overdue report.
* **11.6 Incremental changes and rollback**
  * One step, one check, one commit.
* **11.7 Technical debt and evidence**
* **11.8 AI in practice:** review a refactoring patch.

---

## Chapter Roadmap (3 of 3)

* **11.9 Common mistakes**
* **11.10 Practical activity**
  * Book project B1 to B7; Team project T1 to T4.
* **11.11 Review and transfer**
  * An ML-serving analysis script.
  * **Quiz 2 revision pointers** (Chapters 6 to 10).
* **Summary and next chapter**
  * Chapter 12: measuring progress and flow.

---

## Learning Outcomes (1 of 2)

By the end of this chapter, you should be able to:

1. **Diagnose a smell** from a concrete difficulty of change, instead of treating it as a verdict.
2. **Distinguish a refactoring from a behaviour change**, and state what must stay the same.
3. **Write characterisation tests** that record current behaviour, including behaviour that looks wrong.

---

## Learning Outcomes (2 of 2)

4. **Create a seam** that removes a hidden dependency, so that code can be tested.
5. **Apply small refactorings** (Extract Method, Extract Class, Move Method, Rename) with a check after each step and a way back.
6. **Record uncertainties, suspected defects and technical debt** separately, with evidence.

---

## Module Connection and Scope

* Supports **LO3 and LO4**. Readings: the refactoring chapter of Martin; **Feathers** on legacy code is the recommended companion. The Week 10 lab is refactoring untested legacy code with regression tests.
* **Quiz 2** is held in Week 10 and covers dependency injection, TDD and test doubles, design patterns and layered architecture (**Weeks 5 to 9**). **The legacy lab is separate from that scope.**
* **Entry:** Chapter 10's project and package structure. This chapter adds **one isolated package, `legacy`**, standing for the old records system's overdue report. Production code **must not refer to it**, and the dependency test now checks that.

---

## Reading Route

* **Core reading:** Sections 11.1 to 11.6.
* **Working knowledge:** 11.7 (technical debt and evidence): describe debt with evidence and separate defects from preferences. You do not manage a debt register for a real project.
* **Minimum lab:** **B1 to B3** (Book project: extend the supplied tests, take the first refactoring steps) and **T1 to T4** (your Team project: characterise one untested method and refactor it in small commits).
* **Optional extension:** B4 to B7, the review questions, the transfer challenge.

---

## Opening Scenario: An Old Overdue Report

* It lists every unreturned loan past its due date and adds a fine.
* A laptop **two days late shows a fine of 0.00** yet still counts as overdue.
* A colleague on another machine sees amounts printed as **`0,50`** where everyone else sees `0.50`.
* The office asks for a small change: staff should get **seven days of grace instead of five**.

---

## You Open the Code

* One method of about **forty lines**.
* The staff rule in one branch, the student rule in another, and a **third branch for anyone else**.
* The number five appears **twice** in the staff branch; **changing only one is a bug**.
* It reads **today's date from the system clock**: its output changes every day.
* **Nobody wrote tests, and the author has left.**

---

## A Cautionary Tale

* A colleague once tidied a report like this one. The new version was **shorter. It also listed fewer loans.**
* Nobody could say whether **a defect had been repaired or a promise broken**: nobody had recorded what the old report promised.
* So what do you change first? **Not the staff grace period.**
* Before changing a rule, **know what the code does today**, so you can tell afterwards that you changed only what you meant to.

---

## The Method of This Chapter

1. **Observe.**
2. **Pin** what you observe.
3. **Reshape** the structure in small checked steps.
4. **Keep every correction of behaviour separate** from every improvement of structure.
* Changing code you do not yet understand, **without tests that protect it**.

---

# 11.1 Working With Unfamiliar Code
### Legacy means no tests

---

## What Makes Code "Legacy"

* Feathers: **legacy code is code without tests.** Age does not matter.
* Code written last month becomes legacy when you must change it, **cannot tell what a change will break, and nothing will tell you**.
* The report is old, but the habits that produced it (**global state, hidden dependencies, one long method**) are not.

---

## The Dilemma

* Refactoring changes internal structure while **external behaviour stays the same**.
* To know behaviour stayed the same you need **tests**.
* But the code is hard to test **because of its structure**, so you want to refactor first.
* The way out is a short sequence.

---

## The Way Out: Five Steps

1. **Observe:** run the code and read it with a specific question in mind. You need not understand all of it.
2. **Make the smallest edit that lets you test it**: a *seam*. Keep it mechanical, so the compiler and a quick read can check it.
3. **Pin:** characterisation tests that record what the code does now.
4. **Reshape:** refactor in small steps, tests after each.
5. **Only then change behaviour**, in a separate step with its own tests.

---

## Figure 11.1: The Order of Work

<!--svg:ch11-order-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 290" role="img" aria-label="Figure 11.1: observe, make the smallest mechanical edit that creates a seam, pin behaviour with characterisation tests, reshape with small refactorings testing after each, and only then change behaviour in a separate step. If a test fails, roll back the step and redo it." style="display:block;width:100%;height:calc(var(--u) * 29.00);margin:0 auto">
<defs><marker id="ch11-order-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-order-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-order-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-order-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-order-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="25.0" width="150.0" height="92.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="85.0" y="66.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Observe</text>
<text x="85.0" y="86.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">run and read</text>
<rect x="185.0" y="25.0" width="150.0" height="92.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="260.0" y="56.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Seam</text>
<text x="260.0" y="76.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">smallest</text>
<text x="260.0" y="96.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">mechanical edit</text>
<rect x="360.0" y="25.0" width="150.0" height="92.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="435.0" y="56.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Pin</text>
<text x="435.0" y="76.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">characterisation</text>
<text x="435.0" y="96.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">tests</text>
<rect x="535.0" y="25.0" width="150.0" height="92.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="610.0" y="56.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Reshape</text>
<text x="610.0" y="76.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">small refactorings,</text>
<text x="610.0" y="96.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">test after each</text>
<rect x="710.0" y="25.0" width="150.0" height="92.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="785.0" y="56.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Change behaviour</text>
<text x="785.0" y="76.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">a separate step,</text>
<text x="785.0" y="96.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">new tests</text>
<path d="M160.0,71.0 L185.0,71.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-order-arr)"/>
<path d="M335.0,71.0 L360.0,71.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-order-arr)"/>
<path d="M510.0,71.0 L535.0,71.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-order-arr)"/>
<path d="M685.0,71.0 L710.0,71.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-order-arr)"/>
<rect x="520.0" y="195.0" width="180.0" height="56.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="610.0" y="228.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Roll back the step</text>
<path d="M585.0,117.0 L585.0,195.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-order-arr)"/>
<text x="532.0" y="160.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">a test fails</text>
<path d="M635.0,195.0 L635.0,117.0" fill="none" stroke="#b4762e" stroke-width="2.2" marker-end="url(#ch11-order-arr)"/>
<text x="680.0" y="160.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">redo it</text>
<text x="80.0" y="225.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">Debug backwards, not forwards:</text>
<text x="80.0" y="247.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">undo the last step and redo it.</text>
</svg>
</div>
<!--/svg-->

---

## The Code as Found (1 of 3)

```java
public static String build(List<LoanRow> rows) {
    String out = "";
    double total = 0;
    int count = 0;
    LocalDate today = LocalDate.now();
    out += "OVERDUE REPORT " + today + "\n";
    for (int i = 0; i < rows.size(); i++) {
        LoanRow r = rows.get(i);
        if (r.returned) {
            continue;
        }
        long late = ChronoUnit.DAYS.between(r.due, today);
```

* Read it once and write down what you notice **before reading on**.

---

## The Code as Found (2 of 3)

```java
        if (late > 0) {
            double fine = 0;
            if (r.kind.equals("S")) {
                if (late > 2) {
                    fine = (late - 2) * 0.50;
                    if (fine > 10) {
                        fine = 10;
                    }
                }
            } else if (r.kind.equals("T")) {
                if (late > 5) {
                    fine = (late - 5) * 0.25;
                    if (fine > 5) { fine = 5; }
                }
            } else {
                fine = 1.00 * late;
            }
```

---

## The Code as Found (3 of 3)

```java
            out += r.item + " " + r.borrower + " " + late
                    + " day(s) late, fine " + String.format("%.2f", fine) + "\n";
            total += fine;
            count++;
        }
    }
    out += count + " overdue, total fines " + String.format("%.2f", total) + "\n";
    return out;
}
```

* `LoanRow` is the old system's **export format**: item, borrower, kind (`"S"` student, `"T"` staff), due date, returned flag, all **public mutable fields**. Other programs read it, so it stays as it is.

---

## Separate What You Know From What You Guess

| Observation | How you know | Status |
|---|---|---|
| Returned loans are skipped | Read: `continue` on `returned` | Known |
| Fines start after a grace period and are capped | Read: two nested comparisons per kind | Known |
| Neither `"S"` nor `"T"` pays 1.00 a day, no grace, no cap | Read: the final `else` | Known what, **unknown whether intended** |

---

## Separate What You Know From What You Guess (2)

| Observation | How you know | Status |
|---|---|---|
| The output depends on the date the program runs | Read: `LocalDate.now()` | Known |
| Amounts print with a comma in some locales | `String.format` without a locale; `%f` localises the separator | Likely; confirm by running |
| A loan two days late is listed with a fine of 0.00 and counted | The count is incremented inside `late > 0` | Likely; confirm by running |

* **"Unknown whether intended" is an honest status.** It is not your job yet to decide it is wrong.

---

# 11.2 Smells as Investigation Prompts
### A smell is a prompt, not a verdict

---

## What a Smell Is

* A surface indication that **usually corresponds to a deeper problem**: not always a problem.
* Its use here: a **prompt to investigate**.
* Only worth acting on when you can name **a concrete difficulty of change** that it causes.

---

## Smells in the Report (1 of 3)

| Smell | The difficulty it causes |
|---|---|
| Duplicated branches (student and staff blocks have the same shape) | A change to the rule shape must be made in every branch; the grace number appears twice in each, so editing one of the two gives a wrong result |
| Long method | To change the fine you must read the loop, the formatting and the totals too |

---

## Smells in the Report (2 of 3)

| Smell | The difficulty it causes |
|---|---|
| Hidden dependency on the system clock | The output differs every day: no test can compare it with a fixed answer |
| Hidden dependency on the default locale | The same data prints differently on two machines |
| Magic numbers (`2`, `0.50`, `10`, `5`, `0.25`) | A reader cannot tell a grace period from a cap |

---

## Smells in the Report (3 of 3)

| Smell | The difficulty it causes |
|---|---|
| A string kind compared with `equals` | An unexpected kind falls into the final branch without anyone deciding that |
| `String +=` in a loop | **Not a difficulty of change here**; a possible slowness for very long reports |

* The last row is a **deliberate counter-example**.

---

## Not Every Smell Needs Repair

* A smell in code **nobody changes** costs very little. Its repair value depends on **how often the code changes and how much the difficulty costs**.
* Decide where to spend effort by asking **which changes are coming**.
* The office has just asked for a grace-period change: the **duplicated branches and magic numbers** are worth fixing now.
* The `String +=` loop is **not**.

---

# 11.3 Characterisation and Regression Tests
### Record what the code does

---

## Two Different Promises

* A **regression test** protects behaviour that everyone agrees is **correct**.
* A **characterisation test** records **what the code does today, whatever that is**, so you notice if a change alters it.
* They look the same in the test framework.
* A passing characterisation test means **"unchanged"**. It does **not** mean "correct".

---

## How to Write One (1 of 2)

1. **Isolate the code** so it can run in a test (often the hardest part).
2. **Write a test with a placeholder expectation**, a value you know to be wrong.
3. **Run it and read the actual result** from the failure message.

---

## How to Write One (2 of 2)

4. **Record that result** as the expectation, **after you have looked at it**.
5. **Rename the test** to say what you now understand the code does.
6. **Keep exploring** with further inputs, especially boundaries and odd cases.

* Step 4 holds the discipline: **do not paste the result blindly**. Look at each one and classify it.

---

## Classify Every Result

| Class | Meaning | What you do |
|---|---|---|
| Expected | Matches the rule you were told | Keep the test |
| Surprising | You did not expect it, but it may be intended | Keep the test; ask the owner |
| Suspected defect | It looks wrong | Keep the test, mark it clearly, record the question; **do not fix it here** |
| Unknown | You cannot tell | Keep the test and record the question |

---

## What the Report Does: Fines by Days Late

<!--svg:ch11-fines-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 340" role="img" aria-label="Fine against days late: a student pays nothing for 2 days, then 0.50 a day up to a cap of 10.00 at 22 days; staff pay nothing for 5 days, then 0.25 a day up to a cap of 5.00 at 25 days; any other kind pays 1.00 a day with no grace and no cap (suspected defect)." style="display:block;width:100%;height:calc(var(--u) * 34.00);margin:0 auto">
<defs><marker id="ch11-fines-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-fines-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-fines-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-fines-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-fines-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<path d="M80.0,285.0 L800.0,285.0" fill="none" stroke="#c3cfdd" stroke-width="1.4"/>
<text x="70.0" y="290.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">0.00</text>
<path d="M80.0,241.7 L800.0,241.7" fill="none" stroke="#c3cfdd" stroke-width="1.4"/>
<text x="70.0" y="246.7" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">5.00</text>
<path d="M80.0,198.3 L800.0,198.3" fill="none" stroke="#c3cfdd" stroke-width="1.4"/>
<text x="70.0" y="203.3" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">10.00</text>
<path d="M80.0,111.7 L800.0,111.7" fill="none" stroke="#c3cfdd" stroke-width="1.4"/>
<text x="70.0" y="116.7" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">20.00</text>
<path d="M80.0,25.0 L800.0,25.0" fill="none" stroke="#c3cfdd" stroke-width="1.4"/>
<text x="70.0" y="30.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">30.00</text>
<text x="80.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">0</text>
<text x="200.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">5</text>
<text x="320.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">10</text>
<text x="440.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">15</text>
<text x="560.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">20</text>
<text x="680.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">25</text>
<text x="800.0" y="307.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="middle">30</text>
<text x="440.0" y="328.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">days late</text>
<path d="M80.0,285.0 L128.0,285.0 L608.0,198.3 L800.0,198.3" fill="none" stroke="#1d588c" stroke-width="3.4"/>
<path d="M80.0,285.0 L200.0,285.0 L680.0,241.7 L800.0,241.7" fill="none" stroke="#b4762e" stroke-width="3.4"/>
<path d="M80.0,285.0 L800.0,25.0" fill="none" stroke="#172a42" stroke-width="2.6" stroke-dasharray="8 6"/>
<text x="808.0" y="203.3" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#1d588c" text-anchor="start">student</text>
<text x="808.0" y="246.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="start">staff</text>
<text x="794.0" y="47.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="end">other kinds</text>
<text x="608.0" y="188.3" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#1d588c" text-anchor="middle" font-style="italic">cap at 22 days</text>
<text x="684.0" y="219.7" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="middle" font-style="italic">cap at 25 days</text>
<text x="396.0" y="155.7" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="end" font-style="italic">no grace, no cap</text>
<text x="396.0" y="173.7" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="end" font-style="italic">(suspected defect)</text>
</svg>
</div>
<!--/svg-->

---

## Observed Fines (1 of 2)

| Kind | Days late | Fine | Comment |
|---|---:|---:|---|
| S | 1, 2 | 0.00 | Listed and counted with no fine (grace) |
| S | 3 | 0.50 | First fine |
| S | 10 | 4.00 | |
| S | 22, 23, 100 | 10.00 | The cap is reached at 22 days and holds |
| T | 1 to 5 | 0.00 | Listed and counted with no fine (grace) |
| T | 6 | 0.25 | First fine |
| T | 25, 26, 100 | 5.00 | The cap is reached at 25 days and holds |

---

## Observed Fines (2 of 2)

| Kind | Days late | Fine | Comment |
|---|---:|---:|---|
| X (unknown) | 1 | **1.00** | Suspected defect: no grace |
| X (unknown) | 100 | **100.00** | Suspected defect: no cap |
| s (lower case) | 3 | **3.00** | Suspected defect: a typo in the data costs six times the student fine |
| blank | 2 | **2.00** | Same branch |

* Run on the supplied code with today fixed at **20 October 2026**.

---

## Four More Observations

* A loan **due today or later** is not listed.
* A **returned** loan is ignored.
* A **null kind** throws `NullPointerException` (and only for a loan that is actually overdue).
* Under a **German locale** the amounts print with a comma.
* One of each class: the grace listing and the comma are **surprising**; the unknown kinds are **suspected defects**; the null-kind failure is **unknown**.

---

## One Test, in the Style

```java
// SUSPECTED DEFECT, pinned on purpose: any other kind pays 1.00 a day
// with no grace and no cap.
@ParameterizedTest
@CsvSource({"X,1,1.00", "X,100,100.00", "s,3,3.00"})
void otherKindsPayTheFullRateWithNoGraceOrCap(String kind, int daysLate, String fine) {
    assertEquals(oneLoan(daysLate, fine), OverdueReport.build(List.of(open(kind, daysLate)), TODAY));
}
```

* **The comment is part of the test.** In six months someone sees it fail during an unrelated change: the comment tells them whether to fix their change or ask a question.

---

## A Second Net: A Differential Check

* Keep a copy of the **original code as an oracle**, generate thousands of inputs with a **fixed seed**, compare old and new output.
* The companion's test runs **3,000 generated lists**.
* Stronger than the examples for the **kinds of input it generates**. It says nothing about inputs **outside** them.
* Neither net proves equivalence: they show a **chosen set of behaviours is unchanged**. Add more where you are about to change more.

---

# 11.4 Seams and Dependency Isolation
### The smallest edit that lets you test

---

## What a Seam Is

* A **seam** is a place where you can change what the program does **without editing the code at that place**.
* To use it you need an **enabling point**: somewhere you can choose the other behaviour.
* The report has **three hidden dependencies**, each needing a different answer.

---

## Three Hidden Dependencies

| Hidden dependency | Where it is | How to isolate it |
|---|---|---|
| The system clock | `LocalDate.now()` inside `build` | A **parameter seam**: add `build(rows, today)`; the old method calls it |
| The default locale | `String.format("%.2f", ...)` | Pin the locale in the test and **restore it afterwards** |
| Standard output | `print` writes to `System.out` | Capture `System.out` in one test and **restore it afterwards** |

---

## The Clock Seam

```java
public static String build(List<LoanRow> rows) {
    return build(rows, LocalDate.now());
}

public static String build(List<LoanRow> rows, LocalDate today) {
    String out = "";
    double total = 0;
    int count = 0;
    out += "OVERDUE REPORT " + today + "\n";
    // ... the rest of the method is unchanged
```

---

## Why This Edit Is Safe Before Any Test

* It is **mechanical**: one expression moves from the body to a call, one line is deleted.
* It is **checked by the compiler**: if anything else changed, the code would not compile.
* It is **visible to a reviewer**: a few lines, readable in a minute.
* Existing callers **see no difference**. This is Chapter 7's injected `Clock` at the smallest scale: a parameter suffices for a static method.
* A bigger seam (injected `Clock`, non-static class) is **better design but an untested edit**: the very risk the chapter is about.

---

## Check the Enabling Edit by Running It

* The companion's **probe** contains the **original report with only its class name changed** (`OriginalUnseamed`) and a program comparing the original with the seamed report through their public one-argument entry points.
* It compares **five rows** (a late student, a late staff member, a row due today, an unknown kind, a returned loan) and an **empty list**, and checks one literal result.
* It refuses to run if the date changes while it executes.
* Expected: `Original and seamed reports agree on 5 rows and on an empty list.`

---

## The Probe Is Bounded

* It examines a few rows, not every input, and **cannot tell you the report is correct**.
* What it adds to the compiler and your eyes: **a direct comparison of the code as found with the code after the only untested edit**.
* Keep it small, run it **once**, then put the real protection in the characterisation tests.

---

## Who Chooses the Zone?

* The report now takes a date, so **the caller decides which calendar date "today" is**.
* A `Clock` carries a zone; `LocalDate.now(clock)` converts its instant using it.
* At **22:30 UTC on 21 October** it is already **22 October in Baghdad**. A loan due on 21 October is **not late in UTC** and **one day late in Baghdad**.
* The seam did not remove the question of which zone is right. It **moved it to the one place that has to answer it**.

---

## The Locale and the Output Stream

* Left alone, because changing them would be **a bigger edit than the tests justify**. The tests deal with them instead:
  * a fixture sets the default locale to `Locale.ROOT` before each test and **restores it**;
  * one test sets `Locale.GERMANY` and records the comma;
  * one test replaces `System.out` and **restores it in a `finally` block**.
* Both are **global, process-wide state**. Such tests cannot safely run in parallel, and one that forgets to restore **breaks an unrelated test far away**.

---

## Other Seams Worth Knowing

* **Subclass and override:** make a class non-final; a test subclass replaces one method.
* **Extract interface:** put a dependency behind an interface (Chapter 6's move).
* Both change more code than a parameter does: **choose the smallest seam that gets the code under test**.
* A better design (a `PrintStream` parameter on `print`, a locale argument) is worth adding **when you have a reason to change those lines**.

---

# 11.5 Extract Method, Extract Class, Move Method and Rename
### Four stages, each checked

---

## Refactorings Have Names

* So a team can say **what it did** and a reviewer can check it.
* Fowler's catalogue: **Extract Function**, **Move Function**; the first edition called them Extract Method and Move Method. Used interchangeably.
* Each stage below was a separate step; the characterisation tests and the differential test **passed after each**.

---

## Stage 2: Extract Method

```java
double fine = fineFor(r.kind, late);
out += r.item + " " + r.borrower + " " + late + " day(s) late, fine " + money(fine) + "\n";
...
private static double fineFor(String kind, long late) { /* the three branches, moved as they were */ }
private static String money(double amount) { return String.format("%.2f", amount); }
```

* The behaviour is the same **because the moved code is the same**.
* The loop reads in one glance, and the formatting rule (and its locale dependency) lives in **exactly one place**.

---

## Stage 3: A Missing Concept

* The three branches differ only in **three numbers**: free days, a daily rate, a cap.
* That is **a missing concept**, and it can be a small class.

```java
record FinePolicy(int graceDays, double ratePerDay, double cap) {
    double fineFor(long daysLate) {
        if (daysLate <= graceDays) {
            return 0;
        }
        return Math.min((daysLate - graceDays) * ratePerDay, cap);
    }
}
```

---

## Stage 3: Three Named Policies

```java
private static final FinePolicy STUDENT = new FinePolicy(2, 0.50, 10.00);
private static final FinePolicy STAFF = new FinePolicy(5, 0.25, 5.00);
/** Suspected defect, preserved on purpose: any other kind pays 1.00 a day
 *  with no grace and no cap. */
private static final FinePolicy ANY_OTHER_KIND = new FinePolicy(0, 1.00, Double.MAX_VALUE);
```

* `fineFor` moved into the new class (**Move Method**).
* The odd third branch **did not disappear**: it now has **a name, a comment and a policy of its own**.

---

## Is the New Code Equal to the Old?

| Old code | `FinePolicy.fineFor(daysLate)` with the same numbers |
|---|---|
| `if (late > 2)` not taken: fine stays 0 | `daysLate <= graceDays` returns 0 |
| `fine = (late - 2) * 0.50; if (fine > 10) fine = 10;` | `Math.min((daysLate - graceDays) * ratePerDay, cap)` |
| Staff: the same with 5, 0.25 and 5 | The same with those values |
| Other kinds: `fine = 1.00 * late` | Grace 0, rate 1.00, cap `Double.MAX_VALUE` |

* Check it **algebraically**, then let the tests confirm the algebra **for the inputs they cover**.

---

## Figure 11.2: After Stage 3

<!--svg:ch11-classes-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 365" role="img" aria-label="Figure 11.2: OverdueReport holds three FinePolicy values (STUDENT, STAFF, ANY_OTHER_KIND) and only reads LoanRow, the old system&#x27;s export format, which is unchanged." style="display:block;width:100%;height:calc(var(--u) * 36.50);margin:0 auto">
<defs><marker id="ch11-classes-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-classes-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-classes-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-classes-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-classes-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="10.0" width="375.0" height="163.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,46.0 L12.0,16.0 Q12.0,12.0 16.0,12.0 L379.0,12.0 Q383.0,12.0 383.0,16.0 L383.0,46.0 Z" fill="#e6eef6"/>
<text x="197.5" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">OverdueReport</text>
<line x1="10.0" y1="46.0" x2="385.0" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+build(List&lt;LoanRow&gt;) String</text>
<text x="22.0" y="91.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+build(List&lt;LoanRow&gt;, LocalDate) String</text>
<text x="22.0" y="114.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+print(List&lt;LoanRow&gt;) void</text>
<text x="22.0" y="137.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-policyFor(String) FinePolicy</text>
<text x="22.0" y="160.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-money(double) String</text>
<rect x="560.0" y="10.0" width="290.0" height="172.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M562.0,66.0 L562.0,16.0 Q562.0,12.0 566.0,12.0 L844.0,12.0 Q848.0,12.0 848.0,16.0 L848.0,66.0 Z" fill="#e6eef6"/>
<text x="705.0" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«record»</text>
<text x="705.0" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">FinePolicy</text>
<line x1="560.0" y1="66.0" x2="850.0" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="572.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">int graceDays</text>
<text x="572.0" y="111.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">double ratePerDay</text>
<text x="572.0" y="134.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">double cap</text>
<line x1="560.0" y1="147.0" x2="850.0" y2="147.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="572.0" y="169.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">~fineFor(long) double</text>
<rect x="560.0" y="205.0" width="290.0" height="163.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M562.0,241.0 L562.0,211.0 Q562.0,207.0 566.0,207.0 L844.0,207.0 Q848.0,207.0 848.0,211.0 L848.0,241.0 Z" fill="#e6eef6"/>
<text x="705.0" y="230.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">LoanRow</text>
<line x1="560.0" y1="241.0" x2="850.0" y2="241.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="572.0" y="263.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+String item</text>
<text x="572.0" y="286.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+String borrower</text>
<text x="572.0" y="309.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+String kind</text>
<text x="572.0" y="332.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+LocalDate due</text>
<text x="572.0" y="355.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+boolean returned</text>
<path d="M385.0,70.0 L560.0,70.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-classes-open)"/>
<text x="472.5" y="56.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">holds three</text>
<path d="M200.0,173.0 L200.0,280.0 L560.0,280.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch11-classes-open)"/>
<text x="380.0" y="266.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">reads</text>
<text x="470.0" y="105.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">STUDENT, STAFF,</text>
<text x="470.0" y="123.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">ANY_OTHER_KIND</text>
</svg>
</div>
<!--/svg-->

---

## What the Refactoring Did Not Do

* The odd third branch is **not hidden**: **hiding a suspected defect inside tidy code is the opposite of what refactoring is for**.
* `LoanRow` is **unchanged**; the signatures of `build` and `print` are **unchanged**, because other programs call them.
* The solid arrow means `OverdueReport` **holds** three `FinePolicy` values; the dashed arrow means it only **uses** `LoanRow`.

---

## Stage 4: Rename and Tidy

* `r` becomes `row`, `late` becomes `daysLate`; a **for-each** loop; `StringBuilder` instead of `String +=`; `count` and `total` become `overdueCount` and `totalFines`.
* **None of this changes the output.**

```java
long daysLate = ChronoUnit.DAYS.between(row.due, today);
if (daysLate > 0) {
    double fine = policyFor(row.kind).fineFor(daysLate);
    report.append(row.item).append(' ').append(row.borrower).append(' ')
            .append(daysLate).append(" day(s) late, fine ").append(money(fine)).append('\n');
    totalFines += fine;
    overdueCount++;
}
```

---

## The Request That Started the Chapter

* The staff grace period is now a **one-number change**: `new FinePolicy(7, 0.25, 5.00)`.
* It is a **functional change**: it waits for its own commit and test change.
* Run the suite after it: **five of the 28 report invocations fail**: the rows `T,6` (0.25 becomes 0.00), `T,25` (5.00 becomes 4.50), `T,26` (5.00 becomes 4.75), the mixed-list test and the differential test.
* Those failures are **the expected evidence of the intended change**. Update the expectations **in the same commit as the rule**.

---

# 11.6 Incremental Changes and Rollback
### One step, one check, one commit

---

## The Commit Sequence

| Commit | Kind | What the reviewer checks |
|---|---|---|
| 1. Add a date parameter to `build` (seam) | Mechanical edit before tests | The old method delegates and nothing else moved |
| 2. Add characterisation tests and the differential test | Tests only | Every expectation was run and reviewed; surprises commented |
| 3. Extract `fineFor` and `money` | Refactoring | The moved code is identical; all tests pass |
| 4. Extract `FinePolicy` | Refactoring | The algebra; all tests pass; the odd policy is visible |
| 5. Rename and tidy | Refactoring | No behavioural edits hide among the renames |

---

## Do Not Mix

* Mixing a refactoring and a behaviour change in one commit is **the most common way to lose control**.
* A failing test **no longer says which of the two caused it**.
* Chapter 5 made the same point with its two-stage change.
* The sixth commit in the companion (**rejecting unknown kinds**) is a different kind and reviewed as one: its message says what behaviour changed and why, and its test diff shows **old expectations deliberately replaced**.

---

## Decide What a Difference Means

<!--svg:ch11-difference-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="Figure 11.3: when a check reports a difference, ask whether the behaviour change was agreed. If not, inspect or undo the latest edit and rerun the unchanged expectations. If yes, separate the functional change, record the rule and the affected examples, and rerun." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch11-difference-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-difference-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-difference-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-difference-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch11-difference-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="115.0" width="175.0" height="66.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="97.5" y="143.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">A check reports</text>
<text x="97.5" y="163.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">a difference</text>
<polygon points="332.5,70.0 440.0,145.0 332.5,220.0 225.0,145.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="332.5" y="140.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Was this behaviour</text>
<text x="332.5" y="160.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">change agreed?</text>
<rect x="480.0" y="12.0" width="205.0" height="60.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="582.5" y="37.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Inspect or undo</text>
<text x="582.5" y="57.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">the latest edit</text>
<rect x="480.0" y="225.0" width="180.0" height="60.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="570.0" y="250.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Separate the</text>
<text x="570.0" y="270.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">functional change</text>
<rect x="690.0" y="225.0" width="170.0" height="60.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="775.0" y="250.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Record the rule and</text>
<text x="775.0" y="269.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">affected examples</text>
<rect x="690.0" y="118.0" width="175.0" height="66.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="777.5" y="146.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Rerun the unchanged</text>
<text x="777.5" y="165.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">expectations</text>
<path d="M185.0,148.0 L225.0,145.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-difference-arr)"/>
<path d="M332.5,70.0 L332.5,42.0 L480.0,42.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-difference-arr)"/>
<text x="350.5" y="60.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">No</text>
<path d="M332.5,220.0 L332.5,255.0 L480.0,255.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-difference-arr)"/>
<text x="352.5" y="246.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Yes</text>
<path d="M685.0,42.0 L788.0,42.0 L777.5,118.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-difference-arr)"/>
<path d="M660.0,255.0 L690.0,255.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-difference-arr)"/>
<path d="M775.0,225.0 L775.0,184.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch11-difference-arr)"/>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 11.3

* A check reports a difference: ask **one question before touching anything**: was this behaviour change **agreed**?
* An agreement needs **a specific rule**: "clean up the report" is not one.
* Until the records office agrees a rule for **unknown kinds** or for **loans inside their grace period**, a difference at those boundaries is **an unintended change**.

---

## Roll Back, Do Not Debug Forward

* After a step, a failing test gives you **a precise failing change** and a **green state one step behind**.
* **Undo the step** (`git restore` for uncommitted work, `git revert` for a commit) and **redo it more carefully**.
* Debugging forward from a half-changed structure is **slower and riskier**.
* The failing test is **evidence about what the step got wrong**: keep its name and message in your notes.

---

## Separate the Functional Correction

* Suppose the records office confirms only `"S"` and `"T"` exist and anything else is a **data error**.
* That is a **functional change**: its own branch and commit. `policyFor` throws `IllegalArgumentException("Unknown borrower kind: ...")`; `ANY_OTHER_KIND` disappears.
* The tests that **pinned** the suspected defect are **replaced deliberately in the same commit**, and the message says so.
* The differential test is **restricted to the kinds that did not change**.
* The rule itself is illustrative: **the records office decides it, not the developer**.

---

# 11.7 Technical Debt and Evidence
### A claim needs evidence

---

## The Metaphor

* "Technical debt": attributed to **Ward Cunningham**, the accumulated cruft that makes a system harder to change.
* The extra effort of every later change is the **interest**; cleaning up is **paying down the principal**.
* It helps in conversations with people who do not read code. It **misleads when it excuses neglect**.
* Fowler notes the cost **cannot be measured objectively, only estimated**.

---

## Attach Evidence

* "This code is messy" is an **opinion**.
* "A change to the staff grace period needs **two edits in one branch** and breaks silently if one is missed, and there is **no test**" is a statement a colleague can **check**.
* After the refactoring the same change is **one number**, protected by **27 characterisation tests**.

---

## A Register Entry

| Field | Entry for the report |
|---|---|
| Item | Overdue report: fine rules duplicated, hidden clock and locale |
| Evidence | Grace number appears twice per branch; output varies by date and locale; no tests |
| Cost (interest) | Each fine change needs careful edits in several places and a manual check |
| Decision | Paid down: seam, tests and refactoring in five commits |
| Remaining | Three suspected defects, one unknown |

---

## Four Kinds of Statement

* A **known defect**: confirmed wrong.
* A **suspected defect**: looks wrong, unconfirmed.
* **Accepted behaviour**: confirmed as intended, however odd.
* A **question**: unknown.
* **Only the owner of the requirement can move an item between them.** Mixing them is how a refactoring becomes an unreviewed behaviour change, and how a developer's taste becomes a defect report.

---

## The Pinned Behaviours and Questions for the Owner (1 of 2)

| Pinned behaviour | Class | Question |
|---|---|---|
| A loan within grace is listed with fine 0.00 and counted | Surprising (SD-11-2) | Should it appear at all? |
| Student fines start day 3, 0.50 a day, stop at 10.00 | Expected | None |
| Staff fines start day 6, 0.25 a day, stop at 5.00 | Expected | None |
| Any other kind pays 1.00 a day, no grace, no cap | **Suspected defect** (SD-11-1) | Do other kinds exist? Reject them? |

---

## The Pinned Behaviours and Questions for the Owner (2 of 2)

| Pinned behaviour | Class | Question |
|---|---|---|
| A loan due today, due later, or returned is not listed | Expected | None |
| A null kind throws `NullPointerException`, only for an overdue unreturned loan | Unknown (SD-11-3) | Can the export contain a null kind? |
| Amounts use the default locale: `0,50` under `Locale.GERMANY` | Surprising (SD-11-4) | Should the separator follow the machine or the office? |

---

# 11.8 AI in Practice: Review a Refactoring Patch
### "Equivalent" is a claim to trace

---

## Activity Frame (1 of 2)

| Element | For this activity |
|---|---|
| Engineering objective | Decide whether a proposed refactoring patch preserves behaviour, using evidence rather than the patch's own claims |
| Input | The refactored `OverdueReport` from 11.5, the characterisation suite and the differential test |
| Permitted scope | Evaluate and, if worthwhile, repair the patch; **do not change the tests to make it pass** |

---

## Activity Frame (2 of 2)

| Element | For this activity |
|---|---|
| Independent checks | Trace the boundary case by hand; apply each claim to a scratch copy; run the suite; read each failing test |
| Accept or reject | A verdict on each claim, with the failing tests as evidence |
| No-account route | The fixture is sufficient |

---

## The Fixture

**Author-written fictional AI output.**

> I tidied `build`. The overdue test is now `!row.due.isAfter(today)`, which reads better and is equivalent to `daysLate > 0`. I also choose the fine policy before the check, so the loop has one path. Unknown kinds fall back to the student policy, since students are the only borrowers who should ever be fined. All formatting is unchanged, so behaviour is preserved.

---

## The Patch

```java
long daysLate = ChronoUnit.DAYS.between(row.due, today);
FinePolicy policy = row.kind.equals("T") ? STAFF : STUDENT;
if (!row.due.isAfter(today)) {
    double fine = policy.fineFor(daysLate);
    // ... append the line, add to the total and the count, as before
}
```

* **Trace the first claim before running anything.** On the due date `daysLate` is 0, so the original skips the row. What does `!row.due.isAfter(today)` do for a row due today?

---

## Verdicts (1 of 2)

| Claim | Finding |
|---|---|
| `!row.due.isAfter(today)` is equivalent to `daysLate > 0` | **False on the due date**: `daysLate` is 0 so the original skips the row, but `isAfter` is false so the patch includes it. 5 invocations fail |
| Choose the policy before the check | **A second behaviour change**: a row not yet due now has its kind inspected, so a null kind throws where it was ignored. 1 invocation fails: the only test that notices |

---

## Verdicts (2 of 2)

| Claim | Finding |
|---|---|
| Unknown kinds fall back to the student policy | **A functional change presented as a tidy-up**: `X`, `s` and blank paid 1.00 a day; now they follow student rules. 5 invocations fail |
| Formatting is unchanged, so behaviour is preserved | **True premise, false conclusion**: formatting is not the only behaviour. **9 of the 38** report and bridge invocations fail |

* **Reject it as a refactoring.** The first two can be repaired; the third needs a decision from the records office.

---

## Tracing and Running

* The equality case can be settled by **tracing the due date before any test runs**.
* The null-kind change is **not visible from the patch text** unless you ask what each line now does for a row that is not overdue.
* **Applying the claims one at a time** is what lets each failing test point at one claim.
* Do not use a generated test to approve a generated change.

---

# 11.9 Common Mistakes
### Eleven to avoid

---

## Mistakes 1 to 4

| Mistake | Consequence | Better action |
|---|---|---|
| Fix a suspected defect during a refactoring | One commit cannot be reviewed as "no behaviour change" | Pin it, record the question, fix it later in its own commit |
| Paste actual output into tests without reading it | The suite blesses bugs invisibly | Classify each result and comment the odd ones |
| Test only the happy path of a legacy method | Odd branches change unnoticed | Probe boundaries, unknown inputs, nulls, hidden dependencies |
| Make a large edit to create a seam | The seam edit is itself untested | The smallest mechanical edit, checked by eye |

---

## Mistakes 5 to 8

| Mistake | Consequence | Better action |
|---|---|---|
| Leave a test changing the locale or `System.out` unrestored | Unrelated tests fail far away | Restore global state in `finally` or `@AfterEach` |
| Refactor several things per commit | Failures cannot be attributed | One refactoring per commit, tests between |
| Read "all tests pass" as "behaviour identical" | Untested behaviour was never protected | State what the tests cover and what they do not |
| Refactor everything that smells | Time spent where nothing will change | Pick smells that block a change you must make |

---

## Mistakes 9 to 11

| Mistake | Consequence | Better action |
|---|---|---|
| Change the shape of a public type other programs use | Hidden callers break | Keep signatures and formats others depend on |
| Trust the seam edit because it compiled | The one untested edit could still have changed behaviour | Run the original beside the seamed version on a few rows, then pin |
| Accept "equivalent" for a boundary rewrite | `isAfter` and a day count differ exactly on the due date | Trace the equality case by hand, then run the tests |

---

# 11.10 Practical Activity
### Book project B1 to B7; Team project T1 to T4

---

## Input and Demonstrations

* **Input:** the Chapter 10 checkpoint plus the `legacy` package (`LoanRow`, the stage 1 report, the characterisation suite, the differential test, the probe) and your Team project's repository.
* **Demonstration:** run the legacy report on one day and then another (or two dates through the seam) to show **why the clock must be isolated**. Run the probe. **Pin one surprising result live, with its comment.**
* **Guided practice:** classify five pinned results from 11.3 and say what you would ask the records office about each.

---

## B1 and B2

* **B1. Observe and characterise.** Run the probe, then the supplied suite against stage 1. Add **three characterisation tests of your own** (many loans for one borrower; two loans for the same item; a due date far in the past). For each: record the actual result, **classify it**, comment if surprising.
* **B2. Refactor in small steps.** From stage 1, apply Extract Method and Extract Class (stages 2 and 3), **one commit each**, running the suite after each. **If a test fails, roll back and redo.**

---

## B1: Three Example Answers

| Input | Observed | Class |
|---|---|---|
| Two rows for the same item, both overdue | Two lines, in input order, fines added | Expected |
| A student exactly 22 days late, then 23 | 10.00 for both; the cap is reached at 22 | Expected (a boundary worth pinning) |
| A row with a blank item name | A line that starts with a space | Surprising: can blank names occur? |

---

## B3 and the Team Project Steps

* **B3. Report your findings.** What changed structurally, **what you checked after each step**, what **did not change on purpose** (and why), and which **questions remain**. Add one **suspected-defect register** entry.
* **T1. Choose** one method in your starter codebase with a smell and no tests, that you have a reason to change. Reading note: observation, how you know, status.
* **T2. Pin.** The smallest enabling edit; run original beside edited; **at least six** characterisation tests including a boundary and an odd case; classify each.
* **T3. Refactor.** **At least three** small refactorings, each its own commit, tests before each.
* **T4. Rationale** and a teammate's review.

---

## Optional Extension (Book Project)

* **B4. Break the boundary on purpose:** change `daysLate > 0` to `daysLate >= 0`. **Predict which tests fail before you run them**, read the messages, restore.
* **B5. A separate functional change:** unknown kinds are rejected. Replace pinned tests deliberately; restrict the differential test; write the commit message to say what changed and why.
* **B6.** The AI activity.
* **B7. Connect the report to the live loans** through the bootstrap bridge.

---

## B7: The Bridge to Live Loans

* `LoanSnapshotRows` joins the loan and reservation snapshots into report rows. A loan carries no due date, so it comes from its reservation: **the last permitted day is the day before the exclusive end**. `[20 Oct, 22 Oct)` is due back on **21 October**; the report counts it late from 22 October.
* `OverdueReportService` reads **one date from a `Clock`** and **one snapshot per call**. A source failure **propagates**: it is never reported as "0 overdue".
* A loan with **no matching reservation**, one that **disagrees with its reservation**, and a borrower **with no kind** are each an **error**, not a row.
* It lives in **bootstrap**, the only place allowed to know both the lending layers and `legacy`.

---

## Expected Artefacts and Acceptance

* **Artefacts:** B1 to B3 with the commits or stage files; for the Team project, observation notes, characterisation tests, **at least three refactoring commits**, the rationale and the review.
* **Accept when:** every characterisation test was **run before its expectation was recorded**; surprising and suspect results are commented; **no refactoring commit changes behaviour**; tests pass after every commit; the seam edit is mechanical and was checked against the original; questions are recorded, **not silently fixed**; signatures others depend on are unchanged.
* A passing suite is evidence for the behaviours it covers, **not a proof of equivalence**.

---

## Do the Tests Detect Faults? (1 of 4)

| Area | Faults tried | Result |
|---|---|---|
| Student rules | Grace 2 to 3; rate 0.50 to 0.60; cap 10 to 9 | All three caught |
| Staff rules | Grace 5 to 4; rate 0.25 to 0.30; cap 5 to 6 | All three caught |
| Other kinds | One grace day; a cap of 10; lower-case `s` accepted as a student | All three caught |

---

## Do the Tests Detect Faults? (2 of 4)

| Area | Faults tried | Result |
|---|---|---|
| Policy arithmetic | `Math.max` instead of `Math.min`; grace test `<` instead of `<=` | `max` caught. The `<` change **survives**: an **equivalent mutant**, since at exactly the grace day the fine is `(grace - grace) * rate = 0` either way |
| Listing rules | Due today counted as overdue; returned loans not skipped; count off by two; total not accumulated | All four caught |
| Zero-fine patches | Zero-fine loans skipped; fine computed first and zero-fine loans skipped | Both caught |

---

## Do the Tests Detect Faults? (3 of 4)

| Area | Faults tried | Result |
|---|---|---|
| The AI claims | `!isAfter`; policy looked up first; unknown kinds as students; all three together | All four caught |
| Hidden dependencies | Amounts always formatted with a point; header uses the system date; print writes to standard error; short entry point uses yesterday | All four caught |
| Date arithmetic | Dates subtracted the wrong way round; days late from `Period.getDays()` | Both caught |

---

## Do the Tests Detect Faults? (4 of 4)

| Area | Faults tried | Result |
|---|---|---|
| Bridge | The due day is the exclusive end; returned flag inverted; mismatched loan not detected; null kind passed through | All four caught |
| Service | A source failure becomes an empty report; null snapshot as empty; system date instead of the clock; clock zone ignored; snapshot cached between reports | All five caught |

* **36 faults; 35 caught; 1 survives** (the equivalent mutant). First round: 22 of 24 caught; the test `aNullKindOnALoanThatIsReturnedOrNotYetDueIsIgnored` was added to close one gap.
* `Period.getDays()` is a realistic assistant suggestion: it returns the **days field only**, so 100 days late would not count as 100.

---

# 11.11 Review and Transfer
### Concept, diagnosis, transfer, Quiz 2

---

## Concept Questions

1. Why is a characterisation test not the same as a regression test, and what does a passing characterisation test tell you?
2. What is a seam, and why is the date parameter a better first edit than rewriting the method?
3. Why should a suspected defect be pinned rather than fixed during a refactoring?
4. What can a differential test show that a table of examples cannot, and what can it not show?

---

## Diagnosis Questions (1 of 2)

5. A teammate refactors the report and says "all tests pass, so nothing changed". Name two kinds of behaviour the suite does not cover, and say what you would do about each.
6. A developer extracts `FinePolicy` and, in the same commit, changes the staff cap from 5.00 to 6.00 "because it looked low". Explain what is wrong with the commit and what the test run would and would not show.

---

## Diagnosis Questions (2 of 2)

7. The report runs at 22:30 UTC on a server whose clock zone is Baghdad. A loan was due on 21 October. Which date does the report use, what does it print for that loan, and which one object chooses the zone?

---

## Guidance: Questions 1 to 4

1. A **regression** test protects agreed-correct behaviour; a **characterisation** test records whatever the code does today. A pass means **unchanged, not right**.
2. A seam lets you change behaviour **without editing there**; the second parameter of `build` is the enabling point. It is **mechanical, compiler-checked and small enough to review**, so it can precede any test.
3. A refactoring is defined by **unchanged behaviour**. Combining a fix with it **makes a failing test ambiguous** and review impossible. Pinning keeps the suspect behaviour **visible and protected** until the owner decides.
4. It compares **thousands of generated inputs** with the original, finding differences nobody wrote an example for. It cannot test inputs **the generator does not produce**, and is only as good as the oracle.

---

## Guidance: Questions 5 to 7

5. Not covered: **other time zones or midnight** (the short entry point reads the clock); **null items or borrowers** (a null name prints as `null`); **very large lists**. Add a test for the case you are about to touch, or record it as a **known gap**.
6. The commit **cannot be reviewed as "no behaviour change"**. The staff rows and the differential test fail and look like a refactoring error, or the developer **edits the expectations and hides the change**. Revert the cap, refactor, then change the cap in its own commit.
7. At 22:30 UTC it is 01:30 on **22 October in Baghdad**. A Baghdad clock uses 22 October: **one day late, fine 0.00, still listed**. A UTC clock uses 21 October: **not listed**. The **`Clock` supplied to `OverdueReportService`** chooses the zone.

---

## Transfer Challenge: An ML-Serving Script

An analysis script in an ML model-serving tool formats prediction scores for a daily summary. It **reads the current time, prints numbers in the default locale, and has three near-identical branches** for different model types. **No tests.**

* Describe how you would find its **seams**.
* Which **six or seven inputs** would you pin first?
* Which **refactorings** would you apply?
* Name **one behaviour you would record as a question** instead of fixing.

---

## Transfer Guidance

* **Seams:** a date parameter on the entry point; pin the locale in the fixture; capture standard output once.
* **Pin first:** a score at **each boundary** of a model type's rule; one at the **maximum**; an **unknown model type**; an **empty list**; a **null**; the **locale** case.
* **Refactor:** Extract Method for the formatting; Extract Class for the three near-identical branches (a small value object holding **what differs**); Rename.
* **Question, not fix:** whatever **an unknown model type does today**.

---

## Quiz 2 Revision Pointers (1 of 3)

* Quiz 2 is held in **Week 10** and covers **dependency injection, TDD and test doubles, design patterns and layered architecture (Weeks 5 to 9)**.
* **Revise Chapters 6 to 10.** Do not treat this chapter's legacy lab as quiz content.

| Chapter | Revision focus |
|---|---|
| 6 | Interfaces and ISP, dependency direction, constructor injection, composition root, what a container automates |
| 7 | Red-green-refactor, test anatomy, stubs, fakes, spies and mocks, controlled time, weak tests |

---

## Quiz 2 Revision Pointers (2 of 3)

| Chapter | Revision focus |
|---|---|
| 8 | Factory Method, Abstract Factory, Builder, Adapter, Decorator, and choosing the simpler alternative |
| 9 | Strategy, State, Observer and Command, partial failure, and choosing a pattern by the variation it handles |
| 10 | Layers and dependency direction, ports and adapters, repositories, entities and value objects, package cohesion, coupling and stability |

---

## Quiz 2 Revision Pointers (3 of 3)

* Use the **module leader's confirmed quiz guidance** if it provides more detail.
* These pointers **add no assessment rules and predict no particular questions**.

---

# Summary and Next Chapter
### What to carry forward

---

## Summary

* Changing code you do not understand is **a sequence, not a leap**: observe, make the smallest edit that lets you test it, pin behaviour, reshape in small steps with a check and a way back, and keep behaviour corrections **apart** from structure improvements.
* **Smells say where to look**, **debt claims need evidence**, and **a green suite is evidence for the behaviours it covers**.

---

## Where the Report Stands

* A **seam checked against the original**.
* A **pinned suite**.
* A **small policy class**.
* **Four recorded oddities** waiting for the records office.
* **Chapter 12** turns to measuring progress and flow, and introduces the visiting-researcher change request the rest of the project must absorb.

---

## Sources and Further Reading

1. **Fowler:** *Definition of Refactoring*; the *Refactoring catalogue*; *Technical Debt*; *Code Smell*; *Legacy Seam*.
2. **Feathers:** *Characterization Testing*; *Testing Effectively With Legacy Code*; *Working Effectively with Legacy Code* (2004).
3. **Oracle:** Java SE 17 `Formatter`, `Clock`, `ChronoUnit` and `Period`.
4. **JUnit:** User Guide 5.13.4.
5. **Martin:** *Agile Software Development* (2002).

* Full references and links are in the chapter text.
