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

@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        c_name = request.form.get('c_name')
        c_duration = request.form.get('c_duration')    
        desc = request.form.get('desc')
        curr_week = 0
        username = session["user_id"]
        print('here')
        with sqlite3.connect("app.db") as db:
            db.execute(f"INSERT INTO user (user,c_name,c_duration,curr_week,desc) VALUES ('{username}','{c_name}',{c_duration},{curr_week},'{desc}')")
        print('added')
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    username = session["user_id"]
    with sqlite3.connect("app.db") as db:
        result = db.execute(f"SELECT * FROM user where user = '{username}'")

    data = []
    for row in result:
        data.append(row)
    return render_template('dashboard.html', data=data)

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
        # session["user_id"] = username
        flash("You've been registered!")
        # redirect user to home page
        return redirect(url_for("login"))

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    flash("Logged out successfully.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
    