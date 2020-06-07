import telebot


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