from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import SubmitField, StringField, PasswordField, HiddenField, BooleanField, FormField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from webapp_stores.user.model import User


class Login_form(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={'class': "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': "form-control"})
    hidden_f = HiddenField()
    remember_me = BooleanField('Запомни меня', default=True, render_kw={'class': "form-check-input"})
    submit = SubmitField('SEND', render_kw={"class": "btn btn-primary"})

class Password_reset(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={'class': "form-control"})
    hidden_f = HiddenField()
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

class Reset_pass_process(FlaskForm):

    password = PasswordField('Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')
                                          ], render_kw={'class': "form-control"})
    confirm = PasswordField('Repeat Password', render_kw={'class': "form-control"})
    user_current = HiddenField()
    submit = SubmitField('Сменить пароль', render_kw={"class": "btn btn-primary"})


class Registration_user(FlaskForm):
    name = StringField('Name', [Length(min=1, max=25), DataRequired()], render_kw={'class': 'form-control'})
    surname = StringField('Surname', [DataRequired(), Length(min=1, max=30)], render_kw={'class': "form-control"})
    username = StringField('Username', [Length(min=1, max=25), DataRequired()], render_kw={'class': "form-control"})
    email = StringField('Email Address', [Length(min=6, max=35), Email(), DataRequired()],
                        render_kw={'class': "form-control"})
    password = PasswordField('Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')
                                          ], render_kw={'class': "form-control"})
    confirm = PasswordField('Repeat Password', render_kw={'class': "form-control"})
    accept_tos = BooleanField('Я согласен на сохранение данных обо мне', [DataRequired()],
                              render_kw={'class': "form-check-input"})
    submit = SubmitField('REGISTRATION', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user_c = User.query.filter_by(username=username.data).count()
        if user_c > 0:
            raise ValidationError('Пользователь с таким логином сушествует')

    def validate_email(self, email):
        user_mail = User.query.filter_by(email=email.data).count()
        if user_mail > 0:
            raise ValidationError('Пользователь с таким e-mail сушествует')

class Mailsend_off(FlaskForm):
    """Форма для дизактивации отправки сообшений на email"""
    # on = FormField('Включить', render_kw={"class": "btn btn-primary btn-lg disabled"})

    off = SubmitField('Выключить', render_kw={"class": "btn btn-secondary"})


class Mailsend_on(FlaskForm):
    """Форма для активации отправки сообшений на email"""
    on = SubmitField('Включить', render_kw={"class": "btn btn-secondary" })
    # off = StringField('Выключить', render_kw={"class": "btn btn-primary btn-lg disabled"})

