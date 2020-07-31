.PHONY: all clean migrations

all: delay clean migrations tasks

clean:

delay:
	@echo wait 15 sec
	@sleep 15

migrations:
	@flask db upgrade
	@echo flask upgraded

tasks:
	@echo running celery
	@celery celery -A tasks worker --loglevel=INFO && celery -A tasks beat && celery flower -A tasks worker --address=0.0.0.0 --port=5555

