from flask import Blueprint, render_template, flash, url_for
from werkzeug.utils import redirect
from webapp_stores.stores.model import Product
from webapp_stores import create_app


blueprint = Blueprint('product', __name__,)


@blueprint.route("/products")
def products():
    app = create_app()
    with app.app_context():
        product = Product.query.offset(10).limit(10).all()
        product_page = str(product)
        product_page_clear = product_page.split('!,')
        all_product_page = []
        for product_dict in product_page_clear:
            # print(product_dict)
            product_dict_1 = product_dict.strip('!]')
            product_dict_2 = product_dict_1+']'
            print(product_dict_2)

            all_product_page.append(product_dict_2)
        # print(all_product_page)

if __name__ == "__main__":
    products()