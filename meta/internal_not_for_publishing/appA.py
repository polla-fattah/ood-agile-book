from cleanup_lib import *
import cleanup_lib

M = "Appendix_A_Programming_Readiness_and_Notation.md"
C = "Appendix_A_Code_Explanations_and_Solutions.md"

# the appendix has its own evidence file
EV = EVIDENCE / "Appendix_A_Verification_Evidence.md"
assert not EV.exists()
EV.write_text(
    "# Appendix A: verification and working evidence (NOT FOR PUBLISHING)\n\n"
    "Text removed verbatim from the published appendix files during the first-draft cleanup of 13 October 2026. "
    "The originals are in `../backup_before_cleanup/`.\n\n",
    encoding="utf8", newline="\n")
cleanup_lib.evidence_file = lambda ch: EV

replace_once(M, "*Designing, Testing and Evolving Software with AI Assistance*  \nVersion 1.0 • 13 October 2026\n",
             "*Designing, Testing and Evolving Software with AI Assistance*\n", 0, "manuscript header version line", evidence=True)
replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.0 • 13 October 2026\n",
             "*OO Development and Agile Practices*\n", 0, "companion header version line", evidence=True)
cut(C, 0, "Section 7, Verification record (environment, OpenJDK 17.0.20, results table, limits)",
    "## 7. Verification record", "## References")

entries = [
    "Manuscript and companion: removed the `Version 1.0 • 13 October 2026` line under the title block (R1, R2).",
    "Companion: Section 7 `Verification record` moved to evidence (OpenJDK 17.0.20 run through `java com.sun.tools.javac.Main`, the five-row results table, the remark that Mermaid rendering was not completed because the browser runtime could not be installed, and the closing limits paragraph). `References` now follows Section 6 directly. The fault-experiment limits are still stated in Section 3.",
    "Backups of both files are in `backup_before_cleanup/`; the removed text is in `evidence/Appendix_A_Verification_Evidence.md`.",
    "Not changed (not requested): manuscript line 16 (`a particular Chapter 11 baseline`), the dependency sentence in A.8, References item 2 in the companion, and the `planned to add` wording about Appendix A in Chapters 1 and 2. The `checked 13 October 2026` source access dates are kept.",
    "Re-verification in this session: the four listings were extracted from the companion and compiled with `--release 17 -Xlint:all` (no warnings), printed the six expected lines with 27 checks, and the `count <= 3` fault failed with `AssertionError: fourth reservation rejected`. Run on JDK 24.0.2, not a Java 17 runtime. All 12 source links returned HTTP 200. The two Mermaid diagrams were not rendered.",
]
with LOG.open("a", encoding="utf8", newline="\n") as handle:
    handle.write("## Appendix A\n\n")
    for entry in entries:
        handle.write("- " + entry + "\n")
    handle.write("\n")
with (INTERNAL / "Cleanup_Todo.md").open("a", encoding="utf8", newline="\n") as handle:
    handle.write("- [x] Appendix A — manuscript, companion (done 13 October 2026; see the change log)\n")
print("appendix A cleanup done")
