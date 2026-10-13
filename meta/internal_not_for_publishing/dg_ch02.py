import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE


def fig21():
    s = Svg("ch02-fig21", 360, label="Figure 2.1: ReservationCoordinator uses one ReservationRules and stores zero or more Reservations; each Reservation refers to one LoanPeriod.")
    co = s.cls(10, 6, "ReservationCoordinator",
               ops=["+reserve(String borrowerId, String itemId,", "   LocalDate start, int requestedDays) String", "+reservations() List<Reservation>"],
               row=23, size=15)
    ru = s.cls(570, 6, "ReservationRules",
               ops=["+mayRequest(", "   int activeReservations,", "   int requestedDays) boolean"], w=290, row=23, size=15)
    rs = s.cls(10, 200, "Reservation",
               attrs=["-String id", "-String borrowerId", "-String itemId"], ops=["+period() LoanPeriod"], row=23, size=15)
    lp = s.cls(340, 200, "LoanPeriod",
               attrs=["-LocalDate start", "-LocalDate endExclusive"], ops=["+overlaps(LoanPeriod other) boolean"], row=23, size=15)
    y = co.y + 58
    s.rel("nav", [(co.x + co.w, y), (ru.x, y)], "uses", "1", "1")
    x = co.x + 90
    s.rel("nav", [(x, co.y + co.h), (x, rs.y)], "stores", "1", "0..*")
    y2 = rs.y + 62
    s.rel("nav", [(rs.x + rs.w, y2), (lp.x, y2)], "refers to", "0..*", "1")
    return s


def fig22():
    s = Svg("ch02-fig22", 372, label="Figure 2.2, a notation sampler: a Pack contains Pages (composition), collects Articles (aggregation) and uses a Printer (dependency); Articles and Authors are associated; ResearchArticle extends Article; PdfPrinter implements Printer.")
    pack = s.cls(10, 19, "Pack", attrs=["-String title"], ops=["+print(Printer printer) String"], row=23, size=15)
    prn = s.cls(10, 179, "Printer", ops=["+render(List<String> lines) String"], stereo="interface", row=23, size=15)
    pdf = s.cls(10, 316, "PdfPrinter", w=190)
    page = s.cls(440, 19, "Page", w=150)
    art = s.cls(440, 144, "Article", w=150)
    res = s.cls(440, 269, "ResearchArticle", w=210)
    aut = s.cls(710, 144, "Author", w=150)
    px = pack.x + pack.w
    s.rel("comp", [(px, 37), (page.x, 37)], "contains", "1", "1..*")
    s.rel("agg", [(px, 104), (385, 104), (385, 162), (art.x, 162)], "collects", "0..*", "1..*", name_seg=1)
    s.rel("assoc", [(art.x + art.w, 162), (aut.x, 162)], "written by", "1..*", "1..*")
    s.rel("inh", [(520, res.y), (520, art.y + art.h)], "extends")
    s.rel("dep", [(100, pack.y + pack.h), (100, prn.y)], "uses")
    s.rel("real", [(100, pdf.y), (100, prn.y + prn.h)], "implements")
    return s


def locker_boxes(s, flawed):
    if flawed:
        te = s.cls(5, 10, "Technician", attrs=["-String name", "-Locker locker"], w=150, row=23, size=15)
        lk = s.cls(270, 10, "Locker", attrs=["-int number"], ops=["+report(PlainTextPrinter", "   printer) String"], row=23, size=15)
    else:
        te = s.cls(5, 10, "Technician", attrs=["-String name"], w=150, row=23, size=15)
        lk = s.cls(270, 10, "Locker", attrs=["-int number"], ops=["+report(ReportPrinter", "   printer) String"], row=23, size=15)
    tl = s.cls(700, 10, "Tool", attrs=["-String name"] if not flawed else [], w=130, row=23, size=15)
    return te, lk, tl


def fig23():
    s = Svg("ch02-fig23", 382, label="Figure 2.3, the corrected workshop model: a Technician looks after many Lockers; a Locker holds at most one Tool; a Locker owns its InspectionEntries (composition); a Locker uses the ReportPrinter interface, which PlainTextPrinter implements.")
    te, lk, tl = locker_boxes(s, False)
    ie = s.cls(270, 215, "InspectionEntry", attrs=["-LocalDate date", "-String note"], row=23, size=15)
    rp = s.cls(480, 215, "ReportPrinter", ops=["+print(List<String> lines) String"], stereo="interface", row=23, size=15)
    pt = s.cls(560, 335, "PlainTextPrinter", w=220)
    y = 45
    s.rel("assoc", [(te.x + te.w, y), (lk.x, y)], "looks after", "1", "0..*")
    s.rel("assoc", [(lk.x + lk.w, y), (tl.x, y)], "holds", "0..1", "0..1")
    s.rel("comp", [(340, lk.y + lk.h), (340, ie.y)], "logs", "1", "0..*")
    s.rel("dep", [(490, lk.y + lk.h), (490, rp.y)], "uses")
    s.rel("real", [(680, pt.y), (680, rp.y + rp.h)], "implements")
    return s


