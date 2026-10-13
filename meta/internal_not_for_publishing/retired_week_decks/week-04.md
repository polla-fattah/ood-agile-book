---
title: "Week 4: SOLID I: Single Responsibility, Extension & Substitutability"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 40
type: slides
layout: page
---

# Week 4: SOLID I: Single Responsibility, Extension & Substitutability
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## 3-Hour Lecture Roadmap

* **Part 1: Change Pressure, Smells & Static Analysis (0:00 - 0:35)**
  * The Equipment Officer's dilemma, Fowler smell taxonomy, compiler vs human vs PMD 7.28.0 analysis.
* **Part 2: Single Responsibility & Protected Refactoring (0:35 - 1:10)**
  * SRP defined as actors/reasons to change, extracting `ConfirmationFormatter`, Stage A regression verification.
* **Part 3: Open-Closed Principle & Polymorphic Policy (1:10 - 1:40)**
  * Axis of variation, `BorrowingPolicy` interface, preserving student entry points, honest selector design.
* **BREAK (1:40 - 1:55)**
* **Part 4: Behavioural Contracts & Liskov Substitutability (1:55 - 2:25)**
  * Preconditions/postconditions/invariants, executable `IntHistory` counterexample, composition-based repair.
* **Part 5: Deliberate Faults & Bounding AI Refactoring (2:25 - 2:45)**
  * Catching silent contract drifts, critiquing the "Make this SOLID" prompt hallucination.
* **Part 6: Workshop Deliverables, Team Lab & Wrap-Up (2:45 - 3:00)**
  * The 8-step lab workflow, comparing PMD findings on team code, preview of Week 5 (ISP & DIP).

---

## Pedagogical Alignment & Module Context

* **Module Learning Outcomes:**
  * **LO1:** Critically evaluate and apply advanced object-oriented programming concepts (encapsulation, polymorphism, design principles).
  * **LO4:** Refactor and improve existing codebases using industry-standard design patterns, metrics, and static analysis.
* **Foundational Literature & Engineering Canon:**
  * Robert C. Martin (2002, 2014): *Agile Software Development: Principles, Patterns, and Practices* (SRP, OCP, LSP).
  * Martin Fowler (2018): *Refactoring: Improving the Design of Existing Code* (Code Smells).
  * Barbara H. Liskov & Jeannette M. Wing (1994): *A Behavioral Notion of Subtyping* (ACM TOPLAS).
* **Core Philosophy:**
  * Principles are reasoning tools about change and contracts, not excuses to add endless interfaces or factory hierarchies.

---

# Part 1: Change Pressure, Code Smells & Static Analysis

---

## The Equipment Officer's Dual Dilemma

* **Scenario:**
  * Two competing stakeholder requests arrive on Monday morning for the Campus Lending System:
    1. **Presentation:** The Equipment Officer requests a redesigned confirmation layout (shorter wording, different timestamp format).
    2. **Policy:** Academic management requests an experimental borrowing tier for faculty and staff (up to 4 items for 14 days, versus student limits of 2 items for 7 days).
* **The Naive Developer's Instinct:**
  * Modify `ReservationCoordinator.java` directly: add `if (isStaff)` checks and tweak the string builder.
* **The Dangerous AI Instinct:**
  * "Make the code SOLID": Generates 14 interfaces, changes rejection strings to exceptions, and breaks existing tests.
* **The Engineering Question:**
  * How do we decouple presentation and policy without breaking existing callers or over-engineering the architecture?

---

## Mapping Change Pressures to System Components

* Before touching any code, catalog where change forces land:

| Change Pressure | Knowledge Domain | Current Location | Architectural Action |
|---|---|---|---|
| Redesign confirmation layout | Presentation formatting | `ReservationCoordinator` private method | Extract collaborator (SRP) |
| Add staff borrowing limits | Eligibility business rules | `ReservationRules` / coordinator | Polymorphic strategy (OCP) |
| Change interval overlap logic | Interval mathematics | `LoanPeriod` | Already isolated (Stable) |
| Persist bookings to PostgreSQL | Storage & lifecycle | In-memory `ArrayList` | Defer to Chapter 10 |
| Authenticate borrower role | Security & identity | Fixture parameter | Label trusted boundary |

* **Key Takeaway:** A change pressure table prevents premature abstraction. We only build extension points where real variations exist today.

---

## Fowler's Code Smell Taxonomy (1999, 2018)

* A "code smell" is a surface indication that usually corresponds to a deeper design flaw.

