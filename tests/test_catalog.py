"""Tests for the catalog hook, the status script, and the code published in the docs.

Everything here runs without a network, a MkDocs build, or ROS: the hook and
script keep their logic in plain functions for exactly this reason. The
doc-example tests execute the code blocks readers copy from conventions.md and
control.md, so a page cannot drift from the numbers it quotes.
"""

from __future__ import annotations

import importlib.util
import logging
import math
import re
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


catalog = _load_module("catalog_hook", ROOT / "hooks" / "catalog.py")
status = _load_module("update_repo_status", ROOT / "scripts" / "update_repo_status.py")


def _doc_code_block(page: str, title: str) -> str:
    """Return the fenced python block with the given title from a docs page."""
    text = (ROOT / "docs" / page).read_text()
    match = re.search(rf'```python title="{re.escape(title)}[^"]*"\n(.*?)```', text, re.S)
    assert match, f"no python block titled {title!r} in docs/{page}"
    return match.group(1)


# ─────────────────────────────────────────────────────────────────────
# Activity classification
# ─────────────────────────────────────────────────────────────────────

TODAY = date(2026, 10, 22)


def test_archived_wins_over_recent_commit():
    assert catalog.classify_activity({"archived": True, "last_commit": "2026-10-01"}, TODAY) == (
        "archived", "2026-10-01")


def test_activity_window_edges():
    # 365 days is still active; one more day drops to low activity.
    assert catalog.classify_activity({"last_commit": "2025-10-22"}, TODAY)[0] == "active"
    assert catalog.classify_activity({"last_commit": "2025-10-21"}, TODAY)[0] == "quiet"
    assert catalog.classify_activity({"last_commit": "2023-10-23"}, TODAY)[0] == "quiet"
    assert catalog.classify_activity({"last_commit": "2020-06-15"}, TODAY)[0] == "dormant"


def test_missing_date_is_unknown_not_dormant():
    # An unreachable host (git.whoi.edu from some runners) must not look abandoned.
    assert catalog.classify_activity({}, TODAY) == ("unknown", None)


# ─────────────────────────────────────────────────────────────────────
# Placeholders and rendering
# ─────────────────────────────────────────────────────────────────────

def test_placeholder_args_keep_quoted_names_with_spaces():
    args = catalog.parse_placeholder_args('names="POSIM (DAVE for ROS 2)|VRX" stray')
    assert args == {"names": "POSIM (DAVE for ROS 2)|VRX"}


def test_names_selection_keeps_author_order_and_warns_on_typo(caplog):
    pkgs = [{"name": "A", "category": "x"}, {"name": "B", "category": "x"}]
    with caplog.at_level(logging.WARNING, logger="mkdocs.hooks.catalog"):
        picked = catalog.select_packages(pkgs, {"names": "B|Typo|A"}, where="test.md")
    assert [p["name"] for p in picked] == ["B", "A"]
    assert "Typo" in caplog.text


def test_pipe_in_description_does_not_split_table_cell():
    pkg = {"name": "x", "repo": "https://example.org/x", "description": "a | b",
           "maintainer": "m", "ros": ["ros2"], "vehicles": ["any"],
           "status": "unknown", "last_commit": None}
    row = next(line for line in catalog.render_table([pkg]).splitlines() if line.startswith("| **[x]"))
    assert row.count(" | ") == 4 and "a \\| b" in row


def test_explorer_payload_cannot_close_its_script_tag():
    cat = {"categories": {"tools": {"title": "Tools"}},
           "packages": [{"name": "x", "description": "evil </script> text"}]}
    block = catalog.render_explorer(cat)
    assert block.count("</script>") == 1


def test_unknown_placeholder_renders_nothing(caplog):
    with caplog.at_level(logging.WARNING, logger="mkdocs.hooks.catalog"):
        out = catalog.expand_placeholders("a<!-- catalog:bogus -->b", {"packages": []})
    assert out == "ab" and "bogus" in caplog.text


# ─────────────────────────────────────────────────────────────────────
# The real catalog data
# ─────────────────────────────────────────────────────────────────────

def test_every_catalog_entry_is_valid(caplog):
    with caplog.at_level(logging.WARNING, logger="mkdocs.hooks.catalog"):
        loaded = catalog.load_catalog(ROOT, today=TODAY)
    assert caplog.text == ""
    raw = (ROOT / "data" / "catalog.yml").read_text()
    assert len(loaded["packages"]) == raw.count("\n  - name: ")


