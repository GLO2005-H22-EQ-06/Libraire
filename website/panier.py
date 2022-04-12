from flask import Blueprint, render_template, request, Response, session
from . import mysql

panier = Blueprint('panier', __name__)


@panier.route('/panier', methods=['GET', 'POST'])
def render_panier():
    """if request.method == 'GET':
        panier_user = ''"""
    return render_template("panier.html")


@panier.route('/checkout', methods=['GET', 'POST'])
def render_checkout():
    if request.method == 'POST':
        return render_template("checkout.html")


@panier.route('/addToCart', methods=['GET', 'POST'])
def addProductToCart():
    if request.method == 'POST':
        userId = str(request.args.get('userId'))
        isbn = request.args['isbn']
        quantity = int(request.args['quantity'])

        cur = mysql.connection.cursor()
        cur.callproc('add_panier', (userId, isbn, quantity))
        mysql.connection.commit()

        return Response(status=201, mimetype='application/json')
