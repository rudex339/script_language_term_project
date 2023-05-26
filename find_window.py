from tkinter import *
from tkinter import messagebox

class FindWindow:
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()
        pass
    def __init__(self) -> None:
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
