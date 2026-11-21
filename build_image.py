#!/usr/bin/env python3
"""Draw an invented passport spread: Republic of Velloria.

Self-contained: reads nothing but the text below, uses only the
standard library plus Pillow, touches no network, no clock and no
randomness, so running it twice produces identical bytes. Writes
entry.png next to this file (or to the path in --out).

The country, the holder and every place and date are invented or,
for the travel stamps, real cities visited on dates that are
mutually consistent: issued 02 JUN 2025, expiry 01 JUN 2035,
Lisbon in 12 SEP 2025, out 19 SEP 2025, Athens in 28 SEP 2025
(inside the Greek visa, 20 SEP - 20 DEC 2025, issued in Lisbon
10 SEP 2025), Istanbul in 09 OCT 2025, out 16 OCT 2025.
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024

NAVY = (22, 38, 64)
NAVY_DARK = (14, 26, 46)
GOLD = (176, 141, 58)
CREAM = (247, 241, 222)
CREAM_DARK = (238, 231, 207)
INK = (24, 28, 36)
MUTED = (105, 98, 84)
TEAL = (38, 90, 96)
GREEN = (46, 92, 58)
STICKER = (220, 234, 217)
MRZ_BG = (233, 228, 210)
BLUE = (30, 70, 140)
BURGUNDY = (140, 40, 50)

LIB = "/usr/share/fonts/truetype/liberation"


def load(name, size):
    return ImageFont.truetype(os.path.join(LIB, name), size)


SERIF_B = "LiberationSerif-Bold.ttf"
SERIF_R = "LiberationSerif-Regular.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS_R = "LiberationSans-Regular.ttf"
MONO_R = "LiberationMono-Regular.ttf"

F_COUNTRY = load(SANS_B, 16)
F_PASSPORT = load(SERIF_B, 32)
F_SUB = load(SERIF_I, 13)
F_PAGE_LBL = load(SANS_B, 12)
F_LABEL = load(SANS_B, 10)
F_VALUE = load(SERIF_B, 15)
F_VALUE_SM = load(SERIF_B, 13)
F_BODY = load(SERIF_R, 14)
F_BODY_SM = load(SERIF_R, 12)
F_ITAL = load(SERIF_I, 13)
F_SIG = load(SERIF_I, 26)
F_MRZ = load(MONO_R, 14)
F_VISAS = load(SERIF_B, 30)
F_STICK_HEAD = load(SANS_B, 15)
F_STAMP_CITY = load(SANS_B, 15)
F_STAMP = load(SANS_B, 12)
F_STAMP_SM = load(SANS_B, 10)
F_FOOT = load(SANS_R, 11)


def fit_lines(draw, text, face, width):
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for word in words[1:]:
            test = line + " " + word
            if draw.textlength(test, font=face) <= width:
                line = test
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def para(draw, x, y, width, text, face, step, colour=INK):
    for line in fit_lines(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=colour)
        y += step
    return y


def centre(draw, cx, y, text, face, colour=INK):
    w = draw.textlength(text, font=face)
    draw.text((cx - w / 2, y), text, font=face, fill=colour)
    return y


def field(draw, x, y, label, value, face=F_VALUE):
    draw.text((x, y), label, font=F_LABEL, fill=MUTED)
    draw.text((x, y + 12), value, font=face, fill=INK)
    return y + 27


# ------------------------------------------------------------------- MRZ
# ICAO 9303 check digits, so the two machine-readable lines are
# well-formed, not just plausible-looking.

def _mrz_value(ch):
    if ch == "<":
        return 0
    if ch.isdigit():
        return int(ch)
    return ord(ch) - 55  # A=10 ... Z=35


def _mrz_check(text):
    total = 0
    for i, ch in enumerate(text):
        total += _mrz_value(ch) * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<VLRILSEN<<MARA<ELENA".ljust(44, "<")
    doc = "VL4829176"
    nat = "VLR"
    dob = "880314"      # 14 MAR 1988
    sex = "F"
    exp = "350601"      # 01 JUN 2035
    personal = "<" * 15  # 9+1+3+6+1+1+6+1+15+1 = 44 chars per line
    body = (doc + _mrz_check(doc) + nat + dob + _mrz_check(dob)
            + sex + exp + _mrz_check(exp) + personal)
    line2 = body + _mrz_check(body)
    assert len(line1) == 44 and len(line2) == 44, (line1, line2)
    return line1, line2


# ------------------------------------------------------------------- art

def draw_arms(d, cx, top, w=64, h=74):
    """Coat of arms: navy shield, gold lighthouse, teal waves, star."""
    x0, x1 = cx - w // 2, cx + w // 2
    y0, y1 = top, top + h
    # shield
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + h - 22),
               (cx, y1), (x0, y0 + h - 22)], fill=NAVY, outline=GOLD)
    d.polygon([(x0 + 3, y0 + 3), (x1 - 3, y0 + 3),
               (x1 - 3, y0 + h - 23), (cx, y1 - 4), (x0 + 3, y0 + h - 23)],
              outline=GOLD)
    # star above the lighthouse
    sx, sy = cx, y0 + 12
    d.polygon([(sx, sy - 6), (sx + 2, sy - 1), (sx + 6, sy),
               (sx + 2, sy + 2), (sx + 1, sy + 6), (sx, sy + 2),
               (sx - 1, sy + 6), (sx - 2, sy + 2), (sx - 6, sy),
               (sx - 2, sy - 1)], fill=GOLD)
    # lighthouse tower
    d.polygon([(cx - 6, y0 + 44), (cx - 4, y0 + 18),
               (cx + 4, y0 + 18), (cx + 6, y0 + 44)], fill=(247, 241, 222))
    d.rectangle([cx - 7, y0 + 14, cx + 7, y0 + 19], fill=GOLD)
    d.polygon([(cx - 8, y0 + 14), (cx, y0 + 7), (cx + 8, y0 + 14)],
              fill=GOLD)
    # light beams
    d.polygon([(cx - 8, y0 + 16), (x0 + 6, y0 + 10),
               (x0 + 6, y0 + 16)], fill=GOLD)
    d.polygon([(cx + 8, y0 + 16), (x1 - 6, y0 + 10),
               (x1 - 6, y0 + 16)], fill=GOLD)
    # waves
    for yy, xx in ((y0 + 50, x0 + 6), (y0 + 56, x0 + 12)):
        d.arc([xx, yy, xx + 18, yy + 10], 180, 360, fill=TEAL, width=2)
        d.arc([xx + 20, yy, xx + 38, yy + 10], 180, 360,
              fill=TEAL, width=2)


def draw_portrait(d, x0, y0, x1, y1):
    """Stylised portrait of Mara Ilsen, lighthouse keeper.

    Drawn, not photographed: flat illustration of a woman with her
    hair in a bun, in a navy keeper's uniform with gold epaulettes.
    """
    # sky / sea backdrop
    d.rectangle([x0, y0, x1, y0 + (y1 - y0) // 2], fill=(185, 205, 210))
    d.rectangle([x0, y0 + (y1 - y0) // 2, x1, y1], fill=(232, 226, 204))
    # faint lighthouse on the horizon, behind her shoulder
    lx = x1 - 26
    d.polygon([(lx - 4, y0 + 62), (lx - 2, y0 + 34),
               (lx + 2, y0 + 34), (lx + 4, y0 + 62)], fill=(120, 130, 128))
    d.rectangle([lx - 5, y0 + 30, lx + 5, y0 + 35], fill=(120, 130, 128))
    # sun
    d.ellipse([x0 + 12, y0 + 12, x0 + 34, y0 + 34], fill=(244, 230, 180))
    # shoulders / uniform
    cx = (x0 + x1) // 2
    d.polygon([(x0, y1), (x1, y1), (x1, y1 - 38), (cx + 34, y1 - 66),
               (cx - 34, y1 - 66), (x0, y1 - 38)], fill=(29, 53, 87))
    # white collar
    d.polygon([(cx - 16, y1 - 62), (cx, y1 - 44), (cx + 16, y1 - 62),
               (cx, y1 - 70)], fill=(247, 241, 222))
    # gold epaulettes + buttons
    d.rectangle([x0 + 6, y1 - 52, x0 + 34, y1 - 46], fill=GOLD)
    d.rectangle([x1 - 34, y1 - 52, x1 - 6, y1 - 46], fill=GOLD)
    for by in (y1 - 26, y1 - 12):
        d.ellipse([cx - 3, by, cx + 3, by + 6], fill=GOLD)
    # lighthouse pin on the chest
    d.polygon([(cx + 22, y1 - 30), (cx + 20, y1 - 42),
               (cx + 24, y1 - 42)], fill=GOLD)
    # neck + face
    d.rectangle([cx - 9, y1 - 78, cx + 9, y1 - 60], fill=(230, 180, 140))
    d.ellipse([cx - 27, y0 + 22, cx + 27, y0 + 82], fill=(230, 180, 140))
    # hair: dark, swept back, bun on top
    d.pieslice([cx - 27, y0 + 22, cx + 27, y0 + 82], 180, 360,
               fill=(74, 47, 34))
    d.ellipse([cx - 11, y0 + 8, cx + 11, y0 + 30], fill=(74, 47, 34))
    d.ellipse([cx - 30, y0 + 34, cx - 18, y0 + 66], fill=(74, 47, 34))
    d.ellipse([cx + 18, y0 + 34, cx + 30, y0 + 66], fill=(74, 47, 34))
    # eyes, brows, nose, smile
    for ex in (cx - 12, cx + 12):
        d.ellipse([ex - 3, y0 + 54, ex + 3, y0 + 60], fill=INK)
        d.line([(ex - 6, y0 + 48), (ex + 6, y0 + 48)], fill=(74, 47, 34),
               width=2)
    d.line([(cx, y0 + 58), (cx - 2, y0 + 68)], fill=(180, 130, 100),
           width=2)
    d.arc([cx - 8, y0 + 66, cx + 8, y0 + 80], 20, 160, fill=(150, 80, 70),
          width=2)


def draw_flag(d, x0, y0, w=118, h=76):
    """Flag of Velloria: navy / teal / white bands, gold lighthouse."""
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=NAVY, width=2)
    d.rectangle([x0, y0, x0 + w, y0 + h // 3], fill=NAVY)
    d.rectangle([x0, y0 + h // 3, x0 + w, y0 + 2 * h // 3], fill=TEAL)
    d.rectangle([x0, y0 + 2 * h // 3, x0 + w, y0 + h],
                fill=(247, 241, 222))
    cx = x0 + w // 2
    d.polygon([(cx - 5, y0 + h - 8), (cx - 3, y0 + 12),
               (cx + 3, y0 + 12), (cx + 5, y0 + h - 8)],
              fill=(247, 241, 222))
    d.rectangle([cx - 6, y0 + 8, cx + 6, y0 + 13], fill=GOLD)
    d.ellipse([cx - 4, y0 + 2, cx + 4, y0 + 10], fill=GOLD)


def draw_stamp(d, cx, cy, r, city, kind, date, colour):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=3)
    d.ellipse([cx - r + 7, cy - r + 7, cx + r - 7, cy + r - 7],
              outline=colour, width=1)
    centre(d, cx, cy - 34, city, F_STAMP_CITY, colour)
    centre(d, cx, cy - 8, kind, F_STAMP, colour)
    d.line([(cx - 34, cy + 12), (cx + 34, cy + 12)], fill=colour, width=1)
    centre(d, cx, cy + 18, date, F_STAMP_SM, colour)
    d.text((cx - 3, cy - 46), "*", font=F_STAMP, fill=colour)


# ------------------------------------------------------------------- page

def render():
    img = Image.new("RGB", (PAGE_W, PAGE_H), NAVY_DARK)
    d = ImageDraw.Draw(img)
    # gold frame around the whole spread
    d.rectangle([10, 10, PAGE_W - 11, PAGE_H - 11], outline=GOLD, width=2)

    for (px0, py0, px1, py1) in ((36, 36, 498, 988), (526, 36, 988, 988)):
        d.rectangle([px0, py0, px1, py1], fill=CREAM)
        # faint guilloche diagonals
        for gx in range(px0, px1, 18):
            d.line([(gx, py1), (gx + 90, py0)], fill=(233, 228, 210),
                   width=1)
        d.rectangle([px0 + 5, py0 + 5, px1 - 5, py1 - 5], outline=GOLD,
                    width=1)
    # centre gutter shadow
    d.rectangle([498, 36, 526, 988], fill=(30, 30, 34))
    d.line([(512, 36), (512, 988)], fill=(70, 60, 40), width=2)

    # ================================================= left: data page ==
    LX0, LX1 = 52, 482
    LCX = (LX0 + LX1) // 2
    centre(d, LCX, 52, "REPUBLIC OF VELLORIA", F_COUNTRY, NAVY)
    draw_arms(d, LCX, 76)
    centre(d, LCX, 156, "PASSPORT", F_PASSPORT, INK)
    centre(d, LCX, 194, "PASSEPORT  ·  PASAPORTA", F_SUB, MUTED)
    d.line([(LX0, 216), (LX1, 216)], fill=INK, width=2)
    d.text((LX0, 226), "DATA PAGE — PAGE 2", font=F_PAGE_LBL, fill=NAVY)
    no = "No. VL 4829176"
    d.text((LX1 - d.textlength(no, font=F_PAGE_LBL), 226), no,
           font=F_PAGE_LBL, fill=NAVY)

    # portrait
    d.rectangle([52, 248, 196, 408], outline=NAVY, width=2)
    draw_portrait(d, 54, 250, 194, 406)
    d.text((52, 412), "PHOTO — PORTRAIT OF HOLDER",
           font=F_STAMP_SM, fill=MUTED)

    # data fields beside the portrait
    fx, fy = 212, 248
    fy = field(d, fx, fy, "SURNAME", "ILSEN")
    fy = field(d, fx, fy, "GIVEN NAMES", "MARA ELENA")
    fy = field(d, fx, fy, "NATIONALITY", "VELLORIAN")
    fy = field(d, fx, fy, "DATE OF BIRTH", "14 MAR 1988")
    fy = field(d, fx, fy, "PLACE OF BIRTH", "PORT LIORA")
    fy = field(d, fx, fy, "SEX", "F")

    d.line([(LX0, 436), (LX1, 436)], fill=INK, width=1)
    y = 448
    y = field(d, LX0, y, "DATE OF ISSUE", "02 JUN 2025")
    y = field(d, 277, 448, "DATE OF EXPIRY", "01 JUN 2035")
    y = 505
    y = field(d, LX0, y, "AUTHORITY", "PORT LIORA", F_VALUE_SM)
    d.text((LX0, y + 12), "PASSPORT OFFICE", font=F_VALUE_SM, fill=INK)
    y = field(d, 277, 505, "OCCUPATION", "LIGHTHOUSE KEEPER", F_VALUE_SM)

    # signature
    d.line([(LX0, 580), (LX1, 580)], fill=INK, width=1)
    d.text((LX0, 590), "HOLDER'S SIGNATURE", font=F_LABEL, fill=MUTED)
    d.text((LX0 + 8, 606), "Mara Elena Ilsen", font=F_SIG, fill=(40, 50, 90))
    d.line([(LX0, 648), (LX1, 648)], fill=INK, width=1)

    # language note
    y = para(d, LX0, 662, LX1 - LX0,
             "Issued in Vellorian, English and French. This passport "
             "remains the property of the Republic of Velloria and must "
             "be returned on demand.", F_ITAL, 17, MUTED)

    # flag + observation
    d.line([(LX0, 724), (LX1, 724)], fill=INK, width=1)
    draw_flag(d, LX0, 740)
    d.text((LX0, 822), "FLAG OF VELLORIA — ADOPTED 1962",
           font=F_STAMP_SM, fill=MUTED)
    tx = 190
    d.text((tx, 740), "OBSERVATION", font=F_LABEL, fill=MUTED)
    para(d, tx, 754, LX1 - tx,
         "Holder is a lighthouse keeper — see Condition 4 on the visa "
         "page. Born at Port Liora General Hospital, Meridian Quay.",
         F_BODY_SM, 16)

    # MRZ
    d.rectangle([LX0, 872, LX1, 946], fill=MRZ_BG)
    line1, line2 = mrz_lines()
    d.text((LX0 + 8, 882), line1, font=F_MRZ, fill=INK)
    d.text((LX0 + 8, 908), line2, font=F_MRZ, fill=INK)
    d.text((LX1 - 10, 958), "2", font=F_FOOT, fill=MUTED)

    # ================================================ right: visa page ==
    RX0, RX1 = 542, 972
    RCX = (RX0 + RX1) // 2
    centre(d, RCX, 52, "VISAS", F_VISAS, INK)
    centre(d, RCX, 90, "VISAS  ·  VISTOS", F_SUB, MUTED)
    d.line([(RX0, 112), (RX1, 112)], fill=INK, width=2)

    # visa sticker — Hellenic Republic
    d.rectangle([RX0, 124, RX1, 302], fill=STICKER, outline=GREEN, width=2)
    d.rectangle([RX0, 124, RX1, 152], fill=GREEN)
    centre(d, RCX, 130, "VISA — HELLENIC REPUBLIC", F_STICK_HEAD,
           (247, 241, 222))
    vy = 162
    vy = field(d, RX0 + 14, vy, "TYPE", "C — MULTIPLE ENTRY")
    vy = field(d, RX0 + 224, 162, "VALID", "20 SEP – 20 DEC 2025",
               F_VALUE_SM)
    vy = field(d, RX0 + 14, 202, "DURATION OF STAY", "90 DAYS")
    vy = field(d, RX0 + 224, 202, "ISSUED", "LISBON, 10 SEP 2025",
               F_VALUE_SM)
    vy = field(d, RX0 + 14, 242, "PURPOSE", "LIGHTHOUSE CONF.", F_VALUE_SM)
    vy = field(d, RX0 + 224, 242, "VISA No.", "GR-884120")
    d.text((RX0 + 14, 282), "FEE PAID — €80  ·  GR-884120",
           font=F_STAMP_SM, fill=GREEN)

    # entry stamps, chronological left to right
    draw_stamp(d, 613, 388, 64, "LISBON", "ENTRY", "12 SEP 2025", BLUE)
    draw_stamp(d, 757, 388, 64, "ATHENS", "ENTRY", "28 SEP 2025", TEAL)
    draw_stamp(d, 901, 388, 64, "ISTANBUL", "ENTRY", "09 OCT 2025",
               BURGUNDY)
    # rectangular exit stamps underneath
    d.rectangle([RX0, 470, RX0 + 196, 508], outline=BLUE, width=2)
    centre(d, RX0 + 98, 478, "DEPARTED LISBON", F_STAMP_SM, BLUE)
    centre(d, RX0 + 98, 492, "19 SEP 2025", F_STAMP_SM, BLUE)
    d.rectangle([RX1 - 196, 470, RX1, 508], outline=BURGUNDY, width=2)
    centre(d, RX1 - 98, 478, "DEPARTED ISTANBUL", F_STAMP_SM, BURGUNDY)
    centre(d, RX1 - 98, 492, "16 OCT 2025", F_STAMP_SM, BURGUNDY)

    # Condition 4 — the storytelling detail
    d.line([(RX0, 530), (RX1, 530)], fill=INK, width=1)
    d.text((RX0, 542), "CONDITION 4 — LIGHTHOUSE SERVICE",
           font=F_PAGE_LBL, fill=NAVY)
    y = para(d, RX0, 564, RX1 - RX0,
             "The holder is a lighthouse keeper of the Republic of "
             "Velloria and may embark at any Vellorian port without a "
             "separate crew visa. This condition was entered at issue "
             "and travels with the passport.", F_BODY, 18)
    d.text((RX0, y + 4), "— A. SOREN, Passport Officer, Port Liora, "
                         "02 JUN 2025", font=F_ITAL, fill=MUTED)

    # voyage route — Port Liora to Lisbon to Athens to Istanbul
    d.line([(RX0, 688), (RX1, 688)], fill=INK, width=1)
    d.text((RX0, 700), "VOYAGE 2025", font=F_LABEL, fill=MUTED)
    pts = [(RX0 + 30, 800), (RX0 + 150, 748), (RX0 + 280, 792),
           (RX0 + 400, 744)]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        steps = 14
        for s in range(steps):
            t0, t1 = s / steps, (s + 0.5) / steps
            d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                    (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
                   fill=NAVY, width=2)
    labels = [("PORT LIORA", "02 JUN 2025"), ("LISBON", "12 SEP 2025"),
              ("ATHENS", "28 SEP 2025"), ("ISTANBUL", "09 OCT 2025")]
    for (px, py), (name, date) in zip(pts, labels):
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=NAVY)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)
        centre(d, px, py + 12, name, F_STAMP_SM, INK)
        centre(d, px, py + 26, date, F_STAMP_SM, MUTED)
    d.text((RX0, 872), "Route of the holder's 2025 voyage, in order. "
                       "Every stamp above falls on this line.",
           font=F_BODY_SM, fill=MUTED)

    # fee stamp, bottom right
    d.rectangle([RX1 - 210, 900, RX1, 946], outline=BURGUNDY, width=2)
    centre(d, RX1 - 105, 908, "FEE PAID — 40 VLR", F_STAMP, BURGUNDY)
    centre(d, RX1 - 105, 924, "02 JUN 2025 · PORT LIORA",
           F_STAMP_SM, BURGUNDY)
    d.text((RX0, 958), "VISAS — PAGE 3", font=F_FOOT, fill=MUTED)
    d.text((RX1 - 10, 958), "3", font=F_FOOT, fill=MUTED)

    return img


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    out = args.out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (out, PAGE_W, PAGE_H))
    print("MRZ: %s / %s" % mrz_lines())
    return 0


if __name__ == "__main__":
    sys.exit(main())
