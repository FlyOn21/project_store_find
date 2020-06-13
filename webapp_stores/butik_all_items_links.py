from bs4 import BeautifulSoup
import math
import pandas as pd
from pprint import PrettyPrinter  # красиво выводит результат из словарей и списков
import re
import requests
import os


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


# Получает все ссылки на товары со страницы
def get_items(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        #pp = PrettyPrinter(indent=2)
        # pp.pprint(soup)

        df = pd.read_csv('butik_all_items.csv', sep=',', encoding="utf-8")
        products = soup.find('div', id='catalog-top').find_all('a', {'data-test': "product-link"})
        for product in products:
            link = 'https://www.butik.ru' + product['href']
            if not link in df['Link'].values:
                df = df.append({'Link': link}, ignore_index=True)
        df['Link'].to_csv(os.path.join(os.path.dirname(__file__), "butik_all_items.csv"))


# Высчитывает количество страниц в категории
def pages_in_category(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        number_of_products = soup.find('div', id='catalog-top').find_all('span', class_='fg-black-10 font-small')[
            0].get_text()
        number_of_products = int(re.findall('\d+', number_of_products)[0])
        number_of_pages = math.ceil(number_of_products / 100)

        return number_of_pages

# Парсит линки всех товаров все товары
def get_full_butik():
    full_butik = ['https://www.butik.ru/catalog/zhenshchinam/odezhda/',
                  'https://www.butik.ru/catalog/zhenshchinam/sumki/',
                  'https://www.butik.ru/catalog/zhenshchinam/obuv/',
                  'https://www.butik.ru/catalog/zhenshchinam/aksessuary/',
                  'https://www.butik.ru/catalog/muzhchinam/odezhda/',
                  'https://www.butik.ru/catalog/muzhchinam/sumki/',
                  'https://www.butik.ru/catalog/muzhchinam/obuv/',
                  'https://www.butik.ru/catalog/muzhchinam/aksessuary/']

    for category in full_butik:
        pages=pages_in_category(category)
        for p in range(1,pages+1):
            final_link=category+'?page='+str(p)+'&per_page=100'
            get_items(final_link)
            print(final_link)


if __name__ == '__main__':
    get_full_butik()

