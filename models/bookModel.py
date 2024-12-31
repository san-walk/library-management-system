from sqlalchemy import Column, String, Integer, Boolean, create_engine, UniqueConstraint
from connection import engine, Base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)
dbSession = Session()

'''
Date: 24th Dec 2024
Purpose: this is the class for the book model from which a book is defined.
'''
class bookModel(Base):
    __tablename__ = "books"

    snum = Column(Integer, primary_key=True, autoincrement=True)
    bookName = Column(String)
    author = Column(String)
    referenceNumber = Column(Integer)
    issued = Column(Integer, default=0)
    quantity = Column(Integer)
    available = Column(Integer, default=quantity)

    # method to get all the books
    @staticmethod
    def getAllBooks():
        booksData = dbSession.query(bookModel).all()
        return booksData
    
    @staticmethod
    def addNewBook(newBook):
        print ("data of new book is going to fillin the bookModel")
        book = bookModel(
            bookName = newBook['bookName'],
            author = newBook['author'],
            referenceNumber = newBook['referenceNumber'],
            issued = 0,
            quantity = newBook['quantity'],
            available = newBook['quantity']
        )
        dbSession.add(book)
        dbSession.commit()
        print ('data is commited successfully!')


    @staticmethod
    def changeIssue(id, num):
        issue = dbSession.query(bookModel).filter(bookModel.referenceNumber==id).first()
        issue.issued += num
        dbSession.add(issue)
        dbSession.commit()

    @staticmethod
    def changeAvailabe(id, num):
        issue = dbSession.query(bookModel).filter(bookModel.referenceNumber==id).first()
        issue.available += num
        dbSession.add(issue)
        dbSession.commit()