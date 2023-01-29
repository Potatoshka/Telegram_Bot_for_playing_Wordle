


def game(word_input, random_word):
    buffer = []
    colors = []
    if word_input == random_word:
        return "🏆 Вы угадали слово! 🏆"
    list_input = list(word_input)
    list_random = list(random_word)
    for j in list_input:
        if j in list_random and list_input.index(j) == list_random.index(j):
            buffer.append(j.upper())
            colors.append('✅')
            list_random[list_random.index(j)] = '_'
            list_input[list_input.index(j)] = '_'
        elif j in list_random:
            buffer.append("'" + j + "'")
            colors.append('☑')
            list_random[list_random.index(j)] = '_'
            list_input[list_input.index(j)] = '_'
        else:
            buffer.append(j)
            colors.append('❌')
            list_input[list_input.index(j)] = '_'

    return ''.join(buffer) + '\n' + ''.join(colors)
