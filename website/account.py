from flask import Blueprint, render_template, request, flash, url_for, redirect
from .forms import LoginForm, RegisterForm
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

account = Blueprint("account", __name__)


@account.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        authenticate(form)

    return render_template("account.html", form=form)


@account.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    form = RegisterForm()

    if form.validate_on_submit():
        registrate_user(form)

    return render_template("sign-up.html", form=form)


def registrate_user(form):
    new_user = User(
        name=form.name.data,
        surname=form.surname.data,
        email=form.email.data,
        phone=form.phone.data,
        address=form.address.data,
        password=generate_password_hash(form.password.data, method="sha256"),
    )

    if User.query.filter_by(email=new_user.email).first():
        flash('Аккаунт с таким электронным адресом уже существует')
    
    if User.query.filter_by(phone=new_user.phone).first():
        flash('Аккаунт с таким номером телефона уже существует')

    else:
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Ваш аккаунт успешно зарегистрирован", category="success")
            return redirect(url_for("account.login"))
        except:
            pass


def authenticate(form):
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        if check_password_hash(user.password, form.password.data):
            flash("Вы успшено вошли в аккаунт", category="success")
        else:
            flash("Не получилось войти в аккаунт", category="error")
