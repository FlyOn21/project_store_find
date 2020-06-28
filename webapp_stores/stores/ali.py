import requests as req
from webapp_stores import db_functions
from webapp_stores.proxy import get_query,curs
from bs4 import BeautifulSoup
import time
import json
import re

category_dir = {'202005148': 'Платья', '202003912': 'Блузки,рубашки', '202001904': 'Толстовки,свитшоты',
                '202003500': 'Кардиганы', '202003502': 'Водолазки', '202003503': 'Джемпера', '202061873': 'Пончо',
                '202003530': 'Куртки', '202005126': 'Парки', '202005127': 'Куртки из искусственного меха',
                '202005128': 'Кожаные куртки', '202005129': 'Плащи и тренчи', '202001903': 'Жилеты, безрукавки',
                '202005130': 'Пальто', '202060221': 'Пуховики', '202061136': 'Шубы, дубленки', '202002388': 'Юбки',
                '202001905': 'Брюки', '202001908': 'Джинсы', '202003586': 'Легинсы',
                '202059291': 'Комбинезоны c шортами',
                '202001901': 'Футболки', '202003454': 'Топы', '202001902': 'Майки', '202032002': 'Футболки поло',
                '202003589': 'Комбинезон', '202059286': 'Боди', '202003508': 'Вечерние костюмы',
                '202003505': 'Брючные костюмы',
                '202003506': 'Костюмы с юбкой', '202032004': 'Спортивные костюмы', '205896101': 'Купальники',
                '205896501': 'Пляжная одежда',
                '202001909': 'Шорты', '202003504': 'Жилеты', '202003507': 'Пиджаки',
                '202003442': 'Женское нижнее белье',
                '202003447': 'Женские носки и чулочные изделия', '202003445': 'Женские пижамы',

                '202001895': 'Толстовки и свитшоты', '202028001': 'Поло', '202001893': 'Футболки',
                '202003386': 'Верхняя одежда',
                '202032005': 'Брюки', '202003388': 'Рубашки', '202001897': 'Джинсы', '202003404': 'Свитера',
                '202003398': 'Костюмы',
                '202001898': 'Шорты', '202060623': 'Спортивные костюмы', '202003411': 'Пляжные плавки'}
full_ali_woman = ['https://aliexpress.ru/af/category/202005148.html',
                  'https://aliexpress.ru/af/category/202003912.html',
                  'https://aliexpress.ru/af/category/202001904.html',
                  'https://aliexpress.ru/af/category/202003500.html',
                  'https://aliexpress.ru/af/category/202003502.html',
                  'https://aliexpress.ru/af/category/202003503.html',
                  'https://aliexpress.ru/af/category/202061873.html',
                  'https://aliexpress.ru/af/category/202003530.html',
                  'https://aliexpress.ru/af/category/202005126.html',
                  'https://aliexpress.ru/af/category/202005127.html',
                  'https://aliexpress.ru/af/category/202005128.html',
                  'https://aliexpress.ru/af/category/202005129.html',
                  'https://aliexpress.ru/af/category/202001903.html',
                  'https://aliexpress.ru/af/category/202005130.html',
                  'https://aliexpress.ru/af/category/202060221.html',
                  'https://aliexpress.ru/af/category/202061136.html',
                  'https://aliexpress.ru/af/category/202002388.html',
                  'https://aliexpress.ru/af/category/202002388.html',
                  'https://aliexpress.ru/af/category/202001905.html',
                  'https://aliexpress.ru/af/category/202001908.html',
                  'https://aliexpress.ru/af/category/202003586.html',
                  'https://aliexpress.ru/af/category/202059291.html',
                  'https://aliexpress.ru/af/category/202001901.html',
                  'https://aliexpress.ru/af/category/202003454.html',
                  'https://aliexpress.ru/af/category/202001902.html',
                  'https://aliexpress.ru/af/category/202032002.html',
                  'https://aliexpress.ru/af/category/202003589.html',
                  'https://aliexpress.ru/af/category/202059286.html',
                  'https://aliexpress.ru/af/category/202003508.html',
                  'https://aliexpress.ru/af/category/202003505.html',
                  'https://aliexpress.ru/af/category/202003506.html',
                  'https://aliexpress.ru/af/category/202032004.html',
                  'https://aliexpress.ru/af/category/205896101.html',
                  'https://aliexpress.ru/af/category/205896501.html',
                  'https://aliexpress.ru/af/category/202001909.html',
                  'https://aliexpress.ru/af/category/202003504.html',
                  'https://aliexpress.ru/af/category/202003507.html',
                  'https://aliexpress.ru/af/category/202003442.html',
                  'https://aliexpress.ru/af/category/202003447.html',
                  'https://aliexpress.ru/af/category/202003445.html', ]
