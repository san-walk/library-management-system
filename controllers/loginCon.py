from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, session
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
        
            # print ('we got a session.')
            # isUser = userModel.getAdmin(session['username'])
            # return redirect('/admin') if isUser else redirect('/books')
        return render_template('loginPage.html')

    # post login function to verify user/admin 
    def post():
        try:
            # get data from the form
            loginCredentials = request.form
            print (loginCredentials)

            # check username from the class function
            confirmUser = False
            userN = loginCredentials['username']
            name = userModel.getPassword(userN)
            if name:
                print ('username got!')
                confirmUser = True
            else: 
                print ('username incorrect!')


            # check password from the class function
            confirmPassword = False
            enteredPassword = loginCredentials['password']
            # storedPassword = userModel.getPassword(userN)      # TODO : Duplicate query
            userData = userModel.getPassword(userN)
            if userData[0] and check_password_hash(userData[0], enteredPassword):
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
                err = "Invalid Credentials!"
                return render_template('loginPage.html', err = err)

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
        print (session['username'])
        session.pop('username', None)
        session.pop('admin', None)
        return redirect('/login')