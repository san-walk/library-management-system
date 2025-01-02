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


    # get all the requests with this function where action is not taken to approve/reject
    @staticmethod
    def getAllRequest():
        reqData = dbSession.query(reqModel).filter(reqModel.action==None).all()
        if reqData:
            return reqData
        else: 
            return None

    # add a new req raised by the user to get book from the library
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

    # get the requests for the particular user
    @staticmethod
    def getUserRequest(user):
        print ('going to retreve user requests')
        reqs = dbSession.query(reqModel).filter(reqModel.issuedBy==user).all()
        if reqs:
            print ('got all requests!')
            return reqs
        else:
            print ("user didn't have any requests yet")

    # delete the request by bookID
    @staticmethod
    def deleteReqByBookID(_bookID):
        dbSession.query(reqModel).filter(reqModel.bookId==_bookID).delete()
        dbSession.commit()
        
    # delete the request by userID
    @staticmethod
    def deleteReqByUser(_user):
        dbSession.query(reqModel).filter(reqModel.issuedBy==_user).delete()
        dbSession.commit()

    # get all the requests of the approved books which can be return
    @staticmethod
    def getReturnableReq(user):
        print ('going to get requests which is approved and may be i am going to return')
        reqs = dbSession.query(reqModel).filter(reqModel.issuedBy==user, reqModel.approval==True, reqModel.returned!=True).all()
        if reqs:
            print ('got all returnable requests!')
            return reqs
        else:
            print ("user didn't have any returnable requests.")

    # function used to get the issued books by a particular user
    @staticmethod
    def checkIssue(_id, _user):
        isPending = dbSession.query(reqModel).filter(reqModel.bookId==_id, reqModel.issuedBy==_user, reqModel.action==None, reqModel.approval==None, reqModel.returned==None).first()
        isReturned = dbSession.query(reqModel).filter(reqModel.bookId==_id, reqModel.issuedBy==_user, reqModel.action==True, reqModel.approval==True, reqModel.returned==False).first()
        message = ''
        if isPending:
            message = 'You have a pending request!'
        elif isReturned:
            message = 'Book was Issued return it first!'
        else:
            message = 'Issue requested! wait for admin to confirm.'
            return ( message, True)
        return ( message, False )

    # function used to change the action on the requests
    @staticmethod
    def changeActionNApproval(_snum, _action, _approval):
        action = dbSession.query(reqModel).filter(reqModel.snum==_snum).first()
        action.action = _action
        action.approval = _approval
        action.returned = False
        dbSession.add(action)
        dbSession.commit()

    # function is used to return the book
    @staticmethod
    def changeReturn(user, _id):
        actions = dbSession.query(reqModel).filter(reqModel.issuedBy==user, reqModel.bookId==_id).all()
        for action in actions:
            if not action.returned:
                action.returned = True
                dbSession.add(action)
        dbSession.commit()

    # function is used to get all requests by a user
    @staticmethod
    def getAllReqByUser(_user):
        allReq = dbSession.query(reqModel).filter(reqModel.issuedBy==_user, reqModel.approval==True, reqModel.returned==False).all()
        if allReq:
            print ('all requests ------> ', allReq)
            print ('lenght of the request is ------> ', len(allReq))
            return allReq
        return None
    
    # function is used to get all requests by a 
    @staticmethod
    def getAllReqByBook(_id):
        allReq = dbSession.query(reqModel).filter(reqModel.bookId==_id, reqModel.approval==True, reqModel.returned==False).all()
        if allReq:
            print ('all requests -------> ', allReq)
            print ('length of the request is -------> ', len(allReq))
            return allReq
        return None 