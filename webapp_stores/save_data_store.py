from webapp_stores.model import db, Model_stores

def save_data(store_title, store_online, store_url, store_name, store_icon):
    if Model_stores.query.filter(Model_stores.store_url == store_url, Model_stores.store_name == store_name).count() \
            and Model_stores.query.filter(Model_stores.store_online!=store_online) :

        # Model_stores.query.filter(Model_stores.store_online!=store_online).update({'store_online': store_online})
        # Model_stores.query.filter(Model_stores.store_title!=store_title).update({'store_title': store_title})
        # Model_stores.query.filter(Model_stores.store_icon!=store_icon).update({'store_icon': store_icon})
        # db.session.commit()
    else:
        base_update = Model_stores(store_title=store_title, store_online=store_online, store_url=store_url,
                                   store_name=store_name, store_icon=store_icon)
        db.session.add(base_update)
        db.session.commit()
