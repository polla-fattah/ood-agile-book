---
title: "Chapter 5: Responsibilities, Extension, and Substitutability"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 50
type: slides
layout: page
---

# Chapter 5: Responsibilities, Extension, and Substitutability
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **5.1 Why would this code change? Change pressure on the service**
  * Compiler, your own reading and PMD, side by side. A new staff rule, stated before any design.
* **5.2 One class, one reason to change? Responsibility and SRP**
  * A reason to change is more useful than a method count.
* **5.3 Making room for variation: OCP and anticipated change**
  * Closed against which change? An honest intermediate design.
* **5.4 What can a caller rely on? Behavioural contracts**
  * Preconditions, postconditions, invariants.

---

## Chapter Roadmap (2 of 3)

* **5.5 When a subtype breaks its promises: LSP and unsafe inheritance**
  * A subtype that compiles and still breaks a client.
* **5.6 Small refactorings and the checks that guard them**
  * Stage A (refactoring) and Stage B (feature) kept apart.
* **5.7 When is an abstraction too early? Avoiding premature abstraction**
  * Every boundary has a cost.
* **5.8 Reviewing a “make this SOLID” suggestion with AI**

---

## Chapter Roadmap (3 of 3)

* **5.9 Design habits that look principled**
* **5.10 Try it yourself: a protected design change**
  * Eight steps; step 8 is on your team's project.
* **5.11 Questions to think with** and **5.12 A different setting: the transfer challenge**
  * A coursework feedback tool.
* **What to take away, and what comes next**
  * Chapter 6: client-specific interfaces, dependency direction, manual assembly.

---

## Learning Outcomes (1 of 2)

By the end of this chapter, you should be able to:

1. **Identify independent reasons for a class to change** using concrete requirements.
2. **Apply SRP** to separate a responsibility and explain the cost of the new boundary.
3. **Justify an extension point** for an observed variation without claiming existing code must never change.

---

## Learning Outcomes (2 of 2)

4. **Describe a behavioural contract** and diagnose a subtype that breaks a client's expectations.
5. **Make a small protected refactoring**, distinguish it from a feature change, and report the supporting evidence.

---

## Where This Chapter Fits

* The first **SOLID** chapter. It supports the formative **smell analysis** and does not change assessment arrangements.
* **Chapter 6:** interface segregation, dependency direction and injection.
* **Chapter 7:** testing practice. **Chapter 11:** systematic smells and legacy refactoring.
* Readings: the SRP, OCP and LSP chapters of Martin, and "Bad Smells in Code" from Fowler.

---

## Where You Start and the Two Stages

* **You start with:** Chapter 4's Java 17 reservation starter, its **34 regression checks** and **five acceptance example groups**.
* US-02 (availability enquiry) **remains planned**.
* The staff rule is a small, explicitly introduced **teaching variation**, not an approved policy.
* **Stage A:** extract formatting **without changing existing behaviour**.
* **Stage B:** add the documented staff variation **while preserving the old student entry point**.

---

## How to Use This Chapter

* **Core reading:** Sections 5.1 to 5.7.
* **What you must do:** steps 1 to 8 of Section 5.10, including the review in step 6 (with another person, or labelled a solo self-review).
  * Steps 1 to 7: the book's project. Step 8: your team's project.
* The lab uses **PMD 7.28.0**, which needs a **one-time download** (described in 5.1).
* **If you want more:** the AI activity, the extension in 5.10, the questions and the transfer challenge.

---

## Opening Scenario: Two Requests, Two Proposals

* The officer asks for a different **confirmation layout**.
* The team must also demonstrate a **second borrowing policy for staff**.
* One developer proposes **a subclass of the reservation coordinator**.
* Another asks an AI assistant to **"make the code SOLID"**.
* The assistant returns **interfaces for almost every class** and turns a rejection into an exception.

---

## The Questions Nobody Has Answered

* Which parts change **for different reasons**?
* Which behaviour should **vary**?
* What may existing callers **continue to rely on**?
* How will the team distinguish **an internal improvement from a new feature**?
* The code looks more elaborate. **More classes, interfaces or principle names are not an improvement by themselves.**

---

## Three Principles as Ways to Reason

* **SRP**: the Single Responsibility Principle.
* **OCP**: the Open-Closed Principle.
* **LSP**: the Liskov Substitution Principle.
* Treat them as ways to **reason about changes and contracts**, not as slogans.

---

# 5.1 Why Would This Code Change?
### Change pressure on the service

---

## Begin With the Code That Exists

* `ReservationCoordinator` validates arguments, counts a borrower's reservations, asks `ReservationRules`, checks overlap, stores, and constructs a confirmation.
* Chapter 2 moved string construction into a private method. Chapter 4 made the checks repeatable.
* That is a useful baseline for asking whether **a further boundary is justified**.

---

## Several Steps Are Not a Fault

* Coordinating a reservation **necessarily involves several collaborators and decisions**.
* The more useful question: do **unrelated changes repeatedly force edits into the same place**?
* The table on the next slides lists five change pressures.

---

## Change Pressures (1 of 2)

| Change pressure | Main knowledge involved | Current location |
|---|---|---|
| Change confirmation wording | Presentation of a completed reservation | Coordinator's private formatting method |
| Add a second count/duration policy | Borrower eligibility rules | Existing rule plus new selection behaviour |
| Change interval overlap semantics | Meaning of a loan period | `LoanPeriod` |

---

## Change Pressures (2 of 2)

| Change pressure | Main knowledge involved | Current location |
|---|---|---|
| Preserve records across restart | Storage lifetime and retrieval | Coordinator's in-memory list |
| Reject unknown equipment identifiers | Authority for equipment identity | Not implemented |

* The first two are the chapter's **actual teaching changes**.
* Persistence and catalogue integration are future questions: **a reason to document a limitation, not to build an extensibility framework now**.

---

## State the New Rule Before Choosing a Design

| Category | Existing active reservations allowed before a successful request | Requested duration |
|---|---|---|
| Student | 0, 1 or 2 | 1 through 7 days |
| Staff | 0, 1, 2, 3 or 4 | 1 through 14 days |

* A successful student request may create the **third** active reservation; a successful staff request the **fifth**.
* Both reject negative counts and nonpositive durations.
* Both still require a valid period and **no overlap** for the same item.

---

## This Is a Feature Change

* A staff request for fourteen days can now succeed where the existing four-argument operation **would reject it**.
* Moving the existing formatter is a refactoring **only if its observable results remain the same**.
* Combining the two in one unexplained edit makes failures **harder to interpret**.

---

## The Category Is Trusted, Not Verified

* The example receives the category from a **trusted caller**.
* It does **not** authenticate staff status, persist a borrower profile or infer category from an identifier.
* Passing `STAFF` is **not proof that a person is staff**.
* A production boundary would need an **authoritative category source**. Adding an enum does not complete that task.

---

## Define Success for Each Stage

* **Stage A succeeds** when the formatting responsibility has moved and existing **outputs, exceptions, state changes and signatures** remain compatible for existing callers.
* **Stage B succeeds** when the explicit category operation implements the new table while the **old operation still means student borrowing**.

---

## Boundaries That Stay Fixed

* All stored records still count as **active**.
* Storage remains **in memory**; calls remain **sequential**; intervals remain **half-open**.
* **No** cancellation, return processing, catalogue, email delivery or availability enquiry is added.
* These boundaries stop a design exercise becoming **an unreviewable expansion of the system**.

