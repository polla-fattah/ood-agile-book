# Chapter 13: Code, Explanations and Solutions

*Integration, Delivery and Feedback*  
*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4

## 1. Scope and execution

This file accompanies `Chapter_13_Integration_Delivery_and_Feedback.md`. It contains the visiting-researcher change that Chapter 12 specified (CR-12), the two real boundaries it adds (an approval file and an HTTP directory client), the tests at three scopes, the pipeline and release scripts, a hosted-runner workflow, a decision record, the two tests of the AI activity, model solutions and the verification record.

**Version note.** Version 1.1 corrects three things found by an independent review of Chapters 12 to 15. (1) The HTTP client's timeout bounded the wait for the response headers and not the whole answer; the client now has a deadline on the whole lookup, and a new stub scenario and test cover a stalled body (Section 7.8). (2) Figure 13.3 showed the count and duration rules before the register was read; the figure now follows the code, and a test pins the order (Section 7.9). (3) Two statements about the simulated release are now explicit. The project version is 0.13.1 and the build runs 232 invocations (it was 0.13.0 and 230). The files that changed are `HttpLegacyDirectoryClient.java`, `DirectoryStub.java`, `DirectoryOutageIntegrationTest.java`, `VisitorAcceptanceTest.java`, `simulate-release.sh`, `ADR-013`, `README.md` and `pom.xml`. The results of Version 1.0 are not rewritten: the 27-fault experiment and the 230-invocation runs are recorded below as the earlier results.

**Input checkpoint.** The starting point is the Chapter 11 checkpoint: the Chapter 10 companion (Version 1.1) plus the new and changed files of the Chapter 11 companion (Version 1.1), which together give 159 JUnit invocations. To keep verified listings from being copied a third time, this file lists **only the files that are new or changed**. Every other file is exactly as in those two companions. Chapter 12 changes no code: its companion is not part of the checkpoint.

**What the change does.** A visiting researcher (borrower category `VISITOR`) may reserve CAM1 or CAM2 for one to three days when a sponsor approval, read from a tab-separated register, matches the exact borrower, item and period and is valid at the request instant. The behaviour is behind one flag that defaults to off. A missing approval is an expected rejection; an unreadable register or an unreachable directory is an operational failure that stops the request. Student and staff behaviour is unchanged. The decision record is `docs/ADR-013-visiting-researchers.md`.

**Boundary decision (Blueprint D1, interim).** The chapter's two real boundaries are a local file and a local HTTP stub service built on the JDK. The module leader has not yet decided D1; if a different boundary is chosen later (an embedded database, for example), the policy table of Section 2.3 and the tests stay, and the adapters change.

### 1.0 Checkpoint manifest

| Item | Value |
|---|---|
| Blueprint | Version 0.4 (the companions say they follow it) |
| Prerequisite 1 | `Chapter_10_Code_Explanations_and_Solutions.md`, Version 1.1, SHA-256 `fc3f7e8aa803a4f65fa5740084291759cff6700401f0c7870ac1e9e478c4ea9e` |
| Prerequisite 2 | `Chapter_11_Code_Explanations_and_Solutions.md`, Version 1.1, SHA-256 `96ee7dc6e8967dd2d669ee0317d8f42309dad254f23069b9da2379332b11cce3` |
| This companion | Version 1.1; project version 0.13.1 |
| Verified build | `mvn --batch-mode verify`: 232 invocations (203 unit, 26 integration, 3 end-to-end), JDK 24.0.2 with `--release 17`, Maven 3.9.11 |

The checksums identify the exact prerequisite files used on 13 October 2026. If either prerequisite is edited later, the checksum above must be refreshed and the reconstruction repeated.

### 1.1 Reconstruct the checkpoint

1. Create the directory `after`. Save every listing of the Chapter 10 companion (Version 1.1) at its path.
2. Save the new and changed listings of the Chapter 11 companion (Version 1.1, its Sections 3 to 6) at their paths. Where a path already exists, that listing replaces it.
3. Save every listing in Sections 3 to 6 of this file at its path. Where a path already exists (`pom.xml` and the three regression tests are edited in place by the hunks shown; the other files are replaced), this file wins. Apply the hunks of Sections 4.7 and 5.1 with `patch -p1` from inside `after`.
4. The files under `ai-activity/` are not compiled by Maven. To run them, copy them into `src/test/java/edu/se506/lending/aifixture/`.

Use a **full Java 17 JDK**, including the `jdk.jdeps` module, and Maven 3.9.11. The pinned versions are unchanged (JUnit Jupiter 5.13.4, Mockito 5.20.0, Compiler Plugin 3.14.1, Surefire 3.5.4); only the project version becomes 0.13.0. Initial builds need dependency access. Then, from inside `after`, run the whole pipeline or the single command:

```bash
bash scripts/pipeline.sh
mvn --batch-mode verify
```

### 1.2 Expected output

The pipeline prints a banner at the start and the end of each stage and stops at the first failing one. On the verification machine (Section 12.2) the passing run was:

```text
=== STAGE: 1 compile
=== PASSED: 1 compile (4 s)
=== STAGE: 2 unit tests and architecture checks
[INFO] Tests run: 203, Failures: 0, Errors: 0, Skipped: 0
=== PASSED: 2 unit tests and architecture checks (13 s)
=== STAGE: 3 integration tests (real file, real HTTP client, local stub service)
[INFO] Tests run: 26, Failures: 0, Errors: 0, Skipped: 0
=== PASSED: 3 integration tests (real file, real HTTP client, local stub service) (6 s)
=== STAGE: 4 end-to-end journeys (separate process)
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
=== PASSED: 4 end-to-end journeys (separate process) (6 s)
=== STAGE: 5 package
=== PASSED: 5 package (4 s)
PIPELINE PASSED
```

The times depend on the machine and on what Maven has cached; read the counts, not the seconds. The three end-to-end journeys check these lines from the separate process (flag off, then flag on):

```text
Visitors enabled: false
Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Visitor V1: Rejected: visitor reservations are not enabled.
Visitor V2: Rejected: visitor reservations are not enabled.
Unknown U9: Rejected: borrower not found or inactive.
Outage BROKEN: Unavailable: Borrower directory unavailable
Reservations: 1
Notices: 1
```

```text
Visitors enabled: true
Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Visitor V1: Confirmed: R2 for V1 on CAM2 [2026-10-20, 2026-10-22).
Visitor V2: Rejected: no valid sponsor approval.
Unknown U9: Rejected: borrower not found or inactive.
Outage BROKEN: Unavailable: Borrower directory unavailable
Reservations: 2
Notices: 2
```

`Chapter13Demo` needs a directory service and an approval file, so it is started by the journeys, which supply both. The demonstrations of earlier chapters print what they printed before.

### 1.3 Run one stage, or one test

```bash
mvn --batch-mode test -DexcludedGroups=integration,e2e     # stage 2: unit tests and architecture checks
mvn --batch-mode test -Dgroups=integration                 # stage 3
mvn --batch-mode test -Dgroups=e2e                         # stage 4
mvn --batch-mode test -Dtest=VisitorAcceptanceTest         # one class
```

A tag that selects nothing fails the stage. `mvn test -Dgroups=nosuchtag` ends with `No tests were executed!` and `BUILD FAILURE`, because the POM sets `failIfNoTests` to true (Section 12.2).

### 1.4 Run the simulated delivery

```bash
RELEASE_LABEL=v1 bash scripts/simulate-release.sh
RELEASE_LABEL=v2 bash scripts/simulate-release.sh
bash scripts/simulate-release.sh rollback
```

This is a **simulation**: staging is the folder `build/staging`, delivering is copying the jar, and the smoke test is the three end-to-end journeys run against the copied jar. Section 12.2 records the result.

## 2. Design map

### 2.1 What is new or changed

| Path | Status | Purpose |
|---|---|---|
| `src/main/java/edu/se506/lending/domain/BorrowerCategory.java` | Changed | Adds `VISITOR` |
| `src/main/java/edu/se506/lending/domain/VisitorReservationRules.java` | New | Count and duration policy only (up to three reservations, one to three days) |
| `src/main/java/edu/se506/lending/domain/ApprovalStatus.java` | New | `APPROVED` or `DENIED` |
| `src/main/java/edu/se506/lending/domain/ApprovalRecord.java` | New | One approval: exact request, validity window, `matches`, `validAt`, `approvesAt` |
| `src/main/java/edu/se506/lending/application/port/ApprovalSource.java` | New | Port: the record for one exact request, or empty |
| `src/main/java/edu/se506/lending/application/port/ApprovalSourceException.java` | New | Operational failure of the register |
| `src/main/java/edu/se506/lending/application/VisitorGate.java` | New | Flag, item allowlist and approval check; one clock read per request |
| `src/main/java/edu/se506/lending/application/DirectoryReservationService.java` | Changed | Three-argument constructor; visitors pass through the gate first |
| `src/main/java/edu/se506/lending/infrastructure/approvals/FileApprovalSource.java` | New | Real file adapter: whole-file validation, read afresh on every call |
| `src/main/java/edu/se506/lending/infrastructure/directory/HttpLegacyDirectoryClient.java` | New | Real HTTP client: bounded wait, one attempt, no retry, no fallback |
| `src/main/java/edu/se506/lending/infrastructure/directory/LegacyDirectoryClient.java` | Changed | Documents the failure contract; adds `Failure` |
| `src/main/java/edu/se506/lending/infrastructure/directory/LegacyDirectoryAdapter.java` | Changed | Maps `V` to `VISITOR`; turns a client failure into `DirectoryException` |
| `src/main/java/edu/se506/lending/bootstrap/ReservationApplication.java` | Changed | Wires the visitor policy |
| `src/main/java/edu/se506/lending/bootstrap/Chapter13Demo.java` | New | The runnable system; settings from system properties |
| `src/test/java/edu/se506/lending/visitor/*` | New | Rules, gate, the eighteen acceptance examples and a precedence test (41 invocations) |
| `src/test/java/edu/se506/lending/integration/*` | New | Stub service, interface contract, directory outage (including a stalled body) and file tests (29 invocations) |
| `src/test/java/edu/se506/lending/e2e/Chapter13JourneyE2ETest.java` | New | Three journeys against a separate process |
| `src/test/java/edu/se506/lending/regression/BehaviourStrategyTest.java`, `Chapter06Checks.java`, `structure/RepositoryBoundaryTest.java` | Changed | The policy map gains the visitor entry; no assertion changed |
| `pom.xml`, `README.md` | Changed | Version 0.13.0; description of the checkpoint |
| `scripts/pipeline.sh`, `scripts/simulate-release.sh` | New | Five-stage pipeline; simulated delivery and rollback |
| `.github/workflows/pipeline.yml` | New | The same stages as a hosted-runner workflow (not run) |
| `docs/ADR-013-visiting-researchers.md` | New | Decision, alternatives, flag removal plan, rollback |
| `ai-activity/*` | New | The proposed and the repaired test of Section 13.9 |

### 2.2 Which test runs in which stage

| Stage | Selection | Invocations | Contents |
|---|---|---|---|
| 2 Unit tests and architecture checks | Everything not tagged `integration` or `e2e` | 203 | The 159 inherited invocations, the 41 visitor tests and the 3 fixture contract invocations |
| 3 Integration | `@Tag("integration")` | 26 | `FileApprovalSourceIntegrationTest` (13), `DirectoryOutageIntegrationTest` (10), `HttpDirectoryClientContractTest` (3) |
| 4 End-to-end | `@Tag("e2e")` | 3 | `Chapter13JourneyE2ETest` |

The total is 232 invocations: 159 inherited and 73 new (41 + 3 + 26 + 3).

### 2.3 The directory failure policy

This table is the policy the HTTP client implements. Each row has a test.

| What the client sees | What the client does | Test |
|---|---|---|
| 200 with one line, kind and status | Returns the row | `anOrdinaryStudentRequestWorksThroughTheRealHttpClient` |
| 404 | Returns no row; the adapter reports the borrower as not found | `aMissingRowIsAnOrdinaryRejection` |
| 500 or any other status | Fails; no retry | `aServerErrorIsAnOutageNotANotFoundAndIsNotRetried` |
| No answer at all within the bounded wait | Fails with a timeout | `aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest` |
| Headers and the first byte promptly, then the body stalls | Fails with a timeout after the same overall wait; never returns the late body | `aStalledBodyIsAFailureWithinTheOverallWait` |
| Connection refused | Fails | `aRefusedConnectionIsAnOutage` |
| A body that is not exactly two fields | Fails | `aMalformedAnswerIsAnOutageNotAGuess` |
| An unknown kind code | Fails at the adapter; never defaulted to student or staff | `anUnknownCategoryCodeIsNeverDefaultedToStaffOrStudent` |

**Policy: one attempt, a bounded wait, no retry and no fallback answer.** The wait bounds the whole lookup, including the time to receive the body. It is a constructor argument; the demonstration passes its own `lending.directory.timeout.millis`.

### 2.4 The outcomes of a visitor request

| Situation | Result | Kind |
|---|---|---|
| Flag off | `Rejected: visitor reservations are not enabled.`; the register is not read | Expected rejection |
| Item not CAM1 or CAM2 | Rejected; the register is not read | Expected rejection |
| Fewer than one or more than three days, or three reservations already retained | Rejected by the existing policy and count rules | Expected rejection |
| No record, a denied record, or a record for a different borrower, item or period | `Rejected: no valid sponsor approval.` | Expected rejection |
| Record valid at the request instant (`validFrom` inclusive, `validUntil` exclusive) | Continues to the existing availability, reservation and notification steps | Success |
| Register missing, unreadable, malformed or with a duplicate key | `ApprovalSourceException`; nothing is reserved or sent | Operational failure |
| Directory unreachable, slow or nonsensical | `DirectoryException`; nothing is reserved or sent | Operational failure |

### 2.5 Regression carry-forward

Adding `VISITOR` to the enum has one deliberate consequence: the coordinator requires a policy for every category, so a construction that lists every category needs one more entry. This happened in four constructions in three test files (Section 4.7). **No assertion changed.** The inherited 159 invocations passed unchanged after those four edits. The assertions carried forward from Chapters 3–9 (Section 2.5 of the Chapter 10 companion) are untouched.

## 3. New and changed production listings

### 3.1 `after/src/main/java/edu/se506/lending/domain/BorrowerCategory.java`

```java
package edu.se506.lending.domain;



public enum BorrowerCategory {
    STUDENT, STAFF, VISITOR
}
```

### 3.2 `after/src/main/java/edu/se506/lending/domain/VisitorReservationRules.java`

```java
package edu.se506.lending.domain;

/**
 * Illustrative teaching rule for visiting researchers (change request CR-12): fewer than three
 * retained reservations, and one to three calendar days. It decides count and duration only;
 * sponsor approval is checked elsewhere, because this contract has no identity, item or clock.
 */
public final class VisitorReservationRules implements BorrowingPolicy {
    @Override
    public boolean mayRequest(int activeReservations, int requestedDays) {
        return activeReservations >= 0
                && activeReservations < 3
                && requestedDays >= 1
                && requestedDays <= 3;
    }
}
```

### 3.3 `after/src/main/java/edu/se506/lending/domain/ApprovalStatus.java`

```java
package edu.se506.lending.domain;

/** A sponsor's decision on one request. Any other word in the register is a data error. */
public enum ApprovalStatus {
    APPROVED, DENIED
}
```

### 3.4 `after/src/main/java/edu/se506/lending/domain/ApprovalRecord.java`

```java
package edu.se506.lending.domain;

import java.time.Instant;
import java.time.LocalDate;
import java.util.Objects;

/**
 * A trusted sponsor decision for one exact request: borrower, item and half-open loan period.
 * The record is valid for requests made at or after {@code validFrom} and strictly before
 * {@code validUntil}. The loan period itself need not lie inside that window.
 */
public record ApprovalRecord(String borrowerId, String itemId, LocalDate start, LocalDate endExclusive,
                             String sponsorId, ApprovalStatus status, Instant validFrom, Instant validUntil) {

    public ApprovalRecord {
        requireText(borrowerId, "borrowerId");
        requireText(itemId, "itemId");
        requireText(sponsorId, "sponsorId");
        Objects.requireNonNull(start, "start");
        Objects.requireNonNull(endExclusive, "endExclusive");
        Objects.requireNonNull(status, "status");
        Objects.requireNonNull(validFrom, "validFrom");
        Objects.requireNonNull(validUntil, "validUntil");
        if (!start.isBefore(endExclusive)) {
            throw new IllegalArgumentException("Loan period must end after it starts.");
        }
        if (!validFrom.isBefore(validUntil)) {
            throw new IllegalArgumentException("Validity must end after it starts.");
        }
    }

    /** True only for the exact borrower, item and period; approval for anything else is not enough. */
    public boolean matches(String borrower, String item, LocalDate periodStart, LocalDate periodEnd) {
        return borrowerId.equals(borrower) && itemId.equals(item)
                && start.equals(periodStart) && endExclusive.equals(periodEnd);
    }

    /** Equality at the start of the window is valid; equality at its end is not. */
    public boolean validAt(Instant now) {
        Objects.requireNonNull(now, "now");
        return !now.isBefore(validFrom) && now.isBefore(validUntil);
    }

    public boolean approvesAt(Instant now) {
        return status == ApprovalStatus.APPROVED && validAt(now);
    }

    private static void requireText(String value, String name) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(name + " must not be blank.");
        }
    }
}
```

