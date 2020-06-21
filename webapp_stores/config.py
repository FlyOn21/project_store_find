import os

# Форматы URL-доступа к базам данных в Flask-SQLAlchemy : sqlite:////absolute/path/to/database
PROXY_API_URL = 'http://hidemy.name/ru/api/proxylist.php?out=plain&' \
                'type=h&maxtime=100&code=714073796989396'
basedir = os.path.abspath(os.path.dirname(__file__))
base = os.path.join(basedir,'..','webapp_store.db')
print(base)
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ base

