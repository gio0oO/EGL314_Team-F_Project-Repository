import tkinter as tk
from reaper import send_message
import time

LaptopReaper = "192.168.254.30"
PORTRP = 7000

LaptopGMA = "192.168.254.229"
PORTGMA = 8888

addr_gma = "/gma3/cmd"
msg_rp = float(1)

ADDR_LEFT_CUE = "/action/40166"  # Address for Left Cue
ADDR_CENTER_CUE = "/action/40167"  # Address for Center Cue
ADDR_RIGHT_CUE = "/action/40169"  # Address for Right Cue
ADDR_PLAY_STOP = "/action/40044"  # Address for Play_Stop
ADDR_GAME_OVER_CUE = "/action/40168"  # Address for Game Over Cue
ADDR_START_CUE = "/action/40162"  # Address for Start Cue
ADDR_HIT_SOUND = "/action/40160"  # Address for Hit Sound
ADDR_GO_TO_STAGE_2 = "/action/40164"  # Address for Go to Stage 2
ADDR_GO_TO_STAGE_3 = "/action/40165"  # Address for Go to Stage 3
ADDR_WIN_CUE = "/action/40161"
ADDR_HIT_LIGHT = "Go+: Sequence 3"

# Off Light
def OffSequence():
    send_message(LaptopGMA, PORTGMA, addr_gma, "Off RunningSequence")

# Play/Stop Reaper
def play_stop():
    send_message(LaptopReaper, PORTRP, ADDR_PLAY_STOP, float(1))

# Act 1
def IntoMarker():
    send_message(LaptopReaper, PORTRP, "/action/40163", float(1))  # Marker 3
    play_stop()

def IntroSeq():
    send_message(LaptopGMA, PORTGMA, addr_gma, "Go+: Sequence 1")  # Sequence 1
    OffSequence()

# Act 2
def LoseMarker():
    send_message(LaptopReaper, PORTRP, "/action/40168", float(1))  # Marker 8
    play_stop()

def LoseLight():
    send_message(LaptopGMA, PORTGMA, "/gma3/cmd", "Go+: Sequence 4")  # Sequence 4


# Act 3
def spotlight():
    send_message(LaptopGMA, PORTGMA, "/gma3/cmd", "Go+: Sequence 6")  # Sequence 6


#Act 4
def hitlight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 3")
    play_stop()
def hitsound():
     send_message(LaptopReaper, PORTRP, "/action/40161", float(1))  #Marker 10

#BGS
def BGSLight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 2")

def BGSSound():
     send_message(LaptopReaper, PORTRP, "/action/40163", float(1))  #Marker 10
     play_stop()

def winlight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 3")
#Direction Warmup
def Left():
     send_message(LaptopReaper, PORTRP, "/action/40166", float(1))  #Left Direction
     play_stop()

def Act1(): #Bringing Them In
    IntoMarker()
    IntroSeq()


def  BGS():
    BGSLight()
    BGSSound()

    OffSequence
def Act2(): #Lose Sequence
    LoseMarker()
    LoseLight()


def Act3(): #Spotlight
    spotlight()


def Act4(): #Hit Sequence
    hitlight()
    hitsound()

def Win():
    winlight()

def Lose():
    LoseLight()
if __name__ == "__main__":
    # Create the Tkinter window
    root = tk.Tk()
    root.title("Sequences and Marker GUI")


    # Create the Start Game button
    Act1_Button = tk.Button(root, text="Bring In", command=lambda: Act1())
    Act1_Button.pack(pady=20)

    Act2_Button = tk.Button(root, text="Lose", command=lambda: Act2())
    Act2_Button.pack(pady=20)

    Act3_Button = tk.Button(root, text="Spotlight(Warmup)", command=lambda: Act3())
    Act3_Button.pack(pady=20)

    Left_Button = tk.Button(root, text="Left Warmup Sequence ", command=lambda: Left())
    Left_Button.pack(pady=20)

    Act4_Button = tk.Button(root, text="Hit ", command=lambda: Act4())
    Act4_Button.pack(pady=20)

    BGS_Button = tk.Button(root, text="Background ", command=lambda: BGS())
    BGS_Button.pack(pady=20)

    Win_Button = tk.Button(root, text="Win Sequence ", command=lambda: Win())
    Win_Button.pack(pady=20)

    Lose_Button = tk.Button(root, text="Lose Sequence ", command=lambda: Lose())
    Lose_Button.pack(pady=20)



    Off_Button = tk.Button(root, text="Off Lights", command=lambda: OffSequence())
    Off_Button.pack(pady=20)

    Play_Button = tk.Button(root, text="Play/Stop", command=lambda: play_stop(),)
    Play_Button.pack(pady=20)


    # Run the Tkinter event loop
    root.mainloop()
