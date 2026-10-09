"""Build the English, source-labelled diagram gallery without external services.

Source: private review of the 2024 thesis, public documentation and UML sources.
No original PDF images, respondent records or identifiable persona imagery are copied.
Run from any directory; generated HTML is committed for build-free GitHub Pages.
"""

import textwrap
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/alyalbina/hotel-guest-experience-platform/blob/main/"


def label(x, y, value, size=18, weight=400, anchor="start", color="#1b3028"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{color}">{escape(value)}</text>'
    )


def paragraph(x, y, value, chars=28, size=18, leading=26):
    return "".join(
        label(x, y + i * leading, line, size) for i, line in enumerate(textwrap.wrap(value, chars))
    )


def box(x, y, w, h, title, detail="", fill="#fff", size=18):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="#b9c6b7"/>'
    title_chars = max(12, int((w - 32) / (size * 0.55)))
    s += paragraph(x + 16, y + 30, title, title_chars, size, 26)
    if detail:
        detail_y = y + max(72, 66 + (len(textwrap.wrap(title, title_chars)) - 1) * 26)
        s += paragraph(x + 16, detail_y, detail, max(12, int((w - 32) / 9)), 16, 24)
    return s


def line(x1, y1, x2, y2, arrow=False, dashed=False):
    return (
        f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#53705c" stroke-width="2"'
        + (' marker-end="url(#arrow)"' if arrow else "")
        + (' stroke-dasharray="7 6"' if dashed else "")
        + "/>"
    )


def path(points, arrow=True, dashed=False):
    coords = " L".join(f"{x},{y}" for x, y in points)
    return (
        f'<path d="M{coords}" fill="none" stroke="#53705c" stroke-width="2"'
        + (' marker-end="url(#arrow)"' if arrow else "")
        + (' stroke-dasharray="7 6"' if dashed else "")
        + "/>"
    )


def svg(title, subtitle, body, height=560, width=1120):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
        f'<desc>{escape(subtitle)}</desc><defs><marker id="arrow" markerWidth="9" '
        'markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" '
        'fill="none" stroke="#53705c" stroke-width="1.5"/></marker></defs>'
        f'<rect width="{width}" height="{height}" fill="#f7f8f3"/>'
        + label(32, 40, title, 24, 600)
        + label(32, 70, subtitle, 15, color="#5e6b63")
        + body
        + "</svg>"
    )


def affinity():
    groups = [
        (
            "Information & communication",
            "Service information is inconsistent. Guests struggle to understand how to ask for help.",
            "Product opportunity",
            "Structured service catalog and actionable request details.",
        ),
        (
            "Room amenities",
            "Room comfort, Wi-Fi and available facilities shape the stay experience.",
            "Operational boundary",
            "The queue can capture issues; it cannot upgrade facilities.",
        ),
        (
            "Stay conditions",
            "Booking friction, service delays and execution quality recur in the thesis synthesis.",
            "MVP focus",
            "Select the request-handling portion of this broader theme.",
        ),
        (
            "Staff skills",
            "Staff knowledge, communication and professional service need attention.",
            "Operational boundary",
            "Training and incentives remain hotel-management work.",
        ),
    ]
    body = ""
    for i, (title, evidence, heading, decision) in enumerate(groups):
        x = 32 + i * 270
        body += box(x, 112, 252, 342, title, fill=["#e7e2f0", "#ddeaf0", "#dfede3", "#eef1e7"][i])
        body += paragraph(x + 16, 206, evidence, 24, 16, 24)
        body += label(x + 16, 335, heading, 16, 600)
        body += paragraph(x + 16, 370, decision, 24, 16, 24)
    body += label(
        32,
        500,
        "Original cluster headings translated; summaries reconstructed from the thesis narrative.",
        16,
    )
    body += label(32, 528, "No fabricated interview quotes, sticky-note counts or theme frequencies.", 16)
    return svg("Affinity synthesis", "Thesis p. 17, Figure 2 | English reconstruction, 2026", body, 558)


def fishbone():
    body = line(80, 350, 825, 350, True)
    groups = [
        (
            80,
            120,
            "People",
            ["Insufficient staff skills", "Communication barriers", "Low motivation"],
            300,
            350,
        ),
        (
            435,
            120,
            "Process",
            ["Inefficient task allocation", "Missing standards", "Integration difficulties"],
            700,
            350,
        ),
        (
            80,
            405,
            "Technology",
            ["Limited access to data", "Insufficient automation", "Outdated software / equipment"],
            300,
            350,
        ),
        (
            435,
            405,
            "Environment & infrastructure",
            ["Organizational culture", "Inconvenient workspace layout"],
            700,
            350,
        ),
    ]
    for x, y, title, causes, ex, ey in groups:
        body += line(x + 280, y + (155 if y < 350 else 0), ex, ey)
        body += box(x, y, 330, 172, title, fill="#eef1e7")
        for j, cause in enumerate(causes):
            body += label(x + 16, y + 72 + j * 29, cause, 16)
    body += box(850, 280, 235, 155, "Delayed service requests", "Effect examined in the thesis", "#dbe7bd")
    body += label(
        32,
        620,
        "The app targets capture, allocation and information flow. Training and facilities stay outside scope.",
        16,
    )
    return svg(
        "Root-cause map / Fishbone",
        "Thesis pp. 19-20, Figure 5 | Translated categories and causes",
        body,
        654,
    )


