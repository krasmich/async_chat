import json
import socket
import sys

from utils import create_presence, receive_message, process_server_answer, send_message, PORT, HOST


def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = HOST
        server_port = PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от  1024 до 65535.')
        sys.exit(1)

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(clientsocket, message_to_server)

    try:
        answer = process_server_answer(receive_message(clientsocket))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
