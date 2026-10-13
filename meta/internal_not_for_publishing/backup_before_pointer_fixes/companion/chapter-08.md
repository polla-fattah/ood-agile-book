---
title: "Chapter 8 Companion: Code, Explanations and Solutions"
weight: 80
---

*Creating and Connecting Objects*  
*OO Development and Agile Practices*

## 1. Scope, starting point and execution

This file accompanies `Chapter_08_Creating_and_Connecting_Objects.md`. It contains a complete reconstructable Maven checkpoint, explanations of the added code, focused tests, model answers and instructor guidance.

**Starting point:** Chapter 7's completed project. Its application classes and tests remain unchanged. **Cumulative addition:** a directory-backed reservation entry point that translates synthetic provider records before calling the existing coordinator. **Separate examples:** the `patterns` package demonstrates Factory Method, Abstract Factory, a fluent Builder and ordered Decorators. Those examples are compiled and tested but are not connected to the lending application.

### 1.1 Reconstruct the complete checkpoint

Create a directory named `after`. Copy the contents of each labelled file listing to the indicated path, preserving case and creating intermediate directories. Sections 3–5 contain every application, test, build and documentation file. Do not copy Markdown fence markers. The README listing uses four backticks because its content includes ordinary fenced commands.

Alternatively, copy Chapter 7's completed `after` directory and add the eight new main-source files and two new test files listed in Section 2. Replace `pom.xml` and `README.md` with this checkpoint's versions. Existing sources, test resources and the check script are unchanged. The Maven project version becomes 0.8.0; dependency versions do not change.

| Tool | Configuration |
|---|---|
| Java | Java 17 language/API target |
| Maven | 3.9.11 used for verification |
| JUnit Jupiter | 5.13.4 |
| Mockito | 5.20.0; retained Chapter 7 interface-proxy configuration |
| Compiler Plugin | 3.14.1; release 17 |
| Surefire Plugin | 3.5.4; fail if no tests are discovered |

With a normal Java 17 JDK and Maven installed, run from `after`:

```bash
mvn --batch-mode verify
java -cp target/classes Chapter08Demo
```

Run the two new test classes alone when examining the examples:

```bash
mvn --batch-mode -Dtest=DirectoryAdapterTest,PatternExamplesTest test
```

The isolated pattern class has no `main` method; its JUnit tests are the executable demonstrations. The existing Bash command `bash scripts/check.sh` still runs the complete Maven gate. The first build requires dependency downloads; later offline execution depends on the required artifacts being cached.

The Chapter 8 demo's exact output is:

```text
Confirmed: R1 for B2 on CAM1 [2026-10-20, 2026-10-30).
Rejected: borrower limit or duration.
Rejected: borrower not found or inactive.
Reservations: 1
Notices: 1
```

The staff fixture B2 is allowed ten days under the inherited staff rule. Student B1's ten-day request is rejected. The missing identifier also creates no record. Only the accepted request creates a notice. These outcomes use a map-backed provider fixture, not real directory access.

## 2. Read the design before the listings

### 2.1 What changed

| New file | Responsibility | Cumulative? |
|---|---|---|
| `Borrower.java` | Immutable application identifier/category value | Yes |
| `BorrowerDirectory.java` | Application-owned presence/absence lookup contract | Yes |
| `DirectoryException.java` | Identifiable directory failure or malformed data | Yes |
| `LegacyDirectoryClient.java` | Illustrative provider contract and raw record | Yes, as a synthetic boundary model |
| `LegacyDirectoryAdapter.java` | Translate provider codes, null and declared failure | Yes |
| `DirectoryReservationService.java` | Look up borrower, then invoke existing reservation behaviour | Yes |
| `Chapter08Demo.java` | Reproducible map-backed integration demonstration | Yes |
| `patterns/PatternExamples.java` | Four separate pattern exercises | No application wiring |
| `DirectoryAdapterTest.java` | Translation and application-boundary tests | Test source |
| `patterns/PatternExamplesTest.java` | Construction, immutability and decorator-order tests | Test source |

The main application's earlier classes stay in the unnamed package to preserve the existing checkpoint. The isolated examples use the named `patterns` package and depend only on Java APIs. They do not import the unnamed-package application classes. Package and layer restructuring is deferred to Chapter 10.

