---
title: "Chapter 9: Designing Changing Behaviour"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 90
type: slides
layout: page
---

# Chapter 9: Designing Changing Behaviour
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **9.1 What changes, and why? Variation in behaviour**
  * Four questions for one domain: which rule, which action, who reacts, what request.
* **9.2 Strategy: swapping one rule for another**
  * Already present in the borrowing policies.
* **9.3 State: behaviour that depends on where you are in a lifecycle**
  * A transition table first, then two implementations.
* **9.4 Observer: telling interested parties without knowing who they are**
  * Order, subscription changes and failure, defined before dispatching.

---

## Chapter Roadmap (2 of 3)

* **9.5 Command: a request you can carry before running it**
  * A request as an object: when is it captured, and when do its effects happen?
* **9.6 Testing behaviour that patterns organise**
  * Let the requirement supply the expected result.
* **9.7 Choosing a pattern, and knowing its limits**
* **9.8 Strategy or State? Judging AI proposals** Strategy or State?

---

## Chapter Roadmap (3 of 3)

* **9.9 Behaviour-pattern habits that mislead**
* **9.10 Try it yourself: lifecycle, publisher and command**
  * Six steps; step 6 is on your team's project.
* **9.11 Questions to think with, and a transfer challenge**
  * A document workflow: draft, approved, published.
* **9.12 The critical book review**
  * The critical book review is due in Week 8.
* **What to take away, and what comes next**
  * Chapter 10: application structure and dependency direction.

---

## Learning Outcomes (1 of 2)

By the end of this chapter, you should be able to:

1. **Distinguish an interchangeable policy from lifecycle-dependent behaviour.**
2. **Explain and test Strategy selection** using the existing borrowing policies.
3. **Define a transition table** and implement a small State-based lifecycle.

---

## Learning Outcomes (2 of 2)

4. **Specify Observer ordering, subscription changes and failure behaviour.**
5. **Represent a request with Command** and explain execution-time side effects.
6. **Justify adopting or declining a pattern** using a concrete change and evidence.

---

## Module Connection and How to Use This Chapter

* Supports **LO2 and LO4**. Entry: Chapters 7 and 8.
* **Core reading:** 9.1 to 9.3, 9.6 and 9.7 (Strategy, State, testing, selection).
* **Working-knowledge reading:** 9.4 and 9.5 (Observer, Command): understand the structure, ordering and failure rules and cost; see each work in the examples; **you do not implement either on your own**.
* **Minimum lab:** steps 1 to 4 and 6. Steps 1 to 4: the book's project. **Step 6: your team's project.
* **If you want more:** the AI activity (step 5), review questions and transfer challenge.

---

## Starting Version

* Chapter 8's Java 17 application, directory adapter and complete Maven suite.
* The existing borrowing policies **already demonstrate Strategy**.
* A **notification publisher** is an optional running collaborator.
* The proposed **lifecycle is a separate exercise**: it does not replace the running project's reservation or loan rules.
* The critical book review (Week 8) is governed by the module leader's instructions; **evidence must come from the selected book, not an AI summary**.

---

## Opening Problem: Three Requests

1. **Borrowing limits** may vary by borrower category.
2. A proposed workflow should allow **cancellation before checkout** but reject it **after the item is on loan**.
3. A successful reservation should **inform several local observers**, even when one expected notification attempt fails.

---

## Different Reasons to Vary

* **Category** selects a rule.
* **Lifecycle history** determines which action is legal.
* **Subscribers** determine who reacts to an accepted reservation.
* One large conditional method could combine them. One generic "behaviour pattern" would **conceal their differences**.
* A fourth question: a request as an object a caller can **execute later**. When is it captured, and when do its side effects happen?

---

# 9.1 What Changes, and Why?
### Variation in behaviour

---

## Four Different Questions

| Question | Primary variation | Candidate |
|---|---|---|
| Which count/duration rule applies? | Chosen algorithm or policy | Strategy |
| Which action is legal now? | Current lifecycle position and transitions | State |
| Who reacts to this occurrence? | Registered interested recipients | Observer |
| What action should this request object execute? | Captured receiver and arguments | Command |

---

## Policy vs. Lifecycle

* `BorrowingPolicy` answers whether a count and duration are permitted. Changing the policy **does not change what a reservation is** or whether a camera is already reserved.
* **Lifecycle** asks something else: the same cancellation may be legal for a confirmed reservation and **illegal after checkout**. A completed transition **changes which later actions are possible**.
* Selecting another duration algorithm cannot capture that history.

---

## Observer and Command Concern Others

* **Observer:** interested recipients. A desk display and a local audit observer respond to the same confirmed reservation **without becoming borrowing rules**.
* **Command:** a request as an action object. It **captures the receiver and arguments**, then invokes the receiver when executed.
* The requirements determine **which structure is useful**. Before drawing classes, write **one example where the behaviour varies** and **one outcome that must remain unchanged**.

---

## The Same Application Need Not Use All Four

* A **two-branch conditional** may remain clearer than an abstraction if the decision is small and stable.
* A **direct method call** is often sufficient if the request never needs to be stored, passed or handled independently.
* "All conditionals violate good design" is **false**. The question is whether decisions are **duplicated, mixed with unrelated responsibilities or hard to extend safely**.
* Pattern-based code still contains conditions: it **relocates** them.

---

## Keep Structural and Behavioural Changes Distinct

* The State exercise **compares two implementations of the same proposed table**: a structural comparison in an isolated example.
* Integrating it into the lending application would **introduce new lifecycle behaviour** and decisions about counts, availability and loans.
* The optional publisher adds observers behind the existing notification boundary: its ordering and failure policy are **new, explicit behaviour**.
* Not everything is "only refactoring".

---

