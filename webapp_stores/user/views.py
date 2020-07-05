from flask import Blueprint, render_template, flash, url_for, request, current_app
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect
from webapp_stores.user.model import User, db, InterestingProduct
from webapp_stores.user.forms import Login_form, Registration_user

from webapp_stores.db_functions import delete_interesting_product, find_product, save_interesting_product
from webapp_stores.utils import get_info

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



@blueprint.route("/my_products")
def my_products():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    title = 'My products'
    user_id=current_user.get_id()
    #user = User.query.filter_by(id=user_id).first()

    user_interesting_products=InterestingProduct.query.filter_by(client_id=user_id).all()
    #print(user_interesting_products)
    return render_template('user/my_products.html', title=title, products=user_interesting_products)


@blueprint.route("/delete_product", methods=['POST'])
def delete_product():
    id=int(request.form['product_to_delete'])
    print(type(id))
    with current_app.app_context():
        delete_interesting_product(id)

    return redirect(url_for('users.my_products'))

@blueprint.route("/search", methods=['GET', 'POST'])
def search():
    search = request.form['search']
    with current_app.app_context():
        products=find_product(search)

    return render_template('user/search_products.html', products=products, search=search)

@blueprint.route('/add_product', methods=['GET', 'POST'])
def add_product():
    size_interesting = request.form['size']

    link = request.form['link']

    # Если ссылка более не работает
    try:
        info = get_info(link)
    except:
        flash('Данный товар не доступен в данный момент')
        return redirect(url_for('index'))
    # Если пользователь не зарегистрирован
    if not current_user.is_authenticated:
        flash('Зарегестрируйтесь, чтобы отслеживать товар в личном кабинете')
        return redirect(url_for('users.register'))
    else:
        email=current_user.email
        save_interesting_product(product_dict=info, email=email, size_interesting=size_interesting)
        return redirect(url_for('users.my_products'))


