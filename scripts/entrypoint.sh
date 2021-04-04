#!/bin/bash
celery --app FLASK_APP --broker CELERY_BROKER_URL tasks beat --loglevel=INFO
celery --app FLASK_APP --broker CELERY_BROKER_URL tasks worker --loglevel=INFO