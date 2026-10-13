---
title: "Appendix B: Tools and Reproducible Setup"
description: "Pinned toolchain, Maven build commands, PMD setup, and Git pull request workflows."
weight: 220
---

*OO Development and Agile Practices*  
*Designing, Testing and Evolving Software with AI Assistance*

## How to use this appendix

A design discussion is only useful if you can run the code it describes. This appendix records, in one place, the tools the book uses, the exact versions it pins, the commands that build and test the examples, and the Git and pull-request routine your team will follow. Chapters explain design and cite this appendix for setup, so that a change of tool does not force a rewrite of an explanation.

Start with B.1 and B.2: they tell you what to install and how to check it. Chapters 1 to 6 need only a JDK and a Bash shell. From Chapter 7 the examples use Maven. Use B.8 beside Chapter 2's Git exercise and again when your team starts its pull-request routine. The remaining sections are reference: look up a tool when a chapter first uses it.

This appendix records what works for the book's examples. It is not institutional policy. Your approved assessment instructions decide which tools you may use in an assessment, and a section here never grants permission. The Appendix B companion (in the Code, Explanations and Solutions companion) contains a complete small starter project (every file), a scripted Git walk-through and the answers to the activity in B.12.

## B.1 What you need, and when

| Tool | Needed from | Used for | What the book pins or requires |
|---|---|---|---|
| JDK (a full Java Development Kit, not only a runtime) | Chapter 1 | Compile and run | Version 17 or later. The examples are compiled with `--release 17`. |
| Bash | Chapter 4 | The check scripts | Git Bash on Windows; a terminal on macOS or Linux. |
| Git | Chapter 2 | Version control and review | Version 2.28 or later, because the commands use `git init -b`, `git switch` and `git restore`. |
| Apache Maven | Chapter 7 | Build, dependencies and tests | Version 3.9.11. |
| JUnit Jupiter | Chapter 7 | Unit tests | 5.13.4 (the `junit-jupiter` aggregate artifact). |
| Mockito | Chapter 7 | One interface-only test double | `mockito-core` 5.20.0. |
| Maven Compiler Plugin, Surefire | Chapter 7 | Compile with `--release 17`; run the tests | 3.14.1 and 3.5.4. |
| PMD | Chapter 5 only | The static-analysis lab | 7.28.0. |
| GitHub Actions | Chapters 4 and 13 | A hosted check | `actions/checkout@v7`, `actions/setup-java@v6`, Temurin 17. |
| An editor or IDE | Any | Writing code | Not pinned. Use what you know. |

**What “pinned” means.** A pinned version is named exactly, so that everyone who follows the book gets the same behaviour. The Maven versions live in each project's `pom.xml`; the others are named in this table. When a tool changes, this table and the POMs change and the design explanations stay as they are. Maven plugins that the POM does not name take the versions that Maven 3.9.11 itself binds; the two that appear in the examples are the Resources plugin (3.3.1) and the Jar plugin (3.4.1).

**Newer releases exist.** The Maven site lists a newer stable release than 3.9.11. The book's output was produced with 3.9.11, so use that version when you want to reproduce what the chapters show, and treat a newer one as your own experiment.

### Why the book compiles with `--release 17`

The examples use only the Java 17 language and library. If you compile with a newer JDK and no option, the compiler checks your code against that JDK's library, so you can call a method that does not exist in Java 17 and nothing complains until the program meets a Java 17 runtime. The option `--release 17` asks the compiler to check against the Java 17 language and library instead. The following program uses `getFirst()`, a method added to lists after Java 17:

```java
import java.util.List;

public class NewApi {
    public static void main(String[] args) {
        System.out.println(List.of("a", "b").getFirst());
    }
}
```

Compiled with plain `javac` on a recent JDK it succeeds and prints `a`. Compiled with `javac --release 17` it fails with `cannot find symbol` for `getFirst()`. The option restricts what the compiler accepts. It does not make a newer runtime behave like Java 17, so run `java -version` separately to see which runtime you have [1].

## B.2 Check your setup

