from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(128), nullable=False)


