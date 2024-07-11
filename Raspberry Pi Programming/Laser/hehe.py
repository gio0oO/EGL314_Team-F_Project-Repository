from pythonosc import udp_client
import time

def send_message(receiver_ip, receiver_port, address, message):
    try:
        # Create an OSC client to send messages
        client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)

        # Send an OSC message to the receiver
        client.send_message(address, message)

        print(f"Message '{message}' sent successfully to {receiver_ip}:{receiver_port}.")
    except Exception as e:
        print(f"Failed to send message '{message}' to {receiver_ip}:{receiver_port}. Error: {e}")

# FOR INFO: IP address and port of the receiving Raspberry Pi
PI_A_ADDR = "192.168.254.49"  # wlan ip
PORT = 2000
y = 0
addr = "/print"

msg = [
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

while y < len(msg):
    send_message(PI_A_ADDR, PORT, addr, msg[y])
    y += 1
    time.sleep(0.5)

print("Finished sending all messages.")
