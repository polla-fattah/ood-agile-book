from cleanup_lib import *
C = "Chapter_11_Code_Explanations_and_Solutions.md"
M = "Chapter_11_Refactoring_and_Legacy_Code.md"

replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 (Asia/Baghdad) • reviewed against Blueprint v0.4\n", "*OO Development and Agile Practices*\n", 11, "header version line", evidence=True)
replace_once(C, "model solutions and the verification record.", "model solutions and teaching notes.", 11, "Section 1, first paragraph", evidence=True)
cut(C, 11, "Section 1, Version note (merge with a second draft)",
    "**Version note.** Version 1.1 merges in material from a second draft of this chapter: the original-versus-seam probe, the clock-zone test, the boundary-based AI patch with a second trap, the decision and defect records, and the bridge to the live loans. Everything else is as in Version 1.0.",
    "**Input checkpoint.** The starting point is the Chapter 10 companion, **Version 1.1** (13 October 2026): its 64 listings, 121 JUnit invocations and the assertions carried forward from Chapters 3–9 (its Section 2.5). To keep those older, verified listings from being copied a second time, this file lists **only the files that are new or changed**. Every other file is exactly as in the Chapter 10 companion. The sections below say which is which.")
rewrite_line(C, "**Input checkpoint.** The starting point is the Chapter 10 companion, **Version 1.1**",
  "**Input checkpoint.** The starting point is the Chapter 10 companion: its 64 listings, its tests and the assertions carried forward from Chapters 3–9 (its Section 2.5). To keep those older, verified listings from being copied a second time, this file lists **only the files that are new or changed**. Every other file is exactly as in the Chapter 10 companion. The sections below say which is which.",
  11, "Section 1, input checkpoint (version, date and invocation count removed)")
replace_once(C, "save every listing of the Chapter 10 companion (Version 1.1) at its path.", "save every listing of the Chapter 10 companion at its path.", 11, "Section 1.1, step 1", evidence=True)
replace_once(C, "Date: 13 October 2026 (Asia/Baghdad)", "Date: 13 October 2026", 11, "ADR-011 date line (time zone removed)", evidence=True)

cut(C, 11, "Section 12.2, Verification record (environment, exact-configuration run, results table)",
    "### 12.2 Verification record",
    "**Do the tests detect faults?** The experiment ran in two rounds, always one fault at a time in a copy of the project and always through `mvn test`.",
    replacement="### 12.2 Do the tests detect faults?\n")
rewrite_line(C, "**Do the tests detect faults?** The experiment ran in two rounds",
  "The experiment ran in two rounds, always one fault at a time in a copy of the project and always through `mvn test`.",
  11, "Section 12.2 lead-in (bold question moved into the heading)")
rewrite_line(C, "The results establish the selected behaviours on the supplied inputs, in the stated environment.",
  "The results establish the selected behaviours on the supplied inputs. They do not establish equivalence with the original for every input, or the behaviour of any real record system.",
  11, "Section 12.2, closing limits sentence (stated environment, pinned versions, Java 17 and hosted CI removed)")
replace_once(C, "## 12. Instructor notes and verification", "## 12. Instructor notes")

# manuscript
replace_once(M, "with its 121 JUnit invocations and its package structure.", "and its package structure.", 11, "Manuscript, entry checkpoint (test count removed)", evidence=True)
replace_once(M, "model answers and the verification record.", "model answers and teaching notes.", 11, "Manuscript line 38", evidence=True)
replace_once(M, "were opened on 13 October 2026; the manuscript was written the same day, Asia/Baghdad.", "were opened on 13 October 2026.", 11, "Manuscript source note", evidence=True)

log(11, [
 "Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • reviewed against Blueprint v0.4` line and the `Version note` paragraph that says the file merges in material from a second draft (R1, R2, R4, R7).",
 "Companion section 1: the input checkpoint paragraph no longer says `Version 1.1 (13 October 2026)` or `121 JUnit invocations`; step 1 of the reconstruction no longer says `(Version 1.1)`. First paragraph: `the verification record` is now `teaching notes`. ADR-011: time zone removed from the date line.",
 "Companion section 12 retitled `Instructor notes`. Subsection 12.2 `Verification record` is now `12.2 Do the tests detect faults?`. Moved to evidence (R3, R8): the environment paragraph (Maven 3.9.16, JDK 24.0.2, cached versions, no JDK 17), the exact-configuration run (Maven 3.9.11, clean repository, 159 tests), and the results table (reconstruction details, full verify, stages, stage C, probe, demonstrations, package metrics, dependency tests, staff grace experiment, Mockito warning, not-performed items).",
 "Kept: the two-round fault experiment and its tables, including the note that the first round's surviving null-kind case led to a new test. The staff-grace-period result is also taught in section 8. Closing limits sentence no longer names the stated environment, pinned versions, Java 17 or hosted CI.",
 "Manuscript: entry checkpoint no longer says `with its 121 JUnit invocations` (R5); line 38 `the verification record` is now `teaching notes`; the source note no longer says `the manuscript was written the same day, Asia/Baghdad` (the access date stays).",
 "Not changed: the project README listing inside the companion (it states the project's own counts, 159 and 121) and the `Asia/Baghdad` time zone in Java code and tests (teaching examples of local dates).",
])
print("chapter 11 done")