### 3.5 `after/src/main/java/edu/se506/lending/application/port/ApprovalSource.java`

```java
package edu.se506.lending.application.port;

import edu.se506.lending.domain.ApprovalRecord;
import java.time.LocalDate;
import java.util.Optional;

/**
 * Finds the sponsor approval recorded for one exact request. Empty means that no record exists
 * for it. A source that cannot give a trustworthy answer (unreadable, malformed, ambiguous) must
 * throw {@link ApprovalSourceException}, never return empty.
 */
@FunctionalInterface
public interface ApprovalSource {
    Optional<ApprovalRecord> find(String borrowerId, String itemId, LocalDate start, LocalDate endExclusive);
}
```

### 3.6 `after/src/main/java/edu/se506/lending/application/port/ApprovalSourceException.java`

```java
package edu.se506.lending.application.port;

/** The approval register could not be read or trusted. This is not a sponsor's rejection. */
public final class ApprovalSourceException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    public ApprovalSourceException(String message) { super(message); }
    public ApprovalSourceException(String message, Throwable cause) { super(message, cause); }
}
```

### 3.7 `after/src/main/java/edu/se506/lending/application/VisitorGate.java`

```java
package edu.se506.lending.application;

import edu.se506.lending.application.port.ApprovalSource;
import edu.se506.lending.domain.ApprovalRecord;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;

/**
 * The extra checks for a visiting researcher, kept apart from the count and duration policy: the
 * feature flag, the item allowlist and a matching sponsor approval that is valid at one request-time
 * instant. It returns a rejection text, or empty when the request may go on to the coordinator.
 * An unreadable or untrustworthy approval register is not a rejection: the exception from the
 * source is not caught here, so no reservation can follow it.
 */
public final class VisitorGate {
    public static final String DISABLED = "Rejected: visitor reservations are not enabled.";
    public static final String ITEM_NOT_ALLOWED = "Rejected: item not available to visitors.";
    public static final String NOT_APPROVED = "Rejected: no valid sponsor approval.";

    private static final Set<String> ALLOWED_ITEMS = Set.of("CAM1", "CAM2");

    private final ApprovalSource source;
    private final Clock clock;
    private final boolean enabled;

    public VisitorGate(ApprovalSource source, Clock clock, boolean enabled) {
        this.source = Objects.requireNonNull(source, "source");
        this.clock = Objects.requireNonNull(clock, "clock");
        this.enabled = enabled;
    }

    /** A gate for applications that have not enabled visitors: the approval source is never read. */
    public static VisitorGate disabled() {
        return new VisitorGate((borrowerId, itemId, start, end) -> {
            throw new IllegalStateException("The approval source must not be read while visitors are disabled.");
        }, Clock.systemUTC(), false);
    }

    public Optional<String> rejection(String borrowerId, String itemId, LocalDate start, int days) {
        if (!enabled) {
            return Optional.of(DISABLED);
        }
        if (!ALLOWED_ITEMS.contains(itemId)) {
            return Optional.of(ITEM_NOT_ALLOWED);
        }
        if (days < 1) {
            return Optional.empty();      // there is no period to look up; the policy rejects it
        }
        Instant now = clock.instant();    // one request-time instant for the whole decision
        LocalDate endExclusive = start.plusDays(days);
        Optional<ApprovalRecord> record = source.find(borrowerId, itemId, start, endExclusive);
        // The source should return only the exact request, but approval for anything else is never enough.
        if (record.isEmpty() || !record.get().matches(borrowerId, itemId, start, endExclusive)
                || !record.get().approvesAt(now)) {
            return Optional.of(NOT_APPROVED);
        }
        return Optional.empty();
    }
}
```

### 3.8 `after/src/main/java/edu/se506/lending/application/DirectoryReservationService.java`

```java
package edu.se506.lending.application;

import edu.se506.lending.application.port.BorrowerDirectory;
import edu.se506.lending.application.port.DirectoryException;
import edu.se506.lending.domain.Borrower;
import edu.se506.lending.domain.BorrowerCategory;

import java.time.LocalDate;
import java.util.Objects;
import java.util.Optional;

/** Directory-backed entry point; this does not authenticate the caller. */
public final class DirectoryReservationService {
    private final BorrowerDirectory directory;
    private final ReservationCoordinator coordinator;
    private final VisitorGate visitorGate;

    public DirectoryReservationService(BorrowerDirectory directory,
                                       ReservationCoordinator coordinator) {
        this(directory, coordinator, VisitorGate.disabled());
    }

    public DirectoryReservationService(BorrowerDirectory directory,
                                       ReservationCoordinator coordinator,
                                       VisitorGate visitorGate) {
        this.directory = Objects.requireNonNull(directory, "directory");
        this.coordinator = Objects.requireNonNull(coordinator, "coordinator");
        this.visitorGate = Objects.requireNonNull(visitorGate, "visitorGate");
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
        if (borrower.category() == BorrowerCategory.VISITOR) {
            Optional<String> rejection = visitorGate.rejection(borrower.id(), itemId, start, days);
            if (rejection.isPresent()) return rejection.get();
        }
        return coordinator.reserve(borrower.id(), itemId, start, days, borrower.category());
    }
}
```

### 3.9 `after/src/main/java/edu/se506/lending/infrastructure/approvals/FileApprovalSource.java`

```java
package edu.se506.lending.infrastructure.approvals;

import edu.se506.lending.application.port.ApprovalSource;
import edu.se506.lending.application.port.ApprovalSourceException;
import edu.se506.lending.domain.ApprovalRecord;
import edu.se506.lending.domain.ApprovalStatus;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;

/**
 * Reads the sponsor-approval register: a local UTF-8 tab-separated file with exactly eight columns
 * (borrowerId, itemId, start, endExclusive, sponsorId, status, validFrom, validUntil) and a header.
 * The file is read afresh on every call and is rejected as a whole if any row is invalid or if two
 * rows share a request key. It is a trusted, sequential fixture, not a concurrent approval database.
 */
public final class FileApprovalSource implements ApprovalSource {
    static final String HEADER =
            "borrowerId\titemId\tstart\tendExclusive\tsponsorId\tstatus\tvalidFrom\tvalidUntil";

    private final Path file;

    public FileApprovalSource(Path file) {
        this.file = Objects.requireNonNull(file, "file");
    }

    @Override
    public Optional<ApprovalRecord> find(String borrowerId, String itemId, LocalDate start, LocalDate endExclusive) {
        List<ApprovalRecord> records = readAll();
        for (ApprovalRecord record : records) {
            if (record.matches(borrowerId, itemId, start, endExclusive)) {
                return Optional.of(record);
            }
        }
        return Optional.empty();
    }

    private List<ApprovalRecord> readAll() {
        List<String> lines;
        try {
            lines = Files.readAllLines(file, StandardCharsets.UTF_8);
        } catch (IOException failure) {
            throw new ApprovalSourceException("Approval register cannot be read: " + file.getFileName(), failure);
        }
        if (lines.isEmpty() || !HEADER.equals(lines.get(0))) {
            throw new ApprovalSourceException("Approval register has no valid header row.");
        }
        List<ApprovalRecord> records = new ArrayList<>();
        Set<String> keys = new HashSet<>();
        for (int i = 1; i < lines.size(); i++) {
            int row = i + 1;
            ApprovalRecord record = parse(lines.get(i), row);
            String key = record.borrowerId() + "|" + record.itemId() + "|" + record.start() + "|" + record.endExclusive();
            if (!keys.add(key)) {
                throw new ApprovalSourceException("Duplicate approval request key at row " + row + ".");
            }
            records.add(record);
        }
        return List.copyOf(records);
    }

    private static ApprovalRecord parse(String line, int row) {
        String[] columns = line.split("\t", -1);
        if (columns.length != 8) {
            throw new ApprovalSourceException("Row " + row + " has " + columns.length + " columns, not 8.");
        }
        try {
            return new ApprovalRecord(columns[0], columns[1], LocalDate.parse(columns[2]), LocalDate.parse(columns[3]),
                    columns[4], status(columns[5], row), Instant.parse(columns[6]), Instant.parse(columns[7]));
        } catch (DateTimeParseException | IllegalArgumentException bad) {
            throw new ApprovalSourceException("Row " + row + " is not a valid approval record.", bad);
        }
    }

    private static ApprovalStatus status(String text, int row) {
        return switch (text) {
            case "APPROVED" -> ApprovalStatus.APPROVED;
            case "DENIED" -> ApprovalStatus.DENIED;
            default -> throw new ApprovalSourceException("Row " + row + " has an unknown status.");
        };
    }
}
```

### 3.10 `after/src/main/java/edu/se506/lending/infrastructure/directory/LegacyDirectoryClient.java`

```java
package edu.se506.lending.infrastructure.directory;

/** Illustrative provider contract, not an actual university API. See HttpLegacyDirectoryClient for a network client. */
@FunctionalInterface
public interface LegacyDirectoryClient {
    // null means no row; codes are exact and case-sensitive.
    Person lookup(String key);

    record Person(String key, String kind, String status) { }

    final class Failure extends RuntimeException {
        private static final long serialVersionUID = 1L;

        public Failure(String message) { super(message); }
        public Failure(String message, Throwable cause) { super(message, cause); }
    }
}
```

### 3.11 `after/src/main/java/edu/se506/lending/infrastructure/directory/LegacyDirectoryAdapter.java`

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
        else if ("V".equals(row.kind())) category = BorrowerCategory.VISITOR;
        else throw new DirectoryException("Unsupported borrower category");
        if ("N".equals(row.status())) return Optional.empty();
        if (!"Y".equals(row.status())) throw new DirectoryException("Unsupported borrower status");
        return Optional.of(new Borrower(row.key(), category));
    }
}
```

### 3.12 `after/src/main/java/edu/se506/lending/infrastructure/directory/HttpLegacyDirectoryClient.java`

```java
package edu.se506.lending.infrastructure.directory;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * Asks a directory service over HTTP: {@code GET <base>/borrowers/<key>}. A 200 response carries one
 * line, the provider's kind and status separated by a tab. A 404 means there is no such row. Everything
 * else is a failure: a timeout, a refused connection, any other status and a body that is not exactly
 * two fields. Policy: one attempt, a bounded wait, no retry and no fallback answer. The wait bounds the
 * whole lookup, including the time to receive the body: the request timeout of the JDK client is not
 * documented to cover the body, and a server that sends its headers and then stalls would otherwise hold
 * the caller for as long as it likes. A caller that cannot get an answer must fail, because an outage
 * must never look like a missing borrower.
 */
public final class HttpLegacyDirectoryClient implements LegacyDirectoryClient {
    private final HttpClient http;
    private final URI base;
    private final Duration requestTimeout;

    public HttpLegacyDirectoryClient(URI base, Duration connectTimeout, Duration requestTimeout) {
        this.base = Objects.requireNonNull(base, "base");
        this.requestTimeout = Objects.requireNonNull(requestTimeout, "requestTimeout");
        this.http = HttpClient.newBuilder()
                .connectTimeout(Objects.requireNonNull(connectTimeout, "connectTimeout"))
                .build();
    }

    @Override
    public Person lookup(String key) {
        URI uri = URI.create(base.toString().replaceAll("/+$", "") + "/borrowers/"
                + URLEncoder.encode(key, StandardCharsets.UTF_8));
        HttpRequest request = HttpRequest.newBuilder(uri).timeout(requestTimeout).GET().build();
        CompletableFuture<HttpResponse<String>> pending =
                http.sendAsync(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
        HttpResponse<String> response;
        try {
            response = pending.get(requestTimeout.toNanos(), TimeUnit.NANOSECONDS);
        } catch (TimeoutException late) {
            pending.cancel(true);   // asks the client to drop the exchange; the caller does not wait for it
            throw new Failure("Directory did not answer within " + requestTimeout.toMillis() + " ms.", late);
        } catch (InterruptedException interrupted) {
            pending.cancel(true);
            Thread.currentThread().interrupt();
            throw new Failure("Directory request was interrupted.", interrupted);
        } catch (ExecutionException failed) {
            Throwable cause = failed.getCause() == null ? failed : failed.getCause();
            throw new Failure("Directory unavailable: " + cause.getClass().getSimpleName(), cause);
        }
        if (response.statusCode() == 404) {
            return null;
        }
        if (response.statusCode() != 200) {
            throw new Failure("Directory answered with status " + response.statusCode() + ".");
        }
        String[] fields = response.body().strip().split("\t", -1);
        if (fields.length != 2) {
            throw new Failure("Directory answered with a malformed row.");
        }
        return new Person(key, fields[0], fields[1]);
    }
}
```

### 3.13 `after/src/main/java/edu/se506/lending/bootstrap/ReservationApplication.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.ConfirmationFormatter;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.application.port.NotificationSender;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.domain.ReservationRules;
import edu.se506.lending.domain.StaffReservationRules;
import edu.se506.lending.domain.VisitorReservationRules;
import edu.se506.lending.infrastructure.notification.ConsoleNotificationSender;
import edu.se506.lending.infrastructure.persistence.InMemoryReservationRepository;

import java.time.LocalDate;
import java.util.Map;

public final class ReservationApplication {
    private ReservationApplication() { }

