from cleanup_lib import *
C = "Chapter_05_Code_Explanations_and_Solutions.md"
replace_once(C, "*OO Development and Agile Practices*  \n## 1. How to use this file", "*OO Development and Agile Practices*\n\n## 1. How to use this file")
rewrite_line(C, "The scripts change to their own checkpoint root, compile application and check sources",
  "The scripts change to their own checkpoint root, compile application and check sources, then run the relevant checks. Ordinary learner setup uses `javac`; no compiler override is needed with a normal JDK installation.",
  5, "Section 1, sentence about the author environment and Section 12 (reworded)")
cut(C, 5, "Section 12.1, Observed author checks (version paragraphs and results table)",
    "### 12.1 Observed author checks",
    "**Do the new checks detect faults?** Fourteen deliberate faults were introduced one at a time into a copy of the `after` checkpoint, and the full gate was run on each.",
    replacement="### 12.1 Do the new checks detect faults?\n")
rewrite_line(C, "**Do the new checks detect faults?** Fourteen deliberate faults",
  "Fourteen deliberate faults were introduced one at a time into a copy of the `after` checkpoint, and the full gate was run on each.",
  5, "Section 12.1, lead-in (bold question moved into the heading)")
replace_once(C, "## 12. Verification record and teaching notes", "## 12. Teaching notes")
log(5, [
 "Companion: removed the `Version 1.2 • 13 October 2026 • reviewed against Blueprint v0.4` line and the `Version note` paragraph about adding the PMD lab (R1, R2). The PMD lab itself is untouched.",
 "Companion section 12 `Verification record and teaching notes` is now `Teaching notes`. In `12.1`, the two version paragraphs (Linux and OpenJDK 17.0.20; Windows 11 and JDK 24.0.2) and the results table moved to evidence: gate and checkpoint results (34 and 44 checks), `javac -Xlint:all`, shared-file comparison, Mermaid rendering, the PMD results, the PMD download details (file size, SHA-256 from GitHub, Maven Central 404, signature not checked), the PMD environment, and the not-performed items (R3, R8).",
 "The PMD findings are also in the companion's section 7.1b and in the student chapter, so no PMD result was lost from the book. The download-and-compare-digest instruction is in section 1 and is unchanged.",
 "Kept: the 14-fault experiment and its explanation of the equivalent survivor. `12.1` is now titled `Do the new checks detect faults?`, taking over the bold lead-in question. Subsections 12.2 and 12.3 are unchanged.",
 "Section 1: the sentence `The author environment needed the compiler override documented in Section 12` now says `no compiler override is needed with a normal JDK installation` only.",
 "Manuscript: no change. `Sources checked 12 and 13 October 2026; PMD sources 8 and 9 on 13 October 2026` are access dates and stay.",
])
print("chapter 5 done")
