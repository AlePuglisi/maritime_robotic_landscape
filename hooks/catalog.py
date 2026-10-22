"""MkDocs hook that renders data/catalog.yml into the site's package tables.

Replaces the hand-edited markdown tables and the regex date updater that
rewrote them in place. Curators edit one YAML file; activity comes from
data/repo_status.yml, which only scripts/update_repo_status.py writes. Every
table on every page and the interactive catalog therefore agree by
construction.

The parsing, classification, and rendering below are plain functions with
no MkDocs dependency, so tests/test_catalog.py can exercise them without a
build. The ``on_*`` functions at the bottom are the MkDocs entry points and
only forward to them.
"""

from __future__ import annotations

import html
import json
import logging
import re
import shlex
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# Must live under "mkdocs." or `mkdocs build --strict` does not count our
# warnings, and a bad catalog entry would ship silently.
logger = logging.getLogger("mkdocs.hooks.catalog")

# Activity windows, in days since the last commit on the checked branch.
# 12 months matches the "maintained" bar most ROS users apply when choosing
# a driver; 3 years is roughly one ROS 2 LTS cycle.
ACTIVE_WINDOW_DAYS = 365
QUIET_WINDOW_DAYS = 3 * 365

# Placeholders are HTML comments so a page still renders cleanly if the hook
# is ever disabled:
#
#   <!-- catalog:table category=simulation -->
#   <!-- catalog:table names="VRX|Stonefish" -->
#   <!-- catalog:explorer -->
#   <!-- catalog:stats -->
#        ^kind         ^args (shell-style key=value, quotes for spaces)
_PLACEHOLDER_RE = re.compile(r"<!--\s*catalog:(\w+)\s*(.*?)\s*-->")

ROS_LABELS = {"ros2": "ROS 2", "ros1": "ROS 1", "none": "Non-ROS"}
VEHICLE_LABELS = {"usv": "USV", "auv": "AUV", "rov": "ROV", "glider": "Glider", "any": "Any"}
STATUS_LABELS = {
    "active": "Active",
    "quiet": "Low activity",
    "dormant": "Dormant",
    "archived": "Archived",
    "unknown": "Unknown",
}
REQUIRED_FIELDS = ("name", "category", "description", "ros", "vehicles")

# Fields the explorer needs; everything else stays out of the page payload.
_EXPLORER_FIELDS = ("name", "repo", "url", "category", "ros", "vehicles", "maintainer",
                    "description", "tags", "note", "status", "last_commit", "branch")

# Filled by on_config, read by the page hooks. MkDocs runs hooks in one
# process per build, so a module-level cache is safe.
_catalog: dict[str, Any] = {}


# ─────────────────────────────────────────────────────────────────────
# Loading and classification
# ─────────────────────────────────────────────────────────────────────

def classify_activity(status: dict[str, Any], today: date) -> tuple[str, str | None]:
    """Map a repo_status.yml record to an activity label and its commit date.

    Archived wins over any date: a read-only repository is not maintained,
    however recent its last commit.
    """
    last = status.get("last_commit")
    if status.get("archived"):
        return "archived", str(last) if last else None
    if not last:
        return "unknown", None
    age_days = (today - date.fromisoformat(str(last))).days
    if age_days <= ACTIVE_WINDOW_DAYS:
        return "active", str(last)
    if age_days <= QUIET_WINDOW_DAYS:
        return "quiet", str(last)
    return "dormant", str(last)


def load_catalog(root: Path, *, today: date | None = None) -> dict[str, Any]:
    """Read the curated catalog and merge in repository activity.

    Invalid entries are logged and dropped rather than raised, so one bad
    pull request cannot take the whole site down; --strict still fails CI
    on the warning.

    Args:
        root: Repository root (the directory holding mkdocs.yml).
        today: Reference date for the activity windows. Defaults to the
            current UTC date; tests pass a fixed one.

    Returns:
        ``{"categories": {...}, "packages": [...]}`` where every package
        carries ``status``, ``last_commit``, and ``branch``.
    """
    today = today or datetime.now(timezone.utc).date()
    catalog = yaml.safe_load((root / "data" / "catalog.yml").read_text())
    status_path = root / "data" / "repo_status.yml"
    repo_status: dict[str, Any] = {}
    if status_path.exists():
        repo_status = (yaml.safe_load(status_path.read_text()) or {}).get("repos") or {}

    categories = catalog["categories"]
    packages = []
    for pkg in catalog["packages"]:
        missing = [key for key in REQUIRED_FIELDS if not pkg.get(key)]
        if not (pkg.get("repo") or pkg.get("url")):
            missing.append("repo or url")
        if missing:
            logger.warning("catalog: entry %r is missing %s", pkg.get("name"), ", ".join(missing))
            continue
        if pkg["category"] not in categories:
            logger.warning("catalog: entry %r has category %r, expected one of %s",
                           pkg["name"], pkg["category"], ", ".join(categories))
            continue
        rec = repo_status.get(pkg.get("status_from") or pkg.get("repo"), {})
        state, last = classify_activity(rec, today)
        packages.append({**pkg, "status": state, "last_commit": last,
                         "branch": rec.get("branch") or pkg.get("branch")})
    return {"categories": categories, "packages": packages}


def parse_placeholder_args(raw: str) -> dict[str, str]:
    """Split ``category=simulation names="A|B"`` into a dict; bare words are ignored."""
    return dict(part.split("=", 1) for part in shlex.split(raw) if "=" in part)


