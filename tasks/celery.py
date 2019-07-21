from celery.schedules import crontab
from datetime import timedelta

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'sum-task': {
            'task': 'tasks.tasks.add',
            'schedule':  timedelta(seconds=20),
            'args': (5, 6)
        },
        'send-report': {
            'task': 'tasks.tasks.report',
            'schedule': crontab(hour=4, minute=30, day_of_week=1),
        }
    }
)