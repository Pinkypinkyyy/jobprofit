from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

JPEG_STEMS = (
    "hvac",
    "electrical",
    "construction",
    "tech-hvac",
    "tech-electrical",
    "desk",
    "yard",
    "pink-home",
    "pink-meet",
    "pink-office",
    "pink-portrait",
    "pink-studio",
)


def to_webp(src: Path, stem: str, widths=(480, 864, 1200)) -> None:
    im = Image.open(src).convert("RGB")
    for w in widths:
        ratio = w / im.width
        h = max(1, int(im.height * ratio))
        resized = im.resize((w, h), Image.Resampling.LANCZOS)
        out = ASSETS / f"{stem}-{w}.webp"
        resized.save(out, "WEBP", quality=78, method=6)
        print(out.name, out.stat().st_size)
    full = ASSETS / f"{stem}.webp"
    im.save(full, "WEBP", quality=78, method=6)
    print(full.name, full.stat().st_size)


INK = "#0E0E12"
PINK = "#ED1651"
WHITE = "#FFFFFF"
MUTED = "#C8C8C8"
SOFT = "#8A8A8A"


def _font(size, bold=True):
    names = (
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    )
    for path in names:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _paste_logo(canvas, xy, height):
    logo_path = ASSETS / "logo-white.png"
    if not logo_path.exists():
        return
    logo = Image.open(logo_path).convert("RGBA")
    ratio = height / logo.height
    logo = logo.resize((max(1, int(logo.width * ratio)), height), Image.Resampling.LANCZOS)
    canvas.paste(logo, xy, logo)


def build_og() -> None:
    og = Image.new("RGB", (1200, 630), INK)
    d = ImageDraw.Draw(og)
    d.rectangle([0, 0, 8, 630], fill=PINK)
    _paste_logo(og, (72, 56), 56)
    d.text((72, 200), "Service Profit", fill=WHITE, font=_font(64))
    d.text((72, 286), "Pink Accounting for HVAC, electrical", fill=MUTED, font=_font(32, bold=False))
    d.text((72, 330), "and construction service businesses.", fill=MUTED, font=_font(32, bold=False))
    d.text((72, 520), "Queensland  ·  Registered Tax Agent 26284368", fill=SOFT, font=_font(22, bold=False))
    png = ASSETS / "og.png"
    webp = ASSETS / "og.webp"
    og.save(png, "PNG", optimize=True)
    og.save(webp, "WEBP", quality=82, method=6)
    print("og", png.stat().st_size, webp.stat().st_size)


def build_social() -> None:
    social = ASSETS / "social"
    social.mkdir(exist_ok=True)

    def save(im, name):
        path = social / name
        im.save(path, "PNG", optimize=True)
        print(name, im.size, path.stat().st_size)

    av = Image.new("RGB", (1080, 1080), INK)
    d = ImageDraw.Draw(av)
    d.rectangle([0, 0, 16, 1080], fill=PINK)
    _paste_logo(av, (96, 280), 88)
    d.text((96, 420), "Service Profit", fill=WHITE, font=_font(64))
    d.text((96, 510), "HVAC, electrical and construction", fill=MUTED, font=_font(28, bold=False))
    d.text((96, 900), "Pink Accounting  ·  Tax Agent 26284368", fill=SOFT, font=_font(24, bold=False))
    save(av, "profile-1080.png")

    fb = Image.new("RGB", (1640, 624), INK)
    d = ImageDraw.Draw(fb)
    d.rectangle([0, 0, 12, 624], fill=PINK)
    _paste_logo(fb, (72, 140), 56)
    d.text((72, 230), "Service Profit", fill=WHITE, font=_font(56))
    d.text((72, 310), "Accounting for HVAC, electrical and construction.", fill=MUTED, font=_font(28, bold=False))
    d.text((72, 500), "Pink Accounting  ·  Brendale  ·  Queensland", fill=SOFT, font=_font(22, bold=False))
    save(fb, "cover-facebook.png")

    li = Image.new("RGB", (1584, 396), INK)
    d = ImageDraw.Draw(li)
    d.rectangle([0, 0, 10, 396], fill=PINK)
    _paste_logo(li, (64, 48), 56)
    d.text((64, 140), "Service Profit", fill=WHITE, font=_font(48))
    d.text((64, 210), "HVAC, electrical and construction accounting  ·  Queensland", fill=MUTED, font=_font(22, bold=False))
    d.text((64, 300), "Pink Accounting  ·  Registered Tax Agent 26284368", fill=SOFT, font=_font(18, bold=False))
    save(li, "cover-linkedin.png")

    g = Image.new("RGB", (1200, 675), INK)
    d = ImageDraw.Draw(g)
    d.rectangle([0, 0, 10, 675], fill=PINK)
    _paste_logo(g, (64, 120), 56)
    d.text((64, 220), "Service Profit", fill=WHITE, font=_font(56))
    d.text((64, 300), "Job profit while you can still", fill=MUTED, font=_font(28, bold=False))
    d.text((64, 344), "change the next quote.", fill=MUTED, font=_font(28, bold=False))
    d.text((64, 540), "Pink Accounting  ·  Brendale QLD  ·  Tax Agent 26284368", fill=SOFT, font=_font(20, bold=False))
    save(g, "cover-google.png")


def build_favicon() -> None:
    src = ASSETS / "logo.png"
    im = Image.open(src).convert("RGBA")
    ico = ROOT / "favicon.ico"
    im.save(ico, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicon.ico", ico.stat().st_size)


if __name__ == "__main__":
    for stem in JPEG_STEMS:
        src = ASSETS / f"{stem}.jpg"
        if src.exists():
            to_webp(src, stem)
    build_og()
    build_social()
    build_favicon()
