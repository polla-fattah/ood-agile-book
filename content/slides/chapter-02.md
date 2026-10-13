---
title: "Chapter 2: Object-Oriented Development Beyond Syntax"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 20
type: slides
layout: page
---

# Chapter 2: Object-Oriented Development Beyond Syntax
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **2.1 Objects, identity, state and behaviour**
  * Four small classes, three kinds of identity, mutable and immutable objects.
* **2.2 Responsibilities and invariants**
  * The half-open period convention and who protects which condition.
* **2.3 Encapsulation and information hiding**
  * Why `private` is not enough, and what `List.copyOf` does.
* **2.4 Cohesion, coupling and dependencies**
  * Diagnosing a method by its reasons to change, then one modest refactoring.

---

## Chapter Roadmap (2 of 3)

* **2.5 Composition and inheritance**
  * Use versus subtype, and why a hierarchy is not the default.
* **2.6 UML class diagrams: reading, drawing and checking**
  * The notation the midterm assesses, so it gets the most time.
* **2.7 Git history, branches and review**
  * A small, reviewable change and the commands that inspect it.
* **2.8 AI in practice: tracing a coordinator**
  * Classifying the claims of a plausible but flawed explanation.

---

## Chapter Roadmap (3 of 3)

* **2.9 Common mistakes**
  * Eight misconceptions, each with a better question.
* **2.10 Practical activity: one checked design improvement**
  * Parts A to D: trace, diagnose, change, organise the team.
* **2.11 Review questions and transfer challenge**
  * Room-booking coordinator in a different domain.
* **2.12 Chapter summary**
  * What carries into Chapter 3 (Agile development and the nature of change).

---

## Learning Outcomes (1 of 2)

By the end of the chapter, you should be able to:

1. **Assign responsibilities** to objects and explain the state they protect.
2. **Distinguish encapsulation and information hiding** from mechanically adding getters and setters.
3. **Diagnose cohesion and coupling** problems using concrete change scenarios.

---

## Learning Outcomes (2 of 2)

4. **Compare composition with inheritance** and justify a modest design choice.
5. **Draw and interpret a small UML class diagram** that matches the code, using associations, multiplicity, aggregation, composition, inheritance and interface realisation appropriately.
6. **Make a behaviour-preserving improvement** and present it as a reviewed Git change.

---

## Reading Route

* **Core reading:** Sections 2.1 to 2.9.
  * Section 2.6 (UML class diagrams) is the notation the midterm assesses, so give it the most time.
* **Minimum required lab:** the Section 2.8 AI activity and Parts A to D of Section 2.10.
  * Parts A to C run on the **Book project**; Part D concerns your **Team project**.
* **Optional extension:** the optional investigation at the end of 2.10, then the review questions and transfer challenge.

---

## Build on Chapter 1, Use the Companion

* This chapter builds on Chapter 1's reservation-rule example.
* You should be able to trace conditions, call methods and explain a returned value.
* Java's official class tutorial gives targeted syntax revision. Appendix A has a short refresher.
* The **companion** holds every complete source file, a starting version, a completed refactoring, checks and suggested answers.
* Use its starting listings first. Consult solutions **after** attempting the activity.

---

## Toolchain Baseline

* Java 17 language and API baseline. **No preview features, no external dependencies.**
* A JDK is required to compile the examples.
* JUnit, Maven and CI configuration are **not** prerequisites for this first design exercise.
* They are introduced with the relevant later work. Appendix B records the toolchain and commands for the whole book.

---

## Weekly Reading and Project Checkpoint

* **Reading:** Martin, *Agile Software Development: Principles, Patterns, and Practices*. The Part I introduction and the object-oriented design fundamentals. Sections 2.1 to 2.5 are the practical counterpart.
* **Starting checkpoint:** the Chapter 2 starter in the companion.
* **Resulting checkpoint:** the same code after the confirmation extraction. It becomes the **cumulative baseline** for later chapters.
* The fault demonstrations and the notation examples in 2.6 are separate teaching material. They do not join the project.

---

## Opening Scenario: A Demonstration That Works

* The equipment officer can now try a small reservation application.
* It checks a borrower's limit, looks for a conflicting reservation, records a successful request and returns a confirmation message.
* The demonstration works.
* But the developer who wrote it is **absent** when another team member is asked to change the message.

---

## The New Developer Opens `ReservationCoordinator`

* One method does all of this:
  * counts reservations,
  * applies a borrowing rule,
  * searches for date conflicts,
  * creates a record,
  * assembles the confirmation text.
* Which lines may be changed **safely**?

---

## Three Questions to Carry Through the Chapter

1. Why is the conflict check concerned with an **equipment item** while the count is concerned with a **borrower**?
2. Could the list of stored reservations be **changed from outside** the class?
3. Which responsibilities **belong together**, and how should other code be allowed to use them?

* Knowing how to declare a class is necessary. It does not answer these.

---

# 2.1 Objects, Identity, State and Behaviour
### Four small classes

---

## Class and Object

* A **class** defines a type and its implementation.
* An **object** is an instance created at run time.
* Two objects from the same class can represent **different things** and hold **different state**.
* Java gives us **fields, constructors and methods** to express these distinctions.

---

## The `Reservation` Record

* A `Reservation` records an arrangement involving a borrower, an equipment item and a period.
* Its state:
  * an identifier such as `R1`,
  * a borrower identifier such as `B1`,
  * an item identifier such as `CAM1`,
  * a `LoanPeriod`.

---

## Identifiers Are Different Kinds of Identity

* Two physical cameras may share a model name but need **different item identifiers**.
* Two reservations for the same camera on different dates are **still separate reservations**.
* A borrower's name is a poor identifier: names can change or be shared by different people.
* The identifiers stand in for borrower and equipment records. A non-blank identifier does **not** prove a real person or item exists.

---

## Java Object Identity

* Two references can point to the **same instance**, or to **distinct instances** that represent the same domain identifier.
* `==` on references checks whether they refer to the **same object**.
* Domain equality needs a **deliberate definition**. It is not automatically established by matching fields.
* Our `Reservation` does **not** override `equals`. Do not assume identifier-based equality.

---

## State and Behaviour

* **State** is information an object holds.
* **Behaviour** is what it can do through its operations.
* A reservation can expose its identifier and period **without** letting callers replace them.
* A coordinator can add a new record **after checking** the request.
* A period can answer whether it **overlaps** another period.

---

## Not Everything Needs to Be Mutable

* In the starter, `Reservation` and `LoanPeriod` are **immutable** after construction:
  * their fields cannot be reassigned,
  * their referenced values are immutable,
  * their operations do not modify state.
* The **coordinator** is different. It accumulates reservations in a private list.

---

## Why the Same Request Can Give a Different Answer

* Chapter 1's `mayRequest` only examined **supplied numbers**.
* A call to the coordinator may **change the state** that the next call examines.
* After one successful reservation, the same request can be rejected as unavailable.

---

## From the Numeric Rule to a Small System

* `ReservationRules` stays **unchanged**: at most three active reservations, one to seven days.
* The staff variation remains a future design exercise.
* This checkpoint applies the **student policy to every borrower identifier**.
* The starter has four domain and application classes.

---

## The Four Starter Classes

| Class | Main role | State held |
|---|---|---|
| `ReservationRules` | Evaluate the numeric borrowing policy | No instance fields |
| `LoanPeriod` | Represent a valid period; answer overlap questions | Start date and exclusive end date |
| `Reservation` | Record a confirmed reservation | Three identifiers; a period |
| `ReservationCoordinator` | Process requests using policy and existing records | In-memory reservations; a rules object |

---

## The Starter Files

| File | Role |
|---|---|
| `ReservationRules.java` | The unchanged numeric policy from Chapter 1 |
| `LoanPeriod.java` | Valid dates and exclusive-end overlap semantics |
| `Reservation.java` | Immutable reservation details |
| `ReservationCoordinator.java` | The starting request workflow |
| `Chapter02Demo.java` | Three requests: success, overlap, adjacency |
| `Chapter02Checks.java` | Supplied behavioural checks (34) |

---

# 2.2 Responsibilities and Invariants
### Who protects which condition?

---

## Responsibility vs. Data

* A **responsibility** is an obligation assigned to part of the system.
* "Hold two dates" describes **data**.
* "Represent a period whose end follows its start" describes an **obligation** that gives the data meaning.

---

## Invariants Belong at Different Boundaries

* An **invariant** is a condition that must hold for valid objects or valid system states.
* One `LoanPeriod` can ensure its **end is after its start**.
* It cannot, by itself, ensure that **another reservation has not already claimed the same equipment**.
* Local invariants and system-level conditions need different enforcement points.

---

## A Period Convention We Can Test

* Dates are **calendar dates** with no time of day.
* A period is **start inclusive, end exclusive**: `[start, end)`.
* 20 October to 22 October covers the **20th and 21st**. Another period may begin on the **22nd**.
* This is an explicit teaching policy. A real service might require a cleaning or inspection interval, which would need another rule.

---

## `LocalDate` and the Convention

* Java's `LocalDate` is **immutable** and represents a date **without** a time or time zone.
* We use `isBefore` and `plusDays` to express the convention.
* We do **not** interpret these dates as UTC instants or fixed numbers of elapsed hours.
* The exclusive-end convention is a **project decision**, not a rule `LocalDate` imposes.

---

## The `LoanPeriod` Constructor

```java
public LoanPeriod(LocalDate start, LocalDate endExclusive) {
    this.start = Objects.requireNonNull(start, "start");
    this.endExclusive =
        Objects.requireNonNull(endExclusive, "endExclusive");
    if (!start.isBefore(endExclusive)) {
        throw new IllegalArgumentException("End must be after start.");
    }
}
```

* Missing date: `NullPointerException`. Zero-length or reversed interval: `IllegalArgumentException`.

---

## The `overlaps` Operation

```java
public boolean overlaps(LoanPeriod other) {
    Objects.requireNonNull(other, "other");
    return start.isBefore(other.endExclusive)
            && other.start.isBefore(endExclusive);
}
```

* Two periods overlap when **each begins before the other ends**.
* Both comparisons are **strict**, so adjacent periods do **not** overlap.
* `requireNonNull` throws for a null argument. It does not fabricate a replacement period.

---

## Four Overlap Examples on a Timeline

