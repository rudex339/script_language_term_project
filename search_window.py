from tkinter import *
from tkinter import font
import urllib
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO

from main_data import *

class MainGui:
    result_windows= []
    c=0
    buttonl = []
    def __init__(self) -> None:
        self.search_window = Tk()
        self.search_window.geometry("210x225")
        self.search_window.title("게임 영수증")
        self.TempFont = font.Font(size=10, family='Consolas')
        #검색 entry
        self.search_entry = Entry(self.search_window,font=self.TempFont)
        self.search_entry.place(x=10, y=12)

        self.frame = Frame()

        # 검색 button
        Button(self.search_window, text="검색", font=self.TempFont, command = self.open_find_window).place(x=165, y=10)

        self.moneylabel = Label(self.search_window, text=str(total_price) + " 원", font=self.TempFont)
        self.moneylabel.place(x=150, y=200)

        # 프레임 생성

        self.search_window.mainloop()
    def purchase(self, data):
        puchase(data["name"], data["steam_appid"], data["price_overview"]["final"])
        self.create_buttons()
        self.moneylabel.configure(text=str(return_money()) + " 원")
        pass

    def cancel_buy(self, p):
        for item in buylist:
            if item[2] == p:
                buylist.remove(item)
                break
        self.create_buttons()
        self.moneylabel.configure(text=str(return_money()) + " 원")
    def create_buttons(self):
        for b in self.buttonl: # result_windows에서 버튼 ID를 가져옵니다
            b.destroy() # 버튼 태그(버튼 ID)를 사용하여 버튼을 삭제합니다
        self.buttonl.clear()
        for i, game in enumerate(buylist):
            button = Button(self.frame, text=str(game[0]) + " " + str(game[1]), command=lambda g=game[2]: self.cancel_buy(g))
            button.grid(row=i, column=0, pady=5)

            self.buttonl.append(button)  # 버튼 ID를 result_windows에 저장합니다

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
        image = ImageTk.PhotoImage(im, master=window)
        label = Label(window)
        label.image = image  # 이미지 객체에 대한 참조 유지
        label.configure(image=image)
        label.grid(row=0, column=0)

        Label(window, text=data["name"], font=self.TempFont).grid(row=0, column=1)
#스크린 샷
        scList= []
        for sc in data["screenshots"]:
            scList.append(sc["path_thumbnail"])
        id = 0

        url = scList[id]
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im, master=window)
        label = Label(window)
        label.image = image  # 이미지 객체에 대한 참조 유지
        label.configure(image=image)
        label.grid(row=1, column=2)

        button = Button(window, text=str(str(data["price_overview"]["final"]) + " 담기"), command=lambda: self.purchase(data))
        button.grid(row=0, column=2)
        #result window에 들어가야하는것은 data와 멀티미디어 정도
        self.result_windows.append([self.c,id, scList,label])
        value = self.c
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_result_window(window,value))
        self.result_windows.append(window)
        window.mainloop()
        self.c += 1
    
    def close_search_window(self):
        self.result_windows.clear()
        self.search_window.destroy()
    
    def close_result_window(self,window, value):
        window.destroy()
        for item in self.result_windows:
            if item[0] == value:
                self.result_windows.remove(item)



MainGui()
        