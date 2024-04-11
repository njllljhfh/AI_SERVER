"""
WSGI config for AI_SERVER project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import logging
import os


from django.conf import settings
from django.core.wsgi import get_wsgi_application

operation_logger = logging.getLogger("OPERATION")

# ENV = os.getenv("AI_SERVER_ENV")
ENV = 'production'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings." + ENV)

# MinIo客户端
# MinioClient = Minio(
#     # 节点
#     endpoint=settings.MINIO_ENDPOINT,
#     # 账号
#     access_key=settings.MINIO_ACCESS_KEY,
#     # 密码
#     secret_key=settings.MINIO_SECRET_KEY,
#     # 是否使用TLS
#     secure=settings.MINIO_SECURE,
# )
# MinioDownLoadClient = Minio(
#     # 节点
#     endpoint=settings.MINIO_DOWNLOAD_ENDPOINT,
#     # 账号
#     access_key=settings.MINIO_ACCESS_KEY,
#     # 密码
#     secret_key=settings.MINIO_SECRET_KEY,
#     # 是否使用TLS
#     secure=settings.MINIO_SECURE,
# )
# if not MinioClient.bucket_exists(settings.MINIO_BUCKET):
#     MinioClient.make_bucket(settings.MINIO_BUCKET)
#
# RedisClient = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=3)
# ResultRedisClient = redis.Redis(
#     host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=4
# )#与celery result相同
# StopRedisClient = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=5)
# REDIS_CNN = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, decode_responses=True)  # 自动任务队列
application = get_wsgi_application()
