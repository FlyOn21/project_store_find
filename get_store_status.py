from webapp_stores import create_app
from webapp_stores.store_butik_ru import Butik_ru
from webapp_stores.srote_rendezvous import Rendezvous
from webapp_stores.store_aliexpress import Aliexpress
from webapp_stores.all_product_randevuze import get_full_randevu,full_randevu_man,full_randevu_women,full_randevu_unisex,full_randevu_chaildren
from webapp_stores.all_product_butik import page_number_url,full_butik_man,full_butik_women

app = create_app()
with app.app_context():
     butik = Butik_ru().get_butik_data()
     randezvous = Rendezvous().get_butik_data()
     ali = Aliexpress().get_butik_data()
     # product_ali = page_ali(full_ali_man,full_ali_women)
     product_butik = page_number_url(full_butik_man, full_butik_women)
     product_randevous = get_full_randevu(full_randevu_man,full_randevu_women,full_randevu_unisex,full_randevu_chaildren)








