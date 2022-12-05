from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import User


class LoginForm(FlaskForm):
    email = StringField(
        "Адрес электронной почты",
        validators=[DataRequired(), Email("Указан неверный адрес электронной почты")],
        render_kw={"placeholder": "Введите адрес электронной почты"},
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired()],
        render_kw={"placeholder": "Введите пароль"},
    )
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField(
        "Имя",
        validators=[DataRequired()],
        render_kw={"placeholder": "Напишите ваше имя"},
    )
    surname = StringField(
        "Фамилия",
        validators=[DataRequired()],
        render_kw={"placeholder": "Напишите вашу фамилию"},
    )
    email = StringField(
        "Адрес электронной почты",
        validators=[DataRequired(), Email("Указан неверный адрес электронной почты")],
        render_kw={"placeholder": "Укажите адрес электронной почты"},
    )
    phone = StringField(
        "Номер телефона",
        validators=[DataRequired()],
        render_kw={"placeholder": "Укажите ваш номер телефона"},
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=4, message=f"Минимальная длина пароля от %{min}d символов"),
            EqualTo("confirm_password", message="Пароли не совпадают"),
        ],
        render_kw={"placeholder": "Введите пароль"},
    )
    confirm_password = PasswordField(
        "Подтверждение пароля", render_kw={"placeholder": "Введите пароль еще раз"}
    )
    submit = SubmitField("Зарегистрироваться")

    def validate_name(form, field):
        if not field.data.isalpha():
            raise ValidationError("Имя содержит не только буквы")

    def validate_surname(form, field):
        if not field.data.isalpha():
            raise ValidationError("Фамилия содержит не только буквы")

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Акканут с такой электронной почтой уже существует")

    def validate_phone(form, field):
        if User.query.filter_by(phone=field.data).first():
            raise ValidationError("Акканут с таким номер телефона уже существует")


class ReviewForm(FlaskForm):
    data = TextAreaField(
        "Отзыв",
        render_kw={"placeholder": "Отзыв"},
        validators=[DataRequired()],
        id="floatingTextarea2",
    )
    submit = SubmitField("Отправить отзыв")


class OrderForm(FlaskForm):
    address = StringField(
        "Адрес", render_kw={"placeholder": "Адрес"}, validators=[DataRequired()]
    )
    home = IntegerField('Дом', validators=[DataRequired()])
    corps = StringField('Корпус', render_kw={'placeholder':'Корпус'})
    door_phone = home = IntegerField('Дом')
    room = IntegerField('Квартира')
    submit = SubmitField('Подтвердить заказ')
