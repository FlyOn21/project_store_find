import requests as req
import re
# from bs4 import BeautifulSoup
# import ast
import json
link = 'https://m.aliexpress.ru/item/4001029405951.html?pid=808_0004_0209&spm=a2g0n.search-amp.list.' \
       '4001029405951&aff_trace_key=d564700142e0428cbb2511c69f77c78e-1591823186507-02610-UneMJZVf&aff' \
       '_platform=msite&m_page_id=134amp-amYxSxGQTsNe1rBA8GVUYg1591872678970&browser_id=' \
       '8e38cef6d6df4afc8fcd192d5dc6d62f&is_c=Y'

def take_id(start_url = None): # Функция для определения ID товара
    try:
        index_first_step = start_url.index('?')
        first_step_clear = start_url[:index_first_step]
        second_step_clear = re.findall('\d', first_step_clear)
        product_id = ''.join(second_step_clear)
        return product_id
    except(TypeError,AttributeError):
        return False

def ali(link): # Получение словаря параметров товара с Алиеспресс
    try:
        id_doc = take_id(link)
        if id_doc:
            url = f'https://m.aliexpress.ru/api/products/{id_doc}/fetch'
            res = req.get(url,headers = {'Referer': url})
            json_dict = res.json()
            return json_dict
        else:
            return False
    except(req.RequestException, ValueError,TypeError):
        print('Url_Error')
        return False

def parser_product_result():
    if ali(link) == False:


# dict = {'code': code, 'price': price, 'brand': brand, 'color': color,
#                     'category_detailed': category_detailed, 'category': category, 'image': image,
#                     'sizes': sizes_available, 'url': url_store}


if __name__ == '__main__':
    ali(link)