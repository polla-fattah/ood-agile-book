import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def order():
    s = Svg("ch11-order", 290, label="Figure 11.1: observe, make the smallest mechanical edit that creates a seam, pin behaviour with characterisation tests, reshape with small refactorings testing after each, and only then change behaviour in a separate step. If a test fails, roll back the step and redo it.")
    labels = [("Observe\nrun and read", "box"), ("Seam\nsmallest\nmechanical edit", "box"), ("Pin\ncharacterisation\ntests", "box"),
              ("Reshape\nsmall refactorings,\ntest after each", "dark"), ("Change behaviour\na separate step,\nnew tests", "copper")]
    boxes = []
    for i, (t, k) in enumerate(labels):
        boxes.append(s.node(10 + i * 175, 25, 150, 92, t, k, size=16, weight=600))
    for a, b in zip(boxes, boxes[1:]):
        s.edge([a.a("r"), b.a("l")])
    rb = s.node(520, 195, 180, 56, "Roll back the step", "copper", size=17, weight=600)
    s.edge([(boxes[3].cx - 25, 117), (boxes[3].cx - 25, 195)], "a test fails", label_at=(boxes[3].cx - 78, 160))
    s.edge([(boxes[3].cx + 25, 195), (boxes[3].cx + 25, 117)], "redo it", label_at=(boxes[3].cx + 70, 160), color=COPPER)
    s.text(80, 225, "Debug backwards, not forwards:", size=16, anchor="start", fill=SOFT, italic=True)
    s.text(80, 247, "undo the last step and redo it.", size=16, anchor="start", fill=SOFT, italic=True)
    return s


def classes():
    s = Svg("ch11-classes", 365, label="Figure 11.2: OverdueReport holds three FinePolicy values (STUDENT, STAFF, ANY_OTHER_KIND) and only reads LoanRow, the old system's export format, which is unchanged.")
    orp = s.cls(10, 10, "OverdueReport", ops=["+build(List<LoanRow>) String", "+build(List<LoanRow>, LocalDate) String", "+print(List<LoanRow>) void", "-policyFor(String) FinePolicy", "-money(double) String"], w=375, row=23, size=15)
    fp = s.cls(560, 10, "FinePolicy", attrs=["int graceDays", "double ratePerDay", "double cap"], ops=["~fineFor(long) double"], stereo="record", w=290, row=23, size=15)
    lr = s.cls(560, 205, "LoanRow", attrs=["+String item", "+String borrower", "+String kind", "+LocalDate due", "+boolean returned"], w=290, row=23, size=15)
    s.rel("nav", [(orp.x + orp.w, 70), (fp.x, 70)], "holds three", name_side=-1)
    s.rel("dep", [(200, orp.y + orp.h), (200, 280), (lr.x, 280)], "reads", name_seg=1)
    s.text(470, 105, "STUDENT, STAFF,", size=13.5, anchor="middle", fill=SOFT, italic=True)
    s.text(470, 123, "ANY_OTHER_KIND", size=13.5, anchor="middle", fill=SOFT, italic=True)
    return s


def difference():
    s = Svg("ch11-difference", 300, label="Figure 11.3: when a check reports a difference, ask whether the behaviour change was agreed. If not, inspect or undo the latest edit and rerun the unchanged expectations. If yes, separate the functional change, record the rule and the affected examples, and rerun.")
    a = s.node(10, 115, 175, 66, "A check reports\na difference", "dark", size=16, weight=600)
    d = s.node(225, 70, 215, 150, "Was this behaviour\nchange agreed?", "diamond", size=16)
    n1 = s.node(480, 12, 205, 60, "Inspect or undo\nthe latest edit", "box", size=16)
    y1 = s.node(480, 225, 180, 60, "Separate the\nfunctional change", "copper", size=16)
    y2 = s.node(690, 225, 170, 60, "Record the rule and\naffected examples", "copper", size=15)
    r = s.node(690, 118, 175, 66, "Rerun the unchanged\nexpectations", "box", size=15)
    s.edge([a.a("r"), d.a("l")])
    s.edge([d.a("t"), (d.cx, 42), n1.a("l")], "No", label_at=(d.cx + 18, 60))
    s.edge([d.a("b"), (d.cx, 255), y1.a("l")], "Yes", label_at=(d.cx + 20, 246))
    s.edge([n1.a("r"), (788, n1.cy), r.a("t")])
    s.edge([y1.a("r"), y2.a("l")])
    s.edge([(775, 225), (775, 184)])
    return s


def fines():
    s = Svg("ch11-fines", 340, label="Fine against days late: a student pays nothing for 2 days, then 0.50 a day up to a cap of 10.00 at 22 days; staff pay nothing for 5 days, then 0.25 a day up to a cap of 5.00 at 25 days; any other kind pays 1.00 a day with no grace and no cap (suspected defect).")
    x0, x1, y0, y1 = 80, 800, 285, 25
    dx = (x1 - x0) / 30
    dy = (y0 - y1) / 30

    def P(d, f):
        return (x0 + d * dx, y0 - f * dy)

    for f in (0, 5, 10, 20, 30):
        yy = y0 - f * dy
        s.path([(x0, yy), (x1, yy)], stroke=LINE, sw=1.4)
        s.text(x0 - 10, yy + 5, f"{f}.00", size=14.5, anchor="end", fill=SOFT, font="'Plex Mono', monospace")
    for d in (0, 5, 10, 15, 20, 25, 30):
        s.text(x0 + d * dx, y0 + 22, str(d), size=14.5, anchor="middle", fill=SOFT, font="'Plex Mono', monospace")
    s.text((x0 + x1) / 2, 328, "days late", size=15, anchor="middle", fill=SOFT, italic=True)
    s.path([P(0, 0), P(2, 0), P(22, 10), P(30, 10)], stroke=NAVY, sw=3.4)
    s.path([P(0, 0), P(5, 0), P(25, 5), P(30, 5)], stroke=COPPER, sw=3.4)
    s.path([P(0, 0), P(30, 30)], stroke=INK, sw=2.6, dash="8 6")
    s.text(P(30, 10)[0] + 8, P(30, 10)[1] + 5, "student", size=15, fill=NAVY, weight=700)
    s.text(P(30, 5)[0] + 8, P(30, 5)[1] + 5, "staff", size=15, fill=COPPER, weight=700)
    s.text(P(30, 30)[0] - 6, P(30, 30)[1] + 22, "other kinds", size=15, anchor="end", fill=INK, weight=700)
    s.text(P(22, 10)[0], P(22, 10)[1] - 10, "cap at 22 days", size=14, anchor="middle", fill=NAVY, italic=True)
    s.text(P(25, 5)[0] + 4, P(25, 5)[1] - 22, "cap at 25 days", size=14, anchor="middle", fill=COPPER, italic=True)
    s.text(P(14, 14)[0] - 20, P(14, 14)[1] - 8, "no grace, no cap", size=14, anchor="end", fill=INK, italic=True)
    s.text(P(14, 14)[0] - 20, P(14, 14)[1] + 10, "(suspected defect)", size=14, anchor="end", fill=INK, italic=True)
    return s


DIAGRAMS = {"ch11-order": order, "ch11-classes": classes, "ch11-difference": difference, "ch11-fines": fines}
