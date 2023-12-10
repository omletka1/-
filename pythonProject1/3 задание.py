import csv
import os
import random
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id,
                        'приветик, я бот.\n'
                     'Используй команду: /infousers')


@bot.message_handler(commands=['infousers'])
def handle_todos(message, city=None, title=None, adress=None, status=None, departaments=None, name=None):
    url = f"https://dummyjson.com/users/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 200:
        infousers = response.json()
        adress = infousers['adress']
        title = infousers['title']
        city = infousers['city']
        name = infousers['name']
        status = infousers['status']
        departament = infousers['departament']
        with open('infousers.csv', 'a', newline='',  encoding='utf-8') as file:
            filenames = ['adress', 'title', 'city', 'status', 'name', 'departament']
            writer = csv.DictWriter(file, fieldnames=filenames)
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'adress': adress,
                'title': title,
                'city': city,
                'status': status,
                'name': name,
                'departament': departament

            })
    else:
        bot.send_message(message.chat.id, f'адрес: {adress}.\n'
                         f'Email: {title}\nКомпания: {city}\n' f'статус: {status}\n' f'name: {name}\n' 
                                          f'departament: {departaments}\n')

bot.polling(none_stop=True)