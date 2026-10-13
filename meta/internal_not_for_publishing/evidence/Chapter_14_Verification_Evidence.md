# Chapter 14: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript, opening problem (232 and 235)

The README promises 232 passing tests, and the build says 235.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript, entry checkpoint (232 invocations)

(visitor change, 232 JUnit invocations, version 0.13.1)

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript, entry checkpoint (235 invocations)

is version 0.14.0 with 235 invocations. Its production code is unchanged.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript line 38

the model answers, the experiments and the verification record.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.1, E1 paragraph (45 of 159 invocations)

Start the change in the smallest possible way and see what the tests say. On the Chapter 11 checkpoint (159 invocations), add `VISITOR` to the category enum and change nothing else. The build fails: 45 of 159 invocations (1 failure and 44 errors), and nearly all of them say `Missing policy: VISITOR`. The coordinator requires a policy for every category and says so when it is constructed.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.1, E2 paragraph (45 to 5, 159)

Now add the visitor policy to the composition root, `ReservationApplication`, as well. The failures drop from 45 to 5, and the five are in exactly the three test files that build their own policy map: `LegacyRegressionTest.chapter06` (through `Chapter06Checks`), `BehaviourStrategyTest` and three tests in `RepositoryBoundaryTest`. Add the policy to those four maps and all 159 invocations pass, with no assertion changed.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.1, B1 count

and 73 of its 235 invocations fail, in fourteen test classes.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.1, E3 paragraph (228 of 232; 203 unit invocations)

Run it against the finished suite (Companion, Section 5.2). 228 of the 232 invocations of the Chapter 13 checkpoint pass. **All 203 unit invocations pass.** The four that fail are the three end-to-end journeys that use visitors and the integration test that serves a visitor through the real directory. In the journey with the flag off, visitor V1 is confirmed, so the flag is ignored; an unapproved visitor is rejected only because the item is already taken, not because it is unapproved; and a malformed register no longer stops anyone. It is a smaller diff, and it does not implement the requirement.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.3, rehearsal count (233)

After the rehearsal the full build ran 233 invocations with no failure, the pipeline passed and the handover check passed.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.4, handover-check description (stage counts)

the pipeline passes, stage 2 ran 206 invocations, stage 3 ran 26, stage 4 ran 3, the document itself states those numbers,

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.4, handover-check experiment (206)

adding one test made it report `FAIL stage 2 ran 206 invocations`, and renaming

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.4, dry run introduction

Following the handover on the machine used for the book, in a fresh folder, found four things before any reader did.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.4, JDK 24.0.2

It ran on one operating system with one JDK (24.0.2, compiling for 17) and a local Maven repository

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.6, evidence index (235)

| 235 invocations; the five-stage pipeline;

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.10 question 6 (233)

“run `mvn verify`; expect 233 tests”

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript source note

were opened on 13 October 2026; the manuscript was written the same day, Asia/Baghdad.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 1, Version note (rebuilt on the corrected Chapter 13; review changes)

**Version note.** Version 1.1 rebuilds this chapter on the corrected Chapter 13 checkpoint (Chapter 13 companion Version 1.1, project 0.13.1), whose HTTP client now bounds the whole lookup, and carries four changes from an independent review of Chapters 12 to 15: the cross-references of this file and of the chapter are repaired; the assumption “the directory cannot fail” is replaced by what Chapter 8 and Chapter 13 actually did; the one-line experiment E3 is explained as a gap in this suite's coverage, with a new exercise (B8) to close it; and the figures are refreshed. The project is still 0.14.0. The build runs **235** invocations (it was 233), stage 3 runs 26 (it was 25), and all production code is as in 0.13.1. The earlier figures of Version 1.0 are not rewritten as if they had been the ones now observed: they were 233, 205/25/3 and 71 of 233 for experiment B1.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 1, 'No production code changed' (pointer to the verification record removed)

**No production code changed.** Every file under `src/main` is byte for byte as in the Chapter 13 checkpoint (Section 10.2 records the check). What changed is tests, scripts, documents and the version.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 1, input checkpoint (versions and 232 invocations removed)

**Input checkpoint.** The starting point is the Chapter 13 checkpoint, which is the Chapter 10 companion (Version 1.1), the new and changed files of the Chapter 11 companion (Version 1.1) and the new and changed files of the Chapter 13 companion (Version 1.1): 232 JUnit invocations. To keep verified listings from being copied again, this file lists **only the files that are new or changed**. Every other file is exactly as in those companions.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 1.0, Checkpoint manifest (SHA-256 of the prerequisite companions)

