from flask import Blueprint, render_template, flash
from flask import render_template, request, redirect, url_for, session
import bcrypt
import uuid
import re
from website import mysql
from . import salt

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        pwd = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(pwd, salt)

        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM compte WHERE identifiant = %s AND motDePasse = %s', (username, hashed_password))
        compte = cursor.fetchone()

        if compte is not None:
            session['loggedin'] = True
            session['username'] = username
            return render_template("home.html", loggedin=True)
        else:
            msg = "Account doesn't exist !"
            flash('Incorrect password or username', category='error')
    return render_template("login.html", msg=msg, loggedin=False)


@auth.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        second_name = request.form['second_name']
        username = request.form['username']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        pwd = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(pwd, salt)

        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM clients Cl, compte Co WHERE Co.identifiant = %s OR Cl.email = %s ', (username, email))
        username_fetch = cursor.fetchone()

        cursor.execute(
            'select telephone from clients')
        phone_numbers = cursor.fetchall()

        found = False
        for i in phone_numbers:
            if i[0] == str(phone):
                found = True
                break

        if username_fetch is not None:
            msg = "email or username already used"
        elif not re.match(r'^[0-9]{10}$', phone):
            msg = "Invalid phone format.Should be 10 digits"
        elif found:
            msg = "Phone number already used"
        elif password != confirm_password:
            msg = "Password have to match"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid e-mail format"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Username must only contain letters and numbers"
        else:
            id = uuid.uuid1()
            cursor.execute('INSERT INTO clients VALUES (% s, % s, % s, % s, % s, % s)', (id, name, second_name,
                                                                                         email, address, phone))
            mysql.connection.commit()
            cursor.execute('INSERT INTO compte VALUES (% s, % s)',
                           (username, hashed_password))
            mysql.connection.commit()
            cursor.execute(
                'INSERT INTO associer VALUES (% s, % s)', (username, id))
            mysql.connection.commit()

            session['loggedin'] = True
            session['username'] = username
            return render_template("home.html", loggedin=True)
    return render_template("submit.html", msg=msg, loggedin=False)


@auth.route('/logout')
def loggin_out():
    session.pop('username', None)
    session.pop('loggedin', False)
    return render_template('home.html', loggedin=False)
