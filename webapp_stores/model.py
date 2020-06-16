from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    product_store = db.Column(db.String,nullable=False)
    product_name = db.Column(db.String,nullable=False)
    product_id_store = db.Column(db.String,nullable=False,unique=True)
    product_prise_full =db.Column(db.String,nullable=False)
    product_prise_discount = db.Column(db.String,nullable=True)
    product_brand = db.Column(db.String,nullable=True)
    product_category = db.Column(db.String, nullable=True)
    product_color = db.Column(db.String,nullable=True)
    product_size = db.Column(db.String,nullable=True)
    product_url = db.Column(db.Text,nullable=False)
    product_image = db.Column(db.Text,nullable=True)
    product_gender = db.Column(db.String,nullable=True)
    product_delivery = db.Column(db.String,nullable=True)
    product_other = db.Column(db.Text,nullable=True)

    def __repr__(self):
        return f'Store ID: {self.product_id_store}, brand: {self.product_brand},' \
               f' url: {self.product_url},{self.product_category}'



class Stores(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String, nullable=False, unique=True)
    store_online = db.Column(db.Boolean, nullable=False)
    store_url = db.Column(db.String, nullable=False, unique=True)
    store_title = db.Column(db.String, nullable=False)
    store_icon = db.Column(db.String, nullable=True)

    def __repr__(self):
        if self.store_online == True:
            store_online = 'ON-LINE'
        else:
            store_online = 'CLOSE'
        return f'Store ID: {self.store_id}, title: {self.store_title}, ' \
               f'url: {self.store_url}, {store_online},{self.store_icon} '
