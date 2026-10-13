# First-draft cleanup: working to-do (NOT FOR PUBLISHING)

Started 13 October 2026. Decisions by the module leader, from `SE506_First_Draft_Cleanup_Candidates.md`:

1. Verification records move to an internal evidence file (one per chapter, in `evidence/`). They are removed from the published chapter files.
2. Test counts are removed from manuscript prose. They stay in each companion's "Expected output" and in the project's own handover check.
3. SHA-256 manifests are removed (moved to evidence).
4. History and review narratives are rewritten as neutral lessons, carefully, and the text is changed where the lesson needs it.
5. Source notes saying "not opened" are removed and replaced by a pointer to the chapters of this book (decided by the module leader; done, 16 notes, see the change log). Chapter 12 not touched.
6. Chapter by chapter, manuscript and companion.
7. Evidence goes into separate files that are not for publishing. The originals of every file are in `backup_before_cleanup/`.

Chapter 12 is by another author: it is not edited. Its two cleanup candidates are listed in the change log for its author.
Appendix pointers (H) and "not yet written" wording are left alone (Appendix A is being written by someone else).

## The rules applied to every chapter

- R1 Remove the `Version ...` line and any "Version note" / "What changed in this version" paragraph. Keep the title and subtitle lines.
- R2 Remove "reviewed/written against Blueprint v0.x" and other blueprint or decision IDs (G-rules, D-decisions); rewrite "interim decision" wording as plain description.
- R3 Move each verification record to `evidence/`. If a section mixes instructor or teaching notes with verification, keep the teaching notes. Keep the fault-experiment tables (the manuscripts cite them) but strip machine, JDK, date and run details. Repair every cross-reference to a moved section.
- R4 Remove "Asia/Baghdad" and sentences about when the manuscript was written. Keep access dates for web sources.
- R5 Remove test counts from manuscript prose. Keep the experiment results as descriptions, with exact figures only in the companion.
- R6 Remove SHA-256 checkpoint manifests (to evidence).
- R7 Rewrite history/review narratives as neutral lessons.
- R8 Replace machine-specific wording ("JDK 24.0.2") in student text by "a recent JDK" where the sentence is still useful.

## To do

- [x] Chapter 1 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 2 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 3 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 4 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 5 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 6 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 7 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 8 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 9 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 10 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 11 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 12 — NOT EDITED (other author); items listed in the change log
- [x] Chapter 13 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 14 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Chapter 15 — manuscript, companion (done 13 October 2026; see the change log)
- [x] Cross-chapter check: all files searched again for the markers; fences checked; cross-references to moved sections repaired. Register update still to do
- [x] Appendix A — manuscript, companion (done 13 October 2026; see the change log)
- [x] Appendix B — written clean (manuscript, companion); evidence in `evidence/Appendix_B_Verification_Evidence.md`
- [x] Appendices A to F reviewed and contrasted with the chapters' references (13 October 2026): see `Appendices_Review_and_Chapter_Reference_Contrast.md`. Appendix C companion (template kit) published. C, D, E, F by another author: blocking items listed, not edited.
- [x] Appendices C (corrected), D and E (regenerated), 13 October 2026; F untouched; chapter pointers pending
- [x] Appendix F corrected (risk lab, companion), 13 October 2026; chapter pointers and old file names still pending
- [x] Chapter pointers and old file names fixed, 13 October 2026 (41 edits, 23 pages; see Pointer_Fixes_Log.md)
- [x] Site address: local server without a folder; published address https://polla.dev/ood_agile-book/ (13 October 2026). Open: the GitHub Pages repository or custom domain must serve the site at that path