### 1.0 Checkpoint manifest

| Item | Value |
|---|---|
| Blueprint | Version 0.4 (the companions say they follow it) |
| Prerequisite 1 | `Chapter_10_Code_Explanations_and_Solutions.md`, Version 1.1, SHA-256 `fc3f7e8aa803a4f65fa5740084291759cff6700401f0c7870ac1e9e478c4ea9e` |
| Prerequisite 2 | `Chapter_11_Code_Explanations_and_Solutions.md`, Version 1.1, SHA-256 `96ee7dc6e8967dd2d669ee0317d8f42309dad254f23069b9da2379332b11cce3` |
| Prerequisite 3 | `Chapter_13_Code_Explanations_and_Solutions.md`, Version 1.1, SHA-256 `8bbc0d7059d9070363dc25d886414796c8cd1b795ac40fd9590ae7658ecab95f` |
| This companion | Version 1.1; project version 0.14.0 (built on 0.13.1) |
| Verified build | `mvn --batch-mode verify`: 235 invocations (206 unit, 26 integration, 3 end-to-end), JDK 24.0.2 with `--release 17`, Maven 3.9.11 |

The checksums identify the exact prerequisite files used on 13 October 2026. If any is edited later, refresh the checksum and repeat the reconstruction.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: HANDOVER.md listing, JDK 24.0.2

(the checks recorded here used JDK 24.0.2), 

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: RELEASE-NOTES listing, time zone

Date: 13 October 2026 (Asia/Baghdad). Built from version 0.13.1

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: ADR-014 listing, time zone

Date: 13 October 2026 (Asia/Baghdad)
Status: Decided for the book project

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 5.2, reference to the exact configuration

Each was run in its own scratch copy under the exact configuration (Section 10.2).

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 5.2, E3 explanation (history of the first version removed)

What E1 and E2 show is how far the fail-fast check reaches. Everything that is constructed through the composition root fails together when the policy is missing there, which is one fix; the tests that spell out their own map fail separately, which is four fixes. What E3 shows is that this suite has a gap, and that a smaller change can pass a whole stage and fail the next one. Notice what it does **not** show: that unit tests cannot see such a change. No unit test checks the adapter's mapping of the visitor code, so nothing in the unit stage goes through it. A focused adapter test would catch the change, and Section 6.2 (B8) says what it should check. The experiment found the hole by trying a change that goes through it. Chapter 13's own tests did not close it, and the first version of this chapter described it as a limit of unit testing, which it is not. Version 1.1 corrects that.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 5.2, paragraph with the Version 1.0 figures for E3 and B1

The figures of the earlier Version 1.0 for E3 and B1 were 4 of 230 (all 202 unit tests passing) and 71 of 233.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 5.3, directory bullet (review finding and the earlier wording removed)

- *The directory is a synthetic in-process provider with no transport (Chapter 8).* Chapter 8 already defined the provider's `Failure`, translated it to a `DirectoryException` and told an outage from an absence. Chapter 13 added the real HTTP client and the cases a transport brings, and a review found that its first timeout did not cover a stalled body. The contract held and the behaviour behind it was corrected. The first version of this note said the directory “cannot fail”, which was wrong.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 5.5 intro

The handover was followed in a fresh folder on the verification machine, as a reader would, before the fixes were made:

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 5.5 item 2 (JDK 24.0.2)

printed a dynamic-agent warning, on JDK 24.0.2. The build

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 5.6, 233 invocations

the full build of that tree ran 233 invocations with no failures; and

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 10.1, 'Alignment with the other chapters' paragraph

**Alignment with the other chapters.** Chapter 13's companion lists `scripts/pipeline.sh` and `scripts/simulate-release.sh` as they were in version 0.13.0 (and in 0.13.1, whose only change to `simulate-release.sh` is two explanatory comments); this companion replaces them with versions that print a clear message when Maven is missing. Chapter 12's text still refers to a 136-test Chapter 11 suite and to a “due-today” suspected defect, which the Chapter 11 of this series does not have (see the Chapter 13 companion, Section 12.1). The numbers in this chapter come from runs of the checkpoint described in Section 1.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 10.2, Verification record (environment, reconstruction, results table; note: the pipeline row carried stale counts)

