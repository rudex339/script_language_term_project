from tkinter import *
from tkinter import font
from main_data import *

class find_window:
    def __init__(self, name):
        gamename = str(self.search_entry.get())
        data = game_list_id_date(game_list_find(gamename))
        if not data:
            return
        window = Tk()
        window.title(data["name"])

        button = Button(window, text=str(data["price_overview"]["final"] + "구매"), command=lambda: self.purchase(data))
        button.grid(row=3, column=0)

        window.protocol("WM_DELETE_WINDOW", lambda: self.close_result_window(window))
        self.result_windows.append(window)
        window.mainloop()

    def close_result_window(self, value):
        value.destroy()
        self.result_windows.remove(value)