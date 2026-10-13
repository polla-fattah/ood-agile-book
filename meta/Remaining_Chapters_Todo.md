# Remaining chapters: working to-do list

*OO Development and Agile Practices: textbook project*
Created 13 October 2026, after Chapters 1–10 were revised against Blueprint v0.4.

**Rule from the module leader:** write the remaining chapters **one at a time, in this order**, with full attention on one chapter before starting the next. Do not draft several chapters in one pass. Use the revised blueprint (`SE506_Textbook_Blueprint_and_Authoring_Instructions.md`, v0.4) and the style, length, tone and methods of Chapters 1–10. If a session runs out of room, resume at the first unchecked item.

## How each item is done (the same method as Chapters 1–10)

1. **Read the inputs.** The blueprint's chapter specification and ground rules G1–G13; the descriptor's week; the previous chapter's manuscript and companion; this register (`Unresolved_Items_Chapters_1-3.md`) for commitments the chapter must honour (its section 4).
2. **Plan, then draft two files:** `Chapter_NN_<Title_With_Underscores>.md` (student manuscript) and `Chapter_NN_Code_Explanations_and_Solutions.md` (companion). Open with the three route entries (*Core reading*, *Minimum required lab*, *Optional extension*), label every task **Book project** or **Team project**, add the Milestone checklist where the week has a milestone, add a transfer note for other provided domains, and keep any AI activity to the AI activity contract (offline fixture labelled as constructed).
3. **Build the code from the previous verified checkpoint** (the Chapter 10 companion's 64 listings are the input to Chapter 11). Every new listing goes in the companion under `### N.N \`path\``.
4. **Verify, do not assume:**
   - extract the listings from the finished companion and build them (`mvn -o verify`; offline cached versions, see below), run every demo, run `javac -Xlint:all`;
   - run a **fault experiment** (single faults, one at a time) on the new code and strengthen any test that lets a plausible fault survive;
   - open every cited web source and check the claim it supports; for printed books that could not be opened, record this in `Unresolved_Items_Chapters_1-3.md`, not in the chapter text, and where this book covers the same material give a pointer to its own chapter or section instead;
   - render every Mermaid diagram in the browser pane.
5. **Report only what was run.** Record the environment and the counts exactly. Never claim hosted CI, JDK 17, the pinned versions or a peer review that did not happen.
6. **Close the loop:** update `Unresolved_Items_Chapters_1-3.md` (new chapter section, commitments, verification row), tick the item below, and update the blueprint if a decision moved.
7. **Stop and report** before the next chapter. Ask the module leader only for decisions that are theirs (D1–D9 and the like).

## Environment and constraints to remember

- Windows 11, Git Bash. JDK 24.0.2 only (no JDK 17). Maven 3.9.11 and the exact pinned dependencies were downloaded on 13 October 2026 with the module leader's approval (a clean local repository in the session scratchpad); Chapters 7–11 pass under them. Maven 3.9.16 from `~/.m2/wrapper`; run it as `mvn.cmd` from a script, because WSL's bash is picked up by Python `subprocess` otherwise.
- Cached and used offline: JUnit 6.0.3, Mockito 5.23.0 (ByteBuddy pinned to 1.18.11), Compiler 3.15.0, Surefire 3.5.6, Resources 3.5.0, Jar 3.5.1. The POMs in the chapters pin older versions (Maven 3.9.11, JUnit 5.13.4, Mockito 5.20.0, Compiler 3.14.1, Surefire 3.5.4); those have never been run. **Do not download anything without asking.**
- Mutation/fault scripts and rebuilt projects from earlier chapters live in the session scratchpad (`mutate7.py` to `mutate10.py`, `ch10x/mut_extra.py`, `extract_any.py`, `rebase10.py`); they are session-temporary and can be rewritten in a few lines from the pattern in the Chapter 10 companion's Section 11.2.
- The cumulative checkpoint after Chapter 10: 64 listings, 121 JUnit invocations, packages under `edu.se506.lending` plus the isolated `patterns`, `behaviour` and `examples.structure`.

## Chapter queue (one at a time)

- [x] **Chapter 11: Refactoring and Legacy Code** (drafted and verified 13 October 2026; see its section in the register) (Week 10; LO3, LO4). Legacy overdue-reporting routine with duplication, long methods and hidden time dependencies; characterisation tests that preserve an intentionally surprising behaviour; seams; Extract Method/Class, Move Method, Rename; incremental commits and rollback; technical debt as evidence. AI activity: a refactoring patch that changes a boundary condition. Cross-reference Chapter 5; Quiz 2 preparation covers Chapters 6–10. Decide how the legacy routine joins the cumulative project (probably an isolated package, like `patterns`).
- [x] **Chapter 12: Measuring Progress, Flow and Technical Health** (drafted and verified 13 October 2026) (Week 11; LO5, LO6). Synthetic issue history; start/end events before durations; velocity versus throughput; burn charts and scope; the **repository-metrics lab (G1, D9)**: derive cycle time or throughput from real git or PR data, with a stated method; the visiting-researcher change requirement and its impact analysis; refer to Chapter 10 for package instability. Preserve the pre-change checkpoint for Chapter 13.
- [x] **Chapter 13: Integration, Delivery and Feedback** (drafted and verified 13 October 2026; see its section in the register) (Week 12; LO3, LO6; Milestone 4). Integration and contract tests, focused E2E, CI stages and gates, delivery versus deployment, one feature flag with both paths tested and a removal plan, the visiting-researcher rule implemented, one real boundary tested against a controlled local service. Needs D1 (integration boundary) decided or an explicit interim choice. AI activity: an integration test that replaces the boundary it claims to test. Hosted CI has never been run: say so.
- [x] **Chapter 14: Responding to Change and Handing Over** (Week 13; LO1–LO6). Review of the change outcome, defects and scope control, documentation and ADRs, reproducible setup, retrospective and individual reflection, final submission preparation. Contribution evidence (G7) described qualitatively; commit counts never treated as a measure of work. AI activity: validate a drafted README and release note. (drafted and verified 13 October 2026; see its section in the register)
- [x] **Chapter 15: AI as a Software Engineering Assistant** (reference chapter). Sections 15.1–15.9 as in the blueprint; vendor-neutral; date any tool-specific instructions; constructed versus captured samples labelled (G11). Chapters 1–9 now mention Chapter 15 only as later reading; check their wording matches the finished sections. (drafted and verified 13 October 2026; see its section in the register)
- [x] **Appendix A: Programming readiness and notation** (diagnostic, Java refresher, exception handling, the Java idioms allowed (D2), class-diagram notation and legend; verified). Chapters 1–2 point to it.
- [x] **Appendix B: Tools and reproducible setup** (runtime, build and test commands, Git and PR workflow, starter CI, and the pinned tools for the DI container (D3), mocking framework (D4), static analysis (D5) and repository metrics (D9)). Chapters 1, 2, 5, 6 and 7 point to it. Several entries depend on decisions that are still open; record them as open rather than inventing them. (drafted 13 October 2026; see its section in the register)
- [x] **Appendix E: Critical reading and project evidence** (critical review method, dialectical reading journal, contribution evidence guide G7, handover dossier, reflection framework; drafted 13 October 2026).
- [x] **Appendix C: Engineering templates** (story, acceptance criteria, DoD, planning, PR, retrospective, ADR, AI verification record; drafted 13 October 2026).
- [x] **Appendix D: Project checkpoints and glossary** (checkpoints, cumulative vs isolated map, invariants, domain transfer map, authoritative glossary; drafted 13 October 2026).
- [x] **Appendix F: Software Engineering for AI and Data Components** (model contracts, gateways, non-determinism, metamorphic tests, Sculley debt, fallback policies, D7; drafted 13 October 2026).
- [ ] **Book-wide consistency review** (blueprint writing-order step 8): terminology, cross-references, commitments table, counts, links, route entries, Book/Team labels, and the open-decision register.

## Chapter 11 outcome (for the next chapter's inputs)

- The input checkpoint for Chapter 12 is the **Chapter 10 companion (Version 1.1) plus the Chapter 11 companion (Version 1.1, merged with a second draft)**, which lists only the files that are new or changed. It has 159 JUnit invocations. The optional bridge classes (`OverdueRowSource`, `OverdueReportService`, `LoanSnapshotRows`) are in bootstrap. Later companions should say which revisions they start from, and may use the same delta style.
- Isolated packages now: `patterns`, `behaviour`, `examples.structure` and `legacy`. The dependency test forbids production references to all of them.
- The generator approach worked well: write the companion as a template with `@@code:path@@` placeholders and fill it from the verified files, then extract the finished Markdown and rebuild it (`ch11x/gen_companion.py`, `extract11.py`; session-temporary).

## Chapter 13 outcome (for the next chapter's inputs)

- The input checkpoint for Chapter 14 is the **Chapter 10 companion (Version 1.1), the Chapter 11 companion (Version 1.1) and the Chapter 13 companion (Version 1.1, corrected 13 October 2026)**, which lists only the files that are new or changed. It has **232 JUnit invocations** (159 inherited, 73 new: 203 unit, 26 integration, 3 end-to-end) and project version 0.13.1 (0.13.0 was the first version, with 230). Chapter 12 changes no code.
- New in the checkpoint: the VISITOR category, `VisitorReservationRules`, `VisitorGate` (one flag, default off), `FileApprovalSource` (real file adapter), `HttpLegacyDirectoryClient` (one attempt, bounded wait, no retry, no fallback), `Chapter13Demo`, the pipeline and release scripts, a hosted-runner workflow (never run) and ADR-013. Chapter 14 reviews how the design accommodated the change and decides the flag's removal (ADR-013 sets the condition).
- Still unresolved and named in Chapter 13: SD-11-1 (a late visitor is charged at the report's "other kind" rate) and SD-12 (the count rule counts every retained reservation).
- **Chapter 12 (another author) does not match the Chapter 11 of this series**: it cites a 136-test Chapter 11 suite and an "SD-11: due-today inclusion preserved" line. The owner of Chapter 12 should reconcile these. Chapter 13 used CR-12, its eighteen acceptance examples and its backlog as written.

## Chapter 14 outcome (for the next chapter's inputs)

- The input checkpoint for Chapter 15 is the Chapter 10, Chapter 11, Chapter 13 and **Chapter 14 companions** (all delta listings), version 0.14.0 (Chapter 14 companion Version 1.1), **235 JUnit invocations** (206 unit, 26 integration, 3 end-to-end; Version 1.0 had 233). No production code changed in Chapter 14.
- New: `TraceabilityTest`, `DemoRun`, `scripts/demo.sh`, `scripts/handover-check.sh`, the handover documents in `docs/` (HANDOVER, REQUIREMENTS-TO-EVIDENCE, KNOWN-ISSUES with 14 items, RELEASE-NOTES-0.14.0, ADR-014), `rehearsal/remove-visitor-flag.patch` (tested, not applied) and `ai-activity/README-draft.md` and `README-corrected.md`.
- Chapter 15 should keep the verification-record idea (task, context, output accepted or rejected, verification performed); Chapter 14 section 14.7 and the Chapter 13 AI activity are worked examples. Appendix C (templates) and Appendix E (final handover, reflection and contribution-evidence guide, G7) are referred to from Chapter 14 as not yet written.

## Chapter 15 outcome (for the appendices and the consistency review)

- Chapter 15 has **no entry checkpoint and no carry-forward**. Its worked example is a small stand-alone Maven project, the **lab** (`assist-lab`, 9 acceptance tests), listed in full in the Chapter 15 companion. The lending project stays at the Chapter 14 handover version 0.14.0 (233 invocations).
- The lab holds: the accepted `AvailabilityFinder`, two constructed AI attempts (rejected), their work orders, a record template, a filled record and `scripts/check-record.sh`, and three more constructed fixtures (an explanation of `VisitorGate`, a privacy example, a dependency suggestion).
- **Appendix C (templates)** should include the AI assistance record template (Chapter 15 section 15.8; `docs/AI-RECORD-TEMPLATE.md`) and the retrospective and decision-note templates that Chapter 14 refers to. **Appendix E** should cover final handover, individual reflection and contribution evidence (G7); Chapter 14 section 14.5 is its starting point. **Appendix B** should say that the build must compile with `--release 17` and why (Chapter 15 section 15.4).
- **Consistency review item (done 13 October 2026):** Chapters 2-14 said "Chapter 15 will later collect the recurring AI workflows"; changed to the present tense in 11 chapters (Chapter 12 belongs to another author). Also check each chapter's AI activity row against the table in Chapter 15 section 15.1.

## Needs the module leader's attention later

- **JDK 17 download and run** (declined for now, 13 October 2026). All verification is on JDK 24.0.2 with `--release 17`. Do not claim a Java 17 runtime run in any chapter until this is done.

## Decisions that block or shape later chapters (the author cannot settle these)

| ID | Needed by | Note |
|---|---|---|
| D1 integration boundary | Chapter 13 | Chapter 8 used a synthetic in-process fixture. Chapter 13 must say what boundary it adds. |
| D3 closed (the educational container is the lab tool; Chapter 6 wording applied), D5 closed (PMD 7.28.0; Chapter 5 lab built) | Appendix B | Appendix B lists no library container for D3, and pins PMD 7.28.0 with the download and digest steps from Chapter 5 companion §1.3. |
| D4 mocking permission in the midterm | Appendix B | Module leader. |
| D7 AI/data collaborator | Chapters 13–14 and Appendix B | **Closed 13 October 2026:** the directory is the data-component route. Chapter 13 must add a timeout and an explicit fallback-or-failure policy for it (an outage is never “not found” and never defaults a borrower to staff). |
| D8 approved reading list | Appendix E | Module leader. |
| D9 repository-metrics method | Chapter 12 | Author and module leader. |

When a chapter needs one of these and it is still open, write the chapter with an explicit interim choice, label it as interim in the text and the register, and carry on. Do not mark a decision closed.
