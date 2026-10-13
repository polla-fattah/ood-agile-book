---
title: "Week 6: Testing as a Design Practice: TDD & Test Doubles"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 60
type: slides
layout: page
---

# Week 6: Testing as a Design Practice: TDD & Test Doubles
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## 3-Hour Lecture Roadmap

* **Part 1: Testing as Design & Availability Enquiry (0:00 - 0:35)**
  * The green build illusion, translating US-02 into AQ-01..AQ-05, observing state and result together, Maven and JUnit 5 setup.
* **Part 2: The Red-Green-Refactor Rhythm in Action (0:35 - 1:10)**
  * The TDD cycle, reaching the intended assertion failure, minimal green implementation, extracting shared conflict detection.
* **Part 3: Boundaries, Determinism & Controlled Time (1:10 - 1:40)**
  * Testing meaningful boundaries, the `Clock` abstraction, zone sensitivity, the bounded `LoanService` increment.
* **BREAK (1:40 - 1:55)**
* **Part 4: Test Double Taxonomy & Mockito (1:55 - 2:25)**
  * Meszaros taxonomy (Dummy, Stub, Fake, Spy, Mock), hand-written vs. Mockito 5.20.0, avoiding over-mocking.
* **Part 5: Mutation Testing, Brittle Tests & AI Bounding (2:25 - 2:45)**
  * Mutation testing with deliberate faults, test fragility, critiquing AI-generated test suites.
* **Part 6: Milestone 2 Deliverables, Midterm Prep & Wrap-Up (2:45 - 3:00)**
  * Milestone 2 checklist, MVP demonstration rehearsal, Midterm practice set (Chapters 2-7), preview of Week 7.

---

## Pedagogical Alignment & Milestone 2 Context

* **Module Learning Outcomes:**
  * **LO3:** Design and implement robust unit test suites, applying test-driven development (TDD) and test double patterns to verify complex software behavior.
* **Foundational Literature & Engineering Canon:**
  * Kent Beck (2002): *Test-Driven Development: By Example* (The TDD rhythm and test list).
  * Gerard Meszaros (2007) / Martin Fowler (2006): *xUnit Test Patterns: Refactoring Test Code* (Test Double Taxonomy).
  * Robert C. Martin (2002): *Agile Software Development* ("A Programming Episode").
* **Milestone 2 Delivery Target:**
  * Milestone 2 falls in Week 6! Teams demonstrate their working in-memory MVP, traceable TDD sequence, acceptance test mappings, and retrospective evidence.

---

# Part 1: Testing as Design & Availability Enquiry

---

## The Green Build Illusion

* **The Scenario:**
  * A developer announces: *"US-02 (Availability Enquiry) is done! Look, my build is 100% green!"*
* **The Embarrassing Live Demonstration:**
  * The Equipment Officer tests the live system: enquired about a camera that was already reserved for today.
  * System response: `Available: true`!
* **What Went Wrong with the Test?**

```java
// THE WEAK TEST ANTI-PATTERN
@Test
void testAvailability() {
    ReservationCoordinator c = new ReservationCoordinator(...);
    boolean result = c.isAvailable("CAM1", start, end);
    assertNotNull(result); // Tests only that a primitive boolean was returned!
}
```

* **Engineering Principle:**
  * Passing tests are meaningless unless they have the power to reject incorrect implementations.

---

## Translating US-02 into Concrete Acceptance Criteria

* From Chapter 3 & 4 user story analysis, we bring 5 formal criteria:

| Code | Setup & Action | Expected Return | Required State Observations |
|---|---|---|---|
| **AQ-01** | Empty schedule; enquire about CAM1 | `true` (Available) | Records empty; zero notices |
| **AQ-02** | CAM1 reserved `[20, 22 Oct)`; enquire `[21, 23 Oct)` | `false` (Unavailable) | Records unchanged; zero notices |
| **AQ-03** | CAM1 reserved `[20, 22 Oct)`; enquire `[22, 23 Oct)` | `true` (Available) | End is exclusive; zero notices |
| **AQ-04** | CAM1 reserved; enquire about MIC1 on same dates | `true` (Available) | Different item available |
| **AQ-05** | Reversed dates or blank item identifier | Throws Exception | No state mutation |

