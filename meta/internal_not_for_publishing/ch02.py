from cleanup_lib import *
C = "Chapter_02_Code_Explanations_and_Solutions.md"
replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.2 • 13 October 2026 • reviewed against Blueprint v0.3; UML section expanded\n", "*OO Development and Agile Practices*\n", 2, "header version line", evidence=True)

old = [l for l in read(C).split("\n") if l.startswith("Blueprint v0.3 continuity:")]
assert len(old) == 1
new = "The Java 17 baseline and the plain `javac` workflow are working choices. The sequence is deliberate: Chapter 2 uses flat files compiled by `javac`; Chapter 4 moves them into conventional source folders with a plain-Java Bash gate; Chapter 7 introduces Maven and JUnit. Chapter 4 explains the migration. Which Java idioms are permitted in assessments is for the module leader to decide."
replace_once(C, old[0], new, 2, "Section 11, paragraph 'Blueprint v0.3 continuity'", evidence=True)

cut(C, 2, "Section 12, Verification record (whole section)",
    "## 12 Verification record",
    None, replacement="## 12 Sources\n\nTechnical source references are in the student chapter. The examples and suggested solutions here are original teaching material.\n")
log(2, [
 "Companion: removed the `Version 1.2 • 13 October 2026 • reviewed against Blueprint v0.3; UML section expanded` line (R1, R2, R4).",
 "Companion section 11: the paragraph beginning `Blueprint v0.3 continuity:` was a conformity checklist written for the author (which parts are Book or Team project, which blueprint items are covered). It also held the teaching sentence about the planned sequence (Chapter 2 flat files, Chapter 4 source folders, Chapter 7 Maven and JUnit). Rewrote it to keep that sentence and the module-leader point about Java idioms, without `Blueprint v0.3` and `Blueprint D2` (R2). Original moved to evidence.",
 "Companion section 12 `Verification record` removed entirely and moved to evidence (R3, R8): re-verification note, `javac --release 17` on JDK 24.0.2, the earlier OpenJDK 17.0.20 mention, the table of demo and check results (34 checks), the line-count difference between the two coordinator variants, the two fault results (the same two faults are taught in section 10, so nothing was lost from the book), the Git sequence replay, the Mermaid rendering note, the `LoanPeriod` signature check, the note on web sources opened, and the Blueprint D2 mention. Replaced by a two-line `12 Sources` section that keeps the closing statement that examples are original.",
 "Manuscript: no change. Source note `Web sources were checked on 12 and 13 October 2026` is an access date and stays.",
])
print("chapter 2 done")
