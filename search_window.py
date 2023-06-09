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

        # 검색 button
        Button(self.search_window, text="검색", font=self.TempFont, command=self.open_find_window).place(x=165, y=10)

        #프레임
        self.frame = Frame(self.search_window, height = 100)
        self.frame.place(x=9, y = 35)
        #스크롤바
        scrollbar = Scrollbar(self.frame)
        scrollbar.pack(side = "right", fill = "both")

        self.listbox = Listbox(self.frame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left",fill="both")

        scrollbar.config(command = self.listbox.yview)



        self.moneylabel = Label(self.search_window, text=str(total_price) + " 원", font=self.TempFont,justify = "right")
        self.moneylabel.place(x=50, y=200)

        # 프레임 생성

        self.search_window.mainloop()
    def purchase(self, data):
        index = puchase(data["name"], data["steam_appid"], data["price_overview"]["final"])
        self.listbox.insert(index,data["name"]+" "+str(data["price_overview"]["final"])+"원")
        self.moneylabel.configure(text=str(return_money()) + " 원")

    def cancel_buy(self, p):
        for item in buylist:
            if item[2] == p:
                buylist.remove(item)
                break
        self.create_buttons()
        self.moneylabel.configure(text=str(return_money()) + " 원")

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
        