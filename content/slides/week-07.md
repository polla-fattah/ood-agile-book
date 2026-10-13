---
title: "Week 7: Creational Patterns & Object Construction"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 70
type: slides
layout: page
---

# Week 7: Creational Patterns & Object Construction
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## 3-Hour Lecture Roadmap

* **Part 1: Why Object Construction is a Design Problem (0:00 - 0:35)**
  * When constructors are fine vs. when creation becomes troublesome; creation vs. compatibility vs. added behavior; the Directory Dilemma.
* **Part 2: Factory Method vs. Simple Factory (0:35 - 1:05)**
  * Simple static factories vs. GoF Factory Method subclass hooks (`ExportJob`); Figure 8.1 architecture; when to decline the pattern.
* **Part 3: Abstract Factory & Product Families (1:05 - 1:35)**
  * Enforcing product consistency (`ReceiptFamily`), avoiding mixed-mode defects, testing family relationships.
* **BREAK (1:35 - 1:50)**
* **Part 4: The Builder Pattern & Immutable Requests (1:50 - 2:20)**
  * Telescoping constructors, staged fluent configuration, invariant validation before publication, preventing builder mutation leaks.
* **Part 5: Adapter & Data-Backed Collaborators (2:20 - 2:45)**
  * Translating legacy vendor records (`S`, `T`, `Y`, `N`), absence vs. outage, `DirectoryReservationService`, Figure 8.2 sequence diagram.
* **Part 6: Decorator, AI Critique, Midterm Prep & Wrap-Up (2:45 - 3:00)**
  * Decorator execution order, auditing AI pattern advice, Midterm exam review (Chapters 2-7), preview of Week 8.

---

## Pedagogical Alignment & Module Context

* **Module Learning Outcomes:**
  * **LO2:** Analyze, select, and implement appropriate software design patterns (creational, structural, and behavioral) to address architectural challenges.
* **Foundational Literature & Engineering Canon:**
  * Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (1994): *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF).
  * Robert C. Martin (2002): *Agile Software Development: Principles, Patterns, and Practices* (Factories and Adapters).
* **Midterm Examination Alignment:**
  * The Midterm Examination covers strictly **Weeks 1 to 6 (Chapters 2 to 7)**!
  * Chapter 8 patterns are assessed in Milestone 3, Assignment 2, and the Final Exam.
  * Today includes dedicated Midterm practice exercises covering UML, smells, refactoring, and test doubles.

---

# Part 1: Why Object Construction is a Design Problem

---

## When Plain Constructors are Perfectly Fine

* In software engineering, the simplest design that satisfies requirements is preferred:

```java
// Ordinary constructor: Clear, deterministic, validates own invariants
LoanPeriod period = new LoanPeriod(start, endExclusive);
```

* **Why this needs no Factory, Builder, or Abstract Provider:**
  * Exactly two required arguments.
  * Invariant is self-contained: `start.isBefore(endExclusive)`.
  * The resulting object is immediately complete, valid, and immutable.
* **The Golden Rule of Creational Patterns:**
  * Do NOT replace simple, readable constructors with creational design patterns unless an explicit change pressure justifies the boundary!

---

## Three Creational Smells That Demand Patterns

* Construction becomes a design problem under three specific pressures:

```
                  ┌────────────────────────────────────────┐
                  │       CREATIONAL CODE SMELLS           │
                  └───────────────────┬────────────────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       ▼                              ▼                              ▼
1. Repeated Type Selection    2. Incompatible Pairing       3. Telescoping Parameters
Callers repeat if-else       Caller accidentally combines  Constructor has 8 args
logic deciding WHICH class   HTML heading with Plain body  full of nulls, booleans,
to instantiate.              (Product Family mismatch).    and mystery integers.
-> Factory Method            -> Abstract Factory           -> Builder
```

---

## Distinguishing Creation, Compatibility & Added Behavior

* Many developers confuse GoF design patterns because they all use interfaces and composition:

