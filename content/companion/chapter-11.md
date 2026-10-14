---
title: "Chapter 11 Companion: Code, Explanations and Solutions"
weight: 110
description: "Code explanations and solutions for Chapter 11 Companion: Code, Explanations and Solutions."
---

*Refactoring and Legacy Code*  
*OO Development and Agile Practices*

## 1. Scope and execution

This file accompanies Chapter 11, Refactoring and Legacy Code. It contains the legacy overdue report, every stage of its refactoring, a probe that checks the enabling edit, the characterisation and differential tests, a separate functional change, an optional bridge that feeds the report from the live loans, two model records (a decision record and a suspected-defect register), the build files that changed, model solutions and teaching notes.

**Input version.** The starting point is the Chapter 10 companion: its 64 listings, its tests and the assertions carried forward from Chapters 3–9 (its Section 2.5). To keep those older, verified listings from being copied a second time, this file lists **only the files that are new or changed**. Every other file is exactly as in the Chapter 10 companion. The sections below say which is which.

The chapter adds one isolated package, `legacy`. Production code under `edu.se506.lending` does not use it, and the dependency test now checks that. Only bootstrap launches it or feeds it rows. No lending behaviour changes.

### 1.1 Reconstruct the version

1. Create the directory `after` and save every listing of the Chapter 10 companion at its path.
2. Save every listing in Sections 3–5 of this file at its path. Where a path already exists (`pom.xml`, `README.md`, `DependencyRulesTest.java`, `PackageMetrics.java`), the listing here **replaces** it.
3. Save the stage listings in Section 6 under `after/stages/` and the probe listings in Section 6.7 under `after/probe/`. They are not compiled by Maven.

Use a **full Java 17 JDK**, including the `jdk.jdeps` module, and Maven 3.9.11. The pinned versions are unchanged (JUnit Jupiter 5.13.4, Mockito 5.20.0, Compiler Plugin 3.14.1, Surefire 3.5.4); the Maven project version becomes 0.11.0. Initial builds need dependency access. Then, from inside `after`:

```bash
mvn --batch-mode verify
java -cp target/classes edu.se506.lending.bootstrap.Chapter11Demo
```

### 1.2 Expected output

```text
OVERDUE REPORT 2026-10-20
CAM1 B1 10 day(s) late, fine 4.00
MIC1 B2 8 day(s) late, fine 0.75
LAP1 B4 2 day(s) late, fine 0.00
3 overdue, total fines 4.75
```

`Chapter10Demo` and the other earlier demonstrations print what they printed before.

### 1.3 Run one stage of the refactoring

Each file in Section 6 is the whole `OverdueReport.java` at one step. To run a stage, copy it over `src/main/java/legacy/OverdueReport.java` and run only the report's tests:

```bash
cp stages/stage2/OverdueReport.java src/main/java/legacy/OverdueReport.java
mvn --batch-mode -Dtest='OverdueReport*Test' test
```

Stages 1 to 4 each pass the same 28 invocations. Stage 0 is the code as found and cannot be tested without a change: it reads the system clock, so the tests cannot give it a fixed date. `FinePolicy.java` can stay in place for every stage; it is first used by stage 3. Stage C is different: it replaces three files (Section 6.6).

### 1.4 Run the probe

The probe checks the one untested edit. It needs only the compiler, and it is run once, with stage 1 (or the final report) in `src/main/java/legacy`:

```bash
mkdir -p probe/out
javac --release 17 -d probe/out src/main/java/legacy/*.java probe/OriginalUnseamed.java probe/OriginalReportProbe.java
java -cp probe/out legacy.OriginalReportProbe
```

Expected: `Original and seamed reports agree on 5 rows and on an empty list.` It uses today's date, so it refuses to run if midnight passes during the run; rerun it if that happens. It examines five rows and an empty list: it is evidence about the enabling edit, not a proof for every input.

## 2. Design map

### 2.1 What is new or changed

| Path | Status | Purpose |
|---|---|---|
| `src/main/java/legacy/LoanRow.java` | New | The old system's export format, unchanged by the refactoring |
| `src/main/java/legacy/FinePolicy.java` | New | Extracted class: free days, daily rate, cap |
| `src/main/java/legacy/OverdueReport.java` | New | The refactored report (stage 4) |
| `src/main/java/edu/se506/lending/bootstrap/Chapter11Demo.java` | New | Prints the report for a fixed date |
| `src/main/java/edu/se506/lending/bootstrap/OverdueRowSource.java` | New (optional bridge) | One complete snapshot of report rows; failure must propagate |
| `src/main/java/edu/se506/lending/bootstrap/OverdueReportService.java` | New (optional bridge) | Reads one date from a `Clock` and one snapshot per report |
| `src/main/java/edu/se506/lending/bootstrap/LoanSnapshotRows.java` | New (optional bridge) | Joins loan and reservation snapshots into report rows |
| `src/test/java/legacy/OverdueReportCharacterisationTest.java` | New | Records what the report does today |
| `src/test/java/legacy/OriginalOverdueReport.java` | New | Test-only oracle: the original code plus the date parameter |
| `src/test/java/legacy/OverdueReportDifferentialTest.java` | New | Compares the report with the oracle on generated inputs |
| `src/test/java/edu/se506/lending/bootstrap/OverdueBridgeTest.java` | New (optional bridge) | Clock zone, one snapshot per report, failure, and the join |
| `src/test/java/edu/se506/lending/structure/DependencyRulesTest.java` | Changed | Production code must not refer to `legacy.` |
| `tools/PackageMetrics.java` | Changed | Counts `legacy` as one of the project's own packages |
| `pom.xml`, `README.md` | Changed | Version 0.11.0; description of the version |
| `stages/…` | New | The report at each step, and the separate functional change |
| `probe/…` | New | Runs the original beside the seamed report |
| `docs/ADR-011-legacy-overdue-report.md`, `docs/SUSPECTED-DEFECTS-legacy-overdue-report.md` | New | Model decision record and suspected-defect register |

### 2.2 The pinned behaviour, classified

Every expectation in the characterisation suite was run on the original code first, read, and classified before it was recorded. This table is the review the chapter asks for. The last column is the question to put to the records office; none of these is answered by the code. The register in `docs/SUSPECTED-DEFECTS-legacy-overdue-report.md` carries the four numbered items.

| Pinned behaviour | Class | Register | Question for the owner |
|---|---|---|---|
| A loan within the grace period is listed with fine 0.00 and counted as overdue | Surprising | SD-11-2 | Should a loan within grace appear in the report at all? |
| Student fines start on day 3, grow by 0.50 a day and stop at 10.00 | Expected | | None |
| Staff fines start on day 6, grow by 0.25 a day and stop at 5.00 | Expected | | None |
| Any other kind (`X`, lower-case `s`, blank) pays 1.00 a day, with no grace and no cap | **Suspected defect** | SD-11-1 | Do other kinds exist? If not, should they be rejected? |
| A loan due today, due later, or returned is not listed | Expected | | None |
| A null kind throws `NullPointerException`, but only for a loan that is overdue and unreturned | Unknown | SD-11-3 | Can the export contain a null kind? |
| Amounts use the default locale: `0,50` under `Locale.GERMANY`, `0.50` otherwise | Surprising | SD-11-4 | Should the separator follow the machine or the office? |
| The report uses whichever date the caller passes, so the zone is the caller's choice | Known design consequence of the seam | | None |
| `build(rows)` uses the system date; `print(rows)` writes to standard output | Known hidden dependencies | | None; isolated by the seam and the test setups |

### 2.3 Why the refactorings preserve behaviour

**Stage 1 (the seam).** `build(rows)` now returns `build(rows, LocalDate.now())`, and the new two-argument method contains the old body without the line `LocalDate today = LocalDate.now();`. One expression moved from a statement to an argument. The only observable difference is that a test can now choose the date. The probe in Section 6.7 runs the original beside the seamed version on five rows and an empty list and compares their text, so this claim is also checked by running the code as found.

**Stage 2 (Extract Method).** `fineFor(kind, late)` holds the three branches exactly as they were, and `money(amount)` holds the `String.format` call. The code moved without being rewritten, so the argument is a reading of the moved text.

**Stage 3 (Extract Class and Move Method).** The branches become three `FinePolicy` values. The equivalence is a short algebraic argument, checked by the tests:

| Old code | `FinePolicy.fineFor(daysLate)` with the same numbers |
|---|---|
| `if (late > 2)` not taken: fine stays 0 | `daysLate <= graceDays` returns 0 |
| `fine = (late - 2) * 0.50; if (fine > 10) fine = 10;` | `Math.min((daysLate - graceDays) * ratePerDay, cap)` |
| Staff: the same with 5, 0.25 and 5 | The same with those values |
| Other kinds: `fine = 1.00 * late` | Grace 0, rate 1.00, cap `Double.MAX_VALUE`: `Math.min(late * 1.00, MAX_VALUE)` |

The comparison `fine > 10` followed by an assignment gives the same number as `Math.min(fine, 10)` for every value, including exactly 10. Likewise the grace comparison could be written `<` or `<=` without changing any output, because at exactly the grace day the fine is `(grace - grace) * rate = 0`; the mutant that makes that change survives for this reason (Section 12).

**Stage 4 (rename and tidy).** Renames do not change behaviour. `String +=` and `StringBuilder.append` give the same text, including `null` printed as the text `null` for a missing item or borrower. The for-each loop replaces an index loop over the same list, and a null list or a null element still throws `NullPointerException`. The policy is looked up only for a loan that is unreturned and overdue, as before.

### 2.4 Carry-forward changes to Chapter 10 files

`DependencyRulesTest` adds `legacy.` to the packages that production code may not refer to (it already forbade `patterns.`, `behaviour.` and `examples.`). `tools/PackageMetrics.java` adds `legacy.` to the packages it counts. The report appears in the metrics output with three classes and Ce = 0, so I = 0.00. Its Ca is 4: the demonstration and the three bridge classes of Section 7.6 refer to it, all in bootstrap. The assertions carried forward from Chapters 3–9 are untouched; see Section 2.5 of the Chapter 10 companion.

## 3. New and changed production listings

### 3.1 `after/src/main/java/legacy/LoanRow.java`

```java
package legacy;

import java.time.LocalDate;

/**
 * One row exported by the old records system. Public mutable fields are the
 * old system's format and other programs read them, so this class stays as it is.
 */
public class LoanRow {
    public String item;
    public String borrower;
    /** "S" for a student, "T" for a staff member, as in the old directory. */
    public String kind;
    public LocalDate due;
    public boolean returned;

    public LoanRow(String item, String borrower, String kind, LocalDate due, boolean returned) {
        this.item = item;
        this.borrower = borrower;
        this.kind = kind;
        this.due = due;
        this.returned = returned;
    }
}
```