def table_svg(title, subtitle, columns, rows, cellw=170, rowh=130):
    width = 190 + len(columns) * cellw
    body = ""
    for i, column in enumerate(["Dimension"] + columns):
        x = 20 if i == 0 else 170 + (i - 1) * cellw
        w = 150 if i == 0 else cellw
        body += box(x, 110, w, 72, column, fill="#dbe7bd", size=17)
    for r, (name, values) in enumerate(rows):
        y = 182 + r * rowh
        body += box(20, y, 150, rowh, name, fill="#eef1e7", size=17)
        for i, value in enumerate(values):
            x = 170 + i * cellw
            body += f'<rect x="{x}" y="{y}" width="{cellw}" height="{rowh}" fill="#fff" stroke="#d9dfd4"/>'
            body += paragraph(x + 12, y + 28, value, int((cellw - 24) / 8.5), 16, 24)
    return svg(title, subtitle, body, 202 + len(rows) * rowh, width)


def journey():
    return table_svg(
        "Customer Journey Map / full hotel journey",
        "Thesis p. 18, Figure 3 | Persona wording summarized; emotions are interpretations",
        ["Booking", "Check-in", "Stay", "Request service", "Check-out", "Review"],
        [
            (
                "Guest goal",
                [
                    "Choose a suitable hotel",
                    "Access the room quickly",
                    "Use facilities comfortably",
                    "Get a clear, timely service",
                    "Leave without friction",
                    "Share feedback",
                ],
            ),
            (
                "Touchpoint",
                [
                    "Booking site",
                    "Reception",
                    "Room, Wi-Fi, restaurant",
                    "Room phone / reception",
                    "Reception / bill",
                    "Review platform",
                ],
            ),
            (
                "Friction",
                [
                    "Navigation and missing information",
                    "Waiting and inconsistent information",
                    "Wi-Fi / service quality",
                    "Delays and lost request details",
                    "Slow answers and billing information",
                    "Weak link to improvement",
                ],
            ),
            (
                "Experience",
                [
                    "Uncertainty / relief",
                    "Impatience / irritation",
                    "Comfort or frustration",
                    "Expectations / disappointment",
                    "Tension about delays",
                    "Reflection / disappointment",
                ],
            ),
            (
                "Product scope",
                [
                    "Outside MVP",
                    "Self-reported room only",
                    "Capture service issues",
                    "Core intake and staff workflow",
                    "Outside MVP",
                    "Per-request CSAT only",
                ],
            ),
        ],
        rowh=137,
    )


def blueprint():
    return table_svg(
        "Service Blueprint / broader hotel experience",
        "Thesis p. 19, Figure 4 | Layer relationships reconstructed; no persona portrait copied",
        ["Booking", "Arrival", "Stay / services", "Departure", "Review"],
        [
            (
                "Evidence",
                [
                    "Hotel / booking site",
                    "Reception",
                    "Room, facilities",
                    "Reception / bill",
                    "Review platform",
                ],
            ),
            (
                "Guest",
                [
                    "Book hotel",
                    "Register at reception",
                    "Use services / ask for help",
                    "Pay and check out",
                    "Publish feedback",
                ],
            ),
            (
                "Frontstage",
                [
                    "Provide service information",
                    "Register guest / give room",
                    "Interact and fulfill",
                    "Explain bill / departure",
                    "Respond to feedback",
                ],
            ),
            (
                "Backstage",
                [
                    "Process reservation",
                    "Prepare room / registration",
                    "Coordinate departments",
                    "Process account",
                    "Analyze feedback",
                ],
            ),
            (
                "Support",
                [
                    "Booking / operations IT",
                    "Training / preparation",
                    "Maintenance / support",
                    "Finance / operations",
                    "Feedback analytics",
                ],
            ),
        ],
        cellw=195,
        rowh=120,
    )


def stakeholders():
    body = line(110, 485, 1000, 485, True) + line(110, 485, 110, 115, True)
    body += line(555, 130, 555, 475, False, True) + line(125, 305, 980, 305, False, True)
    body += label(990, 520, "Interest", 17, anchor="end") + label(35, 105, "Influence", 17)
    for x, y, title in [
        (680, 145, "Hotel leadership"),
        (615, 230, "Service managers"),
        (615, 325, "Hotel staff"),
        (320, 245, "VIP guests"),
        (450, 400, "Hotel guests"),
    ]:
        body += box(x, y, 240, 60, title, fill="#fff")
    body += label(
        140,
        568,
        "Placement is qualitative, translated from the original matrix. It is not a scored survey.",
        16,
    )
    return svg(
        "Stakeholder influence / interest", "Thesis pp. 23-24, Figure 6 | English reconstruction", body, 604
    )


