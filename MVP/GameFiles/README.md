# Sensors Repository

Welcome to the **Sensors** repository! Here, you will find a detailed guide on setting up and testing piezo sensors with your Raspberry Pi. Follow these steps to ensure a smooth setup and successful testing of your sensors.

## What You'll Need

- **Raspberry Pi 4**
- **Dupont wires**
- **Piezo sensor**

## Piezo Sensor Test Code for Raspberry Pi

This script allows you to test a piezo sensor connected to the GPIO pins of a Raspberry Pi. It detects vibrations and prints a message to the console whenever a vibration is detected.

### Prerequisites

Before running the test script, ensure that you have the `RPi.GPIO` library installed on your Raspberry Pi. If it's not already installed, you can install it using pip:

```sh
pip install RPi.GPIO
```

### Wiring the Piezo Sensor

Follow these steps to connect your piezo sensor to the Raspberry Pi:

1. **Connect one terminal** of the piezo sensor to **GPIO pin 17** (or another GPIO pin of your choice).
2. **Connect the other terminal** of the piezo sensor to a **GND (ground) pin** on the Raspberry Pi.

### Running the Script

To test your piezo sensor, follow these instructions:

1. **Connect the Piezo Sensor:** Ensure that the piezo sensor is connected as described in the [Wiring] section.
2. **Run the Script:**
   - Open a terminal on your Raspberry Pi.
   - Navigate to the directory where you saved the `piezo_test.py` script.
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
