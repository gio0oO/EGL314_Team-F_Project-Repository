# L-ISA Guide

Today I will be showing how to setup L-ISA controller and processor.

Resources

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
B --3.5mm/DVS--> D[Output Interface]
```

# Configuration (L-ISA)
1. Open L-ISA Processor and select your heaphone/speaker output

![L-ISA Processor](Images/)

2. Open L-ISA Controller and go to Processors, select and connect to your local processor desktop, and check connection and audio status

![L-ISA Processors setting](Images/)

3.Hit Play in Reaper