import tkinter as tk
from tkinter import messagebox
import random
import time
from reaper import send_message

#Reaper Info
Laptop = "192.168.254.30"
PORT = 7000

#OSC Messages
ADDR_LEFT_CUE = "/action/40166"  # Address for Left Cue
ADDR_CENTER_CUE = "/action/40167"  # Address for Center Cue
ADDR_RIGHT_CUE = "/action/40169"  # Address for Right Cue
ADDR_PLAY_STOP = "/action/40044"  # Address for Play_Stop
ADDR_GAME_OVER_CUE = "/action/40168"  # Address for Game Over Cue
ADDR_START_CUE = "/action/40162"  # Address for Start Cue
ADDR_HIT_SOUND = "/action/40160"  # Address for Hit Sound
ADDR_GO_TO_STAGE_2 = "/action/40164"  # Address for Go to Stage 2
ADDR_GO_TO_STAGE_3 = "/action/40165"  # Address for Go to Stage 3
ADDR_HIT_LIGHT = "Go+: Sequence 3"
ADDR_OFF_SEQ = "Off RunningSequence"
ADDR_WIN_CUE = "/action/40161"

#Definitions for the Messages

#Off/On
def play_stop():
    send_message(Laptop, PORT, ADDR_PLAY_STOP, float(1)) 

def OffSequence():
    send_message("192.168.254.229",8888, "/gma3/cmd", "Off RunningSequence")

def game_over():
    send_message(Laptop, PORT, ADDR_GAME_OVER_CUE, float(1))
    play_stop()
    time.sleep(5)
    play_stop()

#Go To
def go_to_stage_2():
    send_message(Laptop, PORT, ADDR_GO_TO_STAGE_2, float(1))
    play_stop()


def go_to_stage_3():
    send_message(Laptop, PORT, ADDR_GO_TO_STAGE_3, float(1))
    play_stop()


#Hit 
def hitsound():
    send_message(Laptop, PORT, ADDR_HIT_SOUND, float(1))
    play_stop()


def hitlight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 3")
    
#Miss
def misssound():
    send_message(Laptop, PORT, ADDR_GAME_OVER_CUE, float(1))
    play_stop()    

def misslight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 4")




#Win 
def winlight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 3")

def winsound():
    send_message(Laptop, PORT, ADDR_WIN_CUE, float(1))
    play_stop()    

#Lose
def loselight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 4")
    play_stop()

def losesound():
    send_message(Laptop, PORT, ADDR_GAME_OVER_CUE, float(1))
    play_stop()


#Spotlight
def spotlight():
     send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 6")
      
