import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def fig51():
    s = Svg("ch05-fig51", 350, label="Figure 5.1: ReservationCoordinator holds a BorrowingPolicy reference and a ConfirmationFormatter. ReservationRules and StaffReservationRules realise the BorrowingPolicy interface. The coordinator also depends on the two concrete policies because it creates them.")
    co = s.cls(10, 95, "ReservationCoordinator", w=280)
    bp = s.cls(470, 10, "BorrowingPolicy", ops=["+mayRequest(int, int) boolean"], stereo="interface", row=23, size=15)
    rr = s.cls(330, 215, "ReservationRules", w=220)
    sr = s.cls(590, 215, "StaffReservationRules", w=265)
    cf = s.cls(10, 305, "ConfirmationFormatter", w=270)
    s.rel("nav", [(co.x + co.w, 113), (370, 113), (370, 55), (bp.x, 55)], "asks eligibility", name_seg=2)
    s.rel("nav", [(100, co.y + co.h), (100, cf.y)], "formats")
    s.rel("real", [(520, rr.y), (520, bp.y + bp.h)])
    s.rel("real", [(700, sr.y), (700, bp.y + bp.h)])
    s.rel("dep", [(270, co.y + co.h), (270, 250), (rr.x, 250)], "creates", name_seg=1)
    s.rel("dep", [(230, co.y + co.h), (230, 290), (726, 290), (726, sr.y + sr.h)], "creates", name_seg=2)
    return s


def lsp():
    s = Svg("ch05-lsp", 300, label="A client of IntHistory adds 5 then -2 and expects [5, -2]. IntHistory satisfies it. PositiveOnlyHistory, which extends IntHistory, throws IllegalArgumentException on -2, so the subtype has strengthened the precondition.")
    c = s.node(10, 90, 270, 120, "client(IntHistory h)\nh.add(5);\nh.add(-2);\nexpects [5, -2]", "box", size=18)
    a = s.node(360, 25, 220, 70, "IntHistory", "box", size=20, weight=700)
    ar = s.node(640, 25, 220, 70, "[5, -2]\ncontract kept", "round", size=18)
    b = s.node(360, 205, 220, 70, "PositiveOnlyHistory\nextends IntHistory", "copper", size=17, weight=700)
    br = s.node(640, 205, 220, 70, "IllegalArgumentException\non add(-2)", "dark", size=16)
    s.edge([c.a("r", 0.25), (320, c.y + 30), (320, a.cy), a.a("l")])
    s.edge([c.a("r", 0.75), (320, c.y + 90), (320, b.cy), b.a("l")])
    s.edge([a.a("r"), ar.a("l")])
    s.edge([b.a("r"), br.a("l")])
    return s


def stages():
    s = Svg("ch05-stages", 215, label="Baseline gate passes; Stage A extracts the formatter as a refactoring; the unchanged checks run; Stage B adds the staff policy as a feature change; the old and new checks run.")
    labels = [("Baseline\ngate passes", "box"), ("Stage A:\nextract the\nformatter", "copper"),
              ("Unchanged\nchecks\nstill pass", "box"), ("Stage B:\nadd the staff\npolicy", "copper"),
              ("Old and new\nchecks pass", "box")]
    w, g = 150, 30
    boxes = []
    for i, (t, k) in enumerate(labels):
        boxes.append(s.node(10 + i * (w + g), 30, w, 96, t, k, size=17, weight=600))
    for a, b in zip(boxes, boxes[1:]):
        s.edge([a.a("r"), b.a("l")])
    s.text(boxes[1].cx, 160, "refactoring", size=17, anchor="middle", weight=700, fill=COPPER)
    s.text(boxes[1].cx, 183, "behaviour unchanged", size=15, anchor="middle", fill=SOFT, italic=True)
    s.text(boxes[3].cx, 160, "feature change", size=17, anchor="middle", weight=700, fill=COPPER)
    s.text(boxes[3].cx, 183, "student entry point kept", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


DIAGRAMS = {"ch05-fig51": fig51, "ch05-lsp": lsp, "ch05-stages": stages}
