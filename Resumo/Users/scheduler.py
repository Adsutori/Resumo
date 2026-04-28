import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command

logger = logging.getLogger(__name__)


def delete_unverified_users_job():
    try:
        call_command('delete_unverified_users')
    except Exception as e:
        logger.warning(f'delete_unverified_users failed: {e}')


def start():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            delete_unverified_users_job,
            trigger='interval',
            minutes=5,
            id='delete_unverified_users',
            replace_existing=True,
        )

        scheduler.start()
        logger.info('Scheduler uruchomiony.')

    except Exception as e:
        logger.warning(f'Scheduler nie mógł się uruchomić: {e}')
