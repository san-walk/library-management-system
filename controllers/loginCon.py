from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, session, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from connection import engine
from models.userModel import userModel
from helpers import validate


Session = sessionmaker(engine)
dbSession = Session()


'''
Date: 26th Dec 2024
Purpose: this class has the required functions for the login task
'''
class loginController():
    # get login page where session is also checked
    def get():
        if 'username' in session:
            return validate.ifSession(session)
        error = ''
        if 'error' in session:
            error = session['error']
            session.pop('error', None)
        return render_template('loginPage.html', err=error)

    # post login function to verify user/admin 
    def post():
        try:
            # get data from the form
            loginCredentials = request.form
            print (loginCredentials)

            # check username from the class function
            confirmUser = True
            isUser = userModel.getUserData(loginCredentials['username'])
            if not isUser:
                confirmUser = False
                session['error'] = "Username not found!"
                return redirect(url_for('.login'))

            # check password from the class function
            confirmPassword = False
            enteredPassword = loginCredentials['password']
            storedPassword = isUser.password
            if check_password_hash(storedPassword, enteredPassword):
                print ('password matched!')
                confirmPassword = True
            else:
                print ('password incorrect!')
            
            # continue login if username and password is correct
            if confirmUser and confirmPassword:
                session['username'] = loginCredentials['username']
                session['admin'] = False
                # check user is admin or not
                userIsAdmin = False
                admin = userModel.getAdmin(loginCredentials['username'])
                if admin:
                    session['admin'] = True
                    userIsAdmin = True

                return redirect('/admin') if userIsAdmin else redirect('/books')
                
            else:
                session['error'] = "Incorrect password!"
                return redirect('/login')

        except Exception as e:
            dbSession.rollback()
            print(f"error {e}")


'''
Date: 27th Dec 2024
Purpose: this class is resposible for logout, it is not required to define this class in different file, it is ok for this project
'''    
class logoutController():
    # logout function which clears the session
    def logout():
        if 'username' in session:
            print (session['username'])
            session.pop('username', None)
            session.pop('admin', None)
        return redirect('/login')
