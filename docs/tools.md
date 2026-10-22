---
title: Tools and workflows
description: Logging, visualization, geodesy, ground control, CI, and container workflows for marine robotics software.
---

# Tools and workflows

The tools on this page are not marine-specific, but marine teams use them every day. Field time is short, so good logging and fast analysis tools pay for themselves on the first deployment.

## Packages

<!-- catalog:table category=tools -->

## Logging

- **Record everything raw.** Raw sensor data lets you reprocess navigation and perception after the mission. Record the state estimate and the controller commands too.
- **Use MCAP.** It is the default rosbag2 storage format in current ROS 2 releases, and many tools (Lichtblick, Foxglove, PlotJuggler, the `mcap` CLI) read it.
- **Split and compress.** Use `--max-bag-duration` or `--max-bag-size` so that a power loss destroys at most one file. The MCAP storage presets (`zstd_fast`, `zstd_small`, `fastwrite`) set the compression.
- **Do not log through slow links.** Record on the vehicle and download after recovery.

```bash
# Record everything to MCAP with fast zstd chunk compression, in 5-minute files
ros2 bag record -a -s mcap --storage-preset-profile zstd_fast \
  --max-bag-duration 300 -o dive_$(date +%Y%m%d_%H%M)
```

- **Analyze without ROS.** [rosbags](https://gitlab.com/ternaris/rosbags) reads and writes ROS 1 and ROS 2 bags in pure Python, so data scientists do not need a ROS installation.

## Visualization and tuning

| Tool | Use it for |
|---|---|
| RViz2 | TF trees, point clouds, markers, sonar and camera images, live |
| PlotJuggler | Time series: EKF innovations, controller errors, thruster commands. Live or from bags |
| Lichtblick | Open-source web and desktop app for multi-panel dashboards from MCAP files or a live bridge |
| QGroundControl | Pilot interface and parameters for ArduSub, ArduPilot Rover, and PX4 vehicles |
| `rqt_graph`, `ros2 doctor` | Check node connections and the environment |

## Geodesy and coordinate tools

| Task | Tool |
|---|---|
| WGS 84 ↔ UTM in ROS | `geodesy` from [geographic_info](https://github.com/ros-geographic-info/geographic_info) |
| Local ENU tangent plane, geoid heights | [GeographicLib](https://geographiclib.sourceforge.io/) (`LocalCartesian`) |
| Any coordinate reference system, in Python | [pyproj](https://github.com/pyproj4/pyproj) |
| Pressure to depth (TEOS-10) | [GSW Python](https://teos-10.github.io/GSW-Python/) (`gsw.z_from_p`) |
| GNSS fixes into the EKF | `navsat_transform_node` in robot_localization |

See [Frames and conventions](conventions.md) for the rules.

## Development environment

- **Containers.** Docker images make simulation and dependencies reproducible across a team. SUAVE and POSIM publish images; Blue and auv_controllers include development container setups. For GPU simulators, install the NVIDIA Container Toolkit.
- **Workspaces.** Use `vcs` (vcstool) with a `.repos` file to pin the repositories of a vehicle stack, and `rosdep` for system dependencies.
- **Target hardware.** Many vehicles run on ARM computers (Raspberry Pi, NVIDIA Jetson). Build and test on ARM in CI, or cross-compile, before you go to the field.

## Continuous integration

- Build and test each package on every pull request with [action-ros-ci](https://github.com/ros-tooling/action-ros-ci) or [industrial_ci](https://github.com/ros-industrial/industrial_ci).
- Add a headless simulation test: launch the vehicle in Gazebo or Stonefish, run a short mission, and check that it reaches the waypoints.
- Add unit tests for frame conversions and message parsing in drivers; these find the expensive bugs early.
- Release packages to the ROS build farm, so users can install them with `apt`.

## Field laptop checklist

- [ ] Offline copies of documentation, maps, and charts
- [ ] All dependencies installed; no internet needed to build
- [ ] Same software versions as the vehicle (container image tag or `.repos` pins)
- [ ] Bag analysis tools installed (PlotJuggler, Lichtblick, rosbags)
- [ ] Enough disk space and a second drive for backups
