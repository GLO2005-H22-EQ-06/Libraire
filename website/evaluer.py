from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from . import mysql
from datetime import datetime

evaluer = Blueprint('evaluer', __name__)


@evaluer.route('/evaluer/<string:isbn>', methods=['POST'])
def evaluateBook(isbn):
    if 'username' in session:
        note = int(request.form['note'])
        commentaire = request.form['commentaire']
        now = datetime.now()

        username = session['username']

        cur = mysql.connection.cursor()
        cur.execute(
        'SELECT id_client FROM associer WHERE identifiant = %s', [username])
        userId = cur.fetchone()

        if isinstance(note, int) and note <= 5 and note > 0:
            cur.execute('insert into evaluer values (%s, %s, %s, %s, %s)', [userId, isbn, note, commentaire, now])
            flash('Evaluation successfully submitted !', category='success')
            return redirect(url_for('articles.viewBook', isbn=isbn))
        else:
            flash("La note doit être un entier comprise entre 0 et 5", category='error')
            redirect(url_for('evaluer.evaluateBook', isbn=isbn))
