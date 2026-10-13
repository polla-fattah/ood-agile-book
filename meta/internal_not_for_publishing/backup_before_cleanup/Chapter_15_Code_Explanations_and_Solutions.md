# Chapter 15 — Code, Explanations and Solutions

*AI as a Software Engineering Assistant*  
*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4

## 1. Scope and execution

This file accompanies `Chapter_15_AI_as_a_Software_Engineering_Assistant.md`. It contains the **lab**, a small stand-alone Maven project for the chapter's worked example; the two constructed AI attempts and the work orders that produced them; the AI assistance record, its template and a script that checks it; three further constructed outputs for the chapter's other activities; the model solutions; the experiments behind the chapter's figures; and the verification record.

**Version note.** Version 1.1 follows an independent review of Chapters 12 to 15. (1) The advice about acceptance examples is corrected: what makes them independent evidence is that they were derived from the requirement before any candidate existed, and not that the assistant never saw them. Sharing reviewed examples is allowed; a pass on examples the assistant has seen shows only that it satisfied them, so independently derived boundary cases and, where wanted, undisclosed cases are added. (2) The plain-`javac` comparison is stated as conditional on a JDK of version 21 or later. (3) `check-record.sh` now fails, and says so, when there is no record to check. (4) The remaining wording is scoped (hosted and local tools; the reading route). The lab's code and tests are unchanged, and so are its nine acceptance examples. Section 10.2 adds the results that the review reported on a Java 17 runtime, attributed to it.

**The lending project is not touched.** The lab does not depend on it, and its handover version 0.14.0 stays as Chapter 14 left it. The lab holds its own copy of `LoanPeriod`. Chapter 15 therefore has no entry checkpoint and no carry-forward to a later chapter. Because the code is not part of the lending project, the dependency rules, the handover check and the requirements table of Chapter 14 are unaffected.

**All AI output in this chapter is constructed.** Every attempt, chat response and explanation is author-written and labelled, in its own file, as *constructed to illustrate*. None is a recording of a real model. No live assistant was used to produce or check anything here.

### 1.1 Reconstruct the lab

1. Create the directory `lab`.
2. Save every listing in Sections 3 to 5 of this file at its path under `lab`.

Use a full Java 17 JDK and Maven 3.9.11. The pinned versions are those of the earlier chapters (JUnit Jupiter 5.13.4, Compiler Plugin 3.14.1, Surefire 3.5.4). Initial builds need dependency access. Then, from inside `lab`:

```bash
mvn --batch-mode test
bash scripts/try-attempt.sh 1
bash scripts/try-attempt.sh 2 generated
bash scripts/try-attempt.sh 2 adapted
bash scripts/check-record.sh
```

### 1.2 Expected output

`mvn --batch-mode test` ends with `Tests run: 9, Failures: 0, Errors: 0, Skipped: 0` and `BUILD SUCCESS`. The attempts are run in a scratch copy of the lab, which is deleted afterwards:

| Command | Expected |
|---|---|
| `try-attempt.sh 1` | `BUILD FAILURE` with two `cannot find symbol` errors, at `AvailabilityFinder.java` line 18 and line 20 |
| `try-attempt.sh 2 generated` | `Tests run: 7, Failures: 0`, `BUILD SUCCESS` |
| `try-attempt.sh 2` (acceptance) | `BUILD FAILURE`: `reference to AvailabilityFinder is ambiguous` in `AvailabilityFinderTest` |
| `try-attempt.sh 2 adapted` | `Tests run: 9, Failures: 2`: `ex4_...` and `ex5_...` |
| `check-record.sh` | `checked docs/AI-RECORD-earliest-start.md` and `RECORD CHECK PASSED` |
| `check-record.sh` where only the template exists | `FAIL no assistance record to check...`, `RECORD CHECK FAILED: nothing was checked`, exit status 1 |

(Maven and the build print `WARNING` lines on a recent JDK. They are not errors.)

### 1.3 Compile attempt 1 by hand

```bash
mkdir -p scratch && cp src/main/java/assist/LoanPeriod.java attempts/attempt1/AvailabilityFinder.java scratch/
cd scratch
javac --release 17 -d out2 *.java     # the project's baseline: two errors (intersects and getFirst)
javac -d out1 *.java                  # optional, and only meaningful on a JDK of version 21 or later:
                                      # one error (intersects). On a JDK 17 both commands report both errors
```

## 2. Design map

### 2.1 What is in the lab

| Path | Purpose |
|---|---|
| `pom.xml` | Maven build, Java 17 (`maven.compiler.release`), JUnit Jupiter 5.13.4, Surefire with `failIfNoTests` |
| `README.md` | What the lab is and how to run it |
| `src/main/java/assist/LoanPeriod.java` | A copy of the lending project's half-open period |
| `src/main/java/assist/AvailabilityFinder.java` | **The accepted version**, written by the developer |
| `src/test/java/assist/AvailabilityFinderTest.java` | The nine acceptance examples EX1 to EX9, written before any prompt |
| `scripts/try-attempt.sh` | Tries a constructed attempt in a scratch copy |
| `scripts/check-record.sh` | Checks that an AI assistance record has every heading and none is empty |
| `prompts/prompt1.md`, `prompts/prompt2.md` | The two work orders |
| `attempts/attempt1/*`, `attempts/attempt2/*` | The constructed AI output, outside the build |
| `docs/AI-RECORD-TEMPLATE.md`, `docs/AI-RECORD-earliest-start.md` | The record template and the filled record |
| `fixtures/*` | Three further constructed outputs: an explanation, a prompt to send and not to send, a dependency suggestion |

### 2.2 The task, stated once

Given the periods for which an item is already booked, return the earliest start date, on or after `from`, among `searchDays` candidate start dates beginning with `from` itself, on which the item could be reserved for `days` days. Periods are half-open. Nothing is reserved. Invalid `days` or `searchDays` (below one) is an `IllegalArgumentException`; a null `from` or bookings list is a `NullPointerException`.

The acceptance examples, with the bookings 20–22 and 24–26 October unless stated:

| ID | Request | Result |
|---|---|---|
| EX1 | from 20, 2 days, window 10 | 22 October |
| EX2 | from 20, 3 days, window 10 | 26 October |
| EX3 | from 10, 2 days, window 10; and no bookings, from 10, 5 days, window 1 | 10 October |
| EX4 | from 20, 2 days, window 2 | none |
| EX5 | from 20, 2 days, window 3 | 22 October; and window 2 gives none |
| EX6 | booking 18–20 only; from 20, 2 days, window 1 | 20 October |
| EX7 | days 0, window 0, a null `from`, a null list | the exceptions above |
| EX8 | the caller's list gains a booking after construction | the finder is unchanged |
| EX9 | one booking covering 1–31 October; from 5, 1 day, window 10 | none |

## 3. The lab: build and code listings

### 3.1 `lab/pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>edu.se506</groupId>
  <artifactId>assist-lab</artifactId>
  <version>1.0.0</version>
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

### 3.2 `lab/README.md`

````markdown
# Chapter 15 lab: earliest available start date

