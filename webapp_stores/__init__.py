from flask import Flask, render_template,request
import locale
import ast
from flask_login import LoginManager,current_user
from webapp_stores.user.model import User
from webapp_stores.stores.model import db,Stores,Product
from webapp_stores.stores.ali import Aliexpress
from webapp_stores.user.views import blueprint as user_bp
from webapp_stores.product.views import blueprint as prod_bp
from webapp_stores.mail.views import blueprint as mail_bp
from webapp_stores.db_functions import save_data_product, save_interesting_product
from webapp_stores.stores.butik import get_butik_product
from webapp_stores.stores.randevu import get_randevu_product
from webapp_stores.utils import get_info

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    app.register_blueprint(user_bp)
    app.register_blueprint(prod_bp)
    app.register_blueprint(mail_bp)





    @app.route('/', methods=['GET', 'POST'])
    def index():
        #
        locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")
        try:
            link = request.form['link']
            info=get_info(link)
            print(info)

            with app.app_context():

                # Сохранение данных в общую базу данных
                save_data_product(info)

                # Сохранение данных в клиентскую базу данных
                size_interesting = request.form['size']
                print('______________________________________')
                if current_user.is_anonymous is True:
                    email = request.form['email']
                else:
                    email = current_user_mail()


                save_interesting_product(product_dict=info, email=email, price_interesting=None, color_interesting=None,
                                         size_interesting=size_interesting)
                print('_______________________________________')

                img_list = info['product_image']
                # print(type(img_list))
                # if len(img_list)>200:
                #     img_list_all = ast.literal_eval(img_list)
                # else:
                #     img_list_all = info['product_image']
                if len(img_list)>60:
                    img_clear_1 = (img_list.strip('[')).strip(']')
                    img_clear_2 = img_clear_1.split(',')
                    all_img = []
                    for img in img_clear_2:
                        img_clear = (img.strip("'")).strip(" '")
                        print(img_clear)
                        all_img.append(img_clear)

                    info['product_image'] = all_img
                    print(info)

                user = current_user.get_id()
                query = User.query.filter_by(id=user).first()
                name = query.username
                print(name)

        except:
            info = None
        return render_template('index.html', info=info)

    @app.route('/store')
    def store():
        locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")
        store_all = Stores.query.all()
        return render_template('store/store_page.html', store_all=store_all)

    @app.route('/admin')
    def admin_panel():
        locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")
        return render_template('admin/admin_panel.html')

    @login_manager.user_loader
    def lode_user(user_id):
        return User.query.get(user_id)




    def current_user_mail():
        """Функция получения електронной почты текушего активного пользователя"""
        user = current_user.get_id()
        print('------',user,'--------')
        query = User.query.filter_by(id = user).first()
        mail = query.email
        print(mail)
        return mail



    return app









