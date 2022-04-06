from flask import Blueprint, render_template
from . import mysql

panier = Blueprint('panier', __name__)


@panier.route('/panier', methods=['GET', 'POST'])
def render_panier():
    return render_template("panier.html")


@panier.route('/checkout', methods=['GET', 'POST'])
def render_checkout():
    return render_template("checkout.html")
