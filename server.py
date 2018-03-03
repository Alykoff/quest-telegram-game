# https://www.digitalocean.com/community/tutorials/docker-explained-how-to-containerize-python-web-applications
# https://github.com/datamachine/twx.botapi
import sys
import time
import re
import threading
import random
import sqlite3
import telepot
from pprint import pprint
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import inlinequeryresultarticle, inlinequeryresultphoto, inputtextmessagecontent

import config

"""
$ python3.5 skeleton_route.py <token>
"""

message_with_inline_keyboard = none

def on_chat_message(msg):
    print(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        return
    user_id = msg['from']['id']
    print(user_id)
    conn = db_conn()
    cursor = conn.cursor()
    user = none
    try:
        cursor.execute('insert into log (id, chat_id, user_id, msg) values (?, ?, ?, ?)', (int(time.time() * 10000), chat_id, user_id, str(msg)))
        conn.commit()
        cursor.execute('select * from users where id = ?', (user_id, ))
        user = cursor.fetchone()
        isfirst = user is none
        if isfirst:
            pprint(user)
            cursor.execute('insert into users (id, username, level, start_level) values (?, ?, 0, ?)', (user_id, msg['from']['first_name'], int(time.time())))
            conn.commit()
            cursor.execute('select * from users where id = ?', (user_id, ))
            user = cursor.fetchone()
            bot.sendmessage(chat_id, '''приветствую тебя\n\nправительство ---\n''')
        pprint(user)

        (u_id, u_name, u_lvl, u_time) = user
        if config.admin_id is not None and config.trasser_id is not None and u_id == config.admin_id and msg['text'][0] == '!':
            bot.sendmessage(config.trasser_id, msg['text'][1:])
            bot.sendMessage(config.admin_id, msg['text'][1:])
        cursor.execute('select * from lvl where id = ?', (u_lvl, ))
        lvl = cursor.fetchone()
        (l_id, _, l_start_msg, l_end_msg, l_wrong_msg, l_answer, l_image, l_delay) = lvl
        bot.sendMessage(config.admin_id, 'lvl: ' + str(l_id) + '. ' + msg['text'])
        if not re.match(l_answer, msg['text']) is None:
            cursor.execute('update users set level=?,start_level=? where id = ?', ((l_id + 1), int(time.time()), u_id))
            conn.commit()
            bot.sendMessage(chat_id, str(l_id) + ". " + l_end_msg.replace('\\n', '\n'))
            cursor.execute('select * from lvl where id = ?', ((l_id + 1), ))
            lvl = cursor.fetchone()
            (l_id, _, l_start_msg, l_end_msg, l_wrong_msg, l_answer, l_image, l_delay) = lvl
            bot.sendMessage(chat_id, str(l_id) + ". " + l_start_msg.replace('\\n', '\n'))
        elif not isFirst:
            bot.sendMessage(chat_id, l_wrong_msg)
            bot.sendMessage(chat_id, str(l_id) + ". " + l_start_msg.replace('\\n', '\n'))
        else:
            bot.sendMessage(chat_id, str(l_id) + ". " + l_start_msg.replace('\\n', '\n'))
    except Exception as e:
        cursor.execute('insert errors (id, msg) values (?, ?)', (int(time.time() * 1000), str(e)))
        conn.commit()
        exit(1)
    finally:
        conn.close()

def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)


def on_inline_query(msg):
    print('empty')


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)

def db_conn():
    return sqlite3.connect('quest.db')

TOKEN = sys.argv[1]  # get token from command-line
bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

bot.message_loop({'chat': on_chat_message})
print('Listening ...')
# Keep the program running.
while 1:
    time.sleep(10)