```
       [ Surface Code Smell ]
                 │
                 ▼ (Diagnostic Question)
    "Why will this code be hard to modify tomorrow?"
                 │
  ┌──────────────┼──────────────┬──────────────┐
  ▼              ▼              ▼              ▼
Divergent     Shotgun       Primitive       Feature
 Change       Surgery       Obsession        Envy
(1 class,    (1 change,    (Strings/ints   (Method talks
 2 actors)   many files)   stand for types) to another obj)
```

* In our starting `ReservationCoordinator`:
  * **Divergent Change:** Modified when wording changes AND when loan rules change.
  * **Primitive Obsession:** Identifiers and errors represented as raw `String` primitives.
  * **Hidden Construction:** Directly calls `new ReservationRules()` inside fields/methods.

---

## Triangulating Design Evidence

* We evaluate software quality using three distinct lenses:

```
                  ┌────────────────────────┐
                  │ 1. Compiler Diagnostics│
                  │   (javac -Xlint:all)   │
                  └───────────┬────────────┘
                              │ Language correctness
                              ▼
┌────────────────────────┐         ┌────────────────────────┐
│ 2. Manual Human Review │ ◄─────► │ 3. Automated Linter    │
│  (Smells & Pressures)  │         │   (PMD 7.28.0 CLI)     │
└────────────────────────┘         └────────────────────────┘
  Identifies architectural           Catches structural
  responsibilities & actors          threshold violations
```

* Each tool has distinct blind spots:
  * The compiler checks type safety, not responsibility boundaries.
  * PMD checks complexity metrics, not business semantics.
  * Human code review connects code structures to organizational actors.

---

## Lens 1: Compiler Diagnostics (`javac -Xlint`)

* Let us run the Java compiler with all optional lints enabled:

```bash
javac --release 17 -Xlint:all -d build/lint \
  src/main/java/*.java src/test/java/*.java
```

* **Observed Output on Chapter 4 Starter:**
  * *Clean build: zero warnings generated.*
* **What this result proves:**
  * No raw types, no unhandled unchecked conversions, no deprecated API usage, no unreachable code.
* **What this result does NOT prove:**
  * It does not tell you that `ReservationCoordinator` mixes presentation, validation, conflict search, and record storage.
  * Syntactic cleanliness != Architectural soundness.

---

## Lens 2: Manual Smell Audit of Starting Code

* Read `ReservationCoordinator.reserve(...)` line by line:

```java
// Line 10: Identifier and date null-checks (Validation)
if (borrowerId == null || borrowerId.isBlank() ...) throw ...;
// Line 16: Loop counting active loans (Policy input retrieval)
for (Reservation existing : reservations) { if (...) activeCount++; }
// Line 21: Eligibility check (Policy execution)
if (!rules.mayRequest(activeCount, requestedDays)) return "Rejected: ...";
// Line 25: Period construction and overlap loop (Conflict detection)
LoanPeriod requested = new LoanPeriod(start, start.plusDays(requestedDays));
for (Reservation existing : reservations) { if (...) return "Rejected: ..."; }
// Line 34: Storage and ID allocation (Record lifecycle)
reservations.add(new Reservation(...));
// Line 36: Text formatting (Presentation)
return confirmationFor(reservation);
```

* **Human Diagnosis:** Six distinct concerns packed into a single 38-line method!

---

## Lens 3: Automated Static Analysis with PMD 7.28.0

* **PMD** parses Java source code into an Abstract Syntax Tree (AST) and checks for pattern violations.
* For SE506, we define a targeted ruleset in `config/pmd-smells.xml`:
  * 8 rules from PMD's `category/java/design.xml` with default thresholds:
    * `CyclomaticComplexity` (threshold: 10)
    * `CognitiveComplexity` (threshold: 15)
    * `NPathComplexity` (threshold: 200)
    * `GodClass`
    * `DataClass`
    * `TooManyMethods` (threshold: 10)
    * `ExcessiveParameterList` (threshold: 10)
    * `ExcessiveImports` (threshold: 30)

---

## Executing the PMD Smell Gate

* The automated lab script `scripts/pmd.sh`:

```bash
export PMD_HOME=/opt/pmd-bin-7.28.0
bash scripts/check.sh   # Compile classes first for type resolution
bash scripts/pmd.sh
```

