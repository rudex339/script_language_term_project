from tkinter import *
import find_window

class MainGui:
    def __init__(self) -> None:
        self.search_window = Tk()
        self.find_windows=find_window.FindWindow()
        self.search_window.mainloop()


MainGui()
        