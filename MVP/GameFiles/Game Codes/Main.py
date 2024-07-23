import tkinter as tk
import time
import random
import RPi.GPIO as GPIO
from reaper import send_message

# Constants for GPIO
GPIO_LEFT_SENSOR = 26
GPIO_CENTER_SENSOR = 24
GPIO_RIGHT_SENSOR = 22
POLLING_INTERVAL = 0.0001  # 0.1 ms
POLLING_COUNT = 1000
DETECTION_THRESHOLD = 0.001  # Fraction of detections needed to confirm motion
CUE_DURATION = 4  # Duration of each directional cue in seconds
MARKER_DURATION = 14  # Duration of marker files in seconds
HIT_MARKER_DELAY = 1  # Delay in seconds after playing hit marker
GAME_OVER_DELAY = 5  # Delay in seconds before the second play_stop() after game over

# Define parameters for sending messages
Laptop = "192.168.254.30"
PORT = 7000

# Define addresses for cues
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
# Define marker file constants
MARKER_HIT = ADDR_HIT_SOUND
MARKER_GAME_OVER = ADDR_GAME_OVER_CUE
MARKER_HIT_LIGHT = ADDR_HIT_LIGHT
MARKER_WIN = ADDR_WIN_CUE

# Initialize hit flags for GPIO directions
hit_flags = {direction: False for direction in ["Left", "Center", "Right"]}

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_LEFT_SENSOR, GPIO.IN)
GPIO.setup(GPIO_CENTER_SENSOR, GPIO.IN)
GPIO.setup(GPIO_RIGHT_SENSOR, GPIO.IN)

# Dictionary to map GPIO pins to directions
GPIO_DIRECTION_MAP = {
    "Left": GPIO_LEFT_SENSOR,
    "Center": GPIO_CENTER_SENSOR,
    "Right": GPIO_RIGHT_SENSOR
}

def detect_motion(sensor_pin):
    detection_count = 0
    for _ in range(POLLING_COUNT):
        if GPIO.input(sensor_pin):
            detection_count += 1
        time.sleep(POLLING_INTERVAL)
    return detection_count >= POLLING_COUNT * DETECTION_THRESHOLD
def play_audio_cue(direction):
    if direction == "Left":
        send_message(Laptop, PORT, ADDR_LEFT_CUE, float(1))
    elif direction == "Center":
        send_message(Laptop, PORT, ADDR_CENTER_CUE, float(1))
    elif direction == "Right":
        send_message(Laptop, PORT, ADDR_RIGHT_CUE, float(1))
def play_marker(marker_file):
    send_message(Laptop, PORT, marker_file, float(1))

def play_stop():
    send_message(Laptop, PORT, ADDR_PLAY_STOP, float(1))

def OffSequence():
    send_message("192.168.254.229",8888, "/gma3/cmd", "Off RunningSequence")

def game_over():
    send_message(Laptop, PORT, ADDR_GAME_OVER_CUE, float(1))
    play_marker(MARKER_GAME_OVER)
    time.sleep(GAME_OVER_DELAY)
    play_stop()
def update_score_label():
    score_label.config(text=f"Score: {score}")

def go_to_stage_2():
    send_message(Laptop, PORT, ADDR_GO_TO_STAGE_2, float(1))
    time.sleep(2)  # Delay before starting Stage 2

def go_to_stage_3():
    send_message(Laptop, PORT, ADDR_GO_TO_STAGE_3, float(1))
    time.sleep(2)  # Delay before starting Stage 3
def hitlight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 3")
    time.sleep(HIT_MARKER_DELAY)

def loselight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 4")
    time.sleep(HIT_MARKER_DELAY)

def spotlight():
     send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 6")
     time.sleep(HIT_MARKER_DELAY) 

def start_game(stages):
    global score
    score = 0
    update_score_label()
    spotlight()
    try:
        for stage_num, stage_info in stages.items():
            print(f"Starting Stage {stage_num}")
            stage_completed = play_stage(stage_num, stage_info["cues"], stage_info["time_per_cue"])
            if stage_completed:
                score += 1
                update_score_label()
                if stage_num == 1:
                    print("Stage 1 complete. Preparing for Stage 2.")
                    spotlight()
                    go_to_stage_2()
                    play_stop()
                    time.sleep(2)
                    play_stop()
                elif stage_num == 2:
                    print("Stage 2 complete. Preparing for Stage 3.")
                    spotlight()
                    go_to_stage_3()
                    play_stop()
                    time.sleep(2)
                    play_stop()
                elif stage_num == 3:
                    print("Congratulations! You've completed all stages.")
                    play_marker(MARKER_WIN)
                    play_stop()
                    hitlight()
                    time.sleep(2)
                    play_stop()
                    time.sleep(5)
                    OffSequence()
                    break
            else:
                print(f"Stage {stage_num} failed. Game over!")
                break
    finally:
        GPIO.cleanup()
def play_stage(stage_num, cues, time_per_cue):
    missed_all = True  # Flag to track if all cues are missed in the stage

    for cue in range(cues):
        direction = random.choice(list(GPIO_DIRECTION_MAP.keys()))
        print(f"Stage {stage_num}, Cue {cue + 1}: Hit the {direction} board!")

        play_audio_cue(direction)
        play_stop()

        start_time = time.time()
        while time.time() - start_time < time_per_cue:
            if detect_motion(GPIO_DIRECTION_MAP[direction]):
                print(f"{direction} Board Hit!")
                hit_flags[direction] = True
                play_marker(MARKER_HIT)
                hitlight()
                time.sleep(HIT_MARKER_DELAY)
                play_stop()
                OffSequence()
                missed_all = False
                if stage_num == 3:
                    return True  # Win if any cue is hit in Stage 3
                break

        if missed_all and stage_num == 3:
            print(f"Stage {stage_num} failed. Game over!")
            loselight()
            game_over()
            
            time.sleep(5)
            OffSequence()
            return False
        elif missed_all:
            print(f"Missed the {direction} board. Proceeding to the next cue in Stage {stage_num}.")
            play_stop()
            time.sleep(CUE_DURATION)
        else:
            if stage_num == 1:
                next_stage = 2
            elif stage_num == 2:
                next_stage = 3
            else:
                next_stage = None
            
            if next_stage is not None:
                print(f"Stage {stage_num}, Cue {cue + 1} passed. Proceeding to Stage {next_stage}, Cue 1.")
                return True

    return True

# Main section to define the GUI and game logic
if __name__ == "__main__":
    # Create the Tkinter window
    root = tk.Tk()
    root.title("The Range")
    # Create the Start Game button
    start_button = tk.Button(root, text="Start Game", command=lambda: start_game(stages))
    start_button.pack(pady=10)

    # Create the score label
    score_label = tk.Label(root, text="Score: 0")
    score_label.pack(pady=10)

    # Initialize score variable
    score = 0

    # Define stages dictionary
    stages = {
        1: {"cues": 2, "time_per_cue": 10},
        2: {"cues": 2, "time_per_cue": 7},
        3: {"cues": 2, "time_per_cue": 5}
    }

    # Run the Tkinter event loop
    root.mainloop()

