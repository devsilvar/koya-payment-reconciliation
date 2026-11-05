#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json
from datetime import datetime

latest_by_txn_id = {}

with open("payments.jsonl", encoding="utf-8") as f:
    for line in f:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if not isinstance(event, dict) or not event.get("txn_id"):
            continue

        timestamp = datetime.fromisoformat(event["ts"].replace("Z", "+00:00"))
        previous = latest_by_txn_id.get(event["txn_id"])
        if previous is None or timestamp >= previous[0]:
            latest_by_txn_id[event["txn_id"]] = (timestamp, event)

total = 0.0
count = 0
for _, event in latest_by_txn_id.values():
    if event["status"] == "success":
        total += float(str(event["amount"]).replace(",", ""))
        count += 1

with open("expected.txt", encoding="utf-8") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
