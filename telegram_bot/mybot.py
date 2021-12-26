import telebot
import config
import sys
import bot_dbase
import json

# to run bot: python3 mybot.py token_bot
token = config.TOKEN
bot = telebot.TeleBot(token)

def open_json(path):
    try:
        with open(path, 'r', encoding="utf-8") as f:
            data = json.loads(f.read().encode(encoding="utf-8"))
            new_data = {}
            new_data['greetings'] = data['greetings']
            new_data['approval'] = data['approval']
            new_data['unsubscribe'] = data['unsubscribe']
            new_data['advice'] = data['advice']
            new_data['change_name'] = data['change_name']
            return new_data
    except:
        return None

# /start
@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(message.chat.id, 'Привет. Если ты написал мне, то хочешь получать рассылку от МГТУ.')
    greetings = open_json(sys.argv[1])['greetings']
    bot.send_message(message.chat.id, greetings)
    bot_dbase.insert_user_into_table(chat_id=str(message.chat.id), name=str(message.chat.username))
    print("Inserted user {id} into db!".format(id=message.from_user.id))


# /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Commands: /start , /help , /new_name, /unsubscribe, /my_info, /bot_info, /users_info")
    advice = open_json(sys.argv[1])['advice']
    bot.send_message(message.chat.id, advice)
    # bot.reply_to(message, "/help commands, your id :{id} , your username: {username}".format(id=message.chat.id, username=message.chat.username))

# /bot_info
@bot.message_handler(commands=['bot_info'])
def bot_info(message):
    info = "bot_id: " + str(bot.get_me().id) + "\nbot_username: " + str(bot.get_me().username) + "\nbot_firstname: " + str(bot.get_me().first_name)
    bot.send_message(message.chat.id, info)

# /users_info
@bot.message_handler(commands=['users_info'])
def users_info(message):
    info = bot_dbase.get_info()
    bot.send_message(message.chat.id, info)

# /unsubcribe
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    bot_dbase.unsubscribe(chat_id=message.chat.id)
    bot.send_message(message.chat.id, 'OK, you just unsubscribed me:((')
    bot.send_message(message.chat.id, open_json(sys.argv[1])['unsubscribe'])

# /new_name
@bot.message_handler(commands=['new_name'])
def change_name(message):
    msg = bot.send_message(message.chat.id, "Choose your name in db: ")
    bot.register_next_step_handler(msg, process_next_step)

def process_next_step(message):
    new_name = message.text
    # print(new_name)
    if(bot_dbase.name_is_exist(name=new_name) == True):
        bot.send_message(message.chat.id, 'Это имя уже занято. Введите другое')
        msg = bot.send_message(message.chat.id, open_json(sys.argv[1])['change_name'])
        bot.register_next_step_handler(msg, process_next_step)
    else:
        res = bot_dbase.update_name_by_chat_id(chat_id=str(message.chat.id), name=str(new_name))
        if res == 'replaced':
            bot.send_message(message.chat.id, 'Ты успешно внесен в базу данных, ожидай рассылки.')
            bot.send_message(message.chat.id, open_json(sys.argv[1])['approval'])
            bot.send_message(message.chat.id, "Your name in db is " + new_name)

# /my_info
@bot.message_handler(commands=['my_info'])
def my_info(message):
    name_in_db = bot_dbase.get_name_by_chat_id(chat_id=message.chat.id)
    bot.send_message(message.chat.id,"Your id: {id}\n Your Telegram username: {username}\n Your name in db: {name}".format(id=message.chat.id, username=message.chat.username, name=name_in_db))

if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("You did not provide .json file how the bot reply")
    else:
        print("Your bot is running")
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.polling(none_stop=True)
# bot.infinity_polling(True)