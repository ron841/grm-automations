#!/usr/bin/env python3
"""
grm_daily_calls.py — GRM Call-List Builder (v3.1 — calls live on the Company)

Calls do not live in the Task system. A company is flagged for a calling day by
a DATE property, ``grm_next_call_date``. A saved Companies view ("Today's Calls")
filtered to grm_next_call_date = TODAY is the call list Ron dials straight from.

Ron's daily loop (in the company preview):
  • logs a CALL  (incl. "left a voicemail")  → that company is "called"
  • writes a NOTE starting MEETING/APPT       → an appointment was booked
  • pastes an email into a NOTE               → an email follow-up is owed

The automation turns that into:
  • CALLED      → grm_last_call_date stamped, New→Attempted, taken off today's list
  • APPOINTMENT → a Deal ("Meeting Set", right pipeline) created, removed from pool
  • UNREACHED   → carried forward to the next calling day (never lost)
  • re-dials    → a called-but-unreached company comes back automatically after a
                  cooldown (Connected 2d, Attempted 3d, Not Now 14d)
  • email       → a next-day EMAIL task tied to BOTH the contact and the company

────────────────────────────────────────────────────────────────────────────
TWO RUN MODES
  (default / nightly)   build the NEXT calling day:
      A) callbacks    — stamp parsed callback dates from today's notes
      M) meetings     — MEETING/APPT notes → create Deals, drop from pool
      B) worked       — stamp grm_last_call_date + promote from REAL calls/notes,
                        and CLEAR today's reached companies off the list
      C) build        — clear→rebuild the target day to exactly 45 (carry-forward
                        unreached first, then due re-dials, then a fresh-New tier
                        blend A=13 B+=14 B=4 Untiered=14)
      D) email        — today's emailed notes → next-day EMAIL tasks
      E) spot-check   — confirm the EMAIL tasks carry their associations

  --intraday            keep TODAY honest during business hours (a second
                        workflow runs this hourly):
      • worked-detection for today (advance status same-day; does NOT clear the
        list so the day's 45 stay visible while Ron works)
      • meetings for today (drop booked companies same-day)
      • SELF-HEAL: if today's list is unexpectedly empty (a missed/failed
        nightly run), build it on the spot so the morning is never empty

Eligibility is computed from REAL CALL associations (not only the lagging stamp),
so a company dialed yesterday is never re-served even if a stamp/promotion lagged.

The HubSpot token comes from the HUBSPOT_TOKEN environment variable (a GitHub
Actions secret) — never hardcoded.

Usage:
  HUBSPOT_TOKEN=... python3 scripts/grm_daily_calls.py             # nightly, target = tomorrow
  HUBSPOT_TOKEN=... python3 scripts/grm_daily_calls.py --dry-run   # nightly, no writes
  HUBSPOT_TOKEN=... python3 scripts/grm_daily_calls.py --intraday  # maintain today + self-heal
"""

import os
import re
import sys
import time
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

import requests

# ─── CONFIG ──────────────────────────────────────────────────────────────────
TOKEN = os.environ.get("HUBSPOT_TOKEN")
if not TOKEN:
    sys.exit("FATAL: HUBSPOT_TOKEN environment variable is not set.")

TZ           = ZoneInfo("America/New_York")   # all "calendar day" logic is Eastern
UTC          = ZoneInfo("UTC")
MAX_CALLS    = 45                              # companies flagged per calling day
RON_OWNER_ID = "90284376"                      # ron@getrootedmedia.com
OUR_DOMAIN   = "getrootedmedia.com"            # ignore our own addresses on email capture

# HubSpot-defined association type IDs (v4 associations API)
ASSOC_TASK_TO_COMPANY    = 192
ASSOC_TASK_TO_CONTACT    = 204
ASSOC_CONTACT_TO_COMPANY = 279
ASSOC_DEAL_TO_COMPANY    = 341   # HubSpot-defined deal→company
ASSOC_DEAL_TO_CONTACT    = 3     # HubSpot-defined deal→contact

# Daily tier blend — the systematic mix the fresh-New top-up is built from.
# (sums to MAX_CALLS = 45)
TIER_TARGETS = {"A": 13, "B+": 14, "B": 4, "Untiered": 14}
TIER_ORDER   = ["A", "B+", "B", "Untiered"]

# Re-dial cooldown by status, in days, measured against the last REAL call.
# New has no cooldown UNLESS it was actually dialed within the Attempted window
# (a New that's been called is really an un-promoted Attempted — see is_eligible).
REDIAL_DAYS = {"Connected": 2, "Attempted": 3, "Not Now": 14}
NEW_DIALED_COOLDOWN = REDIAL_DAYS["Attempted"]   # 3d guard so New-dialed-yesterday isn't re-served
# Lowest number = highest priority when ordering re-dials (most overdue first uses last_call).
STATUS_RANK = {"New": 0, "Connected": 1, "Attempted": 2, "Not Now": 3}

# Statuses that are NEVER eligible (removed from the calling pool entirely).
EXCLUDED_STATUSES = {"Not a Fit"}
# Statuses that re-dial (everything callable that isn't New / excluded).
REDIAL_STATUSES = ["Connected", "Attempted", "Not Now"]