| Pattern Category | Primary Intent | Core Diagnostic Question | Archetypal Pattern |
|---|---|---|---|
| **Creational** | Isolate instantiation decisions | *"Who decides which concrete class or family to create?"* | Factory Method, Abstract Factory, Builder |
| **Structural (Compatibility)** | Bridge mismatched interfaces | *"How do we make an existing provider look like our domain contract?"* | Adapter |
| **Structural (Extension)** | Attach optional behaviors | *"How do we add logging or retries without changing the interface?"* | Decorator |

* Naming every wrapper a "factory" destroys architectural precision.

---

## The External Directory Dilemma

* **The New Requirement in Chapter 8:**
  * The Equipment Office wants borrower categories to come from the university directory rather than trusting a category parameter passed by the caller.
* **The Raw Legacy Provider Contract:**
  * Vendor interface: `LegacyDirectoryClient.lookup(String key)`.
  * Returns raw `Person` record: `key`, `kind`, and `status`.
  * Vendor encoding rules:
    * `kind = "S"` means Student; `kind = "T"` means Staff (Teacher).
    * `status = "Y"` means Active; `status = "N"` means Inactive.
    * Returns `null` when a user is not found in the database.
    * Throws `LegacyDirectoryClient.Failure` on network timeout or database crash.

---

## The Tempting Hack: Polluting Domain Policy

* What happens if we put legacy vendor handling directly in `ReservationCoordinator`?

```java
// TOXIC: Leaking external vendor codes into core domain logic!
if (person == null || person.status().equals("N")) {
    return "Rejected: borrower not found or inactive.";
}
BorrowerCategory category = switch (person.kind()) {
    case "S" -> BorrowerCategory.STUDENT;
    case "T" -> BorrowerCategory.STAFF;
    default -> throw new IllegalStateException("Unknown kind: " + person.kind());
};
```

* **Why this is an architectural disaster:**
  * Couples core lending rules to external vendor string conventions.
  * If the university upgrades to LDAP or OAuth tomorrow, the reservation engine must be rewritten!
  * Violates SRP, DIP, and clean architecture boundaries.

---

## The Architectural Strategy: Single Boundary Adapter

```
               DOMAIN BOUNDARY (Application Owned)
┌───────────────────────────────┐        ┌───────────────────────────────┐
│  DirectoryReservationService  │ ─────► │   «interface» BorrowerDirectory
└───────────────────────────────┘        └───────────────▲───────────────┘
  (Public entry point; orchestrates                       │ implements
   lookup then reservation)              ┌───────────────┴───────────────┐
                                         │    LegacyDirectoryAdapter     │
                                         └───────────────┬───────────────┘
                                           (Translates)  │ delegates
                                                         ▼
                                         ┌───────────────────────────────┐
                                         │     LegacyDirectoryClient     │
                                         └───────────────────────────────┘
                                           INFRASTRUCTURE / VENDOR VENDOR
```

* The domain defines `BorrowerDirectory.find(...)` returning `Optional<Borrower>`.
* `LegacyDirectoryAdapter` isolates all legacy vendor codes.

---

# Part 2: Factory Method vs. Simple Factory

---

## The Simple Factory: Centralized Selection

* Consider an export utility that formats receipts as text or HTML:

```java
public static Exporter simpleExporter(boolean html) {
    if (html) {
        return value -> "<p>" + value + "</p>";
    }
    return value -> "TEXT: " + value;
}
```

* **Characteristics of a Simple Factory:**
  * Typically a static method or standalone helper class.
  * Contains a conditional (`if` or `switch`) selecting between implementations.
  * Owned by a single assembly location.
* **Limitation:**
  * Adding a Markdown exporter requires modifying the conditional (violates OCP).
  * Does NOT provide an overridable inheritance hook.

---

## The GoF Factory Method Pattern

> "Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses."  
> - Gamma, Helm, Johnson, Vlissides (GoF), 1994

