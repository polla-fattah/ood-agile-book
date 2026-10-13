---
title: "Week 5: SOLID II: Interfaces, Dependency Inversion & Composition"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 50
type: slides
layout: page
---

# Week 5: SOLID II: Interfaces, Dependency Inversion & Composition
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## 3-Hour Lecture Roadmap

* **Part 1: Notification Pressures & Coupled Construction (0:00 - 0:35)**
  * The notification requirement, the coupled coordinator defect, the illusion of interface-typed fields.
* **Part 2: Interface Segregation Principle (ISP) (0:35 - 1:05)**
  * Fat interfaces vs. client role interfaces, `NotificationSender`, multiple views of an object.
* **Part 3: Dependency Inversion Principle (DIP) & Source Direction (1:05 - 1:40)**
  * High-level policy vs. details, source-dependency inversion vs. runtime calls, Figure 6.1 architecture.
* **BREAK (1:40 - 1:55)**
* **Part 4: Constructor Injection & Composition Roots (1:55 - 2:25)**
  * Explicit constructors, defensive map copies, `ReservationApplication` root, Figure 6.2 object assembly, partial failure semantics.
* **Part 5: Educational DI Container & IoC Walkthrough (2:25 - 2:45)**
  * DIP vs. DI vs. IoC vs. Service Locator, `DemoContainer` walkthrough, lifecycle, caching, and cycle detection.
* **Part 6: Workshop Deliverables, Quiz 1 Revision & Wrap-Up (2:45 - 3:00)**
  * Lab steps 1-9, AI refactoring critique, comprehensive Quiz 1 revision (Chapters 2-5), preview of Week 6.

---

## Pedagogical Alignment & Module Context

* **Module Learning Outcomes:**
  * **LO1:** Critically evaluate and apply advanced object-oriented programming concepts (encapsulation, polymorphism, design principles).
  * **LO4:** Refactor and improve existing codebases using industry-standard design patterns, metrics, and static analysis.
* **Foundational Literature & Engineering Canon:**
  * Robert C. Martin (2000, 2002): *Agile Software Development: Principles, Patterns, and Practices* (ISP, DIP).
  * Martin Fowler (2004): *Inversion of Control Containers and the Dependency Injection Pattern*.
* **Assessment Milestone Notice:**
  * **Quiz 1** takes place this week! Stated revision coverage is strictly **Weeks 1 to 4** (Chapters 2 to 5).
  * Week 5 material (ISP, DIP, DI) is covered in Milestone 2 and the Midterm examination.

---

# Part 1: Notification Pressures & Coupled Construction

---

## The New Requirement: Local Notification Output

* **The Backlog Addition:**
  * Following an accepted reservation, the system must dispatch a notification notice to a configured output destination.
* **Formal Requirement Statement:**
  * *"After storing an accepted reservation, attempt one notification through the configured output. Rejected or invalid requests produce no notification. The configured output may record the accepted reservation in memory or print a notice to a supplied stream."*
* **Architectural Constraints:**
  * This is a **local teaching output** (console stream or in-memory list).
  * It is NOT a remote mail server, SMS gateway, or durable message broker.
  * Successful return means local output completed; it does not prove delivery to a human borrower.

---

## The Coupled Implementation: An Illusion of Decoupling

* Consider this initial attempt in `ReservationCoordinator.java`:

```java
public final class ReservationCoordinator {
    private final List<Reservation> reservations = new ArrayList<>();
    private final BorrowingPolicy studentPolicy = new ReservationRules();
    private final BorrowingPolicy staffPolicy = new StaffReservationRules();
    private final ConfirmationFormatter formatter = new ConfirmationFormatter();

    // LOOKS decoupled, but is it?
    private final NotificationSender notifications = 
            new ConsoleNotificationSender(System.out, new ConfirmationFormatter());
    ...
}
```

* **The Developer's Claim:**
  * *"The field is declared as `NotificationSender` (an interface), so my code is decoupled and follows SOLID!"*
* **The Reality:**
  * This code is heavily coupled and actively resists change.

---

## Dissecting the Construction Trap

```
       ReservationCoordinator (Domain Policy)
                 │
                 │ 1. Names concrete class
                 ▼
       ConsoleNotificationSender (Infrastructure Detail)
                 │
                 │ 2. Hardcodes global stream
                 ▼
             System.out (Operating System stdout)
```