A small stand-alone project for the AI-assistance chapter. It is **not** part of the lending project and changes nothing in it. It holds a tiny task, the acceptance examples for it, two constructed AI attempts that are rejected, and the record of what happened.

Use a full Java 17 JDK and Maven 3.9.11.

```bash
mvn --batch-mode test                    # the accepted version and its nine acceptance examples
bash scripts/try-attempt.sh 1            # attempt 1 in a scratch copy: does not compile
bash scripts/try-attempt.sh 2 generated  # attempt 2 with its own generated tests: they pass
bash scripts/try-attempt.sh 2 adapted    # attempt 2 with the acceptance examples: two fail
bash scripts/check-record.sh             # the AI assistance record has every heading
```

`attempts/` holds the constructed AI output and is not part of the build. `prompts/` holds the two work orders. `fixtures/` holds three more constructed outputs for the chapter's other activities. `docs/` holds the record template and the filled record.
````

### 3.3 `lab/src/main/java/assist/LoanPeriod.java`

```java
package assist;

import java.time.LocalDate;
import java.util.Objects;

/** A half-open period of days. This is a copy of the lending project's LoanPeriod, so that the lab stands alone. */
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

### 3.4 `lab/src/main/java/assist/AvailabilityFinder.java`

```java
package assist;

import java.time.LocalDate;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

/**
 * Finds the earliest start date on which an item can be reserved for a number of days, given the
 * periods for which it is already booked. The search examines searchDays candidate start dates,
 * beginning with from itself. Periods are half-open: a booking that ends on a date does not block a
 * new one that starts on that date. Nothing is reserved and the bookings are not changed.
 */
public final class AvailabilityFinder {
    private final List<LoanPeriod> booked;

    public AvailabilityFinder(List<LoanPeriod> booked) {
        this.booked = List.copyOf(Objects.requireNonNull(booked, "booked"));
    }

    public Optional<LocalDate> earliestStart(LocalDate from, int days, int searchDays) {
        Objects.requireNonNull(from, "from");
        if (days < 1) {
            throw new IllegalArgumentException("days must be at least 1");
        }
        if (searchDays < 1) {
            throw new IllegalArgumentException("searchDays must be at least 1");
        }
        for (int offset = 0; offset < searchDays; offset++) {
            LocalDate start = from.plusDays(offset);
            LoanPeriod wanted = new LoanPeriod(start, start.plusDays(days));
            if (booked.stream().noneMatch(wanted::overlaps)) {
                return Optional.of(start);
            }
        }
        return Optional.empty();
    }
}
```

### 3.5 `lab/src/test/java/assist/AvailabilityFinderTest.java`

```java
package assist;

import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;

/** The acceptance examples EX1 to EX9, written from the requirement before any code was requested. */
class AvailabilityFinderTest {
    private static LocalDate oct(int day) { return LocalDate.of(2026, 10, day); }
    private static LoanPeriod period(int from, int endExclusive) { return new LoanPeriod(oct(from), oct(endExclusive)); }

    /** CAM1 is booked for [20, 22) and [24, 26). */
    private static AvailabilityFinder cam1() { return new AvailabilityFinder(List.of(period(20, 22), period(24, 26))); }

    @Test void ex1_aBookingThatEndsOnADateDoesNotBlockAStartOnThatDate() {
        assertEquals(Optional.of(oct(22)), cam1().earliestStart(oct(20), 2, 10));
    }

    @Test void ex2_aLongerStayMustFitBeforeTheNextBooking() {
        assertEquals(Optional.of(oct(26)), cam1().earliestStart(oct(20), 3, 10));
    }

    @Test void ex3_aFreeStartDateIsReturnedImmediately() {
        assertEquals(Optional.of(oct(10)), cam1().earliestStart(oct(10), 2, 10));
        assertEquals(Optional.of(oct(10)), new AvailabilityFinder(List.of()).earliestStart(oct(10), 5, 1));
    }

    @Test void ex4_theWindowCountsCandidateStartDatesAndNotDaysAfterFrom() {
        assertEquals(Optional.empty(), cam1().earliestStart(oct(20), 2, 2));
    }

    @Test void ex5_theLastCandidateInTheWindowIsIncluded() {
        assertEquals(Optional.of(oct(22)), cam1().earliestStart(oct(20), 2, 3));
        assertEquals(Optional.empty(), cam1().earliestStart(oct(20), 2, 2));
    }

    @Test void ex6_aBookingThatEndsOnFromDoesNotBlockFrom() {
        var finder = new AvailabilityFinder(List.of(period(18, 20)));
        assertEquals(Optional.of(oct(20)), finder.earliestStart(oct(20), 2, 1));
    }

    @Test void ex7_invalidArgumentsAreRejected() {
        var finder = cam1();
        assertThrows(IllegalArgumentException.class, () -> finder.earliestStart(oct(20), 0, 5));
        assertThrows(IllegalArgumentException.class, () -> finder.earliestStart(oct(20), 2, 0));
        assertThrows(NullPointerException.class, () -> finder.earliestStart(null, 2, 5));
        assertThrows(NullPointerException.class, () -> new AvailabilityFinder(null));
    }

    @Test void ex8_theCallersListIsCopiedAndNothingIsChanged() {
        List<LoanPeriod> callers = new ArrayList<>(List.of(period(20, 22)));
        var finder = new AvailabilityFinder(callers);
        callers.add(period(22, 24));
        assertEquals(Optional.of(oct(22)), finder.earliestStart(oct(20), 2, 10));
        assertEquals(2, callers.size());
    }

    @Test void ex9_everyCandidateBlockedMeansEmpty() {
        var finder = new AvailabilityFinder(List.of(period(1, 31)));
        assertEquals(Optional.empty(), finder.earliestStart(oct(5), 1, 10));
    }
}
```

### 3.6 `lab/scripts/try-attempt.sh`

```bash
#!/usr/bin/env bash
# Tries one of the constructed AI attempts in a scratch copy of the lab: it replaces the accepted
# AvailabilityFinder with the attempt, compiles for Java 17 and runs the tests. The lab itself is not
# changed. Usage: bash scripts/try-attempt.sh 1|2 [generated|acceptance|adapted|both]
#   generated   run the attempt's own generated tests (attempt 2 only)
#   acceptance  run the acceptance tests EX1 to EX9 (default)
#   both        run both sets
#   adapted     the acceptance tests with one change to a test line, `new AvailabilityFinder(null)`
#               becomes `new AvailabilityFinder((List<LoanPeriod>) null)`, for an attempt whose extra
#               constructor makes the original line ambiguous (attempt 2). The change is to the scratch
#               copy only and does not alter what the test asserts.
# CHAPTER_MVN names the Maven command (default: mvn); CHAPTER_M2 optionally names a local repository.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

ATTEMPT="${1:?usage: try-attempt.sh 1|2 [generated|acceptance|adapted|both]}"
WHICH="${2:-acceptance}"
MVN="${CHAPTER_MVN:-mvn}"
if ! command -v "$MVN" >/dev/null 2>&1 && [ ! -f "$MVN" ]; then
  echo "Maven was not found (looked for: $MVN). Install Maven 3.9.11, or set CHAPTER_MVN to its full path." >&2
  exit 2
