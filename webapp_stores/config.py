import os

# Форматы URL-доступа к базам данных в Flask-SQLAlchemy : sqlite:////absolute/path/to/database
PROXY_API_URL = 'http://hidemy.name/ru/api/proxylist.php?out=plain&' \
                'type=h&maxtime=80&code=714073796989396'
basedir = os.path.abspath(os.path.dirname(__file__))
base = os.path.join(basedir,'..','webapp_store.db')

print(base)
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ base
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "k;lkl;wkermw;emr.,wmerl;k;lm/.ml;';l';lm/.m,;lk;lk;lkm,m"

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'zhogolevpv@gmail.com'
MAIL_PASSWORD = 'Gfdtk2105'

# administrator list
ADMINS = ['zhogolevpv@gmail.com']