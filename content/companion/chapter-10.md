---
title: "Chapter 10 Companion: Code, Explanations and Solutions"
weight: 100
description: "Code explanations and solutions for Chapter 10 Companion: Code, Explanations and Solutions."
---

*From Classes to Application Structure*  
*OO Development and Agile Practices*

## 1. Scope and execution

This file accompanies Chapter 10, From Classes to Application Structure. It contains the complete restructured version, migration instructions, an architecture decision, tests and model solutions. The starting implementation is the Chapter 9 companion.

The change introduces named application packages, a focused reservation repository boundary and a thin console adapter. It preserves the demonstrated use-case outcomes. Package names, imports, constructor wiring and launcher names change; source and binary compatibility with the unnamed-package version are not claimed.

### 1.1 Reconstruct a clean version

Create a new directory named `after`. Save every labelled file listing in Sections 3–5 at its indicated path, including `.gitattributes` and `tools/PackageMetrics.java`. Copy only fence contents, preserving case and creating intermediate directories. README and ADR listings use four backticks where appropriate. Start with a clean directory: leaving the old unnamed-package source files beside the migrated files would create a misleading mixed version.

Use a **full Java 17 JDK**, including the `jdk.jdeps` module, and Maven 3.9.11. JUnit Jupiter 5.13.4, Mockito 5.20.0, Compiler Plugin 3.14.1 and Surefire 3.5.4 remain pinned. The Maven project version becomes 0.10.0. Initial builds require dependency access.

From inside `after`:

```bash
mvn --batch-mode verify
java -cp target/classes edu.se506.lending.bootstrap.Chapter10Demo
```

The existing check wrapper remains available:

```bash
bash scripts/check.sh
```

The dependency check is already part of the normal test run. To examine class dependencies directly:

```bash
java --module jdk.jdeps/com.sun.tools.jdeps.Main -verbose:class -filter:none target/classes
```

This command reports dependencies; `DependencyRulesTest` applies this project's selected rules to them. A full JDK is required even if a smaller runtime could launch the application.

### 1.2 Expected output and earlier launchers

The new demonstration prints the same five lines as Chapter 8's example, now through a thin console adapter:

```text
Confirmed: R1 for B2 on CAM1 [2026-10-20, 2026-10-30).
Rejected: borrower limit or duration.
Rejected: borrower not found or inactive.
Reservations: 1
Notices: 1
```

Earlier demonstrations now use fully qualified names:

```bash
java -cp target/classes edu.se506.lending.bootstrap.Chapter07Demo
java -cp target/classes edu.se506.lending.bootstrap.Chapter08Demo
java -cp target/classes edu.se506.lending.bootstrap.Chapter09Demo
```

`Chapter04Demo`, `Chapter05Demo` and `ReservationApplication` are likewise in `edu.se506.lending.bootstrap`. The old command `java -cp target/classes Chapter09Demo` no longer names the migrated class. This is a documented launcher change, not a failed preservation of the demo's business output.

### 1.3 Package metrics

The metrics in Section 10.5 of the chapter come from a small program that is not part of the Maven build. After compiling, run it from the project root:

```bash
mvn --batch-mode compile
java tools/PackageMetrics.java target/classes
```

It starts the JDK's `jdeps` analyser, so it needs the same full JDK as the dependency test. It prints one row per package:

```text
package                                          classes   Ca   Ce         I
behaviour                                              1    1    0      0.00
edu.se506.lending.application                          6    9    4      0.31
edu.se506.lending.application.port                     5   14    3      0.18
edu.se506.lending.bootstrap                            7    0    7      1.00
edu.se506.lending.domain                               8   16    0      0.00
edu.se506.lending.infrastructure.directory             2    2    1      0.33
edu.se506.lending.infrastructure.notification          3    7    3      0.30
edu.se506.lending.infrastructure.persistence           1    1    1      0.50
edu.se506.lending.presentation                         1    1    1      0.50
examples.structure                                     1    0    0 undefined
patterns                                               1    0    0 undefined
```

The counting rules are in the program's header comment and the chapter: classes are the unit, a nested class counts with its outer class, only this project's own packages count, and the standard library is ignored. Ca is the number of classes outside a package that depend on it, Ce the number of its classes that depend on classes outside it, and I = Ce / (Ca + Ce). When Ca + Ce is zero the program prints *undefined* instead of guessing. Other tools count differently, so compare numbers only from one tool.

## 2. Migration and design map

### 2.1 Package mapping

All package names in this table are beneath `edu.se506.lending` unless otherwise stated.

| Destination | Types moved or introduced |
|---|---|
| `domain` | BorrowerCategory, BorrowingPolicy, ReservationRules, StaffReservationRules, LoanPeriod, Reservation, Borrower, Loan |
| `application` | ConfirmationFormatter, ReservationCoordinator, DirectoryReservationService, LoanService, Command, ReserveEquipmentCommand |
| `application.port` | BorrowerDirectory, NotificationSender, NotificationException, DirectoryException; new ReservationRepository |
| `infrastructure.directory` | LegacyDirectoryClient, LegacyDirectoryAdapter |
| `infrastructure.notification` | RecordingNotificationSender, ConsoleNotificationSender, NotificationPublisher |
| `infrastructure.persistence` | New InMemoryReservationRepository |
| `presentation` | New ReservationConsole |
| `bootstrap` | ReservationApplication; Chapters 4, 5, 7, 8, 9 demos; new Chapter10Demo |
| `regression` in test sources | All formerly unnamed-package tests and legacy check runners |
| `structure` in test sources | RepositoryBoundaryTest, ValueSemanticsTest, ReservationConsoleTest, DependencyRulesTest |
| Existing top-level `patterns` and `behaviour` packages | Earlier isolated examples and their tests, unchanged |
| New top-level `examples.structure` | PeriodValue equality demonstration, not part of the running domain |

Expected-failure types belong to the application ports because callers should not need provider-specific exception types. The adapter still translates the provider's declared failure to the application-facing exception.

### 2.2 Constructor and storage change

Previously, ReservationCoordinator owned an ArrayList directly and accepted policies, formatter and sender. It now accepts those three dependencies plus a ReservationRepository as its fourth argument. Its scans use repository snapshots, insertion uses `add`, and `reservations()` returns the repository's specified snapshot.

ReservationApplication.create(sender) constructs a fresh InMemoryReservationRepository and passes it to the coordinator. Direct coordinator constructions in the earlier checks and Strategy example are updated with the same explicit adapter. Their assertions and expected outcomes remain intact.

No compatibility constructor instantiates infrastructure inside the application package. Such a shortcut would undermine the dependency boundary being demonstrated. Consumers update construction or use the factory in its new bootstrap package.

The repository contract is append-only, insertion ordered, and keyed by explicit reservation ID. Duplicate IDs reject without replacement. Null addition rejects. Snapshot values are safe here because the Reservation graph is immutable. The port does not impose a generic CRUD lifecycle or promise database transaction semantics.

### 2.3 Supported ownership and preserved semantics

The factory supplies one new, empty repository for one sequential coordinator/session. Size-based R1, R2 allocation is retained. Arbitrary preloaded stores, deletion, multiple writers or shared independent loan services would need additional contracts and are not promised by introducing constructor injection.

Storage still precedes notification. A repository that throws before adding does not trigger notification. A future implementation that writes and then loses acknowledgement presents a different failure case; this chapter does not claim to solve it.

The existing running LoanPeriod remains immutable but keeps inherited Java object equality. PeriodValue separately demonstrates record equality and hashing. No entity lifecycle, policy limit, availability rule or cancellation behaviour changes during this restructuring.

### 2.4 Declared production dependency rules

| Source package | Permitted local targets |
|---|---|
| Domain | Domain |
| Application ports | Domain and application ports |
| Application services | Domain and application, including ports |
| Infrastructure | Domain, application and infrastructure |
| Presentation | Domain, application and presentation |
| Bootstrap | All application packages and explicitly demonstrated isolated examples |

Ordinary production layers cannot depend on `patterns`, `behaviour` or `examples`. Bootstrap may launch an isolated demonstration; test setups may assemble whatever they need. The gate examines compiled production classes, not test classes. Standard-library dependencies are outside this local package matrix.

The test catches local bytecode dependency edges, including fully qualified references. A second test builds the package-to-package graph from the same edges and fails if it contains a cycle; the matrix alone would let two infrastructure packages refer to each other. The cycle check looks at the lending packages only. It is not an enforcement of all possible third-party-library policies, reflection, configuration or semantic responsibility. The permitted infrastructure-to-application edge accommodates ports and the retained shared ConfirmationFormatter.

### 2.5 Assertions and fixes carried forward from Chapters 3–9

Several strengthened checks do not change the JUnit count, so a green total cannot show that a migration kept them. This table lists what must survive, and where it lives in this version.

