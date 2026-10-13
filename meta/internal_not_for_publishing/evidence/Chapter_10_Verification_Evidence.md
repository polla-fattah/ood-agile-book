# Chapter 10: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_10_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 (Asia/Baghdad) • reviewed against Blueprint v0.4

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 1, reference to Chapter 9 companion version and review date

The starting implementation is the Chapter 9 companion, Version 1.1 (reviewed 13 October 2026).

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 1, 'What changed in this version' paragraph

**What changed in this version.** Version 1.0 of this file carried older copies of nine files from earlier chapters, so it had lost assertions and fixes that the review of Chapters 3–9 had added. Version 1.1 restores them (Section 2.5), adds a package-cycle check, a repository-null check and a console check for a staff request longer than seven days, adds `.gitattributes` and the `tools/PackageMetrics.java` program, and adds the model answers to the package-design material and to the Team project steps.

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: ADR-010 date line (time zone removed)

Date: 13 October 2026 (Asia/Baghdad)
Status: Implemented teaching example; peer review pending.

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 2.5 table row for Chapter 6

(28 checks, not 26)

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Tests section, sentence on three tests added in version 1.1 (reworded)

Three of these tests were added in Version 1.1 because the fault experiment in Section 11.2 found gaps. `coordinatorRequiresARepository` pins the constructor's null check. `staffRequestAboveTheStudentLimitIsDecidedByThePolicyNotTheConsole` sends a ten-day staff request through the console: the earlier console test used only a student, so a console that quietly enforced the seven-day rule itself passed. `productionPackagesHaveNoDependencyCycles` closes the gap that the layer matrix leaves inside one layer.

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 11.2, Verification record (version paragraphs, exact-configuration run, results table)

### 11.2 Verification record

**Version 1.0 (earlier copy of this file)** recorded a run on OpenJDK 17.0.20 with Maven 3.9.11 and the pinned configuration: 118 invocations, all passing. That run was not repeated. Review found that it carried older copies of nine files (Section 2.5), so its 118 passes did not show that the strengthened assertions from Chapters 3–9 were still present.

**Version 1.1 (13 October 2026)** was run offline on Windows 11 with **Maven 3.9.16 and JDK 24.0.2**, compiling with `--release 17`, and the dependency versions already in the local Maven cache: JUnit Jupiter 6.0.3, Mockito 5.23.0 (with ByteBuddy 1.18.11), Compiler Plugin 3.15.0 and Surefire 3.5.6. **The pinned versions in the POM were not run in this first pass**, because they were not cached and nothing had been downloaded. No JDK 17 was available. The 64 listings were extracted programmatically from this file, so the sources that ran are the sources printed here. The results of the first pass verify the code, tests and configuration files, not the exact pins.

**Exact-configuration run (13 October 2026).** The unmodified POM from this file was run with **Maven 3.9.11** (downloaded from Maven Central and checked against its published SHA-512) on **JDK 24.0.2** (`--release 17`), against a clean local repository, so that nothing already cached could stand in for a pinned version. The versions that ran were JUnit Jupiter 5.13.4, Mockito 5.20.0 (which brought ByteBuddy 1.17.7), Compiler Plugin 3.14.1 and Surefire 3.5.4, plus the plugins that Maven 3.9.11 binds by default (Resources 3.3.1 and JAR 3.4.1). `mvn verify` exited 0 with 121 tests and no failures; the four plain-Java runners reported 34, 5, 44 and 28 as before. The compiled dependency tests (direction and package cycles) passed with the `jdeps` of JDK 24. **Still not verified:** behaviour on a Java 17 runtime (no JDK 17 was available) and a hosted CI run. The fault experiments in this file were run in the earlier pass and were not repeated under the exact configuration.

| Check (version 1.1) | Observed result |
|---|---|
| Reconstruction | All 64 listings extracted; the 61 source and tooling files matched the verified project exactly |
| Full Maven verify | Exit 0; 121 invocations, 0 failures, errors or skipped: 107 migrated, 7 repository, 2 value, 3 console, 2 dependency |
| Bridged plain-Java runners | 34 Chapter 2 checks, 5 Chapter 3 example groups, 44 Chapter 5 checks and **28** Chapter 6 checks, all passing (Version 1.0 of this file reported 26) |
| Migrated files against Chapter 9 | Identical to their Chapter 9 originals apart from package and import lines and the repository argument (Section 2.5) |
| Demonstrations | `Chapter10Demo` printed the five-line transcript in Section 1.2. `Chapter04Demo`, `Chapter05Demo`, `Chapter07Demo`, `Chapter08Demo`, `Chapter09Demo` and `ReservationApplication` produced their earlier output under the new launcher names |
| `javac --release 17 -Xlint:all` on the main sources | No warnings |
| `tools/PackageMetrics.java` | Printed the table in Section 1.3; the figures were also reproduced independently from raw `jdeps` output |
| Option B experiment | With `NotificationException` moved to `infrastructure.notification`, both dependency tests failed, as Section 7.4 describes |
| Mockito agent warning | The dynamic-agent warning described in Chapter 7 also appeared in this build on JDK 24; the tests passed |
| Peer review, hosted CI, real storage | Not performed or claimed |

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 11.2 lead-in (118 and 121 invocations, version 1.0 and the nine stale files removed)

**Do the tests detect faults?** Twenty-five faults were introduced one at a time into copies of the project, and each copy was run through `mvn test`. They were first run against the 118-invocation suite that the migration had produced once the nine stale files were restored (version 1.0's tests plus the restored assertions). Twenty were caught and five survived. The survivors were then run against the version 1.1 tests (121 invocations).

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Fault table header

| Area | Faults tried | Result with 118 invocations | Result with version 1.1 |

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 11.2, paragraph after the fault table (118 and 121 invocations removed)

Of the 25 faults, 20 were caught by the 118-invocation suite, and 23 are caught by the 121 invocations of version 1.1. The two that still survive are an equivalent mutant and a known limit of any bytecode-based dependency check. Different chapters used different fault sets, so these counts say nothing about how this suite compares with earlier ones. The seven-day-rule survivor and the cycle survivor are the most instructive: both tests were green, and both gaps were visible only when a plausible wrong implementation was tried.

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 11.2, closing limits sentence (pinned versions and Java 17 removed)

The results establish the supplied local scenarios and dependency rules. They do not establish persistence, authentication, concurrent consistency, universal behavioural equivalence for unseen consumers, the pinned dependency versions or behaviour on Java 17.

---

## From `Chapter_10_From_Classes_to_Application_Structure.md`: Manuscript source note

; manuscript revised 13 October 2026, Asia/Baghdad.

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 9, flawed alternative 1 (Version 1.1)

The test added in Version 1.1 sends exactly that request.

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Source note ('not opened' wording)

Not opened for this chapter; publication details are from the module descriptor.

---

## From `Chapter_10_From_Classes_to_Application_Structure.md`: Source note ('not opened' wording)

The book itself was not opened for this chapter, and its publication details come from the module descriptor.

---

## From `Chapter_10_Code_Explanations_and_Solutions.md`: Section 11.1, sample PR sentence about the author

The author has not opened a PR, run hosted CI or claimed an independent reviewer.

---

