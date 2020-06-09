from webapp_stores import create_app
from webapp_stores.store_butik_ru import Butik_ru
from webapp_stores.srote_rendezvous import Rendezvous
from webapp_stores.store_aliexpress import Aliexpress

app = create_app()
with app.app_context():
     butik = Butik_ru().get_butik_data()
     randezvous = Rendezvous().get_butik_data()
     ali = Aliexpress().get_butik_data()