| Origin | Preserved item | Location in this version |
|---|---|---|
| Chapter 3 | The AC-03 request that ends exactly where an existing reservation starts, as well as the request that starts where one ends (five acceptance groups) | `regression/Chapter03AcceptanceExamples.java` |
| Chapter 4 | `.gitattributes` keeping `scripts/check.sh` in LF form | `.gitattributes` |
| Chapter 6 | `BrokenSender`: an unexpected sender failure is not swallowed and the record is stored first (28 checks) | `regression/Chapter06Checks.java` |
| Chapters 6–8 | `serialVersionUID` on `NotificationException`, `DirectoryException`, `LegacyDirectoryClient.Failure` and `PatternExamples.DeliveryFailure` | those four files |
| Chapter 7 | `assertThrows(UnsupportedOperationException.class, snapshot::clear)` on the loan snapshot | `regression/LoanServiceTest.java` (`checkoutAndReturnUseTheSuppliedClock`) |
| Chapter 8 | `plain.run(null)` throws `NullPointerException` | `patterns/PatternExamplesTest.java` |
| Chapter 9 | Command construction rejects a null receiver, a blank borrower, a null item and a null start, and the confirmation is compared exactly, period included | `regression/ReserveEquipmentCommandTest.java` |

To check a migration yourself, compare each migrated file with its Chapter 9 original, ignoring `package` and `import` lines. In this version the only differences are the repository argument added to coordinator constructions (in `BehaviourStrategyTest`, `Chapter06Checks` and `ReservationApplication`) and the coordinator's own storage code.

### 2.6 What the package metrics do and do not show

The table in Section 1.3 is a measurement of the compiled version, not a judgement. With one to eight classes per package a single added class moves a ratio by several hundredths. The one arrow that points to a slightly less stable package (`infrastructure.notification` at 0.30 to `application` at 0.31) is the concrete `ConfirmationFormatter` dependency that Section 6.2 already describes. The isolated packages `patterns` and `examples.structure` have no local references in either direction, so their instability is undefined; `behaviour` is referenced by `Chapter09Demo`, so Ca = 1 and I = 0.

## 3. Complete production and isolated example sources

The following files reconstruct the complete version. Package declarations and directory paths are part of each listing and must be preserved.

### 3.1 `after/src/main/java/behaviour/LifecycleExamples.java`

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

### 3.2 `after/src/main/java/edu/se506/lending/application/Command.java`

```java
package edu.se506.lending.application;



/** Executes synchronously on the caller's thread; no queue or retry is implied. */
@FunctionalInterface
public interface Command<R> {
    R execute();
}
```

### 3.3 `after/src/main/java/edu/se506/lending/application/ConfirmationFormatter.java`

```java
package edu.se506.lending.application;

import edu.se506.lending.domain.Reservation;

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

### 3.4 `after/src/main/java/edu/se506/lending/application/DirectoryReservationService.java`

```java
package edu.se506.lending.application;

import edu.se506.lending.application.port.BorrowerDirectory;
import edu.se506.lending.application.port.DirectoryException;
import edu.se506.lending.domain.Borrower;

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

### 3.5 `after/src/main/java/edu/se506/lending/application/LoanService.java`

```java
package edu.se506.lending.application;

import edu.se506.lending.domain.Loan;
import edu.se506.lending.domain.Reservation;

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

### 3.6 `after/src/main/java/edu/se506/lending/application/ReservationCoordinator.java`

```java
package edu.se506.lending.application;

import edu.se506.lending.application.port.NotificationException;
import edu.se506.lending.application.port.NotificationSender;
import edu.se506.lending.application.port.ReservationRepository;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.domain.BorrowingPolicy;
import edu.se506.lending.domain.LoanPeriod;
import edu.se506.lending.domain.Reservation;

import java.time.LocalDate;
import java.util.List;
import java.util.Objects;
import java.util.Map;

public final class ReservationCoordinator {
    private final ReservationRepository repository;
    private final Map<BorrowerCategory, BorrowingPolicy> policies;
    private final ConfirmationFormatter formatter;
    private final NotificationSender notifications;

    public ReservationCoordinator(Map<BorrowerCategory, BorrowingPolicy> policies,
                                  ConfirmationFormatter formatter,
                                  NotificationSender notifications,
                                  ReservationRepository repository) {
        this.policies = Map.copyOf(Objects.requireNonNull(policies, "policies"));
        for (BorrowerCategory category : BorrowerCategory.values()) {
            if (!this.policies.containsKey(category)) {
                throw new IllegalArgumentException("Missing policy: " + category);
            }
        }
        this.formatter = Objects.requireNonNull(formatter, "formatter");
        this.notifications = Objects.requireNonNull(notifications, "notifications");
        this.repository = Objects.requireNonNull(repository, "repository");
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
        for (Reservation existing : repository.findAll()) {
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
                "R" + (repository.findAll().size() + 1), borrowerId, itemId, requested);
        repository.add(reservation);
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
        for (Reservation existing : repository.findAll()) {
            if (existing.itemId().equals(itemId) && existing.period().overlaps(requested)) {
                return true;
            }
        }
        return false;
    }

    public List<Reservation> reservations() {
        return repository.findAll();
    }
}
```

### 3.7 `after/src/main/java/edu/se506/lending/application/ReserveEquipmentCommand.java`

```java
package edu.se506.lending.application;



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

### 3.8 `after/src/main/java/edu/se506/lending/application/port/BorrowerDirectory.java`

```java
package edu.se506.lending.application.port;

import edu.se506.lending.domain.Borrower;

import java.util.Optional;

/** Empty means absent or inactive, never a provider outage. */
@FunctionalInterface
public interface BorrowerDirectory {
    Optional<Borrower> find(String borrowerId);
}
```

### 3.9 `after/src/main/java/edu/se506/lending/application/port/DirectoryException.java`

```java
package edu.se506.lending.application.port;

public final class DirectoryException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    public DirectoryException(String message) { super(message); }
    public DirectoryException(String message, Throwable cause) { super(message, cause); }
}
```

### 3.10 `after/src/main/java/edu/se506/lending/application/port/NotificationException.java`

```java
package edu.se506.lending.application.port;

public final class NotificationException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    public NotificationException(String message) { super(message); }
}
```

### 3.11 `after/src/main/java/edu/se506/lending/application/port/NotificationSender.java`

```java
package edu.se506.lending.application.port;

import edu.se506.lending.domain.Reservation;

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

### 3.12 `after/src/main/java/edu/se506/lending/application/port/ReservationRepository.java`

```java
package edu.se506.lending.application.port;

import edu.se506.lending.domain.Reservation;
import java.util.List;

/** Minimal append-only store contract for one sequential session. */
public interface ReservationRepository {
    /** Stable unmodifiable snapshot, in insertion order. Values are immutable. */
    List<Reservation> findAll();
    /** Add a non-null reservation; duplicate IDs reject without changing the store. */
    void add(Reservation reservation);
}
```

### 3.13 `after/src/main/java/edu/se506/lending/bootstrap/Chapter04Demo.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 3.14 `after/src/main/java/edu/se506/lending/bootstrap/Chapter05Demo.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 3.15 `after/src/main/java/edu/se506/lending/bootstrap/Chapter07Demo.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.LoanService;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.domain.Loan;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 3.16 `after/src/main/java/edu/se506/lending/bootstrap/Chapter08Demo.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.application.port.BorrowerDirectory;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryAdapter;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryClient;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 3.17 `after/src/main/java/edu/se506/lending/bootstrap/Chapter09Demo.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.Command;
import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.application.ReserveEquipmentCommand;
import edu.se506.lending.application.port.NotificationException;
import edu.se506.lending.domain.Borrower;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.infrastructure.notification.NotificationPublisher;

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

### 3.18 `after/src/main/java/edu/se506/lending/bootstrap/Chapter10Demo.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryAdapter;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryClient;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import edu.se506.lending.presentation.ReservationConsole;
import java.time.LocalDate;
import java.util.Map;

public final class Chapter10Demo {
    public static void main(String[] args) {
        var rows = Map.of(
                "B1", new LegacyDirectoryClient.Person("B1", "S", "Y"),
                "B2", new LegacyDirectoryClient.Person("B2", "T", "Y"));
        var sender = new RecordingNotificationSender();
        var coordinator = ReservationApplication.create(sender);
        var service = new DirectoryReservationService(new LegacyDirectoryAdapter(rows::get), coordinator);
        var console = new ReservationConsole(service, System.out);
        var start = LocalDate.of(2026, 10, 20);
        console.reserve("B2", "CAM1", start, 10);
        console.reserve("B1", "MIC1", start, 10);
        console.reserve("UNKNOWN", "MIC1", start, 2);
        System.out.println("Reservations: " + coordinator.reservations().size());
        System.out.println("Notices: " + sender.received().size());
    }
}
```

### 3.19 `after/src/main/java/edu/se506/lending/bootstrap/ReservationApplication.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.ConfirmationFormatter;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.application.port.NotificationSender;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.domain.ReservationRules;
import edu.se506.lending.domain.StaffReservationRules;
import edu.se506.lending.infrastructure.notification.ConsoleNotificationSender;
import edu.se506.lending.infrastructure.persistence.InMemoryReservationRepository;

import java.time.LocalDate;
import java.util.Map;

public final class ReservationApplication {
    private ReservationApplication() { }

