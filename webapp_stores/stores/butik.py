from bs4 import BeautifulSoup
import json
import math
from pprint import PrettyPrinter  # красиво выводит результат из словарей и списков
import re
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
    указан в get_full_butik)
    """
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        # pp = PrettyPrinter(indent=2)
        # pp.pprint(soup)

        products = soup.find('div', id='catalog-top').find_all('a', {'data-test': "product-link"})
        links=[]
        for product in products:
            link = 'https://www.butik.ru' + product['href']
            links.append(link)

        return links


def pages_in_category(url):
    """
    Функция высчитывает количество страниц в категории (список urls органичен и
    указан в get_full_butik)
    """
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        number_of_products = soup.find('div', id='catalog-top').find_all('span', class_='fg-black-10 font-small')[
            0].get_text()
        number_of_products = int(re.findall('\d+', number_of_products)[0])
        number_of_pages = math.ceil(number_of_products / 100)

        return number_of_pages


# Парсинг всех товаров и занесение в базу данных
def get_full_butik():
    """
    Функция запускает функции : pages_in_category и  get_items (иными словами, парсит ссылки на все товары магазина Бутик.ру)
    Список urls точно определен.
    """

    full_butik = [#'https://www.butik.ru/catalog/zhenshchinam/odezhda/',
                  'https://www.butik.ru/catalog/zhenshchinam/sumki/',
                  'https://www.butik.ru/catalog/zhenshchinam/obuv/',
                  'https://www.butik.ru/catalog/zhenshchinam/aksessuary/',
                  'https://www.butik.ru/catalog/muzhchinam/odezhda/',
                  'https://www.butik.ru/catalog/muzhchinam/sumki/',
                  'https://www.butik.ru/catalog/muzhchinam/obuv/',
                  'https://www.butik.ru/catalog/muzhchinam/aksessuary/']


    for category in full_butik:
        pages = pages_in_category(category)
        for p in range(1, pages + 1):
            final_link=category+'?page='+str(p)+'&per_page=100'
            print('\nCategory :' + final_link + ' ' +str(p) + '/' + str(pages))
            links=get_items(final_link)
            for link in links:
                try:
                    dict = get_butik_product(link)
                    save_data_product(dict)
                    print(f" !!!!!!!!!!!!!!!!!!Сохранено {link}")
                except:
                    print('I cant get data from '+link)




# Парсинг данных об одном товаре по ссылке на него
def get_butik_product(url):
    """
    Функция парсит данные о товаре (url) в словарь.
    """
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

    raw_data = soup.find_all('script')[-1].contents[0]
    raw_data = str(raw_data).replace('    window.__DATA__ = ', '')

    replace = '''window.globalUtils = {}
    try {
      window.globalUtils.show_sale = window.__DATA__.data.showSale[0].value.value.show_sale
    }
    catch(e) {
      window.globalUtils.show_sale = null
      console.error(e.message)
    }'''
    raw_data = raw_data.replace(replace, '').strip()

    data = json.loads(raw_data)
    pp = PrettyPrinter(indent=2)
    #pp.pprint(data)

    store = 'Butik.ru'
    name = data['data']['card'][0]['value']['value']['seo_name']
    price = float(data['data']['card'][0]['value']['value']['price'])
    discount = float(data['data']['card'][0]['value']['value']['price_with_discount'])
    color = data['data']['card'][0]['value']['value']['color']
    brand = data['data']['card'][0]['value']['value']['brand']['name']
    category_detailed = data['data']['card'][0]['value']['value']['name']
    category = data['data']['card'][0]['value']['value']['breadcrumbs']['full_ru_array'][0]['text'] + ' ' + \
               data['data']['card'][0]['value']['value']['breadcrumbs']['full_ru_array'][1]['text']
    # code = data['data']['card'][0]['value']['value']['sku']
    id = data['data']['card'][0]['value']['value']['sku_article']
    image = soup.find('div', class_='card-sticky').find('img')['src']
    # image = data['seoData']['ogImage']
    url_store = url


    #sizes_available
    main_criteria = data['data']['card'][0]['value']['value']['product_variations'][0]['size']['main_size']
    product_variations = data['data']['card'][0]['value']['value']['product_variations']
    sizes_available = [str(i['size'][main_criteria]).replace('[', '').replace(']', '').replace("'", '') for i in product_variations if i['size'][
            'stock_with_reserve']]

    # sizes_possible
    sizes_possible = [str(i['size'][main_criteria]).replace('[', '').replace(']', '').replace("'", '') for i in
                       product_variations]

    gender = 'Мужское' if 'muzhchinam/' in url else 'Женское'
    dict = {'name':name, 'id': id, 'price': price, 'product_discount' : discount,'brand': brand, 'color': color,
            'category_detailed': category_detailed, 'category': category, 'product_image': image,
            'size': sizes_available,'size_possible':sizes_possible,'gender':gender ,'product_url': url_store, 'product_store':store}


    return dict

