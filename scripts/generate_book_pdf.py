import os
import sys
import asyncio
import re
import pymupdf  # PyMuPDF
from pyppeteer import launch

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
HTML_SOURCE = os.path.join(WORKSPACE_DIR, "public", "_print", "book", "index.html")

SCRATCH_DIR = os.path.join(WORKSPACE_DIR, "scratch")
TITLE_HTML = os.path.join(SCRATCH_DIR, "title_pages.html")
TITLE_PDF = os.path.join(SCRATCH_DIR, "title_pages.pdf")
CONTENT_HTML = os.path.join(SCRATCH_DIR, "content_pages.html")
CONTENT_PDF = os.path.join(SCRATCH_DIR, "content_pages.pdf")

OUTPUT_PDF = os.path.join(WORKSPACE_DIR, "static", "downloads", "Object_Oriented_Development_and_Agile_Practices.pdf")
PUBLIC_PDF = os.path.join(WORKSPACE_DIR, "public", "downloads", "Object_Oriented_Development_and_Agile_Practices.pdf")
FRONT_COVER_IMG = os.path.join(WORKSPACE_DIR, "images", "cover-front.png")
BACK_COVER_IMG = os.path.join(WORKSPACE_DIR, "images", "cover-back.png")
MAIN_CSS = os.path.join(WORKSPACE_DIR, "public", "scss", "main.css")
FA_CSS = os.path.join(WORKSPACE_DIR, "public", "scss", "fontawesome.css")
MERMAID_JS_PATH = os.path.join(WORKSPACE_DIR, "assets", "third_party", "mermaid", "mermaid.min.js")

os.makedirs(SCRATCH_DIR, exist_ok=True)
os.makedirs(os.path.join(WORKSPACE_DIR, "static", "downloads"), exist_ok=True)
os.makedirs(os.path.join(WORKSPACE_DIR, "public", "downloads"), exist_ok=True)


