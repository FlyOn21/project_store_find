from webapp_stores.stores.model import db, Stores, Product
from webapp_stores.user.model import InterestingProduct, User
from webapp_stores.utils import get_info
from webapp_stores import create_app


def create_dict_interesting_products():
    """
    Функция создает словарь типа { id : url } для всех товаров, интересных клиентам
    """
    # Creation of dict = { id : url } for all interesting products
    dict_id_url = {}
    for i in InterestingProduct.query.all():
        dict_id_url[i.id] = i.url
    return dict_id_url

def insteresting_product_check():
    """
    Функция проверяет наличие товров для клиента (база InterestingProduct) и отрпавляет уведомление
    """
    app = create_app()
    with app.app_context():
        all_interesting_products = create_dict_interesting_products()
        for id, url in all_interesting_products.items():
            all_interesting_products[id] = get_info(url)
        for id, info in all_interesting_products.items():
            check_product(info, id)

def check_product(info, id):
    # print(info)
    """
    Функция проверяет наличие товара, необходимого клиенту, и, в случае наличия, отправляет уведомление клиенту по email
    """
    interesting_product = InterestingProduct.query.filter(InterestingProduct.id == id).first()

    # Updating info about available sizes
    if info:
        interesting_product.size_available = str(info['size'])
        db.session.add(interesting_product)
        db.session.commit()

    # Informing clients about availability of interesting product
    if interesting_product.client_id is not None:
        mail_on_off = User.query.filter_by(id=interesting_product.client_id).first()
        if mail_on_off.send_mail == True:
            check_send(interesting_product)
        else:
            print('Клиент отключил оповищение о найденых товарах')
            interesting_product.notification_sent = 1
            db.session.add(interesting_product)
            db.session.commit()
    else:
        check_send(interesting_product)


def check_send(interesting_product):
    if interesting_product.size_interesting in interesting_product.size_available:
        if interesting_product.notification_sent == 1:
            print(f'Уведомление клиенту {interesting_product.user_email} о товаре уже отправлено'
                  f' {interesting_product.url}')
        else:
            print(f'Для клиента {interesting_product.user_email} найден необходимый размер '
                  f'{interesting_product.size_interesting} товара: {interesting_product.url}')
            from tasks import email_send
            email_send.delay(e_mail=interesting_product.user_email, find_size=interesting_product.size_interesting,
                             product=interesting_product.url)
            # Вставить функцию для отправления сообщений на почту + удаление строки ввобще
            interesting_product.notification_sent = 1
            db.session.add(interesting_product)
            db.session.commit()