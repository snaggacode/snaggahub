#!/usr/bin/env python3
"""Build docs/index.html from every projects/*/STATUS.md.

Run:  python3 build.py
No dependencies beyond the standard library.
"""
from __future__ import annotations

import datetime as dt
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
PROJECTS = ROOT / "projects"
OUT = ROOT / "docs" / "index.html"

HEALTH_LABEL = {"green": "On track", "amber": "Needs attention", "red": "Stuck"}


def parse_status(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    sections: dict[str, list[str]] = {}
    current = None
    for line in m.group(2).splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif line.startswith("- ") and current:
            sections[current].append(line[2:].strip())
    meta["sections"] = sections
    meta["slug"] = path.parent.name
    return meta


def inline(s: str) -> str:
    s = html.escape(s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


def section_html(title: str, items: list[str]) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{inline(i)}</li>" for i in items)
    return f"<section><h3>{html.escape(title)}</h3><ul>{lis}</ul></section>"


def project_html(p: dict) -> str:
    health = p.get("health", "amber")
    secs = p["sections"]
    order = ["Now", "Blocked", "Done recently", "Numbers", "Later"]
    body = "".join(section_html(t, secs.get(t, [])) for t in order)
    for t, items in secs.items():
        if t not in order:
            body += section_html(t, items)
    return f"""
<article class="project health-{health}" id="{html.escape(p['slug'])}">
  <header>
    <div class="titles">
      <h2>{html.escape(p.get('name', p['slug']))}</h2>
      <p class="tagline">{html.escape(p.get('tagline', ''))}</p>
    </div>
    <div class="state">
      <span class="dot" aria-hidden="true"></span>
      <span>{HEALTH_LABEL.get(health, health)}</span>
      <span class="sep">/</span>
      <span>{html.escape(p.get('stage', ''))}</span>
    </div>
  </header>
  <p class="next"><span class="next-label">Next</span>{html.escape(p.get('next', ''))}</p>
  <div class="body">{body}</div>
  <footer>
    <span>Updated {html.escape(p.get('updated', '?'))}</span>
    <span>{html.escape(p.get('owner_tool', ''))}</span>
  </footer>
</article>"""


CSS = """
:root{
  --bg:#EDF0F2; --panel:#FFFFFF; --ink:#14202B; --muted:#5C6B78; --rule:#D5DBE0;
  --accent:#1D5E8A; --green:#2E7D4F; --amber:#C47A12; --red:#B4331F;
}
*{box-sizing:border-box}
html{font-size:17px}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Instrument Sans","Helvetica Neue",Arial,sans-serif;line-height:1.45}
a{color:var(--accent)}
code{font-family:ui-monospace,Menlo,monospace;font-size:.9em;background:var(--bg);padding:0 .3em;border-radius:3px}
.wrap{max-width:1180px;margin:0 auto;padding:2.5rem 1.5rem 4rem}
.top{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid var(--ink);padding-bottom:.75rem;margin-bottom:2rem}
.top h1{font-size:1.4rem;font-weight:600;letter-spacing:-.01em;margin:0}
.top .built{color:var(--muted);font-size:.9rem}
.summary{display:flex;flex-wrap:wrap;gap:.5rem 2rem;margin:0 0 2.5rem;padding:0;list-style:none;font-size:.95rem}
.summary li{display:flex;align-items:center;gap:.5rem}
.summary a{color:inherit;text-decoration:none;border-bottom:1px solid var(--rule)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:1.25rem;align-items:start}
.project{background:var(--panel);border:1px solid var(--rule);border-top:4px solid var(--rule);padding:1.4rem 1.5rem 1rem}
.project.health-green{border-top-color:var(--green)}
.project.health-amber{border-top-color:var(--amber)}
.project.health-red{border-top-color:var(--red)}
.project header{margin-bottom:1rem}
.project h2{margin:0;font-size:1.55rem;font-weight:600;letter-spacing:-.015em}
.tagline{margin:.15rem 0 0;color:var(--muted);font-size:.92rem}
.state{margin-top:.6rem;font-size:.9rem;display:flex;gap:.45rem;align-items:center;flex-wrap:wrap}
.state .sep{color:var(--rule)}
.dot{width:.6rem;height:.6rem;border-radius:50%;background:var(--rule);display:inline-block}
.health-green .dot{background:var(--green)}
.health-amber .dot{background:var(--amber)}
.health-red .dot{background:var(--red)}
.next{font-size:1.25rem;line-height:1.3;font-weight:500;margin:0 0 1.25rem;padding:.9rem 1rem;background:var(--bg);border-left:3px solid var(--accent)}
.next-label{display:block;font-size:.78rem;font-weight:600;color:var(--accent);margin-bottom:.25rem}
.body section{border-top:1px solid var(--rule);padding:.75rem 0}
.body h3{margin:0 0 .35rem;font-size:.85rem;font-weight:600;color:var(--muted)}
.body ul{margin:0;padding-left:1.1rem}
.body li{margin:.2rem 0;font-size:.95rem}
.project footer{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;border-top:1px solid var(--rule);
  margin-top:.5rem;padding-top:.7rem;color:var(--muted);font-size:.82rem}
.empty{color:var(--muted)}
@media (max-width:600px){html{font-size:16px}.wrap{padding:1.5rem 1rem 3rem}}
@media (prefers-reduced-motion:no-preference){.project{transition:border-color .2s}}
"""


def build() -> None:
    projects = [parse_status(p) for p in sorted(PROJECTS.glob("*/STATUS.md"))]
    # red first, then amber, then green — problems at the top
    rank = {"red": 0, "amber": 1, "green": 2}
    projects.sort(key=lambda p: (rank.get(p.get("health"), 1), p.get("name", "")))

    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%a %d %b %Y, %H:%M AWST")
    summary = "".join(
        f'<li class="health-{p.get("health","amber")}"><span class="dot"></span>'
        f'<a href="#{p["slug"]}">{html.escape(p.get("name", p["slug"]))}</a> — '
        f'{html.escape(p.get("stage",""))}</li>'
        for p in projects
    )
    cards = "".join(project_html(p) for p in projects) or '<p class="empty">No projects yet. Add projects/&lt;name&gt;/STATUS.md and rebuild.</p>'

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>snaggahub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <h1>snaggahub</h1>
    <span class="built">Built {now}</span>
  </div>
  <ul class="summary">{summary}</ul>
  <div class="grid">{cards}</div>
</div>
</body>
</html>
"""
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(projects)} projects)")


if __name__ == "__main__":
    build()
