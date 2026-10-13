# First-draft cleanup: change log (NOT FOR PUBLISHING)

One entry per chapter: what was removed or rewritten, where the evidence went, and anything the module leader should look at. Originals are in `backup_before_cleanup/`.

## Chapter 1

- Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).
- Companion section 4: retitled `Use in later chapters`. The verification paragraphs (listing extraction, `javac` 24.0.2, the 12-check run, the two single-fault results, the note about an earlier OpenJDK 17.0.20 run, the Blueprint decision D2 mention, the note that four web sources were opened on 12 October 2026) moved to `evidence/Chapter_01_Verification_Evidence.md` (R3, R8).
- Companion section 4: the closing note about how future companions should be written was a note to the author, not student content. Moved to evidence.
- Kept: the teaching paragraph about Chapter 1 planning the staff change. The two single-fault results are also taught in the companion's section 2 (the deliberate fault), so no fault table was lost from the book.
- Manuscript: no change. Its source note says `Web sources were checked on 12 October 2026`, which is an access date and stays.

## Chapter 2

- Companion: removed the `Version 1.2 • 13 October 2026 • reviewed against Blueprint v0.3; UML section expanded` line (R1, R2, R4).
- Companion section 11: the paragraph beginning `Blueprint v0.3 continuity:` was a conformity checklist written for the author (which parts are Book or Team project, which blueprint items are covered). It also held the teaching sentence about the planned sequence (Chapter 2 flat files, Chapter 4 source folders, Chapter 7 Maven and JUnit). Rewrote it to keep that sentence and the module-leader point about Java idioms, without `Blueprint v0.3` and `Blueprint D2` (R2). Original moved to evidence.
- Companion section 12 `Verification record` removed entirely and moved to evidence (R3, R8): re-verification note, `javac --release 17` on JDK 24.0.2, the earlier OpenJDK 17.0.20 mention, the table of demo and check results (34 checks), the line-count difference between the two coordinator variants, the two fault results (the same two faults are taught in section 10, so nothing was lost from the book), the Git sequence replay, the Mermaid rendering note, the `LoanPeriod` signature check, the note on web sources opened, and the Blueprint D2 mention. Replaced by a two-line `12 Sources` section that keeps the closing statement that examples are original.
- Manuscript: no change. Source note `Web sources were checked on 12 and 13 October 2026` is an access date and stays.

## Chapter 3

- Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).
- Companion section 12 retitled `Instructor guidance` (was `Instructor guidance and verification record`).
- Verification details moved to evidence: the re-verification paragraph (extraction, `javac --release 17` on JDK 24.0.2, the earlier OpenJDK 17.0.20 run), and the paragraph about web sources (opened on 12 and 13 October 2026; four Scrum.org pages returned HTTP 403 in version 1.0 and were replaced; Martin and Rubin).
- Kept as teaching content: the fault table, now introduced by a new subsection `12.1 Do the acceptance examples detect faults?` with one plain sentence, and the point that AC-03's extra request closes a gap (reworded to remove `version 1.0`).
- Kept: the sentence that Martin (2002) and Rubin (2012) are cited with details from the module descriptor and were not independently looked up. It was left in place at first and then replaced by a pointer to this book's chapters (see the section `'Not opened' source notes` at the end of this log).
- Rewrote the paragraph `Blueprint v0.3 continuity` (a checklist of what the chapter contains) to keep the guidance on marking the process note and the transfer note; removed the Blueprint reference and the checklist.
- Reworded `were checked for consistency with the student chapter` to `are consistent with the student chapter` (R3).
- Manuscript: no change. Source note `Sources were checked on 12 and 13 October 2026` is an access date and stays.

## Chapter 4

- Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).
- Companion section 10 `Verification record and teaching notes` is now `Teaching notes`. The whole subsection `10.1 Observed author verification` moved to evidence: the Linux and OpenJDK 17.0.20 run of version 1.0, the Windows 11 / JDK 24.0.2 re-verification, the table of script exit codes, workflow YAML and action versions, the Git workflow replay, the CRLF and WSL results, the Mermaid rendering, the list of checks not performed, and the note on sources opened on 12 and 13 October 2026 (R3, R8).
- The CRLF and `.gitattributes` result is not lost from the book: it is explained in the student chapter and in the companion's section 3.3a, so only the author's experiment table was moved.
- Kept and relocated: the sentence that Martin (2002) and Rubin (2012) use the publication details given in the module descriptor and were not independently looked up (later replaced by a pointer to this book's chapters; see the section `'Not opened' source notes` at the end of this log).
- The former `10.2 Teaching emphasis and next checkpoint` is now the body of section 10, its heading removed because it was the only subsection left. Nothing else referred to it.
- Rewrote the `Blueprint v0.3 continuity` paragraph, keeping the guidance on the starter test, the source layout and the first-session repository, and removing the checklist and the Blueprint reference (R2).
- Line 13 of the companion: removed the sentence that pointed to the verification record in Section 10. Line 549: the sentence `The author environment used this override as explained in Section 10` is now `Some environments provide java but no javac launcher, and the override is for them`.
- Manuscript: no change. `Sources checked 12 and 13 October 2026` is an access date and stays.

## Chapter 5

- Companion: removed the `Version 1.2 • 13 October 2026 • reviewed against Blueprint v0.4` line and the `Version note` paragraph about adding the PMD lab (R1, R2). The PMD lab itself is untouched.
- Companion section 12 `Verification record and teaching notes` is now `Teaching notes`. In `12.1`, the two version paragraphs (Linux and OpenJDK 17.0.20; Windows 11 and JDK 24.0.2) and the results table moved to evidence: gate and checkpoint results (34 and 44 checks), `javac -Xlint:all`, shared-file comparison, Mermaid rendering, the PMD results, the PMD download details (file size, SHA-256 from GitHub, Maven Central 404, signature not checked), the PMD environment, and the not-performed items (R3, R8).
- The PMD findings are also in the companion's section 7.1b and in the student chapter, so no PMD result was lost from the book. The download-and-compare-digest instruction is in section 1 and is unchanged.
- Kept: the 14-fault experiment and its explanation of the equivalent survivor. `12.1` is now titled `Do the new checks detect faults?`, taking over the bold lead-in question. Subsections 12.2 and 12.3 are unchanged.
- Section 1: the sentence `The author environment needed the compiler override documented in Section 12` now says `no compiler override is needed with a normal JDK installation` only.
- Manuscript: no change. `Sources checked 12 and 13 October 2026; PMD sources 8 and 9 on 13 October 2026` are access dates and stay.

## Chapter 6

- Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).
- Companion section 13 `Verification record` is now `Fault experiment and container notes`, with two subsections: `13.1 Do the checks detect faults?` and `13.2 Container lab`.
- Moved to evidence (R3, R8): the two version paragraphs (Linux and OpenJDK 17.0.20; Windows 11 and JDK 24.0.2), the 12-row results table (gate results, `-Xlint:all`, file comparisons, Mermaid, `PrintStream` error flag, not-performed items), the Real-container feasibility paragraph (a Spring Framework 7.0.9 experiment using jars from the author's Maven cache) and the `Sources` paragraph (sources opened on 12 and 13 October 2026; the Martin 2000 PDF; the Spring wording).
- Kept: the 14-fault table. Removed the `Survived in 1.0` history from the row about catching `RuntimeException`, and removed `version 1.0` and `version 1.1` from the lead-in and from the earlier paragraph about the two further checks. The faults are the same, and all fourteen are caught.
- Rewrote the `Container lab (Blueprint decision D3, closed 13 October 2026)` paragraph as a plain description of the lab tool, keeping that the module descriptor mentions a real container and the book pins none. It no longer points to the feasibility note that was moved (R2, R7).
- Kept: the closing paragraph that expected container errors are caught inside the demonstration, which is teaching content.
- Manuscript line 35: `verification evidence` is now `teaching notes`, because the verification record is no longer in the companion. Manuscript line 334: removed `(version 1.1 of the companion, 13 October 2026)`.
- Manuscript: the source note `Sources checked 12 and 13 October 2026` is an access date and stays.

## Chapter 7

- Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).
- Companion line 9: `observed verification evidence` is now `teaching notes`. Tool table: removed `author runtime OpenJDK 17.0.20` (R8).
- Companion section 12 `Verification record` moved to evidence in full: the version 1.0 and version 1.1 paragraphs (OpenJDK 17.0.20; Maven 3.9.16 and the cached versions; the table of differing versions), the exact-configuration run (Maven 3.9.11 with SHA-512 check, JDK 24.0.2, clean repository), the two results tables (red, green and refactor cycle; mutation and restoration; reconstruction), the cached-versions observation table, and the sentence that the author's network needed proxy settings (R3, R8). Section 12 is now `12. What the build establishes` and keeps two paragraphs: the inventory of the 35 invocations (an expected-output statement) and the limits statement that a Maven report does not establish provider behaviour, storage, concurrency, identity or milestone completeness.
- Section 6.1, the wider fault experiment: this was a real inconsistency, not just history. The text said `Fourteen were rejected` and listed fourteen rows, and then said the `loans()` snapshot fault is now caught, so the final suite rejects fifteen and one survives. Rewrote the lead-in to say fifteen are rejected (fourteen in the table and the loan snapshot after it) and one is not (the equivalent add-then-remove change). Removed the sentence about an earlier counting error (`version 1.1 said fifteen and thirteen`), `Two faults survived the version 1.0 tests`, and `Version 1.1 adds one assertion...`. Please check this reading of the counts: it follows the experiment results kept in the evidence file.
- Companion Mockito warning paragraph: removed JDK 24, Mockito 5.23.0, `JDK 17 was not available for this review` and `5.20.0 was not downloaded`. The advice stands.
- Manuscript: the practical warning about the Mockito agent no longer names JDK 24.0.2 or compares two Mockito versions; the source note no longer says that the companion records which versions were run. `Sources checked 12 and 13 October 2026` is an access date and stays. The `Asia/Baghdad` time zone in the manuscript's checkout-date example is teaching content (a local-date example) and stays.
- Manuscript line 422: removed the reference `(Blueprint D4)` after `it has not yet been confirmed for this book` (R2). The sentence still tells students to follow the module leader's instructions about what the exam permits.

## Chapter 8

- Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).
- Companion section 11.2 `Observed local verification` is now `Do the tests detect faults?`. Moved to evidence (R3, R8): the version 1.0 and 1.1 paragraphs (OpenJDK 17.0.20; Maven 3.9.16 with cached versions), the exact-configuration run (Maven 3.9.11, JDK 24.0.2, clean repository, 63 tests), the first observation table (compared files, `-Xlint:all`, exercise solutions, Mermaid) and the second table (full verify, inherited suite, new tests, preserved sources, reconstruction, not-performed items).
- Kept: the 20-fault experiment table. Removed the environment sentence, `With version 1.0's tests, nineteen were caught and one survived`, and the note about an earlier counting error from its lead-in, and rewrote the Factory Method row (`Survived in 1.0`) as a description of what the test catches and why the null check matters. All twenty are caught by the current tests.
- Kept: the note that the 35 inherited invocations include four wrappers, the Mockito agent note (now `on a recent JDK`), the sentence that the check counts must not be added as if equal, and the limits paragraph.
- Section 7: the paragraph that said `Version 1.0 only predicted which tests would reject these candidates. In version 1.1 all three were actually applied` now says that the three candidates were applied one at a time and each was rejected by the named tests.
- Manuscript: no change. `Checked 12 and 13 October 2026` is an access date and stays.
- Companion section 11 retitled `Instructor guidance` (was `Instructor guidance and verification record`).

## Chapter 9

- Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4). Tool table: removed `author runtime OpenJDK 17.0.20` (R8).
- Companion section 12 `Verification record` is now `Fault experiment and limits`, with a subsection `12.1 Do the tests detect faults?`. Moved to evidence (R3, R8): the version 1.0 and 1.1 paragraphs (OpenJDK 17.0.20; Maven 3.9.16 and the cached versions), the exact-configuration run (Maven 3.9.11, JDK 24.0.2, 107 tests), the first observation table (compared files, `-Xlint:all`, Mermaid) and the second table (full verify, inherited suite, new tests, reconstruction, not-performed items).
- Kept: the 18-fault experiment. Removed the history that sixteen were caught in version 1.0 and two survived, and the sentence that the invocation count stays at 107. The two Command rows that read `Survived in 1.0` now say what catches each fault and what would miss it (a construction-validation test; an exact-confirmation assertion), which keeps the lesson. All eighteen are caught by the current tests.
- Kept: the notes on lifecycle table rows and inherited runners, the limits paragraph (concurrency, delivery, authentication, transactions, replay), and the Mockito agent note (now `on a recent JDK`).
- Section 10: removed `Version 1.0 only predicted which tests would reject these alternatives. In version 1.1...` and kept that two of the alternatives were applied and rejected.
- Manuscript: no change. `Checked 12 and 13 October 2026` is an access date and stays. The sentence that Appendix E is planned but not written is left alone (decision pending for the appendices).

## Chapter 10

- Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • reviewed against Blueprint v0.4` line, the paragraph `What changed in this version` (nine stale files restored, package-cycle check, and so on), and the mention of `Chapter 9 companion, Version 1.1 (reviewed 13 October 2026)` (R1, R2, R4).
- ADR-010 inside the companion: `Date: 13 October 2026 (Asia/Baghdad)` is now `Date: 13 October 2026`. The ADR is a teaching example, so the date line stays.
- Section 2.5 (assertions and fixes carried forward) is teaching content and stays. Only `(28 checks, not 26)` became `(28 checks)`. The sentence in the tests section `Three of these tests were added in Version 1.1` now reads `exist because the fault experiment in Section 11.2 found gaps`.
- Companion section 11 retitled `Instructor notes`. Subsection 11.2 `Verification record` is now `11.2 Do the tests detect faults?`. Moved to evidence (R3, R8): the version 1.0 and 1.1 paragraphs (OpenJDK 17.0.20 with 118 invocations; the finding about nine stale files; Maven 3.9.16 and the cached versions), the exact-configuration run (Maven 3.9.11, JDK 24.0.2, 121 tests), and the results table (reconstruction, full verify, bridged runners, migrated files, demonstrations, `-Xlint:all`, package metrics, Option B experiment, Mockito warning, not-performed items).
- Kept the 25-fault experiment. It compared two suites, `118 invocations` and `version 1.1`. Rewrote it as `before the three added tests` and `with the final tests`, with the same results: 20 caught before, 23 now, two survivors (an equivalent mutant and a documented limit). The lead-in and the paragraph after the table no longer name invocation counts. Check this reading: nothing about the faults or results changed, only the labels.
- The closing limits sentence no longer mentions the pinned dependency versions or Java 17 (those were statements about the author's run).
- Manuscript: the source note `manuscript revised 13 October 2026, Asia/Baghdad` removed; the access dates stay.

## Chapter 11

- Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • reviewed against Blueprint v0.4` line and the `Version note` paragraph that says the file merges in material from a second draft (R1, R2, R4, R7).
- Companion section 1: the input checkpoint paragraph no longer says `Version 1.1 (13 October 2026)` or `121 JUnit invocations`; step 1 of the reconstruction no longer says `(Version 1.1)`. First paragraph: `the verification record` is now `teaching notes`. ADR-011: time zone removed from the date line.
- Companion section 12 retitled `Instructor notes`. Subsection 12.2 `Verification record` is now `12.2 Do the tests detect faults?`. Moved to evidence (R3, R8): the environment paragraph (Maven 3.9.16, JDK 24.0.2, cached versions, no JDK 17), the exact-configuration run (Maven 3.9.11, clean repository, 159 tests), and the results table (reconstruction details, full verify, stages, stage C, probe, demonstrations, package metrics, dependency tests, staff grace experiment, Mockito warning, not-performed items).
- Kept: the two-round fault experiment and its tables, including the note that the first round's surviving null-kind case led to a new test. The staff-grace-period result is also taught in section 8. Closing limits sentence no longer names the stated environment, pinned versions, Java 17 or hosted CI.
- Manuscript: entry checkpoint no longer says `with its 121 JUnit invocations` (R5); line 38 `the verification record` is now `teaching notes`; the source note no longer says `the manuscript was written the same day, Asia/Baghdad` (the access date stays).
- Not changed: the project README listing inside the companion (it states the project's own counts, 159 and 121) and the `Asia/Baghdad` time zone in Java code and tests (teaching examples of local dates).

## Chapter 12

- NOT EDITED (written by another author). Items for its owner, in the order they appear:
- Manuscript line 6 and companion line 5: `Version 1.0 • 13 October 2026`.
- Companion section 8 `Verification record and limits`, and the tool-table row `Full JDK 17; locally checked with 17.0.20`.
- References to a `136-test` Chapter 11 suite (companion lines about the baseline and the acceptance matrix; manuscript line 181) and to `SD-11: due-today inclusion preserved; policy unresolved`. These do not match the Chapter 11 and Chapter 13 files of the other chapters (see `SE506_Chapters_12_to_15_Assessment_and_Change_Plan.md`, item S1). That is a baseline decision, not a cleanup item.
- Manuscript source note `Sources checked 13 October 2026` is an access date and can stay.

## Chapter 13

- Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4` line and the whole `Version note` (the three corrections found by the independent review). The files-changed list in that note went to evidence (R1, R2, R4, R7).
- Section 1: first paragraph, `and the verification record` is now `and teaching notes`; the input checkpoint paragraph no longer names `Version 1.1` of the Chapter 10 and 11 companions or `159 JUnit invocations`; reconstruction steps 1 and 2 no longer say `(Version 1.1)`; `only the project version becomes 0.13.0` is now `only the project version changes`.
- Section 1: the paragraph `Boundary decision (Blueprint D1, interim)` is now `The two boundaries`, a plain description. It keeps the point that a different boundary would change the adapters and keep the policy table and tests, and drops the Blueprint ID and `The module leader has not yet decided D1`. The same interim sentence was in the ADR-013 listing's `Status` line, now `Implemented teaching example; peer review pending`, and its date line lost `(Asia/Baghdad)`. **Note:** the working project folder still has the old ADR-013 text. It is not published.
- Section 1.0 `Checkpoint manifest` (Blueprint version, SHA-256 of the Chapter 10 and Chapter 11 companions, verified build line) moved to evidence (R6, R8).
- Section 1.2: `On the verification machine (Section 12.2) the passing run was:` is now `A passing run looks like this:`. Removed the references to the old Section 12.2 (empty-stage check, simulated release). `Section 12.3` references now say `Section 12.2` (three places), and B3 says the fault table lists thirty faults (it said twenty-seven).
- Section 7.8 was `The timeout defect, found in review`; it is now `A timeout that does not cover the body`, a neutral lesson. Removed: the Version 1.0 client, `A review of the chapter`, the review's OpenJDK 17.0.20 figure, the JDK 24.0.2 probe figures and `I did not run the probe on a Java 17 runtime`. Kept: the JDK documentation point, the 300 ms and 1,600 ms case, the asynchronous fix with cancellation [13][14], the table of what the new test shows (fails against a client that relies on the request timeout alone with `execution timed out after 5000 ms`; passes against the chapter's client, which fails the lookup after about 330 ms), and the list of what did not change. Please read it once: it is the main narrative change in this chapter.
- Section 7.9: removed `Figure 13.3 of Version 1.0 put the count and duration rules before the register was read`; the paragraph now starts from the observable order of checks. The test and the point that a different precedence needs a contract change are unchanged.
- Section 12 retitled `Instructor notes`. Removed from 12.1 the paragraph `Alignment with Chapter 12` (notes about the mismatch with the other author's chapter and the scripts of Chapter 13 versus 14; also in the register). Section 12.2 `Verification record` (Windows 11, Maven 3.9.11, JDK 24.0.2, the reconstruction paragraph, the results table, the timeout probe, the review's Java 17 figure) moved to evidence. The fault experiment became 12.2.
- Kept: the 30-fault table and its notes. Removed `Version 1.0 ran twenty-seven faults against 230 invocations`, the `exact configuration` and `232 invocations` wording, the note that two mutants did not compile at first, and the closing sentence about what the experiment of Version 1.0 could not find (now: `Before the stalled-body test existed, ...`).
- Manuscript: see the manuscript entry below.
- Project README listing inside the companion: `only the project version becomes 0.13.0` was stale (the project is 0.13.1) and is now `only the project version changes (to 0.13.1)`.
- Manuscript 13.2: **formatting repair.** The heading `A timeout that covers less than you think` had been joined to the end of the policy paragraph on one line. It is a heading again, on its own line.
- Manuscript 13.2, `A timeout that covers less than you think`, rewritten as a neutral lesson, with the same arguments: removed `An earlier version of this chapter's client`, `A review of the chapter then ran`, the JDK 24.0.2 and OpenJDK 17.0.20 figures, `the old client`, `the corrected client`, and `a review that tries a different one is evidence you cannot produce alone` (now `A second reader, or a fault experiment that applies a different fault, can find what you could not`). Please read it once.
- Manuscript: entry checkpoint no longer says `159 JUnit invocations` or `The completed checkpoint has 232 invocations` (R5); line 38 `the verification record` is now `teaching notes`; in 13.7 `The 159 invocations ... passed unchanged ... total to 232` is now `The inherited Chapter 11 tests passed unchanged after that edit`; the source note lost `the manuscript was written the same day, Asia/Baghdad`.

## Chapter 14

- Manuscript: removed test counts from prose (R5): the opening problem (`232`/`235`, now `one number ... another`), the entry checkpoint (`232 JUnit invocations`, `235 invocations`), the E1 and E2 experiments on the Chapter 11 checkpoint (`45 of 159`, `from 45 to 5`, `all 159`, now `more than a quarter of the suite`, `drop to five tests`, `the whole Chapter 11 suite passes`), the B1 experiment (`73 of its 235`, now `roughly three in ten tests`), the E3 experiment (`228 of the 232`, `203 unit invocations`, now `Every unit test passes`), the rehearsal (`233 invocations`), the handover-check description (`206`, `26`, `3`) and the evidence index (`235 invocations`). The exact figures stay in the companion (section 5.2).
- Line 38: `the verification record` is now `teaching notes`. Section 14.4: `on the machine used for the book` and `JDK (24.0.2, compiling for 17)` removed. Question 6: `expect 233 tests` now says `expect a stated number of tests`. Source note: `the manuscript was written the same day, Asia/Baghdad` removed.
- Kept: the lessons and the dry-run findings, including the finding that the first version of the `mvn` message was wrong (it is about testing a fix, not about document versions), the contribution fixture (synthetic, labelled), the constructed review, and the sentence about what not to claim. The `230 tests` in the AI-drafted README is part of the constructed fixture and stays.
- Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4` line and the `Version note` (rebuild on the corrected Chapter 13; the four review changes) (R1, R2, R4, R7). The sentence `(Section 10.2 records the check)` was removed from `No production code changed`. The input checkpoint paragraph no longer names `Version 1.1` or `232 JUnit invocations`.
- Section 1.0 `Checkpoint manifest` (Blueprint version, SHA-256 of the Chapter 10, 11 and 13 companions) moved to evidence (R6).
- Project documents in the listings: the HANDOVER.md text `(the checks recorded here used JDK 24.0.2)` removed; the time zone removed from the dates of RELEASE-NOTES and ADR-014. The counts that `HANDOVER.md` promises (235, 206, 26, 3) are kept: the handover check reads them. **Note:** the working project folder still has the old wording in these documents. It is not published.
- Section 5.2: removed `under the exact configuration (Section 10.2)`, the sentence that the first version of this chapter described E3 as a limit of unit testing (`Version 1.1 corrects that`), and the paragraph with the Version 1.0 figures for E3 and B1. The experiment table keeps its figures (they are the companion's evidence tables, each labelled with its checkpoint). Section 5.3: the directory bullet no longer says `a review found that its first timeout did not cover a stalled body` or `The first version of this note said...`. Section 5.5 and 5.6: `on the verification machine`, `on JDK 24.0.2` and `233 invocations` removed.
- Section 10 retitled `Instructor notes`. Removed from 10.1 the paragraph `Alignment with the other chapters` (the scripts of Chapter 13 versus 14, and the Chapter 12 mismatch). Section 10.2 `Verification record` moved to evidence (Windows 11, Maven 3.9.11, JDK 24.0.2, the reconstruction paragraph, the results table, Mermaid and sources). **That table's pipeline row still said `205, 25 and 3` after the rebuild (it should have said `206, 26 and 3`), so the evidence file records a stale figure, flagged here.** The fault experiment is now `10.2 Do the checks detect faults?`; two references to `Section 10.3` (companion) and one in the manuscript now say `Section 10.2`.
- Kept: both fault experiments (the six faults against `TraceabilityTest`, the three against the handover check) and their limits. The closing sentence no longer mentions the stated environment, Java 17, hosted CI or independent review (the chapter's own limits statements, section 14.6, remain).
- Section 1, first paragraph: `and the verification record` is now `and teaching notes`.

## Chapter 15

- Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4` line and the `Version note` (the four review changes) (R1, R2, R4, R7). First paragraph: `and the verification record` is now `and teaching notes`.
- Section 10 retitled `Instructor notes`. Section 10.2 `Verification record` moved to evidence: Windows 11, Maven 3.9.11, JDK 24.0.2, the reconstruction paragraph, the results table (including the check-record results and the dependency status codes), and the row with the independent review's Java 17 results (OpenJDK 17.0.20, attributed to the review). The fault experiment is now `10.2 Do the tests detect faults?` and the one reference to `Section 10.3` was updated.
- Kept: the ten-fault experiment table and its explanation, the dependency status table in section 6.6 (it is the exercise's own evidence, with the command and date), and the closing limits sentence without `the stated environment` and `behaviour on a Java 17 runtime`.
- Model record `docs/AI-RECORD-earliest-start.md` inside the listings, and the compile table in section 6.1 and flawed alternative 8.2: `JDK 24.0.2` and `JDK 24` replaced by `a JDK of version 21 or later` or `a newer JDK`. The record still names Maven 3.9.11 and `--release 17`, because a verification record should name the commands. Its Limits line now says the code was compiled for Java 17 and run on a newer JDK, so no Java 17 run is claimed. **Note:** the working lab folder still has the old text. It is not published.
- Manuscript: line 47 `and the verification record` is now `and teaching notes`; the 15.4 sentence about plain `javac` no longer says `JDK 24`; the reference to the fault experiment now says `Section 10.2`; the source note lost `the manuscript was written the same day, Asia/Baghdad`.
- Not changed: the headings `Verification` inside the AI assistance record template and the filled record. They are fields of the record that the chapter teaches (section 15.8), not verification records of the book.
- Project documents in the listings: three remaining mentions of `JDK 24.0.2` / `JDK 24` (the HANDOVER.md requirements table, the gap G5 row of the requirements-to-evidence table, and known issue KI-8) now say `a newer JDK`. The statement that no Java 17 run was made is kept in each.
- Section 9 (flawed alternatives): `The test added in Version 1.1 sends exactly that request` now reads `The console test in the final suite sends exactly that request`.
- Manuscript 14.1, assumptions table, the directory row: removed `A review then found that its first timeout did not cover a stalled body, so the bounded wait was corrected`; it now says Chapter 13 observed the failures a transport brings, including a timeout that has to cover the whole answer.

## 'Not opened' source notes: decision (b), remove and point to this book's chapters

- Decided by the module leader after the first cleanup: remove the `not opened` notes and put a pointer to this book's own chapters in their place. The removed wording is in each chapter's evidence file.
- Chapter 3, `Chapter_03_Code_Explanations_and_Solutions.md`: `Martin (2002) and Rubin (2012) are cited with the publication details given in the module ...` became `Martin (2002) and Rubin (2012) are cited in the student chapter; this book treats Agile practices and Scrum in`
- Chapter 4, `Chapter_04_Code_Explanations_and_Solutions.md`: `Martin (2002) and Rubin (2012) use the publication details given in the module descriptor ...` became `Martin (2002) and Rubin (2012) are cited in the student chapter; this book treats sprint planning and iteratio`
- Chapter 8, `Chapter_08_Creating_and_Connecting_Objects.md`: `The classic book is a bibliographic foundation; the linked publisher excerpts are the port...` became `The design patterns used here are treated in this chapter and, for the behavioural patterns, in Chapter 9.`
- Chapter 9, `Chapter_09_Designing_Changing_Behaviour.md`: `The classic book is a bibliographic foundation, not a claim that its complete text was acc...` became `The behavioural patterns used here are treated in this chapter.`
- Chapter 10, `Chapter_10_Code_Explanations_and_Solutions.md`: `Not opened for this chapter; publication details are from the module descriptor....` became `This book treats package design in Section 10.4 of Chapter 10.`
- Chapter 10, `Chapter_10_From_Classes_to_Application_Structure.md`: `The book itself was not opened for this chapter, and its publication details come from the...` became `This chapter treats package design in Section 10.4.`
- Chapter 11, `Chapter_11_Refactoring_and_Legacy_Code.md`: `the Week 10 reading is its refactoring chapter. Not opened for this chapter; publication d...` became `the Week 10 reading is its refactoring chapter. This chapter treats refactoring in Sections 11.5 and 11.6.`
- Chapter 11, `Chapter_11_Refactoring_and_Legacy_Code.md`: `Not opened; the working definition of legacy code and of a seam are Feathers's, and the ch...` became `The working definition of legacy code and of a seam are Feathers's, and the characterisation-testing descripti`
- Chapter 13, `Chapter_13_Integration_Delivery_and_Feedback.md`: `Not re-opened for this chapter; the features were exercised by the project's own build....` became `This book treats JUnit tests in Chapter 7 and the use of test tags in Section 13.4.`
- Chapter 13, `Chapter_13_Integration_Delivery_and_Feedback.md`: `Not opened for this chapter; publication details come from the module descriptor....` became `This book treats testing in Chapter 7 and integration and end-to-end testing in Sections 13.1 to 13.3.`
- Chapter 13, `Chapter_13_Integration_Delivery_and_Feedback.md`: `The module's recommended reading for Week 12 (selected chapters). Not opened....` became `The module's recommended reading for Week 12 (selected chapters). This chapter treats pipelines, delivery and `
- Chapter 13, `Chapter_13_Code_Explanations_and_Solutions.md`: `Sources 10–12 are not re-opened here....` became `(removed)`
- Chapter 14, `Chapter_14_Responding_to_Change_and_Handing_Over.md`: `The handbook itself was not opened....` became `This chapter treats retrospectives in Section 14.5.`
- Chapter 14, `Chapter_14_Responding_to_Change_and_Handing_Over.md`: `Not opened for this chapter; publication details come from the module descriptor....` became `Chapters 2 to 13 of this book cover the material to review, and this chapter shows how to evidence it.`
- Chapter 14, `Chapter_14_Code_Explanations_and_Solutions.md`: `Source 10 is not re-opened here....` became `(removed)`
- Chapter 15, `Chapter_15_AI_as_a_Software_Engineering_Assistant.md`: `Only the abstract page was read....` became `This chapter treats dependencies in Section 15.7.`
- Not changed: the lines that only say `Publication details as listed in the module descriptor` (Chapters 2-9) because they do not say that the book was not read. Chapter 12 was not edited.
- Companion, Section 11.1: `The author has not opened a PR, run hosted CI or claimed an independent reviewer.` became `The sample is an example: it has no real reviewer and no hosted CI run behind it.` (an author-process statement turned into a statement about the sample).

## Appendix A

- Manuscript and companion: removed the `Version 1.0 • 13 October 2026` line under the title block (R1, R2).
- Companion: Section 7 `Verification record` moved to evidence (OpenJDK 17.0.20 run through `java com.sun.tools.javac.Main`, the five-row results table, the remark that Mermaid rendering was not completed because the browser runtime could not be installed, and the closing limits paragraph). `References` now follows Section 6 directly. The fault-experiment limits are still stated in Section 3.
- Backups of both files are in `backup_before_cleanup/`; the removed text is in `evidence/Appendix_A_Verification_Evidence.md`.
- Not changed (not requested): manuscript line 16 (`a particular Chapter 11 baseline`), the dependency sentence in A.8, References item 2 in the companion, and the `planned to add` wording about Appendix A in Chapters 1 and 2. The `checked 13 October 2026` source access dates are kept.
- Re-verification in this session: the four listings were extracted from the companion and compiled with `--release 17 -Xlint:all` (no warnings), printed the six expected lines with 27 checks, and the `count <= 3` fault failed with `AssertionError: fourth reservation rejected`. Run on JDK 24.0.2, not a Java 17 runtime. All 12 source links returned HTTP 200. The two Mermaid diagrams were not rendered.

## Appendix A follow-up (pointers and small fixes)

- Chapter 1: `Appendix A is planned to add a short Java refresher.` is now `Appendix A has a short Java refresher and a readiness diagnostic.`; `(Appendix A will add a refresher)` is now `(Appendix A has a refresher)`.
- Chapter 2: `Appendix A is planned to add a short refresher.` is now `Appendix A has a short refresher.`
- Appendix A manuscript: `a particular Chapter 11 baseline` is now `any of its checkpoints`; the dependency sentence in A.8 was rewritten (a field implies a dependency, but the diagram shows only the association; a dependency arrow is for a weaker link such as a parameter or local variable).
- Appendix A companion: References item 2 (not a reference) became a plain sentence that the supporting references are listed in the main appendix.

- Mermaid rendering check (13 October 2026): the two diagrams (Figure A.1 and the D10 scenario model) were extracted from the files and rendered with Mermaid 10.9.1 in the browser pane. Both rendered without errors; the multiplicities are at the intended ends. Not checked: print/PDF layout.

## Appendix A: UML reference drafted (A.8)

- Manuscript A.8: the class-relationship table has a new last column, `Drawn by hand`, for each relationship.
- Manuscript A.8: the one-sentence note about Mermaid sequence syntax was replaced by three subsections: `Sequence diagrams` (Figure A.2), `State diagrams` (Figure A.3) and `Flowcharts and dependency views` (Figures A.4 and A.5). Each has a symbol table with the Mermaid source, how it is drawn by hand and how to read it, plus one small original example and a short `do not infer` paragraph. The text points to Figures 6.2, 8.2, 10.1, 11.1 and 13.2, which are the book's own flowchart, sequence and dependency figures.
- The book draws no UML component diagrams: Chapter 10's package view is a flowchart. The reference says so and describes the formal UML package and component notation in one paragraph.
- Manuscript opening paragraph, A.9 and Sources: pointers to the new material; two new sources (Mermaid state diagrams, Mermaid flowcharts). Companion Section 4: new `Reading practice` table for sequence, state and flowchart fragments with two questions.
- No blank hand-drawing worksheet was added. That depends on the open question of how the midterm diagram is produced.

- Mermaid check of the new A.8 diagrams (13 October 2026): all six Appendix A diagrams rendered with Mermaid 10.9.1 in the browser pane, none with a syntax error; the sequence, state and flowchart figures were viewed. The renderer repeats each sequence participant box at the bottom; the table now says so. The two new Mermaid sources (state diagrams, flowcharts) returned HTTP 200. Print/PDF layout not checked.

## Appendix B (written clean, 13 October 2026)

- New files: `Appendix_B_Tools_and_Reproducible_Setup.md` and `Appendix_B_Code_Explanations_and_Solutions.md`. Written to the cleanup rules from the start: no version line, no verification record, no test counts of the book's own project in prose, no machine-specific wording beyond a labelled sample output, no author-process notes about sources.
- The verification record is in `evidence/Appendix_B_Verification_Evidence.md` (environment, results, fault experiments, digests, sources, and a list of what was not verified).
- Chapter 1 (line 352), Chapter 2 (line 510) and Chapter 7 (line 36): `Appendix B is planned ...` is now `Appendix B gives / collects / records ...` (present tense). Chapter 2 line 30 was already in the present tense.
- Register: Appendix B entries ticked, a new section `Appendix B` added with the open items, and the PMD, D4 and Chapter 5 table rows updated. `Remaining_Chapters_Todo.md`: Appendix B ticked.

## Appendices A to F reviewed; Appendix C companion published (13 October 2026, evening)

- After the textbook was moved into `FrontEndBook/content/`, the other appendices C, D, E and F were found in `content/book/`. All six appendices were reviewed against the chapters, the module descriptor and the blueprint. Report: `meta/Appendices_Review_and_Chapter_Reference_Contrast.md`.
- My Appendices A and B: removed the old file names (`Appendix_A_Code_Explanations_and_Solutions.md` and similar) from `content/book/appendix-a.md`, `appendix-b.md`, `content/companion/appendix-a.md` and `appendix-b.md`. Wording now refers to "the Appendix A companion" and "This file accompanies Appendix A".
- Published `content/companion/appendix-c.md`: the template kit (13 templates, 13 examples), the checker and the constructed AI fixture. It follows the headings of the chapters' own records. No existing page was overwritten. Evidence: `evidence/Appendix_C_Companion_Verification_Evidence.md`.
- Not changed, on purpose: Appendices C, D, E and F (written by someone else), and the stale pointers in Chapters 9 and 14 (waiting for the decision on what C and E will contain).

## Appendices C, D and E corrected and regenerated (13 October 2026, later)

- Instruction from the owner: correct Appendix C, regenerate D and E. Backups of C to F as received: `other_appendices_as_received/`.
- `content/book/appendix-c.md`: rebuilt from the verified template kit (13 templates, 13 examples, chapter-faithful headings). The pointer to E was fixed (E.4 to E.6).
- `content/book/appendix-d.md`: regenerated from the chapters; counts, rules, identifiers, packages, tags, lifecycle and glossary now match them. `content/book/appendix-e.md`: regenerated from the descriptor and Chapters 1, 9 and 14.
- Not changed: Appendix F; the stale pointers in Chapters 9 and 14; the old file names in the chapters.
- Evidence: `evidence/Appendices_C_D_E_Correction_Evidence.md`. Findings and resolutions: `Appendices_Review_and_Chapter_Reference_Contrast.md`, section 10.

## Appendix F corrected (13 October 2026, later)

- Instruction from the owner. Backup of the received version: `other_appendices_as_received/appendix-f.md`.
- `content/book/appendix-f.md` rebuilt around the tested risk lab; new companion `content/companion/appendix-f.md` (29 files, the starter, the acceptance tests, a model solution, fifteen fault experiments, answers).
- Appendix D (D.1) now lists `risk-lab` as an isolated example; Appendix E (E.2) points to Appendix F. Nothing else outside F was changed.
- Correction to my review report: the 5% remark is in the Sculley paper (F-7).
- Evidence: `evidence/Appendix_F_Correction_Evidence.md`; findings and resolutions: section 11 of `Appendices_Review_and_Chapter_Reference_Contrast.md`.

## Chapter pointers and old file names fixed (13 October 2026, later)

- Instruction from the owner. 41 edits in 23 pages; each listed in `Pointer_Fixes_Log.md`. Backups: `backup_before_pointer_fixes/`.
- 20 old file names removed; 11 sentences `Chapter 15 will later collect ...` made present tense; Chapter 9 (and its companion) and Chapter 14 no longer describe Appendices C and E as unwritten; 7 new pointers (C from Chapters 3, 4, 14, 15; D from Chapter 1; F from Chapters 13, 15).
- Chapter 12 was not touched (other author).
- Check script: `verify_pointers.py`.

## Site address: no folder locally, a new folder name when published (13 October 2026, later)

- Request from the owner: the local pages should be at `http://localhost:1313/book/chapter-04/` and not under `/oop-and-agile/`; the published address should be `https://polla.dev/ood_agile-book/` (it was `https://polla.dev/oop-and-agile/`).
- `hugo.yaml`: `baseURL` is now `https://polla.dev/ood_agile-book/`.
- New `config/development/hugo.yaml`: `baseURL: http://localhost:1313/`. `hugo server` uses the development environment, so locally the site is at the root; a plain `hugo` build uses the published address.
- `.github/workflows/deploy.yml`: the build step no longer overrides the address. It read `${{ steps.pages.base_url }}`, which is always empty, so it always built for `https://polla.dev/frontend-book/`; it is now `hugo --minify`, which uses `hugo.yaml`.
- Hand-written links that depended on the folder were made independent of it with Hugo's `relref`: `content/slides/_index.md` (10 links, which carried `/oop-and-agile/`), `content/book/_index.md` (1) and `content/topics/_index.md` (30), which had been written without any prefix and so were broken under any folder.
- Backups of the five edited files: `backup_before_baseurl/`. Script: `fix_baseurl.py`.
- Checked: a production build and a development build (127 pages each) and a link crawl of both; a real `hugo server` on another port. See the report to the owner for the numbers.
- Not changed: the GitHub repository URLs (`github.com/polla-fattah/oop-and-agile`), which name the repository and not the site folder.

