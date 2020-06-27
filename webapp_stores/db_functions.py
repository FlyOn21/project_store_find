from webapp_stores.model import db, Stores, Product, InterestingProduct


def save_data(title, online, url, name, icon):
    if Stores.query.filter(Stores.url == url, Stores.name == name).count() \
            and Stores.query.filter(Stores.online != online):
        store = Stores.query.filter(Stores.url == url, Stores.name == name).first()
        store.online = online
        store.title = title
        store.icon = icon
        db.session.add(store)
        db.session.commit()
    else:
        base_update = Stores(title=title,
                             online=online,
                             url=url,
                             name=name,
                             icon=icon)
        db.session.add(base_update)
        db.session.commit()


# Сохранение данных в общую базу данных
def save_data_product(product_dict):
    if Product.query.filter(Product.id_store == product_dict['id']).count():
        product_b = Product.query.filter(Product.id_store == product_dict['id']).first()
        product_b.prise_full = product_dict['price']
        product_b.prise_discount = product_dict['product_discount']
        product_b.color = product_dict['color']
        product_b.size = str(product_dict['size'])
        product_b.url = product_dict['product_url']
        product_b.image = product_dict['product_image']
        product_b.delivery = (product_dict['delivery'] if 'delivery' in product_dict else None)
        db.session.add(product_b)
        db.session.commit()
    else:
        add_product_1 = Product(id_store=product_dict['id'],
                                store=product_dict['product_store'],
                                name=product_dict['name'],
                                prise_full=product_dict['price'],
                                prise_discount=product_dict['product_discount'],
                                brand=product_dict['brand'],
                                category=product_dict['category'],
                                category_detailed=product_dict['category_detailed'],
                                color=product_dict['color'],
                                size=str(product_dict['size']),
                                url=product_dict['product_url'],
                                image=product_dict['product_image'],
                                delivery=(product_dict['delivery'] if 'delivery' in product_dict else None),
                                other=(product_dict['other'] if 'other' in product_dict else None),
                                gender=product_dict['gender'])

        db.session.add(add_product_1)
        db.session.commit()


# Сохранение данных в клиентскую базу данных
def save_interesting_product(product_dict, email=None, price_interesting=None, color_interesting=None, size_interesting=None):

    # Если данный товар уже отслеживается этим клиентом в этом размере (нужно доработать если отслеживается еще по цвету или цене)
    # Нужно добработаь если товара вообще нет в наличие на сайте - словарь может не работать
    if InterestingProduct.query.filter(InterestingProduct.id_store == product_dict['id'], InterestingProduct.user_email == email, InterestingProduct.size_interesting == size_interesting).count():
        interesting_product=InterestingProduct.query.filter(InterestingProduct.id_store == product_dict['id'], InterestingProduct.user_email == email, InterestingProduct.size_interesting == size_interesting).first()
        interesting_product.size_available=str(product_dict['size'])
        interesting_product.price_discount=product_dict['product_discount']
        interesting_product.color=product_dict['color']

    else:
        interesting_product=InterestingProduct(
        id_store=product_dict['id'],
        store=product_dict['product_store'],
        name=product_dict['name'],

        url=product_dict['product_url'],

        prise_full=product_dict['price'],
        prise_discount=product_dict['product_discount'],
        price_interesting=price_interesting,

        size_available = str(product_dict['size']),
        size_possible=str(product_dict['size_possible']) if 'size_possible' in product_dict else None,
        size_interesting=size_interesting,

        color = product_dict['color'],
        color_possible=None,
        color_interesting=color_interesting,

        user_email=email)

    db.session.add(interesting_product)
    db.session.commit()

