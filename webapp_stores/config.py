import os

# Форматы URL-доступа к базам данных в Flask-SQLAlchemy : sqlite:////absolute/path/to/database
basedir = os.path.abspath(os.path.dirname(__file__))
base = os.path.join(basedir,'..','webapp_store.db')
print(base)
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ base
