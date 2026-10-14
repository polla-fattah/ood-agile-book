---
title: "Appendix B Companion: Code, Explanations and Solutions"
weight: 220
description: "Code explanations and solutions for Appendix B Companion: Code, Explanations and Solutions."
---

*Tools and Reproducible Setup*  
*OO Development and Agile Practices*

## 1. Scope and use

This file accompanies Appendix B, Tools and Reproducible Setup. It supplies a complete small starter project, a scripted Git walk-through, explanations of each file and the answers to the activity in B.12.

The starter is an **isolated Book example**, not a lending-project version. Its only purpose is to show that the toolchain works: a Java 17 release target, Maven with pinned JUnit and Mockito, two Bash scripts and a hosted-check file. It does not change the project and its tests do not belong in the project's test totals.

Save every listing in Section 2 at its path inside one new folder, for example `toolchain-check`. Use a Java 17 or later JDK, Git Bash or a Linux or macOS terminal, and Maven 3.9.11. From that folder:

```bash
bash scripts/check-setup.sh
bash scripts/check.sh
```

The first Maven build needs access to Maven Central. If your machine has no network access, build once somewhere that has it and copy the populated local Maven repository folder across, then run with the two variables below. `CHAPTER_M2` names that folder and `CHAPTER_OFFLINE=1` makes Maven use only what it holds:

```bash
CHAPTER_M2=/path/to/repository CHAPTER_OFFLINE=1 bash scripts/check.sh
```

If `mvn` is not on the path, give the full path to the Maven launcher in `CHAPTER_MVN` (on Windows it ends in `mvn.cmd`).

## 2. Complete starter files

### 2.1 `pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>edu.se506</groupId>
  <artifactId>toolchain-check</artifactId>
  <version>0.1.0</version>
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

### 2.2 `src/main/java/edu/se506/setup/ToolchainReport.java`

```java
package edu.se506.setup;

/** Reports which Java runtime is executing and which release the code was compiled for. */
public final class ToolchainReport {
    /** The language and API level the build targets (see maven.compiler.release in pom.xml). */
    public static final int RELEASE_TARGET = 17;

    private ToolchainReport() {
    }

    public static int javaFeatureVersion() {
        return Runtime.version().feature();
    }

    /** Code compiled for a release runs on that Java version and on every later one. */
    public static boolean canRunOn(int runtimeFeature) {
        return runtimeFeature >= RELEASE_TARGET;
    }

    public static String summary() {
        return "Running on Java " + javaFeatureVersion()
                + "; compiled for release target " + RELEASE_TARGET;
    }

    public static void main(String[] args) {
        System.out.println(summary());
    }
}
```

### 2.3 `src/test/java/edu/se506/setup/ToolchainReportTest.java`

```java
package edu.se506.setup;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class ToolchainReportTest {

    @Test
    void theRunningJavaCanRunCodeCompiledForTheTarget() {
        assertTrue(ToolchainReport.canRunOn(ToolchainReport.javaFeatureVersion()));
    }

    @Test
    void theSummaryNamesTheReleaseTarget() {
        assertTrue(ToolchainReport.summary().endsWith("compiled for release target 17"));
    }

    @ParameterizedTest
    @ValueSource(ints = {17, 21, 24})
    void javaVersionsAtOrAboveTheTargetCanRunTheCode(int runtimeFeature) {
        assertTrue(ToolchainReport.canRunOn(runtimeFeature));
    }

    @Test
    void aJavaVersionBelowTheTargetCannotRunTheCode() {
        assertFalse(ToolchainReport.canRunOn(16));
    }
}
```

### 2.4 `src/test/java/edu/se506/setup/GreeterMockTest.java`

```java
package edu.se506.setup;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;

/** Checks that Mockito is configured. It tests the framework setup, not any domain behaviour. */
class GreeterMockTest {

    interface Greeter {
        String greet(String name);
    }

    @Test
    void aMockOfAnInterfaceAnswersWhatItIsTold() {
        Greeter greeter = mock(Greeter.class);
        when(greeter.greet("Ada")).thenReturn("Hello, Ada");

        assertEquals("Hello, Ada", greeter.greet("Ada"));
        verify(greeter).greet("Ada");
    }
}
```

