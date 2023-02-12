"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).
"""

words = ['attribute', 'класс', 'функция', 'type']


def check_for_byte():
    """
    Функция определяет какие слова
    невозможно записать в байтовом типе
    с помощью маркировки b''
    """
    for word in words:
        try:
            conv_word = word.encode('ascii')
        except UnicodeEncodeError:
            print(f'{word} - данное слово нельзя преобразовать в байтовый формат')


check_for_byte()
