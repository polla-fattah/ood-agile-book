import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def tdd():
    s = Svg("ch07-tdd", 362, label="Red, green, refactor: write a behaviour test and run it. If the intended assertion does not fail, inspect setup, test or existing behaviour and run again. If it fails, implement just enough to pass, confirm green, then refactor and run the regression tests. If they pass, take the next behaviour; if they fail, repair the refactoring.")
    a = s.node(10, 25, 175, 62, "Write a\nbehaviour test", "box", size=18)
    b = s.node(225, 25, 150, 62, "Run the test", "box", size=18)
    c = s.node(425, 8, 215, 96, "Intended assertion\nfails?", "diamond", size=17)
    d = s.node(425, 195, 215, 62, "Inspect setup, test or\nexisting behaviour", "copper", size=16)
    e = s.node(690, 25, 170, 62, "Implement enough\nto pass", "box", size=17)
    f = s.node(690, 140, 170, 50, "Confirm green", "box", size=18)
    g = s.node(690, 270, 170, 62, "Refactor and run\nregression tests", "dark", size=17)
    s.edge([a.a("r"), b.a("l")])
    s.edge([b.a("r"), c.a("l")])
    s.edge([c.a("r"), e.a("l")], "Yes", label_at=(665, 44))
    s.edge([c.a("b"), d.a("t")], "No", label_at=(448, 158))
    s.edge([d.a("l"), (300, d.cy), b.a("b")])
    s.edge([e.a("b"), f.a("t")])
    s.edge([f.a("b"), g.a("t")])
    s.edge([g.a("l"), (97, g.cy), a.a("b")], "tests pass: next behaviour", label_at=(330, g.cy - 9))
    s.text(745, 354, "tests fail: repair the refactoring", size=14.5, anchor="middle", fill=COPPER, italic=True)
    return s


def clock():
    s = Svg("ch07-clock", 270, label="One instant, 19 October 22:30 UTC, gives the local date 19 October in the UTC zone and 20 October in the Asia/Baghdad zone, so a test must state both the instant and the zone.")
    i = s.node(10, 95, 250, 80, "Instant\n2026-10-19 22:30 UTC", "dark", size=18)
    z1 = s.node(420, 25, 250, 80, "Zone UTC\nlocal date: 19 October", "box", size=18)
    z2 = s.node(420, 165, 250, 80, "Zone Asia/Baghdad (UTC+3)\nlocal date: 20 October", "copper", size=17)
    s.edge([i.a("r", 0.3), (340, 119), (340, z1.cy), z1.a("l")])
    s.edge([i.a("r", 0.7), (340, 151), (340, z2.cy), z2.a("l")])
    s.text(765, 70, "LocalDate.now(clock)", size=16, anchor="middle", font="'Plex Mono', monospace", fill=NAVY, weight=600)
    s.text(765, 92, "needs both", size=16, anchor="middle", fill=SOFT, italic=True)
    return s


def laptop():
    s = Svg("ch07-laptop", 345, label="Midterm practice task 1, one model: a Borrower and a Laptop each link to zero or more Loans; a Loan owns zero or more Renewals (composition); a Loan depends on the NoticeChannel interface, which EmailChannel implements.")
    bo = s.cls(10, 10, "Borrower", attrs=["-String name"], w=170, row=23, size=15)
    la = s.cls(10, 205, "Laptop", attrs=["-String assetTag", "-String model"], w=190, row=23, size=15)
    lo = s.cls(310, 10, "Loan", attrs=["-LocalDate startedOn", "-LocalDate dueOn"], ops=["+notify(NoticeChannel", "   channel) void"], w=250, row=23, size=15)
    re = s.cls(420, 265, "Renewal", attrs=["-LocalDate newDueOn"], w=200, row=23, size=15)
    nc = s.cls(650, 10, "NoticeChannel", ops=["+deliver(String", "   message) void"], stereo="interface", w=210, row=23, size=15)
    em = s.cls(650, 215, "EmailChannel", w=210)
    s.rel("assoc", [(bo.x + bo.w, 45), (lo.x, 45)], "borrows", "1", "0..*")
    s.rel("assoc", [(la.x + la.w, 250), (350, 250), (350, lo.y + lo.h)], "is lent in", "1", "0..*", name_seg=1)
    s.rel("comp", [(500, lo.y + lo.h), (500, re.y)], "has", "1", "0..*")
    s.rel("dep", [(lo.x + lo.w, 70), (nc.x, 70)], "notices")
    s.rel("real", [(755, em.y), (755, nc.y + nc.h)], "implements")
    return s


DIAGRAMS = {"ch07-tdd": tdd, "ch07-clock": clock, "ch07-laptop": laptop}
