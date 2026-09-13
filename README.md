# snaggahub

One page that shows where every project is at. Each project has a `STATUS.md`;
`build.py` turns them into `docs/index.html`; GitHub Pages serves it at a fixed link.

## Folder layout

```
snaggahub/
  build.py                       # generates the dashboard
  docs/index.html                # the dashboard (generated — don't edit by hand)
  projects/
    planr/STATUS.md
    loose-threads/STATUS.md
    pinnacle-enterprises/STATUS.md
  cowork-weekly-task.md          # prompt for the Cowork scheduled task
  CLAUDE-md-snippet.md           # paste into each code repo's CLAUDE.md
```

Add a project: create `projects/<slug>/STATUS.md` in the same format. Rebuild. Done.

## One-time setup (about 10 minutes)

1. Move this folder somewhere permanent, e.g. `~/Business/snaggahub`.
2. Create an empty **public** repo on GitHub called `snaggahub`.
3. In Terminal:
   ```
   cd ~/Business/snaggahub
   git init && git add . && git commit -m "snaggahub"
   git branch -M main
   git remote add origin git@github.com:YOUR_GITHUB_USERNAME/snaggahub.git
   git push -u origin main
   ```
4. On GitHub: repo → Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, folder `/docs` → Save.
5. Your link is `https://YOUR_GITHUB_USERNAME.github.io/snaggahub/`. Bookmark it on your phone.

Public repo means anyone with the link can read it. Keep numbers you'd rather not
share (revenue, ABN) out of STATUS.md, or make the repo private and pay for
GitHub Pro (private Pages).

## Updating

Manually:
```
cd ~/Business/snaggahub
python3 build.py
git add . && git commit -m "status $(date +%F)" && git push
```

Automatically: give Cowork the `cowork-weekly-task.md` prompt as a scheduled task,
and paste `CLAUDE-md-snippet.md` into each code repo's `CLAUDE.md` so Claude Code
updates its project's STATUS.md at the end of every session.

## STATUS.md format

```
---
name: Planr
tagline: one line
stage: short phrase shown next to the health dot
health: green | amber | red
updated: YYYY-MM-DD
owner_tool: where the work happens
next: the single most important next action (shown large)
---
## Now
- bullets
## Blocked
- bullets
## Done recently
- bullets
## Numbers
- Metric: value
## Later
- bullets
```
Health rule: green = moving, nothing waiting on you; amber = needs a decision or
a push; red = stuck for more than a week.
