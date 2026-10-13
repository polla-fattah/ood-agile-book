---
title: "Chapter 4 Companion: Code, Explanations and Solutions"
weight: 40
description: "Code explanations and solutions for Chapter 4 Companion: Code, Explanations and Solutions."
---

*From Requirements to an Iteration*  
*OO Development and Agile Practices*

## How to use this file

This file accompanies Chapter 4, From Requirements to an Iteration. It contains the complete starter listings, build instructions, a hosted-workflow template, explanations, model planning artefacts, exercise solutions and teaching notes. Read the student chapter before using the solutions.

**Checkpoint:** Java 17; Campus Equipment Lending System; unchanged Chapter 2–3 reservation rules. New material organises the starter and makes verification repeatable. **US-02 availability enquiry remains planned and is not implemented here.** No catalogue, persistence, cancellation, email or concurrent reservation protection has been added.

All people, workload figures and review scenarios in the model answers are fictional.

## 1. Reconstructing the starter

Create one directory, such as `equipment-lending`, and save each listing below at its labelled relative path. A heading gives the filename; do not copy that heading into the file. Create intermediate directories as required.

| Relative path | Purpose |
|---|---|
| `src/main/java/ReservationRules.java` | Existing borrower-count and duration rule |
| `src/main/java/LoanPeriod.java` | Existing immutable interval and overlap behaviour |
| `src/main/java/Reservation.java` | Existing immutable reservation data |
| `src/main/java/ReservationCoordinator.java` | Existing sequential, in-memory reservation operation |
| `src/main/java/Chapter04Demo.java` | Fixed three-request demonstration |
| `src/test/java/Chapter02Checks.java` | Existing 34 regression checks |
| `src/test/java/Chapter03AcceptanceExamples.java` | Existing five acceptance example groups |
| `scripts/check.sh` | Compile and execute the agreed gate |
| `.github/workflows/java-check.yml` | Hosted CI template |
| `.gitignore` | Exclude generated class output |
| `.gitattributes` | Keep shell scripts in LF form on every platform |
| `README.md` | Setup, execution and scope instructions |

Application and check classes still use the unnamed package. The directory names separate source roles without changing the class design. Named packages and broader application structure will be introduced deliberately later. This is not a Maven build: there is no `pom.xml`, and the check classes use `main` methods rather than JUnit discovery. Do not expect `mvn test` to discover them automatically. Maven and JUnit remain the planned fuller toolchain for the testing stage.

### 1.1 Requirements and commands

Use a Java 17 JDK and Bash. Check that both `java -version` and `javac -version` identify the intended installation. A runtime without a compiler is insufficient for the ordinary command. On Windows, use a Bash environment with the JDK on its path, such as Git Bash or WSL; native PowerShell cannot interpret this Bash script. Section 10 records runs on Linux and in Git Bash on Windows.

From the project root:

```bash
bash scripts/check.sh
java -cp build/classes Chapter04Demo
```

The workflow also invokes `bash scripts/check.sh`, so no executable permission bit is required for that file. Store it with ordinary UTF-8 text and LF line endings. Do not copy Markdown fence markers into the script or YAML file.

The gate prints Java version information, then these success lines:

```text
All 34 chapter checks passed.
AC-01 passed
AC-02 passed
AC-03 passed
AC-04 passed
AC-05 passed
All 5 acceptance examples passed.
BUILD AND CHECKS PASSED
```

The five acceptance groups contain multiple assertions; do not add 34 and 5 and describe the total as 39 individual assertions. They are two differently organised sets of checks.

The demonstration prints:

```text
Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Rejected: item unavailable.
Confirmed: R2 for B2 on CAM1 [2026-10-22, 2026-10-23).
Stored reservations: 2
```

The second request must not consume a reservation identifier or create a record. The third request receives R2 and starts exactly at the earlier exclusive end. All three calls run in the same coordinator; rerunning the program creates a new empty coordinator.

## 2. Complete Java listings

These listings preserve the existing baseline. Repetition makes this Markdown file independently reconstructable and prevents accidental mixing of earlier coordinator versions.

### 2.1 `src/main/java/ReservationRules.java`

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

### 2.2 `src/main/java/LoanPeriod.java`

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

### 2.3 `src/main/java/Reservation.java`

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

