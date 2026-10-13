# Chapter 9: Code, Explanations and Solutions

*Designing Changing Behaviour*  
*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3

## 1. Scope and reproducible execution

This file accompanies `Chapter_09_Designing_Changing_Behaviour.md`. It includes the complete cumulative checkpoint, separate before/after lifecycle examples, tests, model solutions and teaching notes. Use Java 17 and the same pinned dependencies as Chapter 8.

**Starting point:** Chapter 8's directory-backed reservation flow. **Cumulative option:** `NotificationPublisher` can be supplied through the existing sender interface. **Action example:** `ReserveEquipmentCommand` invokes the real directory-backed service when executed. **Separate exercise:** `behaviour.LifecycleExamples` contains a proposed lifecycle, with conditional and State versions. It does not modify the actual reservation or loan model.

### 1.1 Reconstruct from the listings

Create a directory called `after`. Copy the content of every labelled file listing in Sections 3–5 to its stated path, creating intermediate directories and preserving case. Do not copy fence markers. The README listing uses four backticks because its own content includes three-backtick code fences.

For an incremental update, copy Chapter 8's completed `after` directory. Add the five new main-source files and four new test files identified in Section 2, then replace the POM and README with this chapter's versions. The project version changes to 0.9.0. Every inherited source file remains unchanged.

| Tool | Tested configuration |
|---|---|
| Java | Release 17; author runtime OpenJDK 17.0.20 |
| Maven | 3.9.11 |
| JUnit Jupiter | 5.13.4 |
| Mockito | 5.20.0; inherited interface proxy configuration |
| Compiler Plugin | 3.14.1 |
| Surefire Plugin | 3.5.4; fail if no tests are found |

From `after`:

```bash
mvn --batch-mode verify
java -cp target/classes Chapter09Demo
```

To run only this chapter's new tests:

```bash
mvn --batch-mode -Dtest=BehaviourStrategyTest,LifecycleExamplesTest,NotificationPublisherTest,ReserveEquipmentCommandTest test
```

The first Maven build needs dependency access. The Bash wrapper `bash scripts/check.sh` still delegates to the full Maven gate. The separate lifecycle and Chapter 8 pattern examples have no standalone launchers; their tests are their executable demonstrations.

### 1.2 Expected demonstration

```text
Before execution: 0
Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22). Notification failed; reservation retained.
Observer events: [Desk: R1, Audit: R1]
Stored reservations: 1
Separate lifecycle exercise: RETURNED
```

The command is constructed before the first line and executed for the second. One synthetic observer fails with an expected notification exception. The later audit observer still receives the record. The final line concerns a different object in the isolated lifecycle exercise; it does not return or cancel R1 in the running application.

The full build executes 107 JUnit invocations. This includes 63 inherited cases and 44 new cases. Invocation count is an execution inventory, not a measure of design quality or a claim of exhaustive application correctness.

## 2. Design map and behaviour contracts

### 2.1 New files

| File | Purpose |
|---|---|
| `NotificationPublisher.java` | Optional Observer-based sender; nested callback and subscription contracts |
| `Command.java` | Result-bearing action interface |
| `ReserveEquipmentCommand.java` | Captured request invoking the existing service |
| `Chapter09Demo.java` | Explicitly composed publisher and command demonstration |
| `behaviour/LifecycleExamples.java` | Separate proposed lifecycle; conditional starting point and State completion |
| `BehaviourStrategyTest.java` | Compare existing strategies with a small conditional and an independent table |
| `behaviour/LifecycleExamplesTest.java` | All 20 status/action pairs plus independent-context test |
| `NotificationPublisherTest.java` | Dispatch, subscription and partial-failure behaviour |
| `ReserveEquipmentCommandTest.java` | Lazy construction, execution state, replay and failure propagation |

The existing `patterns` package remains Chapter 8's isolated material. The new `behaviour` package contains only the lifecycle exercise. Neither named package imports the cumulative application's unnamed-package classes. Chapter 10 will address application structure explicitly.

### 2.2 Strategy is already present

`BorrowingPolicy` is the common contract. `ReservationRules` and `StaffReservationRules` are the existing strategies. The coordinator's injected map chooses the applicable policy. No new runtime policy class is required to demonstrate the pattern.

The conditional comparison exists only inside `BehaviourStrategyTest`. It assumes the two currently supported category enum values; its default branch is not a general policy for unknown future categories. Each implementation is tested against explicit expected values rather than only against the other implementation.

The alternative staff lambda is a test fixture with limits of one counted reservation and two days. It obeys the common side-effect-free boolean contract. It is not adopted as the default staff rule.

### 2.3 Proposed lifecycle contract

The lifecycle starts REQUESTED. Allowed edges are REQUESTED to CONFIRMED or CANCELLED; CONFIRMED to ON_LOAN or CANCELLED; and ON_LOAN to RETURNED. All other operations reject with `IllegalStateException` and preserve status. RETURNED and CANCELLED are terminal for the four exposed actions.

The `ConditionalReservation` class is the starting example, not intentionally broken code. `StateReservation` is the alternative organisation. Private `Phase` enum constants contain stateless behaviour; each context owns its own phase reference. There is no public setter, no date handling, no storage and no connection to `LoanService`.

### 2.4 Publisher contract

The publisher calls a snapshot of registered observers in registration order. Subscription changes during callbacks apply to later publications. Registering the same observer reference twice is rejected; separate observer objects are not deduplicated. Each subscription handle refers to one entry, so closing an old handle cannot remove a newer registration.

Expected `NotificationException` failures are collected as suppressed exceptions on one aggregate exception after remaining observers have been attempted. Unexpected exceptions stop dispatch immediately and propagate. If an unexpected failure occurs after earlier expected failures, that unexpected failure is the propagated outcome; this small implementation does not attach the earlier aggregate to it.

The coordinator stores first, then calls the publisher. Its existing catch handles the aggregate expected failure and retains the record. An unexpected failure escapes after storage. The publisher's `finally` block resets a reentrancy guard in either case. The guard is not thread safety or rollback. Callbacks must not mutate the coordinator or start new reservation operations from inside notification.

Zero subscribers yields normal return without any delivery claim. A subscription can be closed repeatedly. Nested publication through the same publisher is rejected. There is no retry, durable event storage, remote messaging or automatic recovery.

### 2.5 Command contract

The command captures a receiver and request arguments. Required references and identifiers are checked at construction; duration eligibility remains with the receiver at execution. Constructing the command performs no lookup or reservation. `execute` delegates synchronously on the caller's thread.

The record's fields are final, but its receiver is a mutable service. Construction therefore does not capture an availability snapshot or guarantee a later successful reservation. Repeated execution re-enters the service; no deduplication, undo or transactional semantics are supplied.

## 3. Complete application and example sources

Inherited files are included so the checkpoint can be reconstructed independently. New code is additional to the previous checkpoint rather than a rewrite of its contracts.

### 3.1 `after/src/main/java/Borrower.java`

```java
import java.util.Objects;

public record Borrower(String id, BorrowerCategory category) {
    public Borrower {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("Borrower id required");
        Objects.requireNonNull(category, "category");
    }
}
```

### 3.2 `after/src/main/java/BorrowerCategory.java`

```java
public enum BorrowerCategory {
    STUDENT, STAFF
}
```

### 3.3 `after/src/main/java/BorrowerDirectory.java`

```java
import java.util.Optional;

/** Empty means absent or inactive, never a provider outage. */
@FunctionalInterface
public interface BorrowerDirectory {
    Optional<Borrower> find(String borrowerId);
}
```

### 3.4 `after/src/main/java/BorrowingPolicy.java`

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

### 3.5 `after/src/main/java/Chapter04Demo.java`

```java
import java.time.LocalDate;

public final class Chapter04Demo {
    public static void main(String[] args) {
        ReservationCoordinator coordinator = ReservationApplication.create(new RecordingNotificationSender());
        LocalDate start = LocalDate.of(2026, 10, 20);
        System.out.println(coordinator.reserve("B1", "CAM1", start, 2));
        System.out.println(coordinator.reserve("B2", "CAM1", start.plusDays(1), 1));
        System.out.println(coordinator.reserve("B2", "CAM1", start.plusDays(2), 1));
        System.out.println("Stored reservations: " + coordinator.reservations().size());
    }
}
```

### 3.6 `after/src/main/java/Chapter05Demo.java`

```java
import java.time.LocalDate;

public final class Chapter05Demo {
    public static void main(String[] args) {
        ReservationCoordinator coordinator = ReservationApplication.create(new RecordingNotificationSender());
        LocalDate day = LocalDate.of(2026, 10, 20);
        System.out.println(coordinator.reserve("S1", "CAM1", day, 14,
                BorrowerCategory.STAFF));
        System.out.println(coordinator.reserve("B1", "MIC1", day, 14));
        System.out.println(coordinator.reserve("B1", "CAM1", day.plusDays(1), 1));
        System.out.println(coordinator.reserve("B1", "CAM1", day.plusDays(14), 1));
        System.out.println("Stored reservations: " + coordinator.reservations().size());
    }
}
```

### 3.7 `after/src/main/java/Chapter07Demo.java`

```java
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;

public final class Chapter07Demo {
    public static void main(String[] args) {
        RecordingNotificationSender inbox = new RecordingNotificationSender();
        ReservationCoordinator reservations = ReservationApplication.create(inbox);
        LocalDate day = LocalDate.of(2026, 10, 20);
        System.out.println("Available before reservation: " + reservations.isAvailable("CAM1", day, day.plusDays(2)));
        System.out.println(reservations.reserve("B1", "CAM1", day, 2));
        System.out.println("Available after reservation: " + reservations.isAvailable("CAM1", day, day.plusDays(2)));
        LoanService loans = new LoanService(reservations,
                Clock.fixed(Instant.parse("2026-10-20T12:00:00Z"), ZoneOffset.UTC));
        System.out.println("Loan active after checkout: " + loans.checkOut("R1").active());
        System.out.println("Loan active after return: " + loans.returnLoan("R1").active());
        System.out.println("Accepted-reservation notices: " + inbox.received().size());
    }
}
```

### 3.8 `after/src/main/java/Chapter08Demo.java`

```java
import java.time.LocalDate;
import java.util.Map;

public final class Chapter08Demo {
    public static void main(String[] args) {
        var rows = Map.of(
                "B1", new LegacyDirectoryClient.Person("B1", "S", "Y"),
                "B2", new LegacyDirectoryClient.Person("B2", "T", "Y"));
        BorrowerDirectory directory = new LegacyDirectoryAdapter(rows::get);
        var notices = new RecordingNotificationSender();
        var coordinator = ReservationApplication.create(notices);
        var service = new DirectoryReservationService(directory, coordinator);
        LocalDate start = LocalDate.of(2026, 10, 20);
        System.out.println(service.reserve("B2", "CAM1", start, 10));
        System.out.println(service.reserve("B1", "MIC1", start, 10));
        System.out.println(service.reserve("UNKNOWN", "MIC1", start, 2));
        System.out.println("Reservations: " + coordinator.reservations().size());
        System.out.println("Notices: " + notices.received().size());
    }
}
```

### 3.9 `after/src/main/java/Chapter09Demo.java`

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Optional;
import behaviour.LifecycleExamples.StateReservation;

public final class Chapter09Demo {
    public static void main(String[] args) {
        var publisher = new NotificationPublisher();
        var events = new ArrayList<String>();
        publisher.subscribe(reservation -> events.add("Desk: " + reservation.id()));
        publisher.subscribe(reservation -> { throw new NotificationException("Display offline"); });
        publisher.subscribe(reservation -> events.add("Audit: " + reservation.id()));
        var coordinator = ReservationApplication.create(publisher);
        var service = new DirectoryReservationService(
                id -> Optional.of(new Borrower(id, BorrowerCategory.STUDENT)), coordinator);
        Command<String> request = new ReserveEquipmentCommand(
                service, "B1", "CAM1", LocalDate.of(2026, 10, 20), 2);
        System.out.println("Before execution: " + coordinator.reservations().size());
        System.out.println(request.execute());
        System.out.println("Observer events: " + events);
        System.out.println("Stored reservations: " + coordinator.reservations().size());
        var lifecycle = new StateReservation();
        lifecycle.confirm();
        lifecycle.checkOut();
        lifecycle.returnItem();
        System.out.println("Separate lifecycle exercise: " + lifecycle.status());
    }
}
```

### 3.10 `after/src/main/java/Command.java`

```java
/** Executes synchronously on the caller's thread; no queue or retry is implied. */
@FunctionalInterface
public interface Command<R> {
    R execute();
}
```

### 3.11 `after/src/main/java/ConfirmationFormatter.java`

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

### 3.12 `after/src/main/java/ConsoleNotificationSender.java`

```java
import java.io.PrintStream;
import java.util.Objects;

public final class ConsoleNotificationSender implements NotificationSender {
    private final PrintStream output;
    private final ConfirmationFormatter formatter;