* **Domain Invariant:**
  * An enquiry answers: *"Is there an interval conflict?"*
  * It does NOT check borrower eligibility, allocate reservation IDs, or dispatch notifications!

---

## Observing State and Result Together

* In object-oriented testing, assertions must verify **two distinct dimensions**:

```
                  ┌────────────────────────────────────────┐
                  │          OPERATION UNDER TEST          │
                  │   coordinator.isAvailable(item, s, e)  │
                  └───────────────────┬────────────────────┘
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
   [ Direct Return Value ]                            [ System Side Effects ]
  Does it return true/false?                          Did it mutate records?
                                                      Did it send notices?
                                                      Did it consume IDs?
```

* If an enquiry accidentally adds a reservation and deletes it afterwards:
  * A return-value assertion passes!
  * But a notification spy catches the leaked notice!

---

## Modern Tooling: Maven 3.9.11 & JUnit Jupiter 5.13.4

* We upgrade our toolchain from ad-hoc bash scripts to standard Apache Maven:
  * Compiler Plugin 3.14.1 targeting Java 17 LTS.
  * Surefire Plugin 3.5.4 executing the JUnit Platform.
  * JUnit Jupiter 5.13.4 API and engine.
  * Mockito 5.20.0 for interface mocks.
* **The Unified Build Command:**

```bash
mvn --batch-mode verify
```

* **Exit Code Guarantee:**
  * Exits 0 if and only if compilation succeeds AND all tests pass.
  * Any assertion failure or runtime exception immediately terminates the CI pipeline with a nonzero status code.

---

## Bridging Legacy Checks: `LegacyRegressionTest`

* How do we adopt JUnit without throwing away the 100+ assertions from Chapters 2, 3, 5, and 6?
* **The Adapter Pattern for Test Suites:**

```java
import org.junit.jupiter.api.Test;

class LegacyRegressionTest {
    @Test void chapter02() { Chapter02Checks.main(new String[0]); }
    @Test void chapter03() { Chapter03AcceptanceExamples.main(new String[0]); }
    @Test void chapter05() { Chapter05Checks.main(new String[0]); }
    @Test void chapter06() { Chapter06Checks.main(new String[0]); }
}
```

* **Pedagogical Strategy:**
  * Bridges existing verification into Maven Surefire seamlessly.
  * New features are developed test-first using native JUnit Jupiter annotations.

---

## Test Anatomy: Arrange-Act-Assert (AAA)

```java
@Test
void overlappingEnquiryIsUnavailableWithoutChangingRecordsOrNotifying() {
    // 1. ARRANGE: Establish initial state & take baseline snapshots
    RecordingNotificationSender inbox = new RecordingNotificationSender();
    ReservationCoordinator coordinator = ReservationApplication.create(inbox);
    LocalDate start = LocalDate.of(2026, 10, 20);
    coordinator.reserve("B1", "CAM1", start, 2);
    List<Reservation> recordsBefore = coordinator.reservations();
    List<Reservation> noticesBefore = inbox.received();

    // 2. ACT: Execute the query operation
    boolean available = coordinator.isAvailable("CAM1", start.plusDays(1), start.plusDays(3));

    // 3. ASSERT: Verify return outcome AND absence of side effects
    assertAll(
            () -> assertFalse(available, "Overlapping item must be unavailable"),
            () -> assertEquals(recordsBefore, coordinator.reservations()),
            () -> assertEquals(noticesBefore, inbox.received()));
}
```

* Notice: `assertAll` ensures that if `available` is wrong, snapshot assertions still execute and report!

---

## Data-Driven Testing with `@ParameterizedTest`

* Policy boundaries should not be duplicated across 10 identical test methods:

