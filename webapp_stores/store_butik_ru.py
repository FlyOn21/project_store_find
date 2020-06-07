import requests
import os
from bs4 import BeautifulSoup
from webapp_stores.model import db, Model_stores


class Butik_ru():

    def __init__(self, url='https://www.butik.ru/'):
        self.url = url

    def standard_icon(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        standard_icon_path =  basedir +'\\images\\'+'smile.png'
        return standard_icon_path

    def get_butik_ru(self):
        try:
            result = requests.get(self.url)
            result.raise_for_status()
            return result.text
        except(requests.RequestException, ValueError):
            return False

    def get_butik_data(self):
        html = self.get_butik_ru()
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            store_title = soup.title.string
            store_name = 'Butik.ru'
            link = soup.find('link', rel="icon", type="image/png")
            store_icon = self.url + (link['href']).strip('/')
            store_online = True
            store_url = self.url
            self.save_data(store_title=store_title, store_online=store_online, store_url=store_url,
                           store_name = store_name, store_icon = store_icon )
        else:
            store_online = False
            store_url = self.url
            store_name = 'Butik.ru'
            store_title = 'Магазин временно недоступен'
            store_icon = self.standard_icon()
            self.save_data(store_title=store_title, store_online=store_online, store_url=store_url,
                           store_name = store_name,store_icon = store_icon)

    def save_data(self, store_title, store_online, store_url,store_name,store_icon):
        if Model_stores.query.filter(Model_stores.store_url == store_url,
                                          Model_stores.store_name == store_name).count():
            Model_stores.query.filter(Model_stores.store_online != store_online).update({'store_online': store_online })
            Model_stores.query.filter(Model_stores.store_title != store_title).update({'store_title': store_title})
            Model_stores.query.filter(Model_stores.store_icon != store_icon ).update({'store_icon': store_icon})
            db.session.commit()
        else:
            base_update = Model_stores(store_title=store_title, store_online=store_online, store_url=store_url,
                                       store_name = store_name, store_icon = store_icon)
            db.session.add(base_update)
            db.session.commit()


if __name__ == '__main__':
    c = Butik_ru()
    print(c.standard_icon())
