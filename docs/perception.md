---
title: Perception and mapping
description: Sonar and camera perception, underwater SLAM, and seafloor mapping for marine robots, with ROS packages and practical notes.
---

# Perception and mapping

Light is absorbed and scattered in water within meters to tens of meters, depending on turbidity, while sound travels kilometers. Underwater perception therefore combines **sonar** for range and coverage with **cameras** for close-range detail. Surface vehicles add radar, lidar, AIS, and cameras.

## Acoustic or optical?

| | Sonar | Camera |
|---|---|---|
| Range in water | Meters to hundreds of meters, depending on frequency | Centimeters to tens of meters, depending on turbidity and light |
| Resolution | Lower; falls with range | High at close range |
| Works in turbid or dark water | Yes | Poorly; needs artificial light |
| Main artifacts | Speckle, multipath, elevation ambiguity (2D imaging sonar), acoustic shadows | Color loss with depth, backscatter, refraction at the housing port |
| Typical use | Obstacle avoidance, search, SLAM, bathymetry | Inspection, close-range mapping, classification, visual odometry |

## Sonar types

| Type | Output | ROS message (marine_msgs) | Typical use |
|---|---|---|---|
| Single-beam echosounder (for example Ping2) | Range to bottom | `sensor_msgs/Range` | Altitude, shallow bathymetry |
| Mechanically scanned imaging sonar (MSIS, for example Ping360) | One beam that rotates; a full image builds up over seconds | `RawSonarImage` / `ProjectedSonarImage` | Low-cost obstacle detection, SLAM in confined spaces |
| Multibeam imaging / forward-looking sonar (FLS, for example Oculus) | A fan image each ping | `ProjectedSonarImage` | Real-time obstacle avoidance, inspection, sonar SLAM |
| Multibeam echosounder (MBES) | Many range and angle detections across track | `SonarDetections` / `SonarRanges` | Bathymetric mapping |
| Side-scan sonar (SSS) | Wide strips of seabed backscatter on each side | No standard message yet | Search, survey, archaeology |
| Synthetic aperture sonar (SAS) | Very high resolution seabed images | No standard message | Mine countermeasures, high-resolution survey |

**Elevation ambiguity**: a 2D imaging sonar gives range and bearing but not elevation, so objects at different heights in the beam fall on the same pixel. Sonar SLAM and 3D reconstruction methods must handle this explicitly.

## Packages

<!-- catalog:table category=perception -->

## Underwater vision

- **Calibrate in water.** A flat port changes the effective focal length and adds distortion, so an in-air calibration is wrong underwater. Calibrate with a target in the water through the same port, or use a dome port centered on the lens.
- **Color and contrast.** Red light is absorbed first. Enhancement and color correction help people and some detectors, but check whether they help your downstream algorithm before you add them to the pipeline.
- **Lighting.** Strobes or LEDs placed away from the camera axis reduce backscatter.
- **Visual odometry and SLAM** (ORB-SLAM3, OpenVINS, SVIn) work in clear water with texture. They fail in turbid water and over featureless sand, so fuse them with DVL and INS rather than relying on them alone.

## Underwater SLAM

| Approach | Sensors | Examples |
|---|---|---|
| Sonar pose-graph SLAM | Imaging sonar + DVL + IMU | sonar-SLAM (BRUCE, iSAM2 backend) |
| Sonar-visual-inertial | Camera + IMU + sonar + depth | SVIn |
| Visual or visual-inertial | Camera (+ IMU) | ORB-SLAM3 (used by Orca5), OpenVINS |
| Bathymetric SLAM | Multibeam + navigation | Research code; often custom |

Factor-graph libraries (GTSAM, fuse) are the common backends. DVL and INS dead reckoning gives strong odometry factors between sonar or camera observations.

## Seafloor mapping

- **Bathymetry** from multibeam data needs accurate navigation, attitude, sound speed profiles, and lever arms. Process it with [MB-System](https://github.com/dwcaress/MB-System) (open source) or a commercial package.
- **Photomosaics and 3D reconstruction** from cameras use structure-from-motion tools; navigation from the vehicle gives a good initial pose.
- **Sound speed** varies from about 1450 to 1550 m/s with temperature, salinity, and depth. Use a measured profile (from a CTD or sound velocity probe) for multibeam and acoustic positioning; a constant 1500 m/s gives range and refraction errors.

## Surface vehicle perception

- **Radar** sees other vessels and the shoreline at long range. Messages: `marine_sensor_msgs/RadarSector` and `RadarEcho`.
- **Lidar** is good for docking and nearby obstacles, but is affected by spray, rain, and the water surface.
- **AIS** gives positions and identities of equipped vessels: see [marine_ais](https://github.com/rolker/marine_ais). Many small craft do not transmit AIS.
- **Cameras** detect buoys, markers, and small craft; datasets such as LaRS and MODS are on the [Datasets](datasets.md) page.
- **COLREGs**: collision avoidance that follows the collision regulations needs vessel tracking and intent estimation. MOOS-IvP includes COLREGs avoidance behaviors.

## Datasets and simulation for perception

Train and test on public [datasets](datasets.md), and generate labeled data with image-focused simulators such as HoloOcean, OceanSim, and UNav-Sim (see [Simulation](simulation.md)).