    public ConsoleNotificationSender(PrintStream output, ConfirmationFormatter formatter) {
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

### 3.13 `after/src/main/java/DirectoryException.java`

```java
public final class DirectoryException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    public DirectoryException(String message) { super(message); }
    public DirectoryException(String message, Throwable cause) { super(message, cause); }
}
```

### 3.14 `after/src/main/java/DirectoryReservationService.java`

```java
import java.time.LocalDate;
import java.util.Objects;

/** Directory-backed entry point; this does not authenticate the caller. */
public final class DirectoryReservationService {
    private final BorrowerDirectory directory;
    private final ReservationCoordinator coordinator;

    public DirectoryReservationService(BorrowerDirectory directory,
                                       ReservationCoordinator coordinator) {
        this.directory = Objects.requireNonNull(directory, "directory");
        this.coordinator = Objects.requireNonNull(coordinator, "coordinator");
    }

    public String reserve(String borrowerId, String itemId, LocalDate start, int days) {
        if (borrowerId == null || borrowerId.isBlank() || itemId == null || itemId.isBlank()) {
            throw new IllegalArgumentException("Identifiers must not be blank.");
        }
        Objects.requireNonNull(start, "start");
        var found = directory.find(borrowerId);
        if (found.isEmpty()) return "Rejected: borrower not found or inactive.";
        Borrower borrower = found.get();
        if (!borrowerId.equals(borrower.id())) {
            throw new DirectoryException("Directory returned a different borrower");
        }
        return coordinator.reserve(borrower.id(), itemId, start, days, borrower.category());
    }
}
```

### 3.15 `after/src/main/java/LegacyDirectoryAdapter.java`

```java
import java.util.Objects;
import java.util.Optional;

public final class LegacyDirectoryAdapter implements BorrowerDirectory {
    private final LegacyDirectoryClient client;

    public LegacyDirectoryAdapter(LegacyDirectoryClient client) {
        this.client = Objects.requireNonNull(client, "client");
    }

    @Override
    public Optional<Borrower> find(String borrowerId) {
        if (borrowerId == null || borrowerId.isBlank()) {
            throw new IllegalArgumentException("Borrower id required");
        }
        LegacyDirectoryClient.Person row;
        try {
            row = client.lookup(borrowerId);
        } catch (LegacyDirectoryClient.Failure failure) {
            throw new DirectoryException("Borrower directory unavailable", failure);
        }
        if (row == null) return Optional.empty();
        if (!borrowerId.equals(row.key())) throw new DirectoryException("Mismatched borrower id");
        BorrowerCategory category;
        if ("S".equals(row.kind())) category = BorrowerCategory.STUDENT;
        else if ("T".equals(row.kind())) category = BorrowerCategory.STAFF;
        else throw new DirectoryException("Unsupported borrower category");
        if ("N".equals(row.status())) return Optional.empty();
        if (!"Y".equals(row.status())) throw new DirectoryException("Unsupported borrower status");
        return Optional.of(new Borrower(row.key(), category));
    }
}
```

### 3.16 `after/src/main/java/LegacyDirectoryClient.java`

```java
/** Illustrative provider contract, not an actual university API or network client. */
@FunctionalInterface
public interface LegacyDirectoryClient {
    // null means no row; codes are exact and case-sensitive.
    Person lookup(String key);

    record Person(String key, String kind, String status) { }

    final class Failure extends RuntimeException {
        private static final long serialVersionUID = 1L;

        public Failure(String message) { super(message); }
    }
}
```

### 3.17 `after/src/main/java/Loan.java`

```java
import java.time.LocalDate;
import java.util.Objects;

/** Immutable loan state. A null returnedOn means this loan is active. */
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

### 3.18 `after/src/main/java/LoanPeriod.java`

```java
import java.time.LocalDate;
import java.util.Objects;

public final class LoanPeriod {
    private final LocalDate start;
    private final LocalDate endExclusive;

    public LoanPeriod(LocalDate start, LocalDate endExclusive) {
        this.start = Objects.requireNonNull(start, "start");
        this.endExclusive = Objects.requireNonNull(endExclusive, "endExclusive");
        if (!start.isBefore(endExclusive)) {
            throw new IllegalArgumentException("End must be after start.");
        }
    }

    public LocalDate start() {
        return start;
    }

    public LocalDate endExclusive() {
        return endExclusive;
    }

    public boolean overlaps(LoanPeriod other) {
        Objects.requireNonNull(other, "other");
        return start.isBefore(other.endExclusive)
                && other.start.isBefore(endExclusive);
    }
}
```

### 3.19 `after/src/main/java/LoanService.java`

```java
import java.time.Clock;
import java.time.LocalDate;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/** One service per coordinator/session; sequential, in-memory teaching flow. */
public final class LoanService {
    private final ReservationCoordinator reservations;
    private final Clock clock;
    private final Map<String, Loan> loans = new LinkedHashMap<>();

    public LoanService(ReservationCoordinator reservations, Clock clock) {
        this.reservations = Objects.requireNonNull(reservations, "reservations");
        this.clock = Objects.requireNonNull(clock, "clock");
    }

    public Loan checkOut(String reservationId) {
        Reservation reservation = reservations.reservations().stream()
                .filter(r -> r.id().equals(reservationId))
                .findFirst().orElseThrow(() -> new IllegalArgumentException("Unknown reservation."));
        if (loans.containsKey(reservationId)) {
            throw new IllegalStateException("Reservation already used for a loan.");
        }
        LocalDate today = LocalDate.now(clock);
        if (today.isBefore(reservation.period().start())
                || !today.isBefore(reservation.period().endExclusive())) {
            throw new IllegalStateException("Checkout must be within the reservation period.");
        }
        boolean itemAlreadyOut = loans.values().stream()
                .anyMatch(loan -> loan.active() && loan.itemId().equals(reservation.itemId()));
        if (itemAlreadyOut) throw new IllegalStateException("Item is already on loan.");
        Loan loan = new Loan(reservation.id(), reservation.borrowerId(),
                reservation.itemId(), today, null);
        loans.put(reservationId, loan);
        return loan;
    }

    public Loan returnLoan(String reservationId) {
        Loan current = loans.get(reservationId);
        if (current == null || !current.active()) {
            throw new IllegalStateException("No active loan for this reservation.");
        }
        Loan returned = new Loan(current.reservationId(), current.borrowerId(),
                current.itemId(), current.borrowedOn(), LocalDate.now(clock));
        loans.put(reservationId, returned);
        return returned;
    }

    public List<Loan> loans() { return List.copyOf(loans.values()); }
}
```

### 3.20 `after/src/main/java/NotificationException.java`

```java
public final class NotificationException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    public NotificationException(String message) { super(message); }
}
```

### 3.21 `after/src/main/java/NotificationPublisher.java`

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Sequential, in-process Observer example. No retries or durable delivery. */
public final class NotificationPublisher implements NotificationSender {
    @FunctionalInterface
    public interface Observer { void onConfirmed(Reservation reservation); }
    @FunctionalInterface
    public interface Subscription extends AutoCloseable { @Override void close(); }
    private static final class Entry {
        private final Observer observer;
        private Entry(Observer observer) { this.observer = observer; }
    }
    private final List<Entry> entries = new ArrayList<>();
    private boolean publishing;

    public Subscription subscribe(Observer observer) {
        Objects.requireNonNull(observer, "observer");
        if (entries.stream().anyMatch(entry -> entry.observer == observer)) {
            throw new IllegalArgumentException("Observer already subscribed");
        }
        Entry entry = new Entry(observer);
        entries.add(entry);
        return () -> entries.remove(entry);
    }

    @Override
    public void send(Reservation reservation) {
        Objects.requireNonNull(reservation, "reservation");
        if (publishing) throw new IllegalStateException("Reentrant publication is not supported");
        publishing = true;
        try {
            NotificationException aggregate = null;
            for (Entry entry : List.copyOf(entries)) {
                try {
                    entry.observer.onConfirmed(reservation);
                } catch (NotificationException failure) {
                    if (aggregate == null) aggregate = new NotificationException("One or more observers failed");
                    aggregate.addSuppressed(failure);
                }
            }
            if (aggregate != null) throw aggregate;
        } finally {
            publishing = false;
        }
    }
}
```

### 3.22 `after/src/main/java/NotificationSender.java`

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

### 3.23 `after/src/main/java/RecordingNotificationSender.java`

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class RecordingNotificationSender implements NotificationSender {
    private final List<Reservation> received = new ArrayList<>();

    @Override
    public void send(Reservation reservation) {
        received.add(Objects.requireNonNull(reservation, "reservation"));
    }

    public List<Reservation> received() { return List.copyOf(received); }
}
```

### 3.24 `after/src/main/java/Reservation.java`

```java
import java.util.Objects;

public final class Reservation {
    private final String id;
    private final String borrowerId;
    private final String itemId;
    private final LoanPeriod period;

    public Reservation(String id, String borrowerId, String itemId,
                       LoanPeriod period) {
        this.id = requireText(id);
        this.borrowerId = requireText(borrowerId);
        this.itemId = requireText(itemId);
        this.period = Objects.requireNonNull(period, "period");
    }

    private static String requireText(String value) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Identifiers must not be blank.");
        }
        return value;
    }

    public String id() { return id; }
    public String borrowerId() { return borrowerId; }
    public String itemId() { return itemId; }
    public LoanPeriod period() { return period; }
}
```

### 3.25 `after/src/main/java/ReservationApplication.java`

```java
import java.time.LocalDate;
import java.util.Map;

public final class ReservationApplication {
    private ReservationApplication() { }

    public static ReservationCoordinator create(NotificationSender sender) {
        return new ReservationCoordinator(
                Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                       BorrowerCategory.STAFF, new StaffReservationRules()),
                new ConfirmationFormatter(), sender);
    }

    public static void main(String[] args) {
        ConfirmationFormatter noticeFormat = new ConfirmationFormatter();
        NotificationSender sender = new ConsoleNotificationSender(System.out, noticeFormat);
        ReservationCoordinator coordinator = create(sender);
        String result = coordinator.reserve("B1", "CAM1", LocalDate.of(2026, 10, 20), 2);
        System.out.println("Result: " + result);
    }
}
```

### 3.26 `after/src/main/java/ReservationCoordinator.java`

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Map;

public final class ReservationCoordinator {
    private final List<Reservation> reservations = new ArrayList<>();
    private final Map<BorrowerCategory, BorrowingPolicy> policies;
    private final ConfirmationFormatter formatter;
    private final NotificationSender notifications;

    public ReservationCoordinator(Map<BorrowerCategory, BorrowingPolicy> policies,
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

    public String reserve(String borrowerId, String itemId,
                          LocalDate start, int requestedDays) {
        return reserve(borrowerId, itemId, start, requestedDays, BorrowerCategory.STUDENT);
    }

    public String reserve(String borrowerId, String itemId, LocalDate start,
                          int requestedDays, BorrowerCategory category) {
        Objects.requireNonNull(category, "category");
        if (borrowerId == null || borrowerId.isBlank()
                || itemId == null || itemId.isBlank()) {
            throw new IllegalArgumentException("Identifiers must not be blank.");
        }
        Objects.requireNonNull(start, "start");

        int activeCount = 0;
        for (Reservation existing : reservations) {
            if (existing.borrowerId().equals(borrowerId)) {
                activeCount++;
            }
        }
        if (!policies.get(category).mayRequest(activeCount, requestedDays)) {
            return "Rejected: borrower limit or duration.";
        }

        LoanPeriod requested = new LoanPeriod(
                start, start.plusDays(requestedDays));
        if (hasConflict(itemId, requested)) {
            return "Rejected: item unavailable.";
        }

        Reservation reservation = new Reservation(
                "R" + (reservations.size() + 1), borrowerId, itemId, requested);
        reservations.add(reservation);
        String confirmation = formatter.format(reservation);
        try {
            notifications.send(reservation);
        } catch (NotificationException failure) {
            return confirmation + " Notification failed; reservation retained.";
        }
        return confirmation;
    }

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

    public List<Reservation> reservations() {
        return List.copyOf(reservations);
    }
}
```

### 3.27 `after/src/main/java/ReservationRules.java`

```java
public final class ReservationRules implements BorrowingPolicy {
    @Override
    public boolean mayRequest(int activeReservations, int requestedDays) {
        return activeReservations >= 0
                && activeReservations < 3
                && requestedDays >= 1
                && requestedDays <= 7;
    }
}
```

### 3.28 `after/src/main/java/ReserveEquipmentCommand.java`

```java
import java.time.LocalDate;
import java.util.Objects;

/** Captures a request and receiver; constructing it performs no reservation. */
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

### 3.29 `after/src/main/java/StaffReservationRules.java`

```java
/** Illustrative teaching policy, not an approved institutional rule. */
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

### 3.30 `after/src/main/java/behaviour/LifecycleExamples.java`

```java
package behaviour;

/** Proposed lifecycle only: not integrated with ReservationCoordinator or LoanService. */
public final class LifecycleExamples {
    private LifecycleExamples() { }
    public enum Status { REQUESTED, CONFIRMED, ON_LOAN, RETURNED, CANCELLED }
    public interface Lifecycle {
        Status status();
        void confirm();
        void checkOut();
        void returnItem();
        void cancel();
    }

    // Starting design: operation-specific switches repeat state decisions.
    public static final class ConditionalReservation implements Lifecycle {
        private Status status = Status.REQUESTED;
        public Status status() { return status; }
        public void confirm() {
            switch (status) {
                case REQUESTED -> status = Status.CONFIRMED;
                default -> throw rejected("confirm", status);
            }
        }
        public void checkOut() {
            switch (status) {
                case CONFIRMED -> status = Status.ON_LOAN;
                default -> throw rejected("check out", status);
            }
        }
        public void returnItem() {
            switch (status) {
                case ON_LOAN -> status = Status.RETURNED;
                default -> throw rejected("return", status);
            }
        }
        public void cancel() {
            switch (status) {
                case REQUESTED, CONFIRMED -> status = Status.CANCELLED;
                default -> throw rejected("cancel", status);
            }
        }
    }

    // Completed State design: context delegates to the current state object.
    public static final class StateReservation implements Lifecycle {
        private Phase phase = Phase.REQUESTED;
        public Status status() { return phase.status; }
        public void confirm() { phase = phase.confirm(); }
        public void checkOut() { phase = phase.checkOut(); }
        public void returnItem() { phase = phase.returnItem(); }
        public void cancel() { phase = phase.cancel(); }
    }
    private enum Phase {
        REQUESTED(Status.REQUESTED) {
            @Override Phase confirm() { return CONFIRMED; }
            @Override Phase cancel() { return CANCELLED; }
        },
        CONFIRMED(Status.CONFIRMED) {
            @Override Phase checkOut() { return ON_LOAN; }
            @Override Phase cancel() { return CANCELLED; }
        },
        ON_LOAN(Status.ON_LOAN) {
            @Override Phase returnItem() { return RETURNED; }
        },
        RETURNED(Status.RETURNED),
        CANCELLED(Status.CANCELLED);

        final Status status;
        Phase(Status status) { this.status = status; }
        Phase confirm() { throw rejected("confirm", status); }
        Phase checkOut() { throw rejected("check out", status); }
        Phase returnItem() { throw rejected("return", status); }
        Phase cancel() { throw rejected("cancel", status); }
    }
    private static IllegalStateException rejected(String action, Status status) {
        return new IllegalStateException("Cannot " + action + " in " + status);
    }
}
```

### 3.31 `after/src/main/java/patterns/PatternExamples.java`

