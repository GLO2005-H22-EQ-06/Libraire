from flask import Blueprint, render_template
from . import mysql

articles = Blueprint('articles', __name__)


@articles.route('/articles', methods=['GET', 'POST'])
def render_articles():
    return render_template("articles.html")