The companion lists `scripts/check-setup.sh`. It changes nothing and downloads nothing; it reports whether each tool is on the path and whether the compiler is recent enough:

```bash
bash scripts/check-setup.sh
```

On a machine where everything is in place it prints one `OK` line per tool and ends with `SETUP OK`:

```text
OK       bash: GNU bash, version 5.3.9(1)-release (x86_64-pc-cygwin)
OK       git: git version 2.54.0.windows.1
OK       java: java version "24.0.2" 2025-07-15
OK       maven: Apache Maven 3.9.11 (3e54c93a704957b63ee3494413a2b544fd3d825b)
OK       javac: compiler version 24 can compile with --release 17
SETUP OK
```

The version text on your machine will differ. What matters is that no line starts with `MISSING` or `TOO-OLD`. A `MISSING` line names the command that is not on the path. A `TOO-OLD` line means the compiler cannot target Java 17; install a newer JDK. A runtime without `javac` is not enough, which is why the script checks the compiler separately.

**Installing.** Obtain a JDK of version 17 or later from the vendor your institution recommends. The book's hosted-check example uses the Eclipse Temurin build of Java 17 [2]. For Maven, the project's installation page says to extract the binary archive, add its `bin` directory to the `PATH`, make sure a JDK is found either through the `JAVA_HOME` variable or through `java` on the path, and confirm with `mvn -v` in a new shell [3]. To reproduce the book, take version 3.9.11 from the Apache archive, where each archive is published with a checksum file [4]:

```text
apache-maven-3.9.11-bin.zip
SHA-512  03e2d65d4483a3396980629f260e25cac0d8b6f7f2791e4dc20bc83f9514db8d0f05b0479e699a5f34679250c49c8e52e961262ded468a20de0be254d8207076
```

Compare it with the digest of your download (`sha512sum apache-maven-3.9.11-bin.zip`) before you unpack it. If the two differ, delete the file and download it again.

**Windows notes.** Use Git Bash for the scripts. Windows can have more than one program called `bash` on the path, among them the one from Git for Windows and the Windows Subsystem for Linux launcher, and the first one found runs your script. Scripts that assume Windows-style paths fail under the wrong one. The book's scripts take the Maven command from an optional variable, `CHAPTER_MVN`, for the case where `mvn` is not on the path or you call it by its full path; on Windows the launcher is `mvn.cmd`.

## B.3 Compile and run without a build tool (Chapters 1 to 6)

The early chapters use plain Java. A typical compile-and-check pair is:

```bash
javac --release 17 -Xlint:all -encoding UTF-8 -d build/classes src/main/java/*.java src/test/java/*.java
java -cp build/classes Chapter04Demo
```

`-Xlint:all` turns on every compiler warning category, `-encoding UTF-8` makes the source encoding explicit, `-d` names the output folder and `-cp` (class path) tells `java` where to find the compiled classes. The shell expands `*.java` into the files that are directly inside the two folders; it does not enter sub-folders, so a project that grows nested packages needs a build tool. Chapter 4's `scripts/check.sh` wraps these commands, stops at the first failure and ends with an explicit success message that appears only if everything before it passed. Appendix A's lab uses the same commands.

## B.4 Build and test with Maven (from Chapter 7)

Maven builds from a `pom.xml` that names the project, the Java release, the dependencies and the plugin versions. By convention, application code is in `src/main/java`, tests in `src/test/java` and test resources in `src/test/resources`. Generated files go to `target`, which Git ignores.

A Maven build moves through **phases** in a fixed order, and asking for a phase runs everything before it. The ones the book uses are `compile`, `test`, `package` and `verify` [5]. The command you will run most is:

```bash
mvn --batch-mode verify
```

`--batch-mode` removes interactive prompts and colour codes, so the output is the same in a terminal, in a script and in a hosted check. A successful run ends with `BUILD SUCCESS` and exit status 0; a failure prints `BUILD FAILURE` and returns a non-zero status, which is what scripts and hosted checks look at.

