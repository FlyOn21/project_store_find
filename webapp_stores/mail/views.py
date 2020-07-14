from flask_mail import Message, Mail
from webapp_stores.stores.model import db
from flask import render_template
from webapp_stores import create_app
from webapp_stores.user.model import Product_all_check


def email():
    app = create_app()
    mail = Mail(app)
    with app.app_context():
        dict = zapros()
        print(dict)
        if dict is False:
            print('Сообшений для отправки нет')
        else:
            for email, list in dict.items():
                # print(email)
                # print(list)
                msg = Message("Ура мы возможно нашли что вы искали", sender="zhogolevpv@gmail.com",
                              recipients=[email])
                msg.body = render_template('email/message.txt', list=list)
                msg.html = render_template('email/message.html', list=list)
                mail.send(msg)
                print("__________Сообщение отправлено____________")


def zapros():
    """Собирает найденые товар из таблицы для найденого и чистит ее"""
    app = create_app()
    with app.app_context():
        products = Product_all_check.query.all()
        if products == []:
            return False
        else:
            all_mail = []
            for product in products:
                all_mail.append(product.email)
            set_list_mail = (set(all_mail))
            dict_for_mail = {}
            for mail in set_list_mail:
                info = Product_all_check.query.filter_by(email=mail).all()
                list_one_check = {}
                for one_check in info:
                    if one_check.int_product == '':
                        size = 'б/р'
                        url = one_check.url
                        list_one_check[size] = url
                    else:
                        size = one_check.int_product
                        url = one_check.url
                        list_one_check[size] = url
                dict_for_mail[mail] = list_one_check
                clear_table_mail(dict=dict_for_mail)
                print(dict_for_mail)
            return dict_for_mail


def clear_table_mail(dict):
    app = create_app()
    with app.app_context():
        for mail, list in dict.items():
            Product_all_check.query.filter_by(email=mail).delete()
            db.session.commit()


def reset_pass_mail(e_mail, url):
    app = create_app()
    mail = Mail(app)
    with app.app_context():
        msg = Message("Перейдите по ссылке для смены вашего пароля", sender="zhogolevpv@gmail.com",
                      recipients=[e_mail])
        msg.body = render_template('email/reset_mail.txt', url=url)
        msg.html = render_template('email/reset_mail.html', url=url)
        mail.send(msg)
        print("__________Сообщение отправлено____________")


if __name__ == "__main__":
    email()
