---
title: "Chapter 10: From Classes to Application Structure"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 100
type: slides
layout: page
---

# Chapter 10: From Classes to Application Structure
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **10.1 Why class-level design is insufficient**
  * Responsibilities exist at more than one scale.
* **10.2 Layers and separation of concerns**
  * Eight packages, each with a reason.
* **10.3 Presentation, application, domain and infrastructure**
  * Where an outside collaborator sits.
* **10.4 Dependency direction and its check**
  * Source dependencies, runtime calls and a compiled dependency check.
* **10.5 Package design: cohesion, coupling and stability**
  * CCP, CRP, REP, ADP, SDP, SAP and a worked placement comparison.

---

## Chapter Roadmap (2 of 3)

* **10.6 Entities and value objects**
  * Identity, immutability and Java equality are three different things.
* **10.7 Repositories and services**
  * The smallest useful storage contract.
* **10.8 A small architecture decision**
  * ADR-010.
* **10.9 Peer review and Milestone 3**

---

## Chapter Roadmap (3 of 3)

* **10.10 AI in practice:** verify a dependency review.
* **10.11 Common mistakes**
* **10.12 Practical activity**
  * Book project B1 to B6; Team project T1 to T5.
* **10.13 Review and transfer**
  * A clinic appointment application.
* **Summary and next chapter**
  * Chapter 11: refactoring and legacy code.

---

## Learning Outcomes (1 of 2)

By the end of this chapter, you should be able to:

1. **Assign existing responsibilities** to presentation, application, domain and infrastructure code.
2. **Distinguish runtime calls from source-code dependency direction.**
3. **Explain entity identity, immutability and value equality** without conflating them.
4. **Locate a focused repository contract** and its implementation.

---

## Learning Outcomes (2 of 2)

5. **Restructure a use case** while checking its observable behaviour and compatibility limits.
6. **Record an architecture decision** and prepare evidence for peer review and Milestone 3.
7. **Compare two package designs** using cohesion, coupling and stability, and read dependency counts without treating them as a measure of quality.

---

## Module Connection and Starting Point

* Supports **LO2 and LO6**; **Milestone 3** preparation. Readings: Martin's **principles of package design** and selected chapters of Evans's **domain-driven design**.
* **Starting point:** Chapter 9's tested Java 17 project, including the stronger assertions added when it was reviewed.
* The completed checkpoint **preserves its use-case results and earlier demonstrations**.
* **Package names, imports, launcher names and direct coordinator construction change**: not a claim of source or binary compatibility.

---

## Milestone 3 Checklist (1 of 2)

Milestone 3 falls in this week: design patterns and layered architecture, with a demonstration and a retrospective. On your **Team project**:

1. A **design pattern from Chapters 8 and 9** used where it removes a real problem, and **one place you declined** to use one.
2. A **compact package diagram** saying which packages may depend on which.
3. **One restructuring change**, with moves kept separate from logic changes.
4. **Passing checks**, including a dependency check or a documented review of imports.

---

## Milestone 3 Checklist (2 of 2)

5. A short **architecture decision record** with alternatives, consequences and a revisit trigger.
6. **Real peer review** of that change, with the feedback addressed.
7. A **demonstration and a retrospective** with a next action.
8. A statement of **what the architecture does not do**.

* **Start with items 2 and 5**, which need no code.
* The approved Milestone 3 instructions decide what is submitted. This list is **preparation, not a rubric**.

---

## Reading Route

* **Core reading:** 10.1 to 10.5 (except the Ports and Adapters comparison), 10.7, 10.8, 10.9.
* **Working knowledge:** 10.6 (entities and value objects): understand identity versus value meaning, and why Java equality is a separate decision. You do not implement either.
* **Minimum lab:** **B1 to B3** (Book project: reading, tracing, diagnosis; **nothing to rebuild**) and **T1 to T5** (your Team project; your Milestone 3 evidence).
* **Optional:** Ports and Adapters, the AI activity, B4 to B6 (break the rules on purpose; reproduce the migration), review questions, transfer.

---

## Opening Problem: Understandable Classes, No Visible Structure

* The application now has borrowing policies, a directory adapter, notification collaborators, loan operations and several demonstrations.
* Individual classes have understandable responsibilities, but the production code **still sits largely in Java's unnamed package**.
* **Nothing tells a new developer** whether a borrowing policy may depend on a directory client, or where a storage implementation should be constructed.

---

## A Deliberately Modest Change

* Make those boundaries **visible** while **preserving the demonstrated reservation behaviour**.
* Decide which classes express **domain rules**, which **coordinate**, which **communicate with external mechanisms**, which **assemble the application**.
* **Moving files alone will not answer those questions.**
* The chapter adds a small **reservation storage contract**, moves concrete storage outside the coordinator, and documents dependency rules that can be **checked against compiled code**. No database, web framework or distributed system.

---

# 10.1 Why Class-Level Design Is Insufficient
### Responsibilities at more than one scale

---

## Class Correctness Is Not an Application Boundary

* A well-designed `LoanPeriod` can reject an invalid interval while **the surrounding application has poor dependency organisation**.
* A correct directory adapter can be **called directly from several user interfaces, each repeating eligibility logic differently**.
* Chapters 5 to 9 separated several responsibilities. Now we make the distinctions **visible across packages**.

---

## Layering

* Presentation, domain logic and data access are a familiar separation, with an **application service boundary** where operations need coordination.
* Layering narrows the responsibilities a developer must consider together.
* The chapter's exact packages are **a worked design decision, not a universal folder template**.

---

## The Program Already Has an Architecture

* Someone chooses its dependencies, **owns its state** and decides **when effects occur**. Those decisions exist even without a server or database.
* The question is **whether they are explicit enough to review and change**.
* The coordinator **owns an `ArrayList`**: easy to follow, but it ties use-case orchestration to one storage mechanism.

---

## The Cost of Extracting a Boundary

* Extracting a narrow storage contract demonstrates **dependency direction and storage ownership** without inventing persistence requirements.
* It creates **another interface** and requires a contract for **ordering, snapshots and duplicate identifiers**.
* If a program will remain a tiny script with one private list, **it may not be worth it**. Here it supports the structural learning goal and a **concrete, independently testable boundary**.

---

## What Must Remain Unchanged

* Accepted and rejected **reservation strings**.
* **Policy limits** and **half-open overlap rules**.
* **Directory failure distinctions**, **loan behaviour**.
* **Notification timing**: storage still precedes notification; an expected notification failure still retains the reservation.
* The optional publisher keeps its **declared partial-failure semantics**.

---

## What Does Change

* Callers **import named packages**.
* Direct `ReservationCoordinator` construction **requires an additional repository argument**.
* Command-line launchers use **fully qualified names**.
* These must be documented **even when every user-facing transcript stays identical**.
* Behaviour is protected **within the supplied sequential, in-memory checkpoint**, not for an unseen application that reflects on class names or depends on the old constructor.

---

# 10.2 Layers and Separation of Concerns
### Assign a reason for each boundary