# 9.2 Strategy
### Swapping one rule for another

---

## Strategy Is Already Present

* Strategy supplies interchangeable implementations of a behaviour through a **shared contract**.
* `ReservationRules`: a student count **below three**, **one to seven** days.
* `StaffReservationRules`: **below five**, up to **fourteen** days (illustrative).
* The coordinator depends on `BorrowingPolicy`, **not on the calculations**. Its category-to-policy map is supplied through construction.

---

## What Is and Is Not Dynamic

* A strategy need not be replaced while an operation runs.
* The policy map is **fixed for a coordinator instance**; each request **selects an entry by category**.
* Configuration-time selection plus per-request lookup is enough to show the role.
* Chapter 8's directory supplies the category at the entry point: it **does not choose arbitrary policy code or rewrite duration limits**.

---

## Compare With the Conditional Starting Point

* The teaching test includes a small conditional: if student, student limits; otherwise (for the two supported enum values) staff limits.
* Understandable for **two rules in one place**.
* The pressure for Strategy appears when algorithms acquire **distinct reasons to change** or **repeated callers need consistent selection**.
* The conditional is a **teaching example only**: no duplicate policy engine in the application.

---

## Independent Expected Results

* The comparison checks **both** the conditional and the policy objects **against independently written boundary results**.
* Testing only that **the two implementations agree** is weaker: both could contain the same mistaken maximum.
* Eight rows: a student at two records requesting seven days; a student already at three; staff at four requesting fourteen; negative counts; zero and excessive durations.

---

## The Common Contract

* Every policy accepts the same two integers and returns a **deterministic boolean without changing application state**.
* Negative counts and non-positive durations return **false**.
* A true answer means the rule permits a request. It says **nothing about identity, stock or interval conflicts**.
* A strategy that performs **directory lookup, sends a message or stores a reservation** no longer behaves like this contract, even with a matching signature.

---

## A Temporary Staff Strategy

* A test supplies a staff strategy permitting **at most one counted reservation and two days**. The coordinator is **unchanged**.
* Three days: rejected. Two days: accepted (R1). Another request for that borrower: **rejected**. A student's seven-day request still succeeds under its own strategy.
* An isolated configuration test, **not a change to the book's default staff policy**.

---

## Trade-Off and Simpler Alternatives

* Strategy separates variation from the use case and makes the chosen behaviour **easy to supply in a test**.
* It adds a **selection responsibility**: someone must choose a compatible policy, and the constructor must reject an incomplete map.
* If the only difference is two numeric limits, **one parameterised `LimitPolicy(maxCount, maxDays)`** may be simpler. If rules later differ substantially, separate strategies clarify.
* Do not add a **`setPolicy`** method to look dynamic: it raises questions about requests in progress and reproducibility.

---

# 9.3 State
### Behaviour that depends on where you are in a lifecycle

---

## The Proposed Rules

* Begins at **REQUESTED**; may be confirmed or cancelled.
* A **confirmed** reservation may be checked out or cancelled.
* An **on-loan** reservation may be returned.
* **RETURNED** and **CANCELLED** are terminal for the four supported actions.
* Teaching rules for an **isolated model**. The running system confirms accepted reservations immediately, tracks loans separately, and has **no cancellation operation**.

---

## The Transition Table

| Current status | Confirm | Check out | Return | Cancel |
|---|---|---|---|---|
| REQUESTED | CONFIRMED | Reject | Reject | CANCELLED |
| CONFIRMED | Reject | ON_LOAN | Reject | CANCELLED |
| ON_LOAN | Reject | Reject | RETURNED | Reject |
| RETURNED | Reject | Reject | Reject | Reject |
| CANCELLED | Reject | Reject | Reject | Reject |

---

## What a Rejection Means

* Every rejection throws **`IllegalStateException`** and leaves the status **unchanged**.
* **Repeating cancellation is a rejection**, not an idempotent success.
* That choice belongs **in the table before it appears in Java**.
* Twenty parameter rows cover **five statuses and four actions**: five permitted transitions and **fifteen rejected combinations**.

---

## Reading a State Diagram

* A state diagram shows the **positions** an object can be in and the **events that move it**: nothing about implementation.
* Each rounded box is a **state**; an arrow is a **transition** labelled with its event.
* The filled circle is the **start point** (REQUESTED).
* A state with **no outgoing arrow** (RETURNED) allows none of the four actions.
* A **guard** is a condition in square brackets that must hold before a transition fires. This model has none.

---

## Figure 9.1: The Proposed Lifecycle

<!--svg:ch09-states-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="Figure 9.1, the proposed lifecycle: REQUESTED can be confirmed or cancelled; CONFIRMED can be checked out or cancelled; ON_LOAN can be returned. RETURNED and CANCELLED allow none of the four actions." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch09-states-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-states-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-states-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-states-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-states-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="45.0" y="60.0" width="120.0" height="56.0" rx="18" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="105.0" y="93.1" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">REQUESTED</text>
<rect x="265.0" y="60.0" width="120.0" height="56.0" rx="18" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="325.0" y="93.1" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">CONFIRMED</text>
<rect x="485.0" y="60.0" width="120.0" height="56.0" rx="18" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="545.0" y="93.1" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#172a42" text-anchor="middle">ON_LOAN</text>
<rect x="705.0" y="60.0" width="120.0" height="56.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="765.0" y="93.1" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">RETURNED</text>
<rect x="140.0" y="220.0" width="120.0" height="56.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="200.0" y="253.1" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#ffffff" text-anchor="middle">CANCELLED</text>
<circle cx="22.0" cy="88.0" r="9" fill="#172a42"/>
<path d="M31.0,88.0 L45.0,88.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-states-arr)"/>
<path d="M165.0,88.0 L265.0,88.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-states-arr)"/>
<text x="215.0" y="78.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">confirm</text>
<path d="M385.0,88.0 L485.0,88.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-states-arr)"/>
<text x="435.0" y="78.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">check out</text>
<path d="M605.0,88.0 L705.0,88.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-states-arr)"/>
<text x="655.0" y="78.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">return</text>
<path d="M105.0,116.0 L105.0,248.0 L140.0,248.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-states-arr)"/>
<text x="135.0" y="180.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">cancel</text>
<path d="M325.0,116.0 L325.0,248.0 L260.0,248.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-states-arr)"/>
<text x="355.0" y="180.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">cancel</text>
<text x="560.0" y="250.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">Terminal (dark): none of the four actions is allowed.</text>
</svg>
</div>
<!--/svg-->