### 10.2 Verification record

This version was verified offline on Windows 11 with **Maven 3.9.11 and JDK 24.0.2**, compiling with `--release 17`, against the pinned versions (JUnit Jupiter 5.13.4, Mockito 5.20.0 with ByteBuddy 1.17.7, Compiler Plugin 3.14.1, Surefire 3.5.4) in a local repository that already held them. No JDK 17 was available, and no hosted CI run was made. The listings were extracted from the build that ran.

**Reconstruction.** The listings of the Chapter 10 companion (64), the Chapter 11 companion (26), the Chapter 13 companion (31, with four hunks) and this file (15, with one hunk) were extracted programmatically into a fresh directory, in that order, with each companion's hunks applied by `patch -p1` before the next was extracted. The result matched the working project file for file (the Chapter 11 `stages/` directory aside, which is not compiled). `mvn --batch-mode verify` on that reconstruction exited 0 with 235 invocations, no failures, errors or skipped tests; `bash scripts/handover-check.sh` on it passed; and the rehearsal patch applied to a copy of it and gave a build of 233 invocations with no failures. This is the reconstruction of Version 1.1; the one of Version 1.0 ran 233 and 231.


| Check | Observed result |
|---|---|
| Full Maven verify | Exit 0; 235 invocations, 0 failures, errors or skipped (232 inherited and 3 new). Version 1.0 ran 233 |
| The pipeline | Exit 0: 205, 25 and 3 invocations in stages 2, 3 and 4; `PIPELINE PASSED` |
| The demonstration | `scripts/demo.sh` printed the output of Section 1.2 |
| The handover check | Exit 0 with twelve `ok` lines and `HANDOVER CHECK PASSED` |
| Production code unchanged | `diff -r` of `src/main` against the corrected Chapter 13 checkpoint (0.13.1): no differences |
| A folder name with spaces | The demonstration and the pipeline passed in a copy whose folder name contains spaces |
| Missing Maven | With no `mvn` on the path, the scripts printed `Maven was not found (looked for: mvn)...` and exited 2 |
| `javac --release 17 -Xlint:all` | The test sources, `DemoRun` and `TraceabilityTest` compiled through Maven with the same flag and reported no warnings. The main sources are unchanged |
| The rehearsal | The patch applied to a fresh copy and gave a tree identical to the scratch copy; 233 invocations passed; the pipeline and the handover check passed |
| Experiments E1, E2, E3, B1 | Section 5.2 |
| Mermaid | The three figures of the chapter rendered with Mermaid 10.9.1 in the browser pane |
| Web sources | Nine online sources were opened on 13 October 2026 |
| Hosted CI, Java 17, independent review | Not performed or claimed |

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 10.2 closing limits sentence (stated environment, Java 17, hosted CI, independent review removed)

The results establish the selected behaviours on the supplied inputs, in the stated environment. They do not establish that the handover is followable by a reader on another machine, behaviour on a Java 17 runtime, a hosted CI run, or any independent review.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Section 1, first paragraph

the experiments behind the chapter's figures and the verification record.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: HANDOVER.md listing, requirement table row (JDK 24.0.2)

All checks recorded here ran on JDK 24.0.2; a Java 17 run has not been made. |

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: REQUIREMENTS-TO-EVIDENCE listing, gap G5 (JDK 24.0.2)

Not run; all verification was on JDK 24.0.2 with `--release 17` |

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: KNOWN-ISSUES listing, KI-8 (JDK 24)

is tested (`aStalledBodyIsAFailureWithinTheOverallWait`) on JDK 24 only; no Java 17 run was made |

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Manuscript 14.1, assumptions table, directory row (review finding removed)

Chapter 13 added a real HTTP client and observed the failures a transport brings. A review then found that its first timeout did not cover a stalled body, so the bounded wait was corrected | The contract held. The behaviour behind it was extended and corrected |

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Source note ('not opened' wording)

The handbook itself was not opened.

---

## From `Chapter_14_Responding_to_Change_and_Handing_Over.md`: Source note ('not opened' wording)

Not opened for this chapter; publication details come from the module descriptor.

---

## From `Chapter_14_Code_Explanations_and_Solutions.md`: Source note ('not opened' wording)

 Source 10 is not re-opened here.

---

