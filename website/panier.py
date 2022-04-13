from flask import Blueprint, render_template, request, Response, session, flash, redirect, url_for

from website.home import render
from . import mysql

panier = Blueprint('panier', __name__)


@panier.route('/panier', methods=['GET', 'POST'])
def render_panier():
    if request.method == 'GET':
        if 'username' in session:
            username = session['username']
            return render_template("panier.html", loggedin=True, username=username)
        flash('You have to connect or to create an account for acceding cart',
              category='error')
        return render_template("home.html", loggedin=False)


@panier.route('/checkout', methods=['GET', 'POST'])
def render_checkout():
    if request.method == 'POST':
        return render_template("checkout.html")


@panier.route('/addToCart/<string:isbn>', methods=['POST'])
def addProductToCart(isbn):
    if request.method == 'POST':
        if session['loggedin']:
            cur = mysql.connection.cursor()
            wanted_quantity = int(request.form['quantity'])
            username = session['username']
            cur.execute(
                'SELECT id_client FROM associer WHERE identifiant = %s', [username])
            userId = cur.fetchone()

            given_quantity = cur.execute(
                'select quantity from stock where isbn=%s', [isbn])
            if (wanted_quantity > given_quantity):
                flash("Quantité insuffisante en stock", category="error")
            elif(wanted_quantity < 0):
                flash("La quantité doit être positive", category="error")
            else:
                cur.callproc('add_panier', (userId, isbn, wanted_quantity))
                mysql.connection.commit()

            return redirect(url_for('articles.render_articles'))