---

## The Absent Edges Are Specification Too

* The diagram shows **permitted paths only**.
* An action with no arrow from a state is **not allowed there**.
* The table remains the **complete specification**: it states the absent edges, and **those are essential for testing**.
* "Terminal" means no supported outgoing action. It does **not** mean deleting a persisted record.

---

## The Conditional Implementation

```java
public void cancel() {
    switch (status) {
        case REQUESTED, CONFIRMED -> status = Status.CANCELLED;
        default -> throw rejected("cancel", status);
    }
}
```

* `ConditionalReservation` switches on a status enum inside **four operations**.
* The repeated selection is easy to inspect at this size. As operations grow, **one state's complete behaviour is spread across several methods**.

---

## The State Implementation

* `StateReservation` holds a **current state object** and delegates each operation to it.
* Each state provides its allowed successors; **default implementations reject** unsupported operations.
* The context assigns the returned successor **only after the state operation completes**.

```java
public void cancel() {
    phase = phase.cancel();
}
```

---

## Why Status Survives a Rejection

* If `phase.cancel()` throws, **the assignment never occurs**: the local reason the status remains unchanged.
* It is **not** a general transaction mechanism for arbitrary side effects inside state operations.
* Unsupported actions throw **before** assignment.

---

## Figure 9.2: Two Designs, One Contract

<!--svg:ch09-classes-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 235" role="img" aria-label="Figure 9.2: ConditionalReservation and StateReservation both realise the Lifecycle interface. StateReservation holds a Phase and delegates each operation to it; ConditionalReservation keeps a status value and switches on it." style="display:block;width:100%;height:calc(var(--u) * 23.50);margin:0 auto">
<defs><marker id="ch09-classes-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-classes-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-classes-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-classes-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-classes-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="10.0" width="250.0" height="183.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,66.0 L12.0,16.0 Q12.0,12.0 16.0,12.0 L254.0,12.0 Q258.0,12.0 258.0,16.0 L258.0,66.0 Z" fill="#e6eef6"/>
<text x="135.0" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="135.0" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Lifecycle</text>
<line x1="10.0" y1="66.0" x2="260.0" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+status() Status</text>
<text x="22.0" y="111.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+confirm() void</text>
<text x="22.0" y="134.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+checkOut() void</text>
<text x="22.0" y="157.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+returnItem() void</text>
<text x="22.0" y="180.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+cancel() void</text>
<rect x="350.0" y="15.0" width="250.0" height="71.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M352.0,51.0 L352.0,21.0 Q352.0,17.0 356.0,17.0 L594.0,17.0 Q598.0,17.0 598.0,21.0 L598.0,51.0 Z" fill="#e6eef6"/>
<text x="475.0" y="40.0" font-size="16" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ConditionalReservation</text>
<line x1="350.0" y1="51.0" x2="600.0" y2="51.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="362.0" y="73.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-Status status</text>
<rect x="350.0" y="135.0" width="250.0" height="71.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M352.0,171.0 L352.0,141.0 Q352.0,137.0 356.0,137.0 L594.0,137.0 Q598.0,137.0 598.0,141.0 L598.0,171.0 Z" fill="#e6eef6"/>
<text x="475.0" y="160.0" font-size="16" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">StateReservation</text>
<line x1="350.0" y1="171.0" x2="600.0" y2="171.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="362.0" y="193.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">-Phase phase</text>
<rect x="700.0" y="15.0" width="165.0" height="183.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M702.0,71.0 L702.0,21.0 Q702.0,17.0 706.0,17.0 L859.0,17.0 Q863.0,17.0 863.0,21.0 L863.0,71.0 Z" fill="#e6eef6"/>
<text x="782.5" y="34.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«enumeration»</text>
<text x="782.5" y="56.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Phase</text>
<line x1="700.0" y1="71.0" x2="865.0" y2="71.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="712.0" y="93.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">REQUESTED</text>
<text x="712.0" y="116.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">CONFIRMED</text>
<text x="712.0" y="139.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">ON_LOAN</text>
<text x="712.0" y="162.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">RETURNED</text>
<text x="712.0" y="185.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">CANCELLED</text>
<path d="M350.0,50.0 L260.0,50.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch09-classes-tri)"/>
<path d="M350.0,170.0 L260.0,170.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch09-classes-tri)"/>
<path d="M600.0,170.0 L700.0,170.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-classes-open)"/>
<text x="650.0" y="156.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">delegates to</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 9.2

* Both implement the **same `Lifecycle` interface**: a caller cannot tell them apart.
* `ConditionalReservation` keeps a **status value** and switches on it.
* `StateReservation` holds a **`Phase`** and delegates: the enum constants are the state objects.
* In the code `Phase` is **private**; the diagram shows it because it explains the design.
* The realisation arrows say both keep **the same promise**.

---

## State Objects as an Enum (1 of 2)

