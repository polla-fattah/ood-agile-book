# Chapter 1: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_01_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3

---

## From `Chapter_01_Code_Explanations_and_Solutions.md`: Section 4, verification paragraphs

**Verified on 13 October 2026 (review of version 1.0).** The three listings were extracted programmatically from this file, so the code that was run is the code printed here. `ReservationRules.java` and `Chapter01Demo.java` were also confirmed identical to the listings in the student chapter. They were compiled with `javac` 24.0.2 (Java SE 24.0.2+12) and run as follows.

| Version | Observed result |
|---|---|
| Original | `Chapter01Demo` printed `true` and `false`; `Chapter01Checks` printed `All 12 chapter checks passed.` |
| `<= 7` changed to `< 7` | `Chapter01Checks` failed with `mayRequest(2, 7) expected true but got false` |
| `< 3` changed to `<= 3` | `Chapter01Checks` failed with `mayRequest(3, 1) expected false but got true` |

Version 1.0 of this file recorded a run on OpenJDK 17.0.20. That run was not repeated; the code uses no features newer than Java 8, so both results are consistent. The book's working baseline is Java 17 (`--release 17`); confirming the JDK installed on the module's institutional machines remains an open module-leader item (Blueprint decision D2). The only run recorded in this file for the current revision used JDK 24.0.2, so it is not a new Java 17 run. These examples need no external dependencies, database, network service or AI account.

The four web sources cited in the chapter were opened on 12 October 2026. Each page exists, and each supports the specific claim the chapter makes about it.

---

## From `Chapter_01_Code_Explanations_and_Solutions.md`: Section 4, closing note to the author

For future chapters, this second Markdown file should retain the same role: complete code listings, explanations, exercise solutions, useful additional examples, and a concise statement of what was actually verified. Keep the student chapter separate so its exercises remain usable before students consult the answers.

---