* **Raw Console Output on Chapter 4 Starter:**
```text
src/main/java/Reservation.java:3: DataClass:
  The class 'Reservation' is suspected to be a Data Class
  (WOC=0.000%, NOPA=0, NOAM=4, WMC=9)

src/main/java/ReservationCoordinator.java:10: CyclomaticComplexity:
  The method 'reserve(String, String, LocalDate, int)' 
  has a cyclomatic complexity of 12.

[INFO] Found 2 violations.
```

---

## Triangulating PMD Findings: Value vs Context

* Not all linter findings require remediation:

* **Finding 1: `CyclomaticComplexity: 12` in Coordinator**
  * **Assessment:** Highly useful!
  * **Why:** 12 independent linear paths through `reserve(...)` because validation, eligibility, overlap checking, and formatting are tightly coupled.
* **Finding 2: `DataClass` on `Reservation`**
  * **Assessment:** Low-value / False positive in this context.
  * **Why:** `Reservation` is intentionally an immutable domain value record. It holds data and provides accessor methods.
* **What PMD Missed Entirely:**
  * PMD cannot know that `ReservationCoordinator` creates `ReservationRules` with `new`.
  * PMD cannot know that confirmation wording changes on the whim of the equipment officer while rules change on academic policy.

---

## Interactive Prediction: Complexity After Refactoring

* **Question for the class:**
  * Suppose in Stage A we extract confirmation formatting out of `ReservationCoordinator` into a new `ConfirmationFormatter` class.
  * When we re-run PMD, what will happen to the Cyclomatic Complexity score (currently 12) of `reserve(...)`?

* **Options:**
  * (A) It will drop from 12 to 8.
  * (B) It will drop from 12 to 11.
  * (C) It will stay at exactly 12.

* *Pause 60 seconds. Think through what branches exist in formatting vs sequencing.*

---

## Prediction Answer & Explanation

* **Correct Answer:** **(C) It will stay at exactly 12!**
* **The Mathematical Explanation:**
  * Cyclomatic Complexity measures decision points (`if`, `for`, `&&`, `||`, `case`, `? :`).
  * The private `confirmationFor(...)` method had **zero** decision points; it was a straight-line string concatenation (`+`).
  * Moving straight-line code to another class removes lines of code, but does **not** reduce branch count!
* **Pedagogical Takeaway:**
  * Refactoring for SRP aligns code with reasons to change. It is not a mechanical game of driving arbitrary complexity metrics to zero.

---

# Part 2: Single Responsibility & Protected Refactoring

---

## Defining the Single Responsibility Principle (SRP)

> "A module should have one, and only one, reason to change."  
> - Robert C. Martin (Uncle Bob), 2014

```
                  ┌──────────────────────────────┐
                  │          ACTOR / ROLE        │
                  │ (Source of Change Pressure)  │
                  └──────────────┬───────────────┘
                                 │ Demands new behavior
                                 ▼
                  ┌──────────────────────────────┐
                  │       RESPONSIBILITY         │
                  │   (Cohesive Cluster of Logic)│
                  └──────────────┬───────────────┘
                                 │ Expressed in
                                 ▼
                  ┌──────────────────────────────┐
                  │        FOCUSED CLASS         │
                  │ (Single Reason to Change)    │
                  └──────────────────────────────┘
```

* **Common Misconception:** "SRP means a class should only have one method."
* **Reality:** A class may have 10 methods and perfectly respect SRP if they all serve the same actor and business purpose (e.g., `LoanPeriod`).

---

## Stage A Objective: Isolate Presentation

* **Goal:** Extract confirmation message generation out of `ReservationCoordinator` into `ConfirmationFormatter`.
* **Strict Constraint:** This is a **pure refactoring** (behaviour-preserving).
  * Exact return strings must remain character-for-character identical.
  * Exception throwing order and types must remain identical.
  * Coordinator reservation snapshots must remain identical.
* **Non-Goals for Stage A:**
  * Do NOT add HTML or JSON formatting.
  * Do NOT add email or SMS dispatching.
  * Do NOT touch eligibility rules or introduce staff policies yet.

---

## The Extracted Collaborator: `ConfirmationFormatter`

* Listing: `ConfirmationFormatter.java`

