import time
from classes.telagochi import *
from add.bot_add import *


@bot.message_handler(commands=['start'])
def send_start(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "You are not a responsible parent!")
        return
    bot.send_message(message.chat.id,
                     "Hello! I am Telagochies' parent! I am giving you this egg! send /born to open it!")


@bot.message_handler(commands=['born'])
def born_telegochi(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "You are not a responsible parent!")
        return
    if is_exist(message.chat.id):
        telegochi_info(message)
        return
    telagochies[message.chat.id] = Telagochi(message.chat.id)
    telagochies[message.chat.id].say("Telagochi was born! Enter name:", None)


@bot.message_handler(
    func=lambda message:
    message.chat.id in telagochies and telagochies[message.chat.id].last_command == "born")
def name_telegochi(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "You are not a responsible parent!")
        return
    telagochies[message.chat.id].name = message.text
    telagochies[message.chat.id].last_command = ""
    telagochies[message.chat.id].say(
        f"Your telegochi {telagochies[message.chat.id].name} was born at {telagochies[message.chat.id].birth_time.strftime('%Y/%m/%d %H:%M:%S')}! \n"
        "Foreword:\n"
        f"{rules}"
    )


@bot.message_handler(commands=['info'])
def telegochi_info(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "You are not a responsible parent!")
        return
    if not is_exist(message.chat.id):
        send_start(message)
        return
    telagochies[message.chat.id].say(telagochies[message.chat.id].get_info())


@bot.message_handler(commands=['preferences'])
def telegochi_preferences(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "You are not a responsible parent!")
        return
    if not is_exist(message.chat.id):
        send_start(message)
        return
    telagochies[message.chat.id].say(telagochies[message.chat.id].get_preferences(), parse_mode="Markdown")


@bot.message_handler(commands=['run_updater'])
def run_updater(message):
    if not is_admin(message.chat.id):
        bot.reply_to(message, "Permission denied")
        return

    global is_updater_running
    if is_updater_running:
        bot.reply_to(message, "Updater ia already running")
        return
    is_updater_running = True
    while is_updater_running:

        for k in telagochies:
            if not is_banned(k) and telagochies[k].get_age().seconds > updater_delay:
                telagochies[k].effect_event(telagochies[k].time_event)
        time.sleep(updater_delay)


@bot.message_handler(commands=['stop_updater'])
def stop_updater(message):
    if not is_admin(message.chat.id):
        bot.reply_to(message, "Permission denied")
        return
    global is_updater_running
    is_updater_running = False


@bot.message_handler(commands=['set_delay'])
def set_delay(message):
    if not is_admin(message.chat.id):
        bot.reply_to(message, "Permission denied")
        return
    global updater_delay
    updater_delay = int(message.text.split(" ")[1])


@bot.message_handler(func=lambda message: Telagochi.food.get(message.text) is not None)
def food(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "You are not a responsible parent!")
        return
    if not is_exist(message.chat.id):
        send_start(message)
        return
    telagochies[message.chat.id].eat(Telagochi.food.get(message.text))


@bot.message_handler(func=lambda message: Telagochi.activities.get(message.text) is not None)
def activity(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "You are not a responsible parent!")
        return
    if not is_exist(message.chat.id):
        send_start(message)
        return
    telagochies[message.chat.id].play(Telagochi.activities.get(message.text))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True, interval=1)
