---
title: Contributing
description: How to correct, extend, and maintain the Maritime Robotics Landscape website and its package catalog.
---

# Contributing

Contributions are welcome, from a typo fix to a new page. The site is built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) from the [ros-maritime/maritime_robotic_landscape](https://github.com/ros-maritime/maritime_robotic_landscape) repository, under the CC BY-SA 4.0 license.

## Quick edits

1. Click :material-pencil: at the top of the page you want to change.
2. Edit the Markdown in the GitHub editor.
3. Propose the change; GitHub creates a branch and a pull request for you.

A preview of the site is built for every pull request.

## Add or correct a package

All package tables and the [catalog](catalog.md) come from one file: [`data/catalog.yml`](https://github.com/ros-maritime/maritime_robotic_landscape/blob/main/data/catalog.yml). Add an entry in the right section:

```yaml
  - name: my_dvl_driver                       # display name
    repo: https://github.com/me/my_dvl_driver # source repository
    url: https://me.github.io/my_dvl_driver   # optional: docs or website
    branch: jazzy                             # optional: branch to check for activity
    category: drivers                         # see `categories` at the top of the file
    ros: [ros2]                               # ros2, ros1, none
    vehicles: [rov, auv]                      # usv, auv, rov, glider, any
    maintainer: My Lab (University of X)
    description: ROS 2 driver for the Example DVL-100, publishing marine_acoustic_msgs/Dvl and TwistWithCovarianceStamped.
    tags: [dvl, example]
```

Rules for entries:

- **Be factual.** Describe what the project does and which versions it supports, with information from its README or documentation. No marketing words.
- **One or two sentences.** Longer explanations belong on the topic pages.
- **Do not add activity data.** The last-commit date and archived state are written to `data/repo_status.yml` by a weekly workflow. Never edit that file by hand.

To show a table of entries on a page, put a placeholder comment in the Markdown. The supported forms are listed at the top of [`hooks/catalog.py`](https://github.com/ros-maritime/maritime_robotic_landscape/blob/main/hooks/catalog.py): a table for one category, a table of named entries, the explorer, and the summary tiles.

## Writing guidelines

- **Audience**: engineers and students who build marine robots with ROS. Explain marine terms the first time, and link to the [Glossary](glossary.md).
- **Accuracy first**: link to the source of each fact (README, documentation, datasheet, paper). If you are not sure, say so, or leave it out. Do not invent example numbers that look like specifications.
- **Plain, simple language**: short sentences, active voice, one instruction per step. Prefer tables for comparisons.
- **Code must be correct**: test code examples, and mark placeholder names clearly.
- **Diagrams**: use Mermaid code blocks for flows and architectures; they follow the light and dark themes. Use inline SVG with the `mrl-svg-*` classes for drawings (see the frame diagram in [Conventions](conventions.md)).
- **Acronyms**: add new ones to `includes/abbreviations.md`, so readers see the definition when they hover.

## Local preview

```bash
git clone https://github.com/ros-maritime/maritime_robotic_landscape.git
cd maritime_robotic_landscape
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve        # open http://127.0.0.1:8000
```

Before you open a pull request, run the tests and a strict build. The tests check the catalog data and run the code examples published on the Conventions and Control pages; the strict build fails on broken internal links and invalid catalog entries:

```bash
pip install -r requirements-test.txt
python -m pytest -q tests
mkdocs build --strict
```

To refresh package activity locally (optional; the weekly workflow does this):

```bash
python scripts/update_repo_status.py   # set GITHUB_TOKEN to also read archived flags
```

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | Pages (Markdown), styles, scripts, and images |
| `data/catalog.yml` | Curated package catalog |
| `data/repo_status.yml` | Generated activity data (do not edit) |
| `hooks/catalog.py` | Build hook that renders catalog tables and the explorer |
| `includes/abbreviations.md` | Acronym tooltips used on every page |
| `overrides/` | Theme overrides (analytics) |
| `scripts/update_repo_status.py` | Weekly activity refresh |
| `tests/` | Tests for the catalog hook, the status script, and the published code examples |
| `.github/workflows/` | Build, PR preview, and weekly refresh workflows |
