---
title: Vehicle types
description: Surface and underwater vehicle classes in maritime robotics - ASVs, AUVs, ROVs, gliders, and specialized platforms - and what each means for software.
---

# Vehicle types

Maritime robots differ mainly in where they operate (on or below the surface), how they get power and communication (tether or not), and how they move (propellers, thrusters, buoyancy, or sail). Each choice changes the software.

<div class="grid cards" markdown>

-   <svg class="mrl-vehicle" viewBox="0 0 200 75" role="img" aria-label="Surface vehicle"><rect x="0" y="48" width="200" height="27" class="mrl-svg-water"/><path d="M30 48 L170 48 L160 58 L40 58 Z" class="mrl-svg-hull"/><path d="M30 44 L170 44 L165 48 L35 48 Z" class="mrl-svg-hull" opacity="0.7"/><rect x="85" y="28" width="30" height="16" rx="2" class="mrl-svg-accent"/><line x1="100" y1="28" x2="100" y2="12" class="mrl-svg-line" stroke-width="2"/><circle cx="100" cy="10" r="3" class="mrl-svg-accent"/></svg>

    **Surface vehicles (ASV / USV)**

    ---

    Work on the surface: survey, monitoring, logistics, and relay for underwater vehicles. GNSS, radio, and solar power are available. Usually 2 or 3 controlled DOF (surge and yaw, sometimes sway).

    *Software focus:* GNSS and heading fusion, obstacle detection (radar, lidar, AIS, cameras), COLREGs, waves.

-   <svg class="mrl-vehicle" viewBox="0 0 200 75" role="img" aria-label="Torpedo AUV"><rect x="0" y="0" width="200" height="75" class="mrl-svg-water"/><path d="M40 30 H150 Q172 37 150 44 H40 Q28 37 40 30 Z" class="mrl-svg-hull"/><path d="M40 30 L30 22 L36 37 L30 52 L40 44 Z" class="mrl-svg-accent"/><circle cx="26" cy="37" r="4" class="mrl-svg-line" fill="none" stroke-width="2"/></svg>

    **Torpedo AUVs**

    ---

    Untethered, streamlined, efficient for long survey lines. Usually underactuated: one propeller plus fins or a vectored thruster.

    *Software focus:* DVL and INS dead reckoning, depth and altitude control, mission autonomy, acoustic communication.

-   <svg class="mrl-vehicle" viewBox="0 0 200 75" role="img" aria-label="Hovering AUV or ROV"><rect x="0" y="0" width="200" height="75" class="mrl-svg-water"/><rect x="62" y="22" width="76" height="34" rx="6" class="mrl-svg-hull"/><rect x="50" y="18" width="14" height="10" rx="2" class="mrl-svg-accent"/><rect x="136" y="18" width="14" height="10" rx="2" class="mrl-svg-accent"/><rect x="50" y="50" width="14" height="10" rx="2" class="mrl-svg-accent"/><rect x="136" y="50" width="14" height="10" rx="2" class="mrl-svg-accent"/><path d="M100 22 C100 8 120 4 150 2" class="mrl-svg-line" fill="none" stroke-width="2" stroke-dasharray="4 3"/></svg>

    **Hovering AUVs and ROVs**

    ---

    Many thrusters for 4 to 6 controlled DOF; hold station for inspection and intervention. ROVs are tethered and piloted; hovering AUVs are free.

    *Software focus:* thrust allocation, station keeping, perception near structures, manipulation, teleoperation.

-   <svg class="mrl-vehicle" viewBox="0 0 200 75" role="img" aria-label="Underwater glider"><rect x="0" y="0" width="200" height="75" class="mrl-svg-water"/><path d="M10 10 L50 60 L90 10 L130 60 L170 10" class="mrl-svg-line" fill="none" stroke-width="1.5" stroke-dasharray="3 4"/><g transform="rotate(-38 110 40)"><path d="M85 37 H130 Q140 40 130 43 H85 Q80 40 85 37 Z" class="mrl-svg-hull"/><path d="M100 40 L120 28 L114 40 Z" class="mrl-svg-accent"/></g></svg>

    **Underwater gliders**

    ---

    Change buoyancy to move in a sawtooth pattern with wings, with no propeller. Slow, but missions last weeks to months.

    *Software focus:* energy-aware planning, sparse communication at each surfacing, dead reckoning with unknown currents.

</div>

## Comparison

| | ASV / USV | Torpedo AUV | Hovering AUV | ROV | Glider |
|---|---|---|---|---|---|
| Tether | No | No | No | Yes | No |
| Power | Battery, solar, fuel | Battery | Battery | Through the tether | Battery |
| Endurance | Hours to months | Hours to days | Hours | As long as the support vessel stays | Weeks to months |
| Controlled DOF | 2-3 | 3-4 (surge, heading, depth or pitch) | 4-6 | 4-6 | Pitch, heading, buoyancy |
| Position source | GNSS | DVL + INS; GNSS at surface; acoustic | DVL + INS; acoustic; vision | Topside USBL; DVL | Dead reckoning; GNSS at surface |
| Communication | RF, cellular, satellite | Acoustic; RF and satellite at surface | Acoustic | Tether (high bandwidth) | Satellite at surface |
| Typical ROS 2 stacks | Project11, VRX models, Nav2 | SMaRC 2, MVP | Blue, MVP | Blue, Orca, ArduSub | Mostly vendor software |

## Specialized platforms

- **Autonomous sailboats** use wind for propulsion and need sail and rudder control with wind-aware routing. See the rs750 simulation in [Simulation](simulation.md).
- **Intervention vehicles** carry one or two manipulators for valve turning, sampling, or tool use. Software: MoveIt 2 for arm planning, whole-body or impedance control (auv_controllers), and vehicle station keeping.
- **Hybrid ROV / AUV (HROV)** vehicles switch between tethered piloting and free autonomous operation.
- **Wave-powered and energy-harvesting platforms** convert wave motion into propulsion or electrical power; see MBARI WEC in [Simulation](simulation.md).
- **Bio-inspired vehicles** use fins, flippers, or pulsed jets; mostly research platforms.

## What it means for your software

| If your vehicle is... | Then you need... |
|---|---|
| Underactuated (most ASVs, torpedo AUVs) | Guidance that controls course and speed, not sway; LOS path following |
| Over-actuated (most ROVs) | Thrust allocation with saturation handling |
| Untethered and submerged | Full onboard autonomy, safe failsafes, and acoustic or no communication |
| Tethered | Topside processing is possible; manage tether drag in control |
| Long-endurance | Energy-aware mission planning and robust recovery from faults |
