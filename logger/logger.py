import logging.config
import logging_loki
import logging
import logging.handlers
from src.config import LOGGER_LOKI_URL, LOG_LEVEL


class MyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        print(record.__dict__)
        return True


def init_logger(name):
    """ Инициализация логгера
    sh_level - уровень логгера на отображение в экране
    fh_level: int = 30 - уровень логгера для записи в файл
    """

    LOGER_FORMAT = "%(name)s:%(lineno)s - %(levelname)s - %(message)s"

    loki_logger = logging.getLogger(name)
    loki_handler = logging_loki.LokiHandler(
        url=LOGGER_LOKI_URL,
        tags={"application": "rabbit-mg-app"},
        # auth=("username", "password"),
        version="1",
    )

    loki_handler.setFormatter(logging.Formatter(LOGER_FORMAT))
    loki_logger.addHandler(loki_handler)
    loki_logger.setLevel(LOG_LEVEL)

    return loki_logger


logger = init_logger("unnamed_logger")

def main():
    logger = init_logger("test_logger")
    logger.info("START TEST LOGGING")
    logger.debug("DEBUG test msg")
    logger.info("INFO test msg")
    logger.warning("WARNING test msg")
    status_code = 201
    logger.warning(f"WARNING test msg with extra code :[{status_code}]", extra={
        "tags": {
            "status_code": str(status_code)
        }
    })
    status_code = 400
    logger.error("ERROR test msg")
    logger.error(f"ERROR test msg with extra status code: [{status_code}]", extra={
        "tags": {
            "status_code": str(status_code)
        }
    })
    status_code = 500
    logger.critical("CRITICAL test msg")
    logger.critical(f"CRITICAL test msg with extra status code [{status_code}]",  extra={
        "tags": {
            "status_code": str(status_code)
        }
    })
    try:
        print(10 / 0)
    except Exception as e:
        logger.exception(e)

    print("Test logger has been finished")


if __name__ == "__main__":
    main()
