from flask import Flask, render_template,request
import locale
from flask_login import LoginManager
from webapp_stores.user.model import User
from webapp_stores.stores.model import db,Stores,Product
from webapp_stores.stores.ali import Aliexpress
from webapp_stores.user.views import blueprint as user_bp
from webapp_stores.db_functions import save_data_product, save_interesting_product
from webapp_stores.stores.butik import get_butik_product
from webapp_stores.stores.randevu import get_randevu_product


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    app.register_blueprint(user_bp)
    # celery = Celery(broker='redis://localhost:6379/0')


    @app.route('/', methods=['GET', 'POST'])
    def index():
        #
        locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")
        try:
            link = request.form['link']
            if 'butik' in link:
                info=get_butik_product(link) #dictionary with info about product
            elif 'rendez-vous' in link:
                info=get_randevu_product(link) #dictionary with info about product
            elif 'aliexpress' in link:
                al = Aliexpress()
                info = al.parser_product_result(link)

            # print(info)


            with app.app_context():

                # Сохранение данных в общую базу данных
                save_data_product(info)

                # Сохранение данных в клиентскую базу данных
                size_interesting = request.form['size']
                email = request.form['email']

                save_interesting_product(product_dict=info, email=email, price_interesting=None, color_interesting=None,
                                         size_interesting=size_interesting)


                # a = info['product_image']
                # b = (a.strip('[')).strip(']')
                # x = b.split(',')
                # info['product_image'] = x
                # print(c)
                # print(type(c))

        except:
            info = None


        return render_template('index.html', info=info)

    @app.route('/link', methods=['GET', 'POST'])
    def link():
        locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")
        try:
            link = request.form['link']
            print(link)
            c = Aliexpress()
            info = c.parser_product_result(link)
            print(info)
        except:
            info = None
        return render_template('base.html', info=info, title='Главная страница')

    @app.route('/store')
    def store():
        locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")
        store_all = Stores.query.all()
        # Product.query.all()
        return render_template('store/store_page.html', store_all=store_all)

    @app.route('/admin')
    def admin_panel():
        locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")
        return render_template('admin_panel.html')

    @login_manager.user_loader
    def lode_user(user_id):
        return User.query.get(user_id)

    return app







