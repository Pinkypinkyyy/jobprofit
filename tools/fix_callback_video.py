"""Turn the callback draft into a Pink-brand web master."""
from __future__ import annotations

import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\HuongBui\Downloads\callback-cost-clean-draft-20260912.mp4")
OUT_DIR = ROOT / "assets" / "video"
OUT = OUT_DIR / "callback-cost.mp4"
POSTER = OUT_DIR / "callback-cost-poster.jpg"
LOGO = ROOT / "assets" / "logo-white.png"
PINK = (237, 22, 81)  # #ED1651 RGB
INK = (14, 14, 18)
WHITE = (255, 255, 255)


def font(size, bold=True):
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


def recast_orange(bgr: np.ndarray) -> np.ndarray:
    """Swap saturated terracotta overlays to Pink. Leave face and necklace alone."""
    h, w = bgr.shape[:2]
    band = bgr[: int(h * 0.46)]
    rgb = cv2.cvtColor(band, cv2.COLOR_BGR2RGB)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mask = (
        (r > 150)
        & (g > 45)
        & (g < 130)
        & (b < 90)
        & (r > g + 35)
        & (r > b + 70)
    )
    rgb[mask] = PINK
    band[:] = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return bgr


def write_it_overlay(size) -> np.ndarray:
    w, h = size
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((24, 24, w - 24, 520), fill=(245, 245, 245, 250))
    d.rounded_rectangle((72, 72, 430, 124), 16, fill=INK + (255,))
    d.text((92, 86), "NOT THE FIX", fill=WHITE, font=font(22, True))
    d.rounded_rectangle((520, 72, 1008, 124), 16, fill=PINK + (255,))
    d.text((560, 86), "THE FIX", fill=WHITE, font=font(22, True))
    d.text((72, 160), "PUSH HARDER", fill=(120, 120, 120), font=font(52, True))
    d.line((76, 228, 470, 188), fill=PINK, width=7)
    d.text((520, 160), "WRITE IT", fill=INK, font=font(52, True))
    d.text((520, 228), "DOWN", fill=INK, font=font(52, True))
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGBA2BGRA)


def end_card(size) -> np.ndarray:
    w, h = size
    im = Image.new("RGB", (w, h), INK)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 14, h), fill=PINK)
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((280, 100), Image.Resampling.LANCZOS)
        im.paste(logo, (72, 220), logo)
    d.text((72, 380), "Service Profit", fill=WHITE, font=font(42, True))
    d.text((72, 520), "You cannot price a", fill=WHITE, font=font(48, True))
    d.text((72, 584), "problem you have", fill=WHITE, font=font(48, True))
    d.text((72, 648), "never counted.", fill=PINK, font=font(48, True))
    d.text((72, 820), "Book a 15-minute call", fill=WHITE, font=font(36, True))
    d.text((72, 880), "serviceprofit.com.au/book", fill=(200, 200, 200), font=font(28, False))
    d.text((72, 1680), "Pink Accounting  ·  Tax Agent 26284368", fill=(140, 140, 140), font=font(22, False))
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


def overlay_bgra(base_bgr, overlay_bgra):
    alpha = overlay_bgra[:, :, 3:4] / 255.0
    rgb = overlay_bgra[:, :, :3]
    return (base_bgr * (1 - alpha) + rgb * alpha).astype(np.uint8)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}")
    OUT_DIR.mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(SRC))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("in", w, h, fps, n)
    write_ov = write_it_overlay((w, h))
    end = end_card((w, h))
    raw = OUT_DIR / "_callback_raw.avi"
    writer = cv2.VideoWriter(str(raw), cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))
    i = 0
    poster_saved = False
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        t = i / fps
        frame = recast_orange(frame)
        if 28.6 <= t < 31.4:
            frame = overlay_bgra(frame, write_ov)
        if t >= 39.05:
            frame = end
        writer.write(frame)
        if not poster_saved and t >= 1.2:
            cv2.imwrite(str(POSTER), frame, [int(cv2.IMWRITE_JPEG_QUALITY), 86])
            poster_saved = True
        i += 1
        if i % 200 == 0:
            print("frame", i)
    cap.release()
    writer.release()
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(raw),
        "-i",
        str(SRC),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-crf",
        "22",
        "-preset",
        "medium",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "96k",
        "-movflags",
        "+faststart",
        "-shortest",
        str(OUT),
    ]
    subprocess.check_call(cmd)
    raw.unlink(missing_ok=True)
    print("out", OUT, OUT.stat().st_size, "poster", POSTER.stat().st_size)


if __name__ == "__main__":
    main()
