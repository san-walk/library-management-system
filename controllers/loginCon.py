from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from connection import engine
from models.userModel import userModel


Session = sessionmaker(engine)
dbSession = Session()


'''
Date: 26th Dec 2024
Purpose: this class has the required functions for the login task
'''
class loginController():
    def get():
        return render_template('loginPage.html')

    def post():
        try:
            # get data from the form
            loginCredentials = request.form
            print (loginCredentials)

            # check username from the class function
            confirmUser = False
            userN = loginCredentials['username']
            name = userModel.getUsername(userN)
            if name:
                print ('username got!')
                confirmUser = True
            else: 
                print ('username incorrect!')


            # check password from the class function
            confirmPassword = False
            enteredPassword = loginCredentials['password']
            storedPassword = userModel.getPassword(userN)
            if storedPassword and check_password_hash(storedPassword[0], enteredPassword):
                print ('password matched!')
                confirmPassword = True
            else:
                print ('password incorrect!')
            
            # continue login if username and password is correct
            if confirmUser and confirmPassword:
                # check user is admin or not
                userIsAdmin = False
                admin = userModel.getAdmin(loginCredentials['username'])
                if admin:   
                    userIsAdmin = True

                return redirect('/admin') if userIsAdmin else redirect('/books')
                
            else:
                return 'Incorrect Credentials!'

        except Exception as e:
            dbSession.rollback()
            print(f"error {e}")


'''
Date: 27th Dec 2024
Purpose: this class is resposible for logout, it is not required to define this class in different file, it is ok for this project
'''    
class logoutController():
    def logout():
        session.pop('username', None)
        return redirect('/')