---

## The Two Stages

<!--svg:ch05-stages-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 215" role="img" aria-label="Baseline gate passes; Stage A extracts the formatter as a refactoring; the unchanged checks run; Stage B adds the staff policy as a feature change; the old and new checks run." style="display:block;width:100%;height:calc(var(--u) * 21.50);margin:0 auto">
<defs><marker id="ch05-stages-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-stages-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-stages-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-stages-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-stages-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="30.0" width="150.0" height="96.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="85.0" y="73.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Baseline</text>
<text x="85.0" y="94.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">gate passes</text>
<rect x="190.0" y="30.0" width="150.0" height="96.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="265.0" y="62.5" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Stage A:</text>
<text x="265.0" y="83.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">extract the</text>
<text x="265.0" y="105.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">formatter</text>
<rect x="370.0" y="30.0" width="150.0" height="96.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="445.0" y="62.5" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Unchanged</text>
<text x="445.0" y="83.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">checks</text>
<text x="445.0" y="105.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">still pass</text>
<rect x="550.0" y="30.0" width="150.0" height="96.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="625.0" y="62.5" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Stage B:</text>
<text x="625.0" y="83.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">add the staff</text>
<text x="625.0" y="105.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">policy</text>
<rect x="730.0" y="30.0" width="150.0" height="96.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="805.0" y="73.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Old and new</text>
<text x="805.0" y="94.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">checks pass</text>
<path d="M160.0,78.0 L190.0,78.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-stages-arr)"/>
<path d="M340.0,78.0 L370.0,78.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-stages-arr)"/>
<path d="M520.0,78.0 L550.0,78.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-stages-arr)"/>
<path d="M700.0,78.0 L730.0,78.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-stages-arr)"/>
<text x="265.0" y="160.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="middle">refactoring</text>
<text x="265.0" y="183.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">behaviour unchanged</text>
<text x="625.0" y="160.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="middle">feature change</text>
<text x="625.0" y="183.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">student entry point kept</text>
</svg>
</div>
<!--/svg-->

---

## Three Kinds of Evidence, in This Order

1. **The compiler's.**
2. **Your own.**
3. **The tool's.**

* A static-analysis tool examines source **without running it** and reports patterns that often indicate problems.
* Setting the three side by side is the point of the lab.

---

## The Compiler: `javac -Xlint:all`

```bash
javac --release 17 -Xlint:all -d build/lint \
    src/main/java/*.java src/test/java/*.java
```

* On the Chapter 4 starter it prints **nothing**.
* That is informative: the compiler checks **language-level hazards** (unchecked conversions, fall-through), not whether wording and eligibility belong in one class.

---

## Your Own Reading First

* Do the **manual smell review before you run any analyser**, so the tool's output has something to be compared with.
* Read `ReservationCoordinator` once for **each of four smells** and write down each place with its line or method.
* For each finding record: where, what you observed, whether it matches a change pressure, whether you would act.
* Also name **one pressure the compiler did not report and that you found only by reading**.

---

## The Four Smells (1 of 2)

| Smell | What to look for |
|---|---|
| More than one reason to change | A method that mixes eligibility, conflict search, record creation and message wording |
| Hidden construction | A class that creates its collaborators with `new` inside its own methods |

---

## The Four Smells (2 of 2)

| Smell | What to look for |
|---|---|
| Repeated or similar logic | Two loops over the stored list that differ only in the test, or rejection outcomes returned as plain strings a caller must compare |
| Primitive values standing for concepts | Strings or integers carrying meaning (an identifier, a number of days, a rejection reason) without a type of their own |

---

## Five Terms Before the PMD Output

* **Cyclomatic complexity:** the number of **independent paths** through a method; each `if`, loop or `case` adds one.
* **Cognitive complexity:** a variant that **penalises nested** conditions.
* **NPath:** the number of possible **execution paths** through a method.
* **God class:** does too much and knows too much. **Data class:** holds data and little behaviour.
* In the Data-class line, **WOC, NOPA, NOAM and WMC** are PMD's measures of how much of a class is behaviour. **You do not need them to read the result.**

---

## The Analyser: PMD

* The book uses **PMD 7.28.0**, which runs on Java 8 or above.
* Download `pmd-dist-7.28.0-bin.zip` from the project's GitHub release page.
* **Compare the SHA-256 digest** with the one the release page shows (the companion records the digest that was checked).
* Unzip it and set **`PMD_HOME`** to the `pmd-bin-7.28.0` folder.
* This is **the only download the chapter asks for.**

---

## Choosing Rules Is Part of Using PMD

* On the five-file starter, the **quickstart** rule set reports **5** findings, all the same one: classes without a package (chosen deliberately until Chapter 10).
* The **code-style** category reports **34**, for example parameters that "could be final".
* Neither helps a smell diagnosis.
* The lab uses a **small set of eight design rules** from PMD's design category, kept in `config/pmd-smells.xml`, with PMD's default thresholds.

---

## The Eight Lab Rules

* **Cyclomatic complexity** from 10.
* **Cognitive complexity** from 15.
* **NPath** from 200.
* **God class**.
* **Data class**.
* **More than 10 methods**.
* **10 or more parameters**.
* **30 or more imports**.

---

## Running the Lab

```bash
export PMD_HOME=/path/to/pmd-bin-7.28.0
bash scripts/check.sh
bash scripts/pmd.sh
```

* Run the **compiler gate first**, so PMD can read the compiled classes.
* On the Chapter 4 starter it reports two findings (paths and wording shortened here):

```text
Reservation.java:3:  DataClass: suspected Data Class (NOAM=4, WMC=9)
ReservationCoordinator.java:10:  CyclomaticComplexity: 'reserve(...)' has complexity 12
[INFO] Found 2 violations.
```

---

## Finding 1: `reserve` Has Complexity 12 (Useful)

* It validates identifiers, counts the borrower's records, applies eligibility, searches for a conflict and creates the record.
* That is **your first smell seen from another side**.
* Act on the part that has a pressure: **wording (Stage A)** and **eligibility (Stage B)**. Leave the sequence of checks, and say so.

---

## Finding 2: `Reservation` Is a Data Class (Low-Value Here)

* `Reservation` is deliberately an **immutable record of an accepted booking**. Holding data and little behaviour is its job.
* It does carry a question: **where does the behaviour that uses its fields live?**
* In this starter, in the coordinator's confirmation wording. That is what Stage A moves.

---

## What PMD Missed

* It did not report the **`ReservationRules` that the coordinator constructs for itself**.
* It cannot know that **"borrower limit or duration" is one string for two different reasons**.
* The comparison the lab asks for places each finding in **one of three groups**:
  * **useful**,
  * **low-value in this context**,
  * **a concern the tool missed**.

---

## A Finding Is Evidence, Not an Instruction

* At this scale a tool may report items that do not matter, and it cannot know which changes your team expects.
* Rerun PMD after each stage: the complexity finding **stays at 12** after Stage A and Stage B.
* Moving wording and policy out changed **who decides**, not **how many branches the sequence of checks has**.
* Record only output you actually produced.

---

## A Number Is Not a Verdict