---

## The Package Root

* The root is **`edu.se506.lending`**.
* **Domain** expresses the equipment vocabulary and rules.
* **Application** coordinates operations.
* **Infrastructure** implements technical boundaries.
* **Presentation** adapts an interaction to the application.
* **Bootstrap** constructs the chosen object graph.

---

## Packages and Their Types (1 of 2)

| Package | Responsibility | Representative types |
|---|---|---|
| `domain` | Values, records and borrowing decisions | `LoanPeriod`, `Reservation`, `BorrowingPolicy` |
| `application` | Use-case coordination and result formatting | `ReservationCoordinator`, `DirectoryReservationService`, `LoanService` |
| `application.port` | Contracts needed by application operations | `ReservationRepository`, `BorrowerDirectory`, `NotificationSender` |
| `infrastructure.directory` | Provider-specific translation | `LegacyDirectoryAdapter`, `LegacyDirectoryClient` |

---

## Packages and Their Types (2 of 2)

| Package | Responsibility | Representative types |
|---|---|---|
| `infrastructure.notification` | Selected local notification mechanisms | `ConsoleNotificationSender`, `NotificationPublisher` |
| `infrastructure.persistence` | Concrete reservation storage | `InMemoryReservationRepository` |
| `presentation` | Thin console interaction | `ReservationConsole` |
| `bootstrap` | Assembly and executable demonstrations | `ReservationApplication`, `Chapter10Demo` |

* The persistence package names a storage **responsibility**. The implementation is **in memory** and loses data when the process ends.

---

## Packages Communicate; Rules Enforce

* A package is a **namespace**. Public Java types can still be imported from anywhere.
* A folder named `domain` does **not** stop a developer constructing a console sender inside it.
* So the chapter states **permitted production dependencies** and adds a **test that examines compiled class dependencies**.
* Tests may cross boundaries to assemble fixtures; startup wiring has a **deliberate exception** because it must choose concrete implementations.

---

## The Dependency Matrix

| Source package | Permitted local targets |
|---|---|
| `domain` | `domain` |
| `application.port` | `domain`, `application.port` |
| `application` | `domain`, `application.port`, `application` |
| `infrastructure` | `domain`, `application` (including ports), `infrastructure` |
| `presentation` | `domain`, `application`, `presentation` |
| `bootstrap` | every application package, and explicitly demonstrated isolated examples |

---

## Isolated Examples Stay Isolated

* Ordinary production code **must not refer** to the isolated `patterns`, `behaviour` or `examples` packages.
* The value-equality demonstration lives in `examples.structure`.
* A bootstrap demonstration may show an isolated example **explicitly**, as Chapter 9 did.

---

## Avoid Mechanical Layer Multiplication

* A class does **not need an interface merely because it crosses a package boundary**. `DirectoryReservationService` stays a concrete application service.
* Not every domain object needs a repository and a service. `LoanPeriod` is a **value-shaped object**: storing it through its own repository would **obscure its role as part of a reservation**.
* The loan service's internal map stays where it was: this chapter extracts **one justified boundary**, not a generic storage framework.

---

# 10.3 Presentation, Application, Domain and Infrastructure
### What each layer does, and what it must not

---

## Presentation Translates an Interaction

* `ReservationConsole` receives a directory-backed service and a `PrintStream`.
* Its `reserve` method **invokes the service and prints the existing result**.
* It **neither selects a borrower category nor duplicates the seven-day student rule**.
* A test supplies a **byte buffer** and checks exact output; a directory exception propagates **without printing a success line**.

---

## A Thin Adapter

* Not an interactive menu, input parser or complete interface.
* The bootstrap demo supplies **synthetic directory rows** and chooses the sender.
* Presentation does **not construct the adapter or storage**, so output behaviour can be examined **without hiding construction decisions**.

---

## Application Coordinates the Use Case

* `DirectoryReservationService` performs lookup and **delegates a valid borrower** to the coordinator.
* The coordinator applies policy, checks conflicts, creates the record, **stores it**, invokes its sender.
* `LoanService` coordinates checkout and return using the supplied clock.
* These arrange several responsibilities to complete a use case. The label **does not require** a remote service, a DI framework or one service per entity.

---

## Why `ConfirmationFormatter` Stays Here

* Existing **returned strings are part of the observable contract**, so it remains in `application`.
* It is also used by the console notification adapter.
* A future structured result could separate domain outcomes from wording, but doing it now would **mix an API redesign with this restructuring**.

---

## Domain Expresses Meaning and Invariants

* Borrower categories, borrowing policies, reservations, loans and loan periods **belong to the domain vocabulary**.
* They do **not know** about console output, provider codes or repository implementations.
* Domain code may use standard-library types (`LocalDate`, collections). Independence means avoiding **orchestration and external mechanisms** the rules do not need.
* No full Domain-Driven Design set: **first explain the actual identity, invariants and ownership**.

---

## Infrastructure Implements Selected Mechanisms

* The directory adapter translates the provider contract into `BorrowerDirectory`; the in-memory repository implements storage; notification adapters write output or dispatch callbacks.
* Their code depends on **application-owned contracts and the domain types they handle**.
* Infrastructure does **not own eligibility**: the seven-day limit in the directory adapter would tie policy to the provider representation.
* The repository should **not send a notification** when a record is added: orchestration decides when.

---

## Bootstrap Chooses and Connects

* Its **concrete imports are intentional**.
* Keeping construction there makes selection **visible** without a framework or global service registry.

---

## Where an Outside Collaborator Sits

* The equipment directory, the book's data-backed collaborator, shows where **any outside collaborator** belongs (a data source, or something that scores or predicts).
* **Contract** `BorrowerDirectory` and its failure `DirectoryException`: `application.port`. Callers must tell an outage from an absent borrower.
* **Implementation** `LegacyDirectoryAdapter` with `LegacyDirectoryClient`: `infrastructure.directory`.
* **Construction**: bootstrap passes the adapter to `DirectoryReservationService`.

---

## The Same Three Positions for a Model

* A **model-backed collaborator** would occupy the same three positions: a **narrow port** with bounded outcomes and a defined failure; an **adapter in infrastructure**; **construction in bootstrap**.
* The application would **not import the adapter**.
* A test could **substitute the port** exactly as the directory tests do.

---

# 10.4 Dependency Direction and Its Check
### Arrows are source references

---

## Figure 10.1: Permitted Source Dependencies