* **Three Critical Defects in the Field Initializer:**
  1. **Source Coupling:** The coordinator imports and names `ConsoleNotificationSender`.
  2. **Environment Fixing:** Hardcodes `System.out`, making headless testing impossible without hijacking console output.
  3. **Duplicate Instantiation:** Re-creates an extra `ConfirmationFormatter` instead of sharing configuration.
* **The Testing Blockade:**
  * Automated regression tests cannot assert notification contents without capturing console standard output!

---

## The Failure Semantics Dilemma

* When the notification output fails, what should happen to the reservation?
* **Scenario:**
  * Borrower requests a camera.
  * The loan period is valid and available.
  * The reservation is successfully created and stored in memory.
  * The notification output throws an I/O exception (`NotificationException`).

* **Interactive Question for the Class:**
  * Should the coordinator:
    * (A) Delete the newly stored reservation and return `"Rejected"`?
    * (B) Throw a `RuntimeException` and crash the transaction?
    * (C) Retain the stored reservation, return the confirmation, and append an explicit failure notice?

---

## The Architectural Answer: Partial Success

* **Selected Rule:** Option (C) - Retain and Report!
* **The Coordinator Code:**

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

* **Why Option (A) is Toxic:**
  * If the console notice partially printed or remote SMS was already sent, deleting the booking creates a split-brain disaster: the user received a notice, but the system has no booking!
* **Why Option (B) is Dangerous:**
  * Unhandled exceptions disguise whether state was mutated before the failure.

---

## Defining the Baseline Acceptance Criteria

* Before refactoring the design, establish the exact behavioral contract:

| Scenario / Input | Expected Reservation Result | Expected Notification Observation |
|---|---|---|
| Eligible, available request | Exact confirmation string; 1 record stored | Exactly 1 notification sent to output |
| Overlapping date request | `"Rejected: item unavailable."` | Zero notification attempts |
| Limit/duration exceeded | `"Rejected: borrower limit or duration."` | Zero notification attempts |
| Blank borrower identifier | Throws `IllegalArgumentException` | Zero notification attempts |
| Output failure after booking | Confirmation + `" Notification failed; reservation retained."` | 1 attempt recorded; booking retained |
| Immediate repeat of booking | `"Rejected: item unavailable."` | Zero notification attempts |

---

# Part 2: Interface Segregation Principle (ISP)

---

## Defining the Interface Segregation Principle (ISP)

> "Clients should not be forced to depend upon interfaces that they do not use."  
> - Robert C. Martin (Uncle Bob), 2000, 2002

```
THE FAT INTERFACE ANTI-PATTERN
┌────────────────────────────────────────────────────────┐
│                   «interface»                          │
│                EquipmentPlatform                       │
├────────────────────────────────────────────────────────┤
│ +sendNotification(Reservation) : void                  │
│ +registerBorrower(String, String) : void               │
│ +exportInventoryCsv() : File                           │
│ +rotateCredentials(String) : void                      │
│ +deleteBorrowerAccount(String) : void                  │
└────────────────────────────────────────────────────────┘
          ▲                                    ▲
          │ (Only needs send)                  │ (Needs admin ops)
┌─────────┴──────────────┐           ┌─────────┴──────────────┐
│ ReservationCoordinator │           │   SystemAdminPortal    │
└────────────────────────┘           └────────────────────────┘
```

* If `EquipmentPlatform` changes its export CSV signature, `ReservationCoordinator` must be recompiled and redeployed!

---

## The Role Interface Solution: `NotificationSender`

* Instead of an all-purpose platform interface, define a client-driven role:

```java
/**
 * Accept one non-null confirmed reservation for this implementation's local output.
 * Do not modify the reservation or coordinator. Report expected output failure with
 * NotificationException. Normal return is not a promise of email delivery.
 */
@FunctionalInterface
public interface NotificationSender {
    void send(Reservation reservation);
}
```

* **Key Properties of this Contract:**
  * **Client-Specific:** Defined by what `ReservationCoordinator` needs to get its job done.
  * **Minimal Surface:** Exactly one cohesive operation (`send`).
  * **Contractual Boundary:** Documents exceptions (`NotificationException`) and state invariants.

---

