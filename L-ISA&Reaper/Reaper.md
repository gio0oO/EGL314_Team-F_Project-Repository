# Reaper(x64) Guide

Today I will show you on how to run **Reaper** for MIDI timecode for **L-ISA Controller** followed by Using Raspi to control **Reaper**.

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
D[Raspberry Pi] --LAN/WiFi--> C[Reaper<br>DAW]

```

# Configuration (Setup MIDI Timecode)
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

7. Also in **Reaper preferences**, Reaper must be inform of which file to recieve L-ISA plug-ins folder

* Select **VST** in the list
* Enter the path to the folder where L-ISA plug-ins are installed, like c: :\Program Files\L-Acoustics\L-ISA Controller\VST3\
* Hit Rescan

![VST Settings](Images/VST_Settings.png)

8. Also in **Reaper Preferences**, select **L-ISA audio bridge** as an audio device
* Select **ASIO** First

![Audio Bridge](Images/Audio_Bridge.png)

9. In Reaper,click on the **Route** button of timecode generator track in the **Mixer** to open the routing panel of the MIDI TimeCode Track and select the **loopMIDI** port in the MIDI Hardware Output list

![MIDI Routing](Images/MIDI_Routing.png)

10. In the **L-ISA Controller**, go to **Settings > MIDI** and select on **MTC** from loopMIDI Port as the MIDI Interface
* In **Reaper**, hit Play and Verify that the timecode is recieved in the **L-ISA Controller** with the right frame rate and timing

![L-ISA MIDI](Images/L-ISA_MIDI.png)

# Configuration (Reaper for OSC)

1. Go to **Reaper References** (Ctrl+P)
2. Navigate to **Control/OSC/Web**
3. Click on ADD to configure a new OSC device

![OSC Reaper Preferences](Images/OSC_Reaper_Preferences.png)

4. Configure new OSC Device

![OSC Control](Images/OSC_Control.png)