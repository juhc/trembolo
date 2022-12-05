from flask import Blueprint, request, render_template
from flask_login import current_user, login_required
from .forms import OrderForm 

order = Blueprint("order", __name__)


@order.route("/", methods=["POST", "GET"])
@login_required
def apply_order():
    if request.method == "POST":
        pass
    
    else:
        form = OrderForm()
        return render_template('order.html', form=form, user=current_user)

        