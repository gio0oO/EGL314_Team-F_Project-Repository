# Minimum Viable Product

## Description
Welcome to Team F's Game Showcase featuring **The Range**. This repository includes all necessary codes, lighting assets, and video assets used throughout the project. This document will provide an overview of the game, its functionalities, and how the system components are integrated.

## Overview
**The Range** is an interactive game designed to challenge players with a series of timed cues. The game involves hitting targets on various boards, with the time to hit each cue decreasing as the stages progress. Each board and stage is monitored through a complex system involving multiple Raspberry Pis, sensors, and integration with various audio and lighting controls.

## System Diagram

```mermaid
graph TD
    Piezo_Sensor[Piezo Sensor] -->|GPIO| RPi_Game[Raspberry Pi - Game]
    RPi_Game -->|WiFi| GrandMA3[GrandMA3]
    RPi_Game -->|WiFi| Reaper[Reaper]
    GrandMA3 -->|SACN| Moving_Heads[Moving Heads]
    Reaper_DAW -->|Dante VSC| L_ISA_Processor[L-ISA Processor]
    L_ISA_Processor -->|MetaData| L_ISA_Controller[L-ISA Controller]
    L_ISA_Controller -->|DANTE| Yamaha_QL1[Yamaha QL1]
    Yamaha_QL1 -->|DANTE| Amplifier
    Amplifier -->|Spk Cable| Speakers

    Laptop_GUI[Laptop GUI] -->|WiFi| RPi_Laser_Master[Raspberry Pi - Laser Master]
    RPi_Laser_Master -->|WiFi| RPi_Laser_Slave1[Raspberry Pi - Laser Slave 1]
    RPi_Laser_Master -->|WiFi| RPi_Laser_Slave2[Raspberry Pi - Laser Slave 2]
    RPi_Laser_Master -->|WiFi| RPi_Laser_Slave3[Raspberry Pi - Laser Slave 3]
    RPi_Laser_Master -->|WiFi| RPi_Laser_Slave4[Raspberry Pi - Laser Slave 4]
    RPi_Laser_Master -->|WiFi| RPi_Neopixel[Raspberry Pi - Neopixel]