def test_catalog_names_are_unique():
    names = [p["name"] for p in catalog.load_catalog(ROOT, today=TODAY)["packages"]]
    assert len(names) == len(set(names))


def test_every_probed_repo_has_a_status_record():
    pkgs = catalog.load_catalog(ROOT, today=TODAY)["packages"]
    recorded = status.yaml.safe_load((ROOT / "data" / "repo_status.yml").read_text())["repos"]
    missing = sorted(set(status.collect_targets(pkgs)) - set(recorded))
    assert missing == [], f"run scripts/update_repo_status.py; no record for {missing}"


# ─────────────────────────────────────────────────────────────────────
# Status script
# ─────────────────────────────────────────────────────────────────────

def test_symref_regex_reads_default_branch_from_ls_remote():
    out = ("ref: refs/heads/jazzy\tHEAD\n"
           "7609d1bd90ce7edb29d040a082f949e8b089c864\tHEAD\n")
    assert status._SYMREF_RE.search(out).group(1) == "jazzy"


def test_branch_override_applies_only_to_own_repo():
    pkgs = [
        {"name": "a", "repo": "https://h/a", "branch": "ros2"},
        {"name": "b", "repo": "https://h/b", "status_from": "https://h/c"},
        {"name": "c", "repo": "https://h/c", "branch": "jazzy"},
    ]
    assert status.collect_targets(pkgs) == {"https://h/a": "ros2", "https://h/c": "jazzy"}


def test_status_from_alone_probes_default_branch():
    pkgs = [{"name": "b", "repo": "https://h/b", "status_from": "https://h/c"}]
    assert status.collect_targets(pkgs) == {"https://h/c": None}


# ─────────────────────────────────────────────────────────────────────
# Code published in the docs
# ─────────────────────────────────────────────────────────────────────

np = pytest.importorskip("numpy")


def _ned_frd_to_enu_flu():
    ns: dict = {}
    exec(_doc_code_block("conventions.md", "ned_to_enu.py"), ns)
    return ns


def _euler_from_quat(q):
    w, x, y, z = q
    roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch = math.asin(max(-1.0, min(1.0, 2 * (w * y - z * x))))
    yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return np.degrees([roll, pitch, yaw])


def _quat_from_euler(roll, pitch, yaw):
    cr, sr = math.cos(roll / 2), math.sin(roll / 2)
    cp, sp = math.cos(pitch / 2), math.sin(pitch / 2)
    cy, sy = math.cos(yaw / 2), math.sin(yaw / 2)
    return np.array([cr * cp * cy + sr * sp * sy, sr * cp * cy - cr * sp * sy,
                     cr * sp * cy + sr * cp * sy, cr * cp * sy - sr * sp * cy])


@pytest.mark.parametrize("roll, pitch, heading", [(0, 0, 0), (0, 0, 90), (0, 0, 30), (5, -8, 225)])
def test_conventions_page_heading_becomes_enu_yaw(roll, pitch, heading):
    # The page promises: roll keeps its sign, pitch flips, yaw = 90 - heading.
    ns = _ned_frd_to_enu_flu()
    q_ned = _quat_from_euler(*np.radians([roll, pitch, heading]))
    r, p, y = _euler_from_quat(ns["ned_frd_to_enu_flu"](q_ned))
    expected_yaw = (90 - heading + 180) % 360 - 180
    assert (r, p, y) == pytest.approx((roll, -pitch, expected_yaw), abs=1e-9)


def test_conventions_page_ned_vector_maps_to_enu():
    assert _ned_frd_to_enu_flu()["ned_to_enu"](1.0, 2.0, 3.0) == (2.0, 1.0, -3.0)


def test_control_page_allocation_numbers_match_comments():
    ns: dict = {}
    exec(_doc_code_block("control.md", "allocation_example.py"), ns)
    T = ns["T"]
    assert ns["f"] == pytest.approx([6.53, 14.69, -6.53, -14.69], abs=0.01)
    # The page rounds forces to one decimal, so match that precision.
    assert T @ ns["f_clip"] == pytest.approx([23.4, 0.0, 1.28], abs=0.05)
    assert T @ ns["f_scaled"] == pytest.approx([20.4, 0.0, 2.04], abs=0.05)
