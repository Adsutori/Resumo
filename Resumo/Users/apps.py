# Users/apps.py

import os
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class UsersConfig(AppConfig):
    name = 'Users'

    def ready(self):
        # Uruchom scheduler tylko w głównym procesie Django,
        # nie przy migrate / collectstatic / podwójnym starcie reloadera
        if os.environ.get('RUN_MAIN') != 'true':
            return

        try:
            from . import scheduler
            scheduler.start()
        except Exception as e:
            logger.warning(f'Scheduler pominięty przy starcie: {e}')
