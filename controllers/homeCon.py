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
    def get():
        if 'username' in session:
            print ('we got a session.')
            userModel.getUsername(session['username'])
            return redirect('/books')
        return redirect('/register')