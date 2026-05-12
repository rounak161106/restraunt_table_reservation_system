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

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_name = User.query.filter_by(username = username).first()
        user_email = User.query.filter_by(email = email).first()
        if user_name or user_email:
            return "User already exists"
        this_user = User(username = username, password = password, email = email)
        db.session.add(this_user)
        db.session.commit()
        return redirect("/login") 
    return render_template('register.html')
        
@app.route('/manager')
def manager_dash():
    this_user = User.query.filter_by(role = 'manager').first()
    all_tables = Table.query.all()
    return render_template('manager_dash.html',name = this_user.username, all_tables = all_tables)
    
@app.route('/user/<int:id>')
def user_dash(id):
    this_user = User.query.get(id)
    return render_template("user_dash.html", this_user = this_user)