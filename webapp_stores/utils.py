from webapp_stores.stores.butik import get_butik_product
from webapp_stores.stores.randevu import get_randevu_product
from webapp_stores.stores.ali import Aliexpress


def get_info(i):
    """
    Функция принимает ссылку на товар из 3 магазинов (Butik, Ali, Randevu) и возвращает словарь с данными о товаре
    """
    if 'butik' in i:
        info = get_butik_product(i)  # dictionary with info about product
    elif 'rendez-vous' in i:
        info = get_randevu_product(i)  # dictionary with info about product
    elif 'aliexpress' in i:
        al = Aliexpress()
        info = al.parser_product_result(i)
    return info