<!--svg:ch10-layers-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 365" role="img" aria-label="Figure 10.1, permitted source dependencies: Bootstrap may refer to Presentation, Application and ports, Infrastructure adapters and Domain. Presentation refers to Application and Domain. Application refers to Domain. Infrastructure refers to Application and to Domain. Domain refers to nothing else." style="display:block;width:100%;height:calc(var(--u) * 36.50);margin:0 auto">
<defs><marker id="ch10-layers-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-layers-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-layers-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-layers-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-layers-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="285.0" y="10.0" width="300.0" height="62.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="435.0" y="36.2" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Bootstrap</text>
<text x="435.0" y="57.4" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">choose implementations</text>
<rect x="20.0" y="130.0" width="230.0" height="66.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="135.0" y="169.5" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Presentation</text>
<rect x="320.0" y="130.0" width="230.0" height="66.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="435.0" y="157.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Application</text>
<text x="435.0" y="180.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">and ports</text>
<rect x="620.0" y="130.0" width="230.0" height="66.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="735.0" y="157.9" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Infrastructure</text>
<text x="735.0" y="180.4" font-size="18" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">adapters</text>
<rect x="320.0" y="255.0" width="230.0" height="66.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="435.0" y="294.5" font-size="19" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Domain</text>
<path d="M435.0,72.0 L435.0,130.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<path d="M285.0,41.0 L135.0,41.0 L135.0,130.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<path d="M585.0,41.0 L735.0,41.0 L735.0,130.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<path d="M250.0,163.0 L320.0,163.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<path d="M620.0,163.0 L550.0,163.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<path d="M435.0,196.0 L435.0,255.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<path d="M735.0,196.0 L735.0,288.0 L550.0,288.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<path d="M135.0,196.0 L135.0,288.0 L320.0,288.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<path d="M570.0,72.0 L570.0,225.0 L520.0,225.0 L520.0,255.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch10-layers-arr)"/>
<text x="20.0" y="336.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">A missing arrow means the reference is not permitted:</text>
<text x="20.0" y="356.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">Domain refers to nothing else.</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 10.1

* Each box is a **group of packages**; an arrow means classes in the first group **may refer to** classes in the second.
* **The application has no arrow to infrastructure.** `ReservationCoordinator` imports `ReservationRepository`, an application-owned contract; `InMemoryReservationRepository` imports and implements it; **bootstrap** constructs the implementation.
* The figure shows **source references only**, not the order of calls.

---

## The Port Package's Narrower Rule

* Within application, the port package may depend on **domain types and other ports**, not concrete application services.
* This keeps a storage contract **from requiring the coordinator it exists to support**.

---

## Runtime Calls Travel Toward an Adapter

* At runtime the coordinator calls an object that **happens to be** an in-memory repository.
* That does **not** require its source to import the concrete class: **interface dispatch** connects the call to the implementation selected during assembly.
* Source dependency points **toward the port**; the runtime call goes **through** it.

---

## Figure 10.2: One Accepted Reservation at Run Time

<!--svg:ch10-seq-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 378" role="img" aria-label="Figure 10.2: one accepted reservation at run time. The console calls the directory service, which calls the coordinator. The coordinator reads a snapshot from the repository, adds the accepted reservation, then calls the notification sender. The result string returns up the chain." style="display:block;width:100%;height:calc(var(--u) * 37.80);margin:0 auto">
<defs><marker id="ch10-seq-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-seq-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-seq-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-seq-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-seq-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="90.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Reservation</text>
<text x="90.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Console</text>
<path d="M90.0,56.0 L90.0,370.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="180.0" y="6.0" width="160.0" height="50.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="260.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Directory</text>
<text x="260.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Service</text>
<path d="M260.0,56.0 L260.0,370.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="350.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="430.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Reservation</text>
<text x="430.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Coordinator</text>
<path d="M430.0,56.0 L430.0,370.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="520.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="600.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">In-memory</text>
<text x="600.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Repository</text>
<path d="M600.0,56.0 L600.0,370.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="690.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="770.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Notification</text>
<text x="770.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">sender impl.</text>
<path d="M770.0,56.0 L770.0,370.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<path d="M94.0,88.0 L256.0,88.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch10-seq-arr)"/>
<text x="175.0" y="81.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">reserve(request)</text>
<rect x="60.0" y="100.0" width="400.0" height="28.0" rx="5" fill="#f6ead9" stroke="#b4762e" stroke-width="1.6"/>
<text x="260.0" y="120.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle" font-style="italic">resolve the borrower through the directory port</text>
<path d="M264.0,148.0 L426.0,148.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch10-seq-arr)"/>
<text x="345.0" y="141.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">reserve with mapped category</text>
<path d="M434.0,172.0 L596.0,172.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch10-seq-arr)"/>
<text x="515.0" y="165.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">findAll() for policy and conflict checks</text>
<path d="M596.0,196.0 L434.0,196.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch10-seq-arr)"/>
<text x="515.0" y="189.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">snapshot</text>
<path d="M434.0,220.0 L596.0,220.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch10-seq-arr)"/>
<text x="515.0" y="213.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">add(accepted reservation)</text>
<path d="M434.0,244.0 L766.0,244.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch10-seq-arr)"/>
<text x="600.0" y="237.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">send(confirmed reservation)</text>
<path d="M766.0,268.0 L434.0,268.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch10-seq-arr)"/>
<text x="600.0" y="261.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">normal return, or NotificationException</text>
<rect x="220.0" y="280.0" width="420.0" height="28.0" rx="5" fill="#f6ead9" stroke="#b4762e" stroke-width="1.6"/>
<text x="430.0" y="300.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle" font-style="italic">on failure: keep the reservation, append the suffix</text>
<path d="M426.0,330.0 L264.0,330.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch10-seq-arr)"/>
<text x="345.0" y="323.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">existing result string</text>
<path d="M256.0,354.0 L94.0,354.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch10-seq-arr)"/>
<text x="175.0" y="347.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">result string</text>
</svg>
</div>
<!--/svg-->

---

## Reading Figure 10.2

* Each box at the top is an **object**; time runs **down the page**; solid arrows are **calls**, dashed arrows **returns**.
* The coordinator may take **more than one snapshot** during a request. The diagram groups those reads: it does **not claim one storage call or a transaction**.
* The application still assumes **one sequential session**.

---

## Check What the Code Actually References

* `DependencyRulesTest` invokes the JDK's **`jdeps`** on compiled production classes and **rejects local dependency edges** that contradict the policy.
* It also checks that dependencies were **actually discovered** (no vacuous pass on missing output).
* A second test builds the **package-to-package graph** and **searches for a cycle**.
* It catches a **fully qualified reference even with no import**.

---

## What the Dependency Test Cannot See

* **Reflective class names in strings**, runtime configuration relationships.
* A **semantically misplaced rule** that uses only permitted types.
* So source review and behaviour tests remain necessary.
* It needs a **full Java 17 JDK** with the `jdk.jdeps` module. Package rules are **project decisions**, not universal rules the analyser infers.

---

## Optional: Ports and Adapters

* The directory, sender and repository interfaces can be discussed as **ports**, with infrastructure implementations as **adapters**.
* The console **drives** the application; storage and notifications are collaborators the application **calls**.
* Consistent with Cockburn's discussion of isolating application behaviour from runtime mechanisms.
* It does **not** require six adapters, a hexagonal deployment or a package per method. Use it **only when it clarifies which side owns the contract**.

---

# 10.5 Package Design: Cohesion, Coupling and Stability
### Are the packages well cut?

