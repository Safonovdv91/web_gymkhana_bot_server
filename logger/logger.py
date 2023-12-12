import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from src.config import LOG_LEVEL
import os

path = os.path

logger = logging.getLogger()
logHandler = logging.StreamHandler()

fileHandler = logging.FileHandler("logger/journals/log_file.log")


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

# Добавляем обработчик файлового журнала в логгер
logger.addHandler(fileHandler)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(LOG_LEVEL)