```java
import java.util.Objects;

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

* **Key Architectural Properties:**
  * **Input:** Takes a single immutable `Reservation` record.
  * **Output:** Returns a formatted `String`.
  * **Zero Authority:** Cannot alter reservations, approve requests, or access coordinator storage.

---

## Guarding Against Responsibility Leakage

* What must `ConfirmationFormatter` NOT do?

```
BAD: Leaking Policy into Formatter
┌──────────────────────────────────────────────┐
│ class ConfirmationFormatter {                │
│     public String format(Reservation r) {    │
│         if (r.period().durationDays() > 7) { │ <── POLICY LEAK!
│             return "Warning: Long loan";     │
│         }                                    │
│         ...                                  │
│     }                                        │
│ }                                            │
└──────────────────────────────────────────────┘
```

* **Why this is toxic:**
  * If the loan duration policy changes from 7 to 14 days, the developer must remember to update both `ReservationRules` and `ConfirmationFormatter`.
  * The presentation collaborator must be a pure, passive renderer of accepted state.

---

## The Refactored Coordinator (Stage A)

* `ReservationCoordinator.java` changes:

```java
public final class ReservationCoordinator {
    private final List<Reservation> reservations = new ArrayList<>();
    private final ReservationRules rules = new ReservationRules();
    // New collaborator instance
    private final ConfirmationFormatter formatter = new ConfirmationFormatter();

    public String reserve(String borrowerId, String itemId,
                          LocalDate start, int requestedDays) {
        // ... (validation, count, eligibility, overlap checks identical) ...

        Reservation reservation = new Reservation(
                "R" + (reservations.size() + 1), borrowerId, itemId, requested);
        reservations.add(reservation);
        // Delegated presentation call
        return formatter.format(reservation);
    }
}
```

---

## Execution Order & State Invariants

* Notice the exact sequence at the end of `reserve(...)`:

```java
reservations.add(reservation);
return formatter.format(reservation);
```

* **Why add to the list before formatting?**
  * The postcondition of a successful reservation is that the reservation is recorded in the system.
  * The formatter formats an *accepted* booking.
  * If formatting failed with an unexpected exception, the reservation would already be stored.
  * Because `ConfirmationFormatter.format(...)` is deterministic and in-memory, no partial-failure rollback is needed here.
  * If formatting ever involves network I/O, failure semantics will require explicit design.

---

## Verifying Stage A: Regression Safety Gate

* Run the full suite of regression and acceptance checks:

```bash
bash refactored/scripts/check.sh
```

```text
java -version
openjdk version "17.0.12" 2024-07-16 LTS
AC-01 passed
AC-02 passed
AC-03 passed
AC-04 passed
AC-05 passed
All 5 acceptance examples passed.
BUILD AND CHECKS PASSED
```

* **Evidence Check:**
  * All 34 Chapter 2 regression checks passed.
  * All 5 Chapter 3 acceptance example groups passed.
  * Zero test modifications were required!

---

## Stage A Cost-Benefit Accounting

* Every design boundary introduces tradeoffs:

```
  Benefits of Extraction
  ├── Isolated presentation edits (Equipment Officer changes wording in 1 place)
  ├── Independent unit testability for text rendering without mocking coordinator
  └── Reduced coordinator cognitive surface area

  Architectural Costs & Tradeoffs
  ├── +1 new file (ConfirmationFormatter.java)
  ├── +1 new class and object instantiation overhead
  └── Call indirection (developer must jump across files)
```

* **When would extraction NOT be justified?**
  * If confirmation text was a hardcoded constant that had not changed in 5 years, keeping the private method would be entirely acceptable.

---

# Part 3: Open-Closed Principle & Polymorphic Policy

---

## Defining the Open-Closed Principle (OCP)

> "Software entities should be open for extension, but closed for modification."  
> - Bertrand Meyer (1988), Robert C. Martin (2002)

```
        CLIENT / CONSUMER
    (ReservationCoordinator)
               │
               │ Calls stable abstraction
               ▼
      «interface»
    BorrowingPolicy <───────────────── CLOSED to modification
    +mayRequest(...)
           ▲
           │ Implements
     ┌─────┴──────────────┐
     │                    │
StudentPolicy        StaffPolicy <─── OPEN to extension
 (0-2 loans,         (0-4 loans,      (Add without altering
  1-7 days)           1-14 days)       existing policies)
```

* **The Core Question:** "Closed against *which* change?"
  * No software can be closed against every conceivable future request!

---

## Concrete Variation: Staff vs Student Rules

* The required business policy:

| Borrower Category | Maximum Active Loans Allowed | Permitted Duration Range |
|---|---|---|
| **Student** | 0, 1, or 2 (rejects on 3rd existing) | 1 to 7 calendar days |
| **Staff** | 0, 1, 2, 3, or 4 (rejects on 5th existing) | 1 to 14 calendar days |

* **Shared Invariants across both policies:**
  * Active loans cannot be negative (< 0).
  * Requested days must be strictly positive (>= 1).
  * Neither policy checks equipment availability or user identity.

---

## The Contract Interface: `BorrowingPolicy`

* Listing: `BorrowingPolicy.java`

```java
/**
 * A deterministic, side-effect-free borrowing decision for every pair of ints.
 * Return false for negative counts or nonpositive durations; do not throw for them.
 * Return false for requests outside this implementation's documented limits.
 * A true result concerns count/duration only, not item availability or identity.
 */