```java
private enum Phase {
    REQUESTED(Status.REQUESTED) {
        @Override Phase confirm() { return CONFIRMED; }
        @Override Phase cancel()  { return CANCELLED; }
    },
    CONFIRMED(Status.CONFIRMED) {
        @Override Phase checkOut() { return ON_LOAN; }
        @Override Phase cancel()   { return CANCELLED; }
    },
```

* Each constant **overrides only the transitions the table permits**.

---

## State Objects as an Enum (2 of 2)

```java
    ON_LOAN(Status.ON_LOAN) { @Override Phase returnItem() { return RETURNED; } },
    RETURNED(Status.RETURNED),
    CANCELLED(Status.CANCELLED);

    Phase confirm()    { throw rejected("confirm", status); }
    Phase checkOut()   { throw rejected("check out", status); }
    Phase returnItem() { throw rejected("return", status); }
    Phase cancel()     { throw rejected("cancel", status); }
}
```

* Everything not overridden is **rejected by default**, so the terminal states need no code.

---

## Shared State Objects, Separate Progress

* The enum constants contain **no reservation-specific mutable data**.
* Two contexts can refer to the **same REQUESTED constant** without sharing progress: **each context owns its own current-state reference**.
* A test advances one context while leaving another unchanged.
* An enum used only as a tag in a central switch **would be the conditional design instead**.

---

## No Public Setter

* No caller can assign a new phase directly.
* A public setter would let a caller **skip confirmation or resurrect a returned reservation** without passing the rules.
* **Read-only status** is sufficient for observation.
* That the State example has no public setter is established **by reading the API**, not by a runtime test.

---

## Test, Trade-Off and Integration Boundary

* Twenty parameter rows, each run against **both** implementations, with an **independently specified** outcome; rejected actions preserve state.
* Comprehensive for the small table, **not for a real reservation process**: time windows, permissions, conflicts, cancellation effects and loan storage are outside it.
* State groups behaviour by lifecycle position but adds **indirection**. For this small fixed table, **keeping the conditional is defensible**.
* Before integrating: do cancelled reservations stop counting? Do intervals become available? These are **requirements**, not consequences of State.

---

# 9.4 Observer
### Telling interested parties without knowing who they are

---

## Problem and Simple Attempt

* After acceptance, several local components may react.
* Hard-coding each observer in the coordinator **couples reservation decisions to the changing recipient list**.
* A **direct call** remains simpler for a single fixed collaborator: the existing sender interface already supports that.

---

## The Optional `NotificationPublisher`

* It **implements `NotificationSender`**, so the coordinator uses it through its existing boundary.
* Observers register a callback receiving the **immutable confirmed reservation**.
* Registration and dispatch are **the publisher's responsibility**, not new methods on the coordinator.
* Java's `PropertyChangeSupport` is a listener-management example. This publisher has **its own documented contract**: it does not inherit another library's ordering, concurrency or failure guarantees.

---

## Define the Observable Behaviour First

* **Synchronous, sequential, in memory.**
* Observers are called in **registration order**, using a **snapshot taken at the start** of publication.
* Each observer in that snapshot is attempted **once** (unless an unexpected exception stops dispatch).
* **No retries.**

---

## The Publisher's Contract (1 of 2)

| Situation | Selected outcome |
|---|---|
| No observers | Normal return; no delivery claim |
| Same observer object registered twice | Reject duplicate registration |
| Subscription closed | Remove that registration; repeated close is harmless |
| Subscribe or unsubscribe during a callback | Change subsequent publications, not the current snapshot |

---

## The Publisher's Contract (2 of 2)

| Situation | Selected outcome |
|---|---|
| Expected `NotificationException` | Retain failure and continue to later observers |
| Unexpected exception | Propagate immediately; later observers are not attempted |
| Recursive publication through the same publisher | Reject with `IllegalStateException` |

* Observer identity uses the **same object reference**, not custom equality. The publisher does not deduplicate recipients by business identity.

---

## The Publisher's Core

```java
for (Entry entry : List.copyOf(entries)) {          // snapshot
    try {
        entry.observer.onConfirmed(reservation);
    } catch (NotificationException failure) {        // expected failure
        if (aggregate == null)
            aggregate = new NotificationException("One or more observers failed");
        aggregate.addSuppressed(failure);
    }
}
if (aggregate != null) throw aggregate;
```

* A `finally` block resets the recursion guard.

---

## Subscription Handles Own One Registration

* A handle owns **one registration**. Closing an old handle again must **not remove a later registration** of the same observer.
* The implementation keeps **a distinct entry object per registration** to make that ownership precise.
* An implementation removing by observer identity on every close could **incorrectly remove a newer registration**.

---

## Publication Occurs After Storage

* The coordinator **stores the accepted reservation before calling its sender**.
* If an observer fails with the expected exception, the publisher continues, collects the failures, and throws **one aggregate** `NotificationException`.
* The coordinator returns its existing suffix: **notification failed; reservation retained**.

---

## Figure 9.3: One Failing Observer

