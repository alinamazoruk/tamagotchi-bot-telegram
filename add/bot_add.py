import telebot


bot = telebot.TeleBot("1244775976:AAEpZuesdgpHkYBNwT0lIfN6mV5jxBKqL8w")


rules = "You can play and feed your pet.\
But remember that all your actions affect your pet.\
You won't be given a second chance, so treat it well\n\
'You become responsible forever for what you've tamed.' ― Antoine de Saint-Exupéry, The Little Prince"

telagochies = {}

is_updater_running = False

updater_delay = 30

ban = []
admins = [256294474]


def is_exist(chat_id):
    return telagochies.get(chat_id) is not None


def is_admin(chat_id):
    return chat_id in admins


def is_banned(chat_id):
    return chat_id in ban