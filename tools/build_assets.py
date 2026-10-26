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


SOCIAL = ASSETS / "social"
MASTERS = SOCIAL / "masters"


def _cover_crop(im, size):
    tw, th = size
    scale = max(tw / im.width, th / im.height)
    resized = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    x = max(0, (resized.width - tw) // 2)
    y = max(0, (resized.height - th) // 2)
    return resized.crop((x, y, x + tw, y + th))


def _scrim(im, left_alpha=225):
    w, h = im.size
    grad = Image.new("L", (w, h), 0)
    px = grad.load()
    for x in range(w):
        a = int(left_alpha * max(0.0, 1 - x / (w * 0.72)) ** 1.35)
        for y in range(h):
            px[x, y] = a
    black = Image.new("RGB", (w, h), (10, 10, 14))
    return Image.composite(black, im, grad)


def _master(name):
    path = MASTERS / name
    if not path.exists():
        raise FileNotFoundError(f"social master missing: {path}")
    return Image.open(path).convert("RGB")


def _banner(size, master, headline, sub, footer, logo_h, head_size, sub_size, foot_size, pad):
    im = _scrim(_cover_crop(_master(master), size))
    w, h = size
    _paste_logo(im, (pad, pad), logo_h)
    d = ImageDraw.Draw(im)
    y = pad + logo_h + int(h * 0.10)
    d.text((pad, y), headline, fill=WHITE, font=_font(head_size))
    y += int(head_size * 1.45)
    for line in sub:
        d.text((pad, y), line, fill=MUTED, font=_font(sub_size, bold=False))
        y += int(sub_size * 1.5)
    f_foot = _font(foot_size, bold=False)
    fw = d.textlength(footer, font=f_foot)
    d.rectangle([w - pad - fw, h - foot_size - 34, w - pad - fw + 54, h - foot_size - 28], fill=PINK)
    d.text((w - pad - fw, h - foot_size - 22), footer, fill="#E8E8E8", font=f_foot)
    d.rectangle([0, h - 6, w, h], fill=PINK)
    return im


def build_og() -> None:
    og = _banner(
        (1200, 630), "hvac-rooftop.jpg", "Service Profit",
        ["Accounting for air con, electrical", "and construction businesses."],
        "Pink Accounting \u00b7 Brendale QLD \u00b7 Registered Tax Agent 26284368",
        logo_h=52, head_size=62, sub_size=29, foot_size=20, pad=64,
    )
    png = ASSETS / "og.png"
    og.save(png, "PNG", optimize=True)
    print("og", png.stat().st_size)


def build_social() -> None:
    SOCIAL.mkdir(exist_ok=True)

    def save(im, name):
        path = SOCIAL / name
        im.save(path, "PNG", optimize=True)
        print(name, im.size, path.stat().st_size)

    av = Image.new("RGB", (1080, 1080), INK)
    logo = Image.open(ASSETS / "logo-white.png").convert("RGBA")
    lh = 170
    logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.Resampling.LANCZOS)
    av.paste(logo, ((1080 - logo.width) // 2, 300), logo)
    d = ImageDraw.Draw(av)
    f_head = _font(118)
    head = "Service Profit"
    d.text(((1080 - d.textlength(head, font=f_head)) / 2, 512), head, fill=WHITE, font=f_head)
    d.rectangle([440, 662, 640, 672], fill=PINK)
    f_sub = _font(34, bold=False)
    sub = "A Pink Accounting service"
    d.text(((1080 - d.textlength(sub, font=f_sub)) / 2, 700), sub, fill=MUTED, font=f_sub)
    save(av, "profile-1080.png")
    av.resize((720, 720), Image.Resampling.LANCZOS).save(SOCIAL / "profile-facebook-720.png", "PNG", optimize=True)
    av.resize((300, 300), Image.Resampling.LANCZOS).save(SOCIAL / "profile-linkedin-300.png", "PNG", optimize=True)
    print("profile exports 720/300 written")

    save(_banner((1640, 624), "electrical-switchboard.jpg", "Service Profit",
                 ["Accounting for HVAC, electrical and construction."],
                 "Pink Accounting \u00b7 Brendale \u00b7 Queensland",
                 logo_h=56, head_size=60, sub_size=29, foot_size=22, pad=72), "cover-facebook.png")
    save(_banner((1584, 396), "hvac-rooftop.jpg", "Service Profit",
                 ["HVAC, electrical and construction accounting \u00b7 Queensland"],
                 "Pink Accounting \u00b7 Registered Tax Agent 26284368",
                 logo_h=46, head_size=46, sub_size=21, foot_size=17, pad=56), "cover-linkedin.png")
    save(_banner((1200, 675), "construction-fitout.jpg", "Service Profit",
                 ["Job profit while you can still", "change the next quote."],
                 "Pink Accounting \u00b7 Brendale QLD \u00b7 Tax Agent 26284368",
                 logo_h=52, head_size=56, sub_size=28, foot_size=20, pad=64), "cover-google.png")

    posts = [
        ("post-quoted-hours.png", "electrical-switchboard.jpg", "You quoted 6 hours.", "You did 9.", "We show you the gap every Monday, then fix the next quote."),
        ("post-bank-not-yours.png", "hvac-rooftop.jpg", "The bank looks full.", "It is not all yours.", "GST, PAYG, super and wages sit in there. We pull it apart weekly."),
        ("post-first-monday.png", "construction-fitout.jpg", "Know which jobs paid.", "While you can still act.", "Quoted hours against hours on the tools, in your inbox Monday."),
    ]
    for name, master, line1, line2, body in posts:
        im = Image.new("RGB", (1080, 1350), INK)
        photo = _cover_crop(_master(master), (1080, 700))
        im.paste(photo, (0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 694, 1080, 700], fill=PINK)
        _paste_logo(im, (64, 748), 52)
        d = ImageDraw.Draw(im)
        d.text((64, 842), line1, fill=WHITE, font=_font(58))
        d.text((64, 922), line2, fill="#FF6E92", font=_font(58))
        d.text((64, 1032), body, fill=MUTED, font=_font(28, bold=False))
        d.text((64, 1246), "Service Profit \u00b7 Pink Accounting \u00b7 (07) 3544 6386", fill=SOFT, font=_font(22, bold=False))
        d.text((64, 1284), "Illustrative image.", fill=SOFT, font=_font(19, bold=False))
        save(im, name)



def build_favicon() -> None:
    # Square source only: the wide wordmark in an ICO comes out 16x7 and the
    # browser tab shows a smear. icon.png is the pink square logo, padding trimmed.
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