<!--svg:ch02-overlap-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 360" role="img" aria-label="Timeline of four pairs of half-open periods against 19 to 24 October, showing which pairs overlap." style="display:block;width:100%;height:calc(var(--u) * 36.00);margin:0 auto">
<defs><marker id="ch02-overlap-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-overlap-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-overlap-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-overlap-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-overlap-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<text x="382.5" y="26.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="middle">19 Oct</text>
<text x="467.5" y="26.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="middle">20 Oct</text>
<text x="552.5" y="26.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="middle">21 Oct</text>
<text x="637.5" y="26.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="middle">22 Oct</text>
<text x="722.5" y="26.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="middle">23 Oct</text>
<text x="807.5" y="26.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="middle">24 Oct</text>
<line x1="340" y1="38" x2="340" y2="318" stroke="#c3cfdd" stroke-width="1.5"/>
<line x1="425" y1="38" x2="425" y2="318" stroke="#c3cfdd" stroke-width="1.5"/>
<line x1="510" y1="38" x2="510" y2="318" stroke="#c3cfdd" stroke-width="1.5"/>
<line x1="595" y1="38" x2="595" y2="318" stroke="#c3cfdd" stroke-width="1.5"/>
<line x1="680" y1="38" x2="680" y2="318" stroke="#c3cfdd" stroke-width="1.5"/>
<line x1="765" y1="38" x2="765" y2="318" stroke="#c3cfdd" stroke-width="1.5"/>
<line x1="850" y1="38" x2="850" y2="318" stroke="#c3cfdd" stroke-width="1.5"/>
<text x="10.0" y="68.0" font-size="17" font-family="'Plex Mono', monospace" font-weight="600" fill="#1d588c" text-anchor="start">[20, 22) and [21, 23)</text>
<text x="10.0" y="94.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">Overlap: Yes. Both include 21 Oct</text>
<rect x="425.0" y="50.0" width="170.0" height="24.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="2"/>
<rect x="510.0" y="78.0" width="170.0" height="24.0" rx="4" fill="#b4762e" stroke="#b4762e" stroke-width="2"/>
<text x="10.0" y="136.0" font-size="17" font-family="'Plex Mono', monospace" font-weight="600" fill="#1d588c" text-anchor="start">[20, 22) and [22, 23)</text>
<text x="10.0" y="162.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">Overlap: No. Second starts at the first's end</text>
<rect x="425.0" y="118.0" width="170.0" height="24.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="2"/>
<rect x="595.0" y="146.0" width="85.0" height="24.0" rx="4" fill="#b4762e" stroke="#b4762e" stroke-width="2"/>
<text x="10.0" y="204.0" font-size="17" font-family="'Plex Mono', monospace" font-weight="600" fill="#1d588c" text-anchor="start">[20, 22) and [20, 22)</text>
<text x="10.0" y="230.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">Overlap: Yes. Identical periods overlap</text>
<rect x="425.0" y="186.0" width="170.0" height="24.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="2"/>
<rect x="425.0" y="214.0" width="170.0" height="24.0" rx="4" fill="#b4762e" stroke="#b4762e" stroke-width="2"/>
<text x="10.0" y="272.0" font-size="17" font-family="'Plex Mono', monospace" font-weight="600" fill="#1d588c" text-anchor="start">[20, 22) and [19, 24)</text>
<text x="10.0" y="298.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">Overlap: Yes. The second contains the first</text>
<rect x="425.0" y="254.0" width="170.0" height="24.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="2"/>
<rect x="340.0" y="282.0" width="425.0" height="24.0" rx="4" fill="#b4762e" stroke="#b4762e" stroke-width="2"/>
<rect x="340.0" y="328.0" width="22.0" height="14.0" rx="3" fill="#1d588c" stroke="#1d588c" stroke-width="2"/>
<text x="370.0" y="340.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">first period, always [20, 22)</text>
<rect x="620.0" y="328.0" width="22.0" height="14.0" rx="3" fill="#b4762e" stroke="#b4762e" stroke-width="2"/>
<text x="650.0" y="340.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start">second period</text>
</svg>
</div>
<!--/svg-->

---

## The Same Examples as a Table

| First | Second | Overlap? | Why |
|---|---|---|---|
| `[20 Oct, 22 Oct)` | `[21 Oct, 23 Oct)` | Yes | Both include 21 October |
| `[20 Oct, 22 Oct)` | `[22 Oct, 23 Oct)` | No | Second begins at the first's exclusive end |
| `[20 Oct, 22 Oct)` | `[20 Oct, 22 Oct)` | Yes | Identical periods overlap |
| `[20 Oct, 22 Oct)` | `[19 Oct, 24 Oct)` | Yes | The second contains the first |

* Comparing start dates alone would miss some of these relationships.

---

## Who Protects Which Condition?

* The **constructor** protects the local validity of a period.
* **`ReservationRules`** protects the numeric policy, **only when given an accurate count**.
* The **coordinator** counts its records and checks item conflicts before storing.
* No one class can enforce all of these without information from the others.

---

## Operating Assumptions of the Starter (1 of 2)

* All stored records are **confirmed and remain active**: no cancellation, completion or expiry.
* Calls occur **sequentially in one process**.
* Data **disappear** when the process ends.
* Identifiers are matched **exactly**, with no normalisation or authentication.

---

## Operating Assumptions of the Starter (2 of 2)

* The coordinator checks availability **only against its own stored records**.
* Maintenance schedules and other coordinators are outside this checkpoint.
* Within one sequential coordinator, checking conflicts before adding prevents the demonstrated overlap.
* It does **not** establish safe concurrent booking by multiple processes. Later integration work revisits that boundary.

---

# 2.3 Encapsulation and Information Hiding
### Why `private` is not enough

---

## Three Related Ideas

* **Encapsulation** groups state with the operations that govern its use, and controls access to that state.
* **Information hiding** concerns which implementation decisions callers should not need to know.
* **Abstraction** presents what is relevant to a caller and leaves out unnecessary detail.
* None is achieved simply by writing `private` before every field.

---

## Abstraction Through an Ordinary Method

* A caller can ask a period whether it overlaps another without repeating the date comparisons.
* That abstraction exists through an **ordinary public method**.
* It does not need Java's `abstract` keyword or a separate interface.
* A useful abstraction still needs a **clear contract**, including our decision that **adjacent periods do not overlap**.

---

## Setters Can Defeat Private Fields

* Suppose a class exposes separate setters for a period's start and end.
* A caller could move the start **beyond the current end**.
* If each setter merely assigns a field, making the fields private has **not protected the relationship between them**.

---

## How `LoanPeriod` Avoids This

* The constructor requires **both dates together** and validates the relationship.
* It provides readers but **no setters**.
* To express another period, a caller creates **another valid object**.
* No invalid intermediate state enters the public protocol.
* In another domain a controlled mutation operation could be right. Immutability is a **design choice**, not a rule.

---

## A Getter Can Expose a Mutation Path

```java
// Unsafe alternative for diagnosis; not the starter implementation.
public List<Reservation> reservations() {
    return reservations;
}
```

* The field is `private`. The caller still receives **a reference to the mutable list**.

---

## The Attack: `clear()`

* A caller can invoke `coordinator.reservations().clear()`.
* That erases records **without passing through the coordinator's request checks**.
* The next request finds no conflicts.
* "My fields are private" does **not** mean the state is protected.

---

## The Starter's Protection

```java
public List<Reservation> reservations() {
    return List.copyOf(reservations);
}
```

* `List.copyOf` returns an **unmodifiable list** whose contents are not updated by later changes to the source.
* It protects the **list structure** and provides a **snapshot**.

---

## What `List.copyOf` Does Not Do

* It does **not deep-copy** the elements.
* It does **not** make mutable elements immutable.
* Here, `Reservation`, `LoanPeriod`, `String` and `LocalDate` already provide the immutability needed for the values we expose.
* Be able to explain the protection **without claiming all copies are deep copies**.

---

## `final` Does Not Help

* `private final List<Reservation>` alone would be **insufficient**.
* `final` prevents **reassignment of the field** to another list.
* It does **not** prohibit `add` or `clear` on that list.
* Reference fixed, object immutable, or both? Always ask which.

---

## What Remains Exposed

* The coordinator still exposes more representation than a mature system might require: callers know stored reservations can be inspected as a list.
* That is acceptable for a small teaching checkpoint.
* If a caller later needs only a **count** or an **availability answer**, a narrower operation may reduce what the caller must understand.

---

# 2.4 Cohesion, Coupling and Dependencies
### Diagnose by reasons to change

---

## Cohesion

* **Cohesion** concerns how closely the responsibilities within a component belong together.
* `LoanPeriod` has a focused purpose: its **validation and overlap calculation concern the same period concept**.
* A coordinator that also knows message wording, storage details and borrowing policy has **more varied responsibilities**.

---

## Coupling

* **Coupling** concerns the dependencies between components.
* A component depends on another when it relies on its **type, operations, data format or behaviour**.
* Some dependency is necessary: software works because components collaborate.
* The question: does the dependency express a **useful relationship**, or let **unrelated changes spread**?

---

## The `reserve` Method: Validate and Count

```java
public String reserve(String borrowerId, String itemId,
                      LocalDate start, int requestedDays) {
    if (borrowerId == null || borrowerId.isBlank()
            || itemId == null || itemId.isBlank()) {
        throw new IllegalArgumentException(
            "Identifiers must not be blank.");
    }
    Objects.requireNonNull(start, "start");
    int activeCount = 0;
    for (Reservation existing : reservations) {
        if (existing.borrowerId().equals(borrowerId)) { activeCount++; }
    }
```

---

## The `reserve` Method: Policy and Conflict

```java
    if (!rules.mayRequest(activeCount, requestedDays)) {
        return "Rejected: borrower limit or duration.";
    }
    LoanPeriod requested =
            new LoanPeriod(start, start.plusDays(requestedDays));
    for (Reservation existing : reservations) {
        if (existing.itemId().equals(itemId)
                && existing.period().overlaps(requested)) {
            return "Rejected: item unavailable.";
        }
    }
```

* Policy is rejected **before** availability; keep that order.

---

## The `reserve` Method: Store and Confirm

```java
    Reservation reservation = new Reservation(
            "R" + (reservations.size() + 1), borrowerId, itemId, requested);
    reservations.add(reservation);
    return "Confirmed: " + reservation.id()
            + " for " + reservation.borrowerId()
            + " on " + reservation.itemId()
            + " [" + reservation.period().start()
            + ", " + reservation.period().endExclusive() + ").";
}
```

* It creates and stores a reservation, then assembles its confirmation. It **does not send** it.

---

## The Request as a Flow

