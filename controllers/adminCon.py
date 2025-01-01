from flask import redirect, render_template, request, session
from models.userModel import userModel
from models.bookModel import bookModel
from models.requestModel import reqModel
from helpers import validate

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
        # data is going to validate
        error = validate.validateUpdateData(formData)
        if error:
            return render_template('updatePage.html', err=error[0])
        userModel.update(user, formData)
        return redirect('/admin')
    
    # delete user
    def deleteUser(user):
        userModel.delete(user)
        # requests regarding this user also deletes
        reqModel.deleteReqByUser(user)
        return redirect('/admin')


    # approve request function
    def approveReq():
        reqData = request.form
        # update book details
        isAvailable = bookModel.changeAvailabe(reqData['bookId'], -1)
        if isAvailable:
            bookModel.changeIssue(reqData['bookId'], 1)
            # update user details 
            userModel.changeIssue(reqData['issuedBy'], 1)
            userModel.changePending(reqData['issuedBy'], -1)
            # update request table
            reqModel.changeActionNApproval(reqData['snum'], True, True)
        else:
            error = "Can't approve request, the book is not available!"
            userData = userModel.getAllUsers()
            booksData = bookModel.getAllBooks()
            allReqs = reqModel.getAllRequest()
            return render_template('adminsPage.html', users=userData, books=booksData, requests=allReqs, err=error)
        return redirect('/admin')
    
    # reject request function
    def rejectReq():
        reqData = request.form
        # update user details
        userModel.changePending(reqData['issuedBy'], -1)
        # update request table
        reqModel.changeActionNApproval(reqData['snum'], True, False)
        return redirect('/admin')