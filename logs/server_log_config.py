import sys
import os
import logging
import logging.handlers

from utils import LOGGING_LEVEL

sys.path.append('../')
# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')


# Создаем объект-логгер
logger = logging.getLogger('server')
logger.setLevel(LOGGING_LEVEL)

# Создаем объект форматирования:
server_format = logging.Formatter('%(asctime)s %(levelname)-10s %(filename)s %(message)s')

# Создаем файловый обработчик логирования
sh = logging.StreamHandler(sys.stderr)
# Устанавливаем уровень логирования
sh.setLevel(logging.ERROR)

sh.setFormatter(server_format)

# Добавляем в логгер новый обработчик событий
trfh = logging.handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='D')
trfh.setFormatter(server_format)


logger.addHandler(sh)
logger.addHandler(trfh)


# отладка
if __name__ == '__main__':
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
