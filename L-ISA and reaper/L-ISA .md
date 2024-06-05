# L-ISA Guide

Today I will be showing how to setup L-ISA controller and processor.

'''mermaid
graph LR
A[Raspberry Pi] --OSC--> B[L-ISA Controller]
B --Spatial Metadata--> C[L-ISA Processor]
C --Spatial Metadata--> B
D[Digital Audio Workstation<br>DAW] --L-ISA Bridge--> C
C --3.5mm/DVS--> E[Output Interface]
'''