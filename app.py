from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import uuid
import re


app = Flask(__name__)

app.secret_key = "web app"

app.config["MYSQL_HOST"] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'EnvyUS123'
app.config['MYSQL_DATABASE'] = 'glo_2005_labs'

mysql = MySQL(app)

@app.route("/",  methods=['GET', 'POST'])
def index():
    return render_template("home.html")

@app.route("/login",  methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('USE glo_2005_labs')
        cursor.execute('SELECT * FROM compte WHERE identifiant = %s AND motDePasse = %s', (username, password))
        compte = cursor.fetchone()

        if compte is not None:
            session['loggedin'] = True
            session['username'] = username
            return render_template("home.html")
        else:
            msg = "Account doesn't exist !"
    return render_template("login.html", msg=msg)

@app.route("/register",  methods=['GET', 'POST'])
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
        cursor.execute('USE glo_2005_labs')
        cursor.execute('SELECT * FROM clients Cl, compte Co WHERE Co.identifiant = %s OR Cl.email = %s ', (username, email))
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
            cursor.execute('INSERT INTO compte VALUES (% s, % s)', (username, password))
            mysql.connection.commit()
            cursor.execute('INSERT INTO clients VALUES (% s, % s, % s, % s, % s, % s)', (id, name, second_name,
                                                                                              email, address, phone))
            mysql.connection.commit()
            cursor.execute('INSERT INTO associer VALUES (% s, % s)', (username, id))
            mysql.connection.commit()
            return render_template("home.html")
    return render_template("submit.html", msg=msg)



if __name__ == "__main__":
    app.run(debug=True)
