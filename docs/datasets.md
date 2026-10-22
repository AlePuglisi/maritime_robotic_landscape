---
title: Datasets
description: Public datasets for maritime robotics - sonar, underwater imagery, underwater navigation and SLAM, surface vehicle perception, and ocean data.
---

# Datasets

Public datasets let you develop and compare perception, navigation, and mapping algorithms without your own sea time. Links and contents were checked in October 2026. **Check each dataset's license before use**: many are for non-commercial research only, and some state no license at all.

## Quick finder

| I want to work on... | Start with |
|---|---|
| Sonar object detection or classification | Marine Debris FLS, UATD, AI4Shipwrecks; the OpenSonarDatasets index |
| Underwater SLAM with sonar | Girona Underwater Caves, Aurora |
| Visual or visual-inertial navigation underwater | Aqualoc, NTNU-ARL multi-camera, FLSea, VAROS (synthetic), MIMIR-UW (synthetic) |
| Underwater image segmentation or enhancement | SUIM, EUVP, UIEB, TrashCan |
| USV obstacle detection | LaRS, MODS, MaSTr1325, WaterScenes, MassMIND |
| USV multi-sensor navigation | Pohang Canal, USVInland |
| Seafloor mapping | Aurora; MGDS archives |
| Ocean conditions for mission planning | Copernicus Marine, NOAA, Argo |

## Sonar

