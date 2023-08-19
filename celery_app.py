import os
import time
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_service.settings')

app = Celery('food_delivery_service')
app.config_from_object('django.conf:settings')
app.conf.task_default_queue = f'{app.main}@{os.getenv("CELERY_HOSTNAME", "localhost")}'
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(20)
    print('Hello form debug_task')