## Is ISP Just "Make All Interfaces Have 1 Method"?

* **Critical Distinction:** Small does NOT automatically mean one method!
* **The Guiding Rule:**
  * An interface should represent a single cohesive client role.
  * If a client genuinely requires three methods to manage a lifecycle safely (e.g., `open()`, `write()`, `close()`), forcing them into three separate interfaces destroys encapsulation.

```
Cohesive Multi-Method Role:
┌──────────────────────────────────────┐
│             «interface»              │
│          TransactionalBatch          │
├──────────────────────────────────────┤
│ +begin() : void                      │
│ +submit(Command cmd) : void          │
│ +commit() : void                     │
└──────────────────────────────────────┘
(These belong together because calling submit without begin/commit is invalid!)
```

---

## Concrete Implementations: Console vs. Recording

```java
// Production / CLI Demo Implementation
public final class ConsoleNotificationSender implements NotificationSender {
    private final PrintStream output;
    private final ConfirmationFormatter formatter;

    public ConsoleNotificationSender(PrintStream output, 
                                   ConfirmationFormatter formatter) {
        this.output = Objects.requireNonNull(output, "output");
        this.formatter = Objects.requireNonNull(formatter, "formatter");
    }

    @Override
    public void send(Reservation reservation) {
        output.println("Notice: " + formatter.format(reservation));
        if (output.checkError()) {
            throw new NotificationException("Console output failed.");
        }
    }
}
```

* Notice: Translates `PrintStream.checkError()` into domain-level `NotificationException`.

---

## Multiple Views of One Object: `RecordingNotificationSender`

* In testing, we need to inspect what was sent:

```java
public final class RecordingNotificationSender implements NotificationSender {
    private final List<Reservation> received = new ArrayList<>();

    @Override
    public void send(Reservation reservation) {
        received.add(Objects.requireNonNull(reservation, "reservation"));
    }

    // INSPECTION METHOD: Not on NotificationSender!
    public List<Reservation> received() { 
        return List.copyOf(received); 
    }
}
```

```
               ┌───────────────────────┐
               │  NotificationSender   │
               │  +send(Reservation)   │
               └───────────▲───────────┘
                           │ implements
               ┌───────────┴───────────┐
               │ RecordingNotification │
               │        Sender         │
               ├───────────────────────┤
               │ +received() : List    │ ◄── Only Test Harness calls this!
               └───────────────────────┘
```

---

## Domain Payloads vs. Transport Payloads

* Notice what `NotificationSender.send(...)` receives:
  * It takes a complete, immutable `Reservation` domain record!
* **Why not pass raw primitives?**
  * `void send(String borrowerId, String itemId, LocalDate start, LocalDate end)`
  * That creates a 4-parameter list and duplicates reservation concept extraction.
* **Why not pass transport-specific payloads?**
  * `void send(MimeMessage email)` or `void send(AwsSnsPayload payload)`
  * That leaks infrastructure protocols into domain logic.
* **The Balanced Design:**
  * The domain model passes its own immutable entity (`Reservation`).
  * The concrete adapter formats or maps it as needed.

---

# Part 3: Dependency Inversion Principle (DIP)

---

## Defining the Dependency Inversion Principle (DIP)

> "A. High-level modules should not depend on low-level details. Both should depend on abstractions."  
> "B. Abstractions should not depend on details. Details should depend on abstractions."  
> - Robert C. Martin (Uncle Bob), 2000, 2002

```
TRADITIONAL TOP-DOWN DEPENDENCY (Violates DIP)
┌────────────────────────────┐
│   ReservationCoordinator   │ (High-level business policy)
└──────────────┬─────────────┘
               │ depends on concrete
               ▼
┌────────────────────────────┐
│  ConsoleNotificationSender │ (Low-level I/O detail)
└────────────────────────────┘

DEPENDENCY INVERSION (Conforms to DIP)
┌────────────────────────────┐        ┌────────────────────────────┐
│   ReservationCoordinator   │ ─────► │   «role» NotificationSender│
└────────────────────────────┘        └──────────────▲─────────────┘
  (High-level policy)                                │ implements
                                      ┌──────────────┴─────────────┐
                                      │  ConsoleNotificationSender │
                                      └────────────────────────────┘
                                        (Low-level detail)
```

---

