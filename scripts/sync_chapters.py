#!/usr/bin/env python3
"""
sync_chapters.py

Prepares and copies the textbook chapters and companion files from the parent directory
into the Hugo content directories:
  - Manuscripts -> content/book/
  - Companions  -> content/companion/

Adds appropriate Hugo front-matter (title, weight, type) without modifying original files.
Usage:
    python scripts/sync_chapters.py [--dry-run]
"""

import os
import re
import sys
import argparse
from pathlib import Path

# Chapter number mapping and titles
CHAPTER_NAMES = {
    1: "Developing Software That Can Change",
    2: "Object-Oriented Development Beyond Syntax",
    3: "Agile Development and the Nature of Change",
    4: "From Requirements to an Iteration",
    5: "Responsibilities, Extension, and Substitutability",
    6: "Interfaces, Dependencies, and Composition",
    7: "Testing as a Design Practice",
    8: "Creating and Connecting Objects",
    9: "Designing Changing Behaviour",
    10: "From Classes to Application Structure",
    11: "Refactoring and Legacy Code",
    12: "Measuring Progress, Flow and Technical Health",
    13: "Integration, Delivery and Feedback",
    14: "Responding to Change and Handing Over",
    15: "AI as a Software Engineering Assistant",
}

def extract_title(content, default_title):
    """Extract first H1 or H2 markdown heading as title, or fallback."""
    for line in content.splitlines()[:10]:
        line = line.strip()
        if line.startswith("# ") and not line.startswith("# Chapter"):
            return line[2:].strip()
    return default_title

def prepare_markdown(content, title, weight, book_number):
    """Ensures YAML front matter is present."""
    # Check if front-matter already exists
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # Front matter already exists
            return content
    
    front_matter = (
        f"---\n"
        f"title: \"{title}\"\n"
        f"weight: {weight}\n"
        f"book_number: {book_number}\n"
        f"type: book\n"
        f"book_kind: book\n"
        f"---\n\n"
    )
    return front_matter + content

def sync(dry_run=False):
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    parent_dir = repo_root.parent

    book_dest = repo_root / "content" / "book"
    companion_dest = repo_root / "content" / "companion"

    book_dest.mkdir(parents=True, exist_ok=True)
    companion_dest.mkdir(parents=True, exist_ok=True)

    print(f"Parent directory: {parent_dir}")
    print(f"Book destination: {book_dest}")
    print(f"Companion destination: {companion_dest}")
    print(f"Dry run: {dry_run}\n")

    synced_manuscripts = 0
    synced_companions = 0

    # Scan parent directory for chapters
    for f in sorted(parent_dir.glob("Chapter_*.md")):
        fname = f.name
        match = re.match(r"Chapter_(\d+)_", fname)
        if not match:
            continue
        
        ch_num = int(match.group(1))
        content = f.read_text(encoding="utf-8")

        if "Code_Explanations_and_Solutions" in fname:
            # It's a companion file
            title = f"Chapter {ch_num} Companion: Code & Solutions"
            target = companion_dest / fname
            prepared = prepare_markdown(content, title, weight=ch_num, book_number=ch_num)
            
            print(f"[COMPANION] {fname} -> {target.name} (weight: {ch_num})")
            if not dry_run:
                target.write_text(prepared, encoding="utf-8")
            synced_companions += 1
        else:
            # It's a chapter manuscript
            default_title = CHAPTER_NAMES.get(ch_num, f"Chapter {ch_num}")
            title = extract_title(content, default_title)
            target = book_dest / fname
            prepared = prepare_markdown(content, title, weight=ch_num, book_number=ch_num)
            
            print(f"[BOOK]      {fname} -> {target.name} (title: '{title}', weight: {ch_num})")
            if not dry_run:
                target.write_text(prepared, encoding="utf-8")
            synced_manuscripts += 1

    print(f"\nSummary:")
    print(f"  Manuscripts processed: {synced_manuscripts}")
    print(f"  Companions processed:  {synced_companions}")
    if dry_run:
        print("Dry run completed. No files were written.")
    else:
        print("Sync completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync chapters and companions into Hugo content.")
    parser.add_argument("--dry-run", action="store_true", help="Inspect what would be copied without writing.")
    args = parser.parse_args()
    sync(dry_run=args.dry_run)
