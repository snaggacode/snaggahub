# Cowork scheduled task — "Refresh snaggahub"

Schedule: every Monday 6:00 AM AWST (adjust to your swing/roster).
Folder to give Cowork access to: ~/Business (contains snaggahub/).
Connectors needed: Shopify, Google Drive, GitHub (optional — otherwise it will ask you to push).

## Prompt

You maintain my project dashboard in ~/Business/snaggahub. Do the following, then stop.

1. Read every projects/*/STATUS.md.
2. Refresh the "Numbers" section of each project from live sources where you can:
   - Loose Threads: use the Shopify connector to get orders and revenue for the last 7 days and total to date. Note the plan and whether the store is published.
   - Planr: check ~/Business/Planr for any exported RevenueCat/App Store Connect CSVs and update paying coaches, active clients, MRR. If none, leave the numbers as they are and say so.
   - Pinnacle Enterprises: scan ~/Business/PinnacleEnterprises and Google Drive for anything new from Lewis or the ATO in the last 7 days; add anything relevant to "Now" or "Blocked".
3. For each project, set `updated` to today and re-evaluate `health` against the rule in README.md. If something has been in "Blocked" for more than 14 days, mark it red and put it first in "Now".
4. Do not invent progress. Only change "Now", "Blocked" and "Done recently" based on evidence in files, connectors, or the notes I've left in ~/Business/inbox.md (if it exists — clear it after you've folded its contents in).
5. Run `python3 build.py`, then `git add . && git commit -m "weekly refresh <date>" && git push`.
6. Reply with a five-line summary: one line per project (health + next), one line for anything you couldn't verify, one line confirming the push. Nothing else.