def get_base_css():
    main_css_content = ""
    fa_css_content = ""
    if os.path.exists(MAIN_CSS):
        with open(MAIN_CSS, "r", encoding="utf-8") as f:
            main_css_content = f.read()
    if os.path.exists(FA_CSS):
        with open(FA_CSS, "r", encoding="utf-8") as f:
            fa_css_content = f.read()

    # Strip out any counter(page) in @bottom-center to avoid duplicate page numbers
    main_css_content = re.sub(r'@bottom-center\s*\{[^}]*\}', '', main_css_content)

    custom_css = """
    * {
      box-sizing: border-box;
    }

    html, body {
      background: #ffffff !important;
      background-color: #ffffff !important;
      color: #0f172a !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
      font-size: 10pt !important;
      line-height: 1.65 !important;
      -webkit-font-smoothing: antialiased;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
      margin: 0 !important;
      padding: 0 !important;
    }

    .td-print-view {
      background: #ffffff !important;
    }

    .container-fluid, .td-print-shell, .td-print-document, main {
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      border: none !important;
      box-shadow: none !important;
      background: #ffffff !important;
    }

    /* Table of Contents Styling */
    .td-book-print-cover {
      page-break-before: always;
      page-break-after: always;
      break-after: page;
      padding-top: 10px;
    }
    .td-book-print-cover h1.title {
      font-size: 26pt !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      border-bottom: 2pt solid #0284c7;
      padding-bottom: 12px;
      margin-bottom: 12px;
    }
    .td-book-print-cover .lead {
      font-size: 12pt !important;
      color: #475569 !important;
      margin-bottom: 24px !important;
    }
    .td-book-print-toc ol {
      list-style: none;
      padding-left: 0;
      margin: 0;
    }
    .td-book-print-toc li {
      padding: 6px 0;
      border-bottom: 0.5pt dotted #cbd5e1;
      font-size: 9.5pt;
      break-inside: avoid;
    }
    .td-book-print-toc a {
      color: #0f172a !important;
      text-decoration: none;
      font-weight: 500;
    }
    .td-book-print-toc a:hover {
      color: #0284c7 !important;
    }
    .td-book-print-toc .td-book-number {
      font-weight: 700;
      color: #0f172a;
      display: inline-block;
      width: 28px;
    }

    /* Chapter and Section Headings */
    .td-book-print-page {
      page-break-before: always !important;
      break-before: page !important;
      padding-top: 16px !important;
    }
    .td-book-print-page h1 {
      font-size: 22pt !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      border-bottom: 1.5pt solid #0284c7 !important;
      padding-bottom: 10px !important;
      margin-top: 10px !important;
      margin-bottom: 14px !important;
      line-height: 1.25 !important;
    }
    .td-book-print-page .lead {
      font-size: 10.5pt !important;
      font-style: italic !important;
      color: #334155 !important;
      margin-bottom: 18px !important;
      background: #f8fafc;
      padding: 10px 14px;
      border-inline-start: 3pt solid #0284c7;
      border-radius: 4px;
    }
    h2 {
      font-size: 14pt !important;
      font-weight: 700 !important;
      color: #1e293b !important;
      margin-top: 22px !important;
      margin-bottom: 10px !important;
      border-bottom: 0.5pt solid #e2e8f0 !important;
      padding-bottom: 4px !important;
      break-after: avoid-page !important;
    }
    h3 {
      font-size: 11.5pt !important;
      font-weight: 600 !important;
      color: #334155 !important;
      margin-top: 16px !important;
      margin-bottom: 8px !important;
      break-after: avoid-page !important;
    }
    p {
      margin-bottom: 10px !important;
      text-align: justify;
      hyphens: auto;
    }

    /* Code Blocks */
    pre, .chroma, .highlight {
      background: #f8fafc !important;
      border: 0.75pt solid #cbd5e1 !important;
      border-radius: 4px !important;
      padding: 8px 12px !important;
      font-family: "Cascadia Code", Consolas, "Courier New", monospace !important;
      font-size: 8pt !important;
      line-height: 1.45 !important;
      white-space: pre-wrap !important;
      word-break: break-word !important;
      break-inside: avoid-page !important;
      margin-bottom: 12px !important;
    }
    code {
      font-family: "Cascadia Code", Consolas, "Courier New", monospace !important;
      font-size: 8.5pt !important;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
      color: #0f172a !important;
    }

    /* Callout & Notes */
    blockquote, .td-callout {
      background: #f0f9ff !important;
      border-inline-start: 3.5pt solid #0284c7 !important;
      padding: 10px 14px !important;
      margin: 14px 0 !important;
      border-radius: 0 4px 4px 0;
      break-inside: avoid-page !important;
      font-size: 9.5pt !important;
    }

    /* Tables */
    table, .td-table {
      width: 100% !important;
      border-collapse: collapse !important;
      margin: 14px 0 !important;
      font-size: 8.5pt !important;
      break-inside: avoid-page !important;
    }
    th {
      background: #f1f5f9 !important;
      color: #0f172a !important;
      font-weight: 700 !important;
      border: 0.5pt solid #cbd5e1 !important;
      padding: 6px 10px !important;
      text-align: left !important;
    }
    td {
      border: 0.5pt solid #cbd5e1 !important;
      padding: 6px 10px !important;
    }
    tr:nth-child(even) td {
      background: #f8fafc !important;
    }

    /* Figures & Images */
    figure, img {
      max-width: 100% !important;
      height: auto !important;
      break-inside: avoid-page !important;
    }
    figcaption {
      font-size: 8.5pt !important;
      color: #64748b !important;
      text-align: center;
      margin-top: 6px;
      font-style: italic;
    }

    /* Hide Navigation / Web UI Artifacts */
    .td-skip-link, .td-heading-self-link, .td-page-actions, .td-code__copy, .d-print-none, .td-book-cover-page {
      display: none !important;
    }
    """
    return f"""
    <style>
      {main_css_content}
      {fa_css_content}
      {custom_css}
    </style>
    """


