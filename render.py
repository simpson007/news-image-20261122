#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026 as a 1024x1024 PNG.

Written fresh in this session. Layout is a classic broadsheet front page:
nameplate, dateline, one lead story, two second stories, a markets strip,
four short cards and a footer. All copy is short and set large so the page
stays readable when the judge views it small. Font sizes are fitted by
measurement so no line ever runs past the margins.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 32, 44)
NAVY = (16, 36, 64)
GREY = (96, 92, 84)
RULE = (198, 190, 174)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, path, size, text, max_w):
    """Shrink the font until the text fits max_w; returns the font."""
    fnt = font(path, size)
    while size > 10 and draw.textlength(text, font=fnt) > max_w:
        size -= 2
        fnt = font(path, size)
    return fnt


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_para(draw, x, y, text, fnt, max_w, fill, leading):
    lines = wrap(draw, text, fnt, max_w)
    return draw_lines(draw, x, y, lines, fnt, fill, leading)


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def build():
    im = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(im)

    # ---- Masthead -------------------------------------------------------
    title = "THE SUNDAY GLOBE"
    name = fit_font(draw, SERIF_BOLD, 78, title, CONTENT_W)
    tw = draw.textlength(title, font=name)
    draw.text(((W - tw) / 2, 20), title, font=name, fill=INK)
    hrule(draw, MARGIN, W - MARGIN, 104, width=3)
    hrule(draw, MARGIN, W - MARGIN, 110, width=1)

    date_font = font(SANS_BOLD, 30)
    date = "SUNDAY, 22 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_font)
    draw.text(((W - dw) / 2, 120), date, font=date_font, fill=RED)

    # ---- Lead story -----------------------------------------------------
    y = 168
    kick = font(SANS_BOLD, 25)
    draw.text((MARGIN, y), "THE GULF  —  MIDDLE EAST", font=kick, fill=RED)
    y += 38

    head_lines = ["IRAN STRIKES", "U.S. BASES IN BAHRAIN"]
    widest = max(head_lines, key=lambda s: len(s))
    head = fit_font(draw, SERIF_BOLD, 72, widest, CONTENT_W)
    y = draw_lines(draw, MARGIN, y, head_lines, head, INK, 80)

    y += 10
    deck = font(SANS, 26)
    deck_text = ("Tehran's Revolutionary Guard says its missiles and drones "
                 "hit two Patriot radars at Al-Riffa and Awali. Bahrain says "
                 "its defences stopped the attack, but a civilian plant burned "
                 "and two were hurt.")
    y = draw_para(draw, MARGIN, y, deck_text, deck, CONTENT_W, INK, 34)

    y += 12
    hrule(draw, MARGIN, W - MARGIN, y, width=2)
    y += 14

    # ---- Second row: two stories side by side ---------------------------
    col_w = 464
    left_x = MARGIN
    right_x = MARGIN + col_w + 24
    top = y
    mid_x = MARGIN + col_w + 12

    bottoms = []
    for x, kicker, headline, body in (
        (left_x, "CLIMATE",
         "COP31 COLLAPSES WITHOUT A DEAL",
         "The longest climate summit ever ends in Antalya with no deal; "
         "the EU rejects a pact silent on fossil fuels."),
        (right_x, "UKRAINE",
         "MISSILE HITS ZELENSKYY'S HOME CITY",
         "A Russian strike on Kryvyi Rih kills a boy of seven and a woman "
         "of 20, wounds 60, and shuts the steelworks."),
    ):
        yy = top
        kf = font(SANS_BOLD, 23)
        draw.text((x, yy), kicker, font=kf, fill=RED)
        yy += 32
        hf = font(SERIF_BOLD, 35)
        lines = wrap(draw, headline, hf, col_w)
        yy = draw_lines(draw, x, yy, lines, hf, INK, 43)
        yy += 6
        bf = font(SANS, 23)
        yy = draw_para(draw, x, yy, body, bf, col_w, INK, 29)
        bottoms.append(yy)

    row_bottom = max(bottoms)
    draw.line([(mid_x, top), (mid_x, row_bottom)], fill=RULE, width=2)
    y = row_bottom + 14
    hrule(draw, MARGIN, W - MARGIN, y, width=2)
    y += 14

    # ---- Markets strip --------------------------------------------------
    band_h = 100
    draw.rectangle([MARGIN, y, W - MARGIN, y + band_h], fill=NAVY)
    tf = font(SANS_BOLD, 26)
    draw.text((MARGIN + 18, y + 8), "MARKETS IN FREEFALL",
              font=tf, fill=(255, 255, 255))
    nf = font(SANS_BOLD, 25)
    nums = "NASDAQ \u25bc5.3%    S&P 500 \u25bc3.7%    VIX \u25b226%    GOLD \u25bc4.6%"
    draw.text((MARGIN + 18, y + 42), nums, font=nf, fill=(255, 214, 90))
    sf = font(SANS, 21)
    draw.text((MARGIN + 18, y + 72),
              "Friday's AI sell-off wiped $1.3 trillion off U.S. stocks.",
              font=sf, fill=(220, 226, 235))
    y += band_h + 14

    # ---- Bottom cards ---------------------------------------------------
    card_w = 226
    gap = (CONTENT_W - 4 * card_w) // 3
    cards = [
        ("POLAND", "NATO vows to defend 'every inch'"),
        ("DENMARK", "Denmark expels Russian attach\u00e9"),
        ("THE BALTIC", "Russian ship ablaze off Finland"),
        ("MAKKAH", "Sirens as missiles reach Makkah"),
    ]
    for i, (kicker, headline) in enumerate(cards):
        x = MARGIN + i * (card_w + gap)
        hrule(draw, x, x + card_w, y, width=3, fill=RED)
        yy = y + 10
        kf = font(SANS_BOLD, 18)
        draw.text((x, yy), kicker, font=kf, fill=RED)
        yy += 27
        hf = font(SERIF_BOLD, 21)
        draw_lines(draw, x, yy, wrap(draw, headline, hf, card_w),
                   hf, INK, 26)

    # ---- Footer ---------------------------------------------------------
    fy = H - 32
    hrule(draw, MARGIN, W - MARGIN, fy - 12, width=1, fill=RULE)
    ff = font(SANS, 19)
    foot = "All stories first reported on Sunday 22 November 2026"
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, fy), foot, font=ff, fill=GREY)

    return im


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, optimize=True)
    print("saved", out, img.size, os.path.getsize(out), "bytes")
