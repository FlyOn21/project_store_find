from webapp_stores import create_app
from webapp_stores.stores.randevu import get_full_randevu
from webapp_stores.stores.stores import get_randevu_data
from webapp_stores.db_functions import save_data_product


def rand():
    app = create_app()
    with app.app_context():
        randezvous_status = get_randevu_data()
        if randezvous_status is not False:
            get_full_randevu()
            save_data_product(get_full_randevu())
        else:
            print('Рандеву был недоступен, обновление базы не выполнено')
            pass


if __name__ == '__main__':
    c = rand()
