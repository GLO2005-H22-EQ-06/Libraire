from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

mysql = MySQL()


def createApp():
    app = Flask(__name__)
    app.secret_key = "web app"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/glo_2005_labs'

    mysql.__init__(app)

    from .home import home
    from .auth import auth
    from .panier import panier
    from .articles import articles

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(panier, url_prefix='/')
    app.register_blueprint(articles, url_prefix='/')

    return app