### 2.2 Adapter contract and error precedence

`LegacyDirectoryAdapter` accepts a nonblank identifier. It invokes the provider once and translates only its declared `Failure`. A null result means absence. A returned identifier must match exactly. Kind `S` means student and `T` means staff; unknown or null kind is malformed. Status `Y` means active and `N` means inactive; other values are malformed.

Identifier and kind checks precede inactivity. Thus `Person("B1", "X", "N")` is an error, not an empty result. Codes are case-sensitive and no whitespace normalisation occurs. This policy is explicit rather than a presumed property of all university directories.

The service validates blank identifiers and a null start date before lookup. Duration is checked by the existing coordinator after successful lookup. `Optional.empty()` means a completed lookup found no usable borrower. A `DirectoryException` preserves the distinction between that result and an unavailable or malformed provider response. No category is guessed.

The application interface expects a non-null Optional. A custom implementation returning null violates that contract and will fail rather than silently allow a reservation. The service also checks the returned domain borrower's identifier, so a non-provider implementation cannot accidentally substitute another person unnoticed.

### 2.3 Entry point, not authentication

The new `reserve` method accepts borrower ID, item ID, start date and days, but no category. It obtains the category from the directory. The earlier public coordinator methods still exist for trusted internal use and regression examples, so this is not a security enforcement boundary. A real application needs authenticated identity and controlled access to the exposed entry path.

Directory errors happen before coordinator mutation. Once a valid borrower reaches the coordinator, all earlier policy, conflict and notification behaviour applies. There is no directory caching, HTTP client, retry, persistence or cancellation lifecycle in this increment.

### 2.4 How to read the isolated patterns

`ExportJob.run` invokes the overridden `createExporter` hook: this is the Factory Method example. `simpleExporter` is an ordinary selecting function with the same possible output formats. Output similarity does not make the structures identical.

`ReceiptFamily` creates two product roles, `Heading` and `Body`. Each concrete family supplies matching plain or HTML renderers. Products are represented by small lambdas; introducing named classes is an optional readability change, not a prerequisite for either pattern.

`ReportRequest.Builder` stages configuration and publishes an immutable product. It is the common fluent variant, not a full multiple-representation Director arrangement. Defaults and validation are explicit; the request copies columns at construction. The column labels are sample configuration, not an implemented reporting engine.

`AuditedSender` and `RetryOnceSender` share the `Sender` interface. They preserve the method shape but change observations and attempt behaviour. Their interface is deliberately separate from the cumulative `NotificationSender`. Installing retry in the latter would change its one-attempt contract.

The HTML helpers escape ampersand and angle brackets for text-node content. They do not generate attributes, validate arbitrary markup, or claim to be a general HTML sanitiser. Audit events are a mutable in-memory test list, not a durable audit service.

## 3. Complete application and isolated example sources

All listings in this section belong under `after/src/main/java`. Inherited files are included so the checkpoint is reproducible without reconstructing earlier chapters first.

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

### 3.9 `after/src/main/java/ConfirmationFormatter.java`

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

### 3.10 `after/src/main/java/ConsoleNotificationSender.java`

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

### 3.11 `after/src/main/java/DirectoryException.java`

```java
public final class DirectoryException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    public DirectoryException(String message) { super(message); }
    public DirectoryException(String message, Throwable cause) { super(message, cause); }
}
```

### 3.12 `after/src/main/java/DirectoryReservationService.java`

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

### 3.13 `after/src/main/java/LegacyDirectoryAdapter.java`

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

### 3.14 `after/src/main/java/LegacyDirectoryClient.java`

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

### 3.15 `after/src/main/java/Loan.java`

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

### 3.16 `after/src/main/java/LoanPeriod.java`

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

### 3.17 `after/src/main/java/LoanService.java`

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

### 3.18 `after/src/main/java/NotificationException.java`

```java
public final class NotificationException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    public NotificationException(String message) { super(message); }
}
```

### 3.19 `after/src/main/java/NotificationSender.java`

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

### 3.20 `after/src/main/java/RecordingNotificationSender.java`

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

### 3.21 `after/src/main/java/Reservation.java`

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

### 3.22 `after/src/main/java/ReservationApplication.java`

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

