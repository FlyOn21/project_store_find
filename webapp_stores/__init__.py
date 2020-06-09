from flask import Flask, render_template
import locale
from webapp_stores.model import db,Model_stores


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)


    @app.route('/')
    def index():
        locale.setlocale(locale.LC_ALL, "ru")
        return render_template('index.html')


    @app.route('/store')
    def store():
        locale.setlocale(locale.LC_ALL, "ru")
        store_all = Model_stores.query.all()
        return render_template('store_page.html',store_all = store_all)


    @app.route('/admin')
    def admin_panel():
        locale.setlocale(locale.LC_ALL, "ru")
        return render_template('admin_panel.html')

    return app