* **Extract Method** alone can lower the complexity number while **leaving every responsibility where it was**.
* The companion's experiment: extracting `activeReservationsOf(borrowerId)` and `isUnavailable(itemId, requested)` made the finding disappear. The gate still passed (44 checks, five acceptance groups).
* The class still validates, counts, checks eligibility, searches and creates.
* Say **what the tool measures** and **what the change targeted**.

---

# 5.2 One Class, One Reason to Change?
### Responsibility and SRP

---

## SRP Focuses on Reasons to Change

* SRP focuses attention on changes arising from **different responsibilities**.
* Martin connects responsibilities to **the people or groups whose needs drive changes**.
* The people deciding **borrowing limits** may have different concerns from those deciding **how an officer reads a confirmation**.

---

## Method Count Is Unreliable

* A class with several methods can support **one coherent responsibility**.
* A one-method class can **mix policy, storage and presentation**.
* `LoanPeriod` has construction, accessors and overlap, yet describes **one coherent interval abstraction**.
* An organisational chart is **evidence about change**, not a class-generation algorithm.

---

## Twenty Tiny Helpers Are Not a Cure

* Suppose the coordinator's method is short because it delegates to **twenty tiny helpers**.
* If they all reach into **the same mutable list** and repeat the same decision logic, the design may still be difficult to change.
* Smaller methods are not the same as **separated responsibilities**.

---

## Stage A: Extract a Collaborator

* Move the confirmation construction into **`ConfirmationFormatter`**.
* Its **input** is the immutable `Reservation` already accepted. Its **output** is a string.
* It does **not** approve a request, add a record or send a message.

```java
reservations.add(reservation);
return formatter.format(reservation);
```

---

## The Formatter

```java
public final class ConfirmationFormatter {
    public String format(Reservation reservation) {
        Objects.requireNonNull(reservation, "reservation");
        return "Confirmed: " + reservation.id()
                + " for " + reservation.borrowerId()
                + " on " + reservation.itemId()
                + " [" + reservation.period().start()
                + ", " + reservation.period().endExclusive() + ").";
    }
}
```

---

## What the Extraction Preserves

* Formatting is **still performed after the reservation is stored**.
* There is no transaction handling or rollback if some future formatter fails.
* If formatting later gains external dependencies, **failure semantics need a separate design decision**.
* Passing **one coherent reservation object** avoids a long list of unrelated arguments.
* The formatter must **not** receive the coordinator's mutable list: that would give presentation access to storage decisions.

---

## The Cost of the New Boundary

* The original private method was **already a useful seam**.
* A separate class gives the formatting change a **named home** and lets you examine it without running a reservation scenario.
* The cost: **another file, another object, another call to follow**.
* If formatting were a stable one-line expression with no independent change pressure, **keeping the private method could be reasonable**.

---

## What Remains Together

* The coordinator **still creates collaborators directly** and **owns the list**.
* One extraction does not finish its design. Chapter 6 examines how collaborators are supplied.
* The numeric rules were **already outside the coordinator**: do not claim to have newly separated them.
* The actual change: eligibility and presentation now have **named homes**; the coordinator keeps **sequencing**.

---

## A Rationale With a Reason, a Boundary and Evidence

> Confirmation wording can change independently of eligibility and conflict handling. Move it to a formatter that accepts an accepted reservation. Keep the returned text and storage order unchanged, and run existing exact-output checks.

* "Applied SRP" alone identifies **none** of the three.

---

## Do Not Leak Decisions Into the Formatter

* A formatter that checks the requested duration and returns confirmation or rejection **recreates a policy decision in presentation**.
* One that allocates the identifier because it appears in the message confuses **using** an identifier with **assigning** it.
* Ask: **which object has the information and authority** to make each decision?
* The coordinator knows the stored records; the formatter knows how to represent an accepted one.

---

# 5.3 Making Room for Variation
### OCP and anticipated change

---

## Name the Axis of Extension

* OCP encourages a design where **an anticipated kind of extension** can be introduced without repeatedly rewriting stable behaviour.
* The relevant question: **"closed against which change?"**
* There is no promise that **every imaginable requirement** can be added without touching existing code.

---

## The Observed Variation

* A **count-and-duration decision** for two borrower categories.
* **Not** storage technology, notification transport, date arithmetic or authentication.
* A small interface expresses exactly that decision.

```java
public interface BorrowingPolicy {
    boolean mayRequest(int activeReservations, int requestedDays);
}
```

---

## An Interface Needs a Contract

* A class declares `implements BorrowingPolicy` and supplies its public method.
* `@Override` lets the compiler check that the declaration matches.
* The interface **does not supply the meaning of the operation by itself**. We must document its contract too.

---

## The Two Policies

```java
public final class ReservationRules implements BorrowingPolicy {
    @Override
    public boolean mayRequest(int activeReservations, int requestedDays) {
        return activeReservations >= 0 && activeReservations < 3
                && requestedDays >= 1 && requestedDays <= 7;
    }
}
```

* `StaffReservationRules` is identical in shape with `< 5` and `<= 14`: an illustrative teaching policy, not an approved rule.

---

## One Algorithm, Two Policies

* The coordinator **obtains a policy and asks the same question** of it.
* Overlap detection and storage are **not duplicated** into separate student and staff coordinators.
* `BorrowerCategory` is a simple enum: `STUDENT`, `STAFF`.

---

## Preserve the Old Entry Point Explicitly

```java
public String reserve(String borrowerId, String itemId,
                      LocalDate start, int requestedDays) {
    return reserve(borrowerId, itemId, start, requestedDays,
                   BorrowerCategory.STUDENT);
}
```

* The old four-argument operation **delegates with `STUDENT`**: existing code compiles and keeps its student interpretation.
* Choosing staff behaviour requires an **explicit call**.

---

## Do Not Infer Status From an Identifier

* Do **not** use `borrowerId.startsWith("S")`.
* That would hide **a new identity rule in a convenient string convention**.
* The synthetic identifier S1 in the demo is just a label. **The category argument selects the policy.**

---

## Counts Are Per Borrower Identifier

* Every record for the same borrower identifier contributes to the active count, **whichever overload created it**.
* There are no separate student and staff buckets, and the borrower's category is **not remembered**.
* If a caller supplies inconsistent categories, each request uses the supplied category against **all** that borrower's records.
* A limitation of the **example boundary**, not a model of authorised category changes.

---

## The Remaining Selector

```java
private BorrowingPolicy policyFor(BorrowerCategory category) {
    return switch (category) {
        case STUDENT -> studentPolicy;
        case STAFF -> staffPolicy;
    };
}
```

* Adding another enum category still needs **another arm here**. The coordinator is **not completely closed** to new categories.
* The improvement: the algorithm **delegates the varying rule**.

---

## Figure 5.1: Collaborations After Stage B

