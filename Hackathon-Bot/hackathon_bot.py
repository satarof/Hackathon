"""ТЕХНИЧЕСКОЕ ЗАДАНИЕ(сложность: тяжелая)

1. При нажатии на кнопку start, телеграмм бот должен
зайти на сайт KaktusMedia (https://kaktus.media/) и
спарсить категорию “Все новости”
2. При вводе текста должны выйти первые 20
заголовков статей с нумерацией. Должна быть
возможность выбрать новости по нумерации или id
(по желанию)
3. После выбора новости по нумерации, телеграмм
бот должен отправить сообщение в виде “some
title news you can see Description of this news
and Photo” и пользователь отправит текст (либо
нажмет кнопку) Description, то бот должен
отправить описание именно текущего поста, также
аналогично с Photo.
4. При нажатии на кнопку «Quit» бот должен
отправить сообщение “До свидания“"""

from decouple import config
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import csv



# URL = 'https://kaktus.media/?lable=8&date=2023-05-30&order=time' 
# def csv_kaktus(data):
#     with open('kaktus.csv', 'a') as file:
#         writer = csv.writer(file)
#         writer.writerow([data['title']])

# def get_html(link):
#     responce = requests.get(link)
#     return responce.text

# def get_all(html):
#     soup = BeautifulSoup(html, 'lxml')
#     list_news = soup.find_all('div', class_="ArticleItem--data ArticleItem--data--withImage")

#     for news in list_news:
#         title = news.find('a', class_="ArticleItem--name").text.strip().split('"')
#         print(title)
#         dict_ = {'title':title}
#         csv_kaktus(dict_)

# def main():

#     for i in range(1):
#         url = f'https://kaktus.media/?lable=8&date=2023-05-30&order=time'
#         get_all(get_html(url))
# main()

# with open('kaktus.csv') as file:
#     reading = file.read()
# # token(ключ) при помощи которого можно получить доступ к нашему боту
# token = config('TOKEN')

# # при помощи библиотеки telebot и нашего токена, мы сохранили нашего бота в переменную 'bot'
# bot = telebot.TeleBot(token)

# @bot.message_handler(commands=['start'])
# def welcome(message):
#         bot.send_message(message.chat.id, list(enumerate(reading)) )


# bot.polling()

from decouple import config
import telebot
import requests
from bs4 import BeautifulSoup

URL = 'https://kaktus.media/?lable=8&date=2023-05-30&order=time'

def get_all_titles():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    list_news = soup.find_all('div', class_="ArticleItem--data ArticleItem--data--withImage")
    titles = []
    for news in list_news:
        image = news.find('img')

    for i, news in enumerate(list_news, start=1):
        title = news.find('a', class_="ArticleItem--name").text.strip().replace('"', '')
        titles.append(f'{i}. {title}')

    return titles

# token(ключ) при помощи которого можно получить доступ к нашему боту
token = config('TOKEN')

# при помощи библиотеки telebot и нашего токена, мы сохранили нашего бота в переменную 'bot'
bot = telebot.TeleBot(token)

keyboard = types.ReplyKeyboardMarkup()
button1 = types.KeyboardButton('quit')
# button2 = types.KeyboardButton('Next')
keyboard.add(button1)


@bot.message_handler(commands=['start'])
def welcome(message):
    titles = get_all_titles()
    message_text = '\n'.join(titles[:20])
    bot.send_message(message.chat.id, message_text)

@bot.message_handler(func=lambda message: message.text.isdigit())
def news_description(message):
    selected_news_index = int(message.text) - 1
    titles = get_all_titles()

    if selected_news_index < len(titles):
        selected_news_title = titles[selected_news_index]
        bot.send_message(message.chat.id, f"Вы выбрали: {selected_news_title}")
        # Здесь можно добавить код для получения и отправки описания и фото текущей новости


@bot.message_handler(commands=['quit'],reply_markup=types.ReplyKeyboardRemove)
def quit(message):
    bot.send_message(message.chat.id, "До свидания")

bot.polling()