def asis():
    body = ""
    for x, title in [(30, "Guest"), (395, "Reception"), (760, "Department")]:
        body += box(x, 110, 330, 510, title, fill="#eef1e7")
    body += line(190, 250, 190, 285, True) + line(310, 333, 430, 333, True)
    body += line(550, 365, 550, 395, True) + line(670, 440, 795, 440, True)
    body += path([(925, 491), (925, 555), (670, 555)])
    body += path([(430, 575), (350, 575), (350, 600), (190, 600), (190, 550)])
    body += label(205, 590, "if unresolved", 15)
    body += path([(70, 333), (50, 333), (50, 480), (70, 480)])
    body += label(65, 414, "if no answer", 15)
    for args in [
        (70, 180, 70, "Need service", ""),
        (70, 285, 96, "Phone or visit reception", ""),
        (70, 430, 120, "Abandon / repeat contact", "If no answer or unresolved"),
        (430, 285, 80, "Accept request", ""),
        (430, 395, 96, "Fulfill or hand off", "Manual responsibility"),
        (795, 395, 96, "Perform service", ""),
        (430, 515, 96, "Report completion", "Guest satisfaction loop"),
    ]:
        x, y, h, t, d = args
        body += box(x, y, 240, h, t, d, size=17)
    return svg(
        "AS-IS / manual service handling",
        "Thesis pp. 24-26, Figure 7 | Condensed swimlane reconstruction",
        body,
        650,
    )


def tobe():
    body = ""
    steps = [
        ("Guest", "Register and select service", "Telegram guest interface"),
        ("System", "Record the request", "Google Sheets / original bot"),
        ("Staff", "Filter and inspect tasks", "AppSheet staff application"),
        ("Staff", "Assign and update status", "Employee / department workflow"),
    ]
    for i, (actor, title, d) in enumerate(steps):
        y = 112 + i * 117
        if i:
            body += line(560, y - 18, 560, y, True)
        body += label(200, y + 48, actor, 20, 600)
        body += box(340, y, 610, 98, title, d, "#fff")
    body += label(
        32, 608, "Thesis concept, not proof of live staff integration. AppSheet is no longer available.", 16
    )
    body += label(
        32,
        637,
        "2026 changes: SQLite is authoritative; a web workspace replaces AppSheet; Sheets export is optional.",
        16,
    )
    return svg(
        "TO-BE / original prototype concept",
        "Thesis pp. 40-43, 64-73 | Reconstructed from process and implementation evidence",
        body,
        668,
    )


def furps():
    groups = [
        ("F / Functionality", "Capture, classify, assign and track requests. FR-01 to FR-09."),
        (
            "U / Usability",
            "Clear catalog and staff workflow. Browser checks; broader accessibility remains planned.",
        ),
        ("R / Reliability", "Atomic save and duplicate protection. Sheets is outside the intake dependency."),
        (
            "P / Performance",
            "Async adapter avoids blocking the event loop. No load or p95 result is claimed.",
        ),
        ("S / Supportability", "Reproducible setup, documented modules and automated checks."),
        (
            "+ / Constraints",
            "Minimal public data, UTC times, role controls. Verified hotel identity and private hosting remain planned.",
        ),
    ]
    body = ""
    for i, (title, d) in enumerate(groups):
        x = 32 + i % 2 * 544
        y = 112 + i // 2 * 163
        body += box(x, y, 520, 142, title, d)
    return svg(
        "FURPS+ / quality requirements",
        "Thesis pp. 27-31, Figure 8 | Framework translated; current controls and limits added",
        body,
        620,
    )


def actor(x, y, title):
    return (
        f'<circle cx="{x}" cy="{y}" r="13" fill="none" stroke="#53705c" stroke-width="2"/>'
        + line(x, y + 13, x, y + 52)
        + line(x - 25, y + 27, x + 25, y + 27)
        + line(x, y + 52, x - 20, y + 80)
        + line(x, y + 52, x + 20, y + 80)
        + label(x, y + 107, title, 17, anchor="middle")
    )


def usecase():
    body = '<rect x="245" y="110" width="630" height="600" fill="#fff" stroke="#b9c6b7"/>'
    body += label(270, 146, "Current platform boundary", 20, 600)
    cases = [
        ("Intake", 405, 210, "Register / submit"),
        ("Lookup", 405, 320, "Own request status"),
        ("Rate", 405, 430, "Rate resolved service"),
        ("Login", 695, 210, "Sign in as staff"),
        ("Inspect", 695, 320, "Filter / inspect"),
        ("Assign", 695, 430, "Assign employee"),
        ("Update", 695, 540, "State / add note"),
        ("Metrics", 405, 630, "Review metrics"),
    ]
    centers = {k: (x, y) for k, x, y, _ in cases}
    for x, y, keys in [
        (110, 260, ["Intake", "Lookup", "Rate"]),
        (1010, 150, ["Login", "Inspect", "Assign", "Update", "Metrics"]),
        (1010, 370, ["Login", "Inspect", "Assign", "Update", "Metrics"]),
        (110, 560, ["Login", "Inspect", "Metrics"]),
    ]:
        for key in keys:
            cx, cy = centers[key]
            body += line(x + (26 if x < 245 else -26), y + 27, cx + (-126 if x < 245 else 126), cy)
    for _, x, y, title in cases:
        body += f'<ellipse cx="{x}" cy="{y}" rx="128" ry="37" fill="#eef1e7" stroke="#b9c6b7"/>'
        body += label(x, y + 6, title, 17, anchor="middle")
    for args in [(110, 260, "Guest"), (1010, 150, "Manager"), (1010, 370, "Agent"), (110, 560, "Analyst")]:
        body += actor(*args)
    body += label(
        32,
        750,
        "Agent is department-scoped; analyst is read-only. Guest identity is self-reported, not hotel SSO.",
        16,
    )
    return svg("UML / Use Case", "Current 2026 model | Thesis use-case concept: pp. 35-37", body, 786)


