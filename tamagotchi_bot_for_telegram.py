import datetime
import math
import random


def normalize(i):
    if i > 100:
        i = 100
    return i


class Event:

    def __init__(self, event_type, name, happiness, health, energy, balance):
        self.type = event_type
        self.name = name
        self.happiness = happiness
        self.health = health
        self.energy = energy
        self.balance = balance


class Telagochi:
    happiness_smiles = ["💀", "😭", "😫", "😕", "😄", "😀"]
    food = {
        u"\U0001F34A": Event("Food", "Orange", None, 20, 20, -10),
        u"\U0001F34B": Event("Food", "Lemon", None, 20, 20, -10),
        u"\U0001F34C": Event("Food", "Banana", None, 20, 20, -10),
        u"\U0001F34D": Event("Food", "Pineapple", None, 20, 20, -10),
        u"\U0001F34E": Event("Food", "Apple", None, 20, 20, -10),
        u"\U0001F351": Event("Food", "Peach", None, 20, 20, -10),
        u"\U0001F352": Event("Food", "Cherry", None, 20, 20, -10),
        u"\U0001F353": Event("Food", "Strawberry", None, 20, 20, -10),
        u"\U0001F354": Event("Food", "Hamburger", None, 20, 20, -10),
        u"\U0001F355": Event("Food", "Pizza", None, 20, 20, -10),
        u"\U0001F36A": Event("Food", "Cookies", None, 20, 20, -10),
        u"\U0001F966": Event("Food", "Broccoli", None, 20, 20, -10),
    }

    activities = {
        u"⚽": Event("Play", "Football", None, 20, -20, 10),
        u"🏈": Event("Play", "Rugby", None, 20, -20, 10),
        u"⚾": Event("Play", "Baseball", None, 20, -20, 10),
        u"🎾": Event("Play", "Tennis", None, 20, -20, 10),
        u"🏐": Event("Play", "Volleyball", None, 20, -20, 10),
        u"🏓": Event("Play", "Ping-Pong", None, 20, -20, 10),
        u"🏒": Event("Play", "Hockey", None, 20, -20, 10),
        u"🏃": Event("Play", "Dogolyalki", None, 20, -20, 10),
        u"\U0001F3AE": Event("Play", "Video-Games", None, 20, -20, 10),
    }

    def __init__(self, user_id):
        self.user_id = user_id
        self.name = None
        self.birth_time = datetime.datetime.now()
        self.last_command = "born"
        self.happiness = 50
        self.health = 50
        self.energy = 50
        self.happiness_event = {}
        self.time_event = Event("time", "time", -5, -5, -5, 10)
        self.balance = 100

    def get_happiness(self):
        return Telagochi.happiness_smiles[math.ceil(self.happiness / 20)]

    def increase_happiness(self, i):
        self.happiness += int(i)
        self.happiness = normalize(self.happiness)

    def increase_health(self, i):
        self.health += int(i)
        self.health = normalize(self.health)

    def increase_energy(self, i):
        self.energy += int(i)
        self.energy = normalize(self.energy)

    def increase_balance(self, i):
        if self.balance + int(i) >= 0:
            self.balance += int(i)
            return True
        return False

    def effect_event(self, event):
        if not self.increase_balance(event.balance):
            self.say("Not enough money! do something useful")
            return

        happiness = event.happiness
        if happiness is None:
            if self.happiness_event.get(event) is None:
                self.happiness_event[event] = random.randint(-30, 30)
            happiness = self.happiness_event[event]

        self.increase_happiness(happiness)
        if self.happiness < 0:
            self.death(reason="sadness")
            return
        self.increase_health(event.health)
        if self.health < 0:
            self.death(reason="illness")
            return
        self.increase_energy(event.energy)
        if self.energy < 0:
            self.death(reason="exhaustion")
            return
        self.say(self.get_info(Event(None, None, happiness, event.health, event.energy, event.balance)))

    def sprint_age(self):
        age = datetime.datetime.now() - self.birth_time
        return f"{age.days}d, {age.seconds // 3600}h, {(age.seconds % 3600) // 60}m, {age.seconds % 60}s"

    def get_age(self):
        return datetime.datetime.now() - self.birth_time

    def get_info(self, event=None):
        if event is None:
            return \
                f"Telegochi info:\n" \
                f"Name:      {self.name}\n" \
                f"Age:       {self.sprint_age()} \n" \
                f"Happiness: {self.get_happiness()}\n" \
                f"Health:    {self.health}\n" \
                f"Energy:    {self.energy}\n" \
                f"Balance:   {self.balance}"
        return \
            "Telegochi info:\n" \
            f"Name:      {self.name}\n" \
            f"Age:       {self.sprint_age()}\n" \
            f"Happiness: {self.get_happiness()} ({event.happiness:+d})\n" \
            f"Health:    {self.health} ({event.health:+d})\n" \
            f"Energy:    {self.energy} ({event.energy:+d})\n" \
            f"Balance:   {self.balance} ({event.balance:+d})"

    def eat(self, food):
        self.effect_event(food)

    def play(self, activity):
        self.effect_event(activity)

    def get_preferences(self):
        res = "```\n" \
              "name|happy|health|energy|balance\n" \
              "--------------------------------\n"

        for k in Telagochi.food:
            h = f"{self.happiness_event.get(Telagochi.food[k]):+5d}" if self.happiness_event.get(
                Telagochi.food[k]) is not None else '    ?'

            res += f"{k:4s}|{h}|{Telagochi.food[k].health:+6d}|{Telagochi.food[k].energy:+6d}|{Telagochi.food[k].balance:+7d}\n"

        for k in Telagochi.activities:
            h = f"{self.happiness_event.get(Telagochi.activities[k]):+5d}" if self.happiness_event.get(
                Telagochi.activities[k]) is not None else '    ?'

            res += f"{k:4s}|{h}|{Telagochi.activities[k].health:+6d}|{Telagochi.activities[k].energy:+6d}|{Telagochi.activities[k].balance:+7d}\n"
        res += "```"
        return res

    def death(self, reason=None):
        if reason is None:
            self.say("I am dead")
        else:
            self.say(f"I am dead for a reason: {reason}")
        self.say("Game over")
        ban.append(self.user_id)

    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)

    keyboard.row("/start", "/born", "/info", "/preferences")

    keyboard.row(*(food.keys()))
    keyboard.row(*(activities.keys()))

    def say(self, text, custom_keyboard=keyboard, parse_mode=None):
        if is_banned(self.user_id):
            bot.send_message(self.user_id, "I don't believe you anymore")
            return
        bot.send_message(self.user_id, text, reply_markup=custom_keyboard, parse_mode=parse_mode)


