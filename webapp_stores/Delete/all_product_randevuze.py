import requests as req
from bs4 import BeautifulSoup
import ast
import time
from webapp_stores.db_functions import save_data_product


full_randevu_man = ['https://www.rendez-vous.ru/catalog/male/',
                    'https://www.rendez-vous.ru/catalog/bags_male/',
                    'https://www.rendez-vous.ru/catalog/muzhskaya_odezhda/',
                    'https://www.rendez-vous.ru/catalog/accessories_male/']
full_randevu_women = ['https://www.rendez-vous.ru/catalog/female/',
                    'https://www.rendez-vous.ru/catalog/bags_female/',
                    'https://www.rendez-vous.ru/catalog/zhenskaya_odezhda/',
                    'https://www.rendez-vous.ru/catalog/accessories_female/']
full_randevu_chaildren = ['https://www.rendez-vous.ru/catalog/girls/',
                    'https://www.rendez-vous.ru/catalog/boys/']
full_randevu_unisex = ['https://www.rendez-vous.ru/catalog/tools/']



def get_html(url):
    try:
        result = req.get(url)
        result.raise_for_status()
        return result.text
    except(req.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_store_randevu(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            url_store = url
            image = soup.find('div', class_='item-info').find('div', class_='carousel-image-list').find('img')[
                'data-src']

            code =  \
            ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                'name']

            # price = ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
            #     'priceFromCart']

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

            dict = {'code': code, 'brand': brand, 'color': color,
                    'category_detailed': category_detailed, 'category': category, 'image': image,
                    'sizes': sizes_available, 'url': url_store}
            # print(dict)
            return dict

          # if the product is not available in the store
        except:
            # what should we do?
            print('Товар не доступен')


def pages_in_category(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        number_of_pages = int(soup.find('ul', class_='pagination').find_all('li', class_='page')[-1].get_text())
        return number_of_pages


# Парсит линки всех товаров все товары
def get_full_randevu(full_randevu_man,full_randevu_women,full_randevu_chaildren,full_randevu_unisex):
    full_randevu = full_randevu_man + full_randevu_women + full_randevu_chaildren+full_randevu_unisex
    for category in full_randevu:
        pages = pages_in_category(url = category)
        # print(pages)
        for pa in range(1, pages + 1):
            final_link = category + 'page/' + str(pa) + '/'
            randevuze_product_collection(final_link)
            print(final_link)

def prod_url(product):
    url = 'https://www.rendez-vous.ru/' + product.find('a')['href']
    return url

def prod_category(product_randevoyz_all):
    product_category = product_randevoyz_all['category']
    product_category_clear = ((product_category).split('/'))[0]
    return product_category_clear

def prod_discount(product):
    product_discount = str(('').join((product.find('span', class_="item-price-value").get_text()).split()))
    return product_discount

def prod_store():
    return 'Рандеву'

def product_name(product):
    name =((product.find('div', class_="item-name")).text).strip()
    return name



def dict_cliner(product_randevoyz_all):
    try:
        if 'dimension5' in product_randevoyz_all:
            del product_randevoyz_all['dimension5']
        if 'position' in product_randevoyz_all:
            del product_randevoyz_all['position']
        if 'variant' in  product_randevoyz_all:
            del product_randevoyz_all['variant']
        return product_randevoyz_all
    except(KeyError):
        return product_randevoyz_all

def product_gender(final_link):
    category = final_link.split('page/')
    if category[0] in full_randevu_man:
        return 'Man'
    elif category[0] in full_randevu_women:
        return 'Woman'
    elif category[0] in full_randevu_chaildren:
        return 'Children'
    else:
        return 'Unisex'


def randevuze_product_collection(final_link):
    html = get_html(url=final_link)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        product_all = soup.find('ul', class_="list-items list-items-catalog list-view-1 js-list-items").\
            find_all('li', class_="item")
        for product in product_all:
            # print(product)
            try:
                product_randevoyz_all = ast.literal_eval(product['data-productinfo'])
                product_randevoyz = dict_cliner(product_randevoyz_all)
                product_url = prod_url(product)
                product_randevoyz['category'] = prod_category(product_randevoyz_all)
                current_product = get_store_randevu(url = product_url)
                product_randevoyz['name'] = product_name(product)
                # print(current_product)
                product_randevoyz['product_store'] = prod_store()
                product_randevoyz['color'] = current_product['color']
                product_randevoyz['category'] = current_product['category']
                product_randevoyz['category_detailed'] = current_product['category_detailed']
                product_randevoyz['product_url'] = product_url
                product_randevoyz['size'] = str(current_product['sizes'])
                product_randevoyz['product_image'] = current_product['image']
                product_randevoyz['product_discount'] = prod_discount(product)
                product_randevoyz['gender'] = product_gender(final_link)
                print(product_randevoyz)
                time.sleep(3.0)
                save_data_product(product_randevoyz)
            except(KeyError, TypeError):
                continue


if __name__ == '__main__':
    get_full_randevu(full_randevu_man,full_randevu_women,full_randevu_chaildren,full_randevu_unisex)
