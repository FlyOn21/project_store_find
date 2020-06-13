from bs4 import BeautifulSoup
import pandas as pd
from pprint import PrettyPrinter  # красиво выводит результат из словарей и списков
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

        # pp = PrettyPrinter(indent=2)
        # pp.pprint(soup)

        df = pd.read_csv('randevu_all_items.csv', sep=',', encoding="utf-8")
        products = soup.find('ul', id='list-items').find_all('li', class_='item')
        for product in products:
            try:
                link = 'https://www.rendez-vous.ru' + product.find('a', class_='item-link')['href']
                if not link in df['Link'].values:
                    df = df.append({'Link': link}, ignore_index=True)
            except:
                pass
        df['Link'].to_csv(os.path.join(os.path.dirname(__file__), "randevu_all_items.csv"))


# Высчитывает количество страниц в категории
def pages_in_category(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        number_of_pages = int(soup.find('ul', class_='pagination').find_all('li', class_='page')[-1].get_text())

        return number_of_pages


# Парсит линки всех товаров все товары
def get_full_randevu():
    full_randevu = ['https://www.rendez-vous.ru/catalog/female/',
                    'https://www.rendez-vous.ru/catalog/bags_female/',
                    'https://www.rendez-vous.ru/catalog/zhenskaya_odezhda/',
                    'https://www.rendez-vous.ru/catalog/accessories_female/',
                    'https://www.rendez-vous.ru/catalog/tools/',
                    'https://www.rendez-vous.ru/catalog/male/',
                    'https://www.rendez-vous.ru/catalog/bags_male/',
                    'https://www.rendez-vous.ru/catalog/muzhskaya_odezhda/',
                    'https://www.rendez-vous.ru/catalog/accessories_male/',
                    'https://www.rendez-vous.ru/catalog/tools/',
                    'https://www.rendez-vous.ru/catalog/girls/',
                    'https://www.rendez-vous.ru/catalog/boys/']

    for category in full_randevu:
        pages = pages_in_category(category)
        for p in range(1, pages + 1):
            final_link = category + 'page/' + str(p) + '/'
            get_items(final_link)
            print(final_link)


if __name__ == '__main__':
    get_full_randevu()
