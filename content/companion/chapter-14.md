---
title: "Chapter 14 Companion: Code, Explanations and Solutions"
weight: 140
description: "Code explanations and solutions for Chapter 14 Companion: Code, Explanations and Solutions."
---

*Responding to Change and Handing Over*  
*OO Development and Agile Practices*

## 1. Scope and execution

This file accompanies Chapter 14, Responding to Change and Handing Over. It contains the handover version of the visiting-researcher project (0.14.0): a requirements-to-evidence table with a test that keeps it true, a reproducible demonstration, a script that follows the handover in a fresh copy, the handover documents, a decision record about the flag, the prepared and tested removal of that flag, the AI activity files, model solutions, the experiments behind the chapter's figures and teaching notes.

**No production code changed.** Every file under `src/main` is byte for byte as in the Chapter 13 checkpoint. What changed is tests, scripts, documents and the version.

**Input checkpoint.** The starting point is the Chapter 13 checkpoint, which is the Chapter 10 companion, the new and changed files of the Chapter 11 companion and the new and changed files of the Chapter 13 companion. To keep verified listings from being copied again, this file lists **only the files that are new or changed**. Every other file is exactly as in those companions.

### 1.1 Reconstruct the checkpoint

1. Create the directory `after`. Save every listing of the Chapter 10 companion, then the new and changed listings of the Chapter 11 companion, then those of the Chapter 13 companion, applying the hunks of the Chapter 13 companion with `patch -p1` from inside `after`.
2. Save every listing in Sections 3 and 4 of this file at its path. Where a path already exists (`README.md`, `scripts/pipeline.sh`, `scripts/simulate-release.sh`), the listing here replaces it. Apply the hunk of Section 3.2 to `pom.xml` with `patch -p1`.
3. The files under `ai-activity/` and `rehearsal/` are not compiled by Maven.

Use a full Java 17 JDK, including the `jdk.jdeps` module, and Maven 3.9.11. The pinned versions are unchanged (JUnit Jupiter 5.13.4, Mockito 5.20.0, Compiler Plugin 3.14.1, Surefire 3.5.4); only the project version becomes 0.14.0. Then, from inside `after`:

```bash
mvn --batch-mode verify
bash scripts/pipeline.sh
bash scripts/demo.sh
bash scripts/handover-check.sh
```

### 1.2 Expected output

`mvn --batch-mode verify` ends with `Tests run: 235, Failures: 0, Errors: 0, Skipped: 0` and `BUILD SUCCESS`. The 235 are the 232 of Chapter 13 and the three of `TraceabilityTest`. `scripts/pipeline.sh` ends with `PIPELINE PASSED`, with 206, 26 and 3 invocations in stages 2, 3 and 4. `scripts/demo.sh` prints:

```text
== visitors disabled ==
Visitors enabled: false
Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Visitor V1: Rejected: visitor reservations are not enabled.
Visitor V2: Rejected: visitor reservations are not enabled.
Unknown U9: Rejected: borrower not found or inactive.
Outage BROKEN: Unavailable: Borrower directory unavailable
Reservations: 1
Notices: 1
== visitors enabled ==
Visitors enabled: true
Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).
Visitor V1: Confirmed: R2 for V1 on CAM2 [2026-10-20, 2026-10-22).
Visitor V2: Rejected: no valid sponsor approval.
Unknown U9: Rejected: borrower not found or inactive.
Outage BROKEN: Unavailable: Borrower directory unavailable
Reservations: 2
Notices: 2
```

(Maven and the mocking library print `WARNING` lines on a recent JDK; they are not errors. The Maven warnings appear before the demonstration lines.) `scripts/handover-check.sh` ends with `HANDOVER CHECK PASSED` after twelve `ok` lines.

### 1.3 Run the traceability check alone

```bash
mvn --batch-mode test -Dtest=TraceabilityTest
```

Expected: `Tests run: 3, Failures: 0, Errors: 0, Skipped: 0`.

## 2. Design map

### 2.1 What is new or changed

| Path | Status | Purpose |
|---|---|---|
| `src/test/java/edu/se506/lending/docs/TraceabilityTest.java` | New | Fails the build if the requirements table names a test or class that is gone, or an acceptance example loses its row |
| `src/test/java/edu/se506/lending/integration/DemoRun.java` | New | Starts the local directory stub and runs the system twice, for `scripts/demo.sh` |
| `scripts/demo.sh` | New | Compiles and runs `DemoRun`; one command, no other setup |
| `scripts/handover-check.sh` | New | Follows `docs/HANDOVER.md` in a fresh copy and compares the results |
| `scripts/pipeline.sh`, `scripts/simulate-release.sh` | Changed | A clear message and a non-zero exit when Maven is missing |
| `docs/HANDOVER.md` | New | The handover bundle |
| `docs/REQUIREMENTS-TO-EVIDENCE.md` | New | Ten contract clauses and eighteen acceptance examples traced to a deciding class and a test, and five known gaps |
| `docs/KNOWN-ISSUES.md` | New | Fourteen known issues, each with a decision |
| `docs/RELEASE-NOTES-0.14.0.md` | New | What changed in this version |
| `docs/ADR-014-flag-handover.md` | New | Decision: keep the flag, rehearse the removal |
| `rehearsal/remove-visitor-flag.patch` | New | The prepared, tested removal of the visitor flag. Not applied |
| `ai-activity/README-draft.md`, `ai-activity/README-corrected.md` | New | The AI-drafted README and the corrected one |
| `README.md`, `pom.xml` | Changed | Handover pointer; version 0.14.0 |

### 2.2 Test counts by stage

| Stage | Chapter 13 | Chapter 14 |
|---|---|---|
| 2 Unit tests and architecture checks | 203 | 206 (adds `TraceabilityTest`, 3) |
| 3 Integration | 26 | 26 |
| 4 End-to-end | 3 | 3 |
| Total | 232 | 235 |

### 2.3 What `TraceabilityTest` checks, and what it does not

| Check | Method |
|---|---|
| Every test named in the Evidence column exists as a method | `everyTestNamedInTheTableStillExists` (also requires at least 29 named tests, so that a deleted row cannot hide) |
| Every class named in the Decided by column exists under `src/main` | `everyClassNamedAsDecidingStillExists` |
| AC1 to AC18 each have exactly one row, and every `ac<N>_` test in `VisitorAcceptanceTest` appears in the table | `everyAcceptanceExampleHasExactlyOneRowAndEveryAcceptanceTestIsInTheTable` |
| That a named test is the right evidence for its requirement | **Not checked.** A reviewer decides |

## 3. New and changed listings: build, scripts, documents

### 3.1 `after/README.md`

````markdown
# Chapter 14 checkpoint: handover version 0.14.0

Start with `docs/HANDOVER.md`: what this is, what you need, how to set it up, how to see it work, what is known to be missing.

Use a full Java 17 JDK and Maven 3.9.11. The JDK must include jdk.jdeps for the compiled dependency tests. From this directory:

```bash
mvn --batch-mode verify
bash scripts/pipeline.sh
bash scripts/demo.sh
```

The expected results, including the number of test invocations in each pipeline stage, are in `docs/HANDOVER.md`, which `scripts/handover-check.sh` checks in a fresh copy. `TraceabilityTest` fails the build if `docs/REQUIREMENTS-TO-EVIDENCE.md` names a test or class that no longer exists.

Version 0.14.0 changes no production behaviour. It adds the demonstration (`scripts/demo.sh`), the handover documents in `docs/`, a script that follows the handover in a fresh copy (`scripts/handover-check.sh`) and the rehearsed, not applied, removal of the visitor flag (`rehearsal/remove-visitor-flag.patch`, decided in `docs/ADR-014-flag-handover.md`). Known issues, with decisions, are in `docs/KNOWN-ISSUES.md`.

The visitor flag `lending.visitors` defaults to false. `scripts/simulate-release.sh` is a SIMULATION of delivery. `.github/workflows/pipeline.yml` has never run. No Java 17 run, hosted CI run or independent review is claimed.

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

### 3.2 `after/pom.xml`

Change the project version from 0.13.1 to 0.14.0 and nothing else. The hunk is an edit to the Chapter 13 POM:

```diff
--- chapter13/pom.xml
+++ chapter14/pom.xml
@@ -4,7 +4,7 @@
   <modelVersion>4.0.0</modelVersion>
   <groupId>edu.se506</groupId>
   <artifactId>equipment-lending</artifactId>
-  <version>0.13.1</version>
+  <version>0.14.0</version>
   <properties>
     <maven.compiler.release>17</maven.compiler.release>
     <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
```

### 3.3 `after/scripts/pipeline.sh`

```bash
#!/usr/bin/env bash
# A modest delivery pipeline run on one machine. Each stage must pass before the next one starts,
# and the first failing stage stops the run with a non-zero status. CHAPTER_MVN names the Maven
# command (default: mvn); CHAPTER_M2 optionally names a local Maven repository.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

MVN="${CHAPTER_MVN:-mvn}"
if ! command -v "$MVN" >/dev/null 2>&1 && [ ! -f "$MVN" ]; then
  echo "Maven was not found (looked for: $MVN). Install Maven 3.9.11, or set CHAPTER_MVN to its full path." >&2
  exit 2
fi
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

### 3.4 `after/scripts/simulate-release.sh`

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
if ! command -v "$MVN" >/dev/null 2>&1 && [ ! -f "$MVN" ]; then
  echo "Maven was not found (looked for: $MVN). Install Maven 3.9.11, or set CHAPTER_MVN to its full path." >&2
  exit 2
fi
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

### 3.5 `after/scripts/demo.sh`

```bash
#!/usr/bin/env bash
# A reproducible demonstration with no other setup: compile, start the local directory stub inside
# one process, and run the system twice (visitors disabled, then enabled). CHAPTER_MVN names the
# Maven command (default: mvn); CHAPTER_M2 optionally names a local Maven repository.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

MVN="${CHAPTER_MVN:-mvn}"
if ! command -v "$MVN" >/dev/null 2>&1 && [ ! -f "$MVN" ]; then
  echo "Maven was not found (looked for: $MVN). Install Maven 3.9.11, or set CHAPTER_MVN to its full path." >&2
  exit 2
fi
if ! command -v java >/dev/null 2>&1; then
  echo "Java was not found. Install a full Java 17 JDK and make sure java is on the PATH." >&2
  exit 2
fi
ARGS=(--batch-mode -q)
if [ -n "${CHAPTER_M2:-}" ]; then
  ARGS+=("-Dmaven.repo.local=${CHAPTER_M2}")
fi

"$MVN" "${ARGS[@]}" test-compile

SEP=":"
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) SEP=";" ;;
esac
java -cp "target/classes${SEP}target/test-classes" edu.se506.lending.integration.DemoRun
```

### 3.6 `after/scripts/handover-check.sh`

```bash
#!/usr/bin/env bash
# Follows docs/HANDOVER.md in a fresh copy of the project, so that a stale or missing step shows up
# here and not on the day a new reader tries it. It copies the project without build output into a
# new folder, runs the pipeline and the demonstration there, and compares what they print with what
# HANDOVER.md promises. The expected figures below must be kept in step with HANDOVER.md.
#
# CHAPTER_MVN names the Maven command (default: mvn); CHAPTER_M2 optionally names a local Maven
# repository. Both are passed on to the scripts it runs.
set -euo pipefail

EXPECT_UNIT=206          # stage 2 of the pipeline
EXPECT_INTEGRATION=26    # stage 3
EXPECT_E2E=3             # stage 4
EXPECT_TOTAL=$((EXPECT_UNIT + EXPECT_INTEGRATION + EXPECT_E2E))

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
( cd "$SRC" && tar cf - --exclude=./target --exclude=./build --exclude=./.git . ) | ( cd "$WORK" && tar xf - )
cd "$WORK"

failures=0
expect() {   # expect <file> <fixed text> <what it shows>
  if grep -qF -- "$2" "$1"; then
    echo "ok   $3"
  else
    echo "FAIL $3 (expected to find: $2)"
    failures=$((failures + 1))
  fi
}

echo "--- following HANDOVER.md in ${WORK}"
if bash scripts/pipeline.sh > pipeline.out 2>&1; then echo "ok   the pipeline exited 0"; else echo "FAIL the pipeline did not exit 0"; failures=$((failures + 1)); fi
expect pipeline.out "PIPELINE PASSED" "the pipeline reports PIPELINE PASSED"
expect pipeline.out "Tests run: ${EXPECT_UNIT}, Failures: 0, Errors: 0, Skipped: 0" "stage 2 ran ${EXPECT_UNIT} invocations"
expect pipeline.out "Tests run: ${EXPECT_INTEGRATION}, Failures: 0, Errors: 0, Skipped: 0" "stage 3 ran ${EXPECT_INTEGRATION} invocations"
expect pipeline.out "Tests run: ${EXPECT_E2E}, Failures: 0, Errors: 0, Skipped: 0" "stage 4 ran ${EXPECT_E2E} invocations"

expect docs/HANDOVER.md "Tests run: ${EXPECT_TOTAL}, Failures: 0" "HANDOVER.md promises ${EXPECT_TOTAL} invocations in total"
expect docs/HANDOVER.md "Stage 2 runs ${EXPECT_UNIT} invocations, stage 3 runs ${EXPECT_INTEGRATION} and stage 4 runs ${EXPECT_E2E}." "HANDOVER.md promises the stage counts"

if bash scripts/demo.sh > demo.out 2>&1; then echo "ok   the demonstration exited 0"; else echo "FAIL the demonstration did not exit 0"; failures=$((failures + 1)); fi
expect demo.out "Visitor V1: Rejected: visitor reservations are not enabled." "the disabled run rejects a visitor"
expect demo.out "Visitor V1: Confirmed: R2 for V1 on CAM2 [2026-10-20, 2026-10-22)." "the enabled run confirms an approved visitor"
expect demo.out "Visitor V2: Rejected: no valid sponsor approval." "the enabled run rejects an unapproved visitor"
expect demo.out "Outage BROKEN: Unavailable: Borrower directory unavailable" "an outage is reported as unavailable"

