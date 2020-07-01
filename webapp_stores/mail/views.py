from flask_mail import Message,Mail
from flask import Blueprint, render_template, flash, url_for,current_app
from werkzeug.utils import redirect
# from webapp_stores.user.model import User, db
from webapp_stores.stores.model import Product
from webapp_stores.product.views import step_1




blueprint = Blueprint('mail', __name__, url_prefix='/mail')

@blueprint.route('/email',methods=['GET', 'POST'])
def email():
    mail  = Mail(current_app)
    with current_app.app_context():
        dict = zapros()
        msg = Message("Ура мы возможно нашли что вы искали",sender="123@gmail.com",
                      recipients=["zhogolevpv@gmail.com"])
        msg.body = render_template('email/message.txt',dict = dict)
        msg.html = render_template('email/message.html',dict = dict)
        mail.send(msg)
        return redirect(url_for('index'))

def zapros():
    product = Product.query.filter_by(brand = "MELISSA").all()
    print(product)
    count = Product.query.filter_by(brand = "MELISSA").count()
    prod_clear = step_1(product,count=count)
    return prod_clear
if __name__ =="__main__":
    zapros()
