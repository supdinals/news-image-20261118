#!/usr/bin/env python3
"""Renderer for the news-image-20261118 entry.

Draws three 1024x1024 variants (A: tile grid, B: newspaper front page,
C: big lead + numbered list) with Pillow, using only the Liberation Sans
fonts bundled in build/fonts/ and icons drawn with code. Deterministic:
no randomness, no clock, no network.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "variants")
W = H = 1024

DATE_LINE = "WEDNESDAY 18 NOVEMBER 2026"
FOOTER = "Compiled from multiple news sources - see SOURCES.md"

LEAD = {
    "kicker": "CONFLICT - MIDDLE EAST",
    "color": (198, 48, 49),
    "headline": "U.S. STRIKES IRAN'S QESHM ISLAND - IRAN FIRES BACK AT BAHRAIN AND KUWAIT",
    "body": ("US jets hit a Guards missile site on Qeshm Island. Bahrain intercepts "
             "Iranian drones for the third time this week; Kuwait is hit for the "
             "first time since September. A Houthi missile aimed at Riyadh is destroyed."),
    "icon": "strait",
}

STORIES = [
    {
        "kicker": "DIPLOMACY - ASIA",
        "color": (37, 99, 178),
        "headline": "XI AND PUTIN MEET IN SHENZHEN AS APEC OPENS",
        "body": ("Xi calls for free trade and AI cooperation; both pledge stable ties. "
                 "A first Xi-Putin-Trump summit follows on Thursday."),
        "icon": "summit",
    },
    {
        "kicker": "HEALTH - AFRICA",
        "color": (22, 138, 90),
        "headline": "UN APPEALS FOR HELP AS EBOLA CASES DOUBLE IN DR CONGO",
        "body": ("Over 11,000 cases and 5,500 deaths in six months - the second-largest "
                 "Ebola outbreak on record. Africa CDC: still not under control."),
        "icon": "virus",
    },
    {
        "kicker": "POLITICS - AMERICAS",
        "color": (124, 77, 178),
        "headline": "PELTOLA WINS ALASKA - DEMOCRATS TAKE 56-44 SENATE MAJORITY",
        "body": ("The final Senate race is called: Mary Peltola beats Dan Sullivan and "
                 "becomes the first Alaska Native in the US Senate."),
        "icon": "ballot",
    },
    {
        "kicker": "SCIENCE - SPACE",
        "color": (14, 128, 150),
        "headline": "VOYAGER 1 REACHES ONE LIGHT-DAY FROM EARTH",
        "body": ("Launched in 1977, the probe is the first human-made object this far "
                 "out. Its radio signal now takes a full 24 hours to reach Earth."),
        "icon": "probe",
    },
    {
        "kicker": "WEATHER - SOUTH ASIA",
        "color": (214, 116, 22),
        "headline": "CYCLONE AKVAN STRENGTHENS INTO A SEVERE STORM",
        "body": ("Off India's Andhra Pradesh coast, with winds of 100-110 km/h. "
                 "Landfall is expected Friday between Nellore and Visakhapatnam."),
        "icon": "cyclone",
    },
]


def font(size, bold=False):
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.18, bold=False):
    """Draw wrapped text; returns the y just below the block."""
    x, y = xy
    step = int(fnt.size * leading)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def fit_lines(draw, text, size, max_w, max_lines, bold=True, min_size=20):
    """Shrink a headline font until the wrap fits max_lines; returns (font, lines)."""
    size_now = size
    while size_now > min_size:
        fnt = font(size_now, bold=bold)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size_now -= 2
    fnt = font(min_size, bold=bold)
    return fnt, wrap(draw, text, fnt, max_w)


# ---------------------------------------------------------------- icons
def icon_strait(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # starburst over the island (the strike)
    bx, by = cx + 6, cy - 44
    for k in range(8):
        a = math.radians(k * 45)
        sx, sy = bx + int(10 * math.cos(a)), by + int(10 * math.sin(a))
        ex, ey = bx + int(24 * math.cos(a)), by + int(24 * math.sin(a))
        d.line([sx, sy, ex, ey], fill=col, width=5)
    d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=col)
    # island: a low mound
    d.arc([cx - 62, cy - 6, cx + 62, cy + 58], 180, 360, fill=col, width=6)
    d.line([cx - 62, cy + 26, cx + 62, cy + 26], fill=col, width=6)
    # waves below
    for r in range(2):
        yy = cy + 48 + r * 17
        for sx in range(x0 + 10, x1 - 32, 48):
            d.arc([sx, yy - 8, sx + 30, yy + 8], 180, 360, fill=col, width=4)


def icon_summit(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 56, cy - 56, cx + 56, cy + 56], outline=col, width=6)
    d.ellipse([cx - 56, cy - 20, cx + 56, cy + 20], outline=col, width=3)
    d.line([cx - 56, cy, cx + 56, cy], fill=col, width=3)
    d.arc([cx - 28, cy - 56, cx + 28, cy + 56], 90, 270, fill=col, width=3)
    d.arc([cx - 28, cy - 56, cx + 28, cy + 56], 270, 90, fill=col, width=3)
    for px, py in [(cx - 34, cy - 30), (cx + 30, cy - 8), (cx, cy + 34)]:
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col)


def icon_virus(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 34
    for k in range(10):
        a = math.radians(k * 36)
        sx, sy = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        ex, ey = cx + int((r + 20) * math.cos(a)), cy + int((r + 20) * math.sin(a))
        d.line([sx, sy, ex, ey], fill=col, width=5)
        d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], outline=col, width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=6)
    for dx, dy in [(-14, -8), (12, 4), (-2, 16)]:
        d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5], fill=col)


def icon_ballot(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rounded_rectangle([cx - 52, cy - 6, cx + 52, cy + 52], 8, outline=col, width=6)
    d.rectangle([cx - 22, cy - 14, cx + 22, cy - 2], fill=col)
    d.rounded_rectangle([cx - 30, cy - 54, cx + 30, cy - 8], 6, outline=col, width=5)
    d.line([cx - 16, cy - 38, cx - 4, cy - 26, cx + 18, cy - 46], fill=col, width=6)


def icon_probe(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # dish
    d.arc([cx - 58, cy - 52, cx + 6, cy + 12], 300, 130, fill=col, width=7)
    d.line([cx - 26, cy - 20, cx + 34, cy + 26], fill=col, width=5)
    d.ellipse([cx + 28, cy + 20, cx + 42, cy + 34], fill=col)
    # boom + body
    d.line([cx - 20, cy - 14, cx + 52, cy - 44], fill=col, width=5)
    d.rectangle([cx + 44, cy - 56, cx + 60, cy - 34], outline=col, width=4)
    # signal arcs toward lower-left (Earth)
    for rr in (18, 32, 46):
        d.arc([cx - 62 - rr, cy + 26 - rr // 3, cx - 62 + rr, cy + 26 + rr], 300, 30, fill=col, width=4)
    d.ellipse([cx - 70, cy + 20, cx - 56, cy + 34], fill=col)


def icon_cyclone(d, box, col):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for k in range(3):
        start = k * 120
        d.arc([cx - 56, cy - 56, cx + 56, cy + 56], start, start + 95, fill=col, width=7)
        d.arc([cx - 34, cy - 34, cx + 34, cy + 34], start + 60, start + 170, fill=col, width=6)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=col, width=5)


ICONS = {
    "strait": icon_strait,
    "summit": icon_summit,
    "virus": icon_virus,
    "ballot": icon_ballot,
    "probe": icon_probe,
    "cyclone": icon_cyclone,
}


def draw_icon(d, name, box, col):
    ICONS[name](d, box, col)


# ---------------------------------------------------------------- variant A
def variant_a():
    """Tile grid: lead tile, 2x2 supporting tiles, wide fifth tile."""
    img = Image.new("RGB", (W, H), (16, 22, 34))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 92], fill=(232, 236, 240))
    d.text((36, 14), "WORLD NEWS", font=font(44, True), fill=(16, 22, 34))
    tw = d.textlength(DATE_LINE, font=font(30, True))
    d.text((W - 36 - tw, 24), DATE_LINE, font=font(30, True), fill=(198, 48, 49))
    # lead tile
    d.rounded_rectangle([28, 108, 996, 428], 14, fill=(28, 38, 54))
    d.rectangle([28, 108, 42, 428], fill=LEAD["color"])
    d.text((66, 124), LEAD["kicker"], font=font(24, True), fill=(240, 140, 140))
    hf, hlines = fit_lines(d, LEAD["headline"], 50, 690, 3)
    y = 158
    for ln in hlines:
        d.text((66, y), ln, font=hf, fill=(245, 247, 250))
        y += int(hf.size * 1.12)
    text_block(d, (66, y + 6), LEAD["body"], font(22), (205, 214, 226), 680, leading=1.16)
    draw_icon(d, LEAD["icon"], (748, 176, 958, 340), (240, 180, 90))
    # 2x2 tiles
    tiles = [(28, 444, 502, 664), (522, 444, 996, 664),
             (28, 680, 502, 900), (522, 680, 996, 900)]
    for story, (tx0, ty0, tx1, ty1) in zip(STORIES[:4], tiles):
        d.rounded_rectangle([tx0, ty0, tx1, ty1], 12, fill=(28, 38, 54))
        d.rectangle([tx0, ty0, tx1, ty0 + 8], fill=story["color"])
        d.text((tx0 + 22, ty0 + 18), story["kicker"], font=font(20, True), fill=(170, 200, 240))
        hf, hlines = fit_lines(d, story["headline"], 30, tx1 - tx0 - 44, 3, min_size=23)
        y = ty0 + 48
        for ln in hlines:
            d.text((tx0 + 22, y), ln, font=hf, fill=(245, 247, 250))
            y += int(hf.size * 1.12)
        text_block(d, (tx0 + 22, y + 4), story["body"], font(20), (205, 214, 226),
                   tx1 - tx0 - 44, leading=1.12)
    # fifth story, wide bottom tile
    s5 = STORIES[4]
    d.rounded_rectangle([28, 916, 996, 982], 12, fill=(28, 38, 54))
    d.rectangle([28, 916, 40, 982], fill=s5["color"])
    d.text((62, 926), s5["kicker"] + "  -  " + s5["headline"], font=font(22, True),
           fill=(245, 247, 250))
    d.text((62, 954), "Off India's Andhra Pradesh coast, winds 100-110 km/h; landfall expected Friday.",
           font=font(20), fill=(205, 214, 226))
    d.text((36, 990), FOOTER, font=font(18), fill=(140, 152, 168))
    return img


# ---------------------------------------------------------------- variant C
SHORT_BODIES = [
    "Xi urges free trade and AI cooperation; a Trump summit follows Thursday.",
    "Over 11,000 cases, 5,500 deaths in six months - second-largest on record.",
    "The final Senate race is called; first Alaska Native in the US Senate.",
    "Launched in 1977, the first object this far out; signal takes 24 hours.",
    "Off Andhra Pradesh at 100-110 km/h; landfall Friday, Nellore-Visakhapatnam.",
]


def variant_c():
    """Big lead plus a numbered list of the five supporting stories."""
    img = Image.new("RGB", (W, H), (15, 20, 32))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 96], fill=(198, 48, 49))
    d.text((36, 14), "WORLD NEWS", font=font(42, True), fill=(255, 255, 255))
    tw = d.textlength(DATE_LINE, font=font(31, True))
    d.text((W - 36 - tw, 30), DATE_LINE, font=font(31, True), fill=(255, 255, 255))
    # lead
    d.text((36, 110), LEAD["kicker"], font=font(24, True), fill=(240, 140, 140))
    hf, hlines = fit_lines(d, LEAD["headline"], 50, 952, 3)
    y = 142
    for ln in hlines:
        d.text((36, y), ln, font=hf, fill=(248, 249, 251))
        y += int(hf.size * 1.1)
    yb = text_block(d, (36, y + 6), LEAD["body"], font(22), (208, 216, 228), 790, leading=1.14)
    draw_icon(d, LEAD["icon"], (838, y - 6, 978, y + 84), (240, 180, 90))
    y = max(yb, y + 104)
    d.line([36, y + 12, 988, y + 12], fill=(70, 84, 106), width=3)
    # numbered list
    yy = y + 28
    for i, story in enumerate(STORIES, start=1):
        d.ellipse([36, yy + 2, 92, yy + 58], fill=story["color"])
        num = str(i)
        nw = d.textlength(num, font=font(34, True))
        d.text((64 - nw / 2, yy + 10), num, font=font(34, True), fill=(255, 255, 255))
        d.text((112, yy), story["kicker"], font=font(20, True), fill=(170, 200, 240))
        hf, hlines = fit_lines(d, story["headline"], 29, 876, 2, min_size=24)
        hy = yy + 25
        for ln in hlines:
            d.text((112, hy), ln, font=hf, fill=(248, 249, 251))
            hy += int(hf.size * 1.05)
        by = text_block(d, (112, hy + 2), SHORT_BODIES[i - 1], font(20),
                        (208, 216, 228), 876, leading=1.1)
        yy = by + 10
        if i < len(STORIES):
            d.line([112, yy - 5, 988, yy - 5], fill=(46, 58, 78), width=2)
    d.text((36, 988), FOOTER, font=font(18), fill=(140, 152, 168))
    return img


# ---------------------------------------------------------------- variant B
def variant_b():
    """Newspaper front page: masthead, lead, two compact columns, weather strip."""
    img = Image.new("RGB", (W, H), (246, 242, 233))
    d = ImageDraw.Draw(img)
    ink = (24, 24, 28)
    grey = (92, 92, 98)
    d.text((36, 18), "THE WORLD TODAY", font=font(56, True), fill=ink)
    d.line([36, 94, 988, 94], fill=ink, width=5)
    tw = d.textlength(DATE_LINE, font=font(30, True))
    d.text(((W - tw) / 2, 106), DATE_LINE, font=font(30, True), fill=(168, 32, 36))
    d.line([36, 150, 988, 150], fill=ink, width=2)
    # lead
    d.text((36, 164), LEAD["kicker"], font=font(22, True), fill=LEAD["color"])
    hf, hlines = fit_lines(d, LEAD["headline"], 50, 952, 3)
    y = 194
    for ln in hlines:
        d.text((36, y), ln, font=hf, fill=ink)
        y += int(hf.size * 1.08)
    yb = text_block(d, (36, y + 4), LEAD["body"], font(22), (52, 52, 58), 740, leading=1.14)
    draw_icon(d, LEAD["icon"], (800, yb - 134, 962, yb - 2), LEAD["color"])
    y = yb + 10
    d.line([36, y, 988, y], fill=ink, width=3)
    # two columns, two stories each, short bodies
    top = y + 20
    col_x = [36, 522]
    col_w = 450
    col_y = {0: top, 1: top}
    for idx, story in enumerate(STORIES[:4]):
        c = idx % 2
        x, yy = col_x[c], col_y[c]
        d.text((x, yy), story["kicker"], font=font(19, True), fill=story["color"])
        hf, hlines = fit_lines(d, story["headline"], 27, col_w, 3, min_size=22)
        yy += 25
        for ln in hlines:
            d.text((x, yy), ln, font=hf, fill=ink)
            yy += int(hf.size * 1.06)
        yy = text_block(d, (x, yy + 3), SHORT_BODIES[idx], font(19), (52, 52, 58),
                        col_w, leading=1.12)
        col_y[c] = yy + 14
    y = max(col_y.values()) + 0
    d.line([36, y, 988, y], fill=ink, width=2)
    # fifth story as a wide strip
    s5 = STORIES[4]
    d.text((36, y + 10), s5["kicker"], font=font(19, True), fill=s5["color"])
    d.text((36, y + 36), s5["headline"], font=font(27, True), fill=ink)
    d.text((36, y + 70), "Off India's Andhra Pradesh coast, with winds of 100-110 km/h. Landfall is expected Friday",
           font=font(19), fill=(52, 52, 58))
    d.text((36, y + 94), "between Nellore and Visakhapatnam.", font=font(19), fill=(52, 52, 58))
    d.line([36, 968, 988, 968], fill=ink, width=2)
    d.text((36, 978), FOOTER, font=font(18), fill=grey)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [("A", variant_a), ("B", variant_b), ("C", variant_c)]
    for name, fn in jobs:
        img = fn()
        path = os.path.join(OUT, "variant_%s.png" % name)
        img.save(path, optimize=True)
        small = img.resize((512, 512), Image.LANCZOS)
        small.save(os.path.join(OUT, "variant_%s_512.png" % name), optimize=True)
        print(name, os.path.getsize(path))


if __name__ == "__main__":
    main()