    public static ReservationCoordinator create(NotificationSender sender) {
        return new ReservationCoordinator(
                Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                       BorrowerCategory.STAFF, new StaffReservationRules()),
                new ConfirmationFormatter(), sender, new InMemoryReservationRepository());
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

### 3.20 `after/src/main/java/edu/se506/lending/domain/Borrower.java`

```java
package edu.se506.lending.domain;



import java.util.Objects;

public record Borrower(String id, BorrowerCategory category) {
    public Borrower {
        if (id == null || id.isBlank()) throw new IllegalArgumentException("Borrower id required");
        Objects.requireNonNull(category, "category");
    }
}
```

### 3.21 `after/src/main/java/edu/se506/lending/domain/BorrowerCategory.java`

```java
package edu.se506.lending.domain;



public enum BorrowerCategory {
    STUDENT, STAFF
}
```

### 3.22 `after/src/main/java/edu/se506/lending/domain/BorrowingPolicy.java`

```java
package edu.se506.lending.domain;



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

### 3.23 `after/src/main/java/edu/se506/lending/domain/Loan.java`

```java
package edu.se506.lending.domain;



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

### 3.24 `after/src/main/java/edu/se506/lending/domain/LoanPeriod.java`

```java
package edu.se506.lending.domain;



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

### 3.25 `after/src/main/java/edu/se506/lending/domain/Reservation.java`

```java
package edu.se506.lending.domain;



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

### 3.26 `after/src/main/java/edu/se506/lending/domain/ReservationRules.java`

```java
package edu.se506.lending.domain;



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

### 3.27 `after/src/main/java/edu/se506/lending/domain/StaffReservationRules.java`

```java
package edu.se506.lending.domain;



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

### 3.28 `after/src/main/java/edu/se506/lending/infrastructure/directory/LegacyDirectoryAdapter.java`

```java
package edu.se506.lending.infrastructure.directory;

import edu.se506.lending.application.port.BorrowerDirectory;
import edu.se506.lending.application.port.DirectoryException;
import edu.se506.lending.domain.Borrower;
import edu.se506.lending.domain.BorrowerCategory;

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

### 3.29 `after/src/main/java/edu/se506/lending/infrastructure/directory/LegacyDirectoryClient.java`

```java
package edu.se506.lending.infrastructure.directory;

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

### 3.30 `after/src/main/java/edu/se506/lending/infrastructure/notification/ConsoleNotificationSender.java`

```java
package edu.se506.lending.infrastructure.notification;

import edu.se506.lending.application.ConfirmationFormatter;
import edu.se506.lending.application.port.NotificationException;
import edu.se506.lending.application.port.NotificationSender;
import edu.se506.lending.domain.Reservation;

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

### 3.31 `after/src/main/java/edu/se506/lending/infrastructure/notification/NotificationPublisher.java`

```java
package edu.se506.lending.infrastructure.notification;

import edu.se506.lending.application.port.NotificationException;
import edu.se506.lending.application.port.NotificationSender;
import edu.se506.lending.domain.Reservation;

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

### 3.32 `after/src/main/java/edu/se506/lending/infrastructure/notification/RecordingNotificationSender.java`

```java
package edu.se506.lending.infrastructure.notification;

import edu.se506.lending.application.port.NotificationSender;
import edu.se506.lending.domain.Reservation;

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

### 3.33 `after/src/main/java/edu/se506/lending/infrastructure/persistence/InMemoryReservationRepository.java`

```java
package edu.se506.lending.infrastructure.persistence;

import edu.se506.lending.application.port.ReservationRepository;
import edu.se506.lending.domain.Reservation;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/** Insertion ordered, append only, not persistent and not thread-safe. */
public final class InMemoryReservationRepository implements ReservationRepository {
    private final Map<String, Reservation> records = new LinkedHashMap<>();
    @Override public List<Reservation> findAll() { return List.copyOf(records.values()); }
    @Override public void add(Reservation reservation) {
        Objects.requireNonNull(reservation, "reservation");
        if (records.containsKey(reservation.id())) {
            throw new IllegalArgumentException("Duplicate reservation id: " + reservation.id());
        }
        records.put(reservation.id(), reservation);
    }
}
```

### 3.34 `after/src/main/java/edu/se506/lending/presentation/ReservationConsole.java`

```java
package edu.se506.lending.presentation;

import edu.se506.lending.application.DirectoryReservationService;
import java.io.PrintStream;
import java.time.LocalDate;
import java.util.Objects;

/** Thin output adapter: delegates the use case and prints its existing result. */
public final class ReservationConsole {
    private final DirectoryReservationService service;
    private final PrintStream output;
    public ReservationConsole(DirectoryReservationService service, PrintStream output) {
        this.service = Objects.requireNonNull(service, "service");
        this.output = Objects.requireNonNull(output, "output");
    }
    public void reserve(String borrowerId, String itemId, LocalDate start, int days) {
        output.println(service.reserve(borrowerId, itemId, start, days));
    }
}
```

### 3.35 `after/src/main/java/examples/structure/PeriodValue.java`

```java
package examples.structure;

import java.time.LocalDate;
import java.util.Objects;

/** Separate equality example; deliberately does not replace cumulative LoanPeriod. */
public record PeriodValue(LocalDate start, LocalDate endExclusive) {
    public PeriodValue {
        Objects.requireNonNull(start, "start");
        Objects.requireNonNull(endExclusive, "endExclusive");
        if (!start.isBefore(endExclusive)) throw new IllegalArgumentException("End must be after start.");
    }
}
```

### 3.36 `after/src/main/java/patterns/PatternExamples.java`

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

Migrated regression tests retain their original expectations. Structure tests examine the new boundaries and compiled references.

### 4.1 `after/src/test/java/behaviour/LifecycleExamplesTest.java`

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

### 4.2 `after/src/test/java/edu/se506/lending/regression/AvailabilityTddTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.Reservation;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 4.3 `after/src/test/java/edu/se506/lending/regression/AvailabilityTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.Reservation;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 4.4 `after/src/test/java/edu/se506/lending/regression/BehaviourStrategyTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.ConfirmationFormatter;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.domain.BorrowingPolicy;
import edu.se506.lending.domain.ReservationRules;
import edu.se506.lending.domain.StaffReservationRules;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import edu.se506.lending.infrastructure.persistence.InMemoryReservationRepository;

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
                new ConfirmationFormatter(), new RecordingNotificationSender(), new InMemoryReservationRepository());
        var start = LocalDate.of(2026, 10, 20);
        assertEquals("Rejected: borrower limit or duration.", coordinator.reserve("T1", "CAM1", start, 3, BorrowerCategory.STAFF));
        assertTrue(coordinator.reserve("T1", "CAM1", start, 2, BorrowerCategory.STAFF).startsWith("Confirmed: R1"));
        assertEquals("Rejected: borrower limit or duration.", coordinator.reserve("T1", "MIC1", start, 1, BorrowerCategory.STAFF));
        assertTrue(coordinator.reserve("S1", "MIC1", start, 7, BorrowerCategory.STUDENT).startsWith("Confirmed: R2"));
    }
}
```

### 4.5 `after/src/test/java/edu/se506/lending/regression/BorrowingPolicyTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.domain.BorrowingPolicy;
import edu.se506.lending.domain.ReservationRules;
import edu.se506.lending.domain.StaffReservationRules;

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

### 4.6 `after/src/test/java/edu/se506/lending/regression/Chapter02Checks.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.LoanPeriod;
import edu.se506.lending.domain.Reservation;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 4.7 `after/src/test/java/edu/se506/lending/regression/Chapter03AcceptanceExamples.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 4.8 `after/src/test/java/edu/se506/lending/regression/Chapter05Checks.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.domain.BorrowingPolicy;
import edu.se506.lending.domain.Reservation;
import edu.se506.lending.domain.ReservationRules;
import edu.se506.lending.domain.StaffReservationRules;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 4.9 `after/src/test/java/edu/se506/lending/regression/Chapter06Checks.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.ConfirmationFormatter;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.application.port.NotificationException;
import edu.se506.lending.application.port.NotificationSender;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.domain.BorrowingPolicy;
import edu.se506.lending.domain.Reservation;
import edu.se506.lending.domain.ReservationRules;
import edu.se506.lending.domain.StaffReservationRules;
import edu.se506.lending.infrastructure.notification.ConsoleNotificationSender;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import edu.se506.lending.infrastructure.persistence.InMemoryReservationRepository;

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
                null, new ConfirmationFormatter(), inbox, new InMemoryReservationRepository()), "null policy map");
        expect(IllegalArgumentException.class, () -> new ReservationCoordinator(
                Map.of(BorrowerCategory.STUDENT, new ReservationRules()),
                new ConfirmationFormatter(), inbox, new InMemoryReservationRepository()), "missing staff policy");
        expect(NullPointerException.class, () -> new ReservationCoordinator(
                configured, null, inbox, new InMemoryReservationRepository()), "null formatter");
        expect(NullPointerException.class, () -> new ReservationCoordinator(
                configured, new ConfirmationFormatter(), null, new InMemoryReservationRepository()), "null sender");
        Map<BorrowerCategory, BorrowingPolicy> mutable = new EnumMap<>(configured);
        ReservationCoordinator copied = new ReservationCoordinator(mutable,
                new ConfirmationFormatter(), new RecordingNotificationSender(), new InMemoryReservationRepository());
        mutable.put(BorrowerCategory.STUDENT, (count, days) -> false);
        check(copied.reserve("B1", "CAM1", day, 1).startsWith("Confirmed:"),
                "caller map mutation cannot rewire coordinator");
        Map<BorrowerCategory, BorrowingPolicy> restrictive = new EnumMap<>(configured);
        restrictive.put(BorrowerCategory.STUDENT, (count, days) -> false);
        RecordingNotificationSender restrictedInbox = new RecordingNotificationSender();
        ReservationCoordinator restricted = new ReservationCoordinator(restrictive,
                new ConfirmationFormatter(), restrictedInbox, new InMemoryReservationRepository());
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

### 4.10 `after/src/test/java/edu/se506/lending/regression/DirectoryAdapterTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.application.port.DirectoryException;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.Borrower;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryAdapter;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryClient;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 4.11 `after/src/test/java/edu/se506/lending/regression/LegacyRegressionTest.java`

