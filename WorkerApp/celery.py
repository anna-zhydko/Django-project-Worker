import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkerApp.settings')
app = Celery('WorkerApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Europe/Kiev'

app.conf.beat_schedule = {
    'work_ua_insert_3_am': {
        'task': 'main.tasks.work_ua_insert',
        'schedule': crontab(hour=11, minute=40)
    }
}

app.conf.beat_schedule = {
    'work_ua_insert_3_am': {
        'task': 'main.tasks.rabota_ua_insert',
        'schedule': crontab(hour=11, minute=40)
    }
}

app.conf.beat_schedule = {
    'work_ua_insert_3_am': {
        'task': 'main.tasks.jooble_insert',
        'schedule': crontab(hour=11, minute=40)
    }
}