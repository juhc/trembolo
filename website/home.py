from flask import Blueprint, render_template, abort
from flask_login import current_user
from .forms import ReviewForm
from .models import Review, User
from . import db

home = Blueprint("home", __name__)


@home.route("/")
def index():
    return render_template("index.html", user=current_user)


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
        User=User
    )