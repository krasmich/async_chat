import sys
import logging
import logs.client_log_config
import logs.server_log_config
import inspect


if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(logged_function):
    def log_decorated(*args, **kwargs):
        ret = logged_function(*args, **kwargs)
        logger.debug(f'Была вызвана функция {logged_function.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {logged_function.__module__}.'
                     f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return ret
    return log_decorated