---

## Package Cohesion: What Changes Together

* A cohesive package holds types that **change for the same reason** and are **used together**.
* **CCP, Common Closure Principle:** things that **change together** belong together.
* **CRP, Common Reuse Principle:** things **used together** belong together, so a client is not forced to depend on classes it never uses.
* **REP, Reuse/Release Equivalence Principle:** the unit you reuse is the unit you release. This project has no separately released package, so REP is **context, not a check**.
* Test the cuts with **concrete changes**, not slogans: for each change, list the packages whose production code must change.

---

## Five Change Requests (1 of 2)

| Change request | Packages that change | What it shows |
|---|---|---|
| Staff may reserve for 21 days | `domain` (`StaffReservationRules`) | The policy change stays in one package |
| The provider renames its status code `Y` | `infrastructure.directory` | Provider vocabulary stays outside the application |
| The confirmation wording changes | `application` (`ConfirmationFormatter`) | Its users, including the console sender, see it without being edited |

---

## Five Change Requests (2 of 2)

| Change request | Packages that change | What it shows |
|---|---|---|
| Reservations are stored in a file | `infrastructure.persistence` (a new class) and `bootstrap` | The coordinator is not edited: it names only the port |
| A third borrower category is added | `domain`, `infrastructure.directory` and `bootstrap` | One business idea touches **three** packages |

* Most changes touch one or two packages. The last row is **a legitimate cost to record, not a flaw to hide**. Always add **a change you expect to be awkward**.

---

## Package Coupling

* Coupling between packages is the number of references that **cross a package boundary**.
* **Habit 1:** depend on a **small contract** where the other side may vary. The coordinator refers to `ReservationRepository`, not the in-memory class.
* **Habit 2:** keep the package graph **free of cycles**. If `application` referred to `infrastructure.notification` while it referred back, **neither could be compiled, tested or replaced without the other** (the Acyclic Dependencies Principle, ADP).

---

## Layers Rule Out Some Cycles, Not All

* The layer matrix rules out cycles **between layers**, because each pair allows references in one direction only.
* It does **not** rule them out **inside one layer**: the matrix lets `infrastructure.directory` and `infrastructure.notification` refer to each other, so a cycle between them **would pass the direction test**.
* That is why `DependencyRulesTest` has the **separate cycle check**.

---

## The Port Package and Reuse

* `application.port` holds **five small contracts and their failure types**, so a class that needs one is **not forced to depend on a large service**.
* If a port package grew to hold many unrelated contracts, **splitting it would be worth considering**: a client using only the sender should not be affected when the directory contract changes.

---

## Package Stability

* A package is **stable** when it is costly to change: **many depend on it, it depends on little**.
* A package is **unstable** when **little depends on it** and it depends on many.
* Both kinds are needed. The **Stable Dependencies Principle (SDP):** **dependencies should point towards stability**, so code that changes often depends on code that changes rarely.

---

## Counting Stability

* **Afferent coupling Ca:** classes **outside** P that depend on classes inside P (incoming).
* **Efferent coupling Ce:** classes **inside** P that depend on classes outside P (outgoing).
* **Instability I = Ce / (Ca + Ce)**, from **0** (maximally stable) to **1** (maximally unstable).
* This book **counts classes**, treats a nested class as part of its outer class, counts only references **between this project's packages**, and ignores the Java standard library.

---

## Package Metrics (1 of 2)

| Package | Classes | Ca | Ce | I |
|---|---:|---:|---:|---:|
| `domain` | 8 | 16 | 0 | 0.00 |
| `application.port` | 5 | 14 | 3 | 0.18 |
| `infrastructure.notification` | 3 | 7 | 3 | 0.30 |
| `application` | 6 | 9 | 4 | 0.31 |

---

## Package Metrics (2 of 2)

| Package | Classes | Ca | Ce | I |
|---|---:|---:|---:|---:|
| `infrastructure.directory` | 2 | 2 | 1 | 0.33 |
| `infrastructure.persistence` | 1 | 1 | 1 | 0.50 |
| `presentation` | 1 | 1 | 1 | 0.50 |
| `bootstrap` | 7 | 0 | 7 | 1.00 |

* From `tools/PackageMetrics.java`, run as `java tools/PackageMetrics.java target/classes`.

---

## Instability as a Picture

<!--svg:ch10-instability-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 362" role="img" aria-label="Instability I = Ce / (Ca + Ce) of the checkpoint&#x27;s packages: domain 0.00, application.port 0.18, infrastructure.notification 0.30, application 0.31, infrastructure.directory 0.33, infrastructure.persistence 0.50, presentation 0.50, bootstrap 1.00." style="display:block;width:100%;height:calc(var(--u) * 36.20);margin:0 auto">
<defs><marker id="ch10-instability-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-instability-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-instability-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-instability-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch10-instability-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<text x="285.0" y="26.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="end">package</text>
<text x="300.0" y="26.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="start">I = 0</text>
<text x="750.0" y="26.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="end">I = 1</text>
<text x="860.0" y="26.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#46586d" text-anchor="end">Ca / Ce</text>
<text x="285.0" y="61.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="end">domain</text>
<rect x="300.0" y="44.0" width="450.0" height="26.0" rx="4" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.4"/>
<text x="308.0" y="63.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#172a42" text-anchor="start">0.00</text>
<text x="860.0" y="63.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">16 / 0</text>
<text x="285.0" y="98.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="end">application.port</text>
<rect x="300.0" y="81.0" width="450.0" height="26.0" rx="4" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.4"/>
<rect x="300.0" y="81.0" width="81.0" height="26.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="389.0" y="100.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#172a42" text-anchor="start">0.18</text>
<text x="860.0" y="100.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">14 / 3</text>
<text x="285.0" y="135.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="600" fill="#b4762e" text-anchor="end">infrastructure.notification</text>
<rect x="300.0" y="118.0" width="450.0" height="26.0" rx="4" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.4"/>
<rect x="300.0" y="118.0" width="135.0" height="26.0" rx="4" fill="#b4762e" stroke="#b4762e" stroke-width="1.4"/>
<text x="443.0" y="137.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#172a42" text-anchor="start">0.30</text>
<text x="860.0" y="137.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">7 / 3</text>
<text x="285.0" y="172.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="600" fill="#b4762e" text-anchor="end">application</text>
<rect x="300.0" y="155.0" width="450.0" height="26.0" rx="4" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.4"/>
<rect x="300.0" y="155.0" width="139.5" height="26.0" rx="4" fill="#b4762e" stroke="#b4762e" stroke-width="1.4"/>
<text x="447.5" y="174.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#172a42" text-anchor="start">0.31</text>
<text x="860.0" y="174.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">9 / 4</text>
<text x="285.0" y="209.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="end">infrastructure.directory</text>
<rect x="300.0" y="192.0" width="450.0" height="26.0" rx="4" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.4"/>
<rect x="300.0" y="192.0" width="148.5" height="26.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="456.5" y="211.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#172a42" text-anchor="start">0.33</text>
<text x="860.0" y="211.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">2 / 1</text>
<text x="285.0" y="246.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="end">infrastructure.persistence</text>
<rect x="300.0" y="229.0" width="450.0" height="26.0" rx="4" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.4"/>
<rect x="300.0" y="229.0" width="225.0" height="26.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="533.0" y="248.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#172a42" text-anchor="start">0.50</text>
<text x="860.0" y="248.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">1 / 1</text>
<text x="285.0" y="283.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="end">presentation</text>
<rect x="300.0" y="266.0" width="450.0" height="26.0" rx="4" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.4"/>
<rect x="300.0" y="266.0" width="225.0" height="26.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="533.0" y="285.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#172a42" text-anchor="start">0.50</text>
<text x="860.0" y="285.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">1 / 1</text>
<text x="285.0" y="320.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="end">bootstrap</text>
<rect x="300.0" y="303.0" width="450.0" height="26.0" rx="4" fill="#f5f7fa" stroke="#c3cfdd" stroke-width="1.4"/>
<rect x="300.0" y="303.0" width="450.0" height="26.0" rx="4" fill="#1d588c" stroke="#1d588c" stroke-width="1.4"/>
<text x="742.0" y="322.0" font-size="15.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#ffffff" text-anchor="end">1.00</text>
<text x="860.0" y="322.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="400" fill="#46586d" text-anchor="end">0 / 7</text>
<text x="435.0" y="354.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">The orange pair is the one arrow that points to a slightly less stable package.</text>
</svg>
</div>
<!--/svg-->

