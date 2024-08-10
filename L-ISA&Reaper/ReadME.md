In this document, you will get to know how to link **Reaper, L-ISA Controller and L-ISA Processor** for a Surround Sound Game.

# Software Used

* Reaper(x64)
* loopMIDI
* L-ISA Controller
* L-ISA Processor

In this document, it will be seperated into 2 parts:

1. Reaper For MIDI Timecode - Click [Here](./Reaper.md)
2. L-ISA Controller and Processor - Click [Here](./L-ISA.md)

# System Diagram
```mermaid
graph TD
    Reaper_DAW -->|Dante VSC| L_ISA_Processor[L-ISA Processor]
    L_ISA_Processor -->|MetaData| L_ISA_Controller[L-ISA Controller]
    L_ISA_Controller -->|DANTE| Yamaha_QL1[Yamaha QL1]
    Yamaha_QL1 -->|DANTE| Amplifier
    Amplifier -->|Speaker Cable| Speakers
```