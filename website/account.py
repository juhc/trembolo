from flask import Blueprint, render_template, request, flash
from .forms import LoginForm

account = Blueprint("account", __name__)


@account.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        flash('Вы успшено вошли в аккаунт.', category='success')


    return render_template("account.html", form=form)


@account.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")
