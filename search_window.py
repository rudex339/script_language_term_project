from tkinter import *
from tkinter import font
import urllib
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO

from main_data import *

class MainGui:
    result_windows= []
    def __init__(self) -> None:
        self.search_window = Tk()
        self.search_window.title("게임 영수증")
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')
        #검색 entry
        self.search_entry = Entry(self.search_window,font=self.TempFont)
        self.search_entry.grid(row=0, column=0)

        # 검색 button
        Button(self.search_window, text="검색", font=self.TempFont, command = self.open_find_window).grid(row=0, column=1)

        self.moneylabel = Label(self.search_window, text=str(total_price) + " 원", font=self.TempFont)
        self.moneylabel.grid(row=2, column=0)

        # 스크롤바와 Canvas
        scrollbar = Scrollbar(self.search_window)
        scrollbar.grid(row=1, column=2, sticky="NS")

        # Canvas 생성
        self.canvas = Canvas(self.search_window, yscrollcommand=scrollbar.set)
        self.canvas.grid(row=1, column=0, columnspan=2, sticky="NSEW")

        # 스크롤바와 Canvas 연결
        scrollbar.config(command=self.canvas.yview)

        # 프레임 생성
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # 프레임에 버튼 생성
        self.create_buttons()
        # 스크롤바 설정
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


        self.search_window.protocol("WM_DELETE_WINDOW", self.close_search_window)
        self.search_window.mainloop()
    def purchase(self, data):
        puchase(data["name"], data["steam_appid"], data["price_overview"]["final"])
        self.moneylabel.configure(text=str(return_money()) + " 원")
        print(str(return_money())+"원")
        self.create_buttons()
        pass

    def create_buttons(self):
        buttons = self.canvas.find_withtag("games")
        for button in buttons:
            self.frame.delete(button)
        for i, game in enumerate(buylist):
            button = Button(self.frame, text=str(game[0]) + " " + str(game[1]))
            button.grid(row=i, column=0, pady=5)
            button.bindtags((str(button), "games", "Button", ".", "all"))

    def open_find_window(self):
        gamename = str(self.search_entry.get())
        data = game_list_id_date(game_list_find(gamename))
        if not data:
            return
        window = Tk()
        window.title(data["name"])
        url = data["capsule_imagev5"]
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(im)
        Label(window, image=self.image).grid(row=0, column=0)
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(im)
        label = Label(window)
        label.image = self.image  # 이미지 객체에 대한 참조 유지
        label.configure(image=self.image)
        label.grid(row=0, column=0)
        #result window에 들어가야하는것은 data와 멀티미디어 정도

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
        