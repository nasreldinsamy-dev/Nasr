# -*- coding: utf-8 -*-
"""
مولّد الرسومات المعمارية
منزل سكني بشقتين - قطعة أرض 400 م² - نسبة إشغال 60%
طبقاً لقانون البناء الموحد المصري رقم 119 لسنة 2008 والكود المصري للمباني السكنية

يُنتج لوحات A3 بمقياس 1:100 بصيغة SVG.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drawings")
S = 10.0                      # مم لكل متر  (مقياس 1:100)
FONT = "'DejaVu Sans','Noto Sans Arabic',sans-serif"

# ------------------------------------------------------------------ أدوات عامة
def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# محاذاة بصرية -> محاذاة SVG حسب اتجاه النص
ANC = {"rtl": {"middle": "middle", "r": "start", "l": "end",
               "start": "end", "end": "start"},
       "ltr": {"middle": "middle", "r": "end", "l": "start",
               "start": "start", "end": "end"}}
_NUMOK = set(" 0123456789.,:+-*/()=%\u00d7\u00f7\u00b1\u00b2\u0645\u2014")


def auto_dir(t):
    """الأرقام والأبعاد تُكتب من اليسار لليمين، والنصوص العربية بالعكس"""
    return "ltr" if all(ch in _NUMOK for ch in str(t)) else "rtl"


class Sheet:
    """لوحة A3 أفقية 420×297 مم"""
    W, H = 420.0, 297.0
    M = 8.0                                     # هامش

    def __init__(self, no, title, scale="1:100"):
        self.no, self.title, self.scale = no, title, scale
        self.b = []

    def add(self, s):
        self.b.append(s)

    # -------------------------------------------------- إطار اللوحة وخانة البيانات
    def frame(self):
        m, W, H = self.M, self.W, self.H
        tb_h, tb_w = 30.0, 150.0
        x0, y0 = W - m - tb_w, H - m - tb_h
        g = [f'<rect x="{m}" y="{m}" width="{W-2*m}" height="{H-2*m}" '
             f'class="frame"/>',
             f'<rect x="{x0}" y="{y0}" width="{tb_w}" height="{tb_h}" class="frame"/>']
        # خطوط داخلية لخانة البيانات
        g.append(f'<line x1="{x0}" y1="{y0+11}" x2="{x0+tb_w}" y2="{y0+11}" class="thin"/>')
        g.append(f'<line x1="{x0}" y1="{y0+21}" x2="{x0+tb_w}" y2="{y0+21}" class="thin"/>')
        g.append(f'<line x1="{x0+100}" y1="{y0+11}" x2="{x0+100}" y2="{y0+tb_h}" class="thin"/>')
        g.append(f'<line x1="{x0+50}" y1="{y0+21}" x2="{x0+50}" y2="{y0+tb_h}" class="thin"/>')
        t = lambda x, y, s, c="t3", a="middle": (
            f'<text x="{x}" y="{y}" class="{c}" text-anchor="{a}" '
            f'direction="rtl">{esc(s)}</text>')
        g.append(t(x0 + tb_w / 2, y0 + 7.6, "منزل سكني بشقتين - قطعة أرض 400 م²", "t2"))
        g.append(t(x0 + tb_w / 2, y0 + 17.6, self.title, "t2b"))
        g.append(t(x0 + 125, y0 + 26.5, f"مقياس  {self.scale}", "t3"))
        g.append(t(x0 + 75, y0 + 26.5, "رسم ابتدائي (تصميمي)", "t3"))
        g.append(t(x0 + 25, y0 + 26.5, f"لوحة {self.no}", "t2b"))
        return "".join(g)

    def svg(self):
        return (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}mm" '
            f'height="{self.H}mm" viewBox="0 0 {self.W} {self.H}" '
            f'font-family={chr(34)}{FONT}{chr(34)}>\n'
            f'<style>\n'
            f' text{{font-family:{FONT};fill:#111}}\n'
            f' .frame{{fill:none;stroke:#111;stroke-width:0.6}}\n'
            f' .wall{{fill:#3a3a3a;stroke:#111;stroke-width:0.15}}\n'
            f' .wall2{{fill:#6f6f6f;stroke:#111;stroke-width:0.12}}\n'
            f' .slab{{fill:#3a3a3a;stroke:#111;stroke-width:0.15}}\n'
            f' .fill{{fill:#ffffff;stroke:none}}\n'
            f' .thin{{fill:none;stroke:#111;stroke-width:0.15}}\n'
            f' .thin2{{fill:none;stroke:#444;stroke-width:0.25}}\n'
            f' .furn{{fill:#fff;stroke:#666;stroke-width:0.22}}\n'
            f' .furn2{{fill:#eceff1;stroke:#666;stroke-width:0.22}}\n'
            f' .glass{{fill:none;stroke:#111;stroke-width:0.22}}\n'
            f' .dash{{fill:none;stroke:#555;stroke-width:0.2;stroke-dasharray:1.6 1}}\n'
            f' .dashb{{fill:none;stroke:#111;stroke-width:0.3;stroke-dasharray:2.4 1.2}}\n'
            f' .dim{{fill:none;stroke:#111;stroke-width:0.15}}\n'
            f' .green{{fill:#e8f2e2;stroke:#7fa06a;stroke-width:0.25}}\n'
            f' .pave{{fill:#f0ece4;stroke:#9a927f;stroke-width:0.25}}\n'
            f' .void{{fill:#eaf2f8;stroke:#4a7fa5;stroke-width:0.3}}\n'
            f' .sky{{fill:#f7fbfd;stroke:none}}\n'
            f' .t1{{font-size:4.6px;font-weight:bold}}\n'
            f' .t2b{{font-size:3.4px;font-weight:bold}}\n'
            f' .t2{{font-size:3.0px}}\n'
            f' .t3{{font-size:2.6px}}\n'
            f' .t4{{font-size:2.2px}}\n'
            f' .t5{{font-size:1.9px}}\n'
            f' .dimtx{{font-size:2.1px}}\n'
            f'</style>\n'
            f'<rect width="{self.W}" height="{self.H}" fill="#ffffff"/>\n'
            + self.frame() + "\n" + "\n".join(self.b) + "\n</svg>\n")

    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(self.svg())
        print("  ->", os.path.relpath(p, os.path.dirname(OUT)))


class View:
    """نظام إحداثيات بالمتر داخل اللوحة (y لأعلى)"""

    def __init__(self, sheet, ox, oy, s=S):
        self.sh, self.ox, self.oy, self.s = sheet, ox, oy, s

    def P(self, x, y):
        return (self.ox + x * self.s, self.oy - y * self.s)

    # -------------------------------------------------------------- عناصر أولية
    def line(self, x1, y1, x2, y2, c="thin"):
        a, b = self.P(x1, y1), self.P(x2, y2)
        self.sh.add(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" '
                    f'y2="{b[1]:.2f}" class="{c}"/>')

    def rect(self, x1, y1, x2, y2, c="thin", rx=0):
        a, b = self.P(x1, y2), self.P(x2, y1)
        self.sh.add(f'<rect x="{a[0]:.2f}" y="{a[1]:.2f}" width="{abs(b[0]-a[0]):.2f}" '
                    f'height="{abs(b[1]-a[1]):.2f}" rx="{rx}" class="{c}"/>')

    def poly(self, pts, c="thin", close=True):
        d = " ".join(f'{self.P(*p)[0]:.2f},{self.P(*p)[1]:.2f}' for p in pts)
        tag = "polygon" if close else "polyline"
        self.sh.add(f'<{tag} points="{d}" class="{c}"/>')

    def circ(self, x, y, r, c="thin"):
        p = self.P(x, y)
        self.sh.add(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r*self.s:.2f}" '
                    f'class="{c}"/>')

    def arc(self, cx, cy, r, a1, a2, c="thin"):
        import math as _m
        p1 = self.P(cx + r * _m.cos(_m.radians(a1)), cy + r * _m.sin(_m.radians(a1)))
        p2 = self.P(cx + r * _m.cos(_m.radians(a2)), cy + r * _m.sin(_m.radians(a2)))
        sweep = 0 if a2 > a1 else 1
        self.sh.add(f'<path d="M {p1[0]:.2f} {p1[1]:.2f} A {r*self.s:.2f} '
                    f'{r*self.s:.2f} 0 0 {sweep} {p2[0]:.2f} {p2[1]:.2f}" class="{c}"/>')

    def text(self, x, y, s, c="t4", anchor="middle", rot=0, dy=0, dirn=None):
        p = self.P(x, y)
        d = dirn or auto_dir(s)
        tr = (f' transform="rotate({rot} {p[0]:.2f} {p[1]:.2f})"' if rot else "")
        self.sh.add(f'<text x="{p[0]:.2f}" y="{p[1]+dy:.2f}" class="{c}" '
                    f'text-anchor="{ANC[d][anchor]}" direction="{d}"{tr}>'
                    f'{esc(s)}</text>')

    # ------------------------------------------------------------------ حوائط
    def _seg(self, axis, c, a, b, t, cls):
        if b - a <= 1e-9:
            return
        if axis == "h":
            self.rect(a, c - t / 2, b, c + t / 2, cls)
        else:
            self.rect(c - t / 2, a, c + t / 2, b, cls)

    def wall(self, axis, c, a, b, t=0.12, openings=(), cls="wall"):
        """axis='h' (أفقي عند y=c) أو 'v' (رأسي عند x=c) من a إلى b"""
        ops = sorted(openings, key=lambda o: o[0])
        cur = a
        for o in ops:
            st, w = o[0], o[1]
            self._seg(axis, c, cur, st, t, cls)
            cur = st + w
        self._seg(axis, c, cur, b, t, cls)
        for o in ops:
            self._opening(axis, c, t, *o)

    def _opening(self, axis, c, t, st, w, kind, hinge=0, side=1):
        en = st + w
        if axis == "h":
            p1, p2 = (st, c), (en, c)
            n = (0, 1)
        else:
            p1, p2 = (c, st), (c, en)
            n = (1, 0)
        def pt(p, k):
            return (p[0] + n[0] * k, p[1] + n[1] * k)
        # جوانب الفتحة
        self.line(*pt(p1, -t / 2), *pt(p1, t / 2), "thin")
        self.line(*pt(p2, -t / 2), *pt(p2, t / 2), "thin")
        if kind == "win":
            for k in (-t / 2, -t / 6, t / 6, t / 2):
                self.line(*pt(p1, k), *pt(p2, k), "glass")
        elif kind == "open":
            pass
        elif kind in ("door", "dbl"):
            n_leaf = 2 if kind == "dbl" else 1
            lw = w / n_leaf
            for i in range(n_leaf):
                hp = p1 if (hinge == 0) != (i == 1) else p2
                sgn = 1 if hp == p1 else -1
                if axis == "h":
                    hx, hy = hp[0], c
                    self.line(hx, hy, hx, hy + side * lw, "thin2")
                    self.arc(hx, hy, lw, 90 * side, 0 if sgn > 0 else 180, "thin")
                else:
                    hx, hy = c, hp[1]
                    self.line(hx, hy, hx + side * lw, hy, "thin2")
                    a1 = 0 if side > 0 else 180
                    a2 = 90 if sgn > 0 else -90
                    self.arc(hx, hy, lw, a1, a2, "thin")

    # ------------------------------------------------------------------ أبعاد
    def dim(self, x1, y1, x2, y2, off, txt=None, cls="dimtx"):
        """خط أبعاد موازٍ للقطعة (x1,y1)-(x2,y2) بإزاحة off بالمتر"""
        import math as _m
        dx, dy = x2 - x1, y2 - y1
        L = _m.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        ax, ay = x1 + nx * off, y1 + ny * off
        bx, by = x2 + nx * off, y2 + ny * off
        self.line(ax, ay, bx, by, "dim")
        for (px, py) in ((ax, ay), (bx, by)):
            self.line(px - (ux + nx) * .12, py - (uy + ny) * .12,
                      px + (ux + nx) * .12, py + (uy + ny) * .12, "dim")
        self.line(x1, y1, ax + nx * .12, ay + ny * .12, "dim")
        self.line(x2, y2, bx + nx * .12, by + ny * .12, "dim")
        mx, my = (ax + bx) / 2, (ay + by) / 2
        rot = 0 if abs(dx) >= abs(dy) else -90
        t = txt if txt is not None else f"{L:.2f}"
        self.text(mx + nx * .10, my + ny * .10, t, cls, rot=rot, dy=-0.8)

    # ------------------------------------------------------------------ تسميات
    def label(self, x1, y1, x2, y2, name, extra=None, area=True, cs=("t2b", "t5")):
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        a = abs(x2 - x1) * abs(y2 - y1)
        lines = [name]
        if extra:
            lines.append(extra)
        elif area:
            lines.append(f"{abs(x2-x1):.2f} × {abs(y2-y1):.2f} = {a:.1f} م²")
        n = len(lines)
        for i, ln in enumerate(lines):
            self.text(cx, cy, ln, cs[0] if i == 0 else cs[1],
                      dy=(i - (n - 1) / 2) * 3.2)

    def note(self, x, y, s, c="t4", anchor="middle"):
        self.text(x, y, s, c, anchor)

    # ------------------------------------------------------------------ أثاث
    def bed(self, x, y, w, l, face="n"):
        """سرير: (x,y) ركن اللوحة الأدنى، face اتجاه القدم"""
        self.rect(x, y, x + w, y + l, "furn", rx=0.4)
        if face == "n":
            self.rect(x, y + l - 0.45, x + w, y + l, "furn2")
            self.line(x + .1, y + l - .55, x + w - .1, y + l - .55, "thin2")
            for k in (0.12, 0.62):
                self.rect(x + w * k, y + l - .42, x + w * k + w * .26, y + l - .08, "furn2")
        else:
            self.rect(x, y, x + w, y + 0.45, "furn2")
            self.line(x + .1, y + .55, x + w - .1, y + .55, "thin2")
            for k in (0.12, 0.62):
                self.rect(x + w * k, y + .08, x + w * k + w * .26, y + .42, "furn2")

    def sofa(self, x, y, w, d, face="n"):
        self.rect(x, y, x + w, y + d, "furn2", rx=0.25)
        if face == "n":
            self.rect(x, y, x + w, y + d * .32, "furn")
        elif face == "s":
            self.rect(x, y + d * .68, x + w, y + d, "furn")
        elif face == "e":
            self.rect(x, y, x + w * .32, y + d, "furn")
        else:
            self.rect(x + w * .68, y, x + w, y + d, "furn")

    def table(self, cx, cy, w, d, seats=0):
        self.rect(cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2, "furn2", rx=0.2)
        if seats:
            n = seats // 2
            for i in range(n):
                px = cx - w / 2 + w * (i + .5) / n
                self.rect(px - .22, cy + d / 2 + .08, px + .22, cy + d / 2 + .48, "furn")
                self.rect(px - .22, cy - d / 2 - .48, px + .22, cy - d / 2 - .08, "furn")

    def counter(self, x1, y1, x2, y2):
        self.rect(x1, y1, x2, y2, "furn2")

    def sink(self, cx, cy, w=0.5, d=0.4):
        self.rect(cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2, "furn", rx=0.1)

    def cooker(self, cx, cy, w=0.6, d=0.55):
        self.rect(cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2, "furn")
        for sx in (-1, 1):
            for sy in (-1, 1):
                self.circ(cx + sx * w * .22, cy + sy * d * .2, 0.08, "thin")

    def wc(self, cx, cy, face="n"):
        if face in ("n", "s"):
            self.rect(cx - .19, cy - .33, cx + .19, cy + .33, "furn", rx=0.15)
            self.rect(cx - .19, cy + (.20 if face == "s" else -.33), cx + .19,
                      cy + (.33 if face == "s" else -.20), "furn2")
        else:
            self.rect(cx - .33, cy - .19, cx + .33, cy + .19, "furn", rx=0.15)
            self.rect(cx + (.20 if face == "w" else -.33), cy - .19,
                      cx + (.33 if face == "w" else -.20), cy + .19, "furn2")

    def basin(self, cx, cy, w=0.6, d=0.45):
        self.rect(cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2, "furn", rx=0.12)
        self.circ(cx, cy, 0.13, "thin")

    def shower(self, x1, y1, x2, y2):
        self.rect(x1, y1, x2, y2, "furn")
        self.line(x1, y1, x2, y2, "thin")
        self.line(x1, y2, x2, y1, "thin")

    def tub(self, x1, y1, x2, y2):
        self.rect(x1, y1, x2, y2, "furn", rx=0.18)
        self.rect(x1 + .1, y1 + .1, x2 - .1, y2 - .1, "furn2", rx=0.15)

    def wardrobe(self, x1, y1, x2, y2):
        self.rect(x1, y1, x2, y2, "furn2")
        if abs(x2 - x1) > abs(y2 - y1):
            n = max(2, int(abs(x2 - x1) / 0.6))
            for i in range(1, n):
                self.line(x1 + (x2 - x1) * i / n, y1, x1 + (x2 - x1) * i / n, y2, "thin")
        else:
            n = max(2, int(abs(y2 - y1) / 0.6))
            for i in range(1, n):
                self.line(x1, y1 + (y2 - y1) * i / n, x2, y1 + (y2 - y1) * i / n, "thin")

    # ------------------------------------------------------------------ السلم
    def stair(self, x1, y1, x2, y2, n, direction="up", arrow_from="s"):
        """قلبة سلم بعدد n نائمة، الاتجاه رأسي (y) دائماً"""
        self.rect(x1, y1, x2, y2, "thin")
        for i in range(1, n):
            yy = y1 + (y2 - y1) * i / n
            self.line(x1, yy, x2, yy, "thin")
        cx = (x1 + x2) / 2
        if arrow_from == "s":
            self.line(cx, y1 + .25, cx, y2 - .25, "thin2")
            self.poly([(cx, y2 - .1), (cx - .13, y2 - .42), (cx + .13, y2 - .42)],
                      "wall2")
        else:
            self.line(cx, y2 - .25, cx, y1 + .25, "thin2")
            self.poly([(cx, y1 + .1), (cx - .13, y1 + .42), (cx + .13, y1 + .42)],
                      "wall2")

    # ------------------------------------------------------------------ رموز
    def north(self, x, y, r=0.9):
        self.circ(x, y, r, "thin")
        self.poly([(x, y + r * .95), (x - r * .32, y - r * .55), (x, y - r * .2),
                   (x + r * .32, y - r * .55)], "wall2")
        self.text(x, y + r + 0.75, "شمال", "t4")

    def scalebar(self, x, y, n=5):
        for i in range(n):
            self.rect(x + i, y, x + i + 1, y + 0.22,
                      "wall" if i % 2 == 0 else "fill")
        self.rect(x, y, x + n, y + 0.22, "thin")
        for i in range(0, n + 1):
            self.text(x + i, y - 0.30, f"{i}", "t5")
        self.text(x + n / 2, y + 0.75, "مقياس رسم بياني (بالمتر)", "t5")

    def secmark(self, x1, y1, x2, y2, tag="أ"):
        self.line(x1, y1, x2, y2, "dashb")
        for (px, py, s) in ((x1, y1, 1), (x2, y2, -1)):
            self.circ(px, py, 0.45, "fill")
            self.circ(px, py, 0.45, "thin")
            self.text(px, py, tag, "t2b", dy=1.1)


# ===========================================================================
#                           بيانات المشروع الهندسية
# ===========================================================================
PLOT_W, PLOT_D = 20.00, 20.00          # أبعاد قطعة الأرض (م)
SB_F, SB_R, SB_S = 3.00, 2.00, 2.00    # ارتداد أمامي / خلفي / جانبي
BW, BD = 16.00, 15.00                  # أبعاد المبنى  = 240 م² = 60%
T_EXT, T_INT, T_PARTY = 0.25, 0.12, 0.25
FH = 3.30                              # ارتفاع الدور من أرضية لأرضية
SLAB = 0.25
GF_LVL = 0.60                          # منسوب الدور الأرضي فوق الأرض الطبيعية

# ------------------------------------------------- فراغات الشقة (محاور بالمتر)
R = {
    "SALA":   (0.00, 0.00, 8.60, 6.80),
    "SPINE":  (8.60, 0.00, 10.10, 11.60),
    "BED3":   (10.10, 0.00, 13.20, 4.60),
    "FOYER":  (10.10, 4.60, 13.20, 6.80),
    "WELL":   (10.10, 6.80, 13.20, 9.80),
    "BATH1":  (10.10, 9.80, 13.20, 11.60),
    "BED2":   (8.60, 11.60, 13.20, 15.00),
    "KIT":    (0.00, 6.80, 5.60, 10.00),
    "STORE":  (5.60, 6.80, 8.60, 10.00),
    "HALLW":  (0.00, 10.00, 8.60, 11.20),
    "MASTER": (0.00, 11.20, 5.60, 15.00),
    "DRESS":  (5.60, 11.20, 8.60, 12.60),
    "BATH2":  (5.60, 12.60, 8.60, 15.00),
    # الجزء المشترك / نواة الحركة
    "ENT":    (13.20, 0.00, 16.00, 4.20),
    "LOBBY":  (13.20, 4.20, 16.00, 7.40),
    "CSTORE": (13.20, 7.40, 14.50, 9.80),
    "CPASS":  (14.50, 7.40, 16.00, 9.80),
    "STAIR":  (13.20, 9.80, 16.00, 15.00),
}
AR = lambda k: (R[k][2] - R[k][0]) * (R[k][3] - R[k][1])

NAMES_G = {
    "SALA": "صالة الاستقبال والمعيشة والسفرة", "SPINE": "الممر الرئيسي",
    "BED3": "غرفة نوم (3)", "FOYER": "فويية (توزيع)",
    "WELL": "منور مكشوف", "BATH1": "حمام (1)",
    "BED2": "غرفة نوم (2)", "KIT": "المطبخ",
    "STORE": "غسيل ومخزن", "HALLW": "ممر داخلي",
    "MASTER": "غرفة النوم الرئيسية", "DRESS": "دريسنج",
    "BATH2": "حمام (2) خاص", "ENT": "بهو المدخل الرئيسي",
    "LOBBY": "بهو التوزيع", "CSTORE": "عدادات",
    "CPASS": "ممر مشترك", "STAIR": "بئر السلم الخلفي",
}
NAMES_1 = dict(NAMES_G)
NAMES_1.update({"ENT": "مكتب / معيشة", "LOBBY": "مدخل الشقة",
                "CSTORE": "مخزن", "CPASS": "ممر", "STAIR": "بئر السلم الخلفي"})

# --------------------------------------------------------------- فتحات الحوائط
EXT_FRONT = [(1.40, 2.00, "win"), (4.60, 1.60, "dbl", 0, 1),
             (8.90, 1.00, "win"), (10.60, 2.00, "win")]
EXT_REAR = [(0.90, 1.80, "dbl", 0, -1), (6.50, 0.90, "win"),
            (9.10, 1.50, "win"), (11.20, 1.50, "win"), (13.90, 1.60, "win")]
EXT_LEFT = [(2.40, 1.60, "win"), (7.30, 0.90, "door", 0, 1),
            (8.60, 1.20, "win"), (12.00, 1.60, "win")]
EXT_RIGHT = [(1.30, 1.20, "win"), (5.20, 1.40, "win"), (7.90, 1.20, "win"),
             (13.60, 1.20, "win")]

INT_WALLS = [
    ("v", 8.60, 0.25, 14.75, T_INT, [(3.80, 2.20, "open"), (10.00, 1.20, "open")]),
    ("v", 10.10, 0.25, 11.60, T_INT,
     [(1.70, 0.90, "door", 0, -1), (4.90, 1.80, "open"),
      (7.10, 2.40, "win"), (10.30, 0.80, "door", 0, -1)]),
    ("v", 13.20, 0.25, 14.75, T_PARTY,
     [(5.20, 1.00, "door", 0, -1), (7.10, 2.40, "win")]),
    ("v", 5.60, 6.80, 10.00, T_INT, []),
    ("v", 5.60, 11.20, 14.75, T_INT,
     [(11.60, 0.85, "door", 0, 1), (13.20, 0.85, "door", 0, 1)]),
    ("h", 6.80, 0.25, 8.60, T_INT, [(3.60, 0.90, "door", 0, -1)]),
    ("h", 6.80, 10.10, 13.20, T_INT, [(10.55, 2.20, "win")]),
    ("h", 9.80, 10.10, 13.20, T_INT, [(11.00, 1.10, "win")]),
    ("h", 10.00, 0.25, 8.60, T_INT,
     [(1.60, 0.90, "door", 0, 1), (6.40, 0.90, "door", 0, 1)]),
    ("h", 11.20, 0.25, 8.60, T_INT, [(1.80, 0.90, "door", 0, 1)]),
    ("h", 11.60, 8.60, 13.20, T_INT, [(9.00, 0.90, "door", 0, 1)]),
    ("h", 12.60, 5.60, 8.60, T_INT, []),
    ("h", 4.20, 13.20, 16.00, T_INT, [(13.60, 2.00, "open")]),
    ("h", 7.40, 13.20, 16.00, T_INT, [(14.50, 1.50, "open")]),
    ("h", 9.80, 13.20, 16.00, T_INT, [(14.50, 1.50, "open")]),
    ("v", 14.50, 7.40, 9.80, T_INT, [(7.90, 0.80, "door", 0, 1)]),
]


def envelope(v, openings_front):
    """الحوائط الخارجية"""
    v.wall("h", T_EXT / 2, 0, BW, T_EXT, openings_front)
    v.wall("h", BD - T_EXT / 2, 0, BW, T_EXT, EXT_REAR)
    v.wall("v", T_EXT / 2, 0, BD, T_EXT, EXT_LEFT)
    v.wall("v", BW - T_EXT / 2, 0, BD, T_EXT, EXT_RIGHT)


def draw_stair(v, floor):
    """السلم الخلفي: قلبتان بعرض 1.30 م، 10 قوائم لكل قلبة"""
    x1, y1, x2, y2 = R["STAIR"]
    xi1, xi2, yi2 = x1 + T_PARTY / 2, x2 - T_EXT, y2 - T_EXT
    v.text((xi1 + xi2) / 2, y1 + 0.72, "بئر السلم الخلفي", "t2")
    v.text((xi1 + xi2) / 2, y1 + 0.28, "2.80 × 5.20 = 14.6 م²", "t5")
    v.stair(xi1, 10.80, 14.50, 13.32, 9, arrow_from="s")
    v.stair(14.70, 10.80, xi2, 13.32, 9, arrow_from="n")
    v.rect(14.50, 10.80, 14.70, 13.32, "thin")          # فراغ بين القلبتين
    v.line(xi1, 13.32, xi2, 13.32, "thin")
    v.text((xi1 + xi2) / 2, 14.30, "بسطة وسطى", "t5")
    v.text(13.85, 11.90, "طالع", "t5", rot=-90)
    v.text(15.35, 11.90, "نازل" if floor == "g" else "طالع", "t5", rot=-90)
    v.text((xi1 + xi2) / 2, 13.90, "20 قائمة × 16.5 سم", "t5")
    v.text((xi1 + xi2) / 2, 13.62, "نائمة 28 سم", "t5")


def draw_furniture(v):
    # ------------------------------------------------------------- الصالة
    v.sofa(0.42, 1.20, 0.85, 2.40, "e")
    v.sofa(2.20, 0.42, 2.20, 0.85, "n")
    v.sofa(6.10, 1.10, 0.85, 1.70, "w")
    v.table(3.10, 2.35, 1.10, 0.65)
    v.wardrobe(8.10, 1.00, 8.50, 2.90)
    v.table(5.40, 5.00, 1.80, 1.00, seats=6)
    v.text(5.40, 5.95, "ركن السفرة", "t5")
    # ------------------------------------------------------------ غرفة نوم 3
    v.bed(10.70, 2.30, 1.60, 2.00, "n")
    v.wardrobe(12.55, 0.40, 13.05, 2.20)
    # ------------------------------------------------------------ فويية
    v.wardrobe(10.30, 4.78, 11.30, 5.08)
    # ------------------------------------------------------------ غرفة نوم 2
    v.bed(10.30, 11.85, 1.60, 2.00, "s")
    v.wardrobe(12.60, 12.10, 13.05, 14.10)
    # ------------------------------------------------------- غرفة النوم الرئيسية
    v.bed(2.90, 11.50, 1.80, 2.05, "s")
    v.rect(2.42, 11.55, 2.85, 12.05, "furn")
    v.rect(4.75, 11.55, 5.18, 12.05, "furn")
    # ------------------------------------------------------------ دريسنج
    v.wardrobe(5.75, 11.95, 8.45, 12.50)
    # ------------------------------------------------------------ حمام (2)
    v.wc(6.05, 13.20, "n")
    v.basin(7.30, 12.95, 0.70, 0.45)
    v.shower(7.55, 13.95, 8.45, 14.85)
    # ------------------------------------------------------------ حمام (1)
    v.basin(10.80, 11.30, 0.70, 0.45)
    v.wc(11.75, 11.22, "s")
    v.shower(12.30, 9.95, 13.05, 10.95)
    # ------------------------------------------------------------ المطبخ
    v.counter(0.30, 6.92, 3.30, 7.52)
    v.cooker(1.60, 7.22)
    v.counter(0.30, 8.40, 0.90, 9.88)
    v.sink(0.60, 9.20)
    v.counter(5.02, 6.92, 5.52, 9.20)
    v.rect(5.02, 9.25, 5.52, 9.88, "furn2")
    v.text(5.27, 9.57, "ثلاجة", "t5", dy=0.8)
    # ------------------------------------------------------- غرفة الغسيل والمخزن
    v.rect(5.78, 6.95, 6.48, 7.65, "furn")
    v.text(6.13, 7.30, "غسالة", "t5", dy=0.8)
    v.wardrobe(7.92, 6.95, 8.45, 9.85)


def draw_floor(v, floor):
    """floor = 'g' أرضي  |  '1' أول"""
    NAMES = NAMES_G if floor == "g" else NAMES_1
    # أرضيات الفراغات
    for k, (x1, y1, x2, y2) in R.items():
        if k == "WELL":
            continue
        v.rect(x1, y1, x2, y2, "fill")
    # المنور
    wx1, wy1, wx2, wy2 = R["WELL"]
    v.rect(wx1, wy1, wx2, wy2, "void")
    for i in range(1, 7):
        t = i / 7.0
        v.line(wx1, wy1 + (wy2 - wy1) * t, wx1 + (wx2 - wx1) * t, wy1, "dash")
    # الحوائط
    fr = list(EXT_FRONT)
    fr.append((14.00, 1.20, "door", 0, 1) if floor == "g"
              else (14.00, 1.60, "win"))
    envelope(v, fr)
    for (ax, c, a, b, t, ops) in INT_WALLS:
        v.wall(ax, c, a, b, t, ops)
    draw_furniture(v)
    draw_stair(v, floor)
    # الشرفات / التراس
    if floor == "g":
        v.rect(1.20, -1.60, 6.40, 0.0, "pave")
        for i in range(1, 4):
            v.line(6.40, -1.60 + 0.35 * i, 1.20, -1.60 + 0.35 * i, "thin")
        v.text(3.80, -0.95, "تراس أمامي", "t4")
        v.text(3.80, -1.35, "5.20 × 1.60", "t5")
        v.rect(0.60, 15.00, 4.80, 16.20, "pave")
        v.text(2.70, 15.65, "مدخل الحديقة الخلفية", "t5")
    else:
        v.rect(1.20, -1.60, 6.40, 0.0, "fill")
        v.line(1.20, -1.60, 6.40, -1.60, "thin")
        v.line(1.20, -1.45, 6.40, -1.45, "thin")
        v.text(3.80, -0.95, "شرفة الصالة", "t4")
        v.text(3.80, -1.35, "5.20 × 1.60 = 8.3 م²", "t5")
        v.rect(0.60, 15.00, 4.80, 16.20, "fill")
        v.line(0.60, 16.20, 4.80, 16.20, "thin")
        v.text(2.70, 15.70, "شرفة الغرفة الرئيسية", "t5")
        v.text(2.70, 15.30, "4.20 × 1.20", "t5")
    v.rect(-1.00, 7.20, 0.0, 9.60, "pave" if floor == "g" else "fill")
    v.text(-0.50, 8.40, "شرفة خدمة" if floor == "1" else "مدخل جانبي",
           "t5", rot=-90)
    # أسماء الفراغات
    for k, (x1, y1, x2, y2) in R.items():
        if k == "STAIR":
            continue
        if k in ("ENT", "LOBBY", "CSTORE", "CPASS"):
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            cl = "t2" if k in ("ENT", "LOBBY") else "t5"
            v.text(cx + 0.22, cy, NAMES[k], cl, rot=-90)
            v.text(cx - 0.34, cy, f"{AR(k):.1f} م²", "t5", rot=-90)
            continue
        if k == "SPINE":
            v.text((x1 + x2) / 2, 3.00, NAMES[k], "t2b", rot=-90)
            v.text((x1 + x2) / 2 + 0.42, 3.00, f"{AR(k):.1f} م²", "t5", rot=-90)
            continue
        if k == "HALLW":
            v.text(3.40, 10.60, NAMES[k], "t2b")
            continue
        if k == "WELL":
            v.label(x1, y1, x2, y2, NAMES[k],
                    f"3.10 × 3.00 = 9.30 م²")
            continue
        v.label(x1, y1, x2, y2, NAMES[k])


# ===========================================================================
#                     عناصر مساعدة على اللوحة (بالمليمتر)
# ===========================================================================
def stx(sh, x, y, s, c="t3", anchor="middle", dirn=None):
    d = dirn or auto_dir(s)
    sh.add(f'<text x="{x:.2f}" y="{y:.2f}" class="{c}" '
           f'text-anchor="{ANC[d][anchor]}" direction="{d}">{esc(s)}</text>')


def title_block(sh, x, y, w, t):
    sh.add(f'<rect x="{x}" y="{y}" width="{w}" height="8" fill="#3a3a3a"/>')
    sh.add(f'<text x="{x+w/2}" y="{y+5.6}" class="t2b" text-anchor="middle" '
           f'direction="rtl" fill="#ffffff">{esc(t)}</text>')


def info_table(sh, x, y, w, title, rows, rh=5.0, vcol=34.0, foot=None):
    title_block(sh, x, y, w, title)
    yy = y + 8
    for i, (val, lab) in enumerate(rows):
        bg = "#f4f4f4" if i % 2 else "#ffffff"
        sh.add(f'<rect x="{x}" y="{yy}" width="{w}" height="{rh}" fill="{bg}" '
               f'stroke="#bbb" stroke-width="0.15"/>')
        sh.add(f'<line x1="{x+vcol}" y1="{yy}" x2="{x+vcol}" y2="{yy+rh}" '
               f'stroke="#bbb" stroke-width="0.15"/>')
        stx(sh, x + w - 2, yy + rh * 0.68, lab, "t3", "end")
        stx(sh, x + vcol / 2, yy + rh * 0.68, val, "t3", "middle")
        yy += rh
    if foot:
        sh.add(f'<rect x="{x}" y="{yy}" width="{w}" height="{rh}" fill="#e8eef4" '
               f'stroke="#888" stroke-width="0.2"/>')
        stx(sh, x + w - 2, yy + rh * 0.68, foot[1], "t2b", "end")
        stx(sh, x + vcol / 2, yy + rh * 0.68, foot[0], "t2b", "middle")
        yy += rh
    sh.add(f'<rect x="{x}" y="{y}" width="{w}" height="{yy-y}" fill="none" '
           f'stroke="#666" stroke-width="0.3"/>')
    return yy


def sheet_scalebar(sh, x, y, s, n=5):
    View(sh, x, y, s).scalebar(0, 0)


def notes_block(sh, x, y, w, title, lines, lh=4.4):
    title_block(sh, x, y, w, title)
    yy = y + 12.6
    for ln in lines:
        stx(sh, x + w - 2, yy, "• " + ln, "t3", "end")
        yy += lh
    return yy + 1


# ===========================================================================
#                          لوحة 1 : الموقع العام
# ===========================================================================
def sheet_site():
    sh = Sheet("01", "الموقع العام والارتدادات", "1:150")
    v = View(sh, 60, 250, s=200.0 / 30.0)
    # الشارع
    v.rect(-2.0, -4.6, 22.0, 0.0, "pave")
    v.text(10.0, -2.9, "الشارع الرئيسي — عرض 10.00 م", "t2b")
    v.line(-2.0, -2.2, 22.0, -2.2, "dash")
    # الأرض
    v.rect(0, 0, PLOT_W, PLOT_D, "green")
    v.rect(0, 0, PLOT_W, PLOT_D, "thin")
    # خطوط الارتداد
    v.rect(SB_S, SB_F, PLOT_W - SB_S, PLOT_D - SB_R, "dashb")
    # ممر جانبي ومدخل
    v.rect(18.0, 0.0, 20.0, 20.0, "pave")
    v.rect(16.0, 0.0, 17.2, 3.0, "pave")
    v.text(19.0, 10.0, "ممر جانبي مرصوف 2.00 م", "t4", rot=-90)
    v.text(16.6, 1.5, "المدخل الأمامي", "t4", rot=-90)
    # المبنى
    bx, by = SB_S, SB_F
    v.rect(bx, by, bx + BW, by + BD, "fill")
    v.rect(bx, by, bx + BW, by + BD, "wall2")
    v.rect(bx + 0.25, by + 0.25, bx + BW - 0.25, by + BD - 0.25, "fill")
    # تقسيم داخلي مبسط
    for (ax, c, a, b) in (("v", 8.60, 0, 15), ("v", 13.20, 0, 15),
                          ("v", 10.10, 0, 11.60), ("h", 6.80, 0, 8.60),
                          ("h", 10.00, 0, 8.60), ("h", 11.20, 0, 8.60),
                          ("h", 11.60, 8.60, 13.20), ("h", 9.80, 13.20, 16.0),
                          ("h", 4.20, 13.20, 16.0)):
        if ax == "v":
            v.line(bx + c, by + a, bx + c, by + b, "thin")
        else:
            v.line(bx + a, by + c, bx + b, by + c, "thin")
    v.rect(bx + 10.10, by + 6.80, bx + 13.20, by + 9.80, "void")
    v.text(bx + 11.65, by + 8.30, "منور", "t4")
    v.text(bx + 8.0, by + 3.4, "المبنى", "t1")
    v.text(bx + 8.0, by + 1.9, "16.00 × 15.00 = 240.00 م²", "t2b")
    v.text(bx + 6.0, by + 12.9, "السلم الخلفي", "t4")
    v.line(bx + 7.6, by + 12.7, bx + 13.4, by + 11.6, "thin")
    # التراس والشرفات
    v.rect(bx + 1.20, by - 1.60, bx + 6.40, by, "pave")
    v.text(bx + 3.8, by - 0.95, "تراس / شرفة", "t5")
    v.rect(bx + 0.60, by + 15.0, bx + 4.80, by + 16.2, "pave")
    # باب المدخل
    v.poly([(bx + 14.0, by), (bx + 15.2, by)], "wall2", close=False)
    v.line(16.6, 3.0, 16.6, 0.2, "dashb")
    # حدائق
    v.text(10.0, 19.0, "حديقة خلفية", "t2b")
    v.text(1.0, 10.0, "حديقة جانبية", "t4", rot=-90)
    v.text(7.0, 1.2, "حديقة أمامية", "t4")
    # أبعاد
    v.dim(0, 0, 0, PLOT_D, 2.2, "20.00")
    v.dim(0, PLOT_D, PLOT_W, PLOT_D, 2.2, "20.00")
    v.dim(PLOT_W, 0, PLOT_W, PLOT_D, -2.2, "20.00")
    v.dim(0, 0, 0, SB_F, 0.9, "3.00")
    v.dim(0, PLOT_D - SB_R, 0, PLOT_D, 0.9, "2.00")
    v.dim(0, 8.0, SB_S, 8.0, 0.0, "2.00")
    v.dim(PLOT_W - SB_S, 12.0, PLOT_W, 12.0, 0.0, "2.00")
    v.north(24.6, 16.8, 1.1)
    # --------------------------------------------------------------- الجانب
    X, W = 256, 152
    stx(sh, X + W, 22, "الموقع العام", "t1", "end")
    stx(sh, X + W, 28, "Site Plan — 1:150", "t3", "end")
    y = info_table(sh, X, 34, W, "بيانات الأرض والإشغال", [
        ("20.00 × 20.00 م", "أبعاد قطعة الأرض"),
        ("400.00 م²", "مساحة قطعة الأرض"),
        ("60 %", "نسبة الإشغال المسموحة"),
        ("240.00 م²", "أقصى مسطح بناء مسموح"),
        ("16.00 × 15.00 م", "أبعاد المبنى المنفذ"),
        ("240.00 م²", "مسطح البناء بالدور"),
        ("3.00 م", "الارتداد الأمامي"),
        ("2.00 م", "الارتداد الخلفي"),
        ("2.00 م", "الارتداد الجانبي (يمين/يسار)"),
        ("160.00 م²", "صافي المساحات المكشوفة"),
    ], foot=("240 ÷ 400 = 60.0 %", "نسبة الإشغال المحققة"))
    sheet_scalebar(sh, X + 4, 250, 200.0 / 30.0)
    y = notes_block(sh, X, y + 6, W, "ملاحظات الموقع", [
        "المبنى دوران (أرضي + أول) بشقة لكل دور.",
        "المدخل الرئيسي أمامي من الشارع ويؤدي إلى بهو",
        "  مشترك ومنه إلى السلم الخلفي.",
        "ممر جانبي مرصوف عرض 2.00 م يصل الواجهة",
        "  الأمامية بالحديقة الخلفية ويخدم السلم.",
        "المنور المكشوف 3.10 × 3.00 م يخترق الدورين",
        "  لإضاءة وتهوية الحمامات والممر.",
        "أسوار الأرض ارتفاع 2.20 م مبانٍ ودخلات معدنية.",
        "الارتدادات مطابقة لاشتراطات المنطقة، وتُراجع",
        "  مع الإدارة الهندسية قبل التنفيذ.",
    ])
    sh.save("01-الموقع-العام.svg")


# ===========================================================================
#                      لوحة 2 و 3 : المساقط الأفقية
# ===========================================================================
def dim_chains(v):
    v.dim(0, 0, 8.60, 0, -3.2)
    v.dim(8.60, 0, 10.10, 0, -3.2)
    v.dim(10.10, 0, 13.20, 0, -3.2)
    v.dim(13.20, 0, 16.00, 0, -3.2)
    v.dim(0, 0, 16.00, 0, -4.8, "16.00")
    v.dim(0, 0, 0, 6.80, 2.4)
    v.dim(0, 6.80, 0, 10.00, 2.4)
    v.dim(0, 10.00, 0, 11.20, 2.4)
    v.dim(0, 11.20, 0, 15.00, 2.4)
    v.dim(0, 0, 0, 15.00, 4.0, "15.00")
    v.dim(16.00, 0, 16.00, 4.20, -1.8)
    v.dim(16.00, 4.20, 16.00, 7.40, -1.8)
    v.dim(16.00, 7.40, 16.00, 9.80, -1.8)
    v.dim(16.00, 9.80, 16.00, 15.00, -1.8)
    v.dim(0, 15.00, 5.60, 15.00, 2.6)
    v.dim(5.60, 15.00, 8.60, 15.00, 2.6)
    v.dim(8.60, 15.00, 13.20, 15.00, 2.6)
    v.dim(13.20, 15.00, 16.00, 15.00, 2.6)


AREA_ROWS = [("58.5 م²", "صالة استقبال ومعيشة وسفرة"),
             ("21.3 م²", "غرفة النوم الرئيسية"),
             ("15.6 م²", "غرفة نوم (2)"),
             ("14.3 م²", "غرفة نوم (3)"),
             ("17.9 م²", "المطبخ"),
             ("5.6 م²", "حمام (1) مشترك"),
             ("7.2 م²", "حمام (2) خاص"),
             ("4.2 م²", "دريسنج"),
             ("9.6 م²", "غرفة غسيل ومخزن"),
             ("34.5 م²", "ممرات وفويية"),
             ("9.3 م²", "منور مكشوف")]


def sheet_floor(floor):
    if floor == "g":
        sh = Sheet("02", "مسقط الدور الأرضي")
        ttl, sub = "مسقط الدور الأرضي", "Ground Floor Plan — 1:100"
    else:
        sh = Sheet("03", "مسقط الدور الأول")
        ttl, sub = "مسقط الدور الأول", "First Floor Plan — 1:100"
    v = View(sh, 62, 227)
    draw_floor(v, floor)
    dim_chains(v)
    v.secmark(11.65, -2.2, 11.65, 17.2, "أ")
    v.north(-3.2, 16.4, 0.85)
    X, W = 250, 160
    stx(sh, X + W, 22, ttl, "t1", "end")
    stx(sh, X + W, 28, sub, "t3", "end")
    extra = ([("11.8 م²", "مكتب / معيشة صغيرة"),
              ("9.0 م²", "مدخل الشقة (فويية)"),
              ("6.7 م²", "ممر ومخزن")] if floor == "1" else [])
    tot = "198.0 م²" if floor == "g" else "225.4 م²"
    net = "188.7 م²" if floor == "g" else "216.1 م²"
    y = info_table(sh, X, 34, W, "جدول مساحات الشقة",
                   AREA_ROWS + extra + [(net, "صافي المسطح المسقوف (بدون المنور)")],
                   rh=4.6, foot=(tot, "إجمالي مسطح الشقة"))
    rows2 = ([("11.8 م²", "بهو المدخل الرئيسي (مشترك)"),
              ("9.0 م²", "بهو التوزيع (مشترك)"),
              ("6.7 م²", "ممر مشترك وعدادات"),
              ("14.6 م²", "بئر السلم الخلفي")] if floor == "g" else
             [("14.6 م²", "بئر السلم الخلفي")])
    y = info_table(sh, X, y + 5, W, "المساحات المشتركة", rows2, rh=4.6,
                   foot=("240.00 م²", "مسطح الدور الكلي"))
    notes = [
        "جميع الغرف والصالة والمطبخ والحمامين لها إضاءة",
        "  وتهوية طبيعية مباشرة (نسبة الفتحات > 10%).",
        "سمك الحوائط الخارجية 25 سم والقواطيع 12 سم.",
        "ارتفاع الدور 3.30 م والصافي 3.05 م.",
        "الأبعاد بالمتر ومحسوبة على محاور الحوائط.",
    ]
    if floor == "1":
        notes.insert(0, "مسطح بهو المدخل والممر المشترك بالدور الأرضي")
        notes.insert(1, "  يُضم لشقة الدور الأول لتعويض مساحته.")
    notes_block(sh, X, y + 5, W, "ملاحظات", notes)
    sheet_scalebar(sh, X + 4, 250, S)
    sh.save(f"0{2 if floor=='g' else 3}-مسقط-الدور-" +
            ("الأرضي" if floor == "g" else "الأول") + ".svg")


# ===========================================================================
#                        لوحة 4 : القطاع الرأسي أ-أ
# ===========================================================================
L0, L1, L2, L3, L4, L5 = 0.00, 0.60, 3.90, 7.20, 8.20, 10.00


def lvlmark(v, x, y, num, name=""):
    v.poly([(x, y), (x - 0.22, y + 0.34), (x + 0.22, y + 0.34)], "wall2")
    v.line(x - 1.2, y, x + 1.2, y, "thin")
    v.text(x + 1.2, y, num, "t5", "r", dy=-0.9, dirn="ltr")
    if name:
        v.text(x - 1.4, y, name, "t5", "r", dy=-0.9)


def sheet_section():
    sh = Sheet("04", "قطاع رأسي أ-أ", "1:75")
    v = View(sh, 60, 200, s=100.0 / 7.5)
    W_ = 15.0
    # الأرض الطبيعية والأسوار
    v.line(-4.0, L0, 19.0, L0, "thin2")
    for i in range(-8, 47):
        v.line(-4.0 + i * 0.5, L0, -4.3 + i * 0.5, -0.45, "thin")
    v.rect(-2.2, L0, -1.95, 2.20, "wall2")
    v.rect(17.95, L0, 18.2, 2.20, "wall2")
    v.text(-1.0, 1.2, "سور", "t5", rot=-90)
    v.text(18.9, 1.2, "سور", "t5", rot=-90)
    # الأساسات (استرشادي)
    v.rect(0.0, -1.35, W_, L1 - 0.30, "fill")
    v.rect(0.0, -1.35, W_, L1 - 0.30, "dash")
    v.text(7.5, -0.85, "أساسات خرسانية (قواعد منفصلة وسملات) — استرشادي", "t5")
    # بلاطات الأسقف
    for (lv, t) in ((L1, 0.30), (L2, SLAB), (L3, SLAB)):
        if lv == L1:
            v.rect(0.0, lv - t, W_, lv, "slab")
        else:
            v.rect(0.0, lv - t, 5.20, lv, "slab")
            v.rect(8.20, lv - t, W_, lv, "slab")
    # الحوائط المقطوعة
    def cutwall(x, t, win=None):
        for (a, b) in ((L1, L2 - SLAB), (L2, L3 - SLAB)):
            if win:
                s, h = win
                v.rect(x - t / 2, a, x + t / 2, a + s, "wall")
                v.rect(x - t / 2, a + s + h, x + t / 2, b, "wall")
                for k in (-t / 6, t / 6):
                    v.line(x + k, a + s, x + k, a + s + h, "glass")
            else:
                v.rect(x - t / 2, a, x + t / 2, b, "wall")
    v.rect(0.0, L1 - 0.30, 0.25, L4, "wall")          # الحائط الخلفي
    v.rect(W_ - 0.25, L1 - 0.30, W_, L4, "wall")      # الحائط الأمامي
    for (a, b, s, h) in ((L1, L2 - SLAB, 0.90, 1.60), (L2, L3 - SLAB, 0.90, 1.60)):
        v.rect(0.0, a + s, 0.25, a + s + h, "fill")
        for k in (0.08, 0.17):
            v.line(k, a + s, k, a + s + h, "glass")
        v.rect(W_ - 0.25, a + s, W_, a + s + h, "fill")
        for k in (0.08, 0.17):
            v.line(W_ - k, a + s, W_ - k, a + s + h, "glass")
    cutwall(3.40, T_INT, (0.00, 2.20))
    cutwall(5.20, T_INT, (0.90, 1.10))
    cutwall(8.20, T_INT, (0.90, 1.60))
    cutwall(10.40, T_INT, (0.00, 2.20))
    # سور السطح والمنور
    v.rect(0.0, L3, 0.25, L4, "wall")
    v.rect(W_ - 0.25, L3, W_, L4, "wall")
    v.rect(5.20 - T_INT / 2, L3, 5.20 + T_INT / 2, L4 - 0.30, "wall")
    v.rect(8.20 - T_INT / 2, L3, 8.20 + T_INT / 2, L4 - 0.30, "wall")
    v.text(6.70, L4 + 0.55, "منور مكشوف للسماء", "t4")
    for i in range(4):
        v.line(5.6 + i * 0.75, L4 + 0.15, 5.9 + i * 0.75, L4 - 0.15, "dash")
    # غرفة السلم خلف مستوى القطع
    v.rect(0.0, L3, 5.20, L5, "fill")
    v.rect(0.0, L3, 5.20, L5, "dashb")
    v.text(2.60, L5 - 0.95, "غرفة السلم (خلف مستوى القطع)", "t5")
    v.rect(1.2, L5, 2.2, L5 + 0.9, "dash")
    v.text(1.7, L5 + 0.45, "خزان", "t5", dy=0.8)
    # أسماء الفراغات
    rooms = [(0.25, 3.40, "غرفة نوم (2)"), (3.40, 5.20, "حمام (1)"),
             (5.20, 8.20, "منور"), (8.20, 10.40, "فويية"),
             (10.40, W_ - 0.25, "غرفة نوم (3)")]
    for (a, b, nm) in rooms:
        if nm == "منور":
            continue
        v.text((a + b) / 2, L1 + 1.35, nm, "t4")
        v.text((a + b) / 2, L2 + 1.35, nm, "t4")
    v.text(6.70, L1 + 1.35, "منور", "t4")
    v.text(6.70, L2 + 1.35, "منور", "t4")
    v.text(11.60, L3 + 0.45, "سطح المبنى", "t4")
    # مناسيب
    for (lv, n, t) in ((L0, "\u00b1 0.00", "منسوب الأرض الطبيعية"),
                       (L1, "+ 0.60", "أرضية الدور الأرضي"),
                       (L2, "+ 3.90", "أرضية الدور الأول"),
                       (L3, "+ 7.20", "أرضية السطح"),
                       (L4, "+ 8.20", "أعلى سور السطح"),
                       (L5, "+ 10.00", "أعلى غرفة السلم")):
        lvlmark(v, W_ + 0.4, lv, n)
    # أبعاد رأسية
    v.dim(0, L0, 0, L1, 2.0, "0.60")
    v.dim(0, L1, 0, L2, 2.0, "3.30")
    v.dim(0, L2, 0, L3, 2.0, "3.30")
    v.dim(0, L3, 0, L4, 2.0, "1.00")
    v.dim(0, L0, 0, L4, 3.6, "8.20")
    v.text(1.70, L1 + 2.35, "صافي 3.05", "t5")
    v.text(1.70, L2 + 2.35, "صافي 3.05", "t5")
    # أبعاد أفقية
    for (a, b) in ((0, 3.40), (3.40, 5.20), (5.20, 8.20), (8.20, 10.40),
                   (10.40, 15.0)):
        v.dim(a, -1.35, b, -1.35, -0.9)
    v.dim(0, -1.35, W_, -1.35, -2.3, "15.00")
    v.text(-2.9, 3.4, "الواجهة الخلفية", "t4", rot=-90)
    v.text(18.4, 3.4, "الواجهة الأمامية / الشارع", "t4", rot=-90)
    X, W = 300, 110
    stx(sh, X + W, 22, "قطاع رأسي أ-أ", "t1", "end")
    stx(sh, X + W, 28, "Section A-A — 1:75", "t3", "end")
    y = info_table(sh, X, 34, W, "المناسيب والارتفاعات", [
        ("+ 0.60 م", "منسوب أرضية الدور الأرضي"),
        ("3.30 م", "ارتفاع الدور (أرضية لأرضية)"),
        ("3.05 م", "الارتفاع الصافي للدور"),
        ("0.25 م", "سمك البلاطة الخرسانية"),
        ("+ 7.20 م", "منسوب سطح المبنى"),
        ("1.00 م", "ارتفاع سور السطح"),
        ("+ 10.00 م", "أعلى نقطة بالمبنى (غرفة السلم)"),
    ], rh=4.8)
    y = notes_block(sh, X, y + 5, W, "ملاحظات إنشائية", [
        "الهيكل خرسانة مسلحة: قواعد منفصلة + سملات",
        "  + أعمدة + كمرات + بلاطة مصمتة 25 سم.",
        "شبكة الأعمدة في حدود 4.00 – 5.00 م.",
        "المباني طوب أحمر/أسمنتي 25 سم للخارجي",
        "  و 12 سم للقواطيع الداخلية.",
        "عزل مائي للسطح وللحمامات والمنور.",
        "ميول السطح 1.5% نحو مصارف المطر.",
        "الارتفاع الكلي لا يتعدى 1.5 × عرض الشارع",
        "  طبقاً لقانون البناء الموحد.",
    ])
    sheet_scalebar(sh, X, 250, 100.0 / 7.5)
    sh.save("04-قطاع-رأسي-أأ.svg")


# ===========================================================================
#                        لوحة 5 : الواجهة الأمامية
# ===========================================================================
def win(v, x1, x2, y1, y2, mull=2):
    v.rect(x1, y1, x2, y2, "furn2")
    v.rect(x1 + .06, y1 + .06, x2 - .06, y2 - .06, "thin")
    for i in range(1, mull):
        v.line(x1 + (x2 - x1) * i / mull, y1 + .06,
               x1 + (x2 - x1) * i / mull, y2 - .06, "thin")


def sheet_elev():
    sh = Sheet("05", "الواجهة الأمامية (الرئيسية)", "1:75")
    v = View(sh, 52, 210, s=100.0 / 7.5)
    v.line(-3.0, L0, 19.0, L0, "thin2")
    for i in range(-6, 45):
        v.line(-3.0 + i * 0.5, L0, -3.3 + i * 0.5, -0.45, "thin")
    # جسم المبنى
    v.rect(0, L0, BW, L4, "fill")
    v.rect(0, L0, BW, L1, "furn2")                     # سرسيب
    v.rect(0, L3, BW, L4, "furn2")                     # سور السطح
    v.rect(0, L4 - 0.12, BW, L4, "wall2")
    v.rect(0, L2 - 0.30, BW, L2 - 0.05, "furn2")       # حزام أفقي
    v.rect(0, L0, BW, L4, "thin")
    # غرفة السلم والخزانات
    v.rect(13.20, L3, BW, L5, "furn2")
    v.rect(13.20, L5 - 0.12, BW, L5, "wall2")
    win(v, 14.10, 15.10, L5 - 1.70, L5 - 0.55, 2)
    v.rect(14.00, L5, 15.30, L5 + 1.05, "furn")
    v.text(14.65, L5 + 0.42, "خزانات", "t5", dy=0.8)
    # فتحات الدور الأرضي
    win(v, 1.40, 3.40, L1 + 0.90, L1 + 2.80, 2)
    win(v, 4.60, 6.20, L1 + 0.00, L1 + 2.30, 2)
    win(v, 8.90, 9.90, L1 + 1.20, L1 + 2.80, 1)
    win(v, 10.60, 12.60, L1 + 0.90, L1 + 2.50, 2)
    v.rect(14.00, L1, 15.20, L1 + 2.40, "furn2")
    v.rect(14.06, L1, 15.14, L1 + 2.34, "thin")
    v.line(14.60, L1, 14.60, L1 + 2.34, "thin")
    v.text(14.60, L1 + 1.1, "المدخل", "t5", dy=0.8)
    v.rect(13.60, L1 + 2.75, 15.60, L1 + 3.00, "wall2")   # مظلة المدخل
    for i in range(4):
        v.rect(13.80 - 0.0, L0 + 0.15 * i, 15.40, L0 + 0.15 * (i + 1), "thin")
    # تراس أمامي
    v.rect(1.20, L1 - 0.25, 6.40, L1, "furn2")
    v.rect(1.20, L1, 6.40, L1 + 0.60, "fill")
    v.rect(1.20, L1, 6.40, L1 + 0.60, "thin")
    v.text(3.80, L1 + 0.20, "تراس أرضي", "t5", dy=0.8)
    # فتحات الدور الأول
    win(v, 1.40, 3.40, L2 + 0.90, L2 + 2.80, 2)
    win(v, 4.60, 6.20, L2 + 0.00, L2 + 2.30, 2)
    win(v, 8.90, 9.90, L2 + 1.20, L2 + 2.80, 1)
    win(v, 10.60, 12.60, L2 + 0.90, L2 + 2.50, 2)
    win(v, 14.00, 15.60, L2 + 0.90, L2 + 2.50, 2)
    # شرفة الدور الأول
    v.rect(1.20, L2 - 0.25, 6.40, L2, "wall2")
    v.rect(1.20, L2, 6.40, L2 + 1.00, "fill")
    v.rect(1.20, L2, 6.40, L2 + 1.00, "thin")
    for i in range(1, 18):
        v.line(1.20 + i * 0.29, L2 + 0.08, 1.20 + i * 0.29, L2 + 0.92, "thin")
    v.rect(1.20, L2 + 0.92, 6.40, L2 + 1.00, "wall2")
    v.text(3.80, L2 + 1.45, "شرفة الصالة", "t5")
    # مناسيب وأبعاد
    for (lv, t) in ((L0, "\u00b1 0.00"), (L1, "+ 0.60"), (L2, "+ 3.90"),
                    (L3, "+ 7.20"), (L4, "+ 8.20"), (L5, "+ 10.00")):
        lvlmark(v, BW + 0.4, lv, t)
    v.dim(0, L0, 0, L1, 1.6, "0.60")
    v.dim(0, L1, 0, L2, 1.6, "3.30")
    v.dim(0, L2, 0, L3, 1.6, "3.30")
    v.dim(0, L3, 0, L4, 1.6, "1.00")
    v.dim(0, L0, BW, L0, -1.9, "16.00")
    v.text(BW / 2, L5 + 1.9, "الواجهة الأمامية (جهة الشارع)", "t1")
    X, W = 300, 110
    stx(sh, X + W, 22, "الواجهة الأمامية", "t1", "end")
    stx(sh, X + W, 28, "Front Elevation — 1:75", "t3", "end")
    y = info_table(sh, X, 34, W, "التشطيبات الخارجية", [
        ("بياض أسمنتي + دهان واجهات", "الحوائط"),
        ("حجر هاشمي هيصم", "السرسيب والحزام"),
        ("ألوميتال / PVC + زجاج مزدوج", "الشبابيك"),
        ("مصراعان زجاج وخشب معالج", "باب المدخل"),
        ("درابزين معدني + حجر", "الشرفات"),
        ("سور مبانٍ 1.00 م بكرانيش", "سور السطح"),
    ], rh=4.8, vcol=62)
    notes_block(sh, X, y + 5, W, "ملاحظات الواجهة", [
        "الواجهة الأمامية شمالية شرقية التوجيه،",
        "  وتحقق إضاءة جيدة للصالة وغرفة النوم (3).",
        "مظلة خرسانية فوق باب المدخل عرض 2.00 م.",
        "يُفضل كاسرات شمس أفقية 0.40 م أعلى الشبابيك.",
        "منسوب أرضية الدور الأرضي + 0.60 م فوق",
        "  منسوب الرصيف لحماية المبنى من مياه الأمطار.",
    ])
    sheet_scalebar(sh, X, 250, 100.0 / 7.5)
    sh.save("05-الواجهة-الأمامية.svg")


# ===========================================================================
#                         لوحة 6 : مسقط السطح
# ===========================================================================
def sheet_roof():
    sh = Sheet("06", "مسقط السطح")
    v = View(sh, 62, 227)
    v.rect(0, 0, BW, BD, "fill")
    v.rect(0, 0, BW, BD, "thin")
    for (a, b, c, d2) in ((0, 0, BW, 0.25), (0, BD - 0.25, BW, BD),
                          (0, 0, 0.25, BD), (BW - 0.25, 0, BW, BD)):
        v.rect(a, b, c, d2, "wall2")
    v.rect(*R["WELL"], "void")
    v.label(*R["WELL"], "منور مكشوف", "3.10 × 3.00")
    v.rect(*R["STAIR"], "fill")
    v.rect(*R["STAIR"], "wall2")
    v.rect(13.45, 10.05, 15.75, 14.75, "fill")
    v.label(13.20, 9.80, 16.00, 15.00, "غرفة السلم", "2.80 × 5.20")
    v.rect(10.40, 12.20, 12.80, 13.60, "furn2")
    v.text(11.60, 13.00, "خزانات مياه", "t5", dy=-1.0)
    v.text(11.60, 13.00, "2 × 1000 لتر", "t5", dy=2.0)
    v.rect(10.60, 10.40, 12.10, 11.40, "furn2")
    v.text(11.35, 10.70, "سخان شمسي", "t5", dy=0.8)
    for (x, y) in ((1.2, 1.2), (7.4, 1.2), (1.2, 13.8), (7.4, 13.8)):
        v.circ(x, y, 0.22, "thin")
        v.circ(x, y, 0.10, "wall2")
        v.text(x, y - 0.75, "مصرف", "t5")
    for (x1, y1, x2, y2) in ((3.0, 4.2, 1.7, 2.2), (5.8, 4.2, 7.0, 2.4),
                             (3.0, 11.2, 1.7, 12.9), (5.8, 11.2, 7.0, 12.9)):
        v.line(x1, y1, x2, y2, "thin2")
        v.poly([(x2, y2), (x2 + 0.3, y2 + 0.28), (x2 + 0.05, y2 + 0.42)], "wall2")
    v.text(4.3, 3.4, "ميول 1.5%", "t5")
    v.text(4.3, 9.4, "سطح مكشوف — عزل مائي وحراري", "t2b")
    v.rect(1.20, -1.60, 6.40, 0.0, "dash")
    v.text(3.80, -0.9, "سقف شرفة الدور الأول", "t5")
    v.dim(0, 0, BW, 0, -3.2, "16.00")
    v.dim(0, 0, 0, BD, 2.4, "15.00")
    v.north(-3.2, 16.4, 0.85)
    X, W = 250, 160
    stx(sh, X + W, 22, "مسقط السطح", "t1", "end")
    stx(sh, X + W, 28, "Roof Plan — 1:100", "t3", "end")
    notes_block(sh, X, 34, W, "أعمال السطح", [
        "عزل مائي (ممبرين) فوق طبقة ميول خرسانة خفيفة.",
        "عزل حراري 5 سم فوم أسفل بلاط المشايات.",
        "ميول 1.5% نحو 4 مصارف مطر قطر 4 بوصة.",
        "سور مبانٍ ارتفاع 1.00 م حول السطح وحول المنور.",
        "خزانان علويان سعة 1000 لتر لكل شقة.",
        "قواعد خرسانية للخزانات ووحدات التكييف.",
        "غرفة السلم مسقوفة وبها باب خروج للسطح.",
        "السطح حق انتفاع لشقة الدور الأول.",
    ])
    sheet_scalebar(sh, X + 4, 250, S)
    sh.save("06-مسقط-السطح.svg")


if __name__ == "__main__":
    print("إنتاج اللوحات:")
    sheet_site()
    sheet_floor("g")
    sheet_floor("1")
    sheet_section()
    sheet_elev()
    sheet_roof()
    print("تم.")
