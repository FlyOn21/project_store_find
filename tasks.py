from celery import Celery
from webapp_stores import create_app
from webapp_stores.parsing_run import butik, randevy, ali
from celery.schedules import crontab
from webapp_stores.proxy import proxy
from webapp_stores.mail.views import email,reset_pass_mail
from webapp_stores.check.check_product import insteresting_product_check

celery = Celery('tasks', broker='redis://localhost:6379/0')
flask = create_app()

@celery.task
def proxy_1():
    with flask.app_context():
        proxy.proxy()

@celery.task
def randevys():
    with flask.app_context():
        randevy.rand()

@celery.task
def butiks():
    with flask.app_context():
        butik.butik()

@celery.task
def alis():
    with flask.app_context():
        ali.ali()

@celery.task
def email_send(e_mail,find_size,product):
    email(e_mail,find_size,product)

@celery.task
def email_reset_pass(e_mail,url):
    reset_pass_mail(e_mail,url)

@celery.task
def insteresting_product_check_do():
    insteresting_product_check()


@celery.on_after_configure.connect
def periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(crontab(minute='*/1200'),randevys.s())
    sender.add_periodic_task(crontab(minute='*/1200'),butiks.s())
    sender.add_periodic_task(crontab(minute='*/1200'),alis.s())
    sender.add_periodic_task(crontab(minute='*/2'),proxy_1.s())
    # sender.add_periodic_task(crontab(minute='*/20'), insteresting_product_check_do.s())

if __name__ == '__main__':
    alis()
    # randevys()
    # butiks()