### 2.4 `src/main/java/ReservationCoordinator.java`

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

### 2.5 `src/main/java/Chapter04Demo.java`

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

### 2.6 `src/test/java/Chapter02Checks.java`

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

### 2.7 `src/test/java/Chapter03AcceptanceExamples.java`

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

### 2.8 What the supplied checks protect

`ReservationRules` permits a request only when the existing count is nonnegative and below three, and the requested duration is one through seven days. `LoanPeriod` rejects invalid bounds and implements half-open overlap. `ReservationCoordinator` checks eligibility and conflict before storing a record, then builds the confirmation through the private method extracted in Chapter 2.

`reservations()` returns an unmodifiable snapshot. The reservation and period objects are immutable at this checkpoint. The checks cover rejection without storage, adjacency, identifier allocation after rejection and snapshot behaviour. The acceptance examples connect those behaviours to US-01.

The helper methods throw `AssertionError` explicitly when a condition is false. They do not use Java's `assert` keyword, so they do not depend on the `-ea` flag. An uncaught failure makes the Java process return a nonzero exit status. The shell gate must preserve that failure.

The coordinator does not validate known borrowers or equipment, expire old records, cancel reservations or provide a read-only availability operation. Do not turn a passing regression suite into a claim that these features exist.

## 3. Build and repository files

### 3.1 `scripts/check.sh`

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

### 3.2 `.github/workflows/java-check.yml`

```yaml
name: Java starter checks

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: '17'
      - name: Compile and check
        run: bash scripts/check.sh
```

### 3.3 `.gitignore`

```gitignore
/build/
*.class
```

### 3.3a `.gitattributes`

```gitattributes
*.sh text eol=lf
```

On Windows, Git can convert line endings to CRLF when it checks files out. Git Bash tolerates a CRLF script, but WSL and Linux bash do not: `set -euo pipefail` then fails with `set: pipefail: invalid option name`. This one-line file keeps shell scripts in LF form so a fresh clone behaves the same everywhere. Commit it with the other files.

### 3.4 `README.md`

````markdown
# Campus Equipment Lending: Chapter 4 checkpoint

## Requirements

Use Java 17 JDK and Bash (on Windows, Git Bash or WSL). Check `java -version` and `javac -version`.
There are no external Java dependencies in this checkpoint.
The classes use the unnamed package. This is not yet a Maven/JUnit build.

## Verify

From this directory:

```bash
bash scripts/check.sh
```

Expected: all 34 Chapter 2 checks and all 5 Chapter 3 acceptance example
 groups pass, followed by `BUILD AND CHECKS PASSED`.
A compilation or check failure must give a nonzero exit status.

## Demonstrate

After verification:

```bash
java -cp build/classes Chapter04Demo
```

Expect confirmation R1, rejection for an overlapping CAM1 request,
confirmation R2 for an adjacent CAM1 request, and two stored records.
The demonstration has fixed synthetic inputs; it is not interactive.

## Scope

Data lives in one in-memory coordinator and disappears on restart.
Loan periods include the start date and exclude the end date.
All stored reservations count as active. Identifiers are checked for
nonblank text, not against a directory or catalogue. Requests are
sequential; no concurrency guarantee is made. There is no cancellation,
email delivery, database or read-only availability query yet.

## Review and CI

Open a small change for review, explain its purpose and include local
check results. Resolve blocking findings before integrating it.
The supplied workflow checks pushes and pull requests. Keep the passing
run for the integrated revision. A workflow file alone is not evidence
that hosted checks ran. Record real run URLs and review details in the
team evidence notes; do not fabricate them.

## Next slice

US-02: inspect availability for one fixture item and interval without
changing stored reservations. The planned acceptance examples are
AQ-01 through AQ-05 in Chapter 4. They are not implemented by this starter.
````

### 3.5 Why the gate is structured this way

The script first changes to the project root relative to its own location. This makes its source paths independent of the caller's working directory. It removes generated `.class` files beneath this starter's `build/classes`, preventing a deleted source from surviving only as an old compiled class. It does not delete source files.

The shell options stop this straight-line script on a failing command, reject unset variables and propagate failures through pipelines if pipelines are added. The compilation uses UTF-8 source encoding and the Java 17 release target. Every Java file directly within the two listed source directories is compiled together. If named packages or nested source directories are added later, update the source-discovery approach or migrate the gate to the planned build tool; these globs are not recursive.