def select_packages(packages: list[dict[str, Any]], args: dict[str, str],
                    *, where: str = "page") -> list[dict[str, Any]]:
    """Pick table rows by ``category=`` or by an ordered ``names=`` list.

    ``names`` keeps the order the page author wrote, because comparison
    tables read best in a deliberate order, not alphabetically.
    """
    if "category" in args:
        return [p for p in packages if p["category"] == args["category"]]
    if "names" in args:
        by_name = {p["name"]: p for p in packages}
        wanted = [n.strip() for n in args["names"].split("|")]
        for name in wanted:
            if name not in by_name:
                logger.warning("catalog: %s asks for unknown entry %r", where, name)
        return [by_name[n] for n in wanted if n in by_name]
    logger.warning("catalog: table placeholder in %s needs category= or names=", where)
    return []


# ─────────────────────────────────────────────────────────────────────
# Rendering
# ─────────────────────────────────────────────────────────────────────

def render_table(packages: list[dict[str, Any]]) -> str:
    """Markdown table of packages, wrapped so extra.css can size its columns."""
    rows = [
        "| Project | What it does | ROS | Vehicles | Activity |",
        "|---|---|---|---|---|",
    ]
    for pkg in packages:
        desc = _escape_cell(pkg["description"])
        if pkg.get("note"):
            desc += f" <em>{_escape_cell(pkg['note'])}</em>"
        rows.append(
            f"| {_project_cell(pkg)} <br><small>{_escape_cell(pkg.get('maintainer', ''))}</small> "
            f"| {desc} "
            f"| {_badges(pkg['ros'], ROS_LABELS, 'ros')} "
            f"| {_badges(pkg['vehicles'], VEHICLE_LABELS, 'veh')} "
            f"| {_status_badge(pkg)} |"
        )
    return '\n\n<div class="mrl-table" markdown>\n\n' + "\n".join(rows) + "\n\n</div>\n\n"


def render_explorer(catalog: dict[str, Any]) -> str:
    """Explorer markup plus its JSON payload; docs/javascripts/catalog.js draws the cards."""
    payload = json.dumps(
        {
            "categories": {k: v["title"] for k, v in catalog["categories"].items()},
            "packages": [{k: p.get(k) for k in _EXPLORER_FIELDS} for p in catalog["packages"]],
        },
        ensure_ascii=False,
    )
    # A literal "</script>" in a description would end the script block early.
    payload = payload.replace("</", "<\\/")
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


def render_stats(packages: list[dict[str, Any]]) -> str:
    """Summary tiles for the home and software overview pages."""
    counts = {
        "Projects tracked": len(packages),
        "Support ROS 2": sum("ros2" in p["ros"] for p in packages),
        "Simulators": sum(p["category"] == "simulation" for p in packages),
        "Active in last 12 months": sum(p["status"] == "active" for p in packages),
    }
    tiles = "\n".join(
        f'  <div class="mrl-stat"><span class="mrl-stat__value">{value}</span>'
        f'<span class="mrl-stat__label">{html.escape(label)}</span></div>'
        for label, value in counts.items()
    )
    return f'\n\n<div class="mrl-stats">\n{tiles}\n</div>\n\n'


def expand_placeholders(markdown: str, catalog: dict[str, Any], *, where: str = "page") -> str:
    """Replace every catalog placeholder in a page with its rendered block."""

    def _replace(match: re.Match[str]) -> str:
        kind, args = match.group(1), parse_placeholder_args(match.group(2))
        if kind == "table":
            return render_table(select_packages(catalog["packages"], args, where=where))
        if kind == "explorer":
            return render_explorer(catalog)
        if kind == "stats":
            return render_stats(catalog["packages"])
        logger.warning("catalog: unknown placeholder %r in %s", kind, where)
        return ""

    return _PLACEHOLDER_RE.sub(_replace, markdown)


def _badges(values: list[str], labels: dict[str, str], css: str) -> str:
    return " ".join(f'<span class="mrl-badge mrl-{css}-{v}">{labels.get(v, v)}</span>' for v in values)


def _status_badge(pkg: dict[str, Any]) -> str:
    label = STATUS_LABELS[pkg["status"]]
    css = f"mrl-status mrl-status-{pkg['status']}"
    if not pkg["last_commit"]:
        return f'<span class="{css}">{label}</span>'
    stamp = date.fromisoformat(pkg["last_commit"]).strftime("%b %Y")
    title = f"Last commit {pkg['last_commit']} on {pkg.get('branch') or 'default branch'}"
    return f'<span class="{css}" title="{title}">{label}</span><br><small>{stamp}</small>'


def _project_cell(pkg: dict[str, Any]) -> str:
    cell = f"**[{pkg['name']}]({pkg.get('repo') or pkg.get('url')})**"
    if pkg.get("url") and pkg.get("repo"):
        cell += f' <a href="{pkg["url"]}" title="Website or documentation">:material-book-open-variant:</a>'
    return cell


def _escape_cell(text: Any) -> str:
    # A bare "|" would split the markdown table cell.
    return str(text).replace("|", "\\|").replace("\n", " ")


# ─────────────────────────────────────────────────────────────────────
# MkDocs entry points
# ─────────────────────────────────────────────────────────────────────

def on_config(config):
    _catalog.update(load_catalog(Path(config["config_file_path"]).parent))
    logger.info("catalog: loaded %d packages", len(_catalog["packages"]))
    return config


def on_page_markdown(markdown, page, config, files):
    return expand_placeholders(markdown, _catalog, where=page.file.src_uri)


def on_post_build(config):
    out = Path(config["site_dir"]) / "catalog.json"
    out.write_text(json.dumps(_catalog["packages"], indent=2, ensure_ascii=False))
