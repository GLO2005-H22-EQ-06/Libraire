from flask import Blueprint, render_template, session

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def render():
    if 'username' in session:
        username = session['username']
        return render_template("home.html", username)
    return render_template("home.html")
