from webapp_stores import create_app
from webapp_stores.store_butik_ru import Butik_ru

app = create_app()
with app.app_context():
     butik = Butik_ru()
     butik.get_butik_data()

