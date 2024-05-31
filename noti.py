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
import SiluList

TOKEN = '7356654382:AAFfSTy0k6lw16rp_kZGyPCfW4sSBsDIWJQ'
MAX_MSG_LENGTH = 50
bot = telepot.Bot(TOKEN)

def getData():
    res_list = []
    for item in SiluList.SiluList:
        info = f'가게명 : {item[0]} \n주소 : {item[1]}'
        res_list.append(info)
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData(param)
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg) + 1 > MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')
    print( '[',today,']received token :', TOKEN )
    pprint( bot.getMe() )
    run(current_month)