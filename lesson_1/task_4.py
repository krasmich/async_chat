"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).
"""

words = ['разработка', 'администрирование', 'protocol', 'standard']


def convert_to_byte():
    """
    Функция преобразования из строки в байтовый формат и обратно
    """
    for word in words:
        word_byte = word.encode('utf-8')
        print(f'{word} - строковое представление, {word_byte} - байтовое представление')
        word_byte_dec = bytes.decode(word_byte, encoding='utf-8')
        print(f'{word_byte} - байтовое представление, {word_byte_dec} - строковое представление')


convert_to_byte()
