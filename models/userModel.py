from sqlalchemy import Column, String, Integer, Boolean, create_engine, UniqueConstraint
from connection import engine, Base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)
dbSession = Session()


'''
Date: 24th Dec 2024
Purpose: this is the class for the user model from which a user is defined.
'''
class userModel(Base):
    __tablename__ = "users"

    snum = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(15))
    firstName = Column(String(20))
    lastName = Column(String(20))
    email = Column(String(50))
    phoneNumber = Column(Integer)
    password = Column(String)
    isAdmin = Column(Boolean, default=False)
    __table_args__ = (UniqueConstraint('username', name='_username_uc'),)


    # TODO : MAKE MODELS MORE INTERACTIVE
    # done
    # used to get all users data
    @staticmethod
    def getAllUsers():
        userData = dbSession.query(userModel).all()
        return userData
    
    # used to get a username
    @staticmethod
    def getUsername(username):
        isUser = dbSession.query(userModel).filter(userModel.username==username).first()
        if isUser:
            print ('username found!     verified from the userModel.py ')
        else:
            print ('username not found!')
        return isUser
    
    # retrevies password from the username
    @staticmethod
    def getPassword(username):
        isPassword = dbSession.query(userModel.password).filter(userModel.username==username).first()
        if isPassword:
            print (isPassword)
        else:
            print ('password not found')
        return isPassword
        
    # checks if admin with username
    @staticmethod
    def getAdmin(username):
        isAdmin = dbSession.query(userModel.isAdmin).filter(userModel.username==username).first()
        print (isAdmin[0])
        if isAdmin[0]:
            return True
        else:
            return False
    
    # method to update user delails
    @staticmethod
    def update(username, updateCrentials):
        user = dbSession.query(userModel).filter(userModel.username==username).first()
        if not user:
            print ('user not found!')
            return None
        print (user)
        user.firstName = updateCrentials['firstName']
        user.lastName = updateCrentials['lastName']
        user.email = updateCrentials['email']
        user.phoneNumber = updateCrentials['phoneNumber']
        dbSession.add(user)
        dbSession.commit()
        return user
    
    # delete users with username
    @staticmethod
    def delete(username):
        dele = dbSession.query(userModel).filter(userModel.username == username).delete()
        dbSession.commit()
        return dele