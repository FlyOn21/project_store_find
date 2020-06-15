from flask import Flask, render_template,request
import locale
from webapp_stores.model import db,Stores,Product
from webapp_stores import store_parser_by_link,store_parser_bylink_ali



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        locale.setlocale(locale.LC_ALL, "ru_RU")
        try:
            link = request.form['link']
            # print(link)
            info = store_parser_bylink_ali.parser_product_result(link)
            print(info)
        except:
            info = None
        return render_template('index.html', info=info)

    @app.route('/store')
    def store():
        locale.setlocale(locale.LC_ALL, "ru_RU")
        store_all = Stores.query.all()
        # Product.query.all()
        return render_template('store_page.html',store_all = store_all)


    @app.route('/admin')
    def admin_panel():
        locale.setlocale(locale.LC_ALL, "ru_RU")
        return render_template('admin_panel.html')

    return app