---

## Reading the Numbers

* `domain` has **I = 0**: sixteen classes depend on it and it depends on nothing else. Keep it **small and free of mechanisms**: a change can ripple everywhere.
* `bootstrap` has **I = 1**: nothing depends on it, so it **can change freely**, which suits the place where concrete choices are made.
* Most arrows run from a higher I to a lower one: `application` (0.31) to `application.port` (0.18) to `domain` (0.00).

---

## The One Arrow That Does Not

* `infrastructure.notification` (**0.30**) depends on `application` (**0.31**), because `ConsoleNotificationSender` uses the concrete `ConfirmationFormatter`.
* The difference is **one hundredth**, from a handful of classes: **no defect**.
* It is the arrow to **examine first in a review**: the one concrete dependency running from a mechanism to an application class.

---

## An Isolated Package Has No Defined Instability

* `patterns` and `examples.structure` have **no references to or from the lending packages**: Ca + Ce = 0, and the formula divides by zero. The tool prints *undefined*.
* **Do not report it as 0** (maximally stable) **or as 1**. It is simply **isolated, as intended**.
* `behaviour` is referenced only by the Chapter 9 demo: Ca = 1, I = 0.

---

## Numbers Are Questions, Not Grades

* With one to eight classes per package, **adding a single class moves a ratio by several hundredths**.
* A package can have a **good number and a muddled responsibility**; a poor number can be **the right design** (bootstrap).
* Compare numbers **only from the same tool and counting rules**.

---

## Package Abstractness: The Stable Abstractions Principle

* **SAP:** a package that many others depend on cannot change freely, so it should be **abstract enough to be extended without being edited**.
* Martin measures **abstractness A** as the share of a package's classes that are abstract classes or interfaces.
* **This book does not compute A:** it needs a second tool, and with one to eight classes per package the ratio **moves with every class added**. SAP is used as a **reading question**.

---

## Reading SAP on the Checkpoint

* `application.port`: contracts and their failure types, so **mostly abstract**, and stable (I = 0.18). **SAP satisfied.**
* `bootstrap`: concrete and unstable (I = 1.00). **SAP satisfied**: nothing depends on it.
* `domain` **deserves the question**: sixteen classes depend on it, yet it is mostly concrete records and rules. It stays safe because it changes only with the borrowing vocabulary, and `BorrowingPolicy` gives the varying part an **abstract seam**.
* The **warning sign** would be a package that is stable, concrete **and** changes often.

---

## Worked Comparison: Where Does `NotificationException` Live?

