import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER

MONO = "'Plex Mono', monospace"


def timeline():
    s = Svg("ch12-timeline", 345, label="Timeline of the eight synthetic items over 1 to 11 October: waiting before start, active time, B's two-day block, F's removal on day 8, and E and H still open at the end.")
    x0, dw = 150, 60

    def X(d):
        return x0 + (d - 1) * dw

    for d in range(1, 12):
        s.text(X(d), 24, f"{d:02d}", size=14.5, anchor="middle", fill=SOFT, font=MONO)
        s.path([(X(d), 32), (X(d), 292)], stroke=LINE, sw=1.2)
    items = [("A", 3, 1, 1, 3, None), ("B", 5, 1, 2, 6, None), ("C", 2, 1, 3, 4, None), ("D", 3, 1, 5, 8, None),
             ("E", 5, 1, 7, None, None), ("F", 2, 1, None, None, 8), ("G", 3, 4, 6, 10, None), ("H", 2, 6, 8, None, None)]
    for i, (n, pts, acc, st, done, rem) in enumerate(items):
        y = 44 + i * 31
        s.text(12, y + 17, f"{n}", size=16, weight=700, fill=NAVY, font=MONO)
        s.text(38, y + 17, f"{pts} pts", size=14, fill=SOFT, font=MONO)
        end = done or rem or 11
        first = st or end
        if first > acc:
            s.rect(X(acc), y + 5, X(first) - X(acc), 18, fill=PAPER, stroke=SOFT, rx=3, sw=1.4, dash="5 4")
        if st:
            e = done or 11
            s.rect(X(st), y + 5, X(e) - X(st), 18, fill=NAVY if done else "#7fa7cc", stroke=NAVY, rx=3, sw=1.4)
            if not done:
                s.text(X(e) + 8, y + 19, "open", size=13.5, fill=COPPER, italic=True, weight=600)
        if rem:
            s.text(X(rem) + 14, y + 21, "×", size=22, anchor="middle", fill=COPPER, weight=700)
            s.text(X(rem) + 30, y + 19, "removed", size=13.5, fill=COPPER, italic=True)
        if n == "B":
            s.rect(X(3), y + 9, X(5) - X(3), 10, fill=COPPER, stroke=COPPER, rx=2, sw=1)
    s.rect(150, 306, 22, 14, fill=PAPER, stroke=SOFT, rx=3, sw=1.4, dash="4 3")
    s.text(178, 318, "accepted, waiting", size=14, fill=SOFT)
    s.rect(330, 306, 22, 14, fill=NAVY, stroke=NAVY, rx=3, sw=1)
    s.text(358, 318, "started to done", size=14, fill=SOFT)
    s.rect(510, 306, 22, 14, fill=COPPER, stroke=COPPER, rx=3, sw=1)
    s.text(538, 318, "B blocked, 03 to 05", size=14, fill=SOFT)
    return s


def burnup():
    s = Svg("ch12-burnup", 335, label="Burn-up of the synthetic iteration, daily from 1 to 11 October: scope points 20, 20, 20, 23, 23, 25, 25, 23, 23, 23, 23 and completed points 0, 0, 3, 5, 5, 10, 10, 13, 13, 16, 16.")
    x0, x1, y0, y1 = 80, 800, 285, 30
    dx = (x1 - x0) / 10
    dy = (y0 - y1) / 25
    scope = [20, 20, 20, 23, 23, 25, 25, 23, 23, 23, 23]
    done = [0, 0, 3, 5, 5, 10, 10, 13, 13, 16, 16]

    def P(d, v):
        return (x0 + (d - 1) * dx, y0 - v * dy)

    for v in (0, 5, 10, 15, 20, 25):
        yy = y0 - v * dy
        s.path([(x0, yy), (x1, yy)], stroke=LINE, sw=1.3)
        s.text(x0 - 10, yy + 5, str(v), size=14.5, anchor="end", fill=SOFT, font=MONO)
    for d in range(1, 12):
        s.text(P(d, 0)[0], y0 + 22, f"{d:02d}", size=14.5, anchor="middle", fill=SOFT, font=MONO)
    s.path([P(i + 1, v) for i, v in enumerate(scope)], stroke=COPPER, sw=3.4)
    s.path([P(i + 1, v) for i, v in enumerate(done)], stroke=NAVY, sw=3.4)
    for i, v in enumerate(scope):
        s.circle(*P(i + 1, v), 4.5, fill=COPPER)
    for i, v in enumerate(done):
        s.circle(*P(i + 1, v), 4.5, fill=NAVY)
    s.text(P(4, 23)[0], P(4, 23)[1] - 14, "G added", size=14, anchor="middle", fill=COPPER, italic=True)
    s.text(P(6, 25)[0], P(6, 25)[1] - 14, "H added", size=14, anchor="middle", fill=COPPER, italic=True)
    s.text(P(8, 23)[0] + 4, P(8, 23)[1] - 14, "F removed", size=14, anchor="start", fill=COPPER, italic=True)
    s.text(P(11, 23)[0] - 10, P(11, 23)[1] + 24, "scope 23", size=14.5, anchor="end", fill=COPPER, weight=700)
    s.text(P(11, 16)[0] - 10, P(11, 16)[1] + 24, "done 16", size=14.5, anchor="end", fill=NAVY, weight=700)
    s.text(P(11, 20)[0] + 6, P(11, 20)[1] + 5, "7 left", size=14.5, fill=SOFT, italic=True)
    s.text((x0 + x1) / 2, 328, "October 2026 snapshot day", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


DIAGRAMS = {"ch12-timeline": timeline, "ch12-burnup": burnup}
