"""Small SVG kit for the lecture decks (internal, not for publishing).

The deck page does not load a diagram runtime, so a Mermaid block shows as an empty figure. The decks
therefore carry their diagrams as inline SVG, drawn here in the deck's own colours and fonts.

An SVG is 870 units wide, which is 87u, the content width of a slide (1 unit = 0.1u). Its height is
chosen per diagram and must stay under about 36u (360 units) when it shares a slide with a heading.
"""
import html
import math

INK = "#172a42"
NAVY = "#1d588c"
SOFT = "#46586d"
COPPER = "#b4762e"
LINE = "#c3cfdd"
DEEP = "#0c2238"
PAPER = "#f5f7fa"
WHITE = "#ffffff"
TINT = "#e6eef6"          # light navy tint for headers
WARM = "#f6ead9"          # light copper tint

SANS = "Inter, system-ui, sans-serif"
MONO = "'Plex Mono', ui-monospace, monospace"
HEAD = "'Chakra Petch', sans-serif"


def esc(s):
    return html.escape(str(s), quote=False)


class Box:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def a(self, side, t=0.5):
        """Anchor on a side: 'l', 'r', 't' or 'b', t is the fraction along that side."""
        if side == "l":
            return (self.x, self.y + self.h * t)
        if side == "r":
            return (self.x + self.w, self.y + self.h * t)
        if side == "t":
            return (self.x + self.w * t, self.y)
        return (self.x + self.w * t, self.y + self.h)

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2