## Inverting Knowledge, Not Execution

* **A Common Student Confusion:**
  * *"Does Dependency Inversion mean the console sender calls the coordinator at runtime?"*
* **The Crucial Clarification:**
  * **Runtime Control Flow:** The coordinator calls `send(...)` on the sender. Control flows forward.
  * **Compile-Time Source Dependency:** The coordinator's source code depends on an interface that *belongs to the coordinator's domain*, while the sender depends on that interface.
* **Who Owns the Abstraction?**
  * In classic procedural architecture, the database or network defines the interface.
  * In Inverted Architecture, the domain defines the interface it requires!

---

## Source Dependencies vs. Runtime Wiring (Figure 6.1)

```
        COMPILATION / SOURCE KNOWLEDGE VIEW (Figure 6.1)
┌────────────────────────┐
│ ReservationApplication │ ──creates──► ReservationCoordinator
└───────────┬────────────┘ ──creates──► ConsoleNotificationSender
            │              ──creates──► ReservationRules / StaffRules
            ▼              ──creates──► ConfirmationFormatter
┌────────────────────────┐
│   NotificationSender   │ ◄──notifies── ReservationCoordinator
└───────────▲────────────┘
            │ implements
┌───────────┴────────────┐
│ConsoleNotificationSend │
└────────────────────────┘
```

* **The Key Shift from Chapter 5:**
  * In Chapter 5, the coordinator had direct "creates" arrows to concrete policies.
  * In Chapter 6, **every "creates" arrow originates in `ReservationApplication`!**
  * The coordinator's source code is 100% free of concrete sender references.

---

## Dependency Injection (DI) != DIP

* Can you have Dependency Injection WITHOUT Dependency Inversion?
* **Yes! Look at this constructor:**

```java
public ReservationCoordinator(ConsoleNotificationSender sender) {
    this.notifications = Objects.requireNonNull(sender);
}
```

* **Analysis:**
  * Is dependency injection occurring? **Yes.** The collaborator is passed in from outside.
  * Is dependency inversion satisfied? **No!** The high-level coordinator still explicitly names the concrete `ConsoleNotificationSender` class!
* **DIP requires BOTH:**
  1. Collaborators supplied from outside (Injection).
  2. Collaborators typed as client-owned abstractions (Inversion).

---

## When Concrete Dependencies are Entirely Acceptable

* Should *every* single class have an interface?
* In our finished system, what remains concrete?
  * `LoanPeriod` - Value object. Pure domain logic, zero variation.
  * `Reservation` - Immutable record entity.
  * `ConfirmationFormatter` - Concrete class injected directly into the coordinator.
* **Why does `ConfirmationFormatter` not have an `IConfirmationFormatter`?**
  * There is currently only one confirmation format.
  * No requirement exists to swap formatters dynamically.
  * Adding an interface solely to satisfy a rule of thumb is speculative over-engineering.

---

## Preview: Data-Backed Collaborators (Chapter 8)

* The same principle applies when reading external data:

```java
/** Empty means absent or inactive; never an infrastructure outage. */
@FunctionalInterface
public interface BorrowerDirectory {
    Optional<Borrower> find(String borrowerId);
}
```

* **The Contract Promises:**
  * Returns `Optional.empty()` if borrower does not exist.
  * Throws `DirectoryOutageException` if database/network fails.
  * Uses application domain entity `Borrower`, not SQL `ResultSet` or HTTP JSON.
* The application owns this interface. PostgreSQL or LDAP adapters implement it.

---

# Part 4: Constructor Injection & Composition Roots

---

## Eliminating Hidden State: Constructor Injection

* We replace the no-argument coordinator constructor with explicit parameterization:

```java
public final class ReservationCoordinator {
    private final List<Reservation> reservations = new ArrayList<>();
    private final Map<BorrowerCategory, BorrowingPolicy> policies;
    private final ConfirmationFormatter formatter;
    private final NotificationSender notifications;

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
    ...
```

---

## Defensive Copying & Configuration Invariants

* Notice two critical defensive programming techniques in the constructor:

1. **`Map.copyOf(...)`:**
   * Creates an unmodifiable shallow snapshot.
   * If the caller mutates their input map after construction, the coordinator is completely unaffected!
   * Rejects null keys and null values automatically.
