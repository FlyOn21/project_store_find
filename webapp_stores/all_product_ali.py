import requests as req
from bs4 import BeautifulSoup
import json
from webapp_stores.save_data_store import save_data_product_ali

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
full_ali_women = ['https://aliexpress.ru/af/category/202005148.html',
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
                    'https://aliexpress.ru/af/category/202003445.html',]
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
def get_html(url):
    # proxy = {'https':'185.171.24.244:808'}
    try:
        result = req.get(url)  # proxies=proxy,
        result.encoding = 'utf-8'
        result.raise_for_status()
        return result.text
    except(req.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def page_ali(full_ali_man,full_ali_women):
    full_ali = full_ali_man+full_ali_women
    for category in full_ali:
        for page_ali in range(1, 61):
            final_link = category + '?page=' + str(page_ali)
            ali_product_collection(final_link)
            print(final_link)
        else:
            print(f'Оброботка катигории {category} сайта Aliexpress окончена')


def preparation_json(raw_data):
    raw_data = str(raw_data).replace('''                        window.runParams = {};
                    window.runParams = ''', '')

    all_data = raw_data.replace('\n', '')
    raw_data_1 = all_data.replace('                ', '')
    raw_data_2 = ((raw_data_1.split('window.runParams.csrfToken'))[0]).strip(';')
    data = json.loads(raw_data_2)
    return data


def product_name(item):
    return item['title']


def product_id_store(item):
    return str(item['productId'])


def product_prise_full(item):
    # price_1 = (item['originalPrice']).replace(' ', '.')
    price_o = ((item['originalPrice']).replace(',', '.')).strip(' руб.')
    return price_o


def product_prise_discount(item):
    price_dic = ((item['price']).replace(',', '.')).strip(' руб.')
    return price_dic


def product_brand():
    return None


def product_category(item):
    if item['traceInfo']['displayCategoryId'] in category_dir.keys():
        return category_dir[item['traceInfo']['displayCategoryId']]
    else:
        return None


def product_color():
    return None


def product_size():
    return None


def product_url(item):
    url = item['productDetailUrl']
    return url


def product_image(item):
    image = item['imageUrl']
    return image


def product_delivery(item):
    delivery_st = ((item['logisticsDesc']).replace('Отправка:', '')).strip(' руб.')
    delivery_default = delivery_st.replace(',', '.')
    return delivery_default


def product_store_other(item):
    return str(item['store'])

def product_gender(final_link):
    category = final_link.split('?')
    if category[0] in full_ali_women:
        return 'Женское'
    else:
        return 'Мужское'

def ali_product_collection(final_link):
    html = get_html(url=final_link)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        raw_data_1 = soup.find_all('script', type="text/javascript")[-2].contents[0]
        data_all = preparation_json(raw_data_1)
        for item in data_all['items']:
            # print('-------------------------------------')
            # print(item)
            # print('-------------------------------------')
            try:
                ali_product_dict = {}
                ali_product_dict['product_store'] = 'Aliexpress'
                ali_product_dict['name'] = product_name(item)
                ali_product_dict['id'] = product_id_store(item)
                ali_product_dict['price'] = product_prise_full(item)
                ali_product_dict['product_discount'] = product_prise_discount(item)
                ali_product_dict['brand'] = product_brand()
                ali_product_dict['category'] = product_category(item)
                ali_product_dict['variant'] = product_color()
                ali_product_dict['size'] = product_size()
                ali_product_dict['product_url'] = product_url(item)
                ali_product_dict['product_image'] = product_image(item)
                ali_product_dict['delivery'] = product_delivery(item)
                ali_product_dict['other_store'] = product_store_other(item)
                ali_product_dict['gender'] = product_gender(final_link)
                # print('------------------------------------------------')
                # print(ali_product_dict)
                # print('------------------------------------------------')
                save_data_product_ali(ali_product_dict)
            except(KeyError, TypeError):
                pass


if __name__ == '__main__':
    page_ali(full_ali_man,full_ali_women)