```java
package edu.se506.lending.regression;



import org.junit.jupiter.api.Test;

class LegacyRegressionTest {
    @Test void chapter02() { Chapter02Checks.main(new String[0]); }
    @Test void chapter03() { Chapter03AcceptanceExamples.main(new String[0]); }
    @Test void chapter05() { Chapter05Checks.main(new String[0]); }
    @Test void chapter06() { Chapter06Checks.main(new String[0]); }
}
```

### 4.12 `after/src/test/java/edu/se506/lending/regression/LoanServiceTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.LoanService;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.Loan;
import edu.se506.lending.domain.Reservation;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 4.13 `after/src/test/java/edu/se506/lending/regression/NotificationMockitoTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.application.port.NotificationException;
import edu.se506.lending.application.port.NotificationSender;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.Reservation;

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

### 4.14 `after/src/test/java/edu/se506/lending/regression/NotificationPublisherTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.port.NotificationException;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.LoanPeriod;
import edu.se506.lending.domain.Reservation;
import edu.se506.lending.infrastructure.notification.NotificationPublisher;

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

### 4.15 `after/src/test/java/edu/se506/lending/regression/ReserveEquipmentCommandTest.java`

```java
package edu.se506.lending.regression;

import edu.se506.lending.application.Command;
import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.application.ReserveEquipmentCommand;
import edu.se506.lending.application.port.DirectoryException;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.Borrower;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;

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

### 4.16 `after/src/test/java/edu/se506/lending/structure/DependencyRulesTest.java`

```java
package edu.se506.lending.structure;

import static org.junit.jupiter.api.Assertions.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.regex.Pattern;
import org.junit.jupiter.api.Test;

/** Checks compiled local dependency direction; not reflection or semantic correctness. */
class DependencyRulesTest {
    private static final String BASE = "edu.se506.lending.";
    private static final Pattern EDGE =
            Pattern.compile("(?m)^\\s*(edu\\.se506\\.lending\\.[\\w.$]+)\\s+->\\s+([\\w.$]+)\\s+.*$");

    @Test void compiledProductionDependenciesFollowDeclaredDirection() throws Exception {
        String output = jdepsOutput();
        var matcher = EDGE.matcher(output);
        int observed = 0;
        List<String> violations = new ArrayList<>();
        while (matcher.find()) {
            observed++;
            String from = matcher.group(1);
            String to = matcher.group(2);
            if (from.startsWith(BASE + "bootstrap.")) continue;
            if (to.startsWith("patterns.") || to.startsWith("behaviour.") || to.startsWith("examples.")) {
                violations.add(from + " -> " + to);
            } else if (to.startsWith(BASE) && !allowed(from, to)) {
                violations.add(from + " -> " + to);
            }
        }
        assertTrue(observed > 0, "jdeps must discover production class dependencies: " + output);
        assertTrue(violations.isEmpty(), String.join(System.lineSeparator(), violations));
    }

    @Test void productionPackagesHaveNoDependencyCycles() throws Exception {
        Map<String, Set<String>> graph = new TreeMap<>();
        var matcher = EDGE.matcher(jdepsOutput());
        while (matcher.find()) {
            String from = packageOf(matcher.group(1));
            String to = matcher.group(2).startsWith(BASE) ? packageOf(matcher.group(2)) : null;
            graph.computeIfAbsent(from, key -> new TreeSet<>());
            if (to != null && !to.equals(from)) graph.get(from).add(to);
        }
        assertTrue(graph.size() > 1, "jdeps must discover more than one production package");
        List<String> cycle = findCycle(graph);
        assertTrue(cycle.isEmpty(), "Package dependency cycle: " + String.join(" -> ", cycle));
    }

    private static String jdepsOutput() throws Exception {
        String executable = System.getProperty("os.name").toLowerCase().contains("win") ? "java.exe" : "java";
        String java = Path.of(System.getProperty("java.home"), "bin", executable).toString();
        Process process = new ProcessBuilder(java, "--module", "jdk.jdeps/com.sun.tools.jdeps.Main",
                "-verbose:class", "-filter:none", Path.of("target/classes").toAbsolutePath().toString())
                .redirectErrorStream(true).start();
        String output = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        assertEquals(0, process.waitFor(), output);
        return output;
    }

    private static String packageOf(String type) {
        String outer = type.contains("$") ? type.substring(0, type.indexOf('$')) : type;
        return outer.substring(0, outer.lastIndexOf('.'));
    }

    /** Depth-first search; returns the packages on one cycle, or an empty list. */
    private static List<String> findCycle(Map<String, Set<String>> graph) {
        Set<String> done = new HashSet<>();
        for (String start : graph.keySet()) {
            Deque<String> path = new ArrayDeque<>();
            List<String> found = visit(start, graph, path, done);
            if (!found.isEmpty()) return found;
        }
        return List.of();
    }

    private static List<String> visit(String node, Map<String, Set<String>> graph,
                                      Deque<String> path, Set<String> done) {
        if (path.contains(node)) {
            List<String> cycle = new ArrayList<>();
            boolean inCycle = false;
            for (String element : (Iterable<String>) path::descendingIterator) {
                if (element.equals(node)) inCycle = true;
                if (inCycle) cycle.add(element);
            }
            cycle.add(node);
            return cycle;
        }
        if (!done.add(node)) return List.of();
        path.push(node);
        for (String next : graph.getOrDefault(node, Set.of())) {
            List<String> found = visit(next, graph, path, done);
            if (!found.isEmpty()) return found;
        }
        path.pop();
        return List.of();
    }

    private boolean allowed(String from, String to) {
        if (from.startsWith(BASE + "domain.")) return to.startsWith(BASE + "domain.");
        if (from.startsWith(BASE + "application.port.")) {
            return to.startsWith(BASE + "application.port.") || to.startsWith(BASE + "domain.");
        }
        if (from.startsWith(BASE + "application.")) {
            return to.startsWith(BASE + "application.") || to.startsWith(BASE + "domain.");
        }
        if (from.startsWith(BASE + "infrastructure.")) {
            return to.startsWith(BASE + "infrastructure.") || to.startsWith(BASE + "application.")
                    || to.startsWith(BASE + "domain.");
        }
        if (from.startsWith(BASE + "presentation.")) {
            return to.startsWith(BASE + "presentation.") || to.startsWith(BASE + "application.")
                    || to.startsWith(BASE + "domain.");
        }
        return false;
    }
}
```

### 4.17 `after/src/test/java/edu/se506/lending/structure/RepositoryBoundaryTest.java`

```java
package edu.se506.lending.structure;

import static org.junit.jupiter.api.Assertions.*;
import edu.se506.lending.application.*;
import edu.se506.lending.application.port.*;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.*;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import edu.se506.lending.infrastructure.persistence.InMemoryReservationRepository;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

