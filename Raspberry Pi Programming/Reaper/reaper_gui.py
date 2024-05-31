import tkinter as tk
import subprocess

class StealthWalkingApp:
    def __init__(self, master):
        self.master = master
        master.title("Stealth Walking")

        # Stealth Walking Label
        stealth_label = tk.Label(master, text="Stealth Walking")
        stealth_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create buttons for Start, Win, Lose
        self.create_marker_buttons(row=1)

        # Labels for Wind and Bamboo
        wind_label = tk.Label(master, text="Wind")
        wind_label.grid(row=2, column=0, padx=5, pady=5)

        bamboo_label = tk.Label(master, text="Bamboo")
        bamboo_label.grid(row=3, column=0, padx=5, pady=5)

        # Create buttons for Wind and Bamboo
        self.create_wind_bamboo_buttons(row=2, column_start=1)
        self.create_wind_bamboo_buttons(row=3, column_start=1)

        # Play button
        self.is_playing = False
        self.play_button = tk.Button(master, text="Play", width=10, command=self.toggle_play)
        self.play_button.grid(row=4, columnspan=3, pady=10)

    def create_marker_buttons(self, row):
        """Create buttons for Start, Win, Lose markers."""
        marker_names = ["Start", "Win", "Lose"]
        script_numbers = [1, 8, 10]  # Update the script number for Win to 8
        for i, (name, script_number) in enumerate(zip(marker_names, script_numbers)):
            marker_button = tk.Button(self.master, text=name, width=10,
                                      command=lambda script_number=script_number: self.run_script(script_number))
            marker_button.grid(row=row, column=i, padx=5, pady=5)

    def create_wind_bamboo_buttons(self, row, column_start):
        """Create buttons for Wind and Bamboo markers."""
        marker_names = ["Start", "Middle", "End"]
        script_numbers = [2, 3, 4] if row == 2 else [5, 6, 7]
        for i, (name, script_number) in enumerate(zip(marker_names, script_numbers)):
            marker_button = tk.Button(self.master, text=name, width=10,
                                      command=lambda script_number=script_number: self.run_script(script_number))
            marker_button.grid(row=row, column=column_start + i, padx=5, pady=5)

    def run_script(self, script_number):
        """Execute a script corresponding to the marker button pressed."""
        script_name = f"marker_{script_number}.py"
        subprocess.run(["python", script_name])

    def toggle_play(self):
        """Toggle play and stop functionality."""
        if self.is_playing:
            self.play_button.config(text="Play")
            subprocess.run(["python", "play_stop.py", "stop"])
        else:
            self.play_button.config(text="Stop")
            subprocess.run(["python", "play_stop.py", "play"])
        self.is_playing = not self.is_playing

if __name__ == "__main__":
    root = tk.Tk()
    app = StealthWalkingApp(root)
    root.mainloop()

