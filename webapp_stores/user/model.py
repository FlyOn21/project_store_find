from webapp_stores.stores.model import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """
    Класс описывает базу данных, содержащих информацию о пользователях сервиса
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    surname = db.Column(db.String, nullable=False)
    username = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String)
    is_active = db.Column(db.Boolean, nullable=False)
    send_mail = db.Column(db.Boolean, default=True)
    role = db.Column(db.String, index=True)
    search = db.Column(db.String, index=True)
    interesting_products = db.relationship('InterestingProduct', backref='client')

    def __repr__(self):
        return f'id:{self.id}, User:{self.username},role:{self.role}, active:{self.is_active},mail:{self.email},' \
               f'send_mail:{self.send_mail},name:{self.name},surname:{self.surname}'

    def save_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'


class Check_product_all(db.Model):
    """Модель для временного хранения дайнных проверки"""
    id = db.Column(db.Integer, primery_key=True)
    int_product = db.Column(db.String)
    email = db.Column(db.String)
    url = db.Column(db.Text)

    def __repr__(self):
        print(f'id: {self.id}, id_int_product: {self.id_int_product}, email: {self.email}, url: {self.url}')


class InterestingProduct(db.Model):
    """
    Класс описывает базу данных, содержащих информацию о товарах, которые интересны пользователям
    """
    __tablename__ = 'interesting_products'
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    id_store = db.Column(db.String, nullable=False)

    brand = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=True)
    category_detailed = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String, nullable=True)

    url = db.Column(db.Text, nullable=False)

    prise_full = db.Column(db.String, nullable=False)
    prise_discount = db.Column(db.String, nullable=True)
    price_interesting = db.Column(db.String, nullable=True)

    size_available = db.Column(db.String, nullable=True)
    size_possible = db.Column(db.String, nullable=True)
    size_interesting = db.Column(db.String, nullable=True)

    color = db.Column(db.Text, nullable=True)
    color_possible = db.Column(db.Text, nullable=True)
    color_interesting = db.Column(db.Text, nullable=True)

    user_email = db.Column(db.String, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    notification_sent = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'Store : {self.store}, name: {self.name},' \
               f' url: {self.url}'
