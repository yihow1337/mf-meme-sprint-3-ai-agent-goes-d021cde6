#!/usr/bin/env python3
"""Renderer for the "AI Agent Goes Rogue" meme.

Draws everything from shapes and text with Pillow (no downloaded images).
Concept: a chat with an autonomous AI agent. The human asks for "inbox zero";
the agent cheerfully reports it got there by DELETING ALL 9,412 EMAILS,
confetti and all. Over-literal goal pursuit = rogue.

Output: entry.png (1024x1024, PNG) in this directory.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/sand-box/google"
ANTON = f"{FONT_DIR}/Anton/Anton-Regular.ttf"
INTER = f"{FONT_DIR}/Inter/Inter-VariableFont_opsz,wght.ttf"

# palette
BG = (15, 18, 24)
BG2 = (22, 26, 34)
HEADER = (24, 28, 37)
USER_BUBBLE = (46, 54, 68)
USER_TEXT = (205, 212, 224)
AGENT_BUBBLE = (27, 33, 44)
AGENT_BORDER = (44, 54, 70)
WHITE = (243, 246, 250)
GREEN = (44, 201, 110)
MUTED = (120, 132, 150)
RED = (235, 74, 74)
CONFETTI = [(255, 196, 61), (89, 173, 255), (255, 107, 158),
            (44, 201, 110), (178, 120, 255), (255, 138, 76)]


def inter(size, weight=400):
    f = ImageFont.truetype(INTER, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def anton(size):
    return ImageFont.truetype(ANTON, size)


def rounded(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def wrap(d, words, f, maxw):
    lines, cur = [], ""
    for wd in words.split(" "):
        t = (cur + " " + wd).strip()
        if text_w(d, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # subtle vertical gradient background
    for y in range(H):
        t = y / H
        c = tuple(int(BG[i] + (BG2[i] - BG[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    # ---- header bar ----
    hh = 132
    d.rectangle([0, 0, W, hh], fill=HEADER)
    d.line([(0, hh), (W, hh)], fill=(40, 48, 62), width=2)
    # agent avatar: rounded square with a simple bot glyph
    rounded(d, [40, 34, 104, 98], 16, fill=(37, 46, 62))
    # bot face
    d.rounded_rectangle([54, 50, 90, 82], radius=7, outline=(150, 200, 255), width=3)
    d.ellipse([62, 60, 70, 68], fill=(150, 200, 255))
    d.ellipse([74, 60, 82, 68], fill=(150, 200, 255))
    d.line([(72, 44), (72, 50)], fill=(150, 200, 255), width=3)
    d.ellipse([70, 40, 74, 44], fill=(150, 200, 255))
    # name + status
    d.text((124, 40), "Autopilot Agent", font=inter(34, 700), fill=WHITE)
    d.ellipse([126, 86, 142, 102], fill=GREEN)
    d.text((152, 82), "running autonomously", font=inter(25, 500), fill=MUTED)

    # ---- user message (right aligned) ----
    uf = inter(40, 600)
    umsg = "get me to inbox zero"
    uw = text_w(d, umsg, uf)
    pad = 34
    bw = uw + pad * 2
    bx1 = W - 48 - bw
    by1 = hh + 54
    bh = 92
    rounded(d, [bx1, by1, bx1 + bw, by1 + bh], 28, fill=USER_BUBBLE)
    # tail
    d.polygon([(bx1 + bw - 18, by1 + bh - 6),
               (W - 30, by1 + bh + 14),
               (bx1 + bw - 2, by1 + bh - 30)], fill=USER_BUBBLE)
    d.text((bx1 + pad, by1 + bh / 2), umsg, font=uf, fill=USER_TEXT, anchor="lm")
    d.text((bx1 + bw, by1 - 8), "you", font=inter(23, 500), fill=MUTED, anchor="rb")

    # ---- agent message (left, the big one) ----
    ay1 = by1 + bh + 72
    ay2 = 958
    amx = 48
    amw = W - 48 - amx
    rounded(d, [amx, ay1, amx + amw, ay2], 30,
            fill=AGENT_BUBBLE, outline=AGENT_BORDER, width=2)

    inx = amx + 42

    # badge + header row
    hdr_y = ay1 + 78
    br = 32
    bcx, bcy = inx + br, hdr_y
    d.ellipse([bcx - br, bcy - br, bcx + br, bcy + br], fill=GREEN)
    d.line([(bcx - 14, bcy + 1), (bcx - 4, bcy + 12), (bcx + 16, bcy - 12)],
           fill=(12, 20, 14), width=7, joint="curve")
    d.text((inx + br * 2 + 22, bcy), "Done! Task complete",
           font=inter(38, 700), fill=GREEN, anchor="lm")

    # the punchline — huge
    big = anton(108)
    py0 = hdr_y + br + 54
    cy = py0
    for ln in ["DELETED ALL", "9,412 EMAILS"]:
        d.text((inx, cy), ln, font=big, fill=WHITE)
        cy += 116
    punch_bottom = cy

    # sub line (the smug kicker)
    cy += 24
    sub = inter(39, 500)
    sub_top = cy
    for ln in wrap(d, "You're officially at inbox zero. You're welcome!",
                   sub, amw - 84):
        d.text((inx, cy), ln, font=sub, fill=(196, 205, 220))
        cy += 50

    # smug irreversible kicker
    cy += 8
    small = inter(30, 500)
    d.text((inx, cy), "Undo is no longer available.", font=small, fill=RED)
    cy += 44
    sub_bottom = cy

    # confetti behind/around text: top band and bottom band only
    import random
    rnd = random.Random(7)
    placed = 0
    while placed < 54:
        px = rnd.randint(amx + 22, amx + amw - 28)
        band_top = rnd.random() < 0.45
        if band_top:
            py = rnd.randint(ay1 + 20, hdr_y - br - 8)
        else:
            py = rnd.randint(sub_bottom + 6, ay2 - 22)
        s = rnd.randint(7, 15)
        col = rnd.choice(CONFETTI)
        if rnd.random() < 0.5:
            d.rectangle([px, py, px + s, py + s], fill=col)
        else:
            d.ellipse([px, py, px + s, py + s], fill=col)
        placed += 1

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    draw()
