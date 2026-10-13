from cleanup_lib import *
C = "Chapter_14_Code_Explanations_and_Solutions.md"
M = "Chapter_14_Responding_to_Change_and_Handing_Over.md"

# ---- header and section 1
replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4\n", "*OO Development and Agile Practices*\n", 14, "header version line", evidence=True)
cut_prefix(C, 14, "Section 1, Version note (rebuilt on the corrected Chapter 13; review changes)", "**Version note.** Version 1.1 rebuilds this chapter", "**No production code changed.**")
rewrite_line(C, "**No production code changed.**",
  "**No production code changed.** Every file under `src/main` is byte for byte as in the Chapter 13 checkpoint. What changed is tests, scripts, documents and the version.",
  14, "Section 1, 'No production code changed' (pointer to the verification record removed)")
rewrite_line(C, "**Input checkpoint.** The starting point is the Chapter 13 checkpoint, which is",
  "**Input checkpoint.** The starting point is the Chapter 13 checkpoint, which is the Chapter 10 companion, the new and changed files of the Chapter 11 companion and the new and changed files of the Chapter 13 companion. To keep verified listings from being copied again, this file lists **only the files that are new or changed**. Every other file is exactly as in those companions.",
  14, "Section 1, input checkpoint (versions and 232 invocations removed)")
cut(C, 14, "Section 1.0, Checkpoint manifest (SHA-256 of the prerequisite companions)", "### 1.0 Checkpoint manifest", "### 1.1 Reconstruct the checkpoint")
replace_once(C, "(the checks recorded here used JDK 24.0.2), ", "", 14, "HANDOVER.md listing, JDK 24.0.2", evidence=True)
replace_once(C, "Date: 13 October 2026 (Asia/Baghdad). Built from version 0.13.1", "Date: 13 October 2026. Built from version 0.13.1", 14, "RELEASE-NOTES listing, time zone", evidence=True)
replace_once(C, "Date: 13 October 2026 (Asia/Baghdad)\nStatus: Decided for the book project", "Date: 13 October 2026\nStatus: Decided for the book project", 14, "ADR-014 listing, time zone", evidence=True)

# ---- section 5
replace_once(C, "Each was run in its own scratch copy under the exact configuration (Section 10.2).", "Each was run in its own scratch copy.", 14, "Section 5.2, reference to the exact configuration", evidence=True)
rewrite_line(C, "What E1 and E2 show is how far the fail-fast check reaches.",
  "What E1 and E2 show is how far the fail-fast check reaches. Everything that is constructed through the composition root fails together when the policy is missing there, which is one fix; the tests that spell out their own map fail separately, which is four fixes. What E3 shows is that this suite has a gap, and that a smaller change can pass a whole stage and fail the next one. Notice what it does **not** show: that unit tests cannot see such a change. No unit test checks the adapter's mapping of the visitor code, so nothing in the unit stage goes through it. A focused adapter test would catch the change, and Section 6.2 (B8) says what it should check. The experiment found the hole by trying a change that goes through it, and Chapter 13's own tests do not close it: the exercise B8 asks the reader to.",
  14, "Section 5.2, E3 explanation (history of the first version removed)")
cut(C, 14, "Section 5.2, paragraph with the Version 1.0 figures for E3 and B1",
    "The figures of the earlier Version 1.0 for E3 and B1 were 4 of 230 (all 202 unit tests passing) and 71 of 233.",
    "### 5.3 Revised assumptions: notes for the table in Section 14.1")
rewrite_line(C, "- *The directory is a synthetic in-process provider with no transport (Chapter 8).*",
  "- *The directory is a synthetic in-process provider with no transport (Chapter 8).* Chapter 8 already defined the provider's `Failure`, translated it to a `DirectoryException` and told an outage from an absence. Chapter 13 added the real HTTP client and the cases a transport brings, including a timeout that covers the whole answer, the body included. The contract held and the behaviour behind it grew.",
  14, "Section 5.3, directory bullet (review finding and the earlier wording removed)")