    public static ReservationCoordinator create(NotificationSender sender) {
        return new ReservationCoordinator(
                Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
                       BorrowerCategory.STAFF, new StaffReservationRules(),
                       BorrowerCategory.VISITOR, new VisitorReservationRules()),
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

### 3.14 `after/src/main/java/edu/se506/lending/bootstrap/Chapter13Demo.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.application.VisitorGate;
import edu.se506.lending.application.port.ApprovalSourceException;
import edu.se506.lending.application.port.DirectoryException;
import edu.se506.lending.infrastructure.approvals.FileApprovalSource;
import edu.se506.lending.infrastructure.directory.HttpLegacyDirectoryClient;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryAdapter;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import java.net.URI;
import java.nio.file.Path;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;

/**
 * The runnable system for Chapter 13: a directory service reached over HTTP, a sponsor-approval file
 * and one feature flag. Settings are system properties so that a test can start it as a separate process:
 * lending.directory.url (required), lending.approvals.file (required), lending.visitors (default false),
 * lending.now (an ISO instant, default the system clock) and lending.directory.timeout.millis (default 1000).
 */
public final class Chapter13Demo {
    public static void main(String[] args) {
        URI directoryUrl = URI.create(required("lending.directory.url"));
        Path approvals = Path.of(required("lending.approvals.file"));
        boolean visitorsEnabled = Boolean.parseBoolean(System.getProperty("lending.visitors", "false"));
        String now = System.getProperty("lending.now");
        Clock clock = now == null ? Clock.systemUTC() : Clock.fixed(Instant.parse(now), ZoneOffset.UTC);
        long timeoutMillis = Long.parseLong(System.getProperty("lending.directory.timeout.millis", "1000"));

        var sender = new RecordingNotificationSender();
        ReservationCoordinator coordinator = ReservationApplication.create(sender);
        var directory = new LegacyDirectoryAdapter(new HttpLegacyDirectoryClient(
                directoryUrl, Duration.ofMillis(timeoutMillis), Duration.ofMillis(timeoutMillis)));
        var gate = new VisitorGate(new FileApprovalSource(approvals), clock, visitorsEnabled);
        var service = new DirectoryReservationService(directory, coordinator, gate);

        LocalDate start = LocalDate.of(2026, 10, 20);
        System.out.println("Visitors enabled: " + visitorsEnabled);
        attempt("Student B1", service, "B1", "CAM1", start, 2);
        attempt("Visitor V1", service, "V1", "CAM2", start, 2);
        attempt("Visitor V2", service, "V2", "CAM2", start, 2);
        attempt("Unknown U9", service, "U9", "MIC1", start, 1);
        attempt("Outage BROKEN", service, "BROKEN", "MIC1", start, 1);
        System.out.println("Reservations: " + coordinator.reservations().size());
        System.out.println("Notices: " + sender.received().size());
    }

    private static void attempt(String label, DirectoryReservationService service,
                                String borrower, String item, LocalDate start, int days) {
        String outcome;
        try {
            outcome = service.reserve(borrower, item, start, days);
        } catch (DirectoryException failure) {
            outcome = "Unavailable: " + failure.getMessage();
        } catch (ApprovalSourceException failure) {
            outcome = "Approval register unavailable: " + failure.getMessage();
        }
        System.out.println(label + ": " + outcome);
    }

    private static String required(String property) {
        String value = System.getProperty(property);
        if (value == null || value.isBlank()) {
            throw new IllegalStateException("Missing system property " + property);
        }
        return value;
    }
}
```

## 4. New and changed test listings

### 4.1 `after/src/test/java/edu/se506/lending/visitor/VisitorRulesTest.java`

```java
package edu.se506.lending.visitor;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.domain.ApprovalRecord;
import edu.se506.lending.domain.ApprovalStatus;
import edu.se506.lending.domain.VisitorReservationRules;
import java.time.Instant;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

/** Unit tests for the visitor count and duration rule and for the approval record's own rules. */
class VisitorRulesTest {
    private static final LocalDate START = LocalDate.of(2026, 10, 20);
    private static final Instant FROM = Instant.parse("2026-10-18T00:00:00Z");
    private static final Instant UNTIL = Instant.parse("2026-10-20T00:00:00Z");

    private static ApprovalRecord record(ApprovalStatus status) {
        return new ApprovalRecord("V1", "CAM1", START, START.plusDays(2), "S1", status, FROM, UNTIL);
    }

    @ParameterizedTest
    @CsvSource({"0,1,true", "2,3,true", "0,2,true", "3,1,false", "0,4,false", "0,0,false", "-1,1,false", "0,-1,false"})
    void countAndDurationBoundaries(int count, int days, boolean expected) {
        assertEquals(expected, new VisitorReservationRules().mayRequest(count, days));
    }

    @Test void equalityAtTheStartOfTheWindowIsValidAndAtTheEndIsNot() {
        ApprovalRecord approved = record(ApprovalStatus.APPROVED);
        assertTrue(approved.validAt(FROM));
        assertTrue(approved.validAt(UNTIL.minusSeconds(1)));
        assertFalse(approved.validAt(UNTIL));
        assertFalse(approved.validAt(FROM.minusSeconds(1)));
    }

    @Test void onlyAnApprovedStatusApprovesAndOnlyInsideTheWindow() {
        Instant inside = Instant.parse("2026-10-19T12:00:00Z");
        assertTrue(record(ApprovalStatus.APPROVED).approvesAt(inside));
        assertFalse(record(ApprovalStatus.DENIED).approvesAt(inside));
        assertFalse(record(ApprovalStatus.APPROVED).approvesAt(UNTIL));
    }

    @Test void aRecordMatchesOnlyTheExactBorrowerItemAndPeriod() {
        ApprovalRecord approved = record(ApprovalStatus.APPROVED);
        LocalDate end = START.plusDays(2);
        assertTrue(approved.matches("V1", "CAM1", START, end));
        assertFalse(approved.matches("V2", "CAM1", START, end));
        assertFalse(approved.matches("V1", "CAM2", START, end));
        assertFalse(approved.matches("V1", "CAM1", START.plusDays(1), end));
        assertFalse(approved.matches("V1", "CAM1", START, end.plusDays(1)));
    }

    @Test void anInvalidRecordCannotBeBuilt() {
        assertThrows(IllegalArgumentException.class, () ->
                new ApprovalRecord("V1", "CAM1", START, START.plusDays(2), " ", ApprovalStatus.APPROVED, FROM, UNTIL));
        assertThrows(IllegalArgumentException.class, () ->
                new ApprovalRecord("V1", "CAM1", START, START, "S1", ApprovalStatus.APPROVED, FROM, UNTIL));
        assertThrows(IllegalArgumentException.class, () ->
                new ApprovalRecord("V1", "CAM1", START, START.plusDays(2), "S1", ApprovalStatus.APPROVED, UNTIL, UNTIL));
        assertThrows(NullPointerException.class, () ->
                new ApprovalRecord("V1", "CAM1", START, START.plusDays(2), "S1", null, FROM, UNTIL));
    }
}
```

### 4.2 `after/src/test/java/edu/se506/lending/visitor/VisitorGateTest.java`

```java
package edu.se506.lending.visitor;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.application.VisitorGate;
import edu.se506.lending.application.port.ApprovalSource;
import edu.se506.lending.application.port.ApprovalSourceException;
import edu.se506.lending.domain.ApprovalRecord;
import edu.se506.lending.domain.ApprovalStatus;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

/** Unit tests for the visitor gate with a controlled approval source and clock. */
class VisitorGateTest {
    private static final LocalDate START = LocalDate.of(2026, 10, 20);
    private static final Instant FROM = Instant.parse("2026-10-18T00:00:00Z");
    private static final Instant UNTIL = Instant.parse("2026-10-20T00:00:00Z");
    private static final Instant NOW = Instant.parse("2026-10-19T12:00:00Z");

    private final AtomicInteger reads = new AtomicInteger();

    private ApprovalSource sourceOf(ApprovalRecord record) {
        return (borrower, item, start, end) -> {
            reads.incrementAndGet();
            return Optional.ofNullable(record);
        };
    }

    private static ApprovalRecord record(ApprovalStatus status) {
        return new ApprovalRecord("V1", "CAM1", START, START.plusDays(2), "S1", status, FROM, UNTIL);
    }

    private VisitorGate gate(ApprovalRecord record, Instant now, boolean enabled) {
        return new VisitorGate(sourceOf(record), Clock.fixed(now, ZoneOffset.UTC), enabled);
    }

    @Test void aMatchingApprovedRecordInsideItsWindowLetsTheRequestContinue() {
        assertEquals(Optional.empty(), gate(record(ApprovalStatus.APPROVED), NOW, true).rejection("V1", "CAM1", START, 2));
        assertEquals(1, reads.get());
    }

    @Test void aDisabledGateRejectsWithoutReadingTheSource() {
        assertEquals(Optional.of(VisitorGate.DISABLED),
                gate(record(ApprovalStatus.APPROVED), NOW, false).rejection("V1", "CAM1", START, 2));
        assertEquals(0, reads.get());
    }

    @Test void anItemOutsideTheAllowlistIsRejectedWithoutReadingTheSource() {
        assertEquals(Optional.of(VisitorGate.ITEM_NOT_ALLOWED),
                gate(record(ApprovalStatus.APPROVED), NOW, true).rejection("V1", "MIC1", START, 2));
        assertEquals(0, reads.get());
    }

    @Test void aNonPositiveDurationIsLeftToThePolicyWithoutReadingTheSource() {
        VisitorGate gate = gate(record(ApprovalStatus.APPROVED), NOW, true);
        assertEquals(Optional.empty(), gate.rejection("V1", "CAM1", START, 0));
        assertEquals(Optional.empty(), gate.rejection("V1", "CAM1", START, -2));
        assertEquals(0, reads.get());
    }

    @Test void aMissingOrDeniedRecordIsAnExpectedRejection() {
        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(null, NOW, true).rejection("V1", "CAM1", START, 2));
        assertEquals(Optional.of(VisitorGate.NOT_APPROVED),
                gate(record(ApprovalStatus.DENIED), NOW, true).rejection("V1", "CAM1", START, 2));
    }

    @Test void theWindowIncludesItsStartAndExcludesItsEnd() {
        ApprovalRecord approved = record(ApprovalStatus.APPROVED);
        assertEquals(Optional.empty(), gate(approved, FROM, true).rejection("V1", "CAM1", START, 2));
        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(approved, UNTIL, true).rejection("V1", "CAM1", START, 2));
        assertEquals(Optional.of(VisitorGate.NOT_APPROVED),
                gate(approved, FROM.minusSeconds(1), true).rejection("V1", "CAM1", START, 2));
    }

    @Test void aSourceThatReturnsADifferentRequestDoesNotApprove() {
        ApprovalRecord other = new ApprovalRecord("V2", "CAM1", START, START.plusDays(2), "S1",
                ApprovalStatus.APPROVED, FROM, UNTIL);
        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(other, NOW, true).rejection("V1", "CAM1", START, 2));
    }

    @Test void anOperationalFailureOfTheSourceIsNotCaught() {
        ApprovalSourceException failure = new ApprovalSourceException("register unreadable");
        VisitorGate gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC), true);
        assertSame(failure, assertThrows(ApprovalSourceException.class, () -> gate.rejection("V1", "CAM1", START, 2)));
    }

    @Test void oneRequestReadsTheClockOnce() {
        AtomicInteger instants = new AtomicInteger();
        Clock counting = new Clock() {
            @Override public ZoneId getZone() { return ZoneOffset.UTC; }
            @Override public Clock withZone(ZoneId zone) { return this; }
            @Override public Instant instant() { instants.incrementAndGet(); return NOW; }
        };
        new VisitorGate(sourceOf(record(ApprovalStatus.APPROVED)), counting, true).rejection("V1", "CAM1", START, 2);
        assertEquals(1, instants.get());
    }

    @Test void theDisabledFactoryNeverReadsASource() {
        assertEquals(Optional.of(VisitorGate.DISABLED), VisitorGate.disabled().rejection("V1", "CAM1", START, 2));
    }
}
```

### 4.3 `after/src/test/java/edu/se506/lending/visitor/VisitorAcceptanceTest.java`

```java
package edu.se506.lending.visitor;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.application.LoanService;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.application.VisitorGate;
import edu.se506.lending.application.port.ApprovalSourceException;
import edu.se506.lending.application.port.BorrowerDirectory;
import edu.se506.lending.application.port.NotificationException;
import edu.se506.lending.bootstrap.LoanSnapshotRows;
import edu.se506.lending.bootstrap.OverdueReportService;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.domain.ApprovalRecord;
import edu.se506.lending.domain.ApprovalStatus;
import edu.se506.lending.domain.Borrower;
import edu.se506.lending.domain.BorrowerCategory;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * The acceptance matrix of change request CR-12 (examples AC1 to AC18), run through the real
 * directory service, coordinator, repository and loan service with a controlled directory,
 * approval source and clock. Each test builds its own fixture so one failure cannot mask another.
 */
class VisitorAcceptanceTest {
    private static final LocalDate START = LocalDate.of(2026, 10, 20);
    private static final Instant FROM = Instant.parse("2026-10-18T00:00:00Z");
    private static final Instant UNTIL = Instant.parse("2026-10-20T00:00:00Z");
    private static final Instant NOW = Instant.parse("2026-10-19T12:00:00Z");
    private static final String SUCCESS_V1_CAM1 = "Confirmed: R1 for V1 on CAM1 [2026-10-20, 2026-10-22).";
    private static final String LIMIT = "Rejected: borrower limit or duration.";

    private Locale savedLocale;

    @BeforeEach void pinTheLocale() { savedLocale = Locale.getDefault(); Locale.setDefault(Locale.ROOT); }
    @AfterEach void restoreTheLocale() { Locale.setDefault(savedLocale); }

    /** A complete small system with a controlled directory, approval list, clock and sender. */
    private static final class World {
        final List<ApprovalRecord> approvals = new ArrayList<>();
        final AtomicInteger approvalReads = new AtomicInteger();
        final RecordingNotificationSender sender = new RecordingNotificationSender();
        final ReservationCoordinator coordinator;
        final DirectoryReservationService service;

        World(boolean enabled, Instant now, edu.se506.lending.application.port.NotificationSender notifier) {
            coordinator = ReservationApplication.create(notifier);
            BorrowerDirectory directory = id -> switch (id) {
                case "V1", "V2" -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR));
                case "S1" -> Optional.of(new Borrower(id, BorrowerCategory.STUDENT));
                case "T1" -> Optional.of(new Borrower(id, BorrowerCategory.STAFF));
                default -> Optional.empty();
            };
            VisitorGate gate = new VisitorGate((borrower, item, start, end) -> {
                approvalReads.incrementAndGet();
                return approvals.stream().filter(r -> r.matches(borrower, item, start, end)).findFirst();
            }, Clock.fixed(now, ZoneOffset.UTC), enabled);
            service = new DirectoryReservationService(directory, coordinator, gate);
        }

        World(boolean enabled, Instant now) { this(enabled, now, new RecordingNotificationSender()); }

        World approve(String borrower, String item, LocalDate start, int days) {
            approvals.add(new ApprovalRecord(borrower, item, start, start.plusDays(days), "S1",
                    ApprovalStatus.APPROVED, FROM, UNTIL));
            return this;
        }
    }

    private static void assertNothingChanged(World w) {
        assertTrue(w.coordinator.reservations().isEmpty());
    }

    @Test void ac1_aVisitorWithAMatchingApprovalReservesCam1ForTwoDays() {
        var recorder = new RecordingNotificationSender();
        var w = new World(true, NOW, recorder).approve("V1", "CAM1", START, 2);
        assertEquals(SUCCESS_V1_CAM1, w.service.reserve("V1", "CAM1", START, 2));
        assertEquals(1, w.coordinator.reservations().size());
        assertEquals(1, recorder.received().size());
    }

    @Test void ac2_cam2ForThreeDaysNeedsItsOwnRecordAndIsAllowed() {
        var w = new World(true, NOW).approve("V1", "CAM2", START, 3);
        assertEquals("Confirmed: R1 for V1 on CAM2 [2026-10-20, 2026-10-23).", w.service.reserve("V1", "CAM2", START, 3));
    }

    @Test void ac3_fourDaysIsRejectedEvenWithAMatchingRecord() {
        var recorder = new RecordingNotificationSender();
        var w = new World(true, NOW, recorder).approve("V1", "CAM1", START, 4);
        assertEquals(LIMIT, w.service.reserve("V1", "CAM1", START, 4));
        assertNothingChanged(w);
        assertTrue(recorder.received().isEmpty());
    }

    @Test void ac4_zeroOrNegativeDaysIsRejectedWithoutReadingTheRegister() {
        var recorder = new RecordingNotificationSender();
        var w = new World(true, NOW, recorder).approve("V1", "CAM1", START, 2);
        assertEquals(LIMIT, w.service.reserve("V1", "CAM1", START, 0));
        assertEquals(LIMIT, w.service.reserve("V1", "CAM1", START, -1));
        assertNothingChanged(w);
        assertEquals(0, w.approvalReads.get());
        assertTrue(recorder.received().isEmpty());
    }

    @Test void ac5_anItemOutsideTheAllowlistIsRejectedEvenWithAMatchingRecord() {
        var w = new World(true, NOW).approve("V1", "MIC1", START, 2);
        assertEquals(VisitorGate.ITEM_NOT_ALLOWED, w.service.reserve("V1", "MIC1", START, 2));
        assertNothingChanged(w);
    }

    @Test void ac6_aMissingOrDeniedApprovalIsAnExpectedRejection() {
        var missing = new World(true, NOW);
        assertEquals(VisitorGate.NOT_APPROVED, missing.service.reserve("V1", "CAM1", START, 2));
        assertNothingChanged(missing);
        var denied = new World(true, NOW);
        denied.approvals.add(new ApprovalRecord("V1", "CAM1", START, START.plusDays(2), "S1",
                ApprovalStatus.DENIED, FROM, UNTIL));
        assertEquals(VisitorGate.NOT_APPROVED, denied.service.reserve("V1", "CAM1", START, 2));
        assertNothingChanged(denied);
    }

    @Test void ac7_anApprovalForAnotherBorrowerItemOrPeriodDoesNotAuthorise() {
        var w = new World(true, NOW).approve("V2", "CAM1", START, 2).approve("V1", "CAM2", START, 2)
                .approve("V1", "CAM1", START, 3);
        assertEquals(VisitorGate.NOT_APPROVED, w.service.reserve("V1", "CAM1", START, 2));
        assertNothingChanged(w);
    }

    @Test void ac8_theRequestInstantEqualToValidFromIsValid() {
        var w = new World(true, FROM).approve("V1", "CAM1", START, 2);
        assertEquals(SUCCESS_V1_CAM1, w.service.reserve("V1", "CAM1", START, 2));
    }

    @Test void ac9_theRequestInstantAtValidUntilOrBeforeValidFromIsRejected() {
        var atExpiry = new World(true, UNTIL).approve("V1", "CAM1", START, 2);
        assertEquals(VisitorGate.NOT_APPROVED, atExpiry.service.reserve("V1", "CAM1", START, 2));
        var early = new World(true, FROM.minusSeconds(1)).approve("V1", "CAM1", START, 2);
        assertEquals(VisitorGate.NOT_APPROVED, early.service.reserve("V1", "CAM1", START, 2));
        assertNothingChanged(atExpiry);
        assertNothingChanged(early);
    }

    @Test void ac10_anUnreadableApprovalRegisterIsAnOperationalFailureNotARejection() {
        var recorder = new RecordingNotificationSender();
        var coordinator = ReservationApplication.create(recorder);
        ApprovalSourceException failure = new ApprovalSourceException("register unreadable");
        var gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC), true);
        var service = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), coordinator, gate);
        assertSame(failure, assertThrows(ApprovalSourceException.class, () -> service.reserve("V1", "CAM1", START, 2)));
        assertTrue(coordinator.reservations().isEmpty());
        assertTrue(recorder.received().isEmpty());
    }

    @Test void precedence_theRegisterIsReadBeforeTheCountAndDurationRulesApply() {
        var recorder = new RecordingNotificationSender();
        var coordinator = ReservationApplication.create(recorder);
        ApprovalSourceException failure = new ApprovalSourceException("register unreadable");
        var gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC), true);
        var service = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), coordinator, gate);
        // Four days breaks the duration rule, but the gate reads the register first, so the failure is what the caller sees.
        assertSame(failure, assertThrows(ApprovalSourceException.class, () -> service.reserve("V1", "CAM1", START, 4)));
        // Zero days is left to the coordinator: the register is not read and the limit rejection is returned.
        assertEquals(LIMIT, service.reserve("V1", "CAM1", START, 0));
        assertTrue(coordinator.reservations().isEmpty());
        assertTrue(recorder.received().isEmpty());
    }

    @Test void ac11_threeRetainedReservationsBlockAFourthEvenAfterLoansAreReturned() {
        Clock checkoutDay = Clock.fixed(Instant.parse("2026-10-20T09:00:00Z"), ZoneOffset.UTC);
        var w = new World(true, NOW);
        var loans = new LoanService(w.coordinator, checkoutDay);
        for (int i = 0; i < 3; i++) {
            assertTrue(w.coordinator.reserve("V1", "CAM" + (1 + i % 2), START.plusDays(10L * i), 1, BorrowerCategory.VISITOR)
                    .startsWith("Confirmed"));
        }
        loans.checkOut("R1");
        loans.returnLoan("R1");
        w.approve("V1", "CAM1", START.plusDays(40), 1);
        assertEquals(LIMIT, w.service.reserve("V1", "CAM1", START.plusDays(40), 1));
        assertEquals(3, w.coordinator.reservations().size());
    }

    @Test void ac12_aDisabledFlagRejectsExplicitlyWithoutReadingTheRegister() {
        var w = new World(false, NOW).approve("V1", "CAM1", START, 2);
        assertEquals(VisitorGate.DISABLED, w.service.reserve("V1", "CAM1", START, 2));
        assertEquals(0, w.approvalReads.get());
        assertNothingChanged(w);
        var defaultService = new DirectoryReservationService(
                id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), ReservationApplication.create(new RecordingNotificationSender()));
        assertEquals(VisitorGate.DISABLED, defaultService.reserve("V1", "CAM1", START, 2));
    }

    @Test void ac13_studentAndStaffBehaviourIsUnchangedUnderEitherSettingAndNeverReadsTheRegister() {
        for (boolean enabled : new boolean[] {false, true}) {
            var w = new World(enabled, NOW);
            assertEquals("Confirmed: R1 for S1 on CAM1 [2026-10-20, 2026-10-27).", w.service.reserve("S1", "CAM1", START, 7));
            assertEquals("Confirmed: R2 for T1 on MIC1 [2026-10-20, 2026-11-03).", w.service.reserve("T1", "MIC1", START, 14));
            assertEquals("Rejected: borrower limit or duration.", w.service.reserve("S1", "CAM2", START, 8));
            assertEquals(0, w.approvalReads.get());
        }
    }

    @Test void ac14_anOverlapWithAnExistingReservationIsRejectedByTheExistingRule() {
        var w = new World(true, NOW).approve("V1", "CAM1", START, 2);
        assertTrue(w.coordinator.reserve("S1", "CAM1", START, 2).startsWith("Confirmed: R1"));
        assertEquals("Rejected: item unavailable.", w.service.reserve("V1", "CAM1", START, 2));
        assertEquals(1, w.coordinator.reservations().size());
    }

    @Test void ac15_anExpectedNotificationFailureLeavesTheVisitorReservationInPlace() {
        var w = new World(true, NOW, reservation -> { throw new NotificationException("outbox down"); })
                .approve("V1", "CAM1", START, 2);
        assertEquals(SUCCESS_V1_CAM1 + " Notification failed; reservation retained.", w.service.reserve("V1", "CAM1", START, 2));
        assertEquals(1, w.coordinator.reservations().size());
    }

    @Test void ac16_aVisitorReservationStaysUsableAfterTheApprovalExpiresAndTheFlagIsOff() {
        Clock checkoutDay = Clock.fixed(Instant.parse("2026-10-20T09:00:00Z"), ZoneOffset.UTC);
        var w = new World(true, NOW).approve("V1", "CAM1", START, 2);
        assertEquals(SUCCESS_V1_CAM1, w.service.reserve("V1", "CAM1", START, 2));
        var afterwards = new DirectoryReservationService(
                id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), w.coordinator, VisitorGate.disabled());
        assertEquals(VisitorGate.DISABLED, afterwards.reserve("V1", "CAM2", START, 1));
        var loans = new LoanService(w.coordinator, checkoutDay);
        assertTrue(loans.checkOut("R1").active());
        assertFalse(loans.returnLoan("R1").active());
    }

    @Test void ac17_anInactiveOrUnknownBorrowerIsRejectedAsBefore() {
        var w = new World(true, NOW).approve("U9", "CAM1", START, 2);
        assertEquals("Rejected: borrower not found or inactive.", w.service.reserve("U9", "CAM1", START, 2));
        assertEquals(0, w.approvalReads.get());
        assertNothingChanged(w);
    }

    @Test void ac18_aVisitorLoanInTheOverdueReportKeepsTheExistingKindRuleSd11_1() {
        Clock checkoutDay = Clock.fixed(Instant.parse("2026-10-20T09:00:00Z"), ZoneOffset.UTC);
        Clock reportDay = Clock.fixed(Instant.parse("2026-10-22T09:00:00Z"), ZoneOffset.UTC);
        var w = new World(true, NOW).approve("V1", "CAM1", START, 2);
        assertEquals(SUCCESS_V1_CAM1, w.service.reserve("V1", "CAM1", START, 2));
        var loans = new LoanService(w.coordinator, checkoutDay);
        loans.checkOut("R1");
        var rows = new LoanSnapshotRows(loans::loans, w.coordinator::reservations, borrower -> "V");
        // The legacy report knows only S and T. Any other kind pays 1.00 a day (suspected defect SD-11-1,
        // pinned in Chapter 11 and not fixed here), so a visitor one day late is fined 1.00.
        assertEquals("OVERDUE REPORT 2026-10-22\nCAM1 V1 1 day(s) late, fine 1.00\n1 overdue, total fines 1.00\n",
                new OverdueReportService(rows, reportDay).report());
    }
}
```

### 4.4 `after/src/test/java/edu/se506/lending/integration/DirectoryStub.java`

```java
package edu.se506.lending.integration;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * A controlled local directory service for tests: the JDK's own HTTP server on the loopback
 * address and a free port. Known keys answer with a kind and a status separated by a tab. The key
 * "SLOW" waits before sending anything until the stub is closed, "SLOWBODY" sends its headers and the
 * first byte of the body and then holds the rest until the stub is closed, "BROKEN" answers 500 and
 * "GARBAGE" answers with a body that is not two fields. Everything else is 404. It is a stand-in for a real provider, not the provider.
 */
