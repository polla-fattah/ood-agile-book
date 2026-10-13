from cleanup_lib import *
C = "Chapter_08_Code_Explanations_and_Solutions.md"

replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 • reviewed against Blueprint v0.3\n", "*OO Development and Agile Practices*\n", 8, "header version line", evidence=True)

rewrite_line(C, "Version 1.0 only predicted which tests would reject these candidates.",
  "The three candidates were applied, one at a time, to a copy of the project and run through `mvn test`. Each was rejected by the tests named above: the unsafe fallback by `unknownCodesAreErrors` and `malformedRowsAreErrors`, the catch-all by `translatesExpectedFailureAndKeepsCause` and `absenceAndOutageDoNotStoreNotifyOrConsumeId`, and the shared builder list by `builtValueIsIndependentOfReusableBuilder`.",
  8, "Section 7, paragraph on the flawed candidates (version 1.0 and 1.1 history removed)")

cut(C, 8, "Section 11.2, Observed local verification (version paragraphs, exact-configuration run and observation table)",
    "### 11.2 Observed local verification",
    "**Do the tests detect faults?** Twenty faults, listed in the table below (8 + 3 + 2 + 4 + 2 + 1), were introduced one at a time into copies of the project, and each copy was run through `mvn test` in the version 1.1 environment described above (JDK 24.0.2 and the cached dependency versions, not the pinned ones). With version 1.0's tests, nineteen were caught and one survived. Version 1.1 closes that gap, so all twenty are now caught. (An earlier edition of this paragraph said nineteen faults and eighteen caught; that was a counting error, since the table has always listed twenty.)",
    replacement="### 11.2 Do the tests detect faults?\n")
rewrite_line(C, "**Do the tests detect faults?** Twenty faults, listed in the table below",
  "Twenty faults, listed in the table below (8 + 3 + 2 + 4 + 2 + 1), were introduced one at a time into copies of the project, and each copy was run through `mvn test`. All twenty are caught.",
  8, "Section 11.2 lead-in (environment, version 1.0 and the earlier counting error removed)")
rewrite_line(C, "| Factory Method | `ExportJob.run` skips its null check",
  "| Factory Method | `ExportJob.run` skips its null check | Caught by `plain.run(null)` in the existing test. Without that call only `HtmlJob.run(null)` would be tested, and `HtmlJob` fails on null anyway through `escape`, so `PlainJob.run(null)` would silently return `TEXT: null` |",
  8, "Fault table row, Factory Method ('Survived in 1.0' wording removed)")
rewrite_line(C, "The Mockito dynamic-agent warning described in Chapter 7 also appears in this project's log on JDK 24.",
  "The Mockito dynamic-agent warning described in Chapter 7 also appears in this project's log on a recent JDK. It does not affect results, and `-DargLine=-XX:+EnableDynamicAgentLoading` removes it.",
  8, "Mockito warning sentence (JDK 24 named)")
cut(C, 8, "Section 11.2, second results table (full verify, preserved sources, reconstruction)",
    "| Check | Observed result |",
    "Do not add the inherited check counts as if every unit were the same kind of test.")
log(8, [
 "Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).",
 "Companion section 11.2 `Observed local verification` is now `Do the tests detect faults?`. Moved to evidence (R3, R8): the version 1.0 and 1.1 paragraphs (OpenJDK 17.0.20; Maven 3.9.16 with cached versions), the exact-configuration run (Maven 3.9.11, JDK 24.0.2, clean repository, 63 tests), the first observation table (compared files, `-Xlint:all`, exercise solutions, Mermaid) and the second table (full verify, inherited suite, new tests, preserved sources, reconstruction, not-performed items).",
 "Kept: the 20-fault experiment table. Removed the environment sentence, `With version 1.0's tests, nineteen were caught and one survived`, and the note about an earlier counting error from its lead-in, and rewrote the Factory Method row (`Survived in 1.0`) as a description of what the test catches and why the null check matters. All twenty are caught by the current tests.",
 "Kept: the note that the 35 inherited invocations include four wrappers, the Mockito agent note (now `on a recent JDK`), the sentence that the check counts must not be added as if equal, and the limits paragraph.",
 "Section 7: the paragraph that said `Version 1.0 only predicted which tests would reject these candidates. In version 1.1 all three were actually applied` now says that the three candidates were applied one at a time and each was rejected by the named tests.",
 "Manuscript: no change. `Checked 12 and 13 October 2026` is an access date and stays.",
])
print("chapter 8 done")