def prepare_documents():
    print("Preparing Title & Colophon Document...")
    base_css = get_base_css()

    title_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Title & Colophon</title>
  {base_css}
  <style>
    @page {{
      size: A4;
      margin: 20mm 20mm 20mm 20mm;
    }}
    .formal-title-page {{
      page-break-after: always;
      break-after: page;
      min-height: 800px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      text-align: center;
      padding: 40px 10px;
    }}
    .formal-title-page h1 {{
      font-size: 32pt !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      margin-bottom: 12px !important;
      line-height: 1.2 !important;
    }}
    .colophon-page {{
      page-break-before: always;
      break-before: page;
      padding: 80px 20px 40px;
      font-size: 9pt;
      color: #475569;
      line-height: 1.7;
    }}
  </style>
</head>
<body style="background: #ffffff !important;">
  <div class="formal-title-page">
    <div>
      <div style="font-size: 11pt; text-transform: uppercase; letter-spacing: 0.15em; color: #64748b; margin-bottom: 30px; font-weight: 600;">Textbook and Engineering Monograph</div>
      <h1>Object Oriented Development and Agile Practices</h1>
      <div style="font-size: 15pt; color: #475569; font-style: italic; margin-bottom: 40px;">Designing, Testing and Evolving Software with AI Assistance</div>
    </div>

    <div style="height: 40px;"></div>

    <div style="margin-top: auto; border-top: 1.5pt solid #cbd5e1; padding-top: 24px;">
      <div style="font-size: 16pt; font-weight: 700; color: #0f172a;">Dr. Polla Abdulhamid Fattah</div>
      <div style="font-size: 11pt; color: #64748b; margin-top: 4px;">with AI Collaboration and Practical Case Studies</div>
      <div style="font-size: 8.5pt; color: #94a3b8; margin-top: 24px; text-transform: uppercase; letter-spacing: 0.1em;">
        First Edition - Academic and Production Reference - 2026
      </div>
    </div>
  </div>

  <div class="colophon-page">
    <h3 style="font-size: 13pt; color: #0f172a; margin-bottom: 12px;">Object Oriented Development and Agile Practices</h3>
    <p style="font-style: italic; color: #64748b; margin-bottom: 20px;">Designing, Testing and Evolving Software with AI Assistance</p>

    <p><strong>Author:</strong> Dr. Polla Abdulhamid Fattah</p>
    <p><strong>Course Context:</strong> SE506: Object Oriented Development and Agile Practices (MSc in AI / Software Engineering)</p>
    <p><strong>Published By:</strong> Academic and Professional Engineering Monograph Series</p>
    <p><strong>Publication Date:</strong> 2026</p>
    <p><strong>Repository and Continuous Updates:</strong> <a href="https://github.com/polla-fattah/ood-agile-book" style="color: #0284c7;">github.com/polla-fattah/ood-agile-book</a></p>
    <p><strong>Online Interactive Platform:</strong> <a href="https://polla.dev/ood-agile-book/" style="color: #0284c7;">polla.dev/ood-agile-book/</a></p>

    <div style="margin-top: 36px; padding: 16px; background: #f8fafc; border-left: 3pt solid #0284c7; border-radius: 4px;">
      <p style="margin: 0; font-size: 8.5pt; color: #334155;">
        <strong>About This Work:</strong><br>
        This textbook guides postgraduate and advanced students from writing classes to designing, testing, reviewing, and changing maintainable software in a collaborative team workflow. Its central teaching unit is a software change: understand requested behavior, choose an object-oriented design, protect it with automated tests, inspect results, and use feedback to plan subsequent iterations.
      </p>
    </div>

    <div style="margin-top: 50px; font-size: 8pt; color: #64748b; line-height: 1.6;">
      <p><strong>Copyright &copy; 2026 Dr. Polla Abdulhamid Fattah.</strong></p>
      <p>This work is open access and licensed under the <strong>Creative Commons Attribution 4.0 International License (CC BY 4.0)</strong>. You are free to share (copy and redistribute the material in any medium or format) and adapt (remix, transform, and build upon the material) for any purpose, including commercially, provided appropriate credit is given to the author.</p>
    </div>
  </div>
