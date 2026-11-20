#!/usr/bin/env python3
"""Generate the gta6-meme-x-01 v3 meme image (1024x1024 PNG).

Concept (v3, NEW angle -- a fake official Rockstar delay notice, NOT
the v1 "13 years waiting / Mission Passed" joke and NOT the v2
"launch-day sick day" joke): Rockstar has delayed GTA VI again, and
the delay itself is now a bureaucratic document. A Swiss-style
official notice -- one huge light headline, one pink accent, hairline
rules, an itemised ledger with dotted leaders -- lists every date
Rockstar has already missed, counts the 1,081 days since Trailer 1
(5 Dec 2023 -> 20 Nov 2026), and ends on the total: patience
remaining 0%. A pink PAID stamp says the agent already paid on
make.fun; the black footer admits Rockstar still hasn't delivered.

Why this angle: the leaderboard's top entries are all fake official
documents with itemised numbers and a "paid by my AI agent on
make.fun" stamp (Leonida Mart receipt, Steam invoice, library
overdue notice). A delay notice is the same winning *device* -- an
official document -- with a different document and a different joke:
the date that keeps moving, not the wait itself and not a sick day.

Build: everything is drawn deterministically with Pillow -- no scene
plate, no AI-rendered text anywhere, so every word is spelled
exactly right. The only bitmap is the make.fun ghost from the press
kit (assets/mark-1024.png, https://make.fun/press/), pasted white
on the black footer block where it is actually visible.

Style (Guizang Swiss, adapted to a square meme): strict 48px grid,
left-aligned, hairline rules, exactly one accent -- GTA VI pink
#D1006B (5.1:1 on the paper, readable at every size) -- huge
display type in Noto Sans Light ("the larger, the lighter"), small
labels in DejaVu Sans Mono Bold. No gradients, no rounded cards, no
shadows, no decoration that explains nothing.

v3.1: Lucia & Jason join as original flat-vector busts in the empty
band right of "AGAIN." and below the PAID stamp (draw_characters),
same palette plus a light pink skin tint -- no official artwork
copied, no text covered.

Deterministic: fixed coordinates, fixed fonts, no randomness, no
network. Re-running produces the same bytes.

Usage: python3 generate_meme.py  (writes meme.png next to this script)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "meme.png"

W, H = 1024, 1024
M = 48            # grid margin
R = W - M         # right content edge (976)

PAPER = (250, 250, 248)
INK = (10, 10, 10)
ACCENT = (209, 0, 107)        # GTA VI pink, single accent
GREY = (110, 110, 104)
DOT = (169, 169, 160)
FOOT = (10, 10, 10)
FOOT_TEXT = (232, 232, 226)

LIGHT = "/usr/share/fonts/truetype/noto/NotoSans-Light.ttf"
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def draw_left(draw, x, y, text, f, fill):
    draw.text((x, y), text, font=f, fill=fill)


def draw_right(draw, x, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text((x - w, y), text, font=f, fill=fill)


def draw_center(draw, cx, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)


def dotted_leader(draw, x0, x1, y, color=DOT, step=9, r=2):
    """Dotted leader between a row label and its value."""
    x = x0
    while x + r * 2 <= x1:
        draw.ellipse([x, y - r, x + r * 2, y + r], fill=color)
        x += step


def draw_stamp(img):
    """PAID stamp, drawn on its own layer, rotated -8 degrees.

    Mirrors the winning device from the leaderboard (a stamp saying
    the agent already paid on make.fun) without copying any entry's
    stamp artwork: ours is a pink outline box with PAID on top and
    the agent line underneath, placed in the empty space right of
    the headline where it collides with nothing.
    """
    layer = Image.new("RGBA", (360, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([4, 4, 355, 165], outline=ACCENT + (255,), width=5)
    d.rectangle([12, 12, 347, 157], outline=ACCENT + (255,), width=2)
    paid = font(BOLD, 58)
    draw_center(d, 180, 20, "PAID", paid, ACCENT + (255,))
    small = font(MONO, 19)
    draw_center(d, 180, 92, "BY MY AI AGENT", small, ACCENT + (255,))
    draw_center(d, 180, 118, "ON MAKE.FUN", small, ACCENT + (255,))
    layer = layer.rotate(8, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(layer, (628, 138))


def draw_characters(img):
    """Lucia & Jason -- original flat vector busts (v3.1).

    Drawn from scratch in code (Pillow primitives only) in the same
    palette -- GTA pink #D1006B, ink black, paper off-white, plus a
    light pink tint for skin derived from the accent. NOT a copy of
    any official Rockstar artwork: no key art, no screenshot, no
    traced image -- just two simple bust silhouettes (long hair +
    pink top for Lucia; cap + sunglasses + beard for Jason) with a
    small pink Vice City sun between them.

    Placement: the empty band right of "AGAIN." and below the PAID
    stamp. Measured from the v3 render: the stamp's bottom edge
    slopes from y~352 (x=660) to y~309 (x=960), and the ledger
    header starts at y=452 -- so the busts live in y 342..446,
    x 672..954, touching no text at all.
    """
    draw = ImageDraw.Draw(img, "RGBA")
    SKIN = (242, 211, 224)  # light pink tint, accent family

    # ---- Vice City sun (small, between the two heads) ---------------
    draw.ellipse([796, 350, 828, 382], fill=ACCENT)

    # ---- Lucia (left, centre x=738) ----------------------------------
    # hair back mass
    draw.ellipse([676, 358, 800, 446], fill=INK)
    # neck + pink top (shoulders)
    draw.rectangle([729, 404, 747, 422], fill=SKIN)
    draw.polygon([(676, 446), (690, 420), (712, 410),
                  (764, 410), (786, 420), (800, 446)], fill=ACCENT)
    # face
    draw.ellipse([708, 362, 768, 430], fill=SKIN)
    # fringe over forehead
    draw.ellipse([702, 350, 774, 380], fill=INK)
    draw.ellipse([708, 362, 768, 430], fill=SKIN)
    # side locks framing the face
    draw.ellipse([696, 362, 716, 424], fill=INK)
    draw.ellipse([760, 362, 780, 424], fill=INK)
    # eyes, lips, earring
    draw.ellipse([721, 390, 727, 396], fill=INK)
    draw.ellipse([745, 390, 751, 396], fill=INK)
    draw.ellipse([729, 411, 743, 417], fill=ACCENT)
    draw.ellipse([700, 408, 706, 414], fill=ACCENT)

    # ---- Jason (right, centre x=898) ---------------------------------
    # dark shirt (shoulders)
    draw.polygon([(842, 446), (856, 426), (880, 416),
                  (916, 416), (940, 426), (954, 446)], fill=INK)
    # neck + face
    draw.rectangle([889, 408, 907, 420], fill=SKIN)
    draw.ellipse([868, 364, 928, 432], fill=SKIN)
    # beard along the jaw (thin, so cheek skin still shows)
    draw.arc([866, 392, 930, 436], start=15, end=165,
             fill=INK, width=9)
    # sunglasses: two separate lenses + bridge (not one mask bar),
    # with two glints
    draw.rounded_rectangle([870, 389, 894, 403], radius=6, fill=INK)
    draw.rounded_rectangle([902, 389, 926, 403], radius=6, fill=INK)
    draw.line([894, 395, 902, 395], fill=INK, width=3)
    draw.ellipse([877, 392, 882, 397], fill=PAPER)
    draw.ellipse([909, 392, 914, 397], fill=PAPER)
    # cap: pink dome + ink brim + white button (pink breaks up the
    # black mass so the head reads as a cap, not a burglar mask)
    draw.ellipse([864, 342, 932, 378], fill=ACCENT)
    draw.rounded_rectangle([856, 366, 940, 380], radius=7, fill=INK)
    draw.ellipse([894, 340, 902, 348], fill=PAPER)


def main():
    img = Image.new("RGB", (W, H), PAPER).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # ---- Meta row ---------------------------------------------------
    mono22 = font(MONO, 22)
    draw_left(draw, M, 46, "ROCKSTAR GAMES", mono22, INK)
    draw_right(draw, R, 46, "DELAY NOTICE \u2014 N\u00ba 003", mono22, INK)
    draw.line([M, 88, R, 88], fill=INK, width=2)

    # ---- Kicker ------------------------------------------------------
    mono24 = font(MONO, 24)
    draw_left(draw, M, 106, "GRAND THEFT AUTO VI \u2014 RELEASE DATE UPDATE",
              mono24, ACCENT)

    # ---- Headline: huge, light, left-aligned -------------------------
    # "The larger, the lighter": Noto Sans Light at 150px. Auto-fit:
    # line 1 must stay left of the stamp zone (x < 620).
    size = 150
    while size > 110:
        head = font(LIGHT, size)
        if text_w(draw, "DELAYED", head) <= 570:
            break
        size -= 5
    head = font(LIGHT, size)
    draw_left(draw, M, 138, "DELAYED", head, INK)
    draw_left(draw, M, 138 + size - 5, "AGAIN.", head, ACCENT)

    # ---- Ledger header ------------------------------------------------
    hy = 452
    draw_left(draw, M, hy, "ITEM", mono22, GREY)
    draw_right(draw, R, hy, "STATUS", mono22, GREY)
    draw.line([M, hy + 30, R, hy + 30], fill=INK, width=2)

    # ---- Ledger rows (dotted leaders, strikethrough on missed dates) --
    mono29 = font(MONO, 29)
    rows = [
        ("FALL 2025 \u2014 FIRST DATE", "DELAYED", GREY, True),
        ("SPRING 2026 \u2014 SECOND DATE", "DELAYED", GREY, True),
        ("MAY 26, 2026 \u2014 THIRD DATE", "PENDING*", ACCENT, False),
        ("DAYS SINCE TRAILER 1", "1,081 DAYS", INK, False),
        ("GTA V REPLAYS WHILE WAITING", "12", INK, False),
    ]
    y = 492
    for label, value, color, struck in rows:
        draw_left(draw, M, y, label, mono29, INK)
        lw = text_w(draw, label, mono29)
        vw = text_w(draw, value, mono29)
        dotted_leader(draw, M + lw + 14, R - vw - 14, y + 20)
        draw_right(draw, R, y, value, mono29, color)
        if struck:
            # strikethrough through the missed date label only
            mid = y + 20
            draw.line([M, mid, M + lw, mid], fill=GREY, width=3)
        y += 54
        if label is not rows[-1][0]:
            draw.line([M, y - 8, R, y - 8], fill=(201, 201, 194), width=1)

    # ---- Total row ------------------------------------------------------
    draw.line([M, 762, R, 762], fill=INK, width=2)
    mono34 = font(MONO, 34)
    draw_left(draw, M, 774, "PATIENCE REMAINING", mono34, INK)
    draw_right(draw, R, 770, "0%", font(MONO, 40), ACCENT)
    draw_left(draw, M, 826, "*Probably. Ask again in May.",
              font(REGULAR, 20), GREY)

    # ---- Stamp (empty space right of the headline) ----------------------
    draw_stamp(img)
    draw = ImageDraw.Draw(img, "RGBA")

    # ---- Lucia & Jason busts (band below the stamp, right of AGAIN.) ---
    draw_characters(img)
    draw = ImageDraw.Draw(img, "RGBA")

    # ---- Footer: black block, ghost + make.fun + punchline --------------
    draw.rectangle([M, 862, R, 976], fill=FOOT)
    ghost = Image.open(ASSETS / "mark-1024.png").convert("RGBA")
    ghost = ghost.resize((92, 92), Image.LANCZOS)
    img.paste(ghost, (64, 873), ghost)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_left(draw, 176, 876, "make.fun", font(BOLD, 36), (255, 255, 255))
    draw_left(draw, 176, 924, "MY AGENT ALREADY PAID. ROCKSTAR HASN'T DELIVERED.",
              font(MONO, 22), FOOT_TEXT)

    img.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