if [ "$failures" -eq 0 ]; then
  echo "HANDOVER CHECK PASSED"
else
  echo "HANDOVER CHECK FAILED: ${failures} problem(s)"
  exit 1
fi
```

### 3.7 `after/docs/HANDOVER.md`

````markdown
# Handover: Campus Equipment Lending System, version 0.14.0

This is the handover bundle for the book project. It is written for a person who has not seen the project before and has about an hour. A team applies the same headings to its own project.

## 1. What this is

A small Java application that lets borrowers reserve campus equipment. It decides reservations by borrower category (student, staff, visiting researcher), records loans and returns, and prints an overdue report. Visiting researchers are supported by a change request, CR-12, which is a **teaching contract** and not an institutional policy. The visitor behaviour is behind one flag that is **off by default**.

It is an in-memory teaching system: no real database, no real borrower directory and no real sponsor-approval service. The directory and the approval register are controlled stand-ins.

## 2. What you need

| Need | Detail |
|---|---|
| A full Java 17 JDK | It must include the `jdk.jdeps` module, which two architecture tests use. The build compiles with `--release 17`. The checks were run with `--release 17` on a newer JDK; a Java 17 runtime run has not been made. |
| Maven 3.9.11 | The pinned dependency versions are in `pom.xml`. The first build downloads them. |
| A POSIX shell | Git Bash on Windows is enough. The scripts are written for `bash`. |
| Network access | Only for the first build, to fetch dependencies. |

## 3. Set up and check that it works

First check the tools:

```bash
java -version
mvn -version
```

You should see Java 17 or later and Maven 3.9.x. If `mvn` is not found, install Maven, or set `CHAPTER_MVN` to the full path of the Maven command for the scripts (for example `export CHAPTER_MVN=/path/to/apache-maven-3.9.11/bin/mvn`). The scripts print a message and stop if Maven or Java is missing. The commands below that start with `mvn` need Maven on the PATH.

Then, from the project directory (the one that contains `pom.xml`):

```bash
mvn --batch-mode verify
```

Expected: `BUILD SUCCESS` and `Tests run: 235, Failures: 0, Errors: 0, Skipped: 0`.

To run the same checks as the delivery pipeline, stage by stage, and stop at the first failure:

```bash
bash scripts/pipeline.sh
```

Expected: five stages, each ending `PASSED`, then `PIPELINE PASSED`. Stage 2 runs 206 invocations, stage 3 runs 26 and stage 4 runs 3.

If your Maven command is not `mvn`, or you keep dependencies in a separate folder, set `CHAPTER_MVN` and `CHAPTER_M2` before running a script; the scripts say so in their first lines.

**Things you may see that are not errors.** On a recent JDK Maven 3.9.11 prints `WARNING` lines about `sun.misc.Unsafe`, and the mocking library prints a warning that a Java agent was loaded dynamically. The build still ends with `BUILD SUCCESS`. Read the last lines of the output, not the first. A folder name with spaces in it is fine.

**If something fails.** A failing stage prints its name and stops the pipeline. Read the name of the first failing test before the stack trace. If the first build fails while downloading dependencies, check your network and try again. If `TraceabilityTest` fails, a document and the code disagree: read its message, which names the missing test or class.

## 4. See it work

```bash
bash scripts/demo.sh
```

This compiles the project, starts the local directory stub inside one process, and runs the system twice. With visitors disabled, visitor requests are rejected with `visitor reservations are not enabled`. With visitors enabled, the visitor V1 with a matching approval is confirmed, V2 with none is rejected, and an unavailable directory is reported as unavailable and not as a missing borrower. The clock is fixed so that the sample approval is always valid.

## 5. How it is organised

| Package | Role |
|---|---|
| `domain` | Borrowers, reservations, loans, borrowing policies, approval records |
| `application` | Use cases: reserving, loans, the visitor gate, ports for the directory, approvals and notices |
| `infrastructure` | Adapters: the directory client and adapter, the approval file, notices, in-memory storage |
| `bootstrap` | Wiring and the runnable demonstrations |
| `legacy` | The old overdue report, isolated; production code does not depend on it |

The architecture tests (`DependencyRulesTest`) fail the build if a dependency points the wrong way. The decisions behind the structure are in `docs/ADR-010-application-structure.md`, `docs/ADR-011-legacy-overdue-report.md`, `docs/ADR-013-visiting-researchers.md` and `docs/ADR-014-flag-handover.md`.

## 6. The visitor flag

The flag `lending.visitors` defaults to `false`. To change it for the demonstration program, pass `-Dlending.visitors=true`. A mistyped value means `false`, which is the safe direction; the program prints the effective setting on its first line. To stop new visitor reservations, turn the flag off. That does not remove reservations that already exist. The decision about removing the flag is in `docs/ADR-014-flag-handover.md`.

## 7. Requirements to evidence

`docs/REQUIREMENTS-TO-EVIDENCE.md` traces the ten contract clauses and the eighteen acceptance examples to the class that decides each and the test that checks it, and lists five known gaps. `TraceabilityTest` fails the build if a named test or class disappears.

## 8. Known limitations

`docs/KNOWN-ISSUES.md` is the full list, with what was decided and why. In brief:

- The directory and the approval register are stand-ins. Nothing here was run against a real service.
- Two writers of the register, or simultaneous requests, were not considered.
- A late visitor is charged at the rate of the report's "any other kind" rule (suspected defect SD-11-1). The count rule counts every retained reservation, including returned ones (SD-12). Both are unresolved and need an owner's decision.
- No Java 17 run, and no hosted CI run, has been made. The file `.github/workflows/pipeline.yml` has never run.
- `scripts/simulate-release.sh` is a simulation of delivery. Nothing is deployed anywhere.

## 9. Where things are

| Path | What |
|---|---|
| `src/main/java` | Production code |
| `src/test/java` | Tests: unit, integration (tag `integration`), end-to-end (tag `e2e`), and the traceability check |
| `scripts/pipeline.sh` | The five-stage pipeline |
| `scripts/demo.sh` | The demonstration |
| `scripts/simulate-release.sh` | Simulated delivery and rollback |
| `scripts/handover-check.sh` | Copies the project to a new folder and follows this document |
| `docs/` | Decision records, requirements to evidence, known issues, release notes, this file |
| `tools/PackageMetrics.java` | Package coupling and stability figures; see the Chapter 10 notes |
| `stages/`, `probe/`, `ai-activity/`, `rehearsal/` | Teaching material outside the build |

## 10. Demonstration outline (about ten minutes)

1. The problem in one sentence, and what changed in this version (one minute).
2. Run `bash scripts/pipeline.sh` and point at the stage counts (two minutes; start it before you begin talking).
3. Run `bash scripts/demo.sh` and read the two outputs side by side (three minutes).
4. Open `docs/REQUIREMENTS-TO-EVIDENCE.md` and follow one row from requirement to test to stage (two minutes).
5. State what is not shown, from section 8, and the next action (two minutes).

The timings are a suggestion. Your instructions decide the length and the format of your own demonstration.
````

### 3.8 `after/docs/REQUIREMENTS-TO-EVIDENCE.md`

```markdown
# Requirements to evidence: visiting-researcher reservations (CR-12)

This table traces each requirement and acceptance example to the code that decides it and the test that checks it. It is checked by `TraceabilityTest`: every test named in the *Evidence* column must exist, every acceptance example AC1 to AC18 must have exactly one row, and every class named in the *Decided by* column must exist. The test checks that names exist. It does not check that the named test is the right one: a reviewer does that.

The stage is the pipeline stage that runs the evidence (`scripts/pipeline.sh`): 2 is unit tests and architecture checks, 3 is integration tests, 4 is end-to-end journeys.

CR-12 is a teaching contract. It is not an institutional borrowing policy.

## Contract clauses

| ID | Requirement | Decided by | Evidence | Stage |
|---|---|---|---|---|
| C1 | A visitor is recognised through the borrower directory, with the kind code `V` | `LegacyDirectoryAdapter`, `DirectoryReservationService` | `DirectoryOutageIntegrationTest.aVisitorIsServedThroughTheRealDirectoryAndTheRealApprovalFile` | 3 |
| C2 | Only CAM1 and CAM2 may be requested | `VisitorGate` | `VisitorGateTest.anItemOutsideTheAllowlistIsRejectedWithoutReadingTheSource` | 2 |
| C3 | One to three days, and no more than three retained reservations | `VisitorReservationRules` | `VisitorRulesTest.countAndDurationBoundaries` | 2 |
| C4 | The approval matches the borrower, the item and the exact period | `ApprovalRecord` | `VisitorRulesTest.aRecordMatchesOnlyTheExactBorrowerItemAndPeriod` | 2 |
| C5 | The approval is valid at the request instant (start inclusive, end exclusive) | `ApprovalRecord`, `VisitorGate` | `VisitorGateTest.theWindowIncludesItsStartAndExcludesItsEnd` | 2 |
| C6 | A missing, denied, mismatched or expired approval creates no reservation and sends no notice | `VisitorGate`, `DirectoryReservationService` | `VisitorAcceptanceTest.ac7_anApprovalForAnotherBorrowerItemOrPeriodDoesNotAuthorise` | 2 |
| C7 | An unreadable or malformed register is a failure, not a rejection | `FileApprovalSource` | `FileApprovalSourceIntegrationTest.oneBadRowRejectsTheWholeRegisterEvenWhenTheRequestMatchesAGoodRow` | 3 |
| C8 | An unreachable or slow directory is a failure, never "not found" | `HttpLegacyDirectoryClient`, `LegacyDirectoryAdapter` | `DirectoryOutageIntegrationTest.aServerErrorIsAnOutageNotANotFoundAndIsNotRetried` `DirectoryOutageIntegrationTest.aStalledBodyIsAFailureWithinTheOverallWait` | 3 |
| C9 | The visitor behaviour is behind one flag that defaults to off | `VisitorGate`, `Chapter13Demo` | `Chapter13JourneyE2ETest.withTheFlagOffVisitorsAreRefusedAndEveryoneElseIsServed` | 4 |
| C10 | Student and staff behaviour is unchanged | `ReservationCoordinator` | `VisitorAcceptanceTest.ac13_studentAndStaffBehaviourIsUnchangedUnderEitherSettingAndNeverReadsTheRegister` | 2 |

## Acceptance examples

| ID | Example | Decided by | Evidence | Stage |
|---|---|---|---|---|
| AC1 | CAM1, two days, matching approved record valid at request time | `VisitorGate`, `ReservationCoordinator` | `VisitorAcceptanceTest.ac1_aVisitorWithAMatchingApprovalReservesCam1ForTwoDays` | 2 |
| AC2 | CAM2, three days, with its own record | `VisitorReservationRules` | `VisitorAcceptanceTest.ac2_cam2ForThreeDaysNeedsItsOwnRecordAndIsAllowed` | 2 |
| AC3 | Four days is rejected | `VisitorReservationRules` | `VisitorAcceptanceTest.ac3_fourDaysIsRejectedEvenWithAMatchingRecord` | 2 |
| AC4 | Zero or negative days is rejected without reading the register | `VisitorGate`, `VisitorReservationRules` | `VisitorAcceptanceTest.ac4_zeroOrNegativeDaysIsRejectedWithoutReadingTheRegister` | 2 |
| AC5 | An item outside the allowlist is rejected | `VisitorGate` | `VisitorAcceptanceTest.ac5_anItemOutsideTheAllowlistIsRejectedEvenWithAMatchingRecord` | 2 |
| AC6 | A missing or denied approval is an expected rejection | `VisitorGate` | `VisitorAcceptanceTest.ac6_aMissingOrDeniedApprovalIsAnExpectedRejection` | 2 |
| AC7 | An approval for another borrower, item or period does not authorise | `ApprovalRecord`, `VisitorGate` | `VisitorAcceptanceTest.ac7_anApprovalForAnotherBorrowerItemOrPeriodDoesNotAuthorise` | 2 |
| AC8 | The request instant equal to `validFrom` is valid | `ApprovalRecord` | `VisitorAcceptanceTest.ac8_theRequestInstantEqualToValidFromIsValid` | 2 |
| AC9 | The request instant at `validUntil`, or before `validFrom`, is rejected | `ApprovalRecord` | `VisitorAcceptanceTest.ac9_theRequestInstantAtValidUntilOrBeforeValidFromIsRejected` | 2 |
| AC10 | An unreadable register is an operational failure | `FileApprovalSource`, `VisitorGate` | `VisitorAcceptanceTest.ac10_anUnreadableApprovalRegisterIsAnOperationalFailureNotARejection` | 2 |
| AC11 | Three retained reservations block a fourth, even after the loans are returned | `ReservationCoordinator`, `VisitorReservationRules` | `VisitorAcceptanceTest.ac11_threeRetainedReservationsBlockAFourthEvenAfterLoansAreReturned` | 2 |
| AC12 | A disabled flag rejects explicitly without reading the register | `VisitorGate` | `VisitorAcceptanceTest.ac12_aDisabledFlagRejectsExplicitlyWithoutReadingTheRegister` | 2 |
| AC13 | Student and staff requests are unchanged under either setting | `DirectoryReservationService` | `VisitorAcceptanceTest.ac13_studentAndStaffBehaviourIsUnchangedUnderEitherSettingAndNeverReadsTheRegister` | 2 |
| AC14 | An overlap with an existing reservation is rejected by the existing rule | `ReservationCoordinator` | `VisitorAcceptanceTest.ac14_anOverlapWithAnExistingReservationIsRejectedByTheExistingRule` | 2 |
| AC15 | An expected notification failure keeps the reservation | `ReservationCoordinator` | `VisitorAcceptanceTest.ac15_anExpectedNotificationFailureLeavesTheVisitorReservationInPlace` | 2 |
| AC16 | A visitor reservation stays usable after the approval expires and the flag is off | `LoanService` | `VisitorAcceptanceTest.ac16_aVisitorReservationStaysUsableAfterTheApprovalExpiresAndTheFlagIsOff` | 2 |
| AC17 | An unknown or inactive borrower is rejected as before | `DirectoryReservationService`, `LegacyDirectoryAdapter` | `VisitorAcceptanceTest.ac17_anInactiveOrUnknownBorrowerIsRejectedAsBefore` | 2 |
| AC18 | A visitor loan in the overdue report keeps the existing kind rule (suspected defect SD-11-1) | `OverdueReport`, `FinePolicy` | `VisitorAcceptanceTest.ac18_aVisitorLoanInTheOverdueReportKeepsTheExistingKindRuleSd11_1` | 2 |