<!--svg:ch09-seq-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 362" role="img" aria-label="Figure 9.3: one accepted reservation is published to three observers; the display observer fails with the expected exception, the others still run, and the publisher throws one aggregate exception that the coordinator turns into the failure suffix." style="display:block;width:100%;height:calc(var(--u) * 36.20);margin:0 auto">
<defs><marker id="ch09-seq-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-seq-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-seq-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-seq-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-seq-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="30.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="110.0" y="36.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Coordinator</text>
<path d="M110.0,56.0 L110.0,354.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="195.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="275.0" y="36.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Publisher</text>
<path d="M275.0,56.0 L275.0,354.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="360.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="440.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Desk</text>
<text x="440.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">observer</text>
<path d="M440.0,56.0 L440.0,354.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="525.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="605.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Display</text>
<text x="605.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">observer</text>
<path d="M605.0,56.0 L605.0,354.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="690.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="770.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Audit</text>
<text x="770.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">observer</text>
<path d="M770.0,56.0 L770.0,354.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="10.0" y="68.0" width="200.0" height="28.0" rx="5" fill="#f6ead9" stroke="#b4762e" stroke-width="1.6"/>
<text x="110.0" y="88.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle" font-style="italic">Reservation already stored</text>
<path d="M114.0,120.0 L271.0,120.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch09-seq-arr)"/>
<text x="192.5" y="113.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">send(reservation)</text>
<path d="M279.0,148.0 L436.0,148.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch09-seq-arr)"/>
<text x="357.5" y="141.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">onConfirmed(reservation)</text>
<path d="M436.0,174.0 L279.0,174.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch09-seq-arr)"/>
<text x="357.5" y="167.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Normal return</text>
<path d="M279.0,202.0 L601.0,202.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch09-seq-arr)"/>
<text x="440.0" y="195.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">onConfirmed(reservation)</text>
<path d="M601.0,228.0 L279.0,228.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch09-seq-arr)"/>
<text x="440.0" y="221.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">NotificationException</text>
<path d="M279.0,256.0 L766.0,256.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch09-seq-arr)"/>
<text x="522.5" y="249.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">onConfirmed(reservation)</text>
<path d="M766.0,282.0 L279.0,282.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch09-seq-arr)"/>
<text x="522.5" y="275.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Normal return</text>
<path d="M271.0,310.0 L114.0,310.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch09-seq-arr)"/>
<text x="192.5" y="303.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Aggregate NotificationException</text>
<rect x="50.0" y="324.0" width="285.0" height="28.0" rx="5" fill="#f6ead9" stroke="#b4762e" stroke-width="1.6"/>
<text x="192.5" y="344.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle" font-style="italic">Confirmation + failure suffix</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 9.3

* **Partial success:** the desk and audit observers ran; the display observer failed.
* It does **not** roll back earlier observer effects, and the suffix does **not** mean every observer failed.
* The aggregate keeps individual exceptions as **suppressed exceptions**.
* The coordinator returns only its established message: **no detailed observer diagnostics**.

---

## Unexpected Failures

* An unexpected programming exception **stops dispatch** and escapes the coordinator, which catches only `NotificationException`.
* The reservation **still exists** because storage happened earlier.
* A caller must **not infer "nothing happened"** from the fact that the operation threw.
* The recursion guard is **not a concurrency lock or a rollback system**. Callbacks must not mutate the coordinator or start new reservations.

---

## The Snapshot Rule in Action

```text
first, second, first, third
```

* During the first publication, the first observer **removes the second** and **adds a third**.
* The snapshot already includes the second, so **it still runs**. The next publication sees the updated registrations.
* A declared contract, **not an accident of `ArrayList` iteration**. Deterministic sequence tests, not concurrent-race tests.

---

## Trade-Off and Non-Use Case

* Observer reduces direct knowledge of recipients but makes execution **less obvious**: work happens inside registered callbacks.
* **Ordering dependencies** can become hidden. If one observer must finish a business step before another begins, **explicit orchestration** may express it better.
* Keep **a single sender for a fixed output**.
* No durable delivery, broker, asynchronous execution or exactly-once guarantee. **Not an automatic next step.**

---

# 9.5 Command
### A request you can carry before running it

---

## Problem

* `DirectoryReservationService.reserve` **immediately** performs lookup and reservation.
* A user interface action or a small invoker may need **an object containing the request, to execute when selected**.
* `Command<R>` has one method, `R execute()`.
* `ReserveEquipmentCommand` captures the **service, borrower id, item id, start date and days**.

---

## The Command Record

```java
public record ReserveEquipmentCommand(DirectoryReservationService receiver,
        String borrowerId, String itemId, LocalDate start, int days) implements Command<String> {
    public ReserveEquipmentCommand {
        Objects.requireNonNull(receiver, "receiver");
        if (borrowerId == null || borrowerId.isBlank() || itemId == null || itemId.isBlank()) {
            throw new IllegalArgumentException("Identifiers must not be blank.");
        }
        Objects.requireNonNull(start, "start");
    }
    @Override public String execute() {
        return receiver.reserve(borrowerId, itemId, start, days);
    }
}
```

---

## What Construction Does Not Do

* Construction validates **required references and identifiers**.
* It performs **no lookup, allocates no reservation, notifies no one**.
* The receiver stays responsible for the use case: the command does **not** reproduce borrowing policy or store its own reservation list.
* A lambda or method reference can be enough if no named request data is needed. `Runnable` is a familiar no-result action, but **using it is not a Command architecture**.

---

## Three Moments of a Command

