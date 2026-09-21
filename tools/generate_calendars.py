#!/usr/bin/env python3
"""
Generate all ME 301 (term 261) subscribable calendars.

Single source of truth for ME301-F05.ics, ME301-F07.ics, ME301-F05-F07.ics and ME301-OH.ics.
Edit the tables below, then run:  python3 tools/generate_calendars.py

Reflects the 7 September 2026 revision of the course plan.
"""

import datetime
import os

# Bump this when you publish a revision (UTC, format YYYYMMDDTHHMMSSZ).
DTSTAMP = "20260921T120000Z"

# ---------------------------------------------------------------------------
# Class sessions: (date, "CodeAndTitle", "HW/project note" or "")
# One row per class day. Holidays are listed separately below.
# ---------------------------------------------------------------------------
SESSIONS = [
    ("20260820", "C0L1_3.1: Equilibrium and Free-Body Diagrams", ""),
    ("20260823", "C0L2_3.1: Equilibrium and Free-Body Diagrams (continued)", ""),
    ("20260825", "C3L1_3.2: Shear Force and Bending Moment Diagrams", "HW1 Assigned"),
    ("20260827", "C3L2_3.10: Normal Stresses for Beams in Bending", ""),
    ("20260830", "C3L3_3.11: Shear Stresses for Beams in Bending", ""),
    ("20260901", "C3L4_3.12: Torsion", ""),
    ("20260903", "C3L5_3.6: Mohr's Circle and Stress Transformation", ""),
    ("20260906", "C3L6_3.6: Mohr's Circle and Stress Transformation (continued)", ""),
    ("20260908", "C3L7_3.14: Stresses in Pressurized Cylinders + 3.16: Press and Shrink Fits (Reading)", ""),
    ("20260910", "C3L8_Review: Chapter 3", ""),
    ("20260913", "C5L1_5.4/5.5: Maximum Shear-Stress and Distortion-Energy Theories", "HW1 Due | HW2 Assigned"),
    ("20260915", "Quiz_Quiz 1 (Chapter 3)", ""),
    ("20260917", "C5L2_5.6/5.8: Coulomb-Mohr and Maximum Normal-Stress Theories", ""),
    ("20260920", "C5L3_5.9: Modification of the Mohr Theory for Brittle Materials", ""),
    ("20260922", "C5L4_Review: Chapter 5", ""),
    ("20260927", "C4L1_4.5: Beam Deflections by Superposition", "HW3 Assigned"),
    ("20260929", "C4L2_4.8: Castigliano's Theorem (Reading) + 4.10: Statically Indeterminate Problems", "HW2 Due"),
    ("20261001", "Quiz_Quiz 2 (Chapter 5)", "Exam 1 (Evening)"),
    ("20261004", "C4L3_4.12/4.13: Long and Intermediate-Length Columns", ""),
    ("20261006", "C4L4_Review: Chapter 4", ""),
    ("20261008", "C6L1_6.4: The Stress-Life Method", ""),
    ("20261011", "C6L2_6.7: The Endurance Limit", "HW3 Due"),
    ("20261013", "C6L3_6.8: Fatigue Strength", "HW4 Assigned"),
    ("20261015", "C6L4_6.9: Endurance Limit Modifying Factors", ""),
    ("20261018", "Quiz_Quiz 3 (Chapter 4)", ""),
    ("20261025", "C6L5_6.10: Stress Concentration and Notch Sensitivity", ""),
    ("20261027", "C6L6_6.12: Fatigue Failure Criteria for Fluctuating Stress", ""),
    ("20261029", "C6L7_6.14: Combinations of Loading Modes", ""),
    ("20261101", "C6L8_Review: Chapter 6", "HW4 Due"),
    ("20261103", "Quiz_Quiz 4 (Chapter 6)", ""),
    ("20261105", "C7L1_7.4: Shaft Design for Stress", "Term Project Assigned | Exam 2 (Evening)"),
    ("20261108", "C7L2_7.5: Deflection Considerations", ""),
    ("20261110", "C7L3_Shaft Design by Finite Element Analysis", ""),
    ("20261112", "C8L1_8.2: The Mechanics of Power Screws", "HW5 Assigned"),
    ("20261115", "C8L2_8.3: Threaded Fasteners", ""),
    ("20261117", "C8L3_8.5: Joint Member Stiffness", ""),
    ("20261119", "C8L4_8.7: Tension Joints - The External Load", ""),
    ("20261124", "C8L5_8.9: Statically Loaded Tension Joint with Preload", ""),
    ("20261126", "C8L6_8.11: Fatigue Loading of Tension Joints", ""),
    ("20261129", "C8L7_8.12: Bolted and Riveted Joints Loaded in Shear", ""),
    ("20261201", "C8L8_Review: Chapter 8", "Term Project Due"),
    ("20261203", "Quiz_Quiz 5 (Chapter 8)", "HW5 Due"),
    ("20261206", "C9L1_9.3: Stresses in Weld Joints in Torsion", ""),
    ("20261208", "C9L2_9.4: Stresses in Weld Joints in Bending", ""),
    ("20261210", "C9L3_Review: Chapter 9", ""),
]