public final class DirectoryStub implements AutoCloseable {
    private final HttpServer server;
    private final CountDownLatch release = new CountDownLatch(1);
    private volatile int requests;

    public DirectoryStub() throws IOException {
        server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        server.createContext("/borrowers/", this::handle);
        server.start();
    }

    public URI baseUri() {
        return URI.create("http://127.0.0.1:" + server.getAddress().getPort());
    }

    public int requests() {
        return requests;
    }

    private void handle(HttpExchange exchange) throws IOException {
        requests++;
        String key = exchange.getRequestURI().getPath().substring("/borrowers/".length());
        int status = 200;
        boolean stallBody = false;
        String body;
        switch (key) {
            case "B1" -> body = "S\tY";
            case "T1" -> body = "T\tY";
            case "V1", "V2" -> body = "V\tY";
            case "VOFF" -> body = "V\tN";
            case "ODD" -> body = "X\tY";
            case "GARBAGE" -> body = "only-one-field";
            case "BROKEN" -> { status = 500; body = "server error"; }
            case "SLOW" -> {
                awaitRelease();
                body = "S\tY";
            }
            case "SLOWBODY" -> {
                stallBody = true;
                body = "S\tY";
            }
            default -> { status = 404; body = "none"; }
        }
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        try {
            exchange.sendResponseHeaders(status, bytes.length);
            if (stallBody) {
                exchange.getResponseBody().write(bytes, 0, 1);
                exchange.getResponseBody().flush();
                awaitRelease();
                exchange.getResponseBody().write(bytes, 1, bytes.length - 1);
            } else {
                exchange.getResponseBody().write(bytes);
            }
        } catch (IOException clientGone) {
            // the client gave up (a timeout test); nothing more to send
        } finally {
            exchange.close();
        }
    }

    private void awaitRelease() {
        try {
            release.await(30, TimeUnit.SECONDS);
        } catch (InterruptedException interrupted) {
            Thread.currentThread().interrupt();
        }
    }

    @Override public void close() {
        release.countDown();
        server.stop(0);
    }
}
```

### 4.5 The directory contract

#### 4.5.1 `after/src/test/java/edu/se506/lending/integration/DirectoryClientContract.java`

```java
package edu.se506.lending.integration;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.infrastructure.directory.LegacyDirectoryClient;
import org.junit.jupiter.api.Test;

/**
 * The behavioural contract that every {@link LegacyDirectoryClient} must honour, written once and run
 * against each implementation: the in-memory fixture the earlier chapters used and the real HTTP client.
 * A contract test says what callers may rely on. It does not prove that a real provider honours it.
 */
abstract class DirectoryClientContract {
    /** A client that answers "S" and "Y" for the key B1 and has no row for the key NONE. */
    abstract LegacyDirectoryClient client() throws Exception;

    /** A client for which every lookup fails because the provider cannot be reached or understood. */
    abstract LegacyDirectoryClient failingClient() throws Exception;

    @Test void aKnownKeyReturnsItsRowWithTheKeyItWasAskedFor() throws Exception {
        LegacyDirectoryClient.Person row = client().lookup("B1");
        assertEquals(new LegacyDirectoryClient.Person("B1", "S", "Y"), row);
    }

    @Test void anUnknownKeyReturnsNullAndIsNotAFailure() throws Exception {
        assertNull(client().lookup("NONE"));
    }

    @Test void aProviderThatCannotAnswerFailsAndNeverReturnsAnEmptyAnswer() throws Exception {
        LegacyDirectoryClient failing = failingClient();
        assertThrows(LegacyDirectoryClient.Failure.class, () -> failing.lookup("B1"));
    }
}
```

#### 4.5.2 `after/src/test/java/edu/se506/lending/integration/FixtureDirectoryClientContractTest.java`

```java
package edu.se506.lending.integration;

import edu.se506.lending.infrastructure.directory.LegacyDirectoryClient;

/** The contract run against the in-memory fixture that earlier chapters used. */
class FixtureDirectoryClientContractTest extends DirectoryClientContract {
    @Override LegacyDirectoryClient client() {
        return key -> "B1".equals(key) ? new LegacyDirectoryClient.Person("B1", "S", "Y") : null;
    }

    @Override LegacyDirectoryClient failingClient() {
        return key -> { throw new LegacyDirectoryClient.Failure("fixture provider is down"); };
    }
}
```

#### 4.5.3 `after/src/test/java/edu/se506/lending/integration/HttpDirectoryClientContractTest.java`

```java
package edu.se506.lending.integration;

import edu.se506.lending.infrastructure.directory.HttpLegacyDirectoryClient;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryClient;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.URI;
import java.time.Duration;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Tag;

/** The same contract run against the real HTTP client and a controlled local service. */
@Tag("integration")
class HttpDirectoryClientContractTest extends DirectoryClientContract {
    private DirectoryStub stub;

    @BeforeEach void startStub() throws IOException { stub = new DirectoryStub(); }
    @AfterEach void stopStub() { stub.close(); }

    @Override LegacyDirectoryClient client() {
        return new HttpLegacyDirectoryClient(stub.baseUri(), Duration.ofSeconds(2), Duration.ofSeconds(2));
    }

    @Override LegacyDirectoryClient failingClient() throws IOException {
        int closedPort;
        try (ServerSocket socket = new ServerSocket(0)) {
            closedPort = socket.getLocalPort();
        }
        return new HttpLegacyDirectoryClient(URI.create("http://127.0.0.1:" + closedPort),
                Duration.ofSeconds(2), Duration.ofSeconds(2));
    }
}
```

### 4.6 Integration and end-to-end tests

#### 4.6.1 `after/src/test/java/edu/se506/lending/integration/DirectoryOutageIntegrationTest.java`

```java
package edu.se506.lending.integration;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.application.DirectoryReservationService;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.application.VisitorGate;
import edu.se506.lending.application.port.DirectoryException;
import edu.se506.lending.bootstrap.ReservationApplication;
import edu.se506.lending.infrastructure.approvals.FileApprovalSource;
import edu.se506.lending.infrastructure.directory.HttpLegacyDirectoryClient;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryAdapter;
import edu.se506.lending.infrastructure.directory.LegacyDirectoryClient;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * The directory policy of Chapter 13 against a controlled local service: one attempt, a bounded wait,
 * no retry and no fallback. An outage is a failure for the caller and never a "not found" answer, and a
 * borrower is never given a category the provider did not state.
 */
@Tag("integration")
class DirectoryOutageIntegrationTest {
    private static final LocalDate START = LocalDate.of(2026, 10, 20);
    private static final String HEADER =
            "borrowerId\titemId\tstart\tendExclusive\tsponsorId\tstatus\tvalidFrom\tvalidUntil";

    private DirectoryStub stub;
    private RecordingNotificationSender sender;
    private ReservationCoordinator coordinator;

    @BeforeEach void start() throws IOException {
        stub = new DirectoryStub();
        sender = new RecordingNotificationSender();
        coordinator = ReservationApplication.create(sender);
    }

    @AfterEach void stop() { stub.close(); }

    private DirectoryReservationService service(URI base, Duration timeout, VisitorGate gate) {
        var client = new HttpLegacyDirectoryClient(base, timeout, timeout);
        return new DirectoryReservationService(new LegacyDirectoryAdapter(client), coordinator, gate);
    }

    private void assertNothingHappened() {
        assertTrue(coordinator.reservations().isEmpty());
        assertTrue(sender.received().isEmpty());
    }

    @Test void anOrdinaryStudentRequestWorksThroughTheRealHttpClient() {
        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
        assertEquals("Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).", service.reserve("B1", "CAM1", START, 2));
        assertEquals(1, sender.received().size());
    }

    @Test void aMissingRowIsAnOrdinaryRejection() {
        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
        assertEquals("Rejected: borrower not found or inactive.", service.reserve("NOBODY", "CAM1", START, 2));
        assertNothingHappened();
    }

    @Test void aServerErrorIsAnOutageNotANotFoundAndIsNotRetried() {
        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
        DirectoryException failure = assertThrows(DirectoryException.class, () -> service.reserve("BROKEN", "CAM1", START, 2));
        assertInstanceOf(LegacyDirectoryClient.Failure.class, failure.getCause());
        assertEquals(1, stub.requests());
        assertNothingHappened();
    }

    @Test void aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest() {
        var service = service(stub.baseUri(), Duration.ofMillis(300), VisitorGate.disabled());
        long begin = System.nanoTime();
        DirectoryException failure = assertThrows(DirectoryException.class, () -> service.reserve("SLOW", "CAM1", START, 2));
        long elapsedMillis = Duration.ofNanos(System.nanoTime() - begin).toMillis();
        assertInstanceOf(LegacyDirectoryClient.Failure.class, failure.getCause());
        assertTrue(elapsedMillis < 5_000, "the call must give up after its timeout, but took " + elapsedMillis + " ms");
        assertEquals(1, stub.requests());
        assertNothingHappened();
    }

    @Test void aStalledBodyIsAFailureWithinTheOverallWait() {
        var service = service(stub.baseUri(), Duration.ofMillis(300), VisitorGate.disabled());
        // The headers and the first byte arrive at once and the rest is held. A client whose timeout covers
        // only the headers would wait for the stub to release the body and return a result, so the outcome
        // is asserted, with a generous outer deadline so that a defect shows as a failure and not a hang.
        DirectoryException failure = assertTimeoutPreemptively(Duration.ofSeconds(5),
                () -> assertThrows(DirectoryException.class, () -> service.reserve("SLOWBODY", "CAM1", START, 2)));
        assertInstanceOf(LegacyDirectoryClient.Failure.class, failure.getCause());
        assertEquals(1, stub.requests());
        assertNothingHappened();
    }

    @Test void aRefusedConnectionIsAnOutage() throws IOException {
        int closedPort;
        try (ServerSocket socket = new ServerSocket(0)) {
            closedPort = socket.getLocalPort();
        }
        var service = service(URI.create("http://127.0.0.1:" + closedPort), Duration.ofSeconds(2), VisitorGate.disabled());
        assertThrows(DirectoryException.class, () -> service.reserve("B1", "CAM1", START, 2));
        assertNothingHappened();
    }

    @Test void aMalformedAnswerIsAnOutageNotAGuess() {
        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
        assertThrows(DirectoryException.class, () -> service.reserve("GARBAGE", "CAM1", START, 2));
        assertNothingHappened();
    }

    @Test void anUnknownCategoryCodeIsNeverDefaultedToStaffOrStudent() {
        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
        DirectoryException failure = assertThrows(DirectoryException.class, () -> service.reserve("ODD", "CAM1", START, 2));
        assertEquals("Unsupported borrower category", failure.getMessage());
        assertNothingHappened();
    }

    @Test void anInactiveVisitorIsRejectedAndTheApprovalRegisterIsNotRead(@TempDir Path dir) {
        Path missingRegister = dir.resolve("never-read.tsv");
        var gate = new VisitorGate(new FileApprovalSource(missingRegister), Clock.systemUTC(), true);
        var service = service(stub.baseUri(), Duration.ofSeconds(2), gate);
        assertEquals("Rejected: borrower not found or inactive.", service.reserve("VOFF", "CAM1", START, 2));
        assertNothingHappened();
    }