```java
package patterns;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Isolated teaching examples; none is wired into the lending application. */
public final class PatternExamples {
    private PatternExamples() { }

    // Factory Method: inherited workflow invokes an overridable creation hook.
    public interface Exporter { String export(String value); }
    public abstract static class ExportJob {
        protected abstract Exporter createExporter();
        public final String run(String value) {
            Objects.requireNonNull(value, "value");
            return createExporter().export(value);
        }
    }
    public static final class PlainJob extends ExportJob {
        @Override protected Exporter createExporter() { return value -> "TEXT: " + value; }
    }
    public static final class HtmlJob extends ExportJob {
        @Override protected Exporter createExporter() { return value -> "<p>" + escape(value) + "</p>"; }
    }
    // Simple factory: useful, but no overridden creation hook.
    public static Exporter simpleExporter(boolean html) {
        return html ? value -> "<p>" + escape(value) + "</p>" : value -> "TEXT: " + value;
    }

    // Abstract Factory: two product roles, supplied as a related family.
    public interface Heading { String render(String text); }
    public interface Body { String render(String text); }
    public interface ReceiptFamily {
        Heading heading();
        Body body();
    }
    public static final class PlainFamily implements ReceiptFamily {
        public Heading heading() { return text -> text + "\n"; }
        public Body body() { return text -> text + "\n"; }
    }
    public static final class HtmlFamily implements ReceiptFamily {
        public Heading heading() { return text -> "<h1>" + escape(text) + "</h1>"; }
        public Body body() { return text -> "<p>" + escape(text) + "</p>"; }
    }
    public static String receipt(ReceiptFamily family, String title, String detail) {
        Objects.requireNonNull(family, "family");
        return family.heading().render(title) + family.body().render(detail);
    }
    private static String escape(String text) {
        return Objects.requireNonNull(text, "text").replace("&", "&amp;")
                .replace("<", "&lt;").replace(">", "&gt;");
    }

    // Fluent builder variant: staged configuration, one immutable product.
    public static final class ReportRequest {
        private final String borrowerId;
        private final LocalDate from;
        private final LocalDate toExclusive;
        private final boolean includeReturned;
        private final List<String> columns;
        private ReportRequest(Builder builder) {
            if ((builder.from == null) != (builder.toExclusive == null)) {
                throw new IllegalArgumentException("Both dates or neither are required");
            }
            if (builder.from != null && !builder.from.isBefore(builder.toExclusive)) {
                throw new IllegalArgumentException("Positive interval required");
            }
            borrowerId = builder.borrowerId;
            from = builder.from;
            toExclusive = builder.toExclusive;
            includeReturned = builder.includeReturned;
            columns = List.copyOf(builder.columns);
        }
        public String borrowerId() { return borrowerId; }
        public LocalDate from() { return from; }
        public LocalDate toExclusive() { return toExclusive; }
        public boolean includeReturned() { return includeReturned; }
        public List<String> columns() { return columns; }
        public static Builder forBorrower(String id) { return new Builder(id); }
        public static final class Builder {
            private final String borrowerId;
            private LocalDate from;
            private LocalDate toExclusive;
            private boolean includeReturned;
            private final List<String> columns = new ArrayList<>();
            private Builder(String id) {
                if (id == null || id.isBlank()) throw new IllegalArgumentException("Borrower id required");
                borrowerId = id;
            }
            public Builder during(LocalDate from, LocalDate toExclusive) {
                Objects.requireNonNull(from, "from");
                Objects.requireNonNull(toExclusive, "toExclusive");
                this.from = from;
                this.toExclusive = toExclusive;
                return this;
            }
            public Builder includeReturned(boolean value) { includeReturned = value; return this; }
            public Builder column(String value) {
                if (value == null || value.isBlank()) throw new IllegalArgumentException("Column required");
                columns.add(value);
                return this;
            }
            public ReportRequest build() { return new ReportRequest(this); }
        }
    }

    // Decorators: same interface, explicit order and expected failure type.
    public interface Sender { void send(String message); }
    public static final class DeliveryFailure extends RuntimeException {
        private static final long serialVersionUID = 1L;

        public DeliveryFailure(String message) { super(message); }
    }
    public static final class AuditedSender implements Sender {
        private final Sender delegate;
        private final List<String> events;
        public AuditedSender(Sender delegate, List<String> events) {
            this.delegate = Objects.requireNonNull(delegate, "delegate");
            this.events = Objects.requireNonNull(events, "events");
        }
        public void send(String message) {
            events.add("attempt");
            try {
                delegate.send(message);
            } catch (DeliveryFailure failure) {
                events.add("failed");
                throw failure;
            }
            events.add("sent");
        }
    }
    public static final class RetryOnceSender implements Sender {
        private final Sender delegate;
        public RetryOnceSender(Sender delegate) { this.delegate = Objects.requireNonNull(delegate, "delegate"); }
        public void send(String message) {
            try {
                delegate.send(message);
            } catch (DeliveryFailure failure) {
                delegate.send(message);
            }
        }
    }
}
```

## 4. Complete test sources

The original tests remain in the build. The four new classes cover this chapter’s declared behaviours.

### 4.1 `after/src/test/java/AvailabilityTddTest.java`

```java
import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AvailabilityTddTest {
    @Test
    void overlappingEnquiryIsUnavailableWithoutChangingRecordsOrNotifying() {
        // Arrange: one confirmed CAM1 reservation, ending exclusively on 22 October.
        RecordingNotificationSender inbox = new RecordingNotificationSender();
        ReservationCoordinator coordinator = ReservationApplication.create(inbox);
        LocalDate start = LocalDate.of(2026, 10, 20);
        coordinator.reserve("B1", "CAM1", start, 2);
        List<Reservation> recordsBefore = coordinator.reservations();
        List<Reservation> noticesBefore = inbox.received();

        // Act: inspect the overlapping interval without requesting a reservation.
        boolean available = coordinator.isAvailable("CAM1", start.plusDays(1), start.plusDays(3));

        // Assert: the answer and both kinds of state matter.
        assertAll(
                () -> assertFalse(available, "An overlapping item must be unavailable"),
                () -> assertEquals(recordsBefore, coordinator.reservations()),
                () -> assertEquals(noticesBefore, inbox.received()));
    }
}
```

### 4.2 `after/src/test/java/AvailabilityTest.java`

```java
import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

class AvailabilityTest {
    private final LocalDate day = LocalDate.of(2026, 10, 20);
    private final RecordingNotificationSender inbox = new RecordingNotificationSender();
    private final ReservationCoordinator c = ReservationApplication.create(inbox);

    @Test void emptyScheduleIsAvailableWithoutAnySideEffect() {
        assertTrue(c.isAvailable("CAM1", day, day.plusDays(2)));
        assertTrue(c.reservations().isEmpty());
        assertTrue(inbox.received().isEmpty());
    }

    @Test void adjacentPeriodAndDifferentItemAreAvailable() {
        c.reserve("B1", "CAM1", day, 2);
        List<Reservation> records = c.reservations();
        List<Reservation> notices = inbox.received();
        assertTrue(c.isAvailable("CAM1", day.plusDays(2), day.plusDays(3)));
        assertTrue(c.isAvailable("MIC1", day, day.plusDays(2)));
        assertEquals(records, c.reservations());
        assertEquals(notices, inbox.received());
    }

    @ParameterizedTest @ValueSource(ints = {0, -1})
    void invalidPeriodFailsWithoutChangingState(int endOffset) {
        c.reserve("B1", "CAM1", day, 2);
        List<Reservation> records = c.reservations();
        List<Reservation> notices = inbox.received();
        assertThrows(IllegalArgumentException.class,
                () -> c.isAvailable("CAM1", day, day.plusDays(endOffset)));
        assertEquals(records, c.reservations());
        assertEquals(notices, inbox.received());
    }

    @Test void malformedIdentifiersAndNullDatesAreRejected() {
        assertThrows(IllegalArgumentException.class, () -> c.isAvailable(" ", day, day.plusDays(1)));
        assertThrows(IllegalArgumentException.class, () -> c.isAvailable(null, day, day.plusDays(1)));
        assertThrows(NullPointerException.class, () -> c.isAvailable("CAM1", null, day.plusDays(1)));
        assertThrows(NullPointerException.class, () -> c.isAvailable("CAM1", day, null));
        assertTrue(c.reservations().isEmpty());
        assertTrue(inbox.received().isEmpty());
    }

    @Test void queryDoesNotAllocateAnIdentifier() {
        c.isAvailable("CAM1", day, day.plusDays(1));
        assertEquals("Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-21).",
                c.reserve("B1", "CAM1", day, 1));
    }

    @Test void availabilityDoesNotMeanBorrowerEligibility() {
        for (String item : List.of("CAM1", "MIC1", "TRI1")) c.reserve("B1", item, day, 1);
        assertTrue(c.isAvailable("CAM2", day, day.plusDays(1)));
        assertEquals("Rejected: borrower limit or duration.", c.reserve("B1", "CAM2", day, 1));
        assertEquals(3, inbox.received().size());
    }

    @Test void queryCanSpanMoreDaysThanAStudentMayReserve() {
        assertTrue(c.isAvailable("CAM1", day, day.plusDays(30)));
        assertEquals("Rejected: borrower limit or duration.", c.reserve("B1", "CAM1", day, 30));
    }
}
```

### 4.3 `after/src/test/java/BehaviourStrategyTest.java`

```java
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDate;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class BehaviourStrategyTest {
    // Starting conditional design retained only for comparison in this exercise.
    private boolean conditional(BorrowerCategory category, int count, int days) {
        if (category == BorrowerCategory.STUDENT) {
            return count >= 0 && count < 3 && days >= 1 && days <= 7;
        }
        return count >= 0 && count < 5 && days >= 1 && days <= 14;
    }
    @ParameterizedTest
    @CsvSource({"STUDENT,2,7,true", "STUDENT,3,7,false", "STUDENT,0,8,false",
            "STUDENT,-1,2,false", "STAFF,4,14,true", "STAFF,5,14,false",
            "STAFF,0,15,false", "STAFF,0,0,false"})
    void strategiesAndConditionalMatchIndependentExamples(BorrowerCategory category,
            int count, int days, boolean expected) {
        var policies = Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                BorrowerCategory.STAFF, new StaffReservationRules());
        assertEquals(expected, conditional(category, count, days));
        assertEquals(expected, policies.get(category).mayRequest(count, days));
    }
    @Test void injectedPolicyChangesDecisionWithoutChangingCoordinator() {
        BorrowingPolicy temporaryStaffRule = (count, days) -> count >= 0 && count < 1 && days >= 1 && days <= 2;
        var coordinator = new ReservationCoordinator(
                Map.of(BorrowerCategory.STUDENT, new ReservationRules(), BorrowerCategory.STAFF, temporaryStaffRule),
                new ConfirmationFormatter(), new RecordingNotificationSender());
        var start = LocalDate.of(2026, 10, 20);
        assertEquals("Rejected: borrower limit or duration.", coordinator.reserve("T1", "CAM1", start, 3, BorrowerCategory.STAFF));
        assertTrue(coordinator.reserve("T1", "CAM1", start, 2, BorrowerCategory.STAFF).startsWith("Confirmed: R1"));
        assertEquals("Rejected: borrower limit or duration.", coordinator.reserve("T1", "MIC1", start, 1, BorrowerCategory.STAFF));
        assertTrue(coordinator.reserve("S1", "MIC1", start, 7, BorrowerCategory.STUDENT).startsWith("Confirmed: R2"));
    }
}
```

### 4.4 `after/src/test/java/BorrowingPolicyTest.java`

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.assertEquals;

class BorrowingPolicyTest {
    @ParameterizedTest(name = "{0}: count={1}, days={2} -> {3}")
    @CsvSource({
        "STUDENT, 0, 1, true", "STUDENT, 2, 7, true",
        "STUDENT, 3, 1, false", "STUDENT, 0, 8, false",
        "STAFF, 4, 14, true", "STAFF, 5, 1, false",
        "STAFF, 0, 15, false", "STUDENT, -1, 1, false",
        "STAFF, 0, 0, false", "STAFF, 0, -1, false"
    })
    void documentedBoundaries(BorrowerCategory category, int count, int days, boolean expected) {
        BorrowingPolicy policy = category == BorrowerCategory.STUDENT
                ? new ReservationRules() : new StaffReservationRules();
        assertEquals(expected, policy.mayRequest(count, days));
    }
}
```

### 4.5 `after/src/test/java/Chapter02Checks.java`

```java
import java.time.DateTimeException;
import java.time.LocalDate;
import java.util.List;

public class Chapter02Checks {
    private static int checks;

    public static void main(String[] args) {
        LocalDate day = LocalDate.of(2026, 10, 20);
        LoanPeriod first = new LoanPeriod(day, day.plusDays(2));
        LoanPeriod overlapping = new LoanPeriod(day.plusDays(1), day.plusDays(3));
        LoanPeriod adjacent = new LoanPeriod(day.plusDays(2), day.plusDays(3));
        check(first.overlaps(overlapping), "overlap detected");
        check(overlapping.overlaps(first), "overlap is symmetric");
        check(!first.overlaps(adjacent), "adjacent periods allowed");
        check(!adjacent.overlaps(first), "adjacency symmetric");
        check(first.overlaps(new LoanPeriod(day, day.plusDays(2))), "equal periods overlap");
        check(first.overlaps(new LoanPeriod(day.minusDays(1), day.plusDays(4))),
                "containment overlaps");
        expect(IllegalArgumentException.class, () -> new LoanPeriod(day, day),
                "zero-length period");
        expect(IllegalArgumentException.class, () -> new LoanPeriod(day, day.minusDays(1)),
                "reversed period");
        expect(NullPointerException.class, () -> new LoanPeriod(null, day), "null start");
        expect(NullPointerException.class, () -> new LoanPeriod(day, null), "null end");

        ReservationCoordinator c = ReservationApplication.create(new RecordingNotificationSender());
        check(c.reserve("B1", "CAM1", day, 2).equals(
                "Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)."),
                "exact first confirmation");
        check(c.reservations().size() == 1, "one success stored");
        check(c.reserve("B2", "CAM1", day.plusDays(1), 1).equals(
                "Rejected: item unavailable."), "overlapping same item rejected");
        check(c.reservations().size() == 1, "conflict stores nothing");
        check(c.reserve("B2", "CAM1", day.plusDays(2), 1).equals(
                "Confirmed: R2 for B2 on CAM1 [2026-10-22, 2026-10-23)."),
                "adjacent request and identifier after rejection");
        check(c.reserve("B1", "MIC1", day, 7).equals(
                "Confirmed: R3 for B1 on MIC1 [2026-10-20, 2026-10-27)."),
                "different item and seven-day limit allowed");
        check(c.reserve("B1", "TRI1", day, 1).startsWith("Confirmed:"),
                "third active reservation allowed");
        check(c.reserve("B1", "CAM2", day, 1).equals(
                "Rejected: borrower limit or duration."), "fourth rejected");
        check(c.reservations().size() == 4, "borrower-limit rejection stores nothing");

        List<Reservation> snapshot = c.reservations();
        expect(UnsupportedOperationException.class, snapshot::clear, "snapshot unmodifiable");
        check(c.reservations().size() == 4, "failed clear preserves coordinator state");
        check(c.reserve("B3", "CAM2", day, 1).startsWith("Confirmed:"),
                "another borrower unaffected by B1 limit");
        check(snapshot.size() == 4 && c.reservations().size() == 5,
                "old snapshot does not track later additions");
        check(snapshot.get(0).period().start().equals(day), "stored period preserved");

        ReservationCoordinator invalid = ReservationApplication.create(new RecordingNotificationSender());
        check(invalid.reserve("B1", "CAM1", day, 0).equals(
                "Rejected: borrower limit or duration."), "zero duration rejected");
        check(invalid.reserve("B1", "CAM1", day, -1).equals(
                "Rejected: borrower limit or duration."), "negative duration rejected");
        check(invalid.reserve("B1", "CAM1", day, 8).equals(
                "Rejected: borrower limit or duration."), "eight-day duration rejected");
        expect(IllegalArgumentException.class, () -> invalid.reserve(" ", "CAM1", day, 1),
                "blank borrower");
        expect(IllegalArgumentException.class, () -> invalid.reserve("B1", null, day, 1),
                "null item");
        expect(NullPointerException.class, () -> invalid.reserve("B1", "CAM1", null, 1),
                "null request date");
        expect(DateTimeException.class, () -> invalid.reserve("B1", "CAM1", LocalDate.MAX, 1),
                "unrepresentable end date");
        check(invalid.reservations().isEmpty(), "invalid requests store nothing");
        expect(IllegalArgumentException.class,
                () -> new Reservation("", "B1", "CAM1", first), "blank reservation identifier");
        expect(NullPointerException.class,
                () -> new Reservation("R1", "B1", "CAM1", null), "null reservation period");
        System.out.println("All " + checks + " chapter checks passed.");
    }

