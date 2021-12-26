import psycopg2
import telebot
import select
import bot_dbase
import msg_dbase
import config

token = config.TOKEN

# dbase for AUTOMATICALLY sending messages using messages databases
# in message_db the messages is 'queued' if the listen is still not running (or updating)

def sending(user_name, message):
    chat_ids = bot_dbase.get_chat_id_by_name(name=str(user_name))
    if chat_ids is None:
        print("Cannot send "+user_name+" message!")
    else:
        for id in chat_ids:
            bot.send_message(id[0], message)
            print(f"Sent user {user_name} new message!")

def sending_queued_msg():
    rows = msg_dbase.get_queued_messages()
    for row in rows:
        sending(row[0], row[1])
        print(f"Queued msg: {row[1]} --> {row[0]}")
    res = msg_dbase.update_state_messages()
    if res == 'success':
         print("Successfully updated queued messages!")
    else:
         print("Error with updating queued msg!")

if __name__ == '__main__':
    bot = telebot.TeleBot(token)
    conn = psycopg2.connect(dbname='fn1131_2021', user='student', password='bmstu', host='195.19.32.74', port='5432')
    cursor = conn.cursor()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True

    cursor.execute("LISTEN bot_users_msg;")
    print("Waiting for new messages in bot_users_msg:")

    while True:
        sending_queued_msg()
        if select.select([conn], [], [], 10) != ([], [], []):
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                (user,message,state) = str(notify.payload).split(", ")
                # sending(user, message)






