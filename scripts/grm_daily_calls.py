#!/usr/bin/env python3
"""
grm_daily_calls.py — GRM Nightly Builder (v3 — Calls live on the Company, not in Tasks)

WHAT CHANGED IN v3 (and why)
────────────────────────────────────────────────────────────────────────────
Calls left the Task system entirely. The old design created 45 CALL *tasks*
every night, and it flipped a company's lead status New→Attempted the moment a
task was QUEUED — so a company that was merely scheduled (never actually dialed)
looked "Attempted". Status drifted and the pool emptied.

v3 fixes both problems:

  • A company is flagged for a calling day by a DATE PROPERTY,
    `grm_next_call_date`. A saved Companies view ("Today's Calls") shows the
    day's batch, and Ron calls straight from that list. No CALL tasks at all.

  • Lead status now changes ONLY when real work is logged (a note or a CALL
    engagement on the company that day) — never on stamp/queue. We track the
    last real dial in `grm_last_call_date`.

  • Tasks are now EMAIL-ONLY: the follow-ups generated from emails captured the
    day before (PASS D below).

THE NIGHTLY RUN builds the NEXT day (the "target day") in five passes:

  A) CALLBACK PASS       — scan today's notes for callback intent, stamp the
                           parsed date on `grm_next_call_date`.
  B) WORKED-DETECTION    — for companies stamped for TODAY (the day finishing),
                           if real work was logged, set `grm_last_call_date` and
                           promote New→Attempted. Stamping never changes status.
  C) BUILD TARGET DAY    — fill the target day up to 45 companies using a
                           systematic tier blend (A=13, B+=14, B=4, Untiered=14),
                           drawing eligible companies and stamping
                           `grm_next_call_date`.
  D) EMAIL CAPTURE       — scan today's notes for emails → next-day EMAIL tasks.
  E) SPOT-CHECK          — confirm 3 EMAIL tasks created this run carry their
                           contact + company associations; fail the run if not.

The HubSpot token comes from the HUBSPOT_TOKEN environment variable (a GitHub
Actions secret) — it is never hardcoded here.

Usage:
  HUBSPOT_TOKEN=... python3 scripts/grm_daily_calls.py            # live (target = tomorrow)
  HUBSPOT_TOKEN=... python3 scripts/grm_daily_calls.py --dry-run  # no writes
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

# Daily tier blend — the systematic mix the target day is built from.
# (sums to MAX_CALLS = 45)
TIER_TARGETS = {"A": 13, "B+": 14, "B": 4, "Untiered": 14}
# Priority order used both for filling each tier and for backfilling shortfalls.
TIER_ORDER   = ["A", "B+", "B", "Untiered"]

# Re-dial cooldown by status, measured in days against grm_last_call_date.
# New has no cooldown (always eligible, top priority). A status with no
# last_call_date recorded is treated as eligible (never dialed → no cooldown).
REDIAL_DAYS = {"Connected": 2, "Attempted": 3, "Not Now": 14}
# Lowest number = highest priority when ordering within a tier.
STATUS_RANK = {"New": 0, "Connected": 1, "Attempted": 2, "Not Now": 3}

# Statuses that are NEVER eligible (removed from the calling pool entirely).
EXCLUDED_STATUSES = {"Not a Fit"}

DRY_RUN = "--dry-run" in sys.argv

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
    """Run a CRM search and follow pagination until every page is collected.
    Returns the full list of result objects."""
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


# ─── DATE HELPERS ────────────────────────────────────────────────────────────
def now_et():
    return datetime.now(tz=TZ)


def today_et():
    return now_et().date()


def tomorrow_et():
    return today_et() + timedelta(days=1)


def nine_am_ms(d):
    """9:00 AM Eastern on date d, as epoch milliseconds (HubSpot task due time)."""
    dt = datetime(d.year, d.month, d.day, 9, 0, 0, tzinfo=TZ)
    return int(dt.timestamp() * 1000)


def et_day_start_ms(d):
    """Midnight Eastern on date d, as epoch milliseconds. Used for 'created
    today' style filters on engagement timestamps (notes/calls)."""
    dt = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=TZ)
    return int(dt.timestamp() * 1000)


def utc_midnight_ms(d):
    """Midnight UTC on date d, as epoch milliseconds.

    HubSpot stores DATE-type properties (grm_next_call_date, grm_last_call_date)
    as midnight UTC. To filter 'grm_next_call_date == this calendar date' we must
    compare against this value, not the Eastern midnight."""
    dt = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def iso_date(d):
    """'YYYY-MM-DD' — the form HubSpot accepts when WRITING a date property."""
    return d.strftime("%Y-%m-%d")


