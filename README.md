# Maritime Robotics Landscape

A community reference for ROS-based maritime robotics: software, simulators, drivers, frame conventions, hardware, field operations, datasets, and events. Curated by the ROS Maritime Community Working Group.

**Website: <https://ros-maritime.oceansoft.org/>**

## What is on the site

| Section | Contents |
|---|---|
| Start here | Getting started, learning path and tutorials, FAQ, glossary |
| Software | Searchable package catalog, autonomy frameworks, simulation, drivers and interfaces, frames and conventions, control, localization, perception, communication, tools, integration examples, quick reference |
| Hardware | Vehicle types; sensors and components with ROS 2 driver status |
| Field operations | Checklists, power budgets, failure modes, maintenance |
| Datasets | Sonar, underwater imagery, navigation, USV perception, ocean data |
| Community | Working group meetings and channels, events and competitions, contributing |

## How it works

- Pages are Markdown in `docs/`, built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
- Every package table and the interactive catalog come from one curated file, [`data/catalog.yml`](data/catalog.yml), rendered by the build hook [`hooks/catalog.py`](hooks/catalog.py).
- A weekly workflow runs [`scripts/update_repo_status.py`](scripts/update_repo_status.py), which reads the latest commit date (and the GitHub archived flag) of each repository and opens a pull request that updates [`data/repo_status.yml`](data/repo_status.yml).
- Every push to `main` builds the site with `mkdocs build --strict` and deploys it to GitHub Pages. Pull requests get a preview build.

## Contributing

Corrections and additions are welcome. Small changes: use the pencil button on any page of the website. Larger changes: see the [Contributing page](https://ros-maritime.oceansoft.org/contributing/) ([source](docs/contributing.md)).

Local preview:

```bash
git clone https://github.com/ros-maritime/maritime_robotic_landscape.git
cd maritime_robotic_landscape
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve            # http://127.0.0.1:8000
mkdocs build --strict   # run before you open a pull request
```

## Community

- **Forum:** [ROS Discourse, Marine Robotics](https://discourse.openrobotics.org/c/community-groups/marine-robotics/36)
- **Chat:** [Zulip, Marine Robotics channel](https://openrobotics.zulipchat.com/#narrow/channel/526058-Marine-Robotics)
- **Meetings:** monthly, announced on Discourse; [agendas and minutes](https://docs.google.com/document/d/1Wnddq4xRXR6HF2XFWeejfUGII_hj7DilKrGcFj1qlEA/edit?usp=drive_link); [calendar invites](https://groups.google.com/g/maritime-robotics-working-group-invites)
- **Project board:** [GitHub Projects](https://github.com/orgs/ros-maritime/projects)

## License

The documentation is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).
