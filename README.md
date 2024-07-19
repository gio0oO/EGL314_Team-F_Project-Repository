# TeamF_EGL314

We are Team F of the MTS 2024 Batch and in this repository, it features documentation of our project S.O.N.I.C Game Station 1. It includes all the installations made, raspi codes and operation procedures. 

Our game station is a Target Practice station that requires players to shoot at targets with shurikens. Their aim is to hit at the correct targets indictated by directional audio cues, meaning if a sound comes from that target, that is the target to aim for. T
We have designed an A4 poster to explain the rules and will be uploaded below.

# System Diagram

```mermaid
graph TD
    LaunchPad -->|USB C| RPi_Game[Raspberry Pi - Game]
    RPi_Game -->|WiFi| GrandMA3[GrandMA3]
    RPi_Game -->|WiFi| Reaper_DAW[Reaper DAW]
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