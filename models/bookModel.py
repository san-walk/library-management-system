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

    # method to get all the books
    @staticmethod
    def getAllBooks():
        booksData = dbSession.query(bookModel).all()
        return booksData
