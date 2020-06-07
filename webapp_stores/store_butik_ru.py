import requests
from bs4 import BeautifulSoup
from webapp_stores.model import db, Model_stores


class Butik_ru():

    def __init__(self, url='https://www.butik.ru/'):
        self.url = url

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
            store_online = True
            store_url = self.url
            self.save_data(store_title=store_title, store_online=store_online, store_url=store_url)
        else:
            store_online = False
            store_url = self.url
            store_title = 'the store is not responding'
            self.save_data(store_title=store_title, store_online=store_online, store_url=store_url)

    def save_data(self, store_title, store_online, store_url):
        store =Model_stores.query.filter(Model_stores.store_url == store_url).count()
        if not store:
            base_update = Model_stores(store_title = store_title, store_online = store_online,store_url = store_url )
            db.session.add(base_update)
            db.session.commit()


if __name__ == '__main__':
    c = Butik_ru()
    print(c.get_butik_data())
