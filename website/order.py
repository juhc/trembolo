from flask import Blueprint, request, render_template, session, redirect, url_for
from flask_login import current_user, login_required
from .forms import OrderForm
from . import mail
from flask_mail import Message
from .main import MAIL_USERNAME

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
        msg_to_user = Message('Ваш заказ принят', sender=MAIL_USERNAME, recipients=['chalkov2002@mail.ru'])
        msg_to_user.body = 'test'

        msg_to_trembolo = Message(f'Заказ от пользователя {current_user.email}', sender=MAIL_USERNAME, recipients=[MAIL_USERNAME])
        msg_to_trembolo.body = f'Заказ от пользователя {current_user.email}'
        
        try:
            mail.send(msg_to_user)
            mail.send(msg_to_trembolo)
        except:
            pass

        session['shoppingcart'] = {}
        return render_template('order-accept.html')

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
