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

v3.3: Lucia & Jason redrawn FROM the official references (Rockstar
Lucia portrait, Jason hero render, duo key art -- studied, never
pasted or traced): Lucia's signature HIGH PONYTAIL with a wavy
cascade + stern angled brows + hoops + chain; Jason's short
sandy-blonde faded cut, visible eyes, solid dark stubble band on
the squared jaw (draw_characters). Same palette, same band, no
text covered.

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
    """Lucia & Jason -- original flat vector busts (v3.3).

    Drawn from scratch in code (Pillow primitives only) in the same
    palette -- GTA pink #D1006B, ink black, paper off-white, plus
    skin tints derived from the accent family. NOT a copy of any
    official Rockstar artwork: no key art, no screenshot, no traced
    image -- the likeness comes from STUDYING the official
    references (Rockstar's Lucia portrait + Jason hero render + duo
    key art, viewed in /tmp only, never pasted or traced) and
    rebuilding the two signature silhouettes in code:

    - Lucia (left): HIGH PONYTAIL -- hair swept up into a knot at
      the crown, a wavy cascade falling past her shoulder on one
      side, loose strands framing the face; tan skin, brows angled
      down toward the nose (stern), full closed lips, pink hoop
      earrings, thin pink chain with pendant, dark tank top.
    - Jason (right): short SANDY BLONDE hair, faded sides, textured
      top swept back, NO cap and NO sunglasses over the eyes (eyes
      visible); heavy straight brows, squared jaw, DARK STUBBLE
      filled along the whole jaw/chin (a solid band, not a ring),
      serious closed mouth, black shirt with a pink open collar.

    Placement: the empty band right of "AGAIN." and below the PAID
    stamp. The stamp's bottom edge slopes from y~352 (x=660) to
    y~309 (x=960), and the ledger header starts at y=452 -- so
    the busts live in y 342..446, x 672..954, touching no text.
    """
    draw = ImageDraw.Draw(img, "RGBA")
    SKIN_LUCIA = (199, 147, 108)   # tan / sawo matang
    SKIN_JASON = (235, 195, 170)   # tanned, warmer than v3.2
    BLONDE = (208, 172, 100)       # sandy blonde
    BLONDE_DARK = (178, 142, 72)   # blonde shading strokes
    STUBBLE = (96, 70, 44)         # dark stubble (jaw/chin band)
    NOSE_J = (205, 160, 135)
    NOSE_L = (150, 105, 70)

    # ---- Lucia (left, centre x=738) ----------------------------------
    # hair pulled back: swept-up mass behind the head
    draw.ellipse([700, 352, 776, 410], fill=INK)
    # dark tank top (thin straps) + neck
    draw.rectangle([729, 420, 747, 436], fill=SKIN_LUCIA)
    draw.polygon([(680, 446), (694, 422), (714, 414),
                  (762, 414), (782, 422), (796, 446)], fill=INK)
    # face (oval)
    draw.ellipse([710, 366, 766, 430], fill=SKIN_LUCIA)
    # swept hairline: hair pulled back off the forehead, high at the
    # centre, dipping at the temples
    draw.polygon([(706, 382), (714, 360), (738, 354), (762, 360),
                  (770, 382), (760, 372), (738, 366), (716, 372)],
                 fill=INK)
    # high ponytail knot at the crown (kept just below the stamp edge)
    draw.ellipse([726, 342, 756, 368], fill=INK)
    draw.ellipse([735, 358, 747, 366], fill=ACCENT)
    # wavy cascade falling past the shoulder on her left side
    # (overlapping ellipses = wavy edge)
    draw.ellipse([682, 368, 708, 408], fill=INK)
    draw.ellipse([678, 396, 704, 434], fill=INK)
    draw.ellipse([684, 422, 710, 448], fill=INK)
    # one loose curl on her right side, near the shoulder
    draw.ellipse([760, 394, 780, 430], fill=INK)
    # thin strands framing the face
    draw.polygon([(706, 374), (714, 374), (712, 402), (706, 402)],
                 fill=INK)
    draw.polygon([(762, 374), (770, 374), (770, 402), (764, 402)],
                 fill=INK)
    # stern brows angled DOWN toward the nose, heavy-lashed eyes,
    # nose, full closed lips, hoop earrings, chain + pendant
    draw.line([717, 386, 733, 390], fill=INK, width=4)
    draw.line([759, 386, 743, 390], fill=INK, width=4)
    draw.line([718, 391, 732, 391], fill=INK, width=2)
    draw.line([744, 391, 758, 391], fill=INK, width=2)
    draw.ellipse([720, 393, 728, 399], fill=INK)
    draw.ellipse([748, 393, 756, 399], fill=INK)
    draw.ellipse([722, 394, 724, 396], fill=PAPER)
    draw.ellipse([750, 394, 752, 396], fill=PAPER)
    draw.line([738, 401, 737, 409], fill=NOSE_L, width=2)
    draw.ellipse([729, 413, 747, 421], fill=ACCENT)
    draw.ellipse([733, 414, 736, 416], fill=PAPER)
    draw.ellipse([701, 402, 709, 410], outline=ACCENT, width=2)
    draw.ellipse([767, 402, 775, 410], outline=ACCENT, width=2)
    draw.arc([706, 424, 770, 452], start=15, end=165,
             fill=ACCENT, width=2)
    draw.ellipse([735, 442, 741, 448], fill=ACCENT)

    # ---- Vice City sun (small, between the two heads) ---------------
    draw.ellipse([796, 350, 828, 382], fill=ACCENT)

    # ---- Jason (right, centre x=898) ---------------------------------
    # short sandy-blonde hair: faded sides, textured top swept back,
    # NO cap so the blond hair shows
    draw.ellipse([862, 346, 934, 392], fill=BLONDE)
    # neck + black shirt with pink open collar
    draw.rectangle([889, 412, 907, 424], fill=SKIN_JASON)
    draw.polygon([(842, 446), (856, 426), (880, 416),
                  (916, 416), (940, 426), (954, 446)], fill=INK)
    draw.line([884, 418, 898, 432], fill=ACCENT, width=3)
    draw.line([912, 418, 898, 432], fill=ACCENT, width=3)
    # face with a squared jaw (strong jawline)
    draw.ellipse([868, 362, 928, 432], fill=SKIN_JASON)
    draw.polygon([(872, 408), (924, 408), (920, 432),
                  (876, 432)], fill=SKIN_JASON)
    # short fringe: hair only on top, then the face redrawn so the
    # forehead shows and the sides stay faded (skin)
    draw.ellipse([864, 346, 932, 376], fill=BLONDE)
    draw.ellipse([868, 370, 928, 432], fill=SKIN_JASON)
    draw.polygon([(872, 408), (924, 408), (920, 432),
                  (876, 432)], fill=SKIN_JASON)
    # swept-back texture strokes on top + short sideburns
    draw.arc([880, 348, 914, 368], start=200, end=340,
             fill=BLONDE_DARK, width=2)
    draw.line([884, 352, 906, 350], fill=BLONDE_DARK, width=2)
    draw.line([890, 356, 912, 354], fill=BLONDE_DARK, width=2)
    draw.rectangle([866, 378, 873, 400], fill=BLONDE)
    draw.rectangle([923, 378, 930, 400], fill=BLONDE)
    # heavy straight brows, VISIBLE deep-set eyes (no sunglasses
    # over them), nose
    draw.line([876, 390, 893, 392], fill=INK, width=4)
    draw.line([920, 390, 903, 392], fill=INK, width=4)
    draw.line([877, 394, 892, 394], fill=INK, width=2)
    draw.line([904, 394, 919, 394], fill=INK, width=2)
    draw.ellipse([880, 396, 887, 402], fill=INK)
    draw.ellipse([909, 396, 916, 402], fill=INK)
    draw.ellipse([882, 397, 884, 399], fill=PAPER)
    draw.ellipse([911, 397, 913, 399], fill=PAPER)
    draw.line([897, 402, 896, 411], fill=NOSE_J, width=2)
    # stubble: LIGHT shadow over the jaw/chin -- drawn on its own
    # layer with alpha so skin shows through (short stubble, NOT a
    # solid beard); the band starts below the nose (y=414), then the
    # mouth is redrawn on top of it
    stubble_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(stubble_layer)
    sd.pieslice([870, 392, 926, 436], start=0, end=180,
                fill=STUBBLE + (150,))
    sd.ellipse([878, 420, 881, 423], fill=STUBBLE + (150,))
    sd.ellipse([915, 420, 918, 423], fill=STUBBLE + (150,))
    img.alpha_composite(stubble_layer)
    draw = ImageDraw.Draw(img, "RGBA")
    draw.line([889, 419, 907, 419], fill=(120, 55, 55), width=3)


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
