from main import read_config
from celery import Celery

cfg = read_config()
celery = Celery("uploader.tasks",
                broker=cfg.config["CELERY_BROKER_REDIS_UPLOADERS"])


def stop_celery_task(task_id):
  celery.control.revoke(task_id, terminate=True, signal="SIGKILL")
