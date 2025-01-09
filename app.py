from flask import Flask, request, redirect, jsonify
from flask_mail import Mail
from config import keys



mail = Mail()
def create_app():
   app = Flask(__name__)
   app.secret_key = keys.SECRETKEY

   app.config['MAIL_SERVER'] = keys.MAIL_SERVER
   app.config['MAIL_PORT'] = keys.MAIL_PORT
   app.config['MAIL_USE_TLS'] = True
   app.config['MAIL_USE_SSL'] = False
   app.config['MAIL_USERNAME'] = keys.MAIL_USER
   app.config['MAIL_PASSWORD'] = keys.MAIL_PASS
   
   mail.init_app(app)
   from routes import main
   app.register_blueprint(main)
   return app



'''
Date: 7th Jan 2025
Command: alaways use 'flask --app app run --port=5542 --debug' to run this app
'''