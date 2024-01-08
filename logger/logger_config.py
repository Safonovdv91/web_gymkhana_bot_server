# import logging
#
#
# class MyFilter(logging.Filter):
#     def filter(self, record):
#         """
#         Determine if the specified record is to be logged.
#
#         Returns True if the record should be logged, or False otherwise.
#         If deemed appropriate, the record may be modified in-place.
#         """
#         return True
#
#
# class InfoFilter(logging.Filter):
#     def filter(self, record: logging.LogRecord) -> bool:
#         if record.levelno == 20:
#             return True
#
#
# class WarningFilter(logging.Filter):
#     def filter(self, record: logging.LogRecord) -> bool:
#         if record.levelno == 30:
#             return True
#
#
# logger_conf = {
#     "version": 1,
#     "formatters": {
#         "console_msg": {
#             "format": "[{levelname}]file:-> {filename} func:-> {funcName}[{lineno}]: '{msg}'",
#             "style": "{"
#         }
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "level": "DEBUG",
#             "formatter": "console_msg"
#         },
#         "file_info": {
#             "class": "logging.FileHandler",
#             "level": "INFO",
#             "formatter": "console_msg",
#             "filename": "log_INFO.log",
#             "filters": ["info_filter"]
#         },
#         "file_warning": {
#             "class": "logging.FileHandler",
#             "level": "WARNING",
#             "formatter": "console_msg",
#             "filename": "log_WARNING.log",
#             "filters": ["warning_filter"]
#         },
#         "file_all_data": {
#             "class": "logging.FileHandler",
#             "level": "WARNING",
#             "formatter": "console_msg",
#             "filename": "application_logs.log",
#             "filters": ["my_filter"]
#         },
#     },
#     "filters": {
#         "my_filter": {
#             "()": MyFilter
#
#         },
#         "info_filter": {
#             "()": InfoFilter
#
#         },
#         "warning_filter": {
#             "()": WarningFilter
#
#         },
#
#     },
#     "loggers": {
#         "my_python_logger": {
#             "level": "INFO",
#             "handlers": ["console", "file_warning", "file_info", "file_all_data"],
#             "filters": ["my_filter"]
#         },
#     }
# }
