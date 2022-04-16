from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from . import mysql
from datetime import datetime

evaluer = Blueprint('evaluer', __name__)


@evaluer.route('/evaluer/<string:isbn>', methods=['POST'])
def evaluateBook(isbn):
    if 'username' in session:
        try:
            note = int(request.form['note'])
        except:
            flash('You must chose a rating to evaluate the book', category='error')
            return redirect(url_for('articles.viewBook', isbn=isbn))

        commentaire = request.form['commentaire']

        now = datetime.now()

        username = session['username']

        cur = mysql.connection.cursor()
        cur.execute(
        'SELECT id_client FROM associer WHERE identifiant = %s', [username])
        userId = cur.fetchone()

        cur.execute('select * from evaluer where id_client=%s and ISBN=%s', (userId, isbn))
        evaluation = cur.fetchone()

        if evaluation is not None:
            flash('You have already reviewed this book', category='error')
            return redirect(url_for('articles.viewBook', isbn=isbn))

        cur.execute('insert into evaluer values (%s, %s, %s, %s, %s)', (userId, isbn, note, commentaire, now))
        mysql.connection.commit()
        
        flash('Evaluation successfully submitted !', category='success')
        return redirect(url_for('articles.viewBook', isbn=isbn))

    flash('You have te be connected to review a book', category='error')
    return redirect(url_for('articles.viewBook', isbn=isbn))