<!--svg:ch02-reserve-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 335" role="img" aria-label="The reserve method as a flow: validate identifiers, count the borrower&#x27;s records, apply the numeric rule, check for an overlapping reservation of the same item, then create, store and confirm. Two paths end in a rejection with nothing stored." style="display:block;width:100%;height:calc(var(--u) * 33.50);margin:0 auto">
<defs><marker id="ch02-reserve-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-reserve-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-reserve-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-reserve-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-reserve-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="5.0" y="55.0" width="112.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="61.0" y="75.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Validate</text>
<text x="61.0" y="95.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">identifiers</text>
<text x="61.0" y="115.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">and start</text>
<rect x="142.0" y="55.0" width="122.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="203.0" y="75.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Count this</text>
<text x="203.0" y="95.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">borrower's</text>
<text x="203.0" y="115.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">records</text>
<polygon points="372.5,40.0 455.0,90.0 372.5,140.0 290.0,90.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="372.5" y="85.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">rules.mayRequest</text>
<text x="372.5" y="104.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">(count, days)?</text>
<polygon points="602.5,40.0 685.0,90.0 602.5,140.0 520.0,90.0" fill="#f6ead9" stroke="#b4762e" stroke-width="2.2"/>
<text x="602.5" y="85.7" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Overlaps a record</text>
<text x="602.5" y="104.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">for this item?</text>
<rect x="745.0" y="55.0" width="120.0" height="70.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="805.0" y="75.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">Create, add</text>
<text x="805.0" y="95.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">and return</text>
<text x="805.0" y="115.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">confirmation</text>
<rect x="262.0" y="225.0" width="220.0" height="62.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="372.0" y="251.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Rejected: borrower</text>
<text x="372.0" y="271.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">limit or duration</text>
<rect x="492.0" y="225.0" width="220.0" height="62.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="602.0" y="251.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Rejected:</text>
<text x="602.0" y="271.4" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">item unavailable</text>
<path d="M117.0,90.0 L142.0,90.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-reserve-arr)"/>
<path d="M264.0,90.0 L290.0,90.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-reserve-arr)"/>
<path d="M455.0,90.0 L520.0,90.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-reserve-arr)"/>
<text x="487.0" y="80.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">allowed</text>
<path d="M685.0,90.0 L745.0,90.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-reserve-arr)"/>
<text x="715.0" y="80.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">free</text>
<path d="M372.5,140.0 L372.5,225.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-reserve-arr)"/>
<text x="390.5" y="188.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">no</text>
<path d="M602.5,140.0 L602.5,225.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-reserve-arr)"/>
<text x="622.5" y="188.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">yes</text>
<text x="435.0" y="322.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Neither rejection adds a record or uses an identifier.</text>
</svg>
</div>
<!--/svg-->

---

## Not Wrong Merely Because It Has Several Steps

* Coordination often involves several collaborators.
* "The method is long" is **not** a diagnosis.
* The useful question is: **which decisions have independent reasons to change?**

---

## Diagnosis by Change Scenario (1 of 2)

| Possible request | Decision it affects | Current location |
|---|---|---|
| Change a borrowing limit | Numeric policy | `ReservationRules` |
| Add a maintenance gap between reservations | Availability policy and period use | Coordinator conflict check, possibly period rules |

---

## Diagnosis by Change Scenario (2 of 2)

| Possible request | Decision it affects | Current location |
|---|---|---|
| Store records beyond process lifetime | Storage mechanism | Coordinator's list and storage operations |
| Translate a confirmation message | Presentation wording | Coordinator's final return expression |

* This identifies which changes **currently require editing the coordinator**, and why.
* A future database is a **possible** boundary. It is not a reason to build a repository framework now.

---

## A Small Improvement with a Limited Claim

* Extract the confirmation expression into a **private method** `confirmationFor`.
* The request method still **adds the record first**, then returns the helper's result.
* The helper receives the existing reservation and returns **exactly the same text**.
* This is a modest **refactoring**: it gives the formatting a name.

---

## What the Extraction Does Not Do

* It does **not** create a separate presentation component.
* It does **not** remove storage coupling.
* It does **not** make the coordinator thread-safe.
* A private helper changes **readability inside the class**. A new component would change the **collaboration between classes**.
* If translation later needs collaborators, a separate formatting responsibility may become justified.

---

## Preserving Behaviour: Text and State

* The supplied checks examine **both returned messages and stored state**.
* After the extraction both must remain the same.
* Preserving the success string while **forgetting to store** the reservation would **not** preserve behaviour.

---

# 2.5 Composition and Inheritance
### Use, containment or subtype?

---

## Composition

* **Composition**, in the broad programming sense: building behaviour by giving an object collaborators or component objects.
* A `Reservation` **has** a `LoanPeriod` and delegates the overlap question through it.
* A coordinator **has** a `ReservationRules` object. It does not inherit from it.

---

## It Fits the Domain Meanings

* A coordinator is **not a kind of** borrowing rule.
* A reservation is **not a kind of** period.
* Their relationships concern **what they use or contain**, not a subtype relationship.

---

## Inheritance

* **Inheritance** defines a derived class in relation to a superclass.
* Java supports inherited members, method overriding and run-time selection of overridden instance methods.
* These mechanisms can express a useful family of related behaviours.
* They also establish **expectations that callers may rely on**.

---

## A Hypothetical `SpecialReservation`

* Suppose a subclass is introduced **only because some borrowers have longer limits**.
* Is the difference really a **new kind of reservation**, or a **policy governing whether one may be created**?
* If staff status can change while an existing reservation keeps its identity, forcing that distinction into a hierarchy may be awkward.

---

## Not a Verdict Against Inheritance

* This does not prove inheritance is always unsuitable.
* Ask: **what varies**, **what remains stable**, and **what a caller expects from the base type**.
* Chapter 5 develops **behavioural substitutability** more formally.
* For this checkpoint, constructors, fields and collaborators already express the relationships **without a custom hierarchy**.

---

## Composition vs. Inheritance: Questions

| Question | Composition can help when | Inheritance deserves consideration when |
|---|---|---|
| What is the relationship? | One object uses or contains another | One type has a meaningful subtype relationship |
| What varies? | A collaborator or delegated responsibility | Behaviour shared through a stable base contract |
| What must be reviewed? | How collaborators are selected and called | Whether derived behaviour preserves caller expectations |

---

## Composition Has Costs Too

* Too many small collaborators make a request **harder to follow**.
* Avoid replacing one readable expression with several classes **unless that organisation solves an actual problem**.
* The design goal is **understandable responsibility boundaries**, not the maximum number of objects.

---

# 2.6 UML Class Diagrams
### Reading, drawing and checking

---

## What a Class Diagram Is

* A class diagram is a **selective explanation** of a design.
* It answers **one question for one audience**: for example, "which objects take part in a reservation request, and how are they related?"
* It is **not a copy of the source code**. A diagram showing every field and method answers no question well.
* Class diagrams are the **only UML notation** used in this chapter.

---

## Three Skills in This Section

1. **Read** a diagram.
2. **Draw** one from a written description.
3. **Check** one against code.

* Hand-drawn diagrams use the same symbols as the ones in this book.
* The book's diagrams are written as text (Mermaid) so they can be kept beside the code. Appendix A shows the syntax.

---

## Figure 2.1: The Starter's Collaborators

<!--svg:ch02-fig21-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 360" role="img" aria-label="Figure 2.1: ReservationCoordinator uses one ReservationRules and stores zero or more Reservations; each Reservation refers to one LoanPeriod." style="display:block;width:100%;height:calc(var(--u) * 36.00);margin:0 auto">
<defs><marker id="ch02-fig21-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig21-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig21-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig21-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig21-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="6.0" width="448.5" height="117.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,42.0 L12.0,12.0 Q12.0,8.0 16.0,8.0 L452.5,8.0 Q456.5,8.0 456.5,12.0 L456.5,42.0 Z" fill="#e6eef6"/>
<text x="234.2" y="31.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReservationCoordinator</text>
<line x1="10.0" y1="42.0" x2="458.5" y2="42.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="64.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+reserve(String borrowerId, String itemId,</text>
<text x="22.0" y="87.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">   LocalDate start, int requestedDays) String</text>
<text x="22.0" y="110.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+reservations() List&lt;Reservation&gt;</text>
<rect x="570.0" y="6.0" width="290.0" height="117.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M572.0,42.0 L572.0,12.0 Q572.0,8.0 576.0,8.0 L854.0,8.0 Q858.0,8.0 858.0,12.0 L858.0,42.0 Z" fill="#e6eef6"/>
<text x="715.0" y="31.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReservationRules</text>
<line x1="570.0" y1="42.0" x2="860.0" y2="42.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="582.0" y="64.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+mayRequest(</text>
<text x="582.0" y="87.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">   int activeReservations,</text>
<text x="582.0" y="110.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">   int requestedDays) boolean</text>
<rect x="10.0" y="200.0" width="216.0" height="152.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,236.0 L12.0,206.0 Q12.0,202.0 16.0,202.0 L220.0,202.0 Q224.0,202.0 224.0,206.0 L224.0,236.0 Z" fill="#e6eef6"/>
<text x="118.0" y="225.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Reservation</text>
<line x1="10.0" y1="236.0" x2="226.0" y2="236.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="258.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String id</text>
<text x="22.0" y="281.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String borrowerId</text>
<text x="22.0" y="304.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String itemId</text>
<line x1="10.0" y1="317.0" x2="226.0" y2="317.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="339.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+period() LoanPeriod</text>
<rect x="340.0" y="200.0" width="355.5" height="129.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M342.0,236.0 L342.0,206.0 Q342.0,202.0 346.0,202.0 L689.5,202.0 Q693.5,202.0 693.5,206.0 L693.5,236.0 Z" fill="#e6eef6"/>
<text x="517.8" y="225.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">LoanPeriod</text>
<line x1="340.0" y1="236.0" x2="695.5" y2="236.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="352.0" y="258.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-LocalDate start</text>
<text x="352.0" y="281.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-LocalDate endExclusive</text>
<line x1="340.0" y1="294.0" x2="695.5" y2="294.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="352.0" y="316.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+overlaps(LoanPeriod other) boolean</text>
<path d="M458.5,64.0 L570.0,64.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-fig21-open)"/>
<text x="485.5" y="85.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="543.0" y="85.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="514.2" y="50.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">uses</text>
<path d="M100.0,123.0 L100.0,200.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-fig21-open)"/>
<text x="84.0" y="155.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="84.0" y="178.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="118.0" y="166.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">stores</text>
<path d="M226.0,262.0 L340.0,262.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-fig21-open)"/>
<text x="253.0" y="283.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="313.0" y="283.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="283.0" y="248.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">refers to</text>
</svg>
</div>
<!--/svg-->

---

## Reading the Boxes

* Each box is a class with up to **three compartments**:
  * top: the **class name**,
  * middle: the **attributes** (data the class keeps),
  * bottom: the **operations** (methods other code can call).
* A label in double angle brackets above the name, such as `<<interface>>`, says what **kind** of class it is.
* `+` marks a **public** member and `-` a **private** one.

---

## A Box and the Java It Describes

```java
// Excerpt from LoanPeriod.java; method bodies omitted.
public final class LoanPeriod {
    private final LocalDate start;
    private final LocalDate endExclusive;

    public LoanPeriod(LocalDate start, LocalDate endExclusive) { ... }
    public LocalDate start() { ... }
    public LocalDate endExclusive() { ... }
    public boolean overlaps(LoanPeriod other) { ... }
}
```

---

## Mapping Box Parts to Source

| Part of the box | In the Java source | How to read it |
|---|---|---|
| `LoanPeriod` | `class LoanPeriod` | The class name |
| `-LocalDate start` | `private final LocalDate start;` | A private attribute `start` of type `LocalDate` |
| `+overlaps(LoanPeriod other) boolean` | `public boolean overlaps(LoanPeriod other)` | A public operation taking a `LoanPeriod`, returning `boolean` |

* Type comes **before** the name, as in Java. The return type comes **after** the parameter list.

---

## What a Box Leaves Out