    private static void check(boolean condition, String label) {
        if (!condition) {
            throw new AssertionError(label);
        }
        checks++;
    }

    private static void expect(Class<? extends Throwable> type, Runnable action,
                               String label) {
        try {
            action.run();
        } catch (Throwable error) {
            check(type.isInstance(error), label + ": wrong exception " + error);
            return;
        }
        throw new AssertionError(label + ": expected " + type.getSimpleName());
    }
}
```

### 4.6 `after/src/test/java/Chapter03AcceptanceExamples.java`

```java
import java.time.LocalDate;

public class Chapter03AcceptanceExamples {
    public static void main(String[] args) {
        LocalDate day = LocalDate.of(2026, 10, 20);
        ReservationCoordinator coordinator = ReservationApplication.create(new RecordingNotificationSender());

        // AC-01: an eligible request is stored once and confirmed.
        String accepted = coordinator.reserve("B1", "CAM1", day, 2);
        require(accepted.equals(
                "Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)."),
                "AC-01 confirmation");
        require(coordinator.reservations().size() == 1, "AC-01 one record");
        System.out.println("AC-01 passed");

        // AC-02: an overlapping request for the same item changes no records.
        String conflict = coordinator.reserve("B2", "CAM1", day.plusDays(1), 1);
        require(conflict.equals("Rejected: item unavailable."), "AC-02 rejection");
        require(coordinator.reservations().size() == 1, "AC-02 unchanged count");
        require(coordinator.reservations().get(0).borrowerId().equals("B1"),
                "AC-02 original borrower preserved");
        System.out.println("AC-02 passed");

        // AC-03: a booking may start at an existing exclusive end,
        // or end exactly where an existing booking starts.
        String adjacent = coordinator.reserve("B2", "CAM1", day.plusDays(2), 1);
        require(adjacent.equals(
                "Confirmed: R2 for B2 on CAM1 [2026-10-22, 2026-10-23)."),
                "AC-03 adjacent confirmation");
        require(coordinator.reservations().size() == 2, "AC-03 second record");
        String before = coordinator.reserve("B3", "CAM1", day.minusDays(1), 1);
        require(before.equals(
                "Confirmed: R3 for B3 on CAM1 [2026-10-19, 2026-10-20)."),
                "AC-03 request ending at an existing start");
        require(coordinator.reservations().size() == 3, "AC-03 third record");
        System.out.println("AC-03 passed");

        // AC-04: count limits span items, not just one equipment item.
        ReservationCoordinator limits = ReservationApplication.create(new RecordingNotificationSender());
        for (String item : new String[] {"CAM1", "MIC1", "TRI1"}) {
            require(limits.reserve("B1", item, day, 1).startsWith("Confirmed:"),
                    "AC-04 establish three valid reservations");
        }
        require(limits.reserve("B1", "CAM2", day, 1).equals(
                "Rejected: borrower limit or duration."), "AC-04 fourth rejected");
        require(limits.reservations().size() == 3, "AC-04 unchanged count");
        System.out.println("AC-04 passed");

        // AC-05: one and seven days are allowed; zero, negative and eight are not.
        ReservationCoordinator durations = ReservationApplication.create(new RecordingNotificationSender());
        require(durations.reserve("B1", "CAM1", day, 1).startsWith("Confirmed:"),
                "AC-05 one day");
        require(durations.reserve("B1", "MIC1", day, 7).startsWith("Confirmed:"),
                "AC-05 seven days");
        for (int days : new int[] {0, -1, 8}) {
            require(durations.reserve("B1", "TRI1", day, days).equals(
                    "Rejected: borrower limit or duration."), "AC-05 invalid duration");
            require(durations.reservations().size() == 2, "AC-05 unchanged count");
        }
        System.out.println("AC-05 passed");
        System.out.println("All 5 acceptance examples passed.");
    }

    private static void require(boolean condition, String description) {
        if (!condition) {
            throw new AssertionError(description);
        }
    }
}
```

### 4.7 `after/src/test/java/Chapter05Checks.java`

```java
import java.time.LocalDate;
import java.util.List;

public final class Chapter05Checks {
    private static int checks;

    public static void main(String[] args) {
        BorrowingPolicy student = new ReservationRules();
        BorrowingPolicy staff = new StaffReservationRules();
        sharedPolicyContract(student);
        sharedPolicyContract(staff);
        check(student.mayRequest(2, 7), "student upper accepted boundaries");
        check(!student.mayRequest(3, 7), "student fourth rejected");
        check(!student.mayRequest(0, 8), "student eight days rejected");
        check(staff.mayRequest(4, 14), "staff upper accepted boundaries");
        check(!staff.mayRequest(5, 14), "staff sixth rejected");
        check(!staff.mayRequest(0, 15), "staff fifteen days rejected");

        LocalDate day = LocalDate.of(2026, 10, 20);
        ReservationCoordinator c = ReservationApplication.create(new RecordingNotificationSender());
        check(c.reserve("S1", "CAM1", day, 14, BorrowerCategory.STAFF).equals(
                "Confirmed: R1 for S1 on CAM1 [2026-10-20, 2026-11-03)."),
                "staff confirmation with new limit");
        List<Reservation> snapshot = c.reservations();
        check(c.reserve("B1", "CAM1", day.plusDays(1), 1).equals(
                "Rejected: item unavailable."), "student conflicts with staff booking");
        check(c.reservations().equals(snapshot), "conflict preserves exact records");
        check(c.reserve("B1", "CAM1", day.plusDays(14), 1).equals(
                "Confirmed: R2 for B1 on CAM1 [2026-11-03, 2026-11-04)."),
                "cross-category adjacency and next identifier");
        List<Reservation> beforeInvalid = c.reservations();
        check(c.reserve("S1", "MIC1", day, 15, BorrowerCategory.STAFF).equals(
                "Rejected: borrower limit or duration."), "staff invalid duration result");
        check(c.reservations().equals(beforeInvalid), "invalid staff request preserves records");
        expect(NullPointerException.class,
                () -> c.reserve("S1", "MIC1", day, 1, null), "null category");
        check(c.reservations().equals(beforeInvalid), "null category preserves records");

        ReservationCoordinator limits = ReservationApplication.create(new RecordingNotificationSender());
        for (int i = 1; i <= 5; i++) {
            check(limits.reserve("S2", "ITEM" + i, day, 1, BorrowerCategory.STAFF)
                    .startsWith("Confirmed:"), "staff reservation " + i);
        }
        List<Reservation> five = limits.reservations();
        check(limits.reserve("S2", "ITEM6", day, 1, BorrowerCategory.STAFF).equals(
                "Rejected: borrower limit or duration."), "staff sixth rejected in coordinator");
        check(limits.reservations().equals(five), "staff limit preserves records");

        ReservationCoordinator defaultStudent = ReservationApplication.create(new RecordingNotificationSender());
        ReservationCoordinator explicitStudent = ReservationApplication.create(new RecordingNotificationSender());
        check(defaultStudent.reserve("B1", "MIC1", day, 7).equals(
                explicitStudent.reserve("B1", "MIC1", day, 7, BorrowerCategory.STUDENT)),
                "default and explicit student results agree");
        check(defaultStudent.reserve("B2", "TRI1", day, 8).equals(
                "Rejected: borrower limit or duration."), "default remains student");

        // Counts belong to a borrower ID across all records, not separate category buckets.
        ReservationCoordinator mixedFixture = ReservationApplication.create(new RecordingNotificationSender());
        for (int i = 1; i <= 3; i++) {
            mixedFixture.reserve("X1", "ITEM" + i, day, 1);
        }
        check(mixedFixture.reserve("X1", "ITEM4", day, 1, BorrowerCategory.STAFF)
                .startsWith("Confirmed:"), "supplied staff policy uses existing count three");
        check(mixedFixture.reserve("X1", "ITEM5", day, 1, BorrowerCategory.STAFF)
                .startsWith("Confirmed:"), "supplied staff policy uses existing count four");
        check(mixedFixture.reserve("X1", "ITEM6", day, 1, BorrowerCategory.STAFF).equals(
                "Rejected: borrower limit or duration."), "counts not reset by category selection");
        System.out.println("All " + checks + " Chapter 5 checks passed.");
    }

    private static void sharedPolicyContract(BorrowingPolicy policy) {
        check(!policy.mayRequest(-1, 1), "negative count returns false");
        check(!policy.mayRequest(Integer.MIN_VALUE, 1), "minimum count returns false");
        check(!policy.mayRequest(0, 0), "zero duration returns false");
        check(!policy.mayRequest(0, -1), "negative duration returns false");
        check(!policy.mayRequest(0, Integer.MIN_VALUE), "minimum duration returns false");
        check(policy.mayRequest(0, 1), "documented one-day request allowed");
        check(!policy.mayRequest(Integer.MAX_VALUE, 1), "above documented count limits");
        check(!policy.mayRequest(0, Integer.MAX_VALUE), "above documented duration limits");
        boolean first = policy.mayRequest(1, 2);
        policy.mayRequest(0, 1);
        check(policy.mayRequest(1, 2) == first, "repeat decision unchanged by intervening call");
    }

    private static void check(boolean condition, String label) {
        if (!condition) throw new AssertionError(label);
        checks++;
    }

    private static void expect(Class<? extends Throwable> type, Runnable action,
                               String label) {
        try {
            action.run();
        } catch (Throwable error) {
            check(type.isInstance(error), label + ": wrong exception " + error);
            return;
        }
        throw new AssertionError(label + ": expected " + type.getSimpleName());
    }
}
```

### 4.8 `after/src/test/java/Chapter06Checks.java`

```java
import java.io.ByteArrayOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

public final class Chapter06Checks {
    private static int checks;

    public static void main(String[] args) {
        LocalDate day = LocalDate.of(2026, 10, 20);
        RecordingNotificationSender inbox = new RecordingNotificationSender();
        ReservationCoordinator c = ReservationApplication.create(inbox);
        String first = c.reserve("B1", "CAM1", day, 2);
        check(first.equals("Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)."),
                "accepted return unchanged");
        check(inbox.received().size() == 1, "one notification per accepted request");
        check(inbox.received().get(0) == c.reservations().get(0), "accepted record supplied");
        List<Reservation> oldInbox = inbox.received();
        expect(UnsupportedOperationException.class, oldInbox::clear, "inbox snapshot unmodifiable");
        check(c.reserve("B2", "CAM1", day.plusDays(1), 1).equals(
                "Rejected: item unavailable."), "conflict result preserved");
        check(inbox.received().size() == 1, "conflict sends nothing");
        c.reserve("B1", "MIC1", day, 8);
        check(inbox.received().size() == 1, "duration rejection sends nothing");
        expect(IllegalArgumentException.class, () -> c.reserve("", "CAM1", day, 1), "bad ID");
        check(inbox.received().size() == 1, "invalid argument sends nothing");
        c.reserve("B2", "CAM1", day.plusDays(2), 1);
        check(inbox.received().size() == 2, "adjacent acceptance sends once");
        check(oldInbox.size() == 1, "earlier inbox snapshot stable");

        FailingSender failure = new FailingSender();
        ReservationCoordinator failed = ReservationApplication.create(failure);
        String failureResult = failed.reserve("B1", "CAM1", day, 2);
        check(failureResult.equals(first + " Notification failed; reservation retained."),
                "explicit partial-success result");
        check(failed.reservations().size() == 1, "notification failure retains accepted record");
        check(failure.calls == 1, "one attempt and no automatic retry");
        check(failed.reserve("B1", "CAM1", day, 2).equals("Rejected: item unavailable."),
                "retrying reservation is still a conflict");
        check(failure.calls == 1, "conflicting repeat does not attempt notification");

        ReservationCoordinator unexpected = ReservationApplication.create(new BrokenSender());
        expect(IllegalStateException.class, () -> unexpected.reserve("B1", "CAM1", day, 2),
                "unexpected sender failure is not swallowed");
        check(unexpected.reservations().size() == 1, "record is stored before the unexpected failure");

        Map<BorrowerCategory, BorrowingPolicy> configured = policies();
        expect(NullPointerException.class, () -> new ReservationCoordinator(
                null, new ConfirmationFormatter(), inbox), "null policy map");
        expect(IllegalArgumentException.class, () -> new ReservationCoordinator(
                Map.of(BorrowerCategory.STUDENT, new ReservationRules()),
                new ConfirmationFormatter(), inbox), "missing staff policy");
        expect(NullPointerException.class, () -> new ReservationCoordinator(
                configured, null, inbox), "null formatter");
        expect(NullPointerException.class, () -> new ReservationCoordinator(
                configured, new ConfirmationFormatter(), null), "null sender");
        Map<BorrowerCategory, BorrowingPolicy> mutable = new EnumMap<>(configured);
        ReservationCoordinator copied = new ReservationCoordinator(mutable,
                new ConfirmationFormatter(), new RecordingNotificationSender());
        mutable.put(BorrowerCategory.STUDENT, (count, days) -> false);
        check(copied.reserve("B1", "CAM1", day, 1).startsWith("Confirmed:"),
                "caller map mutation cannot rewire coordinator");
        Map<BorrowerCategory, BorrowingPolicy> restrictive = new EnumMap<>(configured);
        restrictive.put(BorrowerCategory.STUDENT, (count, days) -> false);
        RecordingNotificationSender restrictedInbox = new RecordingNotificationSender();
        ReservationCoordinator restricted = new ReservationCoordinator(restrictive,
                new ConfirmationFormatter(), restrictedInbox);
        check(restricted.reserve("B1", "CAM1", day, 1).equals(
                "Rejected: borrower limit or duration."), "injected policy is used");
        check(restrictedInbox.received().isEmpty(), "injected rejection sends nothing");

        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        ConsoleNotificationSender console = new ConsoleNotificationSender(
                new PrintStream(bytes, true, StandardCharsets.UTF_8), new ConfirmationFormatter());
        console.send(c.reservations().get(0));
        check(bytes.toString(StandardCharsets.UTF_8).equals("Notice: " + first + System.lineSeparator()),
                "console implementation uses supplied stream");
        PrintStream brokenOutput = new PrintStream(new OutputStream() {
            @Override public void write(int value) throws IOException {
                throw new IOException("Expected output failure");
            }
        });
        ConsoleNotificationSender brokenConsole = new ConsoleNotificationSender(
                brokenOutput, new ConfirmationFormatter());
        expect(NotificationException.class, () -> brokenConsole.send(c.reservations().get(0)),
                "console reports expected output failure");
        expect(NullPointerException.class, () -> inbox.send(null), "null notice rejected");
        System.out.println("All " + checks + " Chapter 6 checks passed.");
    }

