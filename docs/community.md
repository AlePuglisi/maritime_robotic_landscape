---
title: Community
description: The ROS Maritime Community Working Group - meetings, chat, forum, and how to get involved.
---

# Community

This site is maintained by the **ROS Maritime Community Working Group** (formerly the Maritime Robotics Working Group), an open group of developers, researchers, and operators who use ROS on marine vehicles. Anyone can join.

<div class="grid cards" markdown>

-   :fontawesome-brands-discourse:{ .lg } **Forum**

    ---

    Announcements, meeting notes, and longer technical questions. Searchable.

    [:octicons-arrow-right-24: ROS Discourse, Marine Robotics](https://discourse.openrobotics.org/c/community-groups/marine-robotics/36)

-   :simple-zulip:{ .lg } **Chat**

    ---

    Quick questions and day-to-day discussion on the Open Robotics Zulip.

    [:octicons-arrow-right-24: Marine Robotics channel](https://openrobotics.zulipchat.com/#narrow/channel/526058-Marine-Robotics)

-   :material-calendar-month:{ .lg } **Monthly meetings**

    ---

    Online meetings with project presentations and discussion. Recordings and notes are posted afterwards.

    [:octicons-arrow-right-24: Meeting details](#meetings)

-   :fontawesome-brands-github:{ .lg } **GitHub**

    ---

    The working group's repositories: this site, the charter, and shared interfaces.

    [:octicons-arrow-right-24: github.com/ros-maritime](https://github.com/ros-maritime)

</div>

## Meetings

The working group meets online once a month. Each meeting usually has one or two presentations of a project, a package, or a field deployment, followed by discussion.

- **Announcements and recordings**: posted in the [Marine Robotics category](https://discourse.openrobotics.org/c/community-groups/marine-robotics/36) on ROS Discourse.
- **Calendar invites**: join the [Google Group](https://groups.google.com/g/maritime-robotics-working-group-invites).
- **Agendas and minutes**: [shared document](https://docs.google.com/document/d/1Wnddq4xRXR6HF2XFWeejfUGII_hj7DilKrGcFj1qlEA/edit?usp=drive_link).

Want to present? Post on Discourse or in the Zulip channel. Short talks about work in progress are welcome.

## Working group repositories

| Repository | Purpose |
|---|---|
| [maritime_robotic_landscape](https://github.com/ros-maritime/maritime_robotic_landscape) | This website |
| [community](https://github.com/ros-maritime/community) | Working group charter and organization |
| [maritime_interfaces](https://github.com/ros-maritime/maritime_interfaces) | Proposals for standard maritime interfaces (no message definitions released yet; use [marine_msgs](drivers.md#message-definitions)) |
| [awesome-maritime-robotics](https://github.com/ros-maritime/awesome-maritime-robotics) | Earlier link list, now superseded by the [catalog](catalog.md) |
| [Project board](https://github.com/orgs/ros-maritime/projects) | Work in progress |

## Ways to help

- **Use the catalog and report errors.** If a package is wrongly described or missing, fix it in `data/catalog.yml`.
- **Share field experience.** Known issues, lessons learned, and sensor integration notes are the most valuable content here.
- **Release your drivers.** A ROS 2 driver in the build farm helps every team that buys the same sensor. See [Write your own driver](drivers.md#write-your-own-driver).
- **Present at a meeting.** Tell the community what you built and what went wrong.
- **Help with shared interfaces.** Join the discussion on maritime message standards in marine_msgs and maritime_interfaces.

See [Contributing](contributing.md) for how to edit this site.