# Publication → deal pipeline label (resolved to live IDs at runtime).
PIPELINE_LABELS = {"CT": "Closing Table", "FP": "Front Porch"}
MEETING_STAGE_LABEL = "Meeting Set"

DRY_RUN  = "--dry-run" in sys.argv
INTRADAY = "--intraday" in sys.argv

# How far back to look at real CALL engagements (covers the longest cooldown).
CALL_LOOKBACK_DAYS = max(REDIAL_DAYS.values()) + 1   # 15

# ─── API HELPER ──────────────────────────────────────────────────────────────
session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type":  "application/json",
})


def api(method, path, body=None, params=None):
    """Call the HubSpot API. Returns (json_dict, status_code).
    Retries once automatically if HubSpot rate-limits us (HTTP 429)."""
    url = "https://api.hubapi.com" + path
    for attempt in (1, 2):
        resp = session.request(method, url, json=body, params=params, timeout=30)
        if resp.status_code == 429 and attempt == 1:
            time.sleep(2)  # back off, then retry once
            continue
        try:
            data = resp.json() if resp.text else {}
        except ValueError:
            data = {"raw": resp.text}
        return data, resp.status_code


def search_all(object_type, filters, properties, sorts=None):
    """Run a CRM search and follow pagination until every page is collected."""
    results, after = [], None
    while True:
        body = {
            "filterGroups": [{"filters": filters}],
            "properties": properties,
            "limit": 200,
        }
        if sorts:
            body["sorts"] = sorts
        if after:
            body["after"] = after
        resp, status = api("POST", f"/crm/v3/objects/{object_type}/search", body)
        if status != 200:
            print(f"  [WARN] {object_type} search failed: {status} {resp}")
            break
        results.extend(resp.get("results", []))
        after = resp.get("paging", {}).get("next", {}).get("after")
        if not after:
            break
        time.sleep(0.25)  # stay under the search-API rate limit
    return results


def batch_associations(from_type, to_type, ids):
    """Return {from_id: [to_id, ...]} via the v4 batch-read endpoint.
    Far cheaper than one GET per object when mapping many engagements at once."""
    out, ids = {}, [str(i) for i in ids]
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        resp, status = api("POST",
                           f"/crm/v4/associations/{from_type}/{to_type}/batch/read",
                           {"inputs": [{"id": x} for x in chunk]})
        if status != 200:
            print(f"  [WARN] batch assoc {from_type}->{to_type} failed: {status} {resp}")
            continue
        for row in resp.get("results", []):
            frm = str(row.get("from", {}).get("id"))
            out.setdefault(frm, []).extend(str(t.get("toObjectId")) for t in row.get("to", []))
    return out


# ─── DATE HELPERS ────────────────────────────────────────────────────────────
def now_et():
    return datetime.now(tz=TZ)


def today_et():
    return now_et().date()


def tomorrow_et():
    return today_et() + timedelta(days=1)


def nine_am_ms(d):
    """9:00 AM Eastern on date d, as epoch milliseconds (HubSpot task due time)."""
    return int(datetime(d.year, d.month, d.day, 9, 0, 0, tzinfo=TZ).timestamp() * 1000)


def et_day_start_ms(d):
    """Midnight Eastern on date d, epoch ms. For 'created today' engagement filters."""
    return int(datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=TZ).timestamp() * 1000)


def utc_midnight_ms(d):
    """Midnight UTC on date d, epoch ms. HubSpot stores DATE-type properties
    (grm_next_call_date, grm_last_call_date) as midnight UTC — filter against this."""
    return int(datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=UTC).timestamp() * 1000)


def iso_date(d):
    """'YYYY-MM-DD' — the form HubSpot accepts when WRITING a date property."""
    return d.strftime("%Y-%m-%d")


def parse_date_property(raw):
    """Stored date-property value → date object, or None. HubSpot returns date
    properties as a midnight-UTC epoch-ms string; tolerate ISO too."""
    if not raw:
        return None
    try:
        return datetime.fromtimestamp(int(raw) / 1000, tz=UTC).date()
    except (ValueError, TypeError):
        try:
            return date.fromisoformat(str(raw)[:10])
        except ValueError:
            return None


def ms_to_et_date(ms):
    """Epoch-ms or ISO-8601 (UTC instant) → the Eastern calendar date it falls on.
    The v3 search API returns datetime properties (e.g. a call's hs_timestamp) as
    ISO strings, not epoch-ms — tolerate both or every real call goes invisible."""
    try:
        return datetime.fromtimestamp(int(ms) / 1000, tz=UTC).astimezone(TZ).date()
    except (ValueError, TypeError):
        try:
            return (datetime.fromisoformat(str(ms).replace("Z", "+00:00"))
                    .astimezone(TZ).date())
        except (ValueError, TypeError):
            return None


# ─── CALLBACK / MEETING PARSING ──────────────────────────────────────────────
WEEKDAY_LOOKUP = {
    "monday": 0, "mon": 0,
    "tuesday": 1, "tue": 1, "tues": 1,
    "wednesday": 2, "wed": 2,
    "thursday": 3, "thu": 3, "thur": 3, "thurs": 3,
    "friday": 4, "fri": 4,
    "saturday": 5, "sat": 5,
    "sunday": 6, "sun": 6,
}
MONTH_NAMES = ["january", "february", "march", "april", "may", "june", "july",
               "august", "september", "october", "november", "december"]