    @Test void aVisitorIsServedThroughTheRealDirectoryAndTheRealApprovalFile(@TempDir Path dir) throws IOException {
        Path register = dir.resolve("approvals.tsv");
        Files.writeString(register, HEADER + "\nV1\tCAM1\t2026-10-20\t2026-10-22\tS1\tAPPROVED\t"
                + "2026-10-18T00:00:00Z\t2026-10-20T00:00:00Z\n", StandardCharsets.UTF_8);
        Clock clock = Clock.fixed(Instant.parse("2026-10-19T12:00:00Z"), ZoneOffset.UTC);
        var gate = new VisitorGate(new FileApprovalSource(register), clock, true);
        var service = service(stub.baseUri(), Duration.ofSeconds(2), gate);
        assertEquals("Confirmed: R1 for V1 on CAM1 [2026-10-20, 2026-10-22).", service.reserve("V1", "CAM1", START, 2));
        assertEquals("Rejected: no valid sponsor approval.", service.reserve("V2", "CAM1", START, 2));
        assertEquals(1, coordinator.reservations().size());
    }
}
```

#### 4.6.2 `after/src/test/java/edu/se506/lending/integration/FileApprovalSourceIntegrationTest.java`

```java
package edu.se506.lending.integration;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.application.port.ApprovalSourceException;
import edu.se506.lending.domain.ApprovalRecord;
import edu.se506.lending.domain.ApprovalStatus;
import edu.se506.lending.infrastructure.approvals.FileApprovalSource;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.time.Instant;
import java.time.LocalDate;
import java.util.Optional;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * Integration tests for the approval-register adapter. Every test writes a real file and reads it
 * back through the real adapter: nothing replaces the file system or the parser, because those are
 * the boundary under test.
 */
@Tag("integration")
class FileApprovalSourceIntegrationTest {
    private static final LocalDate START = LocalDate.of(2026, 10, 20);
    private static final LocalDate END = LocalDate.of(2026, 10, 22);
    private static final String HEADER =
            "borrowerId\titemId\tstart\tendExclusive\tsponsorId\tstatus\tvalidFrom\tvalidUntil";
    private static final String GOOD =
            "V1\tCAM1\t2026-10-20\t2026-10-22\tS1\tAPPROVED\t2026-10-18T00:00:00Z\t2026-10-20T00:00:00Z";

    @TempDir Path dir;

    private Path register(String... lines) throws IOException {
        Path file = dir.resolve("approvals.tsv");
        Files.writeString(file, String.join("\n", lines) + "\n", StandardCharsets.UTF_8);
        return file;
    }

    private static ApprovalSourceException failureOf(Path file) {
        return assertThrows(ApprovalSourceException.class,
                () -> new FileApprovalSource(file).find("V1", "CAM1", START, END));
    }

    @Test void aMatchingRowIsReturnedWithEveryFieldParsed() throws IOException {
        Optional<ApprovalRecord> found = new FileApprovalSource(register(HEADER, GOOD)).find("V1", "CAM1", START, END);
        ApprovalRecord record = found.orElseThrow();
        assertEquals("S1", record.sponsorId());
        assertEquals(ApprovalStatus.APPROVED, record.status());
        assertEquals(Instant.parse("2026-10-18T00:00:00Z"), record.validFrom());
        assertEquals(Instant.parse("2026-10-20T00:00:00Z"), record.validUntil());
    }

    @Test void aRequestWithNoMatchingRowIsEmptyNotAFailure() throws IOException {
        var source = new FileApprovalSource(register(HEADER, GOOD));
        assertEquals(Optional.empty(), source.find("V2", "CAM1", START, END));
        assertEquals(Optional.empty(), source.find("V1", "CAM2", START, END));
        assertEquals(Optional.empty(), source.find("V1", "CAM1", START, END.plusDays(1)));
    }

    @Test void aDeniedRowIsReturnedAsDeniedForTheCallerToDecide() throws IOException {
        String denied = GOOD.replace("APPROVED", "DENIED");
        assertEquals(ApprovalStatus.DENIED,
                new FileApprovalSource(register(HEADER, denied)).find("V1", "CAM1", START, END).orElseThrow().status());
    }

    @Test void theFileIsReadAfreshOnEveryCall() throws IOException {
        Path file = register(HEADER);
        var source = new FileApprovalSource(file);
        assertEquals(Optional.empty(), source.find("V1", "CAM1", START, END));
        Files.writeString(file, HEADER + "\n" + GOOD + "\n", StandardCharsets.UTF_8);
        assertTrue(source.find("V1", "CAM1", START, END).isPresent());
    }

    @Test void aMissingFileIsAnOperationalFailureWithItsCause() {
        ApprovalSourceException failure = failureOf(dir.resolve("absent.tsv"));
        assertInstanceOf(NoSuchFileException.class, failure.getCause());
    }

    @Test void aWrongOrMissingHeaderIsAFailure() throws IOException {
        failureOf(register(GOOD));
        failureOf(register(HEADER.replace("sponsorId", "sponsor"), GOOD));
        Path empty = dir.resolve("empty.tsv");
        Files.writeString(empty, "", StandardCharsets.UTF_8);
        failureOf(empty);
    }

    @Test void aRowWithTheWrongNumberOfColumnsIsAFailure() throws IOException {
        failureOf(register(HEADER, GOOD + "\textra"));
        failureOf(register(HEADER, "V1\tCAM1\t2026-10-20"));
    }

    @Test void anUnknownStatusIsAFailureNotADenial() throws IOException {
        failureOf(register(HEADER, GOOD.replace("APPROVED", "approved")));
        failureOf(register(HEADER, GOOD.replace("APPROVED", "PENDING")));
    }

    @Test void anInvalidDateOrInstantIsAFailure() throws IOException {
        failureOf(register(HEADER, GOOD.replace("2026-10-20\t2026-10-22", "20-10-2026\t2026-10-22")));
        failureOf(register(HEADER, GOOD.replace("2026-10-18T00:00:00Z", "2026-10-18")));
    }

    @Test void aBlankSponsorOrAnInvalidIntervalIsAFailure() throws IOException {
        failureOf(register(HEADER, GOOD.replace("\tS1\t", "\t \t")));
        failureOf(register(HEADER, GOOD.replace("2026-10-20\t2026-10-22", "2026-10-22\t2026-10-20")));
        failureOf(register(HEADER, GOOD.replace("2026-10-18T00:00:00Z\t2026-10-20T00:00:00Z",
                "2026-10-20T00:00:00Z\t2026-10-18T00:00:00Z")));
    }

    @Test void aDuplicateRequestKeyIsAFailureEvenIfTheRowsDisagree() throws IOException {
        failureOf(register(HEADER, GOOD, GOOD.replace("APPROVED", "DENIED")));
    }

    @Test void oneBadRowRejectsTheWholeRegisterEvenWhenTheRequestMatchesAGoodRow() throws IOException {
        failureOf(register(HEADER, GOOD, "V9\tCAM2\tnot-a-date\t2026-10-22\tS1\tAPPROVED\t2026-10-18T00:00:00Z\t2026-10-20T00:00:00Z"));
    }

    @Test void bytesThatAreNotUtf8AreAFailure() throws IOException {
        Path file = dir.resolve("binary.tsv");
        byte[] header = (HEADER + "\n").getBytes(StandardCharsets.UTF_8);
        byte[] bad = {(byte) 0xC3, (byte) 0x28, '\n'};
        byte[] all = new byte[header.length + bad.length];
        System.arraycopy(header, 0, all, 0, header.length);
        System.arraycopy(bad, 0, all, header.length, bad.length);
        Files.write(file, all);
        failureOf(file);
    }
}
```

#### 4.6.3 `after/src/test/java/edu/se506/lending/e2e/Chapter13JourneyE2ETest.java`

```java
package edu.se506.lending.e2e;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.integration.DirectoryStub;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * End-to-end journeys at the real system boundary of this command-line application: a separate Java
 * process, started as a user would start it, talking over HTTP to a controlled local directory service
 * and reading a real approval file. The classpath comes from the system property e2e.classpath
 * (default target/classes), so the same journeys can be run against a packaged jar.
 */
@Tag("e2e")
class Chapter13JourneyE2ETest {
    private static final String HEADER =
            "borrowerId\titemId\tstart\tendExclusive\tsponsorId\tstatus\tvalidFrom\tvalidUntil";
    private static final String V1_CAM2 =
            "V1\tCAM2\t2026-10-20\t2026-10-22\tS1\tAPPROVED\t2026-10-18T00:00:00Z\t2026-10-20T00:00:00Z";

    @TempDir Path dir;

    private record Run(int exitCode, List<String> lines) { }

    private Run run(DirectoryStub stub, Path register, boolean visitors) throws IOException, InterruptedException {
        String java = Path.of(System.getProperty("java.home"), "bin",
                System.getProperty("os.name").toLowerCase().contains("win") ? "java.exe" : "java").toString();
        String classpath = System.getProperty("e2e.classpath", "target/classes");
        ProcessBuilder builder = new ProcessBuilder(java,
                "-Dlending.directory.url=" + stub.baseUri(),
                "-Dlending.approvals.file=" + register,
                "-Dlending.visitors=" + visitors,
                "-Dlending.now=2026-10-19T12:00:00Z",
                "-Dlending.directory.timeout.millis=2000",
                "-cp", classpath, "edu.se506.lending.bootstrap.Chapter13Demo");
        builder.redirectErrorStream(true);
        Process process = builder.start();
        List<String> lines = new ArrayList<>();
        try (var reader = new java.io.BufferedReader(new java.io.InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) lines.add(line);
        }
        assertTrue(process.waitFor(60, TimeUnit.SECONDS), "the demo did not finish");
        return new Run(process.exitValue(), lines);
    }

    private Path register(String... rows) throws IOException {
        Path file = dir.resolve("approvals.tsv");
        Files.writeString(file, String.join("\n", rows) + "\n", StandardCharsets.UTF_8);
        return file;
    }

    @Test void withTheFlagOffVisitorsAreRefusedAndEveryoneElseIsServed() throws Exception {
        try (var stub = new DirectoryStub()) {
            Run run = run(stub, register(HEADER, V1_CAM2), false);
            assertEquals(0, run.exitCode(), String.join("\n", run.lines()));
            assertEquals(List.of(
                    "Visitors enabled: false",
                    "Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).",
                    "Visitor V1: Rejected: visitor reservations are not enabled.",
                    "Visitor V2: Rejected: visitor reservations are not enabled.",
                    "Unknown U9: Rejected: borrower not found or inactive.",
                    "Outage BROKEN: Unavailable: Borrower directory unavailable",
                    "Reservations: 1",
                    "Notices: 1"), run.lines());
        }
    }

    @Test void withTheFlagOnAnApprovedVisitorIsServedAndAnUnapprovedOneIsRefused() throws Exception {
        try (var stub = new DirectoryStub()) {
            Run run = run(stub, register(HEADER, V1_CAM2), true);
            assertEquals(0, run.exitCode(), String.join("\n", run.lines()));
            assertEquals(List.of(
                    "Visitors enabled: true",
                    "Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).",
                    "Visitor V1: Confirmed: R2 for V1 on CAM2 [2026-10-20, 2026-10-22).",
                    "Visitor V2: Rejected: no valid sponsor approval.",
                    "Unknown U9: Rejected: borrower not found or inactive.",
                    "Outage BROKEN: Unavailable: Borrower directory unavailable",
                    "Reservations: 2",
                    "Notices: 2"), run.lines());
        }
    }

    @Test void aMalformedRegisterFailsOnlyTheVisitorRequestsAndIsReportedAsAnOutage() throws Exception {
        try (var stub = new DirectoryStub()) {
            Run run = run(stub, register(HEADER, V1_CAM2, "garbage row"), true);
            assertEquals(0, run.exitCode(), String.join("\n", run.lines()));
            assertEquals("Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).", run.lines().get(1));
            assertEquals("Visitor V1: Approval register unavailable: Row 3 has 1 columns, not 8.", run.lines().get(2));
            assertEquals("Visitor V2: Approval register unavailable: Row 3 has 1 columns, not 8.", run.lines().get(3));
            assertEquals("Reservations: 1", run.lines().get(6));
        }
    }
}
```

### 4.7 The three changed regression tests

Each change adds the visitor policy to a map that lists every category, and one import where the class had none for it. Apply the hunks; every other line is as in the earlier companions. Lines starting with a plus sign are added and lines starting with a minus sign are removed.

#### 4.7.1 `after/src/test/java/edu/se506/lending/regression/BehaviourStrategyTest.java`

```diff
--- chapter11/src/test/java/edu/se506/lending/regression/BehaviourStrategyTest.java
+++ chapter13/src/test/java/edu/se506/lending/regression/BehaviourStrategyTest.java
@@ -6,6 +6,7 @@
 import edu.se506.lending.domain.BorrowingPolicy;
 import edu.se506.lending.domain.ReservationRules;
 import edu.se506.lending.domain.StaffReservationRules;
+import edu.se506.lending.domain.VisitorReservationRules;
 import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
 import edu.se506.lending.infrastructure.persistence.InMemoryReservationRepository;
 
@@ -38,7 +39,8 @@
     @Test void injectedPolicyChangesDecisionWithoutChangingCoordinator() {
         BorrowingPolicy temporaryStaffRule = (count, days) -> count >= 0 && count < 1 && days >= 1 && days <= 2;
         var coordinator = new ReservationCoordinator(
-                Map.of(BorrowerCategory.STUDENT, new ReservationRules(), BorrowerCategory.STAFF, temporaryStaffRule),
+                Map.of(BorrowerCategory.STUDENT, new ReservationRules(), BorrowerCategory.STAFF, temporaryStaffRule,
+                        BorrowerCategory.VISITOR, new VisitorReservationRules()),
                 new ConfirmationFormatter(), new RecordingNotificationSender(), new InMemoryReservationRepository());
         var start = LocalDate.of(2026, 10, 20);
         assertEquals("Rejected: borrower limit or duration.", coordinator.reserve("T1", "CAM1", start, 3, BorrowerCategory.STAFF));
```

#### 4.7.2 `after/src/test/java/edu/se506/lending/regression/Chapter06Checks.java`

```diff
--- chapter11/src/test/java/edu/se506/lending/regression/Chapter06Checks.java
+++ chapter13/src/test/java/edu/se506/lending/regression/Chapter06Checks.java
@@ -10,6 +10,7 @@
 import edu.se506.lending.domain.Reservation;
 import edu.se506.lending.domain.ReservationRules;
 import edu.se506.lending.domain.StaffReservationRules;
+import edu.se506.lending.domain.VisitorReservationRules;
 import edu.se506.lending.infrastructure.notification.ConsoleNotificationSender;
 import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
 import edu.se506.lending.infrastructure.persistence.InMemoryReservationRepository;
@@ -111,7 +112,8 @@
 
     private static Map<BorrowerCategory, BorrowingPolicy> policies() {
         return Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
-                      BorrowerCategory.STAFF, new StaffReservationRules());
+                      BorrowerCategory.STAFF, new StaffReservationRules(),
+                      BorrowerCategory.VISITOR, new VisitorReservationRules());
     }
 
     private static final class FailingSender implements NotificationSender {
```

#### 4.7.3 `after/src/test/java/edu/se506/lending/structure/RepositoryBoundaryTest.java`

```diff
--- chapter11/src/test/java/edu/se506/lending/structure/RepositoryBoundaryTest.java
+++ chapter13/src/test/java/edu/se506/lending/structure/RepositoryBoundaryTest.java
@@ -76,12 +76,14 @@
     }
     @Test void coordinatorRequiresARepository() {
         var policies = Map.<BorrowerCategory, BorrowingPolicy>of(BorrowerCategory.STUDENT, new ReservationRules(),
-                BorrowerCategory.STAFF, new StaffReservationRules());
+                BorrowerCategory.STAFF, new StaffReservationRules(),
+                BorrowerCategory.VISITOR, new VisitorReservationRules());
         assertThrows(NullPointerException.class,
                 () -> new ReservationCoordinator(policies, new ConfirmationFormatter(), reservation -> { }, null));
     }
     private ReservationCoordinator coordinator(ReservationRepository repository, NotificationSender sender) {
         return new ReservationCoordinator(Map.of(BorrowerCategory.STUDENT, new ReservationRules(),
-                BorrowerCategory.STAFF, new StaffReservationRules()), new ConfirmationFormatter(), sender, repository);
+                BorrowerCategory.STAFF, new StaffReservationRules(),
+                BorrowerCategory.VISITOR, new VisitorReservationRules()), new ConfirmationFormatter(), sender, repository);
     }
 }
