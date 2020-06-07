import datetime
import math


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