# Phrases that introduce a callback; each captures the <when> that follows.
CALLBACK_TRIGGERS = [
    re.compile(r"callback:\s*(.+)", re.IGNORECASE),
    re.compile(r"\bcall back\s+(.+)", re.IGNORECASE),
    re.compile(r"\bcallback\s+(.+)", re.IGNORECASE),
    re.compile(r"\bcb\s+(.+)", re.IGNORECASE),
    re.compile(r"^\s*call\s+(.+)", re.IGNORECASE),
]

# A meeting marker is a LINE that STARTS with MEETING / APPT / APPOINTMENT.
# Everything after the marker is an optional <when> (close date).
MEETING_MARKER = re.compile(r"^\s*(?:meeting|appt|appointment)\b[:.\-\s]*(.*)$", re.IGNORECASE)
# Loose detector — used only to flag notes that LOOK like a meeting but lack a marker.
MEETING_HINT = re.compile(r"\b(meeting|appt|appointment|booked|scheduled|demo|sit[- ]?down)\b",
                          re.IGNORECASE)


def _next_weekday(ref, target_weekday, force_next_week=False):
    days_ahead = (target_weekday - ref.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7  # 'wednesday' said on a Wednesday means the coming one
    if force_next_week:
        days_ahead += 7
    return ref + timedelta(days=days_ahead)


def parse_when(text, ref):
    """Resolve a <when> expression to a calendar date relative to ref, or None.
    Recognized: tomorrow | in N days | N days | <weekday> | next <weekday> |
    M/D[/Y] | YYYY-MM-DD | 'Month D'."""
    s = (text or "").strip().lower()
    if not s:
        return None

    if re.match(r"tomorrow\b", s):
        return ref + timedelta(days=1)

    m = re.search(r"\bin\s+(\d{1,3})\s+days?\b", s) or re.match(r"(\d{1,3})\s+days?\b", s)
    if m:
        return ref + timedelta(days=int(m.group(1)))

    m = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None

    m = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", s)
    if m:
        month, day, year = int(m.group(1)), int(m.group(2)), m.group(3)
        if year:
            year = int(year)
            if year < 100:
                year += 2000
        else:
            year = ref.year
        try:
            d = date(year, month, day)
        except ValueError:
            return None
        if not m.group(3) and d < ref:        # no-year date already past → next year
            try:
                d = date(year + 1, month, day)
            except ValueError:
                return None
        return d

    for i, month in enumerate(MONTH_NAMES, start=1):
        m = re.search(rf"\b(?:{month}|{month[:3]})\.?\s+(\d{{1,2}})\b", s)
        if m:
            day = int(m.group(1))
            try:
                d = date(ref.year, i, day)
            except ValueError:
                return None
            if d < ref:
                try:
                    d = date(ref.year + 1, i, day)
                except ValueError:
                    return None
            return d

    m = re.search(r"\bnext\s+([a-z]+)\b", s)
    if m and m.group(1) in WEEKDAY_LOOKUP:
        return _next_weekday(ref, WEEKDAY_LOOKUP[m.group(1)], force_next_week=True)

    for name, wd in WEEKDAY_LOOKUP.items():
        if re.search(rf"\b{name}\b", s):
            return _next_weekday(ref, wd)

    return None


def parse_callback_date(note_body, ref):
    """Find callback intent in a note and resolve it to a date, or None.
    Only returns a date when a recognized time expression is present."""
    for line in (note_body or "").splitlines():
        for trigger in CALLBACK_TRIGGERS:
            m = trigger.search(line.strip())
            if m:
                d = parse_when(m.group(1), ref)
                if d:
                    return d
    return None


def parse_meeting(note_body, ref):
    """If a line starts with a meeting marker, return (True, close_date_or_None).
    The close date is parsed from the rest of the marker line if present.
    Returns (False, None) when no marker line exists."""
    for line in (note_body or "").splitlines():
        m = MEETING_MARKER.match(line)
        if m:
            return True, parse_when(m.group(1), ref)
    return False, None


def looks_like_meeting(note_body):
    return bool(MEETING_HINT.search(note_body or ""))


# ─── ASSOCIATION / READ HELPERS ──────────────────────────────────────────────
def companies_for_note(note_id):
    assoc, status = api("GET", f"/crm/v4/objects/notes/{note_id}/associations/companies")
    return {str(a["toObjectId"]) for a in assoc.get("results", [])} if status == 200 else set()


def contacts_for_note(note_id):
    assoc, status = api("GET", f"/crm/v4/objects/notes/{note_id}/associations/contacts")
    return [str(a["toObjectId"]) for a in assoc.get("results", [])] if status == 200 else []


def company_props(cid, names):
    co, status = api("GET", f"/crm/v3/objects/companies/{cid}",
                     params={"properties": ",".join(names)})
    return co.get("properties", {}) if status == 200 else {}


def company_name(cid):
    return company_props(cid, ["name"]).get("name") or f"Company {cid}"


def notes_created_on(day, props=None):
    return search_all(
        "notes",
        [{"propertyName": "hs_createdate", "operator": "GTE", "value": str(et_day_start_ms(day))}],
        props or ["hs_note_body"],
    )


# ─── COMPANY WRITES ──────────────────────────────────────────────────────────
def set_company_props(company_id, props):
    """PATCH one company's properties. No-op (returns True) under --dry-run."""
    if DRY_RUN:
        return True
    _, status = api("PATCH", f"/crm/v3/objects/companies/{company_id}", {"properties": props})
    return status in (200, 201)


def stamp_next_call_date(company_id, d):
    """Set grm_next_call_date to date d, or clear it when d is None."""
    return set_company_props(company_id, {"grm_next_call_date": iso_date(d) if d else ""})


def companies_stamped_for(d):
    """Companies whose grm_next_call_date equals calendar date d."""
    rows = search_all(
        "companies",
        [{"propertyName": "grm_next_call_date", "operator": "EQ", "value": str(utc_midnight_ms(d))}],
        ["name", "grm_lead_status", "grm_next_call_date"],
    )
    return [{"id": str(r["id"]),
             "name": r.get("properties", {}).get("name") or f"Company {r['id']}",
             "grm_lead_status": r.get("properties", {}).get("grm_lead_status")}
            for r in rows]


# ─── REAL-CALL MAP (the activity source of truth) ─────────────────────────────
def recent_calls_by_company(since_date):
    """{company_id: latest Eastern call date} from real CALL engagements logged on
    or after since_date. This — not the stamp — drives worked-detection and the
    re-dial cooldown, so the system is robust to a lagging grm_last_call_date."""
    calls = search_all(
        "calls",
        [{"propertyName": "hs_timestamp", "operator": "GTE", "value": str(et_day_start_ms(since_date))}],
        ["hs_timestamp"],
    )
    if not calls:
        return {}
    call_date = {c["id"]: ms_to_et_date(c.get("properties", {}).get("hs_timestamp")) for c in calls}
    by_company = {}
    assoc = batch_associations("calls", "companies", [c["id"] for c in calls])
    for call_id, cids in assoc.items():
        d = call_date.get(call_id)
        if not d:
            continue
        for cid in cids:
            if cid not in by_company or d > by_company[cid]:
                by_company[cid] = d
    return by_company


# ─── DEALS ───────────────────────────────────────────────────────────────────
def open_deal_company_ids():
    """Company IDs with an OPEN deal (a booked meeting still in play). These leave
    the calling pool. Closed-won/closed-lost deals do not exclude a company."""
    deals = search_all("deals",
                       [{"propertyName": "hs_object_id", "operator": "HAS_PROPERTY"}],
                       ["dealname", "hs_is_closed"])
    open_ids = [d["id"] for d in deals
                if str(d.get("properties", {}).get("hs_is_closed")).lower() != "true"]
    if not open_ids:
        return set()
    company_ids = set()
    assoc = batch_associations("deals", "companies", open_ids)
    for cids in assoc.values():
        company_ids.update(cids)
    return company_ids


def resolve_meeting_stages():
    """Resolve live pipeline + 'Meeting Set' stage IDs from the API.
    Returns {"CT": (pipeline_id, stage_id), "FP": (pipeline_id, stage_id)}."""
    resp, status = api("GET", "/crm/v3/pipelines/deals")
    out = {}
    if status != 200:
        print(f"  [WARN] could not read deal pipelines: {status} {resp}")
        return out
    for pl in resp.get("results", []):
        label = (pl.get("label") or "")
        key = next((k for k, frag in PIPELINE_LABELS.items() if frag.lower() in label.lower()), None)
        if not key:
            continue
        stage_id = next((s["id"] for s in pl.get("stages", [])
                         if (s.get("label") or "").strip().lower() == MEETING_STAGE_LABEL.lower()), None)
        if stage_id:
            out[key] = (pl["id"], stage_id)
    return out


def pipeline_for_publication(pub, stages):
    """Map grm_publication → (pipeline_id, stage_id). CT→CT, FP→FP,
    'CT + FP' (and anything mentioning CT) → CT. Default CT."""
    pub = (pub or "").upper()
    if "CT" in pub and "CT" in stages:
        return stages["CT"]
    if "FP" in pub and "FP" in stages:
        return stages["FP"]
    return stages.get("CT") or stages.get("FP")


def create_deal(company_id, cname, contact_id, close_date, stages):
    """Create a Meeting-Set deal WITH its company (and contact) association in ONE
    call, in the pipeline chosen by the company's grm_publication."""
    pub = company_props(company_id, ["grm_publication"]).get("grm_publication")
    resolved = pipeline_for_publication(pub, stages)
    if not resolved:
        print(f"  [ERROR] no pipeline/stage resolved for {cname} (pub={pub}) — deal skipped")
        return None
    pipeline_id, stage_id = resolved
    props = {"dealname": f"{cname} — Meeting", "pipeline": pipeline_id, "dealstage": stage_id}
    if close_date:
        props["closedate"] = str(utc_midnight_ms(close_date))
    associations = [{
        "to": {"id": str(company_id)},
        "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": ASSOC_DEAL_TO_COMPANY}],
    }]
    if contact_id:
        associations.append({
            "to": {"id": str(contact_id)},
            "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": ASSOC_DEAL_TO_CONTACT}],
        })
    if DRY_RUN:
        return "DRY-RUN"
    resp, status = api("POST", "/crm/v3/objects/deals", {"properties": props, "associations": associations})
    if status not in (200, 201):
        print(f"  [ERROR] deal create failed ({cname}): {status} {resp}")
        return None
    return resp.get("id")


