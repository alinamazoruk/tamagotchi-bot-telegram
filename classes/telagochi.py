import datetime
import math
import random
import telebot


from classes.event import *
from add.bot_add import ban
from add.bot_add import is_banned
from add.bot_add import bot


def normalize(i):
    if i > 100:
        i = 100
    return i


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

    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)

    keyboard.row("/start", "/born", "/info", "/preferences")

    keyboard.row(*(food.keys()))
    keyboard.row(*(activities.keys()))

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

    def say(self, text, custom_keyboard=keyboard, parse_mode=None):
        if is_banned(self.user_id):
            bot.send_message(self.user_id, "I don't believe you anymore")
            return
        bot.send_message(self.user_id, text, reply_markup=custom_keyboard, parse_mode=parse_mode)