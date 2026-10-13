# Chapter 2: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_02_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.2 • 13 October 2026 • reviewed against Blueprint v0.3; UML section expanded

---

## From `Chapter_02_Code_Explanations_and_Solutions.md`: Section 11, paragraph 'Blueprint v0.3 continuity'

Blueprint v0.3 continuity: the chapter labels Parts A–C as Book project and Part D as Team project, covers the class-diagram notation the midterm assesses (Section 2.6 and the kit exercise), includes issue-board setup and a branch-policy decision (the Week 1 lab), and gives Core reading, Minimum required lab and Optional extension entries. The Java 17 baseline and plain `javac` workflow are working choices. The sequence is deliberate: Chapter 2 uses flat files compiled by `javac`; Chapter 4 moves them into conventional source folders with a plain-Java Bash gate; Chapter 7 introduces Maven and JUnit. Chapter 4 explains the migration. Permitted Java idioms for assessments remain a module-leader decision (Blueprint D2).

---

## From `Chapter_02_Code_Explanations_and_Solutions.md`: Section 12, Verification record (whole section)

## 12 Verification record

**Re-verified on 13 October 2026 (review of version 1.0).** All Java listings were extracted programmatically from this file, so the code that ran is the code printed here. Both coordinator variants were compiled with `javac --release 17` from JDK 24.0.2, which enforces the Java 17 language and API baseline the chapter states. Version 1.0 recorded a run on OpenJDK 17.0.20 invoked through `java com.sun.tools.javac.Main`; that run was not repeated.

| Check | Observed result |
|---|---|
| Starting variant: demo and checks | Demo printed the four expected lines; `All 34 chapter checks passed.` |
| Completed variant: demo and checks | Identical demo output; `All 34 chapter checks passed.` |
| Difference between variants | Four added lines (`return confirmationFor(reservation);`, a closing brace, a blank line and the helper's signature); nothing removed |
| Fault 10.1: `return reservations;` | Demo ran; checks failed with `snapshot unmodifiable: expected UnsupportedOperationException` |
| Fault 10.2: `reservations.add(reservation);` removed | Second request printed `Confirmed: R1` instead of being rejected; checks failed with `one success stored` |
| Git sequence in Section 5 | Replayed in an unpublished scratch repository with Git 2.54.0: baseline commit, `git switch -c`, extraction, `git diff`, staging, `git diff --staged`, commit and clean status. A plain `git diff` after staging printed nothing. The second commit changed only `ReservationCoordinator.java` (1 file, 4 insertions) |
| Mermaid diagrams | All six diagrams rendered without error with Mermaid 10.9.1: Figures 2.1–2.4 in the student chapter, and the compact diagram in 6.2 and the kit solution in 6.2a in this file. The interface stereotype displayed in Figures 2.2, 2.3, 2.4 and 6.2a. In a screenshot of the rendered diagrams, the filled diamond, hollow diamond, hollow triangle and dashed lines appeared as the chapter describes |
| `LoanPeriod` excerpt in Section 2.6 | Every signature in the excerpt was matched against the real `LoanPeriod.java` |

The Java excerpts in the student chapter match this file, except the deliberately unsafe getter in Section 2.3, which appears here as the fault in Section 10.1. No push, hosted pull request or actual peer approval is claimed. The checks establish selected behaviour under the stated sequential, in-memory assumptions, not production readiness.

The nine web sources in the student chapter (sources 1–9) were opened on 12 and 13 October 2026. Source 10, the Martin textbook, is a printed book whose pages were not checked; its Week 1 reading is described as the descriptor words it, with no page numbers. Each page exists and supports the claim the chapter makes about it. The Java 17 baseline is the working choice until the toolchain decision (Blueprint D2) is closed.

Technical source references are in the student chapter. The examples and suggested solutions here are original teaching material.

---

