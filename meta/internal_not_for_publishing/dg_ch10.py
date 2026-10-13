import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER
from dg_ch08 import _seq


def layers():
    s = Svg("ch10-layers", 345, label="Figure 10.1, permitted source dependencies: Bootstrap may refer to Presentation, Application and ports, and Infrastructure adapters. Presentation refers to Application. Application refers to Domain. Infrastructure refers to Application and to Domain. Domain refers to nothing else.")
    b = s.node(285, 10, 300, 62, "Bootstrap\nchoose implementations", "dark", size=17, weight=600)
    p = s.node(20, 130, 230, 66, "Presentation", "box", size=19, weight=600)
    a = s.node(320, 130, 230, 66, "Application\nand ports", "copper", size=18, weight=600)
    i = s.node(620, 130, 230, 66, "Infrastructure\nadapters", "box", size=18, weight=600)
    d = s.node(320, 255, 230, 66, "Domain", "box", size=19, weight=600)
    s.edge([b.a("b"), a.a("t")])
    s.edge([b.a("l"), (135, 41), p.a("t")])
    s.edge([b.a("r"), (735, 41), i.a("t")])
    s.edge([p.a("r"), a.a("l")])
    s.edge([i.a("l"), a.a("r")])
    s.edge([a.a("b"), d.a("t")])
    s.edge([i.a("b"), (735, 288), d.a("r")])
    s.text(20, 250, "A missing arrow means the", size=15, fill=SOFT, italic=True)
    s.text(20, 270, "reference is not permitted:", size=15, fill=SOFT, italic=True)
    s.text(20, 290, "Domain refers to nothing else.", size=15, fill=SOFT, italic=True)
    return s


def instability():
    s = Svg("ch10-instability", 362, label="Instability I = Ce / (Ca + Ce) of the checkpoint's packages: domain 0.00, application.port 0.18, infrastructure.notification 0.30, application 0.31, infrastructure.directory 0.33, infrastructure.persistence 0.50, presentation 0.50, bootstrap 1.00.")
    rows = [("domain", 0.00, 16, 0), ("application.port", 0.18, 14, 3), ("infrastructure.notification", 0.30, 7, 3),
            ("application", 0.31, 9, 4), ("infrastructure.directory", 0.33, 2, 1), ("infrastructure.persistence", 0.50, 1, 1),
            ("presentation", 0.50, 1, 1), ("bootstrap", 1.00, 0, 7)]
    s.text(285, 26, "package", size=14.5, anchor="end", fill=SOFT, weight=600)
    s.text(300, 26, "I = 0", size=14.5, fill=SOFT, weight=600)
    s.text(750, 26, "I = 1", size=14.5, anchor="end", fill=SOFT, weight=600)
    s.text(860, 26, "Ca / Ce", size=14.5, anchor="end", fill=SOFT, weight=600)
    for i, (name, v, ca, ce) in enumerate(rows):
        y = 40 + i * 37
        hot = name in ("infrastructure.notification", "application")
        s.text(285, y + 21, name, size=15.5, anchor="end", font="'Plex Mono', monospace", fill=COPPER if hot else INK, weight=600 if hot else 400)
        s.rect(300, y + 4, 450, 26, fill=PAPER, stroke=LINE, rx=4, sw=1.4)
        if v > 0:
            s.rect(300, y + 4, max(6, 450 * v), 26, fill=COPPER if hot else NAVY, stroke=COPPER if hot else NAVY, rx=4, sw=1.4)
        s.text(300 + 450 * v + 8 if v < 0.85 else 300 + 450 * v - 8, y + 23, f"{v:.2f}", size=15.5, anchor="start" if v < 0.85 else "end", weight=700,
               fill=INK if v < 0.85 else "#ffffff", font="'Plex Mono', monospace")
        s.text(860, y + 23, f"{ca} / {ce}", size=15, anchor="end", fill=SOFT, font="'Plex Mono', monospace")
    s.text(435, 354, "The orange pair is the one arrow that points to a slightly less stable package.", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


PARTS = {"P": ("Reservation\nConsole", 90), "S": ("Directory\nService", 260), "C": ("Reservation\nCoordinator", 430), "R": ("In-memory\nRepository", 600), "N": ("Notification\nsender impl.", 770)}


def sequence():
    items = [("msg", "P", "S", 88, "reserve(request)", False),
             ("note", "S", "S", 116, "resolve the borrower through the directory port", 200),
             ("msg", "S", "C", 148, "reserve with mapped category", False),
             ("msg", "C", "R", 172, "findAll() for policy and conflict checks", False),
             ("msg", "R", "C", 196, "snapshot", True),
             ("msg", "C", "R", 220, "add(accepted reservation)", False),
             ("msg", "C", "N", 244, "send(confirmed reservation)", False),
             ("msg", "N", "C", 268, "normal return, or NotificationException", True),
             ("note", "C", "C", 296, "on failure: keep the reservation, append the suffix", 210),
             ("msg", "C", "S", 330, "existing result string", True),
             ("msg", "S", "P", 354, "result string", True)]
    return _seq("ch10-seq", 378, "Figure 10.2: one accepted reservation at run time. The console calls the directory service, which calls the coordinator. The coordinator reads a snapshot from the repository, adds the accepted reservation, then calls the notification sender. The result string returns up the chain.", PARTS, items)


DIAGRAMS = {"ch10-layers": layers, "ch10-instability": instability, "ch10-seq": sequence}
