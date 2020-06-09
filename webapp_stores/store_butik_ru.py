import requests
from webapp_stores import standard_icon, save_data_store
from bs4 import BeautifulSoup


class Butik_ru():

    def __init__(self, url='https://www.butik.ru'):
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
            store_name = 'Butik.ru'
            link = soup.find('link', rel="icon", type="image/png")
            store_icon = self.url + (link['href'])
            store_online = True
            store_url = self.url
            save_data_store.save_data(store_title=store_title, store_online=store_online, store_url=store_url,
                                      store_name=store_name, store_icon=store_icon)
        else:
            store_online = False
            store_url = self.url
            store_name = 'Butik.ru'
            store_title = 'Магазин временно недоступен'
            store_icon = standard_icon.standard_icon()
            save_data_store.save_data(store_title=store_title, store_online=store_online, store_url=store_url,
                                      store_name=store_name, store_icon=store_icon)


if __name__ == '__main__':
    c = Butik_ru()
    print(c.get_butik_ru())
