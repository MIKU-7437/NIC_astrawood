from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from scripts.backup_db import run_backup
from celery.schedules import crontab

# Установите переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_api.settings')

# Создайте приложение Celery
app = Celery('backend_api')

# Загрузите настройки из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически искать задачи
app.autodiscover_tasks(['scripts'])

# Настройки для подключения к Redis
broker_connection_retry_on_startup = True

# Настройка расписания задач
app.conf.beat_schedule = {
    'backup-database-every-day': {
        'task': 'scripts.backup_db.run_backup',
        'schedule': crontab(minute=0, hour=12),  # Запускать каждый день в 12:00
    },
}

app.conf.timezone = 'UTC'
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
