from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


class LoginForm(FlaskForm):
    email = StringField(
        "Электронный адрес",
        validators=[DataRequired(), Email("Указан неверный адрес электронной почты")],
    )
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    email = StringField(
        "Адрес электронной почты",
        validators=[DataRequired(), Email("Указан неверный адрес электронной почты")],
    )
    phone = StringField(
        "Номер телефона", validators=[DataRequired()]
    )
    address = StringField("Адрес", validators=[DataRequired()])
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=4, message=f"Минимальная длина пароля от %{min}d символов"),
            EqualTo("confirm_password", message="Пароли не совпадают"),
        ],
    )
    confirm_password = PasswordField("Подтверждение пароля")
    submit = SubmitField('Зарегистрироваться')

    def validate_name(form, field):
        if not field.data.isalpha():
            raise ValidationError('Имя содержит не только буквы')
    
    def validate_surname(form, field):
        if not field.data.isalpha():
            raise ValidationError('Фамилия содержит не только буквы')