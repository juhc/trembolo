from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Cart

account = Blueprint("account", __name__)


@account.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        authenticate(form)
        if current_user.is_authenticated:
            return redirect(url_for('account.profile'))

    return render_template("account.html", form=form, user=current_user)


@account.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@account.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("account.login"))


@account.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    form = RegisterForm()

    if form.validate_on_submit():
        registrate_user(form)
        return redirect(url_for("account.profile"))

    return render_template("sign-up.html", form=form, user=current_user)


def registrate_user(form):
    new_user = User(
        name=form.name.data,
        surname=form.surname.data,
        email=form.email.data,
        phone=form.phone.data,
        password=generate_password_hash(form.password.data, method="sha256"),
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        new_cart = Cart(user_id=User.query.filter_by(phone=form.phone.data).first().id)
        db.session.add(new_cart)
        db.session.commit()
        login_user(new_user)
        flash("Ваш аккаунт успешно зарегистрирован", category="success")
    except Exception as e:
        print(e)


def authenticate(form):
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user)
        else:
            flash("Неправильный пароль", category="error")
    else:
        flash("Аккаунт с такой электронной почтой не найден", category="error")

