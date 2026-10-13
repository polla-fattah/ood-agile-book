import pathlib

META = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile/FrontEndBook/meta")

# ---- 1. the review report
report = META / "Appendices_Review_and_Chapter_Reference_Contrast.md"
t = report.read_text(encoding="utf8")
assert "## 11. Appendix F corrected" not in t

old_note = "Appendix F was not touched and its findings still stand.\n\n"
assert t.count(old_note) == 1
t = t.replace(old_note, "Appendix F was corrected afterwards; see section 11.\n\n")

old_f7 = "| F-7 | S | F.4 | The text diagram labels “ML Model Code (5%)” and credits it to Sculley et al. I could not confirm a percentage in the paper (the paper says only that the ML code is a small fraction). | Remove the figure or cite the exact figure |"
assert t.count(old_f7) == 1
t = t.replace(old_f7,
    "| F-7 | S | F.4 | The text diagram labels “ML Model Code (5%)” and credits it to Sculley et al. **Correction, later the same day:** this finding was wrong in part. The paper's first figure carries no percentage, but its glue-code section does say that a mature system might end up being at most 5% machine learning code and at least 95% glue code. The label should have cited that sentence and the section, and not the figure | Cite the glue-code section |")

t += """
## 11. Appendix F corrected (13 October 2026, later)

The owner asked for Appendix F to be corrected. The received version is in `internal_not_for_publishing/other_appendices_as_received/appendix-f.md`. Because the printed code could not be trusted, the appendix was rebuilt around a **real, tested lab** (the risk lab) in the way Chapter 15 builds its lab, with a companion page that lists every file.

| Findings | Resolution |
|---|---|
| F-1 (the wrapper did not enforce its timeout) | `ResilientRiskAssessor` runs the primary on its own thread, waits with `Future.get(limit)`, cancels on a timeout and falls back only for the expected failure. Test `aStalledPrimaryIsGivenUpOnWithinTheLimitAndTheFallbackAnswers` ends within the limit; fault E1 (a wait of one hour) fails two tests at their five-second deadline |
| F-2 (exercise files did not exist) | The companion supplies the starting class `UnsafeRiskScorer`, a probe that runs it, and the acceptance tests; the model solution follows. All 29 files are listed and were rebuilt from the page |
| F-3 (diagram and code disagreed; not compilable as printed) | The diagram's class names are asserted against the lab, the printed types are the lab's own files, and the lab compiles for Java 17 |
| F-4 (the metamorphic test ignored its parameters) | The metamorphic test uses its two parameters, runs on a deterministic assessor and relates two answers; no third-party library is used (the stub is the JDK's HTTP server) |
| F-5 (the gate was a canary named shadow) | `RolloutAssessor` has four modes (`OFF`, `SHADOW`, `CANARY`, `ON`); shadow calls the model and records its answer while the baseline decides; the canary share is stable; each has tests |
| F-6, internal IDs, and no pointer from a chapter | Internal IDs removed. Appendix D (D.1) and Appendix E (E.2) now point to the lab. No chapter points to Appendix F yet |
| F-7 | See the correction above; F.4 cites the paper's figure, its glue-code remark and its terms, each found in the text |
| F-8 (the interrupt) | The wrapper restores the interrupt flag and has a test |
| F-9 (sources) | Two papers and four Oracle pages, all opened; the Oracle pages are the ones Chapter 13 cites |

### What was removed or changed from the received version

The sections kept their order (the two threads, the contract, testing, debt, failure, rollout, exercise, sources). Removed: the anti-pattern shown as a hypothetical class that could not compile (replaced by the real starting class and its probe), the diagram labelled with a percentage, WireMock, and the books cited without links (Martin, Huyen, Ousterhout, Humble and Farley, Gamma et al.). Added: the checked counts, the fault experiments, a stable canary, a provenance record, and the decision between failing and falling back, with the directory of Chapter 13 as the contrast.

### Checks

- The lab: 67 invocations (56 without the `integration` tag, 11 with it), `--release 17`, pinned Maven 3.9.11 offline; rebuilt from the companion page, byte-identical to the tested copy.
- Fifteen single faults: 14 noticed; the survivor is a different valid bucketing of borrowers (an equivalent change in the sense of Chapter 15).
- The starter probe prints the four lines shown in the appendix (a confidence of 1.7 is approved; a slow service holds the caller for about 1,500 ms; a service that is down looks like a refusal).
- Two Mermaid diagrams render; Hugo builds both pages without warnings; no internal IDs, old file names or version stamps.

### Still open

- No chapter points to Appendices D or F, and Chapters 3, 4 and 15 do not point to C (section 2).
- Chapter 9 lines 41, 434, 436, its companion line 2630 and Chapter 14 line 325 are unchanged.
- Old file names remain in about 24 chapter pages.
- The lab was run on JDK 24 with `--release 17` only.
"""
report.write_text(t, encoding="utf8", newline="\n")

# ---- 2. the evidence file
ev = META / "internal_not_for_publishing/evidence/Appendix_F_Correction_Evidence.md"
ev.write_text("""# Appendix F: correction (NOT FOR PUBLISHING)

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
""", encoding="utf8", newline="\n")

# ---- 3. the change log and the todo
with (META / "internal_not_for_publishing/Cleanup_Change_Log.md").open("a", encoding="utf8", newline="\n") as h:
    h.write("""## Appendix F corrected (13 October 2026, later)

- Instruction from the owner. Backup of the received version: `other_appendices_as_received/appendix-f.md`.
- `content/book/appendix-f.md` rebuilt around the tested risk lab; new companion `content/companion/appendix-f.md` (29 files, the starter, the acceptance tests, a model solution, fifteen fault experiments, answers).
- Appendix D (D.1) now lists `risk-lab` as an isolated example; Appendix E (E.2) points to Appendix F. Nothing else outside F was changed.
- Correction to my review report: the 5% remark is in the Sculley paper (F-7).
- Evidence: `evidence/Appendix_F_Correction_Evidence.md`; findings and resolutions: section 11 of `Appendices_Review_and_Chapter_Reference_Contrast.md`.

""")
with (META / "internal_not_for_publishing/Cleanup_Todo.md").open("a", encoding="utf8", newline="\n") as h:
    h.write("- [x] Appendix F corrected (risk lab, companion), 13 October 2026; chapter pointers and old file names still pending\n")
print("records updated")
