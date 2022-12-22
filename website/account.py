from flask import Blueprint, render_template, flash, url_for, redirect, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, PasswordRecoveryForm, PasswordChangeForm
from . import db, url_serializer, mail
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Cart
from itsdangerous import BadTimeSignature, BadSignature
from flask_mail import Message
from .main import MAIL_USERNAME

account = Blueprint("account", __name__)


@account.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        authenticate(form)
        if current_user.is_authenticated:
            return redirect(url_for("account.profile"))

    return render_template("account.html", form=form, user=current_user)


@account.route("/profile")
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


@account.route("/password-recovery", methods=["POST", "GET"])
def password_recovery():
    if current_user.is_authenticated:
        abort(404)

    form = PasswordRecoveryForm()

    if form.validate_on_submit():
        email = form.email.data.lower()
        if User.query.filter_by(email=email).first():
            token = url_serializer.dumps(email)
            message = Message(
                "Восстановление пароля", sender=MAIL_USERNAME, recipients=[email]
            )
            link = url_for("account.password_change", token=token, _external=True)
            message.body = (
                f"Чтобы сменить пароль, вам необходимо перейти по ссылке {link}"
            )
            try:
                mail.send(message)
            except:
                pass
            flash(
                "Письмо с восстанавлением пароля отправлено на эл. почту",
                category="success",
            )
            return redirect(url_for("account.login"))
        else:
            flash(f"Аккаунт с эл. почтой {email} не найден", category="error")

    return render_template("password-recovery.html", user=current_user, form=form)


@account.route("/password-recovery/<token>", methods=["POST", "GET"])
def password_change(token):
    form = PasswordChangeForm()
    try:
        email = url_serializer.loads(token, max_age=3600)
    except BadTimeSignature:
        abort(404)
    except BadSignature:
        abort(404)
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        new_password = form.password.data
        user.password = generate_password_hash(new_password, method="sha256")

        db.session.commit()

        flash("Пароль успешно изменен", category="success")
        return redirect(url_for("account.login"))

    return render_template("password-change.html", form=form, user=current_user)


def registrate_user(form):
    new_user = User(
        name=form.name.data.capitalize(),
        surname=form.surname.data.capitalize(),
        email=form.email.data.lower(),
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
        flash("Во время регистрации произошла ошбика, попробуйте еще раз")
        return redirect(url_for("account.sign_up"))


def authenticate(form):
    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user)
        else:
            flash("Неправильный пароль", category="error")
    else:
        flash("Аккаунт с такой электронной почтой не найден", category="error")