# ─── PASS A: CALLBACKS ───────────────────────────────────────────────────────
def callback_pass(ref):
    """Stamp grm_next_call_date from callback intent in today's notes."""
    print("\nPASS A — CALLBACKS (notes created today)")
    print("─" * 60)
    notes = notes_created_on(ref)
    print(f"  Notes created today: {len(notes)}")
    stamped = 0
    for note in notes:
        body = note.get("properties", {}).get("hs_note_body", "") or ""
        d = parse_callback_date(body, ref)
        if not d or d < ref:
            continue
        for cid in companies_for_note(note["id"]):
            if stamp_next_call_date(cid, d):
                stamped += 1
                print(f"    [CALLBACK] {company_name(cid)} → {iso_date(d)}")
    print(f"  Callbacks stamped: {stamped}")
    return stamped


# ─── PASS M: MEETINGS → DEALS ────────────────────────────────────────────────
def meeting_pass(ref, deal_ids, stages):
    """MEETING/APPT notes → create a Deal, drop the company from the calling pool.
    Marker required. Notes that look like a meeting but lack a marker are logged
    for manual review (never auto-acted). Mutates deal_ids in place."""
    print("\nPASS M — MEETINGS (notes created today)")
    print("─" * 60)
    notes = notes_created_on(ref)
    created, review = 0, []
    for note in notes:
        body = note.get("properties", {}).get("hs_note_body", "") or ""
        marked, close_date = parse_meeting(body, ref)
        if not marked:
            if looks_like_meeting(body):
                review.append(note["id"])
            continue
        contacts = contacts_for_note(note["id"])
        contact_id = contacts[0] if contacts else None
        for cid in companies_for_note(note["id"]):
            if cid in deal_ids:                       # already has an open deal — dedupe
                continue
            cname = company_name(cid)
            did = create_deal(cid, cname, contact_id, close_date, stages)
            if did:
                deal_ids.add(cid)
                stamp_next_call_date(cid, None)       # booked → off the calling list
                created += 1
                when = f" (close {iso_date(close_date)})" if close_date else ""
                print(f"    [MEETING] {cname} → deal {did}{when}")
            else:
                print(f"    [MEETING] {cname} — deal NOT created (see error above)")
    for nid in review:
        print(f"    [REVIEW] note {nid} looks like a meeting but has no MEETING/APPT marker")
    print(f"  Deals created: {created} | flagged for review: {len(review)}")
    return created, review


