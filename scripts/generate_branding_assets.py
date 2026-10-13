import os
import base64
from pathlib import Path
from PIL import Image

def generate_assets():
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    workspace_root = repo_root.parent

    src_logo = workspace_root / "logo.png"
    src_cover = workspace_root / "front-image.png"

    if not src_logo.exists():
        raise FileNotFoundError(f"Missing {src_logo}")
    if not src_cover.exists():
        raise FileNotFoundError(f"Missing {src_cover}")

    static_dir = repo_root / "static"
    static_images = static_dir / "images"
    assets_dir = repo_root / "assets"
    assets_images = assets_dir / "images"
    assets_icons = assets_dir / "icons"

    static_images.mkdir(parents=True, exist_ok=True)
    assets_images.mkdir(parents=True, exist_ok=True)
    assets_icons.mkdir(parents=True, exist_ok=True)

    # 1. Copy logo and cover to static and assets
    logo_img = Image.open(src_logo).convert("RGBA")
    cover_img = Image.open(src_cover).convert("RGBA")

    logo_img.save(static_images / "logo.png")
    logo_img.save(assets_images / "logo.png")
    logo_img.save(assets_icons / "logo.png")
    print(f"Saved logo: {logo_img.size} to static/images, assets/images, assets/icons")

    cover_img.save(static_images / "front-image.png")
    cover_img.save(static_images / "cover-front.png")
    cover_img.save(assets_images / "front-image.png")
    print(f"Saved cover: {cover_img.size} to static/images (front-image.png & cover-front.png), assets/images")

    # 2. Generate Favicons
    # ICO file
    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    logo_img.save(static_dir / "favicon.ico", format="ICO", sizes=ico_sizes)
    print("Generated static/favicon.ico (16, 32, 48)")

    # PNG sizes
    sizes = [16, 32, 48, 192, 512]
    for s in sizes:
        resized = logo_img.resize((s, s), Image.Resampling.LANCZOS)
        out_path = static_dir / f"favicon-{s}x{s}.png"
        resized.save(out_path, format="PNG")
        print(f"Generated {out_path.name}")

    # Apple touch icons
    apple_icon = logo_img.resize((180, 180), Image.Resampling.LANCZOS)
    apple_icon.save(static_dir / "apple-touch-icon.png", format="PNG")
    apple_icon.save(static_dir / "apple-touch-icon-180x180.png", format="PNG")
    print("Generated static/apple-touch-icon.png and static/apple-touch-icon-180x180.png")

    # 3. Generate SVG wrapper for favicon.svg and assets/icons/logo.svg
    with open(src_logo, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <image width="500" height="500" href="data:image/png;base64,{logo_b64}"/>
</svg>
'''
    (static_dir / "favicon.svg").write_text(svg_content, encoding="utf-8")
    (assets_icons / "logo.svg").write_text(svg_content, encoding="utf-8")
    print("Generated static/favicon.svg and assets/icons/logo.svg")

if __name__ == "__main__":
    generate_assets()
