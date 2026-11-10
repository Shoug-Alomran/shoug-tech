#!/usr/bin/env python3
"""Build the CS331 past papers and the questions-by-chapter page.

Every question is transcribed from photos of graded papers and LMS reviews and
defined once below as a Q, tagged with its course chapter. Each paper lays its
questions out like the printed sheet; exams/07-questions-by-chapter reuses the
same questions grouped by chapter.

Answers on the graded photos are corrected, not copied. Student names and IDs
are left out. Marking comes from docs/javascripts/cys401-past-paper.js, the
paper engine shared with CYS401; docs/styles/cs331-past-paper.css adds the few
CS331 layouts on top of cys401-past-paper.css.

    python3 scripts/build_cs331_past_papers.py

Writes the standalone pages, their wrappers, the Exams listing and the sidebar
entries, and stamps the sidebar on CS331 exam pages only.
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_academic_sidebar as sidebar  # noqa: E402
import build_cys401_past_papers as pp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
COURSE = ROOT / "docs/academics/computer-science/cs331"
EXAMS = COURSE / "exams"
BASE = "/academics/computer-science/cs331/exams/"
SITE = "https://shoug-tech.com"
TEMPLATE = COURSE / "extra-resources/quiz-2-cheat-sheet/index.html"

esc = html.escape
sel, txt, num, written = pp.sel, pp.txt, pp.num, pp.written

CHAPTERS = {
    1: "Introduction to Data Communications and Networking",
    2: "Physical Layer",
    3: "Data Link Layer",
    4: "Ethernet and LANs",
    6: "Interconnecting Devices and VLANs",
    7: "Network Layer Data Transfer",
    8: "Network Layer Routing",
    9: "Transport Layer",
    10: "DNS and Application Layer",
}
SOURCES = {
    "m1": "Major I (181)",
    "m2": "Major II (181)",
    "q1": "Quiz 1",
    "q2": "Quiz 2",
    "l1": "Online quiz, Ch 1",
    "l2": "Online quiz, Ch 3",
}
ALL: list["Q"] = []


class Q:
    """One question. body() is called per render so input names stay unique."""

    tone = 0

    def __init__(self, ch, src, no, marks, body, why="", ctx=""):
        self.ch, self.src, self.no, self.marks = ch, src, no, marks
        self.body, self.why, self.ctx = body, why, ctx
        ALL.append(self)

    def html(self, label, qno, tag, standalone=False, tone=""):
        ctx = f'<p class="q-text ctx">{self.ctx}</p>' if standalone and self.ctx else ""
        why = f'<div class="why">{self.why}</div>' if self.why else ""
        return (
            f'<div class="q" data-ch="{self.ch}"{tone} data-qno="{qno}"><div class="q-row"><span class="n">{label}</span>'
            f'<div class="q-main">{tag}{ctx}{self.body()}</div></div>{why}</div>'
        )

    def on_paper(self, label, qno):
        tag = f'<span class="ch-tag" title="{esc(CHAPTERS[self.ch])}">Ch {self.ch}</span>'
        Q.tone = Q.tone % 6 + 1
        return self.html(label, qno, tag, tone=f' data-tone="{Q.tone}"')

    def on_chapter_page(self, n, qno):
        tag = f'<span class="ch-tag src">{esc(SOURCES[self.src])} · {esc(self.no)} · {self.marks:g} mk</span>'
        return self.html(f"{n}.", qno, tag, standalone=True)


def choose(options, answer, marks, labels="a.|b.|c.|d."):
    """Radio group. answer is the option index; labels mirror the paper."""
    name = pp.uid("r")
    tags = labels.split("|")
    rows = "".join(
        f'<label class="opt"><input type="radio" name="{name}" value="{i}" />'
        f'<span class="ol">{tags[i]}</span><span>{o}</span></label>'
        for i, o in enumerate(options)
    )
    return f'<div class="opts" data-unit="radio" data-marks="{marks}" data-answer="{answer}">{rows}</div>'


ABC = "A)|B)|C)"
TF = "i.|ii."


def mcq(ch, src, no, stem, options, answer, why, marks=0.25, labels="a.|b.|c.|d.", fig=None, ctx=""):
    def body():
        return f'<p class="q-text">{stem}</p>{fig() if fig else ""}{choose(options, answer, marks, labels)}'

    return Q(ch, src, no, marks, body, why, ctx)


def tf(ch, src, no, stem, truth, why, marks=0.25):
    return mcq(ch, src, no, stem, ["True", "False"], 0 if truth else 1, why, marks, TF, ctx="True or False:")


def ip(value):
    return r"^\s*" + re.escape(value) + r"(\s*/\s*\d+)?\s*$"


# ---------------------------------------------------------------- drawings
class S:
    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.g, self.t = [], []

    def line(self, x1, y1, x2, y2, dash=False, sw=1.4):
        d = ' stroke-dasharray="4 4"' if dash else ""
        self.g.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}"{d} stroke-width="{sw}"/>')

    def path(self, d, dash=False, sw=1.8):
        a = ' stroke-dasharray="4 4"' if dash else ""
        self.g.append(f'<path d="{d}"{a} stroke-width="{sw}"/>')

    def rect(self, x, y, w, h, r=0, solid=False):
        f = ' fill="currentColor" fill-opacity="0.75"' if solid else ""
        self.g.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{r}"{f}/>')

    def circle(self, x, y, r):
        self.g.append(f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}"/>')

    def router(self, x, y, rx=20, ry=11):
        self.g.append(
            f'<ellipse cx="{x:g}" cy="{y:g}" rx="{rx}" ry="{ry}" fill="currentColor" fill-opacity="0.75"/>'
        )

    def link(self, x, y):
        self.g.append(f'<ellipse cx="{x:g}" cy="{y:g}" rx="30" ry="11"/>')
        self.text(x, y + 4, "Link")

    def pc(self, x, y, w=36, h=26):
        self.rect(x - w / 2, y - h / 2, w, h, 2)
        self.line(x - w / 2 - 5, y + h / 2 + 5, x + w / 2 + 5, y + h / 2 + 5, sw=2.4)

    def arrow(self, x1, y1, x2, y2):
        a = math.atan2(y2 - y1, x2 - x1)
        self.line(x1, y1, x2, y2)
        for s in (-1, 1):
            self.line(x2, y2, x2 - 8 * math.cos(a + s * 0.45), y2 - 8 * math.sin(a + s * 0.45))

    def text(self, x, y, s, anchor="middle", bold=False, rot=None):
        w = ' font-weight="700"' if bold else ""
        r = f' transform="rotate({rot} {x:g} {y:g})"' if rot else ""
        self.t.append(f'<text class="lbl" x="{x:g}" y="{y:g}" text-anchor="{anchor}"{w}{r}>{esc(s)}</text>')

    def out(self):
        return (
            f'<div class="fig"><svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.label)}" '
            f'style="max-width:{self.w}px"><g fill="none" stroke="currentColor">{"".join(self.g)}</g>'
            f'{"".join(self.t)}</svg></div>'
        )


def fig_levels():
    s = S(590, 180, "Signal with four levels carrying the bits 11 10 01 01 00 00 00 10 in one second")
    x0, w, ys = 76, 54, {4: 44, 3: 70, 2: 118, 1: 144}
    bits = ["11", "10", "01", "01", "00", "00", "00", "10"]
    for lvl, y in ys.items():
        s.text(58, y + 4, f"Level {lvl}", "end")
    s.text(28, 14, "Amplitude", "start")
    s.arrow(x0, 164, x0, 18)
    s.arrow(x0, 94, 570, 94)
    d = []
    for i, b in enumerate(bits):
        y = ys[{"11": 4, "10": 3, "01": 2, "00": 1}[b]]
        d.append(f"{'M' if not i else 'L'}{x0 + i * w} {y} L{x0 + (i + 1) * w} {y}")
        s.text(x0 + (i + 0.5) * w, 34, b, bold=True)
        s.line(x0 + (i + 1) * w, 24, x0 + (i + 1) * w, 164, dash=True, sw=1)
    s.path(" ".join(d), sw=2.6)
    s.text(x0 + 8 * w - 6, 112, "1 s", "end")
    s.text(555, 114, "Time")
    return s.out()


def fig_composite():
    s = S(570, 170, "Composite signal that approximates a square wave")
    x0, per, mid, amp = 18, 150, 84, 62
    pts = []
    for i in range(451):
        t = i / 150 * 2 * math.pi
        v = sum(math.sin((2 * k + 1) * t) / (2 * k + 1) for k in range(4)) * 1.15
        pts.append(f"{'M' if not i else 'L'}{x0 + i / 150 * per:.1f} {mid - amp * v:.1f}")
    s.path(" ".join(pts), sw=2.4)
    for c in range(3):
        a = x0 + c * per
        s.path(f"M{a} {mid} V{mid - amp} H{a + per / 2} V{mid + amp} H{a + per} V{mid}", dash=True, sw=1)
    s.arrow(x0, mid, 556, mid)
    s.text(548, mid - 10, "Time", "end")
    return s.out()


def fig_telephone():
    s = S(640, 180, "Telephone network: computer and modem at each end, codec at each end office, toll office in the middle")
    for left in (True, False):
        m = (lambda x: x) if left else (lambda x: 640 - x)
        x = m(8) if left else m(8) - 196
        s.rect(x, 32, 196, 104, 26)
        s.text(m(106), 22, "Customer premises equipment")
        pc_x = m(52)
        s.rect(pc_x - 30, 54, 60, 42, 3)
        s.text(pc_x, 79, "Computer")
        mx = m(150)
        s.rect(mx - 30, 84, 60, 22, 2)
        s.text(mx, 100, "Modem")
        s.line(m(82), 90, m(120), 95)
        s.text(m(106), 128, "Digital (short cable)")
        s.circle(m(248), 95, 14)
        s.line(m(180), 95, m(234), 95)
        s.text(m(248), 72, "Codec")
        s.text(m(248), 128, "End office")
        s.line(m(262), 95, m(304), 95)
    s.path("M304 106 L320 80 L336 106 Z", sw=1.4)
    s.text(320, 128, "Toll office")
    return s.out()


def fig_sync():
    s = S(590, 230, "Sent bits 1 0 1 1 0 0 0 1 and the same signal read as 12 bits by a receiver with a faster clock")
    x0 = 30
    sent, recv = "10110001", "110111000011"
    w = 60
    def wave(base, high):
        d = [f"M{x0} {base}"]
        cur = base
        for i, b in enumerate(sent):
            y = high if b == "1" else base
            x = x0 + i * w
            if y != cur:
                d.append(f"L{x} {cur} L{x} {y}")
                cur = y
            d.append(f"L{x + w} {y}")
        return " ".join(d)
    s.text(300, 14, "Sent", bold=True)
    s.path(wave(90, 44), sw=2.4)
    for i, b in enumerate(sent):
        s.text(x0 + (i + 0.5) * w, 36, b)
        s.line(x0 + (i + 1) * w, 26, x0 + (i + 1) * w, 94, dash=True, sw=1)
    s.arrow(x0, 90, 560, 90)
    s.text(558, 108, "Time", "end")
    s.path(wave(196, 150), sw=2.4)
    rw = 480 / 12
    for i, b in enumerate(recv):
        s.text(x0 + (i + 0.5) * rw, 142, b)
        s.line(x0 + (i + 1) * rw, 132, x0 + (i + 1) * rw, 200, dash=True, sw=1)
    s.arrow(x0, 196, 560, 196)
    s.text(558, 214, "Time", "end")
    s.text(300, 222, "Received", bold=True)
    return s.out()


def fig_path():
    s = S(640, 215, "Computer A connects through routers B and C to computer D; a second branch from B goes through E to F")
    s.pc(36, 110)
    s.text(36, 150, "A", bold=True)
    s.text(36, 84, "End system")
    s.line(54, 110, 95, 110)
    s.link(125, 110)
    s.line(155, 110, 190, 110)
    s.router(210, 110)
    s.text(210, 136, "B", bold=True)
    s.text(210, 150, "Intermediate")
    for y, r, end in ((52, "C", "D"), (160, "E", "F")):
        s.line(228, 106 if y < 100 else 115, 285, y)
        s.link(315, y)
        s.line(345, y, 385, y)
        s.router(405, y)
        s.text(405, y + 26, r, bold=True)
        s.line(425, y, 465, y)
        s.link(495, y)
        s.line(525, y, 575, y)
        s.pc(600, y)
        s.text(600, y + 36, end, bold=True)
    s.text(405, 32, "Intermediate")
    s.text(600, 26, "End system")
    return s.out()


def fig_bus():
    s = S(440, 300, "Bus with computer A (logical A, physical 10) and E (logical E, physical 87), router interfaces F/20 and T/99, computer H physical 71")
    s.line(20, 72, 330, 72, sw=2.2)
    s.pc(70, 36)
    s.line(70, 54, 70, 72)
    s.text(70, 92, "10 | A")
    s.pc(240, 36)
    s.line(240, 54, 240, 72)
    s.text(240, 92, "87 | E")
    s.text(340, 76, "Bus", "start")
    s.line(300, 72, 300, 160, sw=2)
    s.text(320, 140, "20 | F", "start")
    s.router(300, 170, 26, 13)
    s.text(322, 204, "T | 99", "start")
    s.line(300, 183, 300, 250, sw=3.4)
    s.line(300, 250, 130, 250, sw=3.4)
    s.pc(90, 248)
    s.text(150, 240, "H")
    s.text(150, 272, "71")
    return s.out()


def fig_dll():
    s = S(380, 104, "Data-link layer with a data link control sublayer on top and an empty sublayer below")
    s.rect(30, 6, 340, 92, 2)
    s.text(18, 52, "Data-link layer", rot=-90)
    s.rect(48, 16, 306, 32)
    s.text(201, 37, "Data link control sublayer")
    s.rect(48, 56, 306, 32, solid=True)
    return s.out()


def fig_crc():
    s = S(640, 196, "CRC encoder at the sender and decoder at the receiver, with one item marked Shared between the generator and the checker")
    s.text(125, 14, "Sender", bold=True)
    s.text(515, 14, "Receiver", bold=True)
    s.rect(10, 22, 230, 164, 2)
    s.rect(400, 22, 230, 164, 2)
    s.text(196, 48, "Encoder")
    s.text(444, 48, "Decoder")
    s.rect(24, 32, 110, 24)
    s.text(79, 49, "Dataword")
    s.arrow(79, 56, 79, 96)
    s.text(90, 82, "000", "start")
    s.rect(24, 96, 110, 26)
    s.text(79, 114, "Generator")
    s.arrow(79, 122, 79, 148)
    s.text(89, 140, "Remainder", "start")
    s.rect(24, 148, 180, 24)
    s.text(114, 165, "Codeword")
    s.rect(436, 148, 180, 24)
    s.text(526, 165, "Codeword")
    s.rect(506, 96, 110, 26)
    s.text(561, 114, "Checker")
    s.arrow(561, 148, 561, 122)
    s.rect(410, 62, 84, 24)
    s.text(452, 79, "Syndrome")
    s.line(506, 104, 494, 80)
    s.rect(506, 62, 110, 24)
    s.text(561, 79, "Decision logic")
    s.arrow(561, 62, 561, 48)
    s.rect(506, 30, 110, 18)
    s.text(561, 44, "Dataword")
    s.arrow(320, 109, 136, 109)
    s.arrow(320, 109, 504, 109)
    s.text(320, 100, "Shared", bold=True)
    s.arrow(204, 160, 434, 160)
    s.text(320, 152, "Unreliable transmission")
    return s.out()


def fig_as():
    s = S(600, 312, "Four autonomous systems. Routers R1, R2, R3 and R4 each connect to another autonomous system by a dashed link")
    for x, y, off in ((10, 30, 0), (340, 30, 70), (10, 182, 0), (340, 182, 70)):
        s.rect(x, y, 250, 100, 2)
        s.text(x + 125, y - 8 if y < 100 else y + 118, "Autonomous system")
        a, b, c = (x + 34 + off, y + 72), (x + 90 + off, y + 30), (x + 144 + off, y + 74)
        s.line(*a, *b)
        s.line(*b, *c)
        s.line(*a, *c)
        for p in (a, b, c):
            s.router(*p, rx=10, ry=6)
    pts = {"R1": (206, 62), "R2": (392, 62), "R3": (392, 256), "R4": (206, 256)}
    s.line(*pts["R1"], *pts["R2"], dash=True, sw=1.8)
    s.line(*pts["R2"], *pts["R3"], dash=True, sw=1.8)
    s.line(*pts["R3"], *pts["R4"], dash=True, sw=1.8)
    for name, (x, y) in pts.items():
        s.router(x, y, 22, 12)
        s.text(x + (34 if name in ("R2", "R3") else -34), y - 14, name, bold=True)
    s.line(110, 60, 184, 62)
    s.line(410, 70, 444, 102)
    s.line(414, 256, 434, 254)
    s.line(164, 256, 184, 256)
    return s.out()


def fig_forward():
    s = S(600, 340, "Router R1 with interfaces m0 to 180.70.65.128/25, m1 to 201.4.16.0/22, m2 to 180.70.65.192/26 and m3 to 201.4.22.0/24; a default router leads to the rest of the Internet")
    cx, cy = 300, 142
    s.rect(cx - 90, 6, 180, 60, 2)
    s.text(cx, 26, "180.70.65.128/25")
    s.text(cx, 56, "180.70.65.135/25")
    s.line(cx, 66, cx, cy - 12)
    s.text(cx + 8, 108, "m0", "start")
    s.rect(6, cy - 30, 170, 60, 2)
    s.text(91, cy - 10, "201.4.16.0/22")
    s.text(91, cy + 20, "201.4.16.2/22")
    s.line(176, cy, cx - 22, cy)
    s.text(232, cy - 8, "m1")
    s.rect(424, cy - 30, 170, 60, 2)
    s.text(509, cy - 10, "201.4.22.0/24")
    s.text(509, cy + 20, "201.4.22.3/24")
    s.line(cx + 22, cy, 424, cy)
    s.text(368, cy - 8, "m3")
    s.router(cx, cy, 24, 12)
    s.text(cx + 34, cy + 22, "R1", "start", bold=True)
    s.text(cx - 8, cy + 30, "m2", "end")
    s.line(cx, cy + 12, cx, 190)
    s.rect(cx - 90, 190, 180, 60, 2)
    s.text(cx, 210, "180.70.65.194/26")
    s.text(cx, 240, "180.70.65.192/26")
    s.line(cx, 250, cx, 298)
    s.text(cx - 8, 282, "180.70.65.200/26", "end")
    s.router(cx, 310, 24, 12)
    s.line(cx + 24, 310, 430, 310)
    s.rect(430, 288, 150, 44, 16)
    s.text(505, 315, "Rest of the Internet")
    return s.out()


def fig_model_star():
    s = S(600, 170, "Model answer: two offices, each a star of computers around a switch, joined by one link")
    for left, names, n in ((True, "Dariya office", 5), (False, "Al Waha office", 4)):
        cx = 170 if left else 430
        s.text(cx - (70 if left else -70), 16, names, bold=True)
        s.rect(cx - 22, 72, 44, 24, 2)
        s.text(cx, 89, "Hub")
        for i in range(n):
            y = 30 + i * (110 / (n - 1))
            x = 40 if left else 560
            s.pc(x, y, 26, 16)
            s.line(x + (13 if left else -13), y, cx + (-22 if left else 22), 84)
    s.line(192, 84, 408, 84, sw=2.2)
    s.text(300, 76, "Link between offices")
    return s.out()


def fig_model_isp():
    s = S(620, 300, "Model answer: home connects to a Tier 3 ISP, then a Tier 2 ISP, then a Tier 1 ISP. Tier 1 ISPs meet at private peering points; Tier 2 ISPs meet at an IXP")
    tiers = [(44, "Tier 1 ISP", "International"), (140, "Tier 2 ISP", "National"), (236, "Tier 3 ISP", "Local")]
    for y, name, cover in tiers:
        s.text(10, y + 22, cover, "start")
        for x in (190, 410):
            s.rect(x, y, 130, 34, 3)
            s.text(x + 65, y + 22, name)
    for x in (255, 475):
        s.line(x, 78, x, 140)
        s.line(x, 174, x, 236)
    s.line(320, 61, 410, 61, sw=2.2)
    s.text(365, 24, "Private peering point")
    s.line(365, 28, 365, 61)
    s.line(320, 157, 410, 157, sw=2.2)
    s.text(365, 150, "IXP")
    s.line(255, 270, 255, 284)
    s.text(255, 296, "Your home computer", bold=True)
    return s.out()


def pcm_blanks():
    def box(inner, cls="pcm-box"):
        return f'<div class="{cls}">{inner}</div>'

    down = '<div class="pcm-down" aria-hidden="true">↓</div>'
    a = S(150, 44, "Analog waveform")
    a.path("M4 30 C24 2 36 2 50 26 C60 44 68 44 78 24 C92 -4 112 6 146 26", sw=2)
    d = S(150, 34, "Digital pulses")
    d.path("M4 28 H26 V8 H46 V28 H78 V8 H94 V28 H110 V8 H124 V28 H146", sw=2)
    blank = lambda p, m, label, show: txt("", m, label, show=show, pattern=p, wide=True)
    col1 = (
        box(a.out() + blank("analog", 0.25, "Input signal", "Analog signal"), "pcm-box soft") + down
        + box(blank("sampl", 0.25, "First process", "Sampling")) + down
        + box(blank("pam|sampl|pulse", 0.25, "Output of the first process", "PAM signal (sampled signal)"), "pcm-box soft")
    )
    col2 = (
        box(blank("quanti", 0.25, "Second process", "Quantization")) + down
        + box(blank("quanti", 0.25, "Output of the second process", "Quantized signal"), "pcm-box soft") + down
        + box("Binary encoding", "pcm-box dark")
    )
    col3 = (
        box('<span class="mono">0001100000100110 …</span><br />Binary data', "pcm-box soft") + down
        + box("Line coding", "pcm-box dark") + down
        + box(d.out() + blank("digital", 0.25, "Final signal", "Digital signal"), "pcm-box soft")
    )
    return (
        '<div class="pcm"><div class="pcm-col">' + col1 + '</div><div class="pcm-next" aria-hidden="true"></div>'
        '<div class="pcm-col">' + col2 + '</div><div class="pcm-next" aria-hidden="true"></div>'
        '<div class="pcm-col">' + col3 + "</div></div>"
    )


def frame_table():
    rows = (
        ("Frame sent by computer A", "10", "20"),
        ("Frame sent by the router", "99", "71"),
    )
    body = ""
    for name, src, dst in rows:
        body += (
            f"<tr><td>{name}</td><td>{txt(src, 0.125, name + ' source physical')}</td>"
            f"<td>{txt(dst, 0.125, name + ' destination physical')}</td>"
            f"<td>{txt('A', 0.125, name + ' source logical')}</td>"
            f"<td>{txt('H', 0.125, name + ' destination logical')}</td></tr>"
        )
    return (
        '<table class="ptable stack table-stack-labels center"><thead><tr><th>Frame</th><th>Source physical</th>'
        "<th>Destination physical</th><th>Packet source (logical)</th><th>Packet destination (logical)</th></tr></thead>"
        f"<tbody>{body}</tbody></table>"
    )


def vlsm_table():
    rows = (
        ("Network B (118 hosts)", "25", "204.15.5.0", "204.15.5.1", "204.15.5.126", "204.15.5.127"),
        ("Network A (50 hosts)", "26", "204.15.5.128", "204.15.5.129", "204.15.5.190", "204.15.5.191"),
    )
    body = ""
    for name, pre, net, first, last, bcast in rows:
        cells = [txt(pre, 0.4, name + " prefix", ph="/")]
        for v, lab in ((net, "network"), (first, "first valid"), (last, "last valid"), (bcast, "broadcast")):
            cells.append(txt("", 0.4, f"{name} {lab}", show=v, pattern=ip(v)))
        body += f"<tr><td>{name}</td>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
    return (
        '<table class="ptable stack table-stack-labels center"><thead><tr><th>Subnet</th><th>Prefix</th>'
        "<th>Network address</th><th>First valid host</th><th>Last valid host</th><th>Broadcast</th></tr></thead>"
        f"<tbody>{body}</tbody></table>"
    )


def forwarding_table():
    rows = (
        ("180.70.65.192/26", "—", "m2"),
        ("180.70.65.128/25", "—", "m0"),
        ("201.4.22.0/24", "—", "m3"),
        ("201.4.16.0/22", "—", "m1"),
        ("Default", "180.70.65.200", "m2"),
    )
    body = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return (
        '<table class="ptable center"><thead><tr><th>Network address/mask</th><th>Next hop</th>'
        f"<th>Interface</th></tr></thead><tbody>{body}</tbody></table>"
    )


# ---------------------------------------------------------------- Quiz 1
q1 = {}
q1["1a"] = tf(1, "q1", "Q1a", "Well-defined layers interfaces allow changing the implementation of one layer with a completely different implementation without affecting the other layers.", True,
              "Layers talk only through their interfaces, so one layer's implementation can be replaced while its interface stays the same.")
q1["1b"] = tf(1, "q1", "Q1b", "Physical and data link are implemented in <i>hardware</i> in the network interface card (NIC)", True,
              "The NIC holds the physical and data link layers. The upper layers run in software.")
q1["1c"] = tf(1, "q1", "Q1c", "Semantics of protocol means structure or format of the data message, and their order.", False,
              "That describes <b>syntax</b>. Semantics is the meaning of each section of bits.")
q1["1d"] = tf(1, "q1", "Q1d", "National ISPs (Tier-2 ISPs) connect to each other at <b>private peering points.</b>", False,
              "National ISPs interconnect at IXPs (public peering). Private peering points are how international ISPs connect.")

OSI = ["Physical", "Data Link", "Network", "Transport", "Session", "Presentation", "Application"]


def q1_match():
    rows = (
        ("Packet delivery from source to destination.", "Network"),
        ("Deals with Physical characteristics of transmission medium", "Physical"),
        ("Deals with Physical addresses and node to node delivery of frames", "Data Link"),
        ("Routers works on this layer", "Network"),
    )
    body = "".join(
        f"<tr><td class=\"num\">{i}</td><td>{t}</td><td>{sel(OSI, a, 0.25, 'OSI layer for row ' + str(i))}</td></tr>"
        for i, (t, a) in enumerate(rows, 1)
    )
    return f'<p class="q-text">Match the following table with appropriate OSI Layers.</p><table class="ptable">{body}</table>'


q1["2"] = Q(1, "q1", "Q2", 1, q1_match, "Network layer: source-to-destination packets and routers. Data link: node-to-node frames and physical addresses. Physical: the medium itself.")


def q1_robust():
    opts = ["The network still works", "The whole network fails"]
    return (
        '<p class="q-text">For each of the following networks, write about is the <b>network robust</b> if one computer connection fails?</p>'
        f'<p class="q-text sub">i. Five devices arranged in a star topology {sel(opts, opts[0], 0.5, "Star topology")}</p>'
        f'<p class="q-text sub">ii. Five devices arranged in a ring topology {sel(opts, opts[1], 0.5, "Ring topology")}</p>'
    )


q1["3"] = Q(1, "q1", "Q3", 1, q1_robust, "In a star, only the device on the failed link drops out. In a simple ring, a single break stops the signal going around, so the entire network fails.")


def q1_frames():
    return (
        '<p class="q-text">Computer with IP address A wants to send packet to computer IP address H. Show the Packet and frames encapsulated by source computer A and then by the next node Router.</p>'
        + fig_bus() + frame_table()
    )


q1["4"] = Q(1, "q1", "Q4", 1, q1_frames, "Logical addresses A and H stay the same end to end. Physical addresses change on every hop: 10 to 20 on the first link, then 99 to 71 after the router.")


def q1_company():
    model = "<p>Each office is a star: its computers connect to one central hub or switch (5 at one office, 4 at the other). The two central devices are then linked to join the offices.</p>" + fig_model_star()
    return (
        '<p class="q-text">A new company XYZ has opened in KSA. The company is planning to have two offices; one in Al Waha, Riyadh and other one in Dariya, Riyadh. Company has hired 5 employees for Riyadh office and 4 employees for Jeddah office. The company wants to establish a network between the two offices.</p>'
        '<p class="q-text sub">i. Draw a network diagram for the company XYZ two offices using <b>star topology</b>. Sketch it on paper, then compare.</p>'
        + written(0.5, model, lines=2, label="Describe your diagram")
        + f'<p class="q-text sub">ii. Name the <b>type of network</b> you designed. {txt("", 0.5, "Type of network", show="MAN (Metropolitan Area Network)", pattern=r"^\s*man\b|metropolitan")}</p>'
    )


q1["5"] = Q(1, "q1", "Q5", 1, q1_company, "Al Waha and Dariya are both in Riyadh, so a network spanning one city is a <b>MAN</b>, not a WAN. The paper mentions Jeddah by mistake: the graded copy corrected WAN to MAN.")


# ---------------------------------------------------------------- Quiz 2
q2 = {}
q2["1"] = mcq(3, "q2", "Q1", "To separate one frame from another a ________ is added at the beginning and end of the frame.", ["CRC", "Flag", "Stuff Bits"], 1,
              "Framing marks each frame's start and end with a flag. Stuffing only protects flag patterns that appear inside the data.", labels=ABC)
q2["2"] = mcq(4, "q2", "Q2", "A2:34:45:11:92:F1 is ________ Physical address.", ["Unicast", "Multicast", "Broadcast"], 0,
              "Check the second hex digit from the left: 2 is even, so the last bit of the first byte is 0 and the address is <b>unicast</b> (Chapter 4 slides, even = unicast, odd = multicast). The graded paper ticked Multicast, which contradicts that rule.", labels=ABC)
q2["3"] = mcq(3, "q2", "Q3", "If the receiver using <b>checksum technique</b> gets result a non zero value, the receiver will discard that data word.", ["True", "False"], 0,
              "The receiver accepts only when the checked result is zero. Any non-zero result means an error, so the data word is discarded.", labels="a.|b.")
q2["4"] = mcq(3, "q2", "Q4", "Reed-Solomon code used today for both detection and correction is a ____ code.", ["Block code", "Cyclic code", "Checksum code"], 1,
              "Reed-Solomon is a cyclic code. Block code is the wider family, and a checksum detects errors only.", labels=ABC)


def q2_mac():
    return (
        '<p class="q-text">In which case the data link layer does need a second Sub Layer called MAC.</p>' + fig_dll()
        + txt("", 0.25, "Case that needs the MAC sublayer", pattern="broadcast|multi.?access|multiple.?access|shared", show="Broadcast (shared, multiple-access) links", wide=True)
    )


q2["5"] = Q(3, "q2", "Q5", 0.25, q2_mac, "A shared broadcast link has many stations competing for the medium, so it needs MAC to coordinate them. A point-to-point link has only two ends and does not need it.")


def q2_crc():
    return (
        '<p class="q-text">What is shared between the Sender and Receiver computer using CRC technique.</p>' + fig_crc()
        + txt("", 0.25, "What is shared", pattern="generator|divisor|polynomial", show="The divisor (generator polynomial)", wide=True)
    )


q2["6"] = Q(3, "q2", "Q6", 0.25, q2_crc, "Both sides must divide using the same predetermined <b>divisor (generator)</b>. The syndrome is computed only at the receiver.")


def q2_sw():
    return (
        '<p class="q-text">Briefly write three features added in Stop and Wait protocol to improve the Simple Error and Flow Control Protocol?</p>'
        + written(1.5, "<ol><li><b>Acknowledgment:</b> the sender sends one frame at a time and waits for an ACK before sending the next (flow control).</li><li><b>Error detection:</b> a CRC is added to each data frame, and a corrupted frame is silently discarded.</li><li><b>Timer and retransmission:</b> the sender keeps a copy and starts a timer. If no ACK arrives before it expires, it resends the frame.</li></ol><p>Sequence and acknowledgment numbers are also added so the receiver can spot duplicates.</p>", lines=4)
    )


q2["7"] = Q(3, "q2", "Q7", 1.5, q2_sw)


def q2_parity():
    rows = (("00", "001"), ("01", "010"), ("10", "100"), ("11", "111"))
    cells = "".join(f"<tr><td>{d}</td><td>{txt(c, 0.25, 'Codeword for ' + d)}</td></tr>" for d, c in rows)
    return (
        '<p class="q-text">Design an error detection technique for Dataword k=2 and Codeword n=3 using odd parity?</p>'
        '<p class="q-text sub">a. List the valid code words for your technique?</p>'
        f'<table class="ptable center narrow"><thead><tr><th>Dataword</th><th>Codeword</th></tr></thead><tbody>{cells}</tbody></table>'
        f'<p class="q-text sub">b. Calculate the minimum Hamming distance of your designed code? {num(2, 0.5, "Minimum Hamming distance")}</p>'
        f'<p class="q-text sub">c. How many single bit errors can be detected? {num(1, 0.25, "Detectable bit errors")}</p>'
        f'<p class="q-text sub">d. If the receiver using this coding scheme gets a codeword with 2 single bits error, will the receiver able to detect it? {sel(["Yes", "No"], "No", 0.25, "Detect a two-bit error")}</p>'
    )


q2["8"] = Q(3, "q2", "Q8", 2, q2_parity, "Odd parity makes the count of 1s odd in every codeword: 001, 010, 100, 111. Every pair differs in 2 bits, so d<sub>min</sub> = 2 and s = d<sub>min</sub> − 1 = 1. Two flipped bits keep the count odd, turning one valid codeword into another, so the error goes undetected. The answer sheet appended 1 to every dataword (001, 011, 101, 111), which is not odd parity.")


# ---------------------------------------------------------------- Major I
m1 = {}
m1["1"] = mcq(2, "m1", "Q1", "Computer networks are the example of:", ["Analog to Digital transmission", "Digital to Digital Transmission", "Analog to Analog Transmission"], 1,
              "Computers produce digital data and send it as digital signals, which is digital-to-digital conversion (line coding).")
m1["2"] = mcq(2, "m1", "Q2", "The bit rate for the below signal is:", ["12", "8", "16"], 2,
              "Eight signal elements fit in one second and each carries log<sub>2</sub>4 = 2 bits, so the bit rate is 8 × 2 = 16 bps.", fig=fig_levels)
m1["3"] = mcq(2, "m1", "Q3", "Which statement is true about the figure below", ["It is a composite signal with single sine wave in it.", "It is a composite signal with many sine waves in it", "It is a composite signal with only digital signals in it."], 1,
              "A composite signal is the sum of many sine waves. The ripple on each flat top shows the added harmonics.", fig=fig_composite)
m1["4"] = mcq(2, "m1", "Q4", "Figure below is example of Today's Telephone networks; choose the statement true about it.", ["Today's Telephone network is only using Digital transmission", "Today's Telephone network is using combination of Analog and Digital transmissions", "Today's Telephone network is only using Analog Transmission"], 1,
              "The local loop from modem to end office is analog. The codec at the end office converts it, and the trunk between offices is digital.", fig=fig_telephone)
m1["5"] = mcq(2, "m1", "Q5", "Periodic Digital Signals are used mostly in Computer Data Communications.", ["True", "False"], 1,
              "Data communication mostly uses <b>nonperiodic</b> digital signals, because real data does not repeat in a fixed pattern.", labels="a.|b.")
m1["6"] = mcq(2, "m1", "Q6", "Figure below explains the problem between sender and receiver computer which is:", ["Phase disorientation", "distortion", "lacks synchronization"], 2,
              "The receiver's clock runs faster, so 8 sent bits are read as 12. The bit intervals no longer line up, which is a synchronization problem.", fig=fig_sync)


m1["s1"] = Q(2, "m1", "Short 1", 2, lambda: '<p class="q-text">Briefly write in two lines about attenuation in signals? What devices are used to rectify the problem?</p>' + written(2, "<p><b>Attenuation</b> is the loss of signal energy as the signal travels, because the medium resists it. The signal gets weaker with distance.</p><p><b>Fix:</b> amplifiers boost analog signals. Repeaters regenerate digital signals.</p>", lines=4))
m1["s2"] = Q(2, "m1", "Short 2", 2, lambda: '<p class="q-text">Differentiate between Propagation time and Transmission time in your own words.</p>' + written(2, "<p><b>Propagation time</b> is how long one bit takes to travel from one node to the next: distance ÷ propagation speed. It depends on distance and the medium.</p><p><b>Transmission time</b> is how long it takes to put the whole message onto the link: message length in bits ÷ bandwidth. It depends on message size and bandwidth.</p>", lines=5))
m1["s3"] = Q(1, "m1", "Short 3", 2, lambda: '<p class="q-text">The Computer A wants to send data to Computer D. Draw the responsibility/scope of Data link layer, Network layer and transport layer in the communication from A to D.</p>' + fig_path() + written(2, "<ul><li><b>Data link layer:</b> node to node, once per hop (A to B, B to C, C to D). Unit: frame.</li><li><b>Network layer:</b> end to end, host A to host D across all the routers. Unit: packet.</li><li><b>Transport layer:</b> process to process, from a process on A to a process on D. Unit: segment.</li></ul>", lines=4))
m1["s4"] = Q(2, "m1", "Short 4", 2, lambda: '<p class="q-text">Define bandwidth delay product in measuring performance of a channel? What we get in result of this product?</p>' + written(2, "<p>Bandwidth-delay product = bandwidth × delay. Think of the link as a pipe: bandwidth is its cross-section and delay is its length.</p><p>The result is the <b>number of bits that can fill the link</b>, which is the length of the link in bits.</p>", lines=4))


def m1_pcm():
    return (
        f'<p class="q-text">Fill in the missing blanks in sentence below and the figure?</p>'
        f'<p class="q-text sub">{txt("", 0.25, "Technique", pattern="pcm|pulse.?code", show="PCM (Pulse Code Modulation)")} Technique is used to convert '
        f'{txt("", 0.125, "Data type", pattern="analog", show="analog")} data to '
        f'{txt("", 0.125, "Signal type", pattern="digital", show="digital")} signal.</p>'
        + pcm_blanks()
    )


m1["s5"] = Q(2, "m1", "Short 5", 2, m1_pcm, "PCM has three steps: sampling turns the analog signal into PAM pulses, quantization assigns each sample a level, and binary encoding turns levels into bits. Line coding then produces the digital signal.")


def m1_match():
    terms = [("WAN", "G"), ("Star", "H"), ("Logical Address", "F"), ("Port numbers", "D"), ("Routers", "A"), ("MAN", "B"), ("", ""), ("", "")]
    defs = [
        "Devices are used to find best path from Source to Destination computer",
        "Type of network within a city",
        "This network topology is not Robust and entire network fails if one link in network fails",
        "One of the OSI layer uses this address to find the target Process",
        "One of the OSI layer uses this address for sending frames from one node to next node",
        "One of the OSI layer uses this address to send packets from Source computer to Destination computer",
        "Type of networks with covers long distance geographical areas",
        "Topology used mostly in today's LANs",
    ]
    letters = "ABCDEFGH"
    rows = ""
    for (term, ans), d, l in zip(terms, defs, letters):
        pick = sel(list(letters), ans, 0.25, "Match for " + term, cls="blank short") if term else ""
        rows += f'<tr><td class="pick">{pick}</td><td>{term}</td><td><b>{l}.</b> {d}</td></tr>'
    return f'<p class="q-text">Match the following: (each 0.25 marks)</p><table class="ptable match">{rows}</table>'


m1["match"] = Q(1, "m1", "Match", 1.5, m1_match, "Ring (C) and physical address (E) are distractors: no term on the left uses them.")
m1["6isp"] = Q(1, "m1", "Q6 (CLO1)", 2, lambda: '<p class="q-text">Assume we want an internet connection for our home from an ISP. Draw a diagram showing how your home computer will be connected to different tiers of ISPs to access internet. Also name the two types of Connections between different tiers of ISPs?</p><p class="q-text sub">Sketch it on paper, then compare.</p>' + written(2, fig_model_isp() + "<ul><li><b>Private peering points:</b> direct connections owned by the ISPs. International (Tier 1) ISPs connect this way.</li><li><b>Internet Exchange Points (IXP), or public peering:</b> shared facilities run by a third party. National ISPs interconnect this way.</li></ul>", lines=4))


# ---------------------------------------------------------------- Major II
m2 = {}
m2["1"] = mcq(7, "m2", "Q1", "The first address assigned to an organization in classless addressing ________.", ["must be a power of 4", "must be fully divisible by the number of addresses", "must belong to one of the A, B, or C classes"], 1,
              "A classless block must start on a boundary of its own size, so the first address is divisible by the number of addresses.", labels=ABC)
m2["2"] = mcq(7, "m2", "Q2", "What is the first address of a block of classless addresses if one of the addresses is 12.2.2.76/10?", ["12.2.2.0", "12.2.0.0", "12.0.0.0"], 2,
              "Keep the first 10 bits and zero the rest: 12.00000010… becomes 12.00000000.0.0, so 12.0.0.0.", labels=ABC)
m2["3"] = mcq(7, "m2", "Q3", "In a block, the mask in CIDR is /15; we can write the same as.", ["255.254.0.0", "255.255.0.0", "255.224.0.0"], 0,
              "Fifteen 1s: 11111111.11111110.0.0, which is 255.254.0.0.", labels=ABC)
m2["4"] = mcq(7, "m2", "Q4", "Identify the class of the following IPv4 address: <u>192</u>.1.2.3.", ["Class A", "Class B", "Class C"], 2,
              "A first byte from 192 to 223 is Class C.", labels=ABC)


def m2_vlsm():
    return (
        '<p class="q-text">A block with starting address of <b>204.15.5.0/24</b>. Design variable length <b>classless subneting</b> according to the requirement below and also show the <u>valid range of addresses</u> each subnet will have?</p>'
        '<p class="q-text sub"><b>Network A with 50 hosts</b><br /><b>Network B with 118 hosts</b></p>'
        '<p class="hint">To be marked automatically, allocate the largest network first, starting at the beginning of the block.</p>'
        + vlsm_table()
    )


m2["5"] = Q(7, "m2", "Q5", 4, m2_vlsm, "Allocate the biggest first. B needs 118 + 2 = 120 addresses, so a block of 128 (/25): .0 to .127. A needs 50 + 2 = 52, so a block of 64 (/26): .128 to .191. Valid hosts exclude the network and broadcast addresses.")


def m2_base():
    return (
        '<p class="q-text">In 1000Base F stands for 1000: '
        + txt("", 0.125, "Meaning of 1000", pattern=r"1\s*g|1000\s*m|gigabit", show="1 Gbps")
        + " F: " + txt("", 0.125, "Meaning of F", pattern="fib|optic", show="Fiber optic cable") + "</p>"
    )


m2["6"] = Q(4, "m2", "Q6", 0.25, m2_base, "1000Base-F is Gigabit Ethernet over fiber: 1000 Mbps, baseband, F for fiber.")
m2["7"] = mcq(7, "m2", "Q7", "Routers in the path are not allowed to ________.", ["fragment the packet they receive", "decapsulate the packet", "change source or destination address"], 2,
              "Routers may fragment an IPv4 packet when it exceeds the next link's MTU. They never change the source or destination address. Only (a) is marked wrong on the paper and no key is printed, so (c) is keyed from the textbook rule; (b) is the closest alternative, since routers decapsulate only to fragment.", labels=ABC)
m2["8"] = mcq(7, "m2", "Q8", "What is true about Time to Live (TTL) field of IP header:", ["Router discards the packet when it value becomes 1.", "Router discards the packet when it value becomes 0.", "Router gives top priority to that packet when this field has 100."], 1,
              "Each router decrements TTL. When it reaches 0 the packet is discarded, which stops it looping forever.", labels=ABC)
m2["9"] = mcq(3, "m2", "Q9", "Technique/s for sharing the transmission medium using channelization is/are:", ["CDMA", "TDMA", "Both CDMA and TDMA"], 2,
              "Channelization has three methods: FDMA, TDMA and CDMA.")


def m2_routing():
    opts = ["RIP", "BGP", "Both RIP and BGP"]
    return (
        '<p class="q-text">See the below diagram showing R1 and R4, Write will the routers have RIP running or BGP or both?</p>'
        + fig_as()
        + f'<p class="q-text sub">R1: {sel(opts, opts[2], 0.5, "R1")} &nbsp; R4: {sel(opts, opts[2], 0.5, "R4")}</p>'
    )


m2["10"] = Q(8, "m2", "Q10", 1, m2_routing, "R1 and R4 both sit at the edge of an autonomous system. Each runs RIP inside its own AS and BGP to reach the neighbouring AS.")


def m2_forward():
    return (
        '<p class="q-text">What interface the router will choose to forward packet if it gets a packet with destination IP:<u>180.70.65.132</u>. Fill in the blank below:</p>'
        '<div class="fw-grid">' + forwarding_table() + fig_forward() + "</div>"
        f'<p class="q-text sub">Router will choose interface {txt("m0", 0.2, "Interface")} as it use {txt("AND|bitwise AND|ANDing", 0.2, "Operation", show="AND")} operation between '
        f'{txt("", 0.2, "Mask", pattern=r"255\.255\.255\.128|^\s*/?\s*25\s*$", show="255.255.255.128 (/25)")} &amp; '
        f'{txt("", 0.2, "Address", pattern=ip("180.70.65.132"), show="180.70.65.132")}. It gets result '
        f'{txt("", 0.2, "Result", pattern=ip("180.70.65.128"), show="180.70.65.128")}.</p>'
    )


m2["11"] = Q(7, "m2", "Q11", 1, m2_forward, "Try the longest prefix first. /26: .132 AND .192 = .128, which is not 180.70.65.192. /25: .132 AND .128 = .128, which matches 180.70.65.128/25, so the packet leaves on m0.")
m2["12"] = Q(3, "m2", "Q12", 1, lambda: '<p class="q-text">Write the main difference between CSMA and CSMA/CD?</p>' + written(1, "<p><b>CSMA</b> senses the medium before sending, which reduces collisions, but it has no procedure once a collision happens.</p><p><b>CSMA/CD</b> adds collision detection: the station keeps monitoring while it transmits. On a collision it stops, sends a jamming signal, waits a random backoff time and retries.</p>", lines=4))

SCENARIO = "A computer in a LAN with <b>Private IP 10.4.4.65</b> wants to access a web server on internet with <b>IP 200.53.25.67</b>. The gateway of LAN is a router with <b>Public IP 130.50.60.8</b>."
m2["13a"] = Q(7, "m2", "Q13a", 2, lambda: '<p class="q-text">How this computer can access web resources on internet? Write the technique and explain briefly how it works in your own words (minimum 4 lines)?</p>' + written(2, "<p><b>NAT (Network Address Translation).</b> The computer sends the packet to its gateway. The router replaces the private source address 10.4.4.65 with its public address 130.50.60.8 and records the mapping in a translation table, using port numbers (PAT) to tell hosts apart.</p><p>When the reply from 200.53.25.67 comes back, the router looks up the table, restores 10.4.4.65 and forwards the packet into the LAN.</p>", lines=5), ctx=SCENARIO)
m2["13b"] = Q(7, "m2", "Q13b", 2, lambda: '<p class="q-text">The same computer with IP 10.4.4.65 wants to send data within LAN to a computer with IP 10.4.4.89. How the source computer can get the physical address of that computer? Write the protocol and explain briefly how it works in your own words (4 lines atleast)?</p>' + written(2, "<p><b>ARP (Address Resolution Protocol).</b> The source first checks its ARP cache. If the address is missing, it <b>broadcasts</b> an ARP request asking who has 10.4.4.89.</p><p>Every host on the LAN receives it, but only 10.4.4.89 answers, with a <b>unicast</b> ARP reply carrying its MAC address. The source stores the result in its cache and sends the frame.</p>", lines=5), ctx=SCENARIO)
m2["13c"] = Q(7, "m2", "Q13c", 2, lambda: '<p class="q-text">The network administrator of above LAN is tired of manually giving IPs to this LAN of 200 computers? Suggest a solution to make his job easy?</p>' + written(2, "<p><b>DHCP (Dynamic Host Configuration Protocol).</b> A DHCP server automatically leases each computer an IP address, along with the subnet mask, default gateway and DNS server, so nothing has to be configured by hand.</p>", lines=3), ctx=SCENARIO)


# ---------------------------------------------------------------- LMS quizzes
L1 = [
    ("A company has 10 computers that need to be connected in a fully connected mesh topology. How many dedicated links are required?", ["20", "45", "90", "10"], 1, "A fully connected mesh with 10 computers requires 10×9÷2 = 45 dedicated links."),
    ("Scenario: Your company needs to set up a network where devices can be easily added or removed, and failure of one device should not affect others. However, if the central connecting point fails, the entire network stops working. Which topology best fits this scenario?", ["Mesh topology", "Bus topology", "Ring topology", "Star topology"], 3, "A star topology connects devices through a central connecting point, so failure of that point can stop the network."),
    ("In the OSI model, which layer is responsible for moving frames from one hop (node) to the next?", ["Data Link layer", "Transport layer", "Physical layer", "Network layer"], 0, "The Data Link layer is responsible for node-to-node delivery of frames."),
    ("A user wants to send a large file over the Internet. Which of the following correctly describes the flow of data from the user's application to the network cable?", ["Data → Application → Presentation → Session → Transport → Network → Data Link → Physical", "Data → Transport → Network → Data Link → Physical", "Data → Data Link → Network → Transport → Physical", "Data → Network → Transport → Data Link → Physical"], 0, "The OSI data flow toward the medium passes through Application, Presentation, Session, Transport, Network, Data Link, and Physical layers."),
    ("Scenario: Two computers are communicating. Computer A is sending data to Computer B. At the Transport layer of Computer A, a TCP header is added. When Computer B receives the data, which layer will read and process this TCP header?", ["Physical layer of Computer B", "Data Link layer of Computer B", "Transport layer of Computer B", "Network layer of Computer B"], 2, "The Transport layer processes the TCP header at the receiving computer."),
    ("Which type of network connection uses a dedicated link between exactly two devices?", ["Broadcast connection", "Multipoint connection", "Point-to-point connection", "Shared connection"], 2, "A point-to-point connection provides a dedicated link between exactly two devices."),
    ("What is the PDU (Protocol Data Unit) called at the Network layer of the OSI model?", ["Frame", "Segment", "Bit", "Packet or Datagram"], 3, "Packet or datagram is the PDU associated with the Network layer."),
    ("The physical layer is responsible for all of the following EXCEPT:", ["Representation of bits into electrical or optical signals", "Data rate (bandwidth)", "Process-to-process delivery", "Synchronization of bits"], 2, "Process-to-process delivery is a Transport layer responsibility, not a Physical layer responsibility."),
    ("Scenario: You are downloading multiple files simultaneously from a web server. Which layer of the OSI model is responsible for keeping these different application data separate from each other?", ["Network layer", "Transport layer", "Presentation layer", "Session layer"], 3, "The Session layer is responsible for managing sessions and keeping different application activities logically separate."),
    ("In the OSI model, which of the following layers is implemented in hardware (in the Network Interface Card)?", ["Physical and Data Link layers", "Session and Transport layers", "Transport and Network layers", "Application and Presentation layers"], 0, "The Physical and Data Link layers are implemented in the network interface hardware."),
]
l1 = [mcq(1, "l1", f"Q{i}", s, o, a, w, marks=1) for i, (s, o, a, w) in enumerate(L1, 1)]

L2 = [
    (3, "If a CRC generator polynomial has a degree of r, how many zero bits are appended to the dataword during CRC encoding?", ["r + 1 zeros", "2r zeros", "r - 1 zeros", "r zeros"], 3, "The remainder has r bits, so r zeros are appended before dividing."),
    (3, "What is Forward Error Correction (FEC)?", ["A technique to detect and correct a limited number of errors without needing retransmission.", "An encryption standard for securing L2 frames.", "A protocol requiring the sender to resend all corrupted data blocks automatically.", "A mechanism for doubling physical link bandwidth capacity."], 0, "FEC adds enough redundancy for the receiver to repair limited errors by itself, without retransmission."),
    (3, "In p-persistent CSMA, what step does a station take when it finds the medium idle?", ["Sends a polling frame to the central coordinator.", "Transmits immediately with probability 1 without waiting.", "Transmits with probability p, OR waits one time slot with probability (1 - p) and then re-senses.", "Waits a random exponential backoff time before sensing again."], 2, "Transmitting with probability 1 is 1-persistent. p-persistent transmits with probability p, otherwise waits one slot and senses again."),
    (3, "CSMA/CD is widely used in which network topology when a hub is deployed?", ["Mesh topology", "Point-to-point satellite link", "Star topology", "Ring topology"], 2, "Stations cabled to a hub form a physical star, and the hub makes them share one collision domain, so CSMA/CD applies."),
]
l2 = [mcq(ch, "l2", f"Item {i}", s, o, a, w, marks=1) for i, (ch, s, o, a, w) in enumerate(L2, 1)]


# ---------------------------------------------------------------- page shell
def shell(slug, name, title, desc, chip, intro_html, sheets):
    url = f"{SITE}{BASE}{slug}/"
    t, d = esc(title), esc(desc)
    return f"""<!doctype html>
