import requests as req
from bs4 import BeautifulSoup
import ast
import re


def page_namber_url(url_page = 'https://www.rendez-vous.ru/catalog/page/1/'):
    request_page = valid_url(url=url_page)
    if request_page != False:
        request_page.raise_for_status()
        text_html =  request_page.text
        while True:
            page_query = randevuze_product_collection(html=text_html)
            print(url_page)
            print(page_query)
            page_numder = re.findall('\d', url_page)
            number = ''.join(page_numder)
            new_page = int (number)+1
            page_namber_url(url_page = f'https://www.rendez-vous.ru/catalog/page/{new_page}/')
    else:
        print('Оброботка товаров сайта Рандеву окончена')



def valid_url(url):
    try:
        request = req.get(url)
        if request:
            return request
        else:
            print(request)
            return False
    except(req.RequestException,ValueError):
        return False


def randevuze_product_collection(html):
    soup = BeautifulSoup(html,'html.parser')
    list_product = []
    product_all = soup.find('ul' ,class_="list-items").find_all('li', class_="item")
    # print(product_all)
    for product in product_all:
        print("--------------------------------------------")
        print(product)
        print("--------------------------------------------")
        product_1 = product.find('li')['data-productinfo']
        print(product_1)
        list_product.append(product_1)
    return list_product






if __name__ == '__main__':
    page_namber_url()