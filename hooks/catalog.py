"""
MkDocs hook: render the software catalog (data/catalog.yml) into pages.

Placeholders (HTML comments, so they stay invisible if the hook is disabled):

    <!-- catalog:table category=simulation -->   Table of one category
    <!-- catalog:table names="VRX|Stonefish" --> Table of named entries, in order
    <!-- catalog:explorer -->                    Interactive, filterable catalog
    <!-- catalog:stats -->                       Summary tiles

The hook also writes catalog.json to the site root for reuse by other tools.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import logging
import re
import shlex
from pathlib import Path

import yaml

log = logging.getLogger("mkdocs.hooks.catalog")

PLACEHOLDER = re.compile(r"<!--\s*catalog:(\w+)\s*(.*?)\s*-->")
ROS_LABELS = {"ros2": "ROS 2", "ros1": "ROS 1", "none": "Non-ROS"}
VEHICLE_LABELS = {"usv": "USV", "auv": "AUV", "rov": "ROV", "glider": "Glider", "any": "Any"}
STATUS_LABELS = {
    "active": "Active",
    "quiet": "Low activity",
    "dormant": "Dormant",
    "archived": "Archived",
    "unknown": "Unknown",
}
REQUIRED = ("name", "category", "description", "ros", "vehicles")

_data: dict = {}


def _activity(status: dict, today: dt.date) -> tuple[str, str | None]:
    """Classify activity from the last commit date relative to the build date."""
    if status.get("archived"):
        return "archived", status.get("last_commit")
    last = status.get("last_commit")
    if not last:
        return "unknown", None
    age_days = (today - dt.date.fromisoformat(str(last))).days
    if age_days <= 365:
        return "active", last
    if age_days <= 3 * 365:
        return "quiet", last
    return "dormant", last


def on_config(config):
    root = Path(config["config_file_path"]).parent
    catalog = yaml.safe_load((root / "data" / "catalog.yml").read_text())
    status_file = root / "data" / "repo_status.yml"
    status = {}
    if status_file.exists():
        status = (yaml.safe_load(status_file.read_text()) or {}).get("repos", {}) or {}

    categories = catalog["categories"]
    today = dt.date.today()
    packages = []
    for pkg in catalog["packages"]:
        missing = [key for key in REQUIRED if not pkg.get(key)]
        if missing or not (pkg.get("repo") or pkg.get("url")):
            log.warning("catalog: entry %r is missing %s", pkg.get("name"), missing or ["repo/url"])
            continue
        if pkg["category"] not in categories:
            log.warning("catalog: entry %r has unknown category %r", pkg["name"], pkg["category"])
            continue
        repo_status = status.get(pkg.get("status_from") or pkg.get("repo"), {})
        state, last = _activity(repo_status, today)
        packages.append({
            **pkg,
            "status": state,
            "last_commit": str(last) if last else None,
            "branch": repo_status.get("branch") or pkg.get("branch"),
        })
    _data.update(categories=categories, packages=packages)
    return config


# ── Rendering helpers ─────────────────────────────────────────────────────

def _badges(values, labels, css):
    return " ".join(
        f'<span class="mrl-badge mrl-{css}-{v}">{labels.get(v, v)}</span>' for v in values
    )


def _status_badge(pkg):
    label = STATUS_LABELS[pkg["status"]]
    if pkg["last_commit"]:
        stamp = dt.date.fromisoformat(pkg["last_commit"]).strftime("%b %Y")
        title = f"Last commit {pkg['last_commit']} on {pkg.get('branch') or 'default branch'}"
        return (f'<span class="mrl-status mrl-status-{pkg["status"]}" title="{title}">'
                f'{label}</span><br><small>{stamp}</small>')
    return f'<span class="mrl-status mrl-status-{pkg["status"]}">{label}</span>'


def _project_cell(pkg):
    main = pkg.get("repo") or pkg.get("url")
    cell = f"**[{pkg['name']}]({main})**"
    if pkg.get("url") and pkg.get("repo"):
        cell += f' <a href="{pkg["url"]}" title="Website or documentation">:material-book-open-variant:</a>'
    return cell


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def _table(pkgs):
    rows = [
        "| Project | What it does | ROS | Vehicles | Activity |",
        "|---|---|---|---|---|",
    ]
    for pkg in pkgs:
        desc = _cell(pkg["description"])
        if pkg.get("note"):
            desc += f" <em>{_cell(pkg['note'])}</em>"
        rows.append(
            f"| {_project_cell(pkg)} <br><small>{_cell(pkg.get('maintainer', ''))}</small> "
            f"| {desc} "
            f"| {_badges(pkg['ros'], ROS_LABELS, 'ros')} "
            f"| {_badges(pkg['vehicles'], VEHICLE_LABELS, 'veh')} "
            f"| {_status_badge(pkg)} |"
        )
    return "\n".join(rows)


def _render_table(args, page):
    pkgs = _data["packages"]
    if "category" in args:
        selected = [p for p in pkgs if p["category"] == args["category"]]
    elif "names" in args:
        by_name = {p["name"]: p for p in pkgs}
        wanted = [n.strip() for n in args["names"].split("|")]
        for name in wanted:
            if name not in by_name:
                log.warning("catalog: %s asks for unknown entry %r", page.file.src_uri, name)
        selected = [by_name[n] for n in wanted if n in by_name]
    else:
        log.warning("catalog: table placeholder in %s needs category= or names=", page.file.src_uri)
        return ""
    if not selected:
        log.warning("catalog: table placeholder in %s matched nothing", page.file.src_uri)
    return '\n\n<div class="mrl-table" markdown>\n\n' + _table(selected) + "\n\n</div>\n\n"


def _render_explorer():
    payload = json.dumps(
        {
            "categories": {k: v["title"] for k, v in _data["categories"].items()},
            "packages": [
                {k: p.get(k) for k in (
                    "name", "repo", "url", "category", "ros", "vehicles", "maintainer",
                    "description", "tags", "note", "status", "last_commit", "branch")}
                for p in _data["packages"]
            ],
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")
    return f"""

