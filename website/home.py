from flask import Blueprint, render_template, redirect, request, session, jsonify
from flask_login import current_user
from .forms import ReviewForm
from .models import Review, User, Product
import json
from . import db

home = Blueprint("home", __name__)


@home.route("/")
def index():
    pizza = Product.query.filter_by(category="Пицца").all()
    snacks = Product.query.filter_by(category="Закуски").all()
    desserts = Product.query.filter_by(category="Десерты").all()
    drinks = Product.query.filter_by(category="Напитки").all()

    return render_template(
        "index.html",
        user=current_user,
        pizza=pizza,
        snacks=snacks,
        desserts=desserts,
        drinks=drinks,
    )


@home.route("/reviews", methods=["POST", "GET"])
def reviews():
    review_form = ReviewForm()

    if review_form.validate_on_submit():
        new_review = Review(data=review_form.data.data, user_id=current_user.id)
        db.session.add(new_review)
        db.session.commit()

    return render_template(
        "reviews.html",
        user=current_user,
        review_form=review_form,
        reviews=Review.query.all(),
        User=User,
    )


@home.route("/add-to-cart", methods=["POST", "GET"])
def add_product_to_cart():
    if request.method == "POST":
        product_id = str(json.loads(request.data)['productId'])
        product = Product.query.get(product_id)
        product_dict = {
            product_id: {
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "photo": product.photo_url,
                "count": 1,
            }
        }

        if "shoppingcart" in session:
            if product_id in session["shoppingcart"]:
                return jsonify({})
            else:
                session["shoppingcart"] = dict(
                    list(session["shoppingcart"].items()) + list(product_dict.items())
                )
        else:
            session["shoppingcart"] = product_dict

        return jsonify({})


@home.route("/increase-product", methods=["POST"])
def increase_product():
    if request.method == "POST":
        product_id = str(json.loads(request.data)["productId"])
        session["shoppingcart"][product_id]["count"] += 1
        session.modified = True
        return jsonify({})


@home.route("/decrease-product", methods=["POST"])
def decrease_product():
    if request.method == "POST":
        product_id = str(json.loads(request.data)["productId"])
        session["shoppingcart"][product_id]["count"] -= 1
        session.modified = True
        return jsonify({})


@home.route("/delete-product", methods=["POST"])
def delete_product():
    if request.method == "POST":
        product_id = str(json.loads(request.data)["productId"])
        session["shoppingcart"].pop(product_id)
        session.modified = True
        return jsonify({})


def mergedicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    else:
        return False


@home.route("/product/<int:id>")
def get_product_byId(id):
    product = Product.query.get({id})
    return jsonify(
        {
            "id":str(product.id),
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "photo_url": product.photo_url,
            "price": product.price,
        }
    )
