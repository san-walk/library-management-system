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
        retun = reqModel.getReturnableReq(user)
        booksReq = reqModel.getUserRequest(user)
        return render_template('booksPage.html', books=booksData, approves=retun, requests=booksReq)

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
    
    def returnBook():
        print ('book is going to return user read this book or no longer wants this book.')
        book = request.form
        print (book)
        # update user details 
        userModel.changeReturn(book['issuedBy'], 1)
        userModel.changeIssue(book['issuedBy'], -1)
        # update books table
        bookModel.changeIssue(book['bookId'], -1)
        bookModel.changeAvailabe(book['bookId'], 1)
        # update request table
        reqModel.changeReturn(book['issuedBy'], book['bookId'])
        return redirect('/books')