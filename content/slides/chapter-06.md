---
title: "Chapter 6: Interfaces, Dependencies, and Composition"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 60
type: slides
layout: page
---

# Chapter 6: Interfaces, Dependencies, and Composition
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **6.1 Dependencies that make change difficult**
  * A real boundary: notification output, first built the coupled way.
* **6.2 Client-specific contracts and ISP**
  * Design the interface around what a particular client needs.
* **6.3 Policy and implementation dependencies**
  * Three decisions, and the partial-success case made explicit.
* **6.4 DIP**
  * Source dependency direction; DI can exist without DIP.

---

## Chapter Roadmap (2 of 3)

* **6.5 Constructor injection and composition roots**
  * Two views of one design: classes and objects.
* **6.6 IoC and DI containers**
  * An educational container makes lifetime visible.
* **6.7 Costs of abstraction**
* **6.8 AI in practice: an interface that hides little**

---

## Chapter Roadmap (3 of 3)

* **6.9 Common mistakes**
* **6.10 Practical activity: assemble a replaceable output**
  * Nine steps; step 9 is on your Team project.
* **6.11 Review questions**, **6.12 Transfer challenge**
* **6.13 Quiz 1 revision pointers**
* **Summary and next chapter**
  * Chapter 7: test design, controlled substitutes, red-green-refactor.

---

## Learning Outcomes (1 of 2)

By the end of this chapter, you should be able to:

1. **Design an interface** around what a particular client needs.
2. **Explain ISP** through a concrete dependency that is unnecessarily broad.
3. **Distinguish DIP, dependency injection and inversion of control.**

---

## Learning Outcomes (2 of 2)

4. **Construct a small object graph** using constructor injection and an explicit composition root.
5. **Explain the benefits and costs of an interface**, including the limits of what it guarantees.

---

## Module Connection and Entry Checkpoint

* Supports LO1 and LO4. **Quiz 1** revision points appear later and refer to Chapters 2 to 5, matching its Weeks 1 to 4 coverage. This chapter's material is **not silently added** to that coverage.
* **Entry:** Chapter 5's Java 17 code: student and illustrative staff policies, extracted formatter, the original **34 checks**, the **five acceptance groups** and the **44 Chapter 5 checks**.
* Formatting a string has never meant sending email. **Notification output is a new, explicitly bounded teaching feature.**

---

## Reading Route

* **Core reading:** Sections 6.1 to 6.6. Section 6.6 compares manual assembly with a small educational container.
* **Minimum required lab:** steps 1 to 9 of Section 6.10, including step 7 (the container walkthrough). Steps 1 to 8: **Book project**. Step 9: **Team project**.
* **Optional extension:** the AI activity, the optional extension in 6.10, the review questions and the transfer challenge.
* Readings: the DIP and ISP chapters of Martin, and Fowler's article on dependency injection.

---

## Opening Scenario: A Console Sender Inside the Coordinator

* The coordinator now uses separate borrowing policies and a confirmation formatter.
* A new requirement: **pass each accepted reservation to a notification output**.
* One member creates a **console sender inside the coordinator**. It works.
* But another member **cannot inspect notifications without watching console output**.
* Replacing the output **requires editing the reservation workflow**.

---

## An AI Proposes an Interface

* The coordinator's field becomes `NotificationSender`.
* But its constructor **still creates a particular sender and reads provider settings**.
* The diagram looks different. **The code still chooses its own environment.**
* Naming an abstraction is not the same as **depending on a useful contract** or **being supplied a collaborator from outside**.

---

## What the Chapter Introduces

* The **Interface Segregation Principle (ISP)**.
* The **Dependency Inversion Principle (DIP)**.
* **Constructor injection** and a **composition root** to assemble the running application.
* A small **container walkthrough** that makes object lifetime visible, with no framework installation.

---

# 6.1 Dependencies That Make Change Difficult
### Begin with a real boundary

---

## What a Dependency Is

* A dependency exists when one part of the program **needs knowledge or behaviour from another**.
* Dependencies are necessary: the coordinator needs dates, reservations and borrowing decisions.
* The design problem: **which knowledge should remain stable, and where should changing details live?**

---

## What Chapter 5 Left Behind

* Two visible decisions inside the coordinator: **construction of concrete policies** and **selection of a policy by category**.
* The formatter was also constructed there.
* A deliberate intermediate checkpoint.
* Now: **move assembly out of the request workflow** while introducing a notification boundary.

---

## The New Requirement

> After storing an accepted reservation, attempt one notification through the configured output. Rejected or invalid requests produce no notification. The configured output may record the accepted reservation in memory or print a notice to a supplied stream.

* Local teaching outputs: **not** an email service, durable queue or proof of receipt.
* A normal return means the output **completed its own local operation**, not remote delivery.

---

## The Deliberately Coupled Version

```java
private final NotificationSender notifications =
        new ConsoleNotificationSender(System.out, new ConfirmationFormatter());
```

* The field has an **interface type**, but the coordinator still:
  * **names the console implementation**,
  * **chooses the global output stream**,
  * **constructs its formatting dependency**.
* The interface alone has **not** separated configuration from use.

---

## Feature Change, Then Structural Change

* This intermediate version is **newly introduced teaching code**, not a description of Chapter 5.
* Adding notification is a **feature change**.
* Replacing direct construction with an injected collaborator is a **subsequent structural change**, with an explicit constructor migration.
* The concrete pressure: **one caller wants console output; another wants to inspect accepted records in memory.** The same algorithm should serve both.

---

## Decisions That Should Remain in the Coordinator

* The coordinator still decides **when a reservation has been accepted**, and so when notification is eligible.
* Moving that decision into the sender would **duplicate policy and conflict handling**.
* The sender decides **how its local output handles the accepted record**, without granting or rejecting anything.

---

## A Reviewable Dependency Diagnosis

* "Remove all dependencies" is **not** a useful goal.
* "Remove the coordinator's knowledge of which notification provider to construct, **while keeping its acceptance sequencing**" is reviewable.
* A good diagnosis lists **both** the unwanted choice **and** the decision that belongs in the client.
* Output **failure** needs an application-level answer too: injection does not settle it.

---

# 6.2 Client-Specific Contracts and ISP
### Design for the caller's role