2. **Category Completeness Check:**
   * Loops through all `BorrowerCategory.values()`.
   * Throws `IllegalArgumentException` immediately if any category lacks a policy.
   * **Fail Fast:** Configuration errors explode at startup, not in production when a staff member submits a booking!

---

## Constructor Injection vs. Setter Injection

* Why avoid setter injection for core collaborators?

```
CONSTRUCTOR INJECTION: Safe & Complete
ReservationCoordinator c = new ReservationCoordinator(policies, fmt, sender);
c.reserve(...); // GUARANTEED to be fully initialized and valid

SETTER INJECTION: Temporal Coupling Risk
ReservationCoordinator c = new ReservationCoordinator();
c.reserve(...); // CRASH! NullPointerException (someone forgot to call setSender!)
c.setFormatter(fmt);
c.setSender(sender);
```

* **Rule of Thumb:**
  * Use **Constructor Injection** for mandatory, immutable dependencies.
  * Use **Setter Injection** only for truly optional runtime adjustments.

---

## The Composition Root Pattern

* A **Composition Root** is the centralized location where concrete components are instantiated and wired together.

```java
public final class ReservationApplication {
    private ReservationApplication() { }

    // Factory method for assembling standard graph
    public static ReservationCoordinator create(NotificationSender sender) {
        return new ReservationCoordinator(
                Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                       BorrowerCategory.STAFF, new StaffReservationRules()),
                new ConfirmationFormatter(), 
                sender);
    }

    public static void main(String[] args) {
        ConfirmationFormatter noticeFormat = new ConfirmationFormatter();
        NotificationSender sender = 
                new ConsoleNotificationSender(System.out, noticeFormat);
        ReservationCoordinator coordinator = create(sender);
        ...
    }
}
```

---

## Object Assembly View (Figure 6.2)

* Do not confuse source diagrams with runtime object graphs!

```
               RUNTIME OBJECT GRAPH (Figure 6.2)
                ┌────────────────────────┐
                │ ReservationApplication │
                └───────────┬────────────┘
                            │ constructs & wires
    ┌───────────────────────┼───────────────────────┐
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐       ┌───────────────┐
│  Policy Map   │   │  Formatter    │       │ ConsoleSender │
└───────┬───────┘   └───────┬───────┘       └───────┬───────┘
        │                   │                       │
        └───────────────────┼───────────────────────┘
                            │ passed into constructor
                            ▼
                ┌────────────────────────┐
                │ ReservationCoordinator │
                └────────────────────────┘
```

* Classes are static; objects are dynamic instances created in memory at boot time.

---

## Sticky Error States in `PrintStream.checkError()`

* Why did `ConsoleNotificationSender` use `output.checkError()`?

```java
output.println("Notice: " + formatter.format(reservation));
if (output.checkError()) {
    throw new NotificationException("Console output failed.");
}
```

* **The Java Standard Library Quirk:**
  * Java's `PrintStream` suppresses `IOException` from its write methods!
  * If stdout is closed or broken, `println` returns silently.
  * You MUST call `checkError()` to detect I/O failure.
* **The "Sticky" Error Trap:**
  * Once `PrintStream` records an error, `checkError()` returns `true` forever.
  * Subsequent writes to the same stream will all be reported as failed.

---

## Migrating Caller Tests: The Clean Seam

* Because we removed the no-argument constructor:
  * Old test suites (`Chapter02Checks`, `Chapter05Checks`) must be updated.
* **How they are migrated:**
  * They now instantiate the coordinator through a test fixture:

```java
RecordingNotificationSender inbox = new RecordingNotificationSender();
ReservationCoordinator coordinator = ReservationApplication.create(inbox);
```

* **The Payoff:**
  * The domain checks run identically.
  * We can now assert notification counts without touching standard out!
  * Zero changes to reservation rules, boundary checks, or interval math.

---

# Part 5: Inversion of Control & Educational DI Containers

---

## Disentangling the Buzzwords

| Term | Core Meaning | Question It Answers |
|---|---|---|
| **DIP** | Design principle regarding abstraction ownership | Does high-level policy avoid naming concrete providers? |
| **DI** | Object composition technique | Who passes collaborators into the class? |
| **IoC** | Broad architectural paradigm | Who controls the program's execution lifecycle? |
| **DI Container** | Tool/Library for automated dependency wiring | What manages bean registration and resolution? |
| **Service Locator** | Registry anti-pattern where objects fetch dependencies | Does an object query a global context to find helpers? |