## Known gaps: requirements with no evidence here

| ID | Gap | Why it is not covered |
|---|---|---|
| G1 | Behaviour against a real directory service | There is none in this project; the stub is the author's assumption |
| G2 | Two writers of the register, or two simultaneous requests | The register is a trusted sequential file; no concurrency test exists |
| G3 | Revoking an approval after a reservation | Not part of CR-12; see the revisit triggers in `ADR-013-visiting-researchers.md` |
| G4 | The right late-fine rate for a visitor | Suspected defect SD-11-1: only the records office can decide it |
| G5 | Behaviour on a Java 17 runtime and on a hosted CI runner | Not run; the checks used `--release 17` on a newer JDK |
```

### 3.9 `after/docs/KNOWN-ISSUES.md`

```markdown
# Known issues and decisions, version 0.14.0

Each item has a decision. **Fixed** means changed in this version and covered by a check. **Deferred** means a named owner must decide first, or the cost is not justified yet. **Accepted** means a known limit that the documents state.

The version is a handover, not a feature sprint. Nothing below was fixed by adding behaviour; the one fix is to the setup and demonstration.

| ID | Item | Effect on a user | Decision | Reason and next step |
|---|---|---|---|---|
| KI-1 | The demonstration program needed a directory service that only the tests could start, so a new reader could not run it | A reader could not see the system work | **Fixed** (`scripts/demo.sh`, `DemoRun`) | Covered by the dry run in `scripts/handover-check.sh` |
| KI-2 | SD-11-1: any borrower kind other than student or staff is fined at 1.00 a day with no grace and no cap. A late visitor now reaches this rule (AC18 pins it) | A late visitor is fined at a rate nobody chose | **Deferred** | Only the records office can say what the rate should be. Pinned in `docs/SUSPECTED-DEFECTS-legacy-overdue-report.md` |
| KI-3 | SD-11-2: a loan within the grace period is listed with fine 0.00 and counted as overdue | A report line that may not be wanted | **Deferred** | Needs the owner's answer to "should it appear at all?" |
| KI-4 | SD-11-3: a null kind throws `NullPointerException`, but only for a loan that is overdue and unreturned | A crash if the export ever contains a null kind | **Deferred** | Ask whether the export can contain one |
| KI-5 | SD-11-4: amounts use the default locale (`0,50` under a German locale) | A different separator on a different machine | **Deferred** | Owner decides whether the separator follows the machine or the office |
| KI-6 | SD-12: the count rule counts every retained reservation, including returned ones | A borrower with three returned loans cannot reserve a fourth | **Deferred** | Preserved on purpose by CR-12 and pinned by AC11. Owner decides |
| KI-7 | One bad row in the approval register rejects the whole register | One typo blocks every visitor request until it is repaired | **Accepted** | A silent skip could hide a lost approval or a duplicate. Revisit with real use |
| KI-8 | The directory wait defaults to one second and was not measured. It bounds the whole lookup, body included | A slow or stalled directory fails the request after about a second | **Accepted** | It is a setting, `lending.directory.timeout.millis`. Measure before changing it. The stalled-body case is tested (`aStalledBodyIsAFailureWithinTheOverallWait`) on a newer JDK only; no Java 17 run was made |
| KI-9 | No retry and no cached answer after a directory outage | An outage stops the request | **Accepted** | By design (ADR-013). Revisit after measured outages |
| KI-10 | The directory stub and the approval file are stand-ins | Nothing here shows how a real service behaves | **Accepted** | Needs a provider contract test against a real service, which does not exist here |
| KI-11 | Concurrency: two writers of the register, or simultaneous requests, were not considered | Unknown | **Accepted** | Out of scope; the register is a trusted sequential file |
| KI-12 | No Java 17 run and no hosted CI run; the workflow's action versions were not re-checked | The Java 17 baseline and the workflow are untested | **Deferred** | Run both when a JDK 17 and a hosted runner are available |
| KI-13 | The visitor flag is still in the code | Two paths to keep tested | **Deferred** | Decided in `docs/ADR-014-flag-handover.md`; the removal is rehearsed in `rehearsal/` |
| KI-14 | `DirectoryReservationService` now has a branch on the visitor category | One category-specific special case in the entry point | **Accepted** | Fine for one special category. At a second, replace the branch with a per-category pre-check, as a refactoring with its own tests |
```

### 3.10 `after/docs/RELEASE-NOTES-0.14.0.md`

```markdown
# Release notes: version 0.14.0 (handover)

Date: 13 October 2026. Built from version 0.13.1, the visiting-researcher change with its corrected directory timeout.

## What this version is

A handover version. It changes **no production behaviour**: every production source file is byte for byte as in 0.13.1. It adds the material that a new reader needs: a runnable demonstration, a requirements-to-evidence table that a test keeps honest, a list of known issues with decisions, and a decision about the visitor flag.

## Added

- `scripts/demo.sh` and `DemoRun`: run the system with visitors disabled and then enabled, with no other setup.
- `scripts/handover-check.sh`: copies the project to a new folder, follows `docs/HANDOVER.md` there and compares the results.
- `docs/HANDOVER.md`, `docs/KNOWN-ISSUES.md`, `docs/REQUIREMENTS-TO-EVIDENCE.md` and `docs/ADR-014-flag-handover.md`.
- `TraceabilityTest` (three invocations): fails the build if a test or class named in the requirements table no longer exists, or an acceptance example loses its row.
- `rehearsal/remove-visitor-flag.patch`: the prepared, tested removal of the visitor flag. Not applied.

## Changed

- Version 0.14.0. The build runs 235 invocations (232 from 0.13.1 and the three above).

## Fixed

- KI-1: the demonstration could not be run without a directory service that only the tests could start.

## Behaviour you should know about

- Visitors remain **disabled by default**. Set `-Dlending.visitors=true` for the demonstration program to enable them.
- An unreachable directory or an unreadable approval register stops the request. It is never reported as "not found" or "not approved".

## Known issues

See `docs/KNOWN-ISSUES.md`. The most important: a late visitor is fined at the rate of the report's "any other kind" rule, which nobody has chosen (SD-11-1); the count rule counts returned reservations (SD-12).

## Not verified

No Java 17 run and no hosted CI run has been made. The directory and the approval register are stand-ins; nothing was run against a real service. No independent review has been made of this release.
```

### 3.11 `after/docs/ADR-014-flag-handover.md`

```markdown
# ADR-014: Keep the visitor flag at handover; removal rehearsed, not applied

Date: 13 October 2026
Status: Decided for the book project by its author, as a model decision. Not an institutional decision. A team decides for its own flag.

## Context

ADR-013 introduced one flag, `visitingResearchersEnabled` (the property `lending.visitors`), default off, and said to remove it when all of three conditions hold: the released variant of CR-12 is accepted, both settings have passed in the pipeline for the release candidate, and a decision to keep visitors enabled is recorded. It also said to review the flag at the end of the handover.

The state today: both settings pass in the pipeline (the second condition holds). CR-12 is a teaching contract and no owner has accepted it as the borrowing policy (the first condition does not hold). Nobody has recorded a decision to keep visitors enabled (the third does not hold).

## Decision

Keep the flag, default off, in version 0.14.0. Do not remove it yet.

The removal was **rehearsed** in a scratch copy so that the cost is known and the change is ready. The rehearsal is `rehearsal/remove-visitor-flag.patch`; apply it from the project directory with `patch -p1`. It deletes the flag, the `DISABLED` result and `VisitorGate.disabled()`, and adds `VisitorGate.noApprovals()` for an application with no register, so that the older two-argument service constructor keeps its meaning: no visitor is approved. It touches eleven files (three production classes, five test classes, the requirements table, the expected numbers in `docs/HANDOVER.md` and `scripts/handover-check.sh`) with 87 lines added and 131 removed, and the prose of `README.md`, the rest of `docs/HANDOVER.md` and the two decision records still needs editing by hand. After the patch, the full build ran 233 invocations with no failures (235 before), the pipeline passed, and the handover check passed.

## Alternatives considered

- **Remove the flag now.** Rejected: it would turn an unaccepted teaching contract into permanent behaviour, and it would remove the one switch that stops new visitor reservations without a new build.
- **Keep the flag with no removal plan.** Rejected: an owner-less flag is a permanent branch. This record names the condition and the prepared change.
- **Replace the flag by configuration that is read at run time.** Not adopted: the flag is already a system property for the demonstration program, and a configuration service is outside the scope of the module.

## Consequences

Both paths stay tested: the acceptance example AC12 (disabled flag), the flag-off journey and the gate's disabled tests remain. A visitor can never be served unless someone sets the property to `true`. Two small costs remain: every new test that builds a visitor gate must pick a setting, and the documents must keep saying that the default is off.

When the three conditions hold, apply `rehearsal/remove-visitor-flag.patch`. It retires AC12 as written (an application with no register approves no visitor instead), rewrites AC13 and AC16, which name the flag, and updates the requirements table and the handover check. Then edit `README.md`, `docs/HANDOVER.md` and ADR-013 by hand, and record the removal in a new decision record. Rollback after removal is a redelivery of the previous release, not a flag change.

## Validation and review

The rehearsal was run, not reasoned about: 233 invocations, 0 failures. No independent peer review is claimed.

## Revisit triggers

An owner accepts or rejects the visitor variant; a decision to keep visitors enabled is recorded; a second flag is proposed (decide the policy for several flags first); or the flag stays in place for longer than the team's own limit for release toggles.
```

## 4. New listings: tests, the rehearsal and the AI activity files

### 4.1 `after/src/test/java/edu/se506/lending/docs/TraceabilityTest.java`

```java
package edu.se506.lending.docs;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;

/**
 * Keeps docs/REQUIREMENTS-TO-EVIDENCE.md honest. It checks that the names in the table still exist
 * (test methods, production classes) and that every acceptance example has exactly one row. It does
 * not check that a named test is the right evidence for its requirement: a reviewer does that.
 */
class TraceabilityTest {
    private static final Path TABLE = Path.of("docs", "REQUIREMENTS-TO-EVIDENCE.md");
    private static final Path MAIN = Path.of("src", "main", "java");
    private static final Path TEST = Path.of("src", "test", "java");
    private static final Pattern TEST_REFERENCE = Pattern.compile("`([A-Z]\\w+)\\.([a-z]\\w*)`");
    private static final Pattern CLASS_REFERENCE = Pattern.compile("`([A-Z]\\w+)`");
    private static final Pattern ACCEPTANCE_ID = Pattern.compile("^AC\\d+$");
    private static final Pattern ACCEPTANCE_TEST = Pattern.compile("void (ac\\d+_\\w+)\\(");

    /** One table row: its cells, trimmed, without the outer bars. */
    private record Row(List<String> cells) {
        String id() { return cells.get(0); }
        String decidedBy() { return cells.get(2); }
        String evidence() { return cells.get(3); }
    }

    private static List<Row> rows() throws IOException {
        List<Row> rows = new ArrayList<>();
        for (String line : Files.readAllLines(TABLE, StandardCharsets.UTF_8)) {
            if (!line.startsWith("| ") || line.startsWith("| ---") || line.startsWith("| ID ")) continue;
            List<String> cells = new ArrayList<>();
            for (String cell : line.substring(1, line.length() - 1).split("\\|", -1)) cells.add(cell.trim());
            if (cells.size() == 5) rows.add(new Row(cells));   // the gap table has three columns
        }
        return rows;
    }

    private static String sourceOf(Path root, String className) throws IOException {
        try (Stream<Path> files = Files.walk(root)) {
            List<Path> found = files.filter(p -> p.getFileName().toString().equals(className + ".java")).toList();
            assertEquals(1, found.size(), "expected exactly one " + className + ".java under " + root + " but found " + found);
            return Files.readString(found.get(0), StandardCharsets.UTF_8);
        }
    }

    @Test void everyTestNamedInTheTableStillExists() throws IOException {
        List<String> missing = new ArrayList<>();
        int checked = 0;
        for (Row row : rows()) {
            Matcher m = TEST_REFERENCE.matcher(row.evidence());
            assertTrue(m.find(), row.id() + " names no test");
            do {
                checked++;
                String source = sourceOf(TEST, m.group(1));
                if (!Pattern.compile("void " + Pattern.quote(m.group(2)) + "\\(").matcher(source).find()) {
                    missing.add(row.id() + ": " + m.group(1) + "." + m.group(2));
                }
            } while (m.find());
        }
        assertTrue(checked >= 29, "the table should name at least 29 tests, found " + checked);
        assertEquals(List.of(), missing, "tests named in the table that no longer exist");
    }

