from flask import redirect
from flask_mail import Message
from celery import Celery
from app import create_app, mail
from config import keys


app = create_app()

# configure the app celery broker and backend
app.config['CELERY_BROKER_URL'] = keys.CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = keys.CELERY_RESULT_BACKEND


'''
Date: 29th Dec 2024
Purpose: this function is used to handles all the invalid routes
'''
@app.errorhandler(404)
def not_found(e):
   return redirect('/')


'''
Date: 8th Jan 2025
Purpose: this function creates the celery app
'''
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)


'''
Date: 9th Jan 2025
Purpose: function made to send emails to the user
'''
@celery.task
def sendEmail(subject, recipient, body):
    with app.app_context():
        msg = Message(subject=subject, sender=keys.MAIL_USER, recipients=[recipient])
        msg.body = body
        mail.send(msg)
        print ('Mail sent successfully!')