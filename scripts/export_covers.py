import os
import sys
from pathlib import Path
import win32com.client

def export_covers():
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    pptx_path = repo_root / "OOP_Agile_BookCover.pptx"

    if not pptx_path.exists():
        print(f"Error: {pptx_path} not found")
        sys.exit(1)

    print(f"Opening presentation: {pptx_path}")
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    try:
        # Open in read-only and without window
        pres = ppt.Presentations.Open(str(pptx_path), ReadOnly=True, Untitled=False, WithWindow=False)
        slide_count = pres.Slides.Count
        print(f"Total slides: {slide_count}")

        # Page setup dimensions
        page_width = pres.PageSetup.SlideWidth
        page_height = pres.PageSetup.SlideHeight
        print(f"Slide points: {page_width} x {page_height}")

        # Scale factor (e.g. target height around 1600-2400 for crisp book cover)
        scale = 3.0
        target_w = int(page_width * scale)
        target_h = int(page_height * scale)
        print(f"Export target resolution: {target_w} x {target_h}")

        static_images = repo_root / "static" / "images"
        assets_images = repo_root / "assets" / "images"
        static_images.mkdir(parents=True, exist_ok=True)
        assets_images.mkdir(parents=True, exist_ok=True)

        # Slide 1 -> front cover
        slide_front = pres.Slides(1)
        front_static_1 = static_images / "front-image.png"
        front_static_2 = static_images / "cover-front.png"
        front_assets = assets_images / "front-image.png"

        slide_front.Export(str(front_static_1), "PNG", target_w, target_h)
        slide_front.Export(str(front_static_2), "PNG", target_w, target_h)
        slide_front.Export(str(front_assets), "PNG", target_w, target_h)
        print(f"Exported Slide 1 to front-image.png and cover-front.png")

        # Slide last -> back cover
        slide_back = pres.Slides(slide_count)
        back_static_1 = static_images / "back-image.png"
        back_static_2 = static_images / "cover-back.png"
        back_assets = assets_images / "cover-back.png"

        slide_back.Export(str(back_static_1), "PNG", target_w, target_h)
        slide_back.Export(str(back_static_2), "PNG", target_w, target_h)
        slide_back.Export(str(back_assets), "PNG", target_w, target_h)
        print(f"Exported Slide {slide_count} to back-image.png and cover-back.png")

        pres.Close()
    finally:
        ppt.Quit()

if __name__ == "__main__":
    export_covers()
