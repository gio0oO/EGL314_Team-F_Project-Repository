import RPi.GPIO as GPIO
import time
import subprocess

# Constants
GPIO_VIBRATION_SENSOR = 24
POLLING_INTERVAL = 0.0001  # 0.1 ms
CHECK_INTERVAL = 0.01  # 10 ms
POLLING_COUNT = 1000
DETECTION_THRESHOLD = 0.1  # Number of detections needed to confirm motion
SCRIPT_PATH = "../reaper/marker_1.py"

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_VIBRATION_SENSOR, GPIO.IN)

def detect_motion():
    """
    Poll the vibration sensor multiple times to check for micro vibrations.
    Returns True if motion is detected based on the detection threshold, otherwise False.
    """
    detection_count = 0
    for _ in range(POLLING_COUNT):  # Poll the sensor POLLING_COUNT times
        if GPIO.input(GPIO_VIBRATION_SENSOR):
            detection_count += 1
        time.sleep(POLLING_INTERVAL)  # Wait for POLLING_INTERVAL between each poll
    return detection_count >= DETECTION_THRESHOLD

try:
    while True:
        if detect_motion():
            print("Motion detected! Running another file...")
            try:
                # Execute the file "reaper/marker_1.py"
                subprocess.run(["python", SCRIPT_PATH], check=True)
                print("File execution completed.")
            except subprocess.CalledProcessError as e:
                print(f"Subprocess error: {e}")
            except FileNotFoundError:
                print(f"File {SCRIPT_PATH} not found.")
        else:
            print("No motion detected.")
        
        time.sleep(CHECK_INTERVAL)  # Check every CHECK_INTERVAL seconds

except KeyboardInterrupt:
    print("Detection stopped by User")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    GPIO.cleanup()
 

