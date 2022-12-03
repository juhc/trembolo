from flask_login import UserMixin
from sqlalchemy import func
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
    reviews = db.relationship("Review")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(512), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True ,nullable=False)
    description = db.Column(db.String(256))
    category = db.Column(db.String(32), nullable=False)
    photo_url = db.Column(db.String(256))
    price = db.Column(db.Integer, nullable=False)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    products = db.relationship('CartProduct')


class CartProduct(db.Model):
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id', ondelete='CASCADE'), primary_key=True,)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), primary_key=True,)