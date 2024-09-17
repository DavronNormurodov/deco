import telebot

from core.settings import BOT_TOKEN, CHANNEL_ID


def send_alert(text):
    bot = telebot.TeleBot(BOT_TOKEN)
    bot.send_message(CHANNEL_ID, text=text, parse_mode='html')
