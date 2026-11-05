# Payment reconciliation

`payments.jsonl` is an export of payment events from a payments provider, one JSON object per line. The reconciliation script works out how much money was actually collected and prints a code when the successful-payment count matches `expected.txt`.

## What was fixed

- The JavaScript script now reads each payment line, rather than mistakenly treating each line's position as the payment.
- If a line contains broken JSON, the script skips that unreadable line and continues with the remaining lines. It cannot recover payment details that are missing from a broken line.
- If a transaction has multiple attempts, only its latest attempt by timestamp is used. It counts as collected only if that attempt succeeded.
- Amounts with commas, such as `"3,218.81"`, are now read correctly.
- The script checks its successful-payment count against `expected.txt` before printing the final code.

## How the data works

- Each line is one event: `txn_id`, `status` (`success`, `failed` or `pending`), `amount` in naira, `currency`, and `ts` (when it happened, UTC).
- A payment can be attempted more than once. Every attempt has the same `txn_id`. Only the latest attempt for each `txn_id` counts.
- A payment counts as collected only if its latest attempt is `success`.
- The export comes from a production system and isn't perfectly clean. Ignore lines that can't be read, and events without a `txn_id`. Every other event is valid and must be counted correctly.
- `expected.txt` holds the number of successful payments the finance team counted by hand. The script checks itself against it.

## What to submit

1. Fork this repo, fix the script, and commit your fix to your fork.
2. Run it. Paste the code it prints into the form.
3. Paste the link to your fork into the form.
