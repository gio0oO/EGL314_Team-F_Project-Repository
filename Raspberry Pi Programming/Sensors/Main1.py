
import RPi.GPIO as GPIO
import time
import subprocess

# Constants
GPIO_VIBRATION_SENSOR_1 = 23  # Pin for sensor 1
GPIO_VIBRATION_SENSOR_2 = 26  # Pin for sensor 2 (added for increased sensitivity)
POLLING_INTERVAL = 0.0001  # 0.1 ms polling interval
CHECK_INTERVAL = 0.01  # 10 ms check interval
POLLING_COUNT = 1000  # Number of polls per detection check
DETECTION_THRESHOLD = 0.5  # Minimum detections needed from either sensor (adjusted for two sensors)
SCRIPT_PATH = "../reaper/marker_1.py"  # Path to the script to execute

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_VIBRATION_SENSOR_1, GPIO.IN)
GPIO.setup(GPIO_VIBRATION_SENSOR_2, GPIO.IN)

def detect_motion():
    """
    Checks both vibration sensors for micro vibrations.
    Returns True if motion is detected based on the detection threshold, otherwise False.
    """
    detection_count = 0
    for _ in range(POLLING_COUNT):
        # Check both sensors simultaneously for efficiency
        if GPIO.input(GPIO_VIBRATION_SENSOR_1) or GPIO.input(GPIO_VIBRATION_SENSOR_2):
            detection_count += 1
        time.sleep(POLLING_INTERVAL)

    # Adjust threshold based on using two sensors
    return detection_count >= DETECTION_THRESHOLD

try:
    while True:
        if detect_motion():
            print("Motion detected! Running another file...")
            try:
                # Execute the script "reaper/marker_1.py"
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
    print("Detection stopped by User.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    GPIO.cleanup()

