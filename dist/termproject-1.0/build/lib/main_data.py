import requests
import xml.etree.ElementTree as ET
import json
import re
import ssl
import spam
Swindow = None

import time
def Swindow_connect(window):
    global Swindow
    Swindow = window
fstack = []
def add_fstack(window):
    global fstack
    fstack.append(window)
def pop_all():
    global fstack
    for unit in fstack:
        unit.close()
    return
def pop_this(window):
    global fstack
    fstack.remove(window)
def pop_index(index):
    global fstack
    for num in index:
        del fstack[num]

ssl._create_default_https_context = ssl._create_unverified_context

params = {
    "key": "4C882AC12E087E0B0E834D14F1B74EA3",
    "format": "XML",
}
def input_game_list():
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/"

    response = requests.get(url, params)
    return ET.fromstring(response.text)

game_list = input_game_list()
total_price = 0
buylist = []
def game_list_id_date(Id):
    if Id < 0:
        return None
    id_url = "http://store.steampowered.com/api/appdetails?appids="+str(Id)
    response = requests.get(id_url, params)
    data = json.loads(response.text)
    return data[str(Id)]["data"]
def game_list_find(name):
    # 게임 리스트 내 파일 찾기
    # 입력하지 않음
    if name == '':
        return -1
    name = re.sub(r'[^a-zA-Z]', '', name.strip())  # 앞뒤 공백 제거 후 처리
    for app in game_list.iter("app"):
        id = app.find("appid").text
        gname = app.find("name").text
        if gname:
            if spam.comparison(gname, name):
                return int(id)
    # 존재하지 않음
    return -2
def puchase(name, id, price):
    buylist.append([name, int(price)//100, id])
    Swindow.update_data([name, int(price)//100, id])
def cancel_buy(index):
    global buylist
    for num in index:
        del buylist[num]
def return_money():
    return sum(item[1] for item in buylist)
def data_review(Id):
    id_url = "http://store.steampowered.com/appreviews/" + str(Id) + "?json=1&filter=recent&num_per_page=100$language=all"
    response = requests.get(id_url)
    data = json.loads(response.text)
    return data
def save(self):
    pass
def load(self):
    pass