```

Other test files that build a coordinator needed no edit, and the 159 inherited invocations passed with these four edits and nothing else.

## 5. Build, scripts and documentation

### 5.1 `after/pom.xml`

Change the project version from 0.11.0 to 0.13.0 and nothing else. The POM already sets `failIfNoTests` to true for Surefire, which is why a stage that selects no tests fails (Section 1.3). The hunk is an edit to the Chapter 11 POM:

```diff
--- chapter11/pom.xml
+++ chapter13/pom.xml
@@ -4,7 +4,7 @@
   <modelVersion>4.0.0</modelVersion>
   <groupId>edu.se506</groupId>
   <artifactId>equipment-lending</artifactId>
-  <version>0.11.0</version>
+  <version>0.13.1</version>
   <properties>
     <maven.compiler.release>17</maven.compiler.release>
     <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
```

### 5.2 `after/scripts/pipeline.sh`

```bash
#!/usr/bin/env bash
# A modest delivery pipeline run on one machine. Each stage must pass before the next one starts,
# and the first failing stage stops the run with a non-zero status. CHAPTER_MVN names the Maven
# command (default: mvn); CHAPTER_M2 optionally names a local Maven repository.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

MVN="${CHAPTER_MVN:-mvn}"
ARGS=(--batch-mode)
if [ -n "${CHAPTER_M2:-}" ]; then
  ARGS+=("-Dmaven.repo.local=${CHAPTER_M2}")
fi

stage() {
  local name="$1"
  shift
  echo "=== STAGE: ${name}"
  local began=$SECONDS
  "$@"
  echo "=== PASSED: ${name} ($((SECONDS - began)) s)"
}

stage "1 compile" "$MVN" "${ARGS[@]}" -q compile
stage "2 unit tests and architecture checks" "$MVN" "${ARGS[@]}" test -DexcludedGroups=integration,e2e
stage "3 integration tests (real file, real HTTP client, local stub service)" "$MVN" "${ARGS[@]}" test -Dgroups=integration
stage "4 end-to-end journeys (separate process)" "$MVN" "${ARGS[@]}" test -Dgroups=e2e
stage "5 package" "$MVN" "${ARGS[@]}" package -DskipTests
echo "PIPELINE PASSED"
```

### 5.3 `after/scripts/simulate-release.sh`

```bash
#!/usr/bin/env bash
# This script does not enforce the pipeline's gates: it packages with -DskipTests and then runs only the
# end-to-end smoke journeys, so it assumes that scripts/pipeline.sh has already passed for the same candidate.
# Rollback assumes the same version-derived jar file name in both releases, so the exercise's two releases are
# two labels for one build and not a tested cross-version rollback.
#
# SIMULATION of continuous delivery to a staging target. Nothing here is a server, a network
# deployment or a production release: "staging" is a folder, "deploying" is copying a jar into it,
# and the smoke test is the end-to-end journeys run against the jar that was copied.
#
#   bash scripts/simulate-release.sh              build, deliver as the current release, smoke-test it
#   RELEASE_LABEL=v2 bash scripts/simulate-release.sh   deliver again; the old release becomes "previous"
#   bash scripts/simulate-release.sh rollback     make "previous" the current release again, smoke-test it
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

MVN="${CHAPTER_MVN:-mvn}"
ARGS=(--batch-mode)
if [ -n "${CHAPTER_M2:-}" ]; then
  ARGS+=("-Dmaven.repo.local=${CHAPTER_M2}")
fi
STAGING="build/staging"
VERSION="$(sed -n 's:^  <version>\(.*\)</version>$:\1:p' pom.xml | head -1)"
JAR="equipment-lending-${VERSION}.jar"

smoke() {
  echo "--- smoke test of $(cat "${STAGING}/current/RELEASE") (end-to-end journeys against ${STAGING}/current/${JAR})"
  "$MVN" "${ARGS[@]}" test -Dgroups=e2e "-De2e.classpath=${STAGING}/current/${JAR}"
}

case "${1:-deliver}" in
  deliver)
    "$MVN" "${ARGS[@]}" -q package -DskipTests
    mkdir -p "${STAGING}"
    if [ -d "${STAGING}/current" ]; then
      rm -rf "${STAGING}/previous"
      mv "${STAGING}/current" "${STAGING}/previous"
    fi
    mkdir -p "${STAGING}/current"
    cp "target/${JAR}" "${STAGING}/current/${JAR}"
    echo "${RELEASE_LABEL:-${VERSION}}" > "${STAGING}/current/RELEASE"
    echo "--- delivered $(cat "${STAGING}/current/RELEASE") to ${STAGING}/current (simulation)"
    smoke
    ;;
  rollback)
    if [ ! -d "${STAGING}/previous" ]; then
      echo "No previous release to roll back to." >&2
      exit 1
    fi
    rm -rf "${STAGING}/current"
    mv "${STAGING}/previous" "${STAGING}/current"
    echo "--- rolled back to $(cat "${STAGING}/current/RELEASE") (simulation)"
    smoke
    ;;
  *)
    echo "usage: simulate-release.sh [deliver|rollback]" >&2
    exit 2
    ;;
esac
```

### 5.4 `after/.github/workflows/pipeline.yml`

This workflow expresses the stages as jobs, each waiting for the one before it (`needs`). **It has not been run**: no hosted CI run is claimed. The action versions are those in the file; check the current ones before relying on it.

```yaml
name: Delivery pipeline

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  unit:
    name: 1 Compile, unit tests and architecture checks
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: '17'
          cache: maven
      - name: Compile
        run: mvn --batch-mode -q compile
      - name: Unit tests
        run: mvn --batch-mode test -DexcludedGroups=integration,e2e

  integration:
    name: 2 Integration tests
    needs: unit
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: '17'
          cache: maven
      - name: Integration tests
        run: mvn --batch-mode test -Dgroups=integration

  e2e:
    name: 3 End-to-end journeys
    needs: integration
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: '17'
          cache: maven
      - name: Compile
        run: mvn --batch-mode -q compile
      - name: End-to-end journeys
        run: mvn --batch-mode test -Dgroups=e2e

  package:
    name: 4 Package the release candidate
    needs: e2e
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: '17'
          cache: maven
      - name: Package
        run: mvn --batch-mode package -DskipTests
      - name: Keep the jar
        uses: actions/upload-artifact@v7
        with:
          name: release-candidate
          path: target/equipment-lending-*.jar
          if-no-files-found: error
```

### 5.5 `after/README.md`

````markdown
# Chapter 13 checkpoint

Use a full Java 17 JDK and Maven 3.9.11. The JDK must include jdk.jdeps for the compiled dependency tests. Existing dependency and plugin versions are unchanged; only the project version becomes 0.13.0.

From this directory, run the whole delivery pipeline (compile; unit tests and architecture checks; integration tests; end-to-end journeys; package):

```bash
bash scripts/pipeline.sh
```

or the single command `mvn --batch-mode verify`, which runs every test in one pass. The build executes 232 JUnit invocations: 159 inherited from Chapter 11 and 73 new. Of the 232, 203 run in the unit stage, 26 are tagged `integration` and 3 are tagged `e2e`.

What Chapter 13 adds: a visiting-researcher category (VISITOR), a VisitorReservationRules policy, a VisitorGate that holds one feature flag (default off), an item allowlist and the approval check, an ApprovalSource port with a real file adapter (FileApprovalSource) that reads a tab-separated sponsor register, and an HTTP client for the borrower directory (HttpLegacyDirectoryClient) with a bounded wait over the whole lookup (the body included), one attempt, no retry and no fallback answer. A missing approval is an expected rejection; an unreadable register or an unreachable directory is a failure and never looks like a rejection or a missing borrower.

The directory service in the tests is a local stub built on the JDK's embedded HTTP server. The end-to-end journeys start Chapter13Demo as a separate process against that stub and a real approval file; the demo reads its settings from system properties (see the class comment). There is no real directory service or approval service, so what the stub does is an assumption.

`scripts/simulate-release.sh` is a SIMULATION of delivery: staging is a folder, deploying is copying a jar, and the smoke test is the end-to-end journeys against the copied jar. `.github/workflows/pipeline.yml` expresses the same stages for a hosted runner; it has not been run. `docs/ADR-013-visiting-researchers.md` records the decision, the flag removal plan and the rollback. The directory `ai-activity` holds the two tests of the AI activity; they are not part of the Maven build.

SD-11-1 (the report's rate for any other kind of borrower, which a late visitor now reaches) and SD-12 (the count rule counts every retained reservation) are not changed here.

The package `legacy` stands for the old records system's overdue report. It is isolated, like `patterns`, `behaviour` and `examples`: production code under `edu.se506.lending` must not refer to it, and DependencyRulesTest checks that. Only bootstrap launches it or feeds it rows. LoanRow is the old system's export format and is deliberately unchanged.

The optional bridge (OverdueRowSource, OverdueReportService and LoanSnapshotRows in bootstrap) feeds the report from the live loan and reservation snapshots. It reads one date and one snapshot per report, and a failure to read is never reported as zero overdue loans.

The directory `stages` holds the report at each step of the refactoring. It is not part of the Maven build. To run a stage, copy its OverdueReport.java over src/main/java/legacy/OverdueReport.java and run:

```bash
mvn --batch-mode -Dtest='OverdueReport*Test' test
```

Stages 1 to 4 each pass the same 28 invocations. Stage 0 is the code as found and cannot be tested without a change, because it reads the system clock. stageC is a separate functional change (unknown kinds are rejected) with its own replacement tests; to run it, copy all three of its files to their src locations.

The directory `probe` holds a program that runs the original, unseamed report beside the seamed one and compares their output. It is not part of the Maven build. From this directory, with stage 1 or the final report in place:

```bash
mkdir -p probe/out
javac --release 17 -d probe/out src/main/java/legacy/*.java probe/OriginalUnseamed.java probe/OriginalReportProbe.java
java -cp probe/out legacy.OriginalReportProbe
```

The characterisation tests record what the report does today. A passing characterisation test means unchanged, not correct. Four behaviours are recorded as suspected or surprising in docs/SUSPECTED-DEFECTS-legacy-overdue-report.md and are not fixed here. ADR-011 records the decision to pin, isolate and refactor the report.

To print the package metrics, run `mvn --batch-mode compile` and then `java tools/PackageMetrics.java target/classes`.

ADR-010 from Chapter 10 is still in docs. No hosted CI run and no peer review is claimed.
````

### 5.6 `after/docs/ADR-013-visiting-researchers.md`

```markdown
# ADR-013: Visiting-researcher reservations behind a flag, with two real boundaries

Date: 13 October 2026 (Asia/Baghdad)
Status: Implemented teaching example; peer review pending. The integration boundary (Blueprint D1) is an interim choice awaiting the module leader.

## Context

Change request CR-12 (Chapter 12) adds a visiting-researcher category. A visitor may reserve CAM1 or CAM2 for one to three days when a sponsor approval matches the exact borrower, item and period and is valid at request time. Student and staff behaviour must not change.

Two outside collaborators now have real boundaries. The borrower directory, which the synthetic fixture of Chapter 8 stood in for, can be slow, down or wrong. The sponsor-approval register is a file that can be missing or malformed. Until now neither could fail in a way that tests could see.

## Decision

- Add `VISITOR`, a `VisitorReservationRules` policy (count and duration only) and a `VisitorGate` that holds the feature flag, the item allowlist and the approval check. The existing `BorrowingPolicy` contract is not widened.
- Define an `ApprovalSource` port. `FileApprovalSource` reads a UTF-8 tab-separated register of eight columns and rejects the whole file if any row is invalid or any request key repeats. A missing record is an expected rejection. An unreadable or untrustworthy register is an `ApprovalSourceException`, which no code on the reservation path catches.
- Reach the directory over HTTP with `HttpLegacyDirectoryClient`, behind the existing `LegacyDirectoryClient` contract. **Policy: one attempt, a bounded wait, no retry and no fallback answer.** The wait bounds the whole lookup, including the time to receive the body. A timeout, a refused connection, any other status and a malformed row are failures, which the adapter turns into `DirectoryException`. An outage is never reported as “not found”, and no borrower is ever given a category that the provider did not state.
- Introduce one flag, `visitingResearchersEnabled`, default **false**. When it is off, visitor requests are rejected explicitly and the approval register is not read. Student and staff requests never depend on it.
- Test the file adapter with real temporary files and the HTTP client against a local stub service, and run the contract for directory clients against both the in-memory fixture and the HTTP client. Run focused end-to-end journeys against a separate process.

## Alternatives considered

- Pass sponsor approval to `BorrowingPolicy` through a flag or a static: rejected, because the policy would then depend on hidden global state and could not be tested for identity or time.
- Fall back to a cached or default directory answer after a timeout: rejected, because a stale answer would grant a category the provider did not currently state.
- Retry after a timeout: not adopted in this change. A retry would repeat a slow call for the person waiting, and it would change the one-attempt notification and directory contracts of earlier chapters.
- A database or a real HTTP service for approvals: not needed for CR-12 and outside the course scope.

## Consequences

The directory and the register are now two places that can fail at the edge of the system, and each failure has its own test. Adding `VISITOR` forced a policy for it in every coordinator construction, so four fixture constructions in three test files that enumerate every category were updated. No assertion was weakened.

The count rule still counts every retained reservation, which is SD-12, unresolved. The legacy overdue report still treats any kind other than `S` or `T` at the rate of SD-11-1, so a visitor who is late is charged one unit a day with no grace and no cap. Neither is changed here.

## Flag removal plan

The flag exists to let the controlled demonstration prove both paths before visitors are released. Remove it when all of these hold: the released variant of CR-12 is accepted, both settings have passed in the pipeline for the release candidate, and a decision to keep visitors enabled is recorded. Then delete `VisitorGate.DISABLED`, the `enabled` parameter and the disabled-path tests together, in one commit. Review the flag at the end of Chapter 14's handover; a flag with no removal decision is a permanent branch.

## Rollback

To stop new visitor reservations, turn the flag off. That does not delete existing reservations or undo notices already sent, and an existing reservation can still be checked out and returned. To go back to the previous release, redeliver it (the simulated delivery keeps one previous release) and smoke-test it.

## Validation and review

Run `bash scripts/pipeline.sh` for all stages, then `bash scripts/simulate-release.sh` for the simulated delivery. No hosted CI run, public deployment or independent peer review is claimed.

## Revisit triggers

A decision on SD-11-1 or SD-12; a requirement to revoke an approval after a reservation; a real approval service or directory with authentication; concurrent writers to the register; a need for retry or caching after measured outages.
```

## 6. The AI activity files

Both files live in `after/ai-activity/` and are outside the build. To run them, copy them into `src/test/java/edu/se506/lending/aifixture/` and run `mvn test -Dtest='ProposedRegisterIntegrationTest,RepairedRegisterIntegrationTest' -Dgroups=integration`.

### 6.1 `after/ai-activity/ProposedRegisterIntegrationTest.java`

```java
package edu.se506.lending.aifixture;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import edu.se506.lending.application.VisitorGate;
import edu.se506.lending.application.port.ApprovalSource;
import edu.se506.lending.domain.ApprovalRecord;
import edu.se506.lending.domain.ApprovalStatus;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.Optional;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** AI-proposed "integration test" for the approval register. */
@Tag("integration")
class ProposedRegisterIntegrationTest {
    @Test void anApprovedVisitorIsAcceptedFromTheRegister() {
        LocalDate start = LocalDate.of(2026, 10, 20);
        LocalDate end = start.plusDays(2);
        Instant now = Instant.parse("2026-10-19T12:00:00Z");
        ApprovalSource register = mock(ApprovalSource.class);
        ApprovalRecord record = new ApprovalRecord("V1", "CAM1", start, end, "S1", ApprovalStatus.APPROVED,
                Instant.parse("2026-10-18T00:00:00Z"), Instant.parse("2026-10-20T00:00:00Z"));
        when(register.find("V1", "CAM1", start, end)).thenReturn(Optional.of(record));

        VisitorGate gate = new VisitorGate(register, Clock.fixed(now, ZoneOffset.UTC), true);

        assertEquals(Optional.empty(), gate.rejection("V1", "CAM1", start, 2));
        verify(register).find("V1", "CAM1", start, end);
    }
}
```

### 6.2 `after/ai-activity/RepairedRegisterIntegrationTest.java`

```java
package edu.se506.lending.aifixture;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.application.VisitorGate;
import edu.se506.lending.application.port.ApprovalSourceException;
import edu.se506.lending.infrastructure.approvals.FileApprovalSource;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.Optional;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/** The repaired test: a real register file, read by the real adapter, through the real gate. */
@Tag("integration")
class RepairedRegisterIntegrationTest {
    private static final String HEADER =
            "borrowerId\titemId\tstart\tendExclusive\tsponsorId\tstatus\tvalidFrom\tvalidUntil";
    private static final String ROW =
            "V1\tCAM1\t2026-10-20\t2026-10-22\tS1\tAPPROVED\t2026-10-18T00:00:00Z\t2026-10-20T00:00:00Z";
    private static final LocalDate START = LocalDate.of(2026, 10, 20);