<!--svg:ch05-fig51-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 350" role="img" aria-label="Figure 5.1: ReservationCoordinator holds a BorrowingPolicy reference and a ConfirmationFormatter. ReservationRules and StaffReservationRules realise the BorrowingPolicy interface. The coordinator also depends on the two concrete policies because it creates them." style="display:block;width:100%;height:calc(var(--u) * 35.00);margin:0 auto">
<defs><marker id="ch05-fig51-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-fig51-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-fig51-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-fig51-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-fig51-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="95.0" width="280.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,131.0 L12.0,101.0 Q12.0,97.0 16.0,97.0 L284.0,97.0 Q288.0,97.0 288.0,101.0 L288.0,131.0 Z" fill="#e6eef6"/>
<text x="150.0" y="120.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReservationCoordinator</text>
<rect x="470.0" y="10.0" width="299.7" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M472.0,66.0 L472.0,16.0 Q472.0,12.0 476.0,12.0 L763.7,12.0 Q767.7,12.0 767.7,16.0 L767.7,66.0 Z" fill="#e6eef6"/>
<text x="619.9" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="619.9" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">BorrowingPolicy</text>
<line x1="470.0" y1="66.0" x2="769.7" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="482.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+mayRequest(int, int) boolean</text>
<rect x="330.0" y="215.0" width="220.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M332.0,251.0 L332.0,221.0 Q332.0,217.0 336.0,217.0 L544.0,217.0 Q548.0,217.0 548.0,221.0 L548.0,251.0 Z" fill="#e6eef6"/>
<text x="440.0" y="240.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReservationRules</text>
<rect x="590.0" y="215.0" width="265.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M592.0,251.0 L592.0,221.0 Q592.0,217.0 596.0,217.0 L849.0,217.0 Q853.0,217.0 853.0,221.0 L853.0,251.0 Z" fill="#e6eef6"/>
<text x="722.5" y="240.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">StaffReservationRules</text>
<rect x="10.0" y="305.0" width="270.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,341.0 L12.0,311.0 Q12.0,307.0 16.0,307.0 L274.0,307.0 Q278.0,307.0 278.0,311.0 L278.0,341.0 Z" fill="#e6eef6"/>
<text x="145.0" y="330.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ConfirmationFormatter</text>
<path d="M290.0,113.0 L370.0,113.0 L370.0,55.0 L470.0,55.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-fig51-open)"/>
<text x="420.0" y="41.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">asks eligibility</text>
<path d="M100.0,131.0 L100.0,305.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-fig51-open)"/>
<text x="118.0" y="223.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">formats</text>
<path d="M520.0,215.0 L520.0,101.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch05-fig51-tri)"/>
<path d="M700.0,215.0 L700.0,101.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch05-fig51-tri)"/>
<path d="M270.0,131.0 L270.0,250.0 L330.0,250.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch05-fig51-open)"/>
<text x="300.0" y="236.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">creates</text>
<path d="M230.0,131.0 L230.0,290.0 L726.0,290.0 L726.0,251.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch05-fig51-open)"/>
<text x="708.0" y="275.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="end" font-style="italic">creates</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 5.1

* **Solid arrows** are associations: the coordinator holds a `BorrowingPolicy` reference and a `ConfirmationFormatter`.
* **Dashed lines with a hollow triangle** are realisations: each rules class implements `BorrowingPolicy`.
* **Plain dashed arrows** are dependencies: the coordinator **creates the concrete policies itself**.
* The interface gives one type to ask, but **does not remove the dependence on the concrete classes**.
* When Chapter 6 moves creation outward, those two dashed arrows should **disappear**.

---

## Compare With a Smaller Alternative

* A single `BorrowingLimits` class with validated `maximumActive` and `maximumDays` could also be reasonable.
* The two policies differ only in **constants**. A compact conditional could even do in a short-lived demo.
* The interface earns its place by making the **decision contract explicit** and allowing policy behaviour to be examined separately.
* It adds **names and selection work**. Do not justify it by asserting two constants always require polymorphism.

---

## Do Not Invent Requirements

* Do not invent **sponsor approval, network checks or a rule engine** to make the abstraction look necessary.
* Those changes need their own requirements.
* The later changed-requirement exercise remains later work.
* This chapter uses only the small second rule stated above.

---

# 5.4 What Can a Caller Rely on?
### Behavioural contracts

---

## A Signature Leaves Questions

* Can the method **reject input with an exception**?
* Does it **mutate** anything?
* Is the result **stable for the same input**?
* What exactly does `true` **mean**?
* A signature describes parameter and result types and answers none of these.

---

## The `BorrowingPolicy` Contract (1 of 2)

| Aspect | Promise |
|---|---|
| Accepted input domain | Every pair of Java `int` values can be passed |
| Invalid numeric values | Negative count or nonpositive duration returns `false` |
| Decision | `true` exactly when the inputs satisfy that implementation's documented limits |

---

## The `BorrowingPolicy` Contract (2 of 2)

| Aspect | Promise |
|---|---|
| Side effects | Does not create reservations, change a counter or perform external I/O |
| Repeatability | Same inputs and fixed policy configuration give the same result |
| Scope of approval | Only count and duration; no assertion about availability or identity |

---

## Different Results, Same Contract

* Student and staff have **different documented limits**, so they can return different booleans for `(0, 14)`.
* A client of the common interface **must not assume every policy uses seven days**. That belongs to the student policy's own contract.
* The interface is meaningful because all implementations answer **the same kind of question** under common input and side-effect rules.
* "Do anything and return a boolean" would give **no basis for client reasoning**.

---

## Preconditions, Postconditions, Invariants

* A **precondition** states what must hold before an operation for its promised behaviour to apply.
* A **postcondition** states what the operation guarantees afterwards.
* An **invariant** is a property maintained by an object's valid observable states.
* They turn vague expectations into **reviewable statements**.
* `LoanPeriod`: construction **requires** non-null dates, start strictly before exclusive end; success **establishes** that invariant.

---

## A Decision: Negative Counts

* Chapter 1 noted that returning `false` for a negative count treats an impossible input like an ordinary refusal. This contract **settles it deliberately**.
* **Return `false`:** every existing client keeps working (they branch on the result), and the policy is defined for every pair of integers.
* **Throw:** signals a caller bug loudly, but **changes a result existing callers and checks rely on**, and adds a new exception to every client's contract.
* Here, **preserving behaviour decides**. In new code you control, the exception can be better. **Write the choice into the contract.**

---

## Postconditions and Order

* A successful reservation: **one new stored record** and a confirmation identifying it.
* An eligibility or overlap rejection: **stored records unchanged**.
* **Order matters:** count and duration are checked before the requested period is built and before overlap. Reordering can change **which failure a caller observes**.

---

## Exceptional Outcomes Are Part of the Contract

* The four-argument operation rejects blank identifiers with `IllegalArgumentException`, null dates with `NullPointerException`, and an unrepresentable end date through Java's date exception.
* The new overload rejects a **null category**.
* Refactoring is **not an opportunity to normalise those outcomes silently**. A more consistent error model is a separate API change.

---

## Check Observable Behaviour, Not Only Return Values

* An implementation returning the expected rejection string but **first inserting a reservation**: a string-only check misses it.
* One returning `false` for a negative count on the first call and **throwing on the second**: one isolated assertion misses it.
* Choose checks that match real promises: **state after rejection**, accepted and rejected **boundaries**, calls **through the common type**.

---

## Evidence, Not Proof

* **Direct policy checks** make boundaries easy to diagnose; **coordinator-level checks** verify the right policy is selected and applied.
* Passing examples are **not a proof** for every integer or call sequence.
* For tiny predicates, **reading the complete expression** complements boundary tests; the lack of fields and external calls supports the claim that they are **stateless**.

---

# 5.5 When a Subtype Breaks Its Promises
### LSP and unsafe inheritance

---

## Subtyping Promises Something to Clients

