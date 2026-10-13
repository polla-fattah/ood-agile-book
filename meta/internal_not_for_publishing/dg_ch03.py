import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def board():
    s = Svg("ch03-board", 350, label="A five-column board: Backlog, Ready (US-03, US-04), Building (US-02), Review (EN-01, blocked) and Done (US-01). Building and Review share a combined work-in-progress limit of two, which is reached.")
    cols = ["Backlog", "Ready", "Building", "Review", "Done"]
    cards = {1: [("US-03", False), ("US-04", False)], 2: [("US-02", False)], 3: [("EN-01", True)], 4: [("US-01", False)]}
    w, g, x0 = 160, 10, 15
    for i, name in enumerate(cols):
        x = x0 + i * (w + g)
        s.rect(x, 38, w, 232, fill="#eef3f8", stroke=LINE, rx=8, sw=1.6)
        s.rect(x, 38, w, 38, fill=NAVY if name not in ("Done",) else DEEP, stroke=NAVY, rx=8, sw=1.6)
        s.text(x + w / 2, 63, name, size=19, anchor="middle", weight=700, fill="#ffffff", font="'Chakra Petch', sans-serif")
        for j, (cid, blocked) in enumerate(cards.get(i, [])):
            y = 90 + j * 62
            s.rect(x + 12, y, w - 24, 50, fill=WARM if blocked else WHITE, stroke=COPPER if blocked else NAVY, rx=6)
            s.text(x + w / 2, y + (22 if blocked else 31), cid, size=19, anchor="middle", weight=600, fill=INK)
            if blocked:
                s.text(x + w / 2, y + 41, "blocked", size=14.5, anchor="middle", fill=COPPER, italic=True, weight=600)
    s.text(x0 + 2 * (w + g) + w / 2, 26, "start point", size=15, anchor="middle", fill=SOFT, italic=True)
    s.text(x0 + 4 * (w + g) + w / 2, 26, "finish point", size=15, anchor="middle", fill=SOFT, italic=True)
    xa, xb = x0 + 2 * (w + g), x0 + 3 * (w + g) + w
    s.path([(xa, 282), (xa, 298), (xb, 298), (xb, 282)], stroke=COPPER, sw=2.6)
    s.text((xa + xb) / 2, 326, "WIP limit: 2 items in Building and Review combined", size=18, anchor="middle", weight=600, fill=COPPER)
    s.text(x0 + 80, 296, "Hypothetical snapshot", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


def sprint():
    s = Svg("ch03-sprint", 300, label="A Sprint of one month or less contains Sprint Planning, the Daily Scrum, the Sprint Review and the Sprint Retrospective.")
    s.rect(8, 44, 854, 232, fill="#f1f5fa", stroke=NAVY, rx=14, dash="9 6")
    s.text(24, 34, "Sprint: a fixed length of one month or less, containing all the events", size=18, weight=600, fill=NAVY)
    items = [
        (24, "Sprint\nPlanning", "why the Sprint matters,\nwhat is selected,\nand an approach"),
        (232, "Daily\nScrum", "Developers inspect\nprogress toward the\nSprint Goal and adapt"),
        (440, "Sprint\nReview", "inspect the outcome\nwith stakeholders;\nconsider adaptations"),
        (648, "Sprint\nRetrospective", "examine how the team\nworked; choose\nimprovements"),
    ]
    boxes = []
    for x, name, why in items:
        b = s.node(x, 68, 190, 76, name, "box", size=20, weight=700)
        s.lines(x + 95, 178, why.split("\n"), size=16, anchor="middle", fill=INK)
        boxes.append(b)
    for a, b in zip(boxes, boxes[1:]):
        s.edge([a.a("r"), b.a("l")])
    s.text(435, 268, "Together they inspect progress and adapt: the Sprint Goal ties the selected work to one outcome.", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


def commitments():
    s = Svg("ch03-commitments", 290, label="Scrum links each artefact to a commitment: the Product Backlog to the Product Goal, the Sprint Backlog to the Sprint Goal and the Increment to the Definition of Done.")
    rows = [("Product Backlog", "an ordered, emergent list", "Product Goal", "the future state to work toward"),
            ("Sprint Backlog", "goal, selected work, plan", "Sprint Goal", "why this Sprint's work belongs together"),
            ("Increment", "a usable step toward the goal", "Definition of Done", "the shared quality standard")]
    for i, (a, ad, c, cd) in enumerate(rows):
        y = 8 + i * 92
        A = s.node(10, y, 330, 82, a, "box", size=22, weight=700)
        s.text(175, y + 70, ad, size=14.5, anchor="middle", fill=SOFT, italic=True)
        C = s.node(530, y, 330, 82, c, "copper", size=22, weight=700)
        s.text(695, y + 70, cd, size=14.5, anchor="middle", fill=SOFT, italic=True)
        s.edge([A.a("r"), C.a("l")], "commitment", label_at=(435, y + 36), size=16)
    return s


DIAGRAMS = {"ch03-board": board, "ch03-sprint": sprint, "ch03-commitments": commitments}