def class_box(x, y, w, title, attrs, methods=()):
    height = 58 + len(attrs) * 25 + (len(methods) * 25 + 15 if methods else 0)
    s = box(x, y, w, height, title, fill="#fff") + line(x, y + 44, x + w, y + 44)
    for i, a in enumerate(attrs):
        s += label(x + 12, y + 71 + i * 25, a, 16)
    if methods:
        my = y + 57 + len(attrs) * 25
        s += line(x, my, x + w, my)
        for i, m in enumerate(methods):
            s += label(x + 12, my + 25 + i * 25, m, 16)
    return s


def classes():
    body = line(280, 190, 405, 190) + label(292, 180, "1", 16) + label(363, 180, "0..*", 16)
    body += path([(535, 253), (535, 390)], False) + label(547, 277, "1", 16) + label(547, 377, "0..*", 16)
    body += (
        line(940, 228, 940, 390)
        + label(952, 255, "0..*", 16)
        + label(952, 377, "0..1", 16)
        + path([(810, 450), (770, 450), (770, 330), (160, 330), (160, 390)], False)
        + label(780, 440, "1", 16)
        + label(170, 378, "0..*", 16)
    )
    body += (
        path([(810, 190), (745, 190), (745, 500), (685, 500)], False)
        + label(749, 223, "0..1", 16)
        + label(698, 490, "0..*", 16)
    )
    body += path([(280, 460), (405, 460)], False) + label(292, 450, "1", 16) + label(363, 450, "0..*", 16)
    body += (
        path([(535, 613), (535, 710), (810, 710)], False)
        + label(547, 680, "1", 16)
        + label(763, 700, "1..*", 16)
    )
    body += class_box(40, 120, 240, "Room", ["id : text"])
    body += class_box(
        405, 120, 260, "Guest", ["id : integer", "telegram_id : integer", "name / room_id : text"]
    )
    body += class_box(810, 120, 260, "Staff", ["id / department_id", "role : manager|agent|analyst"])
    body += class_box(40, 390, 240, "Category", ["id / department_id"])
    body += class_box(
        405,
        390,
        280,
        "Request",
        ["id / status / version", "responded_at : UTC", "resolved_at : UTC"],
        ["acknowledge()", "resolve()", "reopen(reason)"],
    )
    body += class_box(810, 390, 260, "Department", ["id : text", "sla_minutes : integer"])
    body += class_box(810, 650, 260, "RequestEvent", ["action / note", "occurred_at : UTC"])
    body += label(
        32,
        835,
        "Selected logical relationships. Complete multiplicities and staff/event links: class.puml.",
        16,
    )
    body += label(
        32,
        862,
        "Domain operations live in a service over SQLite rows; these are not ORM class declarations.",
        16,
    )
    return svg("UML / logical Class view", "Current 2026 model | Thesis class concept: pp. 37-40", body, 894)


def activity():
    body = ""
    for x, title in [(32, "Guest"), (397, "System"), (762, "Staff")]:
        body += box(x, 110, 325, 1060, title, fill="#eef1e7")
    body += '<circle cx="195" cy="172" r="10" fill="#254d3b"/>'
    body += line(195, 182, 195, 210, True)
    body += path([(320, 270), (555, 270), (555, 352)])
    body += line(555, 408, 555, 455, True) + label(572, 435, "yes", 16)
    body += line(513, 380, 320, 380, True) + label(390, 367, "no", 16)
    body += line(195, 436, 195, 475, True)
    body += line(555, 551, 555, 572, True)
    body += line(513, 600, 320, 600, True) + label(390, 587, "yes", 16)
    body += path([(597, 600), (720, 600), (720, 720), (680, 720)]) + label(660, 587, "no", 16)
    body += line(555, 795, 555, 810, True)
    body += path([(320, 622), (922, 622), (922, 670)])
    body += line(922, 748, 922, 800, True)
    body += line(922, 878, 922, 917, True)
    body += path([(880, 945), (800, 945), (800, 710), (825, 710)]) + label(776, 852, "reopen", 15)
    body += path([(964, 945), (1090, 945), (1090, 980), (195, 980), (195, 1000)])
    body += label(992, 935, "no", 16)
    body += line(195, 1078, 195, 1110, True)
    for x, y, w, h, t, d in [
        (70, 210, 250, 120, "Choose / describe service", "Room and name context"),
        (70, 350, 250, 86, "Ask for correction", ""),
        (430, 455, 250, 96, "Save request + event", "Atomic transaction"),
        (70, 560, 250, 98, "Receive saved ID", ""),
        (430, 675, 250, 120, "Rollback / retry guidance", "No false success"),
        (825, 670, 250, 78, "Assign / acknowledge", ""),
        (825, 800, 250, 78, "Perform / resolve", ""),
        (70, 1000, 250, 78, "Check / optionally rate", ""),
    ]:
        body += box(x, y, w, h, t, d)
    for cx, cy, title in [(555, 380, "Valid?"), (555, 600, "Saved?"), (922, 945, "More work?")]:
        body += f'<polygon points="{cx},{cy - 28} {cx + 42},{cy} {cx},{cy + 28} {cx - 42},{cy}" fill="#dbe7bd" stroke="#53705c"/>'
        body += label(cx, cy + 5, title, 14, anchor="middle")
    for cx, cy in [(195, 488), (555, 823), (195, 1123)]:
        body += f'<circle cx="{cx}" cy="{cy}" r="13" fill="none" stroke="#254d3b" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="8" fill="#254d3b"/>'
    return svg(
        "UML / Activity with responsibilities",
        "Current 2026 model | Thesis TO-BE activity: pp. 40-42",
        body,
        1185,
    )


