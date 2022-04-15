from flask import Blueprint, render_template, request, Response, session, flash, redirect, url_for

from website.home import render
from . import mysql

user = Blueprint('user', __name__)


@user.route('/profil')
def getUserInfo():
    if not 'username' in session:
        flash('You have to be connected for acceding')
        return redirect(url_for('home.render'))

    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute(
        'select id_client from associer where identifiant = %s', [username])
    userid = cur.fetchone()

    cur.execute('select * from clients where id_client = %s', [userid])
    profil_user = cur.fetchone()

    # change for the new function, to get commandeInfo
    cur.execute(
        'select * from commandes where id_client = %s order by date desc', [userid])
    factures_user = cur.fetchall()

    return render_template('userInfo.html', profil=profil_user, commandes=factures_user,loggedin=True)
