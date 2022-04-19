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
    limit = 10
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
        "select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L order by ISBN limit %s offset %s", (limit, offset))

    items = cur.fetchall()
    ratings = []
    for i in items:
        if i[8] is not None:
            ratings.append(int(i[8]))
        else:
            ratings.append(0)

    loggedIn = 'username' in session
    return render_template("articles.html", items=items, loggedin=loggedIn, total_page=total_page,
                           page_start=page_start, page_end=page_end, next=next, prev=prev,
                           searchInput="Search for a title or ISBN ", current_page=page, all=True, ratings=ratings)


@articles.route('/articles/details/isbn=<string:isbn>')
def viewBook(isbn):
    cur = mysql.connection.cursor()
    cur.execute('select * from livres where isbn = %s', [isbn])
    livre = cur.fetchone()
    if livre[8] is not None:
        mean_rating = livre[8]
    else:
        mean_rating = 0

    intMean = int(mean_rating)
    flMean = mean_rating - intMean

    if 'username' in session:
        username = session['username']

        cur.execute(
            'SELECT id_client FROM associer WHERE identifiant = %s', [username])
        userId = cur.fetchone()

        cur.execute(
            'SELECT * from associer JOIN (SELECT * FROM evaluer WHERE id_client=%s and ISBN=%s) as tb on associer.id_client = tb.id_client', [userId, isbn])
        current_user_evaluated_books = cur.fetchone()
        if current_user_evaluated_books:
            current_user_rating = current_user_evaluated_books[4]
        else:
            current_user_rating = 0

        cur.execute(
            'SELECT * from associer natural join evaluer WHERE id_client !=%s and isbn=%s', [userId, isbn])
        all_other_evaluations = cur.fetchall()
        ratings = []
        for evaluation in all_other_evaluations:
            ratings.append(evaluation[3])
        ratings_len = len(ratings)

        return render_template('livre.html', livre=livre,
                               all_other_evaluations=all_other_evaluations, current_user_evaluated_books=current_user_evaluated_books,
                               current_user_rating=current_user_rating, ratings=ratings, ratings_len=ratings_len, loggedin=True, mean_rating=intMean, flMean=flMean)
    else:
        cur.execute(
            'SELECT * from associer natural join evaluer WHERE isbn=%s', [isbn])
        all_evaluations = cur.fetchall()
        ratings = []
        for evaluation in all_evaluations:
            ratings.append(evaluation[3])
        ratings_len = len(ratings)

        return render_template('livre.html', livre=livre,
                               all_other_evaluations=all_evaluations, ratings=ratings, ratings_len=ratings_len, loggedin=False, mean_rating=intMean, flMean=flMean)


@articles.route('/articles/filters/byTitle/', methods=['GET'])
def searchByTitleOrIsbn():
    searchEntered = request.args.get('search')
    cur = mysql.connection.cursor()

    cur.execute("select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L where titre like %s or ISBN = %s order by ISBN limit 50",
                (('%' + searchEntered + '%'), searchEntered))
    items = cur.fetchall()

    ratings = []
    for i in items:
        if i[8] is not None:
            ratings.append(int(i[8]))
        else:
            ratings.append(0)

    loggedIn = 'username' in session
    return render_template("articles.html", items=items, loggedin=loggedIn, all=False, searchInput=searchEntered, ratings=ratings)


@articles.route('/articles/filters/', methods=['GET'])
def filter():
    filtre = request.args.get('filter')
    cur = mysql.connection.cursor()

    loggedIn = 'username' in session

    if filtre == 'None':
        return redirect(url_for('articles.render_articles'))

    if filtre == 'Price asc':
        cur.execute(
            "select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L order by prix asc limit 50")
        items = cur.fetchall()
        ratings = []
        for i in items:
            if i[8] is not None:
                ratings.append(int(i[8]))
            else:
                ratings.append(0)
        return render_template('articles.html', loggedin=loggedIn, items=items, title=False, all=False, searchInput="Search for a title or ISBN", ratings=ratings)

    if filtre == 'Price desc':
        cur.execute(
            "select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L order by prix desc limit 50")
        items = cur.fetchall()

        ratings = []
        for i in items:
            if i[8] is not None:
                ratings.append(int(i[8]))
            else:
                ratings.append(0)
        return render_template('articles.html', loggedin=loggedIn, items=items, title=False, all=False, searchInput="Search for a title or ISBN", ratings=ratings)

    if filtre == 'Rating asc':
        cur.execute(
            "select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L order by note asc limit 50")

        items = cur.fetchall()
        ratings = []
        for i in items:
            if i[8] is not None:
                ratings.append(int(i[8]))
            else:
                ratings.append(0)
        return render_template('articles.html', loggedin=loggedIn, items=items, title=False, all=False, searchInput="Search for a title or ISBN", ratings=ratings)

    if filtre == 'Rating desc':
        cur.execute(
            "select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L order by note desc limit 50")

        items = cur.fetchall()
        ratings = []
        for i in items:
            if i[8] is not None:
                ratings.append(int(i[8]))
            else:
                ratings.append(0)
        return render_template('articles.html', loggedin=loggedIn, items=items, title=False, all=False, searchInput="Search for a title or ISBN", ratings=ratings)

    if filtre == 'Nombre de page asc':
        cur.execute(
            "select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L order by nbrepages asc limit 50")
        items = cur.fetchall()

        ratings = []
        for i in items:
            if i[8] is not None:
                ratings.append(int(i[8]))
            else:
                ratings.append(0)
        return render_template('articles.html', loggedin=loggedIn, items=items, title=False, all=False, searchInput="Search for a title or ISBN", ratings=ratings)

    if filtre == 'Nombre de page desc':
        cur.execute(
            "select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L order by nbrepages desc limit 50")
        items = cur.fetchall()

        ratings = []
        for i in items:
            if i[8] is not None:
                ratings.append(int(i[8]))
            else:
                ratings.append(0)
        return render_template('articles.html', loggedin=loggedIn, items=items, title=False, all=False, searchInput="Search for a title or ISBN", ratings=ratings)
