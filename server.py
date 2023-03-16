import argparse
import socket
import sys
import logging
import select
import logs.server_log_config
from decor import log

from utils import receive_message, process_client_message, send_message, PORT, \
    MAX_CONNECTIONS, SENDER, DESTINATION

server_logger = logging.getLogger('server')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        server_logger.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


class Server:
    def __init__(self, listen_port, listen_address):
        self.listen_port = listen_port
        self.listen_address = listen_address

        self.clients = []
        self.messages = []

        self.names = dict()

    def main(self):

        server_logger.info(
            f'Запущен сервер, порт для подключений: {self.listen_port}, '
            f'адрес с которого принимаются подключения: {self.listen_address}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.listen_address, self.listen_port))
        serversocket.settimeout(0.5)
        serversocket.listen(MAX_CONNECTIONS)

        while True:
            try:
                client, client_address = serversocket.accept()
            except OSError:
                pass
            else:
                server_logger.info(f'Установлено соедение с ПК {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        process_client_message(receive_message(client_with_message),
                                               self.messages, client_with_message, self.clients, self.names)
                    except:
                        server_logger.info(f'Клиент {client_with_message.getpeername()} '
                                           f'отключился от сервера.')
                        self.clients.remove(client_with_message)

            # Если есть сообщения, обрабатываем каждое.
            for i in self.messages:
                try:
                    self.process_message(i, self.names, send_data_lst)
                except Exception:
                    server_logger.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                    self.clients.remove(self.names[i[DESTINATION]])
                    del self.names[i[DESTINATION]]
            self.messages.clear()

    @log
    def process_message(self, message, names, listen_socks):
        """
        Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
        список зарегистрированных пользователей и слушающие сокеты. Ничего не возвращает.
        :param message:
        :param names:
        :param listen_socks:
        :return:
        """
        if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
            send_message(names[message[DESTINATION]], message)
            server_logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                               f'от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            server_logger.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                f'отправка сообщения невозможна.')


def main():
    listen_address, listen_port = arg_parser()
    server = Server(listen_port, listen_address)
    server.main()


if __name__ == '__main__':
    main()