<html lang="en" data-sg-styled>
  <head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
    <link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{t}</title>
    <meta name="description" content="{d}" />
    <link rel="canonical" href="{url}" />
    <meta property="og:title" content="{t}" />
    <meta property="og:description" content="{d}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:type" content="article" />
    <meta property="og:image" content="{SITE}/assets/og-banner.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap"
      rel="stylesheet"
    />
{pp.THEME_BOOT}    <script src="/javascripts/html-theme-sync.js"></script>
    <link rel="stylesheet" href="/styles/cys401-past-paper.css" />
    <link rel="stylesheet" href="/styles/cs331-past-paper.css" />
    <script src="/javascripts/cys401-past-paper.js" defer></script>
    <script src="/javascripts/cs331-paper-fx.js" defer></script>
    <link rel="stylesheet" href="/styles/site-shell.css" />
    <script defer src="/javascripts/site-palette.js"></script>
  </head>
  <body>
    <header class="pp-bar">
      <div class="pp-bar-row">
        <a class="pp-brand" href="#top">{esc(name)}</a>
        <span class="pp-chip term">{esc(chip)}</span>
        <span class="pp-score" id="pp-score" aria-live="polite"></span>
        <div class="pp-actions">
          <div data-page-search-host></div>
          <button class="pp-btn primary" type="button" id="pp-check">Check<span class="long"> all</span></button>
          <button class="pp-btn" type="button" id="pp-reveal" aria-pressed="false" data-short="Answers">Show model answers</button>
          <button class="pp-btn" type="button" id="pp-reset">Reset</button>
          <button class="pp-btn" type="button" onclick="toggleTheme()"><span data-theme-label>Dark</span></button>
        </div>
      </div>
    </header>
    <main class="desk" id="top">
      <section class="pp-intro">
{intro_html}
      </section>
{sheets}
    </main>
  </body>
