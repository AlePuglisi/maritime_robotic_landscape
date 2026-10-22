---
title: Package catalog
description: Search and filter open-source maritime robotics software by purpose, ROS version, vehicle type, and activity.
hide:
  - navigation
  - toc
---

# Package catalog

Every open-source project this site tracks, in one place. Type to search names, purposes, and tags, or filter by category, ROS version, and vehicle type. The same data drives the tables on each Software page.

<p class="mrl-legend">
Activity comes from the date of the latest commit on the branch that matters for ROS 2 (usually the default branch) and refreshes every week:
<span class="mrl-status mrl-status-active">Active</span> within 12 months,
<span class="mrl-status mrl-status-quiet">Low activity</span> within 3 years,
<span class="mrl-status mrl-status-dormant">Dormant</span> older,
<span class="mrl-status mrl-status-archived">Archived</span> read-only on its host.
Low activity does not mean broken: some stable packages need few changes.
</p>

<!-- catalog:explorer -->

## Missing a project?

Add it to [`data/catalog.yml`](https://github.com/ros-maritime/maritime_robotic_landscape/blob/main/data/catalog.yml) with a pull request. Each entry needs a name, a repository or website, a category, the ROS versions, the vehicle types, and a one-sentence factual description. See [Contributing](contributing.md) for the field list. The full data set is also available as <a href="../catalog.json"><code>catalog.json</code></a> for your own tools.
