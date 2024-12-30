from flask import render_template, request, redirect, url_for, session
from models.bookModel import bookModel
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
        print (booksData)
        return render_template('booksPage.html', books = booksData)