    @Test void everyClassNamedAsDecidingStillExists() throws IOException {
        List<String> missing = new ArrayList<>();
        for (Row row : rows()) {
            Matcher m = CLASS_REFERENCE.matcher(row.decidedBy());
            assertTrue(m.find(), row.id() + " names no deciding class");
            do {
                try {
                    sourceOf(MAIN, m.group(1));
                } catch (AssertionError gone) {
                    missing.add(row.id() + ": " + m.group(1));
                }
            } while (m.find());
        }
        assertEquals(List.of(), missing, "classes named in the table that no longer exist");
    }

    @Test void everyAcceptanceExampleHasExactlyOneRowAndEveryAcceptanceTestIsInTheTable() throws IOException {
        TreeMap<String, Integer> rowsPerExample = new TreeMap<>();
        TreeSet<String> referenced = new TreeSet<>();
        for (Row row : rows()) {
            if (ACCEPTANCE_ID.matcher(row.id()).matches()) rowsPerExample.merge(row.id(), 1, Integer::sum);
            Matcher m = TEST_REFERENCE.matcher(row.evidence());
            while (m.find()) referenced.add(m.group(2));
        }
        for (int n = 1; n <= 18; n++) {
            assertEquals(1, rowsPerExample.getOrDefault("AC" + n, 0), "rows for AC" + n);
        }
        assertEquals(18, rowsPerExample.size(), "unexpected acceptance ids: " + rowsPerExample.keySet());

        Matcher declared = ACCEPTANCE_TEST.matcher(sourceOf(TEST, "VisitorAcceptanceTest"));
        List<String> unlisted = new ArrayList<>();
        int tests = 0;
        while (declared.find()) {
            tests++;
            if (!referenced.contains(declared.group(1))) unlisted.add(declared.group(1));
        }
        assertEquals(18, tests, "VisitorAcceptanceTest should declare one test per example");
        assertEquals(List.of(), unlisted, "acceptance tests that the table does not mention");
    }
}
```

### 4.2 `after/src/test/java/edu/se506/lending/integration/DemoRun.java`

```java
package edu.se506.lending.integration;

import edu.se506.lending.bootstrap.Chapter13Demo;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * A runnable demonstration for a reader who has no directory service: it starts the controlled local
 * directory stub, writes a small approval register, and runs the Chapter 13 system twice, with
 * visitors disabled and then enabled. It lives with the tests because the stub does. The clock is
 * fixed so that the sample approval is always valid. Run it with scripts/demo.sh.
 */
public final class DemoRun {
    private static final String REGISTER = String.join("\n",
            "borrowerId\titemId\tstart\tendExclusive\tsponsorId\tstatus\tvalidFrom\tvalidUntil",
            "V1\tCAM2\t2026-10-20\t2026-10-22\tS1\tAPPROVED\t2026-10-18T00:00:00Z\t2026-10-20T00:00:00Z", "");

    private DemoRun() { }

    public static void main(String[] args) throws IOException {
        Path register = Files.createTempFile("approvals", ".tsv");
        try (DirectoryStub stub = new DirectoryStub()) {
            Files.writeString(register, REGISTER, StandardCharsets.UTF_8);
            System.setProperty("lending.directory.url", stub.baseUri().toString());
            System.setProperty("lending.approvals.file", register.toString());
            System.setProperty("lending.now", "2026-10-19T12:00:00Z");
            for (String enabled : new String[] {"false", "true"}) {
                System.out.println("== visitors " + (enabled.equals("true") ? "enabled" : "disabled") + " ==");
                System.setProperty("lending.visitors", enabled);
                Chapter13Demo.main(new String[0]);
            }
        } finally {
            Files.deleteIfExists(register);
        }
    }
}
```

### 4.3 `after/rehearsal/remove-visitor-flag.patch`

This is a unified diff against the finished 0.14.0 checkpoint. Apply it from inside `after` with `patch -p1 < rehearsal/remove-visitor-flag.patch`. It is the **rehearsal** of ADR-014: it is stored and tested, not applied.

```patch
diff --git a/docs/HANDOVER.md b/docs/HANDOVER.md
--- a/docs/HANDOVER.md
+++ b/docs/HANDOVER.md
@@ -36,3 +36,3 @@
 
-Expected: `BUILD SUCCESS` and `Tests run: 235, Failures: 0, Errors: 0, Skipped: 0`.
+Expected: `BUILD SUCCESS` and `Tests run: 233, Failures: 0, Errors: 0, Skipped: 0`.
 
@@ -44,3 +44,3 @@
 
-Expected: five stages, each ending `PASSED`, then `PIPELINE PASSED`. Stage 2 runs 206 invocations, stage 3 runs 26 and stage 4 runs 3.
+Expected: five stages, each ending `PASSED`, then `PIPELINE PASSED`. Stage 2 runs 205 invocations, stage 3 runs 26 and stage 4 runs 2.
 
diff --git a/docs/REQUIREMENTS-TO-EVIDENCE.md b/docs/REQUIREMENTS-TO-EVIDENCE.md
--- a/docs/REQUIREMENTS-TO-EVIDENCE.md
+++ b/docs/REQUIREMENTS-TO-EVIDENCE.md
@@ -20,4 +20,4 @@
 | C8 | An unreachable or slow directory is a failure, never "not found" | `HttpLegacyDirectoryClient`, `LegacyDirectoryAdapter` | `DirectoryOutageIntegrationTest.aServerErrorIsAnOutageNotANotFoundAndIsNotRetried` `DirectoryOutageIntegrationTest.aStalledBodyIsAFailureWithinTheOverallWait` | 3 |
-| C9 | The visitor behaviour is behind one flag that defaults to off | `VisitorGate`, `Chapter13Demo` | `Chapter13JourneyE2ETest.withTheFlagOffVisitorsAreRefusedAndEveryoneElseIsServed` | 4 |
-| C10 | Student and staff behaviour is unchanged | `ReservationCoordinator` | `VisitorAcceptanceTest.ac13_studentAndStaffBehaviourIsUnchangedUnderEitherSettingAndNeverReadsTheRegister` | 2 |
+| C9 | An application with no approval register approves no visitor (the flag was removed) | `VisitorGate` | `VisitorGateTest.aGateWithNoRegisterApprovesNoVisitor` | 2 |
+| C10 | Student and staff behaviour is unchanged | `ReservationCoordinator` | `VisitorAcceptanceTest.ac13_studentAndStaffBehaviourIsUnchangedAndNeverReadsTheRegister` | 2 |
 
@@ -38,7 +38,7 @@
 | AC11 | Three retained reservations block a fourth, even after the loans are returned | `ReservationCoordinator`, `VisitorReservationRules` | `VisitorAcceptanceTest.ac11_threeRetainedReservationsBlockAFourthEvenAfterLoansAreReturned` | 2 |
-| AC12 | A disabled flag rejects explicitly without reading the register | `VisitorGate` | `VisitorAcceptanceTest.ac12_aDisabledFlagRejectsExplicitlyWithoutReadingTheRegister` | 2 |
-| AC13 | Student and staff requests are unchanged under either setting | `DirectoryReservationService` | `VisitorAcceptanceTest.ac13_studentAndStaffBehaviourIsUnchangedUnderEitherSettingAndNeverReadsTheRegister` | 2 |
+| AC12 | An application with no register approves no visitor | `VisitorGate` | `VisitorAcceptanceTest.ac12_anApplicationWithNoRegisterApprovesNoVisitor` | 2 |
+| AC13 | Student and staff requests are unchanged | `DirectoryReservationService` | `VisitorAcceptanceTest.ac13_studentAndStaffBehaviourIsUnchangedAndNeverReadsTheRegister` | 2 |
 | AC14 | An overlap with an existing reservation is rejected by the existing rule | `ReservationCoordinator` | `VisitorAcceptanceTest.ac14_anOverlapWithAnExistingReservationIsRejectedByTheExistingRule` | 2 |
 | AC15 | An expected notification failure keeps the reservation | `ReservationCoordinator` | `VisitorAcceptanceTest.ac15_anExpectedNotificationFailureLeavesTheVisitorReservationInPlace` | 2 |
-| AC16 | A visitor reservation stays usable after the approval expires and the flag is off | `LoanService` | `VisitorAcceptanceTest.ac16_aVisitorReservationStaysUsableAfterTheApprovalExpiresAndTheFlagIsOff` | 2 |
+| AC16 | A visitor reservation stays usable after the approval expires and new requests are not approved | `LoanService` | `VisitorAcceptanceTest.ac16_aVisitorReservationStaysUsableAfterTheApprovalExpiresAndNewRequestsAreNotApproved` | 2 |
 | AC17 | An unknown or inactive borrower is rejected as before | `DirectoryReservationService`, `LegacyDirectoryAdapter` | `VisitorAcceptanceTest.ac17_anInactiveOrUnknownBorrowerIsRejectedAsBefore` | 2 |
diff --git a/scripts/handover-check.sh b/scripts/handover-check.sh
--- a/scripts/handover-check.sh
+++ b/scripts/handover-check.sh
@@ -10,5 +10,5 @@
 
-EXPECT_UNIT=206          # stage 2 of the pipeline
+EXPECT_UNIT=205          # stage 2 of the pipeline
 EXPECT_INTEGRATION=26    # stage 3
-EXPECT_E2E=3             # stage 4
+EXPECT_E2E=2             # stage 4
 EXPECT_TOTAL=$((EXPECT_UNIT + EXPECT_INTEGRATION + EXPECT_E2E))
@@ -42,5 +42,4 @@
 if bash scripts/demo.sh > demo.out 2>&1; then echo "ok   the demonstration exited 0"; else echo "FAIL the demonstration did not exit 0"; failures=$((failures + 1)); fi
-expect demo.out "Visitor V1: Rejected: visitor reservations are not enabled." "the disabled run rejects a visitor"
-expect demo.out "Visitor V1: Confirmed: R2 for V1 on CAM2 [2026-10-20, 2026-10-22)." "the enabled run confirms an approved visitor"
-expect demo.out "Visitor V2: Rejected: no valid sponsor approval." "the enabled run rejects an unapproved visitor"
+expect demo.out "Visitor V1: Confirmed: R2 for V1 on CAM2 [2026-10-20, 2026-10-22)." "an approved visitor is confirmed"
+expect demo.out "Visitor V2: Rejected: no valid sponsor approval." "an unapproved visitor is rejected"
 expect demo.out "Outage BROKEN: Unavailable: Borrower directory unavailable" "an outage is reported as unavailable"
diff --git a/src/main/java/edu/se506/lending/application/DirectoryReservationService.java b/src/main/java/edu/se506/lending/application/DirectoryReservationService.java
--- a/src/main/java/edu/se506/lending/application/DirectoryReservationService.java
+++ b/src/main/java/edu/se506/lending/application/DirectoryReservationService.java
@@ -19,3 +19,3 @@
                                        ReservationCoordinator coordinator) {
-        this(directory, coordinator, VisitorGate.disabled());
+        this(directory, coordinator, VisitorGate.noApprovals());
     }
diff --git a/src/main/java/edu/se506/lending/application/VisitorGate.java b/src/main/java/edu/se506/lending/application/VisitorGate.java
--- a/src/main/java/edu/se506/lending/application/VisitorGate.java
+++ b/src/main/java/edu/se506/lending/application/VisitorGate.java
@@ -13,3 +13,3 @@
  * The extra checks for a visiting researcher, kept apart from the count and duration policy: the
- * feature flag, the item allowlist and a matching sponsor approval that is valid at one request-time
+ * item allowlist and a matching sponsor approval that is valid at one request-time
  * instant. It returns a rejection text, or empty when the request may go on to the coordinator.