* The constructor and the accessors `start()` and `endExclusive()` exist in the code but **not in the box**.
* The explanation does not need them.
* You can **trust a diagram for what it shows**.
* You **cannot assume that what it omits does not exist**.

---

## Attribute or Line, Not Both

* A field whose type is a plain value (`String`, `int`, `LocalDate`) is normally an **attribute**.
* A field whose type is **another class of your design** is normally a **line** to that class's box.
* Do not show it both ways. A `-LoanPeriod period` attribute **beside** a line to `LoanPeriod` says one thing twice.

---

## Reading Multiplicity

* The number at each end of a line is a **multiplicity**: how many objects take part.
* Stand at one class and read the number at the **far** end.
* That is how many objects of the far class **one object of your class** is linked to.

| Written | Means |
|---|---|
| `1` | exactly one |
| `0..1` | none or one |
| `0..*` | zero or more |
| `1..*` | one or more |

---

## Reading One Line in Both Directions

`ReservationCoordinator "1" --> "0..*" Reservation : stores`

* From the coordinator: **"each coordinator stores zero or more reservations."**
* From a reservation: **"each reservation is stored by exactly one coordinator."**
* The arrowhead shows **which object holds the reference**.

---

## Try It 1: The Other Two Lines

* Write one sentence for each of the other two lines in Figure 2.1, **reading from both ends**.
* For each number, find **where the Java code enforces it** and **where the model merely assumes it**.
* A strong answer separates "enforced by the code" from "true of how the code happens to be used".

---

## Try It 1: Answers (1 of 2)

| Line | Reading | Enforced by |
|---|---|---|
| Coordinator `1` to `1` Rules | Each coordinator uses one rules object; each rules object is used by one coordinator | `private final ReservationRules rules = new ReservationRules();` |
| Coordinator `1` to `0..*` Reservation | Each coordinator stores zero or more; each reservation is stored by one coordinator | The list starts empty and has no upper limit |

---

## Try It 1: Answers (2 of 2)

| Line | Reading | Enforced by |
|---|---|---|
| Reservation `0..*` to `1` LoanPeriod | Each reservation refers to exactly one period; a period may be referred to by any number of reservations | `requireNonNull(period, "period")` and the `final` field |

* **Only assumed:**
  * that a rules object is never shared,
  * that a reservation is held by only one coordinator (the constructor is public; snapshots hold the same objects),
  * the `0..*` on periods (nothing prevents sharing, though each reservation currently gets its own).

---

## The Relationships You Need to Read and Draw

<!--svg:ch02-notation-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 345" role="img" aria-label="The six relationships: association, dependency, aggregation, composition, inheritance and interface realisation, each drawn between two small boxes." style="display:block;width:100%;height:calc(var(--u) * 34.50);margin:0 auto">
<defs><marker id="ch02-notation-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-notation-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-notation-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-notation-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-notation-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<text x="10.0" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="start">Association</text>
<rect x="230.0" y="8.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="255.0" y="34.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">A</text>
<rect x="420.0" y="8.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="445.0" y="34.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">B</text>
<path d="M280.0,29.0 L420.0,29.0" fill="none" stroke="#1d588c" stroke-width="2.2"/>
<text x="500.0" y="35.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="start">Lasting link; arrowhead shows who holds it</text>
<text x="10.0" y="90.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="start">Dependency</text>
<rect x="230.0" y="63.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="255.0" y="89.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">A</text>
<rect x="420.0" y="63.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="445.0" y="89.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">B</text>
<path d="M280.0,84.0 L420.0,84.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-notation-open)"/>
<text x="500.0" y="90.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="start">Uses another class without keeping it</text>
<text x="10.0" y="145.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="start">Aggregation</text>
<rect x="230.0" y="118.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="255.0" y="144.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">A</text>
<rect x="420.0" y="118.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="445.0" y="144.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">B</text>
<path d="M280.0,139.0 L420.0,139.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch02-notation-dia)"/>
<text x="500.0" y="145.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="start">Whole groups parts that exist on their own</text>
<text x="10.0" y="200.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="start">Composition</text>
<rect x="230.0" y="173.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="255.0" y="199.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">A</text>
<rect x="420.0" y="173.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="445.0" y="199.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">B</text>
<path d="M280.0,194.0 L420.0,194.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch02-notation-diaf)"/>
<text x="500.0" y="200.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="start">Whole owns parts that need it to exist</text>
<text x="10.0" y="255.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="start">Inheritance</text>
<rect x="230.0" y="228.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="255.0" y="254.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">A</text>
<rect x="420.0" y="228.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="445.0" y="254.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">B</text>
<path d="M280.0,249.0 L420.0,249.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-notation-tri)"/>
<text x="500.0" y="255.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="start">Subclass is a kind of the superclass</text>
<text x="10.0" y="310.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="start">Realisation</text>
<rect x="230.0" y="283.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="255.0" y="309.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">A</text>
<rect x="420.0" y="283.0" width="50.0" height="42.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="445.0" y="309.8" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">B</text>
<path d="M280.0,304.0 L420.0,304.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-notation-tri)"/>
<text x="500.0" y="310.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="start">Class implements the interface's contract</text>
</svg>
</div>
<!--/svg-->

---

## Relationships: When to Use Each (1 of 2)

| Relationship | Read it as | Use it when |
|---|---|---|
| Association | One object is linked to another | The link is structural and lasting |
| Dependency | One class uses another without keeping it | A parameter or brief call is the only link |
| Aggregation | A whole groups parts that can exist without it | Parts can be shared or removed and still exist |

---

## Relationships: When to Use Each (2 of 2)

| Relationship | Read it as | Use it when |
|---|---|---|
| Composition | A whole owns parts with no meaning without it | A part's lifetime is tied to its owner |
| Inheritance | The subclass is a kind of the superclass | A real subtype relationship holds |
| Interface realisation | The class implements the interface's contract | Several classes satisfy one contract callers rely on |

---

## Figure 2.2: A Notation Sampler

<!--svg:ch02-fig22-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 372" role="img" aria-label="Figure 2.2, a notation sampler: a Pack contains Pages (composition), collects Articles (aggregation) and uses a Printer (dependency); Articles and Authors are associated; ResearchArticle extends Article; PdfPrinter implements Printer." style="display:block;width:100%;height:calc(var(--u) * 37.20);margin:0 auto">
<defs><marker id="ch02-fig22-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig22-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig22-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig22-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig22-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="19.0" width="309.0" height="106.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,55.0 L12.0,25.0 Q12.0,21.0 16.0,21.0 L313.0,21.0 Q317.0,21.0 317.0,25.0 L317.0,55.0 Z" fill="#e6eef6"/>
<text x="164.5" y="44.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Pack</text>
<line x1="10.0" y1="55.0" x2="319.0" y2="55.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="77.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String title</text>
<line x1="10.0" y1="90.0" x2="319.0" y2="90.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="112.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+print(Printer printer) String</text>
<rect x="10.0" y="179.0" width="346.2" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,235.0 L12.0,185.0 Q12.0,181.0 16.0,181.0 L350.2,181.0 Q354.2,181.0 354.2,185.0 L354.2,235.0 Z" fill="#e6eef6"/>
<text x="183.1" y="198.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="183.1" y="220.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Printer</text>
<line x1="10.0" y1="235.0" x2="356.2" y2="235.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="257.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+render(List&lt;String&gt; lines) String</text>
<rect x="10.0" y="316.0" width="190.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,352.0 L12.0,322.0 Q12.0,318.0 16.0,318.0 L194.0,318.0 Q198.0,318.0 198.0,322.0 L198.0,352.0 Z" fill="#e6eef6"/>
<text x="105.0" y="341.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">PdfPrinter</text>
<rect x="440.0" y="19.0" width="150.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M442.0,55.0 L442.0,25.0 Q442.0,21.0 446.0,21.0 L584.0,21.0 Q588.0,21.0 588.0,25.0 L588.0,55.0 Z" fill="#e6eef6"/>
<text x="515.0" y="44.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Page</text>
<rect x="440.0" y="144.0" width="150.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M442.0,180.0 L442.0,150.0 Q442.0,146.0 446.0,146.0 L584.0,146.0 Q588.0,146.0 588.0,150.0 L588.0,180.0 Z" fill="#e6eef6"/>
<text x="515.0" y="169.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Article</text>
<rect x="440.0" y="269.0" width="210.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M442.0,305.0 L442.0,275.0 Q442.0,271.0 446.0,271.0 L644.0,271.0 Q648.0,271.0 648.0,275.0 L648.0,305.0 Z" fill="#e6eef6"/>
<text x="545.0" y="294.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ResearchArticle</text>
<rect x="710.0" y="144.0" width="150.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M712.0,180.0 L712.0,150.0 Q712.0,146.0 716.0,146.0 L854.0,146.0 Q858.0,146.0 858.0,150.0 L858.0,180.0 Z" fill="#e6eef6"/>
<text x="785.0" y="169.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Author</text>
<path d="M319.0,37.0 L440.0,37.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch02-fig22-diaf)"/>
<text x="346.0" y="58.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="413.0" y="58.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1..*</text>
<text x="379.5" y="23.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">contains</text>
<path d="M319.0,104.0 L385.0,104.0 L385.0,162.0 L440.0,162.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch02-fig22-dia)"/>
<text x="346.0" y="125.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="413.0" y="183.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1..*</text>
<text x="403.0" y="138.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">collects</text>
<path d="M590.0,162.0 L710.0,162.0" fill="none" stroke="#1d588c" stroke-width="2.2"/>
<text x="617.0" y="183.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1..*</text>
<text x="683.0" y="183.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1..*</text>
<text x="650.0" y="148.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">written by</text>
<path d="M520.0,269.0 L520.0,180.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-fig22-tri)"/>
<text x="502.0" y="229.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="end" font-style="italic">extends</text>
<path d="M100.0,125.0 L100.0,179.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-fig22-open)"/>
<text x="118.0" y="157.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">uses</text>
<path d="M100.0,316.0 L100.0,270.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-fig22-tri)"/>
<text x="82.0" y="298.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="end" font-style="italic">implements</text>
</svg>
</div>
<!--/svg-->

---

## Reading the Sampler

* A pack **owns** its pages: a page has no meaning without its pack (**composition**).
* A pack only **collects** articles, which exist independently and can appear in many packs (**aggregation**).
* Articles and authors: a **plain association**, no arrowheads, because the description does not say who holds the reference.
* This is a notation sampler for a course-pack printing service. It is **not** part of the reservation project.

---

## Reading the Sampler, Continued

* A research article is **a kind of** article (**inheritance**).
* A pack uses a printer **only while printing** (**dependency**).
* `PdfPrinter` **implements** the `Printer` interface (**realisation**).

---

## Choosing a Relationship by Meaning

Choose by what it **means**, not how it looks. For each pair of classes, ask in order:

1. Does one class implement a contract that other classes rely on? **Realisation.**
2. Is A a kind of B, so a client of B could be handed an A without noticing? **Inheritance** (Chapter 5 tests this with the Liskov Substitution Principle).
3. Does A keep a lasting reference to B in a field? If not, and A only uses B as a parameter, local variable or short-lived object: **dependency**.

