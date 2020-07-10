from flask_mail import Message,Mail

from flask import Blueprint, render_template,current_app
from webapp_stores import create_app
# from werkzeug.utils import redirect
# from webapp_stores.user.model import User, db
# from webapp_stores.stores.model import Product
# from webapp_stores.product.views import step_1




# blueprint = Blueprint('mail', __name__, url_prefix='/mail')

# @blueprint.route('/email',methods=['GET', 'POST'])
def email(e_mail,find_size=None,product=None):
    app = create_app()
    mail = Mail(app)
    with app.app_context():
        # dict = zapros()
        msg = Message("Ура мы возможно нашли что вы искали",sender="123@gmail.com",
                      recipients=[e_mail])
        msg.body = render_template('email/message.txt',find_size = find_size,product = product )
        msg.html = render_template('email/message.html',find_size = find_size,product = product)
        mail.send(msg)
        print("__________Сообщение отправлено____________")
        # return redirect(url_for('index'))

# def zapros():
#     """Отладачаня функция"""
#     product = Product.query.filter_by(brand = "MELISSA").all()
#     print(product)
#     count = Product.query.filter_by(brand = "MELISSA").count()
#     prod_clear = step_1(product,count=count)
#     return prod_clear
# if __name__ =="__main__":
#     zapros()
def reset_pass_mail(e_mail,url):
    app = create_app()
    mail = Mail(app)
    with app.app_context():
        # dict = zapros()
        msg = Message("Перейдите по ссылке для смены вашего пароля",sender="zhogolevpv@gmail.com",
                      recipients=[e_mail])
        msg.body = render_template('email/reset_mail.txt',url = url )
        msg.html = render_template('email/reset_mail.html',url = url)
        mail.send(msg)
        print("__________Сообщение отправлено____________")