# ─── PASS B: WORKED DETECTION ────────────────────────────────────────────────
def companies_noted_on(day):
    notes = notes_created_on(day, props=["hs_object_id"])
    ids = set()
    if notes:
        for cids in batch_associations("notes", "companies", [n["id"] for n in notes]).values():
            ids.update(cids)
    return ids


def worked_detection_pass(day, call_map, clear_reached):
    """For every company with REAL work logged today (a CALL — incl. off-list — or
    a note): stamp grm_last_call_date and promote New→Attempted. Stamping/queuing
    never changes status; only real work does. When clear_reached (nightly), also
    clear that company off TODAY's list — but never a future-dated callback."""
    print(f"\nPASS B — WORKED DETECTION ({iso_date(day)})")
    print("─" * 60)
    called_today = {cid for cid, d in call_map.items() if d == day}
    worked = called_today | companies_noted_on(day)
    print(f"  Worked today: {len(worked)} (called {len(called_today)} + noted)")

    promoted = cleared = 0
    for cid in worked:
        p = company_props(cid, ["grm_lead_status", "grm_next_call_date", "name"])
        status = p.get("grm_lead_status") or "New"
        if status in EXCLUDED_STATUSES:
            continue
        last = call_map.get(cid) or day
        updates = {"grm_last_call_date": iso_date(last)}
        if status == "New":
            updates["grm_lead_status"] = "Attempted"
            promoted += 1
        ncd = parse_date_property(p.get("grm_next_call_date"))
        if clear_reached and ncd == day:              # only clear TODAY's stamp
            updates["grm_next_call_date"] = ""
            cleared += 1
        set_company_props(cid, updates)
        name = p.get("name") or f"Company {cid}"
        print(f"    [WORKED] {name} ({status}{' → Attempted' if status == 'New' else ''})")
    print(f"  Promoted New→Attempted: {promoted} | cleared off today's list: {cleared}")
    return len(worked)


# ─── PASS C: BUILD THE TARGET DAY ────────────────────────────────────────────
def is_eligible(status, last_call, target):
    """Eligibility by status + real last-call date vs the re-dial cooldown."""
    if status in EXCLUDED_STATUSES:
        return False
    if status == "New":
        # A New that was really dialed within the Attempted window is an
        # un-promoted Attempted — keep it out so it's never re-served too soon.
        if last_call and (target - last_call).days < NEW_DIALED_COOLDOWN:
            return False
        return True
    cooldown = REDIAL_DAYS.get(status)
    if cooldown is None:
        return False
    if last_call is None:
        return True
    return (target - last_call).days >= cooldown


