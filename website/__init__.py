from flask import Flask, session
from flask_mysqldb import \
    MySQL

mysql = MySQL()
salt = b'$2b$12$R2Yw1fjNG8loy69c8PrWWO'


def createApp():
    app = Flask(__name__)
    app.secret_key = "web app"
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = "EnvyUS123"
    app.config["MYSQL_DB"] = "projet_glo_2005"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    mysql.__init__(app)

    from .home import home
    from .auth import auth
    from .panier import panier
    from .articles import articles
    from .user import user
    from .evaluer import evaluer
    from .commande import commande

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(panier, url_prefix='/')
    app.register_blueprint(articles, url_prefix='/')
    app.register_blueprint(user, url_prefic='/')
    app.register_blueprint(evaluer, url_prefic='/')
    app.register_blueprint(commande, url_prefix='/')

    return app
