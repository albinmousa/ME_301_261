# ME 301 — Machine Design I · Course Calendars (Term 261)

Subscribable calendars for **ME 301, First Semester 2026 (261)**, KFUPM Mechanical Engineering.
Instructor: Dr. Jafar Albinmousa.

**Student-facing page:** https://albinmousa.github.io/ME_301_261/

## Subscription links

| Calendar | Subscribe URL |
|---|---|
| Section F05 (Sun/Tue/Thu 12:00–12:50, 63-221) | `https://albinmousa.github.io/ME_301_261/ME301-F05.ics` |
| Section F07 (Sun/Tue/Thu 13:00–13:50, 63-132) | `https://albinmousa.github.io/ME_301_261/ME301-F07.ics` |
| Office hours (63-309) | `https://albinmousa.github.io/ME_301_261/ME301-OH.ics` |
| Both sections combined | `https://albinmousa.github.io/ME_301_261/ME301-F05-F07.ics` |

Swap `https://` for `webcal://` to open the subscribe dialog directly in Apple Calendar or Outlook.

If GitHub Pages is not enabled, the raw URLs work as a fallback (Google Calendar accepts them;
Apple Calendar is less reliable with them because they are served as `text/plain`):

```
https://raw.githubusercontent.com/albinmousa/ME_301_261/main/ME301-F05.ics
```

## What's in each calendar

- All 45 class sessions, 20 Aug – 10 Dec 2026, with section room and time
- Lecture titles keyed to Shigley's sections (e.g. `C6L2_6.7: The Endurance Limit`)
- The five quizzes, each naming its chapter
- Homework and project assign/due notes in the event description
- The two evening exams (19:00–21:00, location TBD)
- The four no-class days as all-day events (National Day, Midterm Break ×2, Autumn Break)
- A 15-minute reminder on every timed event

Current as of the **21 September 2026 revision** of the course plan.

## Updating the calendars

Do not hand-edit the `.ics` files. Everything is generated from one table:

1. Edit the `SESSIONS` list in [`tools/generate_calendars.py`](tools/generate_calendars.py) — one row
   per class day: `("YYYYMMDD", "CodeAndTitle", "HW/project note or empty")`.
2. Run it:
   ```bash
   python3 tools/generate_calendars.py
   ```
   This rewrites all four `.ics` files in place, keeping event counts, UIDs and formatting consistent.
3. Commit and push. Subscribers pick the change up on their calendar app's next refresh.

Holidays, evening exams, section times and rooms live in the `HOLIDAYS`, `EXAMS` and `SECTIONS`
constants at the top of the same script.

### Note on refresh timing

Calendar clients refresh external subscriptions on their own schedule — Google and Outlook
typically somewhere between a few hours and a day; Apple Calendar is user-configurable. Updates
do propagate, but not instantly, so announce anything urgent in class or on Blackboard as well.

### Note on UIDs

Event UIDs are positional (`evt-001`, `evt-002`, …). If a revision changes the *order* of events,
the same UID can end up on a different date. Fresh subscribers are unaffected. Anyone who
*imported* (rather than subscribed to) an older copy may see duplicates and should delete the old
events first — another reason to point students at subscription rather than download.

## Repository layout

```
index.html                     Student-facing subscribe page (GitHub Pages)
ME301-F05.ics                  Section F05 — 51 events
ME301-F07.ics                  Section F07 — 51 events
ME301-F05-F07.ics              Both sections combined — 96 events
ME301-OH.ics                   Office hours — 76 events
tools/generate_calendars.py    Generator — single source of truth for all four files
```
