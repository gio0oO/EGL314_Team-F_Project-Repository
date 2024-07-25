from pythonosc import udp_client
import tkinter as tk
import time
import threading

# Configuration for sending OSC messages
send_addr = '192.168.254.49'  # Replace with the actual IP address of your OSC server
send_port = 2000          # Replace with the actual port of your OSC server

PI_B_ADDR = "192.168.254.242"  # IP address of the Raspberry Pi controlling NeoPixel lights
NEOPIXEL_PORT = 2005

REAPER_ADDR = "192.168.254.30"  # Replace with your Reaper's IP address
REAPER_PORT = 7000

# Create OSC clients
neopixel_client = udp_client.SimpleUDPClient(PI_B_ADDR, NEOPIXEL_PORT)
reaper_client = udp_client.SimpleUDPClient(REAPER_ADDR, REAPER_PORT)

def send_message(client, address, message):
    try:
        client.send_message(address, message)
        print("Message sent:", message)
    except Exception as e:
        print(f"Message not sent: {str(e)}")

def send_color_array(colors):
    """Flatten the color array and send it to NeoPixels."""
    flattened_colors = [color for rgb in colors for color in rgb]
    try:
        neopixel_client.send_message('/color_array', flattened_colors)
        print("NeoPixel colors sent:", flattened_colors)
    except Exception as e:
        print(f"NeoPixel colors not sent: {str(e)}")

def snake_up_fast(total_duration=5):
    """Run a fast snake effect on NeoPixels with alternating colors."""
    num_pixels = 170  # Update to the number of NeoPixels
    delay = total_duration / num_pixels  # Calculate the delay to fit the total duration
    
    # Define the color sequence
    color_sequence = [(255, 0, 0), (255, 255, 255), (128, 0, 128), (0, 0, 255)]
    
    for i in range(num_pixels):
        if stop_flag:
            break
        frame = [(0, 0, 0)] * num_pixels
        frame[i] = color_sequence[i % len(color_sequence)]  # Alternate between colors
        send_color_array(frame)
        time.sleep(delay)

def strobe_effect(strobe_duration=0.05):
    """Run a strobe effect on NeoPixels with alternating colors."""
    num_pixels = 170  # Assuming you have 170 NeoPixels
    
    # Define the color sequence
    color_sequence = [(255, 0, 0), (255, 255, 255), (128, 0, 128), (0, 0, 255)]
    
    for _ in range(int(5 / strobe_duration)):  # Run for 5 seconds
        if stop_flag:
            break
        for color in color_sequence:
            frame = [color] * num_pixels
            send_color_array(frame)
            time.sleep(strobe_duration)
            frame = [(0, 0, 0)] * num_pixels
            send_color_array(frame)
            time.sleep(strobe_duration)

# Laser control functions
def front_lasers_on(value):
    for i in range(10, 13):
        msg = [f"{i},1,{value}"]
        send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)

def right_lasers_on(value):
    for i in range(1, 4, 2):
        msg = [f"{i},1,{value}"]
        send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)
    for i in range(2, 4, 2):
        msg = [f"{i},2,{value}"]
        send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)

def back_lasers_on(value):
    for i in range(4, 7, 2):
        msg = [f"{i},1,{value}"]
        send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)
    for i in range(5, 7, 2):
        msg = [f"{i},2,{value}"]
        send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)

def left_lasers_on(value):
    for i in range(7, 10, 2):
        msg = [f"{i},1,{value}"]
        send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)
    for i in range(8, 10, 2):
        msg = [f"{i},2,{value}"]
        send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)

def all_middle_lasers_on(value):
    for i in range(1, 7):
        if i % 2 == 0:
            msg = [f"{i},2,{value}"]
            send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)

def every_other_speaker_on(value):
    for i in [1, 3, 5, 7, 9, 12]:
        msg = [f"{i},1,{value}"]
        send_message(udp_client.SimpleUDPClient(send_addr, send_port), '/print', msg)

# Function to turn off all lasers
def turn_off_all_lasers():
    front_lasers_on(0)
    right_lasers_on(0)
    back_lasers_on(0)
    left_lasers_on(0)
    all_middle_lasers_on(0)
    every_other_speaker_on(0)

def run_neopixel_effects():
    global stop_flag
    stop_flag = False
    snake_up_fast(total_duration=5)
    strobe_effect(strobe_duration=0.05)

def jump_to_marker(marker_number):
    """Jump to a specified marker in Reaper."""
    send_message(reaper_client, "/marker/{}".format(marker_number), 1.0)

def trigger_play_stop():
    """Trigger Play/Stop action in Reaper."""
    send_message(reaper_client, "/action/40044", 1.0)

def start_show():
    global stop_flag
    stop_flag = False

    # Jump to marker 63 in Reaper before starting the music
    jump_to_marker(63)

    # Start NeoPixel effects in a separate thread
    neopixel_thread = threading.Thread(target=run_neopixel_effects)
    neopixel_thread.start()

    # Trigger Play/Stop in Reaper to start the music
    trigger_play_stop()

    # Define laser sequence for the 25-second show
    start_time = time.time()
    end_time = start_time + 25  # Set the end time to 25 seconds from start time

    while time.time() < end_time:
        front_lasers_on(1)
        time.sleep(2)  # Wait for 2 seconds
        turn_off_all_lasers()  # Turn off lasers

        right_lasers_on(1)
        time.sleep(2)  # Wait for 2 seconds
        turn_off_all_lasers()  # Turn off lasers

        back_lasers_on(1)
        time.sleep(2)  # Wait for 2 seconds
        turn_off_all_lasers()  # Turn off lasers

        left_lasers_on(1)
        time.sleep(2)  # Wait for 2 seconds
        turn_off_all_lasers()  # Turn off lasers

        all_middle_lasers_on(1)
        time.sleep(2)  # Wait for 2 seconds
        turn_off_all_lasers()  # Turn off lasers

        every_other_speaker_on(1)
        time.sleep(2)  # Wait for 2 seconds
        turn_off_all_lasers()  # Turn off lasers

    # Stop NeoPixel effects
    stop_flag = True
    neopixel_thread.join()

    # Stop the music by triggering Play/Stop in Reaper again
    trigger_play_stop()

    print("Show finished.")

# Setup UI function
def setup_ui():
    main = tk.Tk()
    main.title("Laser and NeoPixel Show Control")

    # Button to start the show
    start_button = tk.Button(main, text="Start Show", command=start_show)
    start_button.pack(pady=20)

    return main

# Main function to run the GUI
def main():
    root = setup_ui()
    root.mainloop()

if __name__ == "__main__":
    main()
