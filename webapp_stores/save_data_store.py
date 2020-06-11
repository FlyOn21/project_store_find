from webapp_stores.model import db, Stores

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
        base_update = Stores(store_title=store_title, store_online=store_online, store_url=store_url,
                                   store_name=store_name, store_icon=store_icon)
        db.session.add(base_update)
        db.session.commit()
