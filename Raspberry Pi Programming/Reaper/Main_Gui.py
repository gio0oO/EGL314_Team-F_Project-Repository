import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import threading
import queue

# Define paths (adjust if needed)
marker_folder = ""  # Set folder path for marker scripts (optional)
grandma_folder = "../grandma"  # Set path for sequence scripts
sensors_folder = "../Sensors"  # Set path for sensors scripts

# Queue to communicate between threads
hit_queue = queue.Queue()

# Function to call marker and sequence scripts in order
def run_sequence_and_marker(sequence_number, marker_number=None):
    sequence_script = os.path.join(grandma_folder, f"Sequence{sequence_number}.py")
    marker_script = os.path.join(marker_folder, f"marker_{marker_number}.py") if marker_number else None
    
    if os.path.isfile(sequence_script):
        subprocess.run(["python3", sequence_script])
    else:
        print(f"File not found: {sequence_script}")
    
    if marker_script and os.path.isfile(marker_script):
        subprocess.run(["python3", marker_script])
        subprocess.run(["python3", "play_stop.py"])
    elif marker_script:
        print(f"File not found: {marker_script}")

# Function to run OffSequence.py
def run_off_script():
    script_name = os.path.join(grandma_folder, "OffSequence.py")
    if os.path.isfile(script_name):
        subprocess.run(["python3", script_name])
    else:
        print(f"File not found: {script_name}")

# Function to run Main_1.py and Main_2.py
def run_start_scripts():
    script_1 = os.path.join(sensors_folder, "Main1.py")
    script_2 = os.path.join(sensors_folder, "Main2.py")
    if os.path.isfile(script_1) and os.path.isfile(script_2):
        threading.Thread(target=run_script, args=(script_1,)).start()
        threading.Thread(target=run_script, args=(script_2,)).start()
    else:
        print(f"File not found: {script_1} or {script_2}")

def run_script(script):
    process = subprocess.Popen(["python3", script], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            message = output.strip().decode()
            hit_queue.put(message)
            print(f"Output from {script}: {message}")  # Debugging line

# Function to flash the hit indicator
def flash_hit_indicator(iterations=5, delay=100):
    original_color = hit_indicator.cget("background")
    for i in range(iterations):
        window.after(i * delay, lambda: hit_indicator.config(bg='red'))
        window.after(i * delay + delay // 2, lambda: hit_indicator.config(bg=original_color))
    window.after(iterations * delay, lambda: hit_indicator.config(bg=original_color))

def check_hits():
    try:
        while not hit_queue.empty():
            message = hit_queue.get_nowait()
            print(f"Received message: {message}")  # Debugging line
            if "Message sent successfully." in message:
                print("Calling flash_hit_indicator()")  # Debugging line
                window.after(0, flash_hit_indicator)
    except queue.Empty:
        pass
    window.after(100, check_hits)

# Create the main window
window = tk.Tk()
# Set window title
window.title("Ninja Target Practice")

# Define button size (adjust as needed)
button_width = 15
button_height = 2
pad_x = 10
pad_y = 10

# Create the buttons with their respective commands
buttons = [
    ("Intro", 1, 1),
    ("Background", 2, 1),
    ("Game Over", 5, 9),
    ("Hit", 3, 6),
    ("Wrong", 4, 7),
    ("Left Side", None, 5),
    ("Center", None, 4),
    ("Right Side", None, 3),
    ("Spotlight", 1, 9)  # New Spotlight button
]

# Place the first row of buttons
for idx, (text, sequence, marker) in enumerate(buttons[:4]):
    button = tk.Button(window, text=text, width=button_width, height=button_height,
                       command=lambda seq=sequence, mark=marker: run_sequence_and_marker(seq, mark))
    button.grid(row=0, column=idx, padx=pad_x, pady=pad_y)

# Place the second row of buttons
for idx, (text, sequence, marker) in enumerate(buttons[4:6]):
    button = tk.Button(window, text=text, width=button_width, height=button_height,
                       command=lambda seq=sequence, mark=marker: run_sequence_and_marker(seq, mark))
    button.grid(row=1, column=idx, padx=pad_x, pady=pad_y)

# Place the third row of buttons
for idx, (text, sequence, marker) in enumerate(buttons[6:8]):
    button = tk.Button(window, text=text, width=button_width, height=button_height,
                       command=lambda seq=sequence, mark=marker: run_sequence_and_marker(seq, mark))
    button.grid(row=2, column=idx, padx=pad_x, pady=pad_y)

# Place the Spotlight button
spotlight_button = tk.Button(window, text="Spotlight", width=button_width, height=button_height,
                             command=lambda: run_sequence_and_marker(1, 9))
spotlight_button.grid(row=2, column=2, padx=pad_x, pady=pad_y)  # Adjust position as needed

# Create the "Off" button
off_button = tk.Button(window, text="Off", width=button_width, height=button_height,
                       command=run_off_script)
off_button.grid(row=3, column=1, padx=pad_x, pady=pad_y)  # Adjust position as needed

# Create the "Start" button
start_button = tk.Button(window, text="Start", width=button_width, height=button_height,
                         command=run_start_scripts)
start_button.grid(row=4, column=1, padx=pad_x, pady=pad_y)  # Adjust position as needed

# Create the hit indicator
hit_indicator = tk.Label(window, text="Hit Indicator", width=button_width, height=button_height, relief="solid")
hit_indicator.grid(row=5, column=1, padx=pad_x, pady=pad_y)  # Adjust position as needed

# Start the main event loop
window.after(100, check_hits)
window.mainloop()
