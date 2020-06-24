from celery import Celery
from webapp_stores import create_app
from webapp_stores.stores.ali import Aliexpress
from celery.schedules import crontab

celery = Celery('tasks', broker='redis://localhost:6379/0')
flask = create_app()

@celery.task()
def store():
    with flask.app_context():
        c = Aliexpress()
        c.get_ali_data()

@celery.on_after_configure.connect
def periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(crontab(minute='*/1'),store.s())

