from webapp_stores import create_app
from webapp_stores.stores.ali import Aliexpress
from webapp_stores.stores.butik import get_full_butik
from webapp_stores.stores.randevu import get_full_randevu
from webapp_stores.stores.stores import get_ali_data, get_butik_data, get_randevu_data

def run():
    app = create_app()
    with app.app_context():
        ali_status = get_ali_data()
        randezvous_status = get_randevu_data()
        butik_status = get_butik_data()
        if ali_status is not False:
            ali = Aliexpress()
            ali.page_ali()
        else:
            print('Алиекспрес был недоступен, обновление базы не выполнено')
            pass

        if randezvous_status is not False:
            get_full_randevu()
        else:
            print('Рандеву был недоступен, обновление базы не выполнено')
            pass

        if butik_status is not False:
            get_full_butik()
        else:
            print('Бутик был недоступен, обновление базы не выполнено')
            pass

    # Добавление в базу данных Product по ссылке - Бутик
    # dict=get_butik_product('https://www.butik.ru/products/muzhchinam-odezhda-dzhempery-i-svitery-dzhempery-armani-exchange-3hzm1c-zml5z-1510-dzhemper/')
    # save_data_product(dict)

    # Добавление в базу данных Product всех товаров Бутик
    # save_data_product(get_full_butik())

    # Добавление в базу данных Product по ссылке - Бутик
    # dict = get_randevu_product('https://www.rendez-vous.ru/catalog/female/sandalii/mm6_maison_margiela_s59wp0029_goluboy-2463124/')
    # save_data_product(dict)

    # Добавление в базу данных Product всех товаров Бутик
    # save_data_product(get_full_randevu())

if __name__ == '__main__':
    c = run()
