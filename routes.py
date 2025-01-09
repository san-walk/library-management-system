import flask
from flask import Flask, jsonify, request, redirect, Blueprint
from controllers.registrationCon import registrationController
from controllers.homeCon import homeController
from controllers.booksCon import booksController
from controllers.loginCon import loginController, logoutController
from controllers.adminCon import adminController
# from models.userModel import userModel

main = Blueprint('main', __name__)



@main.errorhandler(404)
def not_found(e):
   return redirect('/')

'''
Date: 27th Dec 2024
Purpose: this is the home route
'''
@main.route('/')
def home():
    return homeController.get()

'''
Date: 24th Dec 2024
Purpose: route for the home page as registration page
'''
@main.route('/register')
def getRegistrationForm():
    return registrationController.get()

'''
Date: 24th Dec 2024
Purpose: registering the user details after form fillup and submit the data
'''
@main.route('/register', methods = ['POST'])
def postRegistrationForm():
    return registrationController.post()

'''
Date: 24th Dec 2024
Purpose: route for login page 
'''
@main.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return loginController.get()
    else:
        return loginController.post()


'''
Date: 27th Dec 2024
Purpose: route for the books page
'''
@main.route('/books')
def books():
    return booksController.get()

'''
Date: 31st Dec 2024
Purpose: route to get addBooksPage to add new book
'''
@main.route('/books/add-new')
def addBook():
    return booksController.getAddBook()

'''
Date: 31st Dec 2024
Purpose: route to post the new book data
'''
@main.route('/books/add-new', methods = ['POST'])
def postBook():
    return booksController.postAddBook()

'''
Date: 1st Jan 2025
Purpose: route to get books update page
'''
@main.route('/books/update', methods = ['GET', 'POST'])
def getUpdateBookPage():
    if request.method == 'GET':
        return redirect('/')
    book = request.form
    print (book)
    return booksController.getUpdateBook(book)

'''
Date: 1st Jan 2025
Purpose: route to post the books update
'''
@main.route('/books/update/confirm', methods = ['GET', 'POST'])
def postUpdateBook():
    if request.method == 'GET':
        return redirect('/')
    return booksController.postUpdateBook()

'''
Date: 1st Jan 2025
Purpose: route to delete the book
'''
@main.route('/books/delete', methods = ['GET', 'POST'])
def deleteBook():
    if request.method == 'GET':
        return redirect('/')
    return booksController.deleteBookByID()


'''
Date: 31st Dec 2024
Purpose: route used to issue book by user
'''
@main.route('/books/issue', methods = ['GET', 'POST'])
def issueBook():
    if request.method == 'GET':
        return redirect('/')
    return booksController.issueBook()

'''
Date: 31st Dec 2024
Purpose: route used to return a book by user
'''
@main.route('/books/return', methods = ['GET', 'POST'])
def returnBook():
    if request.method == 'GET':
        return redirect('/')
    return booksController.returnBook()


'''
Date: 27th Dec 2024
Purpose: route for the admin page, where admin can see user list
'''
@main.route('/admin')
def admin():
    return adminController.get()


'''
Date: 27th Dec 2024
Purpose: route for the logout task
'''
@main.route('/logout')
def simple():
    return logoutController.logout()


'''
Date: 28th Dec 2024
Purpose: get route for updating the user
'''
@main.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'GET':
        return redirect('/')
    user = request.form
    print (user['username'])
    if not user:
        return redirect('/')
    return adminController.getUpdate(user)
    

'''
Date: 28th Dec 2024
Purpose: this route is used to post any update then redirect to the admins route
'''
@main.route('/update/confirm', methods = ['GET', 'POST'])
def submitUpdate():
    if request.method == 'GET':
        return redirect('/')
    user = request.form.get('username')
    return adminController.postUpdate(user)


'''
Date: 28th Dec 2024
Purpose: this route used to delete a user, only admins can delete users
'''
@main.route('/delete-user', methods = ['GET', 'POST'])
def deleteUser():
    if request.method == 'GET':
        return redirect('/')
    user = request.form.get('username')
    return adminController.deleteUser(user)


'''
Date: 31st Dec 2024
Purpose: post route used to approve issued request for book
'''
@main.route('/approve', methods = ['GET', 'POST'])
def approve():
    if request.method == 'GET':
        return redirect('/')
    return adminController.approveReq()

'''
Date: 31st Dec 2024
Purpose: post route used to reject issued request for book
'''
@main.route('/reject', methods = ['GET', 'POST'])
def reject():
    if request.method == 'GET':
        return redirect('/')
    return adminController.rejectReq()
