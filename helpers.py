from models.userModel import userModel
import re

'''
Date: 27th Dec 2024
Purpose: this is the validate function used to verify the data
'''
class validate():
    def isValidEmail(email):
        emailRegex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(emailRegex, email) is not None

    def isValidPassword(password):
        passwordRegex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'
        return re.match(passwordRegex, password)
        
    def isValidPhone(phone):
        phoneRegex = r'^\d{10}$'
        return re.match(phoneRegex, phone)
    

    # this is the function, in which i want help
    # done 
    def validAllData(form):
        errors = []

        # Check if any required fields are missing
        if not form['firstName']:
            errors.append('FIRSTNAME is not given!')
        if not form['lastName']:
            errors.append('LASTNAME is not given!')
        if not form['username']:
            errors.append('USERNAME is not given!')
        if not form['email']:
            errors.append('EMAIL is not given!')
        if not form['phoneNumber']:
            errors.append('PHONE NUMBER is not given!')
        if not form['password']:
            errors.append('PASSWORD is not given!')

        # Validate email
        email = form['email']
        if email and not validate.isValidEmail(email):
            errors.append('Email is not valid')

        # Validate password
        password = form['password']
        if password and not validate.isValidPassword(password):
            errors.append('Password is not valid')

        # Validate phone number
        phone = form['phoneNumber']
        if phone and not validate.isValidPhone(phone):
            errors.append('Enter a valid 10-digit phone number')

        # Check for unique username in the database
        username = form['username']
        if username:
            name = userModel.getUsername(username)
            if name:
                errors.append('Username already exists!')

        # Return the list of errors (if any)
        if errors:
            print (errors)
            return errors
        else:
            return None
