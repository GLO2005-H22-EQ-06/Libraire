from math import prod
from flask import Blueprint, render_template, request, Response, session, flash, redirect, url_for

from website.home import render
from . import mysql

panier = Blueprint('panier', __name__)


@panier.route('/panier', methods=['GET', 'POST'])
def render_panier():
    if request.method == 'GET':
        if 'username' in session:
            username = session['username']
            cur = mysql.connection.cursor()

            cur.execute(
                'select id_client from associer where identifiant = %s', [username])
            userid = cur.fetchone()

            cur.execute(
                'select * from livres natural join (select * from panier where PANIER.id_client = %s) as all_prod;',
                [userid])
            all_cart_products = cur.fetchall()

            total = 0
            for product in all_cart_products:
                total += product[9] * product[11] 
            
            tax = round(total * 0.15, 2)
            grandTotal = round(total + tax + 15, 2)

            return render_template("panier.html", loggedin=True, username=username, panier=all_cart_products, total=total, tax=tax, grandTotal=grandTotal)

        flash('You have to connect or to create an account for acceding cart',
              category='error')
        return redirect(url_for('articles.render_articles'))


@panier.route('/checkout', methods=['POST'])
def render_checkout():
    if request.method == 'POST':
        username = session['username']
        cur = mysql.connection.cursor()

        cur.execute(
            'select id_client from associer where identifiant = %s', [username])
        userid = cur.fetchone()

        cur.callproc("transfert_from_cart_to_bill", (userid))
        mysql.connection.commit()

        return redirect(url_for('panier.render_panier'))


@panier.route('/addToCart/<string:isbn>', methods=['POST'])
def addProductToCart(isbn):
    if request.method == 'POST':
        if 'username' in session:
            cur = mysql.connection.cursor()
            wanted_quantity = int(request.form['quantity'])
            username = session['username']
            cur.execute(
                'SELECT id_client FROM associer WHERE identifiant = %s', [username])
            userId = cur.fetchone()
            cur.execute(
                'select quantity from stock where isbn=%s', [isbn])
            given_quantity = cur.fetchone()
            print(given_quantity)
            if (wanted_quantity > given_quantity[0]):
                flash("Quantité insuffisante en stock", category="error")
            elif (wanted_quantity < 0):
                flash("La quantité doit être positive", category="error")
            else:
                cur.callproc('add_panier', (userId, isbn, wanted_quantity))
                mysql.connection.commit()

            return redirect(url_for('articles.render_articles'))
        flash("You have to be connected to add an article to your cart",
              category='error')
        return redirect(url_for('articles.render_articles'))


@panier.route('/remove/<string:isbn>', methods=['POST'])
def removeProductFromCart(isbn):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = session['username']
        cur.execute(
            'select id_client from associer where identifiant = %s', [username])
        userid = cur.fetchone()
        print(userid)
        cur.execute('select quantity from panier where id_client = %s and isbn = %s', [
                    userid, isbn])
        quantity_in_cart = cur.fetchone()
        cur.callproc('add_panier', (userid, isbn, -quantity_in_cart[0]))
        mysql.connection.commit()

        cur.execute(
            'delete from panier where id_client = %s and isbn = %s', [userid, isbn])
        mysql.connection.commit()
        flash('Item successfully removed')
        return redirect(url_for('panier.render_panier'))


@panier.route('/update/<string:isbn>', methods=['POST'])
def update_quantity(isbn):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = session['username']
        cur.execute(
            'select id_client from associer where identifiant = %s', [username])
        userid = cur.fetchone()

        cur.execute('select quantity from panier where id_client = %s and isbn = %s', [
                    userid, isbn])
        given_quantity = cur.fetchone()[0]
        new_quantity = int(request.form['quantity'])
        updated_quantity = new_quantity - given_quantity
        try:
            cur.callproc('add_panier', (userid, isbn, updated_quantity))
            mysql.connection.commit()
        except:
            flash('Quantité insuffisante en stock', category='error')
            return redirect(url_for('panier.render_panier'))

        flash('Quantity updated successfully')
        return redirect(url_for('panier.render_panier'))
