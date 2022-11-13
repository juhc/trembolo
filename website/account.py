from flask import Blueprint, render_template

account = Blueprint('account',__name__)


@account.route('/login')
def login():
    return render_template('account.html')

@account.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')