---

## Choosing a Relationship, Continued

4. If A keeps the reference, does B belong to A so completely that it has **no meaning without A** and is **discarded with it**? **Composition.**
5. Does A group Bs that exist independently and could be shared or removed? **Aggregation**, but only if you can say what the grouping adds. Otherwise a plain **association**.

---

## Aggregation and Composition Are Claims

* Aggregation is often **indistinguishable from association in code**.
* Composition describes a **lifetime the Java types do not enforce**.
* Both are **claims about meaning**.
* Figure 2.1 uses plain associations: periods can be shared by reference, and the code enforces no lifetime.
* Do not confuse "composition" as a programming idea (building from collaborators) with the **filled diamond**, a stronger ownership claim.

---

## From Code to Diagram (1 of 2)

| In the Java source | In the diagram |
|---|---|
| `private final LocalDate start;` | Attribute `-LocalDate start` |
| `private final List<Reservation> reservations` | Association to `Reservation`, `0..*` at that end |
| `private final ReservationRules rules` | Association to `ReservationRules`, `1` at that end |
| A parameter, local variable or `new X()` used only inside a method | Dependency on `X` |

---

## From Code to Diagram (2 of 2)

| In the Java source | In the diagram |
|---|---|
| `class A extends B` | Inheritance, triangle at `B` |
| `class A implements I` | Realisation, triangle at `I` |
| `public` and `private` | `+` and `-` |

* **Caution 1:** the Java type does not settle the meaning. A `List<Reservation>` might be an association or a composition. Only the design decides.
* **Caution 2:** a field that can be `null` is `0..1`, not `1`.

---

## A Worked Example: From Scenario to Diagram

The workshop keeps tools in numbered lockers.

* A locker holds **at most one tool**, and a tool sits in **at most one locker**.
* A technician looks after **any number of lockers**; each locker has **exactly one technician at a time**, and can be reassigned.
* Every inspection of a locker is logged as an **entry** with a date and a note; an entry is **meaningless without its locker**.
* Reports are printed as **plain text now**; other formats are expected later.

---

## Steps 1 and 2: Nouns, Then Classes

* **Step 1: find the nouns.** Workshop, tools, lockers, technician, inspection, entry, date, note, report, plain text, formats.
* **Step 2: decide which become classes.** Keep a noun as a class when it has **data or rules the description needs**.
* The table on the next slides records each decision and its reason.

---

## Step 2: Candidates and Decisions (1 of 2)

| Candidate | Decision | Reason |
|---|---|---|
| Workshop | Leave out | The whole system; no behaviour described for it |
| Locker | Class | Has a number, a log and a report |
| Tool | Class | A locker holds one |
| Technician | Class | Looks after lockers |

---

## Step 2: Candidates and Decisions (2 of 2)

| Candidate | Decision | Reason |
|---|---|---|
| Inspection entry | Class | Has a date and a note; belongs to a locker |
| Date, note, number, name | Attributes | Plain values describing a class |
| Report | Operation of `Locker` | Something a locker does, not a thing with its own data |
| Plain text, other formats | `ReportPrinter` interface and `PlainTextPrinter` class | The format is expected to vary |

---

## Step 3: Attributes and Operations

* Separate **what the description states** from **what you assume**.
* Stated: a locker's number and report; an entry's date and note.
* Assumptions, which you should **label as assumptions**:
  * a technician's name and a tool's name as identifying attributes,
  * a single `print` operation on the printer, one reasonable way to give the report a format-independent contract.
* A different, justified choice is acceptable.

---

## Step 4: Choose a Relationship for Each Pair

| Pair | What decides it | Result |
|---|---|---|
| Technician and locker | Neither owns the other; a locker can be reassigned | Plain association |
| Locker and tool | Neither is part of the other | Plain association |
| Locker and inspection entry | An entry is meaningless without its locker | Composition, diamond at `Locker` |
| Locker and `ReportPrinter` | A locker uses a printer only while reporting | Dependency |
| `PlainTextPrinter` and `ReportPrinter` | The class implements the contract | Realisation |

---

## Step 5: Write Each Multiplicity as a Sentence

* Each locker is looked after by **exactly one** technician: `1` at the `Technician` end.
* A technician looks after **any number** of lockers: `0..*` at the `Locker` end.
* A locker holds **at most one** tool and a tool sits in **at most one** locker: `0..1` at both ends.
* A locker has **any number of entries**; an entry belongs to **exactly one** locker.

---

## Step 6: Read It Aloud and Delete

* Read every line in **both directions** against the description.
* **Remove anything the description does not say.**
* Then compare with the model on the next slide: ask why each line differs, not whether it matches.

---

## Figure 2.3: The Resulting Model

<!--svg:ch02-fig23-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 382" role="img" aria-label="Figure 2.3, the corrected workshop model: a Technician looks after many Lockers; a Locker holds at most one Tool; a Locker owns its InspectionEntries (composition); a Locker uses the ReportPrinter interface, which PlainTextPrinter implements." style="display:block;width:100%;height:calc(var(--u) * 38.20);margin:0 auto">
<defs><marker id="ch02-fig23-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig23-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig23-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig23-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig23-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="5.0" y="10.0" width="150.0" height="71.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M7.0,46.0 L7.0,16.0 Q7.0,12.0 11.0,12.0 L149.0,12.0 Q153.0,12.0 153.0,16.0 L153.0,46.0 Z" fill="#e6eef6"/>
<text x="80.0" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Technician</text>
<line x1="5.0" y1="46.0" x2="155.0" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="17.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String name</text>
<rect x="270.0" y="10.0" width="225.3" height="129.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M272.0,46.0 L272.0,16.0 Q272.0,12.0 276.0,12.0 L489.3,12.0 Q493.3,12.0 493.3,16.0 L493.3,46.0 Z" fill="#e6eef6"/>
<text x="382.6" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Locker</text>
<line x1="270.0" y1="46.0" x2="495.3" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="282.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-int number</text>
<line x1="270.0" y1="81.0" x2="495.3" y2="81.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="282.0" y="103.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+report(ReportPrinter</text>
<text x="282.0" y="126.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">   printer) String</text>
<rect x="700.0" y="10.0" width="130.0" height="71.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M702.0,46.0 L702.0,16.0 Q702.0,12.0 706.0,12.0 L824.0,12.0 Q828.0,12.0 828.0,16.0 L828.0,46.0 Z" fill="#e6eef6"/>
<text x="765.0" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Tool</text>
<line x1="700.0" y1="46.0" x2="830.0" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="712.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String name</text>
<rect x="270.0" y="215.0" width="204.4" height="94.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M272.0,251.0 L272.0,221.0 Q272.0,217.0 276.0,217.0 L468.4,217.0 Q472.4,217.0 472.4,221.0 L472.4,251.0 Z" fill="#e6eef6"/>
<text x="372.2" y="240.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">InspectionEntry</text>
<line x1="270.0" y1="251.0" x2="474.4" y2="251.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="282.0" y="273.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-LocalDate date</text>
<text x="282.0" y="296.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String note</text>
<rect x="480.0" y="215.0" width="336.9" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M482.0,271.0 L482.0,221.0 Q482.0,217.0 486.0,217.0 L810.9,217.0 Q814.9,217.0 814.9,221.0 L814.9,271.0 Z" fill="#e6eef6"/>
<text x="648.5" y="234.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="648.5" y="256.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReportPrinter</text>
<line x1="480.0" y1="271.0" x2="816.9" y2="271.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="492.0" y="293.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+print(List&lt;String&gt; lines) String</text>
<rect x="560.0" y="335.0" width="220.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M562.0,371.0 L562.0,341.0 Q562.0,337.0 566.0,337.0 L774.0,337.0 Q778.0,337.0 778.0,341.0 L778.0,371.0 Z" fill="#e6eef6"/>
<text x="670.0" y="360.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">PlainTextPrinter</text>
<path d="M155.0,45.0 L270.0,45.0" fill="none" stroke="#1d588c" stroke-width="2.2"/>
<text x="182.0" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="243.0" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="212.5" y="31.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">looks after</text>
<path d="M495.3,45.0 L700.0,45.0" fill="none" stroke="#1d588c" stroke-width="2.2"/>
<text x="522.3" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..1</text>
<text x="673.0" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..1</text>
<text x="597.6" y="31.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">holds</text>
<path d="M340.0,139.0 L340.0,215.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch02-fig23-diaf)"/>
<text x="324.0" y="171.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="324.0" y="193.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="358.0" y="182.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">logs</text>
<path d="M490.0,139.0 L490.0,215.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-fig23-open)"/>
<text x="508.0" y="182.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">uses</text>
<path d="M680.0,335.0 L680.0,306.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-fig23-tri)"/>
<text x="662.0" y="325.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="end" font-style="italic">implements</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 2.3

* The two plain associations have **no arrowheads**: the description does not say which object holds the reference.
* A model should record **what the description says and no more**.
* Other answers are defensible: `Tool` only as an attribute, or a `Workshop` class if the task were scheduling.

---

## Checking a Diagram Against the Code

A diagram that disagrees with its code is **worse than no diagram**, because readers trust it.

* For every **box**, find the class. For every **attribute**, find the field with that name and type.
* For every **line**, find the field, parameter or `extends`/`implements` clause that creates it. If you cannot, remove the line or fix the code.

---

## Checking Multiplicities and Omissions

* For every **multiplicity**, find where the code enforces it: a constructor check, a `final` field, a collection type. If nothing does, **mark it as an assumption**.
* **List what the diagram leaves out**, and decide whether each omission is deliberate.

---

## Try It 2: What Figure 2.1 Leaves Out

* Find **two details** present in the Java but absent from Figure 2.1.
* Say **why leaving each out is acceptable**.
* Examples of acceptable answers: the constructors and their validation; the accessors `id()`, `borrowerId()`, `itemId()`; the `period` field (the association line already says it); the private `reservations` and `rules` fields; the order of the checks and the exceptions thrown.

---

## What the Diagram Cannot Tell You

* It omits standard library classes and some accessors.
* It does **not** establish the order of operations, display every validation, or prove overlapping bookings are rejected.
* Read the **method body** and the **period convention** for those questions.
* After extracting a private formatting method, **the relationships in Figure 2.1 are unchanged**: useful evidence about the scale of the edit.

---

## Spot the Errors: Figure 2.4

