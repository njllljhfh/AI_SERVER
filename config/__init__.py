import pymysql
# from .Celery import app as celery_app
#
pymysql.version_info = (2, 0, 1, "final", 0)
pymysql.install_as_MySQLdb()
#
# __all__ = ("celery_app",)
