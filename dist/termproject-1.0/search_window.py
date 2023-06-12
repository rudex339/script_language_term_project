from tkinter import *
from tkinter import font
import  find_window
from tkintermapview import TkinterMapView

from main_data import *
import telegrambot
class MainGui:
    result_windows= []
    c=0
    buttonl = []
    def __init__(self) -> None:
        self.search_window = Tk()
        self.search_window.geometry("210x475")
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

        #리스트박스에서 선택된 객체 삭제 버튼
        Button(self.search_window, text="삭제", font=self.TempFont, command= self.cancel_buy).place(x=165, y=150)

        #지도 버튼
        Button(self.search_window, text="저장", font=self.TempFont, command=save).place(x=165, y=120)
        Button(self.search_window, text="로드", font=self.TempFont, command=load).place(x=165, y=90)

        self.moneylabel = Label(self.search_window, text=str(total_price) + " 원", font=self.TempFont,justify = "right")
        self.moneylabel.place(x=50, y=200)

        self.search_window.protocol("WM_DELETE_WINDOW", lambda: self.close())

        self.map_widget = TkinterMapView(self.search_window, width=200, height=200)
        self.map_widget.place(x=5, y= 265)

        self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

        self.map_widget.set_address("Republic of Korea", marker=True)

        Swindow_connect(self)
        telegrambot.start_bot()
        self.search_window.mainloop()

    def update_data(self, data):
        #index = puchase(data["name"], data["steam_appid"], data["price_overview"]["final"])
        self.listbox.insert(self.listbox.size(),data[0]+" "+str(data[1])+"원")
        self.moneylabel.configure(text=str(return_money()) + " 원")

    def cancel_buy(self):
        index = self.listbox.curselection()
        self.listbox.delete(index)
        cancel_buy(index)

        self.moneylabel.configure(text=str(return_money()) + " 원")

    def open_find_window(self):
        gamename = str(self.search_entry.get())
        data = game_list_id_date(game_list_find(gamename))
        if not data:
            return
        fstack.append(find_window.find_window(data))
    
    def close(self):
        pop_all()
        self.search_window.destroy()





MainGui()
        