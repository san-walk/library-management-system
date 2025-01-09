from celery import Celery
from app import app
from config import keys

app.config['CELERY_BROKER_URL'] = keys.CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = keys.CELERY_RESULT_BACKEND



def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)


@celery.task
def add_numbers(a, b):
   return a+b