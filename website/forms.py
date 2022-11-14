from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class LoginForm(FlaskForm):
    email = StringField('Электронный адрес', validators=[DataRequired(), Email('*Указан неверный адрес электронной почты')])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, message='*Длина пароля должна быть больше 4 символов')])
    submit = SubmitField('Войти')

