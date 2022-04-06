from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def render():
    return render_template("home.html")
