import ast
from bs4 import BeautifulSoup
import pandas as pd
import os
from pprint import PrettyPrinter  # красиво выводит результат из словарей и списков
import requests


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_items(url):
    """
    Функция получает все ссылки товары со страницы url (список urls органичен и
    указан в get_full_butik) и сохраняет их в csv файл
    """
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        # pp = PrettyPrinter(indent=2)
        # pp.pprint(soup)

        df = pd.read_csv('data/randevu_all_items.csv', sep=',', encoding="utf-8")
        products = soup.find('ul', id='list-items').find_all('li', class_='item')
        for product in products:
            try:
                link = 'https://www.rendez-vous.ru' + product.find('a', class_='item-link')['href']
                if not link in df['Link'].values:
                    df = df.append({'Link': link}, ignore_index=True)
            except:
                pass
        df['Link'].to_csv(os.path.join(os.path.dirname(__file__), "data/randevu_all_items.csv"))


def pages_in_category(url):
    """
    Функция высчитывает количество страниц в категории (список urls органичен и
    указан в get_full_butik)
    """
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        number_of_pages = int(soup.find('ul', class_='pagination').find_all('li', class_='page')[-1].get_text())

        return number_of_pages


# Парсинг всех ссылок на товары
def get_full_randevu():
    """
    Функция запускает функции : pages_in_category и  get_items (иными словами, парсит ссылки на все товары магазина Рандеву.ру)
    Список urls точно определен.
    """
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


# Парсинг данных об одном товаре по ссылке на него
def get_randevu_product(url):
    """
    Функция парсит данные о товаре (url) в словарь.
    """
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        pp=PrettyPrinter(indent=2)
        # pp.pprint(soup)

        # if product is available
        try:
            url_store = url
            image = soup.find('div', class_='item-info').find('div', class_='carousel-image-list').find('img')[
                'data-src']

            # code =  \
            # ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
            #    'name']

            code = soup.find('section', id='catalog-item')['data-model']

            # price = float(ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
            #     'priceFromCart'])
            price = float(soup.find('span', class_='item-price-value')['content'])

            brand = ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                'brand']
            color = ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                'variant']
            category_detailed = \
                ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                    'category'].split(
                    '/')[0]
            category = soup.find('div', class_='breadcrumbs').find_all('li')[1].find('a').text

            # sizes
            try:
                sizes = soup.find('ul', class_='form-select-list scrollbar scrollbar-y').find_all('li')
                sizes_available = []
                for size in sizes:
                    sizes_available.append(size.text.strip())
            except:
                sizes_available = ['one-size']

            dict = {'code': code, 'price': price, 'brand': brand, 'color': color,
                    'category_detailed': category_detailed, 'category': category, 'image': image,
                    'sizes': sizes_available, 'url': url_store}

        # if the product is not available in the store
        except:
            dict = {}

        return dict


# if __name__ == '__main__':
# get_full_randevu()