```
                          ┌────────────────────────┐
                          │   «abstract» ExportJob  │
                          ├────────────────────────┤
                          │ +run(value) : String   │ ◄── Fixed Workflow
                          │ #createExporter() : Exp│ ◄── Overridable Hook
                          └───────────▲────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
    ┌────────────────────────┐                ┌────────────────────────┐
    │        PlainJob        │                │        HtmlJob         │
    ├────────────────────────┤                ├────────────────────────┤
    │ #createExporter()      │                │ #createExporter()      │
    └────────────────────────┘                └────────────────────────┘
```

* The superclass owns the algorithm (`run`); subclasses supply the creation decision (`createExporter`).

---

## Factory Method in Code: `ExportJob`

```java
public abstract static class ExportJob {
    // The Factory Method: Protected creation hook
    protected abstract Exporter createExporter();

    // The Template Workflow: Fixed algorithm using the created product
    public final String run(String value) {
        Objects.requireNonNull(value, "value");
        Exporter exporter = createExporter(); // Defer to subclass!
        return exporter.export(value);
    }
}

public static final class PlainJob extends ExportJob {
    @Override
    protected Exporter createExporter() {
        return value -> "TEXT: " + value;
    }
}

public static final class HtmlJob extends ExportJob {
    @Override
    protected Exporter createExporter() {
        return value -> "<p>" + value + "</p>";
    }
}
```

---

## Factory Method vs. Simple Factory: Summary

| Feature | Simple Factory | GoF Factory Method |
|---|---|---|
| **Mechanism** | Centralized method with `switch`/`if` | Inheritance and polymorphic method override |
| **Extension Point** | Modify the central selection method | Create a new subclass of the abstract creator |
| **Workflow Coupling** | Creator is independent of product use | Creator owns a fixed template workflow (`run`) |
| **Complexity** | 1 class or static method | Hierarchy of abstract and concrete creators |

* **Warning:** Simply naming a method `create()` or putting `Factory` in a class name does NOT make it the GoF Factory Method pattern!

---

## When to Decline Factory Method

* In Chapter 6, we designed:
  * `ReservationApplication.create(sender)`
* Should we convert `ReservationApplication` into an abstract creator hierarchy with `StudentReservationApplication` and `StaffReservationApplication`?
* **The Architectural Decision: NO!**
  * `create(sender)` is an application assembly function, not a workflow hook.
  * Adding subclasses would introduce tight inheritance coupling for zero benefit.
* **Takeaway:** Decline Factory Method when simple constructor injection or assembly functions already solve the problem.

---

# Part 3: Abstract Factory & Product Families

---

## The Product Family Problem

* **Scenario: Generating Lending Receipts**
  * A receipt consists of two distinct UI components:
    1. A `Heading` renderer.
    2. A `Body` renderer.
  * Both components must share the same presentation style:
    * Plain Text Receipt: `PlainHeading` + `PlainBody`.
    * HTML Fragment Receipt: `HtmlHeading` + `HtmlBody`.
* **The Bug in Loose Factories:**
  * A developer configures `receipt(headingFactory.create(), bodyFactory.create())`.
  * Due to a configuration misconfiguration, the system renders an HTML heading `<h1` combined with raw unescaped plain text body lines!
  * **Result:** Broken markup and presentation defects.

---

## The Abstract Factory Pattern

> "Provide an interface for creating families of related or dependent objects without specifying their concrete classes."  
> - Gamma et al. (GoF), 1994

```
                       ┌──────────────────────┐
                       │     «interface»      │
                       │    ReceiptFamily     │
                       ├──────────────────────┤
                       │ +heading() : Heading │
                       │ +body() : Body       │
                       └──────────▲───────────┘
                                  │
            ┌─────────────────────┴─────────────────────┐
            │                                           │
┌───────────────────────┐                   ┌───────────────────────┐
│      PlainFamily      │                   │      HtmlFamily       │
├───────────────────────┤                   ├───────────────────────┤
│ +heading() -> PlainH  │                   │ +heading() -> HtmlH   │
│ +body()    -> PlainB  │                   │ +body()    -> HtmlB   │
└───────────────────────┘                   └───────────────────────┘
```

* Clients receive a `ReceiptFamily` reference; impossible to accidentally mix plain and HTML components!

---

