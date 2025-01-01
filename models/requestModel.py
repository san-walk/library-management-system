from sqlalchemy import Column, String, Integer, Boolean, create_engine, UniqueConstraint
from connection import engine, Base
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(engine)
dbSession = Session()


'''
Date: 31st Dec 2024
Purpose: this class represents the request raised by the user approve by the admin
'''
class reqModel(Base):
    __tablename__ = "requests"

    snum = Column(Integer, primary_key=True, autoincrement=True)
    bookName = Column(String)
    issuedBy = Column(String)
    bookId = Column(String)
    action = Column(Boolean, default=None)
    approval = Column(Boolean, default=None)
    returned = Column(Boolean, default=None)


    @staticmethod
    def getAllRequest():
        reqData = dbSession.query(reqModel).filter(reqModel.action==None).all()
        if reqData:
            return reqData
        else: 
            return None

    @staticmethod
    def addRequest(newReq):
        print ("adding a new request for the book issue! from the reqModel.py")
        req = reqModel(
            bookName = newReq['bookName'],
            issuedBy = newReq['issuedBy'],
            bookId = newReq['referenceNumber']
        )
        print ("data verified!")
        dbSession.add(req)
        print ("data added in the session!")
        dbSession.commit()
        print ("data successfully commited!")

    @staticmethod
    def getUserRequest(user):
        print ('going to retreve user requests')
        reqs = dbSession.query(reqModel).filter(reqModel.issuedBy==user).all()
        if reqs:
            print ('got all requests!')
            return reqs
        else:
            print ("user didn't have any requests yet")

    @staticmethod
    def deleteReqByBookID(_bookID):
        dbSession.query(reqModel).filter(reqModel.bookId==_bookID).delete()
        dbSession.commit()
        
    @staticmethod
    def deleteReqByUser(_user):
        dbSession.query(reqModel).filter(reqModel.issuedBy==_user).delete()
        dbSession.commit()

    
    @staticmethod
    def getReturnableReq(user):
        print ('going to get requests which is approved and may be i am going to return')
        reqs = dbSession.query(reqModel).filter(reqModel.issuedBy==user, reqModel.approval==True, reqModel.returned!=True).all()
        if reqs:
            print ('got all returnable requests!')
            return reqs
        else:
            print ("user didn't have any returnable requests.")

    @staticmethod
    def changeActionNApproval(_snum, _action, _approval):
        action = dbSession.query(reqModel).filter(reqModel.snum==_snum).first()
        action.action = _action
        action.approval = _approval
        action.returned = False
        dbSession.add(action)
        dbSession.commit()

    @staticmethod
    def changeReturn(user, _id):
        action = dbSession.query(reqModel).filter(reqModel.issuedBy==user, reqModel.bookId==_id).first()
        action.returned = True
        dbSession.add(action)
        dbSession.commit()