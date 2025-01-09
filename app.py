from flask import Flask, request, redirect, jsonify
from flask_mail import Mail
from config import keys


# app = Flask(__name__)   # create a flask app

mail = Mail()
def create_app():
   app = Flask(__name__)
   app.secret_key = keys.SECRETKEY

   app.config['MAIL_SERVER'] = keys.MAIL_SERVER
   app.config['MAIL_PORT'] = keys.MAIL_PORT
   app.config['MAIL_USE_TLS'] = True
   app.config['MAIL_USERNAME'] = keys.MAIL_USER
   app.config['MAIL_PASSWORD'] = keys.MAIL_PASS
   
   mail.init_app(app)
   from routes import main
   app.register_blueprint(main)
   return app

# @main.route('/homeee')
# def add():
#    x = 34
#    y = 43
#    from tasks import add_numbers
#    task = add_numbers.apply_async(args=[x, y])
#    print (task.id)
#    if task.state == "PENDING":
#       return jsonify({"tasks": task.id, "status": task.state})
#    elif task.state == "SUCCESS":
#       return task.get()
#    else:
#       return jsonify({"tasks": task.id})


'''
Date: 29th Dec 2024
Purpose: this function is used to handles all the invalid routes
'''
# @app.errorhandler(404)
# def not_found(e):
#    return redirect('/')



# app.register_blueprint(main)
# app = create_app()
# if __name__ == '__main__':
#    app.run(debug = True)



'''
Date: 7th Jan 2025
Command: alaways use 'flask --app app run --port=5542 --debug' to run this app
'''