<!--svg:ch02-fig24-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 375" role="img" aria-label="Figure 2.4, a flawed attempt at the workshop model, for diagnosis: a locker attribute in Technician, a composition with reversed multiplicities from Technician to Locker, inheritance from Locker to InspectionEntry, a dependency on the concrete PlainTextPrinter, and a solid inheritance line for the interface." style="display:block;width:100%;height:calc(var(--u) * 37.50);margin:0 auto">
<defs><marker id="ch02-fig24-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig24-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig24-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig24-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-fig24-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="5.0" y="10.0" width="150.0" height="94.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M7.0,46.0 L7.0,16.0 Q7.0,12.0 11.0,12.0 L149.0,12.0 Q153.0,12.0 153.0,16.0 L153.0,46.0 Z" fill="#e6eef6"/>
<text x="80.0" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Technician</text>
<line x1="5.0" y1="46.0" x2="155.0" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="17.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String name</text>
<text x="17.0" y="91.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-Locker locker</text>
<rect x="270.0" y="10.0" width="253.2" height="129.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M272.0,46.0 L272.0,16.0 Q272.0,12.0 276.0,12.0 L517.2,12.0 Q521.2,12.0 521.2,16.0 L521.2,46.0 Z" fill="#e6eef6"/>
<text x="396.6" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Locker</text>
<line x1="270.0" y1="46.0" x2="523.2" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="282.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-int number</text>
<line x1="270.0" y1="81.0" x2="523.2" y2="81.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="282.0" y="103.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+report(PlainTextPrinter</text>
<text x="282.0" y="126.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">   printer) String</text>
<rect x="700.0" y="10.0" width="130.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M702.0,46.0 L702.0,16.0 Q702.0,12.0 706.0,12.0 L824.0,12.0 Q828.0,12.0 828.0,16.0 L828.0,46.0 Z" fill="#e6eef6"/>
<text x="765.0" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Tool</text>
<rect x="270.0" y="200.0" width="200.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M272.0,236.0 L272.0,206.0 Q272.0,202.0 276.0,202.0 L464.0,202.0 Q468.0,202.0 468.0,206.0 L468.0,236.0 Z" fill="#e6eef6"/>
<text x="370.0" y="225.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">InspectionEntry</text>
<rect x="500.0" y="200.0" width="220.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M502.0,236.0 L502.0,206.0 Q502.0,202.0 506.0,202.0 L714.0,202.0 Q718.0,202.0 718.0,206.0 L718.0,236.0 Z" fill="#e6eef6"/>
<text x="610.0" y="225.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">PlainTextPrinter</text>
<rect x="500.0" y="282.0" width="336.9" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M502.0,338.0 L502.0,288.0 Q502.0,284.0 506.0,284.0 L830.9,284.0 Q834.9,284.0 834.9,288.0 L834.9,338.0 Z" fill="#e6eef6"/>
<text x="668.5" y="301.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="668.5" y="323.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReportPrinter</text>
<line x1="500.0" y1="338.0" x2="836.9" y2="338.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="512.0" y="360.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+print(List&lt;String&gt; lines) String</text>
<path d="M155.0,45.0 L270.0,45.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch02-fig24-diaf)"/>
<text x="182.0" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="243.0" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="212.5" y="31.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">looks after</text>
<path d="M523.2,45.0 L700.0,45.0" fill="none" stroke="#1d588c" stroke-width="2.2"/>
<text x="550.2" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..1</text>
<text x="673.0" y="66.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..1</text>
<text x="611.6" y="31.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">holds</text>
<path d="M340.0,200.0 L340.0,139.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-fig24-tri)"/>
<text x="322.0" y="174.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="end" font-style="italic">logs</text>
<path d="M510.0,139.0 L510.0,200.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-fig24-open)"/>
<text x="528.0" y="174.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">uses</text>
<path d="M610.0,236.0 L610.0,282.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-fig24-tri)"/>
</svg>
</div>
<!--/svg-->

---

## Try It 3

* Another student's first attempt at the workshop model (Figure 2.4) contains at least **five mistakes**.
* List every mistake you can find.
* For each, say **why it is wrong** using the description.
* Say what the **correct notation** is.
* Then **redraw** the diagram.

---

## Try It 3: Answers (1 of 2)

| # | Mistake | Why it is wrong |
|---|---|---|
| 1 | `-Locker locker` attribute in `Technician` | Repeats the line; implies one locker per technician |
| 2 | Multiplicities reversed on `Technician` to `Locker` | Says each locker has many technicians and each technician one locker |
| 3 | Filled diamond at `Technician` | Claims lockers die with their technician, but a locker can be reassigned |

---

## Try It 3: Answers (2 of 2)

| # | Mistake | Correct notation |
|---|---|---|
| 4 | `Locker <\|-- InspectionEntry` | Composition: filled diamond at `Locker`, `1` and `0..*` |
| 5 | `Locker ..> PlainTextPrinter` and `report(PlainTextPrinter printer)` | Depend on `ReportPrinter`; type the parameter as `ReportPrinter` |
| 6 | `ReportPrinter <\|-- PlainTextPrinter` | Dashed line, hollow triangle at `ReportPrinter` |

* Mistakes 2 and 3 sit on the same line. Count them as two ideas if both are explained.

---

## Common Drawing Mistakes (1 of 3)

| Mistake | Why it is wrong | Better habit |
|---|---|---|
| Multiplicity at the wrong end | The far number counts the far class; reversed numbers say the opposite | Read every line aloud in both directions |
| Arrowhead as ownership | An arrowhead shows who holds the reference, not who owns whom | Use diamonds, with a reason, for ownership |
| Inheritance for "uses" or "has" | A locker is not a kind of technician; an entry is not a kind of locker | Test "A is a kind of B" and its promises |

---

## Common Drawing Mistakes (2 of 3)

| Mistake | Why it is wrong | Better habit |
|---|---|---|
| Solid line for realisation | Realisation is dashed; solid with a triangle is inheritance | Check the line style of every triangle |
| Filled diamond because the field is `final` | Composition claims a lifetime; `final` only fixes a reference | Ask whether the part can exist without the owner |
| Showing a relationship twice | `-Locker locker` plus a line to `Locker` repeats one fact | Show a field of a design class as a line only |

---

## Common Drawing Mistakes (3 of 3)

| Mistake | Why it is wrong | Better habit |
|---|---|---|
| Depending on a concrete class when an interface exists | A client naming `PlainTextPrinter` cannot accept another format | Point the dependency at the interface |
| Drawing every class and member | The design question disappears among the detail | One diagram, one question, only the members it needs |
| A diagram that disagrees with the code | Readers trust the diagram | Run the checking steps before sharing it |

---

# 2.7 Git History, Branches and Review
### A change a team can inspect

---

## Version Control Is Not Evidence of Good Design

* A codebase becomes a shared engineering artefact when the team can **inspect its changes, reproduce its behaviour and explain its decisions**.
* Version control supports that work.
* A commit **alone** is not evidence of a good design.

---

## Working Files, Staging, Commits

<!--svg:ch02-git-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 250" role="img" aria-label="Working files are staged with git add, then recorded with git commit. git diff compares working files with the staging area; git diff --staged compares the staging area with the last commit." style="display:block;width:100%;height:calc(var(--u) * 25.00);margin:0 auto">
<defs><marker id="ch02-git-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-git-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-git-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-git-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-git-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="15.0" y="30.0" width="220.0" height="76.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="125.0" y="62.6" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Working files</text>
<text x="125.0" y="86.3" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">(what you edit)</text>
<rect x="325.0" y="30.0" width="220.0" height="76.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="435.0" y="62.6" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Staging area</text>
<text x="435.0" y="86.3" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">(the next commit)</text>
<rect x="635.0" y="30.0" width="220.0" height="76.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="745.0" y="62.6" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">Recorded commits</text>
<text x="745.0" y="86.3" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">(history)</text>
<path d="M235.0,68.0 L325.0,68.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-git-arr)"/>
<text x="280.0" y="62.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">git add</text>
<path d="M545.0,68.0 L635.0,68.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch02-git-arr)"/>
<text x="590.0" y="62.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">git commit</text>
<path d="M125.0,106.0 L125.0,150.0 L435.0,150.0 L435.0,106.0" fill="none" stroke="#1d588c" stroke-width="1.8" stroke-dasharray="3 5"/>
<text x="280.0" y="142.0" font-size="17" font-family="'Plex Mono', monospace" font-weight="600" fill="#1d588c" text-anchor="middle">git diff</text>
<path d="M435.0,106.0 L435.0,200.0 L745.0,200.0 L745.0,106.0" fill="none" stroke="#1d588c" stroke-width="1.8" stroke-dasharray="3 5"/>
<text x="590.0" y="192.0" font-size="17" font-family="'Plex Mono', monospace" font-weight="600" fill="#1d588c" text-anchor="middle">git diff --staged</text>
<text x="435.0" y="240.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Edit, stage the exact change, inspect it, then record it.</text>
</svg>
</div>
<!--/svg-->

---

## Why the Staging Area Matters

* You edit **working files**, select content for the next commit, and **record that selected state**.
* The staging area matters when **unrelated edits** are present.
* The next commit should contain **the change you intend to explain**.

---

## Branches and Pull Requests

* A **branch** names a line of development. For the lab, use a **short-lived branch** containing the confirmation extraction.
* A **pull request** (or merge request) is a hosting-platform **review proposal**. It is **not** the same as a local commit.
* A local peer review can still serve the learning objective when no hosting account is available.

---

## Trunk-Based or Feature Branches?

* **Trunk-based development:** integrate small changes frequently into a main line, sometimes through very short-lived branches.
* **Feature-branch workflow:** group a feature's work on a branch before integration.
* The approaches overlap: a short reviewed branch can be part of frequent integration.
* For this course: keep changes **small, reviewable and integrated regularly**.

---

## A Reviewable Change: The Sequence

1. Begin with the supplied starting files and a **recorded baseline**.
2. Confirm that the **checks pass before editing**.
3. Create a **branch**.
4. Perform **only the extraction**.
5. **Rerun the checks** and inspect the diff.

* The companion contains the complete setup commands.

---

## The Inspection Commands

```sh
git status
git diff
git diff --staged
```

* `git status` reports file state.
* `git diff` normally shows **tracked changes not yet staged**.
* `git diff --staged` shows **staged changes** against the current commit.

---

## Reading the Output Correctly

* An **empty** `git diff` after staging does **not** mean there is nothing to commit.
* **Untracked files** also need attention in `git status`.
* Keep compiled class files out of commits: the companion's `.gitignore` handles generated files.
* Appendix B collects the Git commands and the pull-request workflow (B.8).

---

## Commit Messages

* A useful message: `Extract reservation confirmation formatting`.
* Many teams adopt a written convention. Conventional Commits puts a **type** before a short description:
  `refactor: extract reservation confirmation formatting`
* Use whichever convention your team agrees, and **apply it consistently**.

---

## A Useful Review Description

* State **the problem**, **the limited change**, and **the checks performed**.
* Example: "The request method interleaves storage and confirmation text. This change moves the text assembly into a private helper. The existing messages and stored records remain unchanged in the supplied checks."
* Add **limits**: persistence, concurrent booking, lifecycle operations and message delivery remain outside this checkpoint.

---

## What the Reviewer Inspects

* Inspect the **diff**.
* Verify that the helper **adds no state changes**.
* Check that the record is **still added before** confirmation is returned.
* "Looks cleaner" is weaker than an explanation of **what was inspected and why it matters**.

---

## A Diff With Only Additions Still Moves Behaviour

