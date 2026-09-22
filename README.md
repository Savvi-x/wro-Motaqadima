# WRO 2026 Future Engineers
## Autonomous Vehicle Project – Team 6001

<p align="center">
  <b>World Robot Olympiad 2026 – Future Engineers</b><br>
  Autonomous Driving Vehicle
</p>

---

## Team Information

**Team Name:** المتقدمة2  
**Team Number:** 6001  

### Team Members
- Faisal Abdullah Faisal Al-Rashidan
- Eyad Waleed Omar Khdejoos


# 1. Project Overview

This repository documents the design, development, programming, testing, and improvement process of our autonomous vehicle for the **WRO 2026 Future Engineers** category.

The goal of the project is to develop a fully autonomous four-wheel vehicle capable of navigating the WRO Future Engineers track without external control.

The vehicle is designed to complete two main competition challenges:

1. **Open Challenge**
2. **Obstacle Challenge**

For the Open Challenge, the vehicle must autonomously navigate the track and complete three laps while adapting to the track configuration.

For the Obstacle Challenge, the vehicle must recognize red and green traffic pillars, choose the correct driving side, complete three laps, and finally perform the parking task.

Our design focuses on:

- Reliable autonomous navigation
- Computer vision
- Distance measurement
- Sensor fusion
- Accurate steering
- Stable vehicle control
- Modular software
- Fast sensor processing
- Repeatable testing and calibration

---

# 2. Vehicle Architecture

The vehicle uses a distributed control architecture.

The main processing tasks are divided between:

### Raspberry Pi 5

The Raspberry Pi 5 is the high-level controller of the vehicle.

Its main responsibilities include:

- Camera processing
- Computer vision
- Traffic pillar detection
- Navigation decisions
- Challenge logic
- State machine control
- Sensor data processing
- Communication with the low-level controller

### Raspberry Pi Pico W

The Raspberry Pi Pico W is used as the low-level real-time controller.

Its responsibilities include:

- Steering servo control
- DC motor control
- Distance sensor reading
- Fast actuator commands
- Communication with the Raspberry Pi 5

Although the Pico W contains wireless hardware, wireless communication is not used during competition operation.

Communication between the Raspberry Pi and the vehicle electronics is implemented using wired communication.

---

# 3. System Block Diagram

The general architecture of the robot is:

```text
                     +----------------------+
                     |    Raspberry Pi 5    |
                     |                      |
Camera Module ------>| Computer Vision      |
                     | Navigation           |
                     | State Machine        |
                     | Decision Making      |
                     +----------+-----------+
                                |
                           USB / UART
                                |
                     +----------v-----------+
                     | Raspberry Pi Pico W  |
                     |                      |
                     | Motor Control        |
                     | Steering Control     |
                     | Sensor Interface     |
                     +----+----------+------+
                          |          |
                       Servo      Motor Driver
                          |          |
                     Steering     DC Motor
                          |
                 Distance Sensors / IMU
