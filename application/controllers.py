from flask import request, render_template, redirect, url_for
from flask import current_app as app
from .models import *

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        this_user = User.query.filter_by(username = username).first()
        if this_user:
            if this_user.password == password:
                if this_user.role == 'manager':
                    return redirect('/manager')
                return redirect(f'/user/{this_user.id}')
            else:
                return "Incorrect Password"
        else:
            return "User doesn't exists!!"
    return render_template('login.html')
        
@app.route('/manager')
def manager_dash():
    return "manager"
    