"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.
"""

# Метод 1
words1 = ['class', 'function', 'method']


def convert_to_byte1():
    """
    Функция преобразования слово в байтовый формат
    """
    for word in words1:
        conv_word = bytes(word, 'utf-8')
        print(f'Тип {type(conv_word)}, содержимое {conv_word}, длина {len(conv_word)}')


convert_to_byte1()


print('-------------------------------------------------------')
# Метод 2
words2 = [b'class', b'function', b'method']


def convert_to_byte2():
    """
    Функция преобразования слово в байтовый формат
    """
    for word in words2:
        print(f'Тип {type(word)}, содержимое {word}, длина {len(word)}')


convert_to_byte2()