from flask import Blueprint, render_template, request, Response
from numpy import product
from . import mysql

panier = Blueprint('panier', __name__)


@panier.route('/panier', methods=['GET', 'POST'])
def render_panier():
    if request.method == 'GET':
        panier_user = ''
        return render_template("panier.html", panier=panier_user)


@panier.route('/checkout', methods=['GET', 'POST'])
def render_checkout():
    if request.method == 'POST':
        return render_template("checkout.html")


@panier.route('/addToCart', methods=['GET', 'POST'])
def addProductToCart():
    if request.method == 'POST':
        userId = str(request.headers.get('userId'))
        isbn = request.headers['isbn']
        quantity = int(request.headers['quantity'])

        cur = mysql.connection.cursor()
        # cur.execute('CALL add_panier(% s, % s, % s)',
        #            (userId, isbn, quantity))

        cur.callproc('add_panier', (userId, isbn, quantity))
        mysql.connection.commit()

        return Response(status=201, mimetype='application/json')