### 3.2 `after/src/main/java/legacy/FinePolicy.java`

```java
package legacy;

/** How a fine grows: free days, a daily rate, and the most one loan can cost. */
record FinePolicy(int graceDays, double ratePerDay, double cap) {

    double fineFor(long daysLate) {
        if (daysLate <= graceDays) {
            return 0;
        }
        return Math.min((daysLate - graceDays) * ratePerDay, cap);
    }
}
```

### 3.3 `after/src/main/java/legacy/OverdueReport.java`

```java
package legacy;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

/** Lists the unreturned loans that are past their due date, with the fine for each. */
public class OverdueReport {
    private static final FinePolicy STUDENT = new FinePolicy(2, 0.50, 10.00);
    private static final FinePolicy STAFF = new FinePolicy(5, 0.25, 5.00);
    /**
     * Suspected defect, preserved on purpose: any other kind pays 1.00 a day with no grace and no cap.
     * Change it only in a separate, agreed functional change (see the chapter, Section 11.7).
     */
    private static final FinePolicy ANY_OTHER_KIND = new FinePolicy(0, 1.00, Double.MAX_VALUE);

    public static String build(List<LoanRow> rows) {
        return build(rows, LocalDate.now());
    }

    public static String build(List<LoanRow> rows, LocalDate today) {
        StringBuilder report = new StringBuilder("OVERDUE REPORT " + today + "\n");
        double totalFines = 0;
        int overdueCount = 0;
        for (LoanRow row : rows) {
            if (row.returned) {
                continue;
            }
            long daysLate = ChronoUnit.DAYS.between(row.due, today);
            if (daysLate > 0) {
                double fine = policyFor(row.kind).fineFor(daysLate);
                report.append(row.item).append(' ').append(row.borrower).append(' ')
                        .append(daysLate).append(" day(s) late, fine ").append(money(fine)).append('\n');
                totalFines += fine;
                overdueCount++;
            }
        }
        report.append(overdueCount).append(" overdue, total fines ").append(money(totalFines)).append('\n');
        return report.toString();
    }

    public static void print(List<LoanRow> rows) {
        System.out.print(build(rows));
    }

    private static FinePolicy policyFor(String kind) {
        if (kind.equals("S")) {
            return STUDENT;
        }
        if (kind.equals("T")) {
            return STAFF;
        }
        return ANY_OTHER_KIND;
    }

    private static String money(double amount) {
        return String.format("%.2f", amount);
    }
}
```

### 3.4 `after/src/main/java/edu/se506/lending/bootstrap/Chapter11Demo.java`

```java
package edu.se506.lending.bootstrap;

import java.time.LocalDate;
import java.util.List;
import legacy.LoanRow;
import legacy.OverdueReport;

/** Prints the legacy overdue report for a fixed date. The legacy package stays outside the lending layers. */
public final class Chapter11Demo {
    public static void main(String[] args) {
        LocalDate today = LocalDate.of(2026, 10, 20);
        List<LoanRow> rows = List.of(
                new LoanRow("CAM1", "B1", "S", today.minusDays(10), false),
                new LoanRow("MIC1", "B2", "T", today.minusDays(8), false),
                new LoanRow("TRI1", "B3", "S", today.minusDays(1), true),
                new LoanRow("LAP1", "B4", "S", today.minusDays(2), false));
        System.out.print(OverdueReport.build(rows, today));
    }
}
```

### 3.5 `after/src/main/java/edu/se506/lending/bootstrap/OverdueRowSource.java`

```java
package edu.se506.lending.bootstrap;

import java.util.List;
import legacy.LoanRow;

/** One complete, non-null snapshot of rows for the legacy report. A failure must propagate. */
@FunctionalInterface
public interface OverdueRowSource {
    List<LoanRow> rows();
}
```

### 3.6 `after/src/main/java/edu/se506/lending/bootstrap/OverdueReportService.java`

```java
package edu.se506.lending.bootstrap;

import java.time.Clock;
import java.time.LocalDate;
import java.util.List;
import java.util.Objects;
import legacy.LoanRow;
import legacy.OverdueReport;

/**
 * Runs the legacy report against the live lending data. It reads one date and one snapshot per
 * call and changes nothing in the lending state. It lives in bootstrap, the only code that may
 * know both the lending layers and the isolated legacy package.
 */
public final class OverdueReportService {
    private final OverdueRowSource source;
    private final Clock clock;

    public OverdueReportService(OverdueRowSource source, Clock clock) {
        this.source = Objects.requireNonNull(source, "source");
        this.clock = Objects.requireNonNull(clock, "clock");
    }

    public String report() {
        LocalDate today = LocalDate.now(clock);
        List<LoanRow> rows = Objects.requireNonNull(source.rows(), "rows");
        return OverdueReport.build(rows, today);
    }
}
```

### 3.7 `after/src/main/java/edu/se506/lending/bootstrap/LoanSnapshotRows.java`

```java
package edu.se506.lending.bootstrap;

import edu.se506.lending.domain.Loan;
import edu.se506.lending.domain.Reservation;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;
import java.util.function.Supplier;
import legacy.LoanRow;

/**
 * Feeds the legacy report from the lending snapshots. A reservation covers a half-open period, so
 * the last permitted day is the day before its exclusive end. Reads two snapshots one after the
 * other (sequential use only, not an atomic read).
 */
public final class LoanSnapshotRows implements OverdueRowSource {
    private final Supplier<List<Loan>> loans;
    private final Supplier<List<Reservation>> reservations;
    private final Function<String, String> kindOf;

    public LoanSnapshotRows(Supplier<List<Loan>> loans, Supplier<List<Reservation>> reservations,
                            Function<String, String> kindOf) {
        this.loans = Objects.requireNonNull(loans, "loans");
        this.reservations = Objects.requireNonNull(reservations, "reservations");
        this.kindOf = Objects.requireNonNull(kindOf, "kindOf");
    }

    @Override public List<LoanRow> rows() {
        List<Loan> loanSnapshot = List.copyOf(loans.get());
        List<Reservation> reservationSnapshot = List.copyOf(reservations.get());
        List<LoanRow> rows = new ArrayList<>();
        for (Loan loan : loanSnapshot) {
            Reservation reservation = reservationSnapshot.stream()
                    .filter(r -> r.id().equals(loan.reservationId())).findFirst()
                    .orElseThrow(() -> new IllegalStateException(
                            "Missing reservation for loan: " + loan.reservationId()));
            if (!reservation.borrowerId().equals(loan.borrowerId())
                    || !reservation.itemId().equals(loan.itemId())) {
                throw new IllegalStateException("Mismatched loan: " + loan.reservationId());
            }
            String kind = kindOf.apply(loan.borrowerId());
            if (kind == null) {
                throw new IllegalStateException("No kind for borrower: " + loan.borrowerId());
            }
            rows.add(new LoanRow(loan.itemId(), loan.borrowerId(), kind,
                    reservation.period().endExclusive().minusDays(1), !loan.active()));
        }
        return List.copyOf(rows);
    }
}
```

These three files are the optional bridge of Section 7.6. They live in bootstrap because that is the only code allowed to know both the lending layers and the isolated `legacy` package.

### 3.8 `after/tools/PackageMetrics.java`

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
                || type.startsWith("behaviour.") || type.startsWith("examples.")
                || type.startsWith("legacy.");
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

## 4. New and changed test listings

### 4.1 `after/src/test/java/legacy/OverdueReportCharacterisationTest.java`

