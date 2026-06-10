#!/usr/bin/env python3
"""
grm_daily_calls.py — GRM Nightly Call List Builder (v2 — GitHub Actions)

Runs Sun-Thu evening (GitHub Actions cron) and does two passes:

  PASS 1 — CALL LIST: builds tomorrow's 45-task call list in HubSpot.
    Priority 1: companies whose MOST RECENT note contains
                "callback: <day> <time>" matching tomorrow.
    Priority 2: random fill from companies with grm_lead_status = New,
                or Attempted with no activity in the last 3 days.
    CRITICAL: every task is created WITH its company association in a
    single API call (the old script associated in a second call that
    failed silently — 2,530 orphaned tasks).

  PASS 2 — EMAIL CAPTURE: scans notes created today for email addresses,
    creates/matches contacts, and creates next-day EMAIL tasks associated
    with both the contact and the company.

The HubSpot token comes from the HUBSPOT_TOKEN environment variable
(set as a GitHub Actions secret) — it is never hardcoded here.

Usage:
  HUBSPOT_TOKEN=... python3 scripts/grm_daily_calls.py            # live
  HUBSPOT_TOKEN=... python3 scripts/grm_daily_calls.py --dry-run  # no writes
"""

import os
import re
import sys
import json
import time
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

# ─── CONFIG ──────────────────────────────────────────────────────────────────
TOKEN = os.environ.get("HUBSPOT_TOKEN")
if not TOKEN:
    sys.exit("FATAL: HUBSPOT_TOKEN environment variable is not set.")

TZ           = ZoneInfo("America/New_York")
MAX_TASKS    = 45
RON_OWNER_ID = "90284376"          # ron@getrootedmedia.com
OUR_DOMAIN   = "getrootedmedia.com"  # ignore our own addresses in email capture

# HubSpot-defined association type IDs (v4 associations API)
ASSOC_TASK_TO_COMPANY    = 192
ASSOC_TASK_TO_CONTACT    = 204
ASSOC_CONTACT_TO_COMPANY = 279

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
    """9:00 AM Eastern on date d, as epoch milliseconds (HubSpot due time)."""
    dt = datetime(d.year, d.month, d.day, 9, 0, 0, tzinfo=TZ)
    return int(dt.timestamp() * 1000)


def day_start_ms(d):
    """Midnight Eastern on date d, as epoch milliseconds."""
    dt = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=TZ)
    return int(dt.timestamp() * 1000)


# ─── CALLBACK PARSING ────────────────────────────────────────────────────────
# Full weekday names and common abbreviations, all lowercase.
WEEKDAY_NAMES = {
    0: ("monday", "mon"), 1: ("tuesday", "tue", "tues"),
    2: ("wednesday", "wed"), 3: ("thursday", "thu", "thur", "thurs"),
    4: ("friday", "fri"), 5: ("saturday", "sat"), 6: ("sunday", "sun"),
}
MONTH_NAMES = ["january", "february", "march", "april", "may", "june", "july",
               "august", "september", "october", "november", "december"]


def callback_matches_tomorrow(note_body):
    """True if the note contains 'callback: <day> <time>' where <day>
    refers to tomorrow. Accepts 'tomorrow', weekday names ('Wednesday',
    'wed'), numeric dates (6/11, 2026-06-11), and 'June 11' style dates."""
    lower = (note_body or "").lower()
    idx = lower.find("callback:")
    if idx == -1:
        return False
    snippet = lower[idx:idx + 80]  # day/time live right after "callback:"
    tmrw = tomorrow_et()

    if "tomorrow" in snippet:
        return True

    # Weekday name match — only counts when tomorrow IS that weekday.
    for name in WEEKDAY_NAMES[tmrw.weekday()]:
        if re.search(rf"\b{name}\b", snippet):
            return True

    # ISO date: 2026-06-11
    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", snippet)
    if m and (int(m.group(1)), int(m.group(2)), int(m.group(3))) == (tmrw.year, tmrw.month, tmrw.day):
        return True

    # US date: 6/11 or 6/11/2026
    m = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", snippet)
    if m and int(m.group(1)) == tmrw.month and int(m.group(2)) == tmrw.day:
        yr = m.group(3)
        if not yr or int(yr) in (tmrw.year, tmrw.year % 100):
            return True

    # Month-name date: "June 11" / "Jun 11"
    month = MONTH_NAMES[tmrw.month - 1]
    if re.search(rf"\b(?:{month}|{month[:3]})\.?\s+{tmrw.day}\b", snippet):
        return True

    return False


