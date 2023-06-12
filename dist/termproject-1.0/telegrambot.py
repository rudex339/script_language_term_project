

import telepot
from pprint import pprint

from datetime import date
import noti
import main_data


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    Id = main_data.game_list_find(msg['text'])
    if Id < 0:
        noti.sendMessage(chat_id, '없는 게임입니다')
        return
    data = main_data.game_list_id_date(Id)
    if not data:
        noti.sendMessage(chat_id, '정보가 없습니다')
        return
    m = ""
    m += data["name"]+" "+str(data["price_overview"]["initial"]/100)+"원 "
    if data["price_overview"]["discount_percent"] !=0:
        m+=str(data["price_overview"]["discount_percent"])+"할인중! 현재가격 "+str(data["price_overview"]["final"]/100)
    noti.sendMessage(chat_id, m)
def start_bot():
    bot = telepot.Bot(noti.TOKEN)
    bot.message_loop(handle)