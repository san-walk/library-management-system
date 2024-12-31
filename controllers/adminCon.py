from flask import redirect, render_template, request, session
from models.userModel import userModel
from models.bookModel import bookModel
from models.requestModel import reqModel

'''
Date: 26th Dec 2024
Purpose: user controller class renders user page
'''
class adminController():
    # to get all
    def get():
        userData = userModel.getAllUsers()
        booksData = bookModel.getAllBooks()
        allReqs = reqModel.getAllRequest()
        return render_template('adminsPage.html', users=userData, books=booksData, requests=allReqs)
    
    # to get update page
    def getUpdate(user):
        return render_template('updatePage.html', user=user)
    
    # to submit the data for update
    def postUpdate(user):
        formData = request.form
        print (formData)
        usr = userModel.update(user, formData)
        return redirect('/admin')
    
    # delete user
    def deleteUser(user):
        delet = userModel.delete(user)
        print (delet)
        return redirect('/admin')


    # approve request function
    def approveReq():
        reqData = request.form
        # update user details 
        userModel.changeIssue(reqData['issuedBy'], 1)
        userModel.changePending(reqData['issuedBy'], -1)
        # update book details
        bookModel.changeIssue(reqData['bookId'], 1)
        bookModel.changeAvailabe(reqData['bookId'], -1)
        # update request table
        reqModel.changeActionNApproval(reqData['snum'], True, True)
        return redirect('/admin')
    
    # reject request function
    def rejectReq():
        reqData = request.form
        # update user details
        userModel.changePending(reqData['issuedBy'], -1)
        # update request table
        reqModel.changeActionNApproval(reqData['snum'], True, False)
        return redirect('/admin')