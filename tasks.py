from celery import Celery
from webapp_stores import create_app
from webapp_stores.parsing_run import butik, randevy, ali
from celery.schedules import crontab
from webapp_stores.proxy import proxy

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

@celery.on_after_configure.connect
def periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(crontab(minute='*/1200'),randevys.s())
    sender.add_periodic_task(crontab(minute='*/1200'),butiks.s())
    sender.add_periodic_task(crontab(minute='*/1200'),alis.s())
    sender.add_periodic_task(crontab(minute='*/2'),proxy_1.s())