### 3.23 `after/src/main/java/ReservationCoordinator.java`

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

### 3.24 `after/src/main/java/ReservationRules.java`

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

### 3.25 `after/src/main/java/StaffReservationRules.java`

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

### 3.26 `after/src/main/java/patterns/PatternExamples.java`

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

The inherited tests remain unchanged. The two new test classes check the directory boundary and the isolated patterns.

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

### 4.3 `after/src/test/java/BorrowingPolicyTest.java`

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

### 4.4 `after/src/test/java/Chapter02Checks.java`

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

### 4.5 `after/src/test/java/Chapter03AcceptanceExamples.java`

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

### 4.6 `after/src/test/java/Chapter05Checks.java`

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

### 4.7 `after/src/test/java/Chapter06Checks.java`

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

### 4.8 `after/src/test/java/DirectoryAdapterTest.java`

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

### 4.9 `after/src/test/java/LegacyRegressionTest.java`

```java
import org.junit.jupiter.api.Test;

class LegacyRegressionTest {
    @Test void chapter02() { Chapter02Checks.main(new String[0]); }
    @Test void chapter03() { Chapter03AcceptanceExamples.main(new String[0]); }
    @Test void chapter05() { Chapter05Checks.main(new String[0]); }
    @Test void chapter06() { Chapter06Checks.main(new String[0]); }
}
```

### 4.10 `after/src/test/java/LoanServiceTest.java`

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

### 4.11 `after/src/test/java/NotificationMockitoTest.java`

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

### 4.12 `after/src/test/java/patterns/PatternExamplesTest.java`

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

Preserve the test-resource path exactly. Mockito is used by the inherited tests; the new tests use manual fixtures.

### 5.1 `after/pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>edu.se506</groupId>
  <artifactId>equipment-lending</artifactId>
  <version>0.8.0</version>
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
# Chapter 8 checkpoint

Java 17; Maven 3.9.11. JUnit 5.13.4 and Mockito 5.20.0 remain pinned in pom.xml.

From this directory:

```bash
mvn --batch-mode verify
java -cp target/classes Chapter08Demo
java -cp target/classes Chapter07Demo
```

New cumulative entry point: DirectoryReservationService, using BorrowerDirectory and LegacyDirectoryAdapter.
LegacyDirectoryClient models a synthetic external contract. Chapter08Demo uses a map fixture, not a network service.

The patterns package contains isolated Factory Method, Abstract Factory, fluent Builder and Decorator examples. It is not wired into the lending application. Its JUnit tests serve as executable examples.

All Chapter 7 application sources and test files remain unchanged. Chapter 7's four legacy wrappers still execute the earlier plain-Java runners. The complete build executes 63 JUnit invocations: 35 inherited, 17 directory-boundary cases and 11 pattern cases.

The new entry point maps categories before reservation. It does not authenticate callers. Direct coordinator methods remain available for trusted internal examples. In-memory state, reservation lifecycle limitations and the original one-attempt notification contract remain unchanged.

No real university API, database, hosted CI or production delivery service is used.
````

## 6. Worked reading and test evidence

### 6.1 Follow one successful directory lookup

For `reserve("B2", "CAM1", 2026-10-20, 10)`, the service first checks the local arguments. The adapter calls `lookup("B2")`. The demo fixture returns `Person("B2", "T", "Y")`. Identity matches, `T` maps to `STAFF`, and `Y` permits a present result. The service passes that category to the unchanged coordinator.

The coordinator applies the staff policy, finds no conflict, stores R1, formats the confirmation and makes its one notification attempt. The adapter neither calculates duration limits nor allocates reservation identifiers. If staff policy changes later, the mapping `T` to `STAFF` need not change.

For B1, the provider returns the student kind and the same ten-day request is rejected by student policy. That is a successful directory lookup followed by a reservation rejection. For UNKNOWN, lookup returns null and the service rejects before calling the coordinator. For a declared provider failure, the adapter throws a domain-facing exception and retains the original cause.

### 6.2 Acceptance mapping