### 2.5 `src/test/resources/mockito-extensions/org.mockito.plugins.MockMaker`

```text
mock-maker-proxy
```

### 2.6 `scripts/check-setup.sh`

```bash
#!/usr/bin/env bash
# Reports whether the tools the book needs are on the PATH and recent enough.
# It changes nothing and downloads nothing. A line that starts with OK, MISSING or TOO-OLD
# is easy to search for; the exit status is 1 if any required tool is not usable.
# CHAPTER_MVN optionally names the Maven command (default: mvn).
set -u

MVN="${CHAPTER_MVN:-mvn}"
status=0

report() {
  printf '%-8s %s\n' "$1" "$2"
}

# Report the first line of the output of a tool's version command.
need() {
  local label="$1"
  shift
  if command -v "$1" >/dev/null 2>&1 || [ -f "$1" ]; then
    report "OK" "${label}: $("$@" 2>&1 | head -1)"
  else
    report "MISSING" "${label}: '$1' is not on the PATH"
    status=1
  fi
}

need "bash" bash --version
need "git" git --version
need "java" java -version
need "maven" "$MVN" --version

if command -v javac >/dev/null 2>&1; then
  feature="$(javac -version 2>&1 | sed -n 's/^javac \([0-9][0-9]*\).*/\1/p')"
  if [ "${feature:-0}" -ge 17 ]; then
    report "OK" "javac: compiler version ${feature} can compile with --release 17"
  else
    report "TOO-OLD" "javac: version '$(javac -version 2>&1)' cannot compile with --release 17; install a JDK of version 17 or later"
    status=1
  fi
else
  report "MISSING" "javac: a JDK (not only a JRE) is needed"
  status=1
fi

if [ "$status" -eq 0 ]; then
  echo "SETUP OK"
else
  echo "SETUP INCOMPLETE"
fi
exit "$status"
```

### 2.7 `scripts/check.sh`

```bash
#!/usr/bin/env bash
# The one command that decides whether the starter is healthy: compile, run every test, package.
# CHAPTER_MVN names the Maven command (default: mvn). CHAPTER_M2 optionally names a local Maven
# repository, and CHAPTER_OFFLINE=1 stops Maven from contacting any remote repository.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

MVN="${CHAPTER_MVN:-mvn}"
ARGS=(--batch-mode)
if [ -n "${CHAPTER_M2:-}" ]; then
  ARGS+=("-Dmaven.repo.local=${CHAPTER_M2}")
fi
if [ "${CHAPTER_OFFLINE:-0}" = "1" ]; then
  ARGS+=(--offline)
fi

"$MVN" "${ARGS[@]}" verify
java -cp target/classes edu.se506.setup.ToolchainReport
echo "BUILD AND TESTS PASSED"
```

### 2.8 `.gitignore`

```gitignore
/target/
/build/
*.class
```

### 2.9 `.gitattributes`

```gitattributes
*.sh text eol=lf
```

### 2.10 `.github/workflows/verify.yml`

```yaml
name: Verify

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-java@v6
        with:
          distribution: temurin
          java-version: '17'
          cache: maven
      - name: Build and test
        run: bash scripts/check.sh
```

### 2.11 `README.md`

````markdown
# Toolchain check

A small project that shows the book's toolchain works: a Java 17 release target, Maven 3.9.11
with JUnit Jupiter 5.13.4 and Mockito 5.20.0, and the Bash scripts. It is not part of the lending project.

## Check the tools

```bash
bash scripts/check-setup.sh
```

Every line should start with `OK`, and the last line should be `SETUP OK`.

## Build and test

```bash
bash scripts/check.sh
```

Expect `BUILD SUCCESS`, seven test invocations (five test methods; one is parameterised with
three values), the line `Running on Java N; compiled for release target 17` and, last,
`BUILD AND TESTS PASSED`. A failing test must stop the script with a non-zero exit status.

Optional variables: `CHAPTER_MVN` names the Maven command, `CHAPTER_M2` names a local Maven
repository folder and `CHAPTER_OFFLINE=1` stops Maven from contacting any remote repository.
````

