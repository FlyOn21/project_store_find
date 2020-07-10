from flask import Blueprint, render_template, flash, url_for, request, current_app
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect
# from webapp_stores.user.model import User, db, InterestingProduct
# from webapp_stores.user.forms import Login_form, Registration_user
#
# from webapp_stores.db_functions import delete_interesting_product
from webapp_stores.user.model import User, db, InterestingProduct
from webapp_stores.user.forms import Login_form, Registration_user,Mailsend_off,Mailsend_on,Password_reset,Reset_pass_process
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


@blueprint.route('/reset_pass')
def reset_pass():
    title = 'Смена пароля'
    form = Password_reset()
    return render_template('user/reset_pass.html',title = title,form = form)

@blueprint.route('/process_reset_pass',methods=['POST'])
def process_reset_pass():
    from tasks import email_reset_pass
    form = Password_reset()
    if form.validate_on_submit():
        print('-------')
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        print(user)
        print('-------')
        if user:
            url = 'http://127.0.0.1:5000' + str(url_for('users.form_reset_pass')) + '?' + 'mail=' + str(email)
            print(url)

            # email_reset_pass.delay(e_mail,url)

@blueprint.route('/form_reset_pass',methods=['GET'])
def form_reset_pass():
    title = 'Форма смены пароля'
    form = Reset_pass_process()
    return render_template('user/reset_pass_process.html',title = title,form = form)


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


