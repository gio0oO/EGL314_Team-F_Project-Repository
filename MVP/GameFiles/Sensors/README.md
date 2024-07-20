# Sensors Repository

Welcome to the **Sensors** repository! Here, you will find a detailed guide on setting up and testing piezo sensors with your Raspberry Pi. Follow these steps to ensure a smooth setup and successful testing of your sensors.

## What You'll Need

- **Raspberry Pi 4**
- **Dupont wires**
- **Piezo sensor**

## Setting Up

### Update Your Raspberry Pi

First, make sure your Raspberry Pi is up-to-date. Open a terminal and run:

```sh
sudo apt update
sudo apt upgrade
```

If the update and/or upgrade is unsuccessful, manually set the date and time by running:

```sh
sudo date -s 'YYYY-MM-DD HH:MM:SS'
```

### Setting Up a Virtual Environment

To install the Virtual Environment, run:

```sh
sudo apt install virtualenv python3-virtualenv -y
```

To create a new virtual environment, use:

```sh
virtualenv -p /usr/bin/python3 <environment_name>
```

**Note:** `<environment_name>` is the name of the folder where the virtual environment will be created.

To activate the virtual environment, run:

```sh
source <environment_folder>/bin/activate
```

To install a package within the virtual environment, use pip:

```sh
pip3 install python-osc
```

To deactivate the virtual environment when you're done, run:

```sh
deactivate
```

## Piezo Sensor Test Code for Raspberry Pi

This script allows you to test a piezo sensor connected to the GPIO pins of your Raspberry Pi. It detects vibrations and prints a message to the console whenever a vibration is detected.

### Creating the Test Script

Create a new file named `piezo_test.py` in your project directory with the following content:

```python
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
```

### Running the Script

To test your piezo sensor, follow these instructions:

1. **Connect the Piezo Sensor:** Ensure that the piezo sensor is connected as described in the [Wiring] section.
2. **Run the Script:**
   - Open a terminal on your Raspberry Pi.
   - Navigate to the directory where you saved the `piezo_test.py` script.
   - Ensure your virtual environment is activated (refer to the [Setting Up] section).
   - Execute the script using Python:

     ```sh
     python piezo_test.py
     ```

When you run this script, it will print `"Vibration detected!"` to the console each time it detects a vibration on the piezo sensor. You can test this by tapping on or vibrating the sensor.

**Note:** If you're using a different GPIO pin, replace `17` in the script with your specific GPIO pin number. The script utilizes the BCM pin numbering scheme.

## Additional Resources

- [Raspberry Pi GPIO Pinout](https://pinout.xyz/): A helpful reference for GPIO pin numbers and configurations.
- [RPi.GPIO Documentation](https://pypi.org/project/RPi.GPIO/): Official documentation for the RPi.GPIO library.

Feel free to reach out with any questions or issues you encounter. Happy testing!