class Svg:
    def __init__(self, name, h, w=870, label=""):
        self.name, self.w, self.h, self.label = name, w, h, label
        self.parts = []

    # ---- low level ---------------------------------------------------------
    def raw(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=19, anchor="start", weight=400, fill=INK, font=SANS, italic=False, spacing=None):
        style = ' font-style="italic"' if italic else ""
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        self.raw(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-family="{font}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"{style}{ls}>{esc(s)}</text>')

    def lines(self, x, y, rows, size=19, gap=1.3, anchor="start", **kw):
        """Several lines of text; y is the baseline of the first."""
        for i, r in enumerate(rows):
            self.text(x, y + i * size * gap, r, size=size, anchor=anchor, **kw)

    def rect(self, x, y, w, h, fill=WHITE, stroke=NAVY, sw=2, rx=8, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, pts, stroke=NAVY, sw=2.2, dash=None, start=None, end=None):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        ms = f' marker-start="url(#{self.name}-{start})"' if start else ""
        me = f' marker-end="url(#{self.name}-{end})"' if end else ""
        self.raw(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"{da}{ms}{me}/>')

    def circle(self, x, y, r, fill=NAVY, stroke=None):
        s = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
        self.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{s}/>')

    # ---- boxes -------------------------------------------------------------
    def cls(self, x, y, name, attrs=(), ops=(), stereo=None, w=None, row=25, size=16, accent=False, dashed=False, ns=19):
        """A UML class box with up to three compartments. Items may span several lines using a leading '  '."""
        longest = max([len(name) * ns / 15.2] + [len(s) for s in list(attrs) + list(ops)] + ([len(stereo) + 4] if stereo else []))
        w = w or max(150, longest * size * 0.62 + 30)
        head = 36 + (20 if stereo else 0)
        ah = (len(attrs) * row + 12) if attrs else 0
        oh = (len(ops) * row + 12) if ops else 0
        h = head + ah + oh
        fill = WARM if accent else TINT
        stroke = COPPER if accent else NAVY
        self.rect(x, y, w, h, fill=WHITE, stroke=stroke, sw=2.2, rx=6, dash="7 5" if dashed else None)
        self.raw(f'<path d="M{x+2:.1f},{y+head:.1f} L{x+2:.1f},{y+6:.1f} Q{x+2:.1f},{y+2:.1f} {x+6:.1f},{y+2:.1f} '
                 f'L{x+w-6:.1f},{y+2:.1f} Q{x+w-2:.1f},{y+2:.1f} {x+w-2:.1f},{y+6:.1f} L{x+w-2:.1f},{y+head:.1f} Z" fill="{fill}"/>')
        ty = y + 25
        if stereo:
            self.text(x + w / 2, y + 19, f"«{stereo}»", size=14, anchor="middle", fill=SOFT, italic=True)
            ty = y + 41
        self.text(x + w / 2, ty, name, size=ns, anchor="middle", weight=700, fill=stroke if accent else NAVY, font=HEAD)
        cy = y + head
        if attrs:
            self.raw(f'<line x1="{x:.1f}" y1="{cy:.1f}" x2="{x+w:.1f}" y2="{cy:.1f}" stroke="{stroke}" stroke-width="1.6"/>')
            for i, s in enumerate(attrs):
                self.text(x + 12, cy + 22 + i * row, s, size=size, font=MONO)
            cy += ah
        if ops:
            self.raw(f'<line x1="{x:.1f}" y1="{cy:.1f}" x2="{x+w:.1f}" y2="{cy:.1f}" stroke="{stroke}" stroke-width="1.6"/>')
            for i, s in enumerate(ops):
                self.text(x + 12, cy + 22 + i * row, s, size=size, font=MONO)
        return Box(x, y, w, h)

    def node(self, x, y, w, h, text, kind="box", size=19, weight=500):
        """A flowchart / state node. kind: box, round, pill, diamond, dark, copper, soft."""
        rows = text.split("\n") if isinstance(text, str) else list(text)
        if kind == "diamond":
            pts = [(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)]
            self.raw('<polygon points="' + " ".join(f"{px:.1f},{py:.1f}" for px, py in pts) +
                     f'" fill="{WARM}" stroke="{COPPER}" stroke-width="2.2"/>')
            tc = INK
        else:
            fill, stroke, tc, rx = {
                "box": (WHITE, NAVY, INK, 6),
                "round": (WHITE, NAVY, INK, 18),
                "pill": (TINT, NAVY, NAVY, h / 2),
                "dark": (DEEP, DEEP, "#ffffff", 8),
                "copper": (WARM, COPPER, INK, 8),
                "soft": (PAPER, LINE, SOFT, 8),
            }[kind]
            self.rect(x, y, w, h, fill=fill, stroke=stroke, rx=rx)
        n = len(rows)
        lh = size * 1.25
        y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.34
        for i, r in enumerate(rows):
            self.text(x + w / 2, y0 + i * lh, r, size=size, anchor="middle", weight=weight, fill=tc)
        return Box(x, y, w, h)

    def label(self, x, y, s, size=16, anchor="middle", fill=SOFT, italic=True, weight=400, font=SANS):
        self.text(x, y, s, size=size, anchor=anchor, fill=fill, italic=italic, weight=weight, font=font)

    def end_label(self, p, q, s, off=16, side=1, size=16):
        """A multiplicity next to point p of a line that runs from p towards q."""
        dx, dy = q[0] - p[0], q[1] - p[1]
        d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d
        px, py = -uy * side, ux * side
        x = p[0] + ux * 27 + px * off
        y = p[1] + uy * 27 + py * off + 5
        self.text(x, y, s, size=size, anchor="middle", fill=INK, font=MONO)

    def mid_label(self, pts, s, off=14, side=1, size=15, seg=None):
        """A name beside the middle of the longest (or given) segment."""
        segs = list(zip(pts, pts[1:]))
        a, b = segs[seg] if seg is not None else max(segs, key=lambda t: math.hypot(t[1][0] - t[0][0], t[1][1] - t[0][1]))
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d * side, dx / d * side
        if abs(dy) > abs(dx):          # vertical line: put the label beside it
            self.text(mx + (off + 4) * (1 if nx >= 0 else -1), my + 5, s, size=size, anchor="start" if nx >= 0 else "end",
                      fill=SOFT, italic=True)
        else:
            self.text(mx, my + ny * off - (0 if ny < 0 else -8), s, size=size, anchor="middle", fill=SOFT, italic=True)

    def rel(self, kind, pts, name=None, m_start=None, m_end=None, name_side=-1, name_seg=None):
        """UML relationships. kind: assoc, nav, dep, agg, comp, inh, real."""
        spec = {
            "assoc": (None, None, None),
            "nav": (None, "open", None),
            "dep": ("7 5", "open", None),
            "agg": (None, None, "dia"),
            "comp": (None, None, "diaf"),
            "inh": (None, "tri", None),
            "real": ("7 5", "tri", None),
        }[kind]
        dash, end, start = spec
        self.path(pts, dash=dash, start=start, end=end)
        if m_start is not None:
            self.end_label(pts[0], pts[1], m_start, side=1)
        if m_end is not None:
            self.end_label(pts[-1], pts[-2], m_end, side=-1)
        if name:
            self.mid_label(pts, name, side=name_side, seg=name_seg)

    def edge(self, pts, label=None, dashed=False, arrow=True, color=NAVY, label_at=None, label_side=1, size=16):
        self.path(pts, stroke=color, dash="7 5" if dashed else None, end="arr" if arrow else None)
        if label:
            if label_at:
                self.text(label_at[0], label_at[1], label, size=size, anchor="middle", fill=SOFT, italic=True)
            else:
                self.mid_label(pts, label, side=label_side, size=size)

    # ---- output ------------------------------------------------------------
    def defs(self):
        n = self.name
        return (
            "<defs>"
            f'<marker id="{n}-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto">'
            f'<path d="M1,1 L15,8 L1,15 Z" fill="{PAPER}" stroke="{NAVY}" stroke-width="2"/></marker>'
            f'<marker id="{n}-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto">'
            f'<path d="M1,7 L11,1 L21,7 L11,13 Z" fill="{PAPER}" stroke="{NAVY}" stroke-width="2"/></marker>'
            f'<marker id="{n}-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto">'
            f'<path d="M1,7 L11,1 L21,7 L11,13 Z" fill="{NAVY}" stroke="{NAVY}" stroke-width="2"/></marker>'
            f'<marker id="{n}-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto">'
            f'<path d="M2,2 L14,8 L2,14" fill="none" stroke="{NAVY}" stroke-width="2"/></marker>'
            f'<marker id="{n}-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto">'
            f'<path d="M0,1 L13,7 L0,13 Z" fill="{NAVY}"/></marker>'
            "</defs>"
        )

    def render(self):
        style = f"display:block;width:100%;height:calc(var(--u) * {self.h / 10:.2f});margin:0 auto"
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" role="img" '
                f'aria-label="{html.escape(self.label, quote=True)}" style="{style}">')
        return "\n".join(["<div>", head, self.defs()] + self.parts + ["</svg>", "</div>"])
