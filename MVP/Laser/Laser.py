import tkinter as tk
from pythonosc import udp_client
import time

# Laser control IP address and port (replace with actual IPs and ports)
PI_A_ADDR = "192.168.254.49"  # IP address of the Raspberry Pi controlling lasers
LASER_PORT = 2000
PI_B_ADDR = "192.168.254.242"  # IP address of the Raspberry Pi controlling NeoPixel lights
NEOPIXEL_PORT = 2005
REAPER_ADDR = "192.168.254.30"  # Replace with your Reaper's IP address
REAPER_PORT = 7000

# Create OSC clients
laser_client = udp_client.SimpleUDPClient(PI_A_ADDR, LASER_PORT)
neopixel_client = udp_client.SimpleUDPClient(PI_B_ADDR, NEOPIXEL_PORT)
reaper_client = udp_client.SimpleUDPClient(REAPER_ADDR, REAPER_PORT)

################################# Laser Functions #################################

def send_message(client, address, message):
    """Send a message via OSC and handle errors."""
    try:
        client.send_message(address, message)
        print(f"Message '{message}' sent to {address}.")
    except Exception as e:
        print(f"Message not sent: {e}")

def off_pattern(client):
    """Turn off all lasers."""
    print("Turning off all lasers.")
    for speaker in range(1, 13):
        for channel in range(1, 3):
            send_message(client, "/print", f"{speaker},{channel},0")

def right_side_pattern(client):
    """Activate the right side pattern."""
    print("Activating right side pattern.")
    for speaker in [1, 2, 3]:
        for channel in range(1, 3):
            send_message(client, "/print", f"{speaker},{channel},1")

def back_side_pattern(client):
    """Activate the back side pattern."""
    print("Activating back side pattern.")
    for speaker in [4, 5, 6]:
        for channel in range(1, 3):
            send_message(client, "/print", f"{speaker},{channel},1")

def left_side_pattern(client):
    """Activate the left side pattern."""
    print("Activating left side pattern.")
    for speaker in [7, 8, 9]:
        for channel in range(1, 3):
            send_message(client, "/print", f"{speaker},{channel},1")

def front_side_pattern(client):
    """Activate the front side pattern."""
    print("Activating front side pattern.")
    for speaker in [10, 11, 12]:
        for channel in range(1, 3):
            send_message(client, "/print", f"{speaker},{channel},1")

def custom_pattern(client):
    """Activate the custom laser pattern."""
    print("Activating custom pattern.")
    speakers = [1, 3, 4, 6, 7, 9, 10, 12]
    for speaker in speakers:
        for channel in range(1, 3):
            send_message(client, "/print", f"{speaker},{channel},1")

def all_on_off_pattern(client):
    """Activate all-on and all-off pattern."""
    print("Activating all on and off pattern.")
    for speaker in range(1, 13):
        for channel in range(1, 3):
            send_message(client, "/print", f"{speaker},{channel},1")
    time.sleep(1)
    for speaker in range(1, 13):
        for channel in range(1, 3):
            send_message(client, "/print", f"{speaker},{channel},0")

################################# NeoPixel Functions #################################

def send_color_array(colors):
    """Send an array of colors to the NeoPixel client."""
    address = "/color_array"
    flattened_colors = [color for rgb in colors for color in rgb]
    neopixel_client.send_message(address, flattened_colors)
    print(f"Sent color array: {flattened_colors}")

def send_brightness(brightness):
    """Send brightness value to NeoPixel client."""
    neopixel_client.send_message("/brightness", brightness)
    print(f"Sent brightness {brightness}")

def send_off_neopixel():
    """Send off command to NeoPixel client."""
    neopixel_client.send_message("/off", [])
    print("Sent off message")

def snake_up_fast(colors, total_duration=5):
    """Run a fast snake effect on NeoPixels."""
    print("Running fast snake effect.")
    num_pixels = len(colors)
    delay = total_duration / num_pixels  # Calculate the delay to fit the total duration
    for i in range(num_pixels):
        frame = [(0, 0, 0)] * num_pixels
        frame[i] = colors[i]
        send_color_array(frame)
        time.sleep(delay)

