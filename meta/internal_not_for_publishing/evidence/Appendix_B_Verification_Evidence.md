# Appendix B: verification and working evidence (NOT FOR PUBLISHING)

Everything below was run on 13 October 2026 while the appendix was written. Nothing here is in the published files.

## Environment

| Item | Value |
|---|---|
| Operating system | Windows 11 Home 10.0.26300, Git Bash |
| Git | 2.54.0.windows.1 |
| JDK | Oracle JDK 24.0.2 (no Java 17 runtime available; all builds use `--release 17`) |
| Maven | 3.9.11, unpacked from the archive downloaded earlier in the project (`mvn_home`) |
| Local repository | A populated copy holding the pinned dependencies (`m2pinned`); every build used `--offline` |
| Pinned versions in the starter POM | JUnit Jupiter 5.13.4, Mockito 5.20.0, Compiler plugin 3.14.1, Surefire 3.5.4; Resources 3.3.1 and Jar 3.4.1 came from Maven 3.9.11's defaults |
| PMD | 7.28.0 (`pmd.bat --version` printed `PMD 7.28.0 (79726f0e..., 2026-09-25)`) |

Nothing was downloaded for this appendix. Web pages were fetched only to read them (and the 128-byte `.sha512` file); archive downloads were checked by header only.

## 1. The starter project

Eleven files (listed in the companion, Section 2). The working copy is in the session scratchpad (`appB/starter`) and is temporary; the companion holds every file.

| Check | Result |
|---|---|
| `bash scripts/check-setup.sh` with the pinned Maven | Five `OK` lines and `SETUP OK`, exit 0 |
| First version of the script, with `CHAPTER_MVN` set to a Windows `.cmd` path | Reported `MISSING maven` although the file exists. **Bug found by running it.** `command -v` does not accept the path; fixed with `|| [ -f "$1" ]`. |
| `bash scripts/check.sh` (`CHAPTER_OFFLINE=1`, pinned repository) | Exit 0; `Tests run: 1` (GreeterMockTest), `Tests run: 6` (ToolchainReportTest), total `Tests run: 7`; `BUILD SUCCESS`; `Running on Java 24; compiled for release target 17`; `BUILD AND TESTS PASSED` |
| First version of the tests | A parameterised test that only compared constants; replaced by `canRunOn` and a boundary test from both sides (17, 21, 24 and 16) |
| Rebuild from the finished companion | 11 extracted files and the walk-through script were identical to the working copy (`diff -r`); `check-setup.sh` and `check.sh` passed again from the rebuilt copy |
| `verify.yml` | Parsed with PyYAML: top-level keys `name`, `on`, `permissions`, `jobs`; the manuscript's copy is identical to the file. It was not run on a hosted runner. |
| Action versions | Latest releases on 13 October 2026: `actions/checkout` v7.0.1 (20 July 2026), `actions/setup-java` v6.0.1 (9 September 2026), matching the `@v7` and `@v6` tags used |

### Fault experiments (scratch copies)

| Change | Command | Observed |
|---|---|---|
| `CHAPTER_MVN=/nonexistent/mvn` | `check-setup.sh` | `MISSING maven`, `SETUP INCOMPLETE`, exit 1 |
| A fake `javac` printing `javac 1.8.0_999` first on the path (first attempt used a Windows-style `PATH` entry and did not take effect; redone with a POSIX path) | `check-setup.sh` | `TOO-OLD javac ... cannot compile with --release 17`, exit 1 |
| `RELEASE_TARGET` 17 to 21 (first test version) | `check.sh` | 3 failures, exit 1 |
| `>=` to `>` in `canRunOn` | `check.sh` | `Tests run: 7, Failures: 1`; the failing invocation is `javaVersionsAtOrAboveTheTargetCanRunTheCode(int)[1]` (the value 17); exit 1; no success line |
| The same change | `mvn -DskipTests verify` | `Tests are skipped.`, `BUILD SUCCESS`, exit 0 |
| The same change | `mvn -Dmaven.test.failure.ignore=true verify` | Failure printed, `BUILD SUCCESS`, exit 0 |
| `--offline` with an empty local repository | `mvn verify` | `Cannot access central ... in offline mode and the artifact org.apache.maven.plugins:maven-resources-plugin:jar:3.3.1 has not been downloaded from it before.` |
| `-Dtest=NoSuchTest` | `mvn test` | `No tests matching pattern "NoSuchTest" were executed!` |
| `-Dtest=ToolchainReportTest` and `-Dtest="ToolchainReportTest#aJavaVersionBelowTheTargetCannotRunTheCode"` | `mvn test` | 6 invocations and 1 invocation |
| `-DargLine=-XX:+EnableDynamicAgentLoading` | `mvn verify` | 7 tests passed and the `Java agent has been loaded dynamically` warning appeared 0 times (it appeared in the default run, even with the `mock-maker-proxy` resource) |

