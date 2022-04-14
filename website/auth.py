from distutils.log import error
import logging
from flask import Blueprint, render_template, flash
from flask import render_template, request, redirect, url_for, session
import uuid
import re
from website import mysql

auth = Blueprint('auth', __name__)


@auth.route('/login',  methods=['GET', 'POST'], endpoint='login')
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM compte WHERE identifiant = %s AND motDePasse = %s', (username, password))
        compte = cursor.fetchone()

        if compte is not None:
            session['loggedin'] = True
            session['username'] = username
            return render_template("home.html", loggedin=True)
        else:
            msg = "Account doesn't exist !"
            flash('Incorrect password or username', category='error')
    return render_template("login.html", msg=msg)


@auth.route('/register',  methods=['GET', 'POST'], endpoint='register')
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

        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM clients Cl, compte Co WHERE Co.identifiant = %s OR Cl.email = %s ', (username, email))
        username_fetch = cursor.fetchone()
        if username_fetch is not None:
            msg = "email or username already in use"
        elif password != confirm_password:
            msg = "Password have to much"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid e-mail format"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Username must only contain letters and numbers"
        else:
            id = uuid.uuid1()
            cursor.execute('INSERT INTO compte VALUES (% s, % s)',
                           (username, password))
            mysql.connection.commit()
            cursor.execute('INSERT INTO clients VALUES (% s, % s, % s, % s, % s, % s)', (id, name, second_name,
                                                                                         email, address, phone))
            mysql.connection.commit()
            cursor.execute(
                'INSERT INTO associer VALUES (% s, % s)', (username, id))
            mysql.connection.commit()

            session['loggedin'] = True
            session['username'] = username
            return render_template("home.html", loggedin=True)
    return render_template("submit.html", msg=msg)


@auth.route('/logout')
def loggin_out():
    session.pop('username', None)
    session.pop('loggedin', False)
    return render_template('home.html', loggedin=False)