## Abstract Factory in Code: `ReceiptFamily`

```java
public interface ReceiptFamily {
    Heading heading();
    Body body();
}

public static final class PlainFamily implements ReceiptFamily {
    @Override public Heading heading() { return title -> title + "\n"; }
    @Override public Body body() { return text -> text + "\n"; }
}

public static final class HtmlFamily implements ReceiptFamily {
    @Override public Heading heading() { return title -> "<h1>" + escape(title) + "</h1>"; }
    @Override public Body body() { return text -> "<p>" + escape(text) + "</p>"; }
}

// Client Workflow: Guarantees family consistency!
public static String renderReceipt(ReceiptFamily family, String title, String detail) {
    return family.heading().render(title) + family.body().render(detail);
}
```

---

## Testing Abstract Factory Consistency

* Unit tests must verify that components operate together without cross-contamination:

```java
@Test
void plainFamilyProducesMatchingTextLines() {
    String output = renderReceipt(new PlainFamily(), "Loan", "R1");
    assertEquals("Loan\nR1\n", output);
}

@Test
void htmlFamilyProducesMatchingHtmlTagsWithEscaping() {
    String output = renderReceipt(new HtmlFamily(), "Loan <1>", "R1 & CAM1");
    assertEquals("<h1>Loan &lt;1&gt;</h1><p>R1 &amp; CAM1</p>", output);
}
```

* **Design Tradeoff:**
  * Adding a new family (`MarkdownFamily`) is easy (OCP).
  * Adding a new product role (`Footer`) requires updating the `ReceiptFamily` interface and modifying every concrete family class!

---

# Part 4: The Builder Pattern & Immutable Requests

---

## The Telescoping Constructor Problem

* Suppose the equipment office needs a complex audit report request:

```java
// TELESCOPING CONSTRUCTOR ANTI-PATTERN
public ReportRequest(String borrowerId, LocalDate start, LocalDate end, 
                     boolean includeReturned, boolean includeDamaged, 
                     String format, List<String> columns, int maxRows) { ... }
```

* Calling this in client code:
```java
var req = new ReportRequest("B1", null, null, true, false, "CSV", null, -1);
```
* **Critical Defects:**
  * Which boolean means `includeReturned` vs `includeDamaged`?
  * What do the `null` dates mean?
  * Prone to catastrophic positional argument swapping errors!

---

## The GoF Builder Pattern (Fluent Request Variant)

> "Separate the construction of a complex object from its representation so that the same construction process can create different representations."  
> - Gamma et al. (GoF), 1994

```java
var request = ReportRequest.forBorrower("B1")
        .during(start, start.plusDays(7))
        .includeReturned(true)
        .column("item")
        .column("date")
        .build();
```

* **Three Fundamental Principles of Safe Builders:**
  1. **Fluent Staged Configuration:** Readable, self-documenting method chaining.
  2. **Validation at Publication:** Invariants checked inside `build()`.
  3. **Immutable Product:** The built object has no setters and defensively copies data.

---

## Inside `ReportRequest.Builder`

```java
public final class ReportRequest {
    private final String borrowerId;
    private final LoanPeriod period; // Optional interval
    private final boolean includeReturned;
    private final List<String> columns;

    public static Builder forBorrower(String borrowerId) {
        return new Builder(borrowerId);
    }

    public static final class Builder {
        private final String borrowerId;
        private LocalDate start;
        private LocalDate endExclusive;
        private boolean includeReturned = false; // Explicit default
        private final List<String> columns = new ArrayList<>();

        private Builder(String borrowerId) {
            if (borrowerId == null || borrowerId.isBlank()) 
                throw new IllegalArgumentException("Borrower required.");
            this.borrowerId = borrowerId;
        }
        ...
```

---

## Enforcing Immutability & Invariants at `build()`