Warnings seen in a passing default run on JDK 24.0.2 with Maven 3.9.11: four `sun.misc.Unsafe` warnings from Maven's own Guice jar, and Mockito's `self-attaching` notice followed by the JVM's dynamic-agent warning. Neither affected the exit status.

## 2. The release experiment (manuscript B.1)

The manuscript's own `NewApi.java` text was extracted and compiled. Plain `javac` (JDK 24): compiled, printed `a`. `javac --release 17`: `NewApi.java:5: error: cannot find symbol ... method getFirst()`, exit 1. The first run used a copy of the program without a blank line; the experiment was rerun with the exact manuscript text.

## 3. The Git walk-through

`git-walkthrough.sh` ran in a throwaway folder (exit 0, three times: once for each edit of the script, and once from the rebuilt copy). A bare repository in the same work folder served as the remote. Observations: on Windows every `git add` printed `LF will be replaced by CRLF` warnings; `git diff --stat` printed nothing after staging while `git diff --staged --stat` printed the change; `git restore --staged` returned the new file to `??`; the merge was a fast-forward. Portability edits: `sed -i` and `\t` in `sed` replaced by a temporary file and `cut -f2` (they behave differently on macOS). The script was not run on macOS or Linux.

## 4. Digests and installers

| Item | Result |
|---|---|
| Maven 3.9.11 archive, local file | SHA-512 `03e2d65d4483a3396980629f260e25cac0d8b6f7f2791e4dc20bc83f9514db8d0f05b0479e699a5f34679250c49c8e52e961262ded468a20de0be254d8207076`; identical to the published `.sha512` file at `archive.apache.org` |
| PMD 7.28.0 zip, local file | SHA-256 `f974ba571f7bc01c73fffe11bade25fbc1f438698f9e9c00e416e8d65e9fbac2`, identical to the digest recorded in the Chapter 5 companion (single source: the GitHub release page) |
| Maven installation page | Says the current stable version is 3.10.0; the book's pin of 3.9.11 is therefore not the latest release (stated in B.1). The page says to extract the archive, add `bin` to the `PATH`, have a JDK through `JAVA_HOME` or `java` on the path, and check with `mvn -v`. |

## 5. Sources opened and what was checked

| # | Source | Check |
|---|---|---|
| 1 | Oracle javac 17 manual | Already used in Appendix A; `--release` |
| 2 | Adoptium | HTTP 200, page names Temurin |
| 3 | Maven installation | Read (see above) |
| 4 | Maven 3.9.11 archive and `.sha512` | Headers 200; checksum compared |
| 5 | Maven build lifecycle | HTTP 200; mentions verify and package phases |
| 6 | Surefire single test | HTTP 200; `-Dtest` present (9 matches) |
| 7 | Surefire and JUnit Platform | HTTP 200; `groups` and `excludedGroups` present |
| 8 | Maven settings | HTTP 200; `settings.xml` locations, `<offline/>`, `<proxies/>` |
| 9 | JUnit 5.13.4 user guide | HTTP 200; `junit-jupiter` present |
| 10 | Mockito `MockMakers` | Source file read: `PROXY = "mock-maker-proxy"`, "avoids code generation, but can only mock interfaces" |
| 11 | JEP 451 | HTTP 200; `EnableDynamicAgentLoading` present |
| 12 | PMD installation page and 7.28.0 release | HTTP 200 for both |
| 13 | gitattributes | HTTP 200; `eol` present |
| 14 | git-restore, git-switch | HTTP 200; `--staged` present |
| 15 | git-revert | HTTP 200; records a new commit |
| 16 | GitHub About pull requests; Pro Git branching | HTTP 200 for both |
| 17 | actions/checkout README | HTTP 200; `actions/checkout@v` usage present |
| 18 | actions/setup-java README | HTTP 200; `cache: maven` present |

## 6. Not verified

- No Java 17 runtime run (JDK 17 was not available; the module leader declined the download).
- No hosted CI run of `verify.yml`; no GitHub or GitLab pull request was opened or merged; the pull-request routine in B.8 is a description.
- No proxy configuration was tested.
- No macOS or Linux run; only Git Bash on Windows.
- Maven 3.10.0 was not tried against the starter.
- The Windows `bash` ambiguity was observed (three `bash.exe` files on the path: Git for Windows, `C:\windows\system32`, and the WindowsApps launcher); the failing CRLF scenario was not repeated here and is taken from Chapter 4.
- The Git version floor (2.28) is stated from knowledge of when `git init -b` was added; no older Git was run.
