from flask import Blueprint, render_template, flash, url_for
from werkzeug.utils import redirect
from webapp_stores.stores.model import Product
from webapp_stores import create_app
import json


blueprint = Blueprint('product', __name__,)


@blueprint.route("/products")
def products():
    app = create_app()
    with app.app_context():
        product = Product.query.offset(0).limit(10).all()
        all_product = []
        for index in range(0,10):
            all_product.append(str(product[index]))
        print(all_product[0])
        f = json.loads(all_product[0])
        print(f)


@blueprint.route("/next_page", methods=['POST'])
def next_page():
    pass

@blueprint.route("/prev_page", methods=['POST'])
def prev_page():
    pass

if __name__ == "__main__":
    products()




