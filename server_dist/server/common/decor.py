import socket
import sys
import logging

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(logged_function):
    def log_decorated(*args, **kwargs):
        logger.debug(f'Была вызвана функция {logged_function.__name__} c параметрами {args}, {kwargs}. Вызов из модуля {logged_function.__module__}')
        ret = logged_function(*args, **kwargs)
        return ret
    return log_decorated


def login_required(func):
    """
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    """

    def checker(*args, **kwargs):

        from server_dist.server.server.core import MessageProcessor
        from server_dist.server.common.utils import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):

                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True

            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
