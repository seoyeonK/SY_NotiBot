import requests
import os
import json
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton as BT
from telepot.namedtuple import InlineKeyboardMarkup as MU

token = os.getenv('TELEGRAM_TOKEN')
bot = telepot.Bot(token)
chat_id = '1273348331' #bot.getUpdates()[-1]["message"]["from"]["id"]

def get_latest_msg():
   # msg = json.loads(requests.get(receive_url).text)["result"][-1]["message"]["text"] # json으로 받기
    msg = bot.getUpdates()[-1]["message"]["text"]
    return msg


def btn_show(msg):
    btn1 = BT(text = "1. Search", callback_data = "1")
    btn2 = BT(text = "2. Cancel", callback_data = "2")
    mu = MU(inline_keyboard = [[btn1, btn2]])
    bot.sendMessage(chat_id, "choose", reply_markup = mu)

def query_ans(msg):         #activated when btn is selected
    query_id = msg["id"]    #id of the selected btn
    query_data = msg["data"]
    if query_data == "1":
        bot.answerCallbackQuery(query_id, text = "search me")
    elif query_data == "2":
        bot.answerCallbackQuery(query_id, text = "okay bye")


MessageLoop(bot, {'chat': btn_show, 'callback_query' : query_ans}).run_as_thread()


# def handle(msg):
#     content_type, chat_type, chat_id = telepot(glance.msg)
#     if get_latest_msg() == 'search':
#        #if the user wants to search a specific watch w/ serial number
#         txt = "input the serial number of the watch"
#         bot.sendMessage(chat_id, txt)
#         return
#        #ask for date

#     SN = int(get_latest_msg())
#     if SN < 250 :
#         bot.sendMessage("good job")

    #print list of the uploaded videos
    #can i get the videos too? can i play it at telegram?


#connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

#defining handle fuction -> need to set precise algorithm for coding
