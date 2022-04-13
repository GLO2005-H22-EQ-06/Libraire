from flask import Blueprint, render_template, make_response, jsonify, request, session
from . import mysql

articles = Blueprint('articles', __name__)


all_products = []
limit = 20


@articles.route('/articles', methods=['GET', 'POST'])
def render_articles():
    cur = mysql.connection.cursor()
    """cur.execute(
        "SELECT * FROM livres OFFSET %s ROWS FETCH NEXT %s ROWS ONLY", (offset, item_per_page))"""
    cur.execute("SELECT * FROM livres LIMIT 100")
    items = cur.fetchall()
    if session['loggedin'] == True:
        userId = session['username']
        return render_template("articles.html", userId=userId, items=items)
    return render_template("articles.html", items=items)