```java
package legacy;

import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Locale;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

/**
 * Characterisation tests: they record what the report does today, including behaviour
 * that looks wrong. A passing test here means "unchanged", not "correct".
 */
class OverdueReportCharacterisationTest {
    private static final LocalDate TODAY = LocalDate.of(2026, 10, 20);
    private static final String HEADER = "OVERDUE REPORT 2026-10-20\n";

    private Locale savedLocale;

    @BeforeEach void pinTheLocale() {
        savedLocale = Locale.getDefault();
        Locale.setDefault(Locale.ROOT);
    }

    @AfterEach void restoreTheLocale() {
        Locale.setDefault(savedLocale);
    }

    private static LoanRow open(String kind, int daysLate) {
        return new LoanRow("CAM1", "B1", kind, TODAY.minusDays(daysLate), false);
    }

    private static String oneLoan(int daysLate, String fine) {
        return HEADER + "CAM1 B1 " + daysLate + " day(s) late, fine " + fine + "\n"
                + "1 overdue, total fines " + fine + "\n";
    }

    // Observed fines for students (2 days of grace, 0.50 a day, capped at 10.00)
    // and staff (5 days of grace, 0.25 a day, capped at 5.00).
    @ParameterizedTest
    @CsvSource({
            "S,1,0.00", "S,2,0.00", "S,3,0.50", "S,10,4.00", "S,22,10.00", "S,23,10.00", "S,100,10.00",
            "T,1,0.00", "T,5,0.00", "T,6,0.25", "T,25,5.00", "T,26,5.00", "T,100,5.00"})
    void finesForStudentsAndStaff(String kind, int daysLate, String fine) {
        assertEquals(oneLoan(daysLate, fine), OverdueReport.build(List.of(open(kind, daysLate)), TODAY));
    }

    // SUSPECTED DEFECT, pinned on purpose: any other kind pays 1.00 a day with no grace and no cap.
    @ParameterizedTest
    @CsvSource({"X,1,1.00", "X,100,100.00", "s,3,3.00"})
    void otherKindsPayTheFullRateWithNoGraceOrCap(String kind, int daysLate, String fine) {
        assertEquals(oneLoan(daysLate, fine), OverdueReport.build(List.of(open(kind, daysLate)), TODAY));
    }

    @Test void aBlankKindIsTreatedLikeAnyOtherKind() {
        assertEquals(oneLoan(2, "2.00"), OverdueReport.build(List.of(open("", 2)), TODAY));
    }

    @Test void loansWithinGraceAreStillListedAndCounted() {
        String report = OverdueReport.build(List.of(open("S", 1), open("T", 4)), TODAY);
        assertEquals(HEADER + "CAM1 B1 1 day(s) late, fine 0.00\n" + "CAM1 B1 4 day(s) late, fine 0.00\n"
                + "2 overdue, total fines 0.00\n", report);
    }

    @Test void loansDueTodayDueLaterOrReturnedAreNotListed() {
        List<LoanRow> rows = List.of(
                open("S", 0),
                new LoanRow("CAM1", "B1", "S", TODAY.plusDays(3), false),
                new LoanRow("CAM1", "B1", "S", TODAY.minusDays(30), true));
        assertEquals(HEADER + "0 overdue, total fines 0.00\n", OverdueReport.build(rows, TODAY));
    }

    @Test void aNullKindOnALoanThatIsReturnedOrNotYetDueIsIgnored() {
        List<LoanRow> rows = List.of(
                new LoanRow("CAM1", "B1", null, TODAY.minusDays(30), true),
                new LoanRow("CAM1", "B1", null, TODAY, false));
        assertEquals(HEADER + "0 overdue, total fines 0.00\n", OverdueReport.build(rows, TODAY));
    }

    @Test void anEmptyListGivesTheHeaderAndAZeroTotal() {
        assertEquals(HEADER + "0 overdue, total fines 0.00\n", OverdueReport.build(List.of(), TODAY));
    }

    @Test void rowsAreListedInInputOrderAndTheTotalAddsTheFines() {
        List<LoanRow> rows = List.of(
                new LoanRow("CAM1", "B1", "S", TODAY.minusDays(10), false),
                new LoanRow("MIC1", "B2", "T", TODAY.minusDays(8), false),
                new LoanRow("TRI1", "B3", "S", TODAY.minusDays(1), true),
                new LoanRow("LAP1", "B4", "S", TODAY.minusDays(2), false));
        assertEquals(HEADER
                + "CAM1 B1 10 day(s) late, fine 4.00\n"
                + "MIC1 B2 8 day(s) late, fine 0.75\n"
                + "LAP1 B4 2 day(s) late, fine 0.00\n"
                + "3 overdue, total fines 4.75\n", OverdueReport.build(rows, TODAY));
    }

    // Hidden dependency: the amounts are formatted in the JVM's default locale.
    // Whether a comma is wanted is a business question; today the report follows the locale.
    @Test void amountsFollowTheDefaultLocale() {
        Locale.setDefault(Locale.GERMANY);
        assertEquals(oneLoan(3, "0,50"), OverdueReport.build(List.of(open("S", 3)), TODAY));
    }

    @Test void aNullKindOrANullListFailsWithNullPointerException() {
        assertThrows(NullPointerException.class, () -> OverdueReport.build(List.of(open(null, 3)), TODAY));
        assertThrows(NullPointerException.class, () -> OverdueReport.build(null, TODAY));
    }

    // Hidden dependency: the entry point without a date reads the system clock.
    @Test void theShortEntryPointUsesTheSystemDate() {
        LocalDate before = LocalDate.now();
        String report = OverdueReport.build(List.of());
        LocalDate after = LocalDate.now();
        assertTrue(report.equals("OVERDUE REPORT " + before + "\n0 overdue, total fines 0.00\n")
                || report.equals("OVERDUE REPORT " + after + "\n0 overdue, total fines 0.00\n"), report);
    }

    // The seam moves the zone decision to the caller: one instant is two different calendar dates.
    @Test void theCallerChoosesTheZoneByChoosingTheDate() {
        Instant instant = Instant.parse("2026-10-21T22:30:00Z");
        LocalDate utcDate = LocalDate.now(Clock.fixed(instant, ZoneOffset.UTC));
        LocalDate baghdadDate = LocalDate.now(Clock.fixed(instant, ZoneId.of("Asia/Baghdad")));
        List<LoanRow> rows = List.of(new LoanRow("CAM1", "B1", "S", LocalDate.of(2026, 10, 21), false));
        assertEquals("OVERDUE REPORT 2026-10-21\n0 overdue, total fines 0.00\n", OverdueReport.build(rows, utcDate));
        assertEquals("OVERDUE REPORT 2026-10-22\nCAM1 B1 1 day(s) late, fine 0.00\n1 overdue, total fines 0.00\n",
                OverdueReport.build(rows, baghdadDate));
    }

    // Hidden dependency: print writes to System.out, which is global state.
    @Test void printWritesTheReportToStandardOutput() {
        PrintStream saved = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
        try {
            OverdueReport.print(List.of());
        } finally {
            System.setOut(saved);
        }
        String text = captured.toString(StandardCharsets.UTF_8);
        assertTrue(text.startsWith("OVERDUE REPORT ") && text.endsWith("0 overdue, total fines 0.00\n"), text);
    }
}
```

The example `pinTheLocale` and `restoreTheLocale` is part of the test design: the default locale is process-wide state, so the suite sets it before every test and restores it after. The suite therefore cannot safely run in parallel with other tests that format numbers.

### 4.2 `after/src/test/java/legacy/OriginalOverdueReport.java`

```java
package legacy;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

/**
 * Test-only oracle: the legacy report exactly as it was when the characterisation tests were written
 * (stage 1: the original plus the date parameter). Never edit this file; it is the reference answer.
 */
final class OriginalOverdueReport {

    public static String build(List<LoanRow> rows) {
        return build(rows, LocalDate.now());
    }

    public static String build(List<LoanRow> rows, LocalDate today) {
        String out = "";
        double total = 0;
        int count = 0;
        out += "OVERDUE REPORT " + today + "\n";
        for (int i = 0; i < rows.size(); i++) {
            LoanRow r = rows.get(i);
            if (r.returned) {
                continue;
            }
            long late = ChronoUnit.DAYS.between(r.due, today);
            if (late > 0) {
                double fine = 0;
                if (r.kind.equals("S")) {
                    if (late > 2) {
                        fine = (late - 2) * 0.50;
                        if (fine > 10) {
                            fine = 10;
                        }
                    }
                } else if (r.kind.equals("T")) {
                    if (late > 5) {
                        fine = (late - 5) * 0.25;
                        if (fine > 5) {
                            fine = 5;
                        }
                    }
                } else {
                    fine = 1.00 * late;
                }
                out += r.item + " " + r.borrower + " " + late + " day(s) late, fine "
                        + String.format("%.2f", fine) + "\n";
                total += fine;
                count++;
            }
        }
        out += count + " overdue, total fines " + String.format("%.2f", total) + "\n";
        return out;
    }

    public static void print(List<LoanRow> rows) {
        System.out.print(build(rows));
    }
}
```

This is the original code with the date parameter added (stage 1). It lives in the test tree, is package-private, and is the oracle for the differential test. It must never be edited.

### 4.3 `after/src/test/java/legacy/OverdueReportDifferentialTest.java`

```java
package legacy;

import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import org.junit.jupiter.api.Test;

/**
 * A second safety net: the current report must give the same text as the original code for
 * thousands of generated inputs. It is stronger than a handful of examples, but it can only
 * compare behaviour for the kinds of input the generator produces.
 */
class OverdueReportDifferentialTest {
    private static final LocalDate TODAY = LocalDate.of(2026, 10, 20);
    private static final String[] KINDS = {"S", "T", "X", "s", ""};

    @Test void currentReportMatchesTheOriginalOnGeneratedInputs() {
        Locale saved = Locale.getDefault();
        Locale.setDefault(Locale.ROOT);
        try {
            Random random = new Random(11);
            for (int run = 0; run < 3000; run++) {
                List<LoanRow> rows = new ArrayList<>();
                int size = random.nextInt(7);
                for (int i = 0; i < size; i++) {
                    String kind = KINDS[random.nextInt(KINDS.length)];
                    LocalDate due = TODAY.minusDays(random.nextInt(70) - 5);
                    rows.add(new LoanRow("I" + random.nextInt(9), "B" + random.nextInt(9), kind, due, random.nextInt(5) == 0));
                }
                assertEquals(OriginalOverdueReport.build(rows, TODAY), OverdueReport.build(rows, TODAY),
                        "run " + run + " with " + size + " rows");
            }
        } finally {
            Locale.setDefault(saved);
        }
    }
}
```

The generator uses a fixed seed so that a failure is repeatable. It produces lists of 0 to 6 rows with five kinds (`S`, `T`, `X`, `s`, blank), due dates from five days in the future to sixty-four days in the past, and about one row in five returned. It does not produce nulls, empty-string items, or very large lists; the characterisation tests cover the nulls.

