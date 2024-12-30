from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import sessionmaker
from models.userModel import userModel
from connection import engine
from sqlalchemy import text
from helpers import validate


Session = sessionmaker(engine)
dbSession = Session()


'''
Date: 26th Dec 2024
Purpose: this class has the required functions for the registration form which is imported in routes.py file
'''
class registrationController():
    def get():
        if 'username' in session:
            print ('we got a session.')
            isUser = userModel.getAdmin(session['username'])
            return redirect('/admin') if isUser else redirect('/books')
        return render_template('registrationPage.html')
    
    def post():
        try:
            # get data from the form
            print ("post_registration_controller running......")
            registrationData = request.form     # form data got
            print (registrationData)            # print the data in the terminal

            # validation of the form data
            errors = validate.validAllData(registrationData)
            if errors: 
                return f'{errors}'
            
            # store the data in database
            hashedPassword = generate_password_hash(registrationData['password'])
            print ('data is going to fillin the userModel.')
            user = userModel(
                firstName = registrationData['firstName'], 
                lastName = registrationData['lastName'], 
                username = registrationData['username'], 
                email = registrationData['email'], 
                phoneNumber = registrationData['phoneNumber'], 
                password = hashedPassword
            )
            # here data is going to store in the database
            dbSession.add(user)                   # add data in the database
            dbSession.flush()
            dbSession.commit()                    # commit the data in database
            session['username'] = registrationData['username']      # session is maintained
            return redirect(f'books')
            
        except Exception as e:
            dbSession.rollback()
            print (f"error {e}")
