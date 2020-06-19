import requests
from bs4 import BeautifulSoup
from pprint import PrettyPrinter # красиво выводит результат из словарей и списков
import ast
import json

# URL_randevu ='https://www.rendez-vous.ru/catalog/female/krossovki/ash_eclipse_bis_chernyy-2230884/' # Общий пример
# URL_randevu ='https://www.rendez-vous.ru/catalog/accessories/schetka-d-volos/la_beaute__sp103_chernyy-1251744/' # One-size
# URL_randevu ='https://www.rendez-vous.ru/catalog/female/kedy/geox_d92fba_belyy-2042567/' # Товар не доступен
# URL_randevu = 'https://www.rendez-vous.ru/catalog/female/bosonoghki/vagabond_4738_040_chernyy-2034463/'
#
# URL_butik = 'https://www.butik.ru/products/zhenshchinam-obuv-bosonozhki-na-kabluke-vagabond-4738-040-20-bosonozhki/'
# URL_butik ='https://www.butik.ru/products/zhenshchinam-obuv-botinki-vysokie-dr-martens-11821006-black-smooth-botinki/'
#
# URL_ali='https://aliexpress.ru/item/4001023889599.html?spm=a2g0o.productlist.0.0.16c82a4aREnhrb&algo_pvid=54eaa039-b5e2-4514-9555-3c8004722209&algo_expid=54eaa039-b5e2-4514-9555-3c8004722209-9&btsid=0b8b035c15916224144315135ebccb&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_'

def get_html(url):
    try:
        result=requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_store_randevu(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        pp=PrettyPrinter(indent=2)
        #pp.pprint(soup)

        # if product is available
        try:
            url_store = url
            image = soup.find('div', class_='item-info').find('div', class_='carousel-image-list').find('img')[
                'data-src']

            code =  \
            ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                'name']

            price = ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                'priceFromCart']

            brand = ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                'brand']
            color = ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                'variant']
            category_detailed = \
                ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                    'category'].split(
                    '/')[0]
            category = soup.find('div', class_='breadcrumbs').find_all('li')[1].find('a').text

            # sizes
            try:
                sizes = soup.find('ul', class_='form-select-list scrollbar scrollbar-y').find_all('li')
                sizes_available = []
                for size in sizes:
                    sizes_available.append(size.text.strip())
            except:
                sizes_available = ['one-size']

            dict = {'code': code, 'price': price, 'brand': brand, 'color': color,
                    'category_detailed': category_detailed, 'category': category, 'image': image,
                    'sizes': sizes_available, 'url': url_store}
            return dict

        # if the product is not available in the store
        except:
            # what should we do?
            print('Товар не доступен')



def get_store_butik(url = 'https://www.butik.ru/products/zhenshchinam-odezhda-dzhinsy-zauzhennye-love-republic-02554267661-dzhinsy/'):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')

        raw_data = soup.find_all('script')[-1]
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
        raw_data = raw_data.replace(replace, '').strip(r'</script>')
        print(raw_data)

        data = json.loads(raw_data)
        #pp = PrettyPrinter(indent=2)
        #pp.pprint(data)


        price = data['data']['card'][0]['value']['value']['price_with_discount']
        color = data['data']['card'][0]['value']['value']['color']
        brand = data['data']['card'][0]['value']['value']['brand']['name']
        category_detailed = data['data']['card'][0]['value']['value']['name']
        category = data['data']['card'][0]['value']['value']['breadcrumbs']['full_ru_array'][0]['text'] + ' ' + \
                   data['data']['card'][0]['value']['value']['breadcrumbs']['full_ru_array'][1]['text']
        code = data['data']['card'][0]['value']['value']['sku']
        image = data['seoData']['ogImage']
        url_store = url
        sizes_available=[i['size']['brand_size'] for i in data['data']['card'][0]['value']['value']['product_variations'] if i['size']['stock_with_reserve']]


        dict = {'code': code, 'price': price, 'brand': brand, 'color': color,
                'category_detailed': category_detailed, 'category': category, 'image': image,
                'sizes': sizes_available, 'url': url_store}
        print(dict)


if __name__ =='__main__':
    c = get_store_butik()
