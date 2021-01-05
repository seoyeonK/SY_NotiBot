import requests
import os
import json
import telepot
import time
from azure.storage.blob import baseblobservice
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton as BT
from telepot.namedtuple import InlineKeyboardMarkup as MU

token = os.getenv('TELEGRAM_TOKEN')
bot = telepot.Bot(token)
chat_id = '1273348331' #bot.getUpdates()[-1]["message"]["from"]["id"]

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

def blob_storage_connect(container_name, Date):
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = baseblobservice.BaseBlobService(connection_string = connect_str)
        # Instantiate a ContainerClient 
        blobs_list = blob_service_client.list_blobs(container_name, prefix = Date)
        return blobs_list
    except Exception as ex:
        print('Exception:')
        print(ex)

# def listToStr(_list):
#     return "\n".join(_list)


def get_latest_msg():
   # msg = json.loads(requests.get(receive_url).text)["result"][-1]["message"]["text"] # json으로 받기
    msg = bot.getUpdates()[-1]["message"]["text"]
    return msg

''' FOR TESTING
date_info = '2010-01-01'
file_info = [x.name for x in blob_storage_connect('smartwatchdata', date_info)]
bot.sendMessage(chat_id, "\n".join(file_info))
'''



def btn_show(msg):
    btn1 = BT(text = "1. Search", callback_data = "1")
    btn2 = BT(text = "2. Cancel", callback_data = "2")
    mu = MU(inline_keyboard = [[btn1, btn2]])
    bot.sendMessage(chat_id, "choose", reply_markup = mu)

def query_ans(msg):         #activated when btn is selected
    query_id = msg["id"]    #id of the selected btn
    query_data = msg["data"]
    if query_data == "1":
        #list_info = listToStr(blob_storage_connect('smartwatchdata'))
        #bot.answerCallbackQuery(query_id, text = list_info)
        bot.sendMessage(chat_id, "hi")     
    elif query_data == "2":
        bot.answerCallbackQuery(query_id, text = "okay bye")


MessageLoop(bot, {'chat': btn_show, 'callback_query' : query_ans}).run_as_thread()

while True:
    time.sleep(5)


'''

 def handle(msg):
     content_type, chat_type, chat_id = telepot(glance.msg)
     if get_latest_msg() == 'search':
        #if the user wants to search a specific watch w/ serial number
         txt = "input the serial number of the watch"
         bot.sendMessage(chat_id, txt)
         return
        #ask for date
'''

