from flask import Flask, render_template
from .main import SECRET_KEY, DB_NAME, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USERNAME
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_mail import Mail
from .admin import AdminView
import datetime
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.permanent_session_lifetime = datetime.timedelta(hours=2)

    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    mail = Mail(app)

    from .models import User, Review, Product, Cart

    admin = Admin(app, template_mode='bootstrap4')
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Review, db.session))
    admin.add_view(AdminView(Product, db.session))
    admin.add_view(AdminView(Cart, db.session))

    @app.errorhandler(404)
    def pageNotFound(error):
        return render_template("404.html", user=current_user)
    
    @app.errorhandler(403)
    def pageNotFound(error):
        return render_template("403.html", user=current_user)

    db.init_app(app)

    from .home import home
    from .account import account
    from .order import order

    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(account, url_prefix="/account")
    app.register_blueprint(order, url_prefix="/order")

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
