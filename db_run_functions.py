from webapp_stores import create_app
from webapp_stores.stores.ali import Aliexpress
from webapp_stores.stores.butik import get_full_butik, get_butik_product
from webapp_stores.stores.randevu import get_full_randevu, get_randevu_product
from webapp_stores.stores.stores import get_ali_data, get_butik_data, get_randevu_data
from webapp_stores.db_functions import save_data_product, \
    save_interesting_product, delete_interesting_product,find_product, hello_user
# from webapp_stores.utils import get_info
# from webapp_stores.check.check_product import check_product



from webapp_stores.user.model import InterestingProduct


# def run():
#     app = create_app()
#     with app.app_context():
# ali_status = get_ali_data()
# randezvous_status = get_randevu_data()
# butik_status = get_butik_data()


# if randezvous_status is not False:
#     get_full_randevu()
#     # save_data_product(get_full_randevu())
# else:
#     print('Рандеву был недоступен, обновление базы не выполнено')
#     pass
#
# if butik_status is not False:
#     get_full_butik()
#     # save_data_product(get_full_butik())
# else:
#     print('Бутик был недоступен, обновление базы не выполнено')
#     pass

# if ali_status is not False:
#     ali = Aliexpress()
#     ali.page_ali()
# else:
#     print('Алиекспрес был недоступен, обновление базы не выполнено')
#     pass

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


# def insteresting_product_check():
#     """
#     Функция проверяет наличие товров для клиента (база InterestingProduct) и отрпавляет уведомление
#     """
#     app = create_app()
#     with app.app_context():
#         all_interesting_products = create_dict_interesting_products()
#         for id, url in all_interesting_products.items():
#             all_interesting_products[id] = get_info(url)
#         for id, info in all_interesting_products.items():
#             check_product(info, id)  # нужно добавить в данную функцию отправления сообщения на почту в данной функции


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


# if __name__ == '__main__':
# c = run()
# insteresting_product_check()
# add_to_products_all_butik()
# add_to_products_url_butik() # put url in brackets
#     add_to_products_all_randevu()
#     add_to_products_url_randevu('https://www.rendez-vous.ru/catalog/male/shlepantsy/officine_creative_sand040_temno_korichnevyy-2469115/') # put url in brackets
# add_interesting_product('https://www.rendez-vous.ru/catalog/female/shlepantsy/calvin_klein_jaimee_zheltyy-2274485/', email='nat1@example.com',size_interesting='37')
# ali='https://aliexpress.ru/item/4001040161418.html?spm=a2g0s.8937460.0.0.559e2e0eXwHzO1&_ga=2.10782772.1228535348.1593582717-1461091439.1591961209'
# add_interesting_product(ali, email='da@example.com',size_interesting='50')


# app = create_app()
# with app.app_context():
#







