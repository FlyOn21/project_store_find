import requests as req
from webapp_stores import standard_icon, db_functions
from bs4 import BeautifulSoup

import json

class Butik_ru():

    def __init__(self):
        self.url = 'https://www.butik.ru'
        self.full_butik_man = ['https://www.butik.ru/catalog/zhenshchinam/obuv/',
                      'https://www.butik.ru/catalog/zhenshchinam/sumki/',
                      'https://www.butik.ru/catalog/zhenshchinam/odezhda/',
                      'https://www.butik.ru/catalog/zhenshchinam/aksessuary/']
        self.full_butik_woman = ['https://www.butik.ru/new/muzhchinam/odezhda/',
                        'https://www.butik.ru/new/muzhchinam/sumki/',
                        'https://www.butik.ru/new/muzhchinam/obuv/',
                        'https://www.butik.ru/new/muzhchinam/aksessuary/']

    def get_butik_data(self):
        html = self.get_html(url = self.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string
            name = 'Butik.ru'
            link = soup.find('link', rel="icon", type="image/png")
            icon = self.url + (link['href'])
            online = True
            url = self.url
            db_functions.save_data(title=title, online=online, url=url,
                                      name=name, icon=icon)
            self.page_number_url()
        else:
            online = False
            url = self.url
            name = 'Butik.ru'
            title = 'Магазин временно недоступен'
            icon = standard_icon.standard_icon()
            db_functions.save_data(title=title, online=online, url=url,
                                      name=name, icon=icon)


    def get_html(self,url):
        try:
            result = req.get(url)
            result.raise_for_status()
            return result.text
        except(req.RequestException, ValueError):
            print('Сетевая ошибка')
            return False

    def get_parser_url(self,url_product):
        html = self.get_html(url = url_product)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            raw_data = soup.find_all('script')[-1].contents[0]
            data = self.preparation_json(raw_data)

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

    def page_number_url(self):
        full_randevu = self.full_butik_man + self.full_butik_woman
        for category in full_randevu:
            request_page = self.valid_url(url=category)
            p = 1
            while request_page == True:
                final_link = category + '?page=' + str(p) + '&per_page=100'
                request_page = self.valid_url(url=final_link)
                query = self.butik_product_collection(final_link)
                if query == False:
                    request_page = False
                p += 1
                print(final_link)
            else:
                print(f'Оброботка катигории {category} сайта Рандеву окончена')

    def valid_url(self,url):
        try:
            request = req.get(url)
            if request:
                return True
            else:
                return False
        except(req.RequestException, ValueError):
            return False

    def preparation_json(self,raw_data):
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

    def product_name(self,item):
        return item['seo_name']

    def product_prise_full(self,item):
        return str(item['price'])

    def product_prise_discount(self,item):
        return str(item['price_with_discount'])

    def product_brand(self,item):
        return item['brand_name']

    def product_category(self,item):
        return item['seo_name']

    def product_size(self,item):
        size_dict = {}
        for size in item['product_variations']:
            size_current = size['size']['brand_size']
            quantity = size['size']['stock_online']
            size_dict[size_current] = quantity
        return size_dict

    def product_url(self,item):
        url = 'https://www.butik.ru/' + item['url_name']
        return url

    def product_gender(self,final_link):
        category = final_link.split('?')
        if category in self.full_butik_man:
            return 'Man'
        else:
            return 'Woman'

    def butik_product_collection(self,final_link):
        html = self.get_html(url=final_link)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            raw_data = soup.find_all('script')[-1].contents[0]
            data_all = self.preparation_json(raw_data)
            current_dir = data_all['data']['catalogs'][0]['value']['value']['data']
            if current_dir == []:
                return False
            else:
                for item in current_dir:
                    print(item)
                    try:
                        butik_product_dict = {}

                        butik_product_dict['product_store'] = 'Butik.ru'
                        butik_product_dict['name'] = self.product_name(item)
                        butik_product_dict['product_url'] = self.product_url(item)
                        current_product = self.get_parser_url(url_product=butik_product_dict['product_url'])
                        butik_product_dict['id'] = current_product['code']
                        butik_product_dict['price'] = self.product_prise_full(item)
                        butik_product_dict['product_discount'] = self.product_prise_discount(item)
                        butik_product_dict['brand'] = self.product_brand(item)
                        butik_product_dict['category'] = current_product['category']
                        butik_product_dict['category_detailed'] = current_product['category_detailed']
                        butik_product_dict['color'] = current_product['color']
                        butik_product_dict['size'] = str(self.product_size(item))
                        butik_product_dict['product_image'] = current_product['image']
                        butik_product_dict['gender'] = self.product_gender(final_link)
                        print(butik_product_dict)
                        db_functions.save_data_product(product_dict= butik_product_dict)
                    except(KeyError, TypeError):
                        pass





if __name__ == '__main__':
    c = Butik_ru()
    print(c.page_number_url())
