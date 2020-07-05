import ast
from bs4 import BeautifulSoup
from pprint import PrettyPrinter  # красиво выводит результат из словарей и списков
import requests
from webapp_stores.db_functions import save_data_product


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

        products = soup.find('ul', id='list-items').find_all('li', class_='item')
        links = []
        for product in products:
            try:
                link = 'https://www.rendez-vous.ru' + product.find('a', class_='item-link')['href']
                links.append(link)
            except:
                pass

        return links


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
        # links=[]
        for p in range(1, pages + 1):
            final_link = category + 'page/' + str(p) + '/'
            print('\nCategory :' + final_link + ' ' + str(p) + '/' + str(pages))
            links = get_items(final_link)
            for link in links:
                try:
                    dict = get_randevu_product(link)
                    save_data_product(dict)
                except:
                    print('I cant get data from ' + link)


# Парсинг данных об одном товаре по ссылке на него
def get_randevu_product(url):
    """
    Функция парсит данные о товаре (url) в словарь.
    """
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        pp = PrettyPrinter(indent=2)
        #pp.pprint(soup)


        # if product is available
        store = 'Randevu'
        url_store = url
        image = soup.find('div', class_='item-info').find('div', class_='carousel-image-list').find('img')[
            'data-src']

        name= ast.literal_eval(soup.find('div', class_='item-checkout').find('button')['data-productinfo'])['name']
        id = soup.find('section', id='catalog-item')['data-model']

        price = float(
            ast.literal_eval(soup.find('div', class_='item-checkout').find('button')['data-productinfo'])['price']) if \
            ast.literal_eval(soup.find('div', class_='item-checkout').find('button')['data-productinfo'])[
                'price'] else None
        discount = float(ast.literal_eval(soup.find('div', class_='item-checkout').find('button')['data-productinfo'])['priceFromCart']) if 'priceFromCart' in ast.literal_eval(soup.find('div', class_='item-checkout').find('button')['data-productinfo']) else None
        if discount==None:
            discount=price

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

        # gender = 'Мужское' if 'muzhchinam/' in url else 'Женское'
        if 'female' in url:
            gender = 'Женское'
        elif 'girls' in url:
            gender = 'Девочки'
        elif 'boys' in url:
            gender = 'Мальчики'
        else:
            gender = 'Мужское'

        dict = {'id': id, 'name': name, 'price': price, 'product_discount': discount, 'brand': brand, 'color': color,
                'category_detailed': category_detailed, 'category': category, 'product_image': image,
                'size': sizes_available, 'product_url': url_store, 'gender': gender, 'product_store': store}
        # print(dict)

        return dict

if __name__ == '__main__':
    c = get_full_randevu()
    print(c)
