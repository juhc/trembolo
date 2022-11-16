from flask import Flask
from .main import SECRET_KEY, DB_NAME
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    db.init_app(app)

    from .home import home
    from .account import account

    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(account, url_prefix="/account")
    
    
    return app


def create_db(app):
    with app.app_context():
        if not os.path.exists(f'website/{DB_NAME}'):
            db.create_all()