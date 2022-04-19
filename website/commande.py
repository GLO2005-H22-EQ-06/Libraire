from math import prod
from flask import Blueprint, render_template, request, Response, session, flash, redirect, url_for

from website.home import render
from . import mysql

commande = Blueprint('commande', __name__)


@commande.route('/commande/<string:id_facture>')
def getCommandeInfo(id_facture):
    cur = mysql.connection.cursor()
    cur.execute(
        'select *, get_prix_remise(ISBN) from facturer natural join livres where id_facture = %s', [id_facture])
    commandeProducts = cur.fetchall()

    return render_template('commande.html', products=commandeProducts)
