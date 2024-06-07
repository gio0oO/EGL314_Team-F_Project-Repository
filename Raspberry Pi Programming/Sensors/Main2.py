import RPi.GPIO as GPIO
import time
import subprocess

# Constants
GPIO_VIBRATION_SENSOR = 24
POLLING_INTERVAL = 0.0001  # 0.1 ms
CHECK_INTERVAL = 0.01  # 10 ms
POLLING_COUNT = 1000
DETECTION_THRESHOLD = 0.001  # Fraction of detections needed to confirm motion
SCRIPT_PATH_MARKER = "../reaper/marker_6.py"  # Relative path as specified
SCRIPT_PATH_PLAY_STOP = "../reaper/play_stop.py"  # Relative path as specified
SCRIPT_PATH_SEQUENCE = "../grandma/Sequence3.py"  # Relative path as specified
SCRIPT_PATH_OFF_SEQUENCE = "../grandma/OffSequence.py"  # Relative path as specified

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
    return detection_count >= POLLING_COUNT * DETECTION_THRESHOLD

try:
    while True:
        if detect_motion():
            print("Motion detected! Running scripts...")

            try:
                # Execute marker_6.py
                print("Running marker_6.py...")
                subprocess.run(["python", SCRIPT_PATH_MARKER], check=True)
                print("marker_6.py execution completed.")

                # Execute sequence3.py
                print("Running sequence3.py...")
                subprocess.run(["python", SCRIPT_PATH_SEQUENCE], check=True)
                print("sequence3.py execution completed.")

                # Wait for 2 seconds and then run OffSequence.py
                print("Waiting for 2 seconds before running OffSequence.py...")
                time.sleep(2)
                print("Running OffSequence.py...")
                subprocess.run(["python", SCRIPT_PATH_OFF_SEQUENCE], check=True)
                print("OffSequence.py execution completed.")

                # Execute play_stop.py
                print("Running play_stop.py...")
                subprocess.run(["python", SCRIPT_PATH_PLAY_STOP], check=True)
                print("Script started. Waiting for 2 seconds...")
                time.sleep(2)  # Wait for 2 seconds

                # Run play_stop.py again
                print("Running play_stop.py again...")
                subprocess.run(["python", SCRIPT_PATH_PLAY_STOP], check=True)
                print("Second run of play_stop.py completed.")
            except subprocess.CalledProcessError as e:
                print(f"Subprocess error: {e}")
            except FileNotFoundError:
                print(f"File not found.")
            except Exception as e:
                print(f"An error occurred while running the script: {e}")
        else:
            print("No motion detected.")
        
        time.sleep(CHECK_INTERVAL)  # Check every CHECK_INTERVAL seconds

except KeyboardInterrupt:
    print("Detection stopped by User")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    GPIO.cleanup()


