#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
জাপানি চা পানি — মেনু কার্ডের ভেক্টর (SVG) আর্ট জেনারেটর (v3: ফ্ল্যাট স্টিকার স্টাইল)।

ডিজাইন নিয়ম (সব কার্ডে একই, তাই মেনু একরকম দেখায়):
  • ৪:৩ ক্যানভাস, ক্যাটাগরিভিত্তিক সফট গ্রেডিয়েন্ট
  • সাদা প্লেট/সসারের ওপর ফ্ল্যাট আইকন
  • প্রতিটি মূল আকৃতিতে গাঢ় আউটলাইন (#43290f, ৪px) → পরিচ্ছন্ন, ইচ্ছাকৃত লুক
  • হট ড্রিংকে বাষ্প, ঠান্ডায় বরফ ও স্ট্র, খাবারে পার্শ্ব উপকরণ

ব্যবহার:  python3 assets/tools/make_art.py
আউটপুট:  assets/img/*.svg
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "img"))
W, H = 400, 300
LINE = "#43290f"          # আউটলাইন
LINE_W = 4.2

# --------------------------------------------------------------- বেসিক অংশ
def defs():
    return '''<defs>
<linearGradient id="tile" x1="0" y1="0" x2="0.35" y2="1">
  <stop offset="0" stop-color="#fffdf8"/><stop offset="0.55" stop-color="#fdf1e0"/><stop offset="1" stop-color="#f6e2c8"/>
</linearGradient>
<radialGradient id="glow" cx=".5" cy=".42" r=".62">
  <stop offset="0" stop-color="#ffffff" stop-opacity=".85"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</radialGradient>
<radialGradient id="shadow" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#6b4a2a" stop-opacity=".26"/><stop offset="1" stop-color="#6b4a2a" stop-opacity="0"/>
</radialGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#ffffff" stop-opacity=".0"/>
  <stop offset=".22" stop-color="#ffffff" stop-opacity=".34"/>
  <stop offset=".5" stop-color="#ffffff" stop-opacity=".05"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity=".22"/>
</linearGradient>
</defs>'''


def tile(tint="#fdf1e0", bottom="#f6e2c8"):
    return (f'<rect width="{W}" height="{H}" fill="url(#tile)"/>'
            f'<rect width="{W}" height="{H}" fill="{tint}" opacity=".55"/>'
            f'<rect y="{H-84}" width="{W}" height="84" fill="{bottom}" opacity=".75"/>'
            f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')


def ground(cx=200, cy=246, rx=112, ry=22):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#shadow)"/>'


def plate(cx=200, cy=240, rx=104, ry=26):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffffff" opacity=".92"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{LINE}" stroke-opacity=".16" stroke-width="3"/>'
            f'<ellipse cx="{cx}" cy="{cy-4}" rx="{rx*0.72:.0f}" ry="{ry*0.6:.0f}" fill="#fffdf6" opacity=".9"/>')


def steam(x=200, y=112):
    return f'''<g fill="none" stroke="#ffffff" stroke-linecap="round" stroke-width="7" opacity=".75">
<path d="M{x-22},{y} c-9,-16 11,-24 3,-40"><animate attributeName="opacity" values=".35;.85;.35" dur="4.4s" repeatCount="indefinite"/></path>
<path d="M{x+2},{y-10} c10,-18 -12,-26 -2,-42"><animate attributeName="opacity" values=".8;.3;.8" dur="5.2s" repeatCount="indefinite"/></path>
<path d="M{x+24},{y+2} c8,-14 -10,-22 -3,-34"><animate attributeName="opacity" values=".45;.9;.45" dur="4.8s" repeatCount="indefinite"/></path>
</g>'''


def glass_cup(cx=200, top=116, bottom=234, top_w=104, bot_w=82, liquid="#b06a2c",
              liquid_top=140, foam=None, ice=False, straw=None, foam_inner=None, lid=False,
              garnish=""):
    """স্ট্রেইট সাইড গ্লাস — ফ্ল্যাট, আউটলাইনসহ।"""
    htw, hbw = top_w / 2, bot_w / 2
    xtl, xtr, xbl, xbr = cx - htw, cx + htw, cx - hbw, cx + hbw
    body = f"M{xtl:.0f},{top} L{xtr:.0f},{top} L{xbr:.0f},{bottom-12} Q{xbr:.0f},{bottom} {xbr-12:.0f},{bottom} L{xbl+12:.0f},{bottom} Q{xbl:.0f},{bottom} {xbl:.0f},{bottom-12} Z"
    s = ground(cx, bottom + 12)
    if straw:
        s += (f'<g transform="rotate(15 {cx+26} {top-20})">'
              f'<rect x="{cx+20}" y="{top-84}" width="15" height="150" rx="7.5" fill="{straw}" stroke="{LINE}" stroke-width="{LINE_W}"/>'
              f'<rect x="{cx+23}" y="{top-80}" width="4" height="140" rx="2" fill="#ffffff" opacity=".45"/></g>')
    if liquid:
        s += f'<clipPath id="cc"><path d="{body}"/></clipPath>'
        s += f'<g clip-path="url(#cc)"><rect x="{xtl-6:.0f}" y="{liquid_top}" width="{top_w+12:.0f}" height="{bottom-liquid_top+8:.0f}" fill="{liquid}"/>'
        if foam_inner:
            s += f'<rect x="{xtl-6:.0f}" y="{liquid_top}" width="{top_w+12:.0f}" height="14" fill="{foam_inner}"/>'
        if ice:
            for dx, dy, rot in [(-28, 26, -14), (8, 14, 12), (-14, 56, 8), (16, 52, -10)]:
                s += (f'<rect x="{cx+dx}" y="{liquid_top+dy}" width="32" height="32" rx="9" '
                      f'fill="#ffffff" fill-opacity=".34" stroke="#ffffff" stroke-opacity=".9" stroke-width="3.2" '
                      f'transform="rotate({rot} {cx+dx+16} {liquid_top+dy+16})"/>')
        s += '</g>'
        if foam:
            s += (f'<ellipse cx="{cx}" cy="{liquid_top+2}" rx="{htw*0.98:.0f}" ry="13" fill="{foam}" stroke="{LINE}" stroke-width="{LINE_W}"/>'
                  f'<ellipse cx="{cx}" cy="{liquid_top+1}" rx="{htw*0.72:.0f}" ry="7" fill="#ffffff" opacity=".45"/>')
    s += f'<path d="{body}" fill="url(#glass)"/>'
    s += f'<path d="{body}" fill="none" stroke="{LINE}" stroke-width="{LINE_W}" stroke-linejoin="round"/>'
    s += f'<path d="M{xtl+6:.0f},{top+10} L{xbl+8:.0f},{bottom-18}" stroke="#ffffff" stroke-opacity=".7" stroke-width="7" stroke-linecap="round"/>'
    if lid:
        s += f'<ellipse cx="{cx}" cy="{top}" rx="{htw:.0f}" ry="10" fill="#ffffff" fill-opacity=".35" stroke="{LINE}" stroke-width="{LINE_W}"/>'
    return s + garnish


def mug(cx=200, top=126, bottom=234, top_w=112, bot_w=100, liquid="#b06a2c", foam=None,
        heart=False, dots_n=0, garnish="", **_ignored):
    """সাদা সিরামিক মগ — উপরে রিম, ভেতরে তরলের পৃষ্ঠ দেখা যায় (হালকা টপ-ভিউ)।"""
    htw, hbw = top_w / 2, bot_w / 2
    ry_rim = 13
    xtl, xtr, xbl, xbr = cx - htw, cx + htw, cx - hbw, cx + hbw
    body = (f"M{xtl:.0f},{top} L{xtr:.0f},{top} L{xbr:.0f},{bottom-16} "
            f"Q{xbr:.0f},{bottom} {xbr-16:.0f},{bottom} L{xbl+16:.0f},{bottom} Q{xbl:.0f},{bottom} {xbl:.0f},{bottom-16} Z")
    s = ground(cx, bottom + 12)
    # হাতল (মগের পিছনে)
    s += (f'<path d="M{xtr-8:.0f},{top+22} C{xtr+56:.0f},{top+26} {xtr+56:.0f},{bottom-38} {xtr-10:.0f},{bottom-34}" '
          f'fill="none" stroke="{LINE}" stroke-width="7" stroke-linecap="round"/>')
    # মগের গা (সিরামিক)
    s += f'<path d="{body}" fill="#fffdf8"/>'
    s += f'<path d="{body}" fill="none" stroke="{LINE}" stroke-width="{LINE_W}" stroke-linejoin="round"/>'
    s += (f'<path d="M{xtl+10:.0f},{top+18} L{xbl+12:.0f},{bottom-22}" stroke="#ffffff" stroke-width="12" '
          f'stroke-linecap="round" opacity=".85"/>'
          f'<path d="M{xtr-12:.0f},{top+26} L{xbr-14:.0f},{bottom-30}" stroke="#e8d5bb" stroke-width="7" '
          f'stroke-linecap="round" opacity=".8"/>')
    # রিম + ভেতরের তরল
    s += f'<ellipse cx="{cx}" cy="{top}" rx="{htw:.0f}" ry="{ry_rim}" fill="#efe0c9"/>'
    s += f'<ellipse cx="{cx}" cy="{top}" rx="{htw:.0f}" ry="{ry_rim}" fill="none" stroke="{LINE}" stroke-width="{LINE_W}"/>'
    s += f'<ellipse cx="{cx}" cy="{top+1}" rx="{htw*0.83:.0f}" ry="{ry_rim*0.76:.0f}" fill="{liquid}"/>'
    if foam:
        s += f'<ellipse cx="{cx}" cy="{top+1}" rx="{htw*0.7:.0f}" ry="{ry_rim*0.6:.0f}" fill="{foam}"/>'
    s += f'<ellipse cx="{cx-htw*0.3:.0f}" cy="{top-3}" rx="{htw*0.28:.0f}" ry="{ry_rim*0.3:.0f}" fill="#ffffff" opacity=".4"/>'
    if heart:
        s += (f'<path d="M{cx},{top-4} c-11,-11 -25,3 -13,12 l13,11 l13,-11 c12,-9 -2,-23 -13,-12z" '
              f'fill="#ffffff" opacity=".8"/>')
    if dots_n:
        for i in range(dots_n):
            s += f'<circle cx="{cx-20+(i*13)%42}" cy="{top-4+(i*9)%10}" r="3.2" fill="#3f7d3a" opacity=".85"/>'
    return s + garnish


def lemon_slice(cx, cy, r=30, rot=0, peel="#f0b429", flesh="#fff3c2"):
    seg = "".join(f'<ellipse cx="{cx}" cy="{cy-r*0.52:.0f}" rx="{r*0.17:.1f}" ry="{r*0.44:.1f}" fill="{flesh}" transform="rotate({a} {cx} {cy})"/>'
                  for a in range(0, 360, 45))
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{flesh}" stroke="{LINE}" stroke-width="{LINE_W}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.8:.0f}" fill="{peel}" opacity=".85"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.74:.0f}" fill="{flesh}"/>{seg}</g>')


def mint(x, y, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<ellipse cx="{x}" cy="{y}" rx="11" ry="19" fill="#5cb85f" stroke="{LINE}" stroke-width="{LINE_W-1}"/>'
            f'<path d="M{x},{y-17} L{x},{y+17}" stroke="#2f7a3a" stroke-width="2.6"/></g>')


def choco_chips(cx, cy, n=6, spread=40):
    return "".join(f'<circle cx="{cx-20+(i*17)%spread}" cy="{cy-8+(i*13)%16}" r="4" fill="#3b2112"/>' for i in range(n))


def crumbs(cx, cy, n=5, c="#8a5a2b"):
    return "".join(f'<circle cx="{cx-24+(i*19)%48}" cy="{cy+(i*11)%14}" r="3.4" fill="{c}"/>' for i in range(n))


# --------------------------------------------------------------- চা
def tea_masala():
    return (tile("#fdf3e2", "#f2ddc0") + steam(196, 112) +
            mug(cx=196, top=120, bottom=240, liquid="#a9662a", foam="#d8ab72") +
            # আস্ত মশলা: দারুচিনি, এলাচ
            f'<rect x="286" y="216" width="62" height="15" rx="7.5" fill="#a9663a" stroke="{LINE}" stroke-width="{LINE_W}" transform="rotate(-14 317 223)"/>'
            f'<rect x="292" y="214" width="50" height="5" rx="2.5" fill="#cf9256" transform="rotate(-14 317 216)"/>'
            f'<ellipse cx="284" cy="252" rx="15" ry="10" fill="#8a5a2b" stroke="{LINE}" stroke-width="{LINE_W}" transform="rotate(-18 284 252)"/>'
            + crumbs(132, 258, 4, "#6f4a1f"))


def tea_lemon_green():
    return (tile("#f4fbe9", "#e2f2d4") + steam(182, 114) +
            mug(cx=182, top=120, bottom=240, top_w=106, bot_w=94, liquid="#b9d377", foam="#e6f2c4") +
            lemon_slice(288, 232, 31, -12, "#d8c94a", "#f4f7cf") +
            mint(324, 262, 22) + mint(126, 262, -18))


def tea_lemon():
    return (tile("#fff8e8", "#fbe9bd") + steam(200, 112) +
            mug(cx=200, top=120, bottom=240, liquid="#c9862c", foam="#eecfa0") +
            lemon_slice(296, 240, 30, 14) + mint(120, 258, 16))


def tea_black():
    return (tile("#f7f0e7", "#e6d6c2") + steam(200, 110) +
            mug(cx=200, top=120, bottom=240, liquid="#6b3411", foam="#8a4a1d") +
            # চায়ের পাতা
            f'<g stroke="{LINE}" stroke-width="2.4">'
            + "".join(f'<ellipse cx="{290+(i*13)%34}" cy="{244+(i*11)%16}" rx="9" ry="4" fill="#4a2c17" transform="rotate({(i*37)%70-35} {290+(i*13)%34} {244+(i*11)%16})"/>' for i in range(6))
            + '</g>')


def tea_roohafza():
    return (tile("#fdeef4", "#f8d3e0") +
            glass_cup(cx=200, top=106, bottom=240, liquid="#e4678f", liquid_top=134,
                      foam=None, ice=True, straw="#d6453d", lid=True,
                      garnish=(f'<ellipse cx="286" cy="222" rx="30" ry="13" fill="#ffffff" opacity=".9"/>'
                               + ''.join(f'<circle cx="{272+(i*11)%34}" cy="{214+(i*9)%14}" r="3.6" fill="#5cb85f"/>' for i in range(6))
                               + f'<circle cx="286" cy="234" r="6" fill="#d6453d"/>')) +
            mint(124, 260, -14))


# --------------------------------------------------------------- কফি
def coffee_hot():
    return (tile("#f6e8d8", "#e8cfb2") + steam(200, 118) +
            mug(cx=200, top=122, bottom=238, top_w=118, bot_w=106, liquid="#3f1e0b",
                foam="#b57a3d") + crumbs(296, 254, 5, "#5b3a1c"))


def coffee_cappuccino():
    return (tile("#f7ede2", "#ead6bd") + steam(200, 120, ) +
            mug(cx=200, top=122, bottom=238, top_w=120, bot_w=108, liquid="#8a5227",
                foam="#fdf3e3", heart=True) + crumbs(128, 256, 4, "#c98d55"))


def coffee_latte():
    return (tile("#f9eee1", "#eed9bd") + steam(200, 120) +
            mug(cx=200, top=122, bottom=238, top_w=118, bot_w=106, liquid="#c08e55",
                foam="#fdf1df", heart=True) + crumbs(288, 258, 5, "#a9663a"))


def coffee_iced_latte():
    layers = (f'<rect x="152" y="132" width="96" height="66" fill="#7a4a24" opacity=".95"/>'
              f'<rect x="152" y="196" width="96" height="10" fill="#ffffff" opacity=".35"/>')
    return (tile("#f3e7d9", "#e3cbb1") +
            glass_cup(cx=200, top=108, bottom=240, liquid="#e9d6b8", liquid_top=132,
                      ice=True, straw="#4a2c17", lid=True, garnish=layers))


def coffee_mocha():
    top = (f'<path d="M152,132 q11,-26 23,-8 q10,-24 22,-7 q11,-22 21,-5 q12,-18 21,8 z" '
           f'fill="#fdf6ea" stroke="{LINE}" stroke-width="{LINE_W}" stroke-linejoin="round"/>'
           + choco_chips(200, 116, 6, 52) + f'<circle cx="200" cy="104" r="10" fill="#d6453d" stroke="{LINE}" stroke-width="3.4"/>')
    return (tile("#f2e8de", "#e0cbb4") +
            glass_cup(cx=200, top=106, bottom=242, liquid="#57331a", liquid_top=130,
                      ice=True, straw="#e2a33c", lid=True, garnish=top))


def coffee_black():
    return (tile("#f0e8de", "#ddccb8") + steam(200, 112) +
            mug(cx=200, top=122, bottom=238, top_w=112, bot_w=102, liquid="#231006",
                foam="#7a4a24") + crumbs(298, 256, 5, "#4a2c17"))


# --------------------------------------------------------------- জুস
def juice_orange():
    return (tile("#fff4de", "#ffe2b4") +
            glass_cup(cx=190, top=106, bottom=240, liquid="#f79c1e", liquid_top=132, ice=True,
                      straw="#e2731f", lid=True) +
            lemon_slice(292, 216, 32, 10, "#f08c1c", "#ffdd93") + mint(316, 258, 24))


def juice_pineapple():
    fruit = (f'<g transform="rotate(-12 300 224)">'
             f'<path d="M292,180 q40,12 36,50 q-4,38 -38,33 q-29,-6 -25,-44 q4,-31 27,-39z" fill="#f3cc3c" stroke="{LINE}" stroke-width="{LINE_W}"/>'
             f'<path d="M276,200 L320,210 M272,224 L324,234 M276,248 L318,254" stroke="#c9a11c" stroke-width="3" opacity=".8"/>'
             f'<path d="M302,182 q4,-24 22,-32 q-9,20 -14,34z" fill="#5cb85f" stroke="{LINE}" stroke-width="3"/></g>')
    return (tile("#fffcdf", "#f7eeb2") +
            glass_cup(cx=192, top=106, bottom=240, liquid="#f2ca34", liquid_top=132, ice=True,
                      straw="#c9a11c", lid=True) + fruit)


def juice_watermelon():
    wm = (f'<g transform="rotate(-20 312 228)">'
          f'<path d="M266,206 a54,54 0 0 1 98,44 z" fill="#f06a75" stroke="{LINE}" stroke-width="{LINE_W}"/>'
          f'<path d="M270,212 a50,50 0 0 1 88,40" fill="none" stroke="#3f9d5a" stroke-width="9"/>'
          + "".join(f'<ellipse cx="{288+(i*17)%52}" cy="{228+(i*13)%20}" rx="3.6" ry="5.2" fill="#2f1a12" opacity=".85"/>' for i in range(6))
          + '</g>')
    return (tile("#fdeef0", "#f9cfd8") +
            glass_cup(cx=192, top=106, bottom=240, liquid="#ef6d78", liquid_top=132, ice=True,
                      straw="#17785a", lid=True) + wm)


def juice_bel():
    pulp = (f'<ellipse cx="288" cy="238" rx="40" ry="16" fill="#ffffff" opacity=".9"/>'
            f'<ellipse cx="288" cy="236" rx="32" ry="12" fill="#e6eeb2" stroke="{LINE}" stroke-width="LINE_W"/>'.replace("LINE_W", str(LINE_W))
            + f'<circle cx="276" cy="234" r="4.4" fill="#a8b95c"/><circle cx="292" cy="238" r="4.4" fill="#a8b95c"/>'
            f'<circle cx="304" cy="232" r="4" fill="#a8b95c"/>')
    return (tile("#f4fbe9", "#e2f0cd") +
            glass_cup(cx=194, top=108, bottom=240, liquid="#dfe9a4", liquid_top=132, ice=True,
                      straw="#8a9a3d", lid=True) + pulp)


def juice_lassi():
    return (tile("#fdf8ef", "#f4e6d0") +
            glass_cup(cx=200, top=104, bottom=240, liquid="#fdf6e7", liquid_top=132,
                      foam="#ffffff", ice=False, straw="#e2a33c", lid=True,
                      garnish=''.join(f'<circle cx="{168+(i*13)%64}" cy="{120+(i*11)%14}" r="3.4" fill="#5cb85f"/>' for i in range(7))
                              + mint(268, 196, 28)))


def juice_banana():
    ban = (f'<g transform="rotate(-16 296 220)">'
           f'<ellipse cx="296" cy="220" rx="36" ry="28" fill="#f7e9a8" stroke="{LINE}" stroke-width="{LINE_W}"/>'
           f'<ellipse cx="296" cy="220" rx="18" ry="13" fill="#fdf6d6"/></g>' + mint(330, 258, -22))
    return (tile("#fffbe4", "#f8efc2") +
            glass_cup(cx=200, top=104, bottom=240, liquid="#f6e7a6", liquid_top=130,
                      ice=True, straw="#e2a33c", lid=True) + ban)


def juice_chocolate():
    top = (f'<path d="M150,132 q11,-26 23,-8 q10,-24 22,-7 q11,-22 21,-5 q12,-18 22,8 z" '
           f'fill="#fdf6ea" stroke="{LINE}" stroke-width="{LINE_W}" stroke-linejoin="round"/>'
           + choco_chips(200, 118, 6, 52)
           + f'<circle cx="200" cy="106" r="10" fill="#d6453d" stroke="{LINE}" stroke-width="3.4"/>'
           + f'<rect x="196" y="84" width="8" height="14" rx="4" fill="#5cb85f"/>')
    return (tile("#f6ece2", "#e6d2ba") +
            glass_cup(cx=200, top=106, bottom=242, liquid="#5e3719", liquid_top=130,
                      ice=True, straw="#d6453d", lid=True, garnish=top))



def juice_lemon():
    return (tile("#fffbe6", "#f6f0b8") +
            glass_cup(cx=196, top=104, bottom=240, liquid="#e8d24a", liquid_top=130,
                      ice=True, straw="#c9a11c", lid=True,
                      garnish=lemon_slice(292, 214, 32, 8, "#e8c93a", "#fdf6c2") + mint(318, 258, 22)))


# --------------------------------------------------------------- ফাস্টফুড
def ff_beef_burger():
    burger = (
        plate(200, 246, 112, 26)
        + f'<rect x="128" y="196" width="144" height="34" rx="17" fill="#d2913f" stroke="{LINE}" stroke-width="{LINE_W}"/>'
        + f'<rect x="132" y="200" width="136" height="12" rx="6" fill="#e8b273"/>'
        + f'<rect x="120" y="170" width="160" height="30" rx="15" fill="#5d351b" stroke="{LINE}" stroke-width="{LINE_W}"/>'
        + f'<path d="M122,176 q40,10 158,0" stroke="#7d4a27" stroke-width="4" fill="none"/>'
        + f'<path d="M124,168 L276,168 L266,188 L248,170 L228,190 L208,170 L188,190 L168,170 L146,188 L134,170 Z" fill="#f2b13c" stroke="{LINE}" stroke-width="{LINE_W}" stroke-linejoin="round"/>'
        + f'<path d="M118,164 q13,-19 26,0 q13,-21 26,0 q13,-21 26,0 q13,-21 26,0 q13,-21 26,0 q13,-19 24,0 q-10,12 -154,0z" fill="#77c46a" stroke="{LINE}" stroke-width="{LINE_W}" stroke-linejoin="round"/>'
        + f'<path d="M118,156 Q200,64 282,156 Z" fill="#dd9f4e" stroke="{LINE}" stroke-width="{LINE_W}" stroke-linejoin="round"/>'
        + f'<path d="M128,152 Q200,82 272,152" fill="none" stroke="#f0c184" stroke-width="8" opacity=".7"/>'
        + "".join(f'<ellipse cx="{x}" cy="{y}" rx="6.4" ry="3.8" fill="#fff6e2" transform="rotate({r} {x} {y})"/>'
                  for x, y, r in [(166, 130, -20), (200, 116, 10), (234, 130, -8), (182, 146, 18), (218, 146, -14)])
    )
    return tile("#fff3e6", "#f7dcc2") + burger


def ff_chicken_fry():
    def drum(cx, cy, rot, c1, c2):
        # হাড়ের মাথা মাংসের পিছনে ছোট করে দেখানো হয় (ললিপপ নয়)
        return (f'<g transform="rotate({rot} {cx} {cy})">'
                f'<rect x="{cx-9}" y="{cy-74}" width="18" height="34" rx="9" fill="#fdf6e8" stroke="{LINE}" stroke-width="{LINE_W-0.8}"/>'
                f'<ellipse cx="{cx}" cy="{cy-14}" rx="50" ry="44" fill="{c1}" stroke="{LINE}" stroke-width="{LINE_W}"/>'
                f'<ellipse cx="{cx-7}" cy="{cy-20}" rx="38" ry="32" fill="{c2}"/>'
                f'<path d="M{cx-34},{cy-34} q16,-16 34,-18" fill="none" stroke="#ffffff" stroke-opacity=".55" stroke-width="7" stroke-linecap="round"/>'
                + crumbs(cx, cy - 18, 8, "#b8762f") + '</g>')
    return (tile("#fff2e4", "#f8ddc0") + plate(200, 256, 124, 26)
            + drum(162, 208, -12, "#c47f38", "#dda057")
            + drum(252, 200, 12, "#b8732f", "#d89a50")
            + f'<ellipse cx="316" cy="230" rx="34" ry="14" fill="#ffffff" opacity=".9" stroke="{LINE}" stroke-width="{LINE_W}"/>'
              f'<ellipse cx="316" cy="228" rx="26" ry="9" fill="#d6453d" opacity=".9"/>')


def ff_nuggets():
    def nugget(cx, cy, rot, c1):
        return (f'<g transform="rotate({rot} {cx} {cy})">'
                f'<path d="M{cx-32},{cy-12} q4,-22 26,-24 q24,-2 36,12 q14,16 2,30 q-14,16 -38,12 q-21,-4 -26,-16 q-4,-10 0,-14z" '
                f'fill="{c1}" stroke="{LINE}" stroke-width="{LINE_W}" stroke-linejoin="round"/>'
                f'<path d="M{cx-24},{cy-10} q6,-16 22,-18 q18,-1 26,10 q9,13 0,22 q-11,12 -30,9 q-16,-3 -20,-13 q-3,-7 2,-10z" fill="#f0c68e"/>'
                + crumbs(cx - 2, cy - 4, 6, "#cf9350") + '</g>')
    return (tile("#fff6e7", "#f9e0c2") + plate(200, 254, 124, 26)
            + nugget(160, 148, -12, "#dc9d4f")
            + nugget(240, 138, 14, "#dc9d4f")
            + nugget(148, 200, 6, "#d08f45")
            + nugget(242, 198, -10, "#d08f45")
            + nugget(196, 236, 0, "#c98640")
            + f'<ellipse cx="308" cy="236" rx="32" ry="14" fill="#ffffff" opacity=".9" stroke="{LINE}" stroke-width="{LINE_W}"/>'
              f'<ellipse cx="308" cy="234" rx="23" ry="9" fill="#e2a33c" opacity=".92"/>')


# --------------------------------------------------------------- তালিকা
ITEMS = [
    ("tea_masala.svg", tea_masala),
    ("tea_lemon_green.svg", tea_lemon_green),
    ("tea_lemon.svg", tea_lemon),
    ("tea_black.svg", tea_black),
    ("tea_roohafza.svg", tea_roohafza),
    ("coffee_hot.svg", coffee_hot),
    ("coffee_cappuccino.svg", coffee_cappuccino),
    ("coffee_latte.svg", coffee_latte),
    ("coffee_iced_latte.svg", coffee_iced_latte),
    ("coffee_mocha.svg", coffee_mocha),
    ("coffee_black.svg", coffee_black),
    ("juice_orange.svg", juice_orange),
    ("juice_pineapple.svg", juice_pineapple),
    ("juice_watermelon.svg", juice_watermelon),
    ("juice_lemon.svg", juice_lemon),
    ("juice_bel.svg", juice_bel),
    ("juice_lassi.svg", juice_lassi),
    ("juice_banana.svg", juice_banana),
    ("juice_chocolate.svg", juice_chocolate),
    ("ff_beef_burger.svg", ff_beef_burger),
    ("ff_chicken_fry.svg", ff_chicken_fry),
    ("ff_nuggets.svg", ff_nuggets),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, fn in ITEMS:
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
               f'aria-label="{name.replace(".svg", "").replace("_", " ")}">{defs()}{fn()}</svg>')
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        total += len(svg)
    print(f"তৈরি: {len(ITEMS)}টি SVG, মোট {total // 1024} KB")


if __name__ == "__main__":
    main()