</html>
"""


def intro(title, lines, extra=""):
    items = "".join(f"<li>{x}</li>" for x in lines)
    return f"        <h1>{esc(title)}</h1>\n        <ul>{items}</ul>{extra}"


def sheet(n, total, body, cls=""):
    return f'<article class="sheet{cls}" aria-label="Page {n} of {total}">{body}</article>'


NAME_LINE = ""
PHOTO_NOTE = "Transcribed from photos of a graded paper. Answers are corrected against the course slides, not copied from the sheet."
CHIP_NOTE = "The tag on each question shows its course chapter."


def build_quiz1():
    Q1 = "all"
    head = (
        '<div class="paper-title">CS-331 (Computer Networks)</div>'
        '<div class="paper-meta"><b>Quiz 1 (5 marks)</b><b>Time (30 minutes)</b>'
        '<b class="marks">Score: <span class="got" data-q="all"></span>/5</b></div>'
    )
    p1 = (
        head + '<p class="part">1. True/ False (1 mark)</p>'
        + "".join(q1[k].on_paper(l, Q1) for k, l in (("1a", "a)"), ("1b", "b)"), ("1c", "c)"), ("1d", "d)")))
        + '<p class="part">(1 mark)</p>' + q1["2"].on_paper("2.", Q1)
    )
    p2 = (
        NAME_LINE + '<p class="part">(1 mark)</p>' + q1["3"].on_paper("3.", Q1)
        + '<p class="part">(1 mark)</p>' + q1["4"].on_paper("4.", Q1)
        + '<p class="part">(1 mark)</p>' + q1["5"].on_paper("5.", Q1)
    )
    return sheet(1, 2, p1) + sheet(2, 2, p2)


def build_quiz2():
    q = "all"
    head = (
        '<div class="paper-title">CS 331</div>'
        '<div class="paper-meta"><b>Quiz 2 (5 marks)</b><b>Time: 30 min</b>'
        '<b class="marks">Score: <span class="got" data-q="all"></span>/5</b></div>'
        '<p class="part center">Questions 1 - 6 = each 0.25 marks</p>'
    )
    p1 = head + "".join(q2[k].on_paper(f"{k}.", q) for k in "12345")
    p2 = NAME_LINE + q2["6"].on_paper("6.", q) + '<p class="part">(1.5 marks)</p>' + q2["7"].on_paper("7.", q)
    p3 = NAME_LINE + '<p class="part">(2 marks)</p>' + q2["8"].on_paper("8.", q)
    return sheet(1, 3, p1) + sheet(2, 3, p2) + sheet(3, 3, p3)


def build_major1():
    head = (
        '<div class="paper-title">CS 331 - Major Exam I - Semester 181</div>'
        '<div class="paper-meta center"><b>Time Duration: 1 hour</b><b>Marks = 15</b>'
        '<b class="marks">Score: <span class="got" data-q="all"></span>/15</b></div>'
        '<div class="paper-title small">VERSION A</div>'
        '<div class="clo-bar"><span>Course Learning outcome 2:</span><span>Total ( <span class="got" data-q="clo2"></span> /11.5)</span></div>'
        '<p class="part"><u>(Each objective 0.25 marks)</u></p>'
    )
    p1 = head + m1["1"].on_paper("1.", "clo2") + m1["2"].on_paper("2.", "clo2") + m1["3"].on_paper("3.", "clo2")
    p2 = NAME_LINE + m1["4"].on_paper("4.", "clo2") + m1["5"].on_paper("5.", "clo2") + m1["6"].on_paper("6.", "clo2")
    p3 = NAME_LINE + '<p class="part center"><u>Small Answer Questions (each 2 marks)</u></p>' + m1["s1"].on_paper("1.", "clo2") + m1["s2"].on_paper("2.", "clo2")
    p4 = NAME_LINE + m1["s3"].on_paper("3.", "clo2") + m1["s4"].on_paper("4.", "clo2")
    p5 = (
        NAME_LINE + m1["s5"].on_paper("5.", "clo2")
        + '<div class="clo-bar"><span>Course Learning outcome 1:</span><span>Total ( <span class="got" data-q="clo1"></span> /3.5)</span></div>'
        + m1["match"].on_paper("", "clo1")
    )
    p6 = NAME_LINE + '<p class="part">(2 marks)</p>' + m1["6isp"].on_paper("6.", "clo1")
    return "".join(sheet(i + 1, 6, b) for i, b in enumerate((p1, p2, p3, p4, p5, p6)))


def build_major2():
    box = lambda q, m: f'<div class="part-box">Total <span class="got" data-q="{q}"></span> /{m}</div>'
    table = (
        '<table class="ptable center"><thead><tr><th>Part 1/5</th><th>Part 2/4</th><th>Part 3/6</th><th>Total /15</th></tr></thead>'
        '<tbody><tr><td><span class="got" data-q="p1"></span></td><td><span class="got" data-q="p2"></span></td>'
        '<td><span class="got" data-q="p3"></span></td><td><span class="got" data-q="all"></span></td></tr></tbody></table>'
    )
    p1 = (
        '<div class="paper-title">CS331 - Major Exam II - Semester 181</div>'
        '<p class="hint center">The top of the first page was not in the photo.</p>'
        + table
        + box("p1", 5) + '<p class="part center"><u>Part I (0.25X4=1 marks, Q5 = 4 marks)</u></p>'
        + "".join(m2[k].on_paper(f"{k}.", "p1") for k in "123")
    )
    p2 = m2["4"].on_paper("4.", "p1") + '<p class="part">(4 marks)</p>' + m2["5"].on_paper("5.", "p1")
    p3 = box("p2", 4) + '<p class="part center"><u>Part II (Q6-Q9=0.25 marks)</u></p>' + "".join(m2[k].on_paper(f"{k}.", "p2") for k in ("6", "7", "8", "9", "10"))
    p4 = '<p class="part">(1 mark)</p>' + m2["11"].on_paper("11.", "p2") + '<p class="part">(1 mark)</p>' + m2["12"].on_paper("12.", "p2")
    p5 = (
        box("p3", 6) + '<p class="part center"><u>Part III (Q13 = 6 marks)</u></p>'
        f'<p class="q-text"><b>13.</b> {SCENARIO}</p>'
        + "".join(m2[k].on_paper(l, "p3") for k, l in (("13a", "a."), ("13b", "b."), ("13c", "c.")))
    )
    return "".join(sheet(i + 1, 5, b) for i, b in enumerate((p1, p2, p3, p4, p5)))


def build_lms(items, numbers):
    out = []
    for i, (it, n) in enumerate(zip(items, numbers), 1):
        out.append(f'<p class="lms-head"><b>{n}</b><span>Mark <span class="got" data-q="l{i}"></span>/1.00</span></p>' + it.on_paper("", f"l{i}"))
    score = '<p class="lms-score">Score <span class="got" data-q="all"></span>/' + str(len(items)) + "</p>"
    return f'<article class="sheet doc lms">{score}{"".join(out)}</article>'


def build_by_chapter():
    out = []
    for ch, name in CHAPTERS.items():
        items = [q for q in ALL if q.ch == ch]
        if not items:
            continue
        total = sum(q.marks for q in items)
        body = (
            f'<h2 class="ch-head"><span>Chapter {ch}: {esc(name)}</span>'
            f'<span class="marks"><span class="got" data-q="ch{ch}"></span>/{total:g}</span></h2>'
            + "".join(q.on_chapter_page(i, f"ch{ch}") for i, q in enumerate(items, 1))
        )
        out.append(f'<article class="sheet doc chapter" data-ch="{ch}" id="ch{ch}">{body}</article>')
    return "".join(out)


def chapter_nav():
    links = []
    for ch in CHAPTERS:
        c = sum(1 for q in ALL if q.ch == ch)
        if c:
            links.append(f'<a class="pp-chip" data-ch="{ch}" href="#ch{ch}">Ch {ch} · {c}</a>')
    return f'<nav class="ch-nav" aria-label="Jump to chapter">{"".join(links)}</nav>'


PAPERS = [
    dict(slug="01-quiz-1", file="quiz-1", label="Quiz 1 - Chapter 1", ar="الاختبار القصير الأول - الفصل 1", chip="Term not printed", name="CS331 Quiz 1",
         desc="CS331 Quiz 1 past paper, interactive: layers, OSI, topologies, encapsulation.", h1="CS331 Quiz 1 (paper)", notes=[PHOTO_NOTE, CHIP_NOTE], build=build_quiz1, group=0),
    dict(slug="02-major-exam-1-semester-181", file="major-exam-1-semester-181", label="Major Exam I (Semester 181) - Chapters 1 and 2", ar="الاختبار الفصلي الأول (181) - الفصلان 1 و2", chip="Semester 181", name="CS331 Major I",
         desc="CS331 Major Exam I, Semester 181, Version A, interactive: signals, PCM, performance, layers, ISP tiers.", h1="CS331 Major Exam I, Semester 181, Version A", notes=[PHOTO_NOTE, CHIP_NOTE, "Short answers are self-marked: open the model answer, then choose your mark."], build=build_major1, group=0),
    dict(slug="03-quiz-2", file="quiz-2", label="Quiz 2 - Chapters 3 and 4", ar="الاختبار القصير الثاني - الفصلان 3 و4", chip="Term not printed", name="CS331 Quiz 2",
         desc="CS331 Quiz 2 past paper, interactive: framing, MAC addresses, checksum, CRC, Stop-and-Wait, parity.", h1="CS331 Quiz 2 (paper)", notes=[PHOTO_NOTE, CHIP_NOTE, "The paper gives Q8 2 marks without a split, so the marks per part here are an estimate."], build=build_quiz2, group=0),
    dict(slug="04-major-exam-2-semester-181", file="major-exam-2-semester-181", label="Major Exam II (Semester 181) - Chapters 3, 4, 7 and 8", ar="الاختبار الفصلي الثاني (181) - الفصول 3 و4 و7 و8", chip="Semester 181 (inferred)", name="CS331 Major II",
         desc="CS331 Major Exam II past paper, interactive: CIDR, VLSM, forwarding, NAT, ARP, DHCP, routing, CSMA.", h1="CS331 Major Exam II, Semester 181",
         notes=[PHOTO_NOTE, CHIP_NOTE, "The title line is missing from the photo. Major II and Semester 181 are inferred from the 15-mark format, the scope and the partly visible date (19/1…)."], build=build_major2, group=0),
    dict(slug="05-online-quiz-chapter-1", file="online-quiz-chapter-1", label="Online Quiz - Chapter 1", ar="اختبار إلكتروني - الفصل 1", chip="LMS, 10 questions", name="CS331 Online Quiz",
         desc="CS331 online quiz on network topologies and the OSI model, ten questions with answers from the LMS review.", h1="CS331 Online Quiz: Topologies and the OSI Model", notes=["Ten questions from an LMS review. The answers and explanations are the ones the LMS gave.", CHIP_NOTE], build=lambda: build_lms(l1, [f"Question {i}" for i in range(1, 11)]), group=1),
    dict(slug="06-online-quiz-chapter-3", file="online-quiz-chapter-3", label="Online Quiz - Chapter 3 (partial)", ar="اختبار إلكتروني - الفصل 3 (جزئي)", chip="LMS, 4 questions", name="CS331 Online Quiz",
         desc="CS331 online quiz on CRC, forward error correction and CSMA, four questions from the LMS review.", h1="CS331 Online Quiz: Data Link Layer (partial)", notes=["Only four questions of this LMS quiz were photographed. The correct answers are from the LMS review; the explanations were added here.", CHIP_NOTE], build=lambda: build_lms(l2, ["CRC encoding", "Question 4", "p-persistent CSMA", "CSMA/CD"]), group=1),
]
BY_CHAPTER = dict(slug="07-questions-by-chapter", file="questions-by-chapter", label="All Questions by Chapter", ar="جميع الأسئلة حسب الفصل", chip="All sources", name="CS331 by Chapter",
                  desc="Every CS331 past-exam question grouped by course chapter, interactive, with its source paper.", group=2)


# ---------------------------------------------------------------- wrappers, listing, sidebar
GROUPS = ["Past papers", "Online quizzes (LMS)", "Practice by chapter"]
GROUPS_AR = ["الاختبارات السابقة", "الاختبارات الإلكترونية", "تدريب حسب الفصل"]
ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>'


def wrapper(p, idx, ordered):
    s = TEMPLATE.read_text(encoding="utf-8")
    new_title = p["label"]
    old = "/academics/computer-science/cs331/extra-resources/quiz-2-cheat-sheet/"
    new = f"{BASE}{p['slug']}/"
    s = s.replace(old + "quiz-2-cheat-sheet.html", f"{new}{p['file']}.html").replace(old, new)
    s = s.replace("CS331 | Quiz 2 Cheat Sheet study material from Shoug&#x27;s Digital Garden.", esc(p["desc"]))
    s = s.replace("CS331 | Quiz 2 Cheat Sheet study material from Shoug's Digital Garden.", p["desc"])
    s = s.replace("CS331 | Quiz 2 Cheat Sheet", "CS331 | " + esc(new_title))
    s = re.sub(r'(<span class="current">)Quiz 2 Cheat Sheet(</span>)', lambda m: m[1] + esc(new_title) + m[2], s)
    s = re.sub(r'(<h1 class="ch-title uppercase">)Quiz 2 Cheat Sheet(</h1>)', lambda m: m[1] + esc(new_title) + m[2], s)
    s = re.sub(r'title="Quiz 2 Cheat Sheet"', f'title="{esc(new_title)}"', s)
    s = s.replace("ITEM_05 // STUDY MATERIAL", f"ITEM_{idx + 1:02d} // EXAMS")
    s = re.sub(
        r'href="/academics/computer-science/cs331/extra-resources/"(\s*)>Study Material</a',
        lambda m: f'href="{BASE}"{m[1]}>Exams</a',
        s,
    )
    s = re.sub(
        r'class="btn btn-secondary"(\s*)href="/academics/computer-science/cs331/extra-resources/"',
        lambda m: f'class="btn btn-secondary"{m[1]}href="{BASE}"',
        s,
    )
    prev_url = f"{BASE}{ordered[idx - 1]['slug']}/" if idx else BASE
    next_url = f"{BASE}{ordered[idx + 1]['slug']}/" if idx + 1 < len(ordered) else BASE
    s = re.sub(r'href="[^"]*"(\s*)class="nav-link prev"', lambda m: f'href="{prev_url}"{m[1]}class="nav-link prev"', s)
    s = re.sub(r'href="[^"]*"(\s*)class="nav-link next"', lambda m: f'href="{next_url}"{m[1]}class="nav-link next"', s)
    return s


DIR_GROUP_CSS = """
      .dir-group {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: var(--text-purple-bright);
        background-color: var(--bg-void);
        padding: 22px 40px 10px;
        border-bottom: 1px solid var(--border-purple);
      }
