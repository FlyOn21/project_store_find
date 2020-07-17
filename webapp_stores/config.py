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
MAIL_SERVER = 'smtp.sendgrid.net'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'flyon21'
MAIL_PASSWORD = 'GSG.xFI-EcotTi-VzJ5EqzYshw.P5lWKje-OLBLN1_jRPbBUFv-UeuP4sY0iQlg5RB4UX0'

# administrator list
ADMINS = ['zhogolevpv@gmail.com']

#Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
