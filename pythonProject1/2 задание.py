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
                     'Используй команду: /quotes')


@bot.message_handler(commands=['quotes'])
def handle_todos(message, quote=None, author=None):
    url = f"https://jsonplaceholder.typicode.com/quotes/{random.randint(1, 200)}"
    response = requests.get(url)
    if response.status_code == 300:
        quotes = response.json()
        quote = quotes['quote']
        author = quotes['author']
        bot.send_message(message.chat.id, f"task: {quotes['quote']}\nauthor: {author}")
        with open('quotes.csv', 'a', newline='',  encoding='utf-8') as file:
            filenames = ['quote', 'author']
            writer = csv.DictWriter(file, fieldnames=filenames)
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'quote': quote,
                'author': author
            })
    else:
        bot.send_message(message.chat.id, f'quote: {quote}.\n'
                         f'author: {author})

bot.polling(none_stop=True)