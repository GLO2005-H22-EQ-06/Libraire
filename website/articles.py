from pydoc import pager
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from . import mysql
from math import ceil

articles = Blueprint('articles', __name__)


all_products = []
limit = 20


@articles.route('/articles', defaults={'page': 1})
@articles.route('/articles/page/<int:page>')
def render_articles(page):
    limit = 20
    page_limit = 10
    offset = page*limit - limit

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM livres")
    total_row = cur.rowcount
    total_page = ceil(total_row / limit)

    next = page + 1
    prev = page - 1
    page_start = page
    page_end = min(page_start + page_limit, total_page)

    cur.execute(
        "select * from livres order by ISBN limit %s offset %s", (limit, offset))
    items = cur.fetchall()

    loggedIn = 'username' in session
    return render_template("articles.html", items=items, loggedin=loggedIn, total_page=total_page, page_start=page_start, page_end =page_end, next=next, prev=prev, searchInput="Search by title", current_page=page)

@articles.route('/articles/details/isbn=<string:isbn>')
def viewBook(isbn) :
    return render_template('livre.html', all_evaluations=all_evaluations, loggedin=True)


@articles.route('/articles/filters/byTitle/<int:page>', methods=['GET'])
def searchByTitle(page) :
    limit = 20
    page_limit = 10
    offset = page*limit - limit

    searchEntered = request.args.get('search')
    cur = mysql.connection.cursor()
    cur.execute('select * from livres where titre like  %s', ['%' + searchEntered + '%'])
    items = cur.fetchall()
    total_row = cur.rowcount
    total_page = ceil(total_row / limit)  

    next = page + 1 
    prev = page - 1
    page_start = page
    page_end = min(page_start + page_limit, total_page)

    cur.execute('select * from livres where titre like %s limit %s offset %s', ('%' + searchEntered + '%', limit, offset))
    items = cur.fetchall()

    loggedIn = 'username' in session
    return render_template("articles.html", items=items, loggedin=loggedIn, page_start=page_start, page_end=page_end, 
                                        total_page=total_page, next=next, prev=prev, searchInput=searchEntered, current_page=page)

@articles.route('/articles/filters')
def filter():
    if request.method == 'GET':
        filtre = request.args.get('filter')
        flash(str(filtre))
        cur = mysql.connection.cursor()

        if filtre == 'None':
            return redirect(url_for('articles.render_articles'))

        if filtre == 'Price asc':
            cur.execute('select * from livres order by prix asc limit 50')
            items = cur.fetchall()
            return render_template('articles.html', items=items, page=1, next=0, prev=2, searchInput="Search by title")

        if filtre == 'Price dsc':
            cur.execute('select * from livres order by prix desc limit 50')
            items = cur.fetchall()
            return render_template('articles.html', items=items, page=1, next=0, prev=2, searchInput="Search by title")

        if filtre == 'Rating asc':
            cur.execute('select * from livres order by note asc limit 50')
            items = cur.fetchall()
            return render_template('articles.html', items=items, page=1, next=0, prev=2, searchInput="Search by title")

        if filtre == 'Rating dsc':
            cur.execute('select * from livres order by note desc limit 50')
            items = cur.fetchall()
            return render_template('articles.html', items=items, page=1, next=0, prev=2, searchInput="Search by title")

        if filtre == 'Nombre de page asc':
            cur.execute(
                'select * from livres order by nbrepages asc limit 50')
            items = cur.fetchall()
            return render_template('articles.html', items=items, page=1, next=0, prev=2, searchInput="Search by title")

        if filtre == 'Nombre de page asc':
            cur.execute(
                'select * from livres order by nbrepages desc limit 50')
            items = cur.fetchall()
            return render_template('articles.html', items=items, page=1, next=0, prev=2, searchInput="Search by title")

    return redirect(url_for('articles.render_articles'))
