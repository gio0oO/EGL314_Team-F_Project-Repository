import tkinter as tk
from pythonosc import udp_client
import time
from reaper import send_message

# Set the IP and port of the OSC server (the Raspberry Pi running your NeoPixel control code)
SERVER_IP = "192.168.254.242"  # Change to your RPi's IP address
SERVER_PORT = 2005

# Set the IP and port for the second pi
SERVER_IP2 = "192.168.254.102"  # Change to your RPi's IP address
SERVER_PORT2 = 2006

Laptop = "192.168.254.30"
PORT = 7000

PI_A_ADDR = "192.168.254.49"  # IP address of the Raspberry Pi controlling lasers
LASER_PORT = 2000

ADDR_PLAY_STOP = "/action/40044"  # Address for Play_Stop
ADDR_LASER_MARKER = "/marker/63"

# Create an OSC client
client = udp_client.SimpleUDPClient(SERVER_IP, SERVER_PORT)
client2 = udp_client.SimpleUDPClient(SERVER_IP2, SERVER_PORT2)
laser_client = udp_client.SimpleUDPClient(PI_A_ADDR, LASER_PORT)

def send_message1(client, address, message):
    try:
        client.send_message(address, message)
        print(f"Message '{message}' sent to {address}.")
    except Exception as e:
        print(f"Message not sent: {e}")

def play_stop():
    send_message(Laptop, PORT, ADDR_PLAY_STOP, float(1))

def go_to_laser_marker():
    send_message(Laptop, PORT, ADDR_LASER_MARKER, float(1))
    time.sleep(2)  # Delay before starting Stage 2

def OffSequence():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Off RunningSequence")

def firstlight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 7")

def lastlight():
    send_message("192.168.254.229", 8888, "/gma3/cmd", "Go+: Sequence 9")

def front_side_pattern():
    for speaker in [2, 5, 8, 11]:
        for channel in range(1, 3):
            send_message1(laser_client, "/print", f"{speaker},{channel},1")

def off_pattern():
    for speaker in range(1, 13):
        for channel in range(1, 3):
            send_message1(laser_client, "/print", f"{speaker},{channel},0")

def send_color_array(colors):
    address = "/color_array"
    flattened_colors = [color for rgb in colors for color in rgb]
    client.send_message(address, flattened_colors)
    print(f"Sent color array: {flattened_colors}")

def send_brightness(brightness):
    client.send_message("/brightness", brightness)
    print(f"Sent brightness {brightness}")

def send_off():
    client.send_message("/off", [])
    print("Sent off message")

def send_color_array2(colors):
    address = "/color_array"
    flattened_colors = [color for rgb in colors for color in rgb]
    client2.send_message(address, flattened_colors)
    print(f"Sent color array: {flattened_colors}")

def send_brightness2(brightness):
    client2.send_message("/brightness", brightness)
    print(f"Sent brightness {brightness}")

def send_off2():
    client2.send_message("/off", [])
    print("Sent off message")

def light_up_pixels_one_by_one(colors, delay):
    for i in range(len(colors)):
        colors[i] = (255, 255, 255)  # Change to desired color
        send_color_array(colors)
        time.sleep(delay)

def strobe_effect(strobe_colors, strobe_duration, strobe_delay):
    end_time = time.time() + strobe_duration
    while time.time() < end_time:
        for color in strobe_colors:
            send_color_array([color] * 170)  # Balloon NeoPixels strobe
            send_color_array2([color] * 170)  # Truss NeoPixels strobe
            time.sleep(strobe_delay)
            send_off()
            time.sleep(strobe_delay)

def start():
    play_stop()
    go_to_laser_marker()
    firstlight()
    time.sleep(12)
    OffSequence()

    front_side_pattern()
    time.sleep(10)
    off_pattern()

def start_show():
    try:
        play_stop()
        go_to_laser_marker()
        
        # Run firstlight for 10 seconds, then turn it off
        firstlight()
        time.sleep(16)
        OffSequence()

        # Run front_side_pattern for 13 seconds
        front_side_pattern()
        time.sleep(6)
        off_pattern()

        # Light up each pixel one by one for 26.5 seconds
        colors = [(0, 0, 0)] * 170
        light_up_pixels_one_by_one(colors, 26.5 / 170)

        # Strobe effect on both balloon and truss NeoPixels
        strobe_effect([(128, 0, 128), (0, 0, 255), (255, 0, 0)], 20, 0.2)

        # Optionally turn off all lights after the strobe effect
        lastlight()
        time.sleep(10)
    
        send_off()
        play_stop()
        
    except Exception as e:
        print(f"Error: {e}")

def stop_show():
    send_off()
    send_off2()
    play_stop()
    OffSequence()
    off_pattern()

# Create the tkinter window
root = tk.Tk()
root.title("Light Show Controller")

# Create and place the buttons
start_button = tk.Button(root, text="Start Show", command=start_show)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Show", command=stop_show)
stop_button.pack(pady=10)

# Run the tkinter main loop
root.mainloop()