* LSP asks whether clients of a supertype can **keep relying on that type's behavioural promises** when given a subtype.
* Liskov and Wing's treatment covers **input requirements, output guarantees, invariants and history**.
* Matching Java signatures is necessary for many substitutions. It does **not** establish those behavioural properties.

---

## A Practical Review Asks

* Does the subtype **require more from the caller**?
* Does it **guarantee less afterwards**?
* Does it violate a **valid-state property**?
* Does it change state in ways **the supertype contract excluded**?
* Different implementations need not give identical results: their differences must stay **within what the common contract allows**.

---

## Staff Is Not a Subclass of Student

* Both implement the broader `BorrowingPolicy` contract.
* A client promised **the student's seven-day maximum** should not receive an object that approves fourteen days while still claiming to fulfil **that exact student contract**.
* The reservation classes do not need an inheritance hierarchy to illustrate LSP.

---

## A Separate Teaching Example: `IntHistory`

* Contract: **accept any `int`, append it once, preserve earlier entries in order.**
* A client is entitled to do this and expect `[5, -2]`:

```java
history.add(5);
history.add(-2);
```

---

## The Invalid Subtype

```java
static final class PositiveOnlyHistory extends IntHistory {
    @Override
    public void add(int value) {
        if (value <= 0)
            throw new IllegalArgumentException("Positive values only.");
        super.add(value);
    }
}
```

* It **compiles**. The original client now **fails on `-2`**.

---

## The Substitution Problem

<!--svg:ch05-lsp-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="A client of IntHistory adds 5 then -2 and expects [5, -2]. IntHistory satisfies it. PositiveOnlyHistory, which extends IntHistory, throws IllegalArgumentException on -2, so the subtype has strengthened the precondition." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch05-lsp-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-lsp-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-lsp-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-lsp-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch05-lsp-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="90.0" width="270.0" height="120.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="145.0" y="122.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">client(IntHistory h)</text>
<text x="145.0" y="144.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">h.add(5);</text>
<text x="145.0" y="167.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">h.add(-2);</text>
<text x="145.0" y="189.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">expects [5, -2]</text>
<rect x="360.0" y="25.0" width="220.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="470.0" y="66.8" font-size="20" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">IntHistory</text>
<rect x="640.0" y="25.0" width="220.0" height="70.0" rx="18" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="750.0" y="54.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">[5, -2]</text>
<text x="750.0" y="77.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">contract kept</text>
<rect x="360.0" y="205.0" width="220.0" height="70.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="470.0" y="235.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">PositiveOnlyHistory</text>
<text x="470.0" y="256.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">extends IntHistory</text>
<rect x="640.0" y="205.0" width="220.0" height="70.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="750.0" y="235.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">IllegalArgumentException</text>
<text x="750.0" y="255.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">on add(-2)</text>
<path d="M280.0,120.0 L320.0,120.0 L320.0,60.0 L360.0,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-lsp-arr)"/>
<path d="M280.0,180.0 L320.0,180.0 L320.0,240.0 L360.0,240.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-lsp-arr)"/>
<path d="M580.0,60.0 L640.0,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-lsp-arr)"/>
<path d="M580.0,240.0 L640.0,240.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch05-lsp-arr)"/>
</svg>
</div>
<!--/svg-->

---

## What Went Wrong

* The subtype **strengthened the input requirement**.
* Its restriction may suit a different domain object, yet it breaks **this supertype's contract**.
* Calling the exception "validation" does **not** repair the substitution.
* The key evidence: **a valid supertype client and the changed observable result**.

---

## Other Faulty Variants

* **Accept `-2` but ignore it:** avoids the exception, **weakens the append guarantee**.
* **Erase earlier entries whenever a new value arrives:** violates **preservation of history**.
* Three different failures, **one identical signature** `void add(int)`.

---

## Repair 1: Make the Type Relationship Honest

```java
static final class PositiveHistory {
    private final IntHistory entries = new IntHistory();

    public void addPositive(int value) {
        if (value <= 0)
            throw new IllegalArgumentException("Positive values only.");
        entries.add(value);
    }
    public List<Integer> values() { return entries.values(); }
}
```

---

## Why the Repair Works

* `PositiveHistory` openly **requires a positive value** and does **not** advertise itself as a substitute for the broader type.
* It may delegate storage to an internal `IntHistory`.
* **Composition alone is not magic:** if it still claimed an interface promising acceptance of every integer, the conflict would remain.
* It works because **the public contract and the advertised type relationship now agree**.

---

## Repair 2: Redefine the Abstraction

* Redefine the common abstraction so clients are told **which values an operation may reject**.
* That **changes the client contract** and may require client changes.
* It is not a behaviour-preserving fix for callers who already rely on accepting every integer.
* Decide whether **the broad contract or the restrictive type** is the intended abstraction before editing.

---

## Exceptions and History Need Context

* Do not memorise "throwing an exception violates LSP". An exception is compatible when **the supertype contract permits that outcome** for that input and state.
* Adding a method to a subtype is not automatically safe: a subtype-specific `eraseAll` can contradict a promise that previously stored entries remain present.
* In a review: **state the promise, demonstrate the call sequence, inspect the outcome**. "This violates LSP" is the **conclusion**, not a substitute.

---

## Run the Counterexample

```bash
javac --release 17 -d after/build/lsp after/examples/lsp/LspExample.java
java -cp after/build/lsp LspExample
```

```text
Base contract client passed.
Expected counterexample: Positive values only.
Separate positive-history contract passed.
```

* Exit status zero means the counterexample was **successfully observed**, not that the invalid subtype satisfies the contract.

---

# 5.6 Small Refactorings and the Checks That Guard Them
### Structural and behavioural steps kept apart

---

## Refactoring Keeps Observable Behaviour

* Refactoring changes **internal structure** while retaining **observable behaviour** (Fowler).
* Stage A follows that idea: introduce the formatter, move the existing expression, replace the call, run the existing checks.
* Avoid **renaming domain concepts, changing validation order and adding staff behaviour in the same step**.

---

## A Practical Sequence (1 of 2)

1. Run the Chapter 4 gate and **record the starting result**.
2. Add the concrete formatter with the **existing confirmation expression**.
3. Replace the private formatting call and **remove the now-unused private method**.

---

## A Practical Sequence (2 of 2)

4. Compile and rerun the **original regression and acceptance checks**.
5. Inspect the diff for **unrelated changes** and record what behaviour was preserved.
6. Begin **Stage B in a separate change**, with the staff rule and its new checks stated explicitly.

* Keep **one coordinator version** per source directory: several classes with the same name is a setup error, not evidence about the design.

---

## Read the Tests in Relation to the Change

* The **exact confirmation assertions** protect punctuation, identifiers and date formatting.
* **Overlap, adjacency and count checks** protect the reservation algorithm.
* **Snapshot checks** protect observation of stored state.
* These stay **unchanged** through Stage A and the compatibility part of Stage B.

---

## What Stage B Adds

* Staff's accepted **fifth** reservation and rejected **sixth**.
* Accepted **fourteen-day** duration and rejected **fifteen-day** duration.
* Cross-category: a staff booking **still blocks** an overlapping student request.
* The original overload **still rejects** a student's eight-day request.
* AQ-01 to AQ-05 are **not** part of this result: no availability API exists.

---

## Diagnose a Failing Check Before Editing It

