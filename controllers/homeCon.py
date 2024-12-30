from flask import redirect, session
from models.userModel import userModel
from sqlalchemy.orm import sessionmaker
from connection import engine


Session = sessionmaker(engine)
dbSession = Session()

'''
Date: 27th Dec 2024
Purpose: home controller class called at home route, but never showed it redirects to the register page
'''
class homeController():
    # home route redirected to the register page
    def get():
        if 'username' in session:
            print ('we got a session.')
            isUser = userModel.getAdmin(session['username'])
            return redirect('/admin') if isUser else redirect('/books')
        return redirect('/register')