"""


def listing(ordered):
    rows = ['<div class="directory-container"><div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span><span>SYS_STATE</span><span></span></div>']
    for g, (en, ar) in enumerate(zip(GROUPS, GROUPS_AR)):
        rows.append(f'<div class="dir-group" data-en-text="{esc(en)}" data-ar-text="{ar}">{esc(en)}</div>')
        for i, p in enumerate(ordered, 1):
            if p["group"] != g:
                continue
            rows.append(
                f'<a href="{BASE}{p["slug"]}/" class="dir-row" data-ar-title="{p["ar"]}">'
                f'<div class="dir-num">{i:02d}</div><div class="dir-title">{esc(p["label"])}</div>'
                '<div class="dir-status"><span class="status-tag available">INTERACTIVE</span></div>'
                f'<div class="dir-arrow">{ARROW}</div></a>'
            )
    rows.append("</div>")
    return "<!-- cs331-exams:start -->\n        " + "\n        ".join(rows) + "\n        <!-- cs331-exams:end -->"


def update_listing(ordered):
    path = EXAMS / "index.html"
    s = path.read_text(encoding="utf-8")
    block = listing(ordered)
    marked = re.compile(r"<!-- cs331-exams:start -->.*?<!-- cs331-exams:end -->", re.S)
    empty = re.compile(r'<style id="empty-section-state-style">.*?</style>\s*<div class="coming-soon-container".*?</div>\s*</div>', re.S)
    if marked.search(s):
        s = marked.sub(lambda _: block, s)
    elif empty.search(s):
        s = empty.sub(lambda _: block, s, count=1)
    else:
        raise SystemExit("exams/index.html: no listing marker or coming-soon block found")
    if ".dir-group {" not in s:
        s = s.replace("      .dir-row {", DIR_GROUP_CSS + "\n      .dir-row {", 1)
    path.write_text(s, encoding="utf-8")


def update_sidebar_json(ordered):
    path = ROOT / "scripts/academic-sidebar.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["children"][BASE] = [
        {"url": f"{BASE}{p['slug']}/", "attrs": f'data-en-text="{esc(p["label"])}" data-ar-text="{p["ar"]}"', "label": p["label"]}
        for p in ordered
    ]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stamp_sidebars():
    """Stamp only the CS331 exam pages; a full sidebar run reformats ~1500 pages."""
    data = sidebar.load_data()
    for path, url in sidebar.page_urls():
        if not url.startswith(BASE):
            continue
        text = Path(path).read_text(encoding="utf-8")
        nav = sidebar.render_nav(data, url)
        text, hits = sidebar.NAV_RE.subn(lambda _: nav, text, count=1)
        if hits:
            Path(path).write_text(text, encoding="utf-8")


def main():
    ordered = PAPERS + [BY_CHAPTER]
    for p in PAPERS:
        folder = EXAMS / p["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        page = shell(p["slug"], p["name"], "CS331 | " + p["label"], p["desc"], p["chip"], intro(p["h1"], p["notes"]), p["build"]())
        (folder / f"{p['file']}.html").write_text(page, encoding="utf-8")

    bc = BY_CHAPTER
    folder = EXAMS / bc["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    empty = [f"Chapter {c}" for c in CHAPTERS if not any(q.ch == c for q in ALL)]
    notes = [
        "The same questions as the past papers, grouped by course chapter. Each one names its source paper.",
        "No photographed question covers " + ", ".join(empty) + ".",
    ]
    page = shell(bc["slug"], bc["name"], "CS331 | " + bc["label"], bc["desc"], bc["chip"], intro("CS331 Questions by Chapter", notes, chapter_nav()), build_by_chapter())
    (folder / f"{bc['file']}.html").write_text(page, encoding="utf-8")

    for i, p in enumerate(ordered):
        (EXAMS / p["slug"] / "index.html").write_text(wrapper(p, i, ordered), encoding="utf-8")
    update_listing(ordered)
    update_sidebar_json(ordered)
    stamp_sidebars()
    print(f"{len(ALL)} questions, {len(ordered)} pages")


if __name__ == "__main__":
    main()
