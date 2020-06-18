import requests
from webapp_stores import standard_icon, db_functions
from bs4 import BeautifulSoup


class Aliexpress():

    def __init__(self, url='https://aliexpress.ru/'):
        self.url = url

    def get_aliexpress(self):
        try:
            result = requests.get(self.url)
            result.raise_for_status()
            return result.text
        except(requests.RequestException, ValueError):
            return False

    def get_butik_data(self):
        html = self.get_aliexpress()
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            store_title = soup.title.string
            store_name = 'Aliexpress'
            store_icon = soup.find('meta', property="og:image", )['content']
            store_online = True
            store_url = self.url
            db_functions.save_data(store_title=store_title, store_online=store_online, store_url=store_url,
                                   store_name=store_name, store_icon=store_icon)
        else:
            store_online = False
            store_url = self.url
            store_name = 'Aliexpress'
            store_title = 'Магазин временно недоступен'
            store_icon = standard_icon.standard_icon()
            db_functions.save_data(store_title=store_title, store_online=store_online, store_url=store_url,
                                   store_name=store_name, store_icon=store_icon)


if __name__ == '__main__':
    c = Aliexpress()
    print(c.get_aliexpress())