public interface BorrowingPolicy {
    boolean mayRequest(int activeReservations, int requestedDays);
}
```

* **Design Elements:**
  * `public interface` expresses a behavioral contract.
  * No state, no side effects, pure decision function.
  * Method signature accepts plain Java `int` primitives.

---

## Student and Staff Implementations

```java
// Student Policy: Preserves existing Chapter 2 rules exactly
public final class ReservationRules implements BorrowingPolicy {
    @Override
    public boolean mayRequest(int activeReservations, int requestedDays) {
        return activeReservations >= 0
                && activeReservations < 3
                && requestedDays >= 1
                && requestedDays <= 7;
    }
}

// Staff Policy: New illustrative teaching rule
public final class StaffReservationRules implements BorrowingPolicy {
    @Override
    public boolean mayRequest(int activeReservations, int requestedDays) {
        return activeReservations >= 0
                && activeReservations < 5
                && requestedDays >= 1
                && requestedDays <= 14;
    }
}
```

---

## BorrowerCategory and Overload Preservation

* We introduce an enum to distinguish caller roles:

```java
public enum BorrowerCategory {
    STUDENT, STAFF
}
```

* **Preserving Backward Compatibility:**
  * Do NOT delete the existing 4-parameter `reserve(...)` method!

```java
// Retained legacy entry point: transparently defaults to STUDENT
public String reserve(String borrowerId, String itemId,
                      LocalDate start, int requestedDays) {
    return reserve(borrowerId, itemId, start, requestedDays, 
                   BorrowerCategory.STUDENT);
}

// New 5-parameter entry point: accepts explicit category
public String reserve(String borrowerId, String itemId, LocalDate start,
                      int requestedDays, BorrowerCategory category) { ... }
```

---

## The Policy Selector in `ReservationCoordinator`

* How does the coordinator select between policies?

```java
public final class ReservationCoordinator {
    private final BorrowingPolicy studentPolicy = new ReservationRules();
    private final BorrowingPolicy staffPolicy = new StaffReservationRules();

    // Inside the 5-parameter reserve method:
    if (!policyFor(category).mayRequest(activeCount, requestedDays)) {
        return "Rejected: borrower limit or duration.";
    }

    private BorrowingPolicy policyFor(BorrowerCategory category) {
        return switch (category) {
            case STUDENT -> studentPolicy;
            case STAFF -> staffPolicy;
        };
    }
}
```

* **Honest Design Analysis:**
  * Is the coordinator completely closed to new categories? **No!**
  * Adding `RESEARCHER` requires editing the `switch`.
  * But policy logic is decoupled from reservation sequencing.

---

## Architecture Diagram (Figure 5.1 Walkthrough)

```
┌────────────────────────────┐
│   ReservationCoordinator   │
└─────────┬───────────────┬──┘
          │               │
  formats │               │ asks eligibility
          ▼               ▼
┌──────────────────┐    ┌─────────────────┐
│ConfirmationFormat│    │ «interface»     │
└──────────────────┘    │ BorrowingPolicy │
                        └────────▲────────┘
                                 │
             ┌───────────────────┴───────────────────┐
             │                                       │
┌────────────────────────────┐       ┌────────────────────────────┐
│      ReservationRules      │       │    StaffReservationRules   │
└────────────────────────────┘       └────────────────────────────┘
```

* **Associations (Solid Arrows):** Coordinator references the interface.
* **Realizations (Dashed with hollow triangle):** Policies implement the interface.
* **Direct Dependencies:** Coordinator instantiates concrete policies (to be resolved in Week 5 via DIP).

---

## The Premature Abstraction Trap

* A student asks:
  * *"Why not build a `PolicyFactoryProviderRegistry` with dynamic reflection and XML rule loading?"*

```
     [ Complexity of Solution ]
                 ▲
                 │              x Over-Engineered Monster
                 │                (12 interfaces, reflection, plugin engine)
                 │
                 │      x Pragmatic OCP (Our 2-class Strategy)
                 │
                 │  x Inline If-Else
                 │
                 └────────────────────────►
                   [ Actual Requirement Complexity ]
