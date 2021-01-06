import requests
import os
import json
import telepot
import re
import time
from azure.storage.blob import baseblobservice
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton as BT
from telepot.namedtuple import InlineKeyboardMarkup as MU

'''
    -TO DO-
    1) need to load the dates of the blob folders to inlinekeyboard
    2) need to make the query connection when the user chooses "other dates" & inputs the date
        (maybe by chat handler... still finding out about it)
    3) need to cut the blob file name by the watch number, filmed date & time (cutoff the "mp4")
    4) addtionally get the upload date & time(last modified attribute), and the size of each videos
    5) use arg parser to flexibly switch between api servers
'''




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
file_info = [x.name for x in blob_storage_connect('smartwatchdata', date_info)]
bot.sendMessage(chat_id, "\n".join(file_info))
'''


date_info = '2010-01-01'

def btn_show(msg):
    btn1 = BT(text = "2021-01-01", callback_data = "2021-01-01")
    btn2 = BT(text = "2021-01-04", callback_data = "2021-01-04")
    btn3 = BT(text = "2021-01-05", callback_data = "2021-01-05")
    btn4 = BT(text = "2021-01-06", callback_data = "2021-01-06")
    btn5 = BT(text = "other dates", callback_data = "other")
    mu = MU(inline_keyboard = [[btn1], [btn2], [btn3], [btn4], [btn5],])
    bot.sendMessage(chat_id, "choose", reply_markup = mu)

# def chat_handler():
    #chat and btn show here 


def query_ans(msg):         #activated when btn is selected
    query_id = msg["id"]    #id of the selected btn
    date_info = msg["data"]
    if date_info == "other":
        bot.sendMessage(chat_id, "input the date in the form of yyyy-mm-dd")
        newMsg = get_latest_msg()
        query_ans()
   
    file_info = [x.name for x in blob_storage_connect('smartwatchdata', date_info)]
    
    printMsg = str(len(file_info)) + " videos from " + date_info + ":" + "\n\n" + "\n".join(file_info)
    bot.sendMessage(chat_id, printMsg)
    return
    #send "watch video?" -> yes / no -> yes -> send 


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

