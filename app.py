from flask import Flask, request
from routes import main
from config import SECRETKEY


app = Flask(__name__)   # create a flask app
app.secret_key = SECRETKEY


app.register_blueprint(main)

if __name__ == '__main__':
   app.run(debug = True)