# Chapter 15: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_15_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Section 1, first paragraph

the experiments behind the chapter's figures; and the verification record.

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Section 1, Version note (independent review)

**Version note.** Version 1.1 follows an independent review of Chapters 12 to 15. (1) The advice about acceptance examples is corrected: what makes them independent evidence is that they were derived from the requirement before any candidate existed, and not that the assistant never saw them. Sharing reviewed examples is allowed; a pass on examples the assistant has seen shows only that it satisfied them, so independently derived boundary cases and, where wanted, undisclosed cases are added. (2) The plain-`javac` comparison is stated as conditional on a JDK of version 21 or later. (3) `check-record.sh` now fails, and says so, when there is no record to check. (4) The remaining wording is scoped (hosted and local tools; the reading route). The lab's code and tests are unchanged, and so are its nine acceptance examples. Section 10.2 adds the results that the review reported on a Java 17 runtime, attributed to it.

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Filled record, JDK 24

plain `javac` on JDK 24 reports only the first.

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Filled record, Verification line (JDK 24.0.2)

(`mvn --batch-mode test`, Maven 3.9.11, JDK 24.0.2, `--release 17`)

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Filled record, Limits (JDK 24)

No Java 17 runtime was available: the code was compiled for 17 with `--release 17` and run on JDK 24.

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Section 6.1 table, JDK 24.0.2

| `javac -d out1 *.java` (JDK 24.0.2, no `--release`) |

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Flawed alternative 8.2, JDK 24

$ javac AvailabilityFinder.java      # JDK 24, no --release

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Section 10.2, Verification record (environment, reconstruction, results table, the review's Java 17 results)

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

---

## From `Chapter_15_Code_Explanations_and_Solutions.md`: Section 10.2 closing limits sentence (stated environment and Java 17 removed)

The results establish the selected behaviours on the supplied inputs, in the stated environment. They do not establish how a real assistant would behave on this task, behaviour on a Java 17 runtime, or that the acceptance examples are the right examples.

---

## From `Chapter_15_AI_as_a_Software_Engineering_Assistant.md`: Manuscript line 47

the model answers and the verification record.

---

## From `Chapter_15_AI_as_a_Software_Engineering_Assistant.md`: Manuscript 15.4, JDK 24

plain `javac` on JDK 24 reported only the first error

---

## From `Chapter_15_AI_as_a_Software_Engineering_Assistant.md`: Manuscript source note

were opened on 13 October 2026; the manuscript was written the same day, Asia/Baghdad. Tool and service behaviour changes quickly, so each source is dated by that opening.

---

## From `Chapter_15_AI_as_a_Software_Engineering_Assistant.md`: Source note ('not opened' wording)

Only the abstract page was read.

---

