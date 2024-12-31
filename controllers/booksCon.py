from flask import render_template, request, redirect, url_for, session
from models.userModel import userModel
from models.bookModel import bookModel
from models.requestModel import reqModel
from sqlalchemy.orm import sessionmaker
from connection import engine

Session = sessionmaker(engine)
dbSession = Session()

'''
Date: 27th Dec 2024
Purpose: books controller class to render booksPage.html
'''
class booksController():
    # get all the books on the web page
    def get():
        booksData = bookModel.getAllBooks()
        user = session['username']
        booksReq = reqModel.getUserRequest(user)
        return render_template('booksPage.html', books=booksData, requests=booksReq)

    def getAddBook():
        return render_template('newBookPage.html')

    def postAddBook():
        try:
            # get data from the form 
            newBook = request.form
            print (newBook)
            # store the data in database
            bookModel.addNewBook(newBook)
            return redirect('/admin')
        
        except Exception as e:
            dbSession.roolback()
            print (f'error {e}')


    def issueBook():
        print ("issue raised! from the booksController.py")
        newReq = request.form
        reqModel.addRequest(newReq)
        user = session['username']
        userModel.changePending(user, 1)
        return redirect('/books')