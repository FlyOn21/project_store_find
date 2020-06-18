import requests as req
from webapp_stores import standard_icon, db_functions
from bs4 import BeautifulSoup
import ast
import time


class Rendezvous():

    def __init__(self):
        self.url = 'https://www.rendez-vous.ru'
        self.full_randevu_man = ['https://www.rendez-vous.ru/catalog/male/',
                                 'https://www.rendez-vous.ru/catalog/bags_male/',
                                 'https://www.rendez-vous.ru/catalog/muzhskaya_odezhda/',
                                 'https://www.rendez-vous.ru/catalog/accessories_male/']
        self.full_randevu_women = ['https://www.rendez-vous.ru/catalog/female/',
                                   'https://www.rendez-vous.ru/catalog/bags_female/',
                                   'https://www.rendez-vous.ru/catalog/zhenskaya_odezhda/',
                                   'https://www.rendez-vous.ru/catalog/accessories_female/']
        self.full_randevu_chaildren = ['https://www.rendez-vous.ru/catalog/girls/',
                                       'https://www.rendez-vous.ru/catalog/boys/']
        self.full_randevu_unisex = ['https://www.rendez-vous.ru/catalog/tools/']

    def get_randevu_data(self):
        html = self.get_html(self.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string
            name = 'Rendezvous'
            icon = soup.find('meta', property="og:image", )['content']
            online = True
            url = self.url
            db_functions.save_data(title=title, online=online, url=url,
                                   name=name, icon=icon)
            self.get_full_randevu()

        else:
            online = False
            url = self.url
            name = 'Rendezvous'
            title = 'Магазин временно недоступен'
            icon = standard_icon.standard_icon()
            db_functions.save_data(title=title, online=online, url=url,
                                   name=name, icon=icon)

    def get_html(self, url):
        try:
            result = req.get(url)
            result.raise_for_status()
            return result.text
        except(req.RequestException, ValueError):
            print('Сетевая ошибка')
            return False

    def get_store_randevu(self, url):
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            try:
                url_store = url
                image = soup.find('div', class_='item-info').find('div', class_='carousel-image-list').find('img')[
                    'data-src']
                id = ((soup.find('span', class_="item-vendor-code").text).split())[1]

                code = \
                    ast.literal_eval(soup.find('button', class_='btn-block btn-primary btn')['data-productinfo'])[
                        'name']

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

                dict = {'code': code, 'brand': brand, 'color': color,'id':id,
                        'category_detailed': category_detailed, 'category': category, 'image': image,
                        'sizes': sizes_available, 'url': url_store}
                # print(dict)
                return dict

            # if the product is not available in the store
            except:
                # what should we do?
                print('Товар не доступен')

    def pages_in_category(self, url):
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            number_of_pages = int(soup.find('ul', class_='pagination').find_all('li', class_='page')[-1].get_text())
            return number_of_pages

    # Парсит линки всех товаров все товары
    def get_full_randevu(self):
        full_randevu = self.full_randevu_man + self.full_randevu_women + \
                       self.full_randevu_chaildren + self.full_randevu_unisex
        for category in full_randevu:
            pages = self.pages_in_category(url=category)
            # print(pages)
            for pa in range(1, pages + 1):
                final_link = category + 'page/' + str(pa) + '/'
                self.randevuze_product_collection(final_link)
                print(final_link)

    def prod_url(self, product):
        url = 'https://www.rendez-vous.ru/' + product.find('a')['href']
        return url

    def prod_category(self, product_randevoyz_all):
        product_category = product_randevoyz_all['category']
        product_category_clear = ((product_category).split('/'))[0]
        return product_category_clear

    def prod_discount(self, product):
        product_discount = str(('').join((product.find('span', class_="item-price-value").get_text()).split()))
        return product_discount

    def prod_store(self):
        return 'Рандеву'

    def product_name(self, product):
        name = ((product.find('div', class_="item-name")).text).strip()
        return name

    def dict_cliner(self, product_randevoyz_all):
        try:
            if 'dimension5' in product_randevoyz_all:
                del product_randevoyz_all['dimension5']
            if 'position' in product_randevoyz_all:
                del product_randevoyz_all['position']
            if 'variant' in product_randevoyz_all:
                del product_randevoyz_all['variant']
            return product_randevoyz_all
        except(KeyError):
            return product_randevoyz_all

    def product_gender(self, final_link):
        category = final_link.split('page/')
        if category[0] in self.full_randevu_man:
            return 'Man'
        elif category[0] in self.full_randevu_women:
            return 'Woman'
        elif category[0] in self.full_randevu_chaildren:
            return 'Children'
        else:
            return 'Unisex'

    def randevuze_product_collection(self, final_link):
        html = self.get_html(url=final_link)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            product_all = soup.find('ul', class_="list-items list-items-catalog list-view-1 js-list-items"). \
                find_all('li', class_="item")
            for product in product_all:
                # print(product)
                try:
                    product_randevoyz_all = ast.literal_eval(product['data-productinfo'])
                    product_randevoyz = self.dict_cliner(product_randevoyz_all)
                    product_url = self.prod_url(product)
                    product_randevoyz['category'] = self.prod_category(product_randevoyz_all)
                    current_product = self.get_store_randevu(url=product_url)
                    product_randevoyz['name'] = self.product_name(product)
                    # print(current_product)
                    product_randevoyz['product_store'] = self.prod_store()
                    product_randevoyz['color'] = current_product['color']
                    product_randevoyz['category'] = current_product['category']
                    product_randevoyz['category_detailed'] = current_product['category_detailed']
                    product_randevoyz['product_url'] = product_url
                    product_randevoyz['size'] = str(current_product['sizes'])
                    product_randevoyz['product_image'] = current_product['image']
                    product_randevoyz['product_discount'] = self.prod_discount(product)
                    product_randevoyz['gender'] = self.product_gender(final_link)
                    product_randevoyz['other'] = product_randevoyz['id']
                    product_randevoyz['id'] = current_product['id']
                    print(product_randevoyz)
                    time.sleep(3.0)
                    db_functions.save_data_product(product_randevoyz)
                except(KeyError, TypeError):
                    continue


if __name__ == '__main__':
    c = Rendezvous()
    print(c.get_randevu_data())
