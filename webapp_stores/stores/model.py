from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stores(db.Model):
    """
    Класс описывает базу данных, содержащих информацию о магазинах
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    online = db.Column(db.Boolean, nullable=False)
    url = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    icon = db.Column(db.String, nullable=True)
    # products = db.relationship('Product', backref='stores')


    def __repr__(self):
        if self.store_online == True:
            store_online = 'ON-LINE'
        else:
            store_online = 'CLOSE'
        return f'Store ID: {self.id}, title: {self.title}, ' \
               f'url: {self.url}, {store_online},{self.icon} '



class Product(db.Model):
    """
    Класс описывает базу данных, содержащих информацию о товаре с подробной детализацией
    """
    id = db.Column(db.Integer,primary_key=True)
    store = db.Column(db.Integer, db.ForeignKey('stores.id'))
    name = db.Column(db.String,nullable=False)
    id_product= db.Column(db.String,nullable=False,unique=True)
    prise_full =db.Column(db.String,nullable=False)
    prise_discount = db.Column(db.String,nullable=True)
    brand = db.Column(db.String,nullable=True)
    category = db.Column(db.String, nullable=True)
    category_detailed = db.Column(db.Text, nullable=True)
    color = db.Column(db.Text,nullable=True)
    size = db.Column(db.String,nullable=True)
    url = db.Column(db.Text,nullable=False)
    image = db.Column(db.Text,nullable=True)
    gender = db.Column(db.String,nullable=True)
    delivery = db.Column(db.String,nullable=True)
    other = db.Column(db.Text,nullable=True)
    stores = db.relationship('Stores') #backref='products'

    def __repr__(self):
        return f"{self.id}|{self.name}|{self.url}|{self.category}|{self.image}|{self.brand}|{self.stores.name}|{self.size}"




