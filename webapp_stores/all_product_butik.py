import requests as req
from bs4 import BeautifulSoup
import json
from webapp_stores.save_data_store import save_data_product_butik


def get_html(url):
    try:
        result = req.get(url)
        result.raise_for_status()
        return result.text
    except(req.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def page_number_url():
    full_randevu = ['https://www.butik.ru/catalog/zhenshchinam/obuv/',
                    'https://www.butik.ru/catalog/zhenshchinam/sumki/',
                    'https://www.butik.ru/catalog/zhenshchinam/odezhda/',
                    'https://www.butik.ru/catalog/zhenshchinam/aksessuary/',
                    'https://www.butik.ru/new/muzhchinam/odezhda/',
                    'https://www.butik.ru/new/muzhchinam/sumki/',
                    'https://www.butik.ru/new/muzhchinam/obuv/',
                    'https://www.butik.ru/new/muzhchinam/aksessuary/']
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
            print(f'Оброботка катигории {category} сайта Рандеву окончена')


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


def product_id_store(item):
    return str(item['photobank_id'])


def product_prise_full(item):
    return float(item['price'])


def product_prise_discount(item):
    return float(item['price_with_discount'])


def product_brand(item):
    return item['brand_name']


def product_category(item):
    return item['seo_name']


def product_color():
    return None


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


def product_image(item):
    image_list = []
    for image_url in item['images_origin']:
        image_list.append(image_url)
    return image_list


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
                    butik_product_dict['id'] = product_id_store(item)
                    butik_product_dict['price'] = product_prise_full(item)
                    butik_product_dict['product_discount'] = product_prise_discount(item)
                    butik_product_dict['brand'] = product_brand(item)
                    butik_product_dict['category'] = product_category(item)
                    butik_product_dict['variant'] = product_color()
                    butik_product_dict['size'] = str(product_size(item))
                    butik_product_dict['product_url'] = product_url(item)
                    butik_product_dict['product_image'] = str(product_image(item))
                    # print(butik_product_dict)
                    save_data_product_butik(butik_product_dict)
                except(KeyError, TypeError):
                    pass


if __name__ == '__main__':
    page_number_url()