`CHAPTER_JAVAC` is an optional path to a compiler executable. Ordinary use leaves it unset, selecting `javac`. It is a single executable path, not a place to put a multiword shell command. Some environments provide `java` but no `javac` launcher, and the override is for them; learners with a normal JDK should not need it.

The script runs the two check programs as separate Java processes. Its final success message follows both. There is no `|| true`, catch-and-ignore handler or success message issued before checking. Adding another check class also requires adding its execution command: compilation alone does not run a class's `main` method.

### 3.6 What the workflow adds

The workflow requests runs for pushes, pull requests and manual dispatch. It grants read access to repository contents, uses a hosted Ubuntu runner, installs Temurin Java 17 and invokes the same gate. A push associated with a pull request may produce both kinds of run; this simple template accepts that duplication. Optimising triggers is outside the kickoff exercise.

The example uses `actions/checkout@v7` and `actions/setup-java@v6`, checked against the current official action sources on 12 October 2026 [4, 5]. It requests the Java 17 line rather than fixing a patch build. Major action tags and the hosted runner image may change; record resolved versions from the run log. For an institution-managed runner, consult the current action requirements before reuse. This file has not been executed on a hosted runner by the author.

A passing workflow does not automatically configure merge requirements. Configure the shared branch to require the agreed review and `verify` job where the repository supports it, or document the manual policy. Do not describe a requested policy as enforced unless it actually is.

### 3.7 A small repository workflow

In a new directory containing only the reconstructed starter, initialise a repository if one does not already exist:

```bash
git init -b main
git add README.md .gitignore .gitattributes src scripts .github
git commit -m "Establish Chapter 4 reservation baseline and checks"
```

Git needs your normal author identity configured. Do not use another person's identity or invent review attribution. In an existing course repository, use its established base branch and workflow instead of reinitialising it.

For subsequent work:

```bash
git switch -c docs/clarify-reservation-scope
```

Make a bounded documentation change, inspect `git diff`, run the gate, stage the specific changed file and commit. Push to the team's already established remote, then open the change for review using the institution's normal interface. Remote creation and authentication are environment-specific; there is no pre-existing remote URL supplied by this book.

A useful review description contains the problem, the change, the behaviour or limitation being clarified, the command run and its result. A reviewer should record an actual observation, such as finding that the README omitted the session-only storage limit. Resolve the comment and retain the real exchange. Model descriptions in this file are examples, not evidence of a performed review.

## 4. Deliberate failure experiment

This exercise checks the execution path from a failed assertion to a failed gate. It is separate from introducing a defect into the application.

1. Obtain a passing baseline with `bash scripts/check.sh`.
2. Create a disposable practice branch, for example `git switch -c practice/ci-failure`.
3. In `src/test/java/Chapter03AcceptanceExamples.java`, change only this line:

```java
require(coordinator.reservations().size() == 1, "AC-01 one record");
```

Replace it with the intentionally incorrect expectation:

```java
require(coordinator.reservations().size() == 2, "AC-01 one record");
```

4. Run the gate and inspect the error. In an interactive Bash terminal, the command below prints the status of the preceding gate:

```bash
bash scripts/check.sh
echo "$?"
```

The author run returned `1` and included:

```text
All 34 chapter checks passed.
Exception in thread "main" java.lang.AssertionError: AC-01 one record
```

The stack trace points to the acceptance program. `BUILD AND CHECKS PASSED` must be absent. This is the intended failure, because one successful reservation should produce one record.

5. For hosted evidence, commit this labelled practice change and push the practice branch to the team's authorised repository. Inspect the failed check step, not merely the overall colour of the run. Keep its revision and result. Do not merge this deliberately wrong expectation into the shared branch.
6. Restore `== 1`, commit the restoration on the practice branch and run the same checks again. Retain the restored passing run.
7. Return to the normal baseline and verify that it also remains green. Close the practice review without merging the deliberate defect, following the team's workflow.

The local experiment can also be done in a separate copy if no remote is available. That proves local failure propagation but does not supply hosted CI evidence. Report the distinction explicitly.

