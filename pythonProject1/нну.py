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
def handler_start(message):
    bot.send_message(message.chat.id, 'приветик, я бот.\n'
                     'Используй команду: /users.')

@bot.message_handler(commands=['users'])
def handler_users(message):
    url = f'https://jsonplaceholder.typicode.com/users/{random.randint(1, 10)}'
    response = requests.get(url)
    if response.status_code == 200:
        users = response.json()
        print(users)
        name = users['name']
        email = users['email']
        company_name = users['company'] ['name']

        with open('users.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['name', 'email', 'company']
            write = csv.DictWriter(file, fieldnames)
            if file.tell() == 0:
                write.writeheader()

            write.writerow({
                'name': name,
                'email': email,
                'company': company_name
            })
        bot.send_message(message.chat.id, f'Имя: {name}.\n'
                         f'Email: {email}\nКомпания: {company_name}')


bot.polling(none_stop=True)


