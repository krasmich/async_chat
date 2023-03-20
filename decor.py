import sys
import logging
import logs.client_log_config
import logs.server_log_config


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