---

## Service Locator: The Disguised Anti-Pattern

* Contrast Dependency Injection with Service Locator:

```
DEPENDENCY INJECTION (Clear, Explicit)
public ReservationCoordinator(NotificationSender sender) { ... }
-> Callers see exact requirements in constructor signature.

SERVICE LOCATOR (Hidden, Fragile)
public ReservationCoordinator(ServiceRegistry registry) {
    this.sender = (NotificationSender) registry.get("mail_service");
}
-> Constructor hides real dependencies.
-> Fails at runtime if key "mail_service" is misspelled.
-> Tightly couples domain to ServiceRegistry!
```

* **Rule:** Pass objects their dependencies; do not pass them a phonebook to look up their dependencies!

---

## The Educational Container: `DemoContainer`

* In `ContainerWalkthrough.java`, we build a complete plain-Java DI container in 35 lines!

```java
static final class DemoContainer {
    private final Map<Class<?>, Supplier<?>> providers = new HashMap<>();
    private final Map<Class<?>, Object> instances = new HashMap<>();
    private final Set<Class<?>> constructing = new HashSet<>();

    public <T> void bind(Class<T> type, Supplier<? extends T> provider) {
        if (providers.containsKey(type)) throw new IllegalArgumentException("Duplicate");
        providers.put(type, provider);
    }

    public <T> T get(Class<T> type) {
        if (instances.containsKey(type)) return type.cast(instances.get(type));
        Supplier<?> provider = providers.get(type);
        if (provider == null) throw new IllegalArgumentException("Missing binding");
        if (!constructing.add(type)) throw new IllegalStateException("Dependency cycle");
        try {
            T instance = type.cast(provider.get());
            instances.put(type, instance);
            return instance;
        } finally {
            constructing.remove(type);
        }
    }
}
```

---

## Wiring the Object Graph with `DemoContainer`

```java
public static void main(String[] args) {
    DemoContainer container = new DemoContainer();

    // 1. Register Formatter
    container.bind(ConfirmationFormatter.class, ConfirmationFormatter::new);

    // 2. Register Notification Role to Recorder Implementation
    container.bind(NotificationSender.class, RecordingNotificationSender::new);

    // 3. Register Coordinator, resolving dependencies dynamically
    container.bind(ReservationCoordinator.class, () -> new ReservationCoordinator(
            Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                   BorrowerCategory.STAFF, new StaffReservationRules()),
            container.get(ConfirmationFormatter.class),
            container.get(NotificationSender.class)));

    // 4. Resolve application root
    ReservationCoordinator coordinator = container.get(ReservationCoordinator.class);
    ...
```

---

## Container Lifecycle: Singletons & State Mutation

* When `container.get(ReservationCoordinator.class)` is called twice:
  * It returns the exact same cached instance!

```
First Call:
container.get(Coordinator.class) ──► Builds new instance ──► Caches in instances map

Second Call:
container.get(Coordinator.class) ──► Returns cached instance directly
```

* **The Architectural Warning:**
  * "Singleton" does NOT mean "Thread-Safe"!
  * Because the coordinator holds mutable in-memory state (`reservations` list), multiple threads resolving the singleton share the un-synchronized list.
  * Lifetime management is an explicit architectural decision.

---

## How Real Frameworks Work (Spring / Guice / CDI)

* Whether using plain Java or enterprise Spring:
  * Every DI container performs the exact same **three fundamental jobs**:

```
1. REGISTRATION    ──► Map interfaces/keys to factories/classes (@Bean, @Component)
2. RESOLUTION      ──► Inspect parameters, traverse graph, and instantiate (@Autowired)
3. LIFETIME        ──► Decide whether to reuse or create fresh (@Scope: singleton vs prototype)
```

* **Key Takeaway:**
  * Frameworks add annotations, reflection, and XML, but the architectural principles (ISP, DIP, Composition Root) remain identical!

---

# Part 6: Workshop Deliverables, Quiz 1 Revision & Wrap-Up

---

## Bounding AI Refactoring: The "Global Context" Trap

* A student prompts an AI assistant:  
  *"Refactor ReservationCoordinator to follow DIP."*