---

## ISP

* ISP directs attention to clients **forced to depend on operations they do not need**.
* The needed role here is small: **accept an already confirmed reservation for notification output**.

```java
public interface NotificationSender {
    void send(Reservation reservation);
}
```

---

## A Broad Interface to Avoid

* An all-purpose `EquipmentPlatform` interface with:
  * `send`,
  * `registerBorrower`,
  * `exportInventory`,
  * `deleteAccount`,
  * `configureMailServer`,
  * `rotateCredentials`.
* The coordinator uses **only the first**. The rest expose unrelated responsibilities and encourage implementations that **supply meaningless methods or throw unsupported-operation exceptions**.

---

## What a Narrow Role Gives

* A console output and an in-memory recorder implement **what they genuinely support**.
* The role does **not** need every capability of a future provider.
* An administration tool may need a **different contract**, if that requirement actually exists.
* Do not create an administration interface **until an administration client exists**.

---

## Small Is Not the Same as One Method

* The notification contract happens to have one method. **ISP does not prescribe one-method interfaces.**
* A client that genuinely needs several **cohesive** operations may benefit from a role containing all of them.
* Example: a document-writing client needing both writing and closing a session. Splitting them only to cut method count could allow **a write without the required lifecycle management**.

---

## Two Views of One Object

* `received()` is an **inspection operation** on the concrete recorder.
* The coordinator does not need it, so it is **not on `NotificationSender`**.
* A check can keep a reference to the recorder while supplying the same object through the narrow sender role.
* A deliberate use of **two views of one object**.

---

## Specify Outcomes and State Effects

* The sender contract: a **non-null accepted reservation**; it **must not modify** that record or the coordinator; expected output failures use **`NotificationException`**.
* The **recorder** appends the immutable record to its own list. The **console** prints a notice to its supplied stream.
* Both have output effects, so this is **not a pure policy operation**. Chapter 5's `BorrowingPolicy` remains side-effect-free under its contract.
* Do not apply one collaborator's restrictions blindly to another.

---

## Why the Sender Receives a `Reservation`

* This keeps the notification **tied to the accepted record**, not raw identifiers and dates assembled afresh.
* It means the boundary **deliberately knows that small domain type**.
* If an external transport later needs a different representation, **an adapter can translate it**. That need does not justify a transport-specific payload now.

---

## Do Not Mirror a Provider SDK

* A provider SDK might expose account management, diagnostics and bulk operations.
* A client-specific interface should express **the application's needs**, not the SDK.
* Review question: can the contract be explained **without referring to a vendor or transport setting**?
  * "Send this accepted reservation to the configured output": **yes**.
  * "Send this vendor request with the provider's retry token": **no**.

---

## The Sender Code

```java
@FunctionalInterface
public interface NotificationSender {
    void send(Reservation reservation);
}

public final class NotificationException extends RuntimeException {
    public NotificationException(String message) { super(message); }
}
```

* A normal return is **not** a promise of email delivery.

---

## The Recorder

```java
public final class RecordingNotificationSender implements NotificationSender {
    private final List<Reservation> received = new ArrayList<>();

    @Override
    public void send(Reservation reservation) {
        received.add(Objects.requireNonNull(reservation, "reservation"));
    }

    public List<Reservation> received() { return List.copyOf(received); }
}
```

---

## The Console Sender

```java
public void send(Reservation reservation) {
    output.println("Notice: " + formatter.format(reservation));
    if (output.checkError()) {
        throw new NotificationException("Console output failed.");
    }
}
```

* `PrintStream` normally **records** I/O errors rather than throwing, so the sender checks `checkError()` and translates the expected local error.
* The error state is **sticky**: once reported, later notices through the same sender are reported as failed too.

---

# 6.3 Policy and Implementation Dependencies
### Three decisions, and partial success

---

## Separate Three Decisions

| Decision | Owner in this checkpoint | Reason |
|---|---|---|
| Whether the request is acceptable | Coordinator and selected borrowing policy | Depends on reservation rules and current records |
| How notification is represented locally | Sender implementation and formatter | Depends on the chosen output |
| Which concrete objects are used | Application composition root | Depends on the demonstration environment |

---

## Moving Assembly Does Not Remove It

* The first decision should **not** depend on console configuration.
* The last decision must exist somewhere: a running program needs concrete objects.
* Moving assembly to the boundary makes it **explicit** rather than pretending it disappears.
* "Policy" has levels: a numeric borrowing policy decides limits; the coordinator implements the broader **application policy** (store before notifying; handle expected failure).

---

## The Partial-Success Case

* The completed operation **stores** the reservation, **formats** the confirmation and **calls the sender**.
* On an expected `NotificationException` it returns the confirmation followed by:

```text
 Notification failed; reservation retained.
```

* The leading space joins the suffix to the confirmation.
* The record **remains stored and counts as active**. It is not deleted, not reported as rejected, and **not retried**.

---

## The Failure Outcomes

