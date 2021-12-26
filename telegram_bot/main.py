import sys
import json
import subprocess
import time
import os
import platform
import signal
import bot_dbase
import bot_helper
import re
import config

token_bot = config.TOKEN

def sending(user_names, message):
    for user_name in user_names:
        chat_ids = bot_dbase.get_chat_id_by_name(name=str(user_name))
        if chat_ids is None:
            print("Cannot send "+user_name+" message!")
        else:
            for id in chat_ids:
                print(id[0])
                bot.send_message(id[0], message)
                print(f"Sent user {user_name} message!")

def sending_all(chats_id, message):
    for id in chats_id:
        bot.send_message(int(id), message)
    return 'ok'

if __name__ == "__main__":
    bot = bot_helper.Bot(token_bot)
    #python3 main.py sendall message
    if sys.argv[1] == 'sendall':
        if len(sys.argv) == 3:
            msg = sys.argv[2]
            chats_id = bot_dbase.get_all_chat_id()
            print(chats_id)
            if chats_id is None:
                print('Пользователи не найдены')
            elif sending_all(chats_id=chats_id, message=msg) == 'ok':
                print('Сообщение отправлено')
            else:
                print(id[0])
                print('Произошла ошибка при отправке сообщений')

    elif sys.argv[1] == 'send':
        #           0       1      2     3     4      5
        # python3 main.py send name1 name2 name3 Message
        if len(sys.argv) < 4:
            print('Вы ввели недостаточно параметров')
        else:
            user_names = sys.argv[2:len(sys.argv) - 1]
            message = sys.argv[len(sys.argv) - 1]
            sending(user_names, message)
            print('Сообщение отправлено')