```

* **Engineering Rule:** Solve the problem in front of you. Two known categories do not justify an enterprise plugin framework.

---

# Part 4: Behavioural Contracts & Liskov Substitutability

---

## Beyond Syntax: What is a Contract?

* A Java method signature only defines syntactic types:
  * `boolean mayRequest(int activeReservations, int requestedDays)`
* It does NOT answer:
  * Can it throw an unchecked exception?
  * Does it mutate internal state?
  * Is calling it twice with the same inputs guaranteed to return the same answer?
  * What does `false` mean versus throwing an exception?

> "A contract defines preconditions, postconditions, and invariants that callers may reliably depend upon."  
> - Bertrand Meyer, Design by Contract (1986)

---

## The Formal `BorrowingPolicy` Contract Table

| Contract Aspect | Supertype Guarantee | Caller Entitlement |
|---|---|---|
| **Input Domain** | Accepts all integer pairs (`Integer.MIN_VALUE` to `MAX_VALUE`) | Caller never needs try-catch for numeric inputs |
| **Invalid Inputs** | Count < 0 or Days <= 0 returns `false` | Safe refusal; no application crashes |
| **Output Meaning** | `true` iff inputs satisfy category rules | Approval relates purely to count & duration |
| **Side Effects** | Pure function; zero mutations or I/O | Safe to call repeatedly; thread-safe |
| **Repeatability** | Deterministic result for identical inputs | Calling twice yields identical booleans |

* Both `ReservationRules` and `StaffReservationRules` strictly obey this exact contract!

---

## The Negative Count Dilemma: Throw vs False

* Should `mayRequest(-1, 5)` throw `IllegalArgumentException`?

```
Option A: Throw Exception
  + Loudly signals caller logic bug (negative count is impossible)
  - Breaks backward compatibility with existing callers
  - Forces clients to handle runtime exceptions

Option B: Return false (Chosen Contract)
  + 100% backward compatible with existing test suite
  + Treats negative counts as ineligible requests
  - Caller bug looks like a policy denial
```

* **Lesson:** There is no universal "right" answer. The engineer's job is to make a conscious choice, document it, and preserve it across all subtypes.

---

## The Liskov Substitution Principle (LSP)

> "Let $\phi(x)$ be a property provable about objects $x$ of type $T$. Then $\phi(y)$ should be true for objects $y$ of type $S$ where $S$ is a subtype of $T$."  
> - Barbara Liskov (1987), Liskov & Wing (1994)

```
        CLIENT CODE
    f(Supertype obj) {
        obj.doSomething(); // Expects contract C
    }

       ▲             ▲
       │             │
   Pass Super     Pass Subtype
       │             │
       ▼             ▼
   [ WORKS ]     [ MUST WORK IDENTICALLY ]
                 (No surprises, no broken invariants)
```

* **Core Rule:** A subtype may **weaken** preconditions (demand less) and **strengthen** postconditions (guarantee more), but NEVER vice versa!

---

## Executable Counterexample: `IntHistory`

* Contract: Accepts any `int`, appends it to history, preserves order.

```java
// Base Class: The Supertype
static class IntHistory {
    private final List<Integer> values = new ArrayList<>();

    public void add(int value) { 
        values.add(value); 
    }
    public List<Integer> values() { 
        return List.copyOf(values); 
    }
}

// Client expecting base contract:
void client(IntHistory history) {
    history.add(5);
    history.add(-2); // Client expects [-2] to be stored!
    assert history.values().equals(List.of(5, -2));
}
```

---

## The Flawed Subtype: `PositiveOnlyHistory`

* A developer attempts to enforce a new constraint via inheritance:

```java
// INTENTIONALLY INVALID SUBTYPE
static final class PositiveOnlyHistory extends IntHistory {
    @Override
    public void add(int value) {
        if (value <= 0) {
            throw new IllegalArgumentException("Positive values only.");
        }
        super.add(value);
    }
}
```

* **What happens when passed to `client(new PositiveOnlyHistory())`?**
  * It compiles perfectly with `@Override`.
  * It crashes at runtime: `IllegalArgumentException: Positive values only.`
  * **LSP Violation:** The subtype strengthened the precondition!

---

## The Deceptive Subtype: Silent Failure

* A junior developer attempts to "fix" the exception:

```java
// EQUALLY FLAWED SUBTYPE
static final class SilentPositiveHistory extends IntHistory {
    @Override
    public void add(int value) {
        if (value > 0) {
            super.add(value);
        }
        // Silently ignore zero and negative numbers!
    }
}
```

* **Does this satisfy LSP?**
  * **NO!** The client asserts `history.values().equals(List.of(5, -2))`.
  * The actual state is `[5]`. The assertion fails!
  * **LSP Violation:** Weakened postconditions (failed to guarantee append).

---

## The Honest Architectural Repair: Composition

* If positive-only history is a distinct concept, model it honestly:

```java
// Distinct Type: Composition instead of Inheritance
static final class PositiveHistory {
    private final IntHistory entries = new IntHistory();

