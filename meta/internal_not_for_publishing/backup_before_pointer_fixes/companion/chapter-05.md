---
title: "Chapter 5 Companion: Code, Explanations and Solutions"
weight: 50
---

*Responsibilities, Extension and Substitutability*  
*OO Development and Agile Practices*

## 1. How to use this file

This file contains complete source listings, checkpoint instructions, explanations, exercise solutions and teaching notes for Chapter 5. Attempt the student activities before reading the model answers in Sections 8–11.

The running project remains the Campus Equipment Lending System. Its Java 17 code begins at Chapter 4. We distinguish three checkpoints:

| Checkpoint directory | Meaning | Behaviour |
|---|---|---|
| `before` | Chapter 4 starting point | Existing student reservation rule and private confirmation method |
| `refactored` | Stage A | Same behaviour; concrete formatter extracted |
| `after` | Stage B; cumulative exit checkpoint | Student behaviour preserved; explicit staff policy added |

Only `after` is the cumulative Chapter 5 result. The separate LSP example is a teaching counterexample; it does not become a reservation collaborator. US-02 availability enquiry remains planned. No actual staff directory, authentication, catalogue, persistence, cancellation or notification delivery is introduced.

### 1.1 Assemble the directories

For a fully independent reconstruction, create the three checkpoint directories above. The listings are divided as follows:

1. Section 2 uses paths beginning with `shared/`. Save those files there, then copy the **contents** of `shared` into each checkpoint. For example, `shared/src/main/java/LoanPeriod.java` becomes `before/src/main/java/LoanPeriod.java`, `refactored/src/main/java/LoanPeriod.java` and `after/src/main/java/LoanPeriod.java`.
2. Section 3 supplies `before`-specific files. Copy its `ReservationRules.java` and `scripts/check.sh` into the same relative locations in `refactored` too. Do **not** copy its coordinator into `refactored`.
3. Section 4 supplies the extracted coordinator and formatter. Copy that formatter into `after/src/main/java/ConfirmationFormatter.java` too.
4. Section 5 supplies the remaining `after` files, including its changed student rules and updated gate.
5. Section 6 supplies the isolated LSP example under `after/examples/lsp`.

Create intermediate directories as needed. Copy the content inside each code fence, not the fence or heading. Keep only one class with each name inside a checkpoint. Compile each checkpoint separately; do not compile every `.java` file beneath the parent directory at once.

The directory prefixes describe alternative teaching checkpoints, not Java packages. Classes remain in the unnamed package. The common application layout is `src/main/java`; executable checks are in `src/test/java`. These are plain Java programs, not JUnit tests, and this chapter does not introduce a Maven configuration.

If you already have the Chapter 4 repository, you may instead make successive commits for Stage A and Stage B. The separate directories are a reconstruction aid, not a requirement to maintain duplicate application trees in your team's repository.

### 1.2 Run each checkpoint

Use Java 17 JDK and Bash. Confirm that `java -version` and `javac -version` refer to the intended installation. From the directory containing the three checkpoints:

```bash
bash before/scripts/check.sh
bash refactored/scripts/check.sh
bash after/scripts/check.sh
java -cp after/build/classes Chapter04Demo
java -cp after/build/classes Chapter05Demo
```

The scripts change to their own checkpoint root, compile application and check sources, then run the relevant checks. Ordinary learner setup uses `javac`; no compiler override is needed with a normal JDK installation.

### 1.3 Run PMD

Install PMD once. Download `pmd-dist-7.28.0-bin.zip` from the project's GitHub release page (`https://github.com/pmd/pmd/releases`, tag `pmd_releases/7.28.0`). The release page shows a SHA-256 digest for each file; the digest recorded for this file when this chapter was checked was:

```text
f974ba571f7bc01c73fffe11bade25fbc1f438698f9e9c00e416e8d65e9fbac2
```

Compare it with the digest of your download (`sha256sum pmd-dist-7.28.0-bin.zip`), unzip the file into its own new folder, and set `PMD_HOME` to the `pmd-bin-7.28.0` folder inside it. PMD needs a Java runtime of version 8 or above. From each checkpoint directory:

```bash
export PMD_HOME=/path/to/pmd-bin-7.28.0
bash scripts/check.sh
bash scripts/pmd.sh
```

Expected output for `before` is in Section 7.1b. The ruleset and script are listings 2.8 and 2.9 and are copied into every checkpoint with the other shared files.

The first two gates should report the original 34 checks and five acceptance example groups passing. The final gate additionally prints:

```text
All 44 Chapter 5 checks passed.
BUILD AND CHECKS PASSED
```

The original example groups contain multiple assertions. Report the groups and check counts separately rather than treating them as identical units.

The Chapter 4 demonstration must retain its original output:

```text
Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Rejected: item unavailable.
Confirmed: R2 for B2 on CAM1 [2026-10-22, 2026-10-23).
Stored reservations: 2
```

The new demonstration should print:

```text
Confirmed: R1 for S1 on CAM1 [2026-10-20, 2026-11-03).
Rejected: borrower limit or duration.
Rejected: item unavailable.
Confirmed: R2 for B1 on CAM1 [2026-11-03, 2026-11-04).
Stored reservations: 2
```

The first request explicitly selects the illustrative staff policy. The second uses the original student operation and rejects fourteen days. The third is a valid-duration student request blocked by the staff reservation. The fourth begins at the staff reservation's exclusive end, so it can succeed. Rejections do not consume identifiers or add records.

## 2. Shared files for all three checkpoints

These files are unchanged from Chapter 4. Their repetition makes the examples reconstructable from this Markdown file.

### 2.1 `shared/src/main/java/LoanPeriod.java`

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

### 2.2 `shared/src/main/java/Reservation.java`

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

### 2.3 `shared/src/main/java/Chapter04Demo.java`