HOLIDAYS = [
    ("20260924", "20260925", "National Day Holiday"),
    ("20261020", "20261021", "Midterm Break"),
    ("20261022", "20261023", "Midterm Break"),
    ("20261122", "20261123", "Autumn Break"),
]

EXAMS = [("20261001", "Exam 1"), ("20261105", "Exam 2")]

SECTIONS = {
    "F05": {"start": "120000", "end": "125000", "room": "63-221", "uid": "me301f05.local"},
    "F07": {"start": "130000", "end": "135000", "room": "63-132", "uid": "me301f07.local"},
}

# ---------------------------------------------------------------------------
# Office hours: weekday -> (start, end).  Monday=0 ... Sunday=6
# ---------------------------------------------------------------------------
OH_TERM = ("20260820", "20261210")
OH_ROOM = "63-309"
OH_SCHEDULE = {
    6: ("140000", "150000"),  # Sunday    2:00-3:00 PM
    0: ("110000", "120000"),  # Monday   11:00-12:00
    1: ("140000", "150000"),  # Tuesday   2:00-3:00 PM
    2: ("110000", "120000"),  # Wednesday 11:00-12:00
    3: ("110000", "120000"),  # Thursday  11:00-12:00
}
# No office hours on these dates (holiday / break days).
OH_EXCLUDED = {"20260924", "20261020", "20261021", "20261022", "20261122"}

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def event(uid, summary, dtstart, dtend, location=None, description=None,
          alarm=True, all_day=False):
    L = ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{DTSTAMP}", f"SUMMARY:{summary}"]
    if all_day:
        L += [f"DTSTART;VALUE=DATE:{dtstart}", f"DTEND;VALUE=DATE:{dtend}"]
    else:
        L += [f"DTSTART:{dtstart}", f"DTEND:{dtend}"]
    if location:
        L.append(f"LOCATION:{location}")
    if description:
        L.append(f"DESCRIPTION:{description}")
    if alarm:
        L += ["BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:Reminder",
              "TRIGGER:-PT15M", "END:VALARM"]
    L.append("END:VEVENT")
    return L


def wrap(calname, body):
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Excel Lecture Schedule//EN",
           "CALSCALE:GREGORIAN", f"X-WR-CALNAME:{calname}"] + body + ["END:VCALENDAR"]
    return "\r\n".join(out) + "\r\n"


def build_course(calname, uid_domain, sections, exam_prefix):
    items = []
    for d, dend, name in HOLIDAYS:
        items.append((d + "000000", ("holiday", d, dend, name)))
    for d, label in EXAMS:
        items.append((d + "190000", ("exam", d, label)))
    for sec in sections:
        for d, title, desc in SESSIONS:
            items.append((d + SECTIONS[sec]["start"] + sec, ("lecture", d, title, desc, sec)))
    items.sort(key=lambda x: x[0])

    body, n = [], 0
    for _, spec in items:
        n += 1
        uid = f"evt-{n:03d}@{uid_domain}"
        if spec[0] == "holiday":
            _, d, dend, name = spec
            body += event(uid, f"No Class - {name}", d, dend,
                          description=f"{name} (No class)", alarm=False, all_day=True)
        elif spec[0] == "exam":
            _, d, label = spec
            body += event(uid, f"{exam_prefix} {label}", f"{d}T190000", f"{d}T210000",
                          description="Evening exam - location TBD")
        else:
            _, d, title, desc, sec = spec
            cfg = SECTIONS[sec]
            body += event(uid, f"ME 301-{sec} | {title}",
                          f"{d}T{cfg['start']}", f"{d}T{cfg['end']}",
                          location=cfg["room"], description=desc or None)
    return wrap(calname, body)


def build_office_hours():
    start = datetime.datetime.strptime(OH_TERM[0], "%Y%m%d").date()
    end = datetime.datetime.strptime(OH_TERM[1], "%Y%m%d").date()
    body, n, d = [], 0, start
    while d <= end:
        key = d.strftime("%Y%m%d")
        if d.weekday() in OH_SCHEDULE and key not in OH_EXCLUDED:
            s, e = OH_SCHEDULE[d.weekday()]
            n += 1
            body += event(f"evt-{n:03d}@me301oh.local",
                          "ME 301 - Office Hours (Dr. Albinmousa)",
                          f"{key}T{s}", f"{key}T{e}", location=OH_ROOM)
        d += datetime.timedelta(days=1)
    return wrap("ME 301 - Office Hours (Dr. Albinmousa)", body)


def write(name, text):
    path = os.path.join(REPO, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(text)
    print(f"  {name:22s} {text.count('BEGIN:VEVENT'):3d} events")


if __name__ == "__main__":
    print("Writing calendars to", REPO)
    write("ME301-F05.ics", build_course("ME 301-F05", "me301f05.local", ["F05"], "ME 301-F05"))
    write("ME301-F07.ics", build_course("ME 301-F07", "me301f07.local", ["F07"], "ME 301-F07"))
    write("ME301-F05-F07.ics",
          build_course("ME 301 - F05 & F07 (Combined)", "me301combined.local",
                       ["F05", "F07"], "ME 301"))
    write("ME301-OH.ics", build_office_hours())
    print("Done. Commit and push to publish.")
