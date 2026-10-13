import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def fig81():
    s = Svg("ch08-fig81", 255, label="Figure 8.1, Factory Method: the abstract ExportJob owns the workflow run and declares the protected createExporter hook. PlainJob and HtmlJob extend it and override the hook. ExportJob creates and uses an Exporter.")
    ej = s.cls(40, 10, "ExportJob", ops=["+run(value) String", "#createExporter() Exporter"], stereo="abstract", w=330, row=23, size=15)
    pj = s.cls(10, 195, "PlainJob", w=170)
    hj = s.cls(230, 195, "HtmlJob", w=170)
    ex = s.cls(580, 10, "Exporter", ops=["+export(value) String"], stereo="interface", w=270, row=23, size=15)
    s.rel("inh", [(95, pj.y), (95, ej.y + ej.h)])
    s.rel("inh", [(315, hj.y), (315, ej.y + ej.h)])
    s.rel("dep", [(ej.x + ej.w, 62), (ex.x, 62)], "creates and uses")
    s.text(75, 164, "extends", size=14.5, anchor="start", fill=SOFT, italic=True)
    return s


def family():
    s = Svg("ch08-family", 265, label="Abstract Factory: the ReceiptFamily interface creates a Heading and a Body. PlainFamily and HtmlFamily realise it and supply matching renderers for both roles.")
    rf = s.cls(290, 10, "ReceiptFamily", ops=["+heading() Heading", "+body() Body"], stereo="interface", w=290, row=23, size=15)
    he = s.cls(10, 10, "Heading", ops=["+render(text) String"], stereo="interface", w=200, row=23, size=15)
    bo = s.cls(660, 10, "Body", ops=["+render(text) String"], stereo="interface", w=200, row=23, size=15)
    pf = s.cls(110, 175, "PlainFamily", w=240)
    hf = s.cls(520, 175, "HtmlFamily", w=240)
    s.rel("dep", [(rf.x, 62), (he.x + he.w, 62)], "creates")
    s.rel("dep", [(rf.x + rf.w, 62), (bo.x, 62)], "creates")
    s.rel("real", [(230, pf.y), (230, rf.y + rf.h)])
    s.rel("real", [(640, hf.y), (640, rf.y + rf.h)])
    s.text(435, 250, "receipt(family, title, detail) uses only the interfaces: it holds no format switch.", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


def builder():
    s = Svg("ch08-builder", 270, label="A fluent builder collects settings (forBorrower, during, includeReturned, column) and build() validates them and copies the column list to publish an immutable ReportRequest.")
    s.rect(10, 15, 430, 235, fill=PAPER, stroke=COPPER, rx=12, dash="9 6")
    s.text(28, 45, "Builder (mutable, one construction sequence)", size=17, weight=700, fill=COPPER)
    rows = ['forBorrower("B1")', ".during(start, start.plusDays(7))", ".includeReturned(true)", '.column("item")', '.column("date")']
    for i, r in enumerate(rows):
        s.rect(28, 62 + i * 34, 394, 28, fill=WHITE, stroke=LINE, rx=5, sw=1.6)
        s.text(40, 82 + i * 34, r, size=16, font="'Plex Mono', monospace", fill=INK)
    s.edge([(440, 132), (530, 132)])
    s.text(485, 118, "build()", size=18, anchor="middle", weight=700, fill=NAVY, font="'Plex Mono', monospace")
    s.text(485, 158, "validate,", size=15, anchor="middle", fill=SOFT, italic=True)
    s.text(485, 176, "copy lists", size=15, anchor="middle", fill=SOFT, italic=True)
    rr = s.rect(530, 40, 330, 190, fill=TINT, stroke=NAVY, rx=10, sw=2.4)
    s.text(695, 74, "ReportRequest", size=20, anchor="middle", weight=700, fill=NAVY, font="'Chakra Petch', sans-serif")
    s.text(695, 98, "immutable", size=15, anchor="middle", fill=SOFT, italic=True)
    for i, r in enumerate(["borrowerId", "from / toExclusive", "includeReturned", "columns = List.copyOf(...)"]):
        s.text(552, 130 + i * 25, r, size=16, font="'Plex Mono', monospace", fill=INK)
    return s


def decorators():
    s = Svg("ch08-decorators", 300, label="Two compositions of the same decorators around a delegate that fails once and then succeeds. Audit outside retry records attempt and sent. Retry outside audit records attempt, failed, attempt, sent. Both make two delegate calls.")
    rows = [("AuditedSender", "RetryOnceSender", "attempt → sent", "one logical call · 2 delegate calls"),
            ("RetryOnceSender", "AuditedSender", "attempt → failed → attempt → sent", "every attempt audited · 2 delegate calls")]
    for i, (o, m, ev, note) in enumerate(rows):
        y = 25 + i * 135
        a = s.node(10, y, 150, 70, o, "box", size=15.5, weight=600)
        b = s.node(190, y, 150, 70, m, "box", size=15.5, weight=600)
        c = s.node(370, y, 150, 70, "delegate:\nfails once,\nthen succeeds", "copper", size=14.5)
        s.edge([a.a("r"), b.a("l")])
        s.edge([b.a("r"), c.a("l")])
        s.text(548, y + 22, "events:", size=15, fill=SOFT, italic=True)
        s.text(548, y + 46, ev, size=15, font="'Plex Mono', monospace", fill=INK, weight=600)
        s.text(548, y + 68, note, size=14, fill=SOFT, italic=True)
    return s


def _seq(name, h, label, parts, items):
    s = Svg(name, h, label=label)
    xs = {}
    for key, (text, cx) in parts.items():
        xs[key] = cx
        s.node(cx - 80, 6, 160, 50, text, "dark" if key == "S" else "box", size=15.5, weight=600)
        s.path([(cx, 56), (cx, h - 8)], stroke=LINE, sw=2, dash="6 6")
    for it in items:
        if it[0] == "msg":
            _, a, b, y, text, dashed = it
            x1, x2 = xs[a], xs[b]
            d = 1 if x2 > x1 else -1
            s.path([(x1 + 4 * d, y), (x2 - 4 * d, y)], stroke=NAVY, sw=2, dash="7 5" if dashed else None, end="arr")
            s.text((x1 + x2) / 2, y - 7, text, size=15, anchor="middle", fill=INK)
        elif it[0] == "note":
            _, a, b, y, text, *rest = it
            half = rest[0] if rest else 70
            x1, x2 = min(xs[a], xs[b]) - half, max(xs[a], xs[b]) + half
            s.rect(x1, y - 16, x2 - x1, 28, fill=WARM, stroke=COPPER, rx=5, sw=1.6)
            s.text((x1 + x2) / 2, y + 4, text, size=15, anchor="middle", fill=INK, italic=True)
        elif it[0] == "frame":
            _, y1, y2, text = it
            s.rect(14, y1, 842, y2 - y1, fill="none", stroke=COPPER, rx=6, sw=1.8)
            s.text(24, y1 + 18, text, size=14.5, fill=COPPER, weight=700, font="'Plex Mono', monospace")
        elif it[0] == "divider":
            _, y, text = it
            s.path([(14, y), (856, y)], stroke=COPPER, sw=1.6, dash="7 5")
            s.text(24, y + 17, text, size=14.5, fill=COPPER, weight=700, font="'Plex Mono', monospace")
    return s


PARTS = {"S": ("Reservation\nservice", 105), "A": ("Directory\nadapter", 340), "P": ("Provider\nclient", 575), "C": ("Coordinator", 780)}


def seq_ok():
    items = [("msg", "S", "A", 88, "find(borrowerId)", False),
             ("msg", "A", "P", 118, "lookup(borrowerId)", False),
             ("msg", "P", "A", 148, "Person(B2, T, Y)", True),
             ("msg", "A", "S", 178, "Borrower(B2, STAFF)", True),
             ("msg", "S", "C", 208, "reserve(..., STAFF)", False),
             ("msg", "C", "S", 238, "existing reservation outcome", True)]
    return _seq("ch08-seq-ok", 262, "Sequence for an active valid borrower: the service asks the adapter, the adapter asks the provider, the provider returns a record, the adapter returns a domain borrower, and the service calls the coordinator with the mapped category.", PARTS, items)


def seq_fail():
    items = [("msg", "S", "A", 86, "find(borrowerId)", False),
             ("msg", "A", "P", 112, "lookup(borrowerId)", False),
             ("frame", 126, 332, "alt"),
             ("msg", "P", "A", 160, "null, or status N", True),
             ("msg", "A", "S", 186, "Optional.empty()", True),
             ("note", "S", "C", 212, "no reservation, no notification"),
             ("divider", 232, "else  declared Failure"),
             ("msg", "P", "A", 268, "Failure", True),
             ("msg", "A", "S", 294, "DirectoryException (cause kept)", True),
             ("note", "S", "C", 320, "no reservation, no notification")]
    return _seq("ch08-seq-fail", 346, "Sequence for a missing or inactive borrower, or a declared provider failure: in both cases no reservation and no notification happen. Absence returns an empty result; a failure becomes a DirectoryException that keeps its cause.", PARTS, items)


DIAGRAMS = {"ch08-fig81": fig81, "ch08-family": family, "ch08-builder": builder, "ch08-decorators": decorators,
            "ch08-seq-ok": seq_ok, "ch08-seq-fail": seq_fail}
