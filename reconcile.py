#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

total = 0.0
count = 0

# A payment can be attempted more than once. Every attempt has the same txn_id.


with open("payments.jsonl") as f:
    for line in f:
        if not line.strip():  # Ignore empty lines
            continue

        try: 
            event = json.loads(line)
                    
            if "txn_id" not in event:   # Ignore events without a txn_id
                continue
            
            # Solution to TypeError = remove comma(s) from string first before converting to float
            if type(event["amount"]) != float:
                event["amount"] = event["amount"].replace(",", "")

            if event["status"] == "success":        # A payment counts as collected only if its LATEST attempt is success.
                total += float(event["amount"])     # TypeError: unsupported operand type(s) for +=: 'float' and 'str'
                count += 1

        # Ignore lines that can't be read: json.decoder.JSONDecodeError
        except json.decoder.JSONDecodeError:
            continue

                                       # Only the latest attempt for each txn_id counts.
        

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")