replace_once(C, "The handover was followed in a fresh folder on the verification machine, as a reader would, before the fixes were made:", "The handover was followed in a fresh folder, as a reader would, before the fixes were made:", 14, "Section 5.5 intro", evidence=True)
replace_once(C, "printed a dynamic-agent warning, on JDK 24.0.2. The build", "printed a dynamic-agent warning, on a recent JDK. The build", 14, "Section 5.5 item 2 (JDK 24.0.2)", evidence=True)
replace_once(C, "the full build of that tree ran 233 invocations with no failures; and", "the full build of that tree passed; and", 14, "Section 5.6, 233 invocations", evidence=True)

# ---- section 10
replace_once(C, "## 10. Instructor notes and verification", "## 10. Instructor notes")
cut_prefix(C, 14, "Section 10.1, 'Alignment with the other chapters' paragraph", "**Alignment with the other chapters.**", "### 10.2 Verification record")
cut(C, 14, "Section 10.2, Verification record (environment, reconstruction, results table; note: the pipeline row carried stale counts)", "### 10.2 Verification record", "### 10.3 Do the checks detect faults?")
replace_once(C, "### 10.3 Do the checks detect faults?", "### 10.2 Do the checks detect faults?")
replace_all(C, "Section 10.3", "Section 10.2", 2)
rewrite_line(C, "The results establish the selected behaviours on the supplied inputs, in the stated environment.",
  "The results establish the selected behaviours on the supplied inputs. They do not establish that the handover is followable by a reader on another machine.",
  14, "Section 10.2 closing limits sentence (stated environment, Java 17, hosted CI, independent review removed)")

# ---- manuscript reference to the renumbered section
replace_once(M, "(Companion, Section 10.3)", "(Companion, Section 10.2)")

log_add([
 "Companion: removed the `Version 1.1 • 13 October 2026 (Asia/Baghdad) • written against Blueprint v0.4` line and the `Version note` (rebuild on the corrected Chapter 13; the four review changes) (R1, R2, R4, R7). The sentence `(Section 10.2 records the check)` was removed from `No production code changed`. The input checkpoint paragraph no longer names `Version 1.1` or `232 JUnit invocations`.",
 "Section 1.0 `Checkpoint manifest` (Blueprint version, SHA-256 of the Chapter 10, 11 and 13 companions) moved to evidence (R6).",
 "Project documents in the listings: the HANDOVER.md text `(the checks recorded here used JDK 24.0.2)` removed; the time zone removed from the dates of RELEASE-NOTES and ADR-014. The counts that `HANDOVER.md` promises (235, 206, 26, 3) are kept: the handover check reads them. **Note:** the working project folder still has the old wording in these documents. It is not published.",
 "Section 5.2: removed `under the exact configuration (Section 10.2)`, the sentence that the first version of this chapter described E3 as a limit of unit testing (`Version 1.1 corrects that`), and the paragraph with the Version 1.0 figures for E3 and B1. The experiment table keeps its figures (they are the companion's evidence tables, each labelled with its checkpoint). Section 5.3: the directory bullet no longer says `a review found that its first timeout did not cover a stalled body` or `The first version of this note said...`. Section 5.5 and 5.6: `on the verification machine`, `on JDK 24.0.2` and `233 invocations` removed.",
 "Section 10 retitled `Instructor notes`. Removed from 10.1 the paragraph `Alignment with the other chapters` (the scripts of Chapter 13 versus 14, and the Chapter 12 mismatch). Section 10.2 `Verification record` moved to evidence (Windows 11, Maven 3.9.11, JDK 24.0.2, the reconstruction paragraph, the results table, Mermaid and sources). **That table's pipeline row still said `205, 25 and 3` after the rebuild (it should have said `206, 26 and 3`), so the evidence file records a stale figure, flagged here.** The fault experiment is now `10.2 Do the checks detect faults?`; two references to `Section 10.3` (companion) and one in the manuscript now say `Section 10.2`.",
 "Kept: both fault experiments (the six faults against `TraceabilityTest`, the three against the handover check) and their limits. The closing sentence no longer mentions the stated environment, Java 17, hosted CI or independent review (the chapter's own limits statements, section 14.6, remain).",
])
print("chapter 14 companion done")
