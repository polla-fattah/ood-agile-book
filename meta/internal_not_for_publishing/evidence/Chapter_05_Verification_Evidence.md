# Chapter 5: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_05_Code_Explanations_and_Solutions.md`: Header: version line and Version note (PMD lab added in version 1.2)

Version 1.2 • 13 October 2026 • reviewed against Blueprint v0.4

**Version note.** Version 1.2 adds the Week 4 static-analysis lab: PMD 7.28.0 with a small design rule set (listings 2.8 and 2.9), the model comparison in Section 7.1b, and the PMD checks in the verification record. No Java listing changed.

---

## From `Chapter_05_Code_Explanations_and_Solutions.md`: Section 1, sentence about the author environment and Section 12 (reworded)

The scripts change to their own checkpoint root, compile application and check sources, then run the relevant checks. Ordinary learner setup uses `javac`. The author environment needed the compiler override documented in Section 12; no override is needed with a normal JDK installation.

---

## From `Chapter_05_Code_Explanations_and_Solutions.md`: Section 12.1, Observed author checks (version paragraphs and results table)

### 12.1 Observed author checks

**Version 1.0 (12 October 2026)** was run on Linux with OpenJDK 17.0.20, using a `CHAPTER_JAVAC` wrapper around `java com.sun.tools.javac.Main` because that environment had no `javac` launcher. That run was not repeated. Learners should use an ordinary Java 17 JDK and the documented `javac` commands.

**Version 1.1 (13 October 2026)** was re-verified on Windows 11 in Git Bash with JDK 24.0.2 and the ordinary `javac` launcher, compiling with `--release 17`. All 21 listings were extracted programmatically from this file and assembled into the three checkpoints exactly as Section 1.1 instructs, so the files that ran are the files printed here.

| Checkpoint or check | Observed result |
|---|---|
| Before: compilation, original regression and acceptance runners | Exit 0; 34 checks and five groups passed |
| Stage A: same original checks, unchanged expectations | Exit 0; 34 checks and five groups passed |
| Stage B: original checks plus Chapter 5 runner | Exit 0; original checks and all 44 new checks passed |
| Chapter 4 demonstration on the Stage B code | Original four-line output unchanged |
| New staff/student demonstration | Expected four decisions and two stored reservations |
| Separate LSP program | Base client passed; invalid subtype rejected -2; narrower separate type passed |
| `javac -Xlint:all` on each checkpoint | No warnings on `before`, `refactored` or `after` |
| Shared files against the Chapter 4 listings | Identical, except that version 1.0 of this file still carried Chapter 3's earlier, narrower AC-03 and omitted `.gitattributes`; both are corrected in version 1.1 |
| Mermaid diagram in the student chapter | Rendered without error with Mermaid 10.9.1 |
| PMD 7.28.0 with the lab rule set, on each checkpoint | Two findings each (`DataClass` on `Reservation` and `CyclomaticComplexity` 12 on `reserve`); see Section 7.1b |
| PMD quickstart, code-style and best-practices sets on `before` | 5, 34 and 4 findings respectively; none used by the lab |
| Extraction experiment in a scratch copy of `after` | Gate passed (five groups, 44 checks); PMD reported only the data-class finding |
| PMD download | `pmd-dist-7.28.0-bin.zip` (132,947,834 bytes) from the GitHub release page; its SHA-256 matched the digest that GitHub shows for the file (`f974ba57…bac2`). Maven Central did not host that file (HTTP 404 on the expected path), so only one source for the digest was available. The PGP signature (`.asc`) was not checked |
| PMD environment | Run on Windows 11 under JDK 24.0.2, analysing Java 17 sources; PMD's documentation requires Java 8 or above. Not run under JDK 17 |
| Hosted workflow | Not executed by the author in this chapter |
| Independent peer review | Not claimed; learners must record actual review |

---

## From `Chapter_05_Code_Explanations_and_Solutions.md`: Section 12.1, lead-in (bold question moved into the heading)

**Do the new checks detect faults?** Fourteen deliberate faults were introduced one at a time into a copy of the `after` checkpoint, and the full gate was run on each.

---