```java
        public Builder during(LocalDate start, LocalDate endExclusive) {
            this.start = start;
            this.endExclusive = endExclusive;
            return this;
        }

        public Builder column(String label) {
            columns.add(Objects.requireNonNull(label));
            return this;
        }

        public ReportRequest build() {
            LoanPeriod period = (start != null || endExclusive != null)
                    ? new LoanPeriod(start, endExclusive) // Validates dates!
                    : null;
            // DEFENSIVE COPY: Isolates built product from future builder edits!
            return new ReportRequest(borrowerId, period, includeReturned, 
                                     List.copyOf(columns));
        }
```

* If someone calls `.column("extra")` on the builder *after* calling `.build()`, the previously published `ReportRequest` is completely unaffected!

---

## When to Decline the Builder Pattern

* A junior developer asks:  
  *"Should we create a `LoanPeriodBuilder` with `.withStart(s).withEnd(e).build()`?"*
* **The Verdict: NO!**
  * `LoanPeriod` has exactly two parameters.
  * Neither parameter is optional.
  * Adding a builder introduces 40 lines of boilerplate and method indirection for zero architectural gain.
* **Rule:** Use Builders when configuring objects with multiple optional parameters, complex invariants across fields, or collections.

---

# Part 5: Adapter & Data-Backed Collaborators

---

## Connecting Incompatible Contracts: The Adapter

> "Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces."  
> - Gamma et al. (GoF), 1994

```
CLIENT APPLICATION VOCABULARY                  EXTERNAL VENDOR VOCABULARY
┌─────────────────────────────────┐           ┌───────────────────────────────┐
│    «interface» BorrowerDirectory│           │     LegacyDirectoryClient     │
├─────────────────────────────────┤           ├───────────────────────────────┤
│ +find(id) : Optional<Borrower>  │           │ +lookup(key) : Person         │
└────────────────▲────────────────┘           └───────────────▲───────────────┘
                 │ implements                                 │ delegates
                 └───────────────┬────────────────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │    LegacyDirectoryAdapter     │
                 └───────────────────────────────┘
```

* The application defines `BorrowerDirectory`. The Adapter translates vendor quirks into clean domain concepts.

---

## The Precise Translation Contract Table

| Vendor Lookup Outcome | Adapter Translation Result | Architectural Meaning |
|---|---|---|
| `Person(id, "S", "Y")` | `Optional.of(new Borrower(id, STUDENT))` | Active Student |
| `Person(id, "T", "Y")` | `Optional.of(new Borrower(id, STAFF))` | Active Staff |
| `null` (Record missing) | `Optional.empty()` | Borrower absent |
| `Person(id, *, "N")` | `Optional.empty()` | Borrower inactive |
| Unknown kind/status code | Throws `DirectoryException` | Corrupted vendor data |
| Vendor throws `Failure` | Throws `DirectoryException` (wrapping cause) | Infrastructure outage |

* **Critical Distinction:**
  * Absence (`Optional.empty()`) is an ordinary business outcome (person not enrolled).
  * Outage (`DirectoryException`) is an operational infrastructure failure!

---

## Inside `LegacyDirectoryAdapter.java`

```java
public final class LegacyDirectoryAdapter implements BorrowerDirectory {
    private final LegacyDirectoryClient client;

    public LegacyDirectoryAdapter(LegacyDirectoryClient client) {
        this.client = Objects.requireNonNull(client);
    }

    @Override
    public Optional<Borrower> find(String borrowerId) {
        if (borrowerId == null || borrowerId.isBlank()) 
            throw new IllegalArgumentException("Borrower ID required.");
        
        LegacyDirectoryClient.Person raw;
        try {
            raw = client.lookup(borrowerId);
        } catch (LegacyDirectoryClient.Failure f) {
            throw new DirectoryException("Directory lookup failed for " + borrowerId, f);
        }
        if (raw == null) return Optional.empty(); // Absent
        return translate(borrowerId, raw);
    }
    ...
```

---

## Translating and Validating Vendor Records