## 3. Worked explanation

### 3.1 The POM

`maven.compiler.release` set to 17 makes the Compiler plugin pass `--release 17` to `javac`, so the build rejects any API newer than Java 17 even on a newer JDK (B.1). `project.build.sourceEncoding` fixes the source encoding so that the build does not depend on the machine's default.

Both dependencies have the scope `test`: they are on the class path for the tests and absent from the packaged application. `junit-jupiter` is an aggregate artifact that brings the API, the parameterised-test support and the engine. Every plugin that the book relies on has an exact version, so a build today and a build next year resolve the same plugins. The Surefire setting `failIfNoTests` makes a build with no tests fail. Without it, a mistyped test location can produce an empty run that looks green, the same reason Chapter 13's pipeline fails a stage that selects no tests.

### 3.2 The two scripts

`check-setup.sh` deliberately does not use `set -e`. It has to examine every tool and report all the problems in one run, so it records a status and exits with it at the end. The helper `need` runs a tool's version command and prints the first line of its output; the extra test `[ -f "$1" ]` accepts a tool named by a full file path, which `command -v` does not always accept for a Windows `.cmd` launcher. The compiler gets its own check because a machine can have a Java runtime and no compiler, and because a compiler older than 17 cannot honour `--release 17`.

`check.sh` is the opposite: it is a gate. `set -euo pipefail` stops it at the first failing command and makes unset variables an error, so the success message at the end cannot appear unless Maven succeeded. The script changes into the project folder first, so it works from any directory. It reads three optional variables and builds the Maven argument list from them, which keeps the same file usable on a laptop, on a machine with no network and in a hosted check.

### 3.3 The tests

`ToolchainReportTest` has four methods and six invocations because one method is parameterised with three values. The first method checks that the Java running the test can run code built for the target. The summary test pins the exact wording that reports the target. The parameterised test checks the boundary at 17 from above, and the last method checks it from below with 16, the same two-sided reading you practised on the borrowing limit in Appendix A. `GreeterMockTest` creates a mock of an interface, tells it what to return and verifies the call. It checks that Mockito is configured, not any domain behaviour; do not copy that pattern into a design test.

### 3.4 Repository files

`.gitignore` keeps generated output out of the repository. `.gitattributes` keeps shell scripts in LF form on Windows. The workflow runs `scripts/check.sh` after installing Java 17, so the hosted run and the local run are the same command. The workflow's action versions are those named in B.1; check the current versions before you reuse it, because tags and runner images change. It has no effect until it runs on a repository, and it can be started by hand through `workflow_dispatch`.

## 4. Expected output

The setup check on a machine where everything is in place (the version text will differ):

```text
OK       bash: GNU bash, version 5.3.9(1)-release (x86_64-pc-cygwin)
OK       git: git version 2.54.0.windows.1
OK       java: java version "24.0.2" 2025-07-15
OK       maven: Apache Maven 3.9.11 (3e54c93a704957b63ee3494413a2b544fd3d825b)
OK       javac: compiler version 24 can compile with --release 17
SETUP OK
```

The build, reduced to its important lines:

```text
[INFO] Compiling 1 source file with javac [debug release 17] to target\classes
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0 ... in edu.se506.setup.GreeterMockTest
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0 ... in edu.se506.setup.ToolchainReportTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
Running on Java 24; compiled for release target 17
BUILD AND TESTS PASSED
```

The `Java N` figure is the runtime you used. Maven and Mockito may print the warnings described in B.4 and B.5 between these lines.

## 5. A small fault experiment

In a separate copy of the starter, make one change at a time, run the named command and then discard the copy. Each experiment checks that a particular gate notices a particular fault.