```java
class BorrowingPolicyTest {
    @ParameterizedTest(name = "{0}: active={1}, days={2} -> expected={3}")
    @CsvSource({
        "STUDENT, 0,  1, true",   // Lower valid bound
        "STUDENT, 2,  7, true",   // Upper valid bound
        "STUDENT, 3,  1, false",  // Exceeded active loan limit
        "STUDENT, 0,  8, false",  // Exceeded duration limit
        "STAFF,   4, 14, true",   // Staff upper bound
        "STAFF,   5,  1, false",  // Staff exceeded active loan limit
        "STAFF,   0, 15, false",  // Staff exceeded duration limit
        "STUDENT, -1, 1, false",  // Negative count invariant
        "STAFF,   0,  0, false"   // Zero duration invariant
    })
    void rulesMatchDocumentedContract(BorrowerCategory category, 
                                      int count, int days, boolean expected) {
        BorrowingPolicy policy = switch (category) {
            case STUDENT -> new ReservationRules();
            case STAFF -> new StaffReservationRules();
        };
        assertEquals(expected, policy.mayRequest(count, days));
    }
}
```

---

# Part 2: The Red-Green-Refactor Rhythm in Action

---

## The Core TDD Cycle (Beck 2002)

```
        ┌─────────────────────────────────────────────────────┐
        │ 1. RED: Write a small test for missing behavior     │
        │    Watch it fail with the INTENDED assertion error  │
        └──────────────────────────┬──────────────────────────┘
                                   │
                                   ▼
        ┌─────────────────────────────────────────────────────┐
        │ 2. GREEN: Write the minimal code to pass the test   │
        │    No premature optimizations; make it work         │
        └──────────────────────────┬──────────────────────────┘
                                   │
                                   ▼
        ┌─────────────────────────────────────────────────────┐
        │ 3. REFACTOR: Clean up design and eliminate smell    │
        │    Keep tests passing at every single step          │
        └──────────────────────────┬──────────────────────────┘
                                   │
                                   └────────────► Next Behavior
```

* **Why TDD is a Design Practice:**
  * Writing the test first forces you to design the API from the client's perspective before writing implementation details!

---

## The Meaning of "Red": Intended Failure vs Syntax Error

* **Common Student Mistake:**
  * *"My build failed because of a missing curly brace or missing Maven JAR. That is my Red step!"*
* **The Truth:**
  * A compiler error or classpath failure is an **environmental failure**, NOT a TDD Red state!
* **The Intended Red State:**
  * The code must compile cleanly.
  * The test harness must execute.
  * The test must fail at the exact assertion that tests the new requirement!

```text
[ERROR] Failures: 
[ERROR]   AvailabilityTddTest.overlappingEnquiryIsUnavailable:
          Overlapping item must be unavailable ==> expected: <false> but was: <true>
[INFO] Tests run: 1, Failures: 1, Errors: 0, Skipped: 0
```

---

## Step 1 (Red): The Compiling Baseline

* Create the public signature in `ReservationCoordinator.java`:

```java
public boolean isAvailable(String itemId, LocalDate start, LocalDate endExclusive) {
    if (itemId == null || itemId.isBlank()) {
        throw new IllegalArgumentException("Item identifier must not be blank.");
    }
    // Minimal compiling stub: deliberately optimistic!
    return true; 
}
```

* Now run `AvailabilityTddTest`:
  * It compiles!
  * It executes!
  * It fails on line 1007: `expected <false> but was: <true>`.
  * We have proven that our test actually observes missing overlap detection!

---

## Step 2 (Green): Minimal Implementation

* Write just enough code to make the failing test pass:

```java
public boolean isAvailable(String itemId, LocalDate start, LocalDate endExclusive) {
    if (itemId == null || itemId.isBlank()) {
        throw new IllegalArgumentException("Item identifier must not be blank.");
    }
    LoanPeriod requested = new LoanPeriod(start, endExclusive);

    // Minimal implementation: loop through existing reservations
    for (Reservation existing : reservations) {
        if (existing.itemId().equals(itemId) 
                && existing.period().overlaps(requested)) {
            return false; // Conflict found!
        }
    }
    return true; // No conflict
}
```

* Run `mvn test -Dtest=AvailabilityTddTest`:
  * **Result: BUILD SUCCESS! 1 test passed.**

---

## Step 3 (Refactor): Eliminate Duplication

