from webapp_stores import db, create_app
# from webapp_stores.model import InterestingProduct
from sqlalchemy import create_engine
from webapp_stores.config import SQLALCHEMY_DATABASE_URI

#delete one table
# engine=create_engine(SQLALCHEMY_DATABASE_URI)
# InterestingProduct.__table__.drop(engine)


#delete all tables
db.drop_all(app=create_app())

#create all tables
db.create_all(app=create_app())
