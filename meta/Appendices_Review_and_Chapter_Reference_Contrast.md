# Appendices A to F: review, and contrast with the chapters' references

Reviewed 13 October 2026, after the textbook was moved into `FrontEndBook/content/`. Files: `content/book/appendix-a.md` to `appendix-f.md` and `content/companion/appendix-a.md`, `appendix-b.md` (and the new `appendix-c.md`).

**Who wrote what.** Appendices A and B are mine and were already verified. Appendices C, D, E and F were written by someone else and arrived in `content/book/`; none has a companion. This report does not edit them. It lists what is wrong, with the evidence, so that you or their author can decide.

**Severity.** **B** (blocking) contradicts the chapters, the module descriptor or the running code, or teaches something false. **S** (should fix) breaks a cleanup rule, a link or a consistency expectation. **M** (minor).

> **Update, 13 October 2026 (later).** Appendix C was corrected, and Appendices D and E were regenerated, at the owner's request. See section 10 for what happened to each finding. The findings below describe the versions as received; those versions are kept in `internal_not_for_publishing/other_appendices_as_received/`. Appendix F was corrected afterwards; see section 11.

## 1. Summary

| Appendix | Author | B | S | M | Verdict |
|---|---|---|---|---|---|
| A Programming readiness and notation | me | 0 | 0 | 0 | Ready. Old file names removed. |
| B Tools and reproducible setup | me | 0 | 0 | 0 | Ready. Old file names removed. |
| C Engineering templates | other | 5 | 6 | 3 | Do not publish as is. Its AI record cannot be used with Chapter 15's check; one example teaches a false lesson. |
| D Checkpoints and glossary | other | 6 | 4 | 2 | Do not publish as is. The master table and the domain rules contradict the chapters. |
| E Critical reading and project evidence | other | 4 | 3 | 2 | Do not publish as is. Wrong deadline for the final submission; adds assessment policy the blueprint forbids. |
| F Software engineering for AI and data | other | 3 | 4 | 2 | Do not publish as is. The resilient wrapper does not enforce its timeout; the exercise needs files that do not exist. |

What I ran to check, beyond reading:

- Rebuilt and compiled the Appendix A lab and the Appendix B starter earlier (see their evidence files).
- **Appendix C, C-1:** compared its rejected AI candidate with `LoanPeriod.overlaps` on 6,084 period pairs: **0 disagreements**. The candidate is correct, so the stated reason for rejecting it is false.
- **Appendix F, F-1:** extracted the printed Java, compiled it with `--release 17` (no errors) and ran the `ResilientRiskAssessor` against a service that takes 1,500 ms with a 250 ms timeout. It **waited 1,513 ms** and returned the slow service's answer.
- Rendered all 6 Mermaid diagrams of Appendices D, E and F with Mermaid 10.9.1: all render. Appendix C has none.
- Checked every `Chapter N Section N.N` reference in C to F against the chapters' headings: two exist (both in C); one points at the wrong section (C-9).
- Compared the Appendix D master table, domain rules, class names, package names and test counts with the chapters' own figures.
- Compared Appendix E with the module descriptor (the `.docx`), and the blueprint's boundary for E.
- Built my new page with Hugo 0.166.0: no errors, placeholders appear literally.

## 2. Contrast: what the chapters say about the appendices