* Inspect `ReservationCoordinator.java`:
  * Look at `reserve(...)` (lines 335-339) and `isAvailable(...)` (lines 359-364).
  * Both methods duplicate the exact same loop scanning `reservations` for item/period overlap!
* **The Refactoring:** Extract Method `hasConflict(...)`

```java
public boolean isAvailable(String itemId, LocalDate start, LocalDate endExclusive) {
    if (itemId == null || itemId.isBlank()) {
        throw new IllegalArgumentException("Item identifier must not be blank.");
    }
    LoanPeriod requested = new LoanPeriod(start, endExclusive);
    return !hasConflict(itemId, requested);
}

private boolean hasConflict(String itemId, LoanPeriod requested) {
    for (Reservation existing : reservations) {
        if (existing.itemId().equals(itemId) && existing.period().overlaps(requested)) {
            return true;
        }
    }
    return false;
}
```

---

## Verifying the Refactoring

* Re-run all tests (both the new TDD test and the legacy regression suite):

```bash
mvn --batch-mode test
```

```text
[INFO] Running AvailabilityTddTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] Running LegacyRegressionTest
All 34 chapter checks passed.
All 5 acceptance examples passed.
All 44 Chapter 5 checks passed.
All 28 Chapter 6 checks passed.
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

* **Outcome:**
  * Internal structure is cleaner (DRY).
  * Zero regression regressions across existing reservation workflows.

---

## Traceable Git History for TDD

* In Milestone 2, you must provide commit evidence of your TDD sequence:

```
Commit 1: test: add failing test for reservation availability query (RED)
          - Added AvailabilityTddTest
          - Added isAvailable stub returning true

Commit 2: feat: implement reservation overlap detection in isAvailable (GREEN)
          - Added loop checking LoanPeriod overlap in isAvailable

Commit 3: refactor: extract private hasConflict helper in coordinator (REFACTOR)
          - Extracted hasConflict(itemId, requested)
          - Shared between reserve() and isAvailable()
```

* A single massive commit with everything already green is NOT evidence of TDD!

---

# Part 3: Boundaries, Determinism & Controlled Time

---

## Testing Meaningful Boundaries vs Arbitrary Data

* Avoid testing random, meaningless inputs:
  * Testing 1,000 random integers gives false confidence.
* Focus test effort on **critical decision boundaries**:

```
        INTERVAL OVERLAP BOUNDARY LINE
        Existing Booking: [20 Oct, 22 Oct)
        
 Case A: [18 Oct, 20 Oct)  ──► Adjacent BEFORE  (Available: TRUE)
 Case B: [19 Oct, 21 Oct)  ──► Overlap START    (Available: FALSE)
 Case C: [20 Oct, 22 Oct)  ──► Identical Match  (Available: FALSE)
 Case D: [21 Oct, 23 Oct)  ──► Overlap END      (Available: FALSE)
 Case E: [22 Oct, 24 Oct)  ──► Adjacent AFTER   (Available: TRUE)
 Case F: [20 Oct, 20 Oct)  ──► Zero-length      (Throws IllegalArgumentException)
```

* Case A and Case E prove that your interval math correctly treats `endExclusive` as open!

---

## Time-Dependent Testing: The `now()` Trap

* **The Problem:**
  * In Milestone 2, we introduce equipment checkout and return.
  * Rule: An item can only be checked out on a date *within the reservation period*.
* **The Flawed Implementation:**

```java
public Loan checkOut(String reservationId) {
    LocalDate today = LocalDate.now(); // TOXIC DEPENDENCY!
    if (today.isBefore(reservation.period().start()) ...) {
        throw new IllegalStateException("Not within loan period");
    }
    ...
}
```

* **Why this breaks:**
  * Tests run on 20 October pass.
  * The exact same tests run on 25 October fail!
  * Tests become non-deterministic and time-coupled.

---

## The Solution: Injecting `java.time.Clock`

* Java 8+ provides the `java.time.Clock` abstraction:

```java
public final class LoanService {
    private final ReservationCoordinator reservations;
    private final Clock clock; // Injected dependency