<div class="mrl-explorer" data-mrl-explorer>
  <div class="mrl-explorer__controls">
    <label class="mrl-search">
      <span class="mrl-sr">Search the catalog</span>
      <input type="search" data-mrl-q placeholder="Search name, purpose, sensor, or tag (for example: dvl, ardusub, sonar)" autocomplete="off">
    </label>
    <div class="mrl-filter-row">
      <select data-mrl-cat aria-label="Category"><option value="">All categories</option></select>
      <div class="mrl-chips" data-mrl-ros role="group" aria-label="ROS version"></div>
      <div class="mrl-chips" data-mrl-veh role="group" aria-label="Vehicle type"></div>
      <label class="mrl-toggle"><input type="checkbox" data-mrl-active> Hide dormant and archived</label>
    </div>
  </div>
  <p class="mrl-count" data-mrl-count aria-live="polite"></p>
  <div class="mrl-grid" data-mrl-grid></div>
  <noscript><p>The interactive catalog needs JavaScript. The same entries appear as tables on each Software page.</p></noscript>
</div>
<script type="application/json" id="mrl-catalog-data">{payload}</script>

"""


def _render_stats():
    pkgs = _data["packages"]
    counts = {
        "Projects tracked": len(pkgs),
        "Support ROS 2": sum("ros2" in p["ros"] for p in pkgs),
        "Simulators": sum(p["category"] == "simulation" for p in pkgs),
        "Active in last 12 months": sum(p["status"] == "active" for p in pkgs),
    }
    tiles = "\n".join(
        f'  <div class="mrl-stat"><span class="mrl-stat__value">{value}</span>'
        f'<span class="mrl-stat__label">{html.escape(label)}</span></div>'
        for label, value in counts.items()
    )
    return f'\n\n<div class="mrl-stats">\n{tiles}\n</div>\n\n'


def on_page_markdown(markdown, page, config, files):
    def replace(match):
        kind, raw_args = match.group(1), match.group(2)
        args = dict(part.split("=", 1) for part in shlex.split(raw_args) if "=" in part)
        if kind == "table":
            return _render_table(args, page)
        if kind == "explorer":
            return _render_explorer()
        if kind == "stats":
            return _render_stats()
        log.warning("catalog: unknown placeholder %r in %s", kind, page.file.src_uri)
        return ""

    return PLACEHOLDER.sub(replace, markdown)


def on_post_build(config):
    out = Path(config["site_dir"]) / "catalog.json"
    out.write_text(json.dumps(_data["packages"], indent=2, ensure_ascii=False))
