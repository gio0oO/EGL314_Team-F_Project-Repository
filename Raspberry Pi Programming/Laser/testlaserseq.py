import tkinter as tk
from threading import Thread
from pythonosc import udp_client
import time
import subprocess

# Functions to control lasers
def send_message(receiver_ip, receiver_port, address, message):
    client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)
    client.send_message(address, message)
    print(f"Message '{message}' sent to {address}.")

def off_pattern(receiver_ip, receiver_port):
    for speaker in range(1, 13):
        for channel in range(1, 3):
            send_message(receiver_ip, receiver_port, "/print", f"{speaker},{channel},0")

# Functions to control NeoPixel lights
def send_color(receiver_ip, receiver_port, r, g, b):
    client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)
    client.send_message("/color", [r, g, b])
    print(f"Color set to ({r}, {g}, {b}).")

def send_brightness(receiver_ip, receiver_port, brightness):
    client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)
    client.send_message("/brightness", [brightness])
    print(f"Brightness set to {brightness}.")

# IP address and port of the receiving Raspberry Pi
PI_A_ADDR = "192.168.254.49"  # Change to your RPi's IP address
PORT = 2000

# New functions to control patterns on each side
def right_side_pattern():
    for speaker in [1, 2, 3]:
        for channel in range(1, 3):
            send_message(PI_A_ADDR, PORT, "/print", f"{speaker},{channel},1")

def back_side_pattern():
    for speaker in [4, 5, 6]:
        for channel in range(1, 3):
            send_message(PI_A_ADDR, PORT, "/print", f"{speaker},{channel},1")

def left_side_pattern():
    for speaker in [7, 8, 9]:
        for channel in range(1, 3):
            send_message(PI_A_ADDR, PORT, "/print", f"{speaker},{channel},1")

def front_side_pattern():
    for speaker in [10, 11, 12]:
        for channel in range(1, 3):
            send_message(PI_A_ADDR, PORT, "/print", f"{speaker},{channel},1")

# Function to control the laser show
def laser_show():
    pattern_duration = 5  # 5 seconds per pattern
    total_show_duration = 30  # Total show duration in seconds
    start_time = time.time()
    while time.time() - start_time < total_show_duration:
        right_side_pattern()
        time.sleep(pattern_duration)

       

        left_side_pattern()
        time.sleep(pattern_duration)

        front_side_pattern()
        time.sleep(pattern_duration)
    
   

# GUI setup
def start_show():
    # Start the laser show in a separate thread
    show_thread = Thread(target=laser_show)
    show_thread.start()
    # Run the tears.py and play.py scripts
    subprocess.Popen(["python3", "Laser/tears.py"])
    subprocess.Popen(["python3", "Laser/play.py"])

def stop_show():
    off_pattern(PI_A_ADDR, PORT)

root = tk.Tk()
root.title("Laser Show Controller")

start_button = tk.Button(root, text="Start Show", command=start_show)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Show", command=stop_show)
stop_button.pack(pady=10)

root.mainloop()