def sequence():
    body = ""
    people = [(100, "Guest"), (320, "Bot"), (540, "Service"), (760, "SQLite"), (980, "Staff via API")]
    for x, title in people:
        body += box(x - 80, 112, 160, 62, title, size=17) + line(x, 174, x, 705, False, True)
    rows = [
        (100, 320, 222, "Select service / details", False),
        (320, 540, 280, "create_request(source_ref)", False),
        (540, 760, 338, "BEGIN: request + event", False),
        (760, 540, 412, "Commit: durable ID", True),
        (540, 320, 470, "Request ID", True),
        (320, 100, 528, "Saved confirmation", True),
        (980, 540, 590, "Authenticated change + version", False),
        (540, 760, 648, "Check version; update + event", False),
    ]
    for x1, x2, y, title, dashed in rows:
        body += line(x1, y, x2, y, True, dashed) + label((x1 + x2) / 2, y - 10, title, 16, anchor="middle")
    body += box(
        32,
        750,
        1055,
        100,
        "Failure branch",
        "Persistence error rolls back the transaction and returns retry guidance. The bot does not confirm success.",
        "#dbe7bd",
    )
    return svg(
        "UML / durable intake Sequence",
        "Current 2026 model | Thesis sequence: pp. 42-43; current failure branch: sequence.puml",
        body,
        884,
    )


def states():
    body = '<circle cx="560" cy="110" r="10" fill="#254d3b"/>' + line(560, 120, 560, 140, True)
    body += line(560, 205, 560, 265, True) + line(560, 330, 560, 390, True) + line(560, 455, 560, 530, True)
    body += path([(405, 562), (170, 562), (170, 680)], True) + label(155, 623, "reason", 16)
    body += path([(325, 712), (355, 712), (355, 420), (405, 420)], True)
    body += path([(325, 740), (370, 740), (370, 590), (405, 590)], True)
    body += path([(405, 300), (350, 300), (350, 550), (405, 550)], True)
    for y in [173, 298, 423]:
        body += path([(715, y), (760, y), (760, 562), (825, 562)], True)
    body += path([(325, 767), (780, 767), (780, 588), (825, 588)], True)
    body += line(942, 625, 942, 705, True)
    body += '<circle cx="942" cy="718" r="13" fill="none" stroke="#254d3b" stroke-width="2"/><circle cx="942" cy="718" r="8" fill="#254d3b"/>'
    for x, y, w, h, title, detail in [
        (405, 140, 310, 65, "New", ""),
        (405, 265, 310, 65, "Acknowledged", ""),
        (405, 390, 310, 65, "InProgress", ""),
        (405, 530, 310, 100, "Resolved", "May reopen"),
        (45, 680, 280, 105, "Reopened", "Clear current rating / resolution"),
        (825, 530, 235, 95, "Cancelled", "Reason; terminal"),
    ]:
        body += box(x, y, w, h, title, detail, "#fff")
    body += label(
        32,
        836,
        "All allowed transitions shown. First response / first resolution are retained; stale changes are rejected.",
        16,
    )
    return svg(
        "UML / enforced State lifecycle",
        "Current 2026 model | Thesis lifecycle: pp. 43-45; exact transitions: state.puml",
        body,
        872,
    )


def components():
    body = path([(280, 175), (440, 270)], True) + path([(280, 375), (440, 290)], True)
    body += line(720, 280, 825, 280, True) + path([(280, 400), (500, 550)], True)
    body += path([(600, 350), (600, 510)], True)
    body += path([(940, 350), (940, 675), (715, 675)], True)
    body += path([(430, 675), (310, 675)], True)
    for x, y, w, h, t, d in [
        (32, 120, 248, 110, "<<component>> Bot", "aiogram adapter"),
        (32, 320, 248, 130, "<<component>> API", "FastAPI / session / CSRF / roles"),
        (440, 210, 280, 140, "<<component>> Domain", "Shared service logic"),
        (825, 210, 260, 140, "<<database>> SQLite", "Authoritative request store"),
        (440, 510, 370, 100, "<<component>> Metrics", "Creation-cohort calculation"),
        (430, 630, 285, 110, "<<component>> Export", "Explicit CLI snapshot"),
        (32, 630, 278, 110, "<<external>> Sheets", "Optional RAW snapshot"),
    ]:
        body += box(x, y, w, h, t, d)
    body += label(
        32,
        800,
        "Intake has no Sheets dependency. Simplified component view; complete dependency sources: component.puml.",
        16,
    )
    return svg(
        "UML / Component boundaries", "Current 2026 model | Thesis component concept: pp. 45-48", body, 835
    )