# ─── TASK CREATION (single-call association — the critical fix) ──────────────
def create_task(subject, task_type, due_ms, association_specs):
    """Create a HubSpot task WITH its associations in ONE API call.
    association_specs is a list of (object_id, association_type_id) tuples.
    Returns the new task ID, or None on failure."""
    payload = {
        "properties": {
            "hs_task_subject":  subject,
            "hs_task_type":     task_type,
            "hs_timestamp":     str(due_ms),
            "hs_task_status":   "NOT_STARTED",
            "hubspot_owner_id": RON_OWNER_ID,
        },
        # Associations ride along in the create payload — no second call.
        "associations": [
            {
                "to": {"id": str(obj_id)},
                "types": [{
                    "associationCategory": "HUBSPOT_DEFINED",
                    "associationTypeId":   type_id,
                }],
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


def update_lead_status(company_id, new_status):
    if DRY_RUN:
        return True
    resp, status = api("PATCH", f"/crm/v3/objects/companies/{company_id}",
                       {"properties": {"grm_lead_status": new_status}})
    return status in (200, 201)


# ─── PASS 1, STEP A: CALLBACK COMPANIES ──────────────────────────────────────
def get_callback_companies():
    """Find companies whose MOST RECENT note contains a callback matching
    tomorrow. Returns list of {company_id, company_name}."""
    # Look at notes from the last 14 days that mention "callback".
    cutoff_ms = day_start_ms(today_et() - timedelta(days=14))
    notes = search_all(
        "notes",
        [{"propertyName": "hs_createdate", "operator": "GTE", "value": str(cutoff_ms)}],
        ["hs_note_body", "hs_createdate"],
    )

    # Collect the companies attached to any recent callback note.
    candidate_company_ids = set()
    for note in notes:
        body = note.get("properties", {}).get("hs_note_body", "") or ""
        if "callback:" not in body.lower():
            continue
        assoc, status = api("GET", f"/crm/v4/objects/notes/{note['id']}/associations/companies")
        if status == 200:
            for a in assoc.get("results", []):
                candidate_company_ids.add(str(a["toObjectId"]))

    # For each candidate, check that its MOST RECENT note (not just any
    # note) is a callback matching tomorrow — a newer note supersedes.
    matches = []
    for cid in candidate_company_ids:
        latest = search_all(
            "notes",
            [{"propertyName": "associations.company", "operator": "EQ", "value": cid}],
            ["hs_note_body", "hs_createdate"],
            sorts=[{"propertyName": "hs_createdate", "direction": "DESCENDING"}],
        )
        if not latest:
            continue
        latest_body = latest[0].get("properties", {}).get("hs_note_body", "") or ""
        if not callback_matches_tomorrow(latest_body):
            continue
        co, status = api("GET", f"/crm/v3/objects/companies/{cid}",
                         params={"properties": "name"})
        name = co.get("properties", {}).get("name") if status == 200 else None
        matches.append({"company_id": cid, "company_name": name or f"Company {cid}"})
    return matches


# ─── PASS 1, STEP B: FILL POOL ───────────────────────────────────────────────
def get_fill_pool():
    """Companies eligible for a cold/retry call:
       - grm_lead_status = New (always eligible)
       - grm_lead_status = Attempted AND last activity 3+ days ago (or none)"""
    three_days_ago_ms = int((now_et() - timedelta(days=3)).timestamp() * 1000)
    props = ["name", "grm_lead_status", "hs_last_activity_date", "notes_last_updated"]
    pool, seen = [], set()

    for status_value in ("New", "Attempted"):
        companies = search_all(
            "companies",
            [{"propertyName": "grm_lead_status", "operator": "EQ", "value": status_value}],
            props,
        )
        for co in companies:
            cid = str(co["id"])
            if cid in seen:
                continue
            p = co.get("properties", {})
            last_raw = p.get("hs_last_activity_date") or p.get("notes_last_updated")
            # Activity timestamps can be ISO strings or epoch ms — normalize to ms.
            last_ms = 0
            if last_raw:
                try:
                    last_ms = int(last_raw)
                except (ValueError, TypeError):
                    try:
                        last_ms = int(datetime.fromisoformat(
                            last_raw.replace("Z", "+00:00")).timestamp() * 1000)
                    except ValueError:
                        last_ms = 0
            # Attempted companies only retry after 3+ quiet days.
            if status_value == "Attempted" and last_ms > three_days_ago_ms:
                continue
            seen.add(cid)
            pool.append({"id": cid, "name": p.get("name") or f"Company {cid}",
                         "lead_status": status_value})
    return pool


def get_companies_with_tomorrow_call_task():
    """Company IDs that already have an open CALL task due tomorrow —
    guards against duplicates if the script runs twice in one evening."""
    tmrw = tomorrow_et()
    tasks = search_all(
        "tasks",
        [
            {"propertyName": "hs_task_type",   "operator": "EQ",  "value": "CALL"},
            {"propertyName": "hs_timestamp",   "operator": "GTE", "value": str(day_start_ms(tmrw))},
            {"propertyName": "hs_timestamp",   "operator": "LT",  "value": str(day_start_ms(tmrw + timedelta(days=1)))},
            {"propertyName": "hs_task_status", "operator": "NEQ", "value": "COMPLETED"},
        ],
        ["hs_task_subject"],
    )
    company_ids = set()
    for t in tasks:
        assoc, status = api("GET", f"/crm/v4/objects/tasks/{t['id']}/associations/companies")
        if status == 200:
            for a in assoc.get("results", []):
                company_ids.add(str(a["toObjectId"]))
    return company_ids, len(tasks)


# ─── PASS 1: BUILD THE CALL LIST ─────────────────────────────────────────────
def build_call_list():
    tmrw = tomorrow_et()
    due_ms = nine_am_ms(tmrw)
    created_task_ids = []
    errors = []

    print(f"\nPASS 1 — CALL LIST for {tmrw.strftime('%A, %B %d, %Y')}")
    print("─" * 60)

    scheduled_company_ids, existing_count = get_companies_with_tomorrow_call_task()
    if existing_count:
        print(f"  {existing_count} open CALL task(s) already due tomorrow — counting toward {MAX_TASKS}.")

    # Priority 1 — callbacks
    print("  Scanning recent notes for callbacks matching tomorrow…")
    callbacks = get_callback_companies()
    print(f"  Callback companies matching tomorrow: {len(callbacks)}")
    for cb in callbacks:
        if cb["company_id"] in scheduled_company_ids:
            print(f"    [SKIP] {cb['company_name']} — already has a task tomorrow")
            continue
        if len(scheduled_company_ids) >= MAX_TASKS:
            break
        tid = create_task(f"Call: {cb['company_name']}", "CALL", due_ms,
                          [(cb["company_id"], ASSOC_TASK_TO_COMPANY)])
        if tid:
            scheduled_company_ids.add(cb["company_id"])
            created_task_ids.append(tid)
            print(f"    [CALLBACK] {cb['company_name']} (task {tid})")
        else:
            errors.append(f"callback task failed: {cb['company_name']}")

    # Priority 2 — random fill from New/Attempted
    remaining = MAX_TASKS - existing_count - len(created_task_ids)
    print(f"  Open slots remaining: {remaining}")
    if remaining > 0:
        pool = get_fill_pool()
        eligible = [c for c in pool if c["id"] not in scheduled_company_ids]
        print(f"  Fill pool: {len(pool)} eligible companies ({len(eligible)} after dedupe)")
        random.shuffle(eligible)
        for co in eligible[:remaining]:
            tid = create_task(f"Call: {co['name']}", "CALL", due_ms,
                              [(co["id"], ASSOC_TASK_TO_COMPANY)])
            if tid:
                scheduled_company_ids.add(co["id"])
                created_task_ids.append(tid)
                print(f"    [FILL] {co['name']} (task {tid})")
                # First touch moves a New company into the Attempted cadence.
                if co["lead_status"] == "New":
                    update_lead_status(co["id"], "Attempted")
            else:
                errors.append(f"fill task failed: {co['name']}")

    print(f"  Call tasks created this run: {len(created_task_ids)} (target {MAX_TASKS}, "
          f"{existing_count} pre-existing)")
    return created_task_ids, errors


# ─── ASSOCIATION VERIFICATION ────────────────────────────────────────────────
def verify_associations(task_ids):
    """Spot-check 3 random created tasks: each MUST have a company
    association. Returns False (and screams in the log) if any is bare."""
    if DRY_RUN or not task_ids:
        print("  [VERIFY] skipped (dry run or no tasks created)")
        return True
    sample = random.sample(task_ids, min(3, len(task_ids)))
    all_ok = True
    for tid in sample:
        assoc, status = api("GET", f"/crm/v4/objects/tasks/{tid}/associations/companies")
        ok = status == 200 and bool(assoc.get("results"))
        print(f"  [VERIFY] task {tid}: company association "
              f"{'OK' if ok else 'MISSING'}")
        if not ok:
            all_ok = False
    if not all_ok:
        print("  [VERIFY] *** ASSOCIATION VERIFICATION FAILED — tasks were "
              "created without company associations. INVESTIGATE NOW. ***")
    return all_ok


# ─── PASS 2: END-OF-DAY EMAIL CAPTURE ────────────────────────────────────────
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# "name: John Smith" — first name required, last name optional.
NAME_RE = re.compile(r"name:\s*([A-Za-z'\-]+)(?:[ \t]+([A-Za-z'\-]+))?", re.IGNORECASE)


def find_contact_by_email(email):
    """Return contact ID if a contact with this email exists, else None."""
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
    # 409 = contact already exists (race with the search above) — reuse it.
    if status == 409:
        return find_contact_by_email(email)
    print(f"  [ERROR] Contact create failed ({email}): {status} {resp}")
    return None


def has_open_email_task(contact_id):
    """True if the contact already has an open EMAIL task (dedupe guard)."""
    resp, status = api("POST", "/crm/v3/objects/tasks/search", {
        "filterGroups": [{"filters": [
            {"propertyName": "associations.contact", "operator": "EQ", "value": str(contact_id)},
            {"propertyName": "hs_task_type",         "operator": "EQ", "value": "EMAIL"},
            {"propertyName": "hs_task_status",       "operator": "NEQ", "value": "COMPLETED"},
        ]}],
        "properties": ["hs_task_subject"], "limit": 1,
    })
    return status == 200 and resp.get("total", 0) > 0


def run_email_capture():
    """Scan today's notes for prospect email addresses and queue next-day
    EMAIL tasks. Returns (emails_found, tasks_created, errors)."""
    print(f"\nPASS 2 — EMAIL CAPTURE (notes created today)")
    print("─" * 60)
    due_ms = nine_am_ms(tomorrow_et())
    notes = search_all(
        "notes",
        [{"propertyName": "hs_createdate", "operator": "GTE",
          "value": str(day_start_ms(today_et()))}],
        ["hs_note_body"],
    )
    print(f"  Notes created today: {len(notes)}")

    emails_found, tasks_created, errors = 0, 0, []
    processed_emails = set()  # same email in two notes → handle once

    for note in notes:
        body = note.get("properties", {}).get("hs_note_body", "") or ""
        emails = [e for e in EMAIL_RE.findall(body)
                  if not e.lower().endswith("@" + OUR_DOMAIN)]
        if not emails:
            continue

        # Company attached to this note (used for contact + task association).
        assoc, status = api("GET", f"/crm/v4/objects/notes/{note['id']}/associations/companies")
        company_id = None
        if status == 200 and assoc.get("results"):
            company_id = str(assoc["results"][0]["toObjectId"])
        company_name = f"Company {company_id}" if company_id else "Unknown Company"
        if company_id:
            co, cstatus = api("GET", f"/crm/v3/objects/companies/{company_id}",
                              params={"properties": "name"})
            if cstatus == 200 and co.get("properties", {}).get("name"):
                company_name = co["properties"]["name"]

        for email in emails:
            email = email.lower()
            if email in processed_emails:
                continue
            processed_emails.add(email)
            emails_found += 1
            print(f"  [EMAIL FOUND] {email} (note {note['id']}, {company_name})")

            # Match or create the contact.
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
                print(f"    contact created: {contact_id}"
                      + (f" ({first} {last or ''})".rstrip() if m else " (email only)"))

            # Dedupe: skip if an open EMAIL task already exists for them.
            if not DRY_RUN and has_open_email_task(contact_id):
                print(f"    [SKIP] open EMAIL task already exists for contact {contact_id}")
                continue

            # Task associated with BOTH contact and company in one call.
            specs = [(contact_id, ASSOC_TASK_TO_CONTACT)]
            if company_id:
                specs.append((company_id, ASSOC_TASK_TO_COMPANY))
            tid = create_task(f"Email: {company_name}", "EMAIL", due_ms, specs)
            if tid:
                tasks_created += 1
                print(f"    [EMAIL TASK] created (task {tid})")
            else:
                errors.append(f"email task failed: {email}")

    print(f"  Emails found: {emails_found} | EMAIL tasks created: {tasks_created}")
    return emails_found, tasks_created, errors


# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    label = "DRY RUN — NOTHING WRITTEN" if DRY_RUN else "LIVE RUN"
    print("=" * 60)
    print(f"  GRM NIGHTLY — {label}")
    print(f"  {now_et().strftime('%Y-%m-%d %I:%M %p ET')}")
    print("=" * 60)

    call_task_ids, call_errors = build_call_list()

    print("\nASSOCIATION VERIFICATION (3 random tasks)")
    print("─" * 60)
    associations_ok = verify_associations(call_task_ids)

    emails_found, email_tasks, email_errors = run_email_capture()

    all_errors = call_errors + email_errors
    print("\n" + "=" * 60)
    print(f"  SUMMARY: {len(call_task_ids)} call task(s) | "
          f"{emails_found} email(s) found | {email_tasks} email task(s) | "
          f"{len(all_errors)} error(s)")
    for e in all_errors:
        print(f"  [!] {e}")
    print("=" * 60)

    # Fail the workflow loudly if anything went wrong.
    if not associations_ok or all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
