import requests
import xml.etree.ElementTree as ET
import json
import re

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
            en_only = re.sub(r'[^a-zA-Z]', '', gname.lower())
            if name.lower() == en_only:
                return int(id)
    # 존재하지 않음
    return -2
def puchase(name, id, price):
    global total_price
    buylist.append([name, int(price)//100, id])
    return len(buylist)-1

def return_money():
    return sum(item[1] for item in buylist)