class RepositoryBoundaryTest {
    private final LocalDate start = LocalDate.of(2026,10,20);
    private Reservation record(String id, String item) {
        return new Reservation(id, "B1", item, new LoanPeriod(start, start.plusDays(2)));
    }
    @Test void snapshotsAreStableOrderedAndUnmodifiable() {
        var repository = new InMemoryReservationRepository();
        var empty = repository.findAll();
        var first = record("R1", "CAM1");
        var second = record("R2", "MIC1");
        repository.add(first);
        var earlier = repository.findAll();
        repository.add(second);
        assertTrue(empty.isEmpty());
        assertEquals(List.of(first), earlier);
        assertEquals(List.of(first, second), repository.findAll());
        assertThrows(UnsupportedOperationException.class, () -> earlier.clear());
    }
    @Test void duplicateIdentityDoesNotReplaceOriginal() {
        var repository = new InMemoryReservationRepository();
        var original = record("R1", "CAM1");
        repository.add(original);
        assertThrows(IllegalArgumentException.class, () -> repository.add(record("R1", "OTHER")));
        assertEquals(1, repository.findAll().size());
        assertSame(original, repository.findAll().get(0));
    }
    @Test void nullAdditionDoesNotChangeStore() {
        var repository = new InMemoryReservationRepository();
        assertThrows(NullPointerException.class, () -> repository.add(null));
        assertTrue(repository.findAll().isEmpty());
    }
    @Test void injectedStoreContainsAcceptanceBeforeNotification() {
        var repository = new InMemoryReservationRepository();
        var calls = new AtomicInteger();
        var coordinator = coordinator(repository, reservation -> {
            assertEquals(List.of(reservation), repository.findAll());
            calls.incrementAndGet();
        });
        assertTrue(coordinator.reserve("B1", "CAM1", start, 2).startsWith("Confirmed: R1"));
        assertEquals(repository.findAll(), coordinator.reservations());
        assertEquals(1, calls.get());
    }
    @Test void failingAddDoesNotReachNotification() {
        var failure = new IllegalStateException("store failed before append");
        ReservationRepository repository = new ReservationRepository() {
            public List<Reservation> findAll() { return List.of(); }
            public void add(Reservation reservation) { throw failure; }
        };
        var calls = new AtomicInteger();
        var coordinator = coordinator(repository, reservation -> calls.incrementAndGet());
        assertSame(failure, assertThrows(IllegalStateException.class, () -> coordinator.reserve("B1", "CAM1", start, 2)));
        assertTrue(coordinator.reservations().isEmpty());
        assertEquals(0, calls.get());
    }
    @Test void assemblyCreatesIndependentSessionStores() {
        var first = ReservationApplication.create(new RecordingNotificationSender());
        var second = ReservationApplication.create(new RecordingNotificationSender());
        first.reserve("B1", "CAM1", start, 2);
        assertTrue(second.reservations().isEmpty());
        assertTrue(second.reserve("B1", "CAM1", start, 2).startsWith("Confirmed: R1"));
    }
    @Test void coordinatorRequiresARepository() {
        var policies = Map.<BorrowerCategory, BorrowingPolicy>of(BorrowerCategory.STUDENT, new ReservationRules(),
                BorrowerCategory.STAFF, new StaffReservationRules());
        assertThrows(NullPointerException.class,
                () -> new ReservationCoordinator(policies, new ConfirmationFormatter(), reservation -> { }, null));
    }
    private ReservationCoordinator coordinator(ReservationRepository repository, NotificationSender sender) {
        return new ReservationCoordinator(Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                BorrowerCategory.STAFF, new StaffReservationRules()), new ConfirmationFormatter(), sender, repository);
    }
}
```

### 4.18 `after/src/test/java/edu/se506/lending/structure/ReservationConsoleTest.java`

```java
package edu.se506.lending.structure;

import static org.junit.jupiter.api.Assertions.*;
import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.application.port.DirectoryException;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.*;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import edu.se506.lending.presentation.ReservationConsole;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.Optional;
import org.junit.jupiter.api.Test;

class ReservationConsoleTest {
    @Test void printsExistingSuccessAndRejectionWithoutDuplicatingPolicy() {
        var buffer = new ByteArrayOutputStream();
        var coordinator = ReservationApplication.create(new RecordingNotificationSender());
        var service = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.STUDENT)), coordinator);
        var console = new ReservationConsole(service, new PrintStream(buffer, true, StandardCharsets.UTF_8));
        var start = LocalDate.of(2026,10,20);
        console.reserve("B1", "CAM1", start, 2);
        console.reserve("B1", "MIC1", start, 8);
        assertEquals("Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22)." + System.lineSeparator()
                + "Rejected: borrower limit or duration." + System.lineSeparator(), buffer.toString(StandardCharsets.UTF_8));
        assertEquals(1, coordinator.reservations().size());
    }
    @Test void staffRequestAboveTheStudentLimitIsDecidedByThePolicyNotTheConsole() {
        var buffer = new ByteArrayOutputStream();
        var coordinator = ReservationApplication.create(new RecordingNotificationSender());
        var service = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.STAFF)), coordinator);
        var console = new ReservationConsole(service, new PrintStream(buffer, true, StandardCharsets.UTF_8));
        console.reserve("T1", "CAM1", LocalDate.of(2026,10,20), 10);
        assertEquals("Confirmed: R1 for T1 on CAM1 [2026-10-20, 2026-10-30)." + System.lineSeparator(),
                buffer.toString(StandardCharsets.UTF_8));
    }
    @Test void directoryFailureDoesNotPrintSuccess() {
        var buffer = new ByteArrayOutputStream();
        var failure = new DirectoryException("offline");
        var coordinator = ReservationApplication.create(new RecordingNotificationSender());
        var service = new DirectoryReservationService(id -> { throw failure; }, coordinator);
        var console = new ReservationConsole(service, new PrintStream(buffer, true, StandardCharsets.UTF_8));
        assertSame(failure, assertThrows(DirectoryException.class,
                () -> console.reserve("B1", "CAM1", LocalDate.of(2026,10,20), 2)));
        assertEquals("", buffer.toString(StandardCharsets.UTF_8));
        assertTrue(coordinator.reservations().isEmpty());
    }
}
```

### 4.19 `after/src/test/java/edu/se506/lending/structure/ValueSemanticsTest.java`

```java
package edu.se506.lending.structure;

import static org.junit.jupiter.api.Assertions.*;
import edu.se506.lending.domain.LoanPeriod;
import examples.structure.PeriodValue;
import java.time.LocalDate;
import java.util.HashSet;
import java.util.List;
import org.junit.jupiter.api.Test;

class ValueSemanticsTest {
    @Test void separateValueExampleUsesDatesForEqualityAndHashing() {
        var start = LocalDate.of(2026,10,20);
        var first = new PeriodValue(start, start.plusDays(2));
        var same = new PeriodValue(start, start.plusDays(2));
        var different = new PeriodValue(start, start.plusDays(3));
        assertEquals(first, same);
        assertEquals(first.hashCode(), same.hashCode());
        assertEquals(2, new HashSet<>(List.of(first, same, different)).size());
        assertThrows(IllegalArgumentException.class, () -> new PeriodValue(start, start));
    }
    @Test void cumulativePeriodEqualityIsDeliberatelyUnchanged() {
        var start = LocalDate.of(2026,10,20);
        var first = new LoanPeriod(start, start.plusDays(2));
        var second = new LoanPeriod(start, start.plusDays(2));
        assertEquals(first.start(), second.start());
        assertEquals(first.endExclusive(), second.endExclusive());
        assertNotEquals(first, second);
    }
}
```

### 4.20 `after/src/test/java/patterns/PatternExamplesTest.java`

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

## 5. Build, documentation and architecture decision

The architecture decision is a reviewable example, with peer review explicitly pending.

### 5.1 `after/pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>edu.se506</groupId>
  <artifactId>equipment-lending</artifactId>
  <version>0.10.0</version>
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

### 5.4b `after/tools/PackageMetrics.java`

```java
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Prints afferent coupling (Ca), efferent coupling (Ce) and instability
 * I = Ce / (Ca + Ce) for each package of the compiled production classes.
 *
 * Counting unit: classes. Nested classes count with their outer class. Only
 * dependencies between this project's own packages are counted; the standard
 * library is ignored. When Ca + Ce is 0 the instability is undefined.
 *
 * Run from the project root after "mvn compile":
 *   java tools/PackageMetrics.java target/classes
 */
public final class PackageMetrics {
    private static final Pattern EDGE =
            Pattern.compile("(?m)^\\s+([\\w.$]+)\\s+->\\s+([\\w.$]+)\\s+\\S+\\s*$");

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.err.println("usage: java tools/PackageMetrics.java <classes directory>");
            System.exit(2);
        }
        String executable = System.getProperty("os.name").toLowerCase().contains("win") ? "java.exe" : "java";
        String java = Path.of(System.getProperty("java.home"), "bin", executable).toString();
        Process process = new ProcessBuilder(java, "--module", "jdk.jdeps/com.sun.tools.jdeps.Main",
                "-verbose:class", "-filter:none", Path.of(args[0]).toAbsolutePath().toString())
                .redirectErrorStream(true).start();
        String output = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        if (process.waitFor() != 0) {
            System.err.println(output);
            System.exit(1);
        }

        Map<String, Set<String>> classesIn = new TreeMap<>();
        Map<String, Set<String>> dependersOutside = new TreeMap<>();   // classes outside P that use P
        Map<String, Set<String>> dependersInside = new TreeMap<>();    // classes in P that use outside classes
        Matcher m = EDGE.matcher(output);
        while (m.find()) {
            String from = outer(m.group(1));
            String to = outer(m.group(2));
            if (!local(from)) continue;
            classesIn.computeIfAbsent(pkg(from), k -> new TreeSet<>()).add(from);
            if (!local(to)) continue;
            classesIn.computeIfAbsent(pkg(to), k -> new TreeSet<>()).add(to);
            if (!pkg(from).equals(pkg(to))) {
                dependersOutside.computeIfAbsent(pkg(to), k -> new TreeSet<>()).add(from);
                dependersInside.computeIfAbsent(pkg(from), k -> new TreeSet<>()).add(from);
            }
        }
        System.out.printf("%-48s %7s %4s %4s %9s%n", "package", "classes", "Ca", "Ce", "I");
        for (String p : classesIn.keySet()) {
            int ca = dependersOutside.getOrDefault(p, Set.of()).size();
            int ce = dependersInside.getOrDefault(p, Set.of()).size();
            String instability = ca + ce == 0 ? "undefined" : String.format("%.2f", ce / (double) (ca + ce));
            System.out.printf("%-48s %7d %4d %4d %9s%n", p, classesIn.get(p).size(), ca, ce, instability);
        }
    }

    private static boolean local(String type) {
        return type.startsWith("edu.se506.") || type.startsWith("patterns.")
                || type.startsWith("behaviour.") || type.startsWith("examples.");
    }

    private static String outer(String type) {
        int dollar = type.indexOf('$');
        return dollar < 0 ? type : type.substring(0, dollar);
    }

    private static String pkg(String type) {
        return type.substring(0, type.lastIndexOf('.'));
    }
}
```