    private static Map<BorrowerCategory, BorrowingPolicy> policies() {
        return Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                      BorrowerCategory.STAFF, new StaffReservationRules());
    }

    private static final class FailingSender implements NotificationSender {
        private int calls;
        @Override public void send(Reservation reservation) {
            calls++;
            throw new NotificationException("Expected teaching failure");
        }
    }

    // A programming defect, not an expected output failure: it must not be swallowed.
    private static final class BrokenSender implements NotificationSender {
        @Override public void send(Reservation reservation) {
            throw new IllegalStateException("Unexpected programming failure");
        }
    }

    private static void check(boolean condition, String label) {
        if (!condition) throw new AssertionError(label);
        checks++;
    }

    private static void expect(Class<? extends Throwable> type, Runnable action, String label) {
        try { action.run(); }
        catch (Throwable error) {
            check(type.isInstance(error), label + ": wrong exception " + error);
            return;
        }
        throw new AssertionError(label + ": expected " + type.getSimpleName());
    }
}
```

### 4.9 `after/src/test/java/DirectoryAdapterTest.java`

```java
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDate;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

class DirectoryAdapterTest {
    private final LocalDate start = LocalDate.of(2026, 10, 20);
    @ParameterizedTest
    @CsvSource({"S,STUDENT", "T,STAFF"})
    void mapsKnownActiveCategories(String code, BorrowerCategory expected) {
        var adapter = new LegacyDirectoryAdapter(id -> new LegacyDirectoryClient.Person(id, code, "Y"));
        assertEquals(new Borrower("B1", expected), adapter.find("B1").orElseThrow());
    }
    @Test void absenceAndInactiveAreEmpty() {
        assertTrue(new LegacyDirectoryAdapter(id -> null).find("B1").isEmpty());
        assertTrue(new LegacyDirectoryAdapter(id -> new LegacyDirectoryClient.Person(id, "S", "N"))
                .find("B1").isEmpty());
    }
    @ParameterizedTest
    @CsvSource({"X,Y", "S,X", "s,Y", "S,y"})
    void unknownCodesAreErrors(String kind, String status) {
        var adapter = new LegacyDirectoryAdapter(id -> new LegacyDirectoryClient.Person(id, kind, status));
        assertThrows(DirectoryException.class, () -> adapter.find("B1"));
    }
    @Test void malformedRowsAreErrors() {
        for (var row : new LegacyDirectoryClient.Person[] {
                new LegacyDirectoryClient.Person("OTHER", "S", "Y"),
                new LegacyDirectoryClient.Person(null, "S", "Y"),
                new LegacyDirectoryClient.Person("B1", null, "Y"),
                new LegacyDirectoryClient.Person("B1", "S", null),
                new LegacyDirectoryClient.Person("B1", "X", "N")}) {
            assertThrows(DirectoryException.class, () -> new LegacyDirectoryAdapter(id -> row).find("B1"));
        }
    }
    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {" "})
    void invalidIdentifierDoesNotReachProvider(String id) {
        var calls = new AtomicInteger();
        var adapter = new LegacyDirectoryAdapter(key -> { calls.incrementAndGet(); return null; });
        assertThrows(IllegalArgumentException.class, () -> adapter.find(id));
        assertEquals(0, calls.get());
    }
    @Test void translatesExpectedFailureAndKeepsCause() {
        var original = new LegacyDirectoryClient.Failure("offline");
        var adapter = new LegacyDirectoryAdapter(id -> { throw original; });
        var result = assertThrows(DirectoryException.class, () -> adapter.find("B1"));
        assertSame(original, result.getCause());
    }
    @Test void unexpectedProgrammingFailureIsNotDisguisedAsAbsence() {
        var original = new IllegalStateException("bug");
        var adapter = new LegacyDirectoryAdapter(id -> { throw original; });
        assertSame(original, assertThrows(IllegalStateException.class, () -> adapter.find("B1")));
    }
    @Test void categoryFromDirectoryControlsReservationPolicy() {
        var notices = new RecordingNotificationSender();
        var coordinator = ReservationApplication.create(notices);
        var directory = new LegacyDirectoryAdapter(id -> new LegacyDirectoryClient.Person(
                id, id.equals("STAFF1") ? "T" : "S", "Y"));
        var service = new DirectoryReservationService(directory, coordinator);
        assertTrue(service.reserve("STAFF1", "CAM1", start, 10).startsWith("Confirmed: R1"));
        assertEquals("Rejected: borrower limit or duration.", service.reserve("STUDENT1", "MIC1", start, 10));
        assertEquals(1, coordinator.reservations().size());
        assertEquals("STAFF1", coordinator.reservations().get(0).borrowerId());
        assertEquals(1, notices.received().size());
    }
    @Test void absenceAndOutageDoNotStoreNotifyOrConsumeId() {
        var notices = new RecordingNotificationSender();
        var coordinator = ReservationApplication.create(notices);
        var missing = new DirectoryReservationService(id -> Optional.empty(), coordinator);
        assertEquals("Rejected: borrower not found or inactive.", missing.reserve("B1", "CAM1", start, 2));
        var failing = new DirectoryReservationService(new LegacyDirectoryAdapter(id -> {
            throw new LegacyDirectoryClient.Failure("offline");
        }), coordinator);
        assertThrows(DirectoryException.class, () -> failing.reserve("B1", "CAM1", start, 2));
        assertTrue(coordinator.reservations().isEmpty());
        assertTrue(notices.received().isEmpty());
        var valid = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.STUDENT)), coordinator);
        assertTrue(valid.reserve("B1", "CAM1", start, 2).startsWith("Confirmed: R1"));
    }
    @Test void mismatchedDomainBorrowerIsRejectedBeforeMutation() {
        var coordinator = ReservationApplication.create(new RecordingNotificationSender());
        var service = new DirectoryReservationService(id -> Optional.of(new Borrower("OTHER", BorrowerCategory.STAFF)), coordinator);
        assertThrows(DirectoryException.class, () -> service.reserve("B1", "CAM1", start, 10));
        assertTrue(coordinator.reservations().isEmpty());
    }
    @Test void localArgumentErrorsPrecedeLookup() {
        var calls = new AtomicInteger();
        var service = new DirectoryReservationService(id -> { calls.incrementAndGet(); return Optional.empty(); },
                ReservationApplication.create(new RecordingNotificationSender()));
        assertThrows(IllegalArgumentException.class, () -> service.reserve("B1", " ", start, 2));
        assertThrows(NullPointerException.class, () -> service.reserve("B1", "CAM1", null, 2));
        assertEquals(0, calls.get());
    }
}
```

### 4.10 `after/src/test/java/LegacyRegressionTest.java`

```java
import org.junit.jupiter.api.Test;

class LegacyRegressionTest {
    @Test void chapter02() { Chapter02Checks.main(new String[0]); }
    @Test void chapter03() { Chapter03AcceptanceExamples.main(new String[0]); }
    @Test void chapter05() { Chapter05Checks.main(new String[0]); }
    @Test void chapter06() { Chapter06Checks.main(new String[0]); }
}
```

### 4.11 `after/src/test/java/LoanServiceTest.java`

```java
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

class LoanServiceTest {
    private final LocalDate start = LocalDate.of(2026, 10, 20);

    private ReservationCoordinator reserved() {
        ReservationCoordinator c = ReservationApplication.create(new RecordingNotificationSender());
        c.reserve("B1", "CAM1", start, 2);
        return c;
    }

    @Test void checkoutAndReturnUseTheSuppliedClock() {
        AdjustableClock clock = new AdjustableClock(Instant.parse("2026-10-20T09:00:00Z"));
        LoanService service = new LoanService(reserved(), clock);
        Loan active = service.checkOut("R1");
        List<Loan> snapshot = service.loans();
        assertThrows(UnsupportedOperationException.class, snapshot::clear);
        assertEquals(start, active.borrowedOn());
        assertTrue(active.active());
        clock.set(Instant.parse("2026-10-21T09:00:00Z"));
        Loan returned = service.returnLoan("R1");
        assertAll(() -> assertFalse(returned.active()),
                () -> assertEquals(start.plusDays(1), returned.returnedOn()),
                () -> assertTrue(snapshot.get(0).active(), "Old immutable snapshot stays active"),
                () -> assertEquals(List.of(returned), service.loans()));
        assertThrows(IllegalStateException.class, () -> service.returnLoan("R1"));
        assertEquals(List.of(returned), service.loans());
    }

    @ParameterizedTest
    @ValueSource(strings = {"2026-10-19T12:00:00Z", "2026-10-22T00:00:00Z"})
    void checkoutOutsideHalfOpenPeriodIsRejected(String instant) {
        LoanService service = new LoanService(reserved(), Clock.fixed(Instant.parse(instant), ZoneOffset.UTC));
        assertThrows(IllegalStateException.class, () -> service.checkOut("R1"));
        assertTrue(service.loans().isEmpty());
    }

    @Test void unknownReservationAndInactiveReturnChangeNothing() {
        LoanService service = new LoanService(reserved(), Clock.fixed(
                Instant.parse("2026-10-20T12:00:00Z"), ZoneOffset.UTC));
        assertThrows(IllegalArgumentException.class, () -> service.checkOut("R99"));
        assertThrows(IllegalStateException.class, () -> service.returnLoan("R1"));
        assertTrue(service.loans().isEmpty());
    }

    @Test void aReservationCannotBeCheckedOutTwiceEvenAfterReturn() {
        LoanService service = new LoanService(reserved(), Clock.fixed(
                Instant.parse("2026-10-20T12:00:00Z"), ZoneOffset.UTC));
        service.checkOut("R1");
        assertThrows(IllegalStateException.class, () -> service.checkOut("R1"));
        service.returnLoan("R1");
        List<Loan> before = service.loans();
        assertThrows(IllegalStateException.class, () -> service.checkOut("R1"));
        assertEquals(before, service.loans());
    }

    @Test void unreturnedItemBlocksTheNextAdjacentReservationUntilReturned() {
        ReservationCoordinator c = reserved();
        c.reserve("B2", "CAM1", start.plusDays(2), 1);
        AdjustableClock clock = new AdjustableClock(Instant.parse("2026-10-20T09:00:00Z"));
        LoanService service = new LoanService(c, clock);
        service.checkOut("R1");
        clock.set(Instant.parse("2026-10-22T09:00:00Z"));
        assertThrows(IllegalStateException.class, () -> service.checkOut("R2"));
        assertEquals(1, service.loans().size());
        service.returnLoan("R1");
        assertTrue(service.checkOut("R2").active());
    }

    @Test void clockZoneDeterminesTheCheckoutDate() {
        Clock local = Clock.fixed(Instant.parse("2026-10-19T22:30:00Z"), ZoneId.of("Asia/Baghdad"));
        LoanService service = new LoanService(reserved(), local);
        assertEquals(start, service.checkOut("R1").borrowedOn());
    }

    @Test void backwardClockCannotRecordReturnBeforeCheckout() {
        AdjustableClock clock = new AdjustableClock(Instant.parse("2026-10-20T09:00:00Z"));
        LoanService service = new LoanService(reserved(), clock);
        service.checkOut("R1");
        List<Loan> before = service.loans();
        clock.set(Instant.parse("2026-10-19T09:00:00Z"));
        assertThrows(IllegalArgumentException.class, () -> service.returnLoan("R1"));
        assertEquals(before, service.loans());
    }

    @Test void returningLoanDoesNotRewriteHistoricalReservationsOrTheirCount() {
        ReservationCoordinator c = reserved();
        LoanService service = new LoanService(c, Clock.fixed(
                Instant.parse("2026-10-20T12:00:00Z"), ZoneOffset.UTC));
        List<Reservation> before = c.reservations();
        service.checkOut("R1");
        service.returnLoan("R1");
        assertEquals(before, c.reservations());
        assertFalse(c.isAvailable("CAM1", start, start.plusDays(1)));
    }

