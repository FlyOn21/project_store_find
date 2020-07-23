from webapp_stores.config import CELERY_BROKER_URL

enable_utc = True
timezone = 'Europe/Riga'
task_time_limit = 172800
broker_url = 'redis://localhost:6379/0'
imports = ('tasks',)
task_annotations = {'*': {'rate_limit': '10/s'}}
