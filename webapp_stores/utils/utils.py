from urllib.parse import urlparse, urljoin
from flask import request
from webapp_stores.stores.butik import get_butik_product
from webapp_stores.stores.randevu import get_randevu_product
from webapp_stores.stores.ali import Aliexpress

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

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