    static final class AdjustableClock extends Clock {
        private final AtomicReference<Instant> now;
        private final ZoneId zone;
        AdjustableClock(Instant instant) { this(new AtomicReference<>(instant), ZoneOffset.UTC); }
        private AdjustableClock(AtomicReference<Instant> now, ZoneId zone) {
            this.now = now; this.zone = zone;
        }
        void set(Instant instant) { now.set(instant); }
        @Override public ZoneId getZone() { return zone; }
        @Override public Clock withZone(ZoneId zone) { return new AdjustableClock(now, zone); }
        @Override public Instant instant() { return now.get(); }
    }
}
```

### 4.12 `after/src/test/java/NotificationMockitoTest.java`

```java
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class NotificationMockitoTest {
    private final LocalDate day = LocalDate.of(2026, 10, 20);

    @Test void acceptedReservationIsSentOnceWithItsDomainDetails() {
        NotificationSender sender = mock(NotificationSender.class);
        ReservationCoordinator c = ReservationApplication.create(sender);
        c.reserve("B1", "CAM1", day, 2);
        ArgumentCaptor<Reservation> captured = ArgumentCaptor.forClass(Reservation.class);
        verify(sender).send(captured.capture());
        Reservation sent = captured.getValue();
        assertAll(() -> assertEquals("R1", sent.id()),
                () -> assertEquals("B1", sent.borrowerId()),
                () -> assertEquals("CAM1", sent.itemId()),
                () -> assertEquals(day, sent.period().start()),
                () -> assertEquals(day.plusDays(2), sent.period().endExclusive()));
    }

    @Test void rejectedDurationDoesNotNotify() {
        NotificationSender sender = mock(NotificationSender.class);
        ReservationCoordinator c = ReservationApplication.create(sender);
        assertEquals("Rejected: borrower limit or duration.", c.reserve("B1", "CAM1", day, 8));
        assertTrue(c.reservations().isEmpty());
        verifyNoInteractions(sender);
    }

    @Test void expectedNotificationFailureRetainsReservationWithoutRetry() {
        NotificationSender sender = mock(NotificationSender.class);
        doThrow(new NotificationException("Expected test failure")).when(sender).send(any(Reservation.class));
        ReservationCoordinator c = ReservationApplication.create(sender);
        assertEquals("Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)."
                + " Notification failed; reservation retained.", c.reserve("B1", "CAM1", day, 2));
        assertEquals(1, c.reservations().size());
        verify(sender, times(1)).send(any(Reservation.class));
    }
}
```

### 4.13 `after/src/test/java/NotificationPublisherTest.java`

```java
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;

class NotificationPublisherTest {
    private Reservation reservation() {
        return new Reservation("R1", "B1", "CAM1", new LoanPeriod(LocalDate.of(2026,10,20), LocalDate.of(2026,10,22)));
    }
    @Test void sendsInRegistrationOrderWithSameImmutableRecord() {
        var publisher = new NotificationPublisher();
        var events = new ArrayList<String>();
        var record = reservation();
        publisher.subscribe(value -> { assertSame(record, value); events.add("desk"); });
        publisher.subscribe(value -> { assertSame(record, value); events.add("audit"); });
        publisher.send(record);
        assertEquals(List.of("desk", "audit"), events);
    }
    @Test void expectedFailuresAreCollectedAndLaterObserversStillRun() {
        var publisher = new NotificationPublisher();
        var events = new ArrayList<String>();
        var first = new NotificationException("first");
        var second = new NotificationException("second");
        publisher.subscribe(value -> { throw first; });
        publisher.subscribe(value -> events.add("middle"));
        publisher.subscribe(value -> { throw second; });
        publisher.subscribe(value -> events.add("last"));
        var failure = assertThrows(NotificationException.class, () -> publisher.send(reservation()));
        assertEquals(List.of("middle", "last"), events);
        assertArrayEquals(new Throwable[] {first, second}, failure.getSuppressed());
    }
    @Test void coordinatorRetainsRecordAndReportsExpectedPartialFailure() {
        var publisher = new NotificationPublisher();
        var events = new ArrayList<String>();
        publisher.subscribe(value -> { throw new NotificationException("offline"); });
        publisher.subscribe(value -> events.add(value.id()));
        var coordinator = ReservationApplication.create(publisher);
        var result = coordinator.reserve("B1", "CAM1", LocalDate.of(2026,10,20), 2);
        assertTrue(result.endsWith("Notification failed; reservation retained."));
        assertEquals(1, coordinator.reservations().size());
        assertEquals(List.of("R1"), events);
    }
    @Test void rejectedReservationPublishesNothing() {
        var publisher = new NotificationPublisher();
        var events = new ArrayList<String>();
        publisher.subscribe(value -> events.add(value.id()));
        var coordinator = ReservationApplication.create(publisher);
        assertEquals("Rejected: borrower limit or duration.", coordinator.reserve("B1", "CAM1", LocalDate.of(2026,10,20), 8));
        assertTrue(events.isEmpty());
    }
    @Test void subscriptionChangesTakeEffectOnNextPublication() {
        var publisher = new NotificationPublisher();
        var events = new ArrayList<String>();
        var second = new AtomicReference<NotificationPublisher.Subscription>();
        var changed = new AtomicBoolean();
        publisher.subscribe(value -> {
            events.add("first");
            if (changed.compareAndSet(false, true)) {
                second.get().close();
                publisher.subscribe(later -> events.add("third"));
            }
        });
        second.set(publisher.subscribe(value -> events.add("second")));
        publisher.send(reservation());
        publisher.send(reservation());
        assertEquals(List.of("first", "second", "first", "third"), events);
    }
    @Test void duplicateIdentityAndOldSubscriptionHandleAreHandled() {
        var publisher = new NotificationPublisher();
        var events = new ArrayList<String>();
        NotificationPublisher.Observer observer = value -> events.add(value.id());
        var old = publisher.subscribe(observer);
        assertThrows(IllegalArgumentException.class, () -> publisher.subscribe(observer));
        old.close();
        publisher.subscribe(observer);
        old.close();
        publisher.send(reservation());
        assertEquals(List.of("R1"), events);
    }
    @Test void unexpectedFailureStopsDispatchAfterReservationWasStored() {
        var publisher = new NotificationPublisher();
        var events = new ArrayList<String>();
        var bug = new IllegalStateException("observer bug");
        publisher.subscribe(value -> events.add("first"));
        publisher.subscribe(value -> { throw bug; });
        publisher.subscribe(value -> events.add("last"));
        var coordinator = ReservationApplication.create(publisher);
        assertSame(bug, assertThrows(IllegalStateException.class,
                () -> coordinator.reserve("B1", "CAM1", LocalDate.of(2026,10,20), 2)));
        assertEquals(List.of("first"), events);
        assertEquals(1, coordinator.reservations().size());
    }
    @Test void guardResetsAfterUnexpectedFailure() {
        var publisher = new NotificationPublisher();
        var bad = publisher.subscribe(value -> { throw new IllegalStateException("bug"); });
        assertThrows(IllegalStateException.class, () -> publisher.send(reservation()));
        bad.close();
        assertDoesNotThrow(() -> publisher.send(reservation()));
    }
    @Test void nestedPublicationIsRejectedAndGuardResets() {
        var publisher = new NotificationPublisher();
        var nested = publisher.subscribe(publisher::send);
        assertThrows(IllegalStateException.class, () -> publisher.send(reservation()));
        nested.close();
        assertDoesNotThrow(() -> publisher.send(reservation()));
    }
    @Test void emptyPublisherAndNullArgumentsHaveExplicitOutcomes() {
        var publisher = new NotificationPublisher();
        assertDoesNotThrow(() -> publisher.send(reservation()));
        assertThrows(NullPointerException.class, () -> publisher.send(null));
        assertThrows(NullPointerException.class, () -> publisher.subscribe(null));
    }
}
```

### 4.14 `after/src/test/java/ReserveEquipmentCommandTest.java`

```java
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDate;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class ReserveEquipmentCommandTest {
    private final LocalDate start = LocalDate.of(2026,10,20);
    @Test void constructionIsLazyAndExecutionUsesTheCapturedRequest() {
        var notices = new RecordingNotificationSender();
        var coordinator = ReservationApplication.create(notices);
        var lookups = new AtomicInteger();
        var service = new DirectoryReservationService(id -> {
            lookups.incrementAndGet();
            return Optional.of(new Borrower(id, BorrowerCategory.STUDENT));
        }, coordinator);
        Command<String> command = new ReserveEquipmentCommand(service, "B1", "CAM1", start, 2);
        assertThrows(NullPointerException.class, () -> new ReserveEquipmentCommand(null, "B1", "CAM1", start, 2));
        assertThrows(IllegalArgumentException.class, () -> new ReserveEquipmentCommand(service, " ", "CAM1", start, 2));
        assertThrows(IllegalArgumentException.class, () -> new ReserveEquipmentCommand(service, "B1", null, start, 2));
        assertThrows(NullPointerException.class, () -> new ReserveEquipmentCommand(service, "B1", "CAM1", null, 2));
        assertEquals(0, lookups.get());
        assertTrue(coordinator.reservations().isEmpty());
        assertTrue(notices.received().isEmpty());
        assertEquals("Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).", command.execute());
        assertEquals(1, lookups.get());
        assertEquals(1, notices.received().size());
    }
    @Test void replayReevaluatesAndDoesNotPromiseTheSameResult() {
        var notices = new RecordingNotificationSender();
        var coordinator = ReservationApplication.create(notices);
        var service = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.STUDENT)), coordinator);
        var command = new ReserveEquipmentCommand(service, "B1", "CAM1", start, 2);
        assertTrue(command.execute().startsWith("Confirmed:"));
        assertEquals("Rejected: item unavailable.", command.execute());
        assertEquals(1, coordinator.reservations().size());
        assertEquals(1, notices.received().size());
    }
    @Test void receiverStateAtExecutionDeterminesTheResult() {
        var coordinator = ReservationApplication.create(new RecordingNotificationSender());
        var service = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.STUDENT)), coordinator);
        var command = new ReserveEquipmentCommand(service, "B1", "CAM1", start, 2);
        coordinator.reserve("OTHER", "CAM1", start, 2);
        assertEquals("Rejected: item unavailable.", command.execute());
        assertEquals(1, coordinator.reservations().size());
    }
    @Test void receiverFailurePropagatesWithoutMutation() {
        var coordinator = ReservationApplication.create(new RecordingNotificationSender());
        var original = new DirectoryException("offline");
        var service = new DirectoryReservationService(id -> { throw original; }, coordinator);
        var command = new ReserveEquipmentCommand(service, "B1", "CAM1", start, 2);
        assertSame(original, assertThrows(DirectoryException.class, command::execute));
        assertTrue(coordinator.reservations().isEmpty());
    }
}
```

### 4.15 `after/src/test/java/behaviour/LifecycleExamplesTest.java`

```java
package behaviour;

import static org.junit.jupiter.api.Assertions.*;
import static behaviour.LifecycleExamples.*;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class LifecycleExamplesTest {
    private enum Action { CONFIRM, CHECK_OUT, RETURN, CANCEL }
    private void act(Lifecycle lifecycle, Action action) {
        switch (action) {
            case CONFIRM -> lifecycle.confirm();
            case CHECK_OUT -> lifecycle.checkOut();
            case RETURN -> lifecycle.returnItem();
            case CANCEL -> lifecycle.cancel();
        }
    }
    private void reach(Lifecycle lifecycle, Status status) {
        switch (status) {
            case REQUESTED -> { }
            case CONFIRMED -> lifecycle.confirm();
            case ON_LOAN -> { lifecycle.confirm(); lifecycle.checkOut(); }
            case RETURNED -> { lifecycle.confirm(); lifecycle.checkOut(); lifecycle.returnItem(); }
            case CANCELLED -> lifecycle.cancel();
        }
    }
    @ParameterizedTest
    @CsvSource({
        "REQUESTED,CONFIRM,CONFIRMED,true", "REQUESTED,CHECK_OUT,REQUESTED,false",
        "REQUESTED,RETURN,REQUESTED,false", "REQUESTED,CANCEL,CANCELLED,true",
        "CONFIRMED,CONFIRM,CONFIRMED,false", "CONFIRMED,CHECK_OUT,ON_LOAN,true",
        "CONFIRMED,RETURN,CONFIRMED,false", "CONFIRMED,CANCEL,CANCELLED,true",
        "ON_LOAN,CONFIRM,ON_LOAN,false", "ON_LOAN,CHECK_OUT,ON_LOAN,false",
        "ON_LOAN,RETURN,RETURNED,true", "ON_LOAN,CANCEL,ON_LOAN,false",
        "RETURNED,CONFIRM,RETURNED,false", "RETURNED,CHECK_OUT,RETURNED,false",
        "RETURNED,RETURN,RETURNED,false", "RETURNED,CANCEL,RETURNED,false",
        "CANCELLED,CONFIRM,CANCELLED,false", "CANCELLED,CHECK_OUT,CANCELLED,false",
        "CANCELLED,RETURN,CANCELLED,false", "CANCELLED,CANCEL,CANCELLED,false"})
    void bothImplementationsMatchTransitionTable(Status from, Action action, Status expected, boolean allowed) {
        for (Lifecycle lifecycle : List.of(new ConditionalReservation(), new StateReservation())) {
            reach(lifecycle, from);
            if (allowed) act(lifecycle, action);
            else assertThrows(IllegalStateException.class, () -> act(lifecycle, action));
            assertEquals(expected, lifecycle.status());
        }
    }
    @Test void stateObjectsDoNotShareReservationProgress() {
        var first = new StateReservation();
        var second = new StateReservation();
        first.confirm();
        first.checkOut();
        assertEquals(Status.ON_LOAN, first.status());
        assertEquals(Status.REQUESTED, second.status());
        second.cancel();
        assertEquals(Status.ON_LOAN, first.status());
    }
}
```

### 4.16 `after/src/test/java/patterns/PatternExamplesTest.java`

```java
package patterns;