<!--svg:ch09-command-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 270" role="img" aria-label="Three moments of a command: constructing it captures the receiver and arguments and does nothing else; executing it makes the service evaluate the current state; executing it again re-enters the service and gives a different result." style="display:block;width:100%;height:calc(var(--u) * 27.00);margin:0 auto">
<defs><marker id="ch09-command-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-command-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-command-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-command-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch09-command-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="20.0" width="230.0" height="74.0" rx="8" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="125.0" y="48.0" font-size="18" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">1  Construct</text>
<text x="125.0" y="76.0" font-size="12.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="middle">new ReserveEquipmentCommand(…)</text>
<text x="125.0" y="130.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">captures the receiver</text>
<text x="125.0" y="149.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">and the arguments;</text>
<text x="125.0" y="169.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">no lookup, no reservation,</text>
<text x="125.0" y="188.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">no notice</text>
<rect x="320.0" y="20.0" width="230.0" height="74.0" rx="8" fill="#e6eef6" stroke="#1d588c" stroke-width="2"/>
<text x="435.0" y="48.0" font-size="18" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">2  Execute</text>
<text x="435.0" y="76.0" font-size="12.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="middle">command.execute()</text>
<text x="435.0" y="130.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">the service evaluates the</text>
<text x="435.0" y="149.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">CURRENT state: lookup,</text>
<text x="435.0" y="169.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">eligibility and conflict</text>
<rect x="630.0" y="20.0" width="230.0" height="74.0" rx="8" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="745.0" y="48.0" font-size="18" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">3  Execute again</text>
<text x="745.0" y="76.0" font-size="12.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="middle">command.execute()</text>
<text x="745.0" y="130.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">re-enters the service: the</text>
<text x="745.0" y="149.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">stored record now conflicts;</text>
<text x="745.0" y="169.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">a different result; one</text>
<text x="745.0" y="188.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">record and one notice remain</text>
<path d="M240.0,57.0 L320.0,57.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-command-arr)"/>
<path d="M550.0,57.0 L630.0,57.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch09-command-arr)"/>
<text x="280.0" y="15.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="middle" font-style="italic">state may change</text>
<text x="590.0" y="15.0" font-size="13.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="middle" font-style="italic">same command</text>
</svg>
</div>
<!--/svg-->

---

## Time of Execution Changes the Outcome

* Between construction and execution, **another request may reserve the item**.
* The command must evaluate **current receiver state** when executed. Capturing an earlier "available" result and using it as permission **bypasses the actual conflict check**.
* The record's fields are immutable, but it holds a **reference to a mutable service**. It is **not a snapshot of application state**.
* A test constructs the command, creates a competing reservation, and verifies rejection when it later executes.

---

## Repeated Execution

* First execution creates a reservation; the second **sees a conflict**: a different result, **without another notice**.
* That does **not** mean commands are idempotent. There is **no request identifier, deduplication record or replay protocol**.
* "Command makes retries safe" is **false**.

---

## Failure, Undo and Alternatives

* A directory failure **propagates unchanged**: the command does not convert it into success, retry it or compensate.
* **Undo needs its own semantics.** Deleting a record would not undo an observer's side effect; the project has no cancellation contract.
* Naming a class `Command` supplies **no undo, transactions, queueing or persistence**.
* Use a **direct call** when there is no reason to represent the action separately.

---

# 9.6 Testing Behaviour That Patterns Organise
### The requirement supplies the expected result

---

## What Each Pattern's Tests Need

* A test that checks an object **implements `BorrowingPolicy`** cannot establish correct limits.
* A test that **constructs a state object** cannot establish a valid transition.
* A test that **counts subscribers** cannot establish what happens after one throws.
* **Strategy:** independent boundary examples. **State:** the transition table, including rejected edges. **Observer:** ordered event histories and state after failures. **Command:** distinguish construction from execution.

---

## Compare Without Circular Proof

* The lifecycle tests send the same action to the conditional and State implementations, but **both are checked against a fixed table**.
* Equality between the two alone is insufficient: if both allowed cancellation on loan, **they would agree while violating the requirement**.
* The table covers this exercise's complete state/action space. It does **not** prove arbitrary sequences with time, external state or permissions. **Keep the claim proportional to the model.**

---

## Hide State Identity

* Tests observe `status()` and operations, **not the private enum field**.
* They survive replacing enum-based states with **separate state classes**, as long as the public contract is unchanged.

---

## Test Partial Effects Explicitly

* **Unexpected exception:** earlier callbacks ran, later ones did not, **the coordinator retained its record**. More informative than checking only the thrown exception.
* **Expected failure:** later observers still run, and the aggregate keeps both failures **in order**.
* **Subscription changes:** removal during a callback affects the **next** publication; the removed observer still appears in the **current** snapshot.

---

## Evidence Narrows Uncertainty

* The command replay test documents **one concrete repeated execution**. It guarantees nothing about future commands or other receiver states.
* Passing evidence should **narrow uncertainty about the selected promise**, not expand into unsupported general assurance.
* The full build executes **107 JUnit invocations**: 63 inherited and 44 new.

---

# 9.7 Choosing a Pattern, and Knowing Its Limits
### Compare alternatives by their costs

---

## Reasonable First Options

| Situation | First option | Pattern when justified |
|---|---|---|
| Two small fixed limit rules | One conditional or parameterised policy | Strategy for independent implementations |
| A small fixed transition table | Enum and explicit operations | State when grouping state-specific behaviour clarifies |
| One fixed notification output | Direct injected sender | Observer for a changing set of local recipients |
| One immediate reservation request | Direct service call | Command when the request must be represented separately |

---

## No Row Says More Classes Is Progress

* A useful explanation identifies **where a future edit will occur**, **which contract stays stable** and **which new obligations arise**.
* **Observer** centralises registration but needs decisions about **order and failure**.
* **State** centralises each state's actions but needs **consistency between model and tests**.

---

## Be Precise About This Version

* The project keeps Chapter 8's directory boundary and all previous application sources.
* `NotificationPublisher` is **an additional sender option**; no earlier demo is silently rewired.
* The State model stays in the separate `behaviour` package and **never updates real reservation or loan storage**.
* Inherited limits remain: in-memory storage, trusted internal APIs, no enforced identity, and reservation records that **still count and block intervals after loan return**.

---

## A Design Decision Must Be Challengeable

> Several local observers need to react; a publisher owns registration and dispatch; one fixed sender remains simpler where recipients do not vary; failures can leave partial effects.

* "Observer decouples everything" **cannot be assessed**.
* "State eliminates invalid operations" is too broad **unless the API and rules enforce the model**.

---

# 9.8 Strategy or State?
### Judging AI proposals

---

## Ground Rules for the Activity (1 of 2)

