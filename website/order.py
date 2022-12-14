from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_login import current_user, login_required
from .forms import OrderForm

order = Blueprint("order", __name__)


@order.route("/", methods=["POST", "GET"])
@login_required
def apply_order():
    try:
        if len(session["shoppingcart"]) == 0:
            raise Exception()
    except:
        return redirect(url_for("home.index"))

    if request.method == "POST":
        pass

    else:
        form = OrderForm()
        total_price = sum(
            [
                session["shoppingcart"][product_id]["price"]
                * session["shoppingcart"][product_id]["count"]
                for product_id in session["shoppingcart"]
            ]
        )
        return render_template(
            "order.html", form=form, user=current_user, total_price=total_price
        )