def get_eligible_pool(target, exclude_ids, deal_ids, call_map):
    """All callable companies for the target day. Each company carries enough
    context to classify it as carry-forward / re-dial / fresh-New downstream.
    Future-stamped companies (reserved for a later day) are left out."""
    rows = search_all(
        "companies",
        [{"propertyName": "phone", "operator": "HAS_PROPERTY"}],
        ["name", "grm_lead_status", "grm_tier", "grm_last_call_date", "grm_next_call_date"],
    )
    pool = []
    for r in rows:
        cid = str(r["id"])
        if cid in exclude_ids or cid in deal_ids:
            continue
        p = r.get("properties", {})
        status = p.get("grm_lead_status") or "New"
        if status in EXCLUDED_STATUSES:
            continue
        next_call = parse_date_property(p.get("grm_next_call_date"))
        if next_call and next_call > target:          # reserved for a future day
            continue
        # Real last-call = newer of the stamp and the real CALL engagement.
        stamp_last = parse_date_property(p.get("grm_last_call_date"))
        real_last = call_map.get(cid)
        last_call = max([d for d in (stamp_last, real_last) if d], default=None)
        if not is_eligible(status, last_call, target):
            continue
        tier = p.get("grm_tier") if p.get("grm_tier") in TIER_TARGETS else "Untiered"
        pool.append({
            "id": cid,
            "name": p.get("name") or f"Company {cid}",
            "status": status,
            "tier": tier,
            "last_call": last_call,
            "carry": bool(next_call and next_call < target and status == "New"),
        })
    return pool


def scaled_targets(slots):
    """Scale the 45-blend down to `slots`, preserving proportions, summing to slots."""
    base_total = sum(TIER_TARGETS.values())
    if slots >= base_total:
        return dict(TIER_TARGETS)
    exact = {t: TIER_TARGETS[t] * slots / base_total for t in TIER_ORDER}
    floored = {t: int(exact[t]) for t in TIER_ORDER}
    leftover = slots - sum(floored.values())
    for t in sorted(TIER_ORDER, key=lambda t: exact[t] - floored[t], reverse=True)[:leftover]:
        floored[t] += 1
    return floored


def tier_blend_fill(candidates, slots):
    """Pick up to `slots` fresh-New companies on the tier blend, backfilling any
    short tier from the others in priority order A → B+ → B → Untiered."""
    by_tier = {t: [] for t in TIER_ORDER}
    for c in candidates:
        by_tier[c["tier"]].append(c)
    targets = scaled_targets(slots)
    selected, used = [], set()
    for tier in TIER_ORDER:
        take = targets.get(tier, 0)
        for co in by_tier[tier]:
            if take <= 0:
                break
            if co["id"] in used:
                continue
            selected.append(co); used.add(co["id"]); take -= 1
    if len(selected) < slots:                          # backfill short tiers
        for tier in TIER_ORDER:
            for co in by_tier[tier]:
                if len(selected) >= slots:
                    break
                if co["id"] in used:
                    continue
                selected.append(co); used.add(co["id"])
            if len(selected) >= slots:
                break
    return selected[:slots]


def build_target_day(target, call_map, deal_ids):
    """Rebuild the target calling day to exactly MAX_CALLS, in priority order:
        1) already stamped for the day (callbacks / future reschedules)
        2) carry-forward — unreached companies you didn't get to (never lost)
        3) due re-dials — called-but-unreached, past their cooldown (oldest first)
        4) fresh New — the tier blend, scaled to whatever slots remain
    Returns (already, carried, redials, fresh, tier_mix)."""
    print(f"\nPASS C — BUILD CALLING DAY for {target.strftime('%A, %B %d, %Y')}")
    print("─" * 60)

    already = companies_stamped_for(target)
    already_ids = {c["id"] for c in already}
    print(f"  Already stamped (callbacks/reschedules): {len(already)}")
    print(f"  Companies excluded (open deal): {len(deal_ids)}")

    slots = MAX_CALLS - len(already)
    if slots <= 0:
        print(f"  Target day already at/over {MAX_CALLS} — nothing to fill.")
        return len(already), 0, 0, 0, {}

    pool = get_eligible_pool(target, already_ids, deal_ids, call_map)

    carry_src  = sorted([c for c in pool if c["carry"]],
                        key=lambda c: (c["last_call"] or date.min))
    redial_src = sorted([c for c in pool if not c["carry"] and c["status"] in REDIAL_STATUSES],
                        key=lambda c: (c["last_call"] or date.min))   # most overdue first
    fresh_src  = [c for c in pool if not c["carry"] and c["status"] == "New"]
    print(f"  Eligible pool: carry-forward {len(carry_src)} | re-dials {len(redial_src)} | "
          f"fresh-New {len(fresh_src)}")

    selected, used = [], set()

    def take(seq, n):
        for co in seq:
            if n <= 0:
                break
            if co["id"] in used:
                continue
            selected.append(co); used.add(co["id"]); n -= 1
        return n

    remaining = slots
    remaining = take(carry_src, remaining)             # 2) carry-forward
    remaining = take(redial_src, remaining)            # 3) due re-dials
    if remaining > 0:                                  # 4) fresh-New tier blend
        for co in tier_blend_fill([c for c in fresh_src if c["id"] not in used], remaining):
            selected.append(co); used.add(co["id"])

    tier_mix = {t: 0 for t in TIER_ORDER}
    carried = redials = fresh = 0
    for co in selected:
        if not stamp_next_call_date(co["id"], target):
            continue
        tier_mix[co["tier"]] += 1
        if co["carry"]:
            carried += 1
        elif co["status"] in REDIAL_STATUSES:
            redials += 1
        else:
            fresh += 1

    mix_str = " ".join(f"{t}:{tier_mix[t]}" for t in TIER_ORDER)
    total = len(already) + carried + redials + fresh
    print(f"  Carried {carried} | re-dials {redials} | fresh {fresh} "
          f"(target {slots}). Tier mix — {mix_str}")
    print(f"  Total stamped for {iso_date(target)}: {total} / {MAX_CALLS}")
    return len(already), carried, redials, fresh, tier_mix