import static org.junit.jupiter.api.Assertions.*;
import static patterns.PatternExamples.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class PatternExamplesTest {
    @Test void factoryMethodChangesProductWithoutReplacingWorkflow() {
        ExportJob plain = new PlainJob();
        ExportJob html = new HtmlJob();
        assertEquals("TEXT: A&B", plain.run("A&B"));
        assertEquals("<p>A&amp;B</p>", html.run("A&B"));
        assertThrows(NullPointerException.class, () -> html.run(null));
        assertThrows(NullPointerException.class, () -> plain.run(null));
    }
    @Test void creatorInvokesOverriddenHookOnce() {
        var calls = new AtomicInteger();
        ExportJob job = new ExportJob() {
            protected Exporter createExporter() {
                calls.incrementAndGet();
                return value -> "chosen:" + value;
            }
        };
        assertEquals("chosen:R1", job.run("R1"));
        assertEquals(1, calls.get());
    }
    @Test void simpleFactoryCanProduceSameOutputs() {
        assertEquals("TEXT: R1", simpleExporter(false).export("R1"));
        assertEquals("<p>&lt;R1&gt;</p>", simpleExporter(true).export("<R1>"));
    }
    @Test void abstractFactorySuppliesBothProductsInEachFamily() {
        assertEquals("Loan\nR1\n", receipt(new PlainFamily(), "Loan", "R1"));
        assertEquals("<h1>Loan</h1><p>&lt;R1&gt;</p>", receipt(new HtmlFamily(), "Loan", "<R1>"));
    }
    @Test void builderDefaultsAndExplicitOptions() {
        var minimal = ReportRequest.forBorrower("B1").build();
        assertFalse(minimal.includeReturned());
        assertNull(minimal.from());
        assertTrue(minimal.columns().isEmpty());
        var from = LocalDate.of(2026, 10, 20);
        var full = ReportRequest.forBorrower("B1").during(from, from.plusDays(2))
                .includeReturned(true).column("item").build();
        assertEquals("B1", full.borrowerId());
        assertEquals(from, full.from());
        assertEquals(from.plusDays(2), full.toExclusive());
        assertTrue(full.includeReturned());
        assertEquals(List.of("item"), full.columns());
    }
    @Test void builtValueIsIndependentOfReusableBuilder() {
        var builder = ReportRequest.forBorrower("B1").column("item");
        var first = builder.build();
        builder.column("date");
        assertEquals(List.of("item"), first.columns());
        assertEquals(List.of("item", "date"), builder.build().columns());
        assertThrows(UnsupportedOperationException.class, () -> first.columns().add("other"));
    }
    @Test void builderRejectsInvalidConfiguration() {
        var date = LocalDate.of(2026, 10, 20);
        assertThrows(IllegalArgumentException.class, () -> ReportRequest.forBorrower(" "));
        assertThrows(IllegalArgumentException.class, () -> ReportRequest.forBorrower("B1").during(date, date).build());
        assertThrows(IllegalArgumentException.class, () -> ReportRequest.forBorrower("B1").during(date, date.minusDays(1)).build());
        assertThrows(NullPointerException.class, () -> ReportRequest.forBorrower("B1").during(date, null));
        assertThrows(IllegalArgumentException.class, () -> ReportRequest.forBorrower("B1").column(" "));
    }
    @Test void auditOutsideRetryObservesOneLogicalCall() {
        var calls = new AtomicInteger();
        Sender flaky = message -> { if (calls.incrementAndGet() == 1) throw new DeliveryFailure("first"); };
        var events = new ArrayList<String>();
        new AuditedSender(new RetryOnceSender(flaky), events).send("R1");
        assertEquals(2, calls.get());
        assertEquals(List.of("attempt", "sent"), events);
    }
    @Test void retryOutsideAuditObservesEachAttempt() {
        var calls = new AtomicInteger();
        Sender flaky = message -> { if (calls.incrementAndGet() == 1) throw new DeliveryFailure("first"); };
        var events = new ArrayList<String>();
        new RetryOnceSender(new AuditedSender(flaky, events)).send("R1");
        assertEquals(2, calls.get());
        assertEquals(List.of("attempt", "failed", "attempt", "sent"), events);
    }
    @Test void secondExpectedFailurePropagatesWithoutThirdAttempt() {
        var calls = new AtomicInteger();
        var original = new DeliveryFailure("still offline");
        Sender failing = message -> { calls.incrementAndGet(); throw original; };
        assertSame(original, assertThrows(DeliveryFailure.class, () -> new RetryOnceSender(failing).send("R1")));
        assertEquals(2, calls.get());
    }
    @Test void unexpectedFailureIsNotRetried() {
        var calls = new AtomicInteger();
        var original = new IllegalArgumentException("bad message");
        Sender failing = message -> { calls.incrementAndGet(); throw original; };
        assertSame(original, assertThrows(IllegalArgumentException.class, () -> new RetryOnceSender(failing).send("R1")));
        assertEquals(1, calls.get());
    }
}
```

## 5. Build and supporting files

Dependency and plugin versions are unchanged; Mockito remains necessary for inherited tests.

### 5.1 `after/pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>edu.se506</groupId>
  <artifactId>equipment-lending</artifactId>
  <version>0.9.0</version>
  <properties>
    <maven.compiler.release>17</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.13.4</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-core</artifactId>
      <version>5.20.0</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.14.1</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.4</version>
        <configuration><failIfNoTests>true</failIfNoTests></configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

### 5.2 `after/src/test/resources/mockito-extensions/org.mockito.plugins.MockMaker`

```text
mock-maker-proxy
```

