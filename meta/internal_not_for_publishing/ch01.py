from cleanup_lib import *
C = "Chapter_01_Code_Explanations_and_Solutions.md"
# R1/R2: version line
replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 • reviewed against Blueprint v0.3\n", "*OO Development and Agile Practices*\n", 1, "header version line", evidence=True)
# R3: verification paragraphs of section 4
cut(C, 1, "Section 4, verification paragraphs",
    "**Verified on 13 October 2026 (review of version 1.0).** The three listings were extracted programmatically from this file, so the code that was run is the code printed here. `ReservationRules.java` and `Chapter01Demo.java` were also confirmed identical to the listings in the student chapter. They were compiled with `javac` 24.0.2 (Java SE 24.0.2+12) and run as follows.",
    "Chapter 1 asks students to plan the staff change, not implement a complete redesign. Suggested acceptance examples and design alternatives therefore appear in the solutions without adding a premature implementation. Later chapters will develop the running system, introduce more explicit responsibilities, and test the resulting changes.")
cut(C, 1, "Section 4, closing note to the author",
    "For future chapters, this second Markdown file should retain the same role: complete code listings, explanations, exercise solutions, useful additional examples, and a concise statement of what was actually verified. Keep the student chapter separate so its exercises remain usable before students consult the answers.",
    None, keep_evidence=True)
replace_once(C, "## 4 Verification and use in later chapters", "## 4 Use in later chapters")
log(1, [
 "Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).",
 "Companion section 4: retitled `Use in later chapters`. The verification paragraphs (listing extraction, `javac` 24.0.2, the 12-check run, the two single-fault results, the note about an earlier OpenJDK 17.0.20 run, the Blueprint decision D2 mention, the note that four web sources were opened on 12 October 2026) moved to `evidence/Chapter_01_Verification_Evidence.md` (R3, R8).",
 "Companion section 4: the closing note about how future companions should be written was a note to the author, not student content. Moved to evidence.",
 "Kept: the teaching paragraph about Chapter 1 planning the staff change. The two single-fault results are also taught in the companion's section 2 (the deliberate fault), so no fault table was lost from the book.",
 "Manuscript: no change. Its source note says `Web sources were checked on 12 October 2026`, which is an access date and stays.",
])
print("chapter 1 done")
