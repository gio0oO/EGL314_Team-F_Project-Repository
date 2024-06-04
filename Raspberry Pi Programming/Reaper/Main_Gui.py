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

# Function to call corresponding marker script and play_stop.py
def run_marker_script(marker_number):
    script_name = f"{marker_folder}marker_{marker_number}.py" if marker_folder else f"marker_{marker_number}.py"
    if os.path.isfile(script_name):
        # Run the marker script using subprocess.run
        subprocess.run(["python3", script_name])
        # Run play_stop.py after the marker script
        subprocess.run(["python3", "play_stop.py"])
    else:
        print(f"File not found: {script_name}")

# Function to call corresponding sequence script
def run_sequence_script(sequence_number):
    script_name = os.path.join(grandma_folder, f"Sequence{sequence_number}.py")
    if os.path.isfile(script_name):
        # Run the sequence script using subprocess.run
        subprocess.run(["python3", script_name])
    else:
        print(f"File not found: {script_name}")

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
            hit_queue.put(output.strip().decode())
            print(f"Output from {script}: {output.strip().decode()}")  # Debugging line


# Function to flash the hit indicator
def flash_hit_indicator(iterations=5, delay=100):
    original_color = hit_indicator.cget("background")
    for i in range(iterations):
        window.after(i * delay, hit_indicator.config, {'bg': 'red'})
        window.after(i * delay + delay // 2, hit_indicator.config, {'bg': original_color})
    window.after(iterations * delay, hit_indicator.config, {'bg': original_color})



def reset_hit_indicator(original_color):
    hit_indicator.config(bg=original_color)

def check_hits():
    try:
        while not hit_queue.empty():
            message = hit_queue.get_nowait()
            print(f"Received message: {message}")  # Debugging line
            if "Message sent successfully." in message:
                print("Calling flash_hit_indicator()")  # Debugging line
                flash_hit_indicator()
    except queue.Empty:
        pass
    window.after(100, check_hits)



# Create the main window
window = tk.Tk()

# Set window title
window.title("Ninja Target Practice")

# Define button size (adjust as needed)
button_width = 10
button_height = 2

# Create buttons for markers in a loop
for row in range(2):
    for col in range(5):
        marker_number = row * 5 + col + 1
        button_text = f"Marker {marker_number}"
        button = tk.Button(window, text=button_text, width=button_width, height=button_height,
                           command=lambda num=marker_number: run_marker_script(num))
        button.grid(row=row, column=col)

# Add a gap below the marker buttons (adjust padding as needed)
window.grid_rowconfigure(2, minsize=20)  # Add padding below row 2

# Create buttons for sequences in a loop (first row)
sequence_numbers = [1, 2, 3, 4]  # List of sequence numbers for the first row
for col in range(4):
    sequence_number = sequence_numbers[col]
    button_text = f"Sequence {sequence_number}"
    button = tk.Button(window, text=button_text, width=button_width, height=button_height,
                       command=lambda num=sequence_number: run_sequence_script(num))
    button.grid(row=3, column=col)  # Place buttons in row 3

# Create buttons for sequences in a loop (second row)
sequence_numbers = [5, 6, 7, 8]  # List of sequence numbers for the second row (adjusted)
for col in range(4):
    sequence_number = sequence_numbers[col]
    button_text = f"Sequence {sequence_number}"
    button = tk.Button(window, text=button_text, width=button_width, height=button_height,
                       command=lambda num=sequence_number: run_sequence_script(num))
    button.grid(row=4, column=col)  # Place buttons in row 4

# Create the "Off" button
off_button = tk.Button(window, text="Off", width=button_width, height=button_height,
                       command=run_off_script)
off_button.grid(row=5, column=2)  # Adjust position as needed

# Create the "Start" button
start_button = tk.Button(window, text="Start", width=button_width, height=button_height,
                         command=run_start_scripts)
start_button.grid(row=6, column=2)  # Adjust position as needed

# Create the hit indicator
hit_indicator = tk.Label(window, text="Hit Indicator", width=button_width, height=button_height, relief="solid")
hit_indicator.grid(row=7, column=2)  # Adjust position as needed

# Start the main event loop
window.after(100, check_hits)
window.mainloop()
