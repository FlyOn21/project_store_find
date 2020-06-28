from webapp_stores import create_app
from webapp_stores.stores.stores import get_ali_data
from webapp_stores.stores.ali import Aliexpress


def ali():
    app = create_app()
    with app.app_context():
        ali_status = get_ali_data()
        if ali_status is not False:
            ali = Aliexpress()
            ali.page_ali()
        else:
            print('Алиекспрес был недоступен, обновление базы не выполнено')
            pass



if __name__ == '__main__':
    c = ali()