<!--svg:ch06-failure-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 340" role="img" aria-label="After a request is accepted, the record is stored, the confirmation formatted, and the sender called once. Normal return gives the confirmation. A NotificationException gives the confirmation plus a failure suffix with the record retained and no retry. Any other exception propagates after the record was stored." style="display:block;width:100%;height:calc(var(--u) * 34.00);margin:0 auto">
<defs><marker id="ch06-failure-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-failure-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-failure-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-failure-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-failure-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="15.0" width="190.0" height="78.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="105.0" y="48.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Request accepted:</text>
<text x="105.0" y="71.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">checks passed</text>
<rect x="225.0" y="15.0" width="170.0" height="78.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="310.0" y="48.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Store the</text>
<text x="310.0" y="71.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">record</text>
<rect x="420.0" y="15.0" width="170.0" height="78.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="505.0" y="48.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Format the</text>
<text x="505.0" y="71.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">confirmation</text>
<rect x="615.0" y="15.0" width="245.0" height="78.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="737.5" y="48.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">notifications.send</text>
<text x="737.5" y="71.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">(reservation)</text>
<path d="M200.0,54.0 L225.0,54.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-failure-arr)"/>
<path d="M395.0,54.0 L420.0,54.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-failure-arr)"/>
<path d="M590.0,54.0 L615.0,54.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-failure-arr)"/>
<rect x="10.0" y="215.0" width="265.0" height="110.0" rx="18" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="142.5" y="253.6" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Returns normally</text>
<text x="142.5" y="276.1" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle"></text>
<text x="142.5" y="298.6" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">the confirmation</text>
<rect x="300.0" y="215.0" width="295.0" height="110.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="447.5" y="243.9" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">NotificationException</text>
<text x="447.5" y="265.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle"></text>
<text x="447.5" y="286.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">confirmation + suffix</text>
<text x="447.5" y="307.7" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">record retained, no retry</text>
<rect x="620.0" y="215.0" width="240.0" height="110.0" rx="8" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="2"/>
<text x="740.0" y="243.9" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">Any other exception</text>
<text x="740.0" y="265.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle"></text>
<text x="740.0" y="286.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">propagates; the record</text>
<text x="740.0" y="307.7" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#46586d" text-anchor="middle">is already stored</text>
<path d="M737.0,93.0 L737.0,150.0 L142.0,150.0 L142.0,215.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-failure-arr)"/>
<path d="M737.0,150.0 L447.0,150.0 L447.0,215.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-failure-arr)"/>
<path d="M737.0,150.0 L737.0,215.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-failure-arr)"/>
<text x="437.0" y="134.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">one attempt per accepted request</text>
</svg>
</div>
<!--/svg-->

---

## Why the Rule Matters

* An author-chosen **teaching rule**. Another application might choose differently, but must make storage and communication consequences explicit.
* A result that just says "failed" can encourage callers **to repeat a reservation request that already succeeded**.
* Repeating it here normally gives an **overlap rejection**. It is **not** a notification retry.
* There is **no queue or worker**: do not call a failed notification "pending".

---

## Invocation Is Not Delivery

* The coordinator attempts the sender **once per successful reservation call**: a local control-flow fact, **not an exactly-once delivery guarantee**.
* A future remote sender might deliver and then fail before confirming. **Retrying could duplicate the delivery.**
* Even the console may **partially write** before reporting an error.

---

## What the Coordinator Catches

* It catches **that specific exception**.
* Unexpected programming failures are **not converted into apparent success**.
* Such failures may still occur **after storage**. The example does not claim transactional atomicity across formatting, storage and output.
* A richer result model and reliable delivery design belong to later integration work.

---

## Acceptance Examples Before Refactoring (1 of 2)

| Example | Reservation result | Notification |
|---|---|---|
| Eligible available request | Exact confirmation; one record stored | One accepted record supplied to the sender |
| Same-item overlap | Existing rejection; records unchanged | No call |
| Invalid duration | Existing rejection; records unchanged | No call |

---

## Acceptance Examples Before Refactoring (2 of 2)

| Example | Reservation result | Notification |
|---|---|---|
| Invalid identifier | Existing exception; records unchanged | No call |
| Expected output failure after acceptance | Confirmation plus failure suffix; record retained | One attempt; no automatic retry |
| Repeat of the accepted request | Overlap rejection | No second attempt |

* These constrain the feature **whether assembly is manual or container-based**.

---

# 6.4 DIP
### Who owns the abstraction?

---

## DIP: Source Dependency Direction

* DIP separates **higher-level policy** from **changing implementation details** through abstractions.
* The coordinator names `NotificationSender`, **an application-owned role**. Concrete outputs implement it.
* The contract does **not import a provider's SDK type** or inherit its configuration vocabulary.
* At runtime the coordinator **still calls a concrete object**. DIP does not reverse that call: it changes **what the source needs to know** and **which side defines the abstraction**.

---

## Figure 6.1: Source-Level Dependencies

<!--svg:ch06-fig61-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 355" role="img" aria-label="Source-level dependencies for the notification role: ReservationApplication creates the coordinator and the console sender; the coordinator holds the NotificationSender role; ConsoleNotificationSender and RecordingNotificationSender realise it." style="display:block;width:100%;height:calc(var(--u) * 35.50);margin:0 auto">
<defs><marker id="ch06-fig61-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-fig61-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-fig61-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-fig61-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-fig61-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="30.0" width="240.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,66.0 L12.0,36.0 Q12.0,32.0 16.0,32.0 L244.0,32.0 Q248.0,32.0 248.0,36.0 L248.0,66.0 Z" fill="#e6eef6"/>
<text x="130.0" y="55.0" font-size="17" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReservationApplication</text>
<rect x="10.0" y="185.0" width="240.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,221.0 L12.0,191.0 Q12.0,187.0 16.0,187.0 L244.0,187.0 Q248.0,187.0 248.0,191.0 L248.0,221.0 Z" fill="#e6eef6"/>
<text x="130.0" y="210.0" font-size="17" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReservationCoordinator</text>
<rect x="350.0" y="160.0" width="355.5" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M352.0,216.0 L352.0,166.0 Q352.0,162.0 356.0,162.0 L699.5,162.0 Q703.5,162.0 703.5,166.0 L703.5,216.0 Z" fill="#e6eef6"/>
<text x="527.8" y="179.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="527.8" y="201.0" font-size="17" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">NotificationSender</text>
<line x1="350.0" y1="216.0" x2="705.5" y2="216.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="362.0" y="238.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+send(Reservation reservation) void</text>
<rect x="350.0" y="30.0" width="270.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M352.0,66.0 L352.0,36.0 Q352.0,32.0 356.0,32.0 L614.0,32.0 Q618.0,32.0 618.0,36.0 L618.0,66.0 Z" fill="#e6eef6"/>
<text x="485.0" y="55.0" font-size="17" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ConsoleNotificationSender</text>
<rect x="350.0" y="305.0" width="290.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M352.0,341.0 L352.0,311.0 Q352.0,307.0 356.0,307.0 L634.0,307.0 Q638.0,307.0 638.0,311.0 L638.0,341.0 Z" fill="#e6eef6"/>
<text x="495.0" y="330.0" font-size="17" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">RecordingNotificationSender</text>
<path d="M250.0,48.0 L350.0,48.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch06-fig61-open)"/>
<text x="300.0" y="34.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">creates</text>
<path d="M130.0,66.0 L130.0,185.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch06-fig61-open)"/>
<text x="148.0" y="130.5" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">creates</text>
<path d="M250.0,203.0 L350.0,203.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-fig61-open)"/>
<text x="300.0" y="189.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">notifies</text>
<path d="M470.0,66.0 L470.0,160.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch06-fig61-tri)"/>
<path d="M470.0,305.0 L470.0,251.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch06-fig61-tri)"/>
<text x="765.0" y="70.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#b4762e" text-anchor="middle">Every “creates” arrow</text>
<text x="765.0" y="92.0" font-size="16" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#b4762e" text-anchor="middle">starts at the application.</text>
<text x="765.0" y="312.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">The policy map and the</text>
<text x="765.0" y="332.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">formatter are built there too.</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 6.1

