import pathlib
import re
import shutil

FRONT = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile/FrontEndBook")
CONTENT = FRONT / "content"
BACKUP = FRONT / "meta/internal_not_for_publishing/backup_before_pointer_fixes"
LOG = FRONT / "meta/internal_not_for_publishing/Pointer_Fixes_Log.md"

assert not BACKUP.exists(), "the backup already exists: the fixes were applied before"
BACKUP.mkdir(parents=True)
for kind in ("book", "companion"):
    (BACKUP / kind).mkdir()
    for f in sorted((CONTENT / kind).glob("chapter-*.md")):
        shutil.copy2(f, BACKUP / kind / f.name)

edits = []   # (kind, file, group, old, new)


def add(kind, name, group, old, new):
    edits.append((kind, name, group, old, new))


# ---- 1. the file names that no longer exist: chapters pointing to their companion
add("book", "chapter-02.md", "old file name", "The companion file, **Chapter_02_Code_Explanations_and_Solutions.md**, contains",
    "The companion file for this chapter contains")
add("book", "chapter-03.md", "old file name", "The companion, **Chapter_03_Code_Explanations_and_Solutions.md**, contains",
    "The companion for this chapter contains")
for n in (4, 5, 11, 13, 14, 15):
    add("book", f"chapter-{n:02d}.md", "old file name", f"The separate `Chapter_{n:02d}_Code_Explanations_and_Solutions.md`",
        "The separate companion for this chapter")
for n in (6, 7):
    add("book", f"chapter-{n:02d}.md", "old file name", f"The companion `Chapter_{n:02d}_Code_Explanations_and_Solutions.md`",
        "The companion for this chapter")

# ---- 2. the file names that no longer exist: companions naming their chapter
OLD = {4: "Chapter_04_From_Requirements_to_an_Iteration.md", 6: "Chapter_06_Interfaces_Dependencies_and_Composition.md",
       7: "Chapter_07_Testing_as_a_Design_Practice.md", 8: "Chapter_08_Creating_and_Connecting_Objects.md",
       9: "Chapter_09_Designing_Changing_Behaviour.md", 10: "Chapter_10_From_Classes_to_Application_Structure.md",
       11: "Chapter_11_Refactoring_and_Legacy_Code.md", 13: "Chapter_13_Integration_Delivery_and_Feedback.md",
       14: "Chapter_14_Responding_to_Change_and_Handing_Over.md", 15: "Chapter_15_AI_as_a_Software_Engineering_Assistant.md"}
for n, old in OLD.items():
    head = (CONTENT / "book" / f"chapter-{n:02d}.md").read_text(encoding="utf8")
    title = re.match(r'---\ntitle: "Chapter (\d+): ([^"]+)"', head)
    assert title and int(title.group(1)) == n, n
    add("companion", f"chapter-{n:02d}.md", "old file name", f"This file accompanies `{old}`.",
        f"This file accompanies Chapter {n}, {title.group(2)}.")

# ---- 3. "Chapter 15 will later collect ..." now that Chapter 15 exists
for n in (2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14):
    add("book", f"chapter-{n:02d}.md", "stale pointer", "Chapter 15 will later collect the recurring AI workflows",
        "Chapter 15 collects the recurring AI workflows")

# ---- 4. appendices described as unwritten or future
add("book", "chapter-09.md", "stale pointer",
    "**Appendix E** is planned to develop the review method in full but is not written yet.",
    "**Appendix E** develops the review method in full: a reading record, questions for each part of the task and prompts for checking your sources.")
add("companion", "chapter-09.md", "stale pointer",
    "The student chapter refers to Appendix E, which is not yet written, and includes a short reading checkpoint that works without it.",
    "The student chapter refers to Appendix E, which develops the review method, and includes a short reading checkpoint that stands on its own.")
add("book", "chapter-14.md", "stale pointer",
    "Appendix C will supply templates for the retrospective and decision notes, and Appendix E will give a fuller guide to final handover and contribution evidence. This chapter stands on its own without them.",
    "Appendix C has templates for the retrospective (C.12) and for decision records (C.5), and Appendix E gives a fuller guide to contribution evidence (E.4), the final handover (E.5) and the reflection (E.6). This chapter stands on its own without them.")

# ---- 5. pointers that were missing
add("book", "chapter-01.md", "new pointer",
    "each later chapter states whether its code joins that project or stays on a separate teaching branch.",
    "each later chapter states whether its code joins that project or stays on a separate teaching branch. Appendix D lists, for every chapter, where the project stands, which count a build should report and the rules of the domain.")
add("book", "chapter-03.md", "new pointer",
    "Passing a story's examples while leaving an unreviewed, unintegrated change does not meet this example DoD.",
    "Passing a story's examples while leaving an unreviewed, unintegrated change does not meet this example DoD. Appendix C has blank forms, each with a worked example, for a story card (C.2), an acceptance example (C.3) and a Definition of Done (C.4).")
add("book", "chapter-04.md", "new pointer",
    "It does not establish that a wireframe was understood, a product decision was approved or a useful outcome was delivered.",
    "It does not establish that a wireframe was understood, a product decision was approved or a useful outcome was delivered. Appendix C has forms for the iteration plan of Section 4.4 (C.6), a team agreement (C.7), a pull-request description (C.8) and the evidence note of this chapter's companion (C.9).")
add("book", "chapter-13.md", "new pointer",
    "Both could be justified later by measured outages, and neither is assumed now.",
    "Both could be justified later by measured outages, and neither is assumed now. Appendix F applies the same questions to a model rather than a directory: a contract the domain owns, an enforced time limit, a cautious fallback where one is safe, and a staged rollout.")
add("book", "chapter-14.md", "new pointer",
    "The project has six, and each is kept true in a different way.",
    "The project has six, and each is kept true in a different way. Appendix C has forms for the requirements table and the known-issues list (C.10), for decision records (C.5) and for release notes (C.11).")
add("book", "chapter-15.md", "new pointer",
    "is a different topic and is treated where it arises.",
    "is a different topic and is treated where it arises and, for a model, in Appendix F.")
add("book", "chapter-15.md", "new pointer",
    "The script cannot tell whether what is written is true, and a reviewer must.",
    "The script cannot tell whether what is written is true, and a reviewer must. Appendix C (C.13) has the blank record and a worked example, and its checker accepts the lab's filled record.")

# ---- apply, each only if it matches exactly once
log = ["# Pointer and file-name fixes (13 October 2026) (NOT FOR PUBLISHING)", "",
       "Every edit made to a chapter or companion page. The originals of all 30 files are in `backup_before_pointer_fixes/`.", "",
       "| # | Group | File | Old wording | New wording |", "|---|---|---|---|---|"]
by_file = {}
for kind, name, group, old, new in edits:
    by_file.setdefault((kind, name), []).append((group, old, new))
count = 0
for (kind, name), items in sorted(by_file.items()):
    path = CONTENT / kind / name
    text = path.read_text(encoding="utf8")
    for group, old, new in items:
        assert text.count(old) == 1, (kind, name, old[:70], text.count(old))
        text = text.replace(old, new)
        count += 1
        cell = lambda s: s.replace("|", "\\|")
        log.append(f"| {count} | {group} | {kind}/{name} | {cell(old)} | {cell(new)} |")
    path.write_text(text, encoding="utf8", newline="\n")
LOG.write_text("\n".join(log) + "\n", encoding="utf8", newline="\n")
print(count, "edits applied in", len(by_file), "files; log:", LOG.name)
