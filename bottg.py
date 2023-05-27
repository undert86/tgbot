import os
import spotipy
import spotipy.oauth2 as oauth2
import telebot
from telebot import types
from googleapiclient.discovery import build
import yt_dlp as youtube_dl
import io
import requests
# Получаем credentials для Spotify API
credentials = oauth2.SpotifyClientCredentials(
    client_id='e9f794eb35d8483d86dc0bd8b04dc76e',
    client_secret='888651fbda704dcdaf387368b554d871'
)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# Получаем токен бота
BOT_TOKEN = '6104472904:AAGdgAniuOY3zHf-7OXH5SAlNV_GmtcnRM0'

bot = telebot.TeleBot(BOT_TOKEN)

# Получаем ключ API YouTube Data API
YOUTUBE_API_KEY = 'AIzaSyBF0NEv8x05AqTPvZJQK_uFchlN8EredDk'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


@bot.message_handler(commands=['start'])
def start_message(message):
    text = "Привет! Я могу искать треки на Spotify и отправлять их вам аудиофайлами в формате MP3."
    bot.send_message(message.chat.id, text)
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Помощь')
    itembtn2 = types.KeyboardButton('Найти трек')

    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def echo(message):
    text = message.text

    print("Пользователь:", message.from_user.username)
    print(f"Запрос пользователя: {text}")
    items = text.split('-')
    if message.text == 'Помощь':
        bot.send_message(message.chat.id, 'За помощью к создателю этого бота - @undert86')
    elif message.text == 'Найти трек':
        bot.reply_to(message, 'Введите название исполнителя и трека через знак "-".')
    elif len(items) != 2:
        bot.reply_to(message, 'Я не понимаю тебя. Введите команду "Найти трек" или введите название исполнителя и трека через знак "-".')
    else:
        artist = items[0].strip()
        track = items[1].strip()
        # Ищем трек на Spotify
        query = f"artist:{artist} track:{track}"
        result = sp.search(q=query, type='track', limit=1)
        if result['tracks']['items']:
            track_data = result['tracks']['items'][0]
            track_name = track_data['name']
            track_artist = track_data['artists'][0]['name']
            track_preview_url = track_data['preview_url']
            track_cover_url = track_data['album']['images'][0]['url']
            response = requests.get(track_cover_url, headers={'Content-Type': 'image/jpeg'})
            if response.status_code == 200:
                photo = io.BytesIO(response.content)
                bot.send_photo(message.chat.id, photo, caption=f'{track_artist} - {track_name}')

            if not track_preview_url:
                bot.reply_to(message, 'К сожалению, для этого трека нет превью.')
                return

            # Получаем ссылку на полную версию трека с YouTube
            search_response = youtube.search().list(
                q=f"{track_artist} {track_name}",
                part='id',
                maxResults=1,
                type='video'
            ).execute()

            if 'items' in search_response and len(search_response['items']) > 0:
                video_id = search_response['items'][0]['id']['videoId']
                track_url = f"https://www.youtube.com/watch?v={video_id}"

                # Скачиваем аудиофайл с YouTube
                # Скачиваем аудиофайл с YouTube
                # ...
# Скачиваем аудиофайл с YouTube
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': 'track',  # Обновляем расширение файла на .mp3
                    'verbose': True
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(track_url, download=False)
                    if 'entries' in info_dict:
                        # Если ссылка содержит плейлист, выбираем первую запись
                        info_dict = info_dict['entries'][0]
                    track_filename = ydl.prepare_filename(info_dict)
                    track_title = info_dict.get('title', '')
                    track_extension = 'mp3'  # Устанавливаем расширение файла в .mp3
                    track_path = f'{track_filename}.{track_extension}'
                    ydl.process_info(info_dict)  # Скачиваем аудиофайл

                # Отправляем аудиофайл в формате MP3 в Telegram
                with open(track_path, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, title=f'{track_artist} - {track_name}')

                # Удаляем временный аудиофайл
                # os.remove(track_path)  # Удалите эту строку

                # ...

                # Удаляем временный аудиофайл
                os.remove(track_path)

            else:
                bot.reply_to(message, 'К сожалению, не удалось найти полную версию трека.')

        else:
            bot.reply_to(message, 'К сожалению, я не нашел такой трек на Spotify.')


# Запускаем бота
def main():
    """Запуск бота."""
    print('стартуем..')
    bot.polling()


if __name__ == '__main__':
    main()