    @Test void anApprovedVisitorIsAcceptedFromARealRegisterFile(@TempDir Path dir) throws IOException {
        Path file = dir.resolve("approvals.tsv");
        Files.writeString(file, HEADER + "\n" + ROW + "\n", StandardCharsets.UTF_8);
        Clock clock = Clock.fixed(Instant.parse("2026-10-19T12:00:00Z"), ZoneOffset.UTC);
        VisitorGate gate = new VisitorGate(new FileApprovalSource(file), clock, true);

        assertEquals(Optional.empty(), gate.rejection("V1", "CAM1", START, 2));
        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate.rejection("V2", "CAM1", START, 2));

        Files.writeString(file, HEADER + "\n" + ROW + "\nbroken row\n", StandardCharsets.UTF_8);
        assertThrows(ApprovalSourceException.class, () -> gate.rejection("V1", "CAM1", START, 2));
    }
}
```

## 7. Worked explanation and evidence

### 7.1 Why the gate sits in front of the coordinator

`BorrowingPolicy.mayRequest(count, days)` answers a count and duration question and nothing else. Approval needs the borrower, the item, the period and the time. Putting any of those into the policy through a flag or a static would give it hidden state and make it untestable for identity and time. So the policy stays small (`VisitorReservationRules`), and the request-specific decision lives in `VisitorGate`, which sits in the application layer and is called by `DirectoryReservationService` before the coordinator. Student and staff requests never reach the gate. The order inside the gate is cheap to expensive: flag, then item, then duration, then one clock read, then one register read, then an exact-request re-check and the validity window.

The exact-request re-check looks redundant, since the source is asked for the exact request. It is there because the source is a boundary: a source that returns the wrong record (a bug, or a register that was changed underneath) must not approve. `aSourceThatReturnsADifferentRequestDoesNotApprove` and the fault experiment in Section 12.3 test it.

### 7.2 Exceptions and expected results

An expected result is a return value; an operational failure is an exception that nothing on the request path catches. `FileApprovalSource.find` returns an empty `Optional` when no record matches and throws `ApprovalSourceException` when the register cannot be trusted. The gate does not catch it, and neither does the service. The demonstration catches it at the edge and prints `Approval register unavailable: ...`. That is the whole difference between “no sponsor approved this” and “we could not find out”, and AC10 checks that a malformed register creates no reservation and sends no notice. The same applies to the directory: `DirectoryException` is the failure and a missing row is a rejection.

### 7.3 The acceptance examples, with their evidence

| Example | Test in `VisitorAcceptanceTest` | Also checked at a narrower level |
|---|---|---|
| AC1 | `ac1_aVisitorWithAMatchingApprovalReservesCam1ForTwoDays` | `aMatchingApprovedRecordInsideItsWindowLetsTheRequestContinue` |
| AC2 | `ac2_cam2ForThreeDaysNeedsItsOwnRecordAndIsAllowed` | `countAndDurationBoundaries` |
| AC3 | `ac3_fourDaysIsRejectedEvenWithAMatchingRecord` | `countAndDurationBoundaries` |
| AC4 | `ac4_zeroOrNegativeDaysIsRejectedWithoutReadingTheRegister` | `aNonPositiveDurationIsLeftToThePolicyWithoutReadingTheSource` |
| AC5 | `ac5_anItemOutsideTheAllowlistIsRejectedEvenWithAMatchingRecord` | `anItemOutsideTheAllowlistIsRejectedWithoutReadingTheSource` |
| AC6 | `ac6_aMissingOrDeniedApprovalIsAnExpectedRejection` | `aMissingOrDeniedRecordIsAnExpectedRejection`; `aDeniedRowIsReturnedAsDeniedForTheCallerToDecide` |
| AC7 | `ac7_anApprovalForAnotherBorrowerItemOrPeriodDoesNotAuthorise` | `aRecordMatchesOnlyTheExactBorrowerItemAndPeriod` |
| AC8 | `ac8_theRequestInstantEqualToValidFromIsValid` | `theWindowIncludesItsStartAndExcludesItsEnd` |
| AC9 | `ac9_theRequestInstantAtValidUntilOrBeforeValidFromIsRejected` | `equalityAtTheStartOfTheWindowIsValidAndAtTheEndIsNot` |
| AC10 | `ac10_anUnreadableApprovalRegisterIsAnOperationalFailureNotARejection` | The file tests of Section 7.4; `anOperationalFailureOfTheSourceIsNotCaught`; the third journey |
| AC11 | `ac11_threeRetainedReservationsBlockAFourthEvenAfterLoansAreReturned` | `countAndDurationBoundaries` |
| AC12 | `ac12_aDisabledFlagRejectsExplicitlyWithoutReadingTheRegister` | `aDisabledGateRejectsWithoutReadingTheSource`; the first journey |
| AC13 | `ac13_studentAndStaffBehaviourIsUnchangedUnderEitherSettingAndNeverReadsTheRegister` | The inherited 159 invocations |
| AC14 | `ac14_anOverlapWithAnExistingReservationIsRejectedByTheExistingRule` | |
| AC15 | `ac15_anExpectedNotificationFailureLeavesTheVisitorReservationInPlace` | |
| AC16 | `ac16_aVisitorReservationStaysUsableAfterTheApprovalExpiresAndTheFlagIsOff` | |
| AC17 | `ac17_anInactiveOrUnknownBorrowerIsRejectedAsBefore` | `anUnknownCategoryCodeIsNeverDefaultedToStaffOrStudent`; `anInactiveVisitorIsRejectedAndTheApprovalRegisterIsNotRead` |
| AC18 | `ac18_aVisitorLoanInTheOverdueReportKeepsTheExistingKindRuleSd11_1` | The Chapter 11 characterisation tests |

### 7.4 What the file tests cover

`FileApprovalSourceIntegrationTest` writes real files into a `@TempDir` and reads them through the real adapter. Thirteen tests cover: a matching row with every field parsed; no matching row (empty, not a failure); a denied row (returned for the caller to decide); a file changed between two calls (read afresh every time); a missing file (a failure, with the `NoSuchFileException` as its cause); a wrong, missing or empty header; a row with the wrong number of columns; an unknown status (a failure, not a denial); a bad date or instant; a blank sponsor or an interval whose end is not after its start; a duplicate request key even when the rows disagree; one bad row rejecting the whole register even when the request matches a good row; and bytes that are not UTF-8.

The whole-file rule is a design choice, and it has a cost: one bad row stops every visitor request until the register is repaired. The alternative, skipping bad rows, would let a typo silently remove a sponsor's approval, or worse, hide a duplicate that makes two rows disagree. The fault experiment includes it (Section 12.3), and the ADR names the revisit triggers.

### 7.5 What the stub is, and what it is not

`DirectoryStub` is a JDK `HttpServer` on the loopback address with an ephemeral port. It answers keys B1, T1, V1, V2, VOFF, ODD and GARBAGE with prepared bodies, BROKEN with status 500, SLOW by not answering until the test releases it, and SLOWBODY by sending the headers and the first byte of the body and then holding the rest until the test releases it. Closing the stub releases any waiting request, so a test never leaves a thread hanging. Its answers are the author's assumption of what a provider could say. Nothing in this book checks them against a real directory, which is why the chapter names a provider contract test as a limit and not as something done. The interface contract (`DirectoryClientContract`) is run against the in-memory fixture and the HTTP client, so a caller can substitute one for the other; that is a statement about our two implementations, not about the provider.

### 7.6 The failing pipeline, read

A deliberate fault was introduced into a scratch copy: the header comparison in `FileApprovalSource.readAll` was changed from `lines.isEmpty() || !HEADER.equals(lines.get(0))` to `lines.isEmpty()`. The pipeline ended with exit status 1 after stage 3, which is where a person should look first:

```text
=== STAGE: 1 compile
=== PASSED: 1 compile (5 s)
=== STAGE: 2 unit tests and architecture checks
[INFO] Tests run: 203, Failures: 0, Errors: 0, Skipped: 0
=== PASSED: 2 unit tests and architecture checks (11 s)
=== STAGE: 3 integration tests (real file, real HTTP client, local stub service)
[ERROR] edu.se506.lending.integration.FileApprovalSourceIntegrationTest.aWrongOrMissingHeaderIsAFailure -- Time elapsed: 0.013 s <<< FAILURE!
org.opentest4j.AssertionFailedError: Expected edu.se506.lending.application.port.ApprovalSourceException to be thrown, but nothing was thrown.
[ERROR] Failures: 
[ERROR]   FileApprovalSourceIntegrationTest.aWrongOrMissingHeaderIsAFailure:84->failureOf:44 Expected edu.se506.lending.application.port.ApprovalSourceException to be thrown, but nothing was thrown.
[ERROR] Tests run: 26, Failures: 1, Errors: 0, Skipped: 0
```

Stages 4 and 5 never started. Reading it: the first failing stage is 3; the first failing test, by name, promises that a wrong or missing header is a failure; the assertion says that it was not. Stage 2 could not have caught it, because no unit test reads a real file: the stage-2 tests use a controlled approval source, and that is correct for their purpose. The other 25 integration tests passed, so the fault is local to the header, and the test's first assertion that fails is at line 84 (the first of its three cases: a file with no header at all, the register's first row used as a header and skipped). This is the reason the integration stage exists.

### 7.7 The simulated delivery and its limits

`simulate-release.sh` kept one previous release and smoke-tested each step against the copied jar. The script packages with the tests skipped and runs only the end-to-end journeys, so it assumes that the pipeline has already passed for the same candidate; it does not enforce the other gates. Rollback assumes the same version-derived jar file name in both releases. Both releases were built from the same source, so the rollback demonstrated the mechanics (which folder is current, and that the smoke test runs against it) and not a change of behaviour. A real rollback has more to settle: data written by the new release, notices already sent and reservations already made (AC16 pins that a visitor reservation made before the flag went off stays usable).

### 7.8 The timeout defect, found in review

The client of Version 1.0 called the blocking `send` with a request timeout. The JDK documents that timeout as the time within which the response must be *received* and says nothing about a body [8]. The only test of a slow provider used a stub that waits before sending anything, so it exercised the one case the timeout certainly covers.

A review of the chapter tried another: a server that sends the headers and the first byte at once and holds the rest. With the client's timeout at 300 ms and the server holding the body for 1,600 ms, the lookup returned a valid result. The review measured about 1,690 ms on OpenJDK 17.0.20. The same probe on the verification machine (JDK 24.0.2, Version 1.0 client) gave `RESULT=Person[key=B1, kind=S, status=Y]` and `ELAPSED_MS=1725`. I did not run the probe on a Java 17 runtime; the Java 17 figure is the review's.

The correction sends the request asynchronously and waits for the future for at most the configured time. On timeout it cancels the future, which asks the client to drop the exchange and is not guaranteed to be prompt or to take effect [13][14], and fails the lookup with a message that names the wait. The caller does not depend on the cancellation, because it has already stopped waiting. An interrupted wait cancels, restores the interrupt flag and fails. A failed future becomes a `Failure` whose message names the cause's class. The header timeout stays on the request.

| Run | Result |
|---|---|
| New test `aStalledBodyIsAFailureWithinTheOverallWait` against the **Version 1.0 client** | Fails: `execution timed out after 5000 ms` (the outer deadline), because the client waits for the stub to release the body and returns it |
| The same test against the corrected client | Passes. A probe with the same 300 ms timeout and 1,600 ms stall: `FAILED=...Failure: Directory did not answer within 300 ms.` after 326 ms |
| Fault experiment, Section 12.3 | Removing the overall deadline is caught by the new test alone. Removing the header timeout alone is **not** caught: the overall deadline still bounds the call, so it is an equivalent change. Removing both is caught by both slow-provider tests |

Not changed: one logical attempt, no retry, no fallback category, the distinction between an unavailable directory and an absent borrower, and no reservation or notice after a failure.

### 7.9 The order of the visitor decision

Figure 13.3 of Version 1.0 put the count and duration rules before the register was read. The code does the opposite: the gate checks the flag, the item, and (for fewer than one day) steps aside; otherwise it reads the clock and the register; then the coordinator applies the count and duration rules and the availability rule. A four-day visitor request with an unreadable register therefore fails with the register's error and is not rejected for its duration. The test `precedence_theRegisterIsReadBeforeTheCountAndDurationRulesApply` pins both ends: four days with an unreadable register throws the register's exception, and zero days does not read the register and returns the limit rejection. It is not one of the eighteen acceptance examples and is not named `ac<N>_`.

If a different precedence is wanted, for example duration before register, it is a change to the contract, the implementation and the tests, decided by the requirement's owner. The picture follows the code.

### 7.10 What this evidence does not show

The pipeline and the tests show the selected behaviours on the supplied inputs in the stated environment. They do not show behaviour against a real directory or a real approval workflow, concurrency (two writers of the register, or two simultaneous requests), authentication, behaviour under load, a hosted run, Java 17 behaviour, or that the suspected defects SD-11-1 and SD-12 are acceptable. AC18 shows that SD-11-1 now has a consequence for a late visitor, and the change leaves it as it was.

## 8. Suggested practical solution

### 8.1 Book project, steps B1–B4

**B1. Run the pipeline.** A good answer reproduces the counts of Section 1.2 (202, 25, 3), notes the time of each stage, and says what a failure at each stage means: 1, the code does not build; 2, a rule or an architectural boundary of our own code is wrong; 3, an adapter does not meet its boundary; 4, the pieces are not joined or a setting is not read; 5, the artefact cannot be built.

**B2. Trace three examples.** For example:

| Example | Test | Deciding production code | Observable result | Stage |
|---|---|---|---|---|
| AC9 (the expiry boundary) | `ac9_...` | `ApprovalRecord.validAt`, called from `VisitorGate.rejection` | `Rejected: no valid sponsor approval.` at `validUntil`; no reservation | 2 |
| AC10 (operational failure) | `ac10_...` and the third journey | `FileApprovalSource.readAll` throws; nothing catches it on the request path | An `ApprovalSourceException`; no reservation or notice. The demonstration prints `Approval register unavailable: ...` | 2 and 4 |
| AC12 (the flag) | `ac12_...` and the first journey | `VisitorGate.rejection`, the first check | `Rejected: visitor reservations are not enabled.`; the register is not read | 2 and 4 |

**B3. Make a test bite.** A good answer predicts before running. Example: change `FileApprovalSource` so that an unknown status becomes `DENIED`. Prediction: stage 2 passes (no unit test reads the real file), and stage 3 fails at `anUnknownStatusIsAFailureNotADenial`. Section 12.3 lists twenty-seven faults and the tests that caught them; use it to check a prediction after making it, not before.

**B4. The evidence table.** A good answer has one row per risk of Section 13.1, with the test's name and what it cannot show, and at least one risk that nothing here covers, for example: the real directory's behaviour; two concurrent writers of the register; a sponsor who is revoked after a reservation; and the effect of an unusual time zone on the request instant.

### 8.1a Book project, optional steps B5–B7

**B5. Deliver and roll back.** Run the commands of Section 1.4. A good answer records `current` and `previous` after each step (after the second delivery, v2 is current and v1 previous; after the rollback, v1 is current and nothing is previous), and says that the rollback in this simulation changes a folder and not any data.

**B6. AI activity.** See Section 9.

**B7. Break a boundary on purpose.** In a scratch copy, change the timeout of `aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest` from 300 milliseconds to twenty seconds and run `mvn test -Dtest=DirectoryOutageIntegrationTest -Dgroups=integration`. Observed: the test **fails** after 20.03 seconds with `the call must give up after its timeout, but took 20015 ms`, and the class takes 20.58 seconds instead of 1.01. The client did exactly what it was told, and the test's own bound (five seconds) caught that the wait is too long to be useful. A good answer explains two things: a test of a timeout should use a short, injected timeout, and a pipeline that waits for the real timeout of every failure case is itself a problem, because slow feedback gets skipped.

### 8.2 Team project, steps T1–T5

These are not model answers, because the code is your team's. A good answer shows:

- **T1:** the change implemented from the smallest vertical slice outwards; one flag that defaults to off; acceptance examples that each have a test; expected rejections and operational failures that are different results.
- **T2:** a boundary test that does not replace the boundary: a real temporary file, a local stub service or a throw-away database; at least one failure case (missing, malformed or slow); no mock standing in for the reader under test.
- **T3:** the existing suite run first; every changed fixture listed with the reason; tests for the flag on and off.
- **T4:** at least three stages; a captured passing run; a captured failing run read in the form of Section 7.6 (first failing stage, first failing test, why the earlier stages could not have caught it); a stage that fails when it selects nothing.
- **T5:** a removal plan for the flag with a named condition; a rollback step that says what it does not undo; a demonstration; a retrospective with one next action; a limits statement; and the eight items of Section 13.8, each marked complete or a gap.

A weak answer replaces the boundary with a mock and calls it an integration test, tests only the happy path of the boundary, defaults to a guess when a service fails, or claims a hosted run that did not happen.

## 9. AI activity solution

The fixture describes a test that “builds a visitor approval, makes the register return it, and checks that the gate accepts the visitor and that the register was consulted”. The code does that, and nothing more.

| Question | Answer |
|---|---|
| Which part of the system does it touch? | `VisitorGate` and `ApprovalRecord`. Nothing else. |
| Is there a file in it? | No. `mock(ApprovalSource.class)` replaces the register; `FileApprovalSource`, the parser and the file system are not in the test. |
| What does it say after the parser is deleted? | The same: it passes. |
| What does `@Tag("integration")` promise that the body does not deliver? | A test of a real boundary. The tag puts it in stage 3, where it adds time and a false sense of cover. |
| What does `verify(register).find(...)` establish? | That the gate asked the mock for the exact request. That is a fact about the gate, not about the register. |

Both tests were run against two faults, each applied to its own scratch copy of the final code, on the exact configuration of Section 12.2.

| Run | Proposed test | Repaired test |
|---|---|---|
| No fault | Passes | Passes |
| Fault A: the `validFrom` and `validUntil` columns are read the wrong way round | **Passes** | **Fails**: `anApprovedVisitorIsAcceptedFromARealRegisterFile` throws `ApprovalSourceException: Row 2 is not a valid approval record.` |
| Fault B: a broken row is skipped instead of rejecting the whole file | **Passes** | **Fails**: `Expected ApprovalSourceException to be thrown, but nothing was thrown` at the broken-row assertion |

The fixture's description is accurate about what the test does, and the name and tag are misleading about what it verifies. The repaired test writes a real register into a temporary directory, reads it through the real `FileApprovalSource`, passes it to the real gate, and adds the failure case: a broken row appended to the file makes the gate throw the register's exception and not reject politely.

What the original is good for: it is a fair unit test of the gate's decision logic with a controlled source, and it belongs in the unit stage under an honest name (`VisitorGateTest` has several like it). **Accept it as a unit test; reject it as an integration test.**

The repaired test is deliberately small. It does not replace `FileApprovalSourceIntegrationTest`, which carries the detail, and it covers only the faults that reach the gate. A header fault, for example, would pass it. Run against the two faults above, it says what it covers and no more.

The secondary activity (reading a pipeline failure) is Section 7.6. If a live assistant is used, keep its actual output, apply any test it writes to a scratch copy, and run it against a fault. Do not use a generated test to approve generated code.

## 10. Intentionally flawed alternatives

These fragments are **diagnostic alternatives**, not files to compile. Each corresponds to a fault in the experiment of Section 12.3 or to a mistake in Section 13.10 of the chapter.

### 10.1 An outage that becomes “not found”

```java
// WRONG: a failure of the provider is reported as an absent borrower.
try {
    return fetch(key);
} catch (IOException | InterruptedException failure) {
    return null;
}
```

The caller then tells a real borrower that they do not exist. The fault experiment includes “connection failure treated as not found”, and `aRefusedConnectionIsAnOutage` catches it. The correct code fails the request with a `Failure` that the adapter turns into `DirectoryException`.

### 10.2 A guess for an unknown code

```java
// WRONG: an unknown kind is given the nearest known category.
default -> BorrowerCategory.STUDENT;
```

A visitor, or a kind added tomorrow, becomes a student without anyone deciding it. `anUnknownCategoryCodeIsNeverDefaultedToStaffOrStudent` fails it.

### 10.3 A wait that is not bounded

```java
// WRONG: no timeout; the request waits for ever.
HttpRequest request = HttpRequest.newBuilder(uri).GET().build();
```

The officer's screen freezes. `aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest` fails it.

### 10.4 A mock standing in for the file

```java
// WRONG for a test named FileApprovalSource...: the reader is replaced by the thing it should be tested against.
ApprovalSource register = mock(ApprovalSource.class);
```

Section 9 runs it.

### 10.5 A flag that is read once and never removed

```java
// WRONG: a flag with no owner and no removal condition.
public static boolean visitingResearchersEnabled = true;
```

A global, mutable and on by default. It cannot be tested for both settings in one process without cleaning up, and it has no removal plan. The chapter's flag is a constructor argument that defaults to off, and the ADR names the condition for removal.

### 10.6 A stage that can select nothing

```bash
mvn test -Dgroups=integraton   # misspelt: no test has this tag
```

Without `failIfNoTests`, a stage that runs zero tests passes. With it, the stage fails with `No tests were executed!`. The pipeline would otherwise report green for a stage that checked nothing.

## 11. Review answers and transfer solution

### 11.1 Concept answers

**1. Unit test and a file adapter.** A unit test controls everything the unit collaborates with, so it cannot show that the real parser reads the real file correctly: the file system, the encoding, the line endings and the parser are exactly what it has replaced. It shows that the logic that consumes a parsed record is right when given one.

**2. The directory contract.** It says that a known key returns its row, an unknown key returns nothing and is not a failure, and a provider that cannot answer fails and never returns an empty answer. Two implementations (the in-memory fixture and the HTTP client against the stub) pass it, so they are interchangeable for a caller. It can never show how the real provider behaves: the stub's answers are the author's assumption, and a provider contract test run against the real service would be the evidence.

**3. Why not “not found”.** An empty answer tells a caller the borrower is absent. After a timeout we do not know that. Two other defaults the policy refuses: treating an unknown kind code as student or staff, and answering from a cached or earlier result when the provider is down.

**4. Delivery and deployment.** Continuous delivery keeps the software releasable at any time; continuous deployment releases every passing change automatically. `simulate-release.sh` imitates delivery (a release candidate that has passed the stages and is smoke-tested in a staging folder). It imitates no deployment to production.

### 11.2 Applied diagnosis answers

**5. The file reader replaced by a mock.** The risk that is no longer covered is the parse of the real register: the header, the columns, the dates, the encoding and the duplicate keys. Keep the repeatability by using a temporary directory: write the file inside the test, read it with the real adapter, and delete it afterwards. Repeatable and real are not opposites.

**6. A green pipeline and a failing demonstration.** In the pipeline, an end-to-end journey with the flag on, which would have started the program with the flag that the demonstration uses. In the delivery process, a smoke test of the packaged jar with the settings of the target and a printed first line stating the effective setting (the program prints `Visitors enabled: ...`). Both are checks of configuration, and neither is a check of logic.

### 11.3 Transfer solution

For the model-serving team:

| Risk | Check |
|---|---|
| The approval rule (only approved versions are served to external callers) | Unit tests with a controlled approval source: approved, not approved, expired, a different version, the boundary of the validity window |
| The approval list file has a stray column or a duplicate | Integration test with a real temporary file and each failure case; a whole-file rule or a skip rule, chosen and written down |
| The registry times out or returns nonsense | Integration test against a local stub with a bounded wait; the policy says the request fails and the version is not served, and that an unknown version is never defaulted to the latest approved one |
| The flag is on in the demonstration and off in the build | One end-to-end journey that starts the serving process with each setting |
| Old behaviour changed | The existing suite |

The flag enables the rule for external callers; rollback turns it off, but does not recall a response already served or revoke an approval a person already acted on. The evidence would not show the model's accuracy, fairness or drift: nothing here evaluates the model, only the gate in front of it.

### 11.4 Quiz 2 revision pointers

None. Quiz 2 covers the earlier weeks; Section 13.11 of the chapter creates no new assessment.

## 12. Instructor notes and verification

### 12.1 Suggested demonstration and review

Run `pipeline.sh` on a clean copy and read each stage's counts aloud. Then make the header-check fault of Section 7.6 and run it again; ask students to predict which stage fails before they see it. Run the flag-off and flag-on journeys and ask what the first printed line is for. Run the simulated delivery twice and the rollback, and ask what the rollback did not change. Show the proposed AI test passing a parser fault before showing the repaired one failing.

Review the Team project against the eight items of Section 13.8 of the chapter: ask for the first failing stage of the failing run, the name of the test, and a statement of what the pipeline did not check. A weak answer to the last question is “nothing”.

**Alignment with Chapter 12.** Chapter 12 was written separately. Its text refers to a “136-test Chapter 11 suite”, and its acceptance matrix refers to “SD-11 status”; the Chapter 11 companion that this chapter builds on has 159 invocations and four numbered suspected defects (SD-11-1 to SD-11-4), and SD-11-1, the rate for any other kind of borrower, is the one that AC18 now reaches. Its line “SD-11: due-today inclusion preserved; policy unresolved” and its remark that the refactoring removed a duplicated selection rule describe the earlier draft of Chapter 11. In the Chapter 11 of this series a loan due today is *not* listed, and the four suspected defects are about other kinds of borrower (SD-11-1), a loan listed within its grace period (SD-11-2), a null kind (SD-11-3) and the locale of amounts (SD-11-4). These statements need to be reconciled by whoever owns Chapter 12 and the Chapter 11 merge. CR-12 itself, its eighteen acceptance examples and its backlog were used as written, and each example has a test (Section 7.3).

### 12.2 Verification record

This version was verified offline on Windows 11 with **Maven 3.9.11 and JDK 24.0.2**, compiling with `--release 17`, against the **pinned versions** (JUnit Jupiter 5.13.4, Mockito 5.20.0 with ByteBuddy 1.17.7, Compiler Plugin 3.14.1, Surefire 3.5.4, Resources 3.3.1, JAR 3.4.1) in a clean local repository. No JDK 17 was available, and no hosted CI run was made. The listings were extracted from the build that ran.

**Reconstruction.** The listings of the Chapter 10 companion (64), the Chapter 11 companion (26) and this file (31, with four hunks applied by `patch -p1`) were extracted programmatically into a fresh directory, in that order, so that later files replace earlier ones. The result matched the working project file for file (byte for byte), except that the reconstruction also contains the `stages/` directory of the Chapter 11 companion, which is not compiled. `mvn --batch-mode verify` on that reconstruction exited 0 with 232 invocations, no failures, errors or skipped tests, and `bash scripts/pipeline.sh` on it passed all five stages (203, 26 and 3 invocations in stages 2, 3 and 4). This is the reconstruction of Version 1.1; the one of Version 1.0 ran 230 invocations.


| Check | Observed result |
|---|---|
| Full Maven verify | Exit 0; 232 invocations, 0 failures, errors or skipped (159 inherited and 73 new). Version 1.0 ran 230 |
| The pipeline | Exit 0: 203, 26 and 3 invocations in stages 2, 3 and 4; `PIPELINE PASSED` (Version 1.0: 202, 25 and 3) |
| A failing pipeline | Exit 1 with the header check removed: stages 1 and 2 pass; stage 3 fails at `aWrongOrMissingHeaderIsAFailure`; stages 4 and 5 do not start (Section 7.6) |
| A stage that selects nothing | `mvn test -Dgroups=nosuchtag` ends with `No tests were executed!` and `BUILD FAILURE` |
| Command-line tag selection | `-DexcludedGroups=integration,e2e`, `-Dgroups=integration` and `-Dgroups=e2e` selected the 203, 26 and 3 invocations above. The Surefire page documents the parameters in the POM; the command-line form was exercised by running it |
| Timeout probe | Version 1.0 client: 1,725 ms and a result (JDK 24.0.2); corrected client: failure after 326 ms. The review's Java 17 figure (about 1,690 ms) is reported by the review and was not reproduced here |
| Simulated delivery | v1 delivered and smoke-tested (3 journeys passed); v2 delivered and smoke-tested; rollback made v1 current again and smoke-tested it; afterwards `build/staging` held only `current` |
| `javac --release 17 -Xlint:all` | No warnings on the main sources (direct `javac`); the test sources and the two AI files compiled through Maven with the same flag and reported none |
| AI fixture | Baseline: both tests pass. Fault A and fault B: the proposed test passes and the repaired one fails (Section 9) |
| Mockito agent warning | The dynamic-agent warning described in Chapter 7 also appeared on JDK 24; the tests passed |
| Hosted CI, Java 17, real directory, peer review | Not performed or claimed |

### 12.3 Do the tests detect faults?

Thirty faults were run one at a time in a copy of the project, through `mvn test` under the exact configuration, against the final suite of 232 invocations. **Twenty-nine were caught. One survived, and it is an equivalent change** (below). Version 1.0 ran twenty-seven faults against 230 invocations and caught all of them; the HTTP rows have changed because the client changed. The harness reports the first two failing tests, in alphabetical order, so the third column is a sample of what noticed each fault and not a full list.

| Area | Fault | A test that caught it |
|---|---|---|
| Gate | Duration check removed (the register is read for zero days) | `VisitorAcceptanceTest.ac4_...`; `precedence_...` |
| Gate | Flag ignored | `ac12_...`; the first journey |
| Gate | Allowlist also admits MIC1 | `ac5_...`; `anItemOutsideTheAllowlistIsRejectedWithoutReadingTheSource` |
| Gate | Exact-request re-check removed | `aSourceThatReturnsADifferentRequestDoesNotApprove` |
| Gate | Clock read twice | `oneRequestReadsTheClockOnce` |
| Record | Expiry instant is valid | `ac9_...`; `theWindowIncludesItsStartAndExcludesItsEnd` |
| Record | Start instant is not valid | `ac8_...`; `theWindowIncludesItsStartAndExcludesItsEnd` |
| Record | DENIED also approves | `ac6_...`; `aMissingOrDeniedRecordIsAnExpectedRejection` |
| Record | Borrower ignored when matching | The second journey; `aVisitorIsServedThroughTheRealDirectoryAndTheRealApprovalFile` |
| Service | Gate applied to every category | The first and third journeys |
| Service | Visitors bypass the gate | The first and third journeys |
| Rules | Visitors may borrow four days | `ac3_...`; `countAndDurationBoundaries` |
| Rules | Visitors may hold three reservations before another | `ac11_...`; `countAndDurationBoundaries` |
| Directory | Code V maps to STUDENT | The first and third journeys |
| Wiring | Visitors get the staff policy | `ac11_...`; `ac3_...` |
| File | Unknown status becomes DENIED | `anUnknownStatusIsAFailureNotADenial` |
| File | Duplicate keys allowed | `aDuplicateRequestKeyIsAFailureEvenIfTheRowsDisagree` |
| File | Header not checked | `aWrongOrMissingHeaderIsAFailure` |
| File | Extra columns allowed | `aRowWithTheWrongNumberOfColumnsIsAFailure` |
| File | Bad rows skipped instead of rejecting the file | The third journey; `aBlankSponsorOrAnInvalidIntervalIsAFailure` |
| File | Register read once and cached | `theFileIsReadAfreshOnEveryCall` |
| File | First row returned whatever the request | `aRequestWithNoMatchingRowIsEmptyNotAFailure` |
| HTTP | 404 treated as an outage | The first and second journeys |
| HTTP | Other statuses treated as not found | The first and second journeys |
| HTTP | No overall deadline (only the header timeout is left) | `aStalledBodyIsAFailureWithinTheOverallWait` (the only test that notices) |
| HTTP | No timeout of any kind (header timeout and deadline both removed) | `aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest`; `aStalledBodyIsAFailureWithinTheOverallWait` |
| HTTP | Header timeout removed, overall deadline kept | **Survived.** Equivalent: the overall deadline bounds the call either way |
| HTTP | A late answer is treated as not found | `aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest`; `aStalledBodyIsAFailureWithinTheOverallWait` |
| HTTP | Malformed body not checked | `aMalformedAnswerIsAnOutageNotAGuess` |
| HTTP | Connection failure treated as not found | `aRefusedConnectionIsAnOutage`; `aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest` |

Two of the HTTP mutants did not compile at first (a `get()` without a timeout makes the `TimeoutException` handler unreachable) and were rerun as `get(Long.MAX_VALUE, ...)`, which is the same fault expressed so that the code still compiles.

One reading note: some faults were first noticed by an end-to-end journey (the service and directory-mapping faults, for example). That does not mean no narrower test would notice; the harness lists only the first two names. It does mean those faults would be caught by stage 4 if every earlier stage were somehow silent, which is a reason to keep a few journeys.

The experiment of Version 1.0 **could not have found** the defect of Section 7.8, because none of its faults concerned the body of the response. A fault experiment finds the faults that someone thought to apply, which is the same limit as the tests it measures. These counts come from one fault set on one small change, chosen by the author, and they say nothing about how this suite compares with earlier chapters. They do not show that the suite catches every fault, that the real directory behaves like the stub, or that the rule is the right rule.

## References

The online references of the student chapter (sources 1–9, 13 and 14) were opened on 13 October 2026; see the chapter for the source context. Sources 10–12 are not re-opened here.

1. Fowler, M., [Integration Test](https://martinfowler.com/bliki/IntegrationTest.html).
2. Fowler, M., [Contract Test](https://martinfowler.com/bliki/ContractTest.html).
3. Fowler, M., [Deployment Pipeline](https://martinfowler.com/bliki/DeploymentPipeline.html).
4. GitHub, [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions).
5. Fowler, M., [Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html).
6. Hodgson, P., [Feature Toggles (aka Feature Flags)](https://martinfowler.com/articles/feature-toggles.html).
7. Maven, [Using JUnit 5 Platform in Surefire](https://maven.apache.org/surefire/maven-surefire-plugin/examples/junit-platform.html).
8. Oracle, [HttpRequest.Builder (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpRequest.Builder.html).
9. Oracle, [com.sun.net.httpserver (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/jdk.httpserver/com/sun/net/httpserver/package-summary.html).
10. JUnit, [User Guide 5.13.4](https://docs.junit.org/5.13.4/user-guide/).
13. Oracle, [HttpClient (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.net.http/java/net/http/HttpClient.html).
14. Oracle, [CompletableFuture (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/CompletableFuture.html).
