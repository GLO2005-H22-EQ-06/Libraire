from flask import Flask, session
from flask_mysqldb import MySQL

mysql = MySQL()


def createApp():
    app = Flask(__name__)
    app.secret_key = "web app"
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = "root"
    app.config["MYSQL_DB"] = "projet_glo_2005"

    mysql.__init__(app)

    from .home import home
    from .auth import auth
    from .panier import panier
    from .articles import articles
    from .user import user
    from .evaluer import evaluer

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(panier, url_prefix='/')
    app.register_blueprint(articles, url_prefix='/')
    app.register_blueprint(user, url_prefic='/')
    app.register_blueprint(evaluer, url_prefic='/')

    return app
