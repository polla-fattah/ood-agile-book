"""Check a lecture deck against its chapter (internal, not for publishing).

  python slidefacts.py content/slides/chapter-02.md 2

Every `code name` and every number on the slides must occur in the chapter, its companion or an appendix.
Whatever is reported is then judged by hand: it may be a derived figure, but nothing is assumed.
"""
import pathlib
import re
import sys

FRONT = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile/FrontEndBook")


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"'))


def main(path, chapter):
    n = int(chapter)
    text = pathlib.Path(path).read_text(encoding="utf8")
    body = text.split("\n---\n", 2)[2]
    body = re.sub(r"<!--svg:.*?<!--/svg-->", "", body, flags=re.S)
    src = ""
    for kind in ("book", "companion"):
        src += (FRONT / f"content/{kind}/chapter-{n:02d}.md").read_text(encoding="utf8") + "\n"
    pool = src
    for f in sorted((FRONT / "content/book").glob("*.md")) + sorted((FRONT / "content/companion").glob("*.md")):
        pool += f.read_text(encoding="utf8")
    src, pool = norm(src), norm(pool)
    names, seen = [], set()
    for tok in re.findall(r"`([^`\n]{2,90})`", body):
        t = tok.strip().replace("\\|", "|")
        if t in seen:
            continue
        seen.add(t)
        if norm(t) not in src:
            names.append(("elsewhere in the book" if norm(t) in pool else "NOT FOUND", t))
    plain = re.sub(r"```.*?```", "", body, flags=re.S)
    nums = sorted(set(re.findall(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+\.\d+|\d{2,})(?![\w.])", plain)))
    nums_missing = [x for x in nums if x not in src]
    print(f"{path} against chapter {n}: {len(seen)} code names, {len(nums)} numbers checked")
    for where, t in names:
        print(f"  {where:22} `{t}`")
    print("  numbers not in the chapter or its companion:", nums_missing)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf8")
    main(sys.argv[1], sys.argv[2])