**What this proves:** the acceptance program runs, its failed condition causes a Java process failure, and the shell gate returns failure instead of hiding it. **What it does not prove:** every defect will be detected, every acceptance criterion is covered, or the hosted workflow has executed. Chapter 7 develops test quality; Chapter 13 develops the delivery pipeline.

## 5. Model kickoff artefacts

These are suggested solutions. They are not signed-off stakeholder decisions, a real team's plan or assessed submission evidence. Alternative solutions are valid when their behaviour, scope and trade-offs are coherent.

### 5.1 Vision and scope

**Working vision:** help an equipment officer demonstrate clear reservation decisions for a controlled set of student borrowers and equipment, and inspect accepted records without creating overlapping reservations for the same item in one coordinator.

**Kickoff goal:** make the existing baseline reproducible and reviewable, and prepare the next availability slice.

**Candidate next iteration goal:** let the officer inspect availability for one fixture item and interval without changing reservations.

**In scope for the demonstration:** one item per request; inclusive start and exclusive end; student rules of fewer than three existing reservations and durations from one to seven days; deterministic synthetic fixtures; sequential calls in one process.

**Outside this checkpoint:** persistent storage, actual directory or catalogue validation, cancellation, return processing, email delivery, multi-user concurrency and a polished web or mobile interface. These boundaries do not settle the production design.

**Open questions:** treatment of past dates; operational turnaround between loans; authority to cancel; definition of an active reservation after cancellation or completion; catalogue source and its failure behaviour. Resolve only those that block the selected next outcome; attach an owner and a review trigger to the others.

### 5.2 Two decision records

| Field | D-01: storage | D-02: availability interaction |
|---|---|---|
| Question | Must kickoff preserve records across restarts? | What input expresses the query interval? |
| Proposed decision | Keep one in-memory coordinator | Use start and explicitly labelled exclusive end |
| Reason | Demonstration evaluates reservation decisions in one session | Makes the half-open interval visible during discussion |
| Consequence | Restart loses records and identifier sequence restarts | Officer needs clear date guidance; equal/reversed bounds must be reported |
| Review trigger | A selected outcome requires a session to survive restart | User walkthrough reveals persistent confusion or prefers duration |
| Status | Existing teaching baseline | Proposed interaction decision; obtain team agreement before implementation |

D-02 does not change the existing `reserve` signature, which still accepts start and duration. Separate operations may have different interaction needs, but the team should justify the difference. A duration-based query sketch is also reasonable if its conversion to an interval is explicit and checked.

### 5.3 Epics and ordered backlog

| Group | Item | State and next action |
|---|---|---|
| Reservation decisions | US-01: eligible reservation | Core exists; collect actual delivery and review evidence |
| Reservation decisions | US-02: availability enquiry | Refine AQ-01–AQ-05; select as candidate next slice |
| Delivery support | EN-01: automated build/checks | Local gate supplied; obtain hosted run evidence |
| Record lifecycle | US-03: borrower record inspection | Defer filtering and interaction until selected |
| Record lifecycle | US-04: cancellation | Clarify authority and count effects before estimating |
| Equipment identity | US-05: unknown-item rejection | Clarify catalogue contract before implementing |

The row order retains Chapter 3's backlog order. Scheduling EN-01 during kickoff is a visible enabling dependency, not a claim that it is a newly requested user feature. US-01 should not move to Done solely because its implementation already exists: the agreed delivery conditions still need evidence.

### 5.4 Proposed US-02 contract

**Story:** as an equipment officer, I want to inspect whether one fixture item is available for a stated interval, so I can discuss a possible reservation without creating one.

**Acceptance:** AQ-01–AQ-04 report availability correctly for empty state, overlap, adjacency and a different fixture item. AQ-05 reports an identifiable invalid-period outcome for equal or reversed bounds. Every enquiry leaves all reservation contents unchanged.

**Interface decision still required:** choose and document an invalid-input representation, such as a caught argument exception translated at the interaction boundary, or a result value that distinguishes invalid from unavailable. Do not present both as simultaneously implemented. No new API is supplied in this checkpoint.

**Necessary tasks:** agree the contract; add a read-only operation; add the thin interaction; test results and non-mutation; review and integrate; update instructions and demonstrate. **Deferred tasks:** calendar styling, bulk search, live catalogue integration and persistent storage.

