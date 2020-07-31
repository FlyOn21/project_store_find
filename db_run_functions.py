from webapp_stores import create_app
from webapp_stores.stores.butik import get_full_butik, get_butik_product
from webapp_stores.stores.randevu import get_full_randevu, get_randevu_product
from webapp_stores.db_functions import save_data_product, \
    save_interesting_product


def add_to_products_url_butik(url):
    """
    Функция добавляет в базу данных Product товар Бутик.ру по ссылке
    """
    app = create_app()
    with app.app_context():
        dict = get_butik_product(url)
        save_data_product(dict)


def add_to_products_all_butik():
    """
    Функция добавляет в базу данных Product все товары Бутик.ру
    """
    app = create_app()
    with app.app_context():
        get_full_butik()


def add_to_products_url_randevu(url):
    """
    Функция добавляет в базу данных Product товар Рандеву по ссылке
    """
    app = create_app()
    with app.app_context():
        dict = get_randevu_product(url)
        save_data_product(dict)


def add_to_products_all_randevu():
    """
    Функция добавляет в базу данных Product все товары Рандеву
    """
    app = create_app()
    with app.app_context():
        get_full_randevu()


def add_interesting_product(url, email=None, price_interesting=None, color_interesting=None,
                            size_interesting=None):
    """
    Функция сохраняет товар, интересный клиенту, в базу InterestingProduct
    """
    app = create_app()
    with app.app_context():
        dict = get_info(url)
        # print(dict)
        save_interesting_product(dict, email=email, price_interesting=price_interesting,
                                 color_interesting=color_interesting, size_interesting=size_interesting)
