# Reaper(x64) Guide

Today I will show you on how to run reaper(x64) for midi timecode for L-ISA controller

# Resources
* L-ISA Controller
* L-ISA Processor
* Reaper(x64)
* loopMIDI

# System Flowchart

```mermaid
graph LR
A[L-ISA Controller] --Spatial Metadata--> B[L-ISA Processor]
B --Spatial Metadata--> A
C[Digital Audio Workstation<br>DAW] --L-ISA Bridge--> B
```

# Configuration
1. Open **loopMIDI** and create a new virtual port by pressing the plus(+) sign after renaming the port to the name of your choice.

![loopMIDI](Images/loopMIDI.png)

2. Open **Reaper** and create a new project
3. Go to insert and select SMPTE LTC/MTC Timecode Generator and the timecode generator will appear on the timelime selected

![Timecode Generator](Images/Timecode_Generator.png)

4. After the timecode generator appear, right click on the timecode generator and select source properties
5. On the SMPTE Generator Properties, select Send MIDI(MTC) to send MIDI Timecode and select Ok to save the settings

![SMPTE Generator Properties](Images/SMPTE_Generator_Properties.png)

6. Open **Reaper preferences** (Ctrl + P), Go to Audio > MIDI Devices, select the loopMIDI port in the MIDI output list
* If it is not enabled, right-click on it and select "Enable Output" 

![Reaper Preferences](Images/Reaper_References.png)

7. In Reaper,click on the **Route** button of timecode generator track in the **Mixer** to open the routing panel of the MIDI TimeCode Track and select the **loopMIDI** port in the MIDI Hardware Output list

![MIDI Routing](Images/MIDI_Routing.png)

8. In the **L-ISA Controller**, go to **Settings > MIDI** and select on **MTC** from loopMIDI Port as the MIDI Interface
* In **Reaper**, hit Play and Verify that the timecode is recieved in the **L-ISA Controller** with the right frame rate and timing

![L-ISA MIDI](Images/L-ISA_MIDI.png)