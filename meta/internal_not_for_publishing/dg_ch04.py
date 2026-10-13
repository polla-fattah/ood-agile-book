import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def review():
    s = Svg("ch04-review", 300, label="Team policy: a small change and local checks go to review and CI. If there is a blocking finding, correct and rerun, then return to review. If not, integrate and verify the shared branch.")
    a = s.node(10, 110, 200, 80, "Small change\nand local checks", "box", size=19)
    b = s.node(270, 110, 200, 80, "Review and CI", "box", size=19)
    c = s.node(530, 95, 150, 110, "Blocking\nfinding?", "diamond", size=18)
    d = s.node(520, 235, 170, 50, "Correct and rerun", "copper", size=18)
    e = s.node(730, 110, 135, 80, "Integrate and\nverify the\nshared branch", "dark", size=16)
    s.edge([a.a("r"), b.a("l")])
    s.edge([b.a("r"), c.a("l")])
    s.edge([c.a("r"), e.a("l")], "No", label_at=(705, 138))
    s.edge([c.a("b"), (c.cx, d.y)], "Yes", label_at=(c.cx + 22, 224))
    s.edge([d.a("l"), (370, d.cy), b.a("b")])
    s.text(370, 20, "A team policy: git does not enforce review by itself.", size=16, anchor="middle", fill=SOFT, italic=True)
    return s


def gate():
    s = Svg("ch04-gate", 330, label="The gate: scripts/check.sh compiles with --release 17, runs Chapter02Checks and then Chapter03AcceptanceExamples, and only then prints BUILD AND CHECKS PASSED. Any failing step stops the script with a nonzero exit. The hosted workflow checks out the repository, installs Temurin Java 17 and runs the same script.")
    top = [("Compile\njavac --release 17", 10), ("Chapter02Checks\n34 checks", 230), ("Chapter03\nAcceptanceExamples\n5 groups", 450), ("BUILD AND\nCHECKS PASSED", 670)]
    boxes = []
    for i, (t, x) in enumerate(top):
        kind = "dark" if i == 3 else "box"
        boxes.append(s.node(x, 20, 190, 84, t, kind, size=17))
    for a, b in zip(boxes, boxes[1:]):
        s.edge([a.a("r"), b.a("l")])
    for b in boxes[:3]:
        s.edge([b.a("b"), (b.cx, 150)], dashed=True, color=COPPER)
    s.rect(10, 150, 630, 40, fill=WARM, stroke=COPPER, rx=8)
    s.text(325, 177, "any failure stops the script: nonzero exit, no success line", size=18, anchor="middle", weight=600, fill=INK)
    s.text(10, 232, "Hosted workflow (GitHub Actions template):", size=17, weight=600, fill=NAVY)
    w = [("actions/checkout", 10), ("actions/setup-java\nTemurin 17", 290), ("bash scripts/check.sh\nthe same gate", 570)]
    wb = []
    for t, x in w:
        wb.append(s.node(x, 248, 250, 64, t, "soft" if False else "box", size=16))
    for a, b in zip(wb, wb[1:]):
        s.edge([a.a("r"), b.a("l")])
    return s


def slicing():
    s = Svg("ch04-slicing", 310, label="Left: a horizontal split does all screens, then all services, then all storage, so nothing can be demonstrated until the end. Right: a vertical slice is a thin path through interaction, domain behaviour and storage that delivers one observable outcome.")
    s.text(215, 24, "Horizontal split", size=21, anchor="middle", weight=700, fill=NAVY, font="'Chakra Petch', sans-serif")
    s.text(655, 24, "Vertical slice", size=21, anchor="middle", weight=700, fill=NAVY, font="'Chakra Petch', sans-serif")
    for i, t in enumerate(["All screens first", "Then all services", "Then all storage"]):
        s.node(15, 46 + i * 78, 400, 62, t, "box", size=19)
    s.text(215, 296, "Work exists, but nothing is demonstrable until the end.", size=15, anchor="middle", fill=SOFT, italic=True)
    for i, t in enumerate(["Interaction", "Domain behaviour", "Storage"]):
        s.rect(455, 46 + i * 78, 400, 62, fill=PAPER, stroke=LINE, rx=8)
        s.text(475, 84 + i * 78, t, size=19, weight=500, fill=SOFT)
    s.rect(745, 38, 90, 232, fill=WARM, stroke=COPPER, sw=2.6, rx=10)
    s.text(790, 160, "US-02", size=18, anchor="middle", weight=700, fill=COPPER)
    s.text(655, 296, "A thin path through every layer: one observable outcome.", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


def capacity():
    s = Svg("ch04-capacity", 262, label="22 person-hours reported: 4 reserved for coordination, integration and administration, leaving an 18-hour planning budget. Selected work is 14 hours (2, 4, 3, 3 and 2), leaving 4 hours unallocated.")
    x0, k = 6, 39
    s.text(435, 24, "Four members report 6 + 6 + 5 + 5 = 22 person-hours", size=18, anchor="middle", weight=600, fill=NAVY)
    segs = [(4, "Reserved", "#c3cfdd", INK, "coordination,\nintegration, admin"),
            (2, "2", NAVY, "#ffffff", "resolve the\nquery contract"),
            (4, "4", "#2f78b3", "#ffffff", "implement the\nread-only query"),
            (3, "3", NAVY, "#ffffff", "thin interaction,\ninvalid input"),
            (3, "3", "#2f78b3", "#ffffff", "query and\nregression checks"),
            (2, "2", NAVY, "#ffffff", "review, notes,\nrehearsal"),
            (4, "4", WHITE, COPPER, "unallocated:\nroom for uncertainty")]
    x = x0
    for h, lab, fill, tc, cap in segs:
        w = h * k
        dash = "7 5" if fill == WHITE else None
        s.rect(x, 40, w, 52, fill=fill, stroke=COPPER if fill == WHITE else NAVY, sw=2, rx=4, dash=dash)
        s.text(x + w / 2, 74, lab, size=20 if len(lab) < 3 else 15, anchor="middle", weight=700, fill=tc)
        s.lines(x + w / 2, 112, cap.split("\n"), size=13.5, anchor="middle", fill=SOFT, gap=1.2)
        x += w
    xs = x0 + 4 * k
    xe14 = x0 + 18 * k
    xe18 = x0 + 22 * k
    s.path([(xs, 160), (xs, 170), (xe14, 170), (xe14, 160)], stroke=NAVY, sw=2.4)
    s.text((xs + xe14) / 2, 192, "Selected work: 14 person-hours", size=18, anchor="middle", weight=600, fill=NAVY)
    s.path([(xs, 208), (xs, 218), (xe18, 218), (xe18, 208)], stroke=COPPER, sw=2.4)
    s.text((xs + xe18) / 2, 240, "Planning budget: 18 person-hours", size=18, anchor="middle", weight=600, fill=COPPER)
    return s


DIAGRAMS = {"ch04-review": review, "ch04-gate": gate, "ch04-slicing": slicing, "ch04-capacity": capacity}
