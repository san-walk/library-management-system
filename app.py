from flask import Flask, request, redirect
from routes import main
from config import SECRETKEY


app = Flask(__name__)   # create a flask app
app.secret_key = SECRETKEY

'''
Date: 29th Dec 2024
Purpose: this function is used to handles all the invalid routes
'''
@app.errorhandler(404)
def not_found(e):
   return redirect('/')


app.register_blueprint(main)

if __name__ == '__main__':
   app.run(debug = True)



'''
Date: 7th Jan 2025
Command: alaways use 'flask --app app run --port=5542 --debug' to run this app
'''