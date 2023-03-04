import argparse
import json
import socket
import sys
import logging
import logs.server_log_config


from utils import receive_message, process_client_message, send_message, PORT, MAX_CONNECTIONS

server_logger = logging.getLogger('server')


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():

    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        server_logger.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    server_logger.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((listen_address, listen_port))
    serversocket.listen(MAX_CONNECTIONS)

    while True:
        client, address = serversocket.accept()
        server_logger.info(f'Установлено соедение с ПК {address}')
        try:
            msg_client = receive_message(client)
            print(msg_client)
            response = process_client_message(msg_client)
            server_logger.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            server_logger.debug(f'Соединение с клиентом {address} закрывается.')
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