* If the **old seven-day check** fails after introducing staff rules, inspect **policy selection** first. The old entry point was promised student behaviour. Updating the test would hide a compatibility defect.
* If an **exact confirmation check** fails because the formatter says "Reserved" instead of "Confirmed", the extraction changed a client-visible result. **Restore the text, or separate and approve a wording change.**
* A test is not sacred, but its replacement needs **a reason grounded in the intended contract**.

---

## Report the Evidence and Its Limits

* Distinguish the **baseline run**, **Stage A's unchanged checks** and **Stage B's additional checks**.
* Include the command, the revision or version, the observed output and the limitations.
* Do **not** claim independent review or hosted CI when only local checks ran.
* A clean local result **supports review**; it does not replace it or establish production readiness.

---

## Stage B Code: The Overload

```java
public String reserve(String borrowerId, String itemId, LocalDate start,
                      int requestedDays, BorrowerCategory category) {
    Objects.requireNonNull(category, "category");
    // ... same validation and counting as before ...
    if (!policyFor(category).mayRequest(activeCount, requestedDays)) {
        return "Rejected: borrower limit or duration.";
    }
    // ... same overlap check, store, then:
    return formatter.format(reservation);
}
```

---

## The Demonstration

```java
System.out.println(coordinator.reserve("S1", "CAM1", day, 14,
        BorrowerCategory.STAFF));
System.out.println(coordinator.reserve("B1", "MIC1", day, 14));
System.out.println(coordinator.reserve("B1", "CAM1", day.plusDays(1), 1));
System.out.println(coordinator.reserve("B1", "CAM1", day.plusDays(14), 1));
```

* A staff fourteen-day booking succeeds; the same duration through the **old** entry point is rejected; an overlap with the staff booking is rejected; a request from the staff booking's end is accepted.

---

## Do the New Checks Detect Faults? (1 of 4)

| Fault introduced into a copy | Result |
|---|---|
| Staff count limit `< 5` to `<= 5` | Caught: `staff sixth rejected` |
| Staff duration `<= 14` to `< 14` | Caught: `staff upper accepted boundaries` |
| Staff duration `<= 14` to `<= 15` | Caught: `staff fifteen days rejected` |
| Staff negative-count guard removed | Caught: `negative count returns false` |

---

## Do the New Checks Detect Faults? (2 of 4)

| Fault introduced into a copy | Result |
|---|---|
| Student count limit `< 3` to `< 5` | Caught: `fourth rejected` |
| Student duration `<= 7` to `<= 14` | Caught: `eight-day duration rejected` |
| Selector arms swapped | Caught: `fourth rejected` |
| Old overload delegates with `STAFF` | Caught: `fourth rejected` |

---

## Do the New Checks Detect Faults? (3 of 4)

| Fault introduced into a copy | Result |
|---|---|
| Confirmation text changed to `Reserved:` | Caught: `exact first confirmation` |
| Confirmation drops the end date | Caught: `exact first confirmation` |
| Storing the reservation skipped | Caught: `one success stored` |
| Count restricted to staff requests only | Caught: `fourth rejected` |

---

## Do the New Checks Detect Faults? (4 of 4)

| Fault introduced into a copy | Result |
|---|---|
| Overlap check ignores the item | Caught: `different item and seven-day limit allowed` |
| Explicit `Objects.requireNonNull(category, ...)` removed | **Not caught**, and not a gap |

* Thirteen of fourteen faults caught.
* The survivor: `switch (category)` on `null` still throws `NullPointerException` before any state changes. Only the **order against identifier validation** differs, which the contract does not specify.
* A surviving fault can mean the fault is **behaviourally equivalent**, not that the checks are weak.

---

# 5.7 When Is an Abstraction Too Early?
### Avoiding premature abstraction

---

## A Boundary Costs Something

* A new interface needs a **name, a contract, implementations and a place where one is selected**.
* An abstraction that hides a real variation can **reduce future edits**.
* One that merely mirrors a single class can **add navigation without changing which decisions are coupled**.

---

## The Cost of Each Decision (1 of 2)

| Decision | Benefit | Cost or remaining limitation |
|---|---|---|
| Extract a concrete formatter | Independent presentation changes get a home | Another object and file; no configurable presentation yet |
| Use a small policy interface | Names the count/duration contract shared by two rules | Extra types and selection; numeric parameterisation is also possible |
| Keep a selector in the coordinator | Intermediate stage is easy to inspect | New categories still require a coordinator edit |

---

## The Cost of Each Decision (2 of 2)

| Decision | Benefit | Cost or remaining limitation |
|---|---|---|
| Retain direct construction | Keeps focus on SRP, OCP and contracts | Dependency assembly stays coupled until Chapter 6 |
| Avoid coordinator inheritance | Prevents duplicating or overriding the workflow | Variation must be expressed through explicit collaborators |

* A reasonable review can conclude that **a cost outweighs its benefit** for a particular project. Principles make the judgement **explainable**; they do not remove it.

---

## Warning Signs Without a Smell Catalogue

* **Repeated edits** to the same policy conditional.
* **Message changes breaking reservation logic.**
* **Subclasses that disable inherited operations.**
* Investigate the change history or **construct a client counterexample** before prescribing a repair.
* A long method alone does not tell you **which boundary is needed**.

---

## Do Not Create `IReservation` Because a Tool Said "SOLID"

* No `IReservation`, `ILoanPeriod`, abstract coordinator factory or generic notification bus **simply because an automated suggestion calls them SOLID**.
* Ask: **what concrete variation does each support, and what client contract does it improve?**
* A missing answer is a reason to **postpone** that abstraction.
* SRP, OCP, LSP, ISP and DIP are **not interchangeable names for adding interfaces**.

---

# 5.8 Reviewing a “Make This SOLID” Suggestion with AI
### Verdicts with concrete reasons

---

## Ground Rules for the Activity (1 of 2)

| | For this activity |
|---|---|
| Your goal | Judge a "make this SOLID" proposal against concrete requirements, contracts and costs |
| You start with | The Chapter 4 source, the staff-rule table in 5.1 and the policy contract in 5.4 |
| What is in bounds | Review the proposal; do not apply it wholesale |

---

## Ground Rules for the Activity (2 of 2)

| | For this activity |
|---|---|
| How to check | Compilation (is `ReservationRules` `final`?), the exact-output checks, the rejection and state checks |
| How to decide | A verdict with a concrete defect or cost for each proposal, then the smallest defensible two-stage change |
| No AI account? | The ready-made example is enough |

---

## The Ready-Made Example (1 of 2)

**Author-written fictional AI output**, not an actual model transcript.

> Create an interface for every class, including immutable reservation and period values. Add a coordinator factory and an abstract base coordinator. Replace all rejection strings with exceptions because exceptions are cleaner.

---

## The Ready-Made Example (2 of 2)

> Make `StaffReservationRules` extend `ReservationRules` and override the seven-day limit. Remove all category conditionals so no existing file ever changes. While extracting the formatter, shorten the confirmation to "Reserved". The green build proves the design follows SOLID.

* Identify one proposal that **would not compile**, one that **changes existing behaviour**, one whose **benefit has not been demonstrated**.

---

## Model Review (1 of 3)

