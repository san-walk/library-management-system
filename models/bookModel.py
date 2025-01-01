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
    __table_args__ = (UniqueConstraint('referenceNumber', name='_referenceNumber_uc'),)


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

    def CheckReferenceNum(bookID):
        book = dbSession.query(bookModel).filter(bookModel.referenceNumber==bookID).first()
        if book:
            err = 'Book already exists with this reference number!'
            print (err)
            return err
        else:
            return None

    @staticmethod
    def update(bookID, updateCrentials):    # TODO : Add validations here too similar to register user
        book = dbSession.query(bookModel).filter(bookModel.referenceNumber==bookID).first()
        if not book:
            print ('user not found!')
            return
        print (book)
        book.bookName = updateCrentials['bookName']
        book.author = updateCrentials['author']
        quan = int(updateCrentials['quantity'])
        if (quan < 0 and abs(quan) <= book.available) or quan > 0:
            book.quantity += quan
            book.available += quan
        else: 
            print ('available quantity is less than the deducted quantity!')
        dbSession.add(book)
        dbSession.commit()
        if book.quantity == 0:
            bookModel.deleteBook(bookID)
        
    @staticmethod
    def deleteBook(bookId):
        dbSession.query(bookModel).filter(bookModel.referenceNumber==bookId).delete()
        dbSession.commit()
        print ('book is deleted!')

    @staticmethod
    def changeQuantity(id, num):
        quan = dbSession.query(bookModel).filter(bookModel.referenceNumber==id).first()
        quan.quantity += num
        dbSession.add(quan)
        dbSession.commit()

    @staticmethod
    def changeIssue(id, num):
        issue = dbSession.query(bookModel).filter(bookModel.referenceNumber==id).first()
        issue.issued += num
        dbSession.add(issue)
        dbSession.commit()

    @staticmethod
    def changeAvailabe(id, num):
        issue = dbSession.query(bookModel).filter(bookModel.referenceNumber==id).first()
        procced = False
        if (num < 0 and abs(num) <= issue.available) or num > 0:
            issue.available += num
            procced = True
        dbSession.add(issue)
        dbSession.commit()
        return procced