### 5.5 `after/README.md`

````markdown
# Chapter 10 checkpoint

Use a full Java 17 JDK and Maven 3.9.11. The JDK must include jdk.jdeps for the compiled dependency test. Existing dependency and plugin versions are unchanged.

From this directory:

```bash
mvn --batch-mode verify
java -cp target/classes edu.se506.lending.bootstrap.Chapter10Demo
java -cp target/classes edu.se506.lending.bootstrap.Chapter09Demo
java -cp target/classes edu.se506.lending.bootstrap.Chapter08Demo
java -cp target/classes edu.se506.lending.bootstrap.Chapter07Demo
```

The full build executes 121 JUnit invocations: 107 migrated inherited cases, seven repository tests, two value-semantics tests, three console tests and two compiled dependency tests (direction and package cycles). Four inherited cases bridge older plain-Java runners. To print the package metrics used in the chapter, run `mvn --batch-mode compile` and then `java tools/PackageMetrics.java target/classes`.

Production classes now live under edu.se506.lending. Bootstrap chooses concrete implementations. Application and domain do not import infrastructure. Application ports depend only on domain and other ports. Infrastructure may depend on application, domain and infrastructure; presentation may depend on application, domain and presentation. Bootstrap may assemble all of them and launch explicitly isolated teaching examples.

ReservationCoordinator now requires a ReservationRepository as its fourth constructor argument. ReservationApplication.create(sender) retains its method shape in its new package and supplies a fresh InMemoryReservationRepository. Existing source/binary compatibility and old unqualified launcher names are not retained.

The existing result strings, policies, loan lifecycle and notification timing remain unchanged. The new console prints those existing results. Repository extraction does not introduce persistence, concurrency safety or transactionality.

The patterns and behaviour packages remain isolated examples. examples.structure.PeriodValue demonstrates record equality without replacing the cumulative LoanPeriod. ADR-010 is included in docs; its status is implemented teaching example, peer review pending.
````

### 5.6 `after/docs/ADR-010-application-structure.md`

````markdown
# ADR-010: Application structure and reservation storage boundary

Date: 13 October 2026
Status: Implemented teaching example; peer review pending.

## Context

The Chapter 9 application has useful class boundaries but mostly unnamed-package production code. ReservationCoordinator owns a concrete list. Concrete construction, storage ownership and permitted dependencies are not sufficiently visible for the growing example.

The change must retain the existing sequential use-case outcomes, policy limits, output strings, directory errors, notification timing and loan behaviour. Java package names, imports, launcher names and direct construction may change if documented.

## Decision

Use edu.se506.lending packages for domain, application, application.port, infrastructure, presentation and bootstrap. Application-owned ports express the directory, sender and reservation store contracts. Domain code has no dependencies on the other application packages. Bootstrap selects concrete adapters.

Extract ReservationRepository with findAll and add only. Its in-memory implementation provides insertion-ordered, stable unmodifiable snapshots and rejects null or duplicate IDs without replacing records. The coordinator receives the port as a fourth constructor argument. The usual factory supplies one fresh repository per coordinator/session.

Retain existing domain equality, size-based IDs, string results and loan storage. Keep the separate pattern/lifecycle exercises isolated. Add a thin console adapter and compiled dependency checks, for direction and for package cycles, using the JDK jdeps tool.

## Alternatives considered

- Keep the unnamed package and private list: less code, but weaker visibility of ownership and dependency direction as the example grows.
- Use narrow packages and one storage port: selected because it makes the current boundaries explicit without a framework.
- Introduce a generic CRUD repository, ORM, database or DI framework: declined because those capabilities are not required by this change.

## Consequences

Existing use-case outcomes remain protected by regression tests. Callers must update imports, direct coordinator construction and Java launcher names. The dependency test requires a full Java 17 JDK with jdk.jdeps. More files and one additional storage contract must be maintained.

The application remains sequential and in memory. A repository interface does not provide transactions, durable storage or concurrency safety. The factory's fresh-store ownership is important for the existing identifier scheme. Arbitrary preloaded/shared stores are not promised by this checkpoint.

ConfirmationFormatter remains application-owned to preserve result text. The console notification adapter may use it. Future structured results require a separate reviewed API decision.

## Validation and review

Run mvn --batch-mode verify, compare the earlier demonstration transcripts under their new fully qualified names, inspect compiled dependency directions and package cycles, and review repository ordering/snapshot/duplicate-ID behaviour.

Local author checks are reported in the chapter companion. No hosted CI run, opened PR or independent peer review is claimed. A learner's review must record actual feedback and its resolution.

## Revisit triggers

Persistent storage; multiple writers; a cancellation lifecycle; a new identifier scheme; adoption of value equality in the cumulative period; or structured application results. Each requires a concrete behaviour and compatibility analysis before implementation.
````

## 6. Worked explanation and evidence

### 6.1 The storage extraction

The Chapter 9 starting point was a coordinator-owned list. Chapter 10 replaces that field with a ReservationRepository reference and redirects reads and append through the port. Policy evaluation, date validation, conflict meaning, identifier calculation and notification handling stay in the coordinator.

The in-memory implementation uses a LinkedHashMap so duplicate-ID detection and ordered snapshots have a clear implementation. Duplicate keys are rejected rather than replacing the original record. The adapter does not calculate borrower limits or trigger notifications.

The standard factory preserves the previous ownership model by creating a new repository for each coordinator. The independent-session test verifies that reserving in one session neither populates another nor consumes its R1. The constructor injection point does not itself define a shared or persistent storage lifecycle.

### 6.2 Source direction versus runtime calls

ReservationCoordinator imports the application port. InMemoryReservationRepository implements that port. Bootstrap imports both the coordinator and the concrete adapter. At runtime, interface dispatch reaches the adapter selected by bootstrap; source dependency still points towards the port.

The infrastructure notification implementation also refers to ConfirmationFormatter in application. This is permitted by the declared matrix and preserves the current text contract. A review should describe that concrete dependency, rather than assuming every infrastructure reference goes only to an interface.

The domain classes do not import application or infrastructure. The compiled dependency test checks this local direction using jdeps output. It also prevents ordinary application code from importing an isolated pattern exercise. A bootstrap demo may refer to one explicitly, which is why the exception is narrow and documented.

### 6.3 The new presentation adapter

ReservationConsole delegates a request to DirectoryReservationService and prints the existing result. Its tests supply a PrintStream backed by a byte buffer. They observe one confirmation and one duration rejection, then verify that only the accepted request was stored.

A separate test makes the directory fail. The same exception propagates and the output buffer remains empty. The console does not manufacture a success message or silently substitute a category.

The class is intentionally small. It does not read input, manage authentication, catch every exception or implement a graphical interface. Those would be new product requirements. Bootstrap remains responsible for selecting examples and collaborators.

### 6.4 Equality, identity and snapshot observations

The repository duplicate-ID test creates two distinct Reservation objects with the same identifier and different item data. The second add rejects, and the original object remains stored. This uses explicit domain identity rather than relying on Reservation.equals.

ValueSemanticsTest makes the separate PeriodValue record's behaviour visible through equals, hashCode and a set. It also deliberately checks that running LoanPeriod objects with equal dates remain unequal under their inherited Java equality. That regression prevents the structural migration from silently adopting a new equality policy.

The repository snapshot test takes an empty snapshot, appends one record, takes another snapshot, and appends a second record. Both earlier snapshots remain unchanged, the new snapshot preserves insertion order, and mutation through the returned list is rejected. This promise relies on immutable values as well as an unmodifiable list.

### 6.5 New test inventory

| Test class | Invocations | Purpose |
|---|---:|---|
| RepositoryBoundaryTest | 7 | Snapshot semantics, duplicate/null rejection, storage-before-notification, failed add, independent sessions and a required repository |
| ValueSemanticsTest | 2 | Separate record equality and preserved running period equality |
| ReservationConsoleTest | 3 | Existing output contract, a staff request above the student limit, and unhidden directory failure |
| DependencyRulesTest | 2 | Compiled production references against the local package matrix; no package cycle |
| Migrated earlier suite | 107 | Existing policies, directory, loan, notification, pattern and lifecycle examples |
| Total | 121 | Complete version gate |

Three of these tests exist because the fault experiment in Section 11.2 found gaps. `coordinatorRequiresARepository` pins the constructor's null check. `staffRequestAboveTheStudentLimitIsDecidedByThePolicyNotTheConsole` sends a ten-day staff request through the console: a console test that used only a student would let a console that quietly enforced the seven-day rule itself pass. `productionPackagesHaveNoDependencyCycles` closes the gap that the layer matrix leaves inside one layer.

The failing-add example throws before storing anything. It establishes that notification follows a successful add in this implementation path. It does not establish the outcome of a database write whose acknowledgement is lost. Likewise, the architecture check establishes observed static relationships, not semantic correctness or runtime transactionality.