* **Solid arrows** are associations: the coordinator holds a `NotificationSender`, a `ConfirmationFormatter` and a `Map<BorrowerCategory, BorrowingPolicy>`.
* **Dashed lines with a hollow triangle** are realisations.
* **Dashed arrows labelled "creates"** show which class's source names which concrete class.
* The recorder is an **alternative implementation**, not an additional mandatory destination: the application creates only the console sender.

---

## Compare With Figure 5.1

* There, two "creates" arrows ran **from the coordinator** to the concrete policy classes.
* Here, **every "creates" arrow starts at `ReservationApplication`**.
* The coordinator's outgoing arrows end at **roles**, apart from the concrete `ConfirmationFormatter`, which stays concrete on purpose.
* The change in arrow direction is **visible evidence that its source no longer chooses its environment**.

---

## Source Knowledge, Not Time Order

* The arrows show **source-level knowledge**, not time order.
* The composition root knows the concrete console implementation because **choosing it is the root's job**.
* The files still use the unnamed Java package. Contract ownership is a **design decision**, not a build-enforced boundary. Chapter 10 organises larger application boundaries.

---

## DI Can Exist Without DIP

* The coordinator receives `ConsoleNotificationSender` through its constructor: that **is** dependency injection. Someone else supplies the collaborator.
* It still **depends on the concrete provider type**: the boundary is not yet inverted.
* Conversely, a field typed `NotificationSender` assigned `new ConsoleNotificationSender(...)` **inside** the coordinator uses an abstraction while keeping concrete construction knowledge. This is the intermediate defect.

---

## Two Different Questions

* **What type of behaviour does the client require?** (the role: DIP, ISP)
* **Who supplies the object?** (injection)
* The final design uses the small application contract **and** passes the implementation from the application root.
* They support each other but **answer different questions**.

---

## A Preview: An Outside Data Source Behind a Contract

```java
/** Empty means absent or inactive, never a provider outage. */
@FunctionalInterface
public interface BorrowerDirectory {
    Optional<Borrower> find(String borrowerId);
}
```

* Chapter 8 builds this equipment-directory contract. **Not part of this checkpoint.**
* Empty means "no such active borrower"; an outage is a **different outcome** (an exception); the contract uses the **application's own types**.

---

## Not Every Concrete Dependency Is Harmful

* The coordinator still constructs accepted `Reservation` and `LoanPeriod` values and uses an in-memory list. Creating a **small domain value** differs from selecting an **environmental output provider**.
* The concrete `ConfirmationFormatter` is **supplied in the constructor**, but has **no interface**: a substitutable formatting role has not been required.
* Using Java's `Map` interface does not itself demonstrate DIP. The decision is that **policy mappings are assembled outside** the coordinator.

---

# 6.5 Constructor Injection and Composition Roots
### Make required collaborators visible

---

## The Completed Constructor

```java
public ReservationCoordinator(
        Map<BorrowerCategory, BorrowingPolicy> policies,
        ConfirmationFormatter formatter,
        NotificationSender notifications) {
    this.policies = Map.copyOf(Objects.requireNonNull(policies, "policies"));
    for (BorrowerCategory category : BorrowerCategory.values()) {
        if (!this.policies.containsKey(category)) {
            throw new IllegalArgumentException("Missing policy: " + category);
        }
    }
    this.formatter = Objects.requireNonNull(formatter, "formatter");
    this.notifications = Objects.requireNonNull(notifications, "notifications");
}
```

---

## What the Constructor Checks

* Null values, and **an entry for every current borrower category**.
* `Map.copyOf` produces an **unmodifiable map** and rejects null keys or values. A caller cannot change the coordinator's mapping by editing the original map later.
* The copy is **shallow**: it does not clone the policy objects. The supplied policies are stateless; a mutable or dishonest policy would not be made safe.
* Missing configuration **fails at construction**, not halfway through a request.

---

## The Request, Now With Notification

```java
reservations.add(reservation);
String confirmation = formatter.format(reservation);
try {
    notifications.send(reservation);
} catch (NotificationException failure) {
    return confirmation + " Notification failed; reservation retained.";
}
return confirmation;
```

* `policies.get(category)` replaces the former category `switch`.

---

## Assemble Once at the Boundary

```java
public static ReservationCoordinator create(NotificationSender sender) {
    return new ReservationCoordinator(
            Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                   BorrowerCategory.STAFF, new StaffReservationRules()),
            new ConfirmationFormatter(), sender);
}
```

* `main` chooses a **console sender with a supplied stream** and starts the demonstration.
* A check chooses a recorder instead.

---

## A Check Chooses a Recorder

```java
RecordingNotificationSender inbox = new RecordingNotificationSender();
ReservationCoordinator coordinator = ReservationApplication.create(inbox);
```

* The check can later inspect `inbox.received()` because it **retained the concrete reference**.
* The coordinator **only sees the sender role**.
* Replaceability without a mocking library. Chapter 7 develops the vocabulary of test doubles.

---

## Figure 6.2: The Objects Built at Run Time

