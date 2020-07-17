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
MAIL_SERVER = 'smtp.ukr.net'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'zhogolev@ukr.net'
MAIL_PASSWORD = 'fMDTnoKbzfNTUORn'
# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_USERNAME = 'zhogolevpv@gmail.com'
# MAIL_PASSWORD = 'Gfdtk2105'
# MAIL_SERVER = 'smtp.sendgrid.net'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_USERNAME = 'apikey'
# MAIL_PASSWORD = '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'

# administrator list
ADMINS = ['zhogolevpv@gmail.com']

#Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
