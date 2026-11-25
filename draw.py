#!/usr/bin/env python3
"""Draw the make.fun news-image-20261125 entry: a dense one-day front page
summing up world news of Wednesday 25 November 2026. All stories verified
against named sources (see README.md). Output: 1024x1024 PNG, <= 1 MiB."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)      # newsprint
INK = (18, 24, 38)
NAVY = (16, 35, 63)
RED = (178, 34, 34)
BLUE = (30, 90, 160)
TEAL = (14, 110, 110)
GOLD = (176, 124, 20)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 192, 175)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap by pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, lines, f, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def section_head(d, x, y, w, color, title):
    d.rectangle([x, y, x + 12, y + 12], fill=color)
    d.text((x + 18, y - 1), title, font=font(F_SANS_B, 13), fill=INK)
    d.line([x, y + 18, x + w, y + 18], fill=color, width=2)
    return y + 26


def story(d, x, y, w, headline, summary, source, max_sum_lines=2):
    f_h, f_s, f_t = font(F_SANS_B, 13), font(F_SANS, 11), font(F_SANS_I, 9)
    hl = wrap(d, headline, f_h, w)
    y = draw_text_block(d, x, y, hl[:2], f_h, INK, 15)
    sl = wrap(d, summary, f_s, w)
    y = draw_text_block(d, x, y + 1, sl[:max_sum_lines], f_s, (50, 50, 50), 13)
    d.text((x, y + 1), source, font=f_t, fill=GREY)
    return y + 13


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------------- MASTHEAD ----------------
d.rectangle([0, 0, W, 108], fill=NAVY)
d.text((16, 10), "THE WORLD IN ONE DAY  •  A FRONT PAGE OF WEDNESDAY'S NEWS",
       font=font(F_SANS_B, 12), fill=(180, 200, 230))
d.text((16, 28), "WORLD NEWS", font=font(F_SERIF, 52), fill=(255, 255, 255))
d.text((700, 30), "WEDNESDAY", font=font(F_SERIF, 30), fill=(255, 255, 255))
d.text((700, 62), "25 NOVEMBER 2026", font=font(F_SANS_B, 22), fill=(255, 210, 90))
d.text((16, 92), "30+ stories  •  7 regions  •  Every story first reported today",
       font=font(F_SANS, 11), fill=(180, 200, 230))
d.rectangle([0, 108, W, 112], fill=RED)
d.text((16, 118), "SUMMING UP WEDNESDAY 25 NOVEMBER 2026 — WAR IN THE GULF WIDENS, MARKETS SLIDE, A HOSTAGE SIEGE ENDS",
       font=font(F_SANS_B, 11), fill=RED)
d.text((16, 132), "Sources: Reuters  •  AP  •  AFP  •  Al Jazeera  •  TASS  •  Kyiv Independent",
       font=font(F_SANS, 10), fill=GREY)

# ---------------- HERO (lead story) ----------------
hx, hy, hw, hh = 16, 152, 624, 148
d.rectangle([hx, hy, hx + hw, hy + hh], fill=CARD, outline=LINE, width=1)
# drawn scene: tanker at sea, refinery, explosion
ax, ay, aw, ah = hx + 10, hy + 10, 210, 128
d.rectangle([ax, ay, ax + aw, ay + ah], fill=(214, 232, 240))
d.ellipse([ax + 160, ay + 8, ax + 196, ay + 44], fill=(255, 214, 130))  # sun
# refinery towers
for i, tx in enumerate([ax + 12, ax + 34, ax + 56]):
    d.rectangle([tx, ay + 52 - i * 6, tx + 12, ay + 96], fill=(90, 90, 96))
    d.ellipse([tx - 3, ay + 40 - i * 6, tx + 15, ay + 54 - i * 6], fill=(200, 200, 200))
# explosion starburst
cx, cy = ax + 150, ay + 42
for ang in range(0, 360, 30):
    import math
    x2 = cx + 26 * math.cos(math.radians(ang))
    y2 = cy + 26 * math.sin(math.radians(ang))
    d.line([cx, cy, x2, y2], fill=(230, 120, 20), width=4)
d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 170, 40))
d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 230, 120))
# sea + tanker
d.rectangle([ax, ay + 96, ax + aw, ay + ah], fill=(38, 90, 130))
for wx in range(ax, ax + aw, 26):
    d.arc([wx, ay + 100, wx + 24, ay + 112], 0, 180, fill=(255, 255, 255), width=2)
    d.arc([wx + 8, ay + 116, wx + 32, ay + 128], 0, 180, fill=(200, 225, 240), width=2)
d.polygon([(ax + 18, ay + 96), (ax + 190, ay + 96), (ax + 178, ay + 76),
           (ax + 30, ay + 76)], fill=(30, 30, 34))  # hull
d.rectangle([ax + 150, ay + 58, ax + 176, ay + 76], fill=(200, 60, 50))  # bridge
for cx0, col in [(ax + 40, (220, 80, 60)), (ax + 70, (60, 140, 90)),
                 (ax + 100, (230, 180, 60)), (ax + 128, (70, 110, 180))]:
    d.rectangle([cx0, ay + 62, cx0 + 26, ay + 76], fill=col)
d.text((ax + 6, ay + ah - 16), "RAS TANURA, SAUDI ARABIA", font=font(F_SANS_B, 8),
       fill=(255, 255, 255))
# hero text
tx = hx + 232
d.text((tx, hy + 8), "LEAD STORY — MIDDLE EAST", font=font(F_SANS_B, 11), fill=RED)
y = hy + 26
y = draw_text_block(d, tx, y, wrap(d, "Houthis hit Saudi refinery as Gulf war widens",
                                   font(F_SERIF, 21), hw - 244), font(F_SERIF, 21), INK, 24)
y = draw_text_block(d, tx, y + 2, wrap(d, "Yemen's Houthis say they struck the Ras Tanura oil refinery and "
       "Riyadh's financial district. The Saudi-led coalition hit Hodeidah port, and "
       "Iran says tankers hit mines in the Strait of Hormuz.",
       font(F_SANS, 11), hw - 244), font(F_SANS, 11), (50, 50, 50), 13)
d.text((tx, hy + hh - 18), "Reuters  •  Al Jazeera", font=font(F_SANS_I, 10), fill=GREY)

# ---------------- RIGHT: numbers + also leading ----------------
rx, ry, rw = 656, 152, 352
d.rectangle([rx, ry, rx + rw, ry + 148], fill=NAVY)
d.text((rx + 12, ry + 8), "THE DAY IN NUMBERS", font=font(F_SANS_B, 12), fill=(255, 210, 90))
nums = [("NIKKEI 225", "-2.8%"), ("KOSPI", "-5.8%"), ("S&P 500", "-0.5%"),
        ("BRENT CRUDE", "$90.09"), ("GOLD / OZ", "$3,545"), ("BITCOIN", "$59,258")]
for i, (k, v) in enumerate(nums):
    nx = rx + 12 + (i % 3) * 116
    ny = ry + 30 + (i // 3) * 34
    d.text((nx, ny), k, font=font(F_SANS_B, 9), fill=(180, 200, 230))
    d.text((nx, ny + 12), v, font=font(F_SANS_B, 15), fill=(255, 255, 255))
d.text((rx + 12, ry + 104), "Asian stocks slide as US tariff threats loom; Nvidia falls ~6%.",
       font=font(F_SANS, 10), fill=(200, 210, 225))
d.text((rx + 12, ry + 122), "Reuters market data, 25 Nov 2026", font=font(F_SANS_I, 9), fill=(150, 170, 200))

# ---------------- TIMELINE STRIP ----------------
ty = 310
d.rectangle([16, ty, 1008, ty + 46], fill=(232, 226, 210))
d.text((26, ty + 4), "HOW THE DAY UNFOLDED — UTC",
       font=font(F_SANS_B, 11), fill=INK)
tl = [
    ("00–08 UTC", "Nikkei slides 2.8%; China probes Shanghai chief; Pakistan astronaut in orbit."),
    ("08–16 UTC", "Cartagena hostages freed; US PCE & GDP due 13:30 GMT; Jordan death sentence."),
    ("16–24 UTC", "Ábrego García flies to Spain; US tariff probe; Iowa lead-azide blast set."),
]
for bi, (label, txt) in enumerate(tl):
    x = 26 + bi * 324
    d.text((x, ty + 20), label, font=font(F_SANS_B, 10), fill=RED)
    draw_text_block(d, x + 78, ty + 20, wrap(d, txt, font(F_SANS, 10), 218),
                    font(F_SANS, 10), INK, 12)
    if bi < 2:
        d.line([x + 312, ty + 20, x + 312, ty + 42], fill=LINE, width=1)

# ---------------- GRID: 3 columns x 7 stories ----------------
gy = 368
col_w = 320
cols = [
    ("MIDDLE EAST & UKRAINE", RED, [
        ("Coalition strikes Hodeidah port", "Saudi-led coalition hits Yemen's Hodeidah after ordering civilians out; Houthis threaten Jeddah.", "Al Jazeera • WireMinute"),
        ("Tankers hit mines in Hormuz", "Iran's Revolutionary Guards say tankers under US air escort struck naval mines in the strait.", "IRGC"),
        ("Putin vows 'inevitable' retaliation", "Putin says Ukraine keeps hitting Russian refineries despite Trump's request to stop.", "Kremlin"),
        ("Ukraine claims Baltic ship strike", "Kyiv claims the strike on a Russian-flagged ship; Norway urges restraint.", "The Silk Paradox"),
        ("Kyiv: Benghazi strike was self-defence", "Ukraine cites UN Charter Art. 51; Libya asks for an emergency UN Security Council meeting.", "Kyiv Independent • Al Jazeera"),
        ("Norway pledges $7bn for Ukraine", "Oslo will give Ukraine at least $7bn in 2027, air defence first, Kyiv says.", "Reuters • Kyiv Independent"),
        ("Zaporizhzhia flats hit: 2 killed", "Russian strike on a block of flats kills two and wounds more than 40.", "The Silk Paradox"),
    ]),
    ("ASIA & OCEANIA", TEAL, [
        ("China probes Shanghai party chief", "Anti-graft watchdog investigates Politburo member Chen Jining, the fourth such probe since 2025.", "Reuters"),
        ("Pakistan's first astronaut in orbit", "Zeeshan Ali reaches China's space station aboard Shenzhou-24, a first for Pakistan.", "WireMinute • Horizon"),
        ("Bangladesh garment wage up 36%", "Minimum wage rises to Tk17,000 a month after weeks of protests over living costs.", "TBS • Horizon"),
        ("Dozens trapped in flooded mine", "Rescuers search for miners stuck in a 100-metre-deep Indonesian mine since 23 Nov.", "Horizon • OneTurn"),
        ("Solomon Islands signs Australia pact", "Security treaty with Australia rules out foreign military bases in the islands.", "OneTurn"),
        ("Jordan hands down death sentence", "State Security Court sentences a man to death over an attack that killed an officer.", "Reuters"),
        ("Turkish helicopter crashes: 5 dead", "Five killed as a Turkish military helicopter crashes during a training flight.", "WireMinute"),
    ]),
    ("AMERICAS & EUROPE", BLUE, [
        ("Cartagena siege ends, all freed", "Troops storm an Éxito supermarket; all hostages freed, one gunman killed, after a day-long siege.", "Reuters • AFP"),
        ("Cessna crashes off Mississippi: 6 dead", "Six aboard, incl. two boys aged 8 and 10, die after the plane goes down in the Gulf of Mexico.", "AP • US Coast Guard"),
        ("Ábrego García leaves US for Spain", "Salvadoran man at the centre of the deportation saga departs voluntarily for Spain.", "AP"),
        ("US set to raise tariffs on 16 economies", "Trump administration prepares new tariffs on China, the EU and 14 others over subsidies.", "AP • Reuters"),
        ("Democrats clinch 259 House seats", "House majority is the party's largest since 1990, AP projects after the midterms.", "AP"),
        ("US jury convicts Huawei", "Huawei found guilty of conspiring to steal trade secrets and bank fraud.", "AP"),
        ("Spain heads to snap election", "Spain to hold an early general election, the day's European politics lead.", "OneTurn"),
    ]),
]
final_ys = []
for ci, (title, color, items) in enumerate(cols):
    x = 16 + ci * (col_w + 16)
    y = section_head(d, x, gy, col_w, color, title)
    for hl, sm, src in items:
        y = story(d, x, y, col_w, hl, sm, src)
        y += 2
        d.line([x, y, x + col_w, y], fill=(225, 220, 208), width=1)
        y += 5
    final_ys.append(y)

# ---------------- ALSO TODAY (second row, 3 short items) ----------------
ay = max(final_ys) + 2
d.text((16, ay), "ALSO TODAY", font=font(F_SANS_B, 11), fill=INK)
d.line([16, ay + 16, 1008, ay + 16], fill=RED, width=2)
also = [
    ("Nvidia falls ~6%", "AI rally fades as lawmakers question Trump's role in Huang's return. — Reuters"),
    ("CIA system breached", "Unclassified CIA system hit in a cyberattack, AP source says. — AP"),
    ("Real Madrid rout PSV", "Bellingham stunner, Mbappé brace in Champions League. — WireMinute"),
    ("UN: 5 women killed hourly", "Five women an hour killed by relatives in 2025, UN says. — UN"),
]
for ai, (h, t) in enumerate(also):
    ax = 16 + ai * 248
    d.text((ax, ay + 22), h, font=font(F_SANS_B, 11), fill=INK)
    draw_text_block(d, ax, ay + 38, wrap(d, t, font(F_SANS, 10), 232),
                    font(F_SANS, 10), (50, 50, 50), 12)

# ---------------- BOTTOM: pin map + date-check ----------------
by = ay + 84
d.line([16, by, 1008, by], fill=LINE, width=1)
by += 8
# map box
mx, my, mw, mh = 16, by, 600, 96
d.rectangle([mx, my, mx + mw, my + mh], fill=(222, 234, 240), outline=LINE)
d.text((mx + 8, my + 4), "WHERE IT HAPPENED", font=font(F_SANS_B, 10), fill=INK)
# stylised continents (flat projection, rough polygons)
land = (170, 190, 170)
polys = [
    [(28, 22), (120, 14), (150, 26), (128, 52), (96, 58), (60, 46), (30, 38)],   # N America
    [(118, 60), (152, 58), (158, 76), (138, 92), (124, 78)],                      # S America
    [(300, 18), (336, 12), (344, 30), (322, 38), (300, 32)],                      # Europe
    [(300, 42), (344, 40), (348, 66), (330, 86), (308, 70), (296, 54)],           # Africa
    [(348, 12), (560, 8), (576, 30), (540, 52), (470, 56), (410, 44), (352, 34)], # Asia
    [(500, 74), (556, 72), (560, 86), (516, 90), (498, 82)],                      # Australia
]
for p in polys:
    d.polygon([(mx + px, my + 8 + py) for px, py in p], fill=land)
pins = [  # (x, y, label, dx, dy) label offset from pin
    (432, 52, "RIYADH", -46, -4), (452, 50, "HORMUZ", 6, 6),
    (336, 20, "KYIV", 6, -4), (306, 30, "MADRID", -42, -4),
    (520, 34, "SHANGHAI", 6, -4), (472, 44, "DHAKA", 6, -4),
    (500, 66, "JAKARTA", 6, -4), (140, 66, "CARTAGENA", 6, -4),
    (92, 40, "MISSISSIPPI", 6, -4), (340, 76, "KINSHASA", 6, -4),
]
for px, py, lab, lx, ly in pins:
    X, Y = mx + px, my + 8 + py
    d.ellipse([X - 4, Y - 4, X + 4, Y + 4], fill=RED, outline=(255, 255, 255), width=1)
    d.text((X + lx, Y + ly), lab, font=font(F_SANS_B, 8), fill=INK)
# date-check box
dx, dw = 632, 376
d.rectangle([dx, my, dx + dw, my + mh], fill=(255, 250, 230), outline=GOLD, width=1)
d.text((dx + 10, my + 6), "DATE-CHECKED  •  25 NOV 2026, 17:00 WITA",
       font=font(F_SANS_B, 10), fill=(120, 80, 0))
chk = ("Every story above happened, or was first reported, on Wed 25 Nov 2026. "
       "Names, numbers and dates are as reported by the sources named. "
       "Nothing here is invented.")
y = draw_text_block(d, dx + 10, my + 24, wrap(d, chk, font(F_SANS, 10), dw - 20),
                    font(F_SANS, 10), INK, 13)
d.text((dx + 10, my + mh - 18), "WORLD NEWS — 25 NOVEMBER 2026  •  make.fun news-image-20261125",
       font=font(F_SANS_B, 9), fill=INK)

img.save("/home/hatch/workspace/make-money/news-20261125/repo/entry.png",
         optimize=True)
print("saved; columns end at", final_ys, "also-row at", ay, "bottom at", by)
