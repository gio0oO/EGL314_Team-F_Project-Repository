# Game Codes Repository

Welcome to the **Game Codes** repository! This is your go-to place for all relevant codes and setup instructions related to our game project.

## Repository Overview

This repository includes:

- **Game Code:** The code that runs the game, including detailed instructions on how to set it up and execute it.
- **Sensor Test Code:** The code to test the sensors and ensure they are functioning correctly.

## Prerequisites

Ensure you have the following:

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
pip3 install <package_name>
```

To deactivate the virtual environment when you're done, run:

```sh
deactivate
```

## Main Files

These are the 2 main files that you need to run the whole game:

- [Main.py](./Main.py)
- [reaper_py](./reaper_py)

### Main.py

The `Main.py` script is the primary file that runs the game. Below is an explanation of the sequences we used, what they're for, and which marker we paired them up with:

- **Sequence 1: Intro**
  - Paired with `marker_3.py`
  - This sequence serves as the introduction to the game.

- **Sequence 2: Background**
  - Paired with `marker_1.py`
  - This sequence provides the background ambiance throughout the game.

- **Sequence 3: Hit correct target**
  - Paired with `marker_10.py`
  - This sequence is triggered when the player hits the correct target.

- **Sequence 4: Hit wrong target**
  - Paired with `marker_8.py`
  - This sequence is triggered when the player hits the wrong target.

- **Sequence 5: Rules spotlight**
  - Paired with `marker_70.py`
  - This sequence highlights the rules of the game.

- **Sequence 6: Spotlight for targets**
  - Paired with `marker_2.py`
  - This sequence focuses the spotlight on the targets.

For detailed setup guides and code explanations, refer to the links above. If you have any questions or need further assistance, feel free to reach out.

Happy coding!