### 5.3 `after/scripts/check.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
"${CHAPTER_MVN:-mvn}" --batch-mode verify
```

### 5.4 `after/.gitignore`

```text
/target/
/build/
*.class
```

### 5.4a `after/.gitattributes`

```gitattributes
*.sh text eol=lf
```

This is the Chapter 4 file that keeps `scripts/check.sh` in LF form when Git on Windows converts line endings. Without it, a CRLF copy of the script fails under WSL or Linux bash.

### 5.5 `after/README.md`

````markdown
# Chapter 9 checkpoint

Java 17; Maven 3.9.11. Existing JUnit, Mockito and plugin versions remain pinned in pom.xml.

From this directory:

```bash
mvn --batch-mode verify
java -cp target/classes Chapter09Demo
java -cp target/classes Chapter08Demo
java -cp target/classes Chapter07Demo
```

The complete build executes 107 JUnit invocations: 63 inherited, nine Strategy cases, 21 lifecycle cases, ten publisher tests and four Command tests. Four inherited cases wrap the older plain-Java runners.

NotificationPublisher is an optional sequential, local sender implementation. It snapshots subscriptions, preserves registration order, continues after expected NotificationException failures, and propagates unexpected exceptions immediately. It has no retry or durable delivery. Chapter09Demo chooses it explicitly; older demonstrations are unchanged.

Command and ReserveEquipmentCommand demonstrate a captured request calling the existing directory-backed service. Constructing a command does not execute the request.

The behaviour package holds a separate proposed lifecycle, with conditional and State implementations checked against the same transition table. It does not change cumulative reservation counts, availability, cancellation or loan behaviour. The existing borrowing policies already demonstrate Strategy.

All Chapter 8 application and test sources are unchanged. The cumulative system remains sequential and in memory, with no authentication or actual university directory client. The patterns package from Chapter 8 is retained as isolated teaching material.
````

## 6. Worked traces and evidence mapping

### 6.1 Strategy: what varies and what remains fixed

The default application assembly supplies one student strategy and one staff strategy. The coordinator obtains the selected category's strategy and asks `mayRequest(activeCount, requestedDays)`. It still validates identifiers, counts existing records, detects conflicts and sends the acceptance notice.

`BehaviourStrategyTest` contains eight parameter rows with independent expected decisions. The values include a student at two records requesting seven days, a student already at three, and staff at four records requesting fourteen days. Negative counts, zero duration and excessive duration are also represented.

The ninth test supplies the temporary staff strategy. Its first three-day request is rejected before storage; a two-day request becomes R1; another request for the same staff borrower is rejected by the one-record maximum. A student's separate seven-day request still succeeds under the unchanged student strategy. This trace shows a configuration change with no edit to coordinator logic.

For this particular count/duration problem, one `LimitPolicy(maxCount, maxDays)` could be a valid alternative. It would replace duplicated arithmetic with data while retaining the interface. Choose separate algorithms only when their behaviour has a reason to vary independently. The current chapter recognises the existing structure rather than adding a class solely to make the pattern visible.

### 6.2 State: the before/after comparison

Both lifecycle implementations expose the same five observations/operations: `status`, `confirm`, `checkOut`, `returnItem` and `cancel`. The starting conditional class selects behaviour inside each operation. The completed class selects behaviour through its current `Phase` object.

For REQUESTED then confirm, both end CONFIRMED. For CONFIRMED then cancel, both end CANCELLED. For ON_LOAN then cancel, both throw and remain ON_LOAN. These examples come from the reviewed table, not from reading what either implementation happens to do.

Each of the 20 parameter rows constructs fresh contexts, reaches the specified starting status using public operations, applies one action and checks the expected result. The same row checks both implementations, but it is still one JUnit invocation. The separate independence test brings the new lifecycle total to 21 invocations.

The `Phase` constants contain no mutable reservation fields. The context assigns `phase = phase.operation()` only after a successful return. Unsupported actions throw before assignment. A state implementation that mutates unrelated external storage before throwing would need additional protection; this exercise has no such side effects.

### 6.3 Observer: partial success and retained failures

The demonstration registers desk, failing display and audit observers. The accepted reservation is stored before publication. Desk records R1; display throws an expected failure; audit still records R1. The publisher then throws an aggregate failure, which the coordinator handles using its existing “reservation retained” message.

For direct publisher diagnostics, `expectedFailuresAreCollectedAndLaterObserversStillRun` registers two expected failures interleaved with successful observers. The aggregate's suppressed exceptions contain the two original exception objects in dispatch order. This preserves their details without discarding later callback attempts.

The coordinator currently returns only its established confirmation string and suffix. It does not expose the aggregate or implement an operational diagnostics service. That limitation should be explicit if the example is proposed for a real application.

Unexpected errors follow a different path. The relevant test runs one successful observer, then an observer throwing `IllegalStateException`, then a final observer. The exception propagates; only the first event is recorded; the reservation still exists. The implementation does not pretend to roll back either the reservation or the successful earlier callback.

### 6.4 Observer lifetime and the snapshot rule

During the first publication in `subscriptionChangesTakeEffectOnNextPublication`, the first observer removes the second and adds a third. The snapshot already includes the second, so it still runs. The next publication observes the updated registrations. The complete history is:

```text
first, second, first, third
```

The snapshot rule is a declared contract, not an incidental result of ArrayList iteration. Iterating a mutable list directly would make callback-time changes unsafe or ambiguous.

The registration entry object also matters. An old subscription is closed, the same observer object is registered again, and the old handle is closed a second time. The newer registration survives because the handles refer to different entry objects. An implementation that removed by observer identity on every close could incorrectly remove that new registration.

The same observer reference cannot be concurrently registered twice in this sequential model. Creating two separate but equivalent callbacks is still possible; there is no domain-recipient deduplication. Subscription ownership and delivery semantics should not be confused.

### 6.5 Command: three moments to inspect

**Construction:** the record receives its receiver and arguments. No directory lookup or notification happens. The constructor rejects missing required values, but does not decide borrowing eligibility.

**Execution:** the directory-backed service obtains the category and the coordinator applies current count/duration and conflict rules. If another reservation appeared after construction, the command can now be rejected.

**Repeated execution:** the same command is invoked again. In the supplied example, the previously stored reservation causes a conflict and the result differs from the first execution. One record and one notice remain. This is re-evaluation through the receiver, not cached completion or an idempotency protocol.

The receiver-failure test keeps the same thrown `DirectoryException` object and verifies no reservation was created. The command adds no catch block that would hide that outcome.

### 6.6 Evidence map

| Behaviour | New test evidence |
|---|---|
| Independent strategy boundary decisions | Eight rows of `strategiesAndConditionalMatchIndependentExamples` |
| Alternate policy without coordinator edits | `injectedPolicyChangesDecisionWithoutChangingCoordinator` |
| Every selected lifecycle status/action combination | Twenty rows of `bothImplementationsMatchTransitionTable` |
| Independent context progress | `stateObjectsDoNotShareReservationProgress` |
| Observer order and immutable shared event | `sendsInRegistrationOrderWithSameImmutableRecord` |
| Continue after expected failures; retain originals | `expectedFailuresAreCollectedAndLaterObserversStillRun` |
| Coordinator keeps acceptance after expected failure | `coordinatorRetainsRecordAndReportsExpectedPartialFailure` |
| No publication after reservation rejection | `rejectedReservationPublishesNothing` |
| Callback-time registration changes | `subscriptionChangesTakeEffectOnNextPublication` |
| Duplicate observer and old handle behaviour | `duplicateIdentityAndOldSubscriptionHandleAreHandled` |
| Unexpected failure has partial effects | `unexpectedFailureStopsDispatchAfterReservationWasStored` |
| Guard recovery and nested publication | The two guard tests in `NotificationPublisherTest` |
| Empty publication and invalid arguments | `emptyPublisherAndNullArgumentsHaveExplicitOutcomes` |
| Lazy command and captured parameters | `constructionIsLazyAndExecutionUsesTheCapturedRequest` |
| Replay and changed receiver state | The two execution-state tests in `ReserveEquipmentCommandTest` |
| Unhidden receiver failure | `receiverFailurePropagatesWithoutMutation` |

## 7. Intentionally wrong alternatives for diagnosis

These are **deliberately incorrect fragments or proposals**, not extra source files for the active build. If experimenting, use a disposable copy and restore the correct source before the full gate. Version 1.0 only predicted which tests would reject these alternatives. In version 1.1, the cancel-on-loan alternative (7.2) and the stop-on-first-failure alternative (7.3) were applied and run, and both were rejected by the tests named below. The setter in 7.1 cannot be rejected by a runtime test, as explained there.

### 7.1 Invalid lifecycle jump

```java
// WRONG as a public escape hatch around reviewed transitions:
public void setStatus(Status requestedStatus) {
    status = requestedStatus;
}
```

A caller can move directly from REQUESTED to RETURNED or resurrect a CANCELLED record. Hiding the status behind a setter still leaves the invariant unenforced. Remove the setter and expose reviewed operations. Tests should attempt checkout before confirmation, cancellation while on loan and repeated return, verifying both the exception and unchanged status.

The final State implementation does not expose a setter at all. Its private phase changes through state operations. Compile-time API review therefore complements runtime transition tests.

### 7.2 Incorrect terminal transition

```java
// WRONG proposed State behaviour: permits cancelling equipment already on loan.
@Override Phase cancel() { return CANCELLED; }
```

If added to ON_LOAN, this contradicts the ON_LOAN/CANCEL row. The existing table expects an exception and ON_LOAN afterwards. Changing the expected result to CANCELLED would be a requirement change, not a repair to the test.

### 7.3 Stop on the first expected observer failure

```java
// WRONG for the selected continuation contract:
for (Entry entry : List.copyOf(entries)) {
    entry.observer.onConfirmed(reservation);
}
```

This can be a valid publisher design under a different fail-fast contract, but it is incorrect here because an expected failure prevents later observers from running. The continuation test expects the middle and last callbacks and both original expected failures. State the intended failure policy before judging the structure.

### 7.4 Reserve while constructing the command

```java
// WRONG inside the request constructor for this chapter's lazy-action contract:
receiver.reserve(borrowerId, itemId, start, days);
```

This performs lookup and side effects before `execute`. The lazy-construction test checks that there are no lookups, records or notices at that point. A command constructor should capture the request; the receiver performs the use case on execution.

## 8. Practical activity solution and design reasoning

### 8.1 Suggested State refactoring sequence

Begin with the complete transition table and `ConditionalReservation`. Run the table tests to establish what is being preserved. Introduce private State objects that implement the four operations, supplying rejection by default and overrides only for permitted transitions. Make the context delegate to its current state and accept a returned successor only on success.

Run the same table against both implementations. Add the independent-context check to guard against placing progress inside shared state objects. Inspect the public API for a setter that could bypass transitions. Keep the before implementation available for comparison rather than describing an unrecorded refactoring history as a completed TDD sequence.

The supplied files embody this before/after design comparison. The author's process is ordinary implementation and verification; it is not presented as a recorded red–green–refactor history.

A reasoned conclusion may still favour the conditional design for the small model. The exercise demonstrates State and its costs; it does not prove that every five-state workflow needs state objects.

### 8.2 A second decision: adopt Observer selectively

**Problem:** several local components need independent reactions after a reservation is accepted, and their registrations can change. Embedding every recipient in the coordinator would mix reservation decisions with the recipient set.

**Solution:** an optional publisher implements the existing sender interface. It owns ordered subscription snapshots, invokes callbacks and applies the declared expected-failure continuation rule. The demonstration supplies it explicitly to the usual application assembly.

**Consequences:** the coordinator remains independent of observer identities. Publication can have partial effects, observers require lifetime management, and unexpected failures still escape after storage. This does not provide durable delivery, rollback or real audit persistence.

**Simpler alternative:** retain one directly injected sender for a single fixed output. If several mandatory steps form one business operation, consider explicit orchestration rather than hiding the sequence in observer registration.

**Revisit when:** actual durability, concurrency or recipient-lifecycle requirements are agreed. Do not turn the classroom publisher into broker infrastructure by assumption.

### 8.3 Decline a pattern with a concrete reason

A direct reservation button handler can call the service if it has no need to carry the request separately. Introducing Command adds a type without a demonstrated benefit in that case. If a UI invoker must receive different actions through one contract, a command or lambda can become useful.

Likewise, one count/duration formula parameterised by two limits may be sufficient for borrowing policies. Separate Strategy classes are useful when rules deserve independent implementations, but parameterisation can be the simpler solution when only values differ.

Explain which change each alternative makes easier and which obligation it adds. Naming the alternatives is insufficient without a decision about the actual requirement.

### 8.4 Optional real cancellation proposal

Before integrating the lifecycle exercise, clarify whether cancellation is allowed after confirmation, how it changes availability and borrower counts, whether it affects an active loan, and what should happen to existing notifications. Define identifier retention and audit/history requirements. Decide whether repeated cancellation is rejected or treated as an idempotent acknowledgement.

Then map those choices to `ReservationCoordinator`, `LoanService`, snapshots, count calculations, availability checks and tests. The current size-based identifier allocation assumes records are not removed. Deleting a cancelled reservation without revisiting identifiers could therefore introduce another defect.

This proposal is an analysis exercise. The provided checkpoint implements none of those lifecycle changes, so all earlier reservation and loan rules remain testable as before.

## 9. AI activity solution

### 9.1 Compare the two lifecycle proposals

Proposal A exposes policy selection to callers without a transition authority. A caller can choose the returned policy even when no checkout occurred. Labelling the classes strategies does not solve the requirement about legal histories.

Proposal B places the current phase in the context and restricts changes to reviewed actions. It is the stronger match for this lifecycle, provided its actual implementation rejects invalid transitions and preserves state after failure. Its more appropriate wording is not sufficient evidence; use the table and API inspection.

For category-based count/duration decisions, the pressure changes. Student and staff are selected policies, not stages through which a reservation progresses. Strategy or a parameterised policy fits that requirement without inventing transitions between borrower categories.

### 9.2 Reliability claim

Observer does not guarantee that every callback completes. The expected-failure policy continues after declared failures but still reports partial success. An unexpected failure stops later callbacks. Snapshot iteration and one attempt per entry do not establish durable or exactly-once delivery.

Command does not make replay safe. Repeated execution re-enters the receiver and can produce a different result or additional effects in other use cases. The supplied conflict check happens to stop a second identical booking, but it is not a general deduplication mechanism. Undo and compensation need separate agreed semantics.

### 9.3 Evidence to retain

For each AI claim, record the relevant requirement, the claimed structure, the confirming or rejecting test, and any remaining limitation. A useful entry is: “Model claims cancellation is legal from any state; transition table forbids ON_LOAN/CANCEL; test requires an exception and unchanged ON_LOAN; proposal rejected.”

The provided fixture is author-written fictional text. Do not report it as an actual response from an AI provider. If conducting a live activity, keep the relevant real output and verify it independently using synthetic data.

## 10. Review answers and transfer solution

### 10.1 Concept answers

**1. Strategy versus State:** category determines which count/duration policy to apply; that choice does not itself advance the reservation lifecycle. State makes the meaning or legality of an operation depend on the context's current position and permitted next positions. Similar delegation structures can serve different purposes.

**2. Shared states, separate progress:** the enum constants contain only behaviour and a fixed status value. Each reservation context owns its current reference. Putting mutable reservation data in a shared constant would couple contexts. The independence test advances one context and observes the other still at REQUESTED.

**3. Snapshot removal:** an observer present when publication begins still receives that publication even if a prior callback closes its subscription. It is absent from the next snapshot. This rule is explicit; a different dispatch design could choose different semantics but would need different tests.

**4. Captured command:** it stores the receiver and request arguments, not a snapshot of receiver state or an advance permission to reserve. Lookup, eligibility and conflicts are evaluated when `execute` calls the service. Construction performs no use-case side effect.

### 10.2 Applied diagnosis answers

**5. Unexpected observer failure:** the coordinator stores before publishing. Earlier callbacks may have completed, so the thrown exception is compatible with a stored reservation and partial external effects. In this local model inspect the reservation snapshot and known event history before choosing recovery. Do not blindly repeat on the assumption that nothing happened; the repeated call may reject while earlier effects remain. A real application would need a reviewed way to identify the original operation and its outcome.

**6. Unrestricted setter:** it permits state changes that bypass the transition table. Remove or tightly control that mutation path. Check REQUESTED/check-out, CONFIRMED/return, ON_LOAN/cancel and repeated return; each rejected action must preserve status. Add valid sequences and independent contexts so the implementation cannot satisfy negative cases merely by rejecting everything. API inspection must also confirm that callers cannot force a terminal status directly.

### 10.3 Document-workflow transfer

A department-specific review algorithm is a Strategy candidate if its contract is stable and different implementations are needed. Draft/approved/published behaviour is a State candidate if actions and transitions depend on lifecycle position. Local views reacting to publication may use Observer. A UI-held publish request may use Command if the request needs a separate representation.

Do not require all four. A small transition table can stay conditional, one fixed view can be a direct call, and a single immediate action can invoke the service directly.

One possible invalid transition is publishing a draft before approval. It must leave the document a draft. Clarify whether revisions invalidate approval before implementing the rule. One observer failure case is a local preview failing after publication state was stored; decide whether remaining observers still run and what the caller sees. One stale-command case is a publish request captured while approved but executed after an edit returns the document to draft; the receiver must check the current state and reject if approval is now required.

Clarify who can approve, whether a published document can be withdrawn, how review policy is selected, and whether notifications are informational or mandatory steps. Those decisions come before selecting classes.

## 11. Instructor guidance and critical reading

Use the existing policy code to show that a design can have a pattern role before anyone gives it that label. Compare it with the conditional fixture and ask when parameterisation would be simpler. Then put the lifecycle table before both implementations and trace one legal and one illegal action.

For Observer, predict the demonstration transcript first. Ask whether the failed display means the desk and audit also failed, and whether the reservation exists. Run the unexpected-failure test as a contrasting declared behaviour, not as a claim that the system automatically recovers.

For Command, pause after construction and inspect the empty state. Execute once, then repeat. Ask students to separate the captured arguments from the evolving receiver state. Do not introduce queue infrastructure or CQRS to make the example appear more sophisticated.

The module descriptor places the critical book review in Week 8. Refer students to the module leader's approved reading list and submission instructions. The student chapter refers to Appendix E, which is not yet written, and includes a short reading checkpoint that works without it. The review's own requirements (length, additional sources, reflection on AI-enabled systems) are in the current assignment brief, and the chapter points to that brief and does not restate it.

A review should identify an actual author claim, locate it precisely, examine the example and evaluate a limitation or alternative using verified evidence. An AI summary of an unread book is not source-based critical reading. This guidance adds no marking rubric, weight or new deadline.

## 12. Verification record

**Version 1.0 (12 October 2026)** was run on OpenJDK 17.0.20 with Maven 3.9.11 and the pinned dependencies in Section 5. That run was not repeated. Verification covers the supplied implementation and examples, not a claimed test-first history or independent review.

**Version 1.1 (13 October 2026)** was re-verified offline on Windows 11 with **Maven 3.9.16 and JDK 24.0.2** (compiling with `--release 17`) and the dependency versions already in the local Maven cache: JUnit Jupiter 6.0.3, Mockito 5.23.0 (with ByteBuddy 1.18.11), Compiler Plugin 3.15.0 and Surefire 3.5.6. **The pinned versions in the POM were not run in this first pass**, because they were not cached and nothing had been downloaded. All 53 listings were extracted programmatically from this file. The results of the first pass verify the code, tests and configuration files, not the exact pins.

**Exact-configuration run (13 October 2026).** The unmodified POM from this file was run with **Maven 3.9.11** (downloaded from Maven Central and checked against its published SHA-512) on **JDK 24.0.2** (`--release 17`), against a clean local repository, so that nothing already cached could stand in for a pinned version. The versions that ran were JUnit Jupiter 5.13.4, Mockito 5.20.0 (which brought ByteBuddy 1.17.7), Compiler Plugin 3.14.1 and Surefire 3.5.4, plus the plugins that Maven 3.9.11 binds by default (Resources 3.3.1 and JAR 3.4.1). `mvn verify` exited 0 with 107 tests and no failures; the four plain-Java runners reported 34, 5, 44 and 28 as before. **Still not verified:** behaviour on a Java 17 runtime (no JDK 17 was available) and a hosted CI run. The fault experiments in this file were run in the earlier pass and were not repeated under the exact configuration.

| Observation (version 1.1) | Result |
|---|---|
| `mvn -o verify` | Exit 0; 107 tests, 0 failures (63 inherited, 44 new: 9 Strategy, 21 lifecycle, 10 publisher, 4 command) |
| Chapter 9 demonstration | Output matched Section 1.2 |
| Files against the current Chapter 8 | Identical apart from eight stale embedded copies in version 1.0 (`DirectoryException`, `LegacyDirectoryClient`, `NotificationException`, `PatternExamples` and its test, the acceptance listing, `Chapter06Checks` with 26 checks, and `LoanServiceTest`) and the missing `.gitattributes`; all refreshed or added in 1.1 |
| `javac -Xlint:all` on all main sources | Version 1.0 gave four `[serial]` warnings from the stale copies; the build is now warning-free |
| Mermaid diagrams | The state diagram, the lifecycle class diagram and the sequence diagram rendered without error with Mermaid 10.9.1 |

**Do the tests detect faults?** Eighteen faults were introduced one at a time into copies of the project, and each copy was run through `mvn test`. With version 1.0's tests, sixteen were caught and two survived. Version 1.1 closes both gaps by strengthening an existing test, so all eighteen are now caught, and the invocation count stays at 107.

| Area | Faults tried | Result |
|---|---|---|
| Observer | No snapshot (live iteration); no reentrancy guard; guard never reset; stop at the first expected failure (7.3); unexpected failures swallowed; duplicate registration allowed; an old handle removing a newer registration; suppressed failures dropped; reverse dispatch order; null reservation accepted | All ten caught by `NotificationPublisherTest` |
| Command | Reserves while constructing (7.4); borrower and item swapped | Both caught |
| Command | **Construction validation removed** | **Survived in 1.0**: no test constructed a command with a blank identifier, a null receiver or a null start date. Caught in 1.1 |
| Command | **Executes with one extra day** | **Survived in 1.0**: the first test checked only that the confirmation `startsWith("Confirmed: R1 for B1 on CAM1")`, which is true for any duration. Caught in 1.1 by asserting the exact confirmation, period included |
| Lifecycle | On-loan reservation may be cancelled (7.2, in State and in the conditional); a returned reservation may be cancelled; progress shared between contexts | All four caught by the transition table and the independence test |

For Observer, all ten selected faults, including the subtle ones about handle ownership and the guard, were caught. That is an observation about these ten faults only; the fault sets in different chapters differ, so the results do not rank the quality of one chapter's tests against another's. The two Command gaps were the same kind of weakness as earlier survivors: a claim made in prose that no assertion checks.

| Check | Observed result |
|---|---|
| Complete Maven verify | Exit 0; 107 JUnit invocations; no failures, errors or skipped cases |
| Inherited Chapter 8 suite | 63 invocations retained and passed |
| New Strategy examples | Nine invocations passed |
| Lifecycle comparison and isolation | Twenty table rows plus one independence test passed |
| Publisher behaviours | Ten tests passed |
| Command behaviours | Four tests passed |
| Source preservation | All earlier main and test sources unchanged |
| Chapter 9 demonstration | Output matched Section 1.2 |
| Markdown reconstruction | All 53 listings matched source; reconstructed build passed all 107 invocations; Chapter 9 transcript matched and Chapters 7–8 demos were unchanged |
| Hosted CI, real provider/delivery and independent peer review | Not performed or claimed |

Each lifecycle table row exercises both implementations, but it remains one reported parameterised test invocation. Four inherited JUnit cases invoke earlier plain-Java runners whose own counts remain distinct: 34 Chapter 2 checks, five Chapter 3 example groups, 44 Chapter 5 checks and 28 Chapter 6 checks.

The table does not establish concurrent safety, durable event delivery, authentication, transactionality or arbitrary command replay safety. One acceptance condition cannot be checked by a runtime test: that the State example has no public setter. That is established by reading the API, as Section 7.1 says, and a reflection test for it would be brittle.

The Mockito dynamic-agent warning described in Chapter 7 also appears in this project's log on JDK 24. It does not affect results, and `-DargLine=-XX:+EnableDynamicAgentLoading` removes it.

## References

Sources checked 12 and 13 October 2026. The student chapter provides the bibliographic distinction and the wider reading context.

1. Gamma, E., Helm, R., Johnson, R. and Vlissides, J., *Design Patterns: Elements of Reusable Object-Oriented Software*. [Publisher catalogue](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-software-9780201633610).
2. Oracle, [Java SE 17 PropertyChangeSupport](https://docs.oracle.com/en/java/javase/17/docs/api/java.desktop/java/beans/PropertyChangeSupport.html), [Throwable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Throwable.html), and [Runnable](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Runnable.html).
3. JUnit Team, [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/).
4. Martin, R. C. (2002), *Agile Software Development: Principles, Patterns, and Practices*, Prentice Hall. The module's required text; the Week 8 reading is its Strategy, Command, Observer and State chapters. Publication details as listed in the module descriptor.