    public LoanService(ReservationCoordinator reservations, Clock clock) {
        this.reservations = Objects.requireNonNull(reservations);
        this.clock = Objects.requireNonNull(clock);
    }

    public Loan checkOut(String reservationId) {
        LocalDate today = LocalDate.now(clock); // Reads from injected clock!
        ...
    }
}
```

* **In Production:** Pass `Clock.systemDefaultZone()`.
* **In Unit Tests:** Pass `Clock.fixed(Instant.parse("2026-10-20T12:00:00Z"), ZoneOffset.UTC)`.

---

## Zone Sensitivity: The Midnight Edge Case

* A fixed UTC instant alone does NOT determine a calendar date:

```
Instant: 2026-10-19T22:30:00Z
  ├── In UTC (London, GMT):         Date is 19 October (22:30)
  └── In Asia/Baghdad (UTC+3):       Date is 20 October (01:30)
```

```java
@Test
void clockZoneDeterminesTheCheckoutDate() {
    LocalDate start = LocalDate.of(2026, 10, 20);
    // Instant is 19 Oct UTC, but Baghdad local time is 20 Oct!
    Clock local = Clock.fixed(
            Instant.parse("2026-10-19T22:30:00Z"), 
            ZoneId.of("Asia/Baghdad"));

    LoanService service = new LoanService(reservedCoordinator(), local);
    assertEquals(start, service.checkOut("R1").borrowedOn());
}
```

* Always make time zones explicit when converting instants to dates!

---

## Simulating Time Flow: `AdjustableClock`

* When a test scenario spans checkout on Monday and return on Wednesday:
  * Do NOT use `Thread.sleep`!

```java
static final class AdjustableClock extends Clock {
    private final AtomicReference<Instant> now;
    private final ZoneId zone;

    AdjustableClock(Instant instant) { 
        this(new AtomicReference<>(instant), ZoneOffset.UTC); 
    }
    private AdjustableClock(AtomicReference<Instant> now, ZoneId zone) {
        this.now = now; this.zone = zone;
    }
    void advanceDays(int days) { 
        now.set(now.get().plus(Duration.ofDays(days))); 
    }
    @Override public Instant instant() { return now.get(); }
    @Override public ZoneId getZone() { return zone; }
    @Override public Clock withZone(ZoneId zone) { return new AdjustableClock(now, zone); }
}
```

* The test controls time deterministically in 1 millisecond.

---

## The Bounded Lending Flow: `Loan` Record & Invariants

```java
/** Immutable loan state. A null returnedOn means this loan is currently active. */
public record Loan(String reservationId, String borrowerId, String itemId,
                   LocalDate borrowedOn, LocalDate returnedOn) {
    public Loan {
        if (reservationId == null || reservationId.isBlank()
                || borrowerId == null || borrowerId.isBlank()
                || itemId == null || itemId.isBlank()) {
            throw new IllegalArgumentException("Loan identifiers must not be blank.");
        }
        Objects.requireNonNull(borrowedOn, "borrowedOn");
        if (returnedOn != null && returnedOn.isBefore(borrowedOn)) {
            throw new IllegalArgumentException("Return cannot precede checkout.");
        }
    }
    public boolean active() { return returnedOn == null; }
}
```

* **Compact Record Constructor:** Enforces class invariants at the moment of construction.

---

## Explicit Lifecycle Boundaries in the MVP

* Notice what `LoanService.returnLoan(...)` does NOT do:
  * Returning an item sets `returnedOn = today`.
  * It does NOT delete or cancel the reservation!
  * It does NOT restore the student's active reservation allowance!

```
                  ┌──────────────────────┐
                  │ Active Reservation   │
                  │   (Occupies Slot)    │
                  └──────────┬───────────┘
                             │ Checkout
                             ▼
                  ┌──────────────────────┐
                  │     Active Loan      │
                  │   (Physical Item)    │
                  └──────────┬───────────┘
                             │ Return
                             ▼
                  ┌──────────────────────┐
                  │    Returned Loan     │
                  │ (Reservation Still   │
                  │  Counts in History)  │
                  └──────────────────────┘
