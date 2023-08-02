# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

#import mysql.connector



app = Flask(__name__, template_folder='templates')
#app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'signlanguage'

mysql = MySQL(app)
#conn = mysql.connector.connect(host="localhost", user="root", password="root123", database="signlanguage")
#cursor = conn.cursor()
class SignUpForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    EmergencyMobileNo = StringField('Emergency Mobile no.', validators=[DataRequired()])
    EmergencyEmail = StringField('EmergencyEmail', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SIGN UP')

class logInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('LOG IN')

class lobbyForm(FlaskForm):
    submit = SubmitField()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    msg = ''
    #form = SignUpForm()
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'emergencymobileno' in request.form and 'emergencyemail' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        emergencymobileno = request.form['emergencymobileno']
        emergencyemail = request.form['emergencyemail']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE name = % s', (name,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Name must contain only characters and numbers !'
        elif not name or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, %s, %s)', (name, email, emergencymobileno, emergencyemail, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('sign-up.html', msg=msg)

    return redirect(url_for('login'))


    #return render_template('sign-up.html', form=form)
#app.run(host='localhost', port=3306)

@app.route('/log-in', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password,))
        account = cursor.fetchone()
        account
        if account:
            session['loggedin'] = True
            #session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('lobby.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('log-in.html', msg=msg)

@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    form = lobbyForm()
    return render_template('lobby.html', form=form)
if __name__ == "__main__":
    app.run(debug=True)