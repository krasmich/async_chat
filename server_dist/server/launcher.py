import os
import signal
import subprocess
import sys
from time import sleep


PYTHON_PATH = sys.executable
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_subprocess(file_with_args):
    sleep(0.2)
    file_full_path = f"{PYTHON_PATH} {BASE_PATH}/{file_with_args}"
    args = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", file_full_path]
    return subprocess.Popen(args, preexec_fn=os.setpgrp)


process = []
while True:
    TEXT_FOR_INPUT = "Выберите действие: q - выход, s - запустить сервер, " \
                     "k - запуск клиентов, x - закрыть все окна: "
    action = input(TEXT_FOR_INPUT)

    if action == "q":
        break
    elif action == "s":
        process.append(get_subprocess("server.py"))

    elif action == 'k':
        print('Убедитесь, что на сервере зарегистрировано необходимое количество клиентов с паролем 123456.')
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))

        for i in range(clients_count):
            process.append(get_subprocess(f"client.py -n test{i+1} -p 123456"))

    elif action == "x":
        while process:
            victim = process.pop()
            os.killpg(victim.pid, signal.SIGINT)