```java
import java.time.LocalDate;

public final class Chapter04Demo {
    public static void main(String[] args) {
        ReservationCoordinator coordinator = new ReservationCoordinator();
        LocalDate start = LocalDate.of(2026, 10, 20);
        System.out.println(coordinator.reserve("B1", "CAM1", start, 2));
        System.out.println(coordinator.reserve("B2", "CAM1", start.plusDays(1), 1));
        System.out.println(coordinator.reserve("B2", "CAM1", start.plusDays(2), 1));
        System.out.println("Stored reservations: " + coordinator.reservations().size());
    }
}
```

### 2.4 `shared/src/test/java/Chapter02Checks.java`

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

        ReservationCoordinator c = new ReservationCoordinator();
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

        ReservationCoordinator invalid = new ReservationCoordinator();
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

### 2.5 `shared/src/test/java/Chapter03AcceptanceExamples.java`

```java
import java.time.LocalDate;

public class Chapter03AcceptanceExamples {
    public static void main(String[] args) {
        LocalDate day = LocalDate.of(2026, 10, 20);
        ReservationCoordinator coordinator = new ReservationCoordinator();

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
        ReservationCoordinator limits = new ReservationCoordinator();
        for (String item : new String[] {"CAM1", "MIC1", "TRI1"}) {
            require(limits.reserve("B1", item, day, 1).startsWith("Confirmed:"),
                    "AC-04 establish three valid reservations");
        }
        require(limits.reserve("B1", "CAM2", day, 1).equals(
                "Rejected: borrower limit or duration."), "AC-04 fourth rejected");
        require(limits.reservations().size() == 3, "AC-04 unchanged count");
        System.out.println("AC-04 passed");

        // AC-05: one and seven days are allowed; zero, negative and eight are not.
        ReservationCoordinator durations = new ReservationCoordinator();
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

### 2.6 `shared/.gitignore`

```gitignore
/build/
*.class
```

### 2.7 `shared/.gitattributes`

```gitattributes
*.sh text eol=lf
```

This is the Chapter 4 file that keeps shell scripts in LF form when Git on Windows converts line endings. Without it, a CRLF copy of `scripts/check.sh` fails under WSL or Linux bash. Commit it with the other files.

### 2.8 `shared/config/pmd-smells.xml`

```xml
<?xml version="1.0"?>
<ruleset name="SE506 design-smell lab"
         xmlns="http://pmd.sourceforge.net/ruleset/2.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://pmd.sourceforge.net/ruleset/2.0.0 https://pmd.sourceforge.io/ruleset_2_0_0.xsd">
  <description>
    Design-smell rules for the Chapter 5 lab. Every rule keeps PMD's default threshold.
    Choosing a small set of rules is a decision: PMD's other categories report many findings
    that this lab does not use.
  </description>

  <rule ref="category/java/design.xml/CyclomaticComplexity"/>
  <rule ref="category/java/design.xml/CognitiveComplexity"/>
  <rule ref="category/java/design.xml/NPathComplexity"/>
  <rule ref="category/java/design.xml/GodClass"/>
  <rule ref="category/java/design.xml/DataClass"/>
  <rule ref="category/java/design.xml/TooManyMethods"/>
  <rule ref="category/java/design.xml/ExcessiveParameterList"/>
  <rule ref="category/java/design.xml/ExcessiveImports"/>
</ruleset>
```

This is the Week 4 lab rule set: eight rules from PMD's design category, each with PMD's default threshold. It is deliberately small. Section 7.1b compares it with PMD's other rule sets.

### 2.9 `shared/scripts/pmd.sh`

```bash
#!/usr/bin/env bash
# Runs PMD's design-smell rules on the application sources. Run scripts/check.sh first if you
# want type information (it creates build/classes). PMD_HOME is the unzipped pmd-bin-7.28.0 directory.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
: "${PMD_HOME:?Set PMD_HOME to the unzipped pmd-bin-7.28.0 directory}"
aux=()
if [ -d build/classes ]; then
  aux=(--aux-classpath build/classes)
fi
PMD_JAVA_DISABLE_AUX_CLASSPATH_WARNINGS=true \
  "$PMD_HOME/bin/pmd" check -d src/main/java -R config/pmd-smells.xml \
  -f text --no-progress --no-cache --no-fail-on-violation "${aux[@]}"
```

The script runs PMD on the application sources and prints the findings. It passes `--no-fail-on-violation` so that findings do not make the script fail, because the lab *expects* findings. Without that option PMD exits with status 4 when it reports violations. Run `scripts/check.sh` first if you want PMD to read the compiled classes. The setting `PMD_JAVA_DISABLE_AUX_CLASSPATH_WARNINGS` only silences a warning about the Java version of the compiler's own runtime image; other `[WARN]` lines, such as the advice to use incremental analysis, may still appear on the error stream.

## 3. Starting checkpoint: before

The coordinator and numeric rule below are the complete starting versions. Copy the rule and gate to `refactored` as directed in Section 1; the intermediate stage changes neither of them.

### 3.1 `before/src/main/java/ReservationRules.java`

```java
public final class ReservationRules {
    public boolean mayRequest(int activeReservations, int requestedDays) {
        return activeReservations >= 0
                && activeReservations < 3
                && requestedDays >= 1
                && requestedDays <= 7;
    }
}
```

### 3.2 `before/src/main/java/ReservationCoordinator.java`

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class ReservationCoordinator {
    private final List<Reservation> reservations = new ArrayList<>();
    private final ReservationRules rules = new ReservationRules();

    public String reserve(String borrowerId, String itemId,
                          LocalDate start, int requestedDays) {
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
        if (!rules.mayRequest(activeCount, requestedDays)) {
            return "Rejected: borrower limit or duration.";
        }

        LoanPeriod requested = new LoanPeriod(
                start, start.plusDays(requestedDays));
        for (Reservation existing : reservations) {
            if (existing.itemId().equals(itemId)
                    && existing.period().overlaps(requested)) {
                return "Rejected: item unavailable.";
            }
        }

        Reservation reservation = new Reservation(
                "R" + (reservations.size() + 1), borrowerId, itemId, requested);
        reservations.add(reservation);
        return confirmationFor(reservation);
    }

    private String confirmationFor(Reservation reservation) {
        return "Confirmed: " + reservation.id()
                + " for " + reservation.borrowerId()
                + " on " + reservation.itemId()
                + " [" + reservation.period().start()
                + ", " + reservation.period().endExclusive() + ").";
    }

    public List<Reservation> reservations() {
        return List.copyOf(reservations);
    }
}
```

