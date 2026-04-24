from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command

def delete_unverified_users_job():
    call_command('delete_unverified_users')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        delete_unverified_users_job,
        trigger='interval',
        minutes=5,              # ← co 5 minut
        id='delete_unverified_users',
        replace_existing=True,
    )

    scheduler.start()
