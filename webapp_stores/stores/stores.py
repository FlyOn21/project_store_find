import requests as req
from webapp_stores import standard_icon, db_functions
from bs4 import BeautifulSoup

import json

class Butik_ru():

    def __init__(self):
        self.url = 'https://www.butik.ru'


    def get_butik_data(self):
        html = self.get_html(url = self.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string
            name = 'Butik.ru'
            link = soup.find('link', rel="icon", type="image/png")
            icon = self.url + (link['href'])
            online = True
            url = self.url
            db_functions.save_data(title=title, online=online, url=url,
                                      name=name, icon=icon)
        else:
            online = False
            url = self.url
            name = 'Butik.ru'
            title = 'Магазин временно недоступен'
            icon = standard_icon.standard_icon()
            db_functions.save_data(title=title, online=online, url=url,
                                      name=name, icon=icon)

    def get_html(self, url):
        try:
            result = req.get(url)
            result.raise_for_status()
            return result.text
        except(req.RequestException, ValueError):
            print('Сетевая ошибка')
            return False


class Rendezvous():

    def __init__(self):
        self.url = 'https://www.rendez-vous.ru'


    def get_randevu_data(self):
        html = self.get_html(self.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string
            name = 'Rendezvous'
            icon = soup.find('meta', property="og:image", )['content']
            online = True
            url = self.url
            db_functions.save_data(title=title, online=online, url=url,
                                   name=name, icon=icon)

        else:
            online = False
            url = self.url
            name = 'Rendezvous'
            title = 'Магазин временно недоступен'
            icon = standard_icon.standard_icon()
            db_functions.save_data(title=title, online=online, url=url,
                                   name=name, icon=icon)

    def get_html(self, url):
        try:
            result = req.get(url)
            result.raise_for_status()
            return result.text
        except(req.RequestException, ValueError):
            print('Сетевая ошибка')
            return False