# ─── PASS D: EMAIL CAPTURE ───────────────────────────────────────────────────
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
NAME_RE  = re.compile(r"name:\s*([A-Za-z'\-]+)(?:[ \t]+([A-Za-z'\-]+))?", re.IGNORECASE)


def create_task(subject, task_type, due_ms, association_specs):
    """Create a HubSpot task WITH its associations in ONE API call."""
    payload = {
        "properties": {
            "hs_task_subject":  subject,
            "hs_task_type":     task_type,
            "hs_timestamp":     str(due_ms),
            "hs_task_status":   "NOT_STARTED",
            "hubspot_owner_id": RON_OWNER_ID,
        },
        "associations": [
            {"to": {"id": str(obj_id)},
             "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": type_id}]}
            for obj_id, type_id in association_specs
        ],
    }
    if DRY_RUN:
        return "DRY-RUN"
    resp, status = api("POST", "/crm/v3/objects/tasks", payload)
    if status not in (200, 201):
        print(f"  [ERROR] Task create failed ({subject}): {status} {resp}")
        return None
    return resp.get("id")


def find_contact_by_email(email):
    resp, status = api("POST", "/crm/v3/objects/contacts/search", {
        "filterGroups": [{"filters": [{"propertyName": "email", "operator": "EQ", "value": email}]}],
        "properties": ["email"], "limit": 1,
    })
    if status == 200 and resp.get("results"):
        return resp["results"][0]["id"]
    return None


def create_contact(email, first_name, last_name, company_id):
    payload = {"properties": {"email": email}}
    if first_name:
        payload["properties"]["firstname"] = first_name
    if last_name:
        payload["properties"]["lastname"] = last_name
    if company_id:
        payload["associations"] = [{
            "to": {"id": str(company_id)},
            "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": ASSOC_CONTACT_TO_COMPANY}],
        }]
    if DRY_RUN:
        return "DRY-RUN"
    resp, status = api("POST", "/crm/v3/objects/contacts", payload)
    if status in (200, 201):
        return resp.get("id")
    if status == 409:                      # already exists (race) — reuse it
        return find_contact_by_email(email)
    print(f"  [ERROR] Contact create failed ({email}): {status} {resp}")
    return None


def has_open_email_task(contact_id):
    resp, status = api("POST", "/crm/v3/objects/tasks/search", {
        "filterGroups": [{"filters": [
            {"propertyName": "associations.contact", "operator": "EQ", "value": str(contact_id)},
            {"propertyName": "hs_task_type",         "operator": "EQ", "value": "EMAIL"},
            {"propertyName": "hs_task_status",       "operator": "NEQ", "value": "COMPLETED"},
        ]}],
        "properties": ["hs_task_subject"], "limit": 1,
    })
    return status == 200 and resp.get("total", 0) > 0


def run_email_capture(target):
    """Today's emailed notes → next-day EMAIL tasks (due 9 AM ET on target)."""
    print("\nPASS D — EMAIL CAPTURE (notes created today)")
    print("─" * 60)
    due_ms = nine_am_ms(target)
    notes = notes_created_on(today_et())
    print(f"  Notes created today: {len(notes)}")

    emails_found, created_ids, errors = 0, [], []
    processed_emails = set()

    for note in notes:
        body = note.get("properties", {}).get("hs_note_body", "") or ""
        emails = [e for e in EMAIL_RE.findall(body) if not e.lower().endswith("@" + OUR_DOMAIN)]
        if not emails:
            continue
        cids = companies_for_note(note["id"])
        company_id = next(iter(cids)) if cids else None
        cname = company_name(company_id) if company_id else "Unknown Company"

        for email in emails:
            email = email.lower()
            if email in processed_emails:
                continue
            processed_emails.add(email)
            emails_found += 1
            print(f"  [EMAIL FOUND] {email} (note {note['id']}, {cname})")

            contact_id = find_contact_by_email(email)
            if contact_id:
                print(f"    contact matched: {contact_id}")
            else:
                m = NAME_RE.search(body)
                first, last = (m.group(1), m.group(2)) if m else (None, None)
                contact_id = create_contact(email, first, last, company_id)
                if not contact_id:
                    errors.append(f"contact create failed: {email}")
                    continue
                print(f"    contact created: {contact_id}")

            if not DRY_RUN and has_open_email_task(contact_id):
                print(f"    [SKIP] open EMAIL task already exists for contact {contact_id}")
                continue

            specs = [(contact_id, ASSOC_TASK_TO_CONTACT)]
            if company_id:
                specs.append((company_id, ASSOC_TASK_TO_COMPANY))
            tid = create_task(f"Email: {cname}", "EMAIL", due_ms, specs)
            if tid:
                created_ids.append(tid)
                print(f"    [EMAIL TASK] created (task {tid})")
            else:
                errors.append(f"email task failed: {email}")

    print(f"  Emails found: {emails_found} | EMAIL tasks created: {len(created_ids)}")
    return emails_found, created_ids, errors


