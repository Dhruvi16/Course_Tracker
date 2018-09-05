from flask import Flask, flash, redirect, render_template, request, session, url_for
# from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'some secret key'





# Decorators

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get("user_id") is None:
            return render_template("login.html")
        return f(*args, **kwargs)
    return wrap

# db_path = os.path.join(os.path.dirname(__file__), 'app.db')
# db_uri = 'sqlite:///{}'.format(db_path)
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     c_name = db.Column(db.String(80), unique=True, nullable=False)
#     c_duration = db.Column(db.Integer, unique=False, nullable=False)
#     curr_week = db.Column(db.Integer, unique=False, nullable=False)
#     desc = db.Column(db.String(100), unique=False, nullable=False)

# db.create_all()

# db = sqlite3.connect('app.db', check_same_thread=False)

@app.route('/')
def index():
    return render_template('index.html')

@login_required
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        c_name = request.form['c_name']
        c_duration = request.form['c_duration']     
        curr_week = request.form['curr_week']     
        desc = request.form['desc'] 
        return render_template('dashboard.html', c_name=c_name, c_duration=c_duration, curr_week=curr_week, desc=desc)    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # To-do: Add validation

        username=request.form.get("username")
        # query database for username
        with sqlite3.connect("app.db") as db:
            rows = db.execute(f"SELECT * FROM login WHERE username = '{username}'")
        
        check = []
        for row in rows:
            check = row

        password = request.form.get("password")

        # ensure username exists and password is correct
        if not len(check) == 2:
            flash('Invalid creds')
            return render_template("login.html")
        elif password != check[1]:
            flash('Invalid creds')
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = username
        flash("You're logged in!")

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":
        # To-do: Add validation for username and password 
        # To-do: Add password conf field
        #If an INSERT, then execute returns the value of the newly inserted row’s primary key.

        password = request.form.get('password')
        username = request.form.get("username")
        with sqlite3.connect("app.db") as db:
            result = db.execute(f"INSERT INTO login (username, password) VALUES ('{username}', '{password}')")

        print('done')
        if not result:
            flash('Username already exists!')
            return render_template("register.html")

        # remember which user has logged in
        session["user_id"] = username
        flash("You've been registered!")
        # redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
    