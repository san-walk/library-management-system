from flask_mail import Message
from celery import Celery
from app import create_app, mail
from config import keys


app = create_app()

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

@celery.task
def send_email(subject, recipient, body):
    with app.app_context():
        msg = Message(subject, sender = keys.MAIL_USER, recipients = [recipient])
        msg.body = body
        mail.send(msg)