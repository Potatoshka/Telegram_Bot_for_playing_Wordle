import time

import telebot


from Game import game
from Word_Generator import word_generator

bot = telebot.TeleBot('XXXXX')
random_word = word_generator().replace('\n', '')


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте слово из 5 букв. Перед словом нужно поставить знак "№"')
    update_word()




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
        bot.send_message(message.chat.id, game(message.text.replace('№', '').replace('#', '').lower(), random_word))
    if message.text.lower() == '№сдаюсь' or message.text.lower() == '#сдаюсь':
        bot.send_message(message.chat.id, random_word)


def update_word():
    global random_word
    random_word = word_generator().replace('\n', '')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)

