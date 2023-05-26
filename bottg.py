import os

import spotipy

import spotipy.oauth2 as oauth2

import telebot

import requests

import io

# Получаем credentials для Spotify API

credentials = oauth2.SpotifyClientCredentials(

    client_id='e9f794eb35d8483d86dc0bd8b04dc76e',

    client_secret='888651fbda704dcdaf387368b554d871'

)

sp = spotipy.Spotify(client_credentials_manager=credentials)

# Получаем токен бота

BOT_TOKEN = '6104472904:AAGdgAniuOY3zHf-7OXH5SAlNV_GmtcnRM0'

bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды start

@bot.message_handler(commands=['start'])

def start_message(message):

    text = "Привет! Я могу искать треки на Spotify. Введите название исполнителя и трека через знак '-'.\nНапример: Ariana Grande - No Tears Left To Cry"

    bot.send_message(message.chat.id, text)

# Обработчик текстовых сообщений

@bot.message_handler(content_types=['text'])

def echo(message):

    text = message.text

    print(f"User's request: {text}")

    items = text.split('-')

    if len(items) != 2:

        bot.reply_to(message, 'Введите название исполнителя и трека через знак "-".')

    else:

        artist = items[0].strip()

        track = items[1].strip()

        # Ищем трек на Spotify

        query = f"artist:{artist} track:{track}"

        result = sp.search(q=query, type='track', limit=1)

        if result['tracks']['items']:

            track = result['tracks']['items'][0]

            track_preview = track['preview_url']

            track_name = track['name']

            track_artist = track['artists'][0]['name']

            track_cover_url = track['album']['images'][0]['url']

            download_button = telebot.types.InlineKeyboardButton('Скачать', url=track_preview)

            # Создаем объект клавиатуры и добавляем на нее кнопку "Скачать"

            keyboard = telebot.types.InlineKeyboardMarkup()

            keyboard.add(download_button)

            # Загружаем обложку трека и отправляем ее вместе с аудиофайлом

            response = requests.get(track_cover_url, headers={'Content-Type': 'image/jpeg'})

            if response.status_code == 200:

                photo = io.BytesIO(response.content)

                bot.send_photo(message.chat.id, photo, caption=f'{track_artist} - {track_name}')

                bot.send_audio(message.chat.id, track_preview, title=track_name, performer=track_artist, reply_markup=keyboard)

        else:

            bot.reply_to(message, 'К сожалению, я не нашел такой трек на Spotify.')

# Запускаем бота

def main():

    """Запуск бота."""

    print('стартуем..')

    bot.polling()

if __name__ == '__main__':

    main()