| Promise | Executable evidence |
|---|---|
| Known active codes map to the correct category | `mapsKnownActiveCategories`: two parameter rows |
| Missing and valid inactive rows yield absence | `absenceAndInactiveAreEmpty` |
| Unknown and differently cased codes are not defaulted | `unknownCodesAreErrors`: four parameter rows |
| Null fields, identity mismatch and malformed inactive rows are errors | `malformedRowsAreErrors` |
| Invalid lookup identifiers never reach the provider | `invalidIdentifierDoesNotReachProvider`: null, empty, blank |
| Expected outage is translated with its cause | `translatesExpectedFailureAndKeepsCause` |
| Unexpected programming failure remains visible | `unexpectedProgrammingFailureIsNotDisguisedAsAbsence` |
| Directory category selects the inherited duration policy | `categoryFromDirectoryControlsReservationPolicy` |
| Absence/outage leave records and notices unchanged and preserve R1 | `absenceAndOutageDoNotStoreNotifyOrConsumeId` |
| A different returned domain identity cannot be reserved | `mismatchedDomainBorrowerIsRejectedBeforeMutation` |
| Local argument failures precede lookup | `localArgumentErrorsPrecedeLookup` |

The table names the tests in `DirectoryAdapterTest`. Some methods contain multiple related assertions; invocation count is not assertion count. The inherited tests continue to protect notification failures, reservation conflicts, query boundaries and the bounded loan lifecycle.

### 6.3 Factory Method versus the simple factory

The following two calls can produce equivalent plain output:

```java
new PatternExamples.PlainJob().run("R1");
PatternExamples.simpleExporter(false).export("R1");
```

The first executes an inherited workflow that invokes the overridden creation hook. The second calls a product returned by a selecting function. The examples differ in who selects the product and how the construction decision is extended. Neither is better solely because it has a more formal pattern name.

A composition alternative is a job with an `Exporter` constructor parameter and a `run` method that invokes it. Choose this when callers should supply the product directly. Choose the demonstrated Factory Method when a framework or inherited workflow explicitly needs subclass-controlled creation. A real requirement for such an extension point should precede the hierarchy.

The test `creatorInvokesOverriddenHookOnce` constructs an anonymous creator for observation. It returns a product with a distinctive output and counts the hook invocation. This intentionally examines the creation mechanism being taught. It does not imply that tests of the lending domain should verify private helper calls.

### 6.4 Abstract Factory and a plausible alternative

`receipt(new PlainFamily(), "Loan", "R1")` produces two text lines. `receipt(new HtmlFamily(), "Loan", "<R1>")` produces a heading and an escaped paragraph. Both products come from the selected family.

A plausible simpler design is one `ReceiptRenderer` per format that returns the whole receipt. It avoids two product interfaces and is appropriate when the parts never vary or collaborate independently. The family design becomes more useful when clients genuinely need several related product roles through stable interfaces.

Adding a Markdown family would require one new implementation supplying both roles; the `receipt` workflow need not change. Adding a footer role would change `ReceiptFamily` and require each family to implement it. That asymmetry is the main extension trade-off to explain in a review.

Returning an HTML heading and plain body from one defective factory is still possible. The interfaces establish product roles; the concrete implementation and complete-output tests establish the selected family behaviour.

### 6.5 Builder and snapshot independence

The builder's mutable `columns` list must not become the request's mutable backing storage. In the final implementation, construction uses `List.copyOf`. A built request therefore preserves its columns when the builder receives another column, and callers cannot modify the returned list.

The test `builtValueIsIndependentOfReusableBuilder` verifies both properties. The immutability claim concerns this object's fields: Strings and LocalDates are immutable, the scalar option is copied, and the list snapshot contains Strings. A shallow copy of mutable element objects in a different design would need further analysis.

The two date arguments are checked for null before the builder changes either date field. Cross-field ordering is checked at `build()`. This lets the builder temporarily hold reversed dates while configuring, but prevents publication of an invalid request. There is no partially valid request object returned to the caller.

The optional interval uses null for both omitted dates inside this small configuration object. The product makes that convention explicit; it does not make every optional application field nullable. A separate interval value could be a reasonable alternative if reporting becomes real cumulative behaviour.

### 6.6 Decorator order and the failure path

`AuditedSender(new RetryOnceSender(flaky), events)` records one logical call. Retry absorbs the first declared failure and calls the underlying sender again. Audit sees only eventual normal return, so its history is `attempt`, `sent`.

