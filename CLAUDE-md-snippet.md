# Paste this into the CLAUDE.md of each code repo (Planr, grind-season-theme, etc.)

## Project status file
This project's status lives in ~/Business/snaggahub/projects/<SLUG>/STATUS.md
(replace <SLUG> with planr, loose-threads, …).

At the end of every working session, before the final message:
1. Update that STATUS.md — move finished items to "Done recently" (keep at most 6),
   rewrite "Now" to reflect what's actually in progress, update "Blocked",
   set `updated` to today's date, and set `next` to the single most important next action.
2. Run `python3 ~/Business/snaggahub/build.py`.
3. Run `cd ~/Business/snaggahub && git add . && git commit -m "<project>: <one line>" && git push`.
Do this without being asked. Don't add bullets for work that wasn't done.
