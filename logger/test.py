import logging
import logging_loki


handler = logging_loki.LokiHandler(
    url="http://127.0.0.1:3100/loki/api/v1/push",
    tags={"application": "my-app"},
    # auth=("username", "password"),
    version="1",
)

logger = logging.getLogger("my-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.error(
    "[ERROR]Something happened",
    extra={"tags": {"service": "my-service"}},
)
logger.warning(
    "[WARNING]Something happened",
    extra={"tags": {"service": "my-service"}},
)
logger.info(
    "[INFO] My new info",
    extra={"tags": {"service": "my-service"}},
)