* In Git, the extraction appears as **four added lines and no removed lines**.
* The existing `return "Confirmed: "...` expression is kept and now sits inside the new method.
* The reviewer must read **where the retained lines ended up**.

---

## One Change at a Time

* Do not combine this refactoring with **changed limits**, **renamed identifiers** or **new message punctuation**.
* Each may be legitimate work.
* Combining them makes it harder to determine **why a result changed**.

---

# 2.8 AI in Practice: Tracing a Coordinator
### Classifying claims against the code

---

## Activity Frame (1 of 2)

| Element | For this activity |
|---|---|
| Engineering objective | Compare an explanation of the coordinator with its actual control flow, state changes and side effects |
| Input | The complete starting `ReservationCoordinator` and collaborators |
| Permitted scope | Judge the explanation only; do not change the code |

---

## Activity Frame (2 of 2)

| Element | For this activity |
|---|---|
| Independent checks | Tracing the code, the three-request demonstration, the supplied checks |
| Accept or reject | Keep supported claims, reject contradicted ones, mark claims the code does not establish |
| No-account route | The fixture is sufficient |

* Chapter 15 collects the recurring AI workflows. This activity is **self-contained**.

---

## The Teaching Fixture (1 of 2)

An **author-written teaching fixture** imitating a plausible AI explanation. Not a captured response from a real model.

> The coordinator validates identifiers, counts the borrower's stored reservations and checks the numeric rule. It tests availability using existing reservations for the same item. On success, it adds a reservation before returning a confirmation.

---

## The Teaching Fixture (2 of 2)

> It sends that confirmation by email and persists the reservation to a database. Because the list field is final, callers receive a deeply immutable copy and booking is safe under concurrent requests.

* Classify each claim as **supported, contradicted or not established**.
* Cite the relevant operation, **or the absence of one**.

---

## Claim Classification (1 of 2)

| Claim | Judgement | Evidence |
|---|---|---|
| Validates identifiers | Supported within scope | Rejects null or blank identifiers; no catalogue check |
| Counts the borrower's stored reservations | Supported | Loops over records, compares borrower identifiers |
| Applies the numeric rule | Supported | Calls `ReservationRules.mayRequest` |
| Checks conflicts for the same item | Supported | Matching item and overlapping period |

---

## Claim Classification (2 of 2)

| Claim | Judgement | Evidence |
|---|---|---|
| Adds before returning a confirmation | Supported | `add` is called before the message is built |
| Sends email | **Contradicted** | No sender or delivery call; the method returns a string |
| Persists to a database | **Contradicted** | An in-memory `ArrayList`; no database operation |
| Final list: callers get a deeply immutable copy | **Incorrect** | `final` stops reassignment; `List.copyOf` is shallow |
| Concurrent booking is safe | **Not established** | Check and add are not one synchronised operation |

---

## A Corrected Four-Sentence Explanation

> The coordinator rejects missing or blank identifiers and requires a start date, then counts the borrower's stored records and applies the numeric rule. It checks overlapping periods for the same item before recording a successful reservation and returning confirmation text.

---

## A Corrected Four-Sentence Explanation, Continued

> Policy and availability rejections do not add a record, and the returned reservation list is an unmodifiable snapshot containing immutable elements. The implementation has in-memory storage only, sends no email, and is intended for sequential use rather than concurrent booking.

---

## Optional Live Assistant

> Trace this coordinator and its supplied collaborators. Identify inputs, returned values and state changes on success and rejection. State what is established about storage, notifications and concurrency. Separate facts visible in the code from assumptions. Do not change the code.

* Record **one accepted claim** and **one rejected or qualified claim** with evidence.
* A second model's agreement is **not** a substitute for tracing the operations.

---

# 2.9 Common Mistakes
### Eight misconceptions, eight better questions

---

## Mistakes 1 and 2

* **"Private fields mean the object is safely encapsulated."**
  * A returned mutable list can still expose a modification path.
  * *Better question:* what can callers change through the references they receive?
* **"A final field makes the referenced object immutable."**
  * The coordinator can still add to its final list.
  * *Better question:* is the reference fixed, the object immutable, or both?

---

## Mistakes 3 and 4

* **"Every noun should immediately become a class."**
  * Several concepts have no behaviour or state we need yet.
  * *Better question:* what responsibility would that class own now?
* **"More interfaces automatically mean less harmful coupling."**
  * An interface can repeat an unstable contract without solving a caller's problem.
  * *Better question:* which dependency would this interface improve?

---

## Mistakes 5 and 6

* **"Calling another class means inheriting from it."**
  * The coordinator uses a policy; it is not a policy subtype.
  * *Better question:* is the relationship use, containment or substitution?
* **"A filled diamond just means 'has a'."**
  * Composition claims the part cannot outlive its owner; `LoanPeriod` objects can be shared by reference.
  * *Better question:* does the code enforce this lifetime, and would the domain agree?

---

## Mistakes 7 and 8

* **"A formatting refactoring fixes the whole design."**
  * The helper leaves storage and other responsibilities in the coordinator.
  * *Better question:* which improvement did this edit actually make?
* **"Green checks prove the application is production-ready."**
  * The starter omits lifecycle, persistence, catalogue validation and concurrency.
  * *Better question:* which claims have we tested, under which assumptions?

---

# 2.10 Practical Activity: One Checked Design Improvement
### Parts A to D

---

## Inputs and Starting Point

* Parts A to C use the **Book project**; Part D concerns your **Team project**.
* Use the companion's common source files and the **starting** `ReservationCoordinator.java`.
* Save all **six Java files in one directory**; compile and run them using the companion's instructions.
* The check runner should report **34 passing checks** before you begin.
* Read the checks as **provided evidence**. You need not master the runner yet.

---

## Compile and Run

```sh
javac --release 17 -d out ReservationRules.java LoanPeriod.java \
    Reservation.java ReservationCoordinator.java \
    Chapter02Demo.java Chapter02Checks.java
java -cp out Chapter02Demo
java -cp out Chapter02Checks
```

* Recompile after every source change. Otherwise the JVM may run **old class files** and give misleading evidence.

---

## Expected Output

```text
Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Rejected: item unavailable.
Confirmed: R2 for B2 on CAM1 [2026-10-22, 2026-10-23).
Stored: 2
```

```text
All 34 chapter checks passed.
```

---

## Part A: Understand the Request

Trace the three requests in `Chapter02Demo`.

* Record the **returned message** and the **number of stored records** after each call.
* Identify the **first condition that rejects** the overlapping request.
* Explain why the **adjacent** request is accepted.
* Explain why the rejected request **does not consume a reservation identifier**.

---

## Part A: The Trace

| Call | Outcome | Stored | Important step |
|---|---|---:|---|
| B1 requests CAM1 from 20 Oct for two days | Confirmed as R1 | 1 | Empty history has no conflict |
| B2 requests CAM1 from 21 Oct for one day | Rejected: unavailable | 1 | Overlaps R1 for the same item |
| B2 requests CAM1 from 22 Oct for one day | Confirmed as R2 | 2 | Equality with R1's exclusive end is permitted |

* Identifiers derive from the **number of stored records**, so a rejection consumes none. That may not suit deletion, persistence or several coordinators.

---

## Part A: Diagram and Invariants

* Draw a small class diagram of the starter **without copying Figure 2.1**.
  * Use the "From code to diagram" table, then run the **four checking steps** on your own drawing.
* Annotate **one local invariant** and **one condition that needs information from multiple objects**.
* A local invariant: a period's end follows its start (the `LoanPeriod` constructor).
* A multi-object condition: confirmed reservations for the same item do not overlap (the coordinator checks it).

---

## Part A: A Separate Modelling Exercise

Equipment kits. It does **not** extend the project.

* A kit has a name and holds **one or more** equipment items.
* Removing a kit does **not** delete its items; an item belongs to **at most one** kit.
* Each item keeps **any number** of maintenance records; a record belongs to **exactly one** item and has no meaning without it.
* A kit summary is produced through an **exporter**: CSV now, other formats later.

---

## Part A: What to Draw

* A class diagram with the classes, their key attributes and multiplicities.
* Include **at least one aggregation, one composition, one interface realisation and one dependency**.
* State **one assumption** you had to make.
* For each relationship, write the **Section 2.6 question** that decided it.
* Then read every line aloud **in both directions** against the scenario.

---

## One Suitable Model: Equipment Kits

