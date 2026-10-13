import difflib
import glob
import pathlib
import re

FRONT = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile/FrontEndBook")
CONTENT = FRONT / "content"
BACKUP = FRONT / "meta/internal_not_for_publishing/backup_before_pointer_fixes"

# 1. only the intended lines changed
total_changed = 0
for kind in ("book", "companion"):
    for f in sorted((CONTENT / kind).glob("chapter-*.md")):
        new = f.read_text(encoding="utf8").split("\n")
        old = (BACKUP / kind / f.name).read_text(encoding="utf8").split("\n")
        assert len(new) == len(old), (f.name, "line count changed")
        changed = [i for i, (a, b) in enumerate(zip(old, new), 1) if a != b]
        total_changed += len(changed)
        if changed:
            print(f"  {kind}/{f.name}: {len(changed)} line(s) changed: {changed}")
        # front matter and fences intact
        text = "\n".join(new)
        assert text.startswith("---\n") and text.count("\n---\n") >= 1, f.name
        fences = [l for l in new if l.startswith("```")]
        assert len(fences) % 2 == 0, f.name
print("lines changed in total:", total_changed)

# 2. no old names, no stale phrases anywhere in the published content
pages = sorted(glob.glob(str(CONTENT / "book/*.md")) + glob.glob(str(CONTENT / "companion/*.md")))
old_names = stale = 0
for p in pages:
    t = pathlib.Path(p).read_text(encoding="utf8")
    old_names += len(re.findall(r"(?:Chapter|Appendix)_[0-9A-F]{1,2}_[A-Za-z_]+\.md", t))
    stale += len(re.findall(r"will later collect|not yet written|not written yet|is not yet written|Appendix [A-F] (?:is|are) planned|Appendix [A-F] will (?:supply|give|add|provide|describe)", t))
print("old file names left:", old_names, "| stale phrases left:", stale)

# 3. every new pointer resolves
book = {a: (CONTENT / f"book/appendix-{a.lower()}.md").read_text(encoding="utf8") for a in "ABCDEF"}
need = {"C": ["C.2", "C.3", "C.4", "C.5", "C.6", "C.7", "C.8", "C.9", "C.10", "C.11", "C.12", "C.13"], "E": ["E.4", "E.5", "E.6"]}
for letter, ids in need.items():
    for sid in ids:
        assert re.search(rf"^## {re.escape(sid)} ", book[letter], re.M), sid
print("every appendix section named in the new pointers exists:", sum(len(v) for v in need.values()), "checked")
ch4 = (CONTENT / "book/chapter-04.md").read_text(encoding="utf8")
assert re.search(r"^## 4\.4 ", ch4, re.M)
ch9 = (CONTENT / "book/chapter-09.md").read_text(encoding="utf8")
assert "(#appendix-e-reading-checkpoint)" in ch9 and re.search(r"^## Appendix E reading checkpoint", ch9, re.M)
print("Chapter 9 anchor link still resolves to its heading")

# 4. what each companion now says it accompanies
for n in (4, 6, 7, 8, 9, 10, 11, 13, 14, 15):
    t = (CONTENT / f"companion/chapter-{n:02d}.md").read_text(encoding="utf8")
    m = re.search(r"This file accompanies (Chapter \d+, [^.]+)\.", t)
    print(f"  companion {n:>2}: {m.group(1)}")
