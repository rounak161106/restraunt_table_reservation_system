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
    return render_template('manager_dash.html',this_user = this_user, all_tables = all_tables)
    
@app.route('/user/<int:id>')
def user_dash(id):
    this_user = User.query.get(id)
    all_tables = Table.query.filter_by(status = 'available').all()
    return render_template("user_dash.html", this_user = this_user, tables = all_tables)

@app.route('/create_table', methods = ["GET", "POST"])
def create_table():
    if request.method == "POST":
        table_number = request.form.get("table_number")
        this_table =  Table.query.filter_by(table_number = table_number).first()
        if this_table:
            return "Table no. already exists, try different!!"
        capacity = request.form.get("capacity")
        location = request.form.get("location")
        new_table = Table(table_number = table_number, capacity = capacity, location = location)
        db.session.add(new_table)
        db.session.commit()
        return redirect('/manager')
    return render_template('create_table.html')

@app.route('/update_table/<int:id>', methods = ["GET", "POST"])
def update_table(id):
    this_table = Table.query.get(id)
    if request.method == "POST":
        table_number = request.form.get("table_number")
        capacity = request.form.get("capacity")
        location = request.form.get("location")
        status = request.form.get("status")
        existing = Table.query.filter_by(table_number = table_number).first()
        if existing and existing.table_number != this_table.table_number:
            return "Table number already exists, try something else"
        this_table.table_number = table_number
        this_table.capacity = capacity
        this_table.location = location
        this_table.status = status
        db.session.commit()
        return redirect('/manager')
    return render_template("update_table.html", table = this_table)

@app.route('/delete_table/<int:id>')
def delete_table(id):
    this_table = Table.query.get(id)
    db.session.delete(this_table)
    db.session.commit()
    return redirect('/manager')

@app.route('/reserve/<int:table_id>/<int:user_id>')
def reserve_table(table_id,user_id):
    this_table = Table.query.get(table_id)
    this_user = Table.query.get(user_id)

@app.route('/manager/requests')
def mgr_request():
    mgr = User.query.filter_by(role = 'Manager').first()
    reservations = Reservation.query.filter_by(status = "pending").all()
    return render_template("mngr_req.html", user = mgr, reservations = reservations)

@app.route('/user/requests/<int:id')
def mgr_request(id):
    this_user = User.query.get(id)
    reservations = Reservation.query.filter_by(id = id).all()
    return render_template("mngr_req.html", user = this_user, reservations = reservations)
