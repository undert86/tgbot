import telebot
import spotipy
from telebot import types
import sys
from spotipy.oauth2 import SpotifyClientCredentials

token = "6104472904:AAGdgAniuOY3zHf-7OXH5SAlNV_GmtcnRM0"
bot = telebot.TeleBot(token)

client_id = "e9f794eb35d8483d86dc0bd8b04dc76e"
client_secret = "888651fbda704dcdaf387368b554d871"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id,
                     "Привет, это бот, который импортирует песни из заблокированной на территории РФ площадки - Spotify. Напиши /help, чтобы ознакомится с командами".format(
                         message.from_user, bot.get_me(), parse_mode='html'))


@bot.message_handler(commands=['button'])
def button_message(message):
    if message.text == "/button":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кнопка")
        markup.add(item1)
        markup.row(item1)


@bot.message_handler(commands=['help'])
def get_text_messages(message):
    bot.send_message(message.from_user.id,
                     "/findsong - найти песню по названию и исполнителю, /findmus - найти исполнителя, /findnamesong - найти песню только по названию")


@bot.message_handler(commands=['findsong'])
def get_text_messages(message):
    bot.send_message(message.chat.id,
                     text='Напиши название и имя исполнителя, к примеру: Snoop Dogg - Drop It Like Its Hot')




# """bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")"""


bot.polling()