```java
    private Optional<Borrower> translate(String expectedId, LegacyDirectoryClient.Person raw) {
        if (!expectedId.equals(raw.key())) {
            throw new DirectoryException("Provider returned mismatched key: " + raw.key());
        }
        BorrowerCategory category = switch (raw.kind()) {
            case "S" -> BorrowerCategory.STUDENT;
            case "T" -> BorrowerCategory.STAFF;
            default -> throw new DirectoryException("Unknown kind code: " + raw.kind());
        };
        return switch (raw.status()) {
            case "Y" -> Optional.of(new Borrower(expectedId, category));
            case "N" -> Optional.empty(); // Inactive borrower
            default -> throw new DirectoryException("Unknown status code: " + raw.status());
        };
    }
```

* Case-sensitive, strict validation. Malformed data never silently defaults to a permitted role!

---

## The New Application Entry Point: `DirectoryReservationService`

* Clients call the service without passing any borrower category:

```java
public final class DirectoryReservationService {
    private final ReservationCoordinator coordinator;
    private final BorrowerDirectory directory;

    public DirectoryReservationService(ReservationCoordinator coordinator, 
                                       BorrowerDirectory directory) {
        this.coordinator = Objects.requireNonNull(coordinator);
        this.directory = Objects.requireNonNull(directory);
    }

    public String reserve(String borrowerId, String itemId, 
                          LocalDate start, int days) {
        // 1. Validate local arguments before making external calls
        if (borrowerId == null || borrowerId.isBlank() ...) throw ...;

        // 2. Query directory via clean interface
        Borrower borrower = directory.find(borrowerId)
                .orElse(null);
        if (borrower == null) {
            return "Rejected: borrower not found or inactive.";
        }

        // 3. Delegate to coordinator using authoritative category!
        return coordinator.reserve(borrowerId, itemId, start, days, borrower.category());
    }
}
```

---

## Sequence Diagram: Directory Lookup Before Booking (Figure 8.2)

```
ReservationService         DirectoryAdapter          VendorClient           Coordinator
        │                         │                        │                     │
        │─── find(borrowerId) ───►│                        │                     │
        │                         │─── lookup(id) ────────►│                     │
        │                         │◄── Person("B2","T","Y")│                     │
        │◄── Borrower(STAFF) ─────│                        │                     │
        │                                                                        │
        │─── reserve(B2, CAM1, start, 14, STAFF) ───────────────────────────────►│
        │◄── "Confirmed: R1..." ─────────────────────────────────────────────────│
```

* **Alternative Path (Outage):**
  * VendorClient throws `Failure` -> Adapter throws `DirectoryException`.
  * ReservationService propagates error; coordinator is NEVER invoked; zero state mutated!

---

## Data-Backed Collaborators & Machine Learning Models

* **Core AI/Software Engineering Lesson:**
  * In modern systems, external data sources, recommendation engines, and Machine Learning models sit outside the core application.
  * An ML model predicting borrower risk or classifying an item is in the exact same architectural position as `LegacyDirectoryClient`!
* **Adapter Rules for AI & Data Components:**
  1. Map raw model tensor outputs/probabilities into domain types.
  2. Treat low confidence / missing prediction and service timeout as distinct outcomes.
  3. Never let raw model prediction errors corrupt business invariants!

---

# Part 6: Decorator, AI Critique, Midterm Prep & Wrap-Up

---

## The Decorator Pattern: Composable Behaviors

> "Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality."  
> - Gamma et al. (GoF), 1994

```
                   «interface» Sender
                   +send(message) : void
                             ▲
                             │ implements & wraps
                 ┌───────────┴───────────┐
                 │     AuditedSender     │ ──wraps──► Sender
                 ├───────────────────────┤
                 │ records send event    │
                 └───────────────────────┘
```

* Implements the same interface as the wrapped object. Delegates the call while adding behavior before, after, or around execution.

---

## Decorator Order Matters!

* Suppose we compose an `AuditedSender` and a `RetryOnceSender`:
  * Scenario: The underlying sender fails on attempt 1, then succeeds on attempt 2.

```
Composition A: AuditedSender( RetryOnceSender( target ) )
Call Flow: Client ──► Audit ──► Retry ──► Target (fails) ──► Retry (succeeds)
Audit Records: [ "attempt", "sent" ]  (Sees 1 overall operation that succeeded!)

Composition B: RetryOnceSender( AuditedSender( target ) )
Call Flow: Client ──► Retry ──► Audit ──► Target (fails) ──► Audit ──► Target (succeeds)
Audit Records: [ "attempt", "failed", "attempt", "sent" ] (Sees individual tries!)
```

