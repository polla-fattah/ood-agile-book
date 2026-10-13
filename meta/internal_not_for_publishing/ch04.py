from cleanup_lib import *
C = "Chapter_04_Code_Explanations_and_Solutions.md"
replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 • reviewed against Blueprint v0.3\n", "*OO Development and Agile Practices*\n", 4, "header version line", evidence=True)
rewrite_line(C, "All people, workload figures and review scenarios in the model answers are fictional.",
  "All people, workload figures and review scenarios in the model answers are fictional.", 4, "Line 13: second sentence about the verification record removed")
rewrite_line(C, "`CHAPTER_JAVAC` is an optional path to a compiler executable.",
  "`CHAPTER_JAVAC` is an optional path to a compiler executable. Ordinary use leaves it unset, selecting `javac`. It is a single executable path, not a place to put a multiword shell command. Some environments provide `java` but no `javac` launcher, and the override is for them; learners with a normal JDK should not need it.",
  4, "Line 549: the sentence about the author environment reworded")
# section 10: verification part to evidence, keep teaching notes
cut(C, 4, "Section 10.1, Observed author verification (whole subsection)",
    "### 10.1 Observed author verification",
    "### 10.2 Teaching emphasis and next checkpoint",
    replacement="Martin (2002) and Rubin (2012) use the publication details given in the module descriptor and were not independently looked up.\n")
replace_once(C, "## 10. Verification record and teaching notes", "## 10. Teaching notes")
replace_once(C, "### 10.2 Teaching emphasis and next checkpoint\n\n", "")
rewrite_line(C, "Blueprint v0.3 continuity:",
  "The practical activity runs on the Team project with the lending starter as the model. The starter test is introduced in Arrange–Act–Assert terms for Chapter 7, and the Chapter 2 flat directory is mapped onto the conventional source layout. Milestone 1 needs hosted CI evidence, which depends on a repository the whole team can use. Ask teams to create that repository in the first session, so a late access problem does not become the only gap in their evidence.",
  4, "Section 10.2, paragraph 'Blueprint v0.3 continuity' (checklist part removed)")
log(4, [
 "Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).",
 "Companion section 10 `Verification record and teaching notes` is now `Teaching notes`. The whole subsection `10.1 Observed author verification` moved to evidence: the Linux and OpenJDK 17.0.20 run of version 1.0, the Windows 11 / JDK 24.0.2 re-verification, the table of script exit codes, workflow YAML and action versions, the Git workflow replay, the CRLF and WSL results, the Mermaid rendering, the list of checks not performed, and the note on sources opened on 12 and 13 October 2026 (R3, R8).",
 "The CRLF and `.gitattributes` result is not lost from the book: it is explained in the student chapter and in the companion's section 3.3a, so only the author's experiment table was moved.",
 "Kept and relocated: the sentence that Martin (2002) and Rubin (2012) use the publication details given in the module descriptor and were not independently looked up (pending your decision on `not opened` notes).",
 "The former `10.2 Teaching emphasis and next checkpoint` is now the body of section 10, its heading removed because it was the only subsection left. Nothing else referred to it.",
 "Rewrote the `Blueprint v0.3 continuity` paragraph, keeping the guidance on the starter test, the source layout and the first-session repository, and removing the checklist and the Blueprint reference (R2).",
 "Line 13 of the companion: removed the sentence that pointed to the verification record in Section 10. Line 549: the sentence `The author environment used this override as explained in Section 10` is now `Some environments provide java but no javac launcher, and the override is for them`.",
 "Manuscript: no change. `Sources checked 12 and 13 October 2026` is an access date and stays.",
])
print("chapter 4 done")
