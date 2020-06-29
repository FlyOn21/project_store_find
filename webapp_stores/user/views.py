from flask import Blueprint, render_template, flash, url_for
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect
from webapp_stores.user.model import User, db
from webapp_stores.user.forms import Login_form, Registration_user

blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'Autorization'
    form = Login_form()
    return render_template('user/login.html', title=title, form=form)

@blueprint.route("/")
def index():
    return redirect(url_for("index"))

@blueprint.route("/process-login", methods=['POST'])
def process_login():
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You come')
            return redirect(url_for('index'))
    flash('incorrect password')
    return redirect(url_for('users.login'))


@blueprint.route("/register")
def register():
    title = 'Registration'
    form = Registration_user()
    return render_template('user/sing_in.html', title=title, form=form)


@blueprint.route("/register_do", methods=['POST'])
def register_do():
    form = Registration_user()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data, surname=form.surname.data,
                        username=form.username.data, is_active=True, role='user')
        new_user.save_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('You registred')
        return redirect(url_for('index'))
    else:
        for field,errors in form.errors.items():
            for error in errors:
                flash('ошибка в поле"{}":{}'.format(getattr(form,field).label.text,error))
                redirect(url_for('users.register'))
    flash('Пожалуйста исправте ошибки в форме')
    return redirect(url_for('users.register'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('You logout')
    return redirect(url_for('index'))
