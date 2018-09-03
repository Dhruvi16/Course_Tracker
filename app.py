from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'some secret key'

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(80), unique=True, nullable=False)
    c_duration = db.Column(db.Integer, unique=False, nullable=False)
    curr_week = db.Column(db.Integer, unique=False, nullable=False)
    desc = db.Column(db.String(100), unique=False, nullable=False)

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=["GET", "POST"])
def results():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        c_name = request.form['c_name']
        c_duration = request.form['c_duration']     
        curr_week = request.form['curr_week']     
        desc = request.form['desc'] 
        return render_template('dashboard.html', c_name=c_name, c_duration=c_duration, curr_week=curr_week, desc=desc)    


if __name__ == "__main__":
    app.run(debug=True)
    