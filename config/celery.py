import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.conf.broker_url = "redis://metsenat_redis:6379/0"
app.conf.timezone = "Asia/Tashkent"
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every minute
    'send-students-info': {
        'task': 'apps.sponsors.tasks.send_students_info',
        'schedule': crontab(minute='*/1'),
    },
}