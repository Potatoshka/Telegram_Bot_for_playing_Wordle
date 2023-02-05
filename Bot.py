import time
import sqlite3 as sl
import telebot
import re


from Game import game
from Word_Generator import word_generator

bot = telebot.TeleBot('xxxx')
con = sl.connect('words.db', check_same_thread=False)
cur = con.cursor()


random_word = {}


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте слово из 5 букв. Перед словом нужно поставить знак "№"')
    update_word(m)


@bot.message_handler(commands=["help"])
def bot_help(m, res=False):
    bot.send_message(m.chat.id, 'Бот загадывает слово, вы должны это слово угадать. Если в слове, которое вы '
                                 'отправили есть буквы из загаданного слова, то бот их выделит в кавычки. '
                                 'Если буквы еще и '
                                 'расположены там же, где в загадонном слове, то бот эти буквы вернет в '
                                 'верхнем регистре. Отправьте "№сдаюсь" - если не можете отгадать. Для сброса'
                                ' загаданного слова отправьте /start')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if '№' in message.text and len(message.text) != 6 or '#' in message.text and len(message.text) != 6:
        bot.send_message(message.chat.id, "Только слова из 5 букв!")
    if '№' in message.text and len(message.text) == 6 or '#' in message.text and len(message.text) == 6:
        bot.send_message(message.chat.id, game(message.text.replace('№', '').replace('#', '').lower(),
                                               random_word[str(message.chat.id)]))
    if message.text.lower() == '№сдаюсь' or message.text.lower() == '#сдаюсь':
        bot.send_message(message.chat.id, random_word[str(message.chat.id)])


def update_word(m):
    global random_word

    new_word = word_generator().replace('\n', '')
    with con:
        cur.execute("""CREATE TABLE IF NOT EXISTS chats (chat_name TEXT PRIMARY KEY, 
        word TEXT);""")
        for row in con.execute("SELECT chat_name FROM chats"):
            row_string = ' '.join(str(x) for x in row)
            if str(m.chat.id) == row_string:
                cur.execute("UPDATE chats SET word = ? WHERE chat_name = ?", (new_word, str(m.chat.id)))
            else:
                sql = "INSERT or IGNORE INTO chats (chat_name, word) VALUES(?, ?)"
                data = [str(m.chat.id), word_generator().replace('\n', '')]
                cur.execute(sql, data)
        result = cur.execute("SELECT word FROM chats WHERE chat_name = ?", (str(m.chat.id),)).fetchone()
        result_string = ' '.join(str(x) for x in result)
        print(result_string)
        random_word[str(m.chat.id)] = result


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)

