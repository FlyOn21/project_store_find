from webapp_stores import create_app
from webapp_stores.store_butik_ru import Butik_ru
from webapp_stores.srote_rendezvous import Rendezvous
from webapp_stores.store_aliexpress import Aliexpress
# from webapp_stores.all_product_randevuze import get_full_randevu,full_randevu_man,full_randevu_women,full_randevu_unisex,full_randevu_chaildren
# from webapp_stores.all_product_butik import page_number_url,full_butik_man,full_butik_women
# from webapp_stores.all_product_ali import page_ali,full_ali_women,full_ali_man


app = create_app()
with app.app_context():
     ali = Aliexpress().get_ali_data()
     randezvous = Rendezvous().get_randevu_data()
     butik = Butik_ru().get_butik_data()