<!--svg:ch02-kit-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 372" role="img" aria-label="One suitable kit model: an EquipmentKit groups one or more EquipmentItems (aggregation, an item is in at most one kit); an EquipmentItem keeps zero or more MaintenanceRecords (composition); the kit uses the Exporter interface, which CsvExporter implements." style="display:block;width:100%;height:calc(var(--u) * 37.20);margin:0 auto">
<defs><marker id="ch02-kit-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-kit-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-kit-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-kit-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch02-kit-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="10.0" width="346.2" height="106.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,46.0 L12.0,16.0 Q12.0,12.0 16.0,12.0 L350.2,12.0 Q354.2,12.0 354.2,16.0 L354.2,46.0 Z" fill="#e6eef6"/>
<text x="183.1" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">EquipmentKit</text>
<line x1="10.0" y1="46.0" x2="356.2" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String name</text>
<line x1="10.0" y1="81.0" x2="356.2" y2="81.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="103.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+summary(Exporter exporter) String</text>
<rect x="470.0" y="10.0" width="181.1" height="71.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M472.0,46.0 L472.0,16.0 Q472.0,12.0 476.0,12.0 L645.1,12.0 Q649.1,12.0 649.1,16.0 L649.1,46.0 Z" fill="#e6eef6"/>
<text x="560.6" y="35.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">EquipmentItem</text>
<line x1="470.0" y1="46.0" x2="651.1" y2="46.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="482.0" y="68.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String itemId</text>
<rect x="425.0" y="200.0" width="234.6" height="94.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M427.0,236.0 L427.0,206.0 Q427.0,202.0 431.0,202.0 L653.6,202.0 Q657.6,202.0 657.6,206.0 L657.6,236.0 Z" fill="#e6eef6"/>
<text x="542.3" y="225.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">MaintenanceRecord</text>
<line x1="425.0" y1="236.0" x2="659.6" y2="236.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="437.0" y="258.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-LocalDate performedOn</text>
<text x="437.0" y="281.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-String note</text>
<rect x="10.0" y="190.0" width="346.2" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,246.0 L12.0,196.0 Q12.0,192.0 16.0,192.0 L350.2,192.0 Q354.2,192.0 354.2,196.0 L354.2,246.0 Z" fill="#e6eef6"/>
<text x="183.1" y="209.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="183.1" y="231.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Exporter</text>
<line x1="10.0" y1="246.0" x2="356.2" y2="246.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="268.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+format(List&lt;String&gt; lines) String</text>
<rect x="10.0" y="322.0" width="190.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,358.0 L12.0,328.0 Q12.0,324.0 16.0,324.0 L194.0,324.0 Q198.0,324.0 198.0,328.0 L198.0,358.0 Z" fill="#e6eef6"/>
<text x="105.0" y="347.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">CsvExporter</text>
<path d="M356.2,52.0 L470.0,52.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch02-kit-dia)"/>
<text x="383.2" y="73.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..1</text>
<text x="443.0" y="73.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1..*</text>
<text x="413.1" y="38.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">groups</text>
<path d="M540.0,81.0 L540.0,200.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-start="url(#ch02-kit-diaf)"/>
<text x="524.0" y="113.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">1</text>
<text x="524.0" y="178.0" font-size="16" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="middle">0..*</text>
<text x="558.0" y="145.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">keeps</text>
<path d="M100.0,116.0 L100.0,190.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-kit-open)"/>
<text x="118.0" y="158.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">uses</text>
<path d="M100.0,322.0 L100.0,281.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch02-kit-tri)"/>
<text x="82.0" y="306.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="end" font-style="italic">implements</text>
</svg>
</div>
<!--/svg-->

---

## What a Strong Kit Answer Shows

| Requirement | Model decision |
|---|---|
| A kit holds one or more items; removing it does not delete them | Aggregation, `1..*` at the items end |
| An item belongs to at most one kit | `0..1` at the kit end |
| A record belongs to exactly one item and has no meaning without it | Composition from item to record: `1` at the item, `0..*` at the records |
| A summary is produced through an exporter; other formats expected | `Exporter` interface realised by `CsvExporter`; the kit depends on the interface |

---

## Common Kit Errors

* Interface realisation drawn as inheritance with a **solid line**.
* The **diamond reversed**.
* `1..*` at the **wrong end**.
* The kit depending directly on `CsvExporter`.
* An assumption can be anything stated and consistent: for example, that an item with no kit is allowed.
* Do not credit extra classes for their own sake.

---

## Part B: Diagnose the Design

* Write a short **responsibility inventory** for the coordinator.
* Identify **two distinct reasons it might change**.
* Explain **one cohesive collaborator** and **one dependency that deserves attention**.
* Avoid judging quality by method length alone.

---

## Part B: A Model Answer

* The coordinator validates inputs, counts records, invokes policy, checks availability, allocates an identifier, stores a record and formats a message.
* Two reasons to change: a **new storage mechanism** and **changed confirmation wording**.
* `LoanPeriod` is cohesive: construction rules and overlap concern one concept.
* The coordinator depends on both **reservation representation** and **message wording**.

---

## Part C: Make the Change

* On a **short-lived branch**, move only the confirmation-string expression into a private `confirmationFor(Reservation reservation)` method.
* Keep unchanged: **output, validation order, identifier allocation, storage effects**.
* Do **not** add a new interface or change public method signatures.
* Run the checks again, inspect the diff, ask a peer to review.

---

## Part C: The Completed Method

```java
        reservations.add(reservation);
        return confirmationFor(reservation);
    }

    private String confirmationFor(Reservation reservation) {
        return "Confirmed: " + reservation.id()
                + " for " + reservation.borrowerId()
                + " on " + reservation.itemId()
                + " [" + reservation.period().start()
                + ", " + reservation.period().endExclusive() + ").";
    }
```

---

## Part C: Git Baseline Commands

```sh
git init -b main
git add .gitignore ReservationRules.java LoanPeriod.java \
    Reservation.java ReservationCoordinator.java \
    Chapter02Demo.java Chapter02Checks.java
git diff --staged
git commit -m "Add chapter 2 reservation starter"
git switch -c refactor/confirmation-text
```

* `.gitignore` contains `out/` and `*.class`.

---

## Part C: Commit the Extraction

```sh
git status
git diff
git add ReservationCoordinator.java
git diff --staged
git commit -m "Extract reservation confirmation formatting"
git log --oneline -2
git status
```

* Produce **one focused commit** after addressing relevant feedback.
* In independent study, perform a self-review and **label it honestly as such**.

---

## Part C: A Review Record

* **Problem:** the request method contains message formatting alongside the request workflow.
* **Change:** move only the confirmation-string construction into `confirmationFor`, keeping record creation and storage order.
* **Evidence:** identical demonstration output; the same 34 checks pass; the diff changes only internal organisation.
* **Limits:** persistence, concurrent booking, lifecycle operations and message delivery remain outside this checkpoint.

---

## Part C: What the Review Record Needs

* The change or **commit identifier**.
* The **reviewer**.
* The **evidence inspected**.
* The **findings** and the **response**.
* Creating a commit does **not** create a hosted pull request or establish that anyone reviewed it.
* Record your own observed results. Do not copy a claim you did not verify.

---

## Part D: Organise Collaboration

* Form teams of **three or four** as directed by the module leader.
* Confirm which provided **starter domain** your assessed project uses. If it is not equipment lending, use each chapter's transfer note.
* Set up an **issue board** with columns that match how your team will work.
* Add **three cards with concrete completion conditions**.

---

## Part D: Cards and Branch Policy

* A good card: "extract confirmation formatting with unchanged output and checks". Not: "improve OO".
* Agree a **branch policy**:
  * very short-lived branches integrated into a main line often, **or**
  * one feature branch per story.
* **Write down your reason.** The reason matters more than the choice.
* Agree who prepares the next demonstration and who reviews the next change. **Rotate roles**.

---

## Evidence to Retain

* The annotated **diagram** and the **scenario model**.
* The **responsibility diagnosis**.
* **Before-and-after check results**.
* The **commit identifier** and the **review note**.
* Your **AI claim analysis**.
* Your team's **issue board and branch-policy note**.
* A short **limitation statement**: which risks remain after the extraction?

---

## The Activity Is Complete When

* The **diagram matches the code**.
* The extraction **preserves the checked behaviour**.
* Your review explains **both the improvement and its limits**.
* You can explain the returned list's protection **without claiming all copies are deep copies**.

---

## Optional Investigation: Break It on Purpose

* In a **temporary copy**, replace `List.copyOf(reservations)` with `reservations`.
* **Predict** the effect of an external `clear()` call, then run the checks.
* Result: `snapshot::clear` succeeds; the runner reports that `snapshot unmodifiable` expected an `UnsupportedOperationException`.
* **Restore the original** before continuing. This is a fault demonstration, not an improvement.

---

## A Second Fault: Omit the Storage

* In another disposable copy, remove `reservations.add(reservation);`.
* The first confirmation can still look correct.
* The checks fail with **`one success stored`**.
* A demonstration that inspects only printed text would **miss the changed state**.

---

# 2.11 Review Questions and Transfer Challenge
### Concept, diagnosis, transfer

---

## Concept Questions

1. Distinguish a Java object reference from a reservation's domain identifier. Why are equal identifier strings not sufficient to make two `Reservation` instances equal through `equals` in this starter?
2. Explain one local invariant and one system-level condition in the project. Why do they need different enforcement points?
3. Explain cohesion and coupling using one likely change to the coordinator. Why is reducing the total number of dependencies not a sufficient design goal?
4. Compare composition and inheritance for a reservation and its loan period. What would inheritance incorrectly suggest?

---

## Diagnosis Questions

5. A developer adds a getter returning the private mutable list and claims the coordinator is still encapsulated because the field is private. Give a concrete counterexample and explain the limits of the proposed correction using `List.copyOf`.
6. A refactoring returns the same confirmation text but omits `reservations.add(reservation)`. The developer demonstrates the printed text and declares success. Explain the behavioural change and identify evidence that would expose it.

---

## Guidance: Questions 1 and 2

1. A reference identifies a **Java object instance**; `id` represents **domain identity** in the teaching model. Two separately constructed reservations can hold the same identifier text yet remain distinct under the inherited `equals`. Identifier-based equality needs an **explicit contract and implementation**.
2. `LoanPeriod` protects **its own date relationship**. Conflict prevention needs **other reservations and the requested item**, so it belongs at a boundary with that information.

---

## Guidance: Questions 3 and 4

3. Changed message wording affects presentation but currently requires **editing the coordinator**. A private helper makes the purpose easier to locate; it does not remove the class-level dependency. **Zero dependencies would prevent collaboration**; extra classes can add indirection without solving a problem.
4. A reservation **has** a period. It is not a period subtype. Inheriting would conflate reservation identity and borrower/item details with an interval, and **suggest inappropriate substitutability**. `LoanPeriod` is also `final`.

---

## Guidance: Questions 5 and 6

5. Returning the mutable internal list allows `clear` or `add` **outside the coordinator's validation**. `List.copyOf` blocks structural mutation and isolates later additions, but does **not** deep-copy mutable elements. This starter's elements are separately immutable.
6. A success string is returned for a reservation the coordinator **does not retain**. The next request can wrongly find no conflict. The **`one success stored`** check exposes the fault immediately.

---

## Transfer Challenge: Room Booking

A university room-booking coordinator stores bookings, checks room conflicts and constructs confirmation text. Its users now request a **wording change only**.

* Propose a responsibility diagram with **at most four** domain or application classes.
* State a **period convention**.
* Identify the **state that callers must not modify directly**.
* Describe **one small behaviour-preserving improvement** and **two before-and-after observations** to accept it.
* Include a brief review description and **one remaining limitation**.

---

## Transfer Challenge: Guidance

* One reasonable model: `RoomBookingCoordinator`, `RoomBooking`, `BookingPeriod`, `BookingRules`.
* State an explicit convention, for example start-inclusive, end-exclusive periods in local building time.
* **Extract first, change the wording second**: preserve the old output while extracting; then change the text as a separate behaviour change with updated expectations.
* Two observations: identical confirmation text and identical stored records; a conflicting request still adds nothing.
* A limitation: one process's list cannot coordinate several application instances.

---

# 2.12 Chapter Summary
### What to carry forward

---

## Summary: Objects as Design Units

* Objects become useful design units when their **responsibilities and permitted interactions are clear**.
* **Constructors and controlled operations** protect invariants.
* **Immutable values and careful collection access** stop callers bypassing intended boundaries.

---

## Summary: Cohesion, Coupling and the Limited Claim

* Cohesion and coupling help us discuss the **consequences of change**.
* The formatting extraction makes **one operation easier to follow** without resolving every responsibility the coordinator holds.
* **Explaining that limited improvement** is part of sound design reasoning.

---

## Summary: Evidence Should Agree

* Diagrams, checks, diffs and review notes describe **different aspects of the same codebase**.
* They should **agree with the implementation**.
* An AI explanation is **another candidate description** to check against that evidence.

---

## Next: Chapter 3

* **Chapter 3: Agile Development and the Nature of Change.**
* Turn project needs into an **ordered backlog**.
* Write useful **stories and acceptance criteria**.
* Examine how a team **plans and learns through feedback**.

---

## Sources and Further Reading

1. **Dev.java:** *Classes and Objects*; *Inheritance*.
2. **Oracle:** Java SE 17 API for `LocalDate`, `Objects` and `List`.
3. **Chacon and Straub:** *Pro Git*: Recording Changes; Branching Workflows.
4. **Git documentation:** `git diff` and `git switch`.
5. **Conventional Commits 1.0.0.**
6. **Martin, Robert C.:** *Agile Software Development: Principles, Patterns, and Practices*, 2002.

* Full references and links are in the chapter text.
