import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def workflow():
    s = Svg("ch15-workflow", 300, label="Figure 15.1: the six-step workflow of every AI activity. 1 Requirement and acceptance examples (yours), 2 bounded task and context, 3 candidate output, 4 independent checks. If the checks fail, return to the task. If they pass, 5 human acceptance, then 6 record.")
    r = s.node(0, 56, 190, 84, "1 Requirement and\nacceptance examples\n(yours)", "dark", size=14.5, weight=600)
    t = s.node(226, 56, 190, 84, "2 Bounded task\nand context", "box", size=15.5)
    c = s.node(452, 56, 190, 84, "3 Candidate\noutput", "box", size=15.5)
    v = s.node(678, 56, 190, 84, "4 Independent\nchecks", "box", size=15.5)
    a = s.node(678, 206, 190, 70, "5 Human\nacceptance", "box", size=15.5)
    w = s.node(452, 206, 190, 70, "6 Record", "copper", size=16, weight=600)
    s.edge([r.a("r"), t.a("l")])
    s.edge([t.a("r"), c.a("l")])
    s.edge([c.a("r"), v.a("l")])
    s.edge([v.a("t"), (v.cx, 28), (t.cx, 28), t.a("t")], "fails", label_at=(547, 20), size=13.5)
    s.edge([v.a("b"), a.a("t")], "passes", label_at=(v.cx + 38, 176), size=13.5)
    s.edge([a.a("l"), w.a("r")])
    s.text(4, 236, "The loop from the checks back to the task", size=14.5, anchor="start", fill=SOFT, italic=True)
    s.text(4, 256, "is where most of the work happens.", size=14.5, anchor="start", fill=SOFT, italic=True)
    s.text(4, 276, "A failed candidate is information: keep it.", size=14.5, anchor="start", fill=SOFT, italic=True)
    return s


def example():
    s = Svg("ch15-example", 270, label="Figure 15.2: the worked example. Prompt 1 gives attempt 1, which has an invented method and a Java 21 API and fails with 2 compile errors under release 17. Prompt 2 names the findings and asks for tests and gives attempt 2, which compiles and passes its 7 generated tests but fails acceptance examples EX4 and EX5. The developer's version is one class with the window loop corrected, passes all 9 acceptance examples, and is accepted and recorded.")
    p1 = s.node(0, 20, 210, 78, "Prompt 1:\ntask, context,\nconstraints, scope", "box", size=14)
    a1 = s.node(330, 20, 210, 78, "Attempt 1:\ninvented method,\nJava 21 API", "soft", size=14)
    p2 = s.node(660, 20, 210, 78, "Prompt 2:\nname the findings,\nask for tests", "box", size=14)
    a2 = s.node(660, 172, 210, 78, "Attempt 2:\ncompiles, 7 generated\ntests pass", "soft", size=14)
    h = s.node(330, 172, 210, 78, "Developer's version:\none class, window\nloop corrected", "copper", size=14)
    ok = s.node(0, 172, 210, 78, "Accepted\nand recorded", "dark", size=15, weight=600)
    s.edge([p1.a("r"), a1.a("l")])
    s.edge([a1.a("r"), p2.a("l")], "2 compile errors", label_at=(600, 52), size=13)
    s.edge([p2.a("b"), a2.a("t")])
    s.edge([a2.a("l"), h.a("r")], "EX4, EX5 fail", label_at=(600, 204), size=13)
    s.edge([h.a("l"), ok.a("r")], "9 examples pass", label_at=(270, 204), size=13)
    return s


DIAGRAMS = {"ch15-workflow": workflow, "ch15-example": example}
