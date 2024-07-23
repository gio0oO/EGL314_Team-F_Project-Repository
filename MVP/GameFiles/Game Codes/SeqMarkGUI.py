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
    send_message(LaptopReaper, PORTRP, "/action/40161", float(1))  # Marker 10

#BGS
def BGSLight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 2")

def BGSSound():
    send_message(LaptopReaper, PORTRP, "/action/40163", float(1))  # Marker 10
    play_stop()

def MalayGuy():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 8")

def winlight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 3")

#Direction Warmup
def Left():
    send_message(LaptopReaper, PORTRP, "/action/40166", float(1))  # Left Direction
    play_stop()

def Act1():  # Bringing Them In
    IntoMarker()
    IntroSeq()

def BGS():
    BGSLight()
    BGSSound()
    OffSequence()

def Act2():  # Lose Sequence
    LoseMarker()
    LoseLight()

def Act3():  # Spotlight
    spotlight()

def Act4():  # Hit Sequence
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

    # Set window to fullscreen
    root.attributes('-fullscreen', True)

    # Define button size and style
    button_width = 25  # Adjust width as needed
    button_height = 4  # Adjust height as needed
    button_font = ('Helvetica', 16, 'bold')  # Larger and bolder text
    button_bg = 'orange'  # Button background color
    button_fg = 'black'   # Button text color

    # Create and place buttons in a 4x2 grid
    Act1_Button = tk.Button(root, text="Bring In", command=lambda: Act1(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Act1_Button.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    Act2_Button = tk.Button(root, text="Lose", command=lambda: Act2(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Act2_Button.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    Act3_Button = tk.Button(root, text="Spotlight(Warmup)", command=lambda: Act3(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Act3_Button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    Left_Button = tk.Button(root, text="Left Warmup Sequence", command=lambda: Left(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Left_Button.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    Act4_Button = tk.Button(root, text="Hit", command=lambda: Act4(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Act4_Button.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

    BGS_Button = tk.Button(root, text="Background", command=lambda: BGS(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    BGS_Button.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')

    Win_Button = tk.Button(root, text="Win Sequence", command=lambda: Win(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Win_Button.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

    Lose_Button = tk.Button(root, text="Lose Sequence", command=lambda: Lose(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Lose_Button.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')

    Off_Button = tk.Button(root, text="Off Lights", command=lambda: OffSequence(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Off_Button.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

    Play_Button = tk.Button(root, text="Play/Stop", command=lambda: play_stop(), width=button_width, height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Play_Button.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')

    Malay_Button = tk.Button(root, text="Malay Guy", command=lambda: MalayGuy(), width=button_width,  height=button_height, font=button_font, bg=button_bg, fg=button_fg)
    Malay_Button.grid(row=5, column=1, padx=10, pady=10, sticky='nsew')

    # Make grid cells expand proportionally
    for i in range(5):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i % 2, weight=1)

    # Run the Tkinter event loop
    root.mainloop()