<!--svg:ch06-fig62-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 370" role="img" aria-label="Figure 6.2, the objects assembled at run time: the application entry point creates the policy map, the console sender, the formatter and the coordinator, and passes the first three to the coordinator&#x27;s constructor." style="display:block;width:100%;height:calc(var(--u) * 37.00);margin:0 auto">
<defs><marker id="ch06-fig62-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-fig62-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-fig62-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-fig62-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch06-fig62-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="140.0" width="190.0" height="84.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="105.0" y="176.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">Application</text>
<text x="105.0" y="199.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#ffffff" text-anchor="middle">entry point</text>
<rect x="330.0" y="12.0" width="250.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="455.0" y="38.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Student and staff</text>
<text x="455.0" y="59.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">policy map</text>
<rect x="330.0" y="150.0" width="250.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="455.0" y="176.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Console sender</text>
<text x="455.0" y="197.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">instance</text>
<rect x="330.0" y="290.0" width="250.0" height="62.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="455.0" y="316.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">Confirmation</text>
<text x="455.0" y="337.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">formatter</text>
<rect x="670.0" y="140.0" width="190.0" height="84.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="765.0" y="176.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Coordinator</text>
<text x="765.0" y="199.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">instance</text>
<path d="M200.0,160.0 L330.0,43.0" fill="none" stroke="#b4762e" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch06-fig62-arr)"/>
<path d="M200.0,182.0 L330.0,181.0" fill="none" stroke="#b4762e" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch06-fig62-arr)"/>
<path d="M200.0,204.0 L330.0,321.0" fill="none" stroke="#b4762e" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch06-fig62-arr)"/>
<path d="M100.0,224.0 L100.0,366.0 L765.0,366.0 L765.0,224.0" fill="none" stroke="#b4762e" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch06-fig62-arr)"/>
<text x="215.0" y="358.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="middle" font-style="italic">creates</text>
<text x="264.0" y="100.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#b4762e" text-anchor="middle" font-style="italic">creates</text>
<path d="M580.0,43.0 L720.0,43.0 L720.0,140.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-fig62-arr)"/>
<path d="M580.0,181.0 L670.0,182.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-fig62-arr)"/>
<path d="M580.0,321.0 L720.0,321.0 L720.0,224.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch06-fig62-arr)"/>
<text x="616.0" y="36.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">passed to the</text>
<text x="616.0" y="52.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">constructor</text>
</svg>
</div>
<!--/svg-->

---

## Two Views, Not One

* **Figure 6.1** says which classes **know about** which. **Figure 6.2** says which objects were **wired to** which.
* The sender also receives its own formatter and output stream, left out for readability.
* **Neither shows the order of calls**: the coordinator checks eligibility and conflicts, stores, formats, then calls the sender already supplied.
* Do **not** read event order from either diagram.

---

## The Composition Root

* A **composition root** is the small application-entry area where concrete collaborators are assembled.
* It may call helper factory methods. They do **not** become a service locator merely because they are static.
* What matters: the coordinator **is passed its dependencies** and does **not** call back into a global registry to find them.

---

## The Constructor Migration, Honestly Stated

* The no-argument coordinator constructor is **removed**. Callers must supply dependencies, normally through `ReservationApplication.create`.
* The completed source is **not a drop-in constructor-compatible replacement** for Chapter 5.
* Existing checks and demos are migrated **only at their construction expressions**; their reservation assertions stay the same.
* Claiming every old source line is unchanged would be inaccurate.

---

## What Stays the Same

* The four-argument `reserve` still means **student borrowing**; the explicit category overload still uses the trusted category supplied.
* Student and staff limits, date boundaries, count behaviour and rejection messages remain as before on ordinary paths.
* The **new notification side effect and failure suffix** are separate feature behaviour.

---

## Constructor Injection vs. Later Setters

* Required dependencies fit **constructor injection**: an object cannot be used before they are supplied.
* With later setters, the program may contain **an unusable coordinator**, and every operation may need to ask whether configuration has happened.
* Setters are not universally wrong: optional or intentionally replaceable runtime collaborators have a different lifecycle. This coordinator has **no requirement to swap its sender** while processing.

---

## A Long Constructor

* A very long constructor can expose a class with **too many responsibilities**, but parameter count alone does not prove it.
* Do not hide ten unrelated services inside a **generic context object** to shorten the signature.
* The dependencies would still exist, with **less visibility**.

---

# 6.6 IoC and DI Containers
### Registration, resolution, lifetime

---

## Distinguish the Terms

* **Dependency injection:** supplying collaborators from outside an object.
* **Inversion of control:** another component controls some aspect of execution or assembly the object would otherwise control.
* **DI container:** a tool that uses registration or configuration to assemble and often manage objects.
* The manual coordinator already uses DI. A container **automates repeated assembly**; it cannot decide whether the contract or failure policy is right.

---

## Terms and the Question Each Answers (1 of 2)

| Term | Question answered in this example |
|---|---|
| DIP | Does the coordinator depend on the application's notification role rather than a provider detail? |
| DI | Who supplies the sender, formatter and policy mapping? |
| IoC | Which component controls assembly or later calls into application code? |

---

## Terms and the Question Each Answers (2 of 2)

| Term | Question answered in this example |
|---|---|
| DI container | What mechanism resolves registrations and manages selected object lifetimes? |
| Service locator | Does application code fetch collaborators from a registry rather than receive them explicitly? |

---

## The Educational Container

* `DemoContainer`, in `ContainerWalkthrough.java`: **isolated from the cumulative application**, single-threaded.
* It **registers a provider function** for a type and **lazily creates one instance** of each registered type.
* It **caches** those instances, **reports a missing binding** and **detects a construction cycle**.
* `ReservationCoordinator` has **no container import, field or lookup call**.

---

## The Container

```java
static final class DemoContainer {
    private final Map<Class<?>, Supplier<?>> providers = new HashMap<>();
    private final Map<Class<?>, Object> instances = new HashMap<>();
    private final Set<Class<?>> constructing = new HashSet<>();

    public <T> void bind(Class<T> type, Supplier<? extends T> provider) { /* ... */ }
    public <T> T get(Class<T> type) {
        if (instances.containsKey(type)) return type.cast(instances.get(type));
        Supplier<?> provider = providers.get(type);
        if (provider == null)
            throw new IllegalArgumentException("Missing binding: " + type.getSimpleName());
        if (!constructing.add(type))
            throw new IllegalStateException("Dependency cycle: " + type.getSimpleName());
        /* run the provider, cache, return */
    }
}
```

---

## The Registrations

