import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER
from dg_ch08 import _seq


def states():
    s = Svg("ch09-states", 300, label="Figure 9.1, the proposed lifecycle: REQUESTED can be confirmed or cancelled; CONFIRMED can be checked out or cancelled; ON_LOAN can be returned. RETURNED and CANCELLED allow none of the four actions.")
    w = 120
    rq = s.node(45, 60, w, 56, "REQUESTED", "round", size=15, weight=700)
    cf = s.node(265, 60, w, 56, "CONFIRMED", "round", size=15, weight=700)
    ol = s.node(485, 60, w, 56, "ON_LOAN", "round", size=15, weight=700)
    rt = s.node(705, 60, w, 56, "RETURNED", "dark", size=15, weight=700)
    cn = s.node(140, 220, 120, 56, "CANCELLED", "dark", size=15, weight=700)
    s.circle(22, 88, 9, fill=INK)
    s.edge([(31, 88), rq.a("l")])
    s.edge([rq.a("r"), cf.a("l")], "confirm", label_at=(215, 78))
    s.edge([cf.a("r"), ol.a("l")], "check out", label_at=(435, 78))
    s.edge([ol.a("r"), rt.a("l")], "return", label_at=(655, 78))
    s.edge([rq.a("b", 0.5), (rq.cx, 248), cn.a("l")], "cancel", label_at=(rq.cx + 30, 180))
    s.edge([cf.a("b", 0.5), (cf.cx, 248), cn.a("r")], "cancel", label_at=(cf.cx + 30, 180))
    s.text(560, 250, "Terminal (dark): none of the four actions is allowed.", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


def classes():
    s = Svg("ch09-classes", 235, label="Figure 9.2: ConditionalReservation and StateReservation both realise the Lifecycle interface. StateReservation holds a Phase and delegates each operation to it; ConditionalReservation keeps a status value and switches on it.")
    lc = s.cls(10, 10, "Lifecycle", ops=["+status() Status", "+confirm() void", "+checkOut() void", "+returnItem() void", "+cancel() void"], stereo="interface", w=250, row=23, size=15)
    cr = s.cls(350, 15, "ConditionalReservation", attrs=["-Status status"], w=250, row=23, size=15, ns=16)
    sr = s.cls(350, 135, "StateReservation", attrs=["-Phase phase"], w=250, row=23, size=15, ns=16)
    ph = s.cls(700, 15, "Phase", attrs=["REQUESTED", "CONFIRMED", "ON_LOAN", "RETURNED", "CANCELLED"], stereo="enumeration", w=165, row=23, size=15)
    s.rel("real", [(cr.x, 50), (lc.x + lc.w, 50)])
    s.rel("real", [(sr.x, 170), (lc.x + lc.w, 170)])
    s.rel("nav", [(sr.x + sr.w, 170), (ph.x, 170)], "delegates to")
    return s


PARTS = {"C": ("Coordinator", 110), "P": ("Publisher", 275), "D": ("Desk\nobserver", 440), "X": ("Display\nobserver", 605), "A": ("Audit\nobserver", 770)}


def sequence():
    items = [("note", "C", "C", 84, "Reservation already stored", 100),
             ("msg", "C", "P", 120, "send(reservation)", False),
             ("msg", "P", "D", 148, "onConfirmed(reservation)", False),
             ("msg", "D", "P", 174, "Normal return", True),
             ("msg", "P", "X", 202, "onConfirmed(reservation)", False),
             ("msg", "X", "P", 228, "NotificationException", True),
             ("msg", "P", "A", 256, "onConfirmed(reservation)", False),
             ("msg", "A", "P", 282, "Normal return", True),
             ("msg", "P", "C", 310, "Aggregate NotificationException", True),
             ("note", "C", "P", 340, "Confirmation + failure suffix", 60)]
    return _seq("ch09-seq", 362, "Figure 9.3: one accepted reservation is published to three observers; the display observer fails with the expected exception, the others still run, and the publisher throws one aggregate exception that the coordinator turns into the failure suffix.", PARTS, items)


def command():
    s = Svg("ch09-command", 270, label="Three moments of a command: constructing it captures the receiver and arguments and does nothing else; executing it makes the service evaluate the current state; executing it again re-enters the service and gives a different result.")
    xs = [10, 320, 630]
    heads = ["1  Construct", "2  Execute", "3  Execute again"]
    codes = ["new ReserveEquipmentCommand(…)", "command.execute()", "command.execute()"]
    caps = [["captures the receiver", "and the arguments;", "no lookup, no reservation,", "no notice"],
            ["the service evaluates the", "CURRENT state: lookup,", "eligibility and conflict"],
            ["re-enters the service: the", "stored record now conflicts;", "a different result; one", "record and one notice remain"]]
    boxes = []
    for i in range(3):
        s.rect(xs[i], 20, 230, 74, fill=WHITE if i != 1 else TINT, stroke=NAVY, rx=8)
        s.text(xs[i] + 115, 48, heads[i], size=18, anchor="middle", weight=700, fill=NAVY, font="'Chakra Petch', sans-serif")
        s.text(xs[i] + 115, 76, codes[i], size=12.5, anchor="middle", font="'Plex Mono', monospace", fill=INK)
        s.lines(xs[i] + 115, 130, caps[i], size=15, anchor="middle", fill=INK)
        boxes.append((xs[i], 20, 230, 74))
    s.edge([(240, 57), (320, 57)])
    s.edge([(550, 57), (630, 57)])
    s.text(280, 15, "state may change", size=13.5, anchor="middle", fill=COPPER, italic=True)
    s.text(590, 15, "same command", size=13.5, anchor="middle", fill=COPPER, italic=True)
    return s


DIAGRAMS = {"ch09-states": states, "ch09-classes": classes, "ch09-seq": sequence, "ch09-command": command}
