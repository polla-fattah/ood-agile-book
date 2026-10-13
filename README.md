# Object Oriented Development and Agile Practices

*Designing, Testing and Evolving Software with AI Assistance*  
**SE506, University of Kurdistan Hewlêr (UKH)**  
Author: Dr. Polla Abdulhamid Fattah

This repository is the complete Hugo website and reader for the *Object Oriented Development and Agile Practices* textbook and companion.

```text
FrontEndBook/
├── content/
│   ├── book/         # Chapter and appendix manuscript (/book)
│   ├── companion/    # Code, explanations, and lab solutions (/companion)
│   ├── topics/       # Curriculum blueprint and learning outcomes (/topics)
│   └── slides/       # Lecture decks (/slides)
├── layouts/          # Book shell, presentation layer, and Hugo templates
├── assets/           # SCSS styles, scripts, and runtime assets
├── static/           # Images (front cover, logo), fonts, and static files
├── scripts/          # Ingestion and helper scripts (sync_chapters.py)
├── data/             # Homepage data (home.yaml, footer.yaml)
└── hugo.yaml         # Site configuration
```

## Running Locally

Run development server with live reload:

```powershell
hugo server --source .
```

Build the static site:

```powershell
hugo --source . --cleanDestinationDir
```

## Ingesting Chapters and Companions

When you are ready to copy the manuscript chapters and their companions into the site, run:

```powershell
# Dry run to preview what will be copied:
python scripts/sync_chapters.py --dry-run

# Execute sync:
python scripts/sync_chapters.py
```

This automatically formats and adds the required Hugo front matter (`title`, `weight`, `book_number`, `type: book`) to:
- `content/book/` for chapter manuscripts
- `content/companion/` for code solutions and lab companions
