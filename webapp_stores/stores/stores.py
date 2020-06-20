import requests as req
from webapp_stores import standard_icon, db_functions
from bs4 import BeautifulSoup

import json

class Butik_ru():

    def __init__(self):
        self.url = 'https://www.butik.ru'
        self.full_butik_man = ['https://www.butik.ru/catalog/zhenshchinam/obuv/',
                      'https://www.butik.ru/catalog/zhenshchinam/sumki/',
                      'https://www.butik.ru/catalog/zhenshchinam/odezhda/',
                      'https://www.butik.ru/catalog/zhenshchinam/aksessuary/']
        self.full_butik_woman = ['https://www.butik.ru/new/muzhchinam/odezhda/',
                        'https://www.butik.ru/new/muzhchinam/sumki/',
                        'https://www.butik.ru/new/muzhchinam/obuv/',
                        'https://www.butik.ru/new/muzhchinam/aksessuary/']

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
        self.full_randevu_man = ['https://www.rendez-vous.ru/catalog/male/',
                                 'https://www.rendez-vous.ru/catalog/bags_male/',
                                 'https://www.rendez-vous.ru/catalog/muzhskaya_odezhda/',
                                 'https://www.rendez-vous.ru/catalog/accessories_male/']
        self.full_randevu_women = ['https://www.rendez-vous.ru/catalog/female/',
                                   'https://www.rendez-vous.ru/catalog/bags_female/',
                                   'https://www.rendez-vous.ru/catalog/zhenskaya_odezhda/',
                                   'https://www.rendez-vous.ru/catalog/accessories_female/']
        self.full_randevu_chaildren = ['https://www.rendez-vous.ru/catalog/girls/',
                                       'https://www.rendez-vous.ru/catalog/boys/']
        self.full_randevu_unisex = ['https://www.rendez-vous.ru/catalog/tools/']

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