**Review trap:** availability does not imply eligibility. If B1 already holds three active reservations, an unreserved item can be available even though B1 cannot successfully reserve it. Reusing `reserve` as the enquiry mixes those questions and changes state.

### 5.5 Capacity model and replanning example

Available person-hours are `6 + 6 + 5 + 5 = 22`. Reserve four for coordination, integration support and administration, leaving 18. The selected forecast is `2 + 4 + 3 + 3 + 2 = 14`: contract, query behaviour, interaction, checks, then review/integration/documentation/demo. Four hours remain unallocated. These are invented figures for reasoning, not prescribed team availability.

Suppose implementation is revised from four to nine hours after discovering a contract ambiguity. Selected work becomes 19 hours, exceeding the 18-hour budget even before retaining any margin. Do not preserve the original status by removing checks. Revisit the ambiguity and reduce an optional part of the interaction, or revise the forecast transparently. If no coherent, verified slice fits, report that the outcome is at risk and renegotiate the selected work with the appropriate decision-maker.

A plan might remain infeasible even after the total fits. Check review windows, knowledge concentration and dependencies. If the reviewer is only available early, reserve an early contract review and a second person for final verification, rather than assuming the same reviewer can appear at the last minute.

### 5.6 Team agreement example

- Keep stories and acceptance examples in shared project notes; preserve identifiers when refining wording.
- Use Backlog, Ready, Building, Review and Done. Limit Building plus Review to two items; blocked items count.
- Keep branches small enough for a reviewer to explain their purpose and effects.
- Authors run the gate before review and after corrections. Reviewers inspect behaviour, state effects and evidence.
- Resolve blocking findings before integration. Record the shared branch's check result after integration.
- Mark unavailable review or CI evidence as a gap with a next action; never manufacture it.

Suggested Definition of Done addition: “The agreed automated gate passed on the integrated revision, and the team can locate its result.” Retain Chapter 3's example verification, actual review, updated notes and reproducible demo requirements. This is a model team policy, not a replacement for the module's assessment rules.

### 5.7 Evidence-note template

Create an evidence note using real values. The following is a blank template, deliberately **not completed evidence**:

| Field | Team entry |
|---|---|
| Repository and baseline revision | Fill with the actual repository and commit |
| Implemented behaviour | List only the behaviour present at that revision |
| Local environment and command | Record Java version, shell and command |
| Local check result | Record observed exit status and relevant output |
| Hosted passing run | Actual run URL or retained log, tested revision and date |
| Deliberate failure | Practice revision, failed assertion and failed run |
| Restored pass | Restored revision and passing run |
| Independent review | Actual reviewer, finding, correction and follow-up |
| Unresolved questions | Owner, impact and next decision point |
| Known limitations | Scope boundaries relevant to interpreting the demo |

For traceability, link US-01 AC-01 to its block in `Chapter03AcceptanceExamples`, then to a run that executed that file. Do not link US-02 to the old checks as if they exercise a query that does not yet exist.

## 6. AI activity: model critique

The student chapter's fixture is author-written fictional AI output. The following is a model evaluation, not evidence of an actual AI session.

| Fixture proposal | Verdict | Reason and correction |
|---|---|---|
| Allocate all 22 hours to features | Reject | Coordination, review and uncertainty consume capacity; use the explicit budget |
| Deliver query, cancellation, mobile, database and email together | Reject | The selected goal is one query slice; several additions lack agreed requirements |
| Give each member one layer and integrate at the end | Revise | Ownership can help, but final-day integration delays learning; collaborate around the thin journey |
| Convert three story points into three hours | Reject | No valid conversion was established; estimate tasks using actual understanding |
| Call `reserve` and then delete the record to check availability | Reject | Query must not change state; deletion is not even a supplied operation; eligibility also differs |
| Defer failure cases | Reject | Invalid intervals and non-mutation are part of this outcome's acceptance |
| Mark EN-01 complete when YAML is committed | Reject | Configuration must execute successfully and detect the intended failure |
| A green badge proves the whole story | Reject | The gate only checks executed conditions; current checks cover reservation, not US-02 |

A corrected response should state the candidate availability goal, AQ-01–AQ-05, the 18-hour planning budget and 14-hour selected forecast, as well as review and observed CI evidence. It should state its invented planning assumptions rather than describe them as the team's actual capacity.