def fig24():
    s = Svg("ch02-fig24", 375, label="Figure 2.4, a flawed attempt at the workshop model, for diagnosis: a locker attribute in Technician, a composition with reversed multiplicities from Technician to Locker, inheritance from Locker to InspectionEntry, a dependency on the concrete PlainTextPrinter, and a solid inheritance line for the interface.")
    te, lk, tl = locker_boxes(s, True)
    ie = s.cls(270, 200, "InspectionEntry", w=200)
    pt = s.cls(500, 200, "PlainTextPrinter", w=220)
    rp = s.cls(500, 282, "ReportPrinter", ops=["+print(List<String> lines) String"], stereo="interface", row=23, size=15)
    y = 45
    s.rel("comp", [(te.x + te.w, y), (lk.x, y)], "looks after", "0..*", "1")
    s.rel("assoc", [(lk.x + lk.w, y), (tl.x, y)], "holds", "0..1", "0..1")
    s.rel("inh", [(340, ie.y), (340, lk.y + lk.h)], "logs")
    s.rel("dep", [(510, lk.y + lk.h), (510, pt.y)], "uses")
    s.rel("inh", [(610, pt.y + pt.h), (610, rp.y)])
    return s


def overlap():
    s = Svg("ch02-overlap", 360, label="Timeline of four pairs of half-open periods against 19 to 24 October, showing which pairs overlap.")
    x0, dw = 340, 85
    for i, d in enumerate(range(19, 25)):
        s.text(x0 + i * dw + dw / 2, 26, f"{d} Oct", size=16, anchor="middle", fill=SOFT, weight=600)
    for i in range(7):
        s.raw(f'<line x1="{x0 + i * dw}" y1="38" x2="{x0 + i * dw}" y2="318" stroke="{LINE}" stroke-width="1.5"/>')

    def xd(d):
        return x0 + (d - 19) * dw

    cases = [
        ((20, 22), (21, 23), "Yes", "both include 21 Oct"),
        ((20, 22), (22, 23), "No", "second starts at the first's end"),
        ((20, 22), (20, 22), "Yes", "identical periods overlap"),
        ((20, 22), (19, 24), "Yes", "the second contains the first"),
    ]
    for i, (a, b, res, why) in enumerate(cases):
        y = 46 + i * 68
        s.text(10, y + 22, f"[{a[0]}, {a[1]}) and [{b[0]}, {b[1]})", size=17, font="'Plex Mono', monospace", weight=600, fill=NAVY)
        s.text(10, y + 48, f"Overlap: {res}. {why[0].upper() + why[1:]}", size=14.5, fill=SOFT)
        s.rect(xd(a[0]), y + 4, (a[1] - a[0]) * dw, 24, fill=NAVY, stroke=NAVY, rx=4)
        s.rect(xd(b[0]), y + 32, (b[1] - b[0]) * dw, 24, fill=COPPER, stroke=COPPER, rx=4)
    s.rect(340, 328, 22, 14, fill=NAVY, stroke=NAVY, rx=3)
    s.text(370, 340, "first period, always [20, 22)", size=15, fill=SOFT)
    s.rect(620, 328, 22, 14, fill=COPPER, stroke=COPPER, rx=3)
    s.text(650, 340, "second period", size=15, fill=SOFT)
    return s


def notation():
    s = Svg("ch02-notation", 345, label="The six relationships: association, dependency, aggregation, composition, inheritance and interface realisation, each drawn between two small boxes.")
    rows = [
        ("Association", "assoc", "Lasting link; arrowhead shows who holds it"),
        ("Dependency", "dep", "Uses another class without keeping it"),
        ("Aggregation", "agg", "Whole groups parts that exist on their own"),
        ("Composition", "comp", "Whole owns parts that need it to exist"),
        ("Inheritance", "inh", "Subclass is a kind of the superclass"),
        ("Realisation", "real", "Class implements the interface's contract"),
    ]
    for i, (name, kind, desc) in enumerate(rows):
        y = 8 + i * 55
        cy = y + 21
        s.text(10, cy + 6, name, size=19, weight=700, fill=NAVY, font="'Chakra Petch', sans-serif")
        a = s.node(230, y, 50, 42, "A", "box", size=17)
        b = s.node(420, y, 50, 42, "B", "box", size=17)
        s.rel(kind, [(a.x + a.w, cy), (b.x, cy)])
        s.text(500, cy + 6, desc, size=16, fill=INK)
    return s


