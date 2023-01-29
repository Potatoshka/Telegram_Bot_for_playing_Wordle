import random


def word_generator():
    with open('singular.txt', encoding='utf-8') as file:
        lines = file.readlines()
        random_word = 'word'
        while len(random_word) != 6:
            random_word = random.choice(lines)
        return random_word