| | For this activity |
|---|---|
| Your goal | Decide whether each proposal fits a policy-selection problem or a lifecycle problem, and what each allows a caller to do |
| You start with | The lifecycle table in 9.3, the existing strategies, and the failure and replay behaviour in 9.4 and 9.5 |
| What is in bounds | Compare the proposals and qualify the reliability claim; adopt none without the table |

---

## Ground Rules for the Activity (2 of 2)

| | For this activity |
|---|---|
| How to check | The transition table, the Strategy and State tests, the publisher and command tests |
| How to decide | A verdict with evidence for each claim |
| No AI account? | The ready-made example is enough |

---

## Two Fictional Proposals

**Proposal A:** "Implement `RequestedPolicy`, `ConfirmedPolicy` and `ReturnedPolicy` as strategies. Expose `setPolicy` so callers can choose any policy before each operation. Calling a return method should simply select the returned policy."

**Proposal B:** "Store the current phase inside a reservation context. Delegate confirm, checkout, return and cancel to phase-specific behaviour. Allow only transitions from the reviewed table and preserve the current phase after a rejected action."

---

## Verdicts

* **Proposal A** exposes policy selection with **no transition authority**: a caller can pick the returned policy though no checkout occurred. Calling the classes strategies does not solve **legal histories**.
* **Proposal B** puts the phase in the context and restricts changes to reviewed actions: the **stronger match**, provided the actual implementation rejects invalid transitions and preserves state. **More appropriate wording is not evidence.**
* For student/staff duration rules the pressure differs: they are **selected policies, not stages**.

---

## A Third Claim

> Observer guarantees that all recipients receive the event once, and Command makes retries safe.

* **Observer** does not guarantee every callback completes: the expected-failure policy continues but still reports **partial success**; an unexpected failure **stops later callbacks**.
* **Command** does not make replay safe: repeated execution re-enters the receiver; the conflict check here is **not a general deduplication mechanism**.
* **Undo and compensation** need separate agreed semantics.

---

## Evidence to Retain

* For each AI claim: the **requirement**, the **claimed structure**, the **confirming or rejecting test**, the **remaining limitation**.
* Example entry: "Model claims cancellation is legal from any state; transition table forbids ON_LOAN/CANCEL; test requires an exception and unchanged ON_LOAN; proposal rejected."
* Do not use generated implementation and generated expectations as **mutual proof**.

---

# 9.9 Behaviour-Pattern Habits That Mislead
### Eight to avoid

---

## Mistakes 1 to 3

| Mistake | Consequence | Better action |
|---|---|---|
| Treat category policies as lifecycle positions | Confuses selection with permitted transitions | Identify what changes the behaviour |
| Expose an unrestricted state setter | Allows invalid jumps | Change state only through reviewed operations |
| Store context data in shared state objects | One reservation may affect another | Keep progress in each context |

---

## Mistakes 4 to 6

| Mistake | Consequence | Better action |
|---|---|---|
| Catch all observer errors as expected failures | Hides programming defects | Specify and catch the declared failure type |
| Assume a thrown notification means no reservation exists | Misreads partial effects | Check the storage-before-publication sequence |
| Remove observers from a live iteration | Makes dispatch fragile | Define and test snapshot semantics |

---

## Mistakes 7 and 8

| Mistake | Consequence | Better action |
|---|---|---|
| Treat a captured command as earlier permission | Bypasses current receiver state | Validate the use case at execution |
| Assume a pattern supplies retries or undo | Invents unimplemented guarantees | Define those semantics separately |

---

# 9.10 Try It Yourself
### Lifecycle, publisher and command

---

## What You Start With, and the Demonstration

* **You start with:** the Chapter 8 version, the lifecycle table, the conditional and State examples, the publisher contract. Steps 1 to 5: the book's project. **Step 6: your team's project.
* **Demonstration:** locate the existing strategies; trace **permitted and rejected** lifecycle actions before showing the two implementations. Run one expected observer failure and show the **retained reservation** and the **later callback**.
* **Guided practice:** choose a table row and explain its result **independently of the code**. Predict the effect of unsubscribing during dispatch. Compare a direct service call with constructing and executing a command.

---

## Independent Work: Steps 1 to 3

1. **Replace the repeated conditional** in the isolated lifecycle with State delegation, preserving the table.
2. Show **permitted and rejected** actions, including unchanged status on failure and **independent contexts**.
3. Demonstrate the publisher's **order and expected-failure continuation**. Construct a `ReserveEquipmentCommand` **without executing it**, show construction performs no reservation, then execute it.

---

## Independent Work: Steps 4 to 6

4. Choose a **second scenario** and justify adopting or declining Strategy, Observer or Command against a simpler implementation.
5. **Evaluate the fictional AI proposals** and retain independent evidence.
6. On your team's project, find **one conditional that selects behaviour by type or tracks a lifecycle**. Write a test that **protects its current behaviour**, then decide whether Strategy, State or neither is justified. Record **what you would decline to build and why**.

---

## Expected Output and Acceptance

* **What you should end up with:** before and after source; a reviewed transition table; runnable tests; a reproducible demo; a concise problem-solution-consequence note; the step 6 decision.
* **Accept when:** **no unrestricted phase setter**; correct terminal behaviour; outcomes match independently stated expectations; **observer failure does not imply rollback**; **command construction performs no reservation**; the old regression suite still runs.
* **If you want more:** propose real cancellation. Specify effects on counts, availability, active loans, identifiers and notifications **before changing code**.

---

## A Suggested State Refactoring Sequence

1. Begin with the complete table and `ConditionalReservation`; run the table tests.
2. Introduce private State objects implementing the four operations: **reject by default**, override only permitted transitions.
3. The context delegates and accepts a returned successor **only on success**.
4. Run the same table against both; add the **independent-context** check.
5. Inspect the public API for a **setter**.

