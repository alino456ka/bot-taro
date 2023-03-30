import telebot as tb
from telebot import types
import requests as rq
from bs4 import BeautifulSoup as BS
import random as rd

token = '6293763503:AAEqk9P_omdTCiyFzW3hxMN3obfhtG6GzR8'
bot = tb.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    # создание клавиатуры (разметки кнопок)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # создание кнопки
    button = types.KeyboardButton('Погадать!')
    # добавление кнопки в клавиатуру
    markup.add(button)
    name = message.from_user.first_name
    # добавление клавиатуры к боту
    bot.send_message(message.chat.id, f' Приветствую, {name}!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def ask(message):
  if message.text == 'Погадать!':
    cards_dict = {}
    url = 'https://gadalkindom.ru/gadanie/taro/znachenie-kart-taro'
    response = rq.get(url)
    response.encoding = response.apparent_encoding
    soup = BS(response.text, 'html.parser')
    cards = soup.find_all('div', class_='col-lg-2 col-sm-3 col-xs-4 text-center')
    for i in cards:
        link = i.find('a', href=True)
        card_link = link['href']
        name = i.text
        name = name.strip()
        cards_dict[name] = card_link

    rand_card = rd.choice(list(cards_dict.keys()))
    rand_url = cards_dict[rand_card]
    response = rq.get(rand_url)
    response.encoding = response.apparent_encoding
    soup = BS(response.text, 'html.parser')
    advices = soup.find_all('div', class_='accordion-content')
    res = advices[1].text
    bot.send_message(message.chat.id, f'{rand_card}: {res}')

bot.polling(none_stop=True)