```

* **Honest Scope:** Acknowledge this boundary in your Milestone 2 documentation.

---

# Part 4: Test Double Taxonomy & Mockito

---

## The Meszaros Test Double Taxonomy (2007)

* A "Test Double" is a generic term for any substitute used in place of a production component.

```
                         [ TEST DOUBLE ]
                                │
   ┌────────────┬───────────────┼───────────────┬────────────┐
   ▼            ▼               ▼               ▼            ▼
 Dummy         Stub            Fake            Spy          Mock
(Ignored     (Canned         (Working        (Records     (Pre-set
argument)    response)      in-memory)        calls)    expectation)
```

* In our Campus Lending System:
  * **Dummy:** A sender passed to a test that expects immediate argument rejection.
  * **Stub:** A sender that throws `NotificationException` to test partial-failure reporting.
  * **Fake:** An in-memory database or directory.
  * **Spy:** `RecordingNotificationSender` recording received reservations for later assertions.
  * **Mock:** A Mockito mock verifying `verify(sender, times(1)).send(...)`.

---

## State Verification vs Interaction Verification

```
STATE VERIFICATION (Inspect Observable State)
coordinator.reserve("B1", "CAM1", start, 2);
assertEquals(1, coordinator.reservations().size());
assertEquals("CAM1", coordinator.reservations().get(0).itemId());
-> Tests WHAT the system became. Robust against internal refactorings.

INTERACTION VERIFICATION (Inspect Communication)
NotificationSender mockSender = mock(NotificationSender.class);
coordinator = ReservationApplication.create(mockSender);
coordinator.reserve("B1", "CAM1", start, 2);
verify(mockSender, times(1)).send(any(Reservation.class));
-> Tests HOW collaborators communicated. Critical for boundary contracts.
```

* Prefer State Verification for domain logic.
* Use Interaction Verification strictly for output/I/O boundaries where no state is stored.

---

## Using Mockito 5.20.0 for Boundary Verification

```java
class NotificationMockitoTest {
    private final LocalDate day = LocalDate.of(2026, 10, 20);