def deployment():
    body = line(282, 210, 415, 210, True) + path([(290, 430), (290, 335), (560, 335), (560, 310)], True)
    body += path([(940, 310), (940, 430)], True) + path([(290, 565), (290, 650), (320, 650)], True)
    body += path([(810, 565), (810, 650), (800, 650)], True) + line(560, 718, 560, 785, True)
    body += box(32, 130, 250, 180, "<<device>> Guest", "Telegram client")
    body += box(415, 130, 295, 180, "<<external>> Telegram", "Bot API; polling / replies")
    body += box(810, 130, 275, 180, "<<device>> Staff", "Web browser")
    body += '<rect x="32" y="360" width="1053" height="390" fill="none" stroke="#b9c6b7"/>' + label(
        55, 398, "<<node>> Single application host", 22, 600
    )
    body += box(80, 430, 420, 135, "<<execution environment>> Bot process", "Python / aiogram")
    body += box(600, 430, 420, 135, "<<execution environment>> Web process", "Python / FastAPI")
    body += box(320, 625, 480, 93, "<<artifact>> Shared SQLite file", "One host; one database path")
    body += box(320, 785, 480, 95, "Optional manual Sheets export", "Requires separately issued credentials")
    body += label(
        32,
        928,
        "Local full application. GitHub Pages is a separate synthetic preview, not the Python backend host.",
        16,
    )
    return svg("UML / Deployment", "Current 2026 model | Thesis deployment concept: pp. 48-53", body, 962)


def erd():
    body = line(280, 192, 415, 192) + label(302, 182, "1 : many", 16)
    body += line(690, 192, 815, 192) + label(710, 182, "1 : many", 16)
    body += path([(145, 450), (145, 350), (925, 350), (925, 290)], False) + label(
        415, 337, "Department / category / assignee foreign keys", 16
    )
    body += path([(925, 290), (925, 450)], False) + label(935, 393, "1 : many", 16)
    body += path([(560, 560), (560, 645), (360, 645)], False) + label(376, 632, "staff has sessions", 16)
    body += class_box(32, 112, 250, "ROOMS", ["id PK"])
    body += class_box(415, 112, 275, "GUESTS", ["id PK", "telegram_id UK", "room_id FK"])
    body += class_box(
        815,
        112,
        275,
        "REQUESTS",
        [
            "id PK; guest_id FK",
            "category / department FK",
            "assigned_to FK; version",
            "state / UTC timestamps",
        ],
    )
    body += class_box(32, 450, 280, "DEPARTMENTS / CATEGORIES", ["id PK", "category.department_id FK"])
    body += class_box(415, 450, 275, "STAFF", ["id PK; role", "department_id FK"])
    body += class_box(
        815,
        450,
        275,
        "REQUEST_EVENTS",
        ["id PK; request_id FK", "actor_id FK (nullable)", "action / note / UTC"],
    )
    body += class_box(80, 650, 280, "SESSIONS", ["hashed token; staff_id FK", "expiry; CSRF token"])
    body += label(
        32,
        850,
        "Selected physical relationships. Full ERD, optional fields and constraints: data-model.md.",
        16,
    )
    body += label(
        32,
        879,
        "Original AppSheet model had 7 entities; new events and sessions support history and staff access.",
        16,
    )
    return svg(
        "ERD / current operational data",
        "Thesis model: pp. 64-68 | Selected relationships of the 2026 schema",
        body,
        911,
    )


