from flask import Blueprint, render_template, flash, url_for, current_app
# from webapp_stores import config
# from werkzeug.utils import redirect
from webapp_stores.stores.model import Product

# from webapp_stores import create_app


blueprint = Blueprint('product', __name__, url_prefix='/p')


@blueprint.route("/products")
def defolt_page():
    default()
    def_page = products(start=0)
    return def_page


@blueprint.route("/product")
def products(start):
    with current_app.app_context():
        product = Product.query.offset(start).limit(12).all()
        result = step_1(product)
        page = page_count(start)
        # print(result)
        return render_template('product/all_products.html', dict=result, page=page)


def page_count(start):
    """Функция высчитывает страницу товаров в каталоге"""
    with current_app.app_context():
        all_product = Product.query.count()
        count_pages = int(all_product / 12)
        # print(count_pages)
        start_product = all_product - start
        count_pages_start = int(start_product / 12)
        # print(count_pages_start)
        return (count_pages - count_pages_start) + 1


def step_1(product, count=12):
    all_product = []
    for index in range(0, count):
        f = (str(product[index])).split('|')
        all_product.append(f)
    resalt = dict_p(all_product, count)
    return resalt


def dict_p(all_product, count):
    page = []
    for product_ind in range(0, count):
        dict_page = {}
        product_1 = all_product[product_ind]
        dict_page['name'] = product_1[1]
        dict_page['category'] = product_1[3]
        dict_page['image'] = (clear_img(product_1)).strip("'")
        dict_page['brand'] = brand_name(product_1)
        dict_page['store'] = product_1[6]
        page.append(dict_page)
    return page


def clear_img(product_1):
    img = (product_1[4].strip("['")).strip("']")
    img_2 = img.split(',')
    img_fin = (img_2[0]).strip("'")
    return img_fin


def brand_name(product_1):
    brand = (product_1[5]).strip(' ')
    # print(type(brand))
    if brand == "Без рукавов":
        return 'Бренд неизвестен'
    elif brand == 'Полная':
        return 'Бренд неизвестен'
    else:
        return brand


@blueprint.route("/next_page")
def next_page():
    with open('/home/pasha/PycharmProjects/project_store_find/webapp_stores/product/count.txt', 'r',
              encoding='utf-8') as file:
        data = file.read()
        index = int(data)
    if index == 0:
        index = 12
        next_res = products(index)
        with open('/home/pasha/PycharmProjects/project_store_find/webapp_stores/product/count.txt', 'w',
                  encoding='utf-8') as f:
            f.write(str(index))
        return next_res
    else:
        index += 12
        next_resalt = products(index)
        with open('/home/pasha/PycharmProjects/project_store_find/webapp_stores/product/count.txt', 'w',
                  encoding='utf-8') as f:
            f.write(str(index))
        return next_resalt


@blueprint.route("/prev_page")
def prev_page():
    with open('/home/pasha/PycharmProjects/project_store_find/webapp_stores/product/count.txt', 'r',
              encoding='utf-8') as file:
        data = file.read()
        index = int(data)
    if index == 0:
        resalt = defolt_page()
        return resalt
    else:
        index -= 12
        prev_resalt = products(index)
        with open('/home/pasha/PycharmProjects/project_store_find/webapp_stores/product/count.txt', 'w',
                  encoding='utf-8') as f:
            f.write(str(index))
        return prev_resalt


def default():
    index = 0
    with open('/home/pasha/PycharmProjects/project_store_find/webapp_stores/product/count.txt', 'w',
              encoding='utf-8') as file_clear:
        file_clear.write(str(index))


# @blueprint.route("/product")
# def products(start):
#     with current_app.app_context():
#         all_product = Product.query.count()
#         count_pages = int(all_product / 12)
#         product = Product.query.offset(start).limit(12).all()
#         result = step_1(product)
#         print(result)
#         return render_template('product/all_products.html', dict=result)

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id

if __name__ == "__main__":
    prev_page()
