import csv
import os
import random
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['todos'])
def handler_start(message):
    bot.send_message(message.chat.id, 'приветик, я бот.\n'
                     'Используй команду: /todos.')

@bot.message_handler(commands=['todos'])
def handler_users(message, user=None):
    url = f'https://jsonplaceholder.typicode.com/todos/{random.randint(1, 10)}'
    response = requests.get(url)
    if response.status_code == 200:
        users = response.json()
        print(users)
        todo = users['todo']
        completed = users['completed']
        company_name = users['company'] ['name']

        with open('todos.csv', 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['todo', 'completed', 'userId']
            write = csv.DictWriter(file, fieldnames)
            if file.tell() == 0:
                write.writeheader()

            write.writerow({
                'todo': todo,
                'completed': completed,
                'userId': user
            })
        bot.send_message(message.chat.id, f'todo: {todo}.\n'
                         f'completed: {completed}\nuserId: {user}')


bot.polling(none_stop=True)
