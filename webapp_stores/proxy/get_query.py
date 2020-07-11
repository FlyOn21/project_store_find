import requests as req
from requests.exceptions import Timeout
import random
import time

#/home/pasha/PycharmProjects/project_store_find/

def open_proxy_list():
    with open(r'webapp_stores/proxy/proxy.txt', 'r',
              encoding='utf-8') as file:
        m = [lins.strip() for lins in file]
        f = [clear_line for clear_line in m if clear_line != '']
        return f


def get_html_all(url):
    # proxy = {'https':'185.171.24.244:808'}
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
    proxys = open_proxy_list()
    proxy_d = random.choice(proxys)
    proxy = {'http': f'{proxy_d}'}
    print(proxy)
    try:
        result = req.get(url,proxies=proxy,headers = headers)  # proxies=proxy,proxies=proxy,timeout = 20
        result.encoding = 'utf-8'
        result.raise_for_status()
        return result.text
    except(req.exceptions.ProxyError):
        time.sleep(5)
        get_html_all(url)
    except(req.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