ARTIFACTS = [
    (
        "affinity",
        "research",
        "Affinity Diagram",
        "Thesis-derived",
        "p. 17 / Figure 2",
        affinity,
        "Grouped dispersed guest-service observations into four original clusters.",
        "Separated software opportunities from room facilities and staff-training problems.",
        "English headings preserve the original grouping. Summary text is editorial; no verbatim respondent quotes or frequency claims.",
        "docs/research-deep-dive.md",
    ),
    (
        "fishbone",
        "research",
        "Fishbone / root causes",
        "Thesis-derived",
        "pp. 19-20 / Figure 5",
        fishbone,
        "Organized delayed service around people, processes, technology and infrastructure.",
        "Kept task capture and allocation in the product scope while retaining non-software interventions.",
        "These are hypothesized causes in the thesis, not experimentally established causal effects.",
        "docs/research-deep-dive.md",
    ),
    (
        "journey",
        "research",
        "Customer Journey Map",
        "Thesis-derived",
        "p. 18 / Figure 3",
        journey,
        "Mapped six stages from booking through post-stay review, with goals, friction and experience.",
        "Focused the MVP on asking for service rather than expanding into reservations and billing.",
        "Persona thoughts are not reproduced as interview quotes. Emotions are qualitative interpretations.",
        "docs/customer-journey.md",
    ),
    (
        "blueprint",
        "research",
        "Service Blueprint",
        "Thesis-derived",
        "p. 19 / Figure 4",
        blueprint,
        "Connected visible guest interactions with backstage coordination and support work.",
        "Made departmental handoffs and responsibility explicit in the staff workflow.",
        "This is the broad original journey. The implemented request-only blueprint is documented separately.",
        "docs/service-blueprint.md",
    ),
    (
        "stakeholders",
        "business",
        "Stakeholder matrix",
        "Thesis-derived",
        "pp. 23-24 / Figure 6",
        stakeholders,
        "Compared hotel leadership, managers, staff, VIP guests and guests by influence and interest.",
        "Distinguished sponsorship, process approval, execution and guest feedback responsibilities.",
        "Qualitative placement, not a numerical score or an approved current hotel org chart.",
        "docs/brd.md",
    ),
    (
        "asis",
        "business",
        "AS-IS process",
        "Thesis-derived",
        "pp. 24-26 / Figure 7",
        asis,
        "Exposed unanswered contact, manual routing, abandonment and repeat service contacts.",
        "Translated handoff risk into durable capture and visible responsibility requirements.",
        "A condensed swimlane view preserves the central branches; the full source process is summarized in documentation.",
        "docs/processes.md",
    ),
    (
        "tobe",
        "business",
        "Original TO-BE concept",
        "Thesis-derived",
        "pp. 40-43, 64-73",
        tobe,
        "Connected Telegram intake, Sheets records and the AppSheet staff workflow.",
        "Provided the reconstruction brief for the lost staff application.",
        "Described functionality is distinguished from verified surviving bot behavior. New current safeguards are not backdated.",
        "docs/processes.md",
    ),
    (
        "furps",
        "business",
        "FURPS+ requirements",
        "Thesis framework + new controls",
        "pp. 27-31 / Figure 8",
        furps,
        "Separated functionality from usability, reliability, performance, supportability and constraints.",
        "Turned broad quality ambitions into verifiable controls and explicitly planned pilot requirements.",
        "The framework originates in the thesis; IDs, concrete safeguards and verification belong to the 2026 rebuild.",
        "docs/requirements.md",
    ),
    (
        "usecase",
        "system",
        "UML / Use Case",
        "Current 2026 model",
        "thesis pp. 35-37",
        usecase,
        "Shows guest, manager, agent and analyst capabilities within the current system boundary.",
        "Separates intake, operational permissions and analysis. Analysts remain read-only.",
        "The thesis designed authorization and notifications; hotel identity verification and proactive delivery are not implemented here.",
        "docs/diagrams/use-case.puml",
    ),
    (
        "class",
        "system",
        "UML / Class",
        "Current 2026 model",
        "thesis pp. 37-40",
        classes,
        "Shows selected logical entities and relationships for the reconstructed domain.",
        "Distinguishes request identity, responsibility and event history.",
        "Simplified selected relationships, not ORM code. New events/versioning differ from the thesis design; full source includes all links.",
        "docs/diagrams/class.puml",
    ),
    (
        "activity",
        "system",
        "UML / Activity",
        "Current 2026 model",
        "thesis pp. 40-42",
        activity,
        "Assigns intake, validation, transaction and fulfillment work to guest, system and staff.",
        "Makes failed input/save paths visible alongside the successful service flow.",
        "Current reliability and access controls extend the thesis process. Physical fulfillment still depends on staff procedures.",
        "docs/diagrams/activity.puml",
    ),
    (
        "sequence",
        "system",
        "UML / Sequence",
        "Current 2026 model",
        "thesis pp. 42-43",
        sequence,
        "Makes durable persistence precede guest confirmation and staff updates use expected versions.",
        "Prevents a success message for an unsaved request and makes a failure path explicit.",
        "The main flow is shown visually; the error branch is summarized and fully specified in the editable source.",
        "docs/diagrams/sequence.puml",
    ),
    (
        "state",
        "system",
        "UML / State",
        "Current 2026 model",
        "thesis pp. 43-45",
        states,
        "Defines new, acknowledged, in-progress, resolved, reopened and cancelled states.",
        "Separates auto-confirmation from human response and preserves first-resolution evidence.",
        "The thesis already designed detailed states and reopening; the surviving original bot only created Incompleted tasks. Enforcement is new.",
        "docs/diagrams/state.puml",
    ),
    (
        "component",
        "system",
        "UML / Component",
        "Current 2026 model",
        "thesis pp. 45-48",
        components,
        "Separates adapters, domain logic, persistence, metrics and optional export.",
        "Lets local request capture operate during a Google Sheets outage.",
        "The thesis architecture described several services; the rebuild uses a lean single-host application, not implemented microservices.",
        "docs/diagrams/component.puml",
    ),
    (
        "deployment",
        "system",
        "UML / Deployment",
        "Current 2026 model",
        "thesis pp. 48-53",
        deployment,
        "Shows guest/staff devices, Telegram, two Python processes and one shared SQLite file.",
        "Makes the demonstrator's physical hosting and scaling limits explicit.",
        "GitHub Pages serves a synthetic static preview; it does not host the bot or FastAPI backend.",
        "docs/diagrams/deployment.puml",
    ),
    (
        "erd",
        "system",
        "ERD / data model",
        "Current 2026 model",
        "thesis pp. 64-68",
        erd,
        "Connects rooms, guests, requests, categories, departments, staff and new operational records.",
        "Normalizes legacy string relationships and supports history, constraints and staff sessions.",
        "Selected schema relationships only. No original guest database was provided or migrated; room records do not model reservations.",
        "docs/data-model.md",
    ),
]


