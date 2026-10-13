import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def footprint():
    s = Svg("ch14-footprint", 335, label="Figure 14.1: the footprint of the visitor change in production code. Five existing files changed (BorrowerCategory, DirectoryReservationService, ReservationApplication, LegacyDirectoryAdapter, LegacyDirectoryClient; 21 lines added and 3 removed). Nine new files hold 399 lines (VisitorReservationRules, VisitorGate, ApprovalRecord and ApprovalStatus, ApprovalSource and ApprovalSourceException, FileApprovalSource, HttpLegacyDirectoryClient, Chapter13Demo). DirectoryReservationService uses VisitorGate, ReservationApplication uses VisitorReservationRules, LegacyDirectoryClient is implemented by HttpLegacyDirectoryClient, VisitorGate uses ApprovalSource and ApprovalRecord, and FileApprovalSource implements ApprovalSource.")
    s.rect(2, 2, 266, 331, fill=PAPER, stroke=LINE, rx=8, sw=1.6)
    s.rect(400, 2, 468, 331, fill=PAPER, stroke=LINE, rx=8, sw=1.6)
    s.text(135, 26, "Existing code changed", size=15, anchor="middle", fill=COPPER, weight=700)
    s.text(135, 44, "5 files, +21 -3 lines", size=13.5, anchor="middle", fill=SOFT, italic=True)
    s.text(634, 26, "New production code", size=15, anchor="middle", fill=NAVY, weight=700)
    s.text(634, 44, "9 files, 399 lines", size=13.5, anchor="middle", fill=SOFT, italic=True)
    L = ["BorrowerCategory", "DirectoryReservationService", "ReservationApplication", "LegacyDirectoryAdapter", "LegacyDirectoryClient"]
    ys = [62, 120, 178, 236, 294]
    lb = [s.node(14, y, 240, 32, t, "copper", size=13.5) for y, t in zip(ys, L)]
    rec = s.node(415, 62, 210, 32, "ApprovalRecord, Status", "box", size=13.5)
    gate = s.node(415, 120, 210, 32, "VisitorGate", "box", size=14, weight=600)
    rul = s.node(415, 178, 210, 32, "VisitorReservationRules", "box", size=13.5)
    htp = s.node(415, 294, 210, 32, "HttpLegacyDirectoryClient", "box", size=13.5)
    asr = s.node(655, 120, 200, 32, "ApprovalSource, Exception", "box", size=13)
    fil = s.node(655, 178, 200, 32, "FileApprovalSource", "box", size=13.5)
    dem = s.node(655, 294, 200, 32, "Chapter13Demo", "box", size=13.5)
    s.edge([lb[1].a("r"), gate.a("l")])
    s.edge([lb[2].a("r"), rul.a("l")])
    s.edge([lb[4].a("r"), htp.a("l")])
    s.edge([gate.a("t"), rec.a("b")])
    s.edge([gate.a("r"), asr.a("l")])
    s.edge([fil.a("t"), asr.a("b")])
    s.text(330, 282, "implemented by", size=13.5, anchor="middle", fill=SOFT, italic=True)
    return s


def triage():
    s = Svg("ch14-triage", 320, label="Figure 14.2: triage of a known issue. If it blocks a requirement or the demonstration, fix it now with a check. Otherwise, if it needs a decision that is not ours, defer it and record the question, the owner and the trigger. Otherwise, if it is worth the cost and risk now, fix it now with a check; if not, accept it and state it as a limit.")
    a = s.node(0, 118, 100, 58, "A known\nissue", "dark", size=15, weight=600)
    b = s.node(125, 95, 200, 104, "Blocks a requirement\nor the demonstration?", "diamond", size=13)
    c = s.node(355, 95, 200, 104, "Needs a decision\nthat is not ours?", "diamond", size=13)
    e = s.node(585, 95, 200, 104, "Worth the cost\nand risk now?", "diamond", size=13)
    f = s.node(255, 6, 195, 58, "Fix now,\nwith a check", "copper", size=15, weight=600)
    d = s.node(330, 246, 250, 60, "Defer: record the question,\nthe owner and the trigger", "box", size=14)
    g = s.node(600, 246, 170, 60, "Accept: state it\nas a limit", "soft", size=14)
    s.edge([a.a("r"), b.a("l")])
    s.edge([b.a("r"), c.a("l")], "no", label_at=(340, 138), size=13)
    s.edge([c.a("r"), e.a("l")], "no", label_at=(570, 138), size=13)
    s.edge([b.a("t"), (b.cx, 35), f.a("l")], "yes", label_at=(b.cx - 22, 75), size=13)
    s.edge([e.a("t"), (e.cx, 35), f.a("r")], "yes", label_at=(e.cx + 22, 70), size=13)
    s.edge([c.a("b"), d.a("t")], "yes", label_at=(c.cx + 20, 224), size=13)
    s.edge([e.a("b"), g.a("t")], "no", label_at=(e.cx + 18, 224), size=13)
    return s


def chain():
    s = Svg("ch14-chain", 300, label="Figure 14.3: the chain that the requirements-to-evidence table records. A requirement or example leads to the class that decides it and to the test that checks it. The test leads to the pipeline stage that runs it. Both the class and the test are checked by TraceabilityTest, which asks whether the name still exists.")
    r = s.node(10, 124, 180, 62, "Requirement\nor example", "dark", size=16, weight=600)
    d = s.node(290, 28, 190, 60, "Class that\ndecides it", "box", size=16)
    t = s.node(290, 220, 190, 60, "Test that\nchecks it", "box", size=16)
    g = s.node(600, 118, 250, 74, "TraceabilityTest:\ndoes the name\nstill exist?", "copper", size=15, weight=600)
    sg = s.node(600, 222, 250, 56, "Pipeline stage\nthat runs it", "box", size=15)
    s.edge([(100, 124), (100, 58), d.a("l")])
    s.edge([(100, 186), (100, 250), t.a("l")])
    s.edge([d.a("r"), (g.cx, 58), g.a("t")])
    s.edge([(440, 220), (440, 155), g.a("l")])
    s.edge([(480, 250), (600, 250)])
    return s


DIAGRAMS = {"ch14-footprint": footprint, "ch14-triage": triage, "ch14-chain": chain}
