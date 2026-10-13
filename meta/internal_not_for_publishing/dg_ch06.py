import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import Svg, NAVY, COPPER, INK, SOFT, LINE, WARM, TINT, WHITE, DEEP, PAPER


def fig61():
    s = Svg("ch06-fig61", 355, label="Source-level dependencies for the notification role: ReservationApplication creates the coordinator and the console sender; the coordinator holds the NotificationSender role; ConsoleNotificationSender and RecordingNotificationSender realise it.")
    o = 20
    app = s.cls(10, 10 + o, "ReservationApplication", w=240, ns=17)
    co = s.cls(10, 165 + o, "ReservationCoordinator", w=240, ns=17)
    ns_ = s.cls(350, 140 + o, "NotificationSender", ops=["+send(Reservation reservation) void"], stereo="interface", row=23, size=15, ns=17)
    con = s.cls(350, 10 + o, "ConsoleNotificationSender", w=270, ns=17)
    rec = s.cls(350, 285 + o, "RecordingNotificationSender", w=290, ns=17)
    s.rel("dep", [(app.x + app.w, 28 + o), (con.x, 28 + o)], "creates")
    s.rel("dep", [(130, app.y + app.h), (130, co.y)], "creates")
    s.rel("nav", [(co.x + co.w, 183 + o), (ns_.x, 183 + o)], "notifies")
    s.rel("real", [(470, con.y + con.h), (470, ns_.y)])
    s.rel("real", [(470, rec.y), (470, ns_.y + ns_.h)])
    s.text(765, 70, "Every “creates” arrow", size=16, anchor="middle", fill=COPPER, weight=600)
    s.text(765, 92, "starts at the application.", size=16, anchor="middle", fill=COPPER, weight=600)
    s.text(765, 312, "The policy map and the", size=14.5, anchor="middle", fill=SOFT, italic=True)
    s.text(765, 332, "formatter are built there too.", size=14.5, anchor="middle", fill=SOFT, italic=True)
    return s


def fig62():
    s = Svg("ch06-fig62", 370, label="Figure 6.2, the objects assembled at run time: the application entry point creates the policy map, the console sender, the formatter and the coordinator, and passes the first three to the coordinator's constructor.")
    app = s.node(10, 140, 190, 84, "Application\nentry point", "dark", size=18)
    pm = s.node(330, 12, 250, 62, "Student and staff\npolicy map", "box", size=17)
    cs = s.node(330, 150, 250, 62, "Console sender\ninstance", "box", size=17)
    fm = s.node(330, 290, 250, 62, "Confirmation\nformatter", "box", size=17)
    co = s.node(670, 140, 190, 84, "Coordinator\ninstance", "copper", size=18, weight=600)
    for t, n in ((0.5, pm), (0.5, cs), (0.5, fm)):
        pass
    s.edge([(200, 160), (330, 43)], dashed=True, color=COPPER)
    s.edge([(200, 182), (330, 181)], dashed=True, color=COPPER)
    s.edge([(200, 204), (330, 321)], dashed=True, color=COPPER)
    s.path([(100, 224), (100, 366), (765, 366), (765, 224)], stroke=COPPER, dash="7 5", end="arr")
    s.text(215, 358, "creates", size=15, anchor="middle", fill=COPPER, italic=True)
    s.text(264, 100, "creates", size=15, anchor="middle", fill=COPPER, italic=True)
    s.edge([(580, 43), (720, 43), (720, 140)])
    s.edge([cs.a("r"), co.a("l")])
    s.edge([(580, 321), (720, 321), (720, 224)])
    s.text(616, 36, "passed to the", size=14, anchor="start", fill=SOFT, italic=True)
    s.text(616, 52, "constructor", size=14, anchor="start", fill=SOFT, italic=True)
    return s


def failure():
    s = Svg("ch06-failure", 340, label="After a request is accepted, the record is stored, the confirmation formatted, and the sender called once. Normal return gives the confirmation. A NotificationException gives the confirmation plus a failure suffix with the record retained and no retry. Any other exception propagates after the record was stored.")
    b = []
    for i, (t, x, w) in enumerate([("Request accepted:\nchecks passed", 10, 190), ("Store the\nrecord", 225, 170), ("Format the\nconfirmation", 420, 170), ("notifications.send\n(reservation)", 615, 245)]):
        b.append(s.node(x, 15, w, 78, t, "dark" if i == 3 else "box", size=18, weight=600))
    for p, q in zip(b, b[1:]):
        s.edge([p.a("r"), q.a("l")])
    o1 = s.node(10, 215, 265, 110, "Returns normally\n\nthe confirmation", "round", size=18)
    o2 = s.node(300, 215, 295, 110, "NotificationException\n\nconfirmation + suffix\nrecord retained, no retry", "copper", size=17)
    o3 = s.node(620, 215, 240, 110, "Any other exception\n\npropagates; the record\nis already stored", "soft", size=17)
    s.edge([(737, 93), (737, 150), (142, 150), (142, 215)])
    s.edge([(737, 150), (447, 150), (447, 215)])
    s.edge([(737, 150), (737, 215)])
    s.text(437, 134, "one attempt per accepted request", size=15, anchor="middle", fill=SOFT, italic=True)
    return s


DIAGRAMS = {"ch06-fig61": fig61, "ch06-fig62": fig62, "ch06-failure": failure}
