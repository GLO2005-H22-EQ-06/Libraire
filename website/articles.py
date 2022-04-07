from flask import Blueprint, render_template
from . import mysql

articles = Blueprint('articles', __name__)


@articles.route('/articles', methods=['GET', 'POST'])
def render_articles():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM livres""")
    all_products = cur.fetchall()
    return render_template("articles.html", books=all_products)
