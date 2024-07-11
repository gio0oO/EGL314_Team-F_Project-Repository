import tkinter as tk
from tkinter import messagebox
from pythonosc import udp_client

# Define the IP address and port of the Master Pi OSC server
master_pi_ip = "192.168.254.49"  # Replace with the actual IP address of your Master Pi
master_pi_port = 2000  # Replace with the port number used by your Master Pi

# Function to send a test message to the Master Pi
def send_test_message():
    client = udp_client.SimpleUDPClient(master_pi_ip, master_pi_port)
    client.send_message("/print", "Hello From Team F Laptop")

# Function to run a test sequence using all lasers
def play_sequence():
    client = udp_client.SimpleUDPClient(master_pi_ip, master_pi_port)
    
    # Sequence to activate all lasers one by one
    sequence = [
        "1, 1, 1",  # Laser 1, Channel 1, On
        "1, 2, 1",  # Laser 1, Channel 2, On
        "2, 1, 1",  # Laser 2, Channel 1, On
        "2, 2, 1",  # Laser 2, Channel 2, On
        "3, 1, 1",  # Laser 3, Channel 1, On
        "3, 2, 1",  # Laser 3, Channel 2, On
        "4, 1, 1",  # Laser 4, Channel 1, On
        "4, 2, 1",  # Laser 4, Channel 2, On
        "5, 1, 1",  # Laser 5, Channel 1, On
        "5, 2, 1",  # Laser 5, Channel 2, On
        "6, 1, 1",  # Laser 6, Channel 1, On
        "6, 2, 1",  # Laser 6, Channel 2, On
        "7, 1, 1",  # Laser 7, Channel 1, On
        "7, 2, 1",  # Laser 7, Channel 2, On
        "8, 1, 1",  # Laser 8, Channel 1, On
        "8, 2, 1",  # Laser 8, Channel 2, On
        "9, 1, 1",  # Laser 9, Channel 1, On
        "9, 2, 1",  # Laser 9, Channel 2, On
        "10, 1, 1",  # Laser 10, Channel 1, On
        "10, 2, 1",  # Laser 10, Channel 2, On
        "11, 1, 1",  # Laser 11, Channel 1, On
        "11, 2, 1",  # Laser 11, Channel 2, On
        "12, 1, 1",  # Laser 12, Channel 1, On
        "12, 2, 1"   # Laser 12, Channel 2, On
    ]
    
    # Send each command in the sequence to activate all lasers
    for command in sequence:
        client.send_message("/trigger", command)
    
    messagebox.showinfo("Sequence Played", "Test sequence played using all lasers!")

# Create the main application window
root = tk.Tk()
root.title("Laser GUI")  # Set the window title

# Create buttons
button_play_sequence = tk.Button(root, text="Play Sequence", command=play_sequence)
button_play_sequence.pack(pady=10)

button_test_message = tk.Button(root, text="Test Message", command=send_test_message)
button_test_message.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
