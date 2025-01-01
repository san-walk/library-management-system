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
        if 'error' in session:
            error = session['error']
            session.pop('error', None)
            return render_template('booksPage.html', books=booksData, requests=booksReq, err=error)
        return render_template('booksPage.html', books=booksData, requests=booksReq)

    def getAddBook():
        return render_template('newBookPage.html')

    def postAddBook():
        try:
            # get data from the form 
            newBook = request.form
            print (newBook)
            print (newBook['referenceNumber'])
            # check for the existing reference number
            error = bookModel.CheckReferenceNum(newBook['referenceNumber'])
            if error:
                return render_template('/newBookPage.html', err=error)
            # store the data in database
            bookModel.addNewBook(newBook)
            return redirect('/admin')
        
        except Exception as e:
            dbSession.roolback()
            print (f'error {e}')

    def getUpdateBook(book):
        return render_template('updateBookPage.html', book=book)
    
    def postUpdateBook():
        book = request.form
        bookId = book['id']
        bookModel.update(bookId, book)
        return redirect('/admin')
    
    def deleteBookByID():
        book = request.form
        bookId = book['id']
        reqs = reqModel.getAllReqByBook(bookId)
        if reqs:
            for req in reqs:
                print (req.bookId, ' this book is issued by ------> ', req.issuedBy, ' and the book name is ------> ', req.bookName)
                _user = req.issuedBy
                userModel.changeIssue(_user, -1)
        reqModel.deleteReqByBookID(bookId)
        bookModel.deleteBook(bookId)
        return redirect('/admin')


    def issueBook():
        print ("issue raised! from the booksController.py")
        newReq = request.form
        user = session['username']
        ifReq = reqModel.checkIssue(newReq['referenceNumber'], user)
        if ifReq == None:
            reqModel.addRequest(newReq)
            userModel.changePending(user, 1)
        else:
            error = "Request another book, you already requsted this book!"
            session['error'] = error
            return redirect(url_for('.books'))
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