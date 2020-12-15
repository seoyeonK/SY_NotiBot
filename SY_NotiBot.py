import requests
import os
import json
import telepot
from telepot.loop import MessageLoop 

token = os.getenv('TELEGRAM_TOKEN')
bot = telepot.Bot(token)

def get_latest_msg():
   # msg = json.loads(requests.get(receive_url).text)["result"][-1]["message"]["text"] # json으로 받기
    msg = bot.getUpdates()[-1]["message"]["text"]
    return msg
 
print(get_latest_msg())


chat_id = bot.getUpdates()[-1]["message"]["from"]["id"]
def handle(msg):

    if get_latest_msg() == 'search':
       #if the user wants to search a specific watch w/ serial number
        txt = "input the serial number of the watch"
        bot.sendMessage(chat_id, txt)
        return
       #ask for date

    SN = int(get_latest_msg())
    if SN < 250 :
        bot.sendMessage("good job")

    #print list of the uploaded videos
    #can i get the videos too? can i play it at telegram?

#connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

#defining handle fuction -> need to set precise algorithm for coding