def parse_date_property(raw):
    """Turn a stored date-property value into a date object, or None.

    HubSpot returns date properties as a midnight-UTC epoch-ms string
    (e.g. '1718409600000'); we also tolerate an ISO 'YYYY-MM-DD' string."""
    if not raw:
        return None
    try:
        ms = int(raw)
        return datetime.fromtimestamp(ms / 1000, tz=UTC).date()
    except (ValueError, TypeError):
        try:
            return date.fromisoformat(str(raw)[:10])
        except ValueError:
            return None


# ─── CALLBACK PARSING ────────────────────────────────────────────────────────
# Weekday names + common abbreviations, lowercase.
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

# The phrases that introduce a callback. Each captures the <when> that follows.
# Order matters: more specific phrases are tried before looser ones so that,
# e.g., "call back tomorrow" is read as a callback rather than "call <when>".
CALLBACK_TRIGGERS = [
    re.compile(r"callback:\s*(.+)", re.IGNORECASE),   # "callback: <when>"
    re.compile(r"\bcall back\s+(.+)", re.IGNORECASE),  # "call back <when>"
    re.compile(r"\bcallback\s+(.+)", re.IGNORECASE),   # "callback <when>"
    re.compile(r"\bcb\s+(.+)", re.IGNORECASE),         # "cb <when>"
    re.compile(r"^\s*call\s+(.+)", re.IGNORECASE),     # a line STARTING with "call <when>"
]


