from flask import Flask
from .main import SECRET_KEY, DB_NAME
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    db.init_app(app)

    from .home import home
    from .account import account

    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(account, url_prefix="/account")

    login_manager.login_view = "account.login"
    login_manager.login_message = "Для доступа к данной странице требуется авторизация"
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    create_db(app)
    return app


def create_db(app):
    with app.app_context():
        if not os.path.exists(DB_NAME):
            db.create_all()
