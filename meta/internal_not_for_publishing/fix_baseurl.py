import pathlib
import re
import shutil

FRONT = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile/FrontEndBook")
BACKUP = FRONT / "meta/internal_not_for_publishing/backup_before_baseurl"
assert not BACKUP.exists(), "already applied"
BACKUP.mkdir(parents=True)

TARGETS = ["hugo.yaml", "content/book/_index.md", "content/slides/_index.md", "content/topics/_index.md",
           ".github/workflows/deploy.yml"]
for rel in TARGETS:
    dest = BACKUP / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FRONT / rel, dest)

log = []


def replace(rel, old, new, count=1):
    path = FRONT / rel
    raw = path.read_bytes().decode("utf8")
    crlf = "\r\n" in raw
    o = old.replace("\n", "\r\n") if crlf else old
    n = new.replace("\n", "\r\n") if crlf else new
    assert raw.count(o) == count, (rel, old[:60], raw.count(o), count)
    path.write_bytes(raw.replace(o, n).encode("utf8"))
    log.append((rel, count, old.strip().split("\n")[0][:70], new.strip().split("\n")[0][:70]))


# 1. the published address
replace("hugo.yaml", "baseURL: https://polla.dev/oop-and-agile/", "baseURL: https://polla.dev/ood_agile-book/")

# 2. the deploy workflow: one place defines the address
replace(".github/workflows/deploy.yml", """      - name: Build with Hugo
        run: |
          base_url="${{ steps.pages.base_url }}"
          if [ -z "$base_url" ]; then
            base_url="https://polla.dev/frontend-book"
          fi
          hugo \\
            --minify \\
            --baseURL "${base_url}/"
""", """      - name: Build with Hugo
        # The address of the site is the baseURL in hugo.yaml (https://polla.dev/ood_agile-book/).
        run: hugo --minify
""")

# 3. hand-written links that carried, or lacked, the folder: make them independent of it
for week in range(1, 11):
    replace("content/slides/_index.md", "](/oop-and-agile/slides/week-%02d/)" % week,
            "]({{< relref \"/slides/week-%02d\" >}})" % week)
replace("content/book/_index.md", "](/companion/)", "]({{< relref \"/companion\" >}})")
topics = (FRONT / "content/topics/_index.md").read_bytes().decode("utf8")
nb, nc = topics.count("](/book/)"), topics.count("](/companion/)")
replace("content/topics/_index.md", "](/book/)", ']({{< relref "/book" >}})', count=nb)
replace("content/topics/_index.md", "](/companion/)", ']({{< relref "/companion" >}})', count=nc)

# 4. the local server: no folder
cfg = FRONT / "config/development"
cfg.mkdir(parents=True)
(cfg / "hugo.yaml").write_text(
    "# Used by `hugo server` (the development environment). The published address is in the baseURL of\n"
    "# the root hugo.yaml. Locally the site is served at the root, so the pages are at\n"
    "# http://localhost:1313/book/chapter-04/ and not under the folder of the published address.\n"
    "baseURL: http://localhost:1313/\n", encoding="utf8", newline="\n")
log.append(("config/development/hugo.yaml", 1, "(new file)", "baseURL: http://localhost:1313/"))

for row in log:
    print(row)
print(len(log), "changes; backups in", BACKUP.name)
