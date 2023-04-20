import telebot
from telebot import types
import time
import sqlite3

bot = telebot.TeleBot('5627545355:AAGiAk7xdXVfQCKhw784BYw6hAZHH5Bbpic')

@bot.message_handler(commands=['start'])
def start(message):
# Створюєм БД
    conn = sqlite3.connect('plan.db')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS plan (id int auto_increment primary key, plans varchar (150))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Привіт {message.from_user.first_name}, ти у планер боті😀, щоб додати план тицяй /addplan👾.')
    time.sleep(1)

# Обробка команди /addplan, щоб додати план
@bot.message_handler(commands=['addplan'])
def plan(message):
    bot.send_message(message.chat.id, "Введіть свої плани🤧:")
    bot.register_next_step_handler(message, send_in_bd)

# Функція для обробки повідомлення з назвою плану, запис в базу данних
def send_in_bd(message):
    conn = sqlite3.connect('plan.db')
    cur = conn.cursor()
    planing = message.text.strip()


    cur.execute('INSERT INTO plan (plans) VALUES (?)', (planing,))

    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Плани успішно записані✅')
    time.sleep(1)
    bot.send_message(message.chat.id, 'Щоб подивитись список планів, тисни сюди /list ✨')

# Обробка команди /list, дивитись список всіх планів (витягуєм дані з бази данних)
@bot.message_handler(commands=['list'])
def send_data(message):
    conn = sqlite3.connect('plan.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM plan")
    data = cur.fetchall()
    if len(data) == 0:
        bot.send_message(message.chat.id, "Планів немає🤔 ")
        return
    else:
        for row in data:
            bot.send_message(message.chat.id, row)
    bot.send_message(message.chat.id, 'Щоб очистити список тисни /clear🧹')
    conn.close()


# Очистка таблиці
@bot.message_handler(commands=['clear'])
def delete_data(message):
    conn = sqlite3.connect('plan.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM plan")
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, 'Плани очищенні 👍')


bot.polling(none_stop=True)