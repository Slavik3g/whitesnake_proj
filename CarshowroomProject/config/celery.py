import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('proj', broker='redis://redis:6379/0', broker_connection_retry_on_startup=True)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'buy_car_from_supplier': {
        'task': 'applications.carshowroom.tasks.buy_car_from_supplier',
        'schedule': crontab(minute='*/1'),
    },
    'check_suppliers_benefit': {
        'task': 'src.carshowroom.tasks.check_suppliers_benefit',
        'schedule': crontab(minute='0', hour='*/1'),
    },
    # 'accept_offer': {
    #     'task': 'src.carshowroom.tasks.accept_offer',
    #     'schedule': crontab(minute='*/10'),
    # }
}