## 7. Suggested practical solution

### 7.1 A reviewable migration sequence

Start from the tested Chapter 9 version. Identify each class's responsibility before moving it. Introduce the package layout and update imports and launcher names. Keep the separate pattern and lifecycle exercises separate.

Extract the reservation storage port with the minimum operations needed by the coordinator. Move the concrete collection into its adapter. Update bootstrap and direct test constructions to pass that adapter explicitly. Avoid an application constructor that secretly creates infrastructure to retain the old signature.

Run the inherited tests with their expectations unchanged. Then add the repository contract tests, presentation tests and dependency gate. Compare earlier demonstration transcripts under their new launcher names. Write the decision record and ask a reviewer to inspect both behaviour preservation and dependency ownership.

The supplied files are a completed example of that organisation. They are not a claim that a particular Git history or peer review already exists. A learner's submission should retain its own actual diffs, commands and feedback.

### 7.2 Suggested architecture decision

The complete ADR-010 is included among the file listings. Its status is implemented teaching example, peer review pending. It records the unnamed-package and coordinator-owned-list starting point, the chosen narrow boundaries, alternatives declined and compatibility costs.

A valid alternative could keep the list inside the coordinator for a permanently small program. Another could place a repository contract in domain if a richer domain model genuinely owns that need. Evaluate those alternatives against actual responsibilities rather than treating the selected package name as the only valid answer.

The worked decision declines a database, generic CRUD framework and dependency-injection framework. Those choices avoid making storage and deployment commitments that the requirement did not request. They do not prevent a later reviewed change.

### 7.3 Draft PR description for learners to adapt

**Status: sample text only; no PR has been opened by this chapter.**

> The reservation use case has grown beyond a useful unnamed-package layout, and its coordinator directly owns concrete storage. This change introduces named responsibility packages, an application-owned reservation repository port and an in-memory adapter assembled at bootstrap.
>
> Existing policies, result strings, directory errors, loan behaviour and notification timing remain protected by regression tests. Callers must update imports, direct coordinator construction and fully qualified launcher names. The change adds a thin console adapter and a compiled dependency check.
>
> Validation includes the full Maven suite, repository contract checks, existing demonstration comparisons and inspection of the declared dependency directions. The example remains sequential and in memory; persistence, cancellation, identifier redesign and structured result objects are outside this change.
>
> Review should focus on ownership of the port, preservation of storage-before-notification ordering, snapshot semantics and whether each allowed dependency has a concrete reason.

Replace validation statements with the results for the actual submitted revision. Do not present this draft as an independent review or a hosted CI run.

### 7.4 Model answers: the book's project steps B1–B3

**B1. Classify.**

| Class | Package | May refer to | Must not refer to |
|---|---|---|---|
| `StaffReservationRules` | `domain` | `domain` | Any application, infrastructure or presentation class, for example `NotificationSender` |
| `LegacyDirectoryAdapter` | `infrastructure.directory` | `domain`, `application` (including its ports) and `infrastructure` | `presentation`, `bootstrap` or an isolated example |
| `DirectoryReservationService` | `application` | `domain`, `application.port` and `application` | Any infrastructure class, for example the adapter it receives through its constructor |
| `InMemoryReservationRepository` | `infrastructure.persistence` | `domain`, `application.port` and `infrastructure` | `presentation` or `bootstrap` |
| `ReservationApplication` | `bootstrap` | Every application package, and explicitly demonstrated examples | Nothing in the production matrix is forbidden, but it should hold no business rule |

**B2. Check the references.** A permitted reference in the compiled report is `infrastructure.directory.LegacyDirectoryAdapter -> application.port.BorrowerDirectory`: infrastructure may refer to the application's ports, and the adapter implements that contract. The reference that runs from `infrastructure.notification` to `application` is `ConsoleNotificationSender -> application.ConfirmationFormatter`. It exists because the console sender builds its notice text with the shared formatter, which preserves the existing wording.

**B3. Diagnose the package design.**

(a) Two possible change requests. *The console should print the borrower's name*: `presentation` only, if the service result already carries it, otherwise `application` too, which shows the string-result limitation. *Add an email notifier*: a new class in `infrastructure.notification` and one construction change in `bootstrap`; the coordinator and the domain are untouched. Accept any request for which the packages are named and the reason is given.

(b) The arrow is `infrastructure.notification` (I = 0.30) to `application` (I = 0.31). The difference is too small to act on by itself. What the arrow points at is the concrete dependency on `ConfirmationFormatter`. Reasonable options: leave it, because the formatter's output is part of the observable result; or introduce a small formatting port in `application.port` so that the sender depends only on a contract, at the cost of another interface. Either answer is acceptable if it names the trade-off.

(c) `ConfirmationFormatter` should stay in `application`. The coordinator needs it to build the returned text, so moving it into `infrastructure.notification` would make `application` depend on infrastructure, which is the same failure as moving `NotificationException` (Section 10.5 of the chapter). Moving it into `domain` would put wording in the domain. What would change the answer: a second notification format that needs its own formatter, or the dependency report showing more concrete application classes referenced from infrastructure.

**Experiment behind Option B in the chapter.** `NotificationException` was moved to `infrastructure.notification` in a copy and its imports changed. The direction test failed with `application.ReservationCoordinator -> infrastructure.notification.NotificationException`, and the cycle test failed with `application -> infrastructure.notification -> application`. Both tests together reject the placement.

### 7.5 Guidance for your team's project steps T1–T5

These are not model answers, because the content is your team's. They describe what a good answer shows.

- **T1 diagram.** Boxes are groups of packages, arrows are permitted references, and every arrow can be justified by one sentence. A good diagram marks at least one forbidden reference, and the dependency check or import review confirms that it does not occur. A weak diagram copies Figure 10.1 without checking it against the team's code.
- **T2 decision record.** The context names a problem someone could observe (for example, “the checkout class creates the payment client and cannot be tested”). The alternatives include doing nothing and say why it was rejected or accepted. The revisit trigger is an event, such as “when a second storage mechanism is needed”.
- **T3 restructuring.** Package moves and logic changes are separate commits or clearly separate parts of the diff, and the existing checks pass before and after.
- **T4 dependency evidence.** It says whether the check was compiled or manual, lists forbidden references found or states none were, and states whether a cycle search was made.
- **T5 review.** It records a real reviewer's comments and the response, and the Milestone 3 checklist status is honest about gaps.

## 8. AI activity solution

| Fictional claim | Finding | Evidence to inspect |
|---|---|---|
| A runtime call to the in-memory store proves an application import of infrastructure | Incorrect: interface dispatch and source references are different relationships | Coordinator's port field, bootstrap construction, jdeps edge |
| Put the repository interface in infrastructure | Not justified by this use case; it would make the consuming application depend on an infrastructure-owned contract | Port ownership and the declared dependency matrix |
| Every entity needs repository and service classes | No such requirement follows from identity | Actual access and orchestration needs; LoanPeriod has neither |
| An unmodifiable list makes every element immutable | Incorrect for mutable elements | List contract plus Reservation/LoanPeriod field semantics |
| Bootstrap must not import adapters | Incorrect for the selected composition role | Explicit assembly and absence of concrete construction in application |
| Passing tests establishes peer review | Incorrect evidence substitution | Actual reviewer comments and their resolution |

A dependency review should name the referencing type and referenced type. “Infrastructure coupling” without that trace is a claim to investigate. Conversely, legal imports do not prove appropriate responsibilities: a console can duplicate a policy using only standard Java types and still violate the intended design.

The offline example is author-written fictional AI output. If a live assistant is used, retain relevant actual output, independently inspect references and record accepted/rejected claims. No account or paid service is needed for the supplied exercise.

## 9. Intentionally flawed alternatives

These fragments are **diagnostic alternatives**, not additional files to compile alongside the final version. Each of them corresponds to a fault that was run in the experiment in Section 11.2.

### 9.1 Construct infrastructure inside the coordinator

```java
// WRONG for this chapter's declared application dependency rule:
private final ReservationRepository repository = new InMemoryReservationRepository();
```

Even if reservation behaviour appears unchanged, the application now names a concrete infrastructure type. The dependency check is designed to reject that compiled edge. Bootstrap should construct the implementation and pass the application-owned interface.

### 9.2 Expose mutable repository storage

```java
// WRONG for the stable, unmodifiable snapshot contract:
public List<Reservation> findAll() {
    return backingList;
}
```

Callers could change the store without its add checks, and later additions would appear through previously returned views. The final snapshot test checks both non-mutation and historical independence. An unmodifiable view of a live mutable list would still fail the latter promise.

### 9.3 Replace instead of reject duplicate identity

```java
// WRONG for append-only duplicate-ID rejection if used without the preceding check:
records.put(reservation.id(), reservation);
```

A second object with the same ID would replace the first. The final implementation checks for the existing key and rejects without mutation. If updates become a requirement, define their meaning and concurrency contract explicitly rather than changing this line under the name of refactoring.

### 9.4 Enforce the policy in the console

```java
// WRONG: the console now owns a policy that the domain already decides.
if (days > 7) { output.println("Rejected: borrower limit or duration."); return; }
```

