from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
        return f'Store ID: {self.store_id}, title: {self.store_title}, url: {self.store_url}, {store_online},{self.store_icon} '