* **The AI's Hallucinated Proposal:**

> "I made it DIP!  
> 1. Pass a global `ApplicationContext` into the coordinator constructor.  
> 2. Inside `reserve(...)`, call `context.getBean(NotificationService.class)`.  
> 3. Add `configureMailServer()`, `exportAuditLog()`, and `deleteAccount()` to `NotificationService`.  
> 4. Catch all exceptions and return null."

* **Class Discussion:** How does this violate both ISP and DIP?
  * Violates ISP: Pollutes sender with administrative garbage.
  * Violates DIP: Converts explicit injection into a Service Locator anti-pattern.

---

## Workshop Practical Activity: 9-Step Workflow

* **Steps 1-8: Campus Equipment Lending System (Book Project)**
  1. Define `NotificationSender` role interface (exclude administrative operations).
  2. Implement `ConsoleNotificationSender` and `RecordingNotificationSender`.
  3. Refactor `ReservationCoordinator` constructor to require dependencies; defensively copy policy map.
  4. Build `ReservationApplication` composition root.
  5. Migrate all test suites to use the injected coordinator.
  6. Verify partial failure: record retained + error suffix returned.
  7. Draw separate Figure 6.1 (source) and Figure 6.2 (object) diagrams.
  8. Run `ContainerWalkthrough.java` to test cycle detection and caching.
* **Step 9: Team Project Transfer**
  * Identify one concrete environment choice your team project constructs for itself (e.g., database connection, file logger). Sketch how to extract and inject it.

---

## Quiz 1 Comprehensive Revision: Chapters 2-5

* **Quiz 1 takes place this week!**
  * Stated coverage is strictly **Weeks 1 to 4 (Chapters 2 to 5)**.
  * Review the 4 core pillars:

```
Week 1 (Ch 2) ──► Encapsulation, Invariants, [start, endExclusive),
                  Cohesion & Coupling, UML Class Diagrams.
Week 2 (Ch 3) ──► Agile Values, User Stories, INVEST, Given-When-Then,
                  WIP Limits, Little's Law.
Week 3 (Ch 4) ──► Capacity Planning (75% Load), WBS, Git Hygiene,
                  AAA Pattern, CI Quality Gates.
Week 4 (Ch 5) ──► SRP (Actors), OCP (Variation Axis), LSP (Contracts),
                  Fowler Smells, PMD Static Analysis.
```

---

## High-Yield Quiz 1 Revision Questions

* **1. Interval Invariants:**
  * Why does `LoanPeriod` enforce `start.isBefore(endExclusive)` rather than allowing equal dates?
* **2. Git Line Endings:**
  * Why is `*.sh text eol=lf` in `.gitattributes` vital for cross-platform Linux CI?
* **3. Liskov Substitution:**
  * Why did `PositiveOnlyHistory` violate LSP even though it compiled with `@Override`?
* **4. Static Analysis:**
  * Why did extracting `ConfirmationFormatter` fail to reduce cyclomatic complexity?
* **5. Agile Estimation:**
  * Why does gross capacity differ from net capacity (load factor)?

---

## Summary of SOLID Principles Learned So Far

```
S - Single Responsibility Principle (Week 4)
    A class should have one, and only one, reason to change (actor).

O - Open-Closed Principle (Week 4)
    Open for extension, closed for modification along a named axis.

L - Liskov Substitution Principle (Week 4)
    Subtypes must satisfy supertype behavioral contracts.

I - Interface Segregation Principle (Week 5)
    Clients should not depend on methods they do not call.

D - Dependency Inversion Principle (Week 5)
    High-level policy depends on abstractions; details depend on abstractions.
```

---

## Looking Ahead to Week 6

* **Next Lecture: Testing as a Design Practice: TDD & Test Doubles**
  * **Test-Driven Development (TDD):** Red-Green-Refactor rhythm.
  * **Test Double Taxonomy (Meszaros):** Fakes vs. Stubs vs. Mocks vs. Spies vs. Dummies.
  * **Using Mockito responsibly:** Mocking interfaces vs. over-mocking domain values.
  * **Milestone 2 Delivery:** Assembling the first working system iteration.

---

# Questions & Discussion
### SE506: Object Oriented Development and Agile Practices
*Slides and code available on the module repository.*
