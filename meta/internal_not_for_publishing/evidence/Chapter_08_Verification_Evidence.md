# Chapter 8: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_08_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3

---

## From `Chapter_08_Code_Explanations_and_Solutions.md`: Section 7, paragraph on the flawed candidates (version 1.0 and 1.1 history removed)

Version 1.0 only predicted which tests would reject these candidates. In version 1.1 all three were actually applied, one at a time, to a copy of the project and run through `mvn test`. Each was rejected by the tests named above: the unsafe fallback by `unknownCodesAreErrors` and `malformedRowsAreErrors`, the catch-all by `translatesExpectedFailureAndKeepsCause` and `absenceAndOutageDoNotStoreNotifyOrConsumeId`, and the shared builder list by `builtValueIsIndependentOfReusableBuilder`.

---

## From `Chapter_08_Code_Explanations_and_Solutions.md`: Section 11.2, Observed local verification (version paragraphs, exact-configuration run and observation table)

### 11.2 Observed local verification

**Version 1.0 (12 October 2026)** was run on OpenJDK 17.0.20 with Maven 3.9.11 and the pinned configuration in Section 5. That run was not repeated. The tests are ordinary JUnit examples and regression checks; this chapter does not claim a recorded test-first development history for the new code.

**Version 1.1 (13 October 2026)** was re-verified offline on Windows 11 with **Maven 3.9.16 and JDK 24.0.2** (compiling with `--release 17`) and the dependency versions already in the local Maven cache: JUnit Jupiter 6.0.3, Mockito 5.23.0 (with ByteBuddy 1.18.11), Compiler Plugin 3.15.0 and Surefire 3.5.6. **The pinned versions in the POM were not run in this first pass**, because they were not cached and nothing had been downloaded. All 44 listings were extracted programmatically from this file, so the sources that ran are the sources printed here. The results of the first pass verify the code, tests and configuration files, not the exact pins.

**Exact-configuration run (13 October 2026).** The unmodified POM from this file was run with **Maven 3.9.11** (downloaded from Maven Central and checked against its published SHA-512) on **JDK 24.0.2** (`--release 17`), against a clean local repository, so that nothing already cached could stand in for a pinned version. The versions that ran were JUnit Jupiter 5.13.4, Mockito 5.20.0 (which brought ByteBuddy 1.17.7), Compiler Plugin 3.14.1 and Surefire 3.5.4, plus the plugins that Maven 3.9.11 binds by default (Resources 3.3.1 and JAR 3.4.1). `mvn verify` exited 0 with 63 tests and no failures; the four plain-Java runners reported 34, 5, 44 and 28 as before. **Still not verified:** behaviour on a Java 17 runtime (no JDK 17 was available) and a hosted CI run. The fault experiments in this file were run in the earlier pass and were not repeated under the exact configuration.

| Observation (version 1.1) | Result |
|---|---|
| `mvn -o verify` | Exit 0; 63 tests, 0 failures: 1 TDD, 8 availability, 10 policy, 17 directory, 4 legacy bridges, 9 loan, 3 Mockito, 11 pattern |
| Chapter 8 demo | Output matched Section 1.1 exactly |
| Files against the current Chapter 7 | Identical, except four stale embedded copies in version 1.0 (`NotificationException`, the acceptance listing, `Chapter06Checks` with 26 checks, and `LoanServiceTest` without the `loans()` snapshot assertion) and the missing `.gitattributes`; all refreshed or added in 1.1 |
| `javac -Xlint:all` on all main sources | Version 1.0 gave four `[serial]` warnings (`DirectoryException`, `LegacyDirectoryClient.Failure`, `PatternExamples.DeliveryFailure` and the stale `NotificationException`); fixed with `serialVersionUID`, and the build is now warning-free |
| Builder and Decorator exercise solutions (Section 8.4) | Added in a copy: `PatternExamplesTest` ran 14 tests, 0 failures |
| Mermaid diagrams | The class diagram and the sequence diagram rendered without error with Mermaid 10.9.1 |

---

## From `Chapter_08_Code_Explanations_and_Solutions.md`: Section 11.2 lead-in (environment, version 1.0 and the earlier counting error removed)

**Do the tests detect faults?** Twenty faults, listed in the table below (8 + 3 + 2 + 4 + 2 + 1), were introduced one at a time into copies of the project, and each copy was run through `mvn test` in the version 1.1 environment described above (JDK 24.0.2 and the cached dependency versions, not the pinned ones). With version 1.0's tests, nineteen were caught and one survived. Version 1.1 closes that gap, so all twenty are now caught. (An earlier edition of this paragraph said nineteen faults and eighteen caught; that was a counting error, since the table has always listed twenty.)

---

## From `Chapter_08_Code_Explanations_and_Solutions.md`: Fault table row, Factory Method ('Survived in 1.0' wording removed)

| Factory Method | `ExportJob.run` skips its null check | **Survived in 1.0**: only `HtmlJob.run(null)` was tested, and `HtmlJob` fails on null anyway through `escape`, so `PlainJob.run(null)` silently returned `TEXT: null`. Caught in 1.1 by adding `plain.run(null)` to the existing test |

---

## From `Chapter_08_Code_Explanations_and_Solutions.md`: Mockito warning sentence (JDK 24 named)

The Mockito dynamic-agent warning described in Chapter 7 also appears in this project's log on JDK 24. It does not affect results, and `-DargLine=-XX:+EnableDynamicAgentLoading` removes it.

---

## From `Chapter_08_Code_Explanations_and_Solutions.md`: Section 11.2, second results table (full verify, preserved sources, reconstruction)

| Check | Observed result |
|---|---|
| Full Maven verify | Exit 0; 63 JUnit invocations; no failures, errors or skipped cases |
| Inherited Chapter 7 suite | 35 invocations retained and passed |
| New directory tests | 17 invocations passed |
| Isolated pattern tests | 11 tests passed |
| Existing source preservation | All Chapter 7 application and test source files unchanged |
| Chapter 8 demo | Output matched Section 1.1 |
| Markdown reconstruction | All 44 listings matched source; reconstructed Maven build passed all 63 invocations and both chapter demonstrations |
| Real provider, hosted CI and independent peer review | Not performed or claimed |

---

## From `Chapter_08_Creating_and_Connecting_Objects.md`: Source note ('not opened' wording)

The classic book is a bibliographic foundation; the linked publisher excerpts are the portions inspected online, not a claim to have accessed the entire book in this session.

---

