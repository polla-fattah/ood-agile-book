# Appendix F: correction (NOT FOR PUBLISHING)

13 October 2026. The received version is in `../other_appendices_as_received/appendix-f.md`.

## What was built

A stand-alone Maven project, the risk lab (package `risk`, version 1.0.0, JUnit Jupiter 5.13.4 only), with 14 main files, 9 test files (3 of them support), 2 starter files and 4 build and repository files: 29 files. The appendix is `content/book/appendix-f.md` (349 lines) and the companion is `content/companion/appendix-f.md` (1,468 lines).

## Environment

Windows 11, Git Bash, JDK 24.0.2 with `--release 17`, Maven 3.9.11 (the pinned copy), offline against the pinned local repository, Hugo 0.166.0 extended.

## Results

| Check | Result |
|---|---|
| First build | 66 invocations, all pass |
| After tightening (deadlines, a test that a stalled call is asked to stop, 0% and 100% canary edges) | 67 invocations (56 unit, 11 integration), `RISK LAB PASSED` |
| Per class | RiskAssessmentTest 12, ReservationScreenTest 10, RuleBasedRiskAssessorTest 16, ResilientRiskAssessorTest 8, RolloutAssessorTest 10, HttpRiskPredictionAdapterContractTest 11 |
| Starter probe (`javac --release 17`) | good day true; confidence 1.7 true; slow service true after 1502 ms; service down false |
| Rebuild from the published companion | 29 files extracted; `diff -r` against the tested lab: identical; `check.sh` 67 and 56, exit 0; the probe prints the same four lines |
| Mermaid | 2 diagrams rendered (Mermaid 10.9.1); all 7 class names in the class diagram exist in the lab |
| Hugo | exit 0, no warnings, for appendix F, its companion, D and E |
| Cleanup rules | no internal IDs, old file names or version stamps |

## Fault experiments (single faults in scratch copies)

| Fault | Result |
|---|---|
| E1 wrapper waits one hour | 2 invocations end at the 5 s deadline |
| E2 no cancel | 1 fails (`aStalledPrimaryIsAskedToStop`) |
| E3 all runtime failures fall back | 1 fails |
| E4 interrupt flag not restored | 1 fails |
| E5 `>` for `>=` at the threshold | 2 fail |
| E6 confidence 1.0 rejected | 5 error |
| E7 `<=` for `<` | 1 fails |
| E8 HIGH not rejected | 4 fail |
| E9 outage becomes approval | 1 fails |
| E10 identifiers not encoded | 1 errors |
| E11 adapter waits one hour | 1 ends at the deadline (`aServiceThatStallsInTheMiddleOfTheBodyIsAlsoBounded`); the stall before the headers is caught by the client's own timeout, as Chapter 13 explains |
| E12 shadow returns the model's answer | 1 fails |
| E13 shadow failure escapes | 1 errors |
| E14 canary `<=` | 1 fails (after the 0% and 100% test was strengthened over 1000 borrowers) |
| E15 `Math.abs(hash % 100)` | none: a valid alternative bucketing (a survivor) |

Two experiments were first written so that they did not compile (removing the bound with a bare `get()` makes the timeout handler unreachable); they were redone with a one-hour bound. The first version of the E14 pattern did not match the code and was corrected. A stronger test was needed for E14: with one borrower id, the faulty canary was not noticed.

## Sources opened

Sculley et al. (abstract page and the PDF text: first-figure caption, CACE, boundary erosion, entanglement, glue code, pipeline jungles, data dependencies, the remark of at most 5% machine learning code and at least 95% glue code, wrapping black-box packages in common APIs); Breck et al. (research page); Oracle HttpClient, CompletableFuture, HttpRequest.Builder and com.sun.net.httpserver package summary (HTTP 200, key terms present).

## Correction to the earlier review

The review report said the 5% in the received appendix's diagram could not be confirmed. It can: the paper's glue-code section says it. The report's F-7 row now says so.

## Not verified

JDK 17 runtime; macOS and Linux; print layout; the lab was not used by a student.