A student request over seven days prints the right text, so the original console test cannot tell this from the correct console. A staff request of ten days, which the staff policy allows, is wrongly rejected. The console test in the final suite sends exactly that request.

## 10. Review answers and transfer solution

### 10.1 Concept answers

**1. Runtime and source direction:** the coordinator refers to ReservationRepository. Bootstrap supplies an object implementing that interface. At runtime a call reaches the concrete method through dispatch; the coordinator need not import the implementation. Static and runtime diagrams answer different questions.

**2. Service, policy and repository:** an application service coordinates a use case across collaborators. A domain policy expresses a rule such as count/duration eligibility. A repository provides access to stored domain records through a stated contract. None of these labels requires a remote service or a generic framework.

**3. Identity and equality:** R1 identifies the intended reservation independently of its current data. Immutable fields do not remove that identity. Java equality is a separate implementation choice; this Reservation class retains object equality, so storage keys by its explicit identifier. Value equality must likewise be implemented and tested, as the separate PeriodValue example demonstrates.

**4. Dependency evidence:** jdeps reports compiled class relationships, and the tests compare local edges with the selected matrix and search the package graph for cycles. They do not prove responsibilities are well chosen, inspect reflection, class names held in strings or configuration, or establish transactionality. Behaviour tests and review remain necessary.

### 10.2 Applied diagnosis answers

**5. Duplicated presentation policy:** the console and API can disagree if only one contains the copied seven-day check. Put the rule in the domain policy and delegate both entry points to the same application operation. A test can send the same student request through both entry points and compare outcomes and stored state. Also test an allowed staff duration to expose an over-general console rule that rejects every request above seven days.

**6. Duplicate IDs do not prevent concurrent booking conflicts:** two requests can both observe a free interval and then append different IDs. Even unique identifiers do not make the preceding eligibility/conflict checks and insertion atomic. Define a transaction, locking or constraint strategy appropriate to the real store and test the relevant concurrent outcome before claiming safety. That implementation is beyond this sequential version.

**7. Stability numbers at the extremes:** `bootstrap` has I = 1.00 because nothing depends on it, so it can change freely; that is appropriate for the place that chooses concrete classes. Changing it disturbs nobody else, but it must not accumulate business rules, which would then be hard to reuse or test. `domain` has I = 0.00 because sixteen classes depend on it and it depends on nothing else in the application. A change to it can ripple into every other package, so it is kept small and free of mechanisms. Neither number is a defect.

**8. Cycle between two infrastructure packages:** the cycle test catches it, because it searches the package graph. The direction test does not: the matrix lets infrastructure packages refer to each other, so each reference is individually permitted. The fault experiment in Section 11.2 confirms this: the direction test alone let the cycle pass.

### 10.3 Clinic appointment transfer

Keep appointment times, patient identity and eligibility rules in the domain vocabulary. Put the booking operation in application, with a patient-directory port and a focused appointment-store port as needed. Infrastructure adapts the provider and implements in-memory storage. Presentation delegates booking and presents its result; bootstrap selects concrete collaborators.

An appointment has an explicit identity, while its scheduled interval is a value. Do not assume those concepts automatically provide Java equals/hashCode. Specify the interval's validation and equality and the store's duplicate-ID behaviour.

The store contract belongs with the layer that defines its required capabilities. An application-owned port is a reasonable starting point for this small booking use case. Avoid generic operations that imply unagreed cancellation or modification rules.

One preserved behaviour is that a conflicting interval is rejected without storing another appointment or notifying anyone. Compare that outcome before and after restructuring. Provider failure versus missing patient is another useful distinction to preserve. No deployment services or real patient records are needed to demonstrate the design.

## 11. Instructor notes

### 11.1 Suggested demonstration and review

Show the coordinator's imports before drawing the runtime sequence. Ask students to identify where the concrete repository is selected. Then inspect the repository contract and the snapshot test. Use the duplicate-ID example to distinguish identity from Java object equality.

Run the thin console demonstration and the complete build. Ask students which test would detect a misplaced concrete dependency and which would detect altered overlap behaviour. Neither answer should rely only on a green summary line.

For Milestone 3, use the module leader's approved requirements. The chapter supplies a sample decision and PR description, but learners must obtain and record actual peer review. The sample is an example: it has no real reviewer and no hosted CI run behind it.

**The book's project and your team's project. Keep the two apart in class. The supplied version, ADR-010 and the sample PR description are the book's project: students read, trace and diagnose them (steps B1–B3) and are not asked to rebuild them. Milestone 3 evidence comes from each team's own repository (steps T1–T5). A team that copies ADR-010's decision has not shown its own architectural judgement; ask what problem in their code the decision solves. A team on another provided domain applies the same steps to that domain's starter codebase and uses the transfer challenge for orientation.

**Teaching the package-design material.** Start from the five change requests in Section 10.5 of the chapter and ask students to predict the packages that change before showing the answers. Then show the metrics table and ask which arrow is the odd one out. Resist the urge to turn the numbers into a score: the point is to decide what to examine. Show the `NotificationException` experiment only after students have argued for Option A or Option B.

### 11.2 Do the tests detect faults?

Twenty-five faults were introduced one at a time into copies of the project, and each copy was run through `mvn test`. They were first run before three tests were added: twenty were caught and five survived. The survivors were then run against the final tests.

| Area | Faults tried | Result before the three added tests | Result with the final tests |
|---|---|---|---|
| Repository contract | Duplicate id replaces the original; modifiable snapshot copy; live snapshot view; `HashMap` instead of insertion order | All four caught by `RepositoryBoundaryTest` or the inherited checks | Unchanged |
| Repository contract | Explicit null check removed | **Survived**: removing it still throws `NullPointerException`, from `reservation.id()`, so only the message differs | **Survives**: equivalent behaviour, deliberately not pinned by a message test |
| Coordinator | Stores after notification; `reservations()` returns a modifiable copy; identifier skips a number; conflict check ignores stored records | All four caught | Unchanged |
| Coordinator | Null repository accepted | **Survived**: no test constructed a coordinator without a repository | Caught by `coordinatorRequiresARepository` |
| Assembly | One repository shared by every session | Caught | Unchanged |
| Console | Prints without a newline; swallows directory failures | Both caught | Unchanged |
| Console | Duplicates the seven-day rule | **Survived**: the console test used only a student, for whom the duplicated rule gives the same output | Caught by `staffRequestAboveTheStudentLimitIsDecidedByThePolicyNotTheConsole` |
| Value objects | `PeriodValue` validation removed; `LoanPeriod` gains value equality | Both caught | Unchanged |
| Dependency direction | Application builds the concrete repository; domain refers to application; presentation refers to infrastructure; port refers to application; application refers to an isolated example; persistence refers to presentation; application refers to bootstrap | All seven caught by the direction test | Unchanged |
| Dependency cycle | `infrastructure.directory` and `infrastructure.notification` refer to each other | **Survived**: each reference is individually permitted by the matrix | Caught by `productionPackagesHaveNoDependencyCycles` |
| Dependency evasion | A class name held in a string | **Survived**: `jdeps` reads compiled references, not strings | **Survives**: a documented limit; review and behaviour tests must cover it |

Of the 25 faults, 20 were caught before the three tests were added, and 23 are caught by the final tests. The two that still survive are an equivalent mutant and a known limit of any bytecode-based dependency check. Different chapters used different fault sets, so these counts say nothing about how this suite compares with earlier ones. The seven-day-rule survivor and the cycle survivor are the most instructive: both tests were green, and both gaps were visible only when a plausible wrong implementation was tried.

Four inherited JUnit cases bridge to earlier plain-Java runners, and their counts remain distinct from JUnit invocations. Do not add them as if every unit were the same kind of test.

The results establish the supplied local scenarios and dependency rules. They do not establish persistence, authentication, concurrent consistency or universal behavioural equivalence for unseen consumers.

## References

Online references 1–5 checked 12 October 2026 and 7–8 on 13 October 2026; see the student chapter for source context.

1. Fowler, M., [Presentation Domain Data Layering](https://martinfowler.com/bliki/PresentationDomainDataLayering.html).
2. Stafford, R., [Service Layer](https://martinfowler.com/eaaCatalog/serviceLayer.html).
3. Hieatt, E. and Mee, R., [Repository](https://martinfowler.com/eaaCatalog/repository.html).
4. Cockburn, A., [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture).
5. Oracle, [Java 17 jdeps](https://docs.oracle.com/en/java/javase/17/docs/specs/man/jdeps.html) and [Java SE 17 List](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/List.html).
6. Martin, R. C., *Agile Software Development: Principles, Patterns, and Practices.* Prentice Hall, 2002. The Week 9 reading is its principles of package design. This book treats package design in Section 10.4 of Chapter 10.
7. Evans, E., [Domain-Driven Design Reference: Definitions and Pattern Summaries](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf). Domain Language, 2015 (CC BY 4.0). Layered Architecture p. 10, Entities p. 11, Value Objects p. 12; opened 13 October 2026.
8. Wikipedia, [Software package metrics](https://en.wikipedia.org/wiki/Software_package_metrics). Definitions of afferent coupling, efferent coupling and instability; opened 13 October 2026.