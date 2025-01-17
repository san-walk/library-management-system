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
    # get registration form page where session is also checks for any logedin user
    def get():
        if 'username' in session:
            print ('we got into the session for the getregistration form! registration controller........')
            return validate.ifSession(session)
        return render_template('registrationPage.html')
    
    # post the registration data on the database
    def post():
        try:
            # get data from the form
            print ("post_registration_controller running......")
            registrationData = request.form     # form data got
            print (registrationData)            # print the data in the terminal

            # validation of the form data
            errors = validate.validAllData(registrationData)
            if errors: 
                return render_template('registrationPage.html', err = errors[0])
            
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
            session['admin'] = False
            # send email task after the succesfully registered
            sendTo = user.email
            mailSubject = 'Thanks for creating your account.'
            mailBody = 'Your account is created successfully, thanks for registering. Our library has a huge variety of books. You can issue books from now on. Once the issue is requested you have to wait for the librarian to approve your issued book. The librarian has the othority to approve or reject your issue, please don\'t perform any misleading actions on the behalf of library.'
            from tasks import sendEmail
            task = sendEmail.apply_async(args=[mailSubject, sendTo, mailBody])
            return redirect(f'books')
            
        except Exception as e:
            dbSession.rollback()
            print (f"error {e}")