Independent verification includes tracing `reserve` to its `reservations.add` call, observing the absence of a query method, checking the arithmetic, and inspecting actual check output. Asking a second AI model whether the first plan is good does not replace those observations.

An acceptable AI-use record names the prompt or fixture, claims examined, decisions, evidence and remaining uncertainty. A paid service is unnecessary. The offline fixture supports the same critique and correction.

## 7. Review-question solutions

### 7.1 Concept questions

**1. Vision, goal and task.** The vision describes the officer's improved ability to make clear reservation decisions. The next iteration goal concerns inspecting availability without changing records. Implementing a read-only operation is one task supporting that goal. A list of technical tasks alone does not express the user outcome.

**2. Console vertical slice.** A slice is complete relative to its promised outcome when input reaches the relevant behaviour and storage decision and produces an inspectable result. A console can support that journey. Adding a database or graphical interface is only necessary when the outcome requires it. The supplied fixed demo is evidence of the existing journey; a genuinely interactive new slice must deliver its promised input handling too.

**3. Capacity versus feasibility.** Summed hours omit dependencies, calendar overlap, skill availability and review timing. Four people available on different days may be unable to pair or review when needed. Check the sequence and collaboration windows as well as the total; account for pairing in person-hours.

**4. Meaning of a pass.** The particular checks executed successfully against the compiled revision in the recorded environment. The pass leaves unproven untested cases, unspecified rules, hosted execution if only run locally, independent review, concurrency safety, and user acceptance of the proposed interaction. It does not certify that US-02 exists.

### 7.2 Applied diagnosis

**5. Mutating availability enquiry.** Calling `reserve` violates the read-only requirement before any attempted cleanup. A successful reservation appends a record. Eligibility can also reject the request for borrower-specific reasons even when the item is available. The current public snapshot cannot be used to delete the new record because it is unmodifiable.

Inspect a before-and-after snapshot of record identifiers, borrower/item identifiers and period bounds, not only the number of records. For a future query test, preserve all those values and compare them after every success, unavailable result and invalid-input outcome. The corrected implementation should inspect availability directly without inserting and removing records. A transaction or rollback design is unnecessary for this small query and would not explain the eligibility mismatch.

**6. Ignored exit status.** The `|| true` branch turns the failing Java command into a successful shell list. A subsequent echo can then make the job look successful. Remove the failure suppression and run the acceptance program as a normal command in the supplied gate. Repeat the deliberately wrong AC-01 expectation and verify nonzero exit with no final success marker. Restore the expectation and verify a passing result. A compile failure is insufficient because the defect concerns assertion-failure propagation.

## 8. Practical activity: model reasoning and feedback

A satisfactory solution has agreement across its artefacts. The scope identifies controlled fixtures and session-only storage. The sketches label exclusive ends. The backlog separates existing reservation capability from proposed query behaviour. The plan budgets checks and review. The README lets another person run the intended revision. Actual logs and review records support completion claims.

A useful walkthrough asks one student to play the equipment officer and another to record ambiguities. For example, the officer may interpret “end date” as the last borrowing day. Correct the label and recheck AQ-03. Record that observation as interface feedback only if the walkthrough actually occurred. The example describes a possible finding, not a pre-filled review record.

For the small repository change, reviewing the build script is enough to practise the workflow. A reviewer could ask why the checks are compiled but not executed, or why success is printed before the second runner. The author must correct any actual defect found. Do not intentionally insert those defects into the shared baseline to manufacture review activity.

Give feedback on these questions rather than counts of artefacts:

| Dimension | Useful feedback question |
|---|---|
| Scope | Can the team explain the conditions under which its claim is valid? |
| Slice | Does the result support one observable outcome, including necessary failures? |
| Planning | Is review and uncertainty accounted for, and can people collaborate when needed? |
| Traceability | Does the cited check actually exercise the criterion? |
| Workflow | Is there real evidence of review, corrections and the integrated result? |
| Honesty | Are proposed features, local checks and hosted runs labelled accurately? |

Do not impose an invented numerical rubric or require a specific board product. Use the module leader's assessment criteria. When hosted execution is blocked, the team should preserve useful local evidence and identify the exact missing result; whether an alternative satisfies assessment requirements is the module leader's decision.

