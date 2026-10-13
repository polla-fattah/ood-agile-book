import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def boundaries():
    s = Svg("ch13-boundaries", 330, label="Figure 13.1: the two boundaries added by CR-12. The officer's command-line demo calls DirectoryReservationService, which calls LegacyDirectoryAdapter, then HttpLegacyDirectoryClient, which reaches the directory service over HTTP with a bounded wait. The service also calls VisitorGate, then FileApprovalSource, which reads approvals.tsv on every call, and ReservationCoordinator.")
    off = s.node(5, 128, 120, 64, "Officer:\ncommand-line\ndemo", "box", size=14.5)
    svc = s.node(160, 128, 200, 64, "Directory\nReservationService", "dark", size=15, weight=600)
    ada = s.node(300, 10, 150, 60, "Legacy\nDirectoryAdapter", "box", size=14.5)
    htp = s.node(490, 10, 175, 60, "HttpLegacy\nDirectoryClient", "box", size=14.5)
    dir_ = s.node(715, 10, 145, 60, "Directory service\n(stub in tests)", "copper", size=14)
    gate = s.node(300, 250, 165, 60, "VisitorGate\nflag, allowlist, window", "box", size=13.5)
    fil = s.node(505, 250, 160, 60, "FileApproval\nSource", "box", size=14.5)
    tsv = s.node(715, 250, 145, 60, "approvals.tsv", "copper", size=14.5)
    crd = s.node(490, 128, 175, 64, "Reservation\nCoordinator", "box", size=15)
    s.edge([off.a("r"), svc.a("l")])
    s.edge([(260, 128), (260, 40), ada.a("l")])
    s.edge([ada.a("r"), htp.a("l")])
    s.edge([htp.a("r"), dir_.a("l")])
    s.edge([svc.a("r"), crd.a("l")])
    s.edge([(260, 192), (260, 280), gate.a("l")])
    s.edge([gate.a("r"), fil.a("l")])
    s.edge([fil.a("r"), tsv.a("l")])
    s.text(690, 94, "HTTP, bounded wait", size=13.5, anchor="middle", fill=SOFT, italic=True)
    s.text(690, 238, "reads on every call", size=13.5, anchor="middle", fill=SOFT, italic=True)
    return s


def pipeline():
    s = Svg("ch13-pipeline", 300, label="Figure 13.2: the five-stage pipeline. Compile, then unit tests and architecture checks, then integration tests, then end-to-end journeys, then package a release candidate. Each arrow means only if the previous stage passed. A failure in stage 2, 3 or 4 stops the run and later stages do not run.")
    names = ["1 Compile", "2 Unit tests and\narchitecture\nchecks", "3 Integration\ntests", "4 End-to-end\njourneys", "5 Package:\nrelease\ncandidate"]
    kinds = ["box", "box", "box", "box", "dark"]
    bx = []
    for i, (t, k) in enumerate(zip(names, kinds)):
        bx.append(s.node(9 + i * 176, 14, 148, 92, t, k, size=15.5, weight=600))
    for a, b in zip(bx, bx[1:]):
        s.edge([a.a("r"), b.a("l")])
    stop = s.node(300, 196, 270, 64, "Stop: later stages\ndo not run", "copper", size=16, weight=600)
    s.edge([(bx[1].cx, 106), (bx[1].cx, 228), stop.a("l")], "fails", label_at=(bx[1].cx + 26, 168))
    s.edge([(bx[2].cx, 106), (bx[2].cx, 196)], "fails", label_at=(bx[2].cx + 28, 160))
    s.edge([(bx[3].cx, 106), (bx[3].cx, 228), stop.a("r")], "fails", label_at=(bx[3].cx + 26, 168))
    s.text(435, 288, "Each arrow means: only if the previous stage passed.", size=14.5, anchor="middle", fill=SOFT, italic=True)
    return s


def decision():
    s = Svg("ch13-decision", 335, label="Figure 13.3: the order of the visitor decision. Flag off: rejected, register not read. Item not CAM1 or CAM2: rejected. Fewer than one day: the gate steps aside and the coordinator rejects it, register not read. Otherwise read the clock once and the register once: unreadable or malformed is a failure with nothing reserved or sent; no valid matching approval is a rejection; valid at the request instant goes to the coordinator's count and duration rules, which either reject or pass to the availability, reservation and notice steps.")
    a = s.node(0, 104, 100, 66, "Visitor\nrequest\n(VISITOR)", "dark", size=13.5, weight=600)
    b = s.node(135, 95, 105, 84, "Flag on?", "diamond", size=14)
    c = s.node(272, 95, 118, 84, "Item CAM1\nor CAM2?", "diamond", size=13)
    d = s.node(422, 95, 118, 84, "Fewer than\none day?", "diamond", size=13)
    e = s.node(575, 104, 125, 66, "Read clock once\nand register\nonce", "box", size=13)
    f1 = s.node(732, 104, 136, 66, "FAILURE:\nnothing reserved\nor sent", "copper", size=13)
    r1 = s.node(105, 8, 135, 52, "Rejected:\nnot enabled", "soft", size=13.5)
    r2 = s.node(255, 8, 135, 52, "Rejected:\nitem not allowed", "soft", size=13.5)
    r4 = s.node(542.5, 8, 190, 52, "Rejected: no valid\nsponsor approval", "soft", size=13.5)
    g = s.node(432, 232, 200, 60, "Coordinator:\ncount and duration rules", "box", size=14, weight=600)
    r3 = s.node(150, 232, 200, 60, "Rejected: borrower\nlimit or duration", "soft", size=13.5)
    h = s.node(712, 232, 156, 60, "Availability,\nreservation, notice", "box", size=13.5)
    s.edge([a.a("r"), b.a("l")])
    s.edge([b.a("r"), c.a("l")], "yes", label_at=(256, 138), size=13)
    s.edge([c.a("r"), d.a("l")], "yes", label_at=(406, 138), size=13)
    s.edge([d.a("r"), e.a("l")], "no", label_at=(558, 138), size=13)
    s.edge([e.a("r"), f1.a("l")])
    s.edge([b.a("t"), r1.a("b")], "no", label_at=(b.cx + 16, 80), size=13)
    s.edge([c.a("t"), r2.a("b")], "no", label_at=(c.cx + 16, 80), size=13)
    s.edge([e.a("t"), r4.a("b")])
    s.edge([d.a("b"), (d.cx, 232)], "yes", label_at=(d.cx + 19, 205), size=13)
    s.edge([(e.cx + 20, 170), (e.cx + 20, 200), (600, 200), (600, 232)])
    s.edge([g.a("l"), r3.a("r")], "violated", label_at=(391, 252), size=13)
    s.edge([g.a("r"), h.a("l")], "met", label_at=(672, 252), size=13)
    s.text(e.cx + 8, 90, "no match", size=13, anchor="start", fill=SOFT, italic=True)
    s.text(e.cx + 30, 188, "valid at the", size=13, anchor="start", fill=SOFT, italic=True)
    s.text(e.cx + 30, 203, "request instant", size=13, anchor="start", fill=SOFT, italic=True)
    s.text(800, 190, "unreadable or", size=13, anchor="middle", fill=SOFT, italic=True)
    s.text(800, 205, "malformed", size=13, anchor="middle", fill=SOFT, italic=True)
    return s


DIAGRAMS = {"ch13-boundaries": boundaries, "ch13-pipeline": pipeline, "ch13-decision": decision}