@@ -19,3 +19,2 @@
 public final class VisitorGate {
-    public static final String DISABLED = "Rejected: visitor reservations are not enabled.";
     public static final String ITEM_NOT_ALLOWED = "Rejected: item not available to visitors.";
@@ -27,15 +26,11 @@
     private final Clock clock;
-    private final boolean enabled;
 
-    public VisitorGate(ApprovalSource source, Clock clock, boolean enabled) {
+    public VisitorGate(ApprovalSource source, Clock clock) {
         this.source = Objects.requireNonNull(source, "source");
         this.clock = Objects.requireNonNull(clock, "clock");
-        this.enabled = enabled;
     }
 
-    /** A gate for applications that have not enabled visitors: the approval source is never read. */
-    public static VisitorGate disabled() {
-        return new VisitorGate((borrowerId, itemId, start, end) -> {
-            throw new IllegalStateException("The approval source must not be read while visitors are disabled.");
-        }, Clock.systemUTC(), false);
+    /** A gate for applications with no approval register: no visitor is ever approved. */
+    public static VisitorGate noApprovals() {
+        return new VisitorGate((borrowerId, itemId, start, end) -> Optional.empty(), Clock.systemUTC());
     }
@@ -43,5 +38,2 @@
     public Optional<String> rejection(String borrowerId, String itemId, LocalDate start, int days) {
-        if (!enabled) {
-            return Optional.of(DISABLED);
-        }
         if (!ALLOWED_ITEMS.contains(itemId)) {
diff --git a/src/main/java/edu/se506/lending/bootstrap/Chapter13Demo.java b/src/main/java/edu/se506/lending/bootstrap/Chapter13Demo.java
--- a/src/main/java/edu/se506/lending/bootstrap/Chapter13Demo.java
+++ b/src/main/java/edu/se506/lending/bootstrap/Chapter13Demo.java
@@ -22,3 +22,3 @@
  * and one feature flag. Settings are system properties so that a test can start it as a separate process:
- * lending.directory.url (required), lending.approvals.file (required), lending.visitors (default false),
+ * lending.directory.url (required), lending.approvals.file (required),
  * lending.now (an ISO instant, default the system clock) and lending.directory.timeout.millis (default 1000).
@@ -29,3 +29,2 @@
         Path approvals = Path.of(required("lending.approvals.file"));
-        boolean visitorsEnabled = Boolean.parseBoolean(System.getProperty("lending.visitors", "false"));
         String now = System.getProperty("lending.now");
@@ -38,3 +37,3 @@
                 directoryUrl, Duration.ofMillis(timeoutMillis), Duration.ofMillis(timeoutMillis)));
-        var gate = new VisitorGate(new FileApprovalSource(approvals), clock, visitorsEnabled);
+        var gate = new VisitorGate(new FileApprovalSource(approvals), clock);
         var service = new DirectoryReservationService(directory, coordinator, gate);
@@ -42,3 +41,2 @@
         LocalDate start = LocalDate.of(2026, 10, 20);
-        System.out.println("Visitors enabled: " + visitorsEnabled);
         attempt("Student B1", service, "B1", "CAM1", start, 2);
diff --git a/src/test/java/edu/se506/lending/e2e/Chapter13JourneyE2ETest.java b/src/test/java/edu/se506/lending/e2e/Chapter13JourneyE2ETest.java
--- a/src/test/java/edu/se506/lending/e2e/Chapter13JourneyE2ETest.java
+++ b/src/test/java/edu/se506/lending/e2e/Chapter13JourneyE2ETest.java
@@ -33,3 +33,3 @@
 
-    private Run run(DirectoryStub stub, Path register, boolean visitors) throws IOException, InterruptedException {
+    private Run run(DirectoryStub stub, Path register) throws IOException, InterruptedException {
         String java = Path.of(System.getProperty("java.home"), "bin",
@@ -40,3 +40,2 @@
                 "-Dlending.approvals.file=" + register,
-                "-Dlending.visitors=" + visitors,
                 "-Dlending.now=2026-10-19T12:00:00Z",
@@ -61,24 +60,7 @@
 
-    @Test void withTheFlagOffVisitorsAreRefusedAndEveryoneElseIsServed() throws Exception {
+    @Test void anApprovedVisitorIsServedAndAnUnapprovedOneIsRefused() throws Exception {
         try (var stub = new DirectoryStub()) {
-            Run run = run(stub, register(HEADER, V1_CAM2), false);
+            Run run = run(stub, register(HEADER, V1_CAM2));
             assertEquals(0, run.exitCode(), String.join("\n", run.lines()));
             assertEquals(List.of(
-                    "Visitors enabled: false",
-                    "Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).",
-                    "Visitor V1: Rejected: visitor reservations are not enabled.",
-                    "Visitor V2: Rejected: visitor reservations are not enabled.",
-                    "Unknown U9: Rejected: borrower not found or inactive.",
-                    "Outage BROKEN: Unavailable: Borrower directory unavailable",
-                    "Reservations: 1",
-                    "Notices: 1"), run.lines());
-        }
-    }
-
-    @Test void withTheFlagOnAnApprovedVisitorIsServedAndAnUnapprovedOneIsRefused() throws Exception {
-        try (var stub = new DirectoryStub()) {
-            Run run = run(stub, register(HEADER, V1_CAM2), true);
-            assertEquals(0, run.exitCode(), String.join("\n", run.lines()));
-            assertEquals(List.of(
-                    "Visitors enabled: true",
                     "Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).",
@@ -95,8 +77,8 @@
         try (var stub = new DirectoryStub()) {
-            Run run = run(stub, register(HEADER, V1_CAM2, "garbage row"), true);
+            Run run = run(stub, register(HEADER, V1_CAM2, "garbage row"));
             assertEquals(0, run.exitCode(), String.join("\n", run.lines()));
-            assertEquals("Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).", run.lines().get(1));
-            assertEquals("Visitor V1: Approval register unavailable: Row 3 has 1 columns, not 8.", run.lines().get(2));
-            assertEquals("Visitor V2: Approval register unavailable: Row 3 has 1 columns, not 8.", run.lines().get(3));
-            assertEquals("Reservations: 1", run.lines().get(6));
+            assertEquals("Student B1: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).", run.lines().get(0));
+            assertEquals("Visitor V1: Approval register unavailable: Row 3 has 1 columns, not 8.", run.lines().get(1));
+            assertEquals("Visitor V2: Approval register unavailable: Row 3 has 1 columns, not 8.", run.lines().get(2));
+            assertEquals("Reservations: 1", run.lines().get(5));
         }
diff --git a/src/test/java/edu/se506/lending/integration/DemoRun.java b/src/test/java/edu/se506/lending/integration/DemoRun.java
--- a/src/test/java/edu/se506/lending/integration/DemoRun.java
+++ b/src/test/java/edu/se506/lending/integration/DemoRun.java
@@ -10,4 +10,3 @@
  * A runnable demonstration for a reader who has no directory service: it starts the controlled local
- * directory stub, writes a small approval register, and runs the Chapter 13 system twice, with
- * visitors disabled and then enabled. It lives with the tests because the stub does. The clock is
+ * directory stub, writes a small approval register, and runs the Chapter 13 system once. It lives with the tests because the stub does. The clock is
  * fixed so that the sample approval is always valid. Run it with scripts/demo.sh.
@@ -28,7 +27,3 @@
             System.setProperty("lending.now", "2026-10-19T12:00:00Z");
-            for (String enabled : new String[] {"false", "true"}) {
-                System.out.println("== visitors " + (enabled.equals("true") ? "enabled" : "disabled") + " ==");
-                System.setProperty("lending.visitors", enabled);
-                Chapter13Demo.main(new String[0]);
-            }
+            Chapter13Demo.main(new String[0]);
         } finally {
diff --git a/src/test/java/edu/se506/lending/integration/DirectoryOutageIntegrationTest.java b/src/test/java/edu/se506/lending/integration/DirectoryOutageIntegrationTest.java
--- a/src/test/java/edu/se506/lending/integration/DirectoryOutageIntegrationTest.java
+++ b/src/test/java/edu/se506/lending/integration/DirectoryOutageIntegrationTest.java
@@ -65,3 +65,3 @@
     @Test void anOrdinaryStudentRequestWorksThroughTheRealHttpClient() {
-        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
+        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.noApprovals());
         assertEquals("Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).", service.reserve("B1", "CAM1", START, 2));
@@ -71,3 +71,3 @@
     @Test void aMissingRowIsAnOrdinaryRejection() {
-        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
+        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.noApprovals());
         assertEquals("Rejected: borrower not found or inactive.", service.reserve("NOBODY", "CAM1", START, 2));
@@ -77,3 +77,3 @@
     @Test void aServerErrorIsAnOutageNotANotFoundAndIsNotRetried() {
-        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
+        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.noApprovals());
         DirectoryException failure = assertThrows(DirectoryException.class, () -> service.reserve("BROKEN", "CAM1", START, 2));
@@ -85,3 +85,3 @@
     @Test void aSlowProviderTimesOutAfterTheBoundedWaitAndFailsTheRequest() {
-        var service = service(stub.baseUri(), Duration.ofMillis(300), VisitorGate.disabled());
+        var service = service(stub.baseUri(), Duration.ofMillis(300), VisitorGate.noApprovals());
         long begin = System.nanoTime();
@@ -96,3 +96,3 @@
     @Test void aStalledBodyIsAFailureWithinTheOverallWait() {
-        var service = service(stub.baseUri(), Duration.ofMillis(300), VisitorGate.disabled());
+        var service = service(stub.baseUri(), Duration.ofMillis(300), VisitorGate.noApprovals());
         // The headers and the first byte arrive at once and the rest is held. A client whose timeout covers
@@ -112,3 +112,3 @@
         }
-        var service = service(URI.create("http://127.0.0.1:" + closedPort), Duration.ofSeconds(2), VisitorGate.disabled());
+        var service = service(URI.create("http://127.0.0.1:" + closedPort), Duration.ofSeconds(2), VisitorGate.noApprovals());
         assertThrows(DirectoryException.class, () -> service.reserve("B1", "CAM1", START, 2));
@@ -118,3 +118,3 @@
     @Test void aMalformedAnswerIsAnOutageNotAGuess() {
-        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
+        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.noApprovals());
         assertThrows(DirectoryException.class, () -> service.reserve("GARBAGE", "CAM1", START, 2));
@@ -124,3 +124,3 @@
     @Test void anUnknownCategoryCodeIsNeverDefaultedToStaffOrStudent() {
-        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.disabled());
+        var service = service(stub.baseUri(), Duration.ofSeconds(2), VisitorGate.noApprovals());
         DirectoryException failure = assertThrows(DirectoryException.class, () -> service.reserve("ODD", "CAM1", START, 2));
@@ -132,3 +132,3 @@
         Path missingRegister = dir.resolve("never-read.tsv");
-        var gate = new VisitorGate(new FileApprovalSource(missingRegister), Clock.systemUTC(), true);
+        var gate = new VisitorGate(new FileApprovalSource(missingRegister), Clock.systemUTC());
         var service = service(stub.baseUri(), Duration.ofSeconds(2), gate);
@@ -143,3 +143,3 @@
         Clock clock = Clock.fixed(Instant.parse("2026-10-19T12:00:00Z"), ZoneOffset.UTC);
-        var gate = new VisitorGate(new FileApprovalSource(register), clock, true);
+        var gate = new VisitorGate(new FileApprovalSource(register), clock);
         var service = service(stub.baseUri(), Duration.ofSeconds(2), gate);
diff --git a/src/test/java/edu/se506/lending/visitor/VisitorAcceptanceTest.java b/src/test/java/edu/se506/lending/visitor/VisitorAcceptanceTest.java
--- a/src/test/java/edu/se506/lending/visitor/VisitorAcceptanceTest.java
+++ b/src/test/java/edu/se506/lending/visitor/VisitorAcceptanceTest.java
@@ -58,3 +58,3 @@
 
-        World(boolean enabled, Instant now, edu.se506.lending.application.port.NotificationSender notifier) {
+        World(Instant now, edu.se506.lending.application.port.NotificationSender notifier) {
             coordinator = ReservationApplication.create(notifier);
@@ -69,3 +69,3 @@
                 return approvals.stream().filter(r -> r.matches(borrower, item, start, end)).findFirst();
-            }, Clock.fixed(now, ZoneOffset.UTC), enabled);
+            }, Clock.fixed(now, ZoneOffset.UTC));
             service = new DirectoryReservationService(directory, coordinator, gate);
@@ -73,3 +73,3 @@
 
-        World(boolean enabled, Instant now) { this(enabled, now, new RecordingNotificationSender()); }
+        World(Instant now) { this(now, new RecordingNotificationSender()); }
 
@@ -88,3 +88,3 @@
         var recorder = new RecordingNotificationSender();
-        var w = new World(true, NOW, recorder).approve("V1", "CAM1", START, 2);
+        var w = new World(NOW, recorder).approve("V1", "CAM1", START, 2);
         assertEquals(SUCCESS_V1_CAM1, w.service.reserve("V1", "CAM1", START, 2));
@@ -95,3 +95,3 @@
     @Test void ac2_cam2ForThreeDaysNeedsItsOwnRecordAndIsAllowed() {
-        var w = new World(true, NOW).approve("V1", "CAM2", START, 3);
+        var w = new World(NOW).approve("V1", "CAM2", START, 3);
         assertEquals("Confirmed: R1 for V1 on CAM2 [2026-10-20, 2026-10-23).", w.service.reserve("V1", "CAM2", START, 3));
@@ -101,3 +101,3 @@
         var recorder = new RecordingNotificationSender();
-        var w = new World(true, NOW, recorder).approve("V1", "CAM1", START, 4);
+        var w = new World(NOW, recorder).approve("V1", "CAM1", START, 4);
         assertEquals(LIMIT, w.service.reserve("V1", "CAM1", START, 4));
@@ -109,3 +109,3 @@
         var recorder = new RecordingNotificationSender();
-        var w = new World(true, NOW, recorder).approve("V1", "CAM1", START, 2);
+        var w = new World(NOW, recorder).approve("V1", "CAM1", START, 2);
         assertEquals(LIMIT, w.service.reserve("V1", "CAM1", START, 0));
@@ -118,3 +118,3 @@
     @Test void ac5_anItemOutsideTheAllowlistIsRejectedEvenWithAMatchingRecord() {
-        var w = new World(true, NOW).approve("V1", "MIC1", START, 2);
+        var w = new World(NOW).approve("V1", "MIC1", START, 2);
         assertEquals(VisitorGate.ITEM_NOT_ALLOWED, w.service.reserve("V1", "MIC1", START, 2));
@@ -124,6 +124,6 @@
     @Test void ac6_aMissingOrDeniedApprovalIsAnExpectedRejection() {
-        var missing = new World(true, NOW);
+        var missing = new World(NOW);
         assertEquals(VisitorGate.NOT_APPROVED, missing.service.reserve("V1", "CAM1", START, 2));
         assertNothingChanged(missing);
-        var denied = new World(true, NOW);
+        var denied = new World(NOW);
         denied.approvals.add(new ApprovalRecord("V1", "CAM1", START, START.plusDays(2), "S1",
@@ -135,3 +135,3 @@
     @Test void ac7_anApprovalForAnotherBorrowerItemOrPeriodDoesNotAuthorise() {
-        var w = new World(true, NOW).approve("V2", "CAM1", START, 2).approve("V1", "CAM2", START, 2)
+        var w = new World(NOW).approve("V2", "CAM1", START, 2).approve("V1", "CAM2", START, 2)
                 .approve("V1", "CAM1", START, 3);
@@ -142,3 +142,3 @@
     @Test void ac8_theRequestInstantEqualToValidFromIsValid() {
-        var w = new World(true, FROM).approve("V1", "CAM1", START, 2);
+        var w = new World(FROM).approve("V1", "CAM1", START, 2);
         assertEquals(SUCCESS_V1_CAM1, w.service.reserve("V1", "CAM1", START, 2));
@@ -147,5 +147,5 @@
     @Test void ac9_theRequestInstantAtValidUntilOrBeforeValidFromIsRejected() {
-        var atExpiry = new World(true, UNTIL).approve("V1", "CAM1", START, 2);
+        var atExpiry = new World(UNTIL).approve("V1", "CAM1", START, 2);
         assertEquals(VisitorGate.NOT_APPROVED, atExpiry.service.reserve("V1", "CAM1", START, 2));
-        var early = new World(true, FROM.minusSeconds(1)).approve("V1", "CAM1", START, 2);
+        var early = new World(FROM.minusSeconds(1)).approve("V1", "CAM1", START, 2);
         assertEquals(VisitorGate.NOT_APPROVED, early.service.reserve("V1", "CAM1", START, 2));
@@ -159,3 +159,3 @@
         ApprovalSourceException failure = new ApprovalSourceException("register unreadable");
-        var gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC), true);
+        var gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC));
         var service = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), coordinator, gate);
@@ -170,3 +170,3 @@
         ApprovalSourceException failure = new ApprovalSourceException("register unreadable");
-        var gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC), true);
+        var gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC));
         var service = new DirectoryReservationService(id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), coordinator, gate);
@@ -182,3 +182,3 @@
         Clock checkoutDay = Clock.fixed(Instant.parse("2026-10-20T09:00:00Z"), ZoneOffset.UTC);
-        var w = new World(true, NOW);
+        var w = new World(NOW);
         var loans = new LoanService(w.coordinator, checkoutDay);
@@ -195,20 +195,14 @@
 
-    @Test void ac12_aDisabledFlagRejectsExplicitlyWithoutReadingTheRegister() {
-        var w = new World(false, NOW).approve("V1", "CAM1", START, 2);
-        assertEquals(VisitorGate.DISABLED, w.service.reserve("V1", "CAM1", START, 2));
-        assertEquals(0, w.approvalReads.get());
-        assertNothingChanged(w);
+    @Test void ac12_anApplicationWithNoRegisterApprovesNoVisitor() {
         var defaultService = new DirectoryReservationService(
                 id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), ReservationApplication.create(new RecordingNotificationSender()));
-        assertEquals(VisitorGate.DISABLED, defaultService.reserve("V1", "CAM1", START, 2));
+        assertEquals(VisitorGate.NOT_APPROVED, defaultService.reserve("V1", "CAM1", START, 2));
     }
 
-    @Test void ac13_studentAndStaffBehaviourIsUnchangedUnderEitherSettingAndNeverReadsTheRegister() {
-        for (boolean enabled : new boolean[] {false, true}) {
-            var w = new World(enabled, NOW);
-            assertEquals("Confirmed: R1 for S1 on CAM1 [2026-10-20, 2026-10-27).", w.service.reserve("S1", "CAM1", START, 7));
-            assertEquals("Confirmed: R2 for T1 on MIC1 [2026-10-20, 2026-11-03).", w.service.reserve("T1", "MIC1", START, 14));
-            assertEquals("Rejected: borrower limit or duration.", w.service.reserve("S1", "CAM2", START, 8));
-            assertEquals(0, w.approvalReads.get());
-        }
+    @Test void ac13_studentAndStaffBehaviourIsUnchangedAndNeverReadsTheRegister() {
+        var w = new World(NOW);
+        assertEquals("Confirmed: R1 for S1 on CAM1 [2026-10-20, 2026-10-27).", w.service.reserve("S1", "CAM1", START, 7));
+        assertEquals("Confirmed: R2 for T1 on MIC1 [2026-10-20, 2026-11-03).", w.service.reserve("T1", "MIC1", START, 14));
+        assertEquals("Rejected: borrower limit or duration.", w.service.reserve("S1", "CAM2", START, 8));
+        assertEquals(0, w.approvalReads.get());
     }
@@ -216,3 +210,3 @@
     @Test void ac14_anOverlapWithAnExistingReservationIsRejectedByTheExistingRule() {
-        var w = new World(true, NOW).approve("V1", "CAM1", START, 2);
+        var w = new World(NOW).approve("V1", "CAM1", START, 2);
         assertTrue(w.coordinator.reserve("S1", "CAM1", START, 2).startsWith("Confirmed: R1"));
@@ -223,3 +217,3 @@
     @Test void ac15_anExpectedNotificationFailureLeavesTheVisitorReservationInPlace() {
-        var w = new World(true, NOW, reservation -> { throw new NotificationException("outbox down"); })
+        var w = new World(NOW, reservation -> { throw new NotificationException("outbox down"); })
                 .approve("V1", "CAM1", START, 2);
@@ -229,9 +223,9 @@
 
-    @Test void ac16_aVisitorReservationStaysUsableAfterTheApprovalExpiresAndTheFlagIsOff() {
+    @Test void ac16_aVisitorReservationStaysUsableAfterTheApprovalExpiresAndNewRequestsAreNotApproved() {
         Clock checkoutDay = Clock.fixed(Instant.parse("2026-10-20T09:00:00Z"), ZoneOffset.UTC);
-        var w = new World(true, NOW).approve("V1", "CAM1", START, 2);
+        var w = new World(NOW).approve("V1", "CAM1", START, 2);
         assertEquals(SUCCESS_V1_CAM1, w.service.reserve("V1", "CAM1", START, 2));
         var afterwards = new DirectoryReservationService(
-                id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), w.coordinator, VisitorGate.disabled());
-        assertEquals(VisitorGate.DISABLED, afterwards.reserve("V1", "CAM2", START, 1));
+                id -> Optional.of(new Borrower(id, BorrowerCategory.VISITOR)), w.coordinator, VisitorGate.noApprovals());
+        assertEquals(VisitorGate.NOT_APPROVED, afterwards.reserve("V1", "CAM2", START, 1));
         var loans = new LoanService(w.coordinator, checkoutDay);
@@ -242,3 +236,3 @@
     @Test void ac17_anInactiveOrUnknownBorrowerIsRejectedAsBefore() {
-        var w = new World(true, NOW).approve("U9", "CAM1", START, 2);
+        var w = new World(NOW).approve("U9", "CAM1", START, 2);
         assertEquals("Rejected: borrower not found or inactive.", w.service.reserve("U9", "CAM1", START, 2));
@@ -251,3 +245,3 @@
         Clock reportDay = Clock.fixed(Instant.parse("2026-10-22T09:00:00Z"), ZoneOffset.UTC);
-        var w = new World(true, NOW).approve("V1", "CAM1", START, 2);
+        var w = new World(NOW).approve("V1", "CAM1", START, 2);
         assertEquals(SUCCESS_V1_CAM1, w.service.reserve("V1", "CAM1", START, 2));
diff --git a/src/test/java/edu/se506/lending/visitor/VisitorGateTest.java b/src/test/java/edu/se506/lending/visitor/VisitorGateTest.java
--- a/src/test/java/edu/se506/lending/visitor/VisitorGateTest.java
+++ b/src/test/java/edu/se506/lending/visitor/VisitorGateTest.java
@@ -38,4 +38,4 @@
 
-    private VisitorGate gate(ApprovalRecord record, Instant now, boolean enabled) {
-        return new VisitorGate(sourceOf(record), Clock.fixed(now, ZoneOffset.UTC), enabled);
+    private VisitorGate gate(ApprovalRecord record, Instant now) {
+        return new VisitorGate(sourceOf(record), Clock.fixed(now, ZoneOffset.UTC));
     }
@@ -43,3 +43,3 @@
     @Test void aMatchingApprovedRecordInsideItsWindowLetsTheRequestContinue() {
-        assertEquals(Optional.empty(), gate(record(ApprovalStatus.APPROVED), NOW, true).rejection("V1", "CAM1", START, 2));
+        assertEquals(Optional.empty(), gate(record(ApprovalStatus.APPROVED), NOW).rejection("V1", "CAM1", START, 2));
         assertEquals(1, reads.get());
@@ -47,11 +47,5 @@
 
-    @Test void aDisabledGateRejectsWithoutReadingTheSource() {
-        assertEquals(Optional.of(VisitorGate.DISABLED),
-                gate(record(ApprovalStatus.APPROVED), NOW, false).rejection("V1", "CAM1", START, 2));
-        assertEquals(0, reads.get());
-    }
-
     @Test void anItemOutsideTheAllowlistIsRejectedWithoutReadingTheSource() {
         assertEquals(Optional.of(VisitorGate.ITEM_NOT_ALLOWED),
-                gate(record(ApprovalStatus.APPROVED), NOW, true).rejection("V1", "MIC1", START, 2));
+                gate(record(ApprovalStatus.APPROVED), NOW).rejection("V1", "MIC1", START, 2));
         assertEquals(0, reads.get());
@@ -60,3 +54,3 @@
     @Test void aNonPositiveDurationIsLeftToThePolicyWithoutReadingTheSource() {
-        VisitorGate gate = gate(record(ApprovalStatus.APPROVED), NOW, true);
+        VisitorGate gate = gate(record(ApprovalStatus.APPROVED), NOW);
         assertEquals(Optional.empty(), gate.rejection("V1", "CAM1", START, 0));
@@ -67,5 +61,5 @@
     @Test void aMissingOrDeniedRecordIsAnExpectedRejection() {
-        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(null, NOW, true).rejection("V1", "CAM1", START, 2));
+        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(null, NOW).rejection("V1", "CAM1", START, 2));
         assertEquals(Optional.of(VisitorGate.NOT_APPROVED),
-                gate(record(ApprovalStatus.DENIED), NOW, true).rejection("V1", "CAM1", START, 2));
+                gate(record(ApprovalStatus.DENIED), NOW).rejection("V1", "CAM1", START, 2));
     }
@@ -74,6 +68,6 @@
         ApprovalRecord approved = record(ApprovalStatus.APPROVED);
-        assertEquals(Optional.empty(), gate(approved, FROM, true).rejection("V1", "CAM1", START, 2));
-        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(approved, UNTIL, true).rejection("V1", "CAM1", START, 2));
+        assertEquals(Optional.empty(), gate(approved, FROM).rejection("V1", "CAM1", START, 2));
+        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(approved, UNTIL).rejection("V1", "CAM1", START, 2));
         assertEquals(Optional.of(VisitorGate.NOT_APPROVED),
-                gate(approved, FROM.minusSeconds(1), true).rejection("V1", "CAM1", START, 2));
+                gate(approved, FROM.minusSeconds(1)).rejection("V1", "CAM1", START, 2));
     }
@@ -83,3 +77,3 @@
                 ApprovalStatus.APPROVED, FROM, UNTIL);
-        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(other, NOW, true).rejection("V1", "CAM1", START, 2));
+        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), gate(other, NOW).rejection("V1", "CAM1", START, 2));
     }
@@ -88,3 +82,3 @@
         ApprovalSourceException failure = new ApprovalSourceException("register unreadable");
-        VisitorGate gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC), true);
+        VisitorGate gate = new VisitorGate((b, i, s, e) -> { throw failure; }, Clock.fixed(NOW, ZoneOffset.UTC));
         assertSame(failure, assertThrows(ApprovalSourceException.class, () -> gate.rejection("V1", "CAM1", START, 2)));
