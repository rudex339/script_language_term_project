from tkinter import *
from main_data import *


class MainGui:
    result_windows= []
    def __init__(self) -> None:
        self.search_window = Tk()
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')
        #검색 entry
        self.search_entry = Entry(self.search_window,font=self.TempFont)
        self.search_entry.grid(row=0,column=0)
        #검색 button
        Button(self.search_window, text="검색", 
                font=self.TempFont,command= lambda: self.open_find_window("find")).grid(row=0,column=1)
        
        self.search_window.protocol("WM_DELETE_WINDOW", self.close_search_window)
        self.search_window.mainloop()
    
    def open_find_window(self, data):
        window = Tk()
        Label(window, text=str(self.start), font=self.TempFont).grid(row=0, column=0)

        window.protocol("WM_DELETE_WINDOW", lambda: self.close_result_window(window))
        self.result_windows.append(window)
        window.mainloop()
    
    def close_search_window(self):
        for window in self.result_windows:
            window.destroy()
        self.result_windows.clear()

        self.search_window.destroy()
    
    def close_result_window(self, value):
        value.destroy()
        self.result_windows.remove(value)

    
        



MainGui()
        