def _next_weekday(ref, target_weekday, force_next_week=False):
    """The next calendar date on or after ref+1 whose weekday == target.
    With force_next_week (for 'next <weekday>'), skip a full extra week."""
    days_ahead = (target_weekday - ref.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7  # 'wednesday' said on a Wednesday means the coming one
    if force_next_week:
        days_ahead += 7
    return ref + timedelta(days=days_ahead)


def parse_when(text, ref):
    """Resolve a <when> expression to a calendar date relative to ref (today),
    or None if no recognized time expression is present.

    Recognized: tomorrow | in N days | N days | <weekday> | next <weekday> |
    M/D[/Y] | YYYY-MM-DD | 'Month D'."""
    s = text.strip().lower()
    if not s:
        return None

    # tomorrow
    if re.match(r"tomorrow\b", s):
        return ref + timedelta(days=1)

    # "in N days" / "N days"
    m = re.search(r"\bin\s+(\d{1,3})\s+days?\b", s) or re.match(r"(\d{1,3})\s+days?\b", s)
    if m:
        return ref + timedelta(days=int(m.group(1)))

    # ISO date: 2026-06-11
    m = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None

    # US numeric date: 6/11 or 6/11/2026
    m = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", s)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        year = m.group(3)
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
        # No-year date already past this year → assume next year.
        if not m.group(3) and d < ref:
            try:
                d = date(year + 1, month, day)
            except ValueError:
                return None
        return d

    # Month-name date: "June 11" / "Jun 11"
    for i, month in enumerate(MONTH_NAMES, start=1):
        m = re.search(rf"\b(?:{month}|{month[:3]})\.?\s+(\d{{1,2}})\b", s)
        if m:
            day = int(m.group(1))
            try:
                d = date(ref.year, i, day)
            except ValueError:
                return None
            if d < ref:                       # month already passed → next year
                try:
                    d = date(ref.year + 1, i, day)
                except ValueError:
                    return None
            return d

    # "next <weekday>" — a full week beyond the coming occurrence.
    m = re.search(r"\bnext\s+([a-z]+)\b", s)
    if m and m.group(1) in WEEKDAY_LOOKUP:
        return _next_weekday(ref, WEEKDAY_LOOKUP[m.group(1)], force_next_week=True)

    # plain "<weekday>"
    for name, wd in WEEKDAY_LOOKUP.items():
        if re.search(rf"\b{name}\b", s):
            return _next_weekday(ref, wd)

    return None


def parse_callback_date(note_body, ref):
    """Find callback intent in a note and resolve it to a date, or None.
    Only returns a date when a recognized time expression is present — so a
    prospect merely saying 'they'll call' is not mistaken for a callback."""
    for line in (note_body or "").splitlines():
        for trigger in CALLBACK_TRIGGERS:
            m = trigger.search(line.strip())
            if m:
                d = parse_when(m.group(1), ref)
                if d:
                    return d
    return None


# ─── ASSOCIATION HELPER ──────────────────────────────────────────────────────
def companies_for_note(note_id):
    """Return the set of company IDs associated with a note."""
    assoc, status = api("GET", f"/crm/v4/objects/notes/{note_id}/associations/companies")
    if status != 200:
        return set()
    return {str(a["toObjectId"]) for a in assoc.get("results", [])}


def company_name(cid):
    co, status = api("GET", f"/crm/v3/objects/companies/{cid}", params={"properties": "name"})
    if status == 200:
        return co.get("properties", {}).get("name") or f"Company {cid}"
    return f"Company {cid}"


# ─── COMPANY WRITES ──────────────────────────────────────────────────────────
def set_company_props(company_id, props):
    """PATCH one company's properties. No-op (returns True) under --dry-run."""
    if DRY_RUN:
        return True
    _, status = api("PATCH", f"/crm/v3/objects/companies/{company_id}",
                    {"properties": props})
    return status in (200, 201)


def stamp_next_call_date(company_id, d):
    return set_company_props(company_id, {"grm_next_call_date": iso_date(d)})


# ─── DEAL EXCLUSION ──────────────────────────────────────────────────────────
def get_deal_company_ids():
    """Company IDs with an associated DEAL (= a booked meeting, now in the
    pipeline). These leave the calling pool. Deals are few, so we enumerate
    them and collect their company associations."""
    deal_ids = [d["id"] for d in search_all("deals",
                [{"propertyName": "hs_object_id", "operator": "HAS_PROPERTY"}],
                ["dealname"])]
    company_ids = set()
    for did in deal_ids:
        assoc, status = api("GET", f"/crm/v4/objects/deals/{did}/associations/companies")
        if status == 200:
            for a in assoc.get("results", []):
                company_ids.add(str(a["toObjectId"]))
    return company_ids


# ─── COMPANIES STAMPED FOR A GIVEN DAY ───────────────────────────────────────
def companies_stamped_for(d):
    """Companies whose grm_next_call_date equals calendar date d.
    Returns list of {id, name, grm_lead_status}."""
    rows = search_all(
        "companies",
        [{"propertyName": "grm_next_call_date", "operator": "EQ",
          "value": str(utc_midnight_ms(d))}],
        ["name", "grm_lead_status", "grm_next_call_date"],
    )
    return [{"id": str(r["id"]),
             "name": r.get("properties", {}).get("name") or f"Company {r['id']}",
             "grm_lead_status": r.get("properties", {}).get("grm_lead_status")}
            for r in rows]


# ─── PASS A: CALLBACK PASS ───────────────────────────────────────────────────
def callback_pass(ref=None):
    """Scan notes created today for callback intent and stamp the parsed date
    on grm_next_call_date for the note's company. Returns count stamped."""
    ref = ref or today_et()
    print("\nPASS A — CALLBACKS (notes created today)")
    print("─" * 60)
    notes = search_all(
        "notes",
        [{"propertyName": "hs_createdate", "operator": "GTE",
          "value": str(et_day_start_ms(ref))}],
        ["hs_note_body"],
    )
    print(f"  Notes created today: {len(notes)}")

    stamped = 0
    for note in notes:
        body = note.get("properties", {}).get("hs_note_body", "") or ""
        d = parse_callback_date(body, ref)
        if not d or d < ref:           # ignore unparseable or already-past dates
            continue
        for cid in companies_for_note(note["id"]):
            if stamp_next_call_date(cid, d):
                stamped += 1
                print(f"    [CALLBACK] {company_name(cid)} → {iso_date(d)}")
    print(f"  Callbacks stamped: {stamped}")
    return stamped


# ─── PASS B: WORKED DETECTION ────────────────────────────────────────────────
def worked_today(company_id, day):
    """True if a note OR a CALL engagement was logged on this company on `day`."""
    start = str(et_day_start_ms(day))
    notes = api("POST", "/crm/v3/objects/notes/search", {
        "filterGroups": [{"filters": [
            {"propertyName": "associations.company", "operator": "EQ", "value": str(company_id)},
            {"propertyName": "hs_createdate", "operator": "GTE", "value": start},
        ]}],
        "properties": ["hs_object_id"], "limit": 1,
    })[0]
    if notes.get("total", 0) > 0:
        return True
    calls = api("POST", "/crm/v3/objects/calls/search", {
        "filterGroups": [{"filters": [
            {"propertyName": "associations.company", "operator": "EQ", "value": str(company_id)},
            {"propertyName": "hs_timestamp", "operator": "GTE", "value": start},
        ]}],
        "properties": ["hs_object_id"], "limit": 1,
    })[0]
    return calls.get("total", 0) > 0


def worked_detection_pass(day=None):
    """For each company stamped for `day` (the day just finishing): if real work
    was logged, set grm_last_call_date = day and promote New→Attempted. If not
    worked, leave it New so it returns to the pool. Stamping never changes
    status — only real work does."""
    day = day or today_et()
    print(f"\nPASS B — WORKED DETECTION (companies stamped for {iso_date(day)})")
    print("─" * 60)
    stamped = companies_stamped_for(day)
    print(f"  Companies stamped for today: {len(stamped)}")

    worked = 0
    for co in stamped:
        if not worked_today(co["id"], day):
            continue
        worked += 1
        props = {"grm_last_call_date": iso_date(day)}
        # Real work promotes a New lead into the Attempted cadence; an already
        # Attempted/Connected/Not Now lead keeps its status.
        if co["grm_lead_status"] == "New":
            props["grm_lead_status"] = "Attempted"
        set_company_props(co["id"], props)
        print(f"    [WORKED] {co['name']} "
              f"({co['grm_lead_status']}{' → Attempted' if co['grm_lead_status'] == 'New' else ''})")
    print(f"  Worked today: {worked} | Not worked (stay in pool): {len(stamped) - worked}")
    return worked


# ─── PASS C: BUILD THE TARGET DAY ────────────────────────────────────────────
def is_eligible(status, last_call_date, target):
    """Eligibility by status, keyed off grm_last_call_date and re-dial cooldown.
    New is always eligible. A status with no last_call_date is eligible."""
    if status == "New":
        return True
    if status in EXCLUDED_STATUSES:
        return False
    cooldown = REDIAL_DAYS.get(status)
    if cooldown is None:
        return False                      # unknown status → not eligible
    if last_call_date is None:
        return True                       # never dialed → no cooldown
    return (target - last_call_date).days >= cooldown


def get_eligible_pool(target, exclude_ids, deal_ids):
    """Build the eligible calling pool grouped by tier.

    Pool = all companies EXCEPT 'Not a Fit', EXCEPT companies with a deal,
    that HAVE a phone number, are not already stamped for the target day, and
    are eligible by the status/cooldown rules. Each tier's list is ordered
    New-first, then Connected/Attempted/Not Now (most-overdue first)."""
    rows = search_all(
        "companies",
        [{"propertyName": "phone", "operator": "HAS_PROPERTY"}],
        ["name", "grm_lead_status", "grm_tier", "grm_last_call_date"],
    )
    by_tier = {t: [] for t in TIER_ORDER}
    for r in rows:
        cid = str(r["id"])
        p = r.get("properties", {})
        status = p.get("grm_lead_status") or "New"
        if cid in exclude_ids or cid in deal_ids:
            continue
        if status in EXCLUDED_STATUSES:
            continue
        last_call = parse_date_property(p.get("grm_last_call_date"))
        if not is_eligible(status, last_call, target):
            continue
        tier = p.get("grm_tier") if p.get("grm_tier") in by_tier else "Untiered"
        by_tier[tier].append({
            "id": cid,
            "name": p.get("name") or f"Company {cid}",
            "status": status,
            "tier": tier,
            "last_call": last_call,
        })

    # Order each tier: New first, then by cooldown bucket; within a bucket the
    # most-overdue (oldest last_call) first. None last_call sorts oldest.
    def sort_key(c):
        rank = STATUS_RANK.get(c["status"], 9)
        last_ord = c["last_call"].toordinal() if c["last_call"] else 0
        return (rank, last_ord)

    for tier in by_tier:
        by_tier[tier].sort(key=sort_key)
    return by_tier


def scaled_targets(slots):
    """Scale the per-day tier blend (sums to 45) down to `slots` remaining
    seats, preserving proportions and summing to exactly `slots`."""
    base_total = sum(TIER_TARGETS.values())  # 45
    if slots >= base_total:
        return dict(TIER_TARGETS)
    # Largest-remainder method so the rounded parts still sum to `slots`.
    exact = {t: TIER_TARGETS[t] * slots / base_total for t in TIER_ORDER}
    floored = {t: int(exact[t]) for t in TIER_ORDER}
    leftover = slots - sum(floored.values())
    # Hand out the leftover seats to the tiers with the largest fractional part.
    order = sorted(TIER_ORDER, key=lambda t: exact[t] - floored[t], reverse=True)
    for t in order[:leftover]:
        floored[t] += 1
    return floored


def tier_blend_fill(by_tier, slots):
    """Select up to `slots` companies using the tier blend, then backfill any
    shortfall from other tiers in priority order A → B+ → B → Untiered."""
    targets = scaled_targets(slots)
    selected, used = [], set()

    # First pass: take up to each tier's target.
    for tier in TIER_ORDER:
        take = targets.get(tier, 0)
        for co in by_tier.get(tier, []):
            if take <= 0:
                break
            if co["id"] in used:
                continue
            selected.append(co)
            used.add(co["id"])
            take -= 1

    # Backfill: if a tier was short, pull from any tier in priority order.
    if len(selected) < slots:
        for tier in TIER_ORDER:
            for co in by_tier.get(tier, []):
                if len(selected) >= slots:
                    break
                if co["id"] in used:
                    continue
                selected.append(co)
                used.add(co["id"])
            if len(selected) >= slots:
                break
    return selected[:slots]


def build_target_day(target, deal_ids=None):
    """Build the target calling day up to MAX_CALLS companies.

    Companies already stamped for the target day (callbacks + future-dated)
    come first and are counted; we only fill the gap up to 45 and never exceed
    it. Sets grm_next_call_date = target on each newly selected company.
    Returns (already_count, filled_count, tier_mix)."""
    print(f"\nPASS C — BUILD CALLING DAY for {target.strftime('%A, %B %d, %Y')}")
    print("─" * 60)

    if deal_ids is None:
        deal_ids = get_deal_company_ids()
        print(f"  Companies excluded (associated deal): {len(deal_ids)}")

    # (1) Already stamped for the target day — idempotency guard + callbacks.
    already = companies_stamped_for(target)
    already_ids = {c["id"] for c in already}
    print(f"  Already stamped for target day: {len(already)}")

    slots = MAX_CALLS - len(already)
    if slots <= 0:
        print(f"  Target day already at/over {MAX_CALLS} — nothing to fill.")
        return len(already), 0, {}

    # (2) Eligible pool, grouped by tier.
    by_tier = get_eligible_pool(target, exclude_ids=already_ids, deal_ids=deal_ids)
    counts = {t: len(by_tier[t]) for t in TIER_ORDER}
    print(f"  Eligible pool by tier: A:{counts['A']} B+:{counts['B+']} "
          f"B:{counts['B']} U:{counts['Untiered']}")

    # (3) Tier-blend fill.
    selected = tier_blend_fill(by_tier, slots)

    tier_mix = {t: 0 for t in TIER_ORDER}
    for co in selected:
        if stamp_next_call_date(co["id"], target):
            tier_mix[co["tier"]] += 1

    mix_str = " ".join(f"{t}:{tier_mix[t]}" for t in TIER_ORDER)
    total_for_day = len(already) + sum(tier_mix.values())
    print(f"  Filled {sum(tier_mix.values())} new (target {slots}). "
          f"Tier mix built — {mix_str}")
    print(f"  Total stamped for {iso_date(target)}: {total_for_day} / {MAX_CALLS}")
    return len(already), sum(tier_mix.values()), tier_mix


# ─── PASS D: EMAIL CAPTURE (unchanged behavior) ──────────────────────────────
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
NAME_RE  = re.compile(r"name:\s*([A-Za-z'\-]+)(?:[ \t]+([A-Za-z'\-]+))?", re.IGNORECASE)


def create_task(subject, task_type, due_ms, association_specs):
    """Create a HubSpot task WITH its associations in ONE API call.
    association_specs is a list of (object_id, association_type_id) tuples."""
    payload = {
        "properties": {
            "hs_task_subject":  subject,
            "hs_task_type":     task_type,
            "hs_timestamp":     str(due_ms),
            "hs_task_status":   "NOT_STARTED",
            "hubspot_owner_id": RON_OWNER_ID,
        },
        "associations": [
            {
                "to": {"id": str(obj_id)},
                "types": [{"associationCategory": "HUBSPOT_DEFINED",
                           "associationTypeId": type_id}],
            }
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
        "filterGroups": [{"filters": [
            {"propertyName": "email", "operator": "EQ", "value": email}]}],
        "properties": ["email"], "limit": 1,
    })
    if status == 200 and resp.get("results"):
        return resp["results"][0]["id"]
    return None


def create_contact(email, first_name, last_name, company_id):
    """Create a contact and associate it with the company in the SAME call."""
    payload = {"properties": {"email": email}}
    if first_name:
        payload["properties"]["firstname"] = first_name
    if last_name:
        payload["properties"]["lastname"] = last_name
    if company_id:
        payload["associations"] = [{
            "to": {"id": str(company_id)},
            "types": [{"associationCategory": "HUBSPOT_DEFINED",
                       "associationTypeId": ASSOC_CONTACT_TO_COMPANY}],
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
    """Scan today's notes for prospect emails and queue next-day EMAIL tasks
    (due 9 AM ET on the target day). Returns (emails_found, created_task_ids, errors)."""
    print("\nPASS D — EMAIL CAPTURE (notes created today)")
    print("─" * 60)
    due_ms = nine_am_ms(target)
    notes = search_all(
        "notes",
        [{"propertyName": "hs_createdate", "operator": "GTE",
          "value": str(et_day_start_ms(today_et()))}],
        ["hs_note_body"],
    )
    print(f"  Notes created today: {len(notes)}")

    emails_found, created_ids, errors = 0, [], []
    processed_emails = set()

    for note in notes:
        body = note.get("properties", {}).get("hs_note_body", "") or ""
        emails = [e for e in EMAIL_RE.findall(body)
                  if not e.lower().endswith("@" + OUR_DOMAIN)]
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
                first, last = None, None
                m = NAME_RE.search(body)
                if m:
                    first, last = m.group(1), m.group(2)
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
    """Confirm 3 EMAIL tasks created this run each carry BOTH a contact and a
    company association. Returns False (loudly) if any is missing."""
    print("\nPASS E — SPOT-CHECK (EMAIL task associations)")
    print("─" * 60)
    if DRY_RUN or not task_ids:
        print("  [VERIFY] skipped (dry run or no EMAIL tasks created)")
        return True
    sample = task_ids[:3]
    all_ok = True
    for tid in sample:
        comp, cs = api("GET", f"/crm/v4/objects/tasks/{tid}/associations/companies")
        cont, ts = api("GET", f"/crm/v4/objects/tasks/{tid}/associations/contacts")
        has_company = cs == 200 and bool(comp.get("results"))
        has_contact = ts == 200 and bool(cont.get("results"))
        print(f"  [VERIFY] task {tid}: company {'OK' if has_company else 'MISSING'}, "
              f"contact {'OK' if has_contact else 'MISSING'}")
        if not (has_company and has_contact):
            all_ok = False
    if not all_ok:
        print("  [VERIFY] *** EMAIL TASK ASSOCIATION CHECK FAILED. INVESTIGATE NOW. ***")
    return all_ok


# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    label = "DRY RUN — NOTHING WRITTEN" if DRY_RUN else "LIVE RUN"
    print("=" * 60)
    print(f"  GRM NIGHTLY (v3) — {label}")
    print(f"  {now_et().strftime('%Y-%m-%d %I:%M %p ET')}")
    print("=" * 60)

    target = tomorrow_et()

    # A) Stamp callbacks parsed from today's notes.
    callback_pass(today_et())

    # B) Record real work logged on today's stamped companies; promote status.
    worked_detection_pass(today_et())

    # C) Fill the target day up to 45 with the tier blend.
    already, filled, tier_mix = build_target_day(target)

    # D) Turn emails captured today into next-day EMAIL tasks.
    emails_found, email_task_ids, email_errors = run_email_capture(target)

    # E) Spot-check the EMAIL tasks we created.
    associations_ok = verify_email_tasks(email_task_ids)

    print("\n" + "=" * 60)
    mix_str = " ".join(f"{t}:{tier_mix.get(t, 0)}" for t in TIER_ORDER)
    print(f"  SUMMARY: {already} pre-stamped + {filled} filled = "
          f"{already + filled} for {iso_date(target)} (mix {mix_str}) | "
          f"{emails_found} email(s) found | {len(email_task_ids)} EMAIL task(s) | "
          f"{len(email_errors)} error(s)")
    for e in email_errors:
        print(f"  [!] {e}")
    print("=" * 60)

    # Fail the workflow loudly if the spot-check failed or any error occurred.
    if not associations_ok or email_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
