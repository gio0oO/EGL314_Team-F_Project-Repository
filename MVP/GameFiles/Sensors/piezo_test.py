import RPi.GPIO as GPIO
import time

# Configure the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def detect_vibration(channel):
    print("Vibration detected!")

# Add an event detection on the piezo sensor pin
GPIO.add_event_detect(17, GPIO.RISING, callback=detect_vibration)

try:
    # Run indefinitely
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()