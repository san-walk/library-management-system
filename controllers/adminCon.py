from flask import redirect, render_template, request, session
from models.userModel import userModel

'''
Date: 26th Dec 2024
Purpose: user controller class renders user page
'''
class adminController():
    # to get all the users
    def get():
        userData = userModel.getAllUsers()
        return render_template('adminsPage.html', users = userData)
    
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