def build():
    cards = []
    previews = ROOT / "docs/case-study/assets"
    previews.mkdir(parents=True, exist_ok=True)
    for i, (key, group, title, status, source, render, shows, decision, boundary, doc) in enumerate(
        ARTIFACTS, 1
    ):
        # Unique SVG marker IDs avoid cross-diagram references in the same document.
        diagram = (
            render().replace('id="arrow"', f'id="arrow-{key}"').replace("url(#arrow)", f"url(#arrow-{key})")
        )
        if key in {"journey", "blueprint", "state"}:
            # Reuse the real atlas model, rather than drawing decorative pseudo-diagrams.
            standalone = diagram.replace(
                "<svg xmlns=", '<svg style="font-family:Arial,Helvetica,sans-serif" xmlns=', 1
            )
            (previews / f"{key}.svg").write_text(standalone + "\n", encoding="utf-8")
        cards.append(f'''<article id="{key}" class="artifact" data-group="{group}">
          <header><p class="eyebrow">{i:02} / {group.upper()}</p><h2>{escape(title)}</h2><p class="artifact-meta"><span>{escape(status)}</span><span>T1 / {escape(source)}</span></p></header>
          <button class="diagram-preview" data-diagram="{key}" aria-label="Enlarge {escape(title)} diagram">{diagram}<span class="diagram-hint">Inspect diagram ↗</span></button>
          <dl class="artifact-reading"><div><dt>What it shows</dt><dd>{escape(shows)}</dd></div><div><dt>Decision it supported</dt><dd>{escape(decision)}</dd></div><div><dt>Evidence &amp; scope</dt><dd>{escape(boundary)}</dd></div></dl>
          <a class="source-link" href="{REPO}{doc}">Read the full artifact / source ↗</a>
        </article>''')
    html = (
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Sixteen service-design and system-analysis diagrams from Albina Urubkina's hotel product case, with thesis sources, decisions and evidence limits.">
<title>Research &amp; Analysis Atlas · Albina Urubkina</title>
<link rel="stylesheet" href="../style.css"><link rel="stylesheet" href="atlas.css"><link rel="stylesheet" href="../design.css"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><script src="atlas.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to artifacts</a>
<header class="atlas-header"><a class="wordmark" href="../">AU<span>Albina Urubkina</span></a><nav aria-label="Atlas navigation"><a href="../">Back to case</a><a href="../../demo/">Try the product ↗</a></nav></header>
<main id="main" class="wrap"><section class="atlas-intro"><p class="eyebrow">THE RESEARCH &amp; ANALYSIS ATLAS</p><h1>The work behind<br>the workspace.</h1><p class="atlas-lead">Sixteen models. One thread from guest experience to operational requirements and a demonstrable product.</p><p>HSE University thesis, 2024 / English reconstructions and current-system views, 2026.</p>
<div class="atlas-counts"><div><strong>4</strong><span>research &amp; service-design views</span></div><div><strong>4</strong><span>business-analysis views</span></div><div><strong>8</strong><span>current system &amp; data views</span></div></div>
<div class="atlas-evidence"><p><strong>How to read this atlas.</strong> T1 means the 84-page 2024 thesis. Eight views reconstruct thesis artifacts or its requirements framework. Seven UML views and the ERD depict the current rebuild, informed by the original designs. Each model states its source, useful decision and boundary.</p><p>All visual labels are English. Diagrams are redrawn; original respondent records, persona portraits and sensitive configuration are excluded. No interview quotes or research distributions are fabricated.</p></div>
<div class="atlas-reading-links"><a href="https://github.com/alyalbina/hotel-guest-experience-platform/blob/main/docs/research-deep-dive.md">Research method &amp; synthesis ↗</a><a href="https://github.com/alyalbina/hotel-guest-experience-platform/blob/main/docs/research-traceability.md">Evidence → requirement → verification ↗</a></div></section>
<div class="atlas-toolbar"><div class="atlas-filters" role="group" aria-label="Filter artifact type"><button data-filter="all" aria-pressed="true">All 16</button><button data-filter="research" aria-pressed="false">Research 4</button><button data-filter="business" aria-pressed="false">Business analysis 4</button><button data-filter="system" aria-pressed="false">System &amp; data 8</button></div><p id="artifact-count" role="status" aria-live="polite">16 artifacts shown</p></div>
<div class="atlas-grid">"""
        + "\n".join(cards)
        + """</div>
<section class="atlas-next"><p class="eyebrow">FOLLOW THE THREAD</p><h2>Models become useful<br>when they change a decision.</h2><p>The traceability register connects thesis evidence with requirements, delivered behavior and the checks that support it. Technical checks establish prototype behavior; hotel outcomes still need a pilot.</p><a class="button primary" href="../#decisions">Explore product decisions ↗</a></section>
</main><footer class="site-footer wrap"><p>Albina Urubkina · HSE University, 2024 / portfolio reconstruction, 2026</p><nav><a href="../">Case study</a><a href="../../demo/">Live demo</a><a href="https://github.com/alyalbina/hotel-guest-experience-platform">GitHub</a></nav></footer>
<dialog id="diagram-dialog" aria-labelledby="diagram-title"><form method="dialog"><button class="dialog-close">Close <span aria-hidden="true">×</span></button></form><h2 id="diagram-title"></h2><p id="diagram-instruction">Scroll across the diagram to inspect labels. Press Escape to return.</p><div id="diagram-canvas" tabindex="0" role="region" aria-label="Enlarged diagram, scrollable"></div><p id="diagram-context"></p></dialog>
</body></html>"""
    )
    target = ROOT / "docs/case-study/artifacts/index.html"
    target.parent.mkdir(exist_ok=True)
    target.write_text(html + "\n", encoding="utf-8")
    print(f"Built {len(ARTIFACTS)} labelled views: {target.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
