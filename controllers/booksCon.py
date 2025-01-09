from flask import render_template, request, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from connection import engine
from models.userModel import userModel
from models.bookModel import bookModel
from models.requestModel import reqModel
from helpers import validate

Session = sessionmaker(engine)
dbSession = Session()

'''
Date: 27th Dec 2024
Purpose: books controller class to render booksPage.html
'''
class booksController():
    # get all the books on the web page
    def get():
        if 'username' in session and session['admin'] == False:
            booksData = bookModel.getAllBooks()
            user = session['username']
            booksReq = reqModel.getUserRequest(user)
            if 'error' in session:
                error = session['error']
                session.pop('error', None)
                return render_template('booksPage.html', books=booksData, requests=booksReq, err=error)
            return render_template('booksPage.html', books=booksData, requests=booksReq)
        else: 
            return 'You are not logedin as user!<br><a href="http://localhost:5542/login">Click here to LOGIN</a>'
    
    # render add new book page
    def getAddBook():
        return render_template('newBookPage.html')

    # post the new book data
    def postAddBook():
        try:
            # get data from the form 
            newBook = request.form
            print (newBook)
            # validate the quantity
            quan = validate.naturalNum(newBook['quantity'])
            if not quan:
                print ('Enter the correct quantity!')
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

    # renders the update book page
    def getUpdateBook(book):
        return render_template('updateBookPage.html', book=book)
    
    # post the update data for the book
    def postUpdateBook():
        book = request.form
        bookId = book['id']
        error = bookModel.update(bookId, book)
        if error:
            session['error'] = error
            return redirect('/admin')
        return redirect('/admin')
    
    # function used to delete book by its id(bookID)
    def deleteBookByID():
        book = request.form
        bookId = book['id']
        # check for any issued user of the book
        reqs = reqModel.getAllReqByBook(bookId)
        if reqs:
            error = "Some books are already issued, Please wait for release and retry!"
            session['error'] = error
            return redirect(url_for('.admin'))
        reqModel.deleteReqByBookID(bookId)
        bookModel.deleteBook(bookId)
        return redirect('/admin')


    # function used to raised issue request for the book
    def issueBook():
        print ("issue raised! from the booksController.py")
        newReq = request.form
        user = session['username']
        ifReq = reqModel.checkIssue(newReq['referenceNumber'], user)
        if ifReq[1]:
            reqModel.addRequest(newReq)
            userModel.changePending(user, 1)
        else:
            session['error'] = ifReq[0]
            return redirect(url_for('.books'))
        return redirect('/books')
    
    # function used to return a book after
    def returnBook():
        print ('book is going to return user read this book or no longer wants this book.')
        book = request.form
        print (book)
        # update request table
        reqModel.changeReturn(book['issuedBy'], book['bookId'])
        # update user details 
        userModel.changeReturn(book['issuedBy'], 1)
        userModel.changeIssue(book['issuedBy'], -1)
        # update books table
        bookModel.changeIssue(book['bookId'], -1)
        bookModel.changeAvailabe(book['bookId'], 1)
        return redirect('/books')