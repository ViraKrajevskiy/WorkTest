from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# указываем Django настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configproject.settings')

app = Celery('configproject')

# читаем конфигурацию из settings.py с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# автоматически ищем tasks.py во всех приложениях
app.autodiscover_tasks()