`RetryOnceSender(new AuditedSender(flaky, events))` invokes the audit layer on each attempt. The first history is `attempt`, `failed`, and the second is `attempt`, `sent`. Reversing the wrappers changes observations while leaving the outer method signature identical.

After a second declared failure, the second exception escapes. The retry implementation does not recursively invoke itself. If the first error is an unexpected `IllegalArgumentException`, it escapes immediately and the counter remains one. These outcomes are tested separately from eventual success.

The audit wrapper only labels the declared delivery failure. Unexpected exceptions propagate without a `failed` audit event in this deliberately narrow implementation. The fixture's ordinary mutable ArrayList is assumed to accept events. A real audit sink would require a reviewed contract for recording failures, especially if both audit and delivery fail.

Do not copy the retry example into `ReservationApplication.create` as an exercise shortcut. The cumulative sender interface accepts a `Reservation`, and its existing contract specifies one attempt. Changing both the type and policy is a feature change requiring reviewed outcomes, not merely adaptation of syntax.

## 7. Intentionally wrong candidates for diagnosis

These fragments are **deliberately incorrect alternatives**, not files to add to the active source directory. Review them against the actual tests and restore the correct source after any isolated experiment.

### 7.1 Unsafe category fallback

```java
// WRONG: an unfamiliar provider code silently acquires staff privileges.
BorrowerCategory category = "S".equals(row.kind())
        ? BorrowerCategory.STUDENT : BorrowerCategory.STAFF;
```

The `X,Y` and `s,Y` rows of `unknownCodesAreErrors` require a `DirectoryException`. This candidate instead constructs a staff borrower. The correct implementation explicitly recognises `S` and `T` and rejects every other kind. Whether future categories should be supported is a requirement decision, not a fallback default.

### 7.2 Conflating outage with absence

```java
// WRONG: turns provider or programming failures into a normal empty lookup.
try {
    row = client.lookup(borrowerId);
} catch (RuntimeException failure) {
    return Optional.empty();
}
```

This loses the outage distinction and hides unexpected defects. `translatesExpectedFailureAndKeepsCause` and `unexpectedProgrammingFailureIsNotDisguisedAsAbsence` specify different outcomes. Catch the provider's declared failure at its boundary, translate it with the cause, and let unrelated failures remain visible.

### 7.3 A builder that shares mutable state

```java
// WRONG inside ReportRequest construction:
columns = builder.columns;
```

The next builder change would alter an already built value, and a caller could modify the exposed list. The final implementation copies at construction. The snapshot-independence test contains observations for both defects.

The three candidates were applied, one at a time, to a copy of the project and run through `mvn test`. Each was rejected by the tests named above: the unsafe fallback by `unknownCodesAreErrors` and `malformedRowsAreErrors`, the catch-all by `translatesExpectedFailureAndKeepsCause` and `absenceAndOutageDoNotStoreNotifyOrConsumeId`, and the shared builder list by `builtValueIsIndependentOfReusableBuilder`.

## 8. Suggested practical solution and design decision

### 8.1 Integration solution

The complete listings provide one suggested solution. Keep `ReservationCoordinator` independent of the provider record, codes and failure type. Implement `BorrowerDirectory` with the adapter. Construct the coordinator normally, then supply it and the adapter to `DirectoryReservationService`. Use synthetic rows for the demonstration and tests.

The acceptance outcomes are the mapping table plus preservation of reservation behaviour. No lookup result may introduce a borrower category outside the agreed translation. Missing/inactive lookup produces the selected rejection string; outage or malformed data produces an identifiable exception before storage. The service does not catch that exception and turn it into a confirmation or fallback category.

A different design can still be valid. For example, an application may return a structured result distinguishing rejection and operational failure rather than using strings and exceptions. Such a proposal must define how callers handle it and identify any changed contracts. It should not quietly rewrite all earlier APIs merely to fit a diagram.

### 8.2 Example problem–solution–consequence note

**Problem:** the directory's `lookup` method, raw codes, null absence and provider exception differ from the reservation application's needs. Putting those conventions in the coordinator would make policy code depend on one provider.

**Solution:** introduce the application-owned `BorrowerDirectory` interface and an object adapter. A separate application service looks up a borrower before invoking the coordinator with the mapped category. Keep the earlier assembly function.

