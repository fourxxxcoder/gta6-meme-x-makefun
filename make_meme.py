#!/usr/bin/env python3
"""Compose the GTA 6 meme for the make.fun gta6-meme-x-01 entry.

Scene: an exhausted gamer slumped on a Vice City bench beside a tower of
calendars (the 13-year wait since GTA V), while the make.fun ghost mascot
cruises in large and cheerful, coin in hand, already earning.

Inputs (in assets/):
  - vice-city-bg.png: AI-illustrated Leonida beach boulevard, no text.
  - makefun-mark-1024.png: make.fun's official press-kit mark
    (white ghost, sparkle eyes, magenta star coin, on a magenta disc).

Output: meme.png at the repository root, 1600x1600 PNG. That picture
is the entry itself once posted on X, so it is not committed: the
asset files above are local working files (the mark is make.fun's
own press asset) and meme.png is delivered with the post.
Captions are drawn here, in code, so the spelling is exact and the
letters stay large when the judge shrinks the picture to 480x480.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
BG_PATH = ROOT / "assets" / "vice-city-bg.png"
MARK_PATH = ROOT / "assets" / "makefun-mark-1024.png"
OUT_PATH = ROOT / "meme.png"

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

WHITE = (255, 255, 255)
BLACK = (10, 8, 12)
YELLOW = (255, 213, 74)
MAGENTA = (255, 92, 196)


def caption(draw, center_x, y, lines, size):
    """Draw centred meme lines: (text, colour) pairs, black outline."""
    font = ImageFont.truetype(FONT_BOLD, size)
    for text, colour in lines:
        draw.text(
            (center_x, y),
            text,
            font=font,
            fill=colour,
            anchor="ma",
            stroke_width=max(4, size // 14),
            stroke_fill=BLACK,
        )
        y += int(size * 1.18)
    return y


def paste_ghost(base, mark_path, box):
    """Paste the circular make.fun mark as a character in the scene.

    A soft shadow ellipse grounds it on the road, and the disc itself
    stays whole so the ghost, its sparkle eyes and its star coin read
    exactly as make.fun draws them.
    """
    mark = Image.open(mark_path).convert("RGBA")
    size = box[2] - box[0]
    mark = mark.resize((size, size), Image.LANCZOS)

    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((6, 6, size - 6, size - 6), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(3))

    shadow = ImageDraw.Draw(base)
    cx = (box[0] + box[2]) // 2
    shadow.ellipse(
        (cx - size // 3, box[3] - 26, cx + size // 3, box[3] + 22),
        fill=(40, 16, 60),
    )
    base.paste(mark, (box[0], box[1]), mask)


def main():
    img = Image.open(BG_PATH).convert("RGB")
    w, h = img.size  # 1600 x 1600

    # The ghost rolls in on the right, big enough to read at 480px:
    # roughly a third of the frame wide, overlapping the sports car.
    paste_ghost(img, MARK_PATH, (1035, 760, 1515, 1240))

    draw = ImageDraw.Draw(img)

    # Top and bottom caption bars, classic meme style.
    draw.rectangle((0, 0, w, 235), fill=BLACK)
    draw.rectangle((0, h - 265, w, h), fill=BLACK)

    caption(
        draw,
        w // 2,
        28,
        [
            ("WAITED 13 YEARS", WHITE),
            ("FOR GTA VI", YELLOW),
        ],
        92,
    )
    caption(
        draw,
        w // 2,
        h - 238,
        [
            ("MY AI AGENT ALREADY", WHITE),
            ("GOT PAID ON make.fun", MAGENTA),
        ],
        84,
    )

    img.save(OUT_PATH, "PNG")
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