    public void addPositive(int value) {
        if (value <= 0) {
            throw new IllegalArgumentException("Positive values only.");
        }
        entries.add(value);
    }

    public List<Integer> values() { 
        return entries.values(); 
    }
}
```

* `PositiveHistory` does NOT inherit from `IntHistory`.
* It does not promise clients that it can accept negative numbers.

---

## Running the LSP Demonstration

* Compile and run the standalone counterexample:

```bash
javac --release 17 -d build/lsp examples/lsp/LspExample.java
java -cp build/lsp LspExample
```

* **Console Output:**
```text
Base contract client passed.
Expected counterexample: Positive values only.
Separate positive-history contract passed.
```

* **Interpreting the Test:**
  * The harness catches the expected exception to prove the flaw.
  * An exit code of 0 proves that the violation was successfully detected, not that the subtype was valid!

---

## Verifying Stage B: Cross-Category Regression

* Run the extended test suite in `after/scripts/check.sh`:

```bash
bash after/scripts/check.sh
```

```text
AC-01 passed
AC-02 passed
AC-03 passed
AC-04 passed
AC-05 passed
All 5 acceptance examples passed.
All 44 Chapter 5 checks passed.
BUILD AND CHECKS PASSED
```

* **What the 44 checks verify:**
  * Staff limits: 5th reservation accepted, 6th rejected.
  * Staff duration: 14 days accepted, 15 days rejected.
  * Cross-category conflicts: Student cannot reserve an item held by staff.
  * Default compatibility: 4-arg `reserve(...)` still enforces student limits.

---

# Part 5: Deliberate Faults & Bounding AI Refactoring

---

## Deliberate Fault Experiment 1: The Wording Slip

* **The Experiment:**
  * Suppose during Stage A extraction, a developer changes confirmation text:

```diff
- return "Confirmed: " + reservation.id() + ...
+ return "Reserved: " + reservation.id() + ...
```

* **What Happens:**
  * `javac` compiles cleanly.
  * PMD reports zero violations.
  * `Chapter02Checks` crashes immediately:
```text
AssertionError: exact first confirmation
  Expected: "Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)."
  Actual:   "Reserved: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)."
```
* **Lesson:** Refactoring means preserving observable behavior. Golden-master assertions protect against inadvertent API breaks.

---

## Deliberate Fault Experiment 2: Validation Inversion

* **The Experiment:**
  * Swap the order of eligibility check and overlap check in `reserve(...)`.
* **The Failure:**
  * Suppose an item is unavailable AND the borrower has exceeded their loan limit.
  * Original code: Returns `"Rejected: borrower limit or duration."`
  * Swapped code: Returns `"Rejected: item unavailable."`
* **Why this matters:**
  * Rejection messages are part of the client contract!
  * Automated tests verify error precedence, ensuring client error-handling workflows do not break.

---

## Bounding AI Assistance: The "Make This SOLID" Trap

* A developer gives this prompt to an LLM:  
  *"Refactor ReservationCoordinator.java to follow SOLID principles."*
* **The Fictional AI Generated Response:**

> "I have made your code SOLID!  
> 1. Created interfaces `IReservation`, `ILoanPeriod`, and `IReservationCoordinator`.  
> 2. Added an abstract base `AbstractReservationCoordinator` and a factory.  
> 3. Changed all return rejection strings to `ReservationException` hierarchies.  
> 4. Made `StaffReservationRules` extend `ReservationRules` and override duration.  
> 5. Shortened the confirmation message to 'Reserved'."

* **Critique this proposal!** How many defects can you spot?

---

## Auditing the AI's Proposal: 5 Major Flaws

```
AI Proposal Item       Engineering Verdict           Consequence
────────────────────────────────────────────────────────────────────────
1. IReservation        REJECT (Premature abstraction) Value objects do not 
                                                      need interfaces
2. AbstractCoordinator REJECT (YAGNI / Overkill)      We have 1 coordinator,
                                                      not 10
