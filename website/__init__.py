from flask import Flask
from .home import home
from .account import account
from .main import SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(account, url_prefix="/account")

    return app  