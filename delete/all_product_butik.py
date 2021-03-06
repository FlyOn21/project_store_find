import requests as req
from bs4 import BeautifulSoup
import json
from webapp_stores.db_functions import save_data_product_butik

full_butik_man = ['https://www.butik.ru/catalog/zhenshchinam/obuv/',
                  'https://www.butik.ru/catalog/zhenshchinam/sumki/',
                  'https://www.butik.ru/catalog/zhenshchinam/odezhda/',
                  'https://www.butik.ru/catalog/zhenshchinam/aksessuary/']
full_butik_women = ['https://www.butik.ru/new/muzhchinam/odezhda/',
                    'https://www.butik.ru/new/muzhchinam/sumki/',
                    'https://www.butik.ru/new/muzhchinam/obuv/',
                    'https://www.butik.ru/new/muzhchinam/aksessuary/']


def get_html(url):
    try:
        result = req.get(url)
        result.raise_for_status()
        return result.text
    except(req.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_parser_url(url_product):
    html = get_html(url_product)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        raw_data = soup.find_all('script')[-1].contents[0]
        data = preparation_json(raw_data)

        price = data['data']['card'][0]['value']['value']['price_with_discount']
        color = data['data']['card'][0]['value']['value']['color']
        brand = data['data']['card'][0]['value']['value']['brand']['name']
        category_detailed = data['data']['card'][0]['value']['value']['name']
        category = data['data']['card'][0]['value']['value']['breadcrumbs']['full_ru_array'][0]['text'] + ' ' + \
                   data['data']['card'][0]['value']['value']['breadcrumbs']['full_ru_array'][1]['text']
        code = data['data']['card'][0]['value']['value']['sku']
        image = data['seoData']['ogImage']
        url_store = url_product
        sizes_available = [i['size']['brand_size'] for i in
                           data['data']['card'][0]['value']['value']['product_variations'] if
                           i['size']['stock_with_reserve']]

        dict = {'code': code, 'price': price, 'brand': brand, 'color': color,
                'category_detailed': category_detailed, 'category': category, 'image': image,
                'sizes': sizes_available, 'url': url_store}
        return dict


def page_number_url(full_butik_man, full_butik_women):
    full_randevu = full_butik_man + full_butik_women
    for category in full_randevu:
        request_page = valid_url(url=category)
        p = 1
        while request_page == True:
            final_link = category + '?page=' + str(p) + '&per_page=100'
            request_page = valid_url(url=final_link)
            query = butik_product_collection(final_link)
            if query == False:
                request_page = False
            p += 1
            print(final_link)
        else:
            print(f'Оброботка категории {category} сайта Рандеву окончена')


def valid_url(url):
    try:
        request = req.get(url)
        if request:
            return True
        else:
            return False
    except(req.RequestException, ValueError):
        return False


def preparation_json(raw_data):
    raw_data = str(raw_data).replace('    window.__DATA__ = ', '')

    replace = '''
    
    window.globalUtils = {}
    try {
      window.globalUtils.show_sale = window.__DATA__.data.showSale[0].value.value.show_sale
    }
    catch(e) {
      window.globalUtils.show_sale = null
      console.error(e.message)
    }'''
    raw_data = raw_data.replace(replace, '').strip()

    data = json.loads(raw_data)
    return data


def product_name(item):
    return item['seo_name']


def product_prise_full(item):
    return str(item['price'])


def product_prise_discount(item):
    return str(item['price_with_discount'])


def product_brand(item):
    return item['brand_name']


def product_category(item):
    return item['seo_name']


def product_size(item):
    size_dict = {}
    for size in item['product_variations']:
        size_current = size['size']['brand_size']
        quantity = size['size']['stock_online']
        size_dict[size_current] = quantity
    return size_dict


def product_url(item):
    url = 'https://www.butik.ru/' + item['url_name']
    return url


def product_gender(final_link):
    category = final_link.split('?')
    if category in full_butik_man:
        return 'Man'
    else:
        return 'Woman'


def butik_product_collection(final_link):
    html = get_html(url=final_link)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        raw_data = soup.find_all('script')[-1].contents[0]
        data_all = preparation_json(raw_data)
        current_dir = data_all['data']['catalogs'][0]['value']['value']['data']
        if current_dir == []:
            return False
        else:
            for item in current_dir:
                # print(item)
                try:
                    butik_product_dict = {}
                    butik_product_dict['product_store'] = 'Butik.ru'
                    butik_product_dict['name'] = product_name(item)
                    butik_product_dict['product_url'] = product_url(item)
                    current_product = get_parser_url(url_product=butik_product_dict['product_url'])
                    butik_product_dict['id'] = current_product['code']
                    butik_product_dict['price'] = product_prise_full(item)
                    butik_product_dict['product_discount'] = product_prise_discount(item)
                    butik_product_dict['brand'] = product_brand(item)
                    butik_product_dict['category'] = current_product['category']
                    butik_product_dict['category_detailed'] = current_product['category_detailed']
                    butik_product_dict['color'] = current_product['color']
                    butik_product_dict['size'] = str(product_size(item))
                    butik_product_dict['product_image'] = current_product['image']
                    butik_product_dict['gender'] = product_gender(final_link)
                    save_data_product_butik(butik_product_dict)
                    print(butik_product_dict)
                except(KeyError, TypeError):
                    pass

                # dict = {'code': code, 'price': price, 'brand': brand, 'color': color,
                #         'category_detailed': category_detailed, 'category': category, 'image': image,
                #         'sizes': sizes_available, 'url': url_store}


# if __name__ == '__main__':
#     page_number_url(full_butik_man, full_butik_women)

#butik_product_collection('https://www.butik.ru/products/muzhchinam-odezhda-verkhnyaya-odezhda-dzhinsovye-kurtki-levis-7737900000-kurtka/')
butik_product_collection('https://www.butik.ru/catalog/muzhchinam/odezhda/')


{'code': '3HZP11 ZNCQZ 1704', 'price': 6493.0, 'brand': 'ARMANI EXCHANGE', 'color': 'бежевый',
 'category_detailed': 'Брюки', 'category': 'Мужчинам Одежда',
 'image': 'https://cdn.butik.ru/imgstore/5/1/f/8/51f843ed-5664-4a63-ac1b-1beeb98f774e-orig.jpg?height=907&width=576',
 'sizes': ['36', 'б/р', '38', 'б/р', '40', '42'],
 'url': 'https://www.butik.ru/products/muzhchinam-odezhda-bryuki-chinosy-armani-exchange-3hzp11-zncqz-1704-bryuki/'}
