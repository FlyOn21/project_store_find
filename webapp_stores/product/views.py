from flask import Blueprint, render_template, flash, url_for,current_app
# from webapp_stores import config
# from werkzeug.utils import redirect
from webapp_stores.stores.model import Product
# from webapp_stores import create_app



blueprint = Blueprint('product', __name__,url_prefix='/p')



@blueprint.route("/products")
def products(start = 0):
    #app = current_app.app_context() # .config.from_pyfile('config.py')
    with current_app.app_context():
        all_product = Product.query.count()
        count_pages = int(all_product/12)
        product = Product.query.offset(start).limit(12).all()
        result = step_1(product)
        print(result)
        return render_template('product/all_products.html', dict = result)

def step_1(product,count = 12):
    all_product = []
    for index in range(0, count):
        f = (str(product[index])).split('|')
        all_product.append(f)
    resalt = dict_p(all_product,count)
    return resalt

def dict_p(all_product,count):
    page = []
    for product_ind in range(0,count):
        dict_page = {}
        product_1 = all_product[product_ind]
        dict_page['name'] = product_1[1]
        dict_page['category'] = product_1[3]
        dict_page['image'] = clear_img(product_1)
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
    brand = product_1[5]
    # print(type(brand))
    if brand == 'Без рукавов' or 'Полная' is True:
       return 'Бренд неизвестен'
    else:
        return brand



@blueprint.route("/next_page", methods=['POST'])
def next_page():
    with open('count.txt','r',encoding='utf-8') as file:
        data = file.read()
        index = int(data)
    products(index)
    index+=12
    with open('count.txt','w',encoding='utf-8') as f:
        f.write(str(index))


@blueprint.route("/prev_page", methods=['POST'])
def prev_page():
    with open('count.txt', 'r', encoding='utf-8') as file:
        data = file.read()
        index = int(data)
    products(index)
    index -= 12
    with open('count.txt', 'w', encoding='utf-8') as f:
        f.write(str(index))

if __name__ == "__main__":
    prev_page()





