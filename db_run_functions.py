from webapp_stores import create_app

from webapp_stores.stores.butik import get_full_butik, get_butik_product
from webapp_stores.stores.randevu import get_full_randevu, get_randevu_product
from webapp_stores.db_functions import save_data_product, save_interesting_product
from webapp_stores.stores.stores import Butik_ru, Rendezvous



app = create_app()
with app.app_context():
     #ali = Aliexpress().get_ali_data()
     # randezvous = Rendezvous().get_randevu_data()
     # butik = Butik_ru().get_butik_data()


     # Добавление в базу данных Product по ссылке - Бутик
     # url='https://www.butik.ru/products/zhenshchinam-odezhda-mayki-i-topy-tommy-sport-s10s100451-dw5-desert-sky-top/'
     # dict=get_butik_product(url)
     # save_data_product(dict)

     # Добавление в базу данных Product всех товаров Бутик
     # save_data_product(get_full_butik())

     # Добавление в базу данных Product по ссылке - Бутик
     # dict = get_randevu_product('https://www.rendez-vous.ru/catalog/female/sandalii/mm6_maison_margiela_s59wp0029_goluboy-2463124/')
     # save_data_product(dict)

     # Добавление в базу данных Product всех товаров Бутик
     # save_data_product(get_full_randevu())

     # Добавление в клиентскую базу данных
     # $dict=get_butik_product('https://www.butik.ru/products/zhenshchinam-obuv-sandalii-guess-fl6ofe-ele03-black-sandalii/')
     #save_interesting_product(dict,email='nat@mail.ru',size_interesting='38')