def strobe_effect(colors, strobe_duration=0.05):
    """Run a strobe effect on NeoPixels."""
    print("Running strobe effect.")
    num_pixels = 170  # Assuming you have 170 NeoPixels
    for _ in range(int(5 / strobe_duration)):  # Run for 5 seconds
        for color in colors:
            frame = [color] * num_pixels
            send_color_array(frame)
            time.sleep(strobe_duration)
            frame = [(0, 0, 0)] * num_pixels
            send_color_array(frame)
            time.sleep(strobe_duration)

################################# Light Show #################################

def light_show():
    """Run the light show sequence."""
    pattern_duration = 3  # Duration per laser pattern in seconds
    total_show_duration = 5  # Total show duration in seconds
    start_time = time.time()

    # Jump to Marker One in Reaper
    send_message(reaper_client, "/marker/63", 1.0)

    # Trigger Play in Reaper
    send_message(reaper_client, "/action/40044", 1.0)

    # First 5 seconds: Fast snake effect
    colors = [(255, 0, 0)] * 57 + [(0, 255, 0)] * 56 + [(0, 0, 255)] * 57
    snake_up_fast(colors, total_duration=5)

    # Strobe effect with Purple, Red, White
    strobe_colors = [(128, 0, 128), (255, 0, 0), (255, 255, 255)]  # Purple, Red, White
    strobe_effect(strobe_colors, strobe_duration=0.05)  # Faster strobe

    elapsed_time = time.time() - start_time

    # Run patterns until the total show duration is reached
    while elapsed_time < total_show_duration:
        # Run right side pattern for 3 seconds
        print("Running right side pattern.")
        right_side_pattern(laser_client)
        colors = [(255, 0, 0)] * 57 + [(0, 255, 0)] * 56 + [(0, 0, 255)] * 57
        send_color_array(colors)
        time.sleep(pattern_duration)
        off_pattern(laser_client)

        # Update elapsed time
        elapsed_time = time.time() - start_time
        if elapsed_time >= total_show_duration:
            break

        # Run back side pattern for 3 seconds
        print("Running back side pattern.")
        back_side_pattern(laser_client)
        colors = [(0, 255, 0)] * 57 + [(0, 0, 255)] * 56 + [(255, 0, 0)] * 57
        send_color_array(colors)
        time.sleep(pattern_duration)
        off_pattern(laser_client)

        # Update elapsed time
        elapsed_time = time.time() - start_time
        if elapsed_time >= total_show_duration:
            break

        # Run left side pattern for 3 seconds
        print("Running left side pattern.")
        left_side_pattern(laser_client)
        colors = [(0, 0, 255)] * 57 + [(255, 0, 0)] * 56 + [(0, 255, 0)] * 57
        send_color_array(colors)
        time.sleep(pattern_duration)
        off_pattern(laser_client)

        # Update elapsed time
        elapsed_time = time.time() - start_time
        if elapsed_time >= total_show_duration:
            break

        # Run front side pattern for 3 seconds
        print("Running front side pattern.")
        front_side_pattern(laser_client)
        colors = [(255, 255, 0)] * 57 + [(0, 255, 255)] * 56 + [(255, 0, 255)] * 57
        send_color_array(colors)
        time.sleep(pattern_duration)
        off_pattern(laser_client)

        # Update elapsed time
        elapsed_time = time.time() - start_time
        if elapsed_time >= total_show_duration:
            break

        # Run custom pattern for 3 seconds
        print("Running custom pattern.")
        custom_pattern(laser_client)
        colors = [(255, 0, 0)] * 57 + [(0, 255, 0)] * 56 + [(0, 0, 255)] * 57
        send_color_array(colors)
        time.sleep(pattern_duration)
        off_pattern(laser_client)

        # Update elapsed time
        elapsed_time = time.time() - start_time

    # Ensure everything is turned off at the end of the show
    print("Turning off all lasers and NeoPixels.")
    off_pattern(laser_client)
    send_off_neopixel()

# GUI Setup
root = tk.Tk()
root.title("Laser Light Show")

start_button = tk.Button(root, text="Start Light Show", command=light_show)
start_button.pack(pady=20)

root.mainloop()
