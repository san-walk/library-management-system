from flask import Flask, request, redirect, jsonify
from routes import main
from config import keys
# from tasks import make_celery


app = Flask(__name__)   # create a flask app
app.secret_key = keys.SECRETKEY


'''
Date: 7th Jan 2025
Purpose: celery is intigrated with this project and going to used new tasks by celery
'''
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# celery = make_celery(app)


@main.route('/homeee')
def add():
   x = 34
   y = 43
   from tasks import add_numbers
   task = add_numbers.apply_async(args=[x, y])
   print (task.id)
   # return task.get() if task.state == "SUCCESS" else 'waiting for your response.'
   # print (task.get())
   if task.state == "PENDING":
      return jsonify({"tasks": task.id, "status": task.state})
   elif task.state == "SUCCESS":
      return task.get()
   else:
      return jsonify({"tasks": task.id})


'''
Date: 29th Dec 2024
Purpose: this function is used to handles all the invalid routes
'''
# @app.errorhandler(404)
# def not_found(e):
#    return redirect('/')


# @celery.task
# def add_numbers(a, b):
#    return a+b



app.register_blueprint(main)

if __name__ == '__main__':
   app.run(debug = True)



'''
Date: 7th Jan 2025
Command: alaways use 'flask --app app run --port=5542 --debug' to run this app
'''