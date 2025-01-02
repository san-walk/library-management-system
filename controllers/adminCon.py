from flask import redirect, render_template, request, session, url_for
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
        if 'username' in session and session['admin'] == True:
            userData = userModel.getAllUsers()
            booksData = bookModel.getAllBooks()
            allReqs = reqModel.getAllRequest()
            if 'error' in session:
                error = session['error']
                session.pop('error', None)
                return render_template('adminsPage.html', users=userData, books=booksData, requests=allReqs, err=error)
            return render_template('adminsPage.html', users=userData, books=booksData, requests=allReqs)
        return 'You are not logedin as admin!<br><a href="http://localhost:5000/login">Click here to LOGIN</a>'
    
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
        # checks for the books user issued 
        allReqs = reqModel.getAllReqByUser(user)
        if allReqs:
            for req in allReqs:
                print (req.issuedBy, ' book id is -----> ', req.bookId, ' and book name is ------> ', req.bookName)
                _id = req.bookId
                bookModel.changeIssue(_id, -1)
                bookModel.changeAvailabe(_id, 1)
        # requests regarding this user also deletes
        reqModel.deleteReqByUser(user)
        userModel.delete(user)
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
            session['error'] = "Can't approve request, the book is not available!"
            return redirect(url_for('.admin'))
        return redirect('/admin')
    
    # reject request function
    def rejectReq():
        reqData = request.form
        # update user details
        userModel.changePending(reqData['issuedBy'], -1)
        # update request table
        reqModel.changeActionNApproval(reqData['snum'], True, False)
        return redirect('/admin')