```java
container.bind(ConfirmationFormatter.class, ConfirmationFormatter::new);
container.bind(NotificationSender.class, RecordingNotificationSender::new);
container.bind(ReservationCoordinator.class, () -> new ReservationCoordinator(
        Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
               BorrowerCategory.STAFF, new StaffReservationRules()),
        container.get(ConfirmationFormatter.class),
        container.get(NotificationSender.class)));
```

* The provider calls the **same ordinary constructor**. Only configuration code uses the container.

---

## Trace the First Resolution

1. Registration **stores a provider without running it**.
2. The first coordinator resolution **runs its provider**, which requests the formatter and sender.
3. Those providers run; their instances are passed to the constructor.
4. The coordinator is **cached**.
5. A **second resolution returns the same coordinator**: the reservation stored through the first reference is visible through the second.

---

## Lifetime Is a Design Decision

* Sharing the coordinator means sharing its **in-memory reservation list**.
* A container does **not** make that list thread-safe.
* A **fresh coordinator per request** would discard earlier reservations unless storage were shared elsewhere.
* **Neither lifetime is automatically correct** for a future server application.

---

## Configuration Failures

```text
Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Repeated resolution shares the same coordinator and one reservation.
Missing binding: NotificationSender
Dependency cycle: NotificationSender
```

* A missing registration and a cycle fail with **identifiable configuration errors**, not business-rule rejections.
* Zero exit status means the walkthrough **observed the intended cases**.

---

## The Container's Limits Are Deliberate

