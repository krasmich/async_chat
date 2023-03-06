import argparse
import json
import socket
import sys
import logging
import logs.client_log_config
from decor import log

from utils import create_presence, receive_message, process_server_answer, send_message, PORT, HOST


client_logger = logging.getLogger('client')


@log
def create_arg_parser():
    """
    Создаём парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=HOST, nargs='?')
    parser.add_argument('port', default=PORT, type=int, nargs='?')
    return parser


def main():

    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    if not 1023 < server_port < 65536:
        client_logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    client_logger.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(clientsocket, message_to_server)
        answer = process_server_answer(receive_message(clientsocket))
        client_logger.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
