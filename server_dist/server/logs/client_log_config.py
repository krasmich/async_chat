import sys
import os
import logging

from server_dist.server.logs.server_log_config import LOGGING_LEVEL
# from utils import LOGGING_LEVEL


# sys.path.append('../')
# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.log')


# Создаем объект-логгер
logger = logging.getLogger('client')
logger.setLevel(LOGGING_LEVEL)

client_format = logging.Formatter('%(asctime)s %(levelname)-10s %(filename)s %(message)s')

# Создаем файловый обработчик логирования
sh = logging.StreamHandler(sys.stderr)
# Устанавливаем уровень логирования
sh.setLevel(logging.ERROR)

sh.setFormatter(client_format)


fh = logging.FileHandler(path, encoding='utf8')
fh.setFormatter(client_format)

logger.addHandler(sh)
logger.addHandler(fh)

# отладка
if __name__ == '__main__':
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