**Consequences:** translation is located in one tested boundary. Provider changes have a clear first location for review. The design adds several small types and mapping tests, and local fixtures cannot establish real-provider compatibility. Authentication, retries and lifecycle changes remain separate requirements.

**Alternatives declined:** a creator hierarchy is unnecessary for the existing assembly; there is no provider product family requiring Abstract Factory; core values have small constructors; installing retry would alter the established notification policy.

**Revisit when:** an actual provider SDK contract is available, an authenticated entry point is designed, or a concrete requirement adds a related family of integration products. Review those changes individually rather than pre-building every possible variation.

### 8.3 Second-scenario comparison

For a report containing just borrower ID and two required dates, a constructor or named creation method is sufficient. If several optional configuration choices make positional calls difficult to read, a builder can clarify intent and publish a validated immutable snapshot. The provided example demonstrates that latter pressure but does not require a builder for every record.

For exporter selection, an injected `Exporter` is preferable when the caller can choose it directly. Factory Method is justified when subclass-controlled creation is an intentional part of an inherited workflow. Both alternatives can satisfy the same output tests; the structural requirement decides between them.

A good submission names an actual change that becomes easier and a concrete cost. “Uses more patterns” is neither a benefit nor an acceptance condition.

### 8.4 Builder and Decorator implementation exercises

These solutions extend the isolated `patterns` examples only. They do not touch the lending application, and they are not part of the 63-invocation inventory.

**Builder: an optional maximum row count.** In `ReportRequest`, add an `OptionalInt maximumRows` field and accessor (import `java.util.OptionalInt`), copy it in the constructor with `maximumRows = builder.maximumRows;`, and give the builder an `OptionalInt maximumRows = OptionalInt.empty();` field and this method:

```java
public Builder maximumRows(int value) {
    if (value <= 0) throw new IllegalArgumentException("Positive row limit required");
    maximumRows = OptionalInt.of(value);
    return this;
}
```

`OptionalInt` is immutable, so copying the reference at construction is enough to keep a built request independent of later builder changes. Absence is represented explicitly and not by a sentinel such as zero.

```java
@Test void maximumRowsIsAbsentByDefaultAndMustBePositive() {
    assertTrue(ReportRequest.forBorrower("B1").build().maximumRows().isEmpty());
    assertEquals(5, ReportRequest.forBorrower("B1").maximumRows(5).build().maximumRows().getAsInt());
    assertThrows(IllegalArgumentException.class, () -> ReportRequest.forBorrower("B1").maximumRows(0));
    assertThrows(IllegalArgumentException.class, () -> ReportRequest.forBorrower("B1").maximumRows(-1));
}

@Test void laterBuilderChangeDoesNotAffectABuiltRowLimit() {
    var builder = ReportRequest.forBorrower("B1").maximumRows(5);
    var first = builder.build();
    builder.maximumRows(9);
    assertEquals(5, first.maximumRows().getAsInt());
    assertEquals(9, builder.build().maximumRows().getAsInt());
}
```

**Decorator: counting attempts.** Add this class beside the other senders (import `java.util.concurrent.atomic.AtomicInteger`):

```java
public static final class CountingSender implements Sender {
    private final Sender delegate;
    private final AtomicInteger attempts;
    public CountingSender(Sender delegate, AtomicInteger attempts) {
        this.delegate = Objects.requireNonNull(delegate, "delegate");
        this.attempts = Objects.requireNonNull(attempts, "attempts");
    }
    public void send(String message) {
        attempts.incrementAndGet();
        delegate.send(message);
    }
}
```

The prediction is the point of the exercise. With one failure followed by success, a counter **outside** the retry decorator sees one logical call, so it counts 1. A counter **inside** it sees both delegate attempts, so it counts 2. It is the same order effect as the audit histories, now measured by a number.

```java
@Test void countingOutsideRetryCountsCallsAndInsideCountsAttempts() {
    var flakyCalls = new AtomicInteger();
    Sender flaky = message -> { if (flakyCalls.incrementAndGet() == 1) throw new DeliveryFailure("first"); };
    var outside = new AtomicInteger();
    new CountingSender(new RetryOnceSender(flaky), outside).send("R1");
    assertEquals(1, outside.get());
    flakyCalls.set(0);
    var inside = new AtomicInteger();
    new RetryOnceSender(new CountingSender(flaky, inside)).send("R1");
    assertEquals(2, inside.get());
}
```