| Command | What it does |
|---|---|
| `mvn --batch-mode verify` | Compile, run all tests, package, verify. The normal check. |
| `mvn --batch-mode test` | Compile and run the tests only. |
| `mvn --batch-mode -Dtest=ToolchainReportTest test` | Run one test class. |
| `mvn --batch-mode "-Dtest=ToolchainReportTest#aJavaVersionBelowTheTargetCannotRunTheCode" test` | Run one test method. Quote the argument so the shell does not treat `#` as a comment [6]. |
| `-Dgroups=integration`, `-DexcludedGroups=integration,e2e` | Run or leave out tests that carry a JUnit tag (Chapter 13) [7]. |
| `--offline` | Do not contact any remote repository. |
| `-Dmaven.repo.local=PATH` | Use another local repository folder. |

**What the first build downloads.** Maven fetches the plugins and dependencies named in the POM, and the plugins' own dependencies, from Maven Central, and keeps them in a local repository, by default the `.m2/repository` folder in your home directory. Later builds reuse that folder. `--offline` works only when the folder already holds everything. On an empty one it fails with a message such as:

```text
Cannot access central (https://repo.maven.apache.org/maven2) in offline mode and the artifact
org.apache.maven.plugins:maven-resources-plugin:jar:3.3.1 has not been downloaded from it before.
```

Run one online build first, or copy a populated repository folder to the machine. Behind a proxy, Maven reads a `<proxies>` section from `settings.xml`, either in the Maven installation's `conf` folder or in `.m2` in your home directory [8]. Ask your institution for the proxy details; the book does not supply any.

**Counting tests.** Surefire reports **invocations**: a parameterised test with three values counts as three. The starter in the companion has five test methods and runs seven invocations. When you report a count, say what you counted and do not compare counts from different projects.

**Warnings that are not failures.** On a recent JDK a passing build can still print warnings. Maven's own libraries may print `WARNING: A terminally deprecated method in sun.misc.Unsafe has been called`; they come from Maven itself and do not mean your project is wrong. Mockito may print a notice that it is attaching itself as a Java agent (see B.5). Read the last lines: `BUILD SUCCESS` and a zero exit status mean the build passed.

## B.5 JUnit and Mockito

JUnit Jupiter is the test framework. The single dependency `junit-jupiter` brings the API for `@Test`, the parameterised-test support (`@ParameterizedTest`) and the engine that runs them, and Surefire runs it through the JUnit Platform [9]. The POM gives it the scope `test`, so it is on the class path for tests and not for the application.

Mockito creates test doubles. The book uses it in one place, to replace the notification interface in Chapter 7, and configures it for **interface-only** doubles. A one-line file, `src/test/resources/mockito-extensions/org.mockito.plugins.MockMaker`, contains `mock-maker-proxy`, which selects the mock maker that Mockito's documentation describes as avoiding code generation and able to mock only interfaces [10]. With it you cannot mock a final class or a `Clock`; use a real value or a small hand-written fake instead. Chapter 7 shows hand-written fakes and explains where each kind of double fits.

Whether you may use a mocking framework in an assessment is decided in your assessment instructions. This appendix only records how the book configures it.

**The agent warning.** On a recent JDK, Mockito can still load its helper as a Java agent when it starts, and the JVM prints a warning that a Java agent has been loaded dynamically. The tests pass either way. The JDK's own documentation says that dynamic loading will be disallowed by default in a future release, and names the option `-XX:+EnableDynamicAgentLoading` that permits it and hides the warning [11]. To run the starter without the warning:

```bash
mvn --batch-mode -DargLine=-XX:+EnableDynamicAgentLoading verify
```

## B.6 Static analysis with PMD (Chapter 5)

Chapter 5's lab uses PMD 7.28.0. It is not a Maven dependency: you download it once and run it from the chapter's script.

1. Download `pmd-dist-7.28.0-bin.zip` from the project's GitHub releases page (tag `pmd_releases/7.28.0`) [12].
2. Compare its SHA-256 digest with the one the release page shows. The digest recorded for this file is:

```text
f974ba571f7bc01c73fffe11bade25fbc1f438698f9e9c00e416e8d65e9fbac2
```

3. Unzip it into a new folder and set `PMD_HOME` to the `pmd-bin-7.28.0` folder inside it. PMD needs a Java runtime of version 8 or above.
4. From each Chapter 5 checkpoint, run `bash scripts/pmd.sh`. Confirm the installation with `"$PMD_HOME/bin/pmd" --version` (`pmd.bat` on Windows), whose output includes `PMD 7.28.0`.

A static analyser reports patterns, not defects. Its output is specific to its version and ruleset, and a different version may report different findings. Treat a finding as a prompt for review.

## B.7 Dependency-injection containers (Chapter 6)

The book uses no library container. Chapter 6 walks through a small educational container written in plain Java, so there is nothing to install for that section. It also compares the walk-through with what a framework container does, for reading only. If your team uses a framework container in its own project, record its name and exact version in your team's setup notes, as the pinned tools above are recorded here.

## B.8 Git and the pull-request routine

### One-time setup

Tell Git who you are, once per machine. Use your own name and address; do not use another person's identity.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
```

On Windows, Git may convert line endings to CRLF when it checks files out and print a warning such as `LF will be replaced by CRLF the next time Git touches it`. The warning is harmless for Java files. It matters for shell scripts, because Linux Bash and WSL do not accept a CRLF script (`set -euo pipefail` fails with `invalid option name`). Every starter in this book therefore contains a `.gitattributes` file with one line, `*.sh text eol=lf`, which keeps shell scripts in LF form [13].

### The commands you will use

The companion's `git-walkthrough.sh` runs all of these in a throwaway folder, with a bare repository standing in for the remote so that no account or network is needed. Its output matches what is shown here.

| Task | Command | What to look for |
|---|---|---|
| Start a repository | `git init -b main` | An empty history on branch `main`. |
| See what changed | `git status --short` | `M` modified, `A` staged new file, `??` untracked. |
| See the change | `git diff` | Unstaged changes only. |
| See what will be committed | `git diff --staged` | Staged changes. An empty `git diff` after staging is normal. |
| Stage a file | `git add path/to/file` | Name files; avoid `git add .` until you have read `git status`. |
| Record a commit | `git commit -m "Say what changed"` | One logical change per commit. |
| Start a branch | `git switch -c feature/short-name` | `Switched to a new branch`. |
| Return to a branch | `git switch main` | |
| Discard an edit to a tracked file | `git restore path/to/file` | The edit is gone: this cannot be undone [14]. |
| Unstage a file | `git restore --staged path/to/file` | The file stays changed but leaves the next commit. |
| Reverse a commit safely | `git revert --no-edit HEAD` | A new commit that undoes the old one; history is kept [15]. |
| Combine branches | `git merge feature/short-name` | `Fast-forward` when `main` has not moved, otherwise a merge commit. |
| Look at history | `git log --oneline --graph --decorate` | One line per commit, with the branches. |
| Share | `git push -u origin feature/short-name` | The branch exists on the remote and is tracked. |
| Copy a repository | `git clone URL` | A full copy with its history. |

Two cautions. First, `git restore` on a tracked file and `git reset --hard` throw away uncommitted work. Run `git status` first. Second, never rewrite the history of a branch that other people have pulled, for example with a forced push, unless your team has agreed to it.

### From change to merge

A pull request (a merge request on some platforms) is a proposal, on a hosting platform, to bring one branch into another so that others can review it. It is not the same as a commit [16]. A routine that works for a small team:

1. Update your copy of the shared branch.
2. Create a short branch for one change.
3. Make small commits, each with a message that says what changed. A team may adopt a written convention such as Conventional Commits; use whichever it agrees and apply it consistently (Chapter 2).
4. Run the project's check script before you push, and keep its output.
5. Push the branch and open the pull request. Describe the problem, the limited change and the checks you ran, with their results.
6. Reviewers read the diff and comment on what they inspected and why it matters. Answer by adding commits, not by rewriting the ones they have read.
7. Merge when the agreed review is complete and the required check has passed. Platforms offer a merge commit, a squash or a rebase; your repository's setting decides which one you get.
8. Delete the merged branch and update your copy of the shared branch.

Steps 5 to 8 happen in the hosting platform's interface, which differs between platforms and institutions. The book supplies no remote and no account. Record real pull-request addresses and real review comments in your team's evidence notes, and never invent review attribution. Commit and pull-request counts show activity, not contribution or quality; Chapter 14 and Appendix E explain what such evidence can and cannot show.

## B.9 A starter hosted check

The companion lists `.github/workflows/verify.yml`. It asks GitHub Actions to run the project's check script on every push and pull request, and when started by hand:

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

`permissions: contents: read` gives the job read access only. `actions/checkout` fetches your repository, and `actions/setup-java` installs a Java 17 JDK from the Temurin distribution and, with `cache: maven`, keeps Maven's downloads between runs [17][18]. The job then runs the same script you run locally, so a local pass and a hosted pass mean the same thing. A push that belongs to an open pull request can start two runs; the template accepts that.

A workflow file in the repository is only a request. It becomes evidence when it has actually run on your repository, and you can quote its run address. A green run shows that the script passed on a clean machine of one kind. It does not show that the tests are good, that the design is sound or that a reviewer agreed. To make a pull request wait for the check, configure the shared branch to require it where the platform supports that, or write the manual rule down. If no hosted platform is available, run the script locally and keep its output; that is a weaker but honest substitute.

Major action versions and runner images change. Check the current versions before you reuse the file, and record the versions that a run actually resolved from its log.

## B.10 Repository metrics

Chapter 12 measures flow from real data, and its repository lab pins one method, RM-12, with a supplied calculator and a blank evidence record. This appendix adds only the data-collection facts that every method shares.

Git alone can list commits with their times, for example:

```bash
git log --first-parent -20 --format='%H%x09%cI'
```

`%H` is the commit hash and `%cI` the committer time in strict ISO form. Following only the first parent changes which history you see. A list of commits does not give a pull request's opening time, its review time or any deployment time, and commit counts do not measure work. Those times come from the hosting platform's interface or an authorised export with exact timestamps. If you can see only relative dates such as “3 days ago”, you cannot calculate a precise duration; say so, and do not guess a time.

The module's agreed repository-metrics method is not settled by this appendix. Until your module states one, follow Chapter 12.

## B.11 When something goes wrong

| What you see | Likely cause | What to do |
|---|---|---|
| `mvn: command not found` | Maven's `bin` folder is not on the `PATH`. | Run `scripts/check-setup.sh`; fix the `PATH` and open a new shell. |
| `MISSING` or `TOO-OLD` from `check-setup.sh` | A tool is absent, or the JDK is older than 17 or has no compiler. | Install a full JDK of version 17 or later. |
| `Cannot access central ... in offline mode` | `--offline` with an empty or incomplete local repository. | Run one online build, or supply a populated repository folder. |
| `BUILD FAILURE`, `Tests run: ..., Failures: 1` | A test failed. | Open the named test, read the expected and actual values, and decide whether the code or the test is wrong. |
| `No tests matching pattern ... were executed` | `-Dtest=` named a class or method that does not exist. | Check the spelling; the message names the pattern it used. |
| `WARNING: ... sun.misc.Unsafe ...` | Maven's own libraries on a recent JDK. | Ignore if the build ends in `BUILD SUCCESS`. |
| `WARNING: A Java agent has been loaded dynamically` | Mockito attaching its helper (B.5). | Ignore, or add `-DargLine=-XX:+EnableDynamicAgentLoading`. |
| `set: pipefail: invalid option name` | A shell script was checked out with CRLF line endings and run by Linux Bash or WSL. | Add `.gitattributes` with `*.sh text eol=lf` and check the file out again (Chapter 4). |
| `LF will be replaced by CRLF` from Git | Windows line-ending conversion. | A warning only; see B.8. |
| A script behaves differently in two terminals | Different programs called `bash` on the `PATH`. | Run it from Git Bash and check with `command -v bash`. |

## B.12 A short verification activity

Do these in a copy of the companion's starter project, in a throwaway folder.

1. Run `bash scripts/check-setup.sh`. Resolve any `MISSING` or `TOO-OLD` line.
2. Run `bash scripts/check.sh`. Note the number of tests Maven reports and say what it counted.
3. In a scratch copy, change `>=` to `>` in `ToolchainReport.canRunOn`, and run `bash scripts/check.sh` again. Read the failing test's message. Restore the original.
4. Initialise a repository, commit the starter on `main` and make the one-line change from step 3 on a branch. Run `git diff`, stage the file, run `git diff --staged`, and commit.
5. Write a short setup note: the versions your machine reported, the commands you ran and anything that differed from this appendix.

**Optional AI activity, with an identical offline route.** The following is an author-constructed candidate answer, not a captured model response:

> “Any Java installation will do because the code is plain Java. To confirm a project works, run `mvn install -DskipTests`. If tests fail unpredictably, add `-Dmaven.test.failure.ignore=true` so the build always passes. Share your work with `git add .` and `git push --force`.”

Check each sentence against the starter and this appendix, and say what evidence you used. A live assistant may produce a different candidate if your course allows one, but it is not required. Record the claim, your check and your conclusion; do not accept an unsupported explanation as the final evidence.

The exit artefact is the short setup note. This is formative practice and adds no assessment requirement.

## Sources and further reading

Official references opened on 13 October 2026. The explanations and commands are original; source examples have not been reproduced.

1. Oracle, [The javac Command, Java SE 17](https://docs.oracle.com/en/java/javase/17/docs/specs/man/javac.html). The `--release` option and compilation target.
2. Eclipse Adoptium, [Temurin](https://adoptium.net/). A source of JDK builds; the build named in the hosted-check example.
3. Apache Maven, [Installation](https://maven.apache.org/install.html). Prerequisites, extracting the archive, adding `bin` to the path and `mvn -v`.
4. Apache, [Maven 3.9.11 binary archive and checksum](https://archive.apache.org/dist/maven/maven-3/3.9.11/binaries/). The archive and its `.sha512` file.
5. Apache Maven, [Introduction to the build lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html). Phases and their order.
6. Apache Maven, [Surefire: running a single test](https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html). The `-Dtest` parameter.
7. Apache Maven, [Surefire and the JUnit Platform](https://maven.apache.org/surefire/maven-surefire-plugin/examples/junit-platform.html). Tag selection with `groups` and `excludedGroups`.
8. Apache Maven, [Settings reference](https://maven.apache.org/settings.html). The local repository, offline mode and proxies.
9. JUnit, [User Guide 5.13.4](https://docs.junit.org/5.13.4/user-guide/). Dependency artifacts and parameterised tests.
10. Mockito, [`MockMakers`](https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/MockMakers.html). The proxy mock maker, which can mock only interfaces.
11. OpenJDK, [JEP 451: Prepare to Disallow the Dynamic Loading of Agents](https://openjdk.org/jeps/451). The warning and the `-XX:+EnableDynamicAgentLoading` option.
12. PMD, [Installation](https://pmd.github.io/pmd/pmd_userdocs_installation.html) and the [7.28.0 release page](https://github.com/pmd/pmd/releases/tag/pmd_releases%2F7.28.0).
13. Git, [gitattributes](https://git-scm.com/docs/gitattributes). The `eol` and `text` attributes.
14. Git, [git-restore](https://git-scm.com/docs/git-restore) and [git-switch](https://git-scm.com/docs/git-switch).
15. Git, [git-revert](https://git-scm.com/docs/git-revert). A revert records a new commit.
16. GitHub Docs, [About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests). Also Chacon and Straub, [Pro Git: branching](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging).
17. GitHub, [actions/checkout](https://github.com/actions/checkout). Usage and versions.
18. GitHub, [actions/setup-java](https://github.com/actions/setup-java). Distributions, `java-version` and `cache: maven`.