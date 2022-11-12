celery -A main.uploaders.common.celery_worker.celery multi restart worker -c 1 --pidfile="./uploaders.pid" --logfile="files/log/uploaders.log"
