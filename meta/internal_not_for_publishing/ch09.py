from cleanup_lib import *
C = "Chapter_09_Code_Explanations_and_Solutions.md"

replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 • reviewed against Blueprint v0.3\n", "*OO Development and Agile Practices*\n", 9, "header version line", evidence=True)
replace_once(C, "| Java | Release 17; author runtime OpenJDK 17.0.20 |", "| Java | Release 17 |", 9, "Tool table row (author runtime)", evidence=True)

rewrite_line(C, "These are **deliberately incorrect fragments or proposals**",
  "These are **deliberately incorrect fragments or proposals**, not extra source files for the active build. If experimenting, use a disposable copy and restore the correct source before the full gate. The cancel-on-loan alternative (7.2) and the stop-on-first-failure alternative (7.3) were applied and run, and both were rejected by the tests named below. The setter in 7.1 cannot be rejected by a runtime test, as explained there.",
  9, "Section 10, intro to the flawed alternatives (version 1.0 and 1.1 history removed)")

cut(C, 9, "Section 12, version paragraphs and the first observation table",
    "**Version 1.0 (12 October 2026)** was run on OpenJDK 17.0.20 with Maven 3.9.11 and the pinned dependencies in Section 5. That run was not repeated. Verification covers the supplied implementation and examples, not a claimed test-first history or independent review.",
    "**Do the tests detect faults?** Eighteen faults were introduced one at a time into copies of the project, and each copy was run through `mvn test`. With version 1.0's tests, sixteen were caught and two survived. Version 1.1 closes both gaps by strengthening an existing test, so all eighteen are now caught, and the invocation count stays at 107.",
    replacement="### 12.1 Do the tests detect faults?\n")
rewrite_line(C, "**Do the tests detect faults?** Eighteen faults were introduced",
  "Eighteen faults were introduced one at a time into copies of the project, and each copy was run through `mvn test`. All eighteen are caught.",
  9, "Section 12 lead-in (version 1.0 survivors and the invocation count removed)")
rewrite_line(C, "| Command | **Construction validation removed** |",
  "| Command | **Construction validation removed** | Caught by a test that constructs a command with a blank identifier, a null receiver and a null start date. Without such a test the fault would survive, because nothing else exercises construction validation |",
  9, "Fault table row, construction validation ('Survived in 1.0' wording removed)")
rewrite_line(C, "| Command | **Executes with one extra day** |",
  "| Command | **Executes with one extra day** | Caught by asserting the exact confirmation, period included. A check that only tests `startsWith(\"Confirmed: R1 for B1 on CAM1\")` would miss it, because that is true for any duration |",
  9, "Fault table row, one extra day ('Survived in 1.0' wording removed)")
cut(C, 9, "Section 12, second results table (Maven verify, inherited suite, reconstruction)",
    "| Check | Observed result |",
    "Each lifecycle table row exercises both implementations, but it remains one reported parameterised test invocation. Four inherited JUnit cases invoke earlier plain-Java runners whose own counts remain distinct: 34 Chapter 2 checks, five Chapter 3 example groups, 44 Chapter 5 checks and 28 Chapter 6 checks.")
rewrite_line(C, "The Mockito dynamic-agent warning described in Chapter 7 also appears in this project's log on JDK 24.",
  "The Mockito dynamic-agent warning described in Chapter 7 also appears in this project's log on a recent JDK. It does not affect results, and `-DargLine=-XX:+EnableDynamicAgentLoading` removes it.",
  9, "Mockito warning sentence (JDK 24 named)")
replace_once(C, "## 12. Verification record", "## 12. Fault experiment and limits")

log(9, [
 "Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4). Tool table: removed `author runtime OpenJDK 17.0.20` (R8).",
 "Companion section 12 `Verification record` is now `Fault experiment and limits`, with a subsection `12.1 Do the tests detect faults?`. Moved to evidence (R3, R8): the version 1.0 and 1.1 paragraphs (OpenJDK 17.0.20; Maven 3.9.16 and the cached versions), the exact-configuration run (Maven 3.9.11, JDK 24.0.2, 107 tests), the first observation table (compared files, `-Xlint:all`, Mermaid) and the second table (full verify, inherited suite, new tests, reconstruction, not-performed items).",
 "Kept: the 18-fault experiment. Removed the history that sixteen were caught in version 1.0 and two survived, and the sentence that the invocation count stays at 107. The two Command rows that read `Survived in 1.0` now say what catches each fault and what would miss it (a construction-validation test; an exact-confirmation assertion), which keeps the lesson. All eighteen are caught by the current tests.",
 "Kept: the notes on lifecycle table rows and inherited runners, the limits paragraph (concurrency, delivery, authentication, transactions, replay), and the Mockito agent note (now `on a recent JDK`).",
 "Section 10: removed `Version 1.0 only predicted which tests would reject these alternatives. In version 1.1...` and kept that two of the alternatives were applied and rejected.",
 "Manuscript: no change. `Checked 12 and 13 October 2026` is an access date and stays. The sentence that Appendix E is planned but not written is left alone (decision pending for the appendices).",
])
print("chapter 9 done")