**Optional extension solution:** duration matches the current reservation input and can be easier for an officer thinking “two days”. An exclusive end makes overlap boundaries explicit but may be misread as an inclusive last day. Either choice needs labels, conversion rules, invalid-input handling and examples at adjacent boundaries. The appropriate choice follows a user walkthrough, not a universal claim that one representation is always better.

## 9. Transfer challenge: one possible clinic plan

**Bounded goal:** let reception demonstrate an availability enquiry for one synthetic appointment slot without creating or altering bookings, within one running coordinator.

**Proposed sketch:** practitioner/resource identifier, appointment date, start time, duration, a Check action and a result that clearly distinguishes availability from a confirmed booking. Display the applicable time zone once the team has agreed it. Do not allow the interface to imply that the enquiry reserves the slot.

**Assumptions to revisit:** the demonstration uses one known synthetic resource and a single agreed scheduling zone; it excludes real appointment authority, patient identity and clinical workflow decisions. Before real use, clarify the authoritative schedule and booking permissions with the responsible stakeholders. These are open operational requirements, not policies for students to invent.

**Boundary example:** one appointment occupies `[09:00, 09:30)` and another requests `[09:30, 10:00)`. They do not overlap under that interval model. A required preparation interval could still make the second appointment invalid, so clarify it rather than copying the equipment answer. The equipment starter uses whole dates; an appointment system must decide how local times, dates and zones represent slots. Do not paste `LocalDate.plusDays` into a minute-based rule.

**Plan:** determine actual individual availability; budget coordination, review and uncertainty; select the single enquiry outcome with checks for overlap, adjacency and unchanged bookings. Defer reminders, payments, multiple clinics and calendars unless the selected outcome depends on them. Identify review windows before committing to the forecast.

**Gate evidence:** compile the starter and run supplied checks for the agreed booking semantics, then prove assertion-failure propagation. **Human evidence:** a walkthrough confirms that reception understands the result and time labels; stakeholder discussion resolves authority and operational assumptions. The automated gate cannot supply either conversation.

This solution illustrates transfer of planning principles while revisiting domain rules. Students should not be rewarded for reproducing the equipment project's exact class names or interval representation.

## 10. Teaching notes

Martin (2002) and Rubin (2012) are cited in the student chapter; this book treats sprint planning and iteration evidence in Chapter 4, and Scrum in Chapter 3.

The practical activity runs on the Team project with the lending starter as the model. The starter test is introduced in Arrange–Act–Assert terms for Chapter 7, and the Chapter 2 flat directory is mapped onto the conventional source layout. Milestone 1 needs hosted CI evidence, which depends on a repository the whole team can use. Ask teams to create that repository in the first session, so a late access problem does not become the only gap in their evidence.

Keep the chapter centred on planning a believable outcome and making evidence reproducible. Students can run supplied checks before learning TDD. They should understand which behaviours the checks protect, without being required to invent a testing framework.

Do not solve US-02 merely to make the repository look busier. Its refined story is the planning exercise; the cumulative code remains a stable starting point for the design work in Chapters 5–6. Likewise, do not add interfaces solely because the repository now has separate source directories.

For a team with stronger tooling experience, adapting the same gate to the institution's CI service is acceptable. Require equivalent observable behaviour: the intended revision is compiled, the checks execute, assertion failures fail the run and restored code passes. Do not confuse sophistication of pipeline configuration with quality of the engineering explanation.

The next chapter, **Responsibilities, Extension and Substitutability**, will use this baseline to inspect reasons for change and make small, protected design improvements. Comprehensive CI/CD, deployment and integration-testing choices remain for Chapter 13.

## References

The sources below support the referenced process and tool behaviour; the planning artefacts and solutions are author-created examples. Checked 12 October 2026.

1. Schwaber, K. and Sutherland, J., [The Scrum Guide](https://scrumguides.org/scrum-guide.html), November 2020.
2. Oracle, [The `javac` command, Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/specs/man/javac.html).
3. GitHub, [Building and testing Java with Maven](https://docs.github.com/en/actions/tutorials/build-and-test-code/java-with-maven). This checkpoint uses its own shell gate; the page supplies CI context rather than a claim that Maven is configured here.
4. GitHub Actions, [setup-java](https://github.com/actions/setup-java).
5. GitHub Actions, [checkout](https://github.com/actions/checkout).