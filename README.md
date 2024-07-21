

# Welcome to the S.O.N.I.C Game Station 1 Documentation!

We are Team F from the MTS 2024 Batch, and this repository provides comprehensive documentation for our project, S.O.N.I.C Game Station 1. Here, you'll find detailed instructions for installations, Raspberry Pi code, and operation procedures.

## About Our Project

S.O.N.I.C Game Station 1 is an interactive target practice game. Players aim to hit targets with shurikens based on directional audio cues. When a sound originates from a specific target, that target becomes the player's focus. The game features three rounds, with decreasing time to hit the targets, increasing the challenge and excitement.

### Game Rules

1. **Three Rounds**: The game consists of three rounds, each with progressively less time to hit the targets.
2. **Targets**: There are three targets – left, right, and center – each represented by a board.
3. **Weapon**: Players use shurikens to hit the targets.
4. **Audio Cues**: Directional audio cues indicate which target to aim for. A sound from a specific direction signals the corresponding target.

Good luck, and aim well!



# System Diagram

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
    Amplifier -->|Speaker Cable| Speakers

    Laptop_GUI[Laptop GUI] -->|WiFi| RPi_Laser_Master[Raspberry Pi - Laser Master]
    RPi_Laser_Master -->|WiFi| RPi_Laser_Slave1[Raspberry Pi - Laser Slave 1]
    RPi_Laser_Master -->|WiFi| RPi_Laser_Slave2[Raspberry Pi - Laser Slave 2]
    RPi_Laser_Master -->|WiFi| RPi_Laser_Slave3[Raspberry Pi - Laser Slave 3]
    RPi_Laser_Master -->|WiFi| RPi_Laser_Slave4[Raspberry Pi - Laser Slave 4]
    RPi_Laser_Master -->|WiFi| RPi_Neopixel[Raspberry Pi - Neopixel]
```


## Contributors

- **gio0oO**
- **samisbackagain05**
- **Genwei1811**


These individuals have committed to this repository and contributed to the development of S.O.N.I.C Game Station 1.