from webapp_stores import db_functions
from webapp_stores.images import standard_icon
from bs4 import BeautifulSoup
from webapp_stores.proxy.get_query import get_html_all
import requests


# def get_html(url):
#     try:
#         result = requests.get(url)
#         result.raise_for_status()
#         return result.text
#     except(requests.RequestException, ValueError):
#         print('Сетевая ошибка')
#         return False

# Butik

def get_butik_data(url='https://www.butik.ru'):
    html = get_html_all(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string
        name = 'Butik.ru'
        link = soup.find('link', rel="icon", type="image/png")
        icon = url + (link['href'])
        online = True
        url = url
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)
    else:
        online = False
        url = url
        name = 'Butik.ru'
        title = 'Магазин временно недоступен'
        icon = standard_icon.standard_icon()
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)
        return False


# Randevu

def get_randevu_data(url='https://www.rendez-vous.ru'):
    html = get_html_all(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string
        name = 'Rendezvous'
        icon = soup.find('meta', property="og:image", )['content']
        online = True
        url = url
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)


    else:
        online = False
        url = url
        name = 'Rendezvous'
        title = 'Магазин временно недоступен'
        icon = standard_icon.standard_icon()
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)
        return False


# Aliexpress

def get_ali_data(url = 'https://aliexpress.ru/'):
    html = get_html_all(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string
        name = 'Aliexpress'
        icon = soup.find('meta', property="og:image")['content']
        online = True
        url = url
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)
    else:
        online = False
        url = url
        name = 'Aliexpress'
        title = 'Магазин временно недоступен'
        icon = standard_icon.standard_icon()
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)
        return False