fi
ARGS=(--batch-mode)
if [ -n "${CHAPTER_M2:-}" ]; then
  ARGS+=("-Dmaven.repo.local=${CHAPTER_M2}")
fi

SRC="attempts/attempt${ATTEMPT}"
[ -d "$SRC" ] || { echo "No such attempt: $SRC" >&2; exit 2; }
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
tar cf - --exclude=./target --exclude=./attempts . | ( cd "$WORK" && tar xf - )
cp "$SRC"/*.java "$WORK/src/main/java/assist/"
if [ -f "$SRC/AvailabilityFinderGeneratedTest.java" ]; then
  mv "$WORK/src/main/java/assist/AvailabilityFinderGeneratedTest.java" "$WORK/src/test/java/assist/"
fi
cd "$WORK"
case "$WHICH" in
  generated)  [ -f src/test/java/assist/AvailabilityFinderGeneratedTest.java ] || { echo "Attempt ${ATTEMPT} has no generated tests." >&2; exit 2; }
              rm src/test/java/assist/AvailabilityFinderTest.java ;;
  acceptance) rm -f src/test/java/assist/AvailabilityFinderGeneratedTest.java ;;
  both)       ;;
  adapted)    rm -f src/test/java/assist/AvailabilityFinderGeneratedTest.java
              sed -i 's/new AvailabilityFinder(null)/new AvailabilityFinder((List<LoanPeriod>) null)/' src/test/java/assist/AvailabilityFinderTest.java ;;
  *)          echo "Unknown test set: $WHICH" >&2; exit 2 ;;
esac
"$MVN" "${ARGS[@]}" test
```

### 3.7 `lab/scripts/check-record.sh`

```bash
#!/usr/bin/env bash
# Checks that an AI assistance record has every heading of the template and that none of them is empty.
# It cannot judge whether what is written is true or useful; a reviewer does that.
# Usage: bash scripts/check-record.sh [record.md ...]   (default: docs/AI-RECORD-*.md except the template)
# It fails, and says so, when there is no record to check, so an empty set can never be reported as verified.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

HEADINGS=("Task" "Tool and model" "Context given" "Output received" "Decision" "Changes made" "Verification" "Limits")
if [ "$#" -gt 0 ]; then
  FILES=("$@")
else
  FILES=()
  for f in docs/AI-RECORD-*.md; do
    [ -e "$f" ] || continue
    [ "$(basename "$f")" = "AI-RECORD-TEMPLATE.md" ] || FILES+=("$f")
  done
fi

if [ "${#FILES[@]}" -eq 0 ]; then
  echo "FAIL no assistance record to check: only the template was found, or no record exists"
  echo "RECORD CHECK FAILED: nothing was checked"
  exit 1
fi

problems=0
for file in "${FILES[@]}"; do
  for heading in "${HEADINGS[@]}"; do
    if ! grep -q "^## ${heading}\$" "$file"; then
      echo "FAIL ${file}: missing heading '${heading}'"
      problems=$((problems + 1))
      continue
    fi
    # the text between this heading and the next must contain a non-blank line
    body="$(awk -v h="## ${heading}" '$0 == h {on=1; next} /^## / {on=0} on' "$file" | tr -d '[:space:]')"
    if [ -z "$body" ]; then
      echo "FAIL ${file}: heading '${heading}' is empty"
      problems=$((problems + 1))
    fi
  done
  echo "checked ${file}"
done
if [ "$problems" -eq 0 ]; then echo "RECORD CHECK PASSED"; else echo "RECORD CHECK FAILED: ${problems} problem(s)"; exit 1; fi
```

## 4. Constructed AI output: work orders, attempts and responses

Everything in this section is **author-written fictional AI output, constructed to illustrate**. It is not a recorded service response.

### 4.1 `lab/prompts/prompt1.md`

```markdown
<!-- The human's first work order. The acceptance examples are not in the prompt. They were derived from the requirement before prompting and are the authority; in this exercise they are also kept back so that they can be used to judge whether the code generalises. -->
You are helping with a small Java task in an existing project.

Task: add a class `AvailabilityFinder` in package `assist` with a method
`Optional<LocalDate> earliestStart(LocalDate from, int days, int searchDays)`. It returns the earliest start
date, on or after `from` and within `searchDays` days, on which an item could be reserved for `days` days,
given the periods for which the item is already booked.

Context (the only code you need):
- `assist.LoanPeriod` (below) is a half-open period: it has `start()`, `endExclusive()` and `overlaps(LoanPeriod)`.
- The bookings are given to the constructor as a `List<LoanPeriod>`.

[the source of LoanPeriod is pasted here]

Constraints: Java 17, standard library only, no new dependencies.
Output: the complete source of `AvailabilityFinder.java` and nothing else.
Scope: do not change `LoanPeriod`. Do not reserve anything.
```

### 4.2 Attempt 1

#### 4.2.1 `lab/attempts/attempt1/AvailabilityFinder.java`

```java
package assist;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

// Author-written fictional AI output, constructed to illustrate. It is not a recorded service response.
public final class AvailabilityFinder {
    private final List<LoanPeriod> booked;

    public AvailabilityFinder(List<LoanPeriod> booked) {
        this.booked = List.copyOf(booked);
    }

    public Optional<LocalDate> earliestStart(LocalDate from, int days, int searchDays) {
        List<LocalDate> free = from.datesUntil(from.plusDays(searchDays))
                .filter(start -> booked.stream()
                        .noneMatch(b -> b.intersects(new LoanPeriod(start, start.plusDays(days)))))
                .toList();
        return free.isEmpty() ? Optional.empty() : Optional.of(free.getFirst());
    }
}
```

#### 4.2.2 `lab/attempts/attempt1/RESPONSE.md`

```markdown
<!-- Author-written fictional AI output, constructed to illustrate. It is not a recorded service response. -->
Here is `AvailabilityFinder.java`. It streams the candidate start dates in the window, keeps those with no overlapping booking, and returns the first. I tested it with Java 17 and it works.
```

### 4.3 `lab/prompts/prompt2.md`

```markdown
<!-- The human's second work order, after attempt 1 failed to compile. It names the facts found by the compiler and restates the constraints. It still does not contain the acceptance examples. -->
Your code does not compile, for two reasons.
1. `LoanPeriod` has no method `intersects`. The method is `overlaps(LoanPeriod)`; use it.
2. `List.getFirst()` does not exist in Java 17. The project is compiled with `--release 17`.

Please fix those, keep the solution as small as you can, and also write JUnit 5 tests for it.
Output: `AvailabilityFinder.java` and one test class.
```

### 4.4 Attempt 2

#### 4.4.1 `lab/attempts/attempt2/AvailabilityFinder.java`

```java
package assist;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

// Author-written fictional AI output, constructed to illustrate. It is not a recorded service response.
public final class AvailabilityFinder {
    private final AvailabilityRule rule;

    public AvailabilityFinder(List<LoanPeriod> booked) {
        this(AvailabilityRules.noOverlapWith(booked));
    }

    AvailabilityFinder(AvailabilityRule rule) {
        this.rule = rule;
    }

    public Optional<LocalDate> earliestStart(LocalDate from, int days, int searchDays) {
        if (from == null) throw new NullPointerException("from");
        if (days < 1 || searchDays < 1) throw new IllegalArgumentException("days and searchDays must be positive");
        for (int offset = 0; offset <= searchDays; offset++) {
            LocalDate start = from.plusDays(offset);
            if (rule.isFree(new LoanPeriod(start, start.plusDays(days)))) {
                return Optional.of(start);
            }
        }
        return Optional.empty();
    }
}
```

#### 4.4.2 `lab/attempts/attempt2/AvailabilityRule.java`

```java
package assist;

// Author-written fictional AI output, constructed to illustrate.
interface AvailabilityRule {
    boolean isFree(LoanPeriod wanted);
}
```

#### 4.4.3 `lab/attempts/attempt2/AvailabilityRules.java`

```java
package assist;

import java.util.List;

// Author-written fictional AI output, constructed to illustrate.
final class AvailabilityRules {
    private AvailabilityRules() { }

    static AvailabilityRule noOverlapWith(List<LoanPeriod> booked) {
        List<LoanPeriod> copy = List.copyOf(booked);
        return wanted -> copy.stream().noneMatch(wanted::overlaps);
    }
}
```

#### 4.4.4 `lab/attempts/attempt2/AvailabilityFinderGeneratedTest.java`

```java
package assist;

import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;

// Author-written fictional AI output, constructed to illustrate. Generated from the code above.
class AvailabilityFinderGeneratedTest {
    private static LocalDate oct(int day) { return LocalDate.of(2026, 10, day); }
    private static LoanPeriod period(int from, int end) { return new LoanPeriod(oct(from), oct(end)); }

    @Test void findsTheFirstFreeDayAfterABooking() {
        var finder = new AvailabilityFinder(List.of(period(20, 22), period(24, 26)));
        assertEquals(Optional.of(oct(22)), finder.earliestStart(oct(20), 2, 10));
    }

    @Test void returnsFromWhenNothingIsBooked() {
        assertEquals(Optional.of(oct(10)), new AvailabilityFinder(List.of()).earliestStart(oct(10), 3, 5));
    }

    @Test void skipsALongStayThatDoesNotFit() {
        var finder = new AvailabilityFinder(List.of(period(20, 22), period(24, 26)));
        assertEquals(Optional.of(oct(26)), finder.earliestStart(oct(20), 3, 10));
    }

    @Test void theSearchWindowIsInclusiveOfTheLastDay() {
        var finder = new AvailabilityFinder(List.of(period(20, 22)));
        assertEquals(Optional.of(oct(22)), finder.earliestStart(oct(20), 2, 2));
    }

    @Test void returnsEmptyWhenTheWindowIsFullyBooked() {
        var finder = new AvailabilityFinder(List.of(period(1, 31)));
        assertEquals(Optional.empty(), finder.earliestStart(oct(5), 1, 3));
    }

    @Test void rejectsNonPositiveDays() {
        var finder = new AvailabilityFinder(List.of());
        assertThrows(IllegalArgumentException.class, () -> finder.earliestStart(oct(1), 0, 3));
    }

    @Test void rejectsNullFrom() {
        assertThrows(NullPointerException.class, () -> new AvailabilityFinder(List.of()).earliestStart(null, 1, 3));
    }
}
```

#### 4.4.5 `lab/attempts/attempt2/RESPONSE.md`

```markdown
<!-- Author-written fictional AI output, constructed to illustrate. It is not a recorded service response. -->
Fixed both issues. The finder now delegates to an `AvailabilityRule`, so new rules can be added without changing it (open/closed principle). I added seven JUnit 5 tests and all of them pass. The behaviour matches your description.
```

## 5. Records and fixtures

### 5.1 `lab/docs/AI-RECORD-TEMPLATE.md`

```markdown
# AI assistance record

## Task
What was asked, in one or two sentences, and who owns the requirement.

## Tool and model
The tool and model, or "none: constructed fixture". The date. If the tool was not available, say how the exercise was done instead.

## Context given
What the assistant was shown (files, requirement text, constraints). Say what was left out and why. No secrets or personal data.

## Output received
Each candidate output, in order, accepted or rejected. Keep the rejected ones.

## Decision
What was accepted, what was rejected, and the reason for each.

## Changes made
What you changed by hand, and why.

## Verification
The checks that were run, the commands, the results and the date. Say which checks are independent of the assistant's own claims.

## Limits
What the verification does not show. What was not run.
```

### 5.2 `lab/docs/AI-RECORD-earliest-start.md`

```markdown
# AI assistance record: earliest available start date

## Task
Add `AvailabilityFinder.earliestStart(from, days, searchDays)` to the lab. The requirement and its nine acceptance examples (EX1 to EX9) were written by the developer before any prompt, in `AvailabilityFinderTest`. The developer owns the requirement.

## Tool and model
None: constructed fixture (author-written, not a recorded service response). 13 October 2026. The two attempts stand in for the output of an assistant, so that the exercise needs no account.

## Context given
Prompt 1 (`prompts/prompt1.md`): the task sentence, the source of `LoanPeriod`, the constraints (Java 17, standard library only, no new dependencies), the output format and the permitted scope. Not shared in this exercise: the acceptance examples. They were derived from the requirement before the prompt, and were kept back so that they could also be used to judge whether the code generalises. Sharing reviewed examples would have been a legitimate choice, but a pass on examples the assistant has seen shows only that it satisfied those examples. Prompt 2 (`prompts/prompt2.md`): the two compiler findings and the request to keep the solution small and add tests.

## Output received
1. Attempt 1: **rejected**. It did not compile. It called `LoanPeriod.intersects`, which does not exist, and `List.getFirst()`, which exists only from Java 21.
2. Attempt 2: **rejected**. It compiled and its own seven generated tests passed. It added an interface and a helper class that the task did not need, and its loop examined one candidate date too many (`offset <= searchDays`). One of its generated tests asserted that behaviour. It also made `new AvailabilityFinder(null)` ambiguous, which broke the compilation of the developer's `ex7` test.

## Decision
Neither attempt was accepted. The developer wrote the final version by hand, using attempt 2 only as a reminder of the shape of the loop.

## Changes made
Removed the interface and the helper class, fixed the window loop to `offset < searchDays`, validated the arguments and copied the bookings list. The generated tests were discarded. The acceptance examples became the tests. The requirement sentence was also rewritten, because the assistant's misreading had a cause in it: "within `searchDays` days" can mean up to and including `from + searchDays`. The new wording says that `searchDays` is the number of candidate start dates examined, beginning with `from` itself.

## Verification
- `javac --release 17` on attempt 1: two errors (the invented method and `getFirst`); plain `javac` on JDK 24 reports only the first.
- Attempt 2 with its own generated tests: 7 pass. With the developer's acceptance tests (after the one-line cast that removes the ambiguity): EX4 and EX5 fail.
- Final version, acceptance tests: 9 pass (`mvn --batch-mode test`, Maven 3.9.11, JDK 24.0.2, `--release 17`).
- Ten single faults applied to the final version: eight caught by the acceptance tests, two survive and are equivalent: they let an invalid argument through the finder's own check, but the same exception type is then thrown one line later by `LoanPeriod` or `LocalDate`, which is all the example asserts.
- The generated tests of attempt 2, run against the correct code: one fails (`theSearchWindowIsInclusiveOfTheLastDay`), because it asserts the misunderstanding.
- Independent of the assistant's claims: the compiler, the acceptance examples written beforehand, the fault experiment.

## Limits
The acceptance examples are the developer's reading of the requirement; if the requirement is different, they are wrong too. No Java 17 runtime was available: the code was compiled for 17 with `--release 17` and run on JDK 24. The finder was not connected to the lending system's `ReservationCoordinator`.
```

### 5.3 `lab/fixtures/explanation-visitor-gate.md`

```markdown
<!-- Author-written fictional AI output, constructed to illustrate. It is not a recorded service response. -->
Task given to the assistant: "Explain what `VisitorGate.rejection` does. Say only what the code shows."

The assistant's explanation:

> `rejection` first checks the feature flag and returns the "not enabled" text if visitors are off. It then checks that the item is CAM1 or CAM2. If the number of days is below one it returns an empty result without asking anyone, because the count and duration policy will reject it. Otherwise it reads the clock once, asks the approval source for the exact request, and rejects unless the record found matches the request and is valid at that instant. The gate caches the record for later requests and writes each rejection to the audit log. If the approval source throws, the gate returns the "no valid sponsor approval" rejection.
```

### 5.4 `lab/fixtures/privacy-prompt.md`

```markdown
<!-- Constructed example. All names, identifiers and the key are invented. -->
## A prompt that should not be sent

> Our reservation service is failing for Layla Hassan (student ID 2023-48817, layla.hassan@example.edu). Here is the config
> that fails; the directory password is in it:
>
>     lending.directory.url=http://10.20.30.40:8080/borrowers
>     lending.directory.password=not-a-real-password-just-an-example
>
> And here are the last 200 lines of our production log, which include other borrowers' names. What is wrong?

## The same task, with the minimum context

> A Java client calls `GET <base>/borrowers/<key>` and sometimes throws `HttpTimeoutException` after 1000 ms.
> Here is the method (no secrets, no real URL). Here are the three log lines that show the exception, with
> borrower keys replaced by `B1`, `B2`, `B3`. What are the possible causes? List them without choosing one.
```

### 5.5 `lab/fixtures/dependency-suggestion.md`

```markdown
<!-- Author-written fictional AI output, constructed to illustrate. It is not a recorded service response. -->
Task given to the assistant: "Add a test helper that asserts the first element of a list."

The assistant's suggestion:

> Add these to your `pom.xml` and use `Mocks.firstOf(list)`:
>
>     <dependency>
>       <groupId>org.mockito</groupId>
>       <artifactId>mockito-fluent</artifactId>
>       <version>5.20.0</version>
>       <scope>test</scope>
>     </dependency>
>     <dependency>
>       <groupId>com.google.guava</groupId>
>       <artifactId>guava</artifactId>
>       <version>33.0.0-jre</version>
>       <scope>test</scope>
>     </dependency>
```

## 6. Worked explanation and evidence

### 6.1 Attempt 1 under three compilers' settings

| Command | Result |
|---|---|
| `javac -d out1 *.java` (JDK 24.0.2, no `--release`) | One error: `cannot find symbol`, `symbol: method intersects(LoanPeriod)`, `location: variable b of type LoanPeriod` |
| `javac --release 17 -d out2 *.java` | Two errors: the same, and `cannot find symbol`, `symbol: method getFirst()`, `location: variable free of type List<LocalDate>` |
| After changing only `intersects` to `overlaps`: plain `javac` | No error. The code compiles |
| After the same change: `javac --release 17` | One error: `getFirst()` |
| Maven (`maven.compiler.release` 17), `try-attempt.sh 1` | Two errors, at `[18,42]` and `[20,68]` |
| Either command on a JDK 17 | Both errors. The plain-`javac` contrast needs a JDK of version 21 or later; the project's command fails in the same way on every JDK |

The third row is the point. After the invented method is fixed, the code compiles on the machine it was written on and fails on the baseline. `List.getFirst()` is declared in the Java 21 `List` (since 21) and not in the Java 17 `List`, and `--release` restricts the API as well as the language level. An assistant told that the project targets Java 17 may still use it, and a developer who compiles without `--release` will not notice until the pipeline does.

### 6.2 Attempt 2, step by step

| Run | Result |
|---|---|
| Attempt 2 with its own seven generated tests | 7 pass |
| Attempt 2 with the acceptance tests as written | Does not compile: `reference to AvailabilityFinder is ambiguous` at the line `new AvailabilityFinder(null)` of `ex7`. Attempt 2 has two constructors, one taking a `List` and one taking an `AvailabilityRule`, so a bare `null` fits both |
| Attempt 2 with the acceptance tests after the one-line cast (`try-attempt.sh 2 adapted`) | 9 run, **2 fail**: `ex4_...` (expected `Optional.empty`, was `Optional[2026-10-22]`) and `ex5_...` (the same) |
| The 7 generated tests against the **accepted** finder | 6 pass and 1 fails: `theSearchWindowIsInclusiveOfTheLastDay` |

What this shows:

- The failing acceptance examples are both about the window. The loop in attempt 2 is `offset <= searchDays`, so it examines `searchDays + 1` candidates. From the 20th with a window of 2 it examines 20, 21 and 22 and returns the 22nd.
- The generated test `theSearchWindowIsInclusiveOfTheLastDay` asserts exactly that result. It was derived from the code, passes on it, and fails on correct code. It is a test of what the code does.
- The acceptance examples were independent because they were **derived from the requirement before any candidate existed**, and not from code. They were also not shared with the assistant, which let them be used a second way, to judge whether the output generalises. Sharing them would have been a legitimate choice. It would probably have produced a correct loop, and the pass would then have shown only that the assistant satisfied those examples.
- The ambiguity is a cost of the abstraction. The one-line cast in `try-attempt.sh 2 adapted` changes the type of an argument and does not change what the test asserts. Editing a test to suit the code is the wrong direction in general: here the edit is only so that the logic failure can be seen at all. The right response to the compile error, in the developer's own project, is to remove the unneeded overload.

**Size of the abstractions.** The accepted `AvailabilityFinder` is one type of 38 lines, six of them documentation. Attempt 2's production code is three types in 49 lines (`AvailabilityFinder` 30, `AvailabilityRule` 6, `AvailabilityRules` 13) with no documentation comment. The interface has one implementation, built in one place by a factory that is called once. The task has one rule.

### 6.3 The explanation of `VisitorGate.rejection`

The code and tests referred to are in the lending project at version 0.14.0.

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | The flag is checked first and the “not enabled” text is returned | Supported | The first statement of `rejection` is `if (!enabled) return Optional.of(DISABLED)` |
| 2 | Then the item is checked against CAM1 or CAM2 | Supported | `ALLOWED_ITEMS = Set.of("CAM1", "CAM2")` and the check that follows |
| 3 | Fewer than one day returns empty without asking anyone, because the policy will reject it | Supported | `if (days < 1) return Optional.empty()` and its comment; `ac4_zeroOrNegativeDaysIsRejectedWithoutReadingTheRegister` asserts that the register is not read; `VisitorReservationRules.mayRequest` requires `requestedDays >= 1` |
| 4 | The clock is read once | Supported | `oneRequestReadsTheClockOnce` |
| 5 | The exact request is asked of the source, and the request is rejected unless the record matches and is valid at that instant | Supported | `aSourceThatReturnsADifferentRequestDoesNotApprove`; `theWindowIncludesItsStartAndExcludesItsEnd` |
| 6 | The gate caches the record for later requests | **Contradicted** | The class has no field that holds a record. Its fields are the source, the clock and the flag. The file source itself reads afresh on every call (`theFileIsReadAfreshOnEveryCall`) |
| 7 | Each rejection is written to the audit log | **Contradicted** | The class has no logger and no call that writes anywhere |
| 8 | If the source throws, the gate returns the “no valid sponsor approval” rejection | **Contradicted** | The exception is not caught: `anOperationalFailureOfTheSourceIsNotCaught` asserts that the same exception object reaches the caller. This is the difference between a rejection and a failure that Chapters 12 and 13 insist on |

A corrected explanation: *`rejection` returns an empty result when the request may go on to the coordinator, and a rejection text otherwise. It checks the flag first, then the item, then returns empty for fewer than one day (the policy rejects it). Otherwise it reads the clock once, asks the source for the exact request and rejects unless the record matches and is valid at that instant. It keeps no state and writes no log. If the source throws, the exception reaches the caller; nothing is reserved.*

Note which three claims were wrong. Each describes something a gate like this could plausibly do. All three would have been believed by a reader who did not check, and the third would have produced a wrong design decision about error handling.

### 6.4 The two prompts

| Prompt | Contains | Does not contain |
|---|---|---|
| `prompt1.md` | The task sentence; the source of `LoanPeriod`; the constraints (Java 17, standard library only, no new dependencies); the output format; the scope | The acceptance examples; any statement of how the window counts |
| `prompt2.md` | The two compiler findings; the request for a small solution and tests | The acceptance examples |

Two things about them. First, `prompt1.md` says “within `searchDays` days” and nowhere says what that counts. The assistant resolved the ambiguity one way and the developer meant the other. The record shows that the requirement was rewritten afterwards. Second, `prompt2.md` asks the assistant to write tests. That request is where the shared misreading gets locked in: code and tests from the same source agree with each other.

If the acceptance examples had been in the prompt, the assistant would probably have returned a correct loop. They would still have been good requirement-based acceptance checks. What would have changed is what a pass means: it would show that the assistant satisfied those examples, not that its code is right beyond them. A sound practice is to state the **requirement** precisely, share reviewed examples if they help, add boundary cases or properties that you derived independently, and keep some of them undisclosed when you want to judge generalisation. The one thing to avoid is deriving the expected results and the implementation from the same unexamined assumption, which is what happens when an assistant writes the code and then its tests from that code.

### 6.5 The privacy example

The first prompt of `privacy-prompt.md` should not be sent. What it discloses, and what the second prompt does instead:

| In the first prompt | Why it should not be sent | In the second prompt |
|---|---|---|
| A student's name, student ID and email | Personal data about a real borrower | Keys replaced by `B1`, `B2`, `B3` |
| A configuration file with a password (invented here) | A credential. Anything that is a secret in real life must not be pasted | No configuration; the method only |
| An internal address and path | Information about your infrastructure | `<base>`, no real URL |
| 200 lines of production log with other borrowers' names | More personal data, and far more than the question needs | Three log lines, with the keys replaced |
| “What is wrong?” | No hypothesis, no limit on scope | “What are the possible causes? List them without choosing one” |

The second prompt is also better engineering: it states the symptom precisely (a timeout after 1000 ms) and asks for causes, which you will check, and not for a verdict.

### 6.6 The dependency suggestion

The constructed suggestion proposes two dependencies for a test helper that asserts the first element of a list. The status codes were read from Maven Central with `curl -sI -o /dev/null -w "%{http_code}"` on 13 October 2026. Nothing was downloaded.

| Coordinate | Request | Status |
|---|---|---|
| `org.mockito:mockito-core` | `https://repo1.maven.org/maven2/org/mockito/mockito-core/` | 200 |
| `org.mockito:mockito-junit-jupiter` | the same pattern | 200 |
| `org.mockito:mockito-fluent` | `https://repo1.maven.org/maven2/org/mockito/mockito-fluent/` | **404** |
| `org.mockito:mockito-core:5.20.0` | the version's `.pom` | 200 |
| `org.mockito:mockito-core:9.9.9` | the version's `.pom` | 404 |
| `com.google.guava:guava` | `https://repo1.maven.org/maven2/com/google/guava/guava/` | 200 |
| `com.google.guava:guava:33.0.0-jre` | the version's `.pom` | 200 |

Decisions. `mockito-fluent`: **reject**. It does not exist under that group, and a plausible name is not a reason to search for a similar one. Even a real mocking library would be wrong here, because a helper that asserts the first element of a list does not need mocking. `guava:33.0.0-jre`: **reject**. It exists, and nothing in the task needs it: `list.get(0)` and `assertEquals` do the job. A status of 200 shows only that something is published under that name. It does not show that it is the project you meant, that it is safe, or that you need it.

### 6.7 The fault experiment (summary)

The full tables are in Section 10.3.

## 7. Suggested practical solution

### 7.1 Book project, steps B1–B4

**B1. Reject attempt 1.** A good answer runs `try-attempt.sh 1` and reports two errors, then repeats by hand with `javac --release 17` and reads both errors (and, with a JDK of version 21 or later, shows that plain `javac` reports one). It lists the defects and categories: invented method (`intersects`); API newer than the baseline (`getFirst`, Java 21); self-reported verification (“I tested it with Java 17”). It says what the claim could mean: possibly that it compiled on some JDK, perhaps without `--release`; it cannot mean that it was checked under the project's settings, because the code does not compile under them.

**B2. Diagnose attempt 2.** A good answer reports 7 passing generated tests, then 2 failing acceptance examples (EX4, EX5) and the cause (`offset <= searchDays`). It names the shared misunderstanding (the window is inclusive of one extra candidate) and points at the generated test that asserts it. It says why the acceptance examples were independent (derived first, from the requirement, and not from the code; they were also kept back, so that they could judge generalisation). It reports that the generated tests fail one test against the accepted finder. It notes the overload ambiguity and the unneeded abstraction.

**B3. Make the tests bite.** A good answer applies three faults, for example `offset < searchDays - 1`, `start.plusDays(days - 1)` and `allMatch`, predicts the failing examples before running (Section 10.3 lists what happened), and finds one that survives. The survivors in the experiment are equivalent faults; a good answer says why no test of the exception type can detect them.

**B4. Fill in a record.** A good answer uses all eight headings, keeps rejected output, names at least one check that is independent of the assistant and at least one limit, and passes `check-record.sh`. A weak answer says “reviewed and verified” under Verification.

### 7.2 Book project, optional steps B5–B7

**B5. Repeat with a live assistant.** There is no model answer, because the output differs. A good answer keeps every attempt, compiles under `--release 17`, runs the acceptance examples, and names which failure modes from Section 15.6 appeared. An assistant that gets it right the first time is a valid result: record that and the checks that showed it.

**B6. Verify two dependencies.** See Section 6.6.

**B7. Swap and find.** A good answer lists the flaws it found, the flaws it missed and why. Missing a flaw of the invented-method kind (it looked like the real name) is common and instructive.

### 7.3 Team project, steps T1–T3 (and T4)

These are not model answers, because the task is your team's. A good answer shows:

- **T1:** a requirement stated precisely, including how any count or window is defined; acceptance examples with inputs and expected results, on the boundaries; the constraints (language level, no new dependencies) and the scope; and a stated decision about what stays out of the prompt.
- **T2:** every attempt kept, the project's own build and compiler settings used, and the acceptance examples run against each attempt. If no live assistant was used, the constructed or classmate-written candidate and the routes of Section 15.9.
- **T3:** a record with every heading, the independent checks named, the limits stated, the record checked by the script and reviewed by a person.
- **T4:** a short team note that follows the module leader's rules and says what is shared with tools and what is not, how AI-assisted work is disclosed and recorded, and who reviews it.

A weak answer derives the examples from the candidate code, treats a pass on examples the assistant has seen as proof of behaviour beyond them, accepts a claim of testing, or keeps only the final version. A sound answer that **shares** reviewed examples is not weak for that reason: it should then add independently derived cases.

## 8. Intentionally flawed alternatives

These fragments are **diagnostic alternatives**, not files to compile.

### 8.1 “Reviewed by another assistant”

```markdown
## Verification
Reviewed by a second assistant, which found no issues. All tests pass.
```

A second candidate opinion with the same weaknesses is not verification, and “all tests pass” does not say whose tests. Name the independent checks and the commands.

### 8.2 Accepting it because it compiled

```text
$ javac AvailabilityFinder.java      # JDK 24, no --release
$ echo $?
0
```

The project compiles with `--release 17`. A call that exists only from Java 21 compiled here and fails there.

### 8.3 Tests derived from the implementation

```java
// "Generated from the code above": it asserts what the code does.
@Test void theSearchWindowIsInclusiveOfTheLastDay() {
    assertEquals(Optional.of(oct(22)), finder.earliestStart(oct(20), 2, 2));
}
```

The name states a requirement that nobody wrote. Examples come from the requirement.

### 8.4 A record that says nothing

```markdown
## Task
Used AI for the finder.
## Verification
Reviewed and verified.
## Limits
None.
```

It passes the heading check and tells a reader nothing. The checker looks only for structure.

### 8.5 A prompt that carries the requirement and the secrets

```text
Fix it so it matches the spec. Here is the spec (confidential) and our production config,
including the directory password.
```

The requirement belongs in your own documents, stated once; the assistant gets the minimum. Secrets do not go in a prompt.

## 9. Review answers and transfer solution

### 9.1 Concept answers

**1. “I tested it with Java 17.”** It is a sentence from a system that did not run your build, and it names no command or result. Two checks that are evidence: compile and test with the project's own command (`mvn --batch-mode test`, which sets `release` 17) and read the result; and run `javac --release 17` on the file.

**2. Function and tests that pass.** Tests derived from the code agree with it, including where it is wrong: the generated test `theSearchWindowIsInclusiveOfTheLastDay` passes on attempt 2 and fails on correct code. Examples written from the requirement beforehand would show it, and a fault experiment on the tests would show that they miss the window fault.

**3. `--release`.** `--source` and `--target` set the language level and the class-file target. `--release` also restricts the **API** to the one that release defines, and cannot be combined with `--source` or `--target`. On a JDK newer than the baseline, only `--release 17` makes `getFirst()` a compile error under Java 17. On a JDK 17 itself, every compile command rejects it, because the API is not there.

**4. A dependency that exists.** You have learned that something is published under that coordinate. You have not learned that it is the library you meant, that it is safe or licensed for your use, that the version suits your build, or that you need it.

### 9.2 Applied diagnosis answers

**5. “The method caches the result.”** Options: read the class for a field that holds a result (there is none); look for a test that depends on caching, and for a test that depends on its absence (`theFileIsReadAfreshOnEveryCall`); trace two calls by hand. Write down the claim, the evidence and the verdict: contradicted, with the line or test.

**6. A patch of four claims with one failing test.** Apply the claims one at a time in scratch copies and run the suite after each; the failing claim is the one whose copy fails. The patch's summary is a claim of the same kind as the code, and cannot tell you which of its own claims was the cause.

### 9.3 Transfer solution

| Item | Content |
|---|---|
| Requirement and examples | The validation rule stated precisely (what counts as a missing value, which ranges, what happens to a bad record). Examples on the boundaries, with synthetic records. Written first |
| Context to share | The function signature, the record type, the constraints. Synthetic records only |
| Not to share | Real records, keys, tokens, the registry's address, any real model or customer identifiers |
| Independent checks | The compiler under the project's settings; the examples; a fault experiment on the tests; a trace on selected inputs |
| Dependencies | Look up any suggested library; ask whether the standard library already does it; pin the version |
| Record | Task, tool and model, context, each attempt, decision, changes, verification, limits |
| What it does not show about the model | Nothing here evaluates the model: its accuracy, fairness, drift or behaviour on data unlike the synthetic data. Validating the data a model receives is not validating the model |
| AI in the product | The model itself is a component with its own failure modes, contracts and tests. It is a different topic from using an assistant to write the code. In this book it is the borrower directory: Chapter 6 (contract), 7 (doubles), 8 (adapter), 13 (timeout and failure policy) |

### 9.4 Quiz and revision pointers

None. This chapter adds no assessed content and creates no rubric. Whether and how AI tools may be used in assessments is the module leader's decision.

## 10. Instructor notes and verification

### 10.1 Suggested demonstration and review

Compile attempt 1 with `javac --release 17`, and, if a JDK of version 21 or later is available, with plain `javac`, and ask why the results differ. With only a JDK 17 the two commands agree, which is itself worth discussing. Run attempt 2 against its own tests, then against the acceptance examples, and ask the class to find the shared misunderstanding before showing the loop. Ask which of the three wrong claims in the `VisitorGate` explanation they would have believed without checking, and why.

Do not let the review turn into a debate about whether students should use assistants. The rules are the module leader's. The skill is the same either way: to check a candidate against evidence it did not write.

Where students have no access to a live service, every activity works from the constructed output. Where they do, ask for the **rejected** attempts as well as the accepted one: the record of a rejection is the evidence that someone checked.

### 10.2 Verification record

This version was verified offline on Windows 11 with **Maven 3.9.11 and JDK 24.0.2**, compiling with `--release 17`, against the pinned versions (JUnit Jupiter 5.13.4, Compiler Plugin 3.14.1, Surefire 3.5.4) in a local repository that already held them. No JDK 17 was available. No live assistant was used for any of the output in this chapter: all of it is constructed.

**Reconstruction.** The 21 listings of this file were extracted programmatically into a fresh directory. The result matched the working lab file for file (byte for byte). `mvn --batch-mode test` on that reconstruction exited 0 with 9 invocations; the four `try-attempt.sh` runs and `check-record.sh` gave the results in the table below, including the new failure when only the template exists. This is the reconstruction of Version 1.1.


| Check | Observed result |
|---|---|
| `mvn --batch-mode test` in the lab | Exit 0; 9 invocations, 0 failures, errors or skipped |
| `try-attempt.sh 1` | `BUILD FAILURE`: two `cannot find symbol` errors, at `[18,42]` and `[20,68]` |
| Attempt 1 by hand | `javac`: one error; `javac --release 17`: two; after fixing the invented method only, `javac` passes and `javac --release 17` fails on `getFirst()` |
| `try-attempt.sh 2 generated` | 7 invocations, 0 failures |
| `try-attempt.sh 2` | `BUILD FAILURE`: ambiguous reference at the `ex7` line |
| `try-attempt.sh 2 adapted` | 9 run, 2 failures: `ex4_...` and `ex5_...` |
| The 7 generated tests on the accepted finder | 6 pass, 1 fails (`theSearchWindowIsInclusiveOfTheLastDay`) |
| `check-record.sh` | `RECORD CHECK PASSED` on the filled record |
| `check-record.sh` where only the template exists | Exit 1: `FAIL no assistance record to check...` and `RECORD CHECK FAILED: nothing was checked`. Version 1.0 exited 0 with `RECORD CHECK PASSED` in that case |
| `check-record.sh` on three damaged copies | A record with a heading removed: `FAIL ... missing heading 'Limits'`. An empty heading: `FAIL ... heading 'Limits' is empty`. A heading renamed (`Decisions`): `FAIL ... missing heading 'Decision'`. All three caught |
| Dependency status codes | Section 6.6, read on 13 October 2026 with `curl -sI`; no artefact downloaded |
| `javac --release 17 -Xlint:all` | The accepted sources compiled with the same flag and reported no warnings (checked through Maven's compiler plugin) |
| Mermaid | Both figures of the chapter rendered with Mermaid 10.9.1 in the browser pane |
| Web sources | Eight online sources were opened on 13 October 2026 |
| Java 17 runtime, as reported by the review | An independent review of Chapters 12 to 15 reported running the lab reconstructed from the Version 1.0 companion on OpenJDK 17.0.20 and Maven 3.9.11: 9 acceptance tests pass; `try-attempt.sh 1` fails with two unresolved symbols; `try-attempt.sh 2 generated` passes 7; `try-attempt.sh 2` fails with the ambiguous constructor; `try-attempt.sh 2 adapted` runs 9 with 2 failures; `check-record.sh` passes on the filled record. These results are the review's and I have not reproduced them. They cover the lab only. The ten-fault experiment was not rerun on Java 17 |
| Live assistant, hosted CI, independent review of the chapter's teaching | Not used, not run, not performed |

### 10.3 Do the tests detect faults?

Ten single faults were applied one at a time to the accepted `AvailabilityFinder` in a scratch copy and run with `mvn test`, once against the nine acceptance examples and once against the seven generated tests (of which the one that fails on correct code is excluded from the comparison, since it already fails).

| Fault | Acceptance examples | Generated tests |
|---|---|---|
| The window loop runs one step too far (`offset <= searchDays`), which is attempt 2's own fault | Caught: EX4, EX5 | **Survived** |
| The window loop stops one step early | Caught: EX3, EX5, EX6 | **Survived** |
| A stay of `days` occupies `days - 1` days | Caught: EX2, EX9 | Caught: `returnsEmptyWhenTheWindowIsFullyBooked`, `skipsALongStayThatDoesNotFit` |
| The search skips `from` itself | Caught: EX3, EX4, EX5, EX6 | Caught: `returnsFromWhenNothingIsBooked` |
| `noneMatch` becomes `allMatch` | Caught: EX1, EX2, EX3, EX5, EX6, EX8, EX9 | Caught: three tests |
| Overlap treats an end date as occupied (inclusive end) | Caught: EX1, EX2, EX5, EX6, EX8 | Caught: `findsTheFirstFreeDayAfterABooking`, `skipsALongStayThatDoesNotFit` |
| `days = 0` is accepted | **Survived** (equivalent) | **Survived** |
| `searchDays = 0` is accepted | Caught: EX7 | **Survived** |
| The caller's list is kept, not copied | Caught: EX8 | **Survived** |
| A null `from` is not rejected early | **Survived** (equivalent) | **Survived** |

Totals: the acceptance examples caught 8 of 10; the generated tests caught 4 of 10. The two faults that survive the acceptance examples are **equivalent** to the correct code as far as the examples can tell. With `days = 0` the finder's own check is gone, but `LoanPeriod`'s constructor throws `IllegalArgumentException` on a period that does not begin before it ends. With a null `from` the early check is gone, but `from.plusDays` throws `NullPointerException`. Each example asserts only the exception type. The faults change where the exception is raised and not what a caller sees, which is the same kind of surviving equivalent mutant as in Chapters 7 and 11.

Notice the first row. The fault that attempt 2 actually contained, a window one step too long, is the one the generated tests cannot catch, because they were derived from code that contains it. The experiment is ten faults chosen by the author on one small class. It says nothing about assistants or tests in general.

The results establish the selected behaviours on the supplied inputs, in the stated environment. They do not establish how a real assistant would behave on this task, behaviour on a Java 17 runtime, or that the acceptance examples are the right examples.

## References

The online references of the student chapter (sources 1–8) were opened on 13 October 2026; see the chapter for the source context.

1. GitHub Docs, [Application card: GitHub Copilot inline suggestions](https://docs.github.com/en/copilot/responsible-use/inline-suggestions).
2. Oracle, [`List` (Java SE 21)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html).
3. Oracle, [`List` (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/List.html).
4. Oracle, [javac (Java SE 17)](https://docs.oracle.com/en/java/javase/17/docs/specs/man/javac.html).
5. Apache Maven, [maven-compiler-plugin: compile mojo](https://maven.apache.org/plugins/maven-compiler-plugin/compile-mojo.html).
6. OWASP, [Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/).
7. Spracklen, J. and others, [We Have a Package for You!](https://arxiv.org/abs/2406.10279), arXiv 2406.10279.
8. Maven Central, [`org/mockito/`](https://repo1.maven.org/maven2/org/mockito/).
