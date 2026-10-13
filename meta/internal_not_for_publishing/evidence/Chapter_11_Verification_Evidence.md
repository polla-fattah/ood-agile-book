# Chapter 11: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_11_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 (Asia/Baghdad) • reviewed against Blueprint v0.4

---

## From `Chapter_11_Code_Explanations_and_Solutions.md`: Section 1, first paragraph

model solutions and the verification record.

---

## From `Chapter_11_Code_Explanations_and_Solutions.md`: Section 1, Version note (merge with a second draft)

**Version note.** Version 1.1 merges in material from a second draft of this chapter: the original-versus-seam probe, the clock-zone test, the boundary-based AI patch with a second trap, the decision and defect records, and the bridge to the live loans. Everything else is as in Version 1.0.

---

## From `Chapter_11_Code_Explanations_and_Solutions.md`: Section 1, input checkpoint (version, date and invocation count removed)

**Input checkpoint.** The starting point is the Chapter 10 companion, **Version 1.1** (13 October 2026): its 64 listings, 121 JUnit invocations and the assertions carried forward from Chapters 3–9 (its Section 2.5). To keep those older, verified listings from being copied a second time, this file lists **only the files that are new or changed**. Every other file is exactly as in the Chapter 10 companion. The sections below say which is which.

---

## From `Chapter_11_Code_Explanations_and_Solutions.md`: Section 1.1, step 1

save every listing of the Chapter 10 companion (Version 1.1) at its path.

---

## From `Chapter_11_Code_Explanations_and_Solutions.md`: ADR-011 date line (time zone removed)

Date: 13 October 2026 (Asia/Baghdad)

---

## From `Chapter_11_Code_Explanations_and_Solutions.md`: Section 12.2, Verification record (environment, exact-configuration run, results table)

### 12.2 Verification record

Version 1.1 of this file (13 October 2026) was verified offline on Windows 11 with **Maven 3.9.16 and JDK 24.0.2**, compiling with `--release 17`, and the dependency versions already in the local Maven cache: JUnit Jupiter 6.0.3, Mockito 5.23.0 (with ByteBuddy 1.18.11), Compiler Plugin 3.15.0 and Surefire 3.5.6. **The pinned versions in the POM were not run in this first pass**, because they were not cached and nothing had been downloaded. No JDK 17 was available. The listings were extracted programmatically from this file and from the Chapter 10 companion (Version 1.1), so the sources that ran are the sources printed.

**Exact-configuration run (13 October 2026).** The unmodified POM from this file was run with **Maven 3.9.11** (downloaded from Maven Central and checked against its published SHA-512) on **JDK 24.0.2** (`--release 17`), against a clean local repository, so that nothing already cached could stand in for a pinned version. The versions that ran were JUnit Jupiter 5.13.4, Mockito 5.20.0 (which brought ByteBuddy 1.17.7), Compiler Plugin 3.14.1 and Surefire 3.5.4, plus the plugins that Maven 3.9.11 binds by default (Resources 3.3.1 and JAR 3.4.1). `mvn verify` exited 0 with 159 tests and no failures; the four plain-Java runners reported 34, 5, 44 and 28 as before. The two dependency tests passed, and the legacy report's 28 invocations and the bridge's 10 were part of the 159. **Still not verified:** behaviour on a Java 17 runtime (no JDK 17 was available) and a hosted CI run. The fault experiments in this file were run in the earlier pass and were not repeated under the exact configuration.

| Check | Observed result |
|---|---|
| Reconstruction | The 64 listings of the Chapter 10 companion (Version 1.1) and the 26 listings of this file were extracted. This file's listings replaced four existing files (`pom.xml`, `README.md`, `DependencyRulesTest.java` and `PackageMetrics.java`) and added 22 files. The 79 source, test, build and probe files matched the verified project exactly, and the seven stage files matched their sources |
| Full Maven verify | Exit 0; 159 invocations, 0 failures, errors or skipped: 121 inherited, 28 for the report (27 characterisation, 1 differential) and 10 for the optional bridge |
| Each stage | Stages 1, 2, 3 and 4 each passed the same 28 report invocations; stage 0 cannot be tested (system clock) |
| Stage C | Exit 0; 159 invocations with its three replaced files |
| Probe | `Original and seamed reports agree on 5 rows and on an empty list.` with stage 1 in place, and again with the final report |
| Demonstrations | `Chapter11Demo` printed the output in Section 1.2; `Chapter10Demo` and the earlier demonstrations printed what they printed before |
| `javac --release 17 -Xlint:all` on the main sources | No warnings |
| Package metrics | `legacy`: 3 classes, Ca = 4, Ce = 0, I = 0.00; `bootstrap`: 11 classes, Ca = 0, Ce = 11, I = 1.00; every other lending package has the figures it had in Chapter 10 |
| Dependency tests | Both pass with `legacy.` forbidden for production code |
| Staff grace period changed to 7 days | Five of the 28 report invocations fail, exactly the staff-rule ones; no bridge test fails |
| Mockito agent warning | The dynamic-agent warning described in Chapter 7 also appeared on JDK 24; the tests passed |
| Peer review, hosted CI, real data | Not performed or claimed |

---

## From `Chapter_11_Code_Explanations_and_Solutions.md`: Section 12.2 lead-in (bold question moved into the heading)

**Do the tests detect faults?** The experiment ran in two rounds, always one fault at a time in a copy of the project and always through `mvn test`.

---

## From `Chapter_11_Code_Explanations_and_Solutions.md`: Section 12.2, closing limits sentence (stated environment, pinned versions, Java 17 and hosted CI removed)

The results establish the selected behaviours on the supplied inputs, in the stated environment. They do not establish equivalence with the original for every input, the pinned dependency versions, Java 17 behaviour, hosted CI or any real record system.

---

## From `Chapter_11_Refactoring_and_Legacy_Code.md`: Manuscript, entry checkpoint (test count removed)

with its 121 JUnit invocations and its package structure.

---

## From `Chapter_11_Refactoring_and_Legacy_Code.md`: Manuscript line 38

model answers and the verification record.

---

## From `Chapter_11_Refactoring_and_Legacy_Code.md`: Manuscript source note

were opened on 13 October 2026; the manuscript was written the same day, Asia/Baghdad.

---

## From `Chapter_11_Refactoring_and_Legacy_Code.md`: Source note ('not opened' wording)

the Week 10 reading is its refactoring chapter. Not opened for this chapter; publication details come from the module descriptor.

---

## From `Chapter_11_Refactoring_and_Legacy_Code.md`: Source note ('not opened' wording)

Not opened; the working definition of legacy code and of a seam are Feathers's, and the characterisation-testing description was checked against source 3.

---

