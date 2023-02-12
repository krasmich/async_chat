"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.
"""
import subprocess
import chardet


ping_resources = [['ping', 'yandex.ru'], ['ping', 'youtube.com']]


def ping_web_res():
    """
    Функция выполняет пинг ресурсов и далее преобразовывает в строковый тип
    """
    for ping_resource in ping_resources:
        ping = subprocess.Popen(ping_resource, stdout=subprocess.PIPE)

        for line in ping.stdout:
            result = chardet.detect(line)
            dec_line = line.decode('ascii')
            print(dec_line)


ping_web_res()
