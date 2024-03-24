# -*- coding:utf-8 -*-
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# log文件夹名称
LOG_DIR_NAME = "logs"


class LogConfig(object):
    LOG_DIR_ABSPATH = ""

    @classmethod
    def create_log_dir(cls):
        """创建log文件夹"""
        if not cls.LOG_DIR_ABSPATH:
            cls.LOG_DIR_ABSPATH = os.path.join(BASE_DIR, LOG_DIR_NAME)

        if not os.path.exists(cls.LOG_DIR_ABSPATH):
            os.mkdir(cls.LOG_DIR_ABSPATH)

    @classmethod
    def log_file_abspath(cls, log_file_name):
        """
        生成log文件的绝对路径
        :param log_file_name: log文件名
        :return:
        """
        cls.create_log_dir()
        abspath = cls.LOG_DIR_ABSPATH + "/" + log_file_name
        return abspath


# 定义日志输出格式
COMPLEXITY = (
    "[%(levelname)-5s][%(asctime)s][thread:%(threadName)s{%(thread)d}][process:%(processName)s{%(process)d}]"
    "[module:%(name)s][line:%(lineno)d] %(message)s"
)
STANDARD = (
    "[%(levelname)-5s][%(asctime)s][module:%(name)s][line:%(lineno)d] %(message)s"
)
LOGGING_DICT = {
    "version": 1,
    "disable_existing_loggers": False,  # 禁用已经存在的logger实例
    "formatters": {
        "complexity": {"format": COMPLEXITY},
        "standard": {"format": STANDARD, "datefmt": "%Y-%m-%d %H:%M:%S"},
    },
    "handlers": {
        # 打印到终端的日志
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",  # 打印到屏幕
            "formatter": "standard",
        },
        # 输出错误日志到错误日志
        "file_error": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",  # 保存到文件
            "when": "midnight",
            "interval": 1,
            "formatter": "standard",
            "filename": LogConfig.log_file_abspath("error.log"),  # 日志文件路径
            # 'maxBytes': 1024 * 1024 * 200,  # 日志大小 200M
            "backupCount": 5,  # 备份5个日志文件
            "encoding": "utf-8",  # 日志文件的编码，再也不用担心中文log乱码了
        },
        "file_ai_server": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",  # 保存到文件
            "when": "midnight",  # 按天分割
            "interval": 1,  # 分割周期1
            "formatter": "standard",
            "filename": LogConfig.log_file_abspath("ai_server.log"),  # 日志文件路径
            # 'maxBytes': 1024 * 1024 * 200,  # 日志大小 200M
            "backupCount": 5,  # 备份5个日志文件
            "encoding": "utf-8",  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    # logger实例
    "loggers": {
        # 默认的logger配置如下,
        # logging.getLogger(__name__)生成的不确定名字的logger都会使用默认logger,
        # 默认的logger会用'root'中的配置。
        "": {  # 默认的logger
            # 'handlers': ['console'],
            "level": "DEBUG",
            "propagate": False,  # 不向父级传递
        },
        "django": {"level": "ERROR", "handlers": ["console"], "propagate": False, },
    },
    "root": {
        "handlers": ["console", "file_ai_server", "file_error"],  # 输出日志到控制台、项目日志、错误日志
        # 'level': 'DEBUG',
        "level": "INFO",
    },
}
