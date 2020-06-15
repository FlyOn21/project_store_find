import requests as req
from bs4 import BeautifulSoup
import ast
from webapp_stores.save_data_store import save_data_product_randevouz


def get_html(url):
    try:
        result = req.get(url)
        result.raise_for_status()
        return result.text
    except(req.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


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
        # print(pages)
        for pa in range(1, pages + 1):
            final_link = category + 'page/' + str(pa) + '/'
            randevuze_product_collection(final_link)
            print(final_link)



def dict_cliner(product_info_all):
    try:
        if 'dimension5' in product_info_all:
            del product_info_all['dimension5']
        if 'position' in product_info_all:
            del product_info_all['position']
        product_category = product_info_all['category']
        product_category_clear = ((product_category).split('/'))[0]
        product_info_all['category'] = product_category_clear
        product_info_all['size'] = None
        product_info_all['store'] = 'Рандеву'
        return product_info_all
    except(KeyError):
        return product_info_all


def randevuze_product_collection(final_link):
    html = get_html(url=final_link)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        product_all = soup.find('ul', class_="list-items list-items-catalog list-view-1 js-list-items").\
            find_all('li', class_="item")
        for product in product_all:
            try:
                product_info_all = ast.literal_eval(product['data-productinfo'])
                product_info = dict_cliner(product_info_all)
                product_url = 'https://www.rendez-vous.ru/' + product.find('a')['href']
                product_info['product_url'] = product_url
                product_image = ((product.find('div', class_="item-image").find('img')['data-srcset']).split(','))[1]
                product_info['product_image'] = product_image
                product_discount = ('').join((product.find('span', class_="item-price-value").get_text()).split())
                product_info['product_discount'] = product_discount
                save_data_product_randevouz(product_info)
            except(KeyError, TypeError):
                continue


if __name__ == '__main__':
    get_full_randevu()
