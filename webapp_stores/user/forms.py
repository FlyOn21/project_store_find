from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class Login_form(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(),Email()], render_kw={'class': "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': "form-control"})
    hidden_f = HiddenField()
    remember_me = BooleanField('Запомни меня', default=True, render_kw={'class': "form-check-input"})
    submit = SubmitField('SEND', render_kw={"class": "btn btn-primary"})


class Registration_user(FlaskForm):
    name = StringField('Name', [Length(min=1, max=25), DataRequired()], render_kw={'class': 'form-control'})
    surname = StringField('Surname', [DataRequired(), Length(min=1, max=30)], render_kw={'class': "form-control"})
    username = StringField('Username', [Length(min=4, max=25)], render_kw={'class': "form-control"})
    email = StringField('Email Address', [Length(min=6, max=35), Email()], render_kw={'class': "form-control"})
    password = PasswordField('Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')
                                          ], render_kw={'class': "form-control"})
    confirm = PasswordField('Repeat Password', render_kw={'class': "form-control"})
    accept_tos = BooleanField('Я согласен на сохранение данных обо мне', [DataRequired()],
                              render_kw={'class': "form-check-input"})
    submit = SubmitField('REGISTRATION', render_kw={"class": "btn btn-primary"})
    remember_me = HiddenField(default=True)