With these three tests added, the class `PatternExamplesTest` runs 14 tests and all pass. Accept other designs that preserve the stated behaviour. A sentinel such as `0` meaning “no limit” is a weaker design here, because it makes “zero rows” unrepresentable and ambiguous; ask students to justify it if they choose it.

**Team project step (practical step 9).** There is no single answer. A strong note names a concrete external or mismatched interface in the team's code, shows the problem–solution–consequence reasoning, and says what the team would decline to build. Reject answers that propose an adapter where two components already share the same contract and meaning.

## 9. AI activity solution

| Fictional claim | Diagnosis and correction | Evidence or decision |
|---|---|---|
| Renaming static `create` makes Factory Method | Names do not create a subclass hook | Compare `simpleExporter` with `ExportJob.createExporter` |
| One product role requires Abstract Factory | No related set has been established | Retain simple assembly until a family requirement exists |
| Catch every exception and return staff | Hides failure and grants an unsupported category | Unknown-code and exception-cause tests |
| Wrap all senders with retry | Changes the one-attempt cumulative contract | Keep retry isolated; review any proposed policy change |
| Decorator order does not matter | Changes which layer observes each attempt | The two exact audit-history tests |
| A builder guarantees immutable products | Mutable aliases can remain after build | Snapshot and unmodifiable-list tests |

Pattern classification needs source inspection as well as output tests. A test cannot prove that a static function became a subclass-based Factory Method because the function was renamed. Conversely, finding an appropriate structure does not establish correct error handling. Check both design reasoning and behaviour.

For a live AI exchange, retain only an actual transcript or relevant excerpts. Record which claims you checked and which you rejected. The fictional fixture is sufficient for learners without an AI account and should never be presented as output from a real service.

## 10. Review answers and transfer solution

### 10.1 Four concept answers

**1. Factory Method versus simple factory:** `ExportJob` owns the inherited workflow and subclasses override a product-creation hook. `simpleExporter` selects and returns a product in an ordinary function. A method named `create` or a return type that is an interface does not alone establish the former structure.

**2. A genuine product family:** several product roles must vary together for a meaningful compatibility reason. In the example, heading and body share an output format. Constructing an unrelated clock and directory together does not establish that requirement. A family interface also needs correct concrete implementations; it cannot prevent every mixed family by itself.

**3. Independence after build:** the request copies mutable builder state, validates before publication and exposes no mutation operation. In this example the list elements and date values are themselves immutable. Returning a final reference to the builder's mutable list would not suffice.

**4. Adapter versus Decorator:** Adapter translates one contract into the contract its client expects. Decorator retains the component interface while adding optional responsibilities around delegation. Holding another object is a common mechanism, not a sufficient classification. Here category translation is Adapter; audit/retry composition is Decorator.

### 10.2 Applied diagnosis answers

**5. Broad exception handling:** it can conceal a legitimate provider outage and a programming defect such as an unexpected illegal state. Both become indistinguishable from a completed lookup finding no borrower. The application may display a misleading rejection and operators lose the meaningful cause. Translate the declared provider failure with cause retention; keep malformed data explicit and unexpected defects visible.

**6. Wrapper order:** with one failure followed by success, audit outside retry records `attempt, sent`; retry outside audit records `attempt, failed, attempt, sent`. Choose the former when the record concerns logical operations, or the latter when every delivery attempt must be observed. Also decide how a real recording failure affects the operation. Interface compatibility alone does not decide those semantics.

### 10.3 Library-patron transfer

First obtain an explicit provider mapping. For a hypothetical contract only, assume category 10 means student, category 20 means staff, and an inactive flag excludes an otherwise valid patron. Do not transplant the equipment example's string codes into a numeric API without that agreement.

Define an application-owned `PatronDirectory.find(id)` returning presence/absence and an identifiable operational failure. Adapt provider records into immutable patron values. Keep borrowing eligibility policy outside the translation layer.