| Change | Command | What must happen |
|---|---|---|
| Name a Maven command that does not exist: `CHAPTER_MVN=/nonexistent/mvn` | `bash scripts/check-setup.sh` | A `MISSING  maven` line, `SETUP INCOMPLETE` and exit status 1. |
| Put a fake `javac` that prints `javac 1.8.0_999` first on the path | `bash scripts/check-setup.sh` | A `TOO-OLD  javac` line and exit status 1. |
| In `ToolchainReport.canRunOn`, change `>=` to `>` | `bash scripts/check.sh` | One failing invocation (the parameterised case for 17), `BUILD FAILURE`, a non-zero status, and no `BUILD AND TESTS PASSED` line. |
| The same change | `mvn --batch-mode -DskipTests verify` | `Tests are skipped.` and `BUILD SUCCESS`: the fault is not detected. |
| The same change | `mvn --batch-mode -Dmaven.test.failure.ignore=true verify` | The failure is printed, yet `BUILD SUCCESS` and exit status 0: the fault is hidden. |

The last two rows show why a green build proves nothing unless you know what was run. They also correct two common habits: skipping tests is not a way to confirm that a project works, and telling Maven to ignore failures does not make failures go away. These experiments check that the gates catch the chosen faults. They do not establish that the starter is correct for every input or on every platform.

## 6. The Git walk-through

`git-walkthrough.sh` copies the starter into a work folder and then performs every command of B.8 in order: create the repository and a first commit, branch, inspect, stage, commit, discard an edit, unstage a file, revert a commit, merge, share through a bare repository and clone it again. The bare repository is a folder on the same machine, so no account and no network are involved. The author identity is set for the new repository only, and the script touches no global Git setting.

```bash
#!/usr/bin/env bash
# A complete Git walk in a throwaway folder: commit, branch, inspect, undo, merge and share.
# Usage: bash git-walkthrough.sh /path/to/starter /path/to/empty-work-folder
# It uses only local folders. The "remote" is a bare repository on this machine, so no account
# and no network are involved. The author identity is set for this repository only.
set -euo pipefail

STARTER="$1"
WORK="$2"
mkdir -p "$WORK"
cp -r "$STARTER/." "$WORK/project"
rm -rf "$WORK/project/target"
cd "$WORK/project"

step() { printf '\n--- %s\n' "$1"; }

step "1 create the repository and the first commit"
git init -b main
git config user.name "Example Student"
git config user.email "student@example.invalid"
git add README.md pom.xml src scripts .gitignore .gitattributes .github
git status --short
git commit -m "Add the toolchain starter"

step "2 a branch for one small change"
git switch -c feature/clearer-summary
FILE=src/main/java/edu/se506/setup/ToolchainReport.java
sed 's/Running on Java /Running on Java version /' "$FILE" > "$FILE.tmp"
mv "$FILE.tmp" "$FILE"
git status --short
git diff

step "3 stage it, compare staged and unstaged, commit"
git add "$FILE"
git diff --staged --stat
git diff --stat
git commit -m "Say 'version' in the runtime summary"

step "4 discard an edit, and unstage a file"
echo "/scratch/" >> .gitignore
git status --short
git restore .gitignore
git status --short
echo "notes" > NOTES.txt
git add NOTES.txt
git status --short
git restore --staged NOTES.txt
git status --short
rm NOTES.txt

step "5 reverse a commit by adding a new one"
git revert --no-edit HEAD
git log --oneline

step "6 merge back and look at the history"
git switch main
git merge feature/clearer-summary
git log --oneline --graph --decorate

step "7 share through a bare repository acting as the remote"
git init --bare -b main "$WORK/remote.git"
git remote add origin "$WORK/remote.git"
git push -u origin main
git push -u origin feature/clearer-summary
git branch -vv
git ls-remote --heads origin | cut -f2

step "8 a second clone sees the same history"
git clone "$WORK/remote.git" "$WORK/second-clone"
git -C "$WORK/second-clone" log --oneline | head -3
```

Run it from any folder:

```bash
bash git-walkthrough.sh /path/to/toolchain-check /path/to/new-empty-work-folder
```

The commit hashes, dates and folder paths in the output will differ. The important lines are these:

