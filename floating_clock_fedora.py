import datetime
import time
import tkinter as tk
from tkinter import *


class Clock(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self["background"] = "#000000"

        x = round(self.winfo_screenwidth() / 2) - 65

        self.geometry(f"130x25+{x}+0")

        date_and_time = Label(
            self, font=("Ubuntu", 12), fg="white", background="#000000"
        )
        date_and_time.pack(padx=10, side=tk.LEFT)
        date_and_time.bind("<ButtonPress-1>", self.source)
        date_and_time.bind("<ButtonRelease-1>", self.target)
        date_and_time.bind("<B1-Motion>", self.move)

        def update_date_and_time():
            current_date = datetime.date.today().strftime("%b %d")
            current_time = time.strftime("%H:%M")
            date_and_time.config(text=f"{current_date}  {current_time}")
            date_and_time.after(1000, update_date_and_time)

        update_date_and_time()

    def move(self, event):
        x = self.winfo_x() + event.x - self.x
        y = self.winfo_y() + event.y - self.y
        self.geometry(f"+{x}+{y}")

    def source(self, event):
        self.x = event.x
        self.y = event.y

    def target(self, event):
        self.x = None
        self.y = None


app = Clock()

if __name__ == "__main__":
    app.mainloop()