    @Test 
    void acceptedReservationIsSentOnceWithDomainDetails() {
        // Arrange
        NotificationSender sender = mock(NotificationSender.class);
        ReservationCoordinator c = ReservationApplication.create(sender);

        // Act
        c.reserve("B1", "CAM1", day, 2);

        // Assert: Capture and inspect the boundary argument
        ArgumentCaptor<Reservation> captor = ArgumentCaptor.forClass(Reservation.class);
        verify(sender).send(captor.capture());
        Reservation sent = captor.getValue();

        assertAll(
            () -> assertEquals("R1", sent.id()),
            () -> assertEquals("B1", sent.borrowerId()),
            () -> assertEquals("CAM1", sent.itemId()),
            () -> assertEquals(day, sent.period().start()));
    }
}
```

---

## Verifying Absence of Calls: `verifyNoInteractions`

* When a request is rejected, the sender must NEVER be called:

```java
@Test 
void rejectedDurationDoesNotNotify() {
    NotificationSender sender = mock(NotificationSender.class);
    ReservationCoordinator c = ReservationApplication.create(sender);

    // Act: Request 8 days (student limit is 7)
    String result = c.reserve("B1", "CAM1", day, 8);

    // Assert
    assertEquals("Rejected: borrower limit or duration.", result);
    assertTrue(c.reservations().isEmpty());
    
    // Explicit boundary verification:
    verifyNoInteractions(sender);
}
```

* `verifyNoInteractions` guarantees that failed workflows do not leak false notifications.

---

## Simulating Output Failure with Mockito Stubs

* What if the output destination crashes?

```java
@Test 
void expectedNotificationFailureRetainsReservationWithoutRetry() {
    NotificationSender sender = mock(NotificationSender.class);
    
    // Stub the mock to throw the expected domain exception
    doThrow(new NotificationException("Console pipe broken"))
        .when(sender).send(any(Reservation.class));

    ReservationCoordinator c = ReservationApplication.create(sender);

    // Act
    String confirmation = c.reserve("B1", "CAM1", day, 2);

    // Assert: Verify exact retain-and-report suffix
    assertEquals("Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)."
            + " Notification failed; reservation retained.", confirmation);
    assertEquals(1, c.reservations().size());
    verify(sender, times(1)).send(any(Reservation.class));
}
```

---

## The Over-Mocking Anti-Pattern

* **Rule 1: NEVER mock Value Objects or Records!**
  * BAD: `LoanPeriod mockPeriod = mock(LoanPeriod.class); when(mockPeriod.overlaps(...)).thenReturn(true);`
  * GOOD: Use a real `new LoanPeriod(start, end)`! Value objects are fast, deterministic, and self-contained.
* **Rule 2: NEVER mock the System Under Test!**
  * If testing `ReservationCoordinator`, do not mock methods on the coordinator itself!
* **Rule 3: Only mock what crosses architectural boundaries.**
  * Mock I/O, external network transports, and third-party APIs.
  * Keep internal domain entities real.

---

# Part 5: Mutation Testing, Brittle Tests & AI Bounding

---

## Code Coverage vs Mutation Testing

* **Code Coverage:** Tells you which lines were executed during the test run.
  * A test that calls every method but has zero `assert` statements achieves 100% code coverage!
* **Mutation Testing:** Measures whether your test suite can **detect deliberate faults** (mutants) injected into the production source code.

```
       [ Production Source Code ] 
                   │
                   ▼ (Inject Fault / Mutation)
       [ Mutated Code: Change "<=" to "<" ]
                   │
                   ▼ (Run Test Suite)
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
[ Mutant KILLED (Test FAILS) ]              [ Mutant SURVIVED (Test PASSES) ]
Test suite successfully                     Test suite has a BLIND SPOT!
detected the defect.                        Add a boundary assertion.
```

---

## 16 Deliberate Fault Experiments in Chapter 7

* The author injected 16 deliberate faults into the lending codebase:
  * 14 mutants were **killed immediately** by existing boundary checks.
  * 1 mutant **survived**: The rule stated loan snapshots must be unmodifiable, but no test had called `.clear()` on `service.loans()`. (Assertion added!).
  * 1 mutant was **untestable sequentially**: An enquiry that creates a temporary record and deletes it immediately leaves no state traces behind.
* **Lesson:**
  * Deliberate mutation experiments expose gaps that standard line coverage hides.

---

## Test Fragility & Implementation Coupling

* A test is **brittle** if it breaks when the internal implementation is refactored, even though observable behavior is preserved.

```
FRAGILE TEST (Tightly coupled to internals)
verify(coordinator, times(1)).hasConflict(any(), any());
assertEquals(2, coordinator.getInternalLoopCounter());
-> Breaks the moment hasConflict is optimized or inlined!

