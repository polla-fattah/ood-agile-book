import pathlib

META = pathlib.Path(r"C:/Users/polla/Drives/PollaFattah/UNi/UKH/Lectures/OOP and Agile/FrontEndBook/meta")

with (META / "internal_not_for_publishing/Cleanup_Change_Log.md").open("a", encoding="utf8", newline="\n") as h:
    h.write("""## Site address: no folder locally, a new folder name when published (13 October 2026, later)

- Request from the owner: the local pages should be at `http://localhost:1313/book/chapter-04/` and not under `/oop-and-agile/`; the published address should be `https://polla.dev/ood_agile-book/` (it was `https://polla.dev/oop-and-agile/`).
- `hugo.yaml`: `baseURL` is now `https://polla.dev/ood_agile-book/`.
- New `config/development/hugo.yaml`: `baseURL: http://localhost:1313/`. `hugo server` uses the development environment, so locally the site is at the root; a plain `hugo` build uses the published address.
- `.github/workflows/deploy.yml`: the build step no longer overrides the address. It read `${{ steps.pages.base_url }}`, which is always empty, so it always built for `https://polla.dev/frontend-book/`; it is now `hugo --minify`, which uses `hugo.yaml`.
- Hand-written links that depended on the folder were made independent of it with Hugo's `relref`: `content/slides/_index.md` (10 links, which carried `/oop-and-agile/`), `content/book/_index.md` (1) and `content/topics/_index.md` (30), which had been written without any prefix and so were broken under any folder.
- Backups of the five edited files: `backup_before_baseurl/`. Script: `fix_baseurl.py`.
- Checked: a production build and a development build (127 pages each) and a link crawl of both; a real `hugo server` on another port. See the report to the owner for the numbers.
- Not changed: the GitHub repository URLs (`github.com/polla-fattah/oop-and-agile`), which name the repository and not the site folder.

""")
with (META / "internal_not_for_publishing/Cleanup_Todo.md").open("a", encoding="utf8", newline="\n") as h:
    h.write("- [x] Site address: local server without a folder; published address https://polla.dev/ood_agile-book/ (13 October 2026). Open: the GitHub Pages repository or custom domain must serve the site at that path\n")
print("recorded")
