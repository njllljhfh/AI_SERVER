"""
ASGI config for AI_SERVER project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import logging
import os
from django.core.asgi import get_asgi_application

operation_logger = logging.getLogger("OPERATION")

# ENV = os.getenv("AI_SERVER_ENV")
ENV = 'production'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings." + ENV)

application = get_asgi_application()
