import os

basedir = os.path.abspath(os.path.dirname(__file__))
base = os.path.join(basedir,'..','webapp_store.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ base