Three failure examples are an unknown category, a returned identifier different from the requested one, and a declared provider outage. All must prevent the borrowing operation before state changes; the outage retains its cause. A valid inactive row yields the agreed empty result, provided the policy follows the chapter's absence convention. Add a test for each outcome and clarify malformed-inactive precedence.

If the receipt has one interchangeable renderer, use direct injection or a simple factory. If multiple independently used receipt components must be supplied as matching plain/HTML families, Abstract Factory becomes a candidate. Explain the compatibility relationship and the cost of adding another product role. Neither patron lookup nor receipt rendering automatically requires a builder or retry decorator.

## 11. Instructor guidance

### 11.1 Suggested teaching sequence

Demonstrate the simple factory and Factory Method side by side. Ask students to locate the point where the product choice varies, then run the two output examples and the hook-observation test. Explain why matching output does not settle the pattern classification.

Next trace the directory adapter. Use one staff success, one unknown code and one provider failure. Ask students where the first reservation mutation is possible and what must remain unchanged before that point. Run the full test suite after the new entry point is introduced.

Assign the family and builder examples as guided reading during the midterm week. Ask students to predict decorator event histories before running the order tests. Use the model answers for discussion, accepting alternatives that preserve the agreed semantics and explain their costs. Do not assess by number of patterns or require the separate examples to be wired into the running application.

The official midterm scope remains Weeks 1–6, Chapters 2–7. This chapter adds no assessment weights, deadlines or official contact-hour allocation.

### 11.2 Do the tests detect faults?

Twenty faults, listed in the table below (8 + 3 + 2 + 4 + 2 + 1), were introduced one at a time into copies of the project, and each copy was run through `mvn test`. All twenty are caught.

| Area | Faults tried | Result |
|---|---|---|
| Adapter | Unknown kind defaults to staff (Section 7.1); catch-all returns empty (7.2); inactive checked before kind; identifier mismatch unchecked; codes case-insensitive; any non-`N` status accepted; blank identifier reaches the provider; outage cause dropped | All eight caught by `DirectoryAdapterTest` |
| Directory service | Directory category ignored; absent borrower gets a student default; returned identity unchecked | All three caught |
| Builder | Shared mutable column list (7.3); interval not validated | Both caught |
| Decorators | Retry on any `RuntimeException`; retry twice; no `failed` audit event; audit swallows the failure | All four caught |
| Abstract Factory and escaping | HTML heading uses the plain renderer; angle brackets not escaped | Both caught |
| Factory Method | `ExportJob.run` skips its null check | Caught by `plain.run(null)` in the existing test. Without that call only `HtmlJob.run(null)` would be tested, and `HtmlJob` fails on null anyway through `escape`, so `PlainJob.run(null)` would silently return `TEXT: null` |

The 35 inherited invocations include four wrappers around the earlier plain-Java check runners. Their internal counts remain distinct: 34 Chapter 2 checks, five Chapter 3 example groups, 44 Chapter 5 checks and 28 Chapter 6 checks.

The Mockito dynamic-agent warning described in Chapter 7 also appears in this project's log on a recent JDK. It does not affect results, and `-DargLine=-XX:+EnableDynamicAgentLoading` removes it.

Do not add the inherited check counts as if every unit were the same kind of test.

Local success does not prove real-provider compatibility, authentication, durable storage, concurrency safety or absence of all defects. It establishes the documented examples for this source and configuration. The intentionally wrong fragments in Section 7 are diagnosis material and were not part of the twenty-fault experiment above; no other mutation-run result is claimed.

## References

Sources checked 12 October 2026. See the chapter's source notes for the distinction between the classic book's bibliographic reference and the publisher excerpts inspected online.

1. Gamma, E., Helm, R., Johnson, R. and Vlissides, J., *Design Patterns: Elements of Reusable Object-Oriented Software*. [Publisher catalogue](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-software-9780201633610).
2. Gamma et al., [Abstract Factory excerpt](https://www.informit.com/articles/article.aspx?p=1398599) and [Adapter excerpt](https://www.informit.com/articles/article.aspx?p=1398600).
3. Oracle, [Java SE 17 Optional](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Optional.html) and [FilterInputStream](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/FilterInputStream.html).
4. JUnit Team, [JUnit 5.13.4 User Guide](https://docs.junit.org/5.13.4/user-guide/).