bot = telebot.TeleBot()

rules = ""

telagochies = {}

is_updater_running = False

updater_delay = 10

ban = []
admins = [256294474]


def is_exist(chat_id):
    return telagochies.get(chat_id) is not None


def is_admin(chat_id):
    return chat_id in admins


def is_banned(chat_id):
    return chat_id in ban


@bot.message_handler(commands=['start'])
def send_start(message):
    if is_banned(message.chat.id):
        bot.send_message("I don't believe you anymore")
        bot.send_message(message.chat.id,
                         "Hello! I am Telagochies' parent! I am giving you this egg! send /born to open it!")


@bot.message_handler(commands=['help'])
def send_help(message):
    if is_banned(message.chat.id):
        bot.send_message("I don't believe you anymore")

    bot.send_message(message.chat.id,
                     "Hello! I am your own Telegochi! You can play with me! that`s my interface:\n" + rules)


@bot.message_handler(commands=['born'])
def born_telegochi(message):
    if is_banned(message.chat.id):
        bot.send_message("I don't believe you anymore")
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
        bot.send_message("I don't believe you anymore")
        return
    telagochies[message.chat.id].name = message.text
    telagochies[message.chat.id].last_command = ""
    telagochies[message.chat.id].say(
        f"Your telegochi {telagochies[message.chat.id].name} was born at {telagochies[message.chat.id].birth_time.strftime('%Y/%m/%d %H:%M:%S')}! \n"
        "That's you can do:\n"
        f"{rules}"
    )


@bot.message_handler(commands=['info'])
def telegochi_info(message):
    if is_banned(message.chat.id):
        bot.send_message("I don't believe you anymore")
        return
    if not is_exist(message.chat.id):
        send_start(message)
        return
    telagochies[message.chat.id].say(telagochies[message.chat.id].get_info())


@bot.message_handler(commands=['preferences'])
def telegochi_preferences(message):
    if is_banned(message.chat.id):
        bot.send_message("I don't believe you anymore")
        return
    if not is_exist(message.chat.id):
        send_start(message)
        return
    telagochies[message.chat.id].say(telagochies[message.chat.id].get_preferences(), parse_mode="Markdown")


@bot.message_handler(commands=['run_updater'])
def run_updater(message):
    if not is_admin(message.chat_id):
        bot.reply_to(message, "Permission denied")
        return

    global is_updater_running
    if is_updater_running:
        bot.reply_to(message, "Updater ia already running")
        return
    is_updater_running = True
    while is_updater_running:

        for k in telagochies:
            if telagochies[k].get_age().seconds >= 10:
                telagochies[k].effect_event(telagochies[k].time_event)
        time.sleep(updater_delay)


@bot.message_handler(commands=['stop_updater'])
def run_updater(message):
    if not is_admin(message.chat_id):
        bot.reply_to(message, "Permission denied")
        return
    global is_updater_running
    is_updater_running = False


@bot.message_handler(commands=['set_delay'])
def run_updater(message):
    if not is_admin(message.chat_id):
        bot.reply_to(message, "Permission denied")
        return
    global updater_delay
    updater_delay = int(message.text.split(" ")[1])
    print(updater_delay)


@bot.message_handler(func=lambda message: Telagochi.food.get(message.text) is not None)
def food(message):
    if is_banned(message.chat.id):
        bot.send_message("I don't believe you anymore")
    if not is_exist(message.chat.id):
        send_start(message)
        return
    telagochies[message.chat.id].eat(Telagochi.food.get(message.text))


@bot.message_handler(func=lambda message: Telagochi.activities.get(message.text) is not None)
def activity(message):
    if is_banned(message.chat.id):
        bot.send_message("I don't believe you anymore")
        return
    if not is_exist(message.chat.id):
        send_start(message)
        return
    telagochies[message.chat.id].play(Telagochi.activities.get(message.text))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True, interval=1)