* **Key Takeaway:** Decorator stacking order fundamentally changes observable system behavior!

---

## Bounding AI Assistance: Auditing Pattern Hallucinations

* A student prompts an LLM: *"Add design patterns to make my code professional."*
* **The Fictional AI Generated Response:**

> "1. Rename `ReservationApplication.create` to `FactoryMethod` and it becomes Factory Method.  
> 2. Add an Abstract Factory even though there is only one product role.  
> 3. In the adapter, catch every exception and default to a Staff borrower so the system stays available.  
> 4. Wrap all senders in retry decorators; order does not matter."

* **The Engineering Critique:**
  * Claim 1: False. Renaming a static method does not make it a subclass hook.
  * Claim 2: False. Abstract Factory requires related product families.
  * Claim 3: Catastrophic security breach! Never default unknown users to staff privileges.
  * Claim 4: False. Decorator order alters audit trails and exception semantics.

---

## Midterm Practice: 4 Essential Question Types

* The Midterm Examination (Weeks 1-6; Chapters 2-7) focuses on 4 core skills:

```
1. UML Modeling (Ch 2, 4, 7)
   - Classes, associations, multiplicities, realization, dependency, sequence diagrams.

2. Code Smell Diagnosis (Ch 5)
   - Fowler smells: Divergent Change, Hidden Construction, Primitive Obsession, Feature Envy.

3. Refactoring with Interfaces & DIP (Ch 5, 6)
   - Extracting collaborators, applying constructor injection, composition roots.

4. Unit Testing & Test Doubles (Ch 6, 7)
   - Writing JUnit Jupiter tests, AAA pattern, testing boundaries, using Stubs/Mocks.
```

---

## Practice Task: Reviewing `OverdueReminder`

```java
public class OverdueReminder {
    public boolean remind(String borrowerEmail, LocalDate dueDate, String itemName) {
        if (LocalDate.now().isAfter(dueDate)) { // Smell: Hardcoded clock!
            // Smell: Direct construction & network coupling!
            MailClient client = new MailClient("smtp.campus.example", 25);
            client.send(borrowerEmail, "Overdue: " + itemName, "Please return...");
            System.out.println("Reminder sent to " + borrowerEmail);
            return true;
        }
        return false;
    }
}
```

* **Exam Answer Key:**
  1. Extract `Clock` dependency and pass via constructor.
  2. Extract `NotificationClient` interface; inject into `OverdueReminder`.
  3. Write JUnit test using `Clock.fixed(...)` and a hand-written recording spy!

---

## Key Takeaways

1. **Patterns Solve Specific Problems:**
   * Factory Method handles subclass creation hooks.
   * Abstract Factory enforces product family consistency.
   * Builder handles complex, multi-option construction.
   * Adapter bridges incompatible interfaces.
   * Decorator adds transparent wrapped behaviors.
2. **Never Pattern-Engineer Speculatively:**
   * If a constructor or simple assembly function suffices, keep it simple!
3. **Data-Backed Collaborators Require Explicit Contracts:**
   * Always distinguish legitimate absence (`Optional.empty()`) from infrastructure outages (`Exception`).
4. **Prepare for the Midterm:**
   * Master UML notations, SOLID refactoring steps, and JUnit test doubles.

---

## Looking Ahead to Week 8

* **Next Lecture: Designing Changing Behaviour: Core Behavioral Patterns**
  * **Strategy Pattern:** Swapping algorithms dynamically.
  * **State Pattern:** Modeling the equipment loan and maintenance lifecycle.
  * **Observer Pattern:** Decoupled event-driven notification dispatch.
  * **Command Pattern:** Encapsulating requests as executable objects.

---

# Questions & Discussion
### SE506: Object Oriented Development and Agile Practices
*Slides and code available on the module repository.*