ROBUST TEST (Coupled to public contracts)
boolean available = coordinator.isAvailable("CAM1", start, end);
assertFalse(available);
assertEquals(1, coordinator.reservations().size());
-> Survives all internal algorithmic optimizations!
```

---

## Bounding AI Test Generation

* Prompting an AI: *"Write unit tests for my availability query."*
* **The Dangerous AI Hallucination:**

```java
// Fictional AI-generated test:
@Test
void testAvailability() {
    c.reserve("B1", "CAM1", LocalDate.of(2026, 10, 20), 2);
    // AI assumes inclusive end dates!
    boolean result = c.isAvailable("CAM1", LocalDate.of(2026, 10, 22), 
                                          LocalDate.of(2026, 10, 23));
    assertFalse(result); // WRONG! 22 Oct is exclusive end, so it IS available!
}
```

* **The Trap:** If you let the AI write both the code and the tests, they will agree with each other on the wrong requirement!
* **Human Duty:** The software engineer enforces the authoritative domain contract (`[start, endExclusive)`).

---

# Part 6: Milestone 2 Deliverables, Midterm Prep & Wrap-Up

---

## Milestone 2 Deliverables Checklist

* Every team must present the following 7 artifacts for Milestone 2:

| # | Required Milestone 2 Artifact | Verification Standard |
|---|---|---|
| **1** | Working in-memory MVP | Another person can run the demo from written instructions |
| **2** | Acceptance test mapping | User stories (US-01, US-02) mapped to named JUnit tests |
| **3** | Traceable TDD sequence | Recorded Red-Green-Refactor commits/diffs from your repo |
| **4** | Test Double justification | Documented choice of Fake, Stub, Spy, or Mock |
| **5** | Automated build evidence | `mvn verify` output passing on the demonstrated revision |
| **6** | Review & Retrospective | Real feedback recorded with at least 1 concrete next action |
| **7** | Documented limitations | Explicit statement of what the MVP does NOT support yet |

---

## Rehearsing the End-to-End MVP Demonstration

* The Chapter 7 demonstration walk-through:

```java
public final class Chapter07Demo {
    public static void main(String[] args) {
        // 1. Initial State: Enquire on empty schedule
        System.out.println("Available before reservation: " + coordinator.isAvailable("CAM1", day, day.plusDays(2)));
        
        // 2. Action: Create confirmed reservation
        System.out.println(coordinator.reserve("B1", "CAM1", day, 2));
        
        // 3. Observed Effect: Enquire on overlapping schedule
        System.out.println("Available after reservation: " + coordinator.isAvailable("CAM1", day, day.plusDays(2)));
        
        // 4. Action: Check out item within loan window
        Loan loan = loans.checkOut("R1");
        System.out.println("Loan active after checkout: " + loan.active());
        
        // 5. Action: Return item
        Loan returned = loans.returnLoan("R1");
        System.out.println("Loan active after return: " + returned.active());
        System.out.println("Accepted-reservation notices: " + inbox.received().size());
    }
}
```

---

## Midterm Examination Practice Set (Chapters 2-7)

* The Midterm covers Weeks 1 to 6 (Chapters 2 to 7).
* **The 4 Exam Question Archetypes:**
  1. **UML Class Modeling:** Draw domain entities, associations, multiplicities, and interfaces.
  2. **Smell Diagnosis:** Identify Divergent Change, Hidden Construction, or Primitive Obsession in supplied code.
  3. **Refactoring & DIP:** Refactor a coupled class by introducing an interface and constructor injection.
  4. **Unit Testing & Test Doubles:** Write JUnit tests using a hand-written stub or fixed clock.

---

## Practice Problem: Diagnosing `OverdueReminder`

```java
// What smells and SOLID violations exist here?
public class OverdueReminder {
    public boolean remind(String borrowerEmail, LocalDate dueDate, String itemName) {
        if (LocalDate.now().isAfter(dueDate)) { // Untestable: hardcoded clock!
            // Coupling: hardcoded network infrastructure!
            MailClient client = new MailClient("smtp.campus.example", 25);
            client.send(borrowerEmail, "Overdue: " + itemName, "Please return...");
            System.out.println("Reminder sent to " + borrowerEmail);
            return true;
        }
        return false;
    }
}
```

* **The Fix:** Inject `Clock` and inject `NotificationChannel` interface!

---

## Key Takeaways

1. **Testing is a Design Activity:**
   * TDD forces you to design clean, client-focused APIs before writing implementation logic.
2. **The Red Stage Must Be Meaningful:**
   * Ensure your test fails for the intended behavioral reason before writing code.
3. **Control Time Deterministically:**
   * Inject `java.time.Clock`; never call `LocalDate.now()` or `Thread.sleep` in domain logic.
4. **Choose the Right Test Double:**
   * Use Stubs for canned inputs, Spies/Recorders for state, and Mocks for boundary verification. Never mock value objects.
5. **Milestone 2 is About Evidence:**
   * A passing test suite must be backed by a working MVP demonstration and real retrospective reflections.

---

## Looking Ahead to Week 7

* **Next Lecture: Creational Patterns & Object Construction**
  * **Factory Method & Abstract Factory:** Controlled polymorphism.
  * **Builder Pattern:** Assembling complex domain aggregates safely.
  * **Invariant Validation During Construction:** Ensuring invalid objects can never exist.
  * **Final Midterm Review & Practice:** Comprehensive review of Chapters 2 to 7.

---

# Questions & Discussion
### SE506: Object Oriented Development and Agile Practices
*Slides and code available on the module repository.*