### 3.3 `before/scripts/check.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p build/classes
# Remove only generated files from this starter's output directory.
find build/classes -type f -name '*.class' -delete

java -version
"${CHAPTER_JAVAC:-javac}" --release 17 -encoding UTF-8 -d build/classes \
  src/main/java/*.java src/test/java/*.java
java -cp build/classes Chapter02Checks
java -cp build/classes Chapter03AcceptanceExamples
echo "BUILD AND CHECKS PASSED"
```

## 4. Stage A: formatter extraction

Use the shared files, the starting rule and starting gate, then add these two files to `refactored`. The formatter is also used unchanged in `after`.

### 4.1 `refactored/src/main/java/ConfirmationFormatter.java`

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

### 4.2 `refactored/src/main/java/ReservationCoordinator.java`

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class ReservationCoordinator {
    private final List<Reservation> reservations = new ArrayList<>();
    private final ReservationRules rules = new ReservationRules();
    private final ConfirmationFormatter formatter = new ConfirmationFormatter();

    public String reserve(String borrowerId, String itemId,
                          LocalDate start, int requestedDays) {
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
        if (!rules.mayRequest(activeCount, requestedDays)) {
            return "Rejected: borrower limit or duration.";
        }

        LoanPeriod requested = new LoanPeriod(
                start, start.plusDays(requestedDays));
        for (Reservation existing : reservations) {
            if (existing.itemId().equals(itemId)
                    && existing.period().overlaps(requested)) {
                return "Rejected: item unavailable.";
            }
        }

        Reservation reservation = new Reservation(
                "R" + (reservations.size() + 1), borrowerId, itemId, requested);
        reservations.add(reservation);
        return formatter.format(reservation);
    }

    public List<Reservation> reservations() {
        return List.copyOf(reservations);
    }
}
```

### 4.3 Explanation of the structural change

The private confirmation expression moved into `ConfirmationFormatter.format`. Its string content is unchanged. The coordinator stores the accepted reservation before requesting its text, just as before. The formatter receives only the immutable accepted record, not a reference to mutable storage or an eligibility rule.

The new formatter rejects a null reservation explicitly. That method is a new collaborator API; existing coordinator calls supply a valid reservation. The extraction does not change the existing public request method's validation or rejection behaviour.

The coordinator still creates the formatter directly. No interface was added for it because this checkpoint has one presentation behaviour and no requirement to swap implementations. The formatter is also not a notification sender: returning a string does not send email.

Compare the `before` and `refactored` coordinator listings. The only application changes are the new formatter field, the delegated return expression and removal of the old private method. Run the unchanged checks before beginning Stage B.

## 5. Stage B: explicit policy variation

Use the shared files and the extracted formatter, then add the following files to `after`. This is the complete cumulative result. The staff limits are an illustrative teaching requirement: fewer than five existing active records and a requested duration from one to fourteen days. They are not approved institutional policy.

### 5.1 `after/src/main/java/BorrowingPolicy.java`

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

### 5.2 `after/src/main/java/ReservationRules.java`

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

### 5.3 `after/src/main/java/StaffReservationRules.java`

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

### 5.4 `after/src/main/java/BorrowerCategory.java`

```java
public enum BorrowerCategory {
    STUDENT, STAFF
}
```

### 5.5 `after/src/main/java/ReservationCoordinator.java`

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class ReservationCoordinator {
    private final List<Reservation> reservations = new ArrayList<>();
    private final BorrowingPolicy studentPolicy = new ReservationRules();
    private final BorrowingPolicy staffPolicy = new StaffReservationRules();
    private final ConfirmationFormatter formatter = new ConfirmationFormatter();

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
        if (!policyFor(category).mayRequest(activeCount, requestedDays)) {
            return "Rejected: borrower limit or duration.";
        }

        LoanPeriod requested = new LoanPeriod(
                start, start.plusDays(requestedDays));
        for (Reservation existing : reservations) {
            if (existing.itemId().equals(itemId)
                    && existing.period().overlaps(requested)) {
                return "Rejected: item unavailable.";
            }
        }

        Reservation reservation = new Reservation(
                "R" + (reservations.size() + 1), borrowerId, itemId, requested);
        reservations.add(reservation);
        return formatter.format(reservation);
    }

    private BorrowingPolicy policyFor(BorrowerCategory category) {
        return switch (category) {
            case STUDENT -> studentPolicy;
            case STAFF -> staffPolicy;
        };
    }

    public List<Reservation> reservations() {
        return List.copyOf(reservations);
    }
}
```

### 5.6 `after/src/main/java/Chapter05Demo.java`

```java
import java.time.LocalDate;

public final class Chapter05Demo {
    public static void main(String[] args) {
        ReservationCoordinator coordinator = new ReservationCoordinator();
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

### 5.7 `after/src/test/java/Chapter05Checks.java`

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
        ReservationCoordinator c = new ReservationCoordinator();
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

        ReservationCoordinator limits = new ReservationCoordinator();
        for (int i = 1; i <= 5; i++) {
            check(limits.reserve("S2", "ITEM" + i, day, 1, BorrowerCategory.STAFF)
                    .startsWith("Confirmed:"), "staff reservation " + i);
        }
        List<Reservation> five = limits.reservations();
        check(limits.reserve("S2", "ITEM6", day, 1, BorrowerCategory.STAFF).equals(
                "Rejected: borrower limit or duration."), "staff sixth rejected in coordinator");
        check(limits.reservations().equals(five), "staff limit preserves records");

        ReservationCoordinator defaultStudent = new ReservationCoordinator();
        ReservationCoordinator explicitStudent = new ReservationCoordinator();
        check(defaultStudent.reserve("B1", "MIC1", day, 7).equals(
                explicitStudent.reserve("B1", "MIC1", day, 7, BorrowerCategory.STUDENT)),
                "default and explicit student results agree");
        check(defaultStudent.reserve("B2", "TRI1", day, 8).equals(
                "Rejected: borrower limit or duration."), "default remains student");

        // Counts belong to a borrower ID across all records, not separate category buckets.
        ReservationCoordinator mixedFixture = new ReservationCoordinator();
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

### 5.8 `after/scripts/check.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p build/classes
# Remove only generated files from this starter's output directory.
find build/classes -type f -name '*.class' -delete

java -version
"${CHAPTER_JAVAC:-javac}" --release 17 -encoding UTF-8 -d build/classes \
  src/main/java/*.java src/test/java/*.java
java -cp build/classes Chapter02Checks
java -cp build/classes Chapter03AcceptanceExamples
java -cp build/classes Chapter05Checks
echo "BUILD AND CHECKS PASSED"
```

### 5.9 Why this is a modest extension point

Both policies answer the same count-and-duration question. `ReservationRules` preserves its original predicate and gains an interface declaration. `StaffReservationRules` supplies the second documented predicate. Neither asks about item availability or creates records.

The original four-argument operation delegates with `STUDENT`. The five-argument overload validates the category and uses the selected policy. A null category raises `NullPointerException` before any state mutation. This is a new overload's documented behaviour; old callers always supply the non-null student category through delegation.

The selector remains in the coordinator, and the concrete policies are still created there. Adding a new enum category requires another selection arm. The design isolates policy evaluation; it does not claim complete closure against adding categories. Chapter 6 will examine moving object selection and assembly outward.

The category is supplied by trusted synthetic callers. The program does not authenticate it or remember it in a borrower profile. The mixed-category fixture in the checks intentionally documents this limitation: all records for a borrower ID count, while the category on the current request selects the limit. It is not a recommended real-world workflow for changing a borrower's authority.

### 5.10 What the new checks establish

The two policies are passed through `BorrowingPolicy` references, exercising their common input handling and repeatability. The helper also checks some cases shared by these two *documented* policies, such as accepting one day at count zero. A future policy with different legitimate limits must have its own concrete expectations; the interface does not universally require every implementation to approve one day.

The integrated checks cover staff's five-record and fourteen-day boundaries, the old student default, cross-category conflicts and adjacency, and unchanged records after rejection. The test uses `List.equals` on snapshots of immutable reservations. Because `Reservation` has identity equality here, equality also requires the same record objects in the same order; a replacement with different record objects would fail.

These finite checks do not prove every possible input and call sequence. Reading the short predicates and checking that they have no mutable state or external calls complements the boundary evidence. The original 34 checks and five acceptance groups remain unchanged and still run.

## 6. Separate LSP counterexample

This is an isolated teaching program, not an application dependency. The invalid subtype is deliberately labelled. Its harness succeeds only when it observes the expected counterexample and the separate positive-history type obeys its own contract.

### 6.1 `after/examples/lsp/LspExample.java`

```java
import java.util.ArrayList;
import java.util.List;

public final class LspExample {
    // Contract: accept any int, append it once, and preserve earlier values in order.
    static class IntHistory {
        private final List<Integer> values = new ArrayList<>();

        public void add(int value) { values.add(value); }
        public List<Integer> values() { return List.copyOf(values); }
    }

    // INTENTIONALLY INVALID SUBTYPE: strengthens the precondition of add.
    static final class PositiveOnlyHistory extends IntHistory {
        @Override
        public void add(int value) {
            if (value <= 0) throw new IllegalArgumentException("Positive values only.");
            super.add(value);
        }
    }

    // Separate type with an honest, narrower contract; not an IntHistory subtype.
    static final class PositiveHistory {
        private final IntHistory entries = new IntHistory();

        public void addPositive(int value) {
            if (value <= 0) throw new IllegalArgumentException("Positive values only.");
            entries.add(value);
        }
        public List<Integer> values() { return entries.values(); }
    }

    private static void client(IntHistory history) {
        history.add(5);
        history.add(-2);
        if (!history.values().equals(List.of(5, -2))) {
            throw new AssertionError("Client expects both entries in order.");
        }
    }

    public static void main(String[] args) {
        client(new IntHistory());
        System.out.println("Base contract client passed.");
        boolean counterexampleObserved = false;
        try {
            client(new PositiveOnlyHistory());
        } catch (IllegalArgumentException expected) {
            counterexampleObserved = true;
            System.out.println("Expected counterexample: " + expected.getMessage());
        }
        if (!counterexampleObserved) {
            throw new AssertionError("Expected the invalid subtype to reject -2.");
        }
        PositiveHistory positive = new PositiveHistory();
        positive.addPositive(5);
        boolean invalidRejected = false;
        try {
            positive.addPositive(-2);
        } catch (IllegalArgumentException expected) {
            invalidRejected = true;
        }
        if (!invalidRejected || !positive.values().equals(List.of(5))) {
            throw new AssertionError("Narrower type must reject without changing entries.");
        }
        System.out.println("Separate positive-history contract passed.");
    }
}
```

### 6.2 Compile and run the isolated example

From the directory containing the three checkpoints:

```bash
javac --release 17 -d after/build/lsp after/examples/lsp/LspExample.java
java -cp after/build/lsp LspExample
```

Expected output:

```text
Base contract client passed.
Expected counterexample: Positive values only.
Separate positive-history contract passed.
```

`client` accepts an `IntHistory` reference. It validly adds 5 and -2, then expects both values in order. The subclass rejects -2, strengthening the accepted-input requirement. Java accepts the override because the signature fits; that does not establish behavioural substitutability.

The corrected `PositiveHistory` has its own public `addPositive` operation and does not claim to be an `IntHistory`. It uses composition internally and rejects invalid values without changing existing entries. It could still be badly designed if it advertised the broad contract through another interface; the key repair is agreement between the public promise and the type relationship.

The harness catches the expected exception outside the base client so it can demonstrate and explain the failure. An overall exit status of zero here means the counterexample was successfully observed, not that the invalid subtype satisfies the base contract. The application gate does not compile or run this isolated teaching directory.

## 7. Model design diagnosis and rationale

### 7.1 Responsibility diagnosis

| Element | Present responsibility | Relevant change pressure | Decision in this chapter |
|---|---|---|---|
| `ReservationCoordinator` | Sequence validation, eligibility, conflict detection and storage | Request workflow and collaborator selection | Preserve sequencing; delegate formatting and policy evaluation |
| `ReservationRules` | Student count/duration decision | Student borrowing limits | Preserve predicate; implement the shared policy contract |
| `LoanPeriod` | Valid interval and overlap semantics | Meaning of dates and boundaries | Leave unchanged |
| `Reservation` | Immutable accepted-record details | Data carried by a reservation | Leave unchanged |
| Confirmation expression | Render an accepted record as text | Wording/layout needs | Extract a concrete formatter |
| Staff eligibility | New count/duration variation | Explicit illustrative staff rule | Add a separate policy implementation |

The original coordinator already delegated numeric rules. Claiming that this chapter first extracts them would misdescribe the starting point. The real design pressure is independent presentation change plus a newly stated second policy.

### 7.1a Model manual smell review of the starting coordinator

This is the answer to the manual smell review in Section 5.1 of the student chapter, applied to the listing in Section 3.2. It is a model of the reading step, done before any tool is run; the tool comparison follows in Section 7.1b. `javac -Xlint:all` printed nothing on this code.

| Smell | Where it appears in `reserve` | Matches a change pressure? | Act now? |
|---|---|---|---|
| More than one reason to change | One method validates identifiers, counts the borrower's records, applies eligibility, searches for a conflict, creates and stores the record and, through `confirmationFor`, produces the wording | Yes: wording and staff eligibility are listed pressures | Yes for wording (Stage A) and eligibility (Stage B); no for storage |
| Hidden construction | `private final ReservationRules rules = new ReservationRules();` fixes the policy inside the coordinator | Yes: the staff variation needs another policy | Only as far as Stage B needs; full dependency choice is Chapter 6 |
| Repeated or similar logic | Two loops over `reservations` differ only in the test (`borrowerId` count versus `itemId` overlap); rejections are returned as two plain strings | Weakly: no listed pressure asks for it | No: two short loops are clearer than a new abstraction here |
| Primitive values standing for concepts | `borrowerId`, `itemId` and `requestedDays` are strings and an integer; the rejection reasons are free text | No pressure in this chapter | No: record it as a limitation |

What `-Xlint:all` did not show: every row above. What reading alone did not settle: whether the repeated loops justify an abstraction, which depends on future change, so a correct answer may reasonably leave them.

Potential storage extraction is a reasonable observation, but persistence is not part of the selected change. A diagnosis should distinguish “this may matter later” from “we have evidence that this boundary is needed now”. A proposed repository interface earns no credit merely because a diagram can accommodate it.

### 7.1b Model PMD comparison

PMD 7.28.0 was run on the `before` checkpoint with the lab rule set (`config/pmd-smells.xml`) after the gate had compiled the classes. The output is exactly what the chapter shows (with Windows path separators in the recorded run):

```text
src\main\java\Reservation.java:3:	DataClass:	The class 'Reservation' is suspected to be a Data Class (WOC=0.000%, NOPA=0, NOAM=4, WMC=9)
src\main\java\ReservationCoordinator.java:10:	CyclomaticComplexity:	The method 'reserve(String, String, LocalDate, int)' has a cyclomatic complexity of 12.
[INFO] Found 2 violations.
```

| Source | Finding | Group | Interpretation and action |
|---|---|---|---|
| PMD, `CyclomaticComplexity` | `reserve` has complexity 12 (threshold 10) | **Useful** | The method validates, counts, applies eligibility, searches for conflicts and creates the record. It matches the first manual smell. Act on the part that has a pressure: wording (Stage A) and eligibility (Stage B). Leave the sequence of checks, and say so |
| PMD, `DataClass` | `Reservation` is a suspected data class | **Low-value here** | It is an immutable record of an accepted booking, so data without behaviour is its design. Keep it, and note that the behaviour using its fields (the wording) is what moved in Stage A |
| Manual reading | `new ReservationRules()` inside the coordinator | **Missed by the tool** | The coordinator fixes its own policy. Act only as far as Stage B needs; the full dependency choice is Chapter 6 |
| Manual reading | “Borrower limit or duration” is one string for two reasons | **Missed by the tool** | A caller must compare strings. Record it as a limitation; no pressure in this chapter |
| Manual reading | Two similar loops over `reservations` | Not reported by PMD at its default thresholds | Leave them, as in Section 7.1a |

**Rule sets compared on the same five files.** The result is the reason the lab uses a small set.

| PMD rule set | Findings on `before` | What they were |
|---|---|---|
| Lab set (eight design rules) | 2 | The two above |
| `rulesets/java/quickstart.xml` | 5 | All `NoPackage`: the book uses the unnamed package until Chapter 10 |
| `category/java/codestyle.xml` | 34 | `MethodArgumentCouldBeFinal`, `LocalVariableCouldBeFinal`, `NoPackage`, `OnlyOneReturn` and similar style rules |
| `category/java/bestpractices.xml` | 4 | `SystemPrintln` in the demonstration class |

**After each stage.** PMD with the lab rule set reported the same two findings on `refactored` and `after`: `Reservation` as a data class, and `reserve` at complexity 12 (in `after` the method is the five-argument overload, at line 17). The refactorings changed who decides wording and eligibility, not the number of branches in the sequence of checks, so a student who expects the finding to disappear should be asked what the tool measures.

**The extraction experiment (optional extension).** In a scratch copy of `after`, `reserve` was split by extracting `activeReservationsOf(borrowerId)` and `isUnavailable(itemId, requested)` as private methods. The gate still passed (all five acceptance groups and 44 checks), and PMD reported only the data-class finding: the complexity finding disappeared. The class still validates, counts, checks eligibility, searches and creates, so every responsibility is where it was. The tool reports the number of branches in one method, and Extract Method lowers it without moving a responsibility. Use this to show why a number is not a verdict.

### 7.2 Suggested Stage A rationale

> Confirmation wording can change independently of reservation eligibility and conflicts. I moved the existing expression into a concrete formatter that receives the accepted immutable record. The coordinator still stores the record before formatting, returns the same text, and rejects requests as before. The original checks pass without edited expectations. This adds one collaborator and leaves direct construction in place.

This rationale says what changed, why, which behaviour was preserved and what cost remains. It is stronger than “SRP means every method needs a class”. It also avoids claiming that the formatter delivers notifications.

### 7.3 Suggested Stage B rationale

> Student and staff requests now have two documented count/duration policies. A small `BorrowingPolicy` contract lets the reservation workflow use either without duplicating overlap or storage logic. The existing overload explicitly keeps student behaviour. The policy selector still lives in the coordinator, so adding another category requires an edit there. Category comes from a trusted fixture and is not verified identity.

The new staff success cases mean this stage is a feature change. The fact that some restructuring occurs while adding it does not make the complete stage behaviour-preserving. Keep the requirements and checks for the feature visible in the change record.

### 7.4 Alternatives that deserve consideration

**Keep the formatter as a private method.** This is defensible when wording is small, stable and changes with the request workflow. It avoids another object and file. The chapter chooses extraction because independent wording change is now an explicit pressure. A student who keeps the method should explain how the stated pressure will be managed, not merely reject classes on aesthetic grounds.

**Use a limits object.** Since the current policies differ only in constants, a validated object with maximum-active and maximum-days values can express both. Validate configuration at construction and retain the common handling of negative counts and nonpositive durations. This approach avoids separate classes for each numeric combination. It is less direct if future policies require qualitatively different decisions; that future must remain a reasoned possibility, not a fabricated requirement.

**Keep a local conditional.** A small conditional can be clearer than an abstraction in a very small program. Its cost grows if the same category decision is copied across validation, messaging and storage. The chapter's interface avoids duplicating the decision operation while leaving selection explicit.

**Subclass the coordinator.** This is a poor fit for the chosen variation. It risks copying or overriding the whole request workflow to change one rule. The current coordinator is also `final`. Removing that modifier solely to gain access to a subclassing technique does not establish that the inheritance contract is sound.

### 7.5 Contract comparison

| Contract | Legitimate inputs/outcomes | Client may not assume |
|---|---|---|
| Common `BorrowingPolicy` | Every integer pair can be evaluated; invalid numeric inputs return false; decision is deterministic and free of the forbidden side effects | Every policy has student limits or proves availability |
| Student policy | Counts 0–2 and days 1–7 accepted; other pairs rejected | Fourteenth-day staff behaviour |
| Staff policy | Counts 0–4 and days 1–14 accepted; other pairs rejected | An authoritative staff identity check |
| Original `reserve` overload | Existing student eligibility and request workflow preserved | Selecting a category based on identifier text |
| Explicit-category overload | Uses the supplied non-null category and all existing records for that borrower | Persisted category or permission to choose staff status |

The shared policy type permits different decision results because concrete limits are documented per implementation. By contrast, a `ReservationRules` client specifically relying on the student predicate has a stronger expectation. The staff class should not claim to be that exact student-policy type.

A broader interface must still promise enough to be useful. If it permits arbitrary exceptions, hidden mutation, random decisions and unbounded external operations, it stops supporting the coordinator's simple reasoning. Broadening a contract to excuse a defective implementation can make existing clients incorrect.

## 8. AI activity: model review

The fixture in the student chapter is author-written fictional AI output. These verdicts illustrate a review method; they are not a record of a real model or reviewer.

| Proposed change | Verdict | Concrete reason |
|---|---|---|
| Give every class an interface | Not justified as stated | No second role or client need is identified for immutable record and interval values; it adds naming and navigation |
| Add coordinator factory and abstract base | Defer | Two rules do not require a factory hierarchy; direct policy selection remains inspectable |
| Replace rejection strings with exceptions | Separate feature/API proposal | Existing callers and acceptance examples observe the current rejection results |
| Make staff rules extend student rules | Reject for this source and contract | `ReservationRules` is final; removing final would still leave staff approval incompatible with the exact student predicate |
| Remove all conditionals so no file ever changes | Reject the promise | An implementation must still be selected somewhere; moving or hiding that decision is not eliminating it |
| Shorten the extracted confirmation to “Reserved” | Reject during Stage A | The exact output changes, so the stage is no longer the promised extraction |
| Green build proves SOLID | Reject | Compilation and checks examine limited behaviour; responsibility and extension claims still need reasoning |

A minimal corrected plan is: run the baseline; extract the unchanged formatter; verify Stage A; state the staff rule; introduce the small policy contract and explicit category path; preserve the old default; run old and new checks; inspect remaining direct dependencies. No real directory or notification integration is required.

Independent evidence includes the `final` declaration, exact confirmation assertions, rejection checks, the selector's source and the source of the category argument. A confident explanation from an AI service does not override those facts.

An acceptable review record contains the candidate claim, accepted/rejected/deferred verdict, reason and evidence. Do not reject the whole output merely because it contains many classes. Identify which boundary lacks a purpose or which behaviour changes. Some larger designs are justified by larger requirements; those requirements are absent here.

## 9. Review-question solutions

### 9.1 Concept questions

**1. Method count and SRP.** `LoanPeriod` has construction, accessors and overlap behaviour supporting one interval abstraction. A single `process` method could contain borrowing rules, persistence and message formatting. Count does not identify independent change pressures. Use the relevant decisions and the reasons they change.

**2. Protected variation and remaining edits.** The reservation algorithm delegates count/duration decisions, so changing staff limits need not alter overlap detection or storage. The category selector and directly constructed policy fields remain in the coordinator. Adding another category requires updating that selection arrangement; the entire coordinator is not closed against that change.

**3. Different booleans with one interface.** The common contract defines the kind of question, valid input handling, determinism and side-effect restrictions. It allows implementation-specific documented limits. Student and staff results for fourteen days differ within that contract. A client that assumes seven days for every implementation has assumed more than the interface promises.

**4. Refactoring versus feature.** Stage A changes where a fixed result is produced while preserving the existing public operation's outputs, state effects and failure behaviour. Stage B introduces successful requests that were not previously available through the old policy. The preserved student path is compatibility evidence within a broader feature addition.

### 9.2 Applied diagnosis

**5. Throwing for negative count and incrementing a counter.** Negative counts are accepted inputs with a specified false result. Throwing instead changes an observable outcome and can break a client that simply branches on the boolean. Pass `(-1, 1)` through a `BorrowingPolicy` reference and assert false; an unexpected exception exposes the defect.

The counter conflicts with this chapter's explicit no-counter-change contract. Repeating the same inputs may reveal a changed result if the implementation uses the counter, but equal results alone do **not** prove that a hidden counter was not incremented. Inspect the implementation for mutable state, or observe an exposed effect where available. Do not claim that a finite set of return-value checks can establish absence of every internal mutation.

If counting evaluations becomes a genuine operational requirement, revisit the contract and where that concern belongs. Adding it silently inside the policy changes the stated design promise. The answer should distinguish the independently observable exception defect from the evidence needed for the internal-state claim.

**6. Silently ignoring negative values.** The base history promises to append any integer once and preserve earlier values. After `add(5); add(-2);`, a result of `[5]` weakens the append postcondition even though no exception occurred. Use the valid base client to compare the complete resulting sequence. Either retain broad acceptance in the subtype or expose a separate narrower type whose contract explicitly restricts input. Changing the base contract would require reviewing existing callers and is not a transparent repair.

## 10. Practical activity: suggested solution and feedback

A complete solution includes both stages and explains their different purposes. The before checkpoint runs. Stage A changes only the presentation boundary and retains the original expected results. Stage B states its new policy, preserves the original overload and checks the new cases. The learner can explain the invalid subtype using a valid client call sequence.

A useful review follows the operation in order: validate identifiers and date; count all records for the borrower; apply the selected policy; create the period; check same-item overlap; store exactly one record; format the accepted record. Ask whether a structural edit changed that order or duplicated any rule.

The review should specifically inspect category trust. A demo may explicitly supply `STAFF`, but a real user selecting a dropdown would not establish authority. The correct chapter-level response is an honest scope note and a future identity-boundary question, not inventing an authentication subsystem for this exercise.

Suggested evidence table:

| Evidence | What to record |
|---|---|
| Starting point | Actual revision/checkpoint and passing original gate |
| Stage A | Relevant diff; original checks with unchanged expectations; observed result |
| Stage B | New rule table; policy contract; compatibility and staff-boundary results |
| LSP example | Valid base call sequence; subtype outcome; precise violated promise |
| Review | Actual reviewer or clearly labelled self-review; findings and corrections |
| Design rationale | Reason for each boundary; alternatives considered; remaining selector coupling |
| Hosted CI, if used | Actual tested revision and run result, not merely the presence of YAML |

Do not invent a peer review to complete this table. A supplied model rationale is not evidence that someone else inspected a student's work. A local passing run is also not proof that the hosted workflow executed.

Give feedback on whether the chosen boundary isolates the stated change, whether the contract is useful, and whether the evidence supports compatibility. Do not grade by number of interfaces, methods or commits. Apply the module leader's approved formative and assessment arrangements.

### 10.1 Optional numeric-configuration experiment

An alternative could use one concrete type with immutable maximum-active and maximum-days configuration. Its constructor must reject invalid configuration rather than let a negative maximum silently define an unusable policy. Its operation should still return false for invalid request inputs, as required by the shared policy contract. Constructor validation and request-input behaviour are different contracts.

Compare these outcomes:

| Future change | Separate policy classes | Configured numeric limits |
|---|---|---|
| Change staff days from 14 to another positive limit | Edit staff predicate | Edit staff configuration |
| Add a third pair of simple limits | Add another policy or share implementation | Supply another configuration |
| Introduce a qualitatively different eligibility rule | New implementation may express it directly | May need a broader design beyond two numbers |
| Trace the current rule in review | Read the concrete predicate | Read implementation plus selected configuration |

No approach wins merely by having fewer files. A short report should say which anticipated changes matter and how the alternative handles them. Keep the alternative in a separate experiment so the cumulative checkpoint remains unambiguous.

## 11. Transfer challenge: one possible answer

The coursework feedback tool has at least three pressures: the allowed score input domain, the policy that maps a valid score to a grade, and how the result is presented. Formatting can change independently of the grading decision. Extracting the existing message without changing its text is a structural step; adding a new grading policy is a feature.

For a small original teaching example, define `GradePolicy.grade(int score)` to accept scores 0 through 100 and return either `PASS` or `REVIEW`; other scores raise `IllegalArgumentException`. The policy is deterministic, performs no I/O and changes no stored records. These are invented exercise rules, not institutional assessment policy.

| Score | Illustrative policy A: pass at 50 | Illustrative policy B: pass at 60 |
|---|---|---|
| 49 | REVIEW | REVIEW |
| 50 | PASS | REVIEW |
| 59 | PASS | REVIEW |
| 60 | PASS | PASS |
| 100 | PASS | PASS |
| -1 or 101 | IllegalArgumentException | IllegalArgumentException |

The shared interface permits documented threshold variation. A client must not assume that every policy passes 50. The formatter receives the score and computed grade, or a coherent result object, without recomputing the grade. Selection stays explicit in the application entry point or a small selector; a factory framework is unnecessary for the exercise.

A subtype counterexample would implement the broad score contract but throw for a valid score of zero because it treats zero as “not submitted”. A base client entitled to grade zero would break. Another would return null even though the contract promises one of the two grade values. Both require contract-based reasoning, not only signature inspection.

Repair the first by preserving zero as a valid score and representing submission status separately if that requirement is real. Alternatively, expose a different operation with a narrower documented input domain, and do not advertise it as a substitute for the original policy. Repair the second by providing the promised grade or explicitly redesigning the result contract with its callers.

Protect the existing policy and message with unchanged examples during extraction. For the feature, add boundary examples around both thresholds and check invalid scores. Review that the formatter does not grade again and that the selected policy matches the intended exercise mode. As in the equipment example, finite checks support the design but do not prove every larger workflow correct.

## 12. Teaching notes

### 12.1 Do the new checks detect faults?

Fourteen deliberate faults were introduced one at a time into a copy of the `after` checkpoint, and the full gate was run on each.

| Fault | Result |
|---|---|
| Staff count limit `< 5` changed to `<= 5` | Caught: `staff sixth rejected` |
| Staff duration `<= 14` changed to `< 14` | Caught: `staff upper accepted boundaries` |
| Staff duration `<= 14` changed to `<= 15` | Caught: `staff fifteen days rejected` |
| Staff negative-count guard removed | Caught: `negative count returns false` |
| Student count limit `< 3` changed to `< 5` | Caught: `fourth rejected` |
| Student duration `<= 7` changed to `<= 14` | Caught: `eight-day duration rejected` |
| Selector arms swapped (`STUDENT` uses the staff policy) | Caught: `fourth rejected` |
| Old four-argument overload delegates with `STAFF` | Caught: `fourth rejected` |
| Confirmation text changed to `Reserved:` | Caught: `exact first confirmation` |
| Confirmation drops the end date | Caught: `exact first confirmation` |
| Storing the reservation skipped | Caught: `one success stored` |
| Count restricted to staff requests only | Caught: `fourth rejected` |
| Overlap check ignores the item | Caught: `different item and seven-day limit allowed` |
| Explicit `Objects.requireNonNull(category, ...)` removed | **Not caught**, and not a gap: `switch (category)` on `null` still throws `NullPointerException` before any state changes, so the documented behaviour is identical. Only the order against identifier validation differs, which the contract does not specify |

Thirteen of fourteen faults were caught. The survivor is a useful teaching point for Chapter 7: a surviving fault can mean the fault is behaviourally equivalent under the documented contract, not that the checks are weak. Adding a check for the order of validation would pin down something the contract deliberately leaves open.

The plain Java check runners throw `AssertionError` explicitly; they do not depend on Java's optional `assert` activation flag. The application gate propagates a runner failure through its nonzero status. Its last line is reached only after all three application check programs pass.

### 12.2 Reuse of the Chapter 4 workflow

When the `after` checkpoint becomes the root of a team's normal application repository, retain the Chapter 4 `.github/workflows/java-check.yml`. It still runs `bash scripts/check.sh`; the updated script now includes `Chapter05Checks`. No pipeline rewrite is needed for this application change.

If the team stores all three teaching directories in one repository instead, its workflow must explicitly invoke the intended checkpoint's script, such as `bash after/scripts/check.sh`. Do not assume that a root-level command will find a script inside a subdirectory. Keep hosted results tied to the actual tested path and revision.

The isolated LSP example is intentionally outside the application gate. It can be run as a teaching demonstration with the commands in Section 6. The fact that it contains a deliberately invalid subtype is clearly documented rather than hidden among application classes.

### 12.3 Teaching emphasis

Ask students to explain a change using its behaviour and maintenance pressure before naming a principle. When they say “SRP”, ask what changes independently. When they say “OCP”, ask which variation is protected and which code still changes. When they say “LSP”, ask for the valid client, its promised result and the subtype's conflicting outcome.

Do not require a perfect final architecture in this chapter. The remaining selector and direct construction are visible discussion points for Chapter 6. Students should understand why the intermediate design improves one concern while retaining another, rather than believe that the word SOLID means the design is finished.

The staff policy is an illustrative progression toward the later MVP work. It does not implement the complete reservation-and-loan flow, an authoritative borrower directory, or the later assessed requirement change. Keep the project backlog and milestone claims aligned with the actual code.

For stronger students, discuss whether internal instrumentation that leaves all public results unchanged violates a behavioural specification. The answer depends on the promises made. This chapter explicitly prohibits changing a counter in the policy; a different contract could permit invisible instrumentation. Distinguish that design choice from a universal claim about subtyping.

## References

Checked 12 October 2026. The source listings, limits, history example and model answers are original teaching examples.

1. Martin, R. C. (2014), [The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html).
2. Martin, R. C. (2014), [The Open Closed Principle](https://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html).
3. Oracle, [Java Language Specification, Java SE 17, Chapter 9: Interfaces](https://docs.oracle.com/javase/specs/jls/se17/html/jls-9.html).
4. Liskov, B. H. and Wing, J. M. (1994), [A Behavioral Notion of Subtyping](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf), *ACM Transactions on Programming Languages and Systems*, 16(6), 1811–1841. DOI: 10.1145/197320.197383.
5. Fowler, M. (2004), [Definition of Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html).