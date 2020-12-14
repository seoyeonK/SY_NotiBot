import requests
import os


token = os.getenv('TELEGRAM_TOKEN')

# 업데이트 내용 받아오기
# 아래의 주소를 호출하면, 업데이트 된 봇의 내용을 가져올 수 있다.

url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
response = json.loads(requests.get(url).text) # json으로 받기
print(response)