# Define play_audio_cue function
def play_audio_cue(direction):
    if direction == "Left":
        send_message("Laptop", "PORT", "ADDR_LEFT_CUE", float(1))
    elif direction == "Center":
        send_message("Laptop", "PORT", "ADDR_CENTER_CUE", float(1))
    elif direction == "Right":
        send_message("Laptop", "PORT", "ADDR_RIGHT_CUE", float(1))

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Game")
        
        self.stages = [10, 7, 5]  # seconds for each stage
        self.current_stage = 0
        self.current_cue = 0
        self.misses_in_stage = 0
        self.directions = ["Left", "Center", "Right"]
        self.timer_id = None
        
        self.label = tk.Label(root, text="Get ready!", font=("Helvetica", 32))
        self.label.pack(pady=20)
        
        self.button_start = tk.Button(root, text="Start Game", command=self.start_game, font=("Helvetica", 24))
        self.button_start.pack(pady=20)
        
        self.button_left = tk.Button(root, text="Left", command=lambda: self.check_hit("Left"), font=("Helvetica", 24))
        self.button_center = tk.Button(root, text="Center", command=lambda: self.check_hit("Center"), font=("Helvetica", 24))
        self.button_right = tk.Button(root, text="Right", command=lambda: self.check_hit("Right"), font=("Helvetica", 24))
        
        self.button_left.pack(side=tk.LEFT, padx=20, pady=20)
        self.button_center.pack(side=tk.LEFT, padx=20, pady=20)
        self.button_right.pack(side=tk.LEFT, padx=20, pady=20)
        
    def start_game(self):
        self.button_start.pack_forget()
        self.next_cue()
        spotlight()

    def next_cue(self):
        self.cancel_timer()
        self.current_cue += 1
        if self.current_cue > 3:
            self.current_cue = 1
            self.misses_in_stage = 0
            self.current_stage += 1
        
        if self.current_stage < 3:
            self.direction = random.choice(self.directions)
            self.label.config(text=f"Stage {self.current_stage + 1} Cue {self.current_cue}: {self.direction}")
            play_audio_cue(self.direction)
            self.timer_id = self.root.after(self.stages[self.current_stage] * 1000, self.check_miss)
        else:
            self.end_game()
    
    def check_hit(self, direction):
        self.cancel_timer()
        if direction == self.direction:
            self.label.config(text=f"Hit!")
            hitlight()
            hitsound()
            time.sleep(1)
            play_stop()
            OffSequence()
            self.root.update()
            self.handle_custom_message()
        else:
            self.label.config(text=f"Missed! Try Again")
            misslight()
            misssound()
            time.sleep(1)
            play_stop()
            OffSequence()
            self.root.update()
            self.root.after(1000, self.next_cue)
    
    def check_miss(self):
        if self.current_cue <= 3:
            self.misses_in_stage += 1
            if self.misses_in_stage == 3:
                self.label.config(text="Game Over! You Lost!")
                messagebox.showinfo("Game Over", "You Lost!")
                loselight()
                losesound
                time.sleep(5)
                play_stop()
                OffSequence()
                self.root.quit()
            else:
                self.label.config(text=f"Cue Missed, Next Cue")
                self.root.update()
                self.handle_miss_message()
    
    def handle_custom_message(self):
        if self.current_stage == 0:
            if self.current_cue == 1:
                self.display_custom_message("Haha", self.next_stage)
            elif self.current_cue == 2:
                self.display_custom_message("Well Done!", self.next_stage)
            elif self.current_cue == 3:
                self.display_custom_message("Great!", self.next_stage)
                go_to_stage_2()
                time.sleep(2)
                play_stop()
            
        elif self.current_stage == 1:
            if self.current_cue == 1:
                self.display_custom_message("Keep it up!", self.next_stage)
            elif self.current_cue == 2:
                self.display_custom_message("Nice!", self.next_stage)
            elif self.current_cue == 3:
                self.display_custom_message("Almost there!", self.next_stage)
                go_to_stage_3()
                time.sleep(2)
                play_stop()
        elif self.current_stage == 2:
            if self.current_cue == 1:
                self.display_custom_message("Final stretch!", self.next_stage)
            elif self.current_cue == 2:
                self.display_custom_message("Almost done!", self.next_stage)
            elif self.current_cue == 3:
                self.display_custom_message("You did it!", self.end_game)
                winlight()
                winsound()
                time.sleep(5)
                play_stop()
                OffSequence()
    
    def handle_miss_message(self):
        if self.current_stage == 0:
            if self.current_cue == 1:
                self.display_custom_message("Missed Cue 1! Try again!", self.next_cue)
            elif self.current_cue == 2:
                self.display_custom_message("Missed Cue 2! Try harder!", self.next_cue)
            elif self.current_cue == 3:
                self.display_custom_message("Missed Cue 3! Keep going!", self.next_cue)
        elif self.current_stage == 1:
            if self.current_cue == 1:
                self.display_custom_message("Missed Cue 1! Focus!", self.next_cue)
            elif self.current_cue == 2:
                self.display_custom_message("Missed Cue 2! Don't give up!", self.next_cue)
            elif self.current_cue == 3:
                self.display_custom_message("Missed Cue 3! You can do it!", self.next_cue)
        elif self.current_stage == 2:
            if self.current_cue == 1:
                self.display_custom_message("Missed Cue 1! Almost there!", self.next_cue)
            elif self.current_cue == 2:
                self.display_custom_message("Missed Cue 2! Keep trying!", self.next_cue)
            elif self.current_cue == 3:
                self.display_custom_message("Missed Cue 3! Push through!", self.next_cue)
    
    def display_custom_message(self, message, callback):
        self.label.config(text=message)
        self.root.update()
        self.root.after(1000, callback)
    
    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def next_stage(self):
        self.current_stage += 1
        self.current_cue = 0
        self.misses_in_stage = 0
        self.next_cue()
    
    def end_game(self):
        self.label.config(text="Game Over!")
        messagebox.showinfo("Game Over", "Congratulations! You completed the game.")
        self.root.quit()

root = tk.Tk()
game = Game(root)
root.mainloop()
