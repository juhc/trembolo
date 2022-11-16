from flask import Blueprint, render_template, request, flash
from .forms import LoginForm, RegisterForm

account = Blueprint("account", __name__)


@account.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        flash('Вы успшено вошли в аккаунт', category='success')


    return render_template("account.html", form=form)


@account.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    form = RegisterForm()

    if form.validate_on_submit():
        flash('Ваш аккаунт успешно зарегистрирован', category='success')
        
    return render_template("sign-up.html", form=form)