* **Option A (the checkpoint's choice):** in `application.port`, with the `NotificationSender` contract.
* **Option B:** in `infrastructure.notification`, beside the senders that throw it ("implementations should own their failures").
* Option B was tried on a copy.

---

## Option B Is Rejected by Two Checks

* The direction check failed: `application.ReservationCoordinator -> infrastructure.notification.NotificationException`: the coordinator must name the exception to catch it, so **application would depend on infrastructure**.
* The cycle check also failed: `infrastructure.notification` already depends on `application`.
* The instability figures **would not have shown it** (application 0.31; notification 0.27).
* **The rule:** a type that callers must **catch or inspect** belongs with **the contract they depend on**, not with one implementation.

---

# 10.6 Entities and Value Objects
### Identity, immutability and equality are separate

---

## Identity Is a Domain Decision

* A reservation has an identifier such as **R1**.
* Whether two records with that identifier and different data mean **an update or an invalid duplicate** depends on the storage contract. This checkpoint is **append-only and rejects duplicate identifiers**.
* `Reservation` is immutable and **does not override `equals` or `hashCode`**: two objects with the same ID are **not equal** through inherited object equality.
* The repository uses the **explicit identifier as its key**.

---

## Entity and Value Object

* An **entity** is distinguished by its **identity** rather than its attributes. A **value object** is one where you care only about **attributes and logic**, treated as immutable (Evans).
* Calling a class an entity does **not** silently implement equality, persistence or a lifecycle.
* Making it immutable does **not** remove its domain identity.

---

## Value Meaning vs. Java Value Equality

* A `LoanPeriod` is characterised by its **start and exclusive end**, not by a generated identifier.
* But the cumulative class **keeps inherited object equality**: two periods with equal dates are **distinct** by `equals`. The chapter preserves that rather than change equality during a package move.
* `examples.structure.PeriodValue` is a **record** demonstrating component-based equality and hashing: two equal-date records are one logical value in a set.
* Adopting it in the real model is **a separate, reviewed change**.

---

## Immutability Supports Snapshots

* An unmodifiable list prevents adding or removing through that list. It does **not generally make the elements immutable**.
* The repository's snapshots are safe **because `Reservation` and its period are also immutable**.
* A previously returned snapshot **stays unchanged** when another reservation is stored.
* If a later reservation becomes mutable, a shallow copy **no longer establishes a historical snapshot**.

---

# 10.7 Repositories and Services
### The smallest useful storage contract

---

## The Port

```java
public interface ReservationRepository {
    List<Reservation> findAll();
    void add(Reservation reservation);
}
```

* **Insertion-ordered, stable, unmodifiable snapshots.**
* `add` **rejects null or duplicate IDs** without replacing existing records.
* The in-memory adapter uses a `LinkedHashMap` keyed by reservation ID and returns `List.copyOf` snapshots.

---

## Where the Port Lives

* The interface is in `application.port` because **the application use case consumes it**.
* Domain-owned repository contracts are another possible design **when the domain's needs justify that ownership**.
* Location should follow **actual responsibilities**, not a rule that all repository interfaces belong in one layer.
* A deliberately smaller example than the classic repository: no data mapper, no query language.

---

## What the Extraction Does Not Change

* The coordinator **still calculates counts, checks conflicts and allocates size-based identifiers**. None of that moves into storage.
* The factory supplies **a fresh repository per coordinator**: the earlier session ownership and R1 starting point stay.
* The new constructor is **an injection point, not a promise** to support preloaded or shared stores.
* No `delete`, generic `save`, transaction manager or repository for every class.

---

## A Port Does Not Supply Transactions

* A test supplies a repository whose `add` **throws before appending**: the exception propagates and **notification is not reached**.
* That establishes the order for **this specific failure**, not that a future database cannot fail **after** a write succeeded.
* Snapshots and duplicate-ID checks do **not** make count-check, conflict-check and append **atomic across concurrent requests**.
* A database would require reviewing those assumptions.

---

## Three Different Responsibilities

* An **application service** coordinates operations.
* A **repository** manages access to stored domain records.
* **Domain policies** express rules.
* The boundaries are useful because they expose **what each responsibility does and does not promise**.

---

# 10.8 A Small Architecture Decision
### ADR-010

---

## The Worked Decision

* **ADR-010:** named packages, application-owned ports, one in-memory reservation adapter, explicit bootstrap wiring.
* Status: **implemented teaching example; peer review pending**. The wording separates author verification from a review that has not occurred.
* **Problem:** construction and storage ownership were insufficiently visible as the example grew.
* **Compares:** keeping the unnamed package; narrow boundaries; a larger framework or generic repository.

---

## ADR-010: Alternatives and Consequences

* **Alternatives:** keep the unnamed package and private list (less code, weaker visibility); **narrow packages and one storage port (selected)**; a generic CRUD repository, ORM, database or DI framework (**declined**: not required).
* **Consequences:** new imports; fully qualified launcher names; **one more coordinator constructor argument**; a **full-JDK dependency** for the architecture test; more files to maintain.
* **Revisit triggers:** persistent storage; multiple writers; a cancellation lifecycle; a new identifier scheme; value equality for the period; structured results.

---

## Your Decision Will Differ

* ADR-010 is the worked model for the **Book project**. On your **Team project**: a different boundary, different alternatives, different costs.
* **Do not copy ADR-010's decision** unless it is also yours.
* An alternative of **"do nothing"** and a revisit trigger naming **an event you could observe** make a record more useful than one that only justifies what was already done.

---

## A Reviewable Migration

* Separate **package moves** from the **repository extraction** and from **newly added checks**.
* Older tests move into a `regression` package; direct constructor calls receive the new repository; **expected behaviours are retained**.
* The checkpoint is **not evidence of Git commits or an opened pull request**. Record your **actual sequence and review comments**.

---

# 10.9 Peer Review and Milestone 3
### One scenario across boundaries

---

## Review One Scenario Across Boundaries

* Trace a **valid staff request** from presentation through directory lookup, policy evaluation, storage and notification.
* Then a **missing borrower** and an **expected notification failure**.
* Check the layer diagram matches **both source dependencies and the observed order of effects**.
* Ask: **who creates each concrete adapter**? Does application code import it? Does domain depend on application services?

---

## Two Kinds of Evidence

* The **dependency test** examines compiled relationships. The **regression suite** examines selected behaviour.
* **A semantically poor design can pass both.** A reasoned human review remains part of the evidence.
* Verify that **presentation has not copied a policy rule** to make the demo pass.
* Inspect the repository's snapshot and duplicate-ID contract.

---

## Preparing Evidence (1 of 3)

| Item | Artefact | What it should establish |
|---|---|---|
| 1 | Pattern note | A pattern used where it removes a real problem, with the reason; one place you declined |
| 2 | Compact package diagram | Actual responsibilities and declared dependency direction, matching your code |
| 3 | Restructuring diff or PR | What moved and what logic changed, kept apart |

---

## Preparing Evidence (2 of 3)

| Item | Artefact | What it should establish |
|---|---|---|
| 4 | Regression result and dependency report | Existing examples still pass; references follow the chosen rules; any cycle is reported |
| 5 | ADR | Problem, alternatives (including doing nothing), decision, consequences, revisit triggers |
| 6 | Actual review record | A reviewer examined the change and the feedback was addressed |

---

## Preparing Evidence (3 of 3)

| Item | Artefact | What it should establish |
|---|---|---|
| 7 | Demonstration and retrospective | What worked, what did not, one next action |
| 8 | Limits statement | What the structure does not provide: persistence, concurrency safety, a cancellation lifecycle |

* Local author testing is **not hosted CI evidence**. A sample PR description is **not a completed peer review**.

---

## A Better Reviewer Question

* Not: "Does it have four layers?"
* But: **"Where would this concrete change belong, and which existing tests protect its consequences?"**
* The answer should name **files, contracts and trade-offs**, not only package names.

---

# 10.10 AI in Practice: Verify a Dependency Review
### A claim needs a trace

---

## The Activity

* **Objective:** examine a proposed dependency review **without treating its wording as evidence**.
* Supply the package map, the relevant Java files and the declared dependency policy.
* Limit the task to **identifying references and responsibility concerns**: do not ask the assistant to invent a database or rewrite requirements.

---

## The Fixture

> The coordinator calls an in-memory repository at runtime, so it must import infrastructure and violates dependency inversion. Move the repository interface into infrastructure. Every entity needs a repository and a service. Making the reservation list unmodifiable makes every future element immutable. The bootstrap imports adapters, so remove it and let services construct their dependencies. Since all tests pass, the pull request has been peer reviewed.

---

## Findings (1 of 2)

| Fictional claim | Finding |
|---|---|
| A runtime call to the in-memory store proves an application import of infrastructure | **Incorrect**: interface dispatch and source references are different relationships |
| Put the repository interface in infrastructure | **Not justified**: the consuming application would depend on an infrastructure-owned contract |
| Every entity needs a repository and service | **No such requirement follows from identity**; `LoanPeriod` has neither |

---

## Findings (2 of 2)

| Fictional claim | Finding |
|---|---|
| An unmodifiable list makes every element immutable | **Incorrect** for mutable elements |
| Bootstrap must not import adapters | **Incorrect** for the selected composition role |
| Passing tests establishes peer review | **Incorrect evidence substitution**: record real reviewer comments |

* A dependency review should name **the referencing type and the referenced type**. "Infrastructure coupling" without that trace is only a claim to investigate.

---

# 10.11 Common Mistakes
### Eleven to avoid

---

## Mistakes 1 to 4

| Mistake | Consequence | Better action |
|---|---|---|
| Treat package names as enforced architecture | Public types can still form forbidden dependencies | State and check a dependency policy |
| Confuse runtime calls with source imports | Misdiagnoses interface-based dispatch | Trace both relationships separately |
| Move provider codes into the domain | Couples rules to an external representation | Keep translation in the adapter |
| Duplicate eligibility in presentation | Inconsistent entry points | Delegate the use case |

---

## Mistakes 5 to 8

| Mistake | Consequence | Better action |
|---|---|---|
| Call immutable objects automatically value-equal | Misreads `equals` and collections | Inspect and test equality semantics |
| Add generic CRUD to every class | Invents unsupported lifecycle operations | Add only needed storage capabilities |
| Construct adapters inside application services | Hides concrete dependencies | Assemble them explicitly at bootstrap |
| Claim passing tests prove peer review | Substitutes one type of evidence for another | Record actual review separately |

---

## Mistakes 9 to 11

| Mistake | Consequence | Better action |
|---|---|---|
| Grade a package by its instability number | A coarse number from few classes; a muddled package can score well | Use it to pick what to examine, then reason about responsibility |
| Report an isolated package as I = 0 or I = 1 | The formula is undefined when Ca + Ce = 0 | Report it as undefined and explain why |
| Accept a cycle because the layers look right | Two packages in one layer can still depend on each other | Check the package graph for cycles |

---

# 10.12 Practical Activity
### Book project B1 to B6; Team project T1 to T5

---

## Input and Demonstration

* **Input:** the migrated checkpoint, the package responsibility table, the metrics table and your Team project's repository.
* **Demonstration:** trace the coordinator's storage access, then the port and adapter after extraction. Compare the **source diagram** with the **runtime sequence**. Run `tools/PackageMetrics.java` and `DependencyRulesTest`, and one demo under its **new fully qualified launcher name**.
* **Guided practice:** classify a domain policy, directory adapter, application service and bootstrap class. Explain why the **same concrete import is right in bootstrap and forbidden in application code**.

---

## B1: Classify

For `StaffReservationRules`, `LegacyDirectoryAdapter`, `DirectoryReservationService`, `InMemoryReservationRepository` and `ReservationApplication`: name the **package**, what it **may refer to**, and one thing it **must not**.

| Class | Package | Must not refer to |
|---|---|---|
| `StaffReservationRules` | `domain` | Any application, infrastructure or presentation class |
| `LegacyDirectoryAdapter` | `infrastructure.directory` | `presentation`, `bootstrap`, an isolated example |
| `DirectoryReservationService` | `application` | Any infrastructure class |
| `InMemoryReservationRepository` | `infrastructure.persistence` | `presentation`, `bootstrap` |
| `ReservationApplication` | `bootstrap` | Nothing forbidden, but **no business rule** |

---

## B2: Check the References

* Run the build and the compiled dependency check.
* A **permitted** reference: `LegacyDirectoryAdapter -> application.port.BorrowerDirectory`. Infrastructure may refer to the application's ports, and the adapter implements the contract.
* The reference from `infrastructure.notification` to `application`: `ConsoleNotificationSender -> application.ConfirmationFormatter`. The console sender builds its notice text with the **shared formatter**, preserving existing wording.

---

## B3: Diagnose the Package Design

* **(a)** Write **two change requests** of your own and list the packages each would change. (Model: "the console prints the borrower's name": `presentation` only, or `application` too, which exposes the string-result limit. "Add an email notifier": a new class in `infrastructure.notification` and one construction change in `bootstrap`.)
* **(b)** Identify **the one arrow to a less stable package**; would you act?
* **(c)** Should `ConfirmationFormatter` stay in `application`? Name the test or number that would change your mind.

---

## B3 (c): The Model Answer

* **Stay in `application`.** The coordinator needs it to build the returned text: moving it into `infrastructure.notification` would make **application depend on infrastructure**, the same failure as moving `NotificationException`.
* Moving it into `domain` would put **wording in the domain**.
* **What would change the answer:** a **second notification format** needing its own formatter, or the dependency report showing **more concrete application classes** referenced from infrastructure.

---

## T1 and T2

* **T1. Diagram.** A compact package diagram of your team's codebase in the style of Figure 10.1: boxes for groups of packages, arrows for permitted references. **Mark one reference you would forbid** and say why. No packages yet? Propose the groups.
* **T2. Decision.** One architecture decision your team actually faces (where a boundary or port belongs; whether to extract a storage contract; where construction happens). An ADR in ADR-010's form: **context, decision, alternatives including doing nothing, consequences, revisit triggers**.

---

## T3, T4 and T5

* **T3. Restructure.** One small change on a branch. **Package moves separate from logic changes**; existing checks passing; say which behaviour you protected.
* **T4. Check the direction.** A compiled dependency check (`DependencyRulesTest` or `jdeps`) if your build can; otherwise a **manual import review, recorded as manual**. Look for **cycles** as well as forbidden directions.
* **T5. Review.** A teammate reviews the change and the ADR. Record the feedback and what you changed. Then work through the Milestone 3 checklist: which items are complete, which are gaps, **who will close each**.

---

## What a Good Team Answer Shows

* **T1:** every arrow justified in one sentence; at least one **forbidden** reference marked; the dependency check **confirms it does not occur**. A weak diagram copies Figure 10.1 without checking.
* **T2:** the context names **a problem someone could observe** ("the checkout class creates the payment client and cannot be tested"); alternatives include **doing nothing**; the trigger is **an event**.
* **T4:** says whether the check was **compiled or manual**, lists forbidden references found or states none, says whether **cycles** were searched.
* **T5:** records a **real reviewer's comments** and the response.

---

## Optional Extension (Book Project)

* **B4. Break the rules on purpose.** In a scratch copy, construct `InMemoryReservationRepository` **inside** `ReservationCoordinator`. Run the dependency test, record the violation, **restore the original**.
* **B5. Reproduce the migration** from the Chapter 9 project: move classes into the declared packages, extract the repository contract, supply it through construction, update imports and launchers, preserve results.
* **B6.** The Section 10.10 AI activity.

---

## Expected Artefacts and Acceptance

* **Artefacts:** answers to B1 to B3; for the Team project the **T1 diagram**, **T2 decision record**, **T3 diff or PR description**, **T4 dependency result**, **T5 review record with the checklist status**.
* **Accept when:** your diagram **matches your code**; your decision states **a real alternative** and an **observable revisit trigger**; moves are apart from logic changes; dependency evidence covers **direction and cycles** and says **compiled or manual**; **the review is real**.
* Do not claim review or hosted CI that has not occurred.

---

## Fixing the Flaws: Four Wrong Alternatives (1 of 2)

```java
// WRONG: the application now names a concrete infrastructure type
private final ReservationRepository repository = new InMemoryReservationRepository();

// WRONG: callers could change the store without add's checks
public List<Reservation> findAll() { return backingList; }
```

* The first: the **dependency check rejects the compiled edge**. The second: the snapshot test checks **non-mutation and historical independence**.

---

## Fixing the Flaws: Four Wrong Alternatives (2 of 2)

```java
// WRONG: a second object with the same ID replaces the first
records.put(reservation.id(), reservation);

// WRONG: the console now owns a policy the domain already decides
if (days > 7) { output.println("Rejected: borrower limit or duration."); return; }
```

* The third: duplicate IDs must **reject without mutation**. The fourth: a **ten-day staff request** exposes it (staff policy allows it): the final console test sends exactly that.

---

## Do the Tests Detect Faults? (1 of 3)

| Fault | Before the three added tests | With the final tests |
|---|---|---|
| Duplicate id replaces the original; modifiable snapshot copy; live snapshot view; `HashMap` instead of insertion order | All four caught | Unchanged |
| Explicit null check removed in the repository | Survived: still throws `NullPointerException`, only the message differs | **Survives** (equivalent behaviour) |
| Stores after notification; `reservations()` modifiable copy; identifier skips a number; conflict check ignores stored records | All four caught | Unchanged |

---

## Do the Tests Detect Faults? (2 of 3)

| Fault | Before the three added tests | With the final tests |
|---|---|---|
| Null repository accepted | **Survived**: no test constructed a coordinator without one | Caught by `coordinatorRequiresARepository` |
| One repository shared by every session | Caught | Unchanged |
| Console prints without a newline; swallows directory failures | Both caught | Unchanged |
| Console duplicates the seven-day rule | **Survived**: the console test used only a student | Caught by the ten-day staff test |

---

## Do the Tests Detect Faults? (3 of 3)

| Fault | Before the three added tests | With the final tests |
|---|---|---|
| `PeriodValue` validation removed; `LoanPeriod` gains value equality | Both caught | Unchanged |
| Seven dependency-direction violations | All caught by the direction test | Unchanged |
| `directory` and `notification` packages refer to each other | **Survived**: each reference is individually permitted | Caught by the cycle test |
| A class name held in a string | **Survived**: `jdeps` reads compiled references | **Survives**: a documented limit |

* Of the 25 faults, **20 caught** before the three tests were added and **23** by the final tests.

---

## The Test Inventory

| Test class | Invocations | Purpose |
|---|---:|---|
| `RepositoryBoundaryTest` | 7 | Snapshots, duplicate/null rejection, storage before notification, failed add, independent sessions, required repository |
| `ValueSemanticsTest` | 2 | Record equality; preserved cumulative period equality |
| `ReservationConsoleTest` | 3 | Output contract, a staff request above the student limit, unhidden directory failure |
| `DependencyRulesTest` | 2 | Compiled references against the matrix; no package cycle |
| Migrated earlier suite | 107 | Existing policies, directory, loan, notification, pattern, lifecycle |
| **Total** | **121** | Complete checkpoint gate |

---

# 10.13 Review and Transfer
### Concept, diagnosis, transfer

---

## Concept Questions

1. Why can the coordinator call an infrastructure object without depending on its concrete class?
2. What distinguishes an application service from a domain policy and a repository?
3. Why does an immutable reservation still have entity identity, and why does that not automatically define Java equality?
4. What can the `jdeps` check establish, and what does it leave for review?

---

## Diagnosis Questions (1 of 2)

5. A console class checks the seven-day limit before calling the service. A new API endpoint does not. Explain the responsibility problem and a test that exposes inconsistent behaviour.
6. A developer adds a database repository and announces concurrent safety because `add` rejects duplicate IDs. Identify the missing consistency question across eligibility, conflicts and insertion.

---

## Diagnosis Questions (2 of 2)

7. In the metrics table `bootstrap` has I = 1.00 and `domain` has I = 0.00. Explain why neither is a defect and what a change to each would disturb.
8. A new class in `infrastructure.directory` refers to `infrastructure.notification`, and a class there already refers back to the directory package. Which check catches this, and which check does not?

---

## Guidance: Questions 1 to 4

1. The coordinator **refers to `ReservationRepository`**; bootstrap supplies an implementation; at runtime **dispatch** reaches the concrete method. Static and runtime diagrams answer different questions.
2. A **service** coordinates a use case; a **policy** expresses a rule; a **repository** provides access to stored records through a stated contract.
3. **R1 identifies the reservation independent of its data**; immutable fields do not remove that. **Java equality is a separate implementation choice**; this class keeps object equality.
4. `jdeps` reports **compiled class relationships**; the tests compare edges with the matrix and search for **cycles**. They do not prove responsibilities are well chosen, see reflection or strings, or establish transactionality.

---

## Guidance: Questions 5 to 8

5. The console and API **disagree** if only one copies the rule. Put it in the domain policy; delegate both to the same operation. Send the same student request through both; also test an **allowed staff duration**.
6. Two requests can **both observe a free interval** and append different IDs. Unique IDs do not make **eligibility, conflict check and insertion atomic**.
7. `bootstrap` I = 1 can change freely, but must not accumulate business rules. `domain` I = 0: a change **ripples into every package**, so keep it small.
8. The **cycle test** catches it. The **direction test does not**: each reference is individually permitted.

---

## Transfer Challenge: A Clinic

A clinic appointment application has **eligibility rules, an external patient directory, a console view and an in-memory appointment list**.

* Propose **responsibilities and dependency directions** without inventing deployment services.
* Choose **one storage port**, say which layer owns its contract, and distinguish an appointment's **identity** from its scheduled-time **value**.
* Name **one behaviour to protect** during restructuring.
* Name **one change request** you would use to test whether your package cuts are cohesive.

---

## Transfer Guidance

* **Domain:** appointment times, patient identity, eligibility. **Application:** the booking operation, with a **patient-directory port** and a focused **appointment-store port**. **Infrastructure:** the provider adapter and in-memory store. **Presentation** delegates; **bootstrap** selects.
* An appointment has an **explicit identity**; its interval is a **value**. Do not assume either gives Java `equals`: specify interval validation, equality and duplicate-ID behaviour.
* **Preserve:** a conflicting interval is rejected **without storing another appointment or notifying anyone**. Also preserve **provider failure versus missing patient**.

---

# Summary and Next Chapter
### What to carry forward

---

## Summary

* Application structure makes responsibilities and dependency decisions **visible beyond individual classes**.
* The checkpoint adds **named packages**, a **narrow storage port**, **explicit assembly** and a **thin presentation adapter** while preserving tested outcomes.
* Package design adds four questions: **what changes together and is released together**, **what clients depend on**, **whether dependencies point towards stability**, and **whether a stable package is abstract enough to extend**.

---

## Deliberate Limitations

* **In-memory, sequential state.**
* **String results.**
* **Unchanged lifecycle rules.**
* **Chapter 11** examines refactoring and legacy code, building on the tests and boundaries established here.

---

## Sources and Further Reading

1. **Fowler:** *Presentation Domain Data Layering*; Stafford: *Service Layer*; Hieatt and Mee: *Repository*.
2. **Oracle:** the Java 17 `jdeps` command; Java SE 17 `List`.
3. **Cockburn:** *Hexagonal Architecture.*
4. **Evans:** *Domain-Driven Design Reference* (2015), pp. 10 to 17.
5. **Martin:** *Agile Software Development* (2002): principles of package design.

* Full references and links are in the chapter text.
