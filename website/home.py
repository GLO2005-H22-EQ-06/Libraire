from flask import Blueprint, render_template, session

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def render():
    if 'username' in session:
        username = session['username']
        print(username)
        return render_template("home.html", username=username)
    return render_template("home.html")
