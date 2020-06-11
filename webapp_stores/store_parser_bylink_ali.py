import requests as req
import re


link = 'https://aliexpress.ru/item/32803837362.html?spm=a2g0o.tm152050.8742387550.3.67683b3dmKsifH&gps-id=seaZeus&scm=1007.25281.150704.0&scm_id=1007.25281.150704.0&scm-url=1007.25281.150704.0&pvid=fafbb906-9997-470c-a939-fa60c134342d'


def take_id(link=None):  # Функция для определения ID товара
    try:
        index_first_step = link.index('?')
        first_step_clear = link[:index_first_step]
        second_step_clear = re.findall('\d', first_step_clear)
        product_id = ''.join(second_step_clear)
        return product_id
    except(TypeError, AttributeError):
        return False


def ali(link):  # Получение словарей параметров товара с Алиеспресс
    try:
        id_doc = take_id(link)
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


def color_list(data_1):
    all_color = []
    for index_color in range(len(data_1['data']['skuInfo']['propertyList'][0]['skuPropertyValues'])):
        color = data_1['data']['skuInfo']['propertyList'][0]['skuPropertyValues'][index_color]['skuPropertyValueTips']
        all_color.append(color)
    return all_color


def product_id(data_1):
    id = data_1['data']['productInfo']['productId']
    return id


def price_product_usd(data_1):
    price_usd = data_1['data']['priceInfo']['tradeMaxPrice']['value']
    return price_usd


def delivery_in_country(data_2):
    delivery = data_2['data']['freightResult'][0]['freightAmount']['value']
    return delivery


def product_brand(data_1):
    brand = data_1['data']['specificationInfo']['propertyList'][0]['attrValue']
    return brand


def category_detail(data_1):
    category_detailed = data_1['data']['productInfo']['subject']
    return category_detailed


def product_category(data_1):
    text_with_category = data_1['data']['seoData']['metaInfo']['title']
    category_list = text_with_category.split('|')
    return category_list[1]


def product_image(data_1):
    image_list_url = data_1['data']['productInfo']['imageList']
    return image_list_url


def product_size(data_1):
    size_list = []
    for index_size in range(len(data_1['data']['skuInfo']['propertyList'][1]['skuPropertyValues'])):
        color = data_1['data']['skuInfo']['propertyList'][1]['skuPropertyValues'][index_size][
            'propertyValueDisplayName']
        size_list.append(color)
    return size_list


def product_url(data_1):
    url = data_1['data']['canonical']
    return url


def parser_product_result(link):
    data = ali(link)
    if data == False:
        return "Упс что то пошло нет так, попробуйте еще раз"
    else:
        data_1, data_2 = data
        code = product_id(data_1)
        price = price_product_usd(data_1) + delivery_in_country(data_2)
        brand = product_brand(data_1)
        color = color_list(data_1)
        category_detailed = category_detail(data_1)
        category = product_category(data_1)
        image = product_image(data_1)
        sizes_available = product_size(data_1)
        url_store = product_url(data_1)
        ali_dict = {'code': code, 'price': price, 'brand': brand, 'color': color,
                    'category_detailed': category_detailed, 'category': category, 'image': image,
                    'sizes': sizes_available, 'url': url_store}
        return ali_dict


if __name__ == '__main__':
    print(parser_product_result())
