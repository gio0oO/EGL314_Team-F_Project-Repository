import tkinter as tk
import random

directions = ["North", "South", "East", "West"]

class DirectionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Direction Game")

        self.direction_label = tk.Label(root, text="", font=("Helvetica", 32))
        self.direction_label.grid(row=0, column=1, pady=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.result_label.grid(row=1, column=1, pady=10)

        self.timer_label = tk.Label(root, text="Time: 10", font=("Helvetica", 24))
        self.timer_label.grid(row=2, column=1, pady=10)

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 24))
        self.score_label.grid(row=3, column=1, pady=10)

        self.score = 0
        self.time_left = 10

        self.north_button = tk.Button(root, text="North", font=("Helvetica", 20),
                                      command=lambda: self.handle_button_press("North"))
        self.north_button.grid(row=4, column=1, padx=10, pady=10)

        self.south_button = tk.Button(root, text="South", font=("Helvetica", 20),
                                      command=lambda: self.handle_button_press("South"))
        self.south_button.grid(row=6, column=1, padx=10, pady=10)

        self.east_button = tk.Button(root, text="East", font=("Helvetica", 20),
                                     command=lambda: self.handle_button_press("East"))
        self.east_button.grid(row=5, column=2, padx=10, pady=10)

        self.west_button = tk.Button(root, text="West", font=("Helvetica", 20),
                                     command=lambda: self.handle_button_press("West"))
        self.west_button.grid(row=5, column=0, padx=10, pady=10)

        self.generate_direction()

    def generate_direction(self):
        self.current_direction = random.choice(directions)
        self.direction_label.config(text=self.current_direction)
        self.result_label.config(text="")
        self.time_left = 10
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.generate_direction()

    def handle_button_press(self, pressed_direction):
        if pressed_direction == self.current_direction:
            self.result_label.config(text="Hit!")
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.generate_direction()
        else:
            self.result_label.config(text="Miss!")

root = tk.Tk()
game = DirectionGame(root)
root.mainloop()
