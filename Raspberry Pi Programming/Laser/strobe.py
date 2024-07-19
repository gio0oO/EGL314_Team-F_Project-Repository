import tkinter as tk
from threading import Thread
from pythonosc import udp_client
import time
import random
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
def send_color(receiver_ip, receiver_port, r, g, b, brightness=255):
    client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)
    client.send_message("/color", [r, g, b, brightness])
    print(f"Color set to ({r}, {g}, {b}) with brightness {brightness}.")

def send_brightness(receiver_ip, receiver_port, brightness):
    client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)
    client.send_message("/brightness", [brightness])
    print(f"Brightness set to {brightness}.")

# IP address and port of the receiving Raspberry Pi
PI_A_ADDR = "192.168.254.49"  # Change to your RPi's IP address for lasers
PORT = 2000
PI_B_ADDR = "192.168.254.242"  # Change to your RPi's IP address for NeoPixel
NEOPIXEL_PORT = 2005

# Patterns for different sides
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

def custom_pattern():
    speakers = [1, 3, 4, 6, 7, 9, 10, 12]
    for speaker in speakers:
        for channel in range(1, 3):
            send_message(PI_A_ADDR, PORT, "/print", f"{speaker},{channel},1")

def random_laser():
    speaker = random.randint(1, 12)
    channel = random.randint(1, 2)
    send_message(PI_A_ADDR, PORT, "/print", f"{speaker},{channel},1")

# Function to control the laser show and NeoPixel lights
def laser_show():
    pattern_duration = 0.41  # 5 seconds per pattern
    total_show_duration = 30  # Total show duration in seconds
    colors = [(0, 0, 255), (128, 0, 128), (255, 0, 0)]  # Blue, Purple, Red
    color_index = 0
    brightness = 255  # Initial brightness level
    start_time = time.time()

    while time.time() - start_time < total_show_duration:
        right_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)], brightness)
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        back_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)], brightness)
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        left_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)], brightness)
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        front_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)], brightness)
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        custom_pattern()  # Activate custom pattern
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)], brightness)
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        # Randomly activate a single laser for effect
        random_laser()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)], brightness)
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

    off_pattern(PI_A_ADDR, PORT)
    send_color(PI_B_ADDR, NEOPIXEL_PORT, 0, 0, 0, 0)  # Turn off NeoPixel

# GUI setup
def start_show():
    # Start the laser show in a separate thread
    show_thread = Thread(target=laser_show)
    show_thread.start()
    
    # Run the tears.py and play.py scripts (adjust paths as needed)
    subprocess.Popen(["python3", "Raspberry Pi Programming/Laser/tears.py"])
    subprocess.Popen(["python3", "Raspberry Pi Programming/Laser/play.py"])

def stop_show():
    off_pattern(PI_A_ADDR, PORT)
    send_color(PI_B_ADDR, NEOPIXEL_PORT, 0, 0, 0, 0)  # Turn off NeoPixel

# Main GUI window
root = tk.Tk()
root.title("Laser Show Controller")

# Start and stop buttons
start_button = tk.Button(root, text="Start Show", command=start_show)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Show", command=stop_show)
stop_button.pack(pady=10)

root.mainloop()