from flask import Flask, render_template,request
import locale
from webapp_stores.model import db,Stores,Product
from webapp_stores.db_functions import save_data_product, save_interesting_product
from webapp_stores.stores.butik import get_butik_product
from webapp_stores.stores.randevu import get_randevu_product
#from webapp_stores import store_parser_bylink_ali





def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)


    @app.route('/', methods=['GET', 'POST'])
    def index():
        locale.setlocale(locale.LC_ALL, "ru_RU")
        try:
            link = request.form['link']
            if 'butik' in link:
                info=get_butik_product(link) #dictionary with info about product
            elif 'rendez-vous' in link:
                info=get_randevu_product(link) #dictionary with info about product
            elif 'aliexpress' in link:
                info=None #вставить функцию алика для того, чтобы получить словарь с данными

            with app.app_context():

                # Сохранение данных в общую базу данных
                save_data_product(info)

                # Сохранение данных в клиентскую базу данных
                size_interesting = request.form['size']
                email = request.form['email']

                save_interesting_product(product_dict=info, email=email, price_interesting=None, color_interesting=None,
                                         size_interesting=size_interesting)
        except:
            info = None
        return render_template('index.html', info=info)

    # @app.route('/store')
    # def store():
    #     locale.setlocale(locale.LC_ALL, "ru_RU")
    #     store_all = Stores.query.all()
    #     # Product.query.all()
    #     return render_template('store_page.html',store_all = store_all)
    #
    #
    # @app.route('/admin')
    # def admin_panel():
    #     locale.setlocale(locale.LC_ALL, "ru_RU")
    #     return render_template('admin_panel.html')

    return app





