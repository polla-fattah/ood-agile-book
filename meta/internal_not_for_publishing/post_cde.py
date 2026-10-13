import pathlib

META = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile/FrontEndBook/meta")

# ---- 1. the review report: a note at the top and section 10 at the end
report = META / "Appendices_Review_and_Chapter_Reference_Contrast.md"
t = report.read_text(encoding="utf8")
assert "## 10. After the corrections" not in t
note = (
    "> **Update, 13 October 2026 (later).** Appendix C was corrected, and Appendices D and E were regenerated, "
    "at the owner's request. See section 10 for what happened to each finding. The findings below describe the "
    "versions as received; those versions are kept in `internal_not_for_publishing/other_appendices_as_received/`. "
    "Appendix F was not touched and its findings still stand.\n\n"
)
marker = "## 1. Summary"
assert t.count(marker) == 1
t = t.replace(marker, note + marker)
t += """
## 10. After the corrections (13 October 2026, later)

The owner asked for Appendix C to be corrected and Appendices D and E to be regenerated from the chapters and the descriptor. The received versions are backed up (`internal_not_for_publishing/other_appendices_as_received/`, four files including F). The new versions are in `content/book/`.

### What was done to each finding

| Findings | Resolution |
|---|---|
| C-1 (false AI example) | Replaced. The new AI record explains the overlap rule; its rejected candidate says adjacent periods overlap, which is wrong, and the verification names the hand trace and the Appendix A lab |
| C-2 (AI record headings) | The eight headings are Chapter 15's. The checker accepts the Chapter 15 lab's filled record |
| C-3 (ADR form and reused number) | The headings are those of ADR-010, ADR-013 and ADR-014; the example is a new, small, clearly constructed ADR-002, and the text says the numbers are not the book's. The checker accepts the three real ADRs |
| C-4, C-5 (rules, IDs, classes) | The examples use US-02, AC-02 and the book's rules, strings and class names |
| C-6, C-7, C-8 (planning, PR, retrospective) | They follow Chapter 4's budget method, the review description of Chapters 2 and 4 and Chapter 14's observation, evidence, action, owner table; no cycle-time wording |
| C-9 (known issues) | The known-issues and requirements-to-evidence templates follow Chapter 14's documents; no invented rates or class names |
| C-10 (sources) | Scrum Guide, Nygard, GitHub's template page and Keep a Changelog, all linked and opened |
| C-11, C-12, C-14 | Internal IDs removed; C.14 points to E.4 to E.6; 13 templates cover everything the chapters use |
| D-1 to D-12 | Regenerated from the chapters. Every count in the table is asserted against the chapters' own text; the rules of the domain are those of Chapters 1, 5, 8, 9, 10, 12 and 13; identifiers, packages, tags and test classes are the real ones; the lifecycle is Chapter 9's; Option C was removed and the model-serving mapping is marked as a suggestion; the glossary entries follow the chapters and each cited section contains the term |
| E-1 to E-9 | Regenerated from the descriptor and Chapters 1, 9 and 14. The deadline is Weeks 15 and 16; no reflection word count; no new policy; the approved list is the module leader's, with the descriptor's own examples; contribution evidence is commits, PR reviews and peer evaluation; the handover files are the real ones; the quotation with page numbers was removed |

### What was removed from the received versions

These were removed because they conflicted with the chapters, the descriptor or the blueprint, or could not be checked. They can be added back as optional extras on a correct basis: the root-cause "5 Whys" in the retrospective, the task breakdown in the iteration plan, "decision drivers" in the ADR, the author self-review checklist in the pull request, the two-column dialectical note in E, and the counter-perspective sources (Ousterhout, Sculley) in E. The AI and data guidance of the old E.1 now lives in a table in E.2.

### Checks run on the new versions

- **C.** 26 template and example blocks compared with the verified kit: identical. Fences balanced, no internal IDs, no old file names. The checker passes all 26 files and accepts the book's own ADRs and AI record.
- **D.** Every count, sub-total and command asserted against the chapters (all present). `TraceabilityTest` has 3 tests, matching 232 + 3 = 235. The four diagrams render. 40 glossary entries were checked against the sections they cite; five section pointers were wrong and were corrected. D.7 now cites only sources the chapters cite (the Scrum Guide, and Fowler's Test Double and Technical Debt pages, all opened).
- **E.** Eleven descriptor facts checked; the contribution table equals Chapter 14's; the six reading-record entries equal Chapter 1's; every chapter and appendix section it cites exists; three GitHub pages opened and checked.
- **All three.** Hugo 0.166.0 builds them with no warnings; no cross-reference to an unknown appendix section; no `Ground Rule`, `Blueprint`, `Decision D` or version stamps.

### Still open

- **Appendix F** (not requested): F-1 to F-9 stand. The most serious: `ResilientRiskAssessor` does not enforce its timeout, and the exercise needs files that do not exist.
- **Chapter pointers** (not yet changed): Chapter 9 lines 41, 434, 436 and its companion line 2630 still say Appendix E is not written; Chapter 14 line 325 still uses the future tense for C and E. Chapters 3, 4 and 15 do not point to Appendix C; no chapter points to D or F.
- **Old file names** in about 24 chapter pages.
"""
report.write_text(t, encoding="utf8", newline="\n")