full_ali_man = ['https://aliexpress.ru/af/category/202001895.html',
                'https://aliexpress.ru/af/category/202028001.html',
                'https://aliexpress.ru/af/category/202001893.html',
                'https://aliexpress.ru/af/category/202003386.html',
                'https://aliexpress.ru/af/category/202032005.html',
                'https://aliexpress.ru/af/category/202003388.html',
                'https://aliexpress.ru/af/category/202001897.html',
                'https://aliexpress.ru/af/category/202003404.html',
                'https://aliexpress.ru/af/category/202003398.html',
                'https://aliexpress.ru/af/category/202001898.html',
                'https://aliexpress.ru/af/category/202060623.html',
                'https://aliexpress.ru/af/category/202003411.html']
count = 0


class Aliexpress():

    def __init__(self):
        self.category_dir = category_dir
        self.full_ali_woman = full_ali_woman
        self.full_ali_man = full_ali_man
        self.count = count

    def page_ali(self):
        full_ali = self.full_ali_man + self.full_ali_woman
        for category in full_ali:
            for page_ali in range(1, 61):
                final_link = category + '?page=' + str(page_ali)
                self.ali_product_collection(final_link)
                print(final_link)
            else:
                print(f'Оброботка катигории {category} сайта Aliexpress окончена')

    def preparation_json(self, raw_data):
        raw_data = str(raw_data).replace('''                        window.runParams = {};
                    window.runParams = ''', '')

        all_data = raw_data.replace('\n', '')
        raw_data_1 = all_data.replace('                ', '')
        raw_data_2 = ((raw_data_1.split('window.runParams.csrfToken'))[0]).strip(';')
        data = json.loads(raw_data_2)
        return data


    def product_gender(self, link):
        category = link.split('?')
        if category[0] in self.full_ali_woman:
            return 'Женское'
        else:
            return 'Мужское'

    def take_id(self, link=None):  # Функция для определения ID товара
        try:
            if '?' in link:
                index_first_step = link.index('?')
                first_step_clear = link[:index_first_step]
            else:
                first_step_clear = link   #[:index_first_step]
            second_step_clear = re.findall('\d', first_step_clear)
            product_id = ''.join(second_step_clear)
            return product_id
        except(TypeError, AttributeError):
            return False

    def ali(self, link=None):  # Получение словарей параметров товара с Алиеспресс
        try:
            id_doc = self.take_id(link)
            if id_doc:
                url_1 = f'https://m.aliexpress.ru/api/products/{id_doc}/fetch'
                url_2 = f'https://m.aliexpress.ru/api/products/{id_doc}/fees?country=RU&tradeCurrency=RUB'
                res_1 = req.get(url_1, headers={'Referer': url_1})
                res_2 = req.get(url_2, headers={'Referer': url_2})
                json_dict_info = res_1.json()
                json_dict_delivery = res_2.json()
                # print(json_dict_info)
                return json_dict_info, json_dict_delivery
            else:
                return False
        except(req.RequestException, ValueError, TypeError):
            print('Url_Error')
            return False

    def color_list(self, data_1):
        all_color = []
        for index_color in range(len(data_1['data']['skuInfo']['propertyList'][0]['skuPropertyValues'])):
            color = data_1['data']['skuInfo']['propertyList'][0]['skuPropertyValues'][index_color][
                'propertyValueName']
            all_color.append(color)
        return all_color

    def product_name(self, item):
        return item['title']

    def product_id_store(self, item):
        return str(item['productId'])

    def product_url(self, item):
        url = str(item['productDetailUrl'])
        url_f = url.split('?')
        return 'https:'+ url_f[0]

    def product_store_other(self, item):
        return str(item['store'])


    def product_id(self, data_1):
        id = data_1['data']['productInfo']['productId']
        return id


    def price_product_usd(self, data_1):
        price_all = {}
        curs_usd = curs.get_curs_usd()
        sale_max_price = data_1['data']['priceInfo']['saleMaxPrice']['value']
        price_all['sale_max_price'] = round((sale_max_price*curs_usd),3)
        sale_min_price = data_1['data']['priceInfo']['saleMinPrice']['value']
        price_all['sale_min_price'] = round((sale_min_price*curs_usd),3)
        trade_max_price = data_1['data']['priceInfo']['tradeMaxPrice']['value']
        price_all['trade_max_price'] = round((trade_max_price*curs_usd),3)
        trade_min_price = data_1['data']['priceInfo']['tradeMinPrice']['value']
        price_all['trade_min_price'] = round((trade_min_price*curs_usd),3)
        return price_all

    def delivery_in_country(self, data_2):
        delivery_dict = {}
        for index_deliv in range(len(data_2['data']['freightResult'])):
            delivery = data_2['data']['freightResult'][index_deliv]['freightAmount']['value']
            delivery_operator = \
                ((data_2['data']['freightResult'][index_deliv]['freightLayout']['layout'][1]['text']).split('>'))[-1]
            delivery_dict[delivery_operator] = delivery
        return delivery_dict

    def product_brand(self, data_1):
        brand = data_1['data']['specificationInfo']['propertyList'][0]['attrValue']
        return brand

    def category_detail(self, data_1):
        category_detailed = data_1['data']['descInfo']['productDescUrl']
        return category_detailed

    def product_category_p(self, data_1):
        text_with_category = data_1['data']['seoData']['metaInfo']['title']
        category_list = text_with_category.split('|')
        return category_list[1]

    def product_image_p(self, data_1):
        image_list_url = data_1['data']['productInfo']['imageList']
        return image_list_url

    def product_size(self, data_1):
        size_list = []
        try:
            for index_size in range(len(data_1['data']['skuInfo']['propertyList'][1]['skuPropertyValues'])):
                color = data_1['data']['skuInfo']['propertyList'][1]['skuPropertyValues'][index_size][
                    'propertyValueDisplayName']
                size_list.append(color)
            return size_list
        except(IndexError):
            return None

    def product_url_p(self, data_1):
        url = data_1['data']['canonical']
        return url

    def parser_product_result(self, link=None):
        data = self.ali(link)
        if data == False:
            return "Упс что то пошло нет так, попробуйте еще раз"
        else:
            data_1, data_2 = data
            id = self.product_id(data_1)
            price_all = [price for price in (self.price_product_usd(data_1)).values()]
            price = price_all[0:2]
            product_discount = price_all[2:5]
            delivery = self.delivery_in_country(data_2)
            brand = self.product_brand(data_1)
            color = self.color_list(data_1)
            category_detailed = self.category_detail(data_1)
            category = self.product_category_p(data_1)
            image = self.product_image_p(data_1)
            sizes_available = self.product_size(data_1)
            url_store = self.product_url_p(data_1)
            product_store = 'Aliexpress'
            gender = self.product_gender(link)
            ali_dict = {'id': id,'name':category,'product_store':product_store, 'price': str(price),'product_discount': str(product_discount),
                        'brand': brand, 'color': str(color),'category_detailed': category_detailed,
                        'category': category, 'product_image': str(image),'size': str(sizes_available), 'url': url_store,
                        'delivery': str(delivery),'product_url':link,'gender':gender,'size_possible':''}
            # {'name': name, 'id': id, 'price': price, 'product_discount': discount, 'brand': brand, 'color': color,
            #  'category_detailed': category_detailed, 'category': category, 'product_image': image,
            #  'size': sizes_available, 'size_possible': sizes_possible, 'gender': gender, 'product_url': url_store,
            #  'product_store': store}
            # print(ali_dict)
            return ali_dict

    def ali_product_collection(self, final_link):
        html = get_query.get_html(url=final_link)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            try:
                raw_data_1 = soup.find_all('script', type="text/javascript")[-2].contents[0]
                data_all = self.preparation_json(raw_data_1)
                for item in data_all['items']:
                    try:
                        ali_product_dict = {}
                        ali_product_dict['product_store'] = 'Aliexpress'
                        ali_product_dict['product_url'] = self.product_url(item)
                        current_product = self.parser_product_result(ali_product_dict['product_url'])

                        ali_product_dict['name'] = self.product_name(item)
                        ali_product_dict['id'] = self.product_id_store(item)
                        ali_product_dict['price'] = str(current_product['price'])
                        ali_product_dict['product_discount'] = str(current_product['product_discount'])
                        ali_product_dict['brand'] = current_product['brand']
                        ali_product_dict['delivery'] = str(current_product['delivery'])
                        ali_product_dict['category'] = current_product['category']
                        ali_product_dict['category_detailed'] = current_product['category_detailed']
                        ali_product_dict['color'] = str(current_product['color'])
                        ali_product_dict['size'] = str(current_product['size'])
                        ali_product_dict['product_image'] = str(current_product['product_image'])
                        ali_product_dict['other'] = str(self.product_store_other(item))
                        ali_product_dict['gender'] = self.product_gender(link = final_link)
                        print('------------------------------------------------')
                        print(ali_product_dict)
                        print('------------------------------------------------')
                        db_functions.save_data_product(product_dict=ali_product_dict)
                        # return ali_product_dict
                    except(KeyError, TypeError):
                        pass
            except(IndexError):
                time.sleep(120)
                self.count += 1
                if self.count > 30:
                    print('Ошибка парсинга, парсинг остановлен')
        else:
            print("повтоная попытка получить страницу")
            self.ali_product_collection(final_link)


if __name__ == '__main__':
    c = Aliexpress()
    print(c.page_ali())