| Dataset | Contents | Platform | License |
|---|---|---|---|
| [OpenSonarDatasets](https://github.com/remaro-network/OpenSonarDatasets) | An index of about 20 public sonar datasets (side-scan, forward-looking, scanning, multibeam, synthetic aperture). Start here | Various | Per dataset |
| [Marine Debris FLS](https://github.com/mvaldenegro/marine-debris-fls-datasets) | ARIS Explorer 3000 forward-looking sonar images for classification, segmentation (11 classes), and matching | Water tank and turntable | Not stated |
| [UATD](https://figshare.com/articles/dataset/UATD_Dataset/21331143) | About 9,200 forward-looking sonar images with object boxes | Multibeam FLS | See record |
| [AI4Shipwrecks](https://umfieldrobotics.github.io/ai4shipwrecks/) | Side-scan sonar images of shipwrecks with segmentation labels | AUV side-scan | See site |
| [SubPipe](https://zenodo.org/records/12666132) | Side-scan sonar, camera, and navigation for pipeline inspection | AUV | See record |

## Underwater navigation and SLAM

| Dataset | Contents | Platform | License |
|---|---|---|---|
| [Girona Underwater Caves](https://cirs.udg.edu/caves-dataset/) | Two scanning sonars, DVL, two IMUs, depth, and camera, as ROS bags, in an underwater cave | Sparus II AUV | See site |
| [Aqualoc](https://www.lirmm.fr/aqualoc/) | Monocular camera, MEMS IMU, and pressure sensor, as ROS bags, at harbor and archaeological sites | ROV | See site |
| [Aurora](https://ieee-dataport.org/open-access/aurora-multi-sensor-dataset-robotic-ocean-exploration) | Multibeam, side-scan, camera, and navigation from the Haig Fras marine protected area | Autosub 6000 AUV | See record |
| [NTNU-ARL underwater datasets](https://github.com/ntnu-arl/underwater-datasets) | Five cameras, IMU, and pressure, with motion-capture ground truth | Multi-camera sensor rig | BSD-3 |
| [FLSea](https://viseaon.haifa.ac.il/datasets) | Forward-looking stereo and visual-inertial sequences with depth ground truth (Mediterranean and Red Sea) | Stereo and visual-inertial rig | See site |
| [Eiffel Tower](https://doi.org/10.17882/92226) | Four visits (2015-2020) to a deep-sea hydrothermal vent, for long-term visual localization | Ifremer deep-sea vehicles | See record |
| [Tasmania Coral Point Count](https://marine.acfr.usyd.edu.au/datasets) | More than 100,000 stereo pairs from 22 dives, with labels | AUV Sirius | Acknowledgment requested |

## Synthetic data

| Dataset | Contents | License |
|---|---|---|
| [MIMIR-UW](https://github.com/remaro-network/MIMIR-UW) | Three cameras, IMU, ground-truth pose, depth, and segmentation in four environments, rendered with AirSim and Unreal Engine 4 | Code GPL-3.0; check the data record |
| [VAROS](https://www.ntnu.edu/arosvisiongroup/varos) | Images, IMU, depth gauge, ground-truth poses, depth, and normals | See site |

Simulators can also generate data with perfect ground truth; see [Simulation](simulation.md).

## Underwater imagery

| Dataset | Contents | License |
|---|---|---|
| [SUIM](https://irvlab.cs.umn.edu/resources/suim-dataset) | 1,635 images with pixel labels in eight classes | See site |
| [EUVP](https://irvlab.cs.umn.edu/resources/euvp-dataset) | Paired and unpaired images for underwater image enhancement | See site |
| [UIEB](https://li-chongyi.github.io/proj_benchmark.html) | 950 real underwater images for enhancement benchmarks | See site |
| [TrashCan 1.0](https://conservancy.umn.edu/items/6dd6a960-c44a-4510-a679-efb8c82ebfb7) | ROV images of marine debris with instance segmentation (from the JAMSTEC J-EDI archive) | Academic use; commercial use needs JAMSTEC permission |

## Surface vehicle perception

| Dataset | Contents | License |
|---|---|---|
| [LaRS](https://lojzezust.github.io/lars-dataset) | More than 4,000 key frames from lakes, rivers, and sea with panoptic labels, for obstacle segmentation | See site |
| [MODS](https://vicos.si/resources/) | Benchmark with about 81,000 stereo frames and IMU, for USV obstacle detection | See site |
| [MaSTr1325](https://vicos.si/resources/mastr1325/) | 1,325 USV images with pixel labels (sky, water, obstacle) | See site |
| [WaterScenes](https://waterscenes.github.io) | 4D radar and camera data with detection and segmentation labels | See site |
| [MassMIND](https://github.com/uml-marine-robotics/massmind) | 2,916 long-wave infrared images from Boston Harbor with segmentation labels | See repository |
| [SeaDronesSee](https://seadronessee.cs.uni-tuebingen.de) | Aerial images over open water, for search and rescue detection | See site |
| [Pohang Canal](https://sites.google.com/view/pohang-canal-dataset) | Three lidars, marine radar, stereo, infrared and omnidirectional cameras, AHRS, and RTK GNSS over a 7.5 km route | CC BY-NC 4.0 |
| [USVInland](https://www.orca-tech.cn/datasets.html) | Lidar, stereo, millimeter-wave radar, GNSS, and IMU over 26 km of inland waterways | See site |

## Ocean and geoscience data

| Source | Contents |
|---|---|
| [Copernicus Marine Service](https://marine.copernicus.eu/) | Ocean currents, temperature, salinity, and waves: analyses and forecasts |
| [NOAA National Centers for Environmental Information](https://www.ncei.noaa.gov/) | Bathymetry, ocean profiles (World Ocean Database), and more |
| [Argo](https://argo.ucsd.edu/) | Temperature and salinity profiles from a global float array |
| [MGDS (Marine Geoscience Data System)](https://www.marine-geo.org/) | Archived multibeam bathymetry and other marine geoscience data, with DOIs |
| [GEBCO](https://www.gebco.net/) | Global gridded bathymetry, for planning and simulation terrain |

Use these to plan missions, to set realistic currents and sound speed profiles in simulation, and to validate maps.

## Share your dataset

A useful dataset release has:

1. **Documentation**: sensors with models and mounting, calibration, environmental conditions, and how the data was collected.
2. **Standard formats**: ROS 2 bags in MCAP for multi-sensor data, plus common image and point cloud formats. Metadata in YAML or JSON.
3. **Ground truth**, with a description of how it was obtained and its accuracy.
4. **A clear license** (for example CC BY 4.0) and a citation.
5. **Permanent hosting with a DOI** (for example Zenodo or an institutional repository).

Then add it to this page with a pull request: name, link, contents, platform, and license.
