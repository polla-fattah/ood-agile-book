from cleanup_lib import *
C = "Chapter_10_Code_Explanations_and_Solutions.md"
M = "Chapter_10_From_Classes_to_Application_Structure.md"

replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 (Asia/Baghdad) • reviewed against Blueprint v0.4\n", "*OO Development and Agile Practices*\n", 10, "header version line", evidence=True)
replace_once(C, "The starting implementation is the Chapter 9 companion, Version 1.1 (reviewed 13 October 2026).", "The starting implementation is the Chapter 9 companion.", 10, "Section 1, reference to Chapter 9 companion version and review date", evidence=True)
rewrite_line(C, "**What changed in this version.** Version 1.0 of this file carried older copies of nine files", "", 10, "Section 1, 'What changed in this version' paragraph")
replace_once(C, "\n\n\nThe change introduces named application packages", "\n\nThe change introduces named application packages")
replace_once(C, "Date: 13 October 2026 (Asia/Baghdad)\nStatus: Implemented teaching example; peer review pending.", "Date: 13 October 2026\nStatus: Implemented teaching example; peer review pending.", 10, "ADR-010 date line (time zone removed)", evidence=True)
replace_once(C, "(28 checks, not 26)", "(28 checks)", 10, "Section 2.5 table row for Chapter 6", evidence=True)
rewrite_line(C, "Three of these tests were added in Version 1.1 because the fault experiment in Section 11.2 found gaps.",
  "Three of these tests exist because the fault experiment in Section 11.2 found gaps. `coordinatorRequiresARepository` pins the constructor's null check. `staffRequestAboveTheStudentLimitIsDecidedByThePolicyNotTheConsole` sends a ten-day staff request through the console: a console test that used only a student would let a console that quietly enforced the seven-day rule itself pass. `productionPackagesHaveNoDependencyCycles` closes the gap that the layer matrix leaves inside one layer.",
  10, "Tests section, sentence on three tests added in version 1.1 (reworded)")

cut(C, 10, "Section 11.2, Verification record (version paragraphs, exact-configuration run, results table)",
    "### 11.2 Verification record",
    "**Do the tests detect faults?** Twenty-five faults were introduced one at a time into copies of the project, and each copy was run through `mvn test`. They were first run against the 118-invocation suite that the migration had produced once the nine stale files were restored (version 1.0's tests plus the restored assertions). Twenty were caught and five survived. The survivors were then run against the version 1.1 tests (121 invocations).",
    replacement="### 11.2 Do the tests detect faults?\n")
rewrite_line(C, "**Do the tests detect faults?** Twenty-five faults were introduced",
  "Twenty-five faults were introduced one at a time into copies of the project, and each copy was run through `mvn test`. They were first run before three tests were added: twenty were caught and five survived. The survivors were then run against the final tests.",
  10, "Section 11.2 lead-in (118 and 121 invocations, version 1.0 and the nine stale files removed)")
replace_once(C, "| Area | Faults tried | Result with 118 invocations | Result with version 1.1 |", "| Area | Faults tried | Result before the three added tests | Result with the final tests |", 10, "Fault table header", evidence=True)
rewrite_line(C, "Of the 25 faults, 20 were caught by the 118-invocation suite",
  "Of the 25 faults, 20 were caught before the three tests were added, and 23 are caught by the final tests. The two that still survive are an equivalent mutant and a known limit of any bytecode-based dependency check. Different chapters used different fault sets, so these counts say nothing about how this suite compares with earlier ones. The seven-day-rule survivor and the cycle survivor are the most instructive: both tests were green, and both gaps were visible only when a plausible wrong implementation was tried.",
  10, "Section 11.2, paragraph after the fault table (118 and 121 invocations removed)")
rewrite_line(C, "The results establish the supplied local scenarios and dependency rules.",
  "The results establish the supplied local scenarios and dependency rules. They do not establish persistence, authentication, concurrent consistency or universal behavioural equivalence for unseen consumers.",
  10, "Section 11.2, closing limits sentence (pinned versions and Java 17 removed)")
replace_once(C, "## 11. Instructor notes and verification", "## 11. Instructor notes")

replace_once(M, "; manuscript revised 13 October 2026, Asia/Baghdad.", ".", 10, "Manuscript source note", evidence=True)

log(10, [
 "Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • reviewed against Blueprint v0.4` line, the paragraph `What changed in this version` (nine stale files restored, package-cycle check, and so on), and the mention of `Chapter 9 companion, Version 1.1 (reviewed 13 October 2026)` (R1, R2, R4).",
 "ADR-010 inside the companion: `Date: 13 October 2026 (Asia/Baghdad)` is now `Date: 13 October 2026`. The ADR is a teaching example, so the date line stays.",
 "Section 2.5 (assertions and fixes carried forward) is teaching content and stays. Only `(28 checks, not 26)` became `(28 checks)`. The sentence in the tests section `Three of these tests were added in Version 1.1` now reads `exist because the fault experiment in Section 11.2 found gaps`.",
 "Companion section 11 retitled `Instructor notes`. Subsection 11.2 `Verification record` is now `11.2 Do the tests detect faults?`. Moved to evidence (R3, R8): the version 1.0 and 1.1 paragraphs (OpenJDK 17.0.20 with 118 invocations; the finding about nine stale files; Maven 3.9.16 and the cached versions), the exact-configuration run (Maven 3.9.11, JDK 24.0.2, 121 tests), and the results table (reconstruction, full verify, bridged runners, migrated files, demonstrations, `-Xlint:all`, package metrics, Option B experiment, Mockito warning, not-performed items).",
 "Kept the 25-fault experiment. It compared two suites, `118 invocations` and `version 1.1`. Rewrote it as `before the three added tests` and `with the final tests`, with the same results: 20 caught before, 23 now, two survivors (an equivalent mutant and a documented limit). The lead-in and the paragraph after the table no longer name invocation counts. Check this reading: nothing about the faults or results changed, only the labels.",
 "The closing limits sentence no longer mentions the pinned dependency versions or Java 17 (those were statements about the author's run).",
 "Manuscript: the source note `manuscript revised 13 October 2026, Asia/Baghdad` removed; the access dates stay.",
])
print("chapter 10 done")
