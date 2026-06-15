#!/usr/bin/env python3
"""
grm_reset_reseed.py — ONE-TIME clean-slate reset + today reseed for the v3
"calls live on the Company" redesign.

This is NOT a nightly script. It is run once (via the manual
`reset-reseed.yml` GitHub Actions workflow) to migrate the board onto the new
model. It is destructive in a bounded way and guarded behind an explicit
confirmation token so it cannot fire by accident.

It performs, in order:

  STEP 1 — PROPERTIES  Create grm_next_call_date and grm_last_call_date
                       (date, label, grm_ group) if they don't already exist.

  STEP 2 — RESET       • Archive ALL NOT_STARTED CALL tasks (call-tasks are
                         deprecated), then verify 0 remain.
                       • Set grm_lead_status = New on ALL companies, verify 0
                         Attempted remain.
                       • Clear grm_next_call_date on any company that has it.
                       (Notes, calls, deals, EMAIL tasks, and grm_tier are
                       NOT touched.)

  STEP 4 — RESEED      Stamp grm_next_call_date = TODAY on 45 companies using
                       the same tier blend / pool / eligibility rules as the
                       nightly build, then verify exactly 45 are stamped and
                       log the tier mix.

Guard: set CONFIRM_RESET=RESET-AND-RESEED in the environment to actually run.
Without it the script prints what it would do and exits.

  HUBSPOT_TOKEN=... CONFIRM_RESET=RESET-AND-RESEED python3 scripts/grm_reset_reseed.py
"""

import os
import sys
import time

# Reuse every helper, constant, and the build logic from the nightly script.
import grm_daily_calls as g

CONFIRM = os.environ.get("CONFIRM_RESET")
ARMED = CONFIRM == "RESET-AND-RESEED"


# ─── STEP 1: PROPERTIES ──────────────────────────────────────────────────────
def grm_group_name():
    """Reuse the property group that grm_tier already lives in (the 'grm_'
    group), falling back to the default company-information group."""
    resp, status = g.api("GET", "/crm/v3/properties/companies/grm_tier")
    if status == 200 and resp.get("groupName"):
        return resp["groupName"]
    return "companyinformation"


def ensure_date_property(name, label, group):
    """Create a DATE company property if it doesn't already exist (idempotent)."""
    _, status = g.api("GET", f"/crm/v3/properties/companies/{name}")
    if status == 200:
        print(f"  [OK] property '{name}' already exists")
        return True
    payload = {
        "name": name,
        "label": label,
        "type": "date",
        "fieldType": "date",
        "groupName": group,
    }
    if not ARMED:
        print(f"  [DRY] would create property '{name}' ({label}) in group '{group}'")
        return True
    resp, status = g.api("POST", "/crm/v3/properties/companies", payload)
    if status in (200, 201):
        print(f"  [CREATED] property '{name}' ({label}) in group '{group}'")
        return True
    print(f"  [ERROR] could not create '{name}': {status} {resp}")
    return False


def step1_properties():
    print("\nSTEP 1 — PROPERTIES")
    print("─" * 60)
    group = grm_group_name()
    ok1 = ensure_date_property("grm_next_call_date", "Next Call Date", group)
    ok2 = ensure_date_property("grm_last_call_date", "Last Call Date", group)
    # Give HubSpot a moment for the new schema to become searchable.
    if ARMED and (ok1 or ok2):
        time.sleep(3)
    return ok1 and ok2


# ─── STEP 2: RESET ───────────────────────────────────────────────────────────
def archive_call_tasks():
    """Archive every NOT_STARTED CALL task, 100 per batch, then verify none
    remain. Touches ONLY call-type tasks."""
    print("\n  Archiving NOT_STARTED CALL tasks…")
    tasks = g.search_all(
        "tasks",
        [{"propertyName": "hs_task_type",   "operator": "EQ", "value": "CALL"},
         {"propertyName": "hs_task_status", "operator": "EQ", "value": "NOT_STARTED"}],
        ["hs_task_subject"],
    )
    ids = [t["id"] for t in tasks]
    print(f"    Found {len(ids)} NOT_STARTED CALL task(s)")
    if not ARMED:
        print("    [DRY] would batch-archive these")
        return
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        _, status = g.api("POST", "/crm/v3/objects/tasks/batch/archive",
                          {"inputs": [{"id": x} for x in chunk]})
        print(f"    archived {len(chunk)} (HTTP {status})")
        time.sleep(0.2)
    # Verify 0 remain.
    remaining = g.search_all(
        "tasks",
        [{"propertyName": "hs_task_type",   "operator": "EQ", "value": "CALL"},
         {"propertyName": "hs_task_status", "operator": "EQ", "value": "NOT_STARTED"}],
        ["hs_object_id"],
    )
    print(f"    VERIFY: {len(remaining)} NOT_STARTED CALL task(s) remain "
          f"(expected 0){'  ✅' if not remaining else '  ❌'}")