Every place a chapter or companion mentions an appendix (the appendices' own pointers to each other are in section 3).

| Where | What it says | Appendix says / status | Result |
|---|---|---|---|
| Ch 1, line 34 and 387 | Appendix A has a refresher and diagnostic | A.1 to A.9 | OK (updated 13 Oct) |
| Ch 1, line 292 | Appendix E develops the review method | E.1 and E.2 | OK, but see E-3 and E-4 |
| Ch 1, line 355 | Appendix B gives a reproducible setup | B.1 to B.4 | OK |
| Ch 2, lines 29, 223 | Appendix A has a refresher; shows the Mermaid text syntax | A.8 | OK |
| Ch 2, lines 33, 513 | Appendix B records the toolchain and the Git commands | B.1, B.8 | OK |
| Ch 7, line 39 | Appendix B records the Maven, JUnit and Mockito setup | B.4, B.5 | OK |
| **Ch 9, lines 41, 434, 436** | **“Appendix E is planned … not written yet”** | E exists | **Stale. Needs a new sentence.** |
| **Companion Ch 9, line 2630** | **“Appendix E, which is not yet written”** | E exists | **Stale** |
| **Ch 14, line 325** | **“Appendix C will supply templates for the retrospective and decision notes, and Appendix E will give a fuller guide”** | Both exist | **Stale (future tense).** Also the retrospective and decision templates in C do not use Chapter 14's own forms (C-3, C-8) |
| Companion Ch 1, line 258 | Appendices A, B and E as navigation | Exist | OK |
| Ch 3, Ch 4 | No pointer to Appendix C, although C's templates (story, DoD, planning) are first used there | | **Missing pointer** |
| Ch 15 | No pointer to Appendix C for the AI record, although C.7 is a second template for it | | **Missing pointer, and conflicting template** (C-2) |
| Any chapter | No pointer to Appendix D (checkpoints, glossary) | | **Missing pointer** |
| Any chapter | No pointer to Appendix F | | **Missing pointer.** The blueprint asks for software around AI and data components to be a light thread in the running project. Chapter 13 (`VisitorGate`, the directory) is the natural place |

## 3. Contrast: what the appendices say about each other and about the chapters

| Where | Claim | Check | Result |
|---|---|---|---|
| A, intro | “Appendix B covers installation…; Appendix D covers project checkpoints and domain terminology.” | B yes; D has checkpoints and a glossary, but see D-1 to D-4 | Pointer OK, content not |
| B.8, B.10 | “Chapter 14 and Appendix E explain what such evidence can and cannot show” | Chapter 14 does. E covers it but with four pillars (E-5) | Partly |
| C intro | “Use Section C.8 … final project handover dossier” | C.8 is a known-issues template only; no dossier template | **S** (C-12) |
| C.7 | “Chapter 15 Section 15.8” eight-part record | 15.8 exists | Section OK; headings do not match (C-2) |
| C.8 | “Chapter 14 Section 14.5” for known issues | 14.5 is the retrospective and reflection; documents are in 14.3 | **Wrong section** (C-9) |
| E.1 | “Chapter 15 and Appendix C” for a provenance statement | The requirement itself is invented (E-3) | **S** |
| E.4 | “Week 13 (Chapter 14)” final handover | Chapter 14 is Week 13; final submission is Weeks 15 and 16 | **B** (E-1) |
| F.6 | “In Chapter 13 you used `VisitorGate`” | True | OK |
| F.7 | “companion repository (`exercises/appendix-f/starter`)” | There is no companion for F and no such folder | **B** (F-5) |

## 4. Appendix C: Engineering Templates (631 lines)

| ID | Sev | Where | Finding and evidence | Suggested fix |
|---|---|---|---|---|
| C-1 | B | C.7 example (lines 523 to 573) | The example's rejected candidate, `start.isBefore(end) && endExclusive.isAfter(start)`, is **the correct half-open overlap test**. I compared it with the book's `LoanPeriod.overlaps` on 6,084 period pairs: identical on all. The record says it “assumes `end` is inclusive”, which is false. Teaches a false lesson inside an example about verification. The example also names the story `US-05` for the availability query (that is US-02 in Chapters 3 and 4), uses `isAvailable(...)` where the Chapter 15 lab has `earliestStart(...)`, claims 6 invocations (the lab has 9), and a fault result (“2 tests fail”) with no run behind it. | Replace the example with Chapter 15's own filled record, or write a candidate whose flaw is real and say how it was found |
| C-2 | B | C.7 schema | The eight headings are renamed and numbered (`Task Definition & Scope`, `Context Provided`, …). Chapter 15's lab checks exact headings (`## Task`, `## Tool and model`, `## Context given`, `## Output received`, `## Decision`, `## Changes made`, `## Verification`, `## Limits`) with `check-record.sh`. A record made from C.7 fails that script. | Use Chapter 15's headings. My kit's `ai-assistance-record` does |
| C-3 | B | C.5 schema and example | The ADR schema (`Decision Drivers`, `Options Considered`, `Decision Outcome`, …) is not the form of ADR-010, ADR-013 and ADR-014, which Chapter 14 describes (context, decision, alternatives considered, consequences, validation and review, revisit triggers). The **example reuses the number ADR-013** with a different story: date 12 November (the real one is 13 October), a three-person team, “directory under maintenance until December”, and “`VisitorGate` will be deleted in v0.15.0 once the directory achieves 99.9% uptime for two sprints”. Chapter 14's ADR-014 **keeps** the flag at handover and rehearses removal; its conditions are three specific ones, none about uptime. A student will read this as the book's ADR-013. | Use the real headings; do not reuse a real ADR number for a fictional record |
| C-4 | B | C.1 example (US-12) | Rules contradict the book: “staff reserve up to 60 days ahead, for at most 30 days; quota 5 loans and reservations”. In the book the staff policy accepts fewer than five retained reservations and up to **14** days, and there is no advance-booking window (Chapter 5). Message text `Policy violation: active loan quota (5) reached` and id `R-1092` are not the book's (`Rejected: borrower limit or duration.`, `R1`). The intro says the examples are “drawn directly from the Campus Equipment Lending System”. | Use the book's rules and strings, or state that the example is invented |
| C-5 | B | C.3 and C.7 examples | Backlog IDs collide with Chapter 3 and 4: `US-03` (the book: borrower record inspection), `US-05` (unknown-item rejection), `US-08`, `US-12`, `TECH-02` are invented. “Student 2-item quota” (the book: fewer than three). `StudentReservationRules` (class is `ReservationRules`), `NotificationGateway` (class is `NotificationSender`). | Rename or use the book's IDs and classes |
| C-6 | S | C.3 | “Hours / Story Points” in one column and a “load factor 75 to 80%” rule contradict Chapter 4, which budgets explicit hours (22 available, 4 reserved, 18 budget, 14 selected) and warns that hour estimates are not converted from story points. | Align with Chapter 4's method |
| C-7 | S | C.4 | The example reports “34 passing test invocations”: 34 is the Chapter 2 **check** count, not JUnit invocations (JUnit starts in Chapter 7). The schema says `mvn clean verify`, the example `mvn --batch-mode verify` (Appendix B uses the latter). The checklist “rebased and free of merge commits” conflicts with B.8, where the repository setting decides merge, squash or rebase. | Align with B.8 and use correct counts |
| C-8 | S | C.6 | The template's “Average PR Cycle Time” contradicts Chapter 12, which says to call it “PR open-to-merge elapsed time” and that it is not cycle time. The example says `LoanPeriod` was extracted “into an immutable record”; it is a final class (Appendix A, Chapters 2 and 10). The quoted CRLF error `invalid option: set -euo pipefail` is not the real message (`set: pipefail: invalid option name`, Chapter 4). The retrospective drops Chapter 14's observation, evidence, action, owner table. | Use Chapter 14's table and Chapter 12's terms |
| C-9 | S | C.8 | Points to “Chapter 14 Section 14.5” (retrospective); the documents are in 14.3. The example's `$2.00` against `$1.50` per day, `LegacyOverdueReporter` and its test names do not exist: in Chapter 11 the legacy code is `legacy.FinePolicy`, and the “other kind” rate is **1.00 a day with no grace and no cap**, flagged SD-11-1 as a *suspected defect* with the question “do other kinds exist?”. The real `KNOWN-ISSUES.md` uses `KI-1` to `KI-14`, not these entries. | Quote the real rows |
| C-10 | S | C.9 sources | “Fowler … characterisation testing” (that is Feathers); “Beck … Arrange-Act-Assert” (the pattern is not from Beck's book); Clean Code is cited nowhere else in the book. No links, no access dates, none of the books opened. Scrum Guide, Keep a Changelog and Nygard (which the chapters do cite) are missing as links. | Use the sources the chapters cite, with links |
| C-11 | S | Throughout | Internal IDs in student text: “Blueprint Section 6”, “Ground Rule G1” (twice), “G4/G11”, “Blueprint G11 offline protocol” (7 occurrences). The intro also says Blueprint Section 6 requires “three elements”; it asks for a purpose and a small example. Appendices A and B have none. | Remove (cleanup rule R2) |
| C-12 | M | C intro | Says C.8 supports the final handover dossier; it is only a known-issues template. | Reword |
| C-13 | M | C.1 | “Scenario 1 … Then … And …” mixes given-when-then forms; the chapter form is one example per acceptance criterion with a “state afterwards” line. | Optional |
| C-14 | M | Coverage | Templates the chapters use and C lacks: team agreement (Ch 4), evidence note (Ch 4, Ch 12), requirements-to-evidence and release notes (Ch 14), decision note small form (Ch 3). My kit covers all of them. | See section 8 |

## 5. Appendix D: Project Checkpoints and Glossary (375 lines)

### The master table (D.2) against the chapters

Values in the left column are what Appendix D prints. The right column is what the chapters say (all taken from the chapter companions).

| Chapter | D prints: version, count | The chapters say | Source |
|---|---|---|---|
| 1 | `0.1.0-alpha`, 3 checks | no version (plain Java); **12** checks | Ch 1: “All 12 chapter checks passed” |
| 2 | `0.2.0-alpha`, 34 checks | no version; 34 checks (count OK) | Ch 2, 4 |
| 3 | `0.3.0-alpha`, 34 checks | no version; no code change; 34 checks and 5 acceptance example groups | Ch 4 README |
| 4 | `0.4.0-alpha`, **18** | 34 checks and 5 acceptance example groups | Ch 4 README |
| 5 | `0.5.0-alpha`, **26** | **44** Chapter 5 checks (runner also reports 34 and 5 groups) | Ch 5 |
| 6 | `0.6.0-alpha`, **31** | **28** Chapter 6 checks | Ch 6 |
| 7 | `0.7.0`, **7 / 48** | `0.7.0`, **35** JUnit invocations (4 wrap the older runners) | Ch 7 README |
| 8 | `0.8.0`, **72** | `0.8.0`, **63** | Ch 8 |
| 9 | `0.9.0`, **98** | `0.9.0`, **107** | Ch 9 |
| 10 | `0.10.0`, 121 | OK | Ch 10 |
| 11 | `0.11.0`, 159 | OK | Ch 11 |
| 12 | `0.12.0`, 159 | **no code and no new version**; the chapter's own text cites 136 (already an open mismatch) | Ch 12, 13 |
| 13 | `0.13.1`, 232 (203/26/3) | OK | Ch 13 |
| 14 | `0.14.0`, 235 (206/26/3) | OK | Ch 14 |
| 15 | `1.0.0`, package `edu.se506.assist`, 9 | lab version 1.0.0 and 9 tests OK; package is **`assist`** | Ch 15 |

“Alpha” versions for Chapters 1 to 6 and 0.12.0 do not exist in the book. Six of fifteen counts are wrong.

### Findings

| ID | Sev | Where | Finding and evidence | Suggested fix |
|---|---|---|---|---|
| D-1 | B | D.2 | The table above: 6 of 15 counts wrong, invented versions. The text calls it “the definitive record” and tells students to “verify your local build against” it, so a correct build would look wrong. | Replace with the right-hand column |
| D-2 | B | D.4 table 3 | Borrower rules contradict the book. Student: “2 items”; the book allows a request when fewer than **three** retained reservations exist, one to seven days. Staff: “30 days”; the book says 14. “Advance booking window 14 / 60 / 7 days” does not exist anywhere. Visitor: “1 item”; the book reuses the student count limit (fewer than three), allows only CAM1 and CAM2 for one to three days, and needs a matching approval record. Counting “active loans plus confirmed future reservations” is wrong: Chapters 12 and 13 say the repository count of retained reservations, “not an active-loan count”. | Replace with Chapters 5, 12 (CR12-1 to CR12-7) and 13 |
| D-3 | B | D.4 table 2 | Identifier formats `B-1001`, `ITEM-CAM-01`, `R-0012`, `L-5001` are not the book's (`B1`, `CAM1`, `R1`). `Money`, `FineAmount` do not exist; “`LoanPeriod` compares all fields” is false: the `LoanPeriod` listings in Chapters 2 and 10 do not override `equals`, and Appendix A says so. | Use the book's identifiers; remove the classes that do not exist |
| D-4 | B | D.4 section 4 | The equipment lifecycle (`AVAILABLE`, `OVERDUE`, `UNDER_MAINTENANCE`, `RETIRED`) is invented. The lifecycle the book teaches (Chapter 9) is the **reservation** lifecycle: REQUESTED, CONFIRMED, ON_LOAN, RETURNED and CANCELLED. | Replace with Chapter 9's states |
| D-5 | B | D.3 | Says unit tests carry `@Tag("unit")` with classes `ReservationTest`, `HttpDirectoryClientIntegrationTest`, `LendingSystemEndToEndTest`. In Chapter 13 unit tests carry **no tag**; the unit stage is `-DexcludedGroups=integration,e2e`. The real classes are `FileApprovalSourceIntegrationTest`, `DirectoryOutageIntegrationTest`, `HttpDirectoryClientContractTest` and `Chapter13JourneyE2ETest`. | Copy the real tags and class names |
| D-6 | B | D.3 “discrepancies” | SD-11-1 is described with `$2.00` and `$1.50` a day; the book has 1.00 a day for “other kinds” (no grace, no cap) and calls it a suspected defect. SD-12 is described as counting “completed loans not archived”; the book says the count rule counts every retained reservation. | Quote Chapters 11, 12, 13 |
| D-7 | S | D.1 | Isolated packages are given as `edu.se506.lending.patterns`, `.behaviour`, `.examples.structure`, `.legacy`. The package declarations in the chapters are `patterns`, `behaviour`, `examples.structure` and `legacy` (top level). | Correct |
| D-8 | S | D.6 | Glossary entries conflict with Chapter 12: cycle time is Started to Done and lead time Accepted to Done there; D says “begins active development until … ready for release” and “proposed until delivered to production”. “Double dispatch … Visitor and Strategy”: Strategy does not use double dispatch. | Align with Chapter 12; fix |
| D-9 | S | D.5 | Presents “Domain Option C: Academic Facility and Resource Scheduling” as an alternative provided domain. The descriptor names equipment lending and an ML model-serving tool as examples, and the blueprint records the second starter checkpoint as an open question. | Label as a suggestion or remove |
| D-10 | S | D.2, D.4 | Internal IDs: “Ground Rules G2 and G3” (cleanup rule R2). | Remove |
| D-11 | M | D.2 | `NotificationGateway` (the class is `NotificationSender`), `Container` (the walk-through class is `ContainerWalkthrough`). | Correct |
| D-12 | M | D.1 | Mermaid diagram labels “Ch 11: Mainline Preservation” and “Ch 12 to 14” are loose but not wrong. | Optional |

All 3 diagrams in D (the evolution map, the lifecycle state diagram) render.

## 6. Appendix E: Critical Reading and Project Evidence (316 lines)

| ID | Sev | Where | Finding and evidence | Suggested fix |
|---|---|---|---|---|
| E-1 | B | Intro, E.4 | Says the contribution evidence and final handover are **“due Week 13”**. The descriptor: Final Project “Weeks 15 to 16 (presentations and final submission)”, submitted on Moodle as repository link, technical report and individual reflection; Week 13 is the final sprint, retrospective and handover content; Week 14 is review with no classes. | Say Week 13 is when to prepare; the deadline is Weeks 15 and 16 |
| E-2 | B | E.5 | The reflection “typically 500 to 750 words, as specified in the assignment brief”. The descriptor gives no word count for the reflection. The three-part structure also differs from Chapter 14's six prompts (what I did, decided, went wrong, how I used AI, what I did not do, what I would change) and drops the AI-use prompt. | Remove the count; use Chapter 14's prompts |
| E-3 | B | E.1 | The blueprint says E “creates no new rubric or assessment policy”. E adds: “Provenance requirement … you **must** document that interaction”, “Reading cannot be outsourced … not acceptable scholarship”, “Markers give higher credit to self-aware reflections”, and “turnitin portal” (the descriptor says only “checked for similarity”). Its five “components” also differ from the descriptor's five criteria (summary 15%, critical evaluation 30%, trade-offs 25%, application 15%, structure and referencing 15%) and omit structure, clarity and referencing. | Point to the descriptor's rubric; keep it as method advice, not policy |
| E-4 | B | E.1 | A “candidate pool” of seven books is presented under “Decision D8” as if it were the approved list. The descriptor says the list is approved by the module leader and gives examples: Clean Code, Refactoring, Design Patterns, Working Effectively with Legacy Code, Accelerate. E omits Clean Code and Design Patterns, which the descriptor names. | Say the list is the module leader's; name the descriptor's examples |
| E-5 | S | E.3 | “Four pillars” (commits; reviews; architectural leadership; process) against the descriptor and Chapter 14: **commits, PR reviews and peer evaluation**. Peer evaluation is missing. | Align with Chapter 14's three kinds |
| E-6 | S | E.4 | The dossier does not match the project's real handover files: `RELEASE-NOTES-v0.14.0.md` (real: `RELEASE-NOTES-0.14.0.md`), `scripts/build-and-test.sh` (no such script; the real ones are `pipeline.sh`, `simulate-release.sh`, `demo.sh`, `handover-check.sh`), `check-setup.sh` (from Appendix B's starter, not in the lending project). The requirements table has `US-01 Student loan limits`, test `studentCannotExceedTwoActiveLoans` (the limit is three; the real table has `AC1` to `AC18` with `ac<N>_` tests in `VisitorAcceptanceTest`) and invented test names. KI-01 repeats the `$2.00`/`$1.50` figures (D-6). | Quote the real files |
| E-7 | S | E.2 template | A quotation with page numbers attributed to Martin (2002), “Chapter 8 … pp. 99 to 112”. The book was not opened and the chapter and pages are unchecked; it also quotes copyrighted text. | Use an obviously invented line, or no quotation |
| E-8 | M | E.1, E.3, E.5 | Internal IDs: “Decision D8”, “Ground Rule G7” (twice). | Remove |
| E-9 | M | E.6 | Ousterhout and Sculley are cited without links or access dates; the Accelerate description (“qualitative contribution indicators”) overreaches. | Fix |

Fine as written: the AI/data application component (E.1), the G7 caution that counts are never a measure, the notice that the appendix does not replace the descriptor, and the warning against summarising a book you have not read (as advice, not as policy). Both diagrams in E render.

## 7. Appendix F: Software Engineering for AI and Data Components (426 lines)

| ID | Sev | Where | Finding and evidence | Suggested fix |
|---|---|---|---|---|
| F-1 | B | F.5 | `ResilientRiskAssessor` does **not** bound the wait. Its `executeWithTimeout` is a stub (`// Concrete thread or executor bounding logic... return task.call();`). I compiled the printed code and ran it with a 250 ms timeout against a service that takes 1,500 ms: it **waited 1,513 ms** and returned the slow answer. This contradicts the appendix's own rule 3 (“a stalled model inference must never hang”) and Chapter 13, whose whole point is that a bounded wait must cover the whole call and be tested. It also catches every `Exception`, hiding programming errors and interrupts. | Implement it (an executor with a `Future.get(timeout)` and a cancel, as `HttpLegacyDirectoryClient` does) and test it with a slow stub |
| F-2 | B | F.7 | The exercise sends students to “the companion repository (`exercises/appendix-f/starter`)” and a file `UnsafeEquipmentScorer.java`. Neither exists: there is no companion for F and no such folder. “Verify … under 50 milliseconds” is also unverified. The exercise cannot be done. | Supply the starter or rewrite the exercise from the printed code |
| F-3 | B | F.2, F.3 | The printed types are inconsistent. The class diagram has `assessRisk(Borrower, EquipmentItem)`, `isAcceptable()`, `ConfidenceScore` and `requestReservation(BorrowerId, ItemId, LoanPeriod)`; the code has `assessRisk(String, String)`, `permitsAutomatedApproval()`, a `double` and none of those types. The coordinator method is `reserve(...)` in the book. `Borrower` exists from Chapter 8 as an immutable identifier and category value, but `EquipmentItem` is not implemented (Chapter 4: “we do not yet implement complete `Borrower` and `EquipmentItem` classes”). The block that is meant to be one file holds three public types; the fake lacks its imports. | Make diagram and code agree and match the book's names |
| F-4 | S | F.3 | The metamorphic test takes the violation counts as parameters and never uses them (`cleanViolations`, `delinquentViolations`), and `riskAdapter` is not defined, so it cannot check the property it states. It names WireMock, which is not in Appendix B's pins. | Rewrite so the data actually varies |
| F-5 | S | F.6 | `ModelRolloutGate` has a field `shadowTrafficPercentage` but routes the **decision** to the model for the bucketed users, which is a canary, not shadow mode (shadow mode needs both calls and ignores the model's answer). The text describes three patterns the class does not implement. | Rename or implement |
| F-6 | S | F.1, F.5 | Internal IDs: “Ground Rule G4” and “Decision D7” (twice). Also no chapter points to F (section 2). | Remove; add a pointer in Chapter 13 or 15 |
| F-7 | S | F.4 | The text diagram labels “ML Model Code (5%)” and credits it to Sculley et al. **Correction, later the same day:** this finding was wrong in part. The paper's first figure carries no percentage, but its glue-code section does say that a mature system might end up being at most 5% machine learning code and at least 95% glue code. The label should have cited that sentence and the section, and not the figure | Cite the glue-code section |
| F-8 | M | F.5 | `catch (Exception ex)` swallows `InterruptedException` without restoring the flag. | Fix with F-1 |
| F-9 | M | F.8 | Sources not linked, not opened. | Add links |

Both diagrams in F render.

## 8. Contrast: what I changed and published (13 October 2026)

| Change | Where |
|---|---|
| Removed the old file names (`Appendix_A_…md`, `Appendix_B_…md`) from my four pages | `content/book/appendix-a.md`, `appendix-b.md`, `content/companion/appendix-a.md`, `appendix-b.md` |
| **Published** the verified template kit as a new companion page | `content/companion/appendix-c.md` (no existing file was overwritten) |
| This report | `meta/Appendices_Review_and_Chapter_Reference_Contrast.md` |

**The new page** is a companion to Appendix C: 13 templates, 13 worked examples, a checker script and its experiments, the common mistakes per template, and a constructed AI fixture. What I ran on it:

- Rebuilt from the published page: byte-identical to the kit I tested. 26 files pass.
- Nine fault experiments and two `--file` cases (a missing path and an unknown template name): all gave the stated result.
- The checker accepts the book's own ADR-010, ADR-013, ADR-014 and the Chapter 15 filled AI record taken from the site content.
- The constructed evidence note passes the structural check (as the page says it does); a reviewer is needed for its content.
- Hugo 0.166.0 builds the page with no warnings.

**It conflicts with the existing Appendix C** in the templates for the decision record and the AI record, because it follows the chapters (C-2, C-3). That is deliberate and should be resolved by correcting Appendix C, not by publishing two forms. Until Appendix C is corrected, a reader sees two templates for the same record.

## 9. Decisions for you

1. **Appendix C.** Correct the existing Appendix C to follow the chapters (my kit already does), or replace its templates with my kit's, or leave it and treat my page as the standard. I recommend correcting C, starting with C-1 to C-3.
2. **Appendices D, E, F.** I recommend not publishing them until the blocking items are fixed. D and E need to be regenerated from the chapters and the descriptor. I can do that if you want me to; I have not touched them.
3. **Stale chapter pointers** (section 2): Chapter 9 lines 41, 434, 436 and companion line 2630, and Chapter 14 line 325. I can update them once you decide what C and E will contain.
4. **Old file names in the chapters.** About 24 pages still mention `Chapter_NN_*.md` and `Appendix_X_*.md`. Mechanical to fix. Do you want it?
5. **Missing pointers** to C (Chapters 3, 4, 15), D and F (Chapter 13 or 15).

## 10. After the corrections (13 October 2026, later)

The owner asked for Appendix C to be corrected and Appendices D and E to be regenerated from the chapters and the descriptor. The received versions are backed up (`internal_not_for_publishing/other_appendices_as_received/`, four files including F). The new versions are in `content/book/`.

### What was done to each finding

| Findings | Resolution |
|---|---|
| C-1 (false AI example) | Replaced. The new AI record explains the overlap rule; its rejected candidate says adjacent periods overlap, which is wrong, and the verification names the hand trace and the Appendix A lab |
| C-2 (AI record headings) | The eight headings are Chapter 15's. The checker accepts the Chapter 15 lab's filled record |
| C-3 (ADR form and reused number) | The headings are those of ADR-010, ADR-013 and ADR-014; the example is a new, small, clearly constructed ADR-002, and the text says the numbers are not the book's. The checker accepts the three real ADRs |
| C-4, C-5 (rules, IDs, classes) | The examples use US-02, AC-02 and the book's rules, strings and class names |
| C-6, C-7, C-8 (planning, PR, retrospective) | They follow Chapter 4's budget method, the review description of Chapters 2 and 4 and Chapter 14's observation, evidence, action, owner table; no cycle-time wording |
| C-9 (known issues) | The known-issues and requirements-to-evidence templates follow Chapter 14's documents; no invented rates or class names |
| C-10 (sources) | Scrum Guide, Nygard, GitHub's template page and Keep a Changelog, all linked and opened |
| C-11, C-12, C-14 | Internal IDs removed; C.14 points to E.4 to E.6; 13 templates cover everything the chapters use |
| D-1 to D-12 | Regenerated from the chapters. Every count in the table is asserted against the chapters' own text; the rules of the domain are those of Chapters 1, 5, 8, 9, 10, 12 and 13; identifiers, packages, tags and test classes are the real ones; the lifecycle is Chapter 9's; Option C was removed and the model-serving mapping is marked as a suggestion; the glossary entries follow the chapters and each cited section contains the term |
| E-1 to E-9 | Regenerated from the descriptor and Chapters 1, 9 and 14. The deadline is Weeks 15 and 16; no reflection word count; no new policy; the approved list is the module leader's, with the descriptor's own examples; contribution evidence is commits, PR reviews and peer evaluation; the handover files are the real ones; the quotation with page numbers was removed |

### What was removed from the received versions

These were removed because they conflicted with the chapters, the descriptor or the blueprint, or could not be checked. They can be added back as optional extras on a correct basis: the root-cause "5 Whys" in the retrospective, the task breakdown in the iteration plan, "decision drivers" in the ADR, the author self-review checklist in the pull request, the two-column dialectical note in E, and the counter-perspective sources (Ousterhout, Sculley) in E. The AI and data guidance of the old E.1 now lives in a table in E.2.

### Checks run on the new versions

- **C.** 26 template and example blocks compared with the verified kit: identical. Fences balanced, no internal IDs, no old file names. The checker passes all 26 files and accepts the book's own ADRs and AI record.
- **D.** Every count, sub-total and command asserted against the chapters (all present). `TraceabilityTest` has 3 tests, matching 232 + 3 = 235. The four diagrams render. 40 glossary entries were checked against the sections they cite; five section pointers were wrong and were corrected. D.7 now cites only sources the chapters cite (the Scrum Guide, and Fowler's Test Double and Technical Debt pages, all opened).
- **E.** Eleven descriptor facts checked; the contribution table equals Chapter 14's; the six reading-record entries equal Chapter 1's; every chapter and appendix section it cites exists; three GitHub pages opened and checked.
- **All three.** Hugo 0.166.0 builds them with no warnings; no cross-reference to an unknown appendix section; no `Ground Rule`, `Blueprint`, `Decision D` or version stamps.

### Still open

- **Appendix F** (not requested): F-1 to F-9 stand. The most serious: `ResilientRiskAssessor` does not enforce its timeout, and the exercise needs files that do not exist.
- **Chapter pointers** (not yet changed): Chapter 9 lines 41, 434, 436 and its companion line 2630 still say Appendix E is not written; Chapter 14 line 325 still uses the future tense for C and E. Chapters 3, 4 and 15 do not point to Appendix C; no chapter points to D or F.
- **Old file names** in about 24 chapter pages.

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

## 12. Chapter pointers and file names fixed (13 October 2026, later)

The owner asked for the chapter pointers and the old file names to be fixed. 41 edits in 23 pages (13 chapters and 10 companions). Each edit is listed, with its old and new wording, in `internal_not_for_publishing/Pointer_Fixes_Log.md`; the 30 chapter and companion pages as they were are in `internal_not_for_publishing/backup_before_pointer_fixes/`.

| Group | Edits | What changed |
|---|---|---|
| Old file names | 20 | Ten chapters said “the companion `Chapter_NN_Code_Explanations_and_Solutions.md`” and ten companions said “This file accompanies `Chapter_NN_<Title>.md`”. They now say “the companion for this chapter” and “This file accompanies Chapter N, <Title>.”, with the title taken from each chapter's own front matter |
| “Chapter 15 will later collect the recurring AI workflows” | 11 | Chapters 2 to 9, 11, 13 and 14: now “Chapter 15 collects the recurring AI workflows”. Chapter 10 has no such sentence and Chapter 12 belongs to another author and was not touched |
| Appendices described as unwritten or future | 3 | Chapter 9 (the reading checkpoint) and its companion now say that Appendix E develops the review method; Chapter 14 says what Appendix C (C.12, C.5) and Appendix E (E.4 to E.6) contain |
| Missing pointers | 7 | Appendix C from Chapters 3, 4, 14 and 15; Appendix D from Chapter 1; Appendix F from Chapters 13 and 15. Each names the sections that hold the material |

**Checks.** Exactly 41 lines changed, one per edit, and every changed file has the same number of lines as before; front matter and code fences are intact; no old file name and none of the stale phrases remain anywhere in `content/book` or `content/companion`; each appendix section named in a new pointer exists (15 checked); the link from Chapter 9 to its reading checkpoint still resolves. The AI-activity table of Chapter 15, Section 15.1, agrees with the titles of the activities in Chapters 1 to 11, 13 and 14.

**Not changed, on purpose.** Forward references of the ordinary kind, such as “Chapter 4 will turn the selected work into an iteration plan”. A reader meets them before the later chapter, and they are accurate. Chapter 12, which belongs to another author.

**Still open.** Nothing in section 2 of this report. The remaining items are outside the pointers: the lab and the appendices have been run on JDK 24 with `--release 17` only, and no second reader has read the new appendices.