</body>
</html>
"""
    with open(TITLE_HTML, "w", encoding="utf-8") as f:
        f.write(title_html)

    print("Preparing Content Pages Document...")
    with open(HTML_SOURCE, "r", encoding="utf-8") as f:
        content_raw = f.read()

    # Force html tag to pure light mode
    content_raw = re.sub(
        r'<html[^>]*>',
        '<html lang="en" data-bs-theme="light" data-theme="light" class="light-mode">',
        content_raw,
        count=1
    )

    # Strip theme switcher script so it doesn't dynamically flip to dark mode
    content_raw = re.sub(r'<script>\s*\(function\(\)\s*\{\s*const themeKey.*?</script>', '', content_raw, flags=re.DOTALL)

    # Set meta color-scheme to light
    content_raw = re.sub(r'<meta name="color-scheme"[^>]*>', '<meta name="color-scheme" content="light">', content_raw)

    # Remove only the inline dark-theme canvas override (keep all script tags so Mermaid runs)
    content_raw = re.sub(r'<style>\s*html\s*\{[^}]*Canvas.*?<\/style>', '', content_raw, flags=re.DOTALL)

    # Remove cover divs
    content_raw = re.sub(r'<div class="td-book-cover-page[^"]*".*?</div>', '', content_raw, flags=re.DOTALL)

    # Remove redundant root book landing section (which duplicates the TOC and overview)
    content_raw = re.sub(
        r'<section[^>]*data-td-book-page=[\"\']?/book[\"\']?[^>]*>.*?(?=<section[^>]*data-td-book-page=[\"\']?/book/chapter-01)',
        '',
        content_raw,
        flags=re.DOTALL
    )

    # Remove the self-referencing first item in the print TOC pointing to the book root
    content_raw = re.sub(
        r'<li>\s*<a\s+href=[\"\']?#pg-[^\"\'>\s]+[\"\']?>\s*Object Oriented Development and Agile Practices\s*</a>\s*</li>',
        '',
        content_raw,
        count=1
    )

    # Convert any mdash to hyphens
    content_raw = content_raw.replace("\u2014", " - ").replace("&mdash;", " - ")

    # Inject base CSS with explicit @page and root white background overrides
    page_white_css = """
    <style>
    @page {
      background: #ffffff !important;
      background-color: #ffffff !important;
    }
    html, :root {
      color-scheme: light !important;
      background: #ffffff !important;
      background-color: #ffffff !important;
    }
    body, .td-print-view, .container-fluid, .td-print-shell, .td-print-document, main {
      background: #ffffff !important;
      background-color: #ffffff !important;
    }
    </style>
    """
    mermaid_script_tag = f'<script src="file:///{MERMAID_JS_PATH.replace(os.sep, "/")}"></script>'
    mermaid_diagram_css = """
    <style>
    .mermaid-rendered-diagram {
      display: block !important;
      text-align: center !important;
      margin: 24px auto !important;
      max-width: 100% !important;
      break-inside: avoid !important;
      page-break-inside: avoid !important;
    }
    .mermaid-rendered-diagram svg {
      display: inline-block !important;
      max-width: 95% !important;
      height: auto !important;
      margin: 0 auto !important;
    }
    </style>
    """
    content_raw = content_raw.replace("</head>", f"{base_css}\n{page_white_css}\n{mermaid_script_tag}\n{mermaid_diagram_css}</head>")

    with open(CONTENT_HTML, "w", encoding="utf-8") as f:
        f.write(content_raw)

    print("Documents prepared.")


async def render_pdfs():
    print("Launching Chrome headless...")
    browser = await launch(
        executablePath=CHROME_PATH,
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-dev-shm-usage",
            "--allow-file-access-from-files",
            "--disable-web-security",
            "--force-color-profile=srgb",
            "--blink-settings=forceDarkModeEnabled=false",
        ],
    )
    page = await browser.newPage()

    # Enforce light color scheme via Chrome DevTools Protocol
    try:
        await page._client.send('Emulation.setEmulatedMedia', {
            'media': 'screen',
            'features': [{'name': 'prefers-color-scheme', 'value': 'light'}]
        })
    except Exception as e:
        print(f"Notice: setEmulatedMedia: {e}")

    await page.emulateMedia('screen')

    # 1. Render Title and Colophon (NO headers, NO footers)
    print("Rendering Title and Colophon to PDF...")
    title_url = f"file:///{TITLE_HTML.replace('\\', '/')}"
    await page.goto(title_url, {"waitUntil": "networkidle0", "timeout": 60000})
    await page.pdf({
        "path": TITLE_PDF,
        "format": "A4",
        "printBackground": True,
        "displayHeaderFooter": False,
        "margin": {
            "top": "20mm",
            "bottom": "20mm",
            "left": "20mm",
            "right": "20mm",
        },
    })

    # 2. Render Content (WITH elegant running headers and footers)
    print("Rendering Content to PDF...")
    content_url = f"file:///{CONTENT_HTML.replace('\\', '/')}"
    await page.goto(content_url, {"waitUntil": "networkidle0", "timeout": 120000})

    # Render all Mermaid diagrams directly to SVGs
    print("Rendering all Mermaid diagrams to SVGs...")
    render_diagrams_script = """
    async () => {
      if (!window.mermaid) {
        console.error("Mermaid library is not loaded!");
        return { success: false, reason: "Mermaid not loaded" };
      }
      mermaid.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        themeVariables: {
          fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          fontSize: '13px',
          primaryColor: '#f0f9ff',
          primaryBorderColor: '#0284c7',
          primaryTextColor: '#0f172a',
          lineColor: '#334155'
        }
      });

      const blocks = Array.from(document.querySelectorAll('pre.td-mermaid-source, pre[class*="td-mermaid-source"]'));
      let rendered = 0;
      let failed = 0;
      for (let i = 0; i < blocks.length; i++) {
        const pre = blocks[i];
        const codeEl = pre.querySelector('code') || pre;
        const source = codeEl.textContent.trim();
        if (!source) continue;

        const id = 'mermaid-pdf-diagram-' + (i + 1);
        try {
          const res = await mermaid.render(id, source);
          const container = document.createElement('div');
          container.className = 'mermaid-rendered-diagram';
          container.innerHTML = res.svg;
          pre.parentNode.replaceChild(container, pre);
          rendered++;
        } catch (err) {
          console.warn("Failed to render diagram " + (i + 1) + ":", err);
          failed++;
          const stray = document.getElementById('d' + id) || document.getElementById(id);
          if (stray && stray.parentNode) stray.parentNode.removeChild(stray);
        }
      }
      return { total: blocks.length, rendered: rendered, failed: failed };
    }
    """
    try:
        diag_stats = await page.evaluate(render_diagrams_script)
        print(f"Mermaid rendering result: {diag_stats}")
    except Exception as e:
        print(f"Warning: Mermaid rendering exception: {e}")

    # Extra settle time for fonts and layout reflow
    await asyncio.sleep(2)

    # Render Content pages cleanly without browser headers/footers
    # Precision running headers and footers are dynamically applied by PyMuPDF during assembly
    await page.pdf({
        "path": CONTENT_PDF,
        "format": "A4",
        "printBackground": True,
        "displayHeaderFooter": False,
        "margin": {
            "top": "22mm",
            "bottom": "22mm",
            "left": "20mm",
            "right": "20mm",
        },
    })

    await browser.close()
    print("Both PDF parts rendered.")


def assemble_final_pdf():
    print("Assembling final publication PDF with PyMuPDF...")
    A4_WIDTH = 595.276
    A4_HEIGHT = 841.890
    a4_rect = pymupdf.Rect(0, 0, A4_WIDTH, A4_HEIGHT)
    bg_color = (13 / 255.0, 20 / 255.0, 28 / 255.0)

    def add_cover(document, image_path):
        page = document.new_page(width=A4_WIDTH, height=A4_HEIGHT)
        page.draw_rect(a4_rect, color=bg_color, fill=bg_color, overlay=True)
        page.insert_image(a4_rect, filename=image_path, keep_proportion=False)
        return page

    final_doc = pymupdf.open()

    # 1. Front Cover (Full Bleed)
    print(f"Adding Front Cover from {FRONT_COVER_IMG}...")
    add_cover(final_doc, FRONT_COVER_IMG)

    # 2. Title & Colophon Pages (2 pages, clean)
    print(f"Inserting Title & Colophon pages ({TITLE_PDF})...")
    title_doc = pymupdf.open(TITLE_PDF)
    final_doc.insert_pdf(title_doc)
    title_doc.close()

    # 3. Main Content Pages (TOC + Chapters 1-15 + Appendices A-F)
    print(f"Structuring recto (two-sided) chapter openings and blank pages ({CONTENT_PDF})...")
    content_doc = pymupdf.open(CONTENT_PDF)

    # Extract starting page for each chapter from TOC links on page 0
    starts = []
    p0_src = content_doc[0]
    for link in p0_src.get_links():
        page = link.get("page")
        if page is not None and page not in [s[0] for s in starts]:
            rect = pymupdf.Rect(link["from"])
            title = p0_src.get_text("text", clip=rect).strip().replace("\n", " ")
            starts.append((page, title))

    starts.sort(key=lambda x: x[0])
    sections = [(0, "Table of Contents")] + starts

    # Build recto document with intentional blank pages so every chapter starts on a right-hand (odd) page
    orig_to_new = {}
    new_chapter_starts = {}
    chapter_first_pages = set()
    blank_pages = set()

    recto_doc = pymupdf.open()
    c_width = p0_src.rect.width
    c_height = p0_src.rect.height

    new_page_idx = 0

    for idx in range(len(sections)):
        orig_start, title = sections[idx]
        orig_end = sections[idx + 1][0] if idx + 1 < len(sections) else len(content_doc)
        page_count = orig_end - orig_start

        new_chapter_starts[new_page_idx] = title
        chapter_first_pages.add(new_page_idx)

        for p_offset in range(page_count):
            orig_p = orig_start + p_offset
            orig_to_new[orig_p] = new_page_idx
            recto_doc.insert_pdf(content_doc, from_page=orig_p, to_page=orig_p)
            new_page_idx += 1

        # If section ends on an ODD page number (new_page_idx % 2 != 0), the next page is an EVEN page (verso).
        # Insert a blank page so the following chapter opens on a fresh ODD page (recto).
        if idx < len(sections) - 1:
            if new_page_idx % 2 != 0:
                recto_doc.new_page(width=c_width, height=c_height)
                blank_pages.add(new_page_idx)
                new_page_idx += 1

    # Apply publication headers and footers across all recto pages
    print("Applying publication running headers and footers to recto pages...")
    left_x = 56.7  # 20mm
    right_x = c_width - 56.7  # page width minus 20mm
    y_header_line = 46.0
    y_header_text = 41.0
    y_footer_line = c_height - 46.0
    y_footer_text = c_height - 34.0

    line_color = (203 / 255.0, 213 / 255.0, 225 / 255.0)
    text_color = (100 / 255.0, 116 / 255.0, 139 / 255.0)
    author_name = "Dr. Polla Abdulhamid Fattah"
    book_title = "Object Oriented Development and Agile Practices"

    curr_chapter = "Table of Contents"

    for pno in range(len(recto_doc)):
        page = recto_doc[pno]
        page_num = pno + 1  # 1-based page number within content

        # Intentional blank pages receive NO headers and NO footers
        if pno in blank_pages:
            continue

        if pno in new_chapter_starts:
            curr_chapter = new_chapter_starts[pno]

        is_even = (page_num % 2 == 0)
        is_first_page = (pno in chapter_first_pages)

        # Header: alternate book name (even pages) and chapter name (odd pages)
        # Suppressed on chapter opening pages for clean typography
        if not is_first_page:
            if is_even:
                header_text = book_title
                page.insert_text(pymupdf.Point(left_x, y_header_text), header_text, fontname="helv", fontsize=8, color=text_color)
            else:
                header_text = curr_chapter
                tw = pymupdf.get_text_length(header_text, fontname="helv", fontsize=8)
                page.insert_text(pymupdf.Point(right_x - tw, y_header_text), header_text, fontname="helv", fontsize=8, color=text_color)

            page.draw_line(pymupdf.Point(left_x, y_header_line), pymupdf.Point(right_x, y_header_line), color=line_color, width=0.5)

        # Footer: author on bottom-left, page number on bottom-right
        page.insert_text(pymupdf.Point(left_x, y_footer_text), author_name, fontname="helv", fontsize=8, color=text_color)

        page_str = str(page_num)
        pw = pymupdf.get_text_length(page_str, fontname="helv", fontsize=8)
        page.insert_text(pymupdf.Point(right_x - pw, y_footer_text), page_str, fontname="helv", fontsize=8, color=text_color)

        page.draw_line(pymupdf.Point(left_x, y_footer_line), pymupdf.Point(right_x, y_footer_line), color=line_color, width=0.5)

    print("Inserting Book Content pages into final publication...")
    final_doc.insert_pdf(recto_doc)

    # 4. Back Cover (Full Bleed)
    print(f"Adding Back Cover from {BACK_COVER_IMG}...")
    add_cover(final_doc, BACK_COVER_IMG)

    # 5. Restore clickable Table of Contents links and generate PDF Bookmarks / Outline
    print("Re-linking Table of Contents and internal links in final PDF...")
    PAGE_OFFSET = 3  # (1 front cover + 2 title/colophon pages)
    pdf_toc = [
        [1, "Cover", 1],
        [1, "Title Page", 2],
        [1, "Colophon and License", 3],
        [1, "Table of Contents", 4],
    ]

    p0_src = content_doc[0]
    final_toc_page = final_doc[PAGE_OFFSET]  # Page index 3

    for link in p0_src.get_links():
        if link.get("kind") == 4 or link.get("nameddest"):
            src_target = link.get("page")
            if src_target is not None and src_target >= 0:
                new_target = orig_to_new.get(src_target, src_target)
                final_target = new_target + PAGE_OFFSET
                new_link = {
                    "kind": pymupdf.LINK_GOTO,
                    "from": link["from"],
                    "page": final_target,
                    "to": pymupdf.Point(0, 0),
                }
                final_toc_page.insert_link(new_link)

                # Extract title for the PDF bookmarks outline
                rect = pymupdf.Rect(link["from"])
                title_text = p0_src.get_text("text", clip=rect).strip().replace("\n", " ")
                if title_text:
                    pdf_toc.append([1, title_text, final_target + 1])

    # Also restore any other internal links across the rest of the content pages
    for orig_page_num in range(1, len(content_doc)):
        src_page = content_doc[orig_page_num]
        new_page_num = orig_to_new.get(orig_page_num)
        if new_page_num is None:
            continue
        final_page = final_doc[new_page_num + PAGE_OFFSET]
        for link in src_page.get_links():
            if link.get("kind") == 4:
                src_target = link.get("page")
                if src_target is not None and src_target >= 0:
                    target_new = orig_to_new.get(src_target, src_target)
                    final_target = target_new + PAGE_OFFSET
                    new_link = {
                        "kind": pymupdf.LINK_GOTO,
                        "from": link["from"],
                        "page": final_target,
                        "to": link.get("to", pymupdf.Point(0, 0)),
                    }
                    final_page.insert_link(new_link)

    # Set PDF bookmarks outline
    final_doc.set_toc(pdf_toc)
    recto_doc.close()
    content_doc.close()

    # Save
    final_doc.save(OUTPUT_PDF, garbage=4, deflate=True)
    final_doc.save(PUBLIC_PDF, garbage=4, deflate=True)
    page_count = len(final_doc)
    final_doc.close()

    file_size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print("=" * 60)
    print(f"SUCCESS! Publication-grade PDF assembled successfully!")
    print(f"Path: {OUTPUT_PDF}")
    print(f"Total Pages: {page_count}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print("=" * 60)


if __name__ == "__main__":
    prepare_documents()
    asyncio.get_event_loop().run_until_complete(render_pdfs())
    assemble_final_pdf()
