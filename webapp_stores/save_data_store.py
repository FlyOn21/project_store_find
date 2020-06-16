from webapp_stores.model import db, Stores,Product

def save_data(store_title, store_online, store_url, store_name, store_icon):
    if Stores.query.filter(Stores.store_url == store_url, Stores.store_name == store_name).count() \
            and Stores.query.filter(Stores.store_online != store_online):
        store = Stores.query.filter(Stores.store_url == store_url,Stores.store_name == store_name).first()
        store.store_online = store_online
        store.store_title = store_title
        store.store_icon = store_icon
        db.session.add(store)
        db.session.commit()
    else:
        base_update = Stores(store_title=store_title,
                             store_online=store_online,
                             store_url=store_url,
                             store_name=store_name,
                             store_icon=store_icon)
        db.session.add(base_update)
        db.session.commit()

def save_data_product_randevouz(product_info):
    if Product.query.filter(Product.product_id_store == product_info['id']).count():
        product = Product.query.filter(Product.product_id_store == product_info['id']).first()
        product.product_store = product_info['store']
        product.product_name = product_info['name']
        product.product_prise_full = float(product_info ['price'])
        product.product_prise_discount = float(product_info ['product_discount'])
        product.product_brand = product_info ['brand']
        product.product_category = product_info ['category']
        product.product_color = product_info ['variant']
        product.product_size = product_info ['size']
        product.product_url = product_info ['product_url']
        product.product_image = product_info ['product_image']
        product.product_gender = product_info['gender']
        db.session.add(product)
        db.session.commit()
    else:
        add_product = Product(product_id_store = product_info['id'],
                              product_store = product_info['store'],
                              product_name = product_info['name'],
                              product_prise_full = float(product_info ['price']),
                              product_prise_discount =float(product_info ['product_discount']),
                              product_brand = product_info ['brand'],
                              product_category = product_info ['category'],
                              product_color = product_info ['variant'],
                              product_size = product_info ['size'],
                              product_url = product_info ['product_url'],
                              product_image = product_info ['product_image'],
                              product_gender = product_info['gender'])
        db.session.add(add_product)
        db.session.commit()



def save_data_product_butik(butik_product_dict):
    if Product.query.filter(Product.product_id_store == butik_product_dict['id']).count():
        product_b = Product.query.filter(Product.product_id_store == butik_product_dict['id']).first()
        product_b.product_store = butik_product_dict['product_store']
        product_b.product_name = butik_product_dict['name']
        product_b.product_prise_full = butik_product_dict ['price']
        product_b.product_prise_discount = butik_product_dict ['product_discount']
        product_b.product_brand = butik_product_dict ['brand']
        product_b.product_category = butik_product_dict ['category']
        product_b.product_color = butik_product_dict ['variant']
        product_b.product_size = butik_product_dict ['size']
        product_b.product_url = butik_product_dict ['product_url']
        product_b.product_image = butik_product_dict ['product_image']
        product_b.product_gender = butik_product_dict['gender']
        db.session.add(product_b)
        db.session.commit()
    else:
        add_product_1 = Product(product_id_store = butik_product_dict['id'],
                              product_store = butik_product_dict['product_store'],
                              product_name = butik_product_dict['name'],
                              product_prise_full = butik_product_dict ['price'],
                              product_prise_discount =butik_product_dict ['product_discount'],
                              product_brand = butik_product_dict ['brand'],
                              product_category = butik_product_dict ['category'],
                              product_color = butik_product_dict ['variant'],
                              product_size = butik_product_dict ['size'],
                              product_url = butik_product_dict ['product_url'],
                              product_image = butik_product_dict ['product_image'],
                              product_gender = butik_product_dict['gender'])
        db.session.add(add_product_1)
        db.session.commit()


def save_data_product_ali(ali_product_dict):
    if Product.query.filter(Product.product_id_store == ali_product_dict['id']).count():
        ali_product_dict = Product.query.filter(Product.product_id_store == ali_product_dict['id']).first()
        ali_product_dict.product_store = ali_product_dict['product_store']
        ali_product_dict.product_name = ali_product_dict['name']
        ali_product_dict.product_prise_full = ali_product_dict ['price']
        ali_product_dict.product_prise_discount = ali_product_dict ['product_discount']
        ali_product_dict.product_brand = ali_product_dict ['brand']
        ali_product_dict.product_category = ali_product_dict ['category']
        ali_product_dict.product_color = ali_product_dict ['variant']
        ali_product_dict.product_size = ali_product_dict ['size']
        ali_product_dict.product_url = ali_product_dict ['product_url']
        ali_product_dict.product_image = ali_product_dict ['product_image']
        ali_product_dict.product_delivery = ali_product_dict['delivery']
        ali_product_dict.product_gender = ali_product_dict['gender']
        ali_product_dict.product_other = ali_product_dict['other_store']
        db.session.add(ali_product_dict)
        db.session.commit()
    else:
        add_product_1 = Product(product_id_store = ali_product_dict['id'],
                              product_store = ali_product_dict['product_store'],
                              product_name = ali_product_dict['name'],
                              product_prise_full = ali_product_dict ['price'],
                              product_prise_discount =ali_product_dict ['product_discount'],
                              product_brand = ali_product_dict ['brand'],
                              product_category = ali_product_dict ['category'],
                              product_color = ali_product_dict ['variant'],
                              product_size = ali_product_dict ['size'],
                              product_url = ali_product_dict ['product_url'],
                              product_image = ali_product_dict ['product_image'],
                              product_delivery = ali_product_dict['delivery'],
                              product_gender = ali_product_dict['gender'],
                              product_other = ali_product_dict['other_store'] )
        db.session.add(add_product_1)
        db.session.commit()