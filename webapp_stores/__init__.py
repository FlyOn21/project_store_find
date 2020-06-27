from flask import Flask, render_template,request
import locale
from flask_login import LoginManager
from webapp_stores.user.model import User
from webapp_stores.stores.model import db,Stores,Product
from webapp_stores.stores.ali import Aliexpress
from celery import Celery
from webapp_stores.user.views import blueprint as user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    app.register_blueprint(user_bp)
    # celery = Celery(broker='redis://localhost:6379/0')


    @app.route('/')
    def index():
        return render_template('base.html', info=None, title = 'Главная страница')

    @app.route('/link',methods=['GET', 'POST'])
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
        return render_template('store_page.html',store_all = store_all)


    @app.route('/admin')
    def admin_panel():
        locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")
        return render_template('admin_panel.html')

    @login_manager.user_loader
    def lode_user(user_id):
        return User.query.get(user_id)

    return app





