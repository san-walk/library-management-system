from flask import redirect, render_template, request, session
from models.userModel import userModel

'''
Date: 26th Dec 2024
Purpose: user controller class renders user page
'''
class adminController():
    def get():
        userData = userModel.getAllUsers()
        return render_template('adminsPage.html', users = userData)
    
    def getUpdate(user):
        return render_template('updatePage.html', username=user)
    
    def postUpdate(user):
        formData = request.form
        print (formData)
        usr = userModel.update(user, formData)
        return redirect('/admin')
    
    def deleteUser(user):
        delet = userModel.delete(user)
        print (delet)
        return redirect('/admin')
