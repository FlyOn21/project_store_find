from webapp_stores import create_app
from webapp_stores.stores.stores import get_butik_data
from webapp_stores.stores.butik import get_full_butik
from webapp_stores.db_functions import save_data_product


def butik():
    app = create_app()
    with app.app_context():
        butik_status = get_butik_data()
        if butik_status is not False:
            get_full_butik()
            # save_data_product(get_full_butik())
        else:
            print('Бутик был недоступен, обновление базы не выполнено')
            pass


if __name__ == '__main__':
    c = butik()