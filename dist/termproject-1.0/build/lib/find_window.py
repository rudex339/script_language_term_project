from tkinter import *
from tkinter import font
import urllib
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO
from main_data import *
from datetime import datetime

class find_window:
    def __init__(self, data):
        self.window = Tk()
        self.window.geometry("1300x415")
        self.window.title(data["name"])

        self.TempFont = font.Font(size=10, family='Consolas')

        url = data["capsule_imagev5"]
        print(url)
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im, master=self.window)
        label = Label(self.window)
        label.image = image  # 이미지 객체에 대한 참조 유지
        label.configure(image=image)
        label.place(x=0, y=0)

        Label(self.window, text=data["name"], font=self.TempFont).place(x=190, y=20)
        # 스크린 샷 리스트
        self.scList = []
        for sc in data["screenshots"]:
            self.scList.append(sc["path_thumbnail"])
        self.cur_img = 0
        # 스크린샷 라벨
        url = self.scList[self.cur_img]
        print(url)
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im, master=self.window)
        self.screenshot = Label(self.window)
        self.screenshot.image = image  # 이미지 객체에 대한 참조 유지
        self.screenshot.configure(image=image)
        self.screenshot.place(x=0, y=70)

        button = Button(self.window, text=str(str(data["price_overview"]["final"]/100) + "원 담기"),
                        command=lambda: self.purchase(data))
        button.place(x=190, y=40)
        # result window에 들어가야하는것은 data와 멀티미디어 정도
        #스크린샷 변경 버튼
        button = Button(self.window, text="img->",
                        command= self.next_img).place(x=300, y=40)
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.close())
        #평가 출력
        self.print_reviews(data["steam_appid"])
        # fstack에 window 저장
        fstack.append(self)

        self.window.mainloop()
    def next_img(self):
        self.cur_img = (self.cur_img+1) % len(self.scList)
        url = self.scList[self.cur_img]
        print(url)
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im, master=self.window)
        self.screenshot.image = image  # 이미지 객체에 대한 참조 유지
        self.screenshot.configure(image=image)
        pass
    def purchase(self, data):
        puchase(data["name"], data["steam_appid"], data["price_overview"]["final"])
    def close(self):
        self.window.destroy()
        pop_this(self)

    def print_reviews(self, Id):
        datas = data_review(Id)
        #라벨로 총
        Label(self.window, text="종합평가 :"+datas["query_summary"]["review_score_desc"], font=self.TempFont).place(x=700, y=45)

        # 데이터를 날짜별로 정리
        count = {}  # 년도: 월 : 날짜:count
        for data in datas["reviews"]:
            # Unix 타임스탬프를 날짜로 변환
            date = datetime.fromtimestamp(data["timestamp_created"])

            # 월과 연도 추출
            day = date.day
            month = date.month
            year = date.year

            # 월과 연도를 키로 사용하여 딕셔너리에 저장
            key = (year, month, day)
            if key not in count:
                count[key] = [0,0]
            if data["voted_up"]:
                count[key][0] += 1
            else:
                count[key][1] += 1
        #날짜별로 정리된 데이터를 그래프로 출력
        graph_width = 500
        graph_height = 200
        padding = 20

        frame = Frame(self.window,height = graph_height,width=graph_width)
        frame.place(x=700,y=100)

        # 그래프 캔버스 생성
        canvas = Canvas(frame, width=graph_width, height=graph_height)
        canvas.pack()

        # X축 라벨 생성
        x_label = Label(frame, text="날짜")
        x_label.pack()

        # Y축 라벨 생성
        y_label = Label(frame, text="리뷰 수")
        y_label.pack()

        # 그래프 그리기
        max_value = max(max(count.values()))  # 가장 큰 값
        bar_width = (graph_width - 2 * 10) / (len(count)*2)  # 막대 너비
        x_pos = padding  # X축 시작 위치

        for date, values in sorted(count.items()):
            # 첫 번째 막대 그리기 (붉은색)
            x = x_pos
            y = graph_height - padding
            bar_height_1 = (graph_height - 2 * padding) * values[0] / max_value

            canvas.create_rectangle(x, y - bar_height_1, x + bar_width, y, fill="blue")
            # 두 번째 막대 그리기 (파란색)
            bar_height_2 = (graph_height - 2 * padding) * values[1] / max_value

            canvas.create_rectangle(x + bar_width, y - bar_height_2, x + bar_width * 2, y, fill="red")


            # 다음 막대의 X축 위치 설정
            x_pos += bar_width*2

            # 날짜 라벨 그리기
            canvas.create_text(x + bar_width / 2, y + padding / 2, text=f"{date[1]}/{date[2]}", anchor="n")

        print(count)


if __name__ == "__main__":
    gamename = "eldenring"
    data = game_list_id_date(game_list_find(gamename))

    find_window(data)