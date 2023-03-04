import telebot
import os
import spotipy
import spotipy.util as util
from telebot import types
import sys
from spotipy.oauth2 import SpotifyClientCredentials

token = "6104472904:AAGdgAniuOY3zHf-7OXН5SAlNV_GmtcnRM0"
bot = telebot.TeleBot(token)

client_id = "e9f7a94eb35d483d86dc0bd8b04dc76e"
client_secret = "888651fbda704dcdaf387368b554d871"
REDIRECTURI = 'http://localhost:8888/callback'

# Права доступа к API Spotify
SCOPE = 'user-library-read'


def authorize_spotify(user_id):
    token = util.prompt_for_user_token(user_id, SCOPE, clientid, client_secret, REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    return sp


@bot.message_handler(commands=['start'])
def start(update):
    user_id = update.chat.id
    sp = authorize_spotify(user_id)
    if sp:
        message = "Привет, это бот, который импортирует песни из заблокированной на территории РФ площадки - Spotify. Для начала авторизуйтесь в Spotify, отправив мне команду /auth. Напиши /help, чтобы ознакомиться с командами"
    else:
        message = "Не удалось авторизоваться в Spotify. Проверьте настройки приложения"
    bot.send_message(update.chat.id, message)


# Функция для обработки команды /auth
@bot.message_handler(commands=['auth'])
def auth(update):
    user_id = update.chatid
    sp = authorize_spotify(user_id)
    if sp:
        message = 'Вы успешно авторизовались в Spotify. Теперь вы можете искать музыку. Напиши /findsong, там дальнейшая инструкция'
    else:
        message = 'Не удалось авторизоваться в Spotify. Проверьте настройки приложения.'
    bot.send_message(update.chat.id, message)



@bot.message_handler(commands['help'])
def get_text_messages(message):
    bot.send_message(message.from_user.id,
                     "/findsong - найти песню по названию и исполнителю, /findmus - найти исполнителя")


@bot.message_handler(func=lambda message: True)
def import_song(message):
    user_id = message.chat.id
    sp = authorize_spotify(user_id)

    # Получение названия песни и исполнителя из сообщения пользователя
    query = ' '.join(message.text.split()[1:])
    # Разделение названия песни и исполнителя на две переменные
    song_name, artist_name = None, None
    for word in query.split():
        if word.lower() == 'by':
            index = query.index(word)
            song_name = query[:index].strip()
            artist_name = query[index+2:].strip()
            break

    # Поиск песни в Spotify
    # Если названия песни и исполнителя не найдены, то сообщаем об ошибке
    if song_name is None or artist_name is None:
        bot.send_message(message.chat.id,
                         'Неверный формат запроса. Попробуйте еще раз, указав название и исполнителя через "by".')
        return

    # Проверка наличия результатов поиска и отправка ссылки на предварительный просмотр песни пользователю
    if len(results['tracks']['items']) > 0:
        track = results['tracks']['items'][0]
        preview_url = track['preview_url']
        bot.send_message(message.chat.id, 'Вот твоя песня: {}'.format(preview_url))
    else:
        bot.send_message(message.chat.id, 'К сожалению, я не смог найти эту песню.')
