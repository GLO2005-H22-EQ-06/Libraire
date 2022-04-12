from flask import Blueprint, render_template, make_response, jsonify, request
from . import mysql

articles = Blueprint('articles', __name__)


all_products = []
limit = 20


@articles.route('/articles', methods=['GET', 'POST'])
def render_articles():
    return render_template("articles.html")


@articles.route('/loads/books')
def loadsBooks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM livres")
    all_products = cur.fetchall()
    maxi = len(all_products)
    print(maxi)
    if request.args:
        counter = int(request.args.get('c'))

        if counter == 0:
            print('fetching data for first time')
            res = make_response(jsonify(all_products[0: limit]), 200)

        elif counter == maxi:
            res = make_response(jsonify({}), 200)

        else:
            res = make_response(
                jsonify(all_products[counter: counter + limit]))

        return res
