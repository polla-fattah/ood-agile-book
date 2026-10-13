from cleanup_lib import *
C = "Chapter_03_Code_Explanations_and_Solutions.md"
replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 • reviewed against Blueprint v0.3\n", "*OO Development and Agile Practices*\n", 3, "header version line", evidence=True)
replace_once(C, "## 12 Instructor guidance and verification record", "## 12 Instructor guidance")
rewrite_line(C, "The six backlog items, top-story criteria, board snapshot and AI classifications were checked",
  "The six backlog items, top-story criteria, board snapshot and AI classifications are consistent with the student chapter. Proposed or hypothetical states are identified; no claim is made that US-02 through US-05 or EN-01 are implemented. The period convention and numeric rules match Chapter 2, and the example DoD does not pretend that an automated pipeline already exists.",
  3, "Section 12, paragraph on consistency checks (reworded)")
rewrite_line(C, "**Re-verified on 13 October 2026 (review of version 1.0).**",
  "### 12.1 Do the acceptance examples detect faults?\n\nEach change below was made on its own to a copy of `LoanPeriod` or `ReservationRules`, and the Chapter 3 acceptance runner was run. Where the Chapter 2 runner is named, it was run as well.",
  3, "Section 12, re-verification paragraph (environment and earlier-run details)")
rewrite_line(C, "With version 1.0's AC-03 (only a request starting at an existing end)",
  "Suppose AC-03 contained only a request that starts at an existing end. The first change would then pass every Chapter 3 acceptance example. The extra request in AC-03, one that ends exactly where an existing reservation begins, closes that gap.",
  3, "Section 12, sentence after the fault table (reworded)")
rewrite_line(C, "The Scrum Guide, Kanban Guide, Agile Manifesto and principles, Jeffries and Wake pages",
  "Martin (2002) and Rubin (2012) are cited with the publication details given in the module descriptor and were not independently looked up.",
  3, "Section 12, paragraph on source checks (the Martin and Rubin sentence was kept)")
rewrite_line(C, "Blueprint v0.3 continuity:",
  "The practical activity runs on the Team project, with the lending backlog as the worked model and a transfer note for other provided domains. The process note asks teams to separate Scrum as defined from classroom adaptations and optional practices. When marking the process note, accept any honest statement. A team that uses stories, points and a board but no designated Scrum Master has described a legitimate adaptation, whereas a team that calls an academic deadline a Sprint without naming that adaptation has not.",
  3, "Section 12, paragraph 'Blueprint v0.3 continuity' (checklist part removed)")
log(3, [
 "Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).",
 "Companion section 12 retitled `Instructor guidance` (was `Instructor guidance and verification record`).",
 "Verification details moved to evidence: the re-verification paragraph (extraction, `javac --release 17` on JDK 24.0.2, the earlier OpenJDK 17.0.20 run), and the paragraph about web sources (opened on 12 and 13 October 2026; four Scrum.org pages returned HTTP 403 in version 1.0 and were replaced; Martin and Rubin).",
 "Kept as teaching content: the fault table, now introduced by a new subsection `12.1 Do the acceptance examples detect faults?` with one plain sentence, and the point that AC-03's extra request closes a gap (reworded to remove `version 1.0`).",
 "Kept: the sentence that Martin (2002) and Rubin (2012) are cited with details from the module descriptor and were not independently looked up. This belongs to the `not opened` question you have not decided yet. It was left in place.",
 "Rewrote the paragraph `Blueprint v0.3 continuity` (a checklist of what the chapter contains) to keep the guidance on marking the process note and the transfer note; removed the Blueprint reference and the checklist.",
 "Reworded `were checked for consistency with the student chapter` to `are consistent with the student chapter` (R3).",
 "Manuscript: no change. Source note `Sources were checked on 12 and 13 October 2026` is an access date and stays.",
])
print("chapter 3 done")
