from celery import Celery
from webapp_stores import create_app
import db_run_functions
from celery.schedules import crontab
from webapp_stores.proxy import proxy

celery = Celery('tasks', broker='redis://localhost:6379/0')
flask = create_app()

@celery.task
def store():
    with flask.app_context():
        db_run_functions.run()

@celery.task
def proxy():
    with flask.app_context():
        proxy()


@celery.on_after_configure.connect
def periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(crontab(minute='*/1200'),store.s())
    sender.add_periodic_task(crontab(minute='*/5'),store.s())