3. Replace strings     REJECT (Breaks contracts)      Breaks all 34 existing
   with Exceptions                                    regression tests!
4. StaffRules extends  REJECT (LSP Violation)         Breaks Liskov 
   StudentRules                                       Substitutability
5. Shorten message     REJECT (Behavior drift)        Breaks AC-01 acceptance
                                                      criteria
```

* **Key Takeaway:** An AI model optimizes for code aesthetic and buzzword density. The software engineer enforces contracts and boundary integrity!

---

## The Correct Way to Prompt AI for Refactoring

* **Prompt Pattern: Bounded Architectural Slicing**

```markdown
Role: Senior Java 17 Software Engineer.
Task: Extract confirmation string formatting from ReservationCoordinator.

Constraints:
1. Do NOT modify public method signatures or return types of ReservationCoordinator.
2. Do NOT change rejection strings or error handling semantics.
3. ConfirmationFormatter must receive an immutable Reservation and return String.
4. Output must match character-for-character with existing tests.
5. Provide a git diff showing only the minimal required extraction.
```

* **Outcome:** The AI produces a surgical, reviewable 15-line diff rather than an unmaintainable rewrite.

---

# Part 6: Workshop Deliverables, Team Lab & Wrap-Up

---

## Workshop Practical Activity: 8-Step Workflow

* **Steps 1-7: Book Project (Campus Lending)**
  1. Produce responsibility table and run `javac -Xlint:all` + PMD on `before`.
  2. Record passing baseline, execute Stage A extraction, rerun checks.
  3. Add `BorrowingPolicy` and `StaffReservationRules` in Stage B.
  4. Run boundary and cross-category checks.
  5. Run `LspExample.java` counterexample harness.
  6. Conduct peer code review on the git diff.
  7. Document design rationale and PMD score comparison.
* **Step 8: Team Project Transfer**
  * Apply the responsibility table and PMD smell ruleset to your team's repo!

---

## Team Project Smell Review Template

* Use this exact format in your weekly lab notebook:

| Class Name | Method Under Review | Identified Smell | Evidence / PMD Metric | Proposed Refactoring |
|---|---|---|---|---|
| `ItemCatalog` | `searchAndFilter(...)` | Long Method | PMD Cyclomatic = 14 | Extract Predicate Strategy |
| `UserSession` | `authenticate(...)` | Feature Envy | Accesses 5 fields of `User` | Move method to `User` |
| `DeviceStore` | Constructor | Hidden Construction | Calls `new SqliteDriver()` | Inject repository (Week 5) |

* Focus on smells that correlate with real change pressures in your team backlog!

---

## Module Review & Exam Pointers

* **Midterm / Exam Question Patterns:**
  * *Question 1:* "Given a class that violates SRP, draw a UML diagram showing how to extract a collaborator and explain the tradeoffs."
  * *Question 2:* "Explain why `PositiveOnlyHistory` violating `IntHistory`'s contract is an LSP defect even though it compiles with `@Override`."
  * *Question 3:* "Why does extracting a straight-line private method fail to reduce Cyclomatic Complexity in static analysis?"
* **Core Vocabulary:**
  * Precondition, Postcondition, Class Invariant, Divergent Change, Cyclomatic Complexity, Protected Variation.

---

## Key Takeaways

1. **SRP is about Actors:**
   * A class should have one reason to change, driven by an organizational role.
2. **OCP requires an Axis of Variation:**
   * Close code against changes you anticipate; do not build speculative plugin engines.
3. **LSP is a Behavioral Contract:**
   * Subtypes must satisfy client expectations. Never strengthen preconditions or weaken postconditions.
4. **Refactoring requires Regression Safety:**
   * Separate structural restructuring (Stage A) from feature additions (Stage B).
5. **Static Analysis is an Assistant, Not a Judge:**
   * Triangulate compiler checks, human reviews, and PMD metrics.

---

## Looking Ahead to Week 5

* **Next Lecture: SOLID II: Interfaces, Inversion & Composition**
  * **Interface Segregation Principle (ISP):** Fat interfaces vs role interfaces.
  * **Dependency Inversion Principle (DIP):** High-level modules must not depend on low-level details.
  * **Plain-Java DI Container:** Building a dependency injection seam without Spring.
  * **Preparation:** Complete steps 1-8 of Chapter 5 lab and review Chapter 6 readings.

---

# Questions & Discussion
### SE506: Object Oriented Development and Agile Practices
*Slides and code available on the module repository.*