* No reflection, annotation scanning, concurrent resolution, scopes beyond one cached instance per type, or resource cleanup.
* Do **not** extend it into a home-grown production framework.
* Its purpose: expose **registration, resolution and lifetime** in ordinary Java.
* Real frameworks (such as Spring's IoC container) supply much more machinery. The manual graph gives you a basis for **reading such configuration**.

---

## Whichever Container You Use

* Identify its **registrations**, **supplied constructor arguments** and **instance lifetimes** before adding annotations.
* The library or framework **name should not replace an explanation of the object graph**.
* A library container arrives with **libraries of its own**, which the plain `javac` gate does not manage. The lab uses the educational container, so everything needed is in the chapter and companion.

---

# 6.7 Costs of Abstraction
### Give each boundary a job

---

## Each Boundary Earns Its Place

* The **notification interface** earns its place: the same client needs two outputs and a predictable failure boundary.
* The **borrowing-policy interface** already expresses a genuine variation.
* The **formatter remains concrete**. **No interface** on immutable `Reservation` or `LoanPeriod`.
* The root may know concrete classes. Hiding every choice behind another factory makes the program **hard to trace without protecting any additional change**.

---

## The Policy Map Has a Cost Too

* It removes a category switch from the coordinator but adds a **configuration invariant**: every category must have a non-null policy.
* Constructor validation makes that cost visible.
* A design explanation should include it, rather than presenting fewer conditionals as an unconditional improvement.

---

## Recognise a Disguised Dependency

* An injected `ApplicationContext` with arbitrary lookups **hides all the coordinator's real needs**. A method calling `context.get("mail")` is still **locating its own collaborator**.
* An interface whose `send` needs server addresses, passwords and transport-specific objects **moves provider setup into every caller**.
* The interface exists syntactically; the application is still **coupled to implementation details**.

---

## Concrete Review Questions

* Can I **choose the recorder** without editing reservation logic?
* Can I **see the required dependencies at construction**?
* Can a provider-specific change **stay at the boundary**?
* Can I **explain the state after expected output failure**?
* These reveal more than counting interface declarations.

---

## What the Chapter Has Not Solved

* An in-memory, sequential teaching application.
* No authoritative borrower categories, persistent notification history, retry queue, remote delivery, cancellation or availability enquiry.
* It does not implement the whole MVP reservation-and-loan flow.
* The new structure makes selected changes and tests easier. **It does not manufacture those features.**

---

# 6.8 AI in Practice: An Interface That Hides Little
### Does the refactoring separate anything?

---

## Activity Frame (1 of 2)

| Element | For this activity |
|---|---|
| Engineering objective | Judge whether a generated refactoring really separates configuration and policy from the reservation workflow |
| Input | The coupled coordinator from 6.1, the notification requirement and Figure 6.1 |
| Permitted scope | Evaluate the proposal and draw a corrected object graph; do not apply it wholesale |

---

## Activity Frame (2 of 2)

| Element | For this activity |
|---|---|
| Independent checks | The coordinator's source (which concrete classes does it name?), the recorder-based checks, the failure case |
| Accept or reject | A verdict with a concrete reason for each proposal, then a corrected constructor |
| No-account route | The fixture is sufficient |

---

## The Fixture (1 of 2)

**Author-written fictional AI output.**

> Add `NotificationSender` and type the coordinator field with it. Inside the coordinator constructor, read the provider settings and create `ConsoleNotificationSender`. Add `configure`, `exportHistory` and `deleteBorrower` to the same interface so it can support future features.

---

## The Fixture (2 of 2)

> Catch every runtime exception and still return the ordinary confirmation. Pass a global container into the coordinator so future dependencies can be found when needed. The new interface means DIP and DI are both complete.

* Find where **configuration still occurs**, what the client **actually needs**, and what a caller would **learn about failure**.
* Explain **receiving a sender** versus **receiving a registry**.

---

## Model Critique (1 of 3)

| Fixture claim or change | Verdict | Reason |
|---|---|---|
| Type the field as `NotificationSender` | Useful but insufficient alone | It expresses a role, but concrete construction can remain |
| Read provider settings inside the coordinator | Reject | Environmental configuration still changes the workflow's source |
| Construct the console sender inside the coordinator | Reject for the final design | The caller cannot select a recorder without editing the client |

---

## Model Critique (2 of 3)

| Fixture claim or change | Verdict | Reason |
|---|---|---|
| Add configure/export/delete to the sender role | Reject without a client need | They couple this client to unrelated capabilities |
| Catch every runtime exception, return ordinary confirmation | Reject | It hides programming defects; expected failure becomes indistinguishable from success |

---

## Model Critique (3 of 3)

| Fixture claim or change | Verdict | Reason |
|---|---|---|
| Inject a global container for future lookups | Reject | Real required collaborators become hidden behind a registry |
| Declare DIP and DI complete because an interface exists | Reject | Contract ownership, provider knowledge and actual assembly must be inspected |

* **Corrected answer:** three explicit constructor parameters, the application-owned sender contract, two implementations, external assembly; the stated notification timing and failure outcome; the constructor migration named; the still-limited in-memory model.

---

## Independent Verification

* **Inspect concrete constructor calls.**
* **Search the coordinator** for provider and container references.
* **Run with the recorder.**
* **Observe the failure case.**
* A second model agreeing with the first is **not a substitute** for those observations.

---

# 6.9 Common Mistakes
### Eight misleading beliefs

---

## Mistakes 1 to 3

| Mistake | Why it is misleading | Better action |
|---|---|---|
| An interface-typed field proves DIP | Concrete construction or provider-specific types may remain | Inspect the actual source dependencies |
| DI means a framework | Ordinary constructors can receive dependencies | Explain assembly before adding tooling |
| Every class needs an interface | Many stable values have no variation | Name the client need and change pressure |

---

## Mistakes 4 to 6

| Mistake | Why it is misleading | Better action |
|---|---|---|
| A sender must expose provider administration | The coordinator does not need those operations | Keep the application role narrow |
| A container singleton is thread-safe | Lifetime and concurrent access are separate | Inspect mutable state and execution model |
| Notification failure means reservation failure | Storage may already have succeeded | State the partial-success outcome explicitly |

---

## Mistakes 7 and 8

| Mistake | Why it is misleading | Better action |
|---|---|---|
| One call means exactly-once delivery | Output may fail after partial or remote effects | Describe only the guarantee implemented |
| Old checks passed, so all compatibility is preserved | Construction changed and notification adds effects | Separate API migration from retained domain behaviour |

---

# 6.10 Practical Activity: Assemble a Replaceable Output
### Nine steps

---

## Input and Demonstration

* **Input:** Chapter 5's exit code, this chapter's requirement and companion listings. Java 17, the plain-Java gate. The container walkthrough is separate from the application.
* **Demonstration:** compare the Chapter 5 baseline, the coupled notification version and the injected version. **Point to every concrete provider choice** and explain which belongs at the entry point.
* **Guided practice:** inject a recorder, accept one reservation, reject an overlapping request and inspect both **stored reservations** and **recorded notifications**; then use an output that throws the documented exception.

---

## Independent Work: Steps 1 to 3

1. **Define the sender role** and identify at least two operations it should not contain.
2. **Move output construction and category-to-policy mapping to the composition root.** Require valid collaborators in the constructor.
3. **Migrate existing caller construction** while preserving existing reservation assertions.

---

## Independent Work: Steps 4 to 6

4. Demonstrate **both console and recording outputs** with the same coordinator implementation.
5. Verify **no notification on rejection**, **one attempt after acceptance**, and the chosen **failure outcome without automatic retry**.
6. Draw **separate source-dependency and object-assembly views**, labelling what each arrow means. In the source view, check that **every "creates" arrow starts at the application class**.

---

## Independent Work: Steps 7 to 9

7. Run the **educational container walkthrough** and explain shared state, missing registration and cycle detection.
8. **Review the change** and write a rationale for every new boundary. Retain real review findings.
9. On your **Team project**, find **one environment or provider choice** that a class constructs for itself (an output, storage, an external service, configuration). Sketch where it would be assembled instead, using both views.

---

## Expected Output and Completion

* **Output:** injected notification contract; two implementations; explicit assembly code; migrated and additional checks; the two diagrams; failure-policy explanation; a short rationale; the step 9 sketch.
* **Complete when:** provider substitution **requires no edit to the reservation algorithm**; setup failures are **distinguishable from reservation rejections**; old rule expectations remain valid; expected notification failure **preserves the record and reports its outcome accurately**.
* **Optional extension:** compare the supplied map with a dedicated policy-resolver in a design sketch. Explain the client benefit before adding another interface.

---

## Review Evidence Worth Inspecting (1 of 2)

| Review concern | Evidence worth inspecting |
|---|---|
| Role is client-specific | Coordinator uses only the sender operation and the domain record |
| Provider choice is external | Concrete output construction is in assembly code, not the coordinator |
| Valid configuration | Null and missing-policy failures occur before request processing |
| Mapping is stable | Editing the caller's map does not rewire an existing coordinator |

---

## Review Evidence Worth Inspecting (2 of 2)

| Review concern | Evidence worth inspecting |
|---|---|
| Existing behaviour | Migrated setup with unchanged reservation assertions passes |
| Feature effects | Accepted record supplied once; rejection causes no send; expected failure retains state |
| Lifetime | Repeated container resolution shares the same coordinator |
| Claims are bounded | No claim of email delivery, atomic messaging, thread safety or a hosted run |

---

## What the 28 New Checks Establish

* The accepted result, **one recorded notification**, the exact accepted record, and **no notification** on conflict, duration rejection or invalid identifiers.
* A controlled **expected failure after storage**: the suffix, **record retention**, no automatic retry.
* **Two further checks**: a sender throwing `IllegalStateException` propagates, with the record already stored. Without them, widening the catch to `RuntimeException` would pass every check.
* Constructor checks for **null dependencies and missing category configuration**; a mutable input map changed after construction does not rewire the coordinator.

---

## Do the Checks Detect Faults? (1 of 4)

| Fault | Result |
|---|---|
| Notification sent before the record is stored | Caught: `notification failure retains accepted record` |
| `catch (NotificationException)` widened to `catch (RuntimeException)` | Caught: `unexpected sender failure is not swallowed` |
| Failure suffix text changed | Caught: `explicit partial-success result` |
| One retry added after a failed send | Caught: `one attempt and no automatic retry` |

---

## Do the Checks Detect Faults? (2 of 4)

| Fault | Result |
|---|---|
| Sender called twice on success | Caught: `one notification per accepted request` |
| `Map.copyOf` removed | Caught: `caller map mutation cannot rewire coordinator` |
| Missing-category check removed | Caught: `missing staff policy` |
| Null sender check removed | Caught: `null sender` |

---

## Do the Checks Detect Faults? (3 of 4)

| Fault | Result |
|---|---|
| Null formatter check removed | Caught: `null formatter` |
| Policy lookup always uses the student policy | Caught: `staff confirmation with new limit` |
| Console `checkError()` test removed | Caught: `console reports expected output failure` |
| Console prefix `Notice:` changed | Caught: `console implementation uses supplied stream` |

---

## Do the Checks Detect Faults? (4 of 4)

| Fault | Result |
|---|---|
| Recorder returns its mutable list | Caught: `inbox snapshot unmodifiable` |
| Factory ignores the supplied sender | Caught: `one notification per accepted request` |

* All fourteen faults caught.
* The checks do **not** prove thread safety, durable output or remote delivery.

---

# 6.11 Review Questions
### Concept and diagnosis

---

## Concept Questions

1. Why does `NotificationSender` omit the recorder's `received()` method?
2. How can constructor injection be present while the intended DIP boundary is still missing?
3. What does the composition root know that the coordinator should not know?
4. Why can sharing a coordinator through a container change application behaviour even when its methods are unchanged?

---

## Diagnosis Questions

5. A coordinator catches a sender failure, deletes the accepted reservation, and returns "Rejected". The sender may already have printed or delivered a notice. Diagnose the inconsistent outcome and compare it with this chapter's explicit failure rule.
6. A constructor copies a map of policies. A reviewer says this proves that policy behaviour can never change. Explain what the copy protects and what still depends on the policy objects' contracts.

---

## Guidance: Questions 1 and 2

1. The coordinator **submits** an accepted record; it does not inspect output history. The recorder's inspection API serves another client, such as check code. Adding it would force the console implementation to **invent a history** it does not need.
2. A constructor taking `ConsoleNotificationSender` **uses DI** but depends on that concrete provider. A contract copied from a provider SDK keeps provider coupling despite its interface name. **Define the application role and inject a conforming implementation.**

---

## Guidance: Questions 3 and 4

3. The root knows **which category maps to which concrete policy**, which sender is selected, which stream it uses, and how formatters are constructed. The coordinator knows **roles and when to invoke them**.
4. Two resolutions of one cached coordinator **share the same reservations**. Two fresh coordinators have separate empty lists and can each accept what looks like the first reservation. **The method source is identical; the assembled graph changes behaviour.**

---

## Guidance: Questions 5 and 6

5. The output **may already have occurred**, so deleting cannot undo it: a notice for a record that no longer exists. "Rejected" hides the earlier acceptance and may prompt a repeat. This chapter **retains the record and reports the output failure**. Another policy needs an explicit consistency design, not a catch block pretending to reverse external effects.
6. The copy fixes **associations between categories and policy references**. It is **shallow**: an externally held policy could still change internally if its implementation permitted it. The stateless policy contract provides the further stability.

---

# 6.12 Transfer Challenge
### A document conversion service

---

## Transfer Challenge

A document conversion service validates a request, converts a file and sends a completion notice. A desktop demonstration displays notices in a window; an automated run records them in memory.

* Define a **client-specific notification role**.
* Identify the **assembly boundary** and what **stays in the conversion workflow**.
* Decide what callers observe if **conversion succeeds but notification fails**.
* Draw a dependency diagram; give **two acceptance examples** separating conversion state from notification state.
* Synthetic filenames only; no assumed retry queue.

---

## Transfer Guidance

* A `CompletionNotifier` role taking an **immutable successful-conversion result**. It does not validate, convert or administer accounts.
* The workflow decides when conversion has succeeded. The **application root** selects the desktop or recording notifier.
* **Failure rule:** keep the converted file; return a result separating conversion success from notification failure.

| Example | Conversion state | Notification state |
|---|---|---|
| Valid input converts | One output produced | One completion result submitted |
| Conversion fails | No success reported | No notice submitted |
| Conversion succeeds, notifier fails | Output retained | Failure reported separately |

---

# 6.13 Quiz 1 Revision Pointers
### Chapters 2 to 5

---

## What Quiz 1 Covers

* Quiz 1 is held in **Week 5**, but its stated coverage is **Weeks 1 to 4**: OO foundations, Agile practices and user stories, Git workflows, and the first SOLID principles.
* **Revise Chapters 2 to 5.** Do not treat all of Chapter 6 as newly included quiz content.
* Follow the module leader's confirmed guidance. These pointers add no assessment rules and predict no questions.

---

## Revision Focus (1 of 2)

| Chapter | Revision focus |
|---|---|
| 2 | Encapsulation, responsibilities, cohesion/coupling, composition and inheritance, UML class diagrams, Git history, branches and small reviewed changes |
| 3 | Agile values in decisions, iterative/incremental delivery, Scrum/Kanban distinctions, stories, acceptance criteria and Definition of Done |

---

## Revision Focus (2 of 2)

| Chapter | Revision focus |
|---|---|
| 4 | Vision and scope, vertical slicing, capacity-aware planning, review workflow and meaningful CI evidence |
| 5 | SRP, OCP, behavioural contracts, LSP counterexamples and protected refactoring |

---

# Summary and Next Chapter
### What to carry forward

---

## Summary

* A useful interface describes **a client's needed role**.
* **DIP** concerns the direction and ownership of dependencies; **DI** supplies collaborators from outside; a **container** is one possible assembly mechanism.
* The running example now makes provider and policy choices **explicit at its entry boundary** and defines the **observable result of expected notification failure**.

---

## Where the Checkpoint Stands

* Local **console and recording** outputs.
* **Explicit construction** and **28 new checks**.
* Existing reservation rules remain covered by their previous expectations, with **caller setup migrated**.

---

## Next: Chapter 7

* **Test design.**
* **Controlled substitutes** (test doubles).
* A complete **red-green-refactor** cycle.

---

## Sources and Further Reading

1. **Martin:** *Design Principles and Design Patterns* (2000); *A Little Architecture* (2016).
2. **Fowler:** *Inversion of Control Containers and the Dependency Injection Pattern* (2004); *Inversion of Control* (2005).
3. **Oracle:** Java SE 17 `Map` and `PrintStream`.
4. **Spring:** *Introduction to the Spring IoC Container and Beans.*
5. **Martin:** *Agile Software Development*, 2002.

* Full references and links are in the chapter text.