| Proposed change | Verdict | Concrete reason |
|---|---|---|
| An interface for every class | Not justified as stated | No second role or client need for immutable values; adds navigation |
| Coordinator factory and abstract base | Defer | Two rules do not require a factory hierarchy |
| Replace rejection strings with exceptions | Separate feature/API proposal | Existing callers and acceptance examples observe the current results |

---

## Model Review (2 of 3)

| Proposed change | Verdict | Concrete reason |
|---|---|---|
| Staff rules extend student rules | Reject | `ReservationRules` is `final`; and staff approval is incompatible with the exact student predicate |
| Remove all conditionals so no file ever changes | Reject the promise | An implementation must still be selected somewhere |

---

## Model Review (3 of 3)

| Proposed change | Verdict | Concrete reason |
|---|---|---|
| Shorten the confirmation to "Reserved" | Reject during Stage A | The exact output changes: no longer the promised extraction |
| Green build proves SOLID | Reject | Checks examine limited behaviour; responsibility claims need reasoning |

* **Minimal corrected plan:** baseline; extract the unchanged formatter; verify Stage A; state the staff rule; small policy contract and explicit category path; preserve the old default; run old and new checks; inspect remaining direct dependencies.

---

## A Good AI Review Record

* The **candidate claim**.
* The **accepted, rejected or deferred** verdict.
* The **reason** and the **evidence**: the `final` declaration, exact confirmation assertions, rejection checks, the selector's source, the source of the category argument.
* Do not reject the whole output merely because it contains many classes. **Identify which boundary lacks a purpose or which behaviour changes.**

---

# 5.9 Design Habits That Look Principled
### Ten to avoid

---

## Mistakes 1 to 3

| Mistake | Counterexample or consequence | Better reasoning |
|---|---|---|
| SRP means one method per class | A one-method service can still mix policy and presentation | Identify independent change pressures |
| OCP forbids editing existing code | A new category still needs an explicit selection decision | State the protected axis and the remaining edit boundary |
| Same signature means safe subtype | `PositiveOnlyHistory.add(-2)` rejects valid base input | Evaluate the behavioural contract |

---

## Mistakes 4 to 6

| Mistake | Counterexample or consequence | Better reasoning |
|---|---|---|
| Any different policy result violates LSP | Student and staff intentionally have different limits | Compare with the shared contract |
| Better wording is part of a refactoring | "Reserved" breaks the preserved result | Separate the presentation feature from extraction |
| A passed LSP demo validates the subtype | The harness may have successfully detected a violation | State what the demonstration observed |

---

## Mistakes 7 and 8

| Mistake | Counterexample or consequence | Better reasoning |
|---|---|---|
| A category parameter verifies authority | A caller can supply `STAFF` without proving identity | Label the trusted-example boundary |
| More interfaces mean better design | Unused variations add navigation and decisions | Relate every boundary to a concrete need |

---

## Mistakes 9 and 10

| Mistake | Counterexample or consequence | Better reasoning |
|---|---|---|
| Switch on every analyser rule | Dozens of low-value findings hide the one that matters | Choose a small rule set for a stated purpose and record why |
| Read an unchanged finding as a failed refactoring | A tool measures one thing, such as branching | Say what the tool measures and what the change targeted |

---

# 5.10 Try It Yourself
### A protected design change

---

## What You Start With, and the Demonstration

* **You start with:** Chapter 4's source and checks, the staff-rule table and the companion listings. Java 17. Keep the **LSP micro-example separate** from the application.
* **Steps 1 to 7:** the book's project. **Step 8:** your team's project.
* **Demonstration:** trace the existing operation and identify **three independent change pressures**. Run one valid base-type client against both `IntHistory` and the invalid subtype and explain the difference.
* **Guided practice:** perform Stage A, reviewing the formatter's input, output and lack of reservation authority.

---

## Independent Work: Steps 1 to 3

1. A **responsibility table** for the coordinator, rules, period and proposed formatter; a concern you deliberately leave unchanged. Run `javac -Xlint:all`, the manual smell review and **PMD**, and place each finding in one of three groups.
2. Record a **passing baseline**, extract the formatter, rerun the original checks **without altering their expected behaviour**.
3. Add the explicit **staff variation** while preserving the student overload. Document the policy contract and the source of the category argument.

---

## Independent Work: Steps 4 to 6

4. Add or use the **boundary and cross-category checks**. Explain what each group establishes.
5. Run the separate **LSP example**. Identify the violated promise and compare the composition-based repair with changing the base contract.
6. **Review the complete diff** with another person where available. Retain actual findings and corrections; label solo review honestly.

---

## Independent Work: Steps 7 and 8

7. Write a short **rationale** connecting each new class or interface to a change pressure and naming the **remaining dependency-selection limitation**. Say what PMD reported after Stage A and after Stage B, and why.
8. On your team's project: the same kind of responsibility table for **one class** in your starter codebase; run the compiler, manual and PMD checks on it; name **one change pressure** you can point to in its backlog or history.

---

## Expected Output and Completion

* **Output:** a smell and responsibility diagnosis with the tool findings compared; the step 8 table; before, refactored and extended versions; check results; a **contract table**; a subtype counterexample explanation; a concise **design rationale**.
* **Complete when:** Stage A preserves behaviour; Stage B implements the staff boundaries and keeps student compatibility; **rejections leave records unchanged**; you can explain why the policy interface helps and **why the selector still changes for another category**.
* The rationale must distinguish a **rule invented for this book from an approved institutional rule**.

---

## If You Want More

