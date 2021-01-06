import requests
import os
import json
import telepot
import re
import time
from datetime import datetime
from collections import defaultdict
from azure.storage.blob import baseblobservice
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton as BT
from telepot.namedtuple import InlineKeyboardMarkup as MU
'''
    - DONE -
    1)  need to make the query connection when the user chooses "other dates" & inputs the date
    2) need to cut the blob file name by the watch number, filmed date & time (cutoff the "mp4")

    - TO DO -
    3) make the chatbot multi-thread
        #from telepot.delegate import pave_event_space, per_chat_id, create_open
    4) need to load the dates of the blob folders to inlinekeyboard
    5) use arg parser to flexibly switch between api servers
    6) addtionally get the upload date & time(last modified attribute), and the size of each videos
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

def cut_str(s, l):
    return [str(s[i:i+l]) for i in range(0, len(s), l)]

def PrintBlobFiles(query_data, storage_name = 'smartwatchdata'):
    file_info = [x.name for x in blob_storage_connect('smartwatchdata', query_data)]

    ''' filter file names - ex
    SN 139 : 5 videos
     record time - 11:52:36, ~~~~
    '''
    watch = defaultdict(list)

    for idx, video in enumerate(file_info):
        watch_sn = (video.split('/')[-1].split('_')[0])[8:11] #only take out the number part
        record_time = ':'.join(cut_str(video.split('/')[-1].split('_')[2], 2))
        if watch_sn not in watch.keys():
            (watch[watch_sn]).append('   ' + record_time)
        else:
            (watch[watch_sn]).append(record_time)

    #printMsg = str(len(file_info)) + " videos from " + query_data + ":\n\n" + "\n".join(file_info)
    printMsg = ''
    for sn in watch.keys():
        Times_str = '\n   '.join(watch[sn])
        printMsg += "SN " + str(sn) + " : " + str(len(watch[sn])) + " videos\n---------------\n" + Times_str + "\n---------------------\n"
    bot.sendMessage(chat_id, str(len(file_info)) + " videos from " + query_data + ":\n---------------------\n" + printMsg)
    return

def get_latest_msg():
   # msg = json.loads(requests.get(receive_url).text)["result"][-1]["message"]["text"] # json으로 받기
    msg = bot.getUpdates()[-1]["message"]["text"]
    return msg

''' FOR TESTING
file_info = [x.name for x in blob_storage_connect('smartwatchdata', date_info)]
bot.sendMessage(chat_id, "\n".join(file_info))
'''

date_info = '2010-01-01'

def chat_handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if '20' in msg["text"] :
        PrintBlobFiles(msg["text"])
    else:
        #SHOW BUTTONS
        btn1 = BT(text = "2021-01-01", callback_data = "2021-01-01")
        btn2 = BT(text = "2021-01-04", callback_data = "2021-01-04")
        btn3 = BT(text = "2021-01-05", callback_data = "2021-01-05")
        btn4 = BT(text = "2021-01-06", callback_data = "2021-01-06")
        btn5 = BT(text = "other dates", callback_data = "other")
        mu = MU(inline_keyboard = [[btn1], [btn2], [btn3], [btn4], [btn5],])
        bot.sendMessage(chat_id, "choose", reply_markup = mu)


def query_ans(msg):         #activated when btn is selected
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    
    if query_data == "other":
        bot.sendMessage(chat_id, "input the date in the form of yyyy-mm-dd")
        return
    elif query_data == "input-date":
        query_data = msg["text"]
   
    file_info = [x.name for x in blob_storage_connect('smartwatchdata', query_data)]
    
    PrintBlobFiles(query_data)
    return 

MessageLoop(bot, {'chat': chat_handle, 'callback_query' : query_ans}).run_as_thread()

while True:
    time.sleep(5)
