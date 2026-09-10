from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def to_webp(src: Path, stem: str, widths=(480, 864, 1200)) -> None:
    im = Image.open(src).convert("RGB")
    for w in widths:
        ratio = w / im.width
        h = max(1, int(im.height * ratio))
        resized = im.resize((w, h), Image.Resampling.LANCZOS)
        out = ASSETS / f"{stem}-{w}.webp"
        resized.save(out, "WEBP", quality=78, method=6)
        print(out.name, out.stat().st_size)


def build_og() -> None:
    og = Image.new("RGB", (1200, 630), "#12161C")
    d = ImageDraw.Draw(og)
    d.rectangle([0, 0, 18, 630], fill="#1E6BD6")
    logo_path = ASSETS / "logo-white.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((72, 72), Image.Resampling.LANCZOS)
        og.paste(logo, (72, 72), logo)
    font_lg = font_md = font_sm = ImageFont.load_default()
    for path in (
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
    ):
        try:
            font_lg = ImageFont.truetype(path, 64)
            font_md = ImageFont.truetype(path, 32)
            font_sm = ImageFont.truetype(path, 22)
            break
        except OSError:
            continue
    d.text((72, 180), "Service Profit", fill="#FFFFFF", font=font_lg)
    d.text((72, 270), "Pink Accounting for HVAC, electrical", fill="#C8D0D8", font=font_md)
    d.text((72, 318), "and construction service businesses.", fill="#C8D0D8", font=font_md)
    d.text((72, 520), "Queensland  ·  Registered Tax Agent 26284368", fill="#8A93A0", font=font_sm)
    png = ASSETS / "og.png"
    webp = ASSETS / "og.webp"
    og.save(png, "PNG", optimize=True)
    og.save(webp, "WEBP", quality=82, method=6)
    print("og", png.stat().st_size, webp.stat().st_size)


if __name__ == "__main__":
    for name in ("hvac", "electrical", "construction"):
        to_webp(ASSETS / f"{name}.jpg", name)
    build_og()