* In a scratch copy of Stage B, **extract two private methods** from `reserve` (one counts a borrower's reservations, one tests whether an item is unavailable). Run the gate, rerun PMD and **explain what changed and what did not**.
* Then implement the two numeric policies using a **validated limits object** in a separate experiment. Compare files changed, clarity and likely future variation.
* **Do not merge both alternative designs** into the running application merely to demonstrate them.

---

## Model Responsibility Diagnosis (1 of 2)

| Element | Present responsibility | Decision in this chapter |
|---|---|---|
| `ReservationCoordinator` | Sequence validation, eligibility, conflict detection and storage | Preserve sequencing; delegate formatting and policy evaluation |
| `ReservationRules` | Student count/duration decision | Preserve predicate; implement the shared policy contract |
| `LoanPeriod` | Valid interval and overlap semantics | Leave unchanged |

---

## Model Responsibility Diagnosis (2 of 2)

| Element | Present responsibility | Decision in this chapter |
|---|---|---|
| `Reservation` | Immutable accepted-record details | Leave unchanged |
| Confirmation expression | Render an accepted record as text | Extract a concrete formatter |
| Staff eligibility | New count/duration variation | Add a separate policy implementation |

* The original coordinator **already delegated numeric rules**. Claiming this chapter first extracts them would misdescribe the starting point.

---

## Model Manual Smell Review (1 of 2)

| Smell | Where it appears in `reserve` | Act now? |
|---|---|---|
| More than one reason to change | One method validates, counts, applies eligibility, searches for a conflict, creates and stores the record, and produces wording | Yes for wording (A) and eligibility (B); no for storage |
| Hidden construction | `private final ReservationRules rules = new ReservationRules();` | Only as far as Stage B needs; full choice is Chapter 6 |

---

## Model Manual Smell Review (2 of 2)

| Smell | Where it appears in `reserve` | Act now? |
|---|---|---|
| Repeated or similar logic | Two loops differ only in the test; rejections are two plain strings | No: two short loops are clearer than a new abstraction |
| Primitives standing for concepts | Identifiers and days are strings and an integer; rejection reasons are free text | No: record it as a limitation |

* `-Xlint:all` showed none of these. Reading alone did not settle whether the repeated loops justify an abstraction: **a correct answer may reasonably leave them**.

---

## Model PMD Comparison

| Source | Finding | Group |
|---|---|---|
| PMD `CyclomaticComplexity` | `reserve` has complexity 12 (threshold 10) | **Useful** |
| PMD `DataClass` | `Reservation` is a suspected data class | **Low-value here** |
| Manual reading | `new ReservationRules()` inside the coordinator | **Missed by the tool** |
| Manual reading | One string for two different reasons | **Missed by the tool** |
| Manual reading | Two similar loops | Not reported at default thresholds; leave them |

---

## Rule Sets Compared on the Same Five Files

| PMD rule set | Findings on `before` | What they were |
|---|---|---|
| Lab set (eight design rules) | 2 | The two above |
| `rulesets/java/quickstart.xml` | 5 | All `NoPackage` |
| `category/java/codestyle.xml` | 34 | `MethodArgumentCouldBeFinal`, `LocalVariableCouldBeFinal`, `NoPackage`, `OnlyOneReturn` and similar |
| `category/java/bestpractices.xml` | 4 | `SystemPrintln` in the demonstration class |

* This is why the lab uses **a small set**.

---

## Suggested Evidence

| Evidence | What to record |
|---|---|
| Starting point | Actual version and passing original gate |
| Stage A | Relevant diff; original checks with unchanged expectations |
| Stage B | New rule table; policy contract; compatibility and staff-boundary results |
| LSP example | Valid base call sequence; subtype outcome; precise violated promise |
| Review | Actual reviewer or labelled self-review; findings and corrections |

* Do **not** invent a peer review. A supplied model rationale is not evidence that someone inspected your work.

---

## Limits Object vs. Separate Classes

| Future change | Separate policy classes | Configured numeric limits |
|---|---|---|
| Change staff days from 14 | Edit the staff predicate | Edit the staff configuration |
| Add a third pair of simple limits | Add another policy | Supply another configuration |
| A qualitatively different eligibility rule | A new implementation can express it | May need a broader design |

* No approach wins merely by having **fewer files**. Constructor validation and request-input behaviour are **different contracts**.

---

# 5.11 Questions to Think with
### Concept and diagnosis

---

## Concept Questions

1. Why is counting methods an unreliable way to apply SRP? Give one example from the running project.
2. Against which variation is the policy design relatively protected, and which selection code remains open to change?
3. How can two implementations return different booleans and still satisfy the same policy interface contract?
4. Why is extracting the formatter a refactoring while introducing staff limits is a feature change?

---

## Diagnosis Questions

5. A policy implements the right Java signature but throws for a negative active count and increments an internal request counter on every call. Compare it with this chapter's policy contract. What evidence would expose each problem?
6. A developer subclasses a history that promises to append every integer. The subclass silently ignores negative numbers rather than throwing. Explain why avoiding an exception does not make the subtype safe, and propose an honest repair.

---

## Guidance: Questions 1 and 2

1. `LoanPeriod` has construction, accessors and overlap supporting **one** interval abstraction. A single `process` method could contain borrowing rules, persistence and formatting. **Count does not identify independent change pressures.**
2. The algorithm **delegates count and duration decisions**, so changing staff limits need not alter overlap or storage. The **selector and directly constructed policy fields** remain in the coordinator: adding a category means updating that selection.

---

## Guidance: Questions 3 and 4

3. The common contract defines the **kind of question**, valid input handling, determinism and side-effect limits. It allows **implementation-specific documented limits**. A client assuming seven days for every implementation has assumed more than the interface promises.
4. Stage A changes **where** a fixed result is produced while preserving outputs, state effects and failure behaviour. Stage B introduces **successful requests that were not available before**.

---

## Guidance: Questions 5 and 6

5. **Throwing** changes an observable outcome and can break a client that branches on the boolean: pass `(-1, 1)` through a `BorrowingPolicy` reference and assert `false`. The **counter** conflicts with the no-counter-change contract; equal results alone do **not** prove no counter was incremented, so inspect the implementation.
6. After `add(5); add(-2);` a result of `[5]` **weakens the append postcondition** though nothing was thrown. Compare the **complete resulting sequence**. Retain broad acceptance, or expose a **separate narrower type** whose contract restricts input.

---

# 5.12 A Different Setting
### The transfer challenge

---

## Transfer Challenge

A coursework feedback tool accepts a score and produces feedback text. A new requirement adds **a second grading policy and a different feedback layout**. Its current class validates input, selects a grade and formats the message.

* Write the **change pressures**, one proposed **responsibility boundary** and a **contract** for the grading decision.
* Give a small input/output table for **two invented policies**.
* State what remains **stable** and where a policy is **selected**.
* Construct a **subtype counterexample** and explain the repair.
* Keep the rules illustrative, **not university assessment policy**.

---

## Transfer Guidance: Policies

* Pressures: the **score input domain**, the **policy mapping a valid score to a grade**, and **presentation**.
* Illustrative `GradePolicy.grade(int score)`: scores 0 to 100 return `PASS` or `REVIEW`; others raise `IllegalArgumentException`. Deterministic, no I/O.

| Score | Policy A: pass at 50 | Policy B: pass at 60 |
|---|---|---|
| 49 | REVIEW | REVIEW |
| 50 | PASS | REVIEW |
| 60 | PASS | PASS |
| -1 or 101 | exception | exception |

---

## Transfer Guidance: Counterexample and Repair

* A client must not assume every policy passes 50.
* The formatter receives the score and computed grade and **does not recompute the grade**.
* **Counterexample:** a subtype that throws for a **valid score of zero** ("not submitted"), or **returns null** though a grade is promised.
* **Repair:** keep zero valid and model submission status separately, or expose a narrower operation that does not claim to be a substitute.
* Protect the existing message with unchanged examples; add boundary examples around both thresholds.

---

# What to Take Away, and What Comes Next
### What to carry forward

---

## Summary

* Responsibility boundaries are most useful when they respond to **distinct change pressures**.
* **Extension points** should protect a named variation.
* **Subtyping** must preserve the promises clients of the broader type can rely on.
* **Small, separately verified steps** make those design claims easier to assess.

---

## Where the Project Stands

* A concrete **confirmation formatter**.
* **Student and staff** count-and-duration policies, with the **original student entry point preserved**.
* The subtype example **remains separate**; the availability enquiry **remains planned**.

---

## Next: Chapter 6

* **Client-specific interfaces.**
* **Dependency direction.**
* **Manual object assembly**: moving the two "creates" arrows out of the coordinator.

---

## Sources and Further Reading

1. **Martin:** *The Single Responsibility Principle* and *The Open Closed Principle*, 2014.
2. **Oracle:** *Java Language Specification, Java SE 17, Chapter 9: Interfaces.*
3. **Liskov and Wing:** *A Behavioral Notion of Subtyping*, 1994.
4. **Fowler:** *Definition of Refactoring*, 2004; *Refactoring*, 2nd ed., 2018.
5. **Martin:** *Agile Software Development*, 2002.
6. **PMD:** installation and Java design rules, 7.28.0.

* Full references and links are in the chapter text.
