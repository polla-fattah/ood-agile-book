import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER


def cycle():
    s = Svg("ch01-cycle", 350, label="Figure 1.1: clarify the change, choose a small implementation, run checks and review, then ask whether the evidence supports acceptance. No: inspect the mismatch and return to clarify. Yes: demonstrate the increment, gather user feedback and return to clarify.")
    A = s.node(10, 20, 230, 70, "Clarify the\nrequested change", "box")
    B = s.node(300, 20, 230, 70, "Choose a small\nimplementation", "box")
    C = s.node(590, 20, 230, 70, "Run checks\nand review", "box")
    D = s.node(585, 150, 240, 100, "Evidence supports\nacceptance?", "diamond", size=17)
    E = s.node(300, 175, 230, 50, "Inspect the mismatch", "copper", size=18)
    F = s.node(585, 288, 240, 56, "Demonstrate\nthe increment", "box", size=17)
    G = s.node(300, 288, 230, 56, "Gather\nuser feedback", "box", size=17)
    s.edge([A.a("r"), B.a("l")])
    s.edge([B.a("r"), C.a("l")])
    s.edge([C.a("b"), D.a("t")])
    s.edge([D.a("l"), E.a("r")], "No", label_at=(557, 192))
    s.edge([E.a("l"), (171, 200), A.a("b", 0.7)])
    s.edge([D.a("b"), F.a("t")], "Yes", label_at=(738, 276))
    s.edge([F.a("l"), G.a("r")])
    s.edge([G.a("l"), (67.5, 316), A.a("b", 0.25)])
    return s


DIAGRAMS = {"ch01-cycle": cycle}