# ---- 2. evidence file
ev = META / "internal_not_for_publishing/evidence/Appendices_C_D_E_Correction_Evidence.md"
ev.write_text("""# Appendices C, D and E: correction and regeneration (NOT FOR PUBLISHING)

13 October 2026, after the owner's instruction "correct appendix C and regenerate D and E". The received versions are in `../other_appendices_as_received/`.

## Appendix C (content/book/appendix-c.md, 842 lines)
Built from the verified kit. 26 blocks identical to the kit; front matter parses; 52 fence lines, balanced; no internal IDs; no old file names. The companion (`content/companion/appendix-c.md`) passed all the checks recorded in `Appendix_C_Companion_Verification_Evidence.md`.

## Appendix D (content/book/appendix-d.md, 352 lines)
- Counts asserted against the chapters' text: 12, 34, 34 plus 5 groups, 44, 28, 35, 63, 107, 121, 159, 232 (203 unit), 235, 206, lab 1.0.0 and 9 tests. All present.
- Sub-totals: Ch9 9+21+10+4, Ch10 7+2+3+2, Ch11 28 and 10, Ch13 73 new. All present. `TraceabilityTest` has 3 `@Test` methods.
- Commands, the `V` kind mapping, "one attempt" and "rejections do not consume identifiers" are present in the chapters.
- Glossary: 40 entries with section pointers; every cited section contains the term; five pointers corrected (13.1/13.2, 13.1/13.3, 11.7, 1.4, 6.5/6.6).
- Four Mermaid diagrams rendered (Mermaid 10.9.1). Sources: Scrum Guide, Fowler Test Double (names Meszaros), Fowler Technical Debt (names Cunningham): HTTP 200.

## Appendix E (content/book/appendix-e.md, 212 lines)
- Descriptor (the .docx text) facts present: 1,500 to 2,000 words; Week 8; Moodle, checked for similarity; Weeks 15 to 16; commits, PR reviews and peer evaluation; moderated by individual contribution; repository link, technical report and individual reflection; Week 13 content; Week 14 no classes; the example books; at least three additional sources.
- The contribution table equals Chapter 14's three rows; the six reading-record entries equal Chapter 1's; sections 1.7, 6.7 and 14.3 to 14.6 exist; C.5, C.10, C.11 and C.12 exist.
- GitHub Docs pages (contributions, co-authors, reviews): HTTP 200, key terms present.

## All
Hugo 0.166.0 extended built C, D, E and the companion page: exit 0, no warnings. Cross-reference scan: no reference to a section id that does not exist in appendices A to F. Mermaid: D has 4, C and E have none.

## Not verified
Print and PDF layout; macOS and Linux; no hosted run; the appendices were not read by a second person.
""", encoding="utf8", newline="\n")

# ---- 3. change log and todo
with (META / "internal_not_for_publishing/Cleanup_Change_Log.md").open("a", encoding="utf8", newline="\n") as h:
    h.write("""## Appendices C, D and E corrected and regenerated (13 October 2026, later)

- Instruction from the owner: correct Appendix C, regenerate D and E. Backups of C to F as received: `other_appendices_as_received/`.
- `content/book/appendix-c.md`: rebuilt from the verified template kit (13 templates, 13 examples, chapter-faithful headings). The pointer to E was fixed (E.4 to E.6).
- `content/book/appendix-d.md`: regenerated from the chapters; counts, rules, identifiers, packages, tags, lifecycle and glossary now match them. `content/book/appendix-e.md`: regenerated from the descriptor and Chapters 1, 9 and 14.
- Not changed: Appendix F; the stale pointers in Chapters 9 and 14; the old file names in the chapters.
- Evidence: `evidence/Appendices_C_D_E_Correction_Evidence.md`. Findings and resolutions: `Appendices_Review_and_Chapter_Reference_Contrast.md`, section 10.

""")
with (META / "internal_not_for_publishing/Cleanup_Todo.md").open("a", encoding="utf8", newline="\n") as h:
    h.write("- [x] Appendices C (corrected), D and E (regenerated), 13 October 2026; F untouched; chapter pointers pending\n")
print("records updated")
