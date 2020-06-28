from webapp_stores.stores.model import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model,UserMixin):
    id  = db.Column(db.Integer, primary_key = True)
    name = db.Column (db.String,nullable = False)
    email = db.Column(db.String,nullable = False,unique = True)
    surname = db.Column(db.String,nullable = False)
    username = db.Column(db.String,index = True,unique = True)
    password = db.Column(db.String)
    is_active = db.Column(db.Boolean,nullable = False)
    role = db.Column(db.String,index = True)

    def __repr__(self):
        return f'User {self.username},role {self.role},id {self.id}, active {self.is_active}'

    def save_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role =='user'

class InterestingProduct(db.Model):
    __tablename__ = 'interesting_products'
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    id_store = db.Column(db.String, nullable=False)

    url = db.Column(db.Text, nullable=False)

    prise_full = db.Column(db.String, nullable=False)
    prise_discount = db.Column(db.String, nullable=True)
    price_interesting = db.Column(db.String, nullable=True)

    size_available = db.Column(db.String, nullable=True)
    size_possible=db.Column(db.String, nullable=True)
    size_interesting=db.Column(db.String, nullable=True)

    color = db.Column(db.Text, nullable=True)
    color_possible=db.Column(db.Text, nullable=True)
    color_interesting=db.Column(db.Text, nullable=True)

    user_email=db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'Store : {self.store}, name: {self.name},' \
               f' url: {self.url}'