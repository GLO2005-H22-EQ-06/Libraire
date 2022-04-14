from flask import Blueprint, render_template, request, session, redirect, url_for, flash
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
    if 'username' in session:
        return render_template("articles.html", items=items, loggedin=True)
    return render_template("articles.html", items=items, loggedin=False)


@articles.route('/articles/filters')
def filter():

    if request.method == 'GET':
        filtre = request.args.get('filter')
        flash(str(filtre))
        cur = mysql.connection.cursor()

        if filtre == 'None':
            return redirect(url_for('articles.render_articles'))

        if filtre == 'Price asc':
            cur.execute('select * from livres order by prix asc')
            items = cur.fetchall()
            return render_template('articles.html', items=items)

        if filtre == 'Price dsc':
            cur.execute('select * from livres order by prix dsc')
            items = cur.fetchall()
            return render_template('articles.html', items=items)

        if filtre == 'Rating asc':
            cur.execute('select * from livres order by note asc limit 200')
            items = cur.fetchall()
            return render_template('articles.html', items=items)

        if filtre == 'Rating dsc':
            cur.execute('select * from livres order by note dsc limit 200')
            items = cur.fetchall()
            return render_template('articles.html', items=items)

        if filtre == 'Nombre de page asc':
            cur.execute(
                'select * from livres order by nbrepages asc limit 200')
            items = cur.fetchall()
            return render_template('articles.html', items=items)

        if filtre == 'Nombre de page asc':
            cur.execute(
                'select * from livres order by nbrepages dsc limit 200')
            items = cur.fetchall()
            return render_template('articles.html', items=items)

    return redirect(url_for('articles.render_articles'))
