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
        base_update = Stores(title=title,
                             online=online,
                             url=url,
                             name=name,
                             icon=icon)
        db.session.add(base_update)
        db.session.commit()


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