def reserve_flow():
    s = Svg("ch02-reserve", 335, label="The reserve method as a flow: validate identifiers, count the borrower's records, apply the numeric rule, check for an overlapping reservation of the same item, then create, store and confirm. Two paths end in a rejection with nothing stored.")
    n1 = s.node(5, 55, 112, 70, "Validate\nidentifiers\nand start", "box", size=16)
    n2 = s.node(142, 55, 122, 70, "Count this\nborrower's\nrecords", "box", size=16)
    d1 = s.node(290, 40, 165, 100, "rules.mayRequest\n(count, days)?", "diamond", size=15)
    d2 = s.node(520, 40, 165, 100, "Overlaps a record\nfor this item?", "diamond", size=15)
    n5 = s.node(745, 55, 120, 70, "Create, add\nand return\nconfirmation", "dark", size=16)
    r1 = s.node(262, 225, 220, 62, "Rejected: borrower\nlimit or duration", "copper", size=16)
    r2 = s.node(492, 225, 220, 62, "Rejected:\nitem unavailable", "copper", size=16)
    s.edge([n1.a("r"), n2.a("l")])
    s.edge([n2.a("r"), d1.a("l")])
    s.edge([d1.a("r"), d2.a("l")], "allowed", label_at=(487, 80), size=15)
    s.edge([d2.a("r"), n5.a("l")], "free", label_at=(715, 80), size=15)
    s.edge([d1.a("b"), (d1.cx, r1.y)], "no", label_at=(d1.cx + 18, 188))
    s.edge([d2.a("b"), (d2.cx, r2.y)], "yes", label_at=(d2.cx + 20, 188))
    s.text(435, 322, "Neither rejection adds a record or uses an identifier.", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


DIAGRAMS = {
    "ch02-fig21": fig21,
    "ch02-fig22": fig22,
    "ch02-fig23": fig23,
    "ch02-fig24": fig24,
    "ch02-overlap": overlap,
    "ch02-notation": notation,
    "ch02-reserve": reserve_flow,
}


def git_areas():
    s = Svg("ch02-git", 250, label="Working files are staged with git add, then recorded with git commit. git diff compares working files with the staging area; git diff --staged compares the staging area with the last commit.")
    a = s.node(15, 30, 220, 76, "Working files\n(what you edit)", "box", size=19)
    b = s.node(325, 30, 220, 76, "Staging area\n(the next commit)", "copper", size=19)
    c = s.node(635, 30, 220, 76, "Recorded commits\n(history)", "dark", size=19)
    s.edge([a.a("r"), b.a("l")], "git add", label_at=(280, 62), size=17)
    s.edge([b.a("r"), c.a("l")], "git commit", label_at=(590, 62), size=17)
    for x0, x1, y, lab in ((125, 435, 150, "git diff"), (435, 745, 200, "git diff --staged")):
        s.path([(x0, 106), (x0, y), (x1, y), (x1, 106)], dash="3 5", sw=1.8)
        s.text((x0 + x1) / 2, y - 8, lab, size=17, anchor="middle", font="'Plex Mono', monospace", fill=NAVY, weight=600)
    s.text(435, 240, "Edit, stage the exact change, inspect it, then record it.", size=16, anchor="middle", fill=SOFT, italic=True)
    return s


def kit():
    s = Svg("ch02-kit", 372, label="One suitable kit model: an EquipmentKit groups one or more EquipmentItems (aggregation, an item is in at most one kit); an EquipmentItem keeps zero or more MaintenanceRecords (composition); the kit uses the Exporter interface, which CsvExporter implements.")
    kitb = s.cls(10, 10, "EquipmentKit", attrs=["-String name"], ops=["+summary(Exporter exporter) String"], row=23, size=15)
    item = s.cls(470, 10, "EquipmentItem", attrs=["-String itemId"], row=23, size=15)
    rec = s.cls(425, 200, "MaintenanceRecord", attrs=["-LocalDate performedOn", "-String note"], row=23, size=15)
    exp = s.cls(10, 190, "Exporter", ops=["+format(List<String> lines) String"], stereo="interface", row=23, size=15)
    csv = s.cls(10, 322, "CsvExporter", w=190)
    y = 52
    s.rel("agg", [(kitb.x + kitb.w, y), (item.x, y)], "groups", "0..1", "1..*")
    s.rel("comp", [(540, item.y + item.h), (540, rec.y)], "keeps", "1", "0..*")
    s.rel("dep", [(100, kitb.y + kitb.h), (100, exp.y)], "uses")
    s.rel("real", [(100, csv.y), (100, exp.y + exp.h)], "implements")
    return s


DIAGRAMS.update({"ch02-git": git_areas, "ch02-kit": kit})
