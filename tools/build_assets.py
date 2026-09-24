from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

JPEG_STEMS = (
    "electrical",
    "construction",
    "tech-hvac",
    "tech-electrical",
    "pink-home",
    "pink-meet",
)


SOURCE = ASSETS / "_source"

# The job photos are graded; the photos of Huong are not. The work reads as a
# system, the person reads as a person. That difference is deliberate.
TRADE_STEMS = ("electrical", "construction", "tech-hvac", "tech-electrical")

# Hi-vis sits in this hue band. Everything outside it loses almost all colour.
HIVIS_HUE = (30, 100)


def hivis_grade(im):
    """Cool grey frame, hi-vis the only colour left in it.

    Does three jobs at once: it makes four photos shot in four different styles
    read as one deliberate set, it sends the eye to the person working instead
    of to whatever happened to be bright, and heavy grading is forgiving of a
    source that is only 838px wide.
    """
    from PIL import ImageEnhance, ImageFilter

    hue = im.convert("HSV").split()[0]
    lo, hi = HIVIS_HUE
    mask = hue.point(lambda h: 255 if lo <= h <= hi else 0)
    mask = mask.filter(ImageFilter.GaussianBlur(0.6))  # soften the cut-out edge
    kept = ImageEnhance.Color(im).enhance(1.25)
    drained = ImageEnhance.Color(im).enhance(0.10)
    out = Image.composite(kept, drained, mask)
    out = ImageEnhance.Contrast(out).enhance(1.24)
    r, g, b = out.split()
    b = b.point(lambda t: min(255, t + 6))
    r = r.point(lambda t: max(0, t - 3))
    return Image.merge("RGB", (r, g, b))


def to_webp(src: Path, stem: str, widths=(480, 864, 1200)) -> None:
    """Write the WebP ladder for one photo.

    Two rules, both learned the hard way:

    1. Never resize above the source. The trade photos are 838px wide. Emitting
       a 1200px variant from them does not add detail, it invents it, and the
       result looks soft on exactly the retina phones the audience uses.
    2. Downscaling softens edges. A light unsharp mask after the resize puts the
       perceived sharpness back without the halos you get from a heavy one.
    """
    from PIL import ImageFilter

    im = Image.open(src).convert("RGB")
    targets = sorted({w for w in widths if w < im.width} | {im.width})
    for w in targets:
        if w == im.width:
            resized = im
        else:
            h = max(1, round(im.height * w / im.width))
            resized = im.resize((w, h), Image.Resampling.LANCZOS)
            resized = resized.filter(
                ImageFilter.UnsharpMask(radius=0.8, percent=70, threshold=3)
            )
        out = ASSETS / f"{stem}-{w}.webp"
        resized.save(out, "WEBP", quality=84, method=6)
        print(f"{out.name:<34} {resized.width}x{resized.height}  {out.stat().st_size/1024:6.1f}KB")


def rebuild_photos() -> None:
    """Regenerate every photo ladder from the JPEG that ships beside it."""
    stale = []
    for stem in JPEG_STEMS:
        # A graded stem is regenerated from its untouched original every time, so
        # rebuilding never grades an already-graded file.
        original = SOURCE / f"{stem}.jpg"
        if stem in TRADE_STEMS and original.exists():
            with Image.open(original) as raw:
                hivis_grade(raw.convert("RGB")).save(
                    ASSETS / f"{stem}.jpg", "JPEG", quality=92, subsampling=0
                )
            print("graded", stem)
        src = ASSETS / f"{stem}.jpg"
        if not src.exists():
            print("missing source:", src.name)
            continue
        with Image.open(src) as probe:
            source_width = probe.width
        for old in ASSETS.glob(f"{stem}-*.webp"):
            width = int(old.stem.rsplit("-", 1)[1])
            if width > source_width:
                stale.append(old)
        to_webp(src, stem)
    for f in stale:
        f.unlink()
        print("removed upscaled variant:", f.name)


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
    # Square source only: the wide wordmark in an ICO comes out 16x7 and the
    # browser tab shows a smear. icon.png is the "pi" mark on a black tile.
    im = Image.open(SOURCE / "icon.png").convert("RGBA")
    assert im.width == im.height, "tab icon source must be square"
    ico = ROOT / "favicon.ico"
    im.save(ico, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    im.resize((180, 180), Image.LANCZOS).save(ROOT / "apple-touch-icon.png")
    print("favicon.ico", ico.stat().st_size)


if __name__ == "__main__":
    for stem in JPEG_STEMS:
        src = ASSETS / f"{stem}.jpg"
        if src.exists():
            to_webp(src, stem)
    build_og()
    build_social()
    build_favicon()
