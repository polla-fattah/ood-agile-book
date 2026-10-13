# Chapter 9: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_09_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3

---

## From `Chapter_09_Code_Explanations_and_Solutions.md`: Tool table row (author runtime)

| Java | Release 17; author runtime OpenJDK 17.0.20 |

---

## From `Chapter_09_Code_Explanations_and_Solutions.md`: Section 10, intro to the flawed alternatives (version 1.0 and 1.1 history removed)

These are **deliberately incorrect fragments or proposals**, not extra source files for the active build. If experimenting, use a disposable copy and restore the correct source before the full gate. Version 1.0 only predicted which tests would reject these alternatives. In version 1.1, the cancel-on-loan alternative (7.2) and the stop-on-first-failure alternative (7.3) were applied and run, and both were rejected by the tests named below. The setter in 7.1 cannot be rejected by a runtime test, as explained there.

---

## From `Chapter_09_Code_Explanations_and_Solutions.md`: Section 12, version paragraphs and the first observation table

**Version 1.0 (12 October 2026)** was run on OpenJDK 17.0.20 with Maven 3.9.11 and the pinned dependencies in Section 5. That run was not repeated. Verification covers the supplied implementation and examples, not a claimed test-first history or independent review.

**Version 1.1 (13 October 2026)** was re-verified offline on Windows 11 with **Maven 3.9.16 and JDK 24.0.2** (compiling with `--release 17`) and the dependency versions already in the local Maven cache: JUnit Jupiter 6.0.3, Mockito 5.23.0 (with ByteBuddy 1.18.11), Compiler Plugin 3.15.0 and Surefire 3.5.6. **The pinned versions in the POM were not run in this first pass**, because they were not cached and nothing had been downloaded. All 53 listings were extracted programmatically from this file. The results of the first pass verify the code, tests and configuration files, not the exact pins.

**Exact-configuration run (13 October 2026).** The unmodified POM from this file was run with **Maven 3.9.11** (downloaded from Maven Central and checked against its published SHA-512) on **JDK 24.0.2** (`--release 17`), against a clean local repository, so that nothing already cached could stand in for a pinned version. The versions that ran were JUnit Jupiter 5.13.4, Mockito 5.20.0 (which brought ByteBuddy 1.17.7), Compiler Plugin 3.14.1 and Surefire 3.5.4, plus the plugins that Maven 3.9.11 binds by default (Resources 3.3.1 and JAR 3.4.1). `mvn verify` exited 0 with 107 tests and no failures; the four plain-Java runners reported 34, 5, 44 and 28 as before. **Still not verified:** behaviour on a Java 17 runtime (no JDK 17 was available) and a hosted CI run. The fault experiments in this file were run in the earlier pass and were not repeated under the exact configuration.

| Observation (version 1.1) | Result |
|---|---|
| `mvn -o verify` | Exit 0; 107 tests, 0 failures (63 inherited, 44 new: 9 Strategy, 21 lifecycle, 10 publisher, 4 command) |
| Chapter 9 demonstration | Output matched Section 1.2 |
| Files against the current Chapter 8 | Identical apart from eight stale embedded copies in version 1.0 (`DirectoryException`, `LegacyDirectoryClient`, `NotificationException`, `PatternExamples` and its test, the acceptance listing, `Chapter06Checks` with 26 checks, and `LoanServiceTest`) and the missing `.gitattributes`; all refreshed or added in 1.1 |
| `javac -Xlint:all` on all main sources | Version 1.0 gave four `[serial]` warnings from the stale copies; the build is now warning-free |
| Mermaid diagrams | The state diagram, the lifecycle class diagram and the sequence diagram rendered without error with Mermaid 10.9.1 |

---

## From `Chapter_09_Code_Explanations_and_Solutions.md`: Section 12 lead-in (version 1.0 survivors and the invocation count removed)

**Do the tests detect faults?** Eighteen faults were introduced one at a time into copies of the project, and each copy was run through `mvn test`. With version 1.0's tests, sixteen were caught and two survived. Version 1.1 closes both gaps by strengthening an existing test, so all eighteen are now caught, and the invocation count stays at 107.

---

## From `Chapter_09_Code_Explanations_and_Solutions.md`: Fault table row, construction validation ('Survived in 1.0' wording removed)

| Command | **Construction validation removed** | **Survived in 1.0**: no test constructed a command with a blank identifier, a null receiver or a null start date. Caught in 1.1 |

---

## From `Chapter_09_Code_Explanations_and_Solutions.md`: Fault table row, one extra day ('Survived in 1.0' wording removed)

| Command | **Executes with one extra day** | **Survived in 1.0**: the first test checked only that the confirmation `startsWith("Confirmed: R1 for B1 on CAM1")`, which is true for any duration. Caught in 1.1 by asserting the exact confirmation, period included |

---

## From `Chapter_09_Code_Explanations_and_Solutions.md`: Section 12, second results table (Maven verify, inherited suite, reconstruction)

| Check | Observed result |
|---|---|
| Complete Maven verify | Exit 0; 107 JUnit invocations; no failures, errors or skipped cases |
| Inherited Chapter 8 suite | 63 invocations retained and passed |
| New Strategy examples | Nine invocations passed |
| Lifecycle comparison and isolation | Twenty table rows plus one independence test passed |
| Publisher behaviours | Ten tests passed |
| Command behaviours | Four tests passed |
| Source preservation | All earlier main and test sources unchanged |
| Chapter 9 demonstration | Output matched Section 1.2 |
| Markdown reconstruction | All 53 listings matched source; reconstructed build passed all 107 invocations; Chapter 9 transcript matched and Chapters 7–8 demos were unchanged |
| Hosted CI, real provider/delivery and independent peer review | Not performed or claimed |

---

## From `Chapter_09_Code_Explanations_and_Solutions.md`: Mockito warning sentence (JDK 24 named)

The Mockito dynamic-agent warning described in Chapter 7 also appears in this project's log on JDK 24. It does not affect results, and `-DargLine=-XX:+EnableDynamicAgentLoading` removes it.

---

## From `Chapter_09_Designing_Changing_Behaviour.md`: Source note ('not opened' wording)

The classic book is a bibliographic foundation, not a claim that its complete text was accessed in this session.

---

