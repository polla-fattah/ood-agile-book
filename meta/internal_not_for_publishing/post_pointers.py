import pathlib

META = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile/FrontEndBook/meta")

# ---- review report: a closing section
report = META / "Appendices_Review_and_Chapter_Reference_Contrast.md"
t = report.read_text(encoding="utf8")
assert "## 12. Chapter pointers and file names fixed" not in t
t += """
## 12. Chapter pointers and file names fixed (13 October 2026, later)

The owner asked for the chapter pointers and the old file names to be fixed. 41 edits in 23 pages (13 chapters and 10 companions). Each edit is listed, with its old and new wording, in `internal_not_for_publishing/Pointer_Fixes_Log.md`; the 30 chapter and companion pages as they were are in `internal_not_for_publishing/backup_before_pointer_fixes/`.

| Group | Edits | What changed |
|---|---|---|
| Old file names | 20 | Ten chapters said “the companion `Chapter_NN_Code_Explanations_and_Solutions.md`” and ten companions said “This file accompanies `Chapter_NN_<Title>.md`”. They now say “the companion for this chapter” and “This file accompanies Chapter N, <Title>.”, with the title taken from each chapter's own front matter |
| “Chapter 15 will later collect the recurring AI workflows” | 11 | Chapters 2 to 9, 11, 13 and 14: now “Chapter 15 collects the recurring AI workflows”. Chapter 10 has no such sentence and Chapter 12 belongs to another author and was not touched |
| Appendices described as unwritten or future | 3 | Chapter 9 (the reading checkpoint) and its companion now say that Appendix E develops the review method; Chapter 14 says what Appendix C (C.12, C.5) and Appendix E (E.4 to E.6) contain |
| Missing pointers | 7 | Appendix C from Chapters 3, 4, 14 and 15; Appendix D from Chapter 1; Appendix F from Chapters 13 and 15. Each names the sections that hold the material |

**Checks.** Exactly 41 lines changed, one per edit, and every changed file has the same number of lines as before; front matter and code fences are intact; no old file name and none of the stale phrases remain anywhere in `content/book` or `content/companion`; each appendix section named in a new pointer exists (15 checked); the link from Chapter 9 to its reading checkpoint still resolves. The AI-activity table of Chapter 15, Section 15.1, agrees with the titles of the activities in Chapters 1 to 11, 13 and 14.

**Not changed, on purpose.** Forward references of the ordinary kind, such as “Chapter 4 will turn the selected work into an iteration plan”. A reader meets them before the later chapter, and they are accurate. Chapter 12, which belongs to another author.

**Still open.** Nothing in section 2 of this report. The remaining items are outside the pointers: the lab and the appendices have been run on JDK 24 with `--release 17` only, and no second reader has read the new appendices.
"""
report.write_text(t, encoding="utf8", newline="\n")

# ---- change log and todo
with (META / "internal_not_for_publishing/Cleanup_Change_Log.md").open("a", encoding="utf8", newline="\n") as h:
    h.write("""## Chapter pointers and old file names fixed (13 October 2026, later)

- Instruction from the owner. 41 edits in 23 pages; each listed in `Pointer_Fixes_Log.md`. Backups: `backup_before_pointer_fixes/`.
- 20 old file names removed; 11 sentences `Chapter 15 will later collect ...` made present tense; Chapter 9 (and its companion) and Chapter 14 no longer describe Appendices C and E as unwritten; 7 new pointers (C from Chapters 3, 4, 14, 15; D from Chapter 1; F from Chapters 13, 15).
- Chapter 12 was not touched (other author).
- Check script: `verify_pointers.py`.

""")
with (META / "internal_not_for_publishing/Cleanup_Todo.md").open("a", encoding="utf8", newline="\n") as h:
    h.write("- [x] Chapter pointers and old file names fixed, 13 October 2026 (41 edits, 23 pages; see Pointer_Fixes_Log.md)\n")

# the consistency item in the working to-do list
todo = META / "Remaining_Chapters_Todo.md"
tt = todo.read_text(encoding="utf8")
old = "- **Consistency review item:** Chapters 2-13 say \"Chapter 15 will later collect the recurring AI workflows\". Change to the present tense now that it exists."
if old in tt:
    tt = tt.replace(old, "- **Consistency review item (done 13 October 2026):** Chapters 2-14 said \"Chapter 15 will later collect the recurring AI workflows\"; changed to the present tense in 11 chapters (Chapter 12 belongs to another author).")
    todo.write_text(tt, encoding="utf8", newline="\n")
    print("todo item updated")
print("records updated")
