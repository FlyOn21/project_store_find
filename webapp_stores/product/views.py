from flask import Blueprint, render_template, flash, url_for, current_app, request
import ast
# from webapp_stores import config
# from werkzeug.utils import redirect
from webapp_stores.stores.model import Product

# from webapp_stores import create_app


blueprint = Blueprint('product', __name__, url_prefix='/p')


@blueprint.route("/products")
def products(start=0):
    """Функция которая обращается в базу для получения товаров на страницу и определяет и определяет номера
    и стартовые индексы страниц"""

    with current_app.app_context():
        product = Product.query.offset(start).limit(12).all()
        result = step_1(product)
        page_start, last_page = page_count(start)

        if start == 0:
            page_one = 1
            query_index_one = (page_one * 12) - 12
            page_two = page_one + 1
            query_index_two = query_index_one + 12
            page_therd = page_two + 1
            query_index_therd = query_index_two + 12
            next_p = page_one + 1
        elif page_start == last_page:
            page_one = page_start - 1
            query_index_one = (page_one * 12) - 12
            page_two = page_one + 1
            query_index_two = query_index_one + 12
            page_therd = page_two + 1
            query_index_therd = query_index_two + 12
            next_p = page_start
        else:
            page_one = page_start - 1
            query_index_one = (page_one * 12) - 12
            page_two = page_one + 1
            query_index_two = query_index_one + 12
            page_therd = page_two + 1
            query_index_therd = query_index_two + 12
            next_p = page_two + 1

        # print(result)
        return render_template('product/all_products.html', dict=result, page_prev=page_one, page=page_two,
                               page_next=page_therd, query_index_one=query_index_one, query_index_two=query_index_two,
                               query_index_therd=query_index_therd, next_p=next_p)


def page_count(start):
    """Функция высчитывает страницу товаров в каталоге"""
    with current_app.app_context():
        all_product = Product.query.count()
        count_pages = int(all_product / 12)
        # print(count_pages)
        start_product = all_product - start
        if start_product != 0:
            count_pages_start = int(start_product / 12)
            start_page = (count_pages - count_pages_start) + 1
            return (start_page,count_pages)
        else:
            count_pages_start = int(start_product / 12)
            start_page = count_pages - count_pages_start
            return (start_page, count_pages)



def step_1(product, count=12):
    all_product = []
    for index in range(0, count):
        f = (str(product[index])).split('|')
        print(f)
        all_product.append(f)
    resalt = dict_p(all_product, count)
    return resalt


def dict_p(all_product, count):
    """Словарь данных о товаре из базы для формирования каталога и страницы товара"""
    page = []
    for product_ind in range(0, count):
        dict_page = {}
        product_1 = all_product[product_ind]
        dict_page['id'] = int(product_1[0])
        dict_page['name'] = product_1[1]
        dict_page['category'] = product_1[3]
        dict_page['image'] = clear_img(product_1)
        dict_page['brand'] = brand_name(product_1)
        dict_page['store'] = product_1[6]
        dict_page['color'] = color(int(product_1[0]))
        dict_page['price_full'] = price_full(int(product_1[0]))
        dict_page['prise_discount'] = prise_discount(int(product_1[0]))
        dict_page['category_detailed'] = category_detailed(int(product_1[0]))
        dict_page['gender'] = gender(int(product_1[0]))
        dict_page['delivery'] = delivery(int(product_1[0]))
        dict_page['url'] = url(int(product_1[0]))

        page.append(dict_page)
    print(page)
    return page


def product_query(id):
    with current_app.app_context():
        query = Product.query.filter_by(id=id).first()
        return query

def url(id):
    query = product_query(id)
    return query.url

def delivery(id):
    query = product_query(id)
    delivery_p = str(query.delivery)
    delivery_res = ast.literal_eval(delivery_p)
    print(delivery_res)
    print(type(delivery_res))
    try:
        delivery_res_list = []
        for key,values in delivery_res.items():
            resalt = key + ':' + str(values)
            delivery_res_list.append(resalt)
        return delivery_res_list
    except AttributeError:
        return None


def gender(id):
    query = product_query(id)
    return query.gender


def category_detailed(id):
    query = product_query(id)
    return query.category_detailed


def price_full(id):
    """Функция получающая полную цену товара из базы"""
    query = product_query(id)
    price_all = str(query.prise_full)
    if price_all[0] == '[':
        price_p = ast.literal_eval(price_all)
    else:
        price_p = [query.prise_full]
    return price_p


def prise_discount(id):
    """Функция получающая цену со скидкой товара из базы"""
    query = product_query(id)
    price_all = str(query.prise_discount)
    if price_all[0] == '[':
        price_d = ast.literal_eval(price_all)
    else:
        price_d = [query.prise_discount]
    return price_d


def color(id):
    """Функция которая преобразует стороку цветов из базы в словарь или возврашает строку цвета если цвет оодин"""
    query = product_query(id)
    color_all = str(query.color)
    if color_all[0] == '[':
        color_p = ast.literal_eval(color_all)
    else:
        color_p = [str(query.color)]
    return color_p


def clear_img(product_1):
    """Функция получения списка ссылок на картинки"""
    img = product_1[4]
    if img[0] == '[':
        image_p = ast.literal_eval(img)
    else:
        image_p = [img]
        # print("-------------------------",image_p,"-------------------------")
    return image_p


def brand_name(product_1):
    brand = (product_1[5]).strip(' ')
    # print(type(brand))
    if brand == "Без рукавов":
        return 'Бренд неизвестен'
    elif brand == 'Полная':
        return 'Бренд неизвестен'
    else:
        return brand


@blueprint.route('/page_num', methods=['GET'])
def page_num():
    """Функция обрабатывает гет запрос по номеру страницы и возвращает словарь товаров на данной странице"""
    page = request.args.get('page')
    start_index = ((int(page)) * 12) - 12
    return products(start_index)


@blueprint.route('/current_product', methods=['GET'])
def current_product():
    id = request.args.get('product_id')
    with current_app.app_context():
        # product = Product.query.filter_by(id = id).first()
        prod_current = [Product.query.filter_by(id=id).first()]
        result_current = step_1(prod_current, count=1)
        return render_template('product/one_product.html', dict=result_current)


# if __name__ == "__main__":
#     prev_page()