def reset_all_companies_to_new():
    """Set grm_lead_status = New on ALL companies (100 per batch), then verify
    0 Attempted remain."""
    print("\n  Resetting grm_lead_status = New on ALL companies…")
    companies = g.search_all(
        "companies",
        [{"propertyName": "hs_object_id", "operator": "HAS_PROPERTY"}],
        ["grm_lead_status"],
    )
    ids = [c["id"] for c in companies]
    print(f"    {len(ids)} companies total")
    if not ARMED:
        print("    [DRY] would batch-set grm_lead_status = New")
        return
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        _, status = g.api("POST", "/crm/v3/objects/companies/batch/update",
                          {"inputs": [{"id": x, "properties": {"grm_lead_status": "New"}}
                                      for x in chunk]})
        print(f"    updated {len(chunk)} (HTTP {status})")
        time.sleep(0.2)
    attempted = g.search_all(
        "companies",
        [{"propertyName": "grm_lead_status", "operator": "EQ", "value": "Attempted"}],
        ["hs_object_id"],
    )
    print(f"    VERIFY: {len(attempted)} Attempted remain (expected 0)"
          f"{'  ✅' if not attempted else '  ❌'}")


def clear_next_call_dates():
    """Clear grm_next_call_date on any company that has it set."""
    print("\n  Clearing grm_next_call_date where set…")
    companies = g.search_all(
        "companies",
        [{"propertyName": "grm_next_call_date", "operator": "HAS_PROPERTY"}],
        ["hs_object_id"],
    )
    ids = [c["id"] for c in companies]
    print(f"    {len(ids)} companies have grm_next_call_date set")
    if not ARMED:
        print("    [DRY] would clear these")
        return
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        _, status = g.api("POST", "/crm/v3/objects/companies/batch/update",
                          {"inputs": [{"id": x, "properties": {"grm_next_call_date": ""}}
                                      for x in chunk]})
        print(f"    cleared {len(chunk)} (HTTP {status})")
        time.sleep(0.2)


def step2_reset():
    print("\nSTEP 2 — RESET")
    print("─" * 60)
    archive_call_tasks()
    reset_all_companies_to_new()
    clear_next_call_dates()


# ─── STEP 4: RESEED TODAY ────────────────────────────────────────────────────
def step4_reseed():
    print("\nSTEP 4 — RESEED TODAY")
    print("─" * 60)
    today = g.today_et()
    if not ARMED:
        print("  [DRY] would build today's 45-company calling day via tier blend")
        return
    already, filled, tier_mix = g.build_target_day(today)
    # Verify exactly 45 are stamped for today.
    stamped = g.companies_stamped_for(today)
    mix_str = " ".join(f"{t}:{tier_mix.get(t, 0)}" for t in g.TIER_ORDER)
    print(f"\n  VERIFY: {len(stamped)} companies stamped for {g.iso_date(today)} "
          f"(expected {g.MAX_CALLS}){'  ✅' if len(stamped) == g.MAX_CALLS else '  ❌'}")
    print(f"  Tier mix built — {mix_str}")
    return len(stamped)


# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print(f"  GRM RESET + RESEED — {'ARMED (LIVE)' if ARMED else 'DRY RUN (set CONFIRM_RESET to arm)'}")
    print(f"  {g.now_et().strftime('%Y-%m-%d %I:%M %p ET')}")
    print("=" * 60)

    props_ok = step1_properties()
    if ARMED and not props_ok:
        sys.exit("FATAL: properties could not be ensured — aborting before reset.")

    step2_reset()
    stamped = step4_reseed()

    print("\n" + "=" * 60)
    if not ARMED:
        print("  DRY RUN complete — no writes made. Set CONFIRM_RESET=RESET-AND-RESEED to run.")
    else:
        ok = stamped == g.MAX_CALLS
        print(f"  RESET + RESEED complete — {stamped} companies stamped for today"
              f"{'  ✅' if ok else '  ❌ (expected 45)'}")
        if not ok:
            sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
