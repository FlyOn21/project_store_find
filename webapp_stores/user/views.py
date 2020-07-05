from flask import Blueprint, render_template, flash, url_for
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect
from webapp_stores.user.model import User, db, InterestingProduct
from webapp_stores.user.forms import Login_form, Registration_user,Mailsend_off,Mailsend_on

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
                        username=form.username.data, is_active=True, role='user', send_mail = True)
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



@blueprint.route("/my_products")
def my_products():
    title = 'My products'

    user_id=current_user.get_id()
    user = User.query.filter_by(id=user_id).first()
    mail_send = user.send_mail
    user_interesting_products = InterestingProduct.query.filter_by(client_id=user_id).all()
    if mail_send == True:
        send = 'Оповищение на e-mail активно'
        form = Mailsend_off()
        return render_template('user/my_products.html', title=title, products=user_interesting_products, send=send,
                               form=form)
    else:
        send = 'Оповищение на e-mail отключено'
        form = Mailsend_on()
        return render_template('user/my_products.html', title=title, products=user_interesting_products, send=send,
                               form=form)

    #print(user.name)
    # mail = query.email


    #print(user_interesting_products)


@blueprint.route("/on_off", methods=['POST'])
def on_off():
    user_id = current_user.get_id()
    user = User.query.filter_by(id=user_id).first()
    mail_send = user.send_mail
    if mail_send == True:
        form = Mailsend_off()
        if form.validate_on_submit():
            user_id = current_user.get_id()
            user_off = User.query.filter_by(id=user_id).first()
            user_off.send_mail = False
            db.session.add(user_off)
            db.session.commit()
            return redirect(url_for('users.my_products'))
    else:
        form = Mailsend_on()
        if form.validate_on_submit():
            user_id = current_user.get_id()
            user_off = User.query.filter_by(id=user_id).first()
            user_off.send_mail = True
            db.session.add(user_off)
            db.session.commit()
            return redirect(url_for('users.my_products'))


