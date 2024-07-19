import tkinter as tk
from pythonosc import udp_client
import time

# Functions to control lasers and NeoPixel lights
def send_message(receiver_ip, receiver_port, address, message):
    try:
        client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)
        client.send_message(address, message)
        print(f"Message '{message}' sent to {address}.")
    except Exception as e:
        print(f"Message not sent: {e}")

def off_pattern(receiver_ip, receiver_port):
    for speaker in range(1, 13):
        for channel in range(1, 3):
            send_message(receiver_ip, receiver_port, "/print", f"{speaker},{channel},0")

def send_color(receiver_ip, receiver_port, r, g, b):
    try:
        client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)
        client.send_message("/color", [r, g, b])
        print(f"Color set to ({r}, {g}, {b}).")
    except Exception as e:
        print(f"Color not set: {e}")

# IP address and port of the receiving Raspberry Pi and Reaper
PI_A_ADDR = "192.168.254.49"  # Change to your RPi's IP address for lasers
PORT = 2000
PI_B_ADDR = "192.168.254.242"  # Change to your RPi's IP address for NeoPixel
NEOPIXEL_PORT = 2005
REAPER_ADDR = "192.168.254.30"  # Change to your Reaper's IP address
REAPER_PORT = 7000

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

# Function to control the laser show, NeoPixel lights, and Reaper
def laser_show():
    pattern_duration = 0.41  # 5 seconds per pattern
    total_show_duration = 30  # Total show duration in seconds
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
    color_index = 0
    start_time = time.time()

    # Jump to Marker One in Reaper
    send_message(REAPER_ADDR, REAPER_PORT, "/marker/63", 1.0)

    # Trigger Play in Reaper
    send_message(REAPER_ADDR, REAPER_PORT, "/action/40044", 1.0)

    while time.time() - start_time < total_show_duration:
        right_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)])
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        back_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)])
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        left_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)])
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        front_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)])
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        custom_pattern()  # Activate custom pattern
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)])
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        front_side_pattern()
        back_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)])
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

        left_side_pattern()
        right_side_pattern()
        send_color(PI_B_ADDR, NEOPIXEL_PORT, *colors[color_index % len(colors)])
        color_index += 1
        time.sleep(pattern_duration)
        off_pattern(PI_A_ADDR, PORT)

    off_pattern(PI_A_ADDR, PORT)
    send_color(PI_B_ADDR, NEOPIXEL_PORT, 0, 0, 0)  # Turn off NeoPixel

# GUI setup
def start_show():
    laser_show()

def stop_show():
    off_pattern(PI_A_ADDR, PORT)
    send_color(PI_B_ADDR, NEOPIXEL_PORT, 0, 0, 0)  # Turn off NeoPixel

# Main GUI window
root = tk.Tk()
root.title("Laser Show Controller")

# Start and stop buttons
start_button = tk.Button(root, text="Start Show", command=start_show)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Show", command=stop_show)
stop_button.pack(pady=10)

root.mainloop()
