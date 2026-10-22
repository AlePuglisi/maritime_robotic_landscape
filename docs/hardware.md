---
title: Sensors and components
description: Navigation sensors, sonars, thrusters, power, housings, and platforms for marine robots, with selection criteria and ROS 2 driver status.
---

# Sensors and components

This page helps you choose hardware with software in mind: what each component does, what to compare, and whether it has a maintained ROS 2 driver. Prices and specifications change often; use vendor datasheets and quotes for decisions.

!!! info "Driver status"

    Driver availability below was checked in October 2026. The [Drivers](drivers.md#ros-2-driver-status-by-vendor) page has the full table with links.

## Platforms

### Commercial underwater platforms

| Platform | Type | ROS support |
|---|---|---|
| Blue Robotics BlueROV2 | Small observation-class ROV (base and heavy configurations) | ArduSub autopilot; ROS 2 through mavros or ardusub_driver; Gazebo models; Blue and Orca stacks |
| IQUA Robotics Girona 500, Sparus II | Hovering and torpedo AUVs for research | COLA2 (ROS 1, licensed); Stonefish simulation |
| MBARI LRAUV (Tethys class) | Long-range AUV | Vendor controller; Gazebo simulation (archived) |
| Work-class and inspection ROVs (various) | Larger ROVs with manipulators | Vendor control systems; ROS usually added through custom interfaces |

### Commercial surface platforms

| Vendor | Platforms | Notes |
|---|---|---|
| Maritime Robotics (Norway) | Otter, Otter X, Mariner, Mariner X | Survey and research USVs |
| L3Harris (formerly ASV Global) | C-Worker series | Work-class USVs |
| Blue Robotics | BlueBoat | Small USV on ArduPilot Rover and BlueOS |
| Ocean Aero | Submaran | Wind and solar powered surface/subsurface vehicle |
| WAM-V (Marine Advanced Research) | Wave Adaptive Modular Vessel | RobotX platform; simulated in VRX |

Many research groups build their own vehicles. Open designs and community builds are a good start; ask on the [community channels](community.md).

## Navigation sensors

### Doppler Velocity Log (DVL)

A DVL measures velocity relative to the seafloor (bottom track) or to the water (water track) from the Doppler shift of acoustic beams, and usually also altitude. It is the main dead-reckoning sensor of most AUVs. See [Localization](navigation.md#dead-reckoning-with-a-dvl).

| Vendor | Example products | ROS 2 driver |
|---|---|---|
| Water Linked | DVL A50, A125 | :material-check-circle:{ .mrl-yes } Official ([waterlinked_dvl](https://github.com/waterlinked/waterlinked_dvl)) |
| Nortek | Nucleus, DVL500, DVL1000 | :material-check-circle:{ .mrl-yes } Official for Nucleus ([nucleus_driver](https://github.com/nortekgroup/nucleus_driver)) |
| Teledyne RDI | Pathfinder, Tasman, Workhorse | Community and lab drivers only |
| LinkQuest | NavQuest | None public found |

**Choose by:**

1. **Bottom-track range** at your operating altitude. Lower frequency gives more range; higher frequency gives better accuracy at short range and is smaller.
2. **Minimum altitude**, for vehicles that work close to the bottom.
3. **Depth rating, size, and power**, for small vehicles.
4. **Accuracy** (long-term velocity error as a percentage of speed) from the datasheet.
5. **Interface and driver**: Ethernet or serial, and a maintained ROS 2 driver.
6. **Interference**: check how pinging is triggered and synchronized with your sonars and modem.

### Inertial navigation (INS / IMU / AHRS)

| Class | Gyro technology | Heading source | Typical use |
|---|---|---|---|
| IMU / AHRS | MEMS | Magnetometer | Small ROVs, ASVs, budget AUVs. Magnetic heading suffers near thrusters and steel |
| GNSS-aided INS | MEMS or tactical | Dual-antenna GNSS or magnetometer | ASVs and surface navigation |
| Navigation-grade INS | Fiber-optic (FOG) or ring-laser gyro | Gyrocompassing (true north from Earth rotation) | Survey AUVs, deep vehicles; DVL-aided dead reckoning |

| Vendor | Example products | ROS 2 driver |
|---|---|---|
| SBG Systems | Ellipse, Ekinox, Apogee | :material-check-circle:{ .mrl-yes } Official, binary release |
| MicroStrain by HBK | 3DM-GX5, CV7, GQ7 | :material-check-circle:{ .mrl-yes } Official, binary release |
| Xsens (Movella) | MTi series | :material-check-circle:{ .mrl-yes } Vendor support repository |
| Advanced Navigation | Spatial, Certus, Boreas | :material-check-circle:{ .mrl-yes } Vendor example driver (Humble) |
| VectorNav | VN-100, VN-200, VN-300 | Community driver |
| Exail (formerly iXblue) | PHINS, Rovins | None public |
| Kearfott, Sonardyne (SPRINT), Sparton | Various | None public |

**Choose by:** gyro bias stability (drift), heading accuracy and its source, the ability to take DVL and GNSS aiding inside the INS, depth rating, and interfaces.

### Depth and pressure

Pressure sensors give depth with good accuracy, and they are simple and reliable. Compare range, accuracy as a percentage of full scale, temperature compensation, and sampling rate. Example: Blue Robotics Bar30 and Bar100 for small vehicles; Paroscientific and Keller for high accuracy. See [depth conversion](conventions.md#depth-pressure-and-altitude).

### GNSS

- **Standard GNSS** for general surface positioning.
- **RTK GNSS** for centimeter-level survey positioning, with a base station or correction service (NTRIP).
- **Dual-antenna GNSS** for heading without a magnetometer, important for ASVs at low speed.

Drivers: nmea_navsat_driver, ublox_dgnss, ublox, swiftnav-ros2 (see [Drivers](drivers.md)).

## Acoustic positioning

| System | Example vendors | Notes |
|---|---|---|
| USBL | Sonardyne, EvoLogics, Kongsberg | Topside array tracks the vehicle; the fix must be sent down to the vehicle if it navigates on it |
| SBL | Water Linked Underwater GPS | Receivers spread around the topside platform; popular with small ROVs |
| LBL | Sonardyne, Kongsberg | Seafloor beacons, highest accuracy over an area |
| Modem ranging | WHOI Micro-Modem, EvoLogics | Ranges from the communication modem itself |

See [Localization](navigation.md#acoustic-positioning).

## Sonar

| Type | Example products | Driver status |
|---|---|---|
| Echosounder | Blue Robotics Ping2 | Community (blueos-ros2, ping-python) |
| Mechanically scanned imaging | Blue Robotics Ping360, Tritech Micron | Ping360: community ROS 2 drivers |
| Multibeam imaging / FLS | Blueprint Subsea Oculus, Teledyne BlueView | Oculus: community ROS 2 drivers |
| Multibeam echosounder | Cerulean Surveyor, Norbit, Kongsberg, R2Sonic | Cerulean: community ROS 2 driver |
| Side-scan | EdgeTech, Klein, Imagenex, Tritech | Mostly vendor software |

See [Perception](perception.md#sonar-types) for what each type is good for.

## Cameras and lights

- Underwater cameras need in-water calibration (see [Perception](perception.md#underwater-vision)). Low-light sensors and good lighting matter more than resolution.
- Strobes and LEDs consume much power; place them away from the camera axis to reduce backscatter.
- Surface vehicles also use thermal cameras and pan-tilt-zoom cameras.

## Propulsion

### Thrusters

| Manufacturer | Examples | Notes |
|---|---|---|
| Blue Robotics | [T200](https://bluerobotics.com/store/thrusters/t200-thruster/), T500 | Brushless, flooded-motor design; need a brushless ESC. The [T100](https://bluerobotics.com/store/retired/t100-thruster/) is end of life |
| Tecnadyne | Various models | Professional subsea thrusters |
| VideoRay | Thrusters for VideoRay ROVs | Vehicle-specific |
| Teledyne SeaBotix | BTD150, BTD300 | Teledyne ended SeaBotix vehicle production in 2025; check spare availability |

**Choose by:**

- **Thrust curve** at your supply voltage, forward and reverse (they differ), and the current draw. You need the curve for allocation (see [Control](control.md#known-issues)).
- **Depth rating** and pressure tolerance.
- **Control interface**: PWM through an ESC (simple) or a digital bus with RPM and current feedback (better diagnostics).
- **Spares and service**: on intermittent research use, a few low-cost thrusters plus spares can be better than fewer expensive ones; for continuous commercial use, prefer vendor-supported units with service intervals.

| Vehicle | Typical configuration |
|---|---|
| Torpedo AUV | One stern propeller with fins, or a vectored thruster |
| Small ROV (for example BlueROV2) | 6 thrusters (heavy configuration: 8) in a vectored layout |
| Work-class ROV | Vectored horizontal plus vertical thrusters, with redundancy |
| ASV | Twin thrusters (differential), or propeller and rudder; azimuth thrusters on larger vessels |

### Control surfaces and buoyancy

Torpedo AUVs and gliders use rudders and elevators. Gliders and some AUVs use buoyancy engines (pumps or pistons) for vertical motion.

## Power

- **Lithium-ion** is the norm. Use a battery management system (BMS), and follow transport and storage rules for lithium batteries.
- **Pressure-tolerant** battery packs avoid large housings on deep vehicles.
- Thrust falls as battery voltage drops; plan for it in control and in [power budgets](operations.md#power-budgets).
- Surface vehicles can add solar panels or fuel generators.

## Housings, connectors, and tethers

- **Housings**: acrylic or polycarbonate tubes for shallow vehicles and cameras; aluminum, titanium, or glass for deeper ones. Check the depth rating with margin.
- **Connectors and penetrators**: MacArtney (SubConn), Teledyne Impulse, Seacon, and Blue Robotics penetrators. Connectors are a common failure point.
- **Tethers**: neutrally buoyant tethers for small ROVs; fiber for high bandwidth over long lengths. Tether drag dominates in a current.

## Manipulators

| Manufacturer | Examples |
|---|---|
| Reach Robotics (formerly Blueprint Lab) | Reach Alpha, Reach Bravo |
| Schilling Robotics (TechnipFMC) | Work-class manipulators |
| Kraft TeleRobotics | Hydraulic manipulators |

For ROS: MoveIt 2 for planning, and whole-body or impedance control for the vehicle and arm together.

## Saving money, and where not to

**Save on:** used instruments from reputable sources, 3D-printed mounts and fairings, simulation before hardware, and testing each sensor alone before integration.

**Do not save on:** pressure housings and seals, connectors, the INS (it sets your navigation accuracy), battery safety, and an engineering review of critical systems.

## Component suppliers

| Area | Examples |
|---|---|
| Small-vehicle components | Blue Robotics |
| Marine sensors | Teledyne Marine, Nortek, Sonardyne, Water Linked, Kongsberg |
| Connectors | MacArtney (SubConn), Seacon, Teledyne Impulse |
| Housings | Blue Robotics, custom machine shops |
