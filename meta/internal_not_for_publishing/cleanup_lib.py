"""Helpers for the first-draft cleanup. Internal, not for publishing."""
import pathlib

ROOT = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile")
INTERNAL = ROOT / "internal_not_for_publishing"
EVIDENCE = INTERNAL / "evidence"
LOG = INTERNAL / "Cleanup_Change_Log.md"


def read(name):
    return (ROOT / name).read_text(encoding="utf8")


def write(name, text):
    (ROOT / name).write_text(text, encoding="utf8", newline="\n")


def evidence_file(chapter):
    return EVIDENCE / f"Chapter_{chapter:02d}_Verification_Evidence.md"


def start_evidence(chapter, title):
    p = evidence_file(chapter)
    if not p.exists():
        p.write_text(
            f"# Chapter {chapter}: verification and working evidence (NOT FOR PUBLISHING)\n\n"
            f"Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. "
            f"The originals of the chapter files are in `../backup_before_cleanup/`.\n\n",
            encoding="utf8", newline="\n")
    return p


def add_evidence(chapter, source_file, label, text):
    p = start_evidence(chapter, "")
    with p.open("a", encoding="utf8", newline="\n") as handle:
        handle.write(f"## From `{source_file}`: {label}\n\n")
        handle.write(text.rstrip("\n") + "\n\n---\n\n")


def cut(name, chapter, label, start, end, replacement="", keep_evidence=True):
    """Remove the text from the line equal to `start` (inclusive) up to the line equal to `end` (exclusive).
    Both lines must occur exactly once. The removed text is appended to the chapter's evidence file."""
    text = read(name)
    lines = text.split("\n")
    s = [i for i, l in enumerate(lines) if l == start]
    assert len(s) == 1, (name, "start", start[:60], len(s))
    if end is None:
        e = len(lines)
    else:
        e = [i for i, l in enumerate(lines) if l == end and i > s[0]]
        assert e, (name, "end", end[:60])
        e = e[0]
    removed = "\n".join(lines[s[0]:e])
    if keep_evidence:
        add_evidence(chapter, name, label, removed)
    new = lines[:s[0]] + ([replacement] if replacement else []) + lines[e:]
    write(name, "\n".join(new))
    return removed


def replace_once(name, old, new, chapter=None, label=None, evidence=False):
    text = read(name)
    assert text.count(old) == 1, (name, old[:70], text.count(old))
    if evidence:
        add_evidence(chapter, name, label, old)
    write(name, text.replace(old, new))


def replace_all(name, old, new, count):
    text = read(name)
    assert text.count(old) == count, (name, old[:70], text.count(old), count)
    write(name, text.replace(old, new))


def log(chapter, lines):
    with LOG.open("a", encoding="utf8", newline="\n") as handle:
        handle.write(f"## Chapter {chapter}\n\n")
        for line in lines:
            handle.write(f"- {line}\n")
        handle.write("\n")


def line_starting(name, prefix):
    found = [l for l in read(name).split("\n") if l.startswith(prefix)]
    assert len(found) == 1, (name, prefix[:60], len(found))
    return found[0]


def rewrite_line(name, prefix, new, chapter, label):
    """Replace the single line that starts with `prefix` by `new`; the original goes to the evidence file."""
    old = line_starting(name, prefix)
    replace_once(name, old, new, chapter, label, evidence=True)
    return old


def log_add(lines):
    """Append bullet lines to the last chapter entry of the change log."""
    text = LOG.read_text(encoding="utf8").rstrip("\n")
    text += "\n" + "\n".join(f"- {l}" for l in lines) + "\n\n"
    LOG.write_text(text, encoding="utf8", newline="\n")


def cut_prefix(name, chapter, label, start_prefix, end_prefix, replacement=""):
    """Like cut(), but the start and end lines are found by their first characters (each must be unique)."""
    start = line_starting(name, start_prefix)
    end = None if end_prefix is None else line_starting(name, end_prefix)
    return cut(name, chapter, label, start, end, replacement)