```text
--- 2 a branch for one small change
Switched to a new branch 'feature/clearer-summary'
 M src/main/java/edu/se506/setup/ToolchainReport.java
...
--- 4 discard an edit, and unstage a file
 M .gitignore
A  NOTES.txt
?? NOTES.txt
--- 5 reverse a commit by adding a new one
[feature/clearer-summary <hash>] Revert "Say 'version' in the runtime summary"
--- 6 merge back and look at the history
Fast-forward
* <hash> (HEAD -> main, feature/clearer-summary) Revert "Say 'version' in the runtime summary"
* <hash> Say 'version' in the runtime summary
* <hash> Add the toolchain starter
--- 7 share through a bare repository acting as the remote
 * [new branch]      main -> main
 * [new branch]      feature/clearer-summary -> feature/clearer-summary
```

Read step 3 carefully: after staging the file, `git diff --stat` prints nothing and `git diff --staged --stat` prints the change. An empty `git diff` after staging does not mean there is nothing to commit. In step 4, a file that has been staged shows `A` in the first column, and after `git restore --staged` it shows `??` again because it is untracked. Step 5 adds a third commit; the history now shows the original change and the commit that reverses it, not a rewritten past. Step 6 is a fast-forward because `main` had no commits of its own; on a branch that has diverged, the same command creates a merge commit.

On Windows you will also see lines such as `warning: in the working copy of '...', LF will be replaced by CRLF the next time Git touches it`. They are warnings from line-ending conversion (B.8), not failures. The script is not a model of a pull request: the review, the comments and the merge button belong to the hosting platform.

## 7. Answers to the activity in B.12

1. **Setup check.** `SETUP OK`. If a line starts `MISSING` or `TOO-OLD`, the named tool is the problem.
2. **First build.** Seven invocations from five test methods: one in `GreeterMockTest` and six in `ToolchainReportTest`, because the parameterised method contributes three. A good setup note says “seven invocations”, not “seven tests”.
3. **Fault.** With `>` the case 17 fails: `expected: <true> but was: <false>`. The script prints no success line and exits non-zero. Restoring `>=` makes it pass again.
4. **Branch and commit.** `git diff` shows the edit; after `git add`, `git diff` is empty and `git diff --staged` shows it; `git commit` records it.
5. **Setup note.** There is no single right answer. A useful note names the versions your machine reported (compare them with B.1), lists the commands run and records every difference from this appendix.

### The constructed AI candidate

The candidate in B.12 is constructed for teaching; it is not a captured model response.

| Candidate sentence | Verdict | Evidence and correction |
|---|---|---|
| “Any Java installation will do because the code is plain Java.” | Incorrect | The project needs a full JDK of version 17 or later: `check-setup.sh` reports a missing compiler and a compiler older than 17. A runtime alone cannot compile, and `--release 17` needs a compiler that supports it. |
| “To confirm a project works, run `mvn install -DskipTests`.” | Incorrect | `-DskipTests` prints `Tests are skipped.` and the build succeeds even when a test would fail (Section 5). It confirms that the code compiles and packages, not that it works. |
| “Add `-Dmaven.test.failure.ignore=true` so the build always passes.” | Incorrect | The failing test is still printed, but the build ends in `BUILD SUCCESS` with status 0 (Section 5). Hiding a failure is the opposite of checking. |
| “Share your work with `git add .` and `git push --force`.” | Unsafe | `git add .` stages everything, including files you did not mean to share; read `git status` and name the files. A forced push can overwrite commits other people have pulled. Push a branch normally and review it. |

An adequate record names the claim, the check and the conclusion. “The assistant was wrong” is weaker than naming the experiment that shows it.

## 8. Teaching and revision notes

Ask learners to predict each fault-experiment result before running it. The `-DskipTests` and failure-ignore rows are worth running in class: they take a minute and change how students read a green build. Learners on machines they do not control may be unable to install tools; the offline route is to run `check-setup.sh` on a lab machine, read the output and do B.12 steps 3 and 4 on paper.

Keep setup detail here and in Appendix B, not in the design chapters. When a pinned version changes, edit the table in B.1, the POM listings and the version lines in this file's README, and leave the design explanations alone. Do not add this starter's test count to the lending project's totals.

## References

1. Appendix B lists the official Maven, Git, JUnit, Mockito, PMD and GitHub Actions references that support the commands in this file.