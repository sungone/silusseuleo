import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
import noti

def replyAptData(user):
    res_list = noti.getData()
    msg = ''
    for r in res_list:
        if len(r + msg) + 1 > noti.MAX_MSG_LENGTH:
            noti.sendMessage(user, msg)
            msg = r + '\n'
        else:
            msg += r + '\n'
    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, '잘못 입력하셨습니다.')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']

    if text.startswith('시루') :
        replyAptData(chat_id)
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.')

today = date.today()
current_month = today.strftime('%Y%m')
print('[',today,']received token :', noti.TOKEN)

bot = telepot.Bot(noti.TOKEN)
print(bot.getMe())
bot.message_loop(handle)

print('Listening...')
while 1:
  time.sleep(10)