@@ -99,3 +93,3 @@
         };
-        new VisitorGate(sourceOf(record(ApprovalStatus.APPROVED)), counting, true).rejection("V1", "CAM1", START, 2);
+        new VisitorGate(sourceOf(record(ApprovalStatus.APPROVED)), counting).rejection("V1", "CAM1", START, 2);
         assertEquals(1, instants.get());
@@ -103,4 +97,4 @@
 
-    @Test void theDisabledFactoryNeverReadsASource() {
-        assertEquals(Optional.of(VisitorGate.DISABLED), VisitorGate.disabled().rejection("V1", "CAM1", START, 2));
+    @Test void aGateWithNoRegisterApprovesNoVisitor() {
+        assertEquals(Optional.of(VisitorGate.NOT_APPROVED), VisitorGate.noApprovals().rejection("V1", "CAM1", START, 2));
     }
```

### 4.4 `after/ai-activity/README-draft.md`

```markdown
<!-- Author-written fictional AI output, constructed for offline review (it is not a recorded service response). -->
# Campus Equipment Lending System

A Java 11 application for reserving campus equipment, with support for students, staff and visiting researchers.

## Quick start

1. Build: `mvn package`
2. Run: `java -jar target/equipment-lending.jar`
3. Check everything: `mvn verify` runs all 230 tests, which pass in under 30 seconds.

## Features

- Visiting researchers are enabled by default. Set `-Dlending.visitors=false` to turn them off.
- Visitors may reserve CAM1 or CAM2 for one to three days when a sponsor approval matches.
- Sponsor approvals are read from a CSV file. The file is cached in memory for speed.
- If the borrower directory does not answer within one second, the system retries three times and then treats the borrower as a student.
- `scripts/pipeline.sh` runs five stages and deploys the application to the staging server.
- Architecture rules are enforced by `DependencyRulesTest`.
- The system is production-ready and safe for concurrent use.

## Demonstration

Run `bash scripts/demo.sh` to see visitors rejected and then approved.
```

### 4.5 `after/ai-activity/README-corrected.md`

```markdown
# Campus Equipment Lending System

A Java 17 teaching application for reserving campus equipment, with support for students, staff and visiting researchers. It is an in-memory system: there is no real borrower directory and no real sponsor-approval service.

## Quick start

1. Check the tools: `java -version` (Java 17 or later) and `mvn -version` (Maven 3.9.x).
2. Build and test: `mvn --batch-mode verify`. The expected result and the number of tests are in `docs/HANDOVER.md`.
3. See it work: `bash scripts/demo.sh`.
4. Run the smallest program: `java -cp target/classes edu.se506.lending.bootstrap.ReservationApplication`. It confirms one reservation for borrower B1. The jar built by `mvn package` has no main class, so it cannot be started with `java -jar`.

## What it does

- Visiting researchers are **disabled by default**. The demonstration program enables them with `-Dlending.visitors=true`.
- A visitor may reserve CAM1 or CAM2 for one to three days when a sponsor approval matches the borrower, the item and the exact period and is valid at the request time.
- Sponsor approvals are read from a tab-separated file with a fixed header and eight columns. The file is read again on every request.
- The borrower directory is asked once, with a default wait of one second (`-Dlending.directory.timeout.millis`). There is no retry and no fallback. If it cannot answer, the request fails and is reported as unavailable, never as "not found" and never as a student.
- `scripts/pipeline.sh` runs five stages (compile, unit tests and architecture checks, integration tests, end-to-end journeys, package). It deploys nothing. `scripts/simulate-release.sh` simulates delivery into a local folder.
- `DependencyRulesTest` checks that package dependencies point the right way and that there are no package cycles.

## Limits

No Java 17 run and no hosted CI run has been made. The directory and the approval file are stand-ins. Concurrent use was not considered. See `docs/KNOWN-ISSUES.md`.
```

## 5. Worked explanation and evidence

### 5.1 The change footprint

The figures of Section 14.1 come from comparing the Chapter 11 and the Chapter 13 checkpoints with `diff -rq`, excluding build output, and counting lines.

| Group | Files | Lines |
|---|---|---|
| New production files | 9 | 399 (63 + 15 + 9 + 73 + 53 + 6 + 16 + 92 + 72) |
| Existing production files changed | 5 | 21 added, 3 removed |
| New test files | 10 | 992 |
| Existing test files changed | 3 | 10 added, 4 removed |
| New scripts, workflow and record | 4 | 213 |
| README and POM changed | 2 | 14 added, 8 removed |

The five existing production files are `BorrowerCategory` (+1 −1), `DirectoryReservationService` (+14), `ReservationApplication` (+3 −1), `LegacyDirectoryAdapter` (+1) and `LegacyDirectoryClient` (+2 −1). A changed line counts as one added and one removed.

### 5.2 Three experiments on the same change

Each was run in its own scratch copy.

| Experiment | Starting point | Edit | Result |
|---|---|---|---|
| E1 | Chapter 11 checkpoint (159 invocations) | Add `VISITOR` to the enum only | 45 of 159 fail (1 failure, 44 errors). 89 lines of output say `Missing policy: VISITOR`; the one failure is `RepositoryBoundaryTest.coordinatorRequiresARepository`, which expects a `NullPointerException` and gets an `IllegalArgumentException` |
| E2 | The same | The enum, `VisitorReservationRules` and the composition root | 5 of 159 fail, in the three files that build their own policy map: `LegacyRegressionTest.chapter06`, `BehaviourStrategyTest.injectedPolicyChangesDecisionWithoutChangingCoordinator`, and three tests in `RepositoryBoundaryTest`. With the four map entries added, all 159 pass |
| E3 | Chapter 13 checkpoint (232 invocations) | `LegacyDirectoryAdapter` maps kind `V` to `BorrowerCategory.STAFF`; nothing else | 4 of 232 fail: the three end-to-end journeys and `DirectoryOutageIntegrationTest.aVisitorIsServedThroughTheRealDirectoryAndTheRealApprovalFile`. All 203 unit invocations pass. With the flag off, visitor V1 is **confirmed**; V2 is rejected only because CAM2 is already taken, with `Rejected: item unavailable.`, not because it is unapproved |
| B1 | Chapter 14 checkpoint (235 invocations) | Remove the visitor policy from `ReservationApplication.create` | 73 of 235 fail (3 failures, 70 errors) in 14 test classes; 146 lines of output say `Missing policy: VISITOR` (each failure is reported more than once). The classes: `VisitorAcceptanceTest` 19, `DirectoryOutageIntegrationTest` 10, `LoanServiceTest` 9, `AvailabilityTest` 8, `ReserveEquipmentCommandTest` 4, `LegacyRegressionTest` 4, `DirectoryAdapterTest` 4, `ReservationConsoleTest` 3, `NotificationPublisherTest` 3, `NotificationMockitoTest` 3, `Chapter13JourneyE2ETest` 3, `RepositoryBoundaryTest` 1, `OverdueBridgeTest` 1, `AvailabilityTddTest` 1 |

What E1 and E2 show is how far the fail-fast check reaches. Everything that is constructed through the composition root fails together when the policy is missing there, which is one fix; the tests that spell out their own map fail separately, which is four fixes. What E3 shows is that this suite has a gap, and that a smaller change can pass a whole stage and fail the next one. Notice what it does **not** show: that unit tests cannot see such a change. No unit test checks the adapter's mapping of the visitor code, so nothing in the unit stage goes through it. A focused adapter test would catch the change, and Section 6.2 (B8) says what it should check. The experiment found the hole by trying a change that goes through it, and Chapter 13's own tests do not close it: the exercise B8 asks the reader to.

### 5.3 Revised assumptions: notes for the table in Section 14.1

- *Policy answers a count and duration question only.* Held: `VisitorReservationRules` is 16 lines and `BorrowingPolicy` was not widened. The approval needs identity and time, which a policy does not have, so the request-specific decision is in `VisitorGate`.
- *Every category has a policy in one place.* Held in production (one map in the composition root). Four test constructions also spelled out the map (Chapter 13 companion, Section 4.7).
- *The directory is a synthetic in-process provider with no transport (Chapter 8).* Chapter 8 already defined the provider's `Failure`, translated it to a `DirectoryException` and told an outage from an absence. Chapter 13 added the real HTTP client and the cases a transport brings, including a timeout that covers the whole answer, the body included. The contract held and the behaviour behind it grew.
- *Retained reservations are the count.* Open, SD-12, pinned by AC11.
- *The report knows two kinds.* Open, SD-11-1, shown by AC18.
- *One attempt, no retry.* Held for notices (Chapter 6) and extended to the directory.

### 5.4 The constructed review of the visitor change

This review is **author-written and fictional**, constructed for this chapter. No real peer review of the project has taken place. The point of the exercise is to check each comment against the code instead of accepting or rejecting it by tone.

| # | Comment | Check | Verdict |
|---|---|---|---|
| R1 | “`DirectoryReservationService` now branches on `VISITOR`. Will that grow?” | Read the class: one `if` on the category, delegating to the gate. | Valid. Recorded as KI-14 with its trigger (a second special category). No code change |
| R2 | “Where is the flag read in production? I cannot find a global.” | Search for `lending.visitors`: only `Chapter13Demo` reads it, and passes a boolean to `VisitorGate`. There is no static state. | No issue |
| R3 | “Is the old two-argument service constructor still safe for visitors?” | `ac12_...` builds a service with the two-argument constructor and asserts the disabled rejection. | Covered |
| R4 | “The README says 230 tests. I count 233 after this change.” | The count appeared in both `README.md` and `HANDOVER.md`. | Valid. A number stated in two places rots. The README now states no number, and `scripts/handover-check.sh` checks the numbers in `HANDOVER.md` |

R4 is the useful one: it led to a change in the checkpoint, and the change has a check.

### 5.5 The dry run, in order

The handover was followed in a fresh folder, as a reader would, before the fixes were made:

1. Step “check the tools”: `mvn -version` was **not found** on the machine's path. The scripts printed `mvn: command not found`. *Finding D1.* Fix: the document starts with a tool check and says what to do; the scripts print a clear message and exit with status 2.
2. Step “build”: Maven 3.9.11 printed `WARNING` lines about `sun.misc.Unsafe` and the mocking library printed a dynamic-agent warning, on a recent JDK. The build ended with `BUILD SUCCESS`. *Finding D2.* Fix: the document lists them as things that are not errors.
3. Step “see it work”: there was no way to run the demonstration program without a directory service. *Finding D3 (KI-1).* Fix: `DemoRun` and `scripts/demo.sh`.
4. The new clear message was then run on the machine's real setup, with the Maven command given as a full path to a `.cmd` file. It **rejected the valid path**, because `command -v` does not accept a file that is not marked executable in the shell. *Finding D4.* Fix: also accept a file that exists. The handover check found this, not a reader.
5. The project was copied into a folder whose name contains spaces and run again. Nothing broke.

### 5.6 The rehearsal of the flag removal

The rehearsal was produced by a script in a scratch copy of the 0.14.0 checkpoint, and then written out as `rehearsal/remove-visitor-flag.patch`. It was verified in three ways: the patch applies to a fresh copy and gives a tree identical to the scratch copy; the full build of that tree passed; and `scripts/handover-check.sh` passed in it.

| File | Change |
|---|---|
| `VisitorGate.java` | Removes `DISABLED`, the `enabled` field and parameter and the `disabled()` factory; adds `noApprovals()` (a gate whose source never has a record) |
| `DirectoryReservationService.java` | The two-argument constructor uses `VisitorGate.noApprovals()` |
| `Chapter13Demo.java` | No `lending.visitors` property and no `Visitors enabled` line |
| `VisitorGateTest.java` | Drops the flag argument; removes the two disabled tests; adds `aGateWithNoRegisterApprovesNoVisitor` |
| `VisitorAcceptanceTest.java` | `World` has no flag; AC12 becomes “no register approves no visitor”; AC13 and AC16 are renamed |
| `Chapter13JourneyE2ETest.java` | Removes the flag-off journey, so two journeys remain |
| `DirectoryOutageIntegrationTest.java` | `disabled()` becomes `noApprovals()`; constructor calls lose the flag |
| `DemoRun.java` | Runs once |
| `REQUIREMENTS-TO-EVIDENCE.md` | C9, C10, AC12, AC13 and AC16 point at the new names |
| `HANDOVER.md`, `handover-check.sh` | The expected counts: 233 in total, 205 in stage 2, 26 in stage 3, 2 in stage 4 |

Eleven files; 87 lines added and 131 removed. The prose of `README.md`, the rest of `HANDOVER.md` and ADR-013 is **not** edited by the patch, and it still says that the flag exists.

Two things worth noticing. `TraceabilityTest` is why the table edits are in the patch: without them, the build fails after the patch on the first stale test name, which is the check doing its job. And the specification changed, not just the code: AC12 as written (a disabled flag rejects explicitly) has no meaning without a flag.

### 5.7 The contribution fixture

The numbers are **synthetic**. P1: 38 commits (17 formatting only), 410 lines changed, 4 reviews given (1 requested changes). P2: 9 commits, 1,150 lines, 11 reviews (5 requested changes). P3: 24 commits (3 formatting only), 620 lines, 7 reviews (0 requested changes). The team total is 71 commits and 2,180 changed lines.

| Measure | Order | Share of the team total |
|---|---|---|
| Commits | P1, P3, P2 | P1 38 of 71 (more than half) |
| Lines changed | P2, P3, P1 | P1 410 of 2,180 (19%) |
| Reviews given | P2, P3, P1 | |
| Reviews that requested changes | P2, P1, P3 | |

The four orders are three different orders. The sentences about what the people did (a pipeline, an adapter, a demonstration and documents, four pair sessions of which two were recorded) are also synthetic. They are included to show what a count leaves out. Nothing in this fixture justifies a ranking.

## 6. Suggested practical solution

### 6.1 Book project, steps B1–B4

**B1. Predict and measure what breaks.** A good answer predicts before running: removing the one map entry in the composition root breaks everything built through it, which is most of the suite (the experiment gave 73 of 235, in 14 classes), and every message names the missing policy. It says what the result shows: the design fails fast and precisely, and the cost is breadth. It says what the result does not show: that the code is correct. Restore the file and rerun.

**B2. Triage.** A good answer applies the three questions to each item and gives a reason, for example:

| Item | Decision | Reason |
|---|---|---|
| KI-2 (SD-11-1, visitor late-fine rate) | Defer | Needs the records office; any rate would be a guess |
| KI-7 (whole-file rejection of the register) | Accept | A silent skip could hide a lost approval or a duplicate; revisit with real use |
| KI-8 (one-second wait, not measured) | Accept | It is a setting; measure before changing |
| KI-12 (no Java 17 or hosted CI run) | Defer | Needs a JDK 17 and a hosted runner |
| KI-14 (the `VISITOR` branch) | Accept | Fine for one category; refactor at the second |

A good new item comes from reading the project, not from the list: for example, that `DemoRun` fixes the clock, so the demonstration cannot show an approval that expires (a limitation of the demonstration, accepted), or that nothing checks the README's description of the architecture packages.

**B3. Follow the handover.** A good answer lists each place the reader guessed. Likely ones: where the project directory is, how to set `CHAPTER_MVN`, what the warnings mean, and how long the build takes. It also notes what did not need a guess.

**B4. Trace and break a row.** A good answer opens the test for each of its three rows and says whether it checks the claim. Example: C5 (valid at request time, start inclusive and end exclusive) is checked by `VisitorGateTest.theWindowIncludesItsStartAndExcludesItsEnd`, which tests exactly the two edges and one instant before the start. After renaming a named test, `TraceabilityTest` fails with the row's ID and the missing name. What it cannot catch: a row that names a different but existing test (Section 10.2, fault 6).

### 6.2 Book project, optional steps B5–B7

**B5. Rehearse the removal.** Apply the patch from inside a scratch copy of `after`: `patch -p1 < rehearsal/remove-visitor-flag.patch`. Run `mvn --batch-mode verify` (233 invocations) and `bash scripts/handover-check.sh` (passes). A good answer lists what still says the flag exists: `README.md` (the paragraph about the flag), `docs/HANDOVER.md` section 6 (the visitor flag), `docs/ADR-013-visiting-researchers.md` (the flag removal plan and the rollback), `docs/KNOWN-ISSUES.md` (KI-13) and `docs/REQUIREMENTS-TO-EVIDENCE.md` (the descriptions are updated; the contract text in Chapter 12 is not).

**B6. AI activity.** See Section 7.

**B7. Read a contribution fixture.** A good answer asks questions, for example “What are the seventeen formatting-only commits, and were they needed?” (read the commit list), “What did P2's two review findings say?” (read the review comments), “Which of P3's pair sessions were with P1, and what was produced?” (read the pull requests and the retrospective notes). It does not conclude that P1 contributed most because of 38 commits, and it does not conclude that P2 contributed least because of 9.

**B8. Close the gap that E3 found.** A good answer adds a unit test class for `LegacyDirectoryAdapter` that uses an in-memory client (no network) and checks at least: a row with kind `V` and status `Y` maps to `BorrowerCategory.VISITOR` (and not to staff or student); a row with kind `V` and status `N` gives an empty result; and an unknown kind code throws `DirectoryException` and is never defaulted. Then it applies the one-line change of Section 14.1 and shows that the **unit** stage now fails. A weak answer adds a test that passes against the changed adapter too, for example one that only checks that a visitor is found. The new unit tests also raise the stage-2 count, so `scripts/handover-check.sh` and `docs/HANDOVER.md` need their numbers updated, which is the handover check doing its job.

### 6.3 Team project, steps T1–T5

These are not model answers, because the code is your team's. A good answer shows:

- **T1:** the four questions answered with real evidence: the list of files changed and what each does; the tests that broke when the change started, and what that says; two or three assumptions the change overturned, with the chapter or document where they were written; actual review comments with responses. It names at least one place where the design bent.
- **T2:** a known-issues list in which every item has a decision, a reason, and (for a deferred item) an owner and a trigger; no feature added; a freeze time.
- **T3:** the bundle (setup, usage example, limitations, test instructions, requirements-to-evidence table, demonstration outline); a dry run in a fresh copy; a record of what a person outside the team struggled with, and what was changed; at least one statement in the bundle that a script checks.
- **T4:** two decision records with a true status, one about the flag or the change (the conditions for removal checked one by one, and a decision) and one other; the old record untouched if the new one applies or supersedes it.
- **T5:** at most three retrospective actions with owners, each tied to evidence; an individual reflection of claims with links and honest limits; the checklist of Section 14.7 with each item marked complete or a gap.

A weak answer describes the code instead of the change, lists defects with no decision, writes documents nobody has followed, edits an accepted decision record, ranks people by commit counts or claims a run that did not happen.

## 7. AI activity solution

The fixture makes sixteen statements. Each was checked by running the command or reading the code and tests it depends on.

| # | Statement | Verdict | Evidence and correction |
|---|---|---|---|
| 1 | A Java 11 application | **Contradicted** | `maven.compiler.release` is 17, and `javac --release 11` on the main sources fails at `behaviour/LifecycleExamples.java`: `switch rules are not supported in -source 11`. A Java 17 application |
| 2 | Supports students, staff and visiting researchers | Supported | `BorrowerCategory`, ADR-013 |
| 3 | Build: `mvn package` | Supported | Produces `target/equipment-lending-0.14.0.jar` (it also runs the tests unless they are skipped) |
| 4 | Run: `java -jar target/equipment-lending.jar` | **Contradicted** | `java -jar target/equipment-lending.jar` prints `Error: Unable to access jarfile target/equipment-lending.jar` (the file name includes the version). With the right name, `java -jar target/equipment-lending-0.14.0.jar` prints `no main manifest attribute, in target\equipment-lending-0.14.0.jar`. The POM has no main class. Run the program with `java -cp target/classes edu.se506.lending.bootstrap.ReservationApplication`, which prints a notice and `Result: Confirmed: R1 for B1 on CAM1 [2026-10-20, 2026-10-22).` |
| 5 | `mvn verify` runs all 230 tests | **Contradicted** | 233 |
| 6 | ...which pass in under 30 seconds | Not established | A full `mvn verify` took about 21 seconds on the verification machine with the dependencies already cached. That is one run on one machine; do not promise a time |
| 7 | Visitors are enabled by default; `-Dlending.visitors=false` turns them off | **Contradicted** | The default is `false`: `Boolean.parseBoolean(System.getProperty("lending.visitors", "false"))`. The first run of `scripts/demo.sh` prints `Visitors enabled: false`. Correct: disabled by default; `=true` enables |
| 8 | A visitor may reserve CAM1 or CAM2 for one to three days when a sponsor approval matches | Supported | C2, C3, C4 of the requirements table |
| 9 | Approvals are read from a CSV file | **Contradicted** | Tab-separated with a fixed header and eight columns (`FileApprovalSource.HEADER`) |
| 10 | The file is cached in memory for speed | **Contradicted** | `theFileIsReadAfreshOnEveryCall`: a changed register is seen at once |
| 11 | If the directory does not answer within one second, the system retries three times and then treats the borrower as a student | **Contradicted** (the one-second default is correct) | One attempt, no retry, no fallback: `aServerErrorIsAnOutageNotANotFoundAndIsNotRetried` asserts exactly one request; the request fails with `Unavailable`. A borrower is never given a category the provider did not state |
| 12 | `scripts/pipeline.sh` runs five stages... | Supported | Compile, unit tests and architecture checks, integration, end-to-end, package |
| 13 | ...and deploys the application to the staging server | **Contradicted** | Stage 5 only packages. `scripts/simulate-release.sh` copies a jar into a local folder and is labelled a simulation. Nothing is deployed |
| 14 | Architecture rules are enforced by `DependencyRulesTest` | Partly supported | It checks the direction of dependencies between packages (and a separate test checks for cycles). It does not enforce every architecture rule |
| 15 | The system is production-ready and safe for concurrent use | **Not established, and contradicted by the project's own limits** | KI-10 and KI-11: stand-in directory and register; concurrency not considered; an in-memory teaching system |
| 16 | Run `bash scripts/demo.sh` to see visitors rejected and then approved | Supported | The output of Section 1.2 |

Of sixteen statements, six are supported or partly supported as written, eight are contradicted and two are not established. (Counting statements, not sentences: statements 5 and 6 split one sentence.) The corrected README is `ai-activity/README-corrected.md`. Each command in it was run, and its claims were checked against the same evidence.

Notice which errors reading alone reveals and which only a run does. A reader who knows the project notices the default of the flag and the CSV. Nobody notices that `java -jar` fails without running it, because the sentence is exactly what a README usually says. And a draft in which half of the statements are contradicted reads as fluently as one that is right. Notice also that the draft says nothing about limitations, and that the corrected README adds them.

If a live assistant is used, keep its actual output, and check its README the same way. Do not use a generated README to approve generated code.

## 8. Intentionally flawed alternatives

These fragments are **diagnostic alternatives**, not files to compile. Each corresponds to a mistake in Section 14.9 of the chapter or to a fault in the experiments of Section 10.2.

### 8.1 A number stated in two places

```text
README.md:    "The build executes 230 JUnit invocations ..."
HANDOVER.md:  "Expected: Tests run: 233 ..."
```

One of them is stale the moment a test is added, and a reader cannot tell which. State a number once, and have a script check it.

### 8.2 A decision record edited after the fact

```markdown
# ADR-013 ...
Status: Accepted
...
- Introduce one flag ... (edited on 20 October: the flag was removed)
```

The reasons the team had at the time are gone. Write a new record that applies or supersedes the old one, and leave the old one readable.

### 8.3 A guess presented as a fix

```java
// WRONG for a handover sprint: nobody knows the visitor rate.
private static final FinePolicy VISITOR = new FinePolicy(2, 0.50, 10.00);
```

It looks like a repair of SD-11-1. It is a new rule, it hides the question and it changes AC18. Defer it with the question and the owner.

### 8.4 A ranking by counts

```text
Contribution: P1 54%, P3 34%, P2 13%   (by commits)
```

Habits are not contributions, and the same team has three other orders by other counts (Section 5.7). Use a count to choose which artefact to read.

### 8.5 A claim that did not happen

```text
CI: passing on GitHub Actions
```

The workflow file has never run. Say `workflow file written, not run` and keep the local run as the evidence.

## 9. Review answers and transfer solution

### 9.1 Concept answers

**1. The four questions.** Which responsibilities were affected (file and line counts do not show importance); what broke when the change started (shows only what the tests cover); which assumptions turned out wrong (only those that were written down); what a reviewer said (only as good as the review).

**2. A one-line change that fails four tests.** The change is smaller than the requirement: it does not implement the flag, the register check or the failure behaviour. The unit tests cannot say so, because none of them goes through the directory adapter with a real visitor. The stage that crosses the real boundary does, which is the reason to have it.

**3. Deferred and accepted.** A deferred issue is waiting for a decision that is not ours, so it carries an owner and a trigger (SD-11-1, the late-fine rate). An accepted issue is a limit we decided to live with, so it carries a reason and a statement (the one-second wait, not measured; no retry).

**4. A requirements-to-evidence check.** It can confirm that a named test or class exists and that each acceptance example has exactly one row. It cannot confirm that the named test is the right evidence for the requirement. A reviewer does that.

### 9.2 Applied diagnosis answers

**5. 40 commits against 8.** Questions: Are most of the 40 formatting, generated or reverted? (read the commit list.) What are the eight? (read the diffs and the pull requests.) Who reviewed whom, and what did the reviews find? (read the review comments.) Was there pair work recorded as one author? (read the commit trailers and the retrospective.) Say nothing about contribution until the artefacts are read.

**6. A colleague adds a test.** Two things that could notice: `scripts/handover-check.sh`, which compares the pipeline's stage counts with what the handover promises (cost: it runs the whole pipeline in a fresh copy, about a minute); and a reviewer reading the pull request who knows the number is stated in the handover (cost: attention, and it relies on memory). The script is cheaper to repeat.

### 9.3 Transfer solution

For the model-serving team:

| Item | Content |
|---|---|
| README for a stranger | What the service does; what it needs (language runtime, build tool, a model file or a synthetic stand-in); three commands with their expected output; where the decisions are |
| Tool check | The runtime and tool versions with the output they should print; what to do if a tool is missing; the warnings that are not errors |
| Demonstration | A fixed model identifier and fixed synthetic data, a fixed clock if time matters, and a script that runs the same requests with the gate off and on |
| Requirements to evidence | Each rule (only approved model versions are served to external callers) to the class that decides it and the test, plus a check that the names exist |
| Known issues | Including what was **not** evaluated about the model: accuracy, fairness, drift, behaviour on data unlike the synthetic data |
| Decision record | The flag that gates a model version: the conditions for removal, the owner, what rollback does not undo (responses already served) |
| Limits statement | No real model evaluated; synthetic identifiers; no load test; no hosted run if none was made |

### 9.4 Quiz and revision pointers

None. This chapter adds no assessed content beyond the descriptor's final project, and it creates no new rubric.

## 10. Instructor notes

### 10.1 Suggested demonstration and review

Run `scripts/handover-check.sh`, then break one thing (add a trivial test, or edit a number in `HANDOVER.md`) and run it again. Rename one test named in the requirements table and run `TraceabilityTest`. Show experiment E3: a one-line change that passes the whole unit stage. Ask the class which stage should have caught it and why. Let students predict B1's failure count before running it.

For the Team project, the review is of the bundle and not of the code: ask for the dry-run record, the person outside the team who followed it, the triage decisions and the statement of what was not run. Ask each student for one artefact that shows what they did. A weak answer to “what was not run?” is “nothing”.

### 10.2 Do the checks detect faults?

*`TraceabilityTest`.* Six faults were applied one at a time to a copy of the project and the test was run each time.

| Fault | Result |
|---|---|
| A named test is renamed | **Caught**: two of the three methods fail |
| An acceptance example loses its row | **Caught**: two of the three methods fail (the row check, and the minimum of 29 named tests) |
| A deciding class is renamed in the table (`VisitorGuard`) | **Caught**: the class check fails |
| An acceptance test is added that no row mentions | **Caught**: the row check fails |
| A row names an extra test that exists | **Not caught**; harmless |
| AC3 is pointed at the AC1 test, which exists | **Not caught**; a wrong mapping that only a reviewer finds |

*`scripts/handover-check.sh`.* Three faults, each run through the whole script: a test added (stage 2 shows 207 invocations: `FAIL stage 2 ran 206 invocations`, one problem); a word changed in the demonstration's output (`FAIL an outage is reported as unavailable`, and the pipeline fails too, because the end-to-end journeys check the same line: three problems); and `HANDOVER.md` edited to promise 232 invocations (`FAIL HANDOVER.md promises 235 invocations in total`, one problem). All three were caught.

These are a few faults, chosen by the author, in two small checks. They say nothing about how these checks compare with others. They show that the checks notice the faults that make a document disagree with a run, and that they do not notice a document that is wrong in a way the script cannot see.

The results establish the selected behaviours on the supplied inputs. They do not establish that the handover is followable by a reader on another machine.

## References

The online references of the student chapter (sources 1–9) were opened on 13 October 2026; see the chapter for the source context.

1. Nygard, M., [Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
2. [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
3. Schwaber, K. and Sutherland, J., [The Scrum Guide](https://scrumguides.org/scrum-guide.html).
4. [Retrospective Wiki: The Prime Directive](https://retrospectivewiki.org/index.php?title=The_Prime_Directive).
5. Fowler, M., [Yagni](https://martinfowler.com/bliki/Yagni.html).
6. GitHub, [Why are my contributions not showing up on my profile?](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/troubleshooting-missing-contributions).
7. GitHub, [Creating a commit with multiple authors](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors).
8. GitHub, [About pull request reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews).
9. Hodgson, P., [Feature Toggles (aka Feature Flags)](https://martinfowler.com/articles/feature-toggles.html).