### 4.4 `after/src/test/java/edu/se506/lending/structure/DependencyRulesTest.java`

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
            if (to.startsWith("patterns.") || to.startsWith("behaviour.") || to.startsWith("examples.")
                    || to.startsWith("legacy.")) {
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

### 4.5 `after/src/test/java/edu/se506/lending/bootstrap/OverdueBridgeTest.java`

```java
package edu.se506.lending.bootstrap;

import static org.junit.jupiter.api.Assertions.*;

import edu.se506.lending.application.LoanService;
import edu.se506.lending.application.ReservationCoordinator;
import edu.se506.lending.domain.Loan;
import edu.se506.lending.domain.LoanPeriod;
import edu.se506.lending.domain.Reservation;
import edu.se506.lending.infrastructure.notification.RecordingNotificationSender;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import legacy.LoanRow;

/** Tests the optional bridge that feeds the legacy report from the live lending data. */
class OverdueBridgeTest {
    private static final Clock UTC_EVENING = Clock.fixed(Instant.parse("2026-10-21T22:30:00Z"), ZoneOffset.UTC);
    private static final LoanRow DUE_ON_THE_21ST =
            new LoanRow("CAM1", "B1", "S", LocalDate.of(2026, 10, 21), false);

    private Locale savedLocale;

    @BeforeEach void pinTheLocale() {
        savedLocale = Locale.getDefault();
        Locale.setDefault(Locale.ROOT);
    }

    @AfterEach void restoreTheLocale() {
        Locale.setDefault(savedLocale);
    }

    @Test void theClockZoneDecidesWhichDateTheReportUses() {
        var utc = new OverdueReportService(() -> List.of(DUE_ON_THE_21ST), UTC_EVENING);
        var baghdad = new OverdueReportService(() -> List.of(DUE_ON_THE_21ST),
                UTC_EVENING.withZone(ZoneId.of("Asia/Baghdad")));
        assertEquals("OVERDUE REPORT 2026-10-21\n0 overdue, total fines 0.00\n", utc.report());
        assertEquals("OVERDUE REPORT 2026-10-22\nCAM1 B1 1 day(s) late, fine 0.00\n"
                + "1 overdue, total fines 0.00\n", baghdad.report());
    }

    @Test void eachReportReadsOneFreshSnapshot() {
        AtomicInteger reads = new AtomicInteger();
        OverdueRowSource source = () -> reads.incrementAndGet() == 1 ? List.of(DUE_ON_THE_21ST) : List.of();
        var service = new OverdueReportService(source, UTC_EVENING.withZone(ZoneId.of("Asia/Baghdad")));
        assertTrue(service.report().contains("1 overdue"));
        assertEquals(1, reads.get());
        assertTrue(service.report().contains("0 overdue"));
        assertEquals(2, reads.get());
    }

    @Test void aSourceFailureIsNotAnEmptySuccessfulReport() {
        IllegalStateException failure = new IllegalStateException("Snapshot unavailable");
        var service = new OverdueReportService(() -> { throw failure; }, UTC_EVENING);
        assertSame(failure, assertThrows(IllegalStateException.class, service::report));
    }

    @Test void aNullSnapshotIsNotTreatedAsEmpty() {
        var service = new OverdueReportService(() -> null, UTC_EVENING);
        assertThrows(NullPointerException.class, service::report);
    }

    @Test void dependenciesMustBeSupplied() {
        assertThrows(NullPointerException.class, () -> new OverdueReportService(null, UTC_EVENING));
        assertThrows(NullPointerException.class, () -> new OverdueReportService(List::of, null));
        assertThrows(NullPointerException.class, () -> new LoanSnapshotRows(null, List::of, id -> "S"));
        assertThrows(NullPointerException.class, () -> new LoanSnapshotRows(List::of, null, id -> "S"));
        assertThrows(NullPointerException.class, () -> new LoanSnapshotRows(List::of, List::of, null));
    }

    @Test void theLastPermittedDayIsTheDayBeforeTheExclusiveEnd() {
        var start = LocalDate.of(2026, 10, 20);
        var reservation = new Reservation("R1", "B1", "CAM1", new LoanPeriod(start, start.plusDays(2)));
        var active = new Loan("R1", "B1", "CAM1", start, null);
        var returned = new Loan("R1", "B1", "CAM1", start, start.plusDays(1));
        var openRow = new LoanSnapshotRows(() -> List.of(active), () -> List.of(reservation), id -> "S").rows().get(0);
        var closedRow = new LoanSnapshotRows(() -> List.of(returned), () -> List.of(reservation), id -> "S").rows().get(0);
        assertEquals(LocalDate.of(2026, 10, 21), openRow.due);
        assertFalse(openRow.returned);
        assertTrue(closedRow.returned);
        assertEquals("CAM1", openRow.item);
        assertEquals("B1", openRow.borrower);
        assertEquals("S", openRow.kind);
    }

    @Test void aLoanWithoutAMatchingReservationIsAnError() {
        var start = LocalDate.of(2026, 10, 20);
        var loan = new Loan("R9", "B1", "CAM1", start, null);
        var rows = new LoanSnapshotRows(() -> List.of(loan), List::of, id -> "S");
        assertThrows(IllegalStateException.class, rows::rows);
    }

    @Test void aLoanThatDisagreesWithItsReservationIsAnError() {
        var start = LocalDate.of(2026, 10, 20);
        var reservation = new Reservation("R1", "B1", "CAM1", new LoanPeriod(start, start.plusDays(2)));
        var otherBorrower = new Loan("R1", "B2", "CAM1", start, null);
        var otherItem = new Loan("R1", "B1", "MIC1", start, null);
        assertThrows(IllegalStateException.class,
                () -> new LoanSnapshotRows(() -> List.of(otherBorrower), () -> List.of(reservation), id -> "S").rows());
        assertThrows(IllegalStateException.class,
                () -> new LoanSnapshotRows(() -> List.of(otherItem), () -> List.of(reservation), id -> "S").rows());
    }

    @Test void aBorrowerWithoutAKindIsAnErrorNotARowWithANullKind() {
        var start = LocalDate.of(2026, 10, 20);
        var reservation = new Reservation("R1", "B1", "CAM1", new LoanPeriod(start, start.plusDays(2)));
        var loan = new Loan("R1", "B1", "CAM1", start, null);
        var rows = new LoanSnapshotRows(() -> List.of(loan), () -> List.of(reservation), id -> null);
        assertThrows(IllegalStateException.class, rows::rows);
    }

    @Test void theReportFollowsARealCheckoutAndReturn() {
        Clock checkoutDay = Clock.fixed(Instant.parse("2026-10-20T09:00:00Z"), ZoneOffset.UTC);
        Clock reportDay = Clock.fixed(Instant.parse("2026-10-24T09:00:00Z"), ZoneOffset.UTC);
        ReservationCoordinator coordinator = ReservationApplication.create(new RecordingNotificationSender());
        LoanService loans = new LoanService(coordinator, checkoutDay);
        assertTrue(coordinator.reserve("B1", "CAM1", LocalDate.of(2026, 10, 20), 2).startsWith("Confirmed: R1"));
        loans.checkOut("R1");
        var rows = new LoanSnapshotRows(loans::loans, coordinator::reservations, id -> "S");
        var service = new OverdueReportService(rows, reportDay);
        assertEquals("OVERDUE REPORT 2026-10-24\nCAM1 B1 3 day(s) late, fine 0.50\n"
                + "1 overdue, total fines 0.50\n", service.report());
        loans.returnLoan("R1");
        assertEquals("OVERDUE REPORT 2026-10-24\n0 overdue, total fines 0.00\n", service.report());
        assertEquals(1, coordinator.reservations().size());
    }
}
```

## 5. Build and documentation

### 5.1 `after/pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>edu.se506</groupId>
  <artifactId>equipment-lending</artifactId>
  <version>0.11.0</version>
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

### 5.2 `after/README.md`

````markdown
# Chapter 11 checkpoint

Use a full Java 17 JDK and Maven 3.9.11. The JDK must include jdk.jdeps for the compiled dependency tests. Existing dependency and plugin versions are unchanged.

From this directory:

```bash
mvn --batch-mode verify
java -cp target/classes edu.se506.lending.bootstrap.Chapter11Demo
java -cp target/classes edu.se506.lending.bootstrap.Chapter10Demo
```

The full build executes 159 JUnit invocations: 121 inherited from Chapter 10 (107 migrated, seven repository, two value-semantics, three console and two compiled dependency tests), 28 for the legacy overdue report (27 characterisation invocations and one differential test) and 10 for the optional bridge to the live loans. Four inherited cases bridge older plain-Java runners.

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

### 5.3 `after/docs/ADR-011-legacy-overdue-report.md`

```markdown
# ADR-011: Pin, isolate and refactor the legacy overdue report

Date: 13 October 2026
Status: Implemented teaching example; peer review pending.

## Context

The old records system's overdue report is one long static method. It reads the system clock and formats amounts in the default locale. It has three near-identical fine branches and no tests. The records office wants the staff grace period changed, and nobody can say what the report does today.

The report must keep producing the same text for the inputs it accepts. Other programs read its input format (`LoanRow`) and call `build` and `print`.

## Decision

Add a date parameter to `build` as the only edit made before tests exist, and keep the old signature as a wrapper. Pin the current behaviour with characterisation tests, including behaviour that looks wrong, and add a differential test against a frozen copy of the original. Refactor in small steps (Extract Method, Extract Class, Rename) with the tests run after each. Keep the `legacy` package isolated from the lending layers; only bootstrap may launch it.

Do not fix suspected defects during the refactoring. Record them in the suspected-defect register and ask the owner. Apply any agreed correction as a separate functional change with replaced tests.

## Alternatives considered

- Leave the report alone: cheapest now, but the requested change would be an untested edit in several places.
- Rewrite it from the specification: there is no specification, and a rewrite would silently change behaviour that other programs rely on.
- Inject a `Clock` into a new non-static class first: a better final design, but an untested rewrite as a first step.

## Consequences

The report gains a seam, a pinned suite and a small policy class. Locale and standard output remain hidden dependencies handled by test fixtures, not by code. The three suspected defects remain until the owner decides.

## Validation and review

Run the full Maven verification and the stage commands in the chapter companion. No hosted CI run or independent peer review is claimed.

## Revisit triggers

A decision on any suspected defect; a requirement to change fines; a requirement to run the report concurrently or against a persistent source; or a decision to move the report into the application layer.
```

### 5.4 `after/docs/SUSPECTED-DEFECTS-legacy-overdue-report.md`

```markdown
# Suspected defects: legacy overdue report

Status date: 13 October 2026. Every entry is pinned by a characterisation test and has **not** been fixed. Only the owner of the requirement can change an entry's status.

| ID | Behaviour today | Status | Evidence | Question for the owner |
|---|---|---|---|---|
| SD-11-1 | A borrower kind other than `S` or `T` (including lower-case `s` and a blank) pays 1.00 a day, with no grace and no cap | Suspected defect | `otherKindsPayTheFullRateWithNoGraceOrCap`, `aBlankKindIsTreatedLikeAnyOtherKind` | Do other kinds exist? If not, should they be rejected? |
| SD-11-2 | A loan inside its grace period is listed with fine 0.00 and counted as overdue | Surprising, clarification pending | `loansWithinGraceAreStillListedAndCounted` | Should a loan inside its grace period appear in the report? |
| SD-11-3 | A null kind throws `NullPointerException`, but only for a loan that is unreturned and past its due date | Unknown | `aNullKindOrANullListFailsWithNullPointerException`, `aNullKindOnALoanThatIsReturnedOrNotYetDueIsIgnored` | Can the export contain a null kind? |
| SD-11-4 | Amounts follow the default locale (`0,50` under `Locale.GERMANY`) | Surprising, clarification pending | `amountsFollowTheDefaultLocale` | Should the separator follow the machine or the office? |

Accepted behaviour (confirmed as intended) is recorded here when the owner confirms it. None has been confirmed yet.
```

These two records are models of the form. A real project's records describe its own code, and only the owner of a requirement can change the status of an entry.

## 6. Stage listings

These files are not part of the Maven build. They show the report at each step. Stage 3 uses `FinePolicy` from Section 3.2, and stage 4 is the file in Section 3.3.

### 6.1 `after/stages/stage0/OverdueReport.java`

The code as found.

```java
package legacy;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

/** Overdue report as found in the old records system. Deliberately untidy; do not copy its style. */
public class OverdueReport {

    public static String build(List<LoanRow> rows) {
        String out = "";
        double total = 0;
        int count = 0;
        LocalDate today = LocalDate.now();
        out += "OVERDUE REPORT " + today + "\n";
        for (int i = 0; i < rows.size(); i++) {
            LoanRow r = rows.get(i);
            if (r.returned) {
                continue;
            }
            long late = ChronoUnit.DAYS.between(r.due, today);
            if (late > 0) {
                double fine = 0;
                if (r.kind.equals("S")) {
                    if (late > 2) {
                        fine = (late - 2) * 0.50;
                        if (fine > 10) {
                            fine = 10;
                        }
                    }
                } else if (r.kind.equals("T")) {
                    if (late > 5) {
                        fine = (late - 5) * 0.25;
                        if (fine > 5) {
                            fine = 5;
                        }
                    }
                } else {
                    fine = 1.00 * late;
                }
                out += r.item + " " + r.borrower + " " + late + " day(s) late, fine "
                        + String.format("%.2f", fine) + "\n";
                total += fine;
                count++;
            }
        }
        out += count + " overdue, total fines " + String.format("%.2f", total) + "\n";
        return out;
    }

    public static void print(List<LoanRow> rows) {
        System.out.print(build(rows));
    }
}
```

### 6.2 `after/stages/stage1/OverdueReport.java`

The seam: the only edit made before there were tests.

```java
package legacy;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

/** Overdue report as found in the old records system. Deliberately untidy; do not copy its style. */
public class OverdueReport {

    public static String build(List<LoanRow> rows) {
        return build(rows, LocalDate.now());
    }

    public static String build(List<LoanRow> rows, LocalDate today) {
        String out = "";
        double total = 0;
        int count = 0;
        out += "OVERDUE REPORT " + today + "\n";
        for (int i = 0; i < rows.size(); i++) {
            LoanRow r = rows.get(i);
            if (r.returned) {
                continue;
            }
            long late = ChronoUnit.DAYS.between(r.due, today);
            if (late > 0) {
                double fine = 0;
                if (r.kind.equals("S")) {
                    if (late > 2) {
                        fine = (late - 2) * 0.50;
                        if (fine > 10) {
                            fine = 10;
                        }
                    }
                } else if (r.kind.equals("T")) {
                    if (late > 5) {
                        fine = (late - 5) * 0.25;
                        if (fine > 5) {
                            fine = 5;
                        }
                    }
                } else {
                    fine = 1.00 * late;
                }
                out += r.item + " " + r.borrower + " " + late + " day(s) late, fine "
                        + String.format("%.2f", fine) + "\n";
                total += fine;
                count++;
            }
        }
        out += count + " overdue, total fines " + String.format("%.2f", total) + "\n";
        return out;
    }

    public static void print(List<LoanRow> rows) {
        System.out.print(build(rows));
    }
}
```

### 6.3 `after/stages/stage2/OverdueReport.java`

Extract Method: `fineFor` and `money`.

```java
package legacy;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

/** Overdue report as found in the old records system. Deliberately untidy; do not copy its style. */
public class OverdueReport {

    public static String build(List<LoanRow> rows) {
        return build(rows, LocalDate.now());
    }

    public static String build(List<LoanRow> rows, LocalDate today) {
        String out = "";
        double total = 0;
        int count = 0;
        out += "OVERDUE REPORT " + today + "\n";
        for (int i = 0; i < rows.size(); i++) {
            LoanRow r = rows.get(i);
            if (r.returned) {
                continue;
            }
            long late = ChronoUnit.DAYS.between(r.due, today);
            if (late > 0) {
                double fine = fineFor(r.kind, late);
                out += r.item + " " + r.borrower + " " + late + " day(s) late, fine "
                        + money(fine) + "\n";
                total += fine;
                count++;
            }
        }
        out += count + " overdue, total fines " + money(total) + "\n";
        return out;
    }

    public static void print(List<LoanRow> rows) {
        System.out.print(build(rows));
    }

    private static double fineFor(String kind, long late) {
        double fine = 0;
        if (kind.equals("S")) {
            if (late > 2) {
                fine = (late - 2) * 0.50;
                if (fine > 10) {
                    fine = 10;
                }
            }
        } else if (kind.equals("T")) {
            if (late > 5) {
                fine = (late - 5) * 0.25;
                if (fine > 5) {
                    fine = 5;
                }
            }
        } else {
            fine = 1.00 * late;
        }
        return fine;
    }

    private static String money(double amount) {
        return String.format("%.2f", amount);
    }
}
```

### 6.4 `after/stages/stage3/OverdueReport.java`

Extract Class and Move Method: `FinePolicy`.

```java
package legacy;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

/** Overdue report as found in the old records system. Deliberately untidy; do not copy its style. */
public class OverdueReport {
    private static final FinePolicy STUDENT = new FinePolicy(2, 0.50, 10.00);
    private static final FinePolicy STAFF = new FinePolicy(5, 0.25, 5.00);
    /** Suspected defect, preserved on purpose: any other kind pays 1.00 a day with no grace and no cap. */
    private static final FinePolicy ANY_OTHER_KIND = new FinePolicy(0, 1.00, Double.MAX_VALUE);

    public static String build(List<LoanRow> rows) {
        return build(rows, LocalDate.now());
    }

    public static String build(List<LoanRow> rows, LocalDate today) {
        String out = "";
        double total = 0;
        int count = 0;
        out += "OVERDUE REPORT " + today + "\n";
        for (int i = 0; i < rows.size(); i++) {
            LoanRow r = rows.get(i);
            if (r.returned) {
                continue;
            }
            long late = ChronoUnit.DAYS.between(r.due, today);
            if (late > 0) {
                double fine = policyFor(r.kind).fineFor(late);
                out += r.item + " " + r.borrower + " " + late + " day(s) late, fine "
                        + money(fine) + "\n";
                total += fine;
                count++;
            }
        }
        out += count + " overdue, total fines " + money(total) + "\n";
        return out;
    }

    public static void print(List<LoanRow> rows) {
        System.out.print(build(rows));
    }

    private static FinePolicy policyFor(String kind) {
        if (kind.equals("S")) {
            return STUDENT;
        }
        if (kind.equals("T")) {
            return STAFF;
        }
        return ANY_OTHER_KIND;
    }

    private static String money(double amount) {
        return String.format("%.2f", amount);
    }
}
```

### 6.5 Stage 4

Stage 4 is the file in Section 3.3: names, for-each loop and `StringBuilder`.

### 6.6 Stage C: the separate functional change

Stage C is **not** a refactoring. It applies the correction of Section 11.6 of the chapter: an unknown kind is rejected. It replaces three files, and the tests that pinned the suspected defect are replaced on purpose. Treat the rule as illustrative: in a real project the records office decides it.

#### 6.6.1 `after/stages/stageC/OverdueReport.java`

```java
package legacy;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

/** Lists the unreturned loans that are past their due date, with the fine for each. */
public class OverdueReport {
    private static final FinePolicy STUDENT = new FinePolicy(2, 0.50, 10.00);
    private static final FinePolicy STAFF = new FinePolicy(5, 0.25, 5.00);

    public static String build(List<LoanRow> rows) {
        return build(rows, LocalDate.now());
    }

    public static String build(List<LoanRow> rows, LocalDate today) {
        StringBuilder report = new StringBuilder("OVERDUE REPORT " + today + "\n");
        double totalFines = 0;
        int overdueCount = 0;
        for (LoanRow row : rows) {
            if (row.returned) {
                continue;
            }
            long daysLate = ChronoUnit.DAYS.between(row.due, today);
            if (daysLate > 0) {
                double fine = policyFor(row.kind).fineFor(daysLate);
                report.append(row.item).append(' ').append(row.borrower).append(' ')
                        .append(daysLate).append(" day(s) late, fine ").append(money(fine)).append('\n');
                totalFines += fine;
                overdueCount++;
            }
        }
        report.append(overdueCount).append(" overdue, total fines ").append(money(totalFines)).append('\n');
        return report.toString();
    }

    public static void print(List<LoanRow> rows) {
        System.out.print(build(rows));
    }

    private static FinePolicy policyFor(String kind) {
        if (kind.equals("S")) {
            return STUDENT;
        }
        if (kind.equals("T")) {
            return STAFF;
        }
        throw new IllegalArgumentException("Unknown borrower kind: " + kind);
    }

    private static String money(double amount) {
        return String.format("%.2f", amount);
    }
}
```

#### 6.6.2 `after/stages/stageC/OverdueReportCharacterisationTest.java`

Only the part that differs from Section 4.1 is described here: the three parameterised rows for unknown kinds and the blank-kind test are replaced by `unknownKindsAreRejected`, and one test (`anUnknownKindOnAReturnedLoanIsStillIgnored`) records that a returned loan never reaches the fine rules. The full file is below.

```java
package legacy;

import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Locale;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

/**
 * Characterisation tests: they record what the report does today, including behaviour
 * that looks wrong. A passing test here means "unchanged", not "correct".
 */
class OverdueReportCharacterisationTest {
    private static final LocalDate TODAY = LocalDate.of(2026, 10, 20);
    private static final String HEADER = "OVERDUE REPORT 2026-10-20\n";

    private Locale savedLocale;

    @BeforeEach void pinTheLocale() {
        savedLocale = Locale.getDefault();
        Locale.setDefault(Locale.ROOT);
    }

    @AfterEach void restoreTheLocale() {
        Locale.setDefault(savedLocale);
    }

    private static LoanRow open(String kind, int daysLate) {
        return new LoanRow("CAM1", "B1", kind, TODAY.minusDays(daysLate), false);
    }

    private static String oneLoan(int daysLate, String fine) {
        return HEADER + "CAM1 B1 " + daysLate + " day(s) late, fine " + fine + "\n"
                + "1 overdue, total fines " + fine + "\n";
    }

    // Observed fines for students (2 days of grace, 0.50 a day, capped at 10.00)
    // and staff (5 days of grace, 0.25 a day, capped at 5.00).
    @ParameterizedTest
    @CsvSource({
            "S,1,0.00", "S,2,0.00", "S,3,0.50", "S,10,4.00", "S,22,10.00", "S,23,10.00", "S,100,10.00",
            "T,1,0.00", "T,5,0.00", "T,6,0.25", "T,25,5.00", "T,26,5.00", "T,100,5.00"})
    void finesForStudentsAndStaff(String kind, int daysLate, String fine) {
        assertEquals(oneLoan(daysLate, fine), OverdueReport.build(List.of(open(kind, daysLate)), TODAY));
    }

    // CHANGED ON PURPOSE (functional change C): an unknown kind used to pay 1.00 a day with no
    // grace and no cap. The records office confirmed that only "S" and "T" exist, so it is now rejected.
    @ParameterizedTest
    @ValueSource(strings = {"X", "s", ""})
    void unknownKindsAreRejected(String kind) {
        IllegalArgumentException failure = assertThrows(IllegalArgumentException.class,
                () -> OverdueReport.build(List.of(open(kind, 3)), TODAY));
        assertEquals("Unknown borrower kind: " + kind, failure.getMessage());
    }

    // Unchanged: a loan that is returned or not yet overdue never reaches the fine rules.
    @Test void anUnknownKindOnAReturnedLoanIsStillIgnored() {
        List<LoanRow> rows = List.of(new LoanRow("CAM1", "B1", "X", TODAY.minusDays(30), true));
        assertEquals(HEADER + "0 overdue, total fines 0.00\n", OverdueReport.build(rows, TODAY));
    }

    @Test void loansWithinGraceAreStillListedAndCounted() {
        String report = OverdueReport.build(List.of(open("S", 1), open("T", 4)), TODAY);
        assertEquals(HEADER + "CAM1 B1 1 day(s) late, fine 0.00\n" + "CAM1 B1 4 day(s) late, fine 0.00\n"
                + "2 overdue, total fines 0.00\n", report);
    }

    @Test void loansDueTodayDueLaterOrReturnedAreNotListed() {
        List<LoanRow> rows = List.of(
                open("S", 0),
                new LoanRow("CAM1", "B1", "S", TODAY.plusDays(3), false),
                new LoanRow("CAM1", "B1", "S", TODAY.minusDays(30), true));
        assertEquals(HEADER + "0 overdue, total fines 0.00\n", OverdueReport.build(rows, TODAY));
    }

    @Test void aNullKindOnALoanThatIsReturnedOrNotYetDueIsIgnored() {
        List<LoanRow> rows = List.of(
                new LoanRow("CAM1", "B1", null, TODAY.minusDays(30), true),
                new LoanRow("CAM1", "B1", null, TODAY, false));
        assertEquals(HEADER + "0 overdue, total fines 0.00\n", OverdueReport.build(rows, TODAY));
    }

    @Test void anEmptyListGivesTheHeaderAndAZeroTotal() {
        assertEquals(HEADER + "0 overdue, total fines 0.00\n", OverdueReport.build(List.of(), TODAY));
    }

    @Test void rowsAreListedInInputOrderAndTheTotalAddsTheFines() {
        List<LoanRow> rows = List.of(
                new LoanRow("CAM1", "B1", "S", TODAY.minusDays(10), false),
                new LoanRow("MIC1", "B2", "T", TODAY.minusDays(8), false),
                new LoanRow("TRI1", "B3", "S", TODAY.minusDays(1), true),
                new LoanRow("LAP1", "B4", "S", TODAY.minusDays(2), false));
        assertEquals(HEADER
                + "CAM1 B1 10 day(s) late, fine 4.00\n"
                + "MIC1 B2 8 day(s) late, fine 0.75\n"
                + "LAP1 B4 2 day(s) late, fine 0.00\n"
                + "3 overdue, total fines 4.75\n", OverdueReport.build(rows, TODAY));
    }

    // Hidden dependency: the amounts are formatted in the JVM's default locale.
    // Whether a comma is wanted is a business question; today the report follows the locale.
    @Test void amountsFollowTheDefaultLocale() {
        Locale.setDefault(Locale.GERMANY);
        assertEquals(oneLoan(3, "0,50"), OverdueReport.build(List.of(open("S", 3)), TODAY));
    }

    @Test void aNullKindOrANullListFailsWithNullPointerException() {
        assertThrows(NullPointerException.class, () -> OverdueReport.build(List.of(open(null, 3)), TODAY));
        assertThrows(NullPointerException.class, () -> OverdueReport.build(null, TODAY));
    }

    // Hidden dependency: the entry point without a date reads the system clock.
    @Test void theShortEntryPointUsesTheSystemDate() {
        LocalDate before = LocalDate.now();
        String report = OverdueReport.build(List.of());
        LocalDate after = LocalDate.now();
        assertTrue(report.equals("OVERDUE REPORT " + before + "\n0 overdue, total fines 0.00\n")
                || report.equals("OVERDUE REPORT " + after + "\n0 overdue, total fines 0.00\n"), report);
    }

    // The seam moves the zone decision to the caller: one instant is two different calendar dates.
    @Test void theCallerChoosesTheZoneByChoosingTheDate() {
        Instant instant = Instant.parse("2026-10-21T22:30:00Z");
        LocalDate utcDate = LocalDate.now(Clock.fixed(instant, ZoneOffset.UTC));
        LocalDate baghdadDate = LocalDate.now(Clock.fixed(instant, ZoneId.of("Asia/Baghdad")));
        List<LoanRow> rows = List.of(new LoanRow("CAM1", "B1", "S", LocalDate.of(2026, 10, 21), false));
        assertEquals("OVERDUE REPORT 2026-10-21\n0 overdue, total fines 0.00\n", OverdueReport.build(rows, utcDate));
        assertEquals("OVERDUE REPORT 2026-10-22\nCAM1 B1 1 day(s) late, fine 0.00\n1 overdue, total fines 0.00\n",
                OverdueReport.build(rows, baghdadDate));
    }

    // Hidden dependency: print writes to System.out, which is global state.
    @Test void printWritesTheReportToStandardOutput() {
        PrintStream saved = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
        try {
            OverdueReport.print(List.of());
        } finally {
            System.setOut(saved);
        }
        String text = captured.toString(StandardCharsets.UTF_8);
        assertTrue(text.startsWith("OVERDUE REPORT ") && text.endsWith("0 overdue, total fines 0.00\n"), text);
    }
}
```

#### 6.6.3 `after/stages/stageC/OverdueReportDifferentialTest.java`

The only change from Section 4.3 is `KINDS = {"S", "T"}` and the comment: the unknown kinds changed on purpose, so the oracle can no longer be the reference for them.

```java
package legacy;

import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import org.junit.jupiter.api.Test;

/**
 * A second safety net: the current report must give the same text as the original code for
 * thousands of generated inputs with a known kind (the unknown kinds changed on purpose). It is stronger than a handful of examples, but it can only
 * compare behaviour for the kinds of input the generator produces.
 */
class OverdueReportDifferentialTest {
    private static final LocalDate TODAY = LocalDate.of(2026, 10, 20);
    private static final String[] KINDS = {"S", "T"};

    @Test void currentReportMatchesTheOriginalOnGeneratedInputs() {
        Locale saved = Locale.getDefault();
        Locale.setDefault(Locale.ROOT);
        try {
            Random random = new Random(11);
            for (int run = 0; run < 3000; run++) {
                List<LoanRow> rows = new ArrayList<>();
                int size = random.nextInt(7);
                for (int i = 0; i < size; i++) {
                    String kind = KINDS[random.nextInt(KINDS.length)];
                    LocalDate due = TODAY.minusDays(random.nextInt(70) - 5);
                    rows.add(new LoanRow("I" + random.nextInt(9), "B" + random.nextInt(9), kind, due, random.nextInt(5) == 0));
                }
                assertEquals(OriginalOverdueReport.build(rows, TODAY), OverdueReport.build(rows, TODAY),
                        "run " + run + " with " + size + " rows");
            }
        } finally {
            Locale.setDefault(saved);
        }
    }
}
```

To try stage C, copy these three files over their counterparts in `src` and run the full build. It passes 159 invocations.

### 6.7 The probe

The probe is not part of the Maven build. It runs the original code beside the seamed version through their public entry points.

#### 6.7.1 `after/probe/OriginalUnseamed.java`

The code as found (stage 0), with only the class name changed so that both versions can be loaded together.

```java
package legacy;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;

/** The report exactly as found (stage 0), with only the class name changed so that it can be run beside the seamed version. */
public final class OriginalUnseamed {

    public static String build(List<LoanRow> rows) {
        String out = "";
        double total = 0;
        int count = 0;
        LocalDate today = LocalDate.now();
        out += "OVERDUE REPORT " + today + "\n";
        for (int i = 0; i < rows.size(); i++) {
            LoanRow r = rows.get(i);
            if (r.returned) {
                continue;
            }
            long late = ChronoUnit.DAYS.between(r.due, today);
            if (late > 0) {
                double fine = 0;
                if (r.kind.equals("S")) {
                    if (late > 2) {
                        fine = (late - 2) * 0.50;
                        if (fine > 10) {
                            fine = 10;
                        }
                    }
                } else if (r.kind.equals("T")) {
                    if (late > 5) {
                        fine = (late - 5) * 0.25;
                        if (fine > 5) {
                            fine = 5;
                        }
                    }
                } else {
                    fine = 1.00 * late;
                }
                out += r.item + " " + r.borrower + " " + late + " day(s) late, fine "
                        + String.format("%.2f", fine) + "\n";
                total += fine;
                count++;
            }
        }
        out += count + " overdue, total fines " + String.format("%.2f", total) + "\n";
        return out;
    }

    public static void print(List<LoanRow> rows) {
        System.out.print(build(rows));
    }
}
```

#### 6.7.2 `after/probe/OriginalReportProbe.java`

```java
package legacy;

import java.time.LocalDate;
import java.util.List;
import java.util.Locale;

/**
 * Compares the original, unseamed report with the seamed one through their public entry points.
 * It examines a bounded set of rows and rejects a run that crosses midnight. It is evidence about
 * the enabling edit, not a proof for arbitrary inputs.
 */
public final class OriginalReportProbe {
    public static void main(String[] args) {
        Locale.setDefault(Locale.ROOT);
        LocalDate before = LocalDate.now();
        List<LoanRow> rows = List.of(
                new LoanRow("CAM1", "B1", "S", before.minusDays(10), false),
                new LoanRow("MIC1", "B2", "T", before.minusDays(8), false),
                new LoanRow("TRI1", "B3", "S", before, false),
                new LoanRow("LAP1", "B4", "X", before.minusDays(1), false),
                new LoanRow("PRJ1", "B5", "S", before.minusDays(40), true));
        String original = OriginalUnseamed.build(rows);
        String seamed = OverdueReport.build(rows);
        String empty = OriginalUnseamed.build(List.of());
        String emptySeamed = OverdueReport.build(List.of());
        if (!LocalDate.now().equals(before)) {
            throw new IllegalStateException("The date changed during the probe; run it again.");
        }
        if (!original.equals(seamed) || !empty.equals(emptySeamed)) {
            throw new AssertionError("The seamed report differs from the original:\n" + original + "---\n" + seamed);
        }
        String expectedFirstLine = "OVERDUE REPORT " + before + "\n";
        if (!original.startsWith(expectedFirstLine) || !original.contains("CAM1 B1 10 day(s) late, fine 4.00\n")
                || !original.contains("LAP1 B4 1 day(s) late, fine 1.00\n") || original.contains("TRI1")
                || original.contains("PRJ1") || !original.endsWith("3 overdue, total fines 5.75\n")) {
            throw new AssertionError("Unexpected original output:\n" + original);
        }
        System.out.println("Original and seamed reports agree on " + rows.size() + " rows and on an empty list.");
    }
}
```

## 7. Worked explanation and evidence

### 7.1 The seam, and why it comes first

Without the date parameter nothing can be pinned, because the output changes every day. The edit has three properties that make it safe to make *before* there are tests. It is **mechanical**: one expression moves into an argument, and one line is deleted. It is **checked by the compiler**: if anything else had changed, the code would not compile. And it is **visible to a reviewer**: the diff is a few lines and can be read in a minute. A larger seam, such as an injected `Clock` and a non-static class, would be better design, but it would be an untested edit of a method that nobody understands, which is exactly the risk the chapter is about.

The probe of Section 6.7 adds a direct check. It compares the code as found with the seamed version on five rows (a late student, a late staff member, a row due today, an unknown kind and a returned loan) and on an empty list, and it checks one literal result. It examines a bounded set, and it is not a proof, but it is the only check that runs the original. The test `theShortEntryPointUsesTheSystemDate` covers the delegation itself. It reads the system date before and after the call, because a test that runs across midnight could otherwise fail by chance, and accepts either.

### 7.2 Pinning, in the order it was done

1. Run the stage 1 code on a small table of inputs (the table of observed results in Section 11.3 of the chapter) and read every result.
2. Classify each result (Section 2.2) and write the test with a comment for each surprising or suspected case.
3. Add the cases that test boundaries (grace and cap on both sides), kinds that are not `S` or `T`, the rows that must be ignored, ordering and totals, the locale, nulls, and the two entry points.
4. Add the differential test as a second net.

The suite then passed on stage 1, which is the point: every expectation describes behaviour the original code really has.

### 7.3 What the two nets cover

The characterisation tests cover the inputs someone thought of, with exact expected text. The differential test covers 3,000 generated lists, each compared with the oracle. A mistake in a rate or a cap is found by both. A change in how an item name prints is found by the characterisation tests only when an example has that item; the differential test finds it for every generated item. A change that only affects an input the generator cannot produce, such as a null item, is found by neither unless a specific example covers it. This is why the chapter says that the suite shows selected behaviour, not equivalence.

### 7.4 The commit sequence

| # | Message | Files | Check run |
|---|---|---|---|
| 1 | `Add a date parameter to OverdueReport.build (seam)` | `OverdueReport.java` | Compiles; the probe agrees with the original |
| 2 | `Add characterisation and differential tests for OverdueReport` | Three test files | All pass on commit 1 |
| 3 | `Extract fineFor and money from OverdueReport.build` | `OverdueReport.java` | 28 invocations pass |
| 4 | `Extract FinePolicy; keep the unknown-kind policy visible` | `OverdueReport.java`, `FinePolicy.java` | 28 invocations pass |
| 5 | `Rename variables and use StringBuilder in OverdueReport` | `OverdueReport.java` | 28 invocations pass |
| 6 | `Reject unknown borrower kinds (functional change)` | Stage C files | 159 invocations pass; tests changed on purpose |

The first five commits are behaviour-preserving. The sixth is a different kind of commit and is reviewed as one: its message says what behaviour changed and why, and its test diff shows the old expectations being replaced.

### 7.5 A change request after the refactoring

The staff grace period becomes seven days: `new FinePolicy(7, 0.25, 5.00)`. Running the suite fails five of the 28 report invocations, exactly the ones that describe the staff rule: the rows `T,6` (0.25 becomes 0.00), `T,25` (5.00 becomes 4.50) and `T,26` (5.00 becomes 4.75), the mixed-list test (the staff loan's fine drops from 0.75 to 0.25), and the differential test. The rows for 1 and 5 days, the 100-day cap and every student row still pass. Those failures are the expected evidence of the intended change, and the next step is to update the expectations in the same commit as the rule. The change is small *because* the structure was fixed first; it would have been two coordinated edits in one branch of the original method.

### 7.6 The optional bridge to the live loans

The report was written for the old records system, and it knows nothing about the lending application. The bridge lets the lending application feed it rows, without letting the old code reach into the new.

- **`LoanSnapshotRows`** turns the loan and reservation snapshots into `LoanRow`s. A loan does not carry its due date, so the row's due date comes from its reservation: the *last permitted day* is the day before the exclusive end of the reserved period. A reservation for `[20 October, 22 October)` is due back on 21 October, and the report counts a loan late from 22 October. Taking the exclusive end itself would shift every loan's lateness by a day. A loan with no matching reservation, a loan that disagrees with its reservation, and a borrower with no kind are each an error, not a row.
- **`OverdueReportService`** reads one date from the supplied `Clock` and one snapshot per call, and passes both to the report. Because the clock carries a zone, the same instant can give different dates (the test uses 22:30 UTC, which is already 22 October in Baghdad). A source failure propagates: it is never reported as “0 overdue”, which would tell the officer that there is nothing to chase.
- **Where it lives.** Both classes are in bootstrap, because only bootstrap may know the lending layers and the isolated `legacy` package. A real system would move the report into the application layer, which is the natural next refactoring, and would give it a `BorrowerDirectory`-style port for the kind instead of the function `kindOf`.
- **Limits.** The two snapshots are read one after the other, so the read is not atomic; the application is sequential and in memory. The mapping from a borrower to a kind (`"S"` or `"T"`) is supplied by the caller, and the tests use a stub.

## 8. Suggested practical solution

### 8.1 the book's project, steps B1–B3

**B1. Probe and three further characterisation tests.** A good answer runs the probe first and reports its single line of output, then adds three inputs that the suite does not cover, each with a recorded actual result and a classification. Examples with answers on stage 1:

| Input | Observed | Class |
|---|---|---|
| Two rows for the same item, both overdue | Two lines, listed in input order, fines added | Expected |
| A student exactly 22 days late, then 23 | 10.00 for both; the cap is reached at 22 | Expected (a boundary worth pinning) |
| A row with a blank item name | A line that starts with a space | Surprising: ask whether blank names can occur |

**B2. Two refactoring commits.** A good answer shows stage 2 and stage 3 as two separate commits, the suite run after each, and no edit to the expectations. If a step failed, it shows the rollback and the retry. The result should be recognisable as stage 3 even if the names differ.

**B3. Rationale and register entry.** A good rationale says what changed structurally (the grace number and the rates now appear once each, in a named policy), what was checked after each step, what was deliberately *not* changed (the odd third policy, the locale-dependent formatting, `LoanRow`, the public signatures), and which questions remain (Section 2.2). The register entry names evidence, cost and decision as in Section 11.7 of the chapter.

### 8.1a the book's project, optional steps B4–B7

**B4. Break the boundary on purpose.** Changing `daysLate > 0` to `daysLate >= 0` includes a loan due today, with 0 days late. The tests that fail are `loansDueTodayDueLaterOrReturnedAreNotListed`, the differential test and the bridge test that follows a real checkout; the failing messages show an extra line and a count that is one higher. Restore the original and rerun. A good answer predicts the failures before running them.

**B5. A separate functional change.** See Section 6.6 and the commit in Section 7.4. The commit message should say that unknown kinds are now rejected, that the three pinned expectations were replaced on purpose, and that the differential test is restricted to known kinds.

**B6. AI activity.** See Section 9.

**B7. Connect the report to the live loans.** See Section 7.6. A good answer traces `[20 October, 22 October)` to a due date of 21 October, explains why `source.rows()` is not wrapped in a `try` that returns an empty list, and adds a test (for example a loan whose borrower kind is `"T"`, checked at the staff grace boundary).

### 8.2 your team's project, steps T1–T4

These are not model answers, because the code is your team's. A good answer shows:

- **T1:** a reading note with three columns (observation, how you know, status). It names at least one thing that was known only by running the code.
- **T2:** at least six characterisation tests, including a boundary and an odd case; each result classified; the seam edit, if any, small, described and compared with the original on a few inputs; global state restored.
- **T3:** at least three commits, each one refactoring, tests run before each; no behaviour change among them; a rollback if a step failed.
- **T4:** a rationale that separates structure from behaviour, lists suspected defects and questions found but not fixed, and a reviewer's feedback with the response.

A weak answer lists smells without a change that they block, pins only the happy path, or fixes a suspected defect inside a refactoring commit.

## 9. AI activity solution

The example makes four statements: the new overdue test is equivalent to `daysLate > 0`; the policy can be chosen before the check; unknown kinds can fall back to the student policy; and behaviour is preserved because formatting is unchanged. The first three are claims about behaviour, and each was applied **to its own copy** of the final code and run against the suite, then all three together.

| Claim | Finding | Evidence (report and bridge tests that fail) |
|---|---|---|
| “`!row.due.isAfter(today)` is equivalent to `daysLate > 0`” | **False on the due date.** For a row due today, `daysLate` is 0, so the original skips it, and `isAfter` is false, so the patch includes it | 5 invocations: `loansDueTodayDueLaterOrReturnedAreNotListed`, `theCallerChoosesTheZoneByChoosingTheDate`, `aNullKindOnALoanThatIsReturnedOrNotYetDueIsIgnored` (a null-kind row due today is now included, so it throws), the differential test, and the bridge test `theClockZoneDecidesWhichDateTheReportUses` |
| “Choose the policy before the check” | **A second behaviour change, easy to miss.** A row that is not yet due, or due today, now has its kind inspected, so a null kind throws `NullPointerException` where it used to be ignored | 1 invocation: `aNullKindOnALoanThatIsReturnedOrNotYetDueIsIgnored`. It is the only test that notices, and it was added after the first fault experiment found that nothing did |
| “Unknown kinds fall back to the student policy” | **A functional change presented as a tidy-up.** `X`, `s` and blank paid 1.00 a day; they now follow the student rules. The suspected defect is changed without a decision | 5 invocations: the three rows of `otherKindsPayTheFullRateWithNoGraceOrCap`, `aBlankKindIsTreatedLikeAnyOtherKind` and the differential test |
| “Formatting is unchanged, so behaviour is preserved” | The premise is true and the conclusion is false: formatting is not the only behaviour | 9 of the 38 report and bridge invocations fail: the union of the three sets above (the differential test appears in two of them, and the null-kind test in two) |

What to do with the patch: **reject it as a refactoring.** The first two claims can be repaired, keeping the neater structure while restoring the original overdue test and the original lookup inside it. The third needs a decision from the records office (entries SD-11-1 in the register), and its own commit with replaced tests (stage C does it one way).

Notice the difference between *tracing* and *running*. The equality case can be settled by tracing the due date before any test runs. The null-kind change is not visible from the patch text at all unless you ask what each line now does for a row that is not overdue, and the suite finds it only because a test was added after the first fault experiment (Section 12). Applying the claims one at a time is what lets each failing test point at one claim.

If a live assistant is used, keep its actual output, apply any patch to a scratch copy, and record which tests fail. Do not use a generated test to approve a generated change.

## 10. Intentionally flawed alternatives

These fragments are **diagnostic alternatives**, not files to compile. Each corresponds to a fault that was run in the experiment in Section 12 or to a mistake in Section 11.9 of the chapter.

### 10.1 Fix the defect while refactoring

```java
// WRONG for a refactoring commit: this changes behaviour for unknown kinds.
private static FinePolicy policyFor(String kind) {
    if (kind.equals("S")) return STUDENT;
    if (kind.equals("T")) return STAFF;
    throw new IllegalArgumentException("Unknown borrower kind: " + kind);
}
```

The code may be better. The commit is no longer a refactoring: three pinned tests fail and the reviewer cannot tell which failures were intended. Do it in its own commit (stage C).

### 10.2 Blind pasting of results

```java
@Test void x() { assertEquals("", OverdueReport.build(rows, TODAY)); }  // run, then paste whatever comes out
```

A suite built this way would bless every oddity, including defects. Each recorded result must be read and classified, and the odd ones commented.

### 10.3 A seam that rewrites the method

```java
// WRONG as a first step: an untested rewrite to make the code testable.
public final class OverdueReport {
    private final Clock clock;
    public OverdueReport(Clock clock) { this.clock = clock; }
    public String build(List<LoanRow> rows) { /* reorganised body */ }
}
```

This is a better design and the wrong first move. The method changed shape, and every caller must change, while there is still no test. Add the parameter first, pin, and consider the object design afterwards.

### 10.4 Locale left set after a test

```java
@Test void amountsFollowTheDefaultLocale() {
    Locale.setDefault(Locale.GERMANY);   // never restored
    ...
}
```

Every later test in the same process now formats with a comma. The chapter's example restores the locale in `@AfterEach`.

### 10.5 A boundary rewrite taken as equivalent

```java
// WRONG as a refactoring: this includes a loan due today, which the original skipped.
if (!row.due.isAfter(today)) { ... }
```

`isAfter` and a day count differ exactly on the due date. Reading the line as “not later than today” hides the difference; tracing a row due today shows it. Section 9 runs it.

## 11. Review answers and transfer solution

### 11.1 Concept answers

**1. Characterisation versus regression.** A regression test protects behaviour that is agreed to be correct; a characterisation test records whatever the code does today. A passing characterisation test tells you the behaviour is unchanged, not that it is right.

**2. Seam.** A seam is a place where behaviour can be changed without editing the code there; here the second parameter of `build` is the enabling point. It is a better first edit than a rewrite because it is mechanical, compiler-checked and small enough to review, so it can be made safely before any test exists.

**3. Pin, not fix.** A refactoring is defined by unchanged behaviour. A fix changes behaviour, so combining them makes a failing test ambiguous and a review impossible. Pinning keeps the suspect behaviour visible and protected until the owner decides.

**4. Differential test.** It can compare thousands of generated inputs with the original code, so it finds differences nobody thought to write an example for. It cannot test inputs the generator does not produce, and it is only as good as the oracle; it shows selected equivalence, not proof.

### 11.2 Applied diagnosis answers

**5. “All tests pass, so nothing changed.”** The suite does not cover, for example, the report for dates in other time zones or at midnight (the short entry point reads the clock), items or borrowers that are null (a null name prints as `null`, which the differential test does not generate), or very large lists. Handle each by adding a test for the case you are about to touch, or by recording it as a known gap in the rationale.

**6. Mixed commit.** Changing the staff cap in a refactoring commit makes the commit unreviewable as “no behaviour change”. The suite would fail on the staff rows and the differential test, which would be mistaken for a refactoring error, or the developer would edit the expectations to make them pass and hide the change. Revert the cap change, refactor, and then change the cap in its own commit with its tests.

**7. The zone question.** At 22:30 UTC it is 01:30 on 22 October in Baghdad (UTC+3). A report run with a Baghdad clock uses 22 October, so the loan due on 21 October is one day late and prints with fine 0.00 (inside the grace period, but listed). A report run with a UTC clock uses 21 October and does not list it. The object that chooses the zone is the `Clock` supplied to `OverdueReportService`, through `LocalDate.now(clock)`; the report itself only receives a date.

### 11.3 ML-serving transfer

An analysis script that formats prediction scores has the same three kinds of hidden dependency: the current time (a date in the summary), the locale (number formatting) and standard output. Add a date parameter to the entry point as the seam; pin the locale in the example data; capture standard output once. Pin six or seven inputs: a score at each boundary of a model type's rule, one at the maximum, an unknown model type, an empty list, a null, and the locale case. Apply Extract Method for the formatting, Extract Class for the three near-identical branches (a small value object holding what differs), and Rename. Record as a question, not a fix, whatever an unknown model type does today.

### 11.4 Quiz 2 revision pointers

Section 11.11 of the chapter lists the revision focus for Chapters 6–10. This file adds nothing to the quiz.

## 12. Instructor notes

### 12.1 Suggested demonstration and review

Run the original report with two different dates (through the seam) to show why it cannot be tested before the seam exists. Run the probe once. Then pin one surprising result live, with its comment, and trace a row due today through `daysLate > 0` and through `!row.due.isAfter(today)` before showing the AI patch. Let students predict, before running, what an unknown kind pays, and discuss why “it looks wrong” is not yet a reason to change it.

Review the commits as a reviewer would: for each refactoring commit, ask for the test run that preceded it and look for any edit that is not a move or a rename. Ask students which of the pinned behaviours they would raise with the records office first.

Keep the legacy lab outside Quiz 2. The chapter lists the quiz scope (Weeks 5–9) and the revision pointers.

**The book's project and your team's project. The supplied report is the book's project: students extend its tests and take the first refactoring steps. your team's project is the team's own method from the provided starter codebase, which contains intentional smells. A team on another provided domain applies the same steps to its starter codebase; the transfer challenge gives an orientation for an ML-serving tool. The bridge of Section 7.6 is optional: it is useful for a team that wants to see the report fed from live data, and a second-week task for most groups.

### 12.2 Do the tests detect faults?

The experiment ran in two rounds, always one fault at a time in a copy of the project and always through `mvn test`.

*First round.* Twenty-four faults of the report itself (stage 4) were run against the suite as first written. Twenty-two were caught and two survived: an equivalent mutant (below) and a policy lookup made before the overdue check, because no test had a null kind on a loan that is returned or not yet due. The test `aNullKindOnALoanThatIsReturnedOrNotYetDueIsIgnored` was added to close that gap.

*Second round.* All 36 faults, which add twelve for the three AI claims, the bridge and the service, were run against the final suite (159 invocations). Thirty-five were caught and one survives, the equivalent mutant.

| Area | Faults tried | Result with the final suite |
|---|---|---|
| Student rules | Grace 2 to 3; rate 0.50 to 0.60; cap 10 to 9 | All three caught |
| Staff rules | Grace 5 to 4; rate 0.25 to 0.30; cap 5 to 6 | All three caught |
| Other kinds | One grace day; a cap of 10; lower-case `s` accepted as a student | All three caught |
| Policy arithmetic | `Math.max` instead of `Math.min`; grace test `<` instead of `<=` | `max` caught. The `<` change **survives**: it is an **equivalent mutant**, because at exactly the grace day the fine is `(grace - grace) * rate = 0` either way |
| Listing rules | Due today counted as overdue; returned loans not skipped; overdue count off by two; total fines not accumulated | All four caught |
| Zero-fine patches | Zero-fine loans skipped; fine computed first and zero-fine loans skipped | Both caught |
| The AI claims | The overdue test written as `!isAfter`; the policy looked up before the overdue check; unknown kinds treated as students; all three together | All four caught (Section 9 lists the failing tests) |
| Hidden dependencies | Amounts always formatted with a point; header shows the system date; print writes to standard error; short entry point uses yesterday | All four caught |
| Date arithmetic | Dates subtracted the wrong way round; days late from `Period.getDays()` | Both caught |
| Bridge | The due day is the exclusive end; the returned flag inverted; a mismatched loan not detected; a null kind passed through | All four caught |
| Service | A source failure becomes an empty report; a null snapshot treated as empty; the system date instead of the clock; the clock zone ignored; the snapshot cached between reports | All five caught |

The `Period` fault matters because it is a realistic suggestion from a code assistant: `Period.getDays()` returns the days field only, stored separately from months and years, so a loan 100 days late would not be counted as 100 days. The `ChronoUnit.DAYS.between` call in the code returns whole days, with the end exclusive. These counts come from one fault set on one small class and its bridge, and they say nothing about how this suite compares with earlier chapters.

The results establish the selected behaviours on the supplied inputs. They do not establish equivalence with the original for every input, or the behaviour of any real record system.

## References

The online references of the student chapter (sources 1–12) were opened on 13 October 2026; see the chapter for the source context.

1. Fowler, M., [Definition of Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html).
2. Fowler, M., [Refactoring catalogue](https://refactoring.com/catalog/).
3. Feathers, M., [Characterization Testing](https://michaelfeathers.silvrback.com/characterization-testing).
4. Fowler, M., [Technical Debt](https://martinfowler.com/bliki/TechnicalDebt.html).
5. Fowler, M., [Code Smell](https://martinfowler.com/bliki/CodeSmell.html); [Legacy Seam](https://martinfowler.com/bliki/LegacySeam.html). Feathers, M., [Testing Effectively With Legacy Code](https://www.informit.com/articles/article.aspx?p=359417).
6. Oracle, [Formatter (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Formatter.html); [ChronoUnit](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/temporal/ChronoUnit.html); [Period](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Period.html); [Clock](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Clock.html); [LocalDate](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/LocalDate.html).
7. JUnit, [User Guide 5.13.4](https://docs.junit.org/5.13.4/user-guide/).