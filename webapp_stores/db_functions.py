from webapp_stores.model import db, Stores,Product


def save_data(title, online, url, name, icon):
    if Stores.query.filter(Stores.url == url, Stores.name == name).count() \
            and Stores.query.filter(Stores.online != online):
        store = Stores.query.filter(Stores.url == url,Stores.name == name).first()
        store.online = online
        store.title = title
        store.icon = icon
        db.session.add(store)
        db.session.commit()
    else:
        stores = Stores(title=title,
                             online=online,
                             url=url,
                             name=name,
                             icon=icon)
        db.session.add(stores)
        db.session.commit()


def save_data_product(product_dict):

    if Product.query.filter(Product.id_product == product_dict['id']).count():
        product_b = Product.query.filter(Product.id_product == product_dict['id']).first()
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
        if product_dict['product_store'] == 'Aliexpress':
            store = 1
        elif product_dict['product_store'] == 'Butik.ru':
            store = 3
        elif product_dict['product_store'] == "Randevu":
            store = 2
        add_product_1 = Product(id_product=product_dict['id'],
                                store_id=store,
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