* A reasoned conclusion may still **favour the conditional** for this small model.

---

## A Second Decision: Adopt Observer Selectively

* **Problem:** several local components react after acceptance, and their registrations can change.
* **Solution:** an optional publisher implementing the existing sender interface; ordered snapshots; the declared failure rule; the demo supplies it explicitly.
* **Consequences:** the coordinator stays independent of observer identities; **partial effects**; observers need lifetime management; unexpected failures escape after storage.
* **Simpler alternative:** one injected sender; or explicit orchestration when several steps form one business operation.

---

## Decline a Pattern With a Concrete Reason

* A button handler can call the service if it **never needs to carry the request separately**: Command adds a type with **no demonstrated benefit**.
* One count/duration formula **parameterised by two limits** may be enough: separate Strategy classes pay off when rules deserve independent implementations.
* Name **which change each alternative makes easier and which obligation it adds**.

---

# 9.11 Questions to Think with, and a Transfer Challenge
### Concept, diagnosis, transfer

---

## Concept Questions

1. Why is category-based borrowing policy a Strategy example while the proposed reservation lifecycle is a State example?
2. Why can stateless enum-based State objects be shared while reservation progress must remain separate?
3. What does snapshot iteration mean for an observer removed during publication?
4. What does a Command capture, and which decisions still belong to execution time?

---

## Diagnosis Questions

5. An unexpected observer exception occurs after two callbacks succeed. The caller assumes no reservation was stored and immediately repeats the request. Explain why that assumption is unsupported and identify the observations needed before choosing a recovery action.
6. An AI-generated State implementation has `setStatus(RETURNED)` and a happy-path test. Explain the missing guarantee and design tests that reject an invalid jump or action sequence.

---

## Guidance: Questions 1 and 2

1. **Category selects which count/duration policy applies**: it does not advance a lifecycle. **State** makes the meaning or legality of an operation depend on the context's current position. Similar delegation structures can serve different purposes.
2. The constants hold **only behaviour and a fixed status**. Each context owns its current reference. Mutable reservation data in a shared constant would couple contexts. The independence test advances one context and observes the other **still at REQUESTED**.

---

## Guidance: Questions 3 and 4

3. An observer present when publication begins **still receives that publication** even if a prior callback closes its subscription; it is **absent from the next snapshot**.
4. The **receiver and request arguments**, **not** a snapshot of receiver state or an advance permission. Lookup, eligibility and conflicts are evaluated **when `execute` calls the service**.

---

## Guidance: Questions 5 and 6

5. The coordinator stores **before** publishing, so the exception is compatible with **a stored reservation and partial external effects**. Inspect the reservation snapshot and the known event history before recovery; **do not blindly repeat**.
6. A setter **bypasses the transition table**. Test: checkout before confirmation, cancellation while on loan, repeated return: each must reject and **preserve status**. Add **valid sequences and independent contexts** so the code cannot pass by rejecting everything.

---

## Transfer Challenge: A Document Workflow

A document workflow has **draft, approved and published** stages. Review policy **differs by department**, several local views react **after publication**, and a user interface can **hold a publish request before executing it**.

* Identify the **four variation pressures**; choose **only the justified patterns**.
* Specify **one invalid transition**, **one observer failure** and **one stale-command outcome**.
* State which requirements need **clarification** before implementation.

---

## Transfer Guidance

* A **department review algorithm**: Strategy candidate. **Draft, approved, published**: State candidate. **Local views reacting**: Observer. A **UI-held publish request**: Command, if it needs separate representation.
* **Do not require all four.**
* **Invalid transition:** publishing a draft before approval; it must stay a draft.
* **Observer failure:** a preview fails after publication was stored: do remaining observers run, and what does the caller see?
* **Stale command:** a publish captured while approved, executed after an edit returned it to draft: the receiver must check **current state** and reject.

---

# 9.12 The Critical Book Review
### Method in Appendix E

---

## What the Version Says

* Your **individual critical review** of a book from the approved list is **due in Week 8**.
* **Appendix E** develops the method: a reading record, questions for each part, prompts for checking sources.
* The **current assignment brief** is always the authority on length, sources, format and deadline.
* Read the selected book **directly**, not a summary. Keep apart **what the author claims**, **what you infer** and **what an AI tool suggested**.

---

## For a Pattern Discussion

* Does the book's example establish the **extension benefit it claims**?
* Which **simpler alternative** did the author consider?
* What **cost** does the author acknowledge?
* A criticism resting on **a source and a concrete case** is stronger than a catalogue of definitions.
* Reading this textbook does not satisfy the assignment, and **an AI summary of an unread book is not evidence about it**.

---

# What to Take Away, and What Comes Next
### What to carry forward

---

## Summary

* **Strategy** selects a behaviour.
* **State** governs behaviour through transitions.
* **Observer** connects interested recipients to an occurrence.
* **Command** represents an action for later invocation.
* Each creates obligations as well as opportunities, **especially around state, ordering and partial effects**.

---

## Where the Project Stands

* An optional, tested **local notification publisher**.
* A **request-action** example.
* The proposed **lifecycle remains clearly separated**.
* **Chapter 10** examines how these responsibilities fit into application structure and dependency direction.

---

## Sources and Further Reading

1. **Gamma, Helm, Johnson, Vlissides:** *Design Patterns*: the Strategy, State, Observer and Command entries.
2. **Oracle:** Java SE 17 `PropertyChangeSupport`, `Throwable` and `Runnable`.
3. **JUnit Team:** JUnit 5.13.4 User Guide.
4. **Martin:** *Agile Software Development* (2002): the Strategy, Command, Observer and State chapters.

* Full references and links are in the chapter text.