# ─── PASS E: SPOT-CHECK ──────────────────────────────────────────────────────
def verify_email_tasks(task_ids):
    """Confirm up to 3 EMAIL tasks created this run carry BOTH a contact and a
    company association. Retries once for HubSpot's brief read lag before failing."""
    print("\nPASS E — SPOT-CHECK (EMAIL task associations)")
    print("─" * 60)
    if DRY_RUN or not task_ids:
        print("  [VERIFY] skipped (dry run or no EMAIL tasks created)")
        return True
    all_ok = True
    for tid in task_ids[:3]:
        ok = False
        for attempt in (1, 2):
            comp, cs = api("GET", f"/crm/v4/objects/tasks/{tid}/associations/companies")
            cont, ts = api("GET", f"/crm/v4/objects/tasks/{tid}/associations/contacts")
            ok = (cs == 200 and bool(comp.get("results"))) and (ts == 200 and bool(cont.get("results")))
            if ok or attempt == 2:
                break
            time.sleep(2)
        print(f"  [VERIFY] task {tid}: {'OK' if ok else 'MISSING association'}")
        all_ok = all_ok and ok
    if not all_ok:
        print("  [VERIFY] *** EMAIL TASK ASSOCIATION CHECK FAILED. INVESTIGATE NOW. ***")
    return all_ok


# ─── MAIN ────────────────────────────────────────────────────────────────────
def run_nightly():
    today, target = today_et(), tomorrow_et()
    call_map = recent_calls_by_company(today - timedelta(days=CALL_LOOKBACK_DAYS))
    stages   = resolve_meeting_stages()
    deal_ids = open_deal_company_ids()

    callback_pass(today)
    meeting_pass(today, deal_ids, stages)               # mutates deal_ids
    worked_detection_pass(today, call_map, clear_reached=True)
    already, carried, redials, fresh, tier_mix = build_target_day(target, call_map, deal_ids)
    emails_found, email_task_ids, email_errors = run_email_capture(target)
    associations_ok = verify_email_tasks(email_task_ids)

    print("\n" + "=" * 60)
    mix_str = " ".join(f"{t}:{tier_mix.get(t, 0)}" for t in TIER_ORDER)
    print(f"  SUMMARY ({iso_date(target)}): {already} kept + {carried} carried + "
          f"{redials} re-dials + {fresh} fresh = {already + carried + redials + fresh} / {MAX_CALLS} "
          f"(mix {mix_str})")
    print(f"  {emails_found} email(s) → {len(email_task_ids)} EMAIL task(s) | "
          f"{len(email_errors)} error(s)")
    for e in email_errors:
        print(f"  [!] {e}")
    print("=" * 60)
    if not associations_ok or email_errors:
        sys.exit(1)


def run_intraday():
    """Hourly during business hours: advance status from work logged so far today,
    book any meetings, and self-heal an empty list — without clearing the live 45."""
    today = today_et()
    call_map = recent_calls_by_company(today - timedelta(days=CALL_LOOKBACK_DAYS))
    stages   = resolve_meeting_stages()
    deal_ids = open_deal_company_ids()

    meeting_pass(today, deal_ids, stages)
    worked_detection_pass(today, call_map, clear_reached=False)

    stamped_today = companies_stamped_for(today)
    print(f"\nSELF-HEAL CHECK — companies stamped for {iso_date(today)}: {len(stamped_today)}")
    healed = None
    if not stamped_today:
        print("  Today's list is EMPTY — building it now.")
        healed = build_target_day(today, call_map, deal_ids)

    print("\n" + "=" * 60)
    if healed:
        already, carried, redials, fresh, _ = healed
        print(f"  INTRADAY SELF-HEAL: built {already + carried + redials + fresh} for {iso_date(today)}")
    else:
        print(f"  INTRADAY: today's list intact ({len(stamped_today)}); status advanced from real work.")
    print("=" * 60)


def main():
    label = "DRY RUN — NOTHING WRITTEN" if DRY_RUN else "LIVE RUN"
    mode = "INTRADAY" if INTRADAY else "NIGHTLY"
    print("=" * 60)
    print(f"  GRM CALLS (v3.1) — {mode} — {label}")
    print(f"  {now_et().strftime('%Y-%m-%d %I:%M %p ET')}")
    print("=" * 60)
    if INTRADAY:
        run_intraday()
    else:
        run_nightly()


if __name__ == "__main__":
    main()
