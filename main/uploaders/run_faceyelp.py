import sys
import os
sys.path.append(os.getcwd())

import argparse

from main.uploaders.common.celery import celery
from main.uploaders.common.db import UploaderDB

from main.uploaders.faceyelp.faceyelp import FaceYelpUploader


@celery.task(name="uploader.tasks.run_faceyelp", bind=True)
def start(self, schema_name):
  print("FaceYelp Uploads Start", schema_name)
  task_id = self.request.id
  print("task_id", task_id)
  db = UploaderDB()
  uploader = FaceYelpUploader(db)
  uploader.upload(schema_name)
  db.close()


def start_delayed(schema_name):
  start.delay(schema_name)


if __name__ == '__main__':
  argparser = argparse.ArgumentParser(description=__doc__)
  argparser.add_argument(
      dest='schema_name',
      metavar='schema_name',
      default=None,
      help='Schema Name')
  argparser.add_argument(
      '--no-celery',
      dest='celery',
      action='store_false',
      default=True,
      help='no celery. direct execution'
  )
  args = argparser.parse_args()

  schema_name = args.schema_name
  if args.celery:
    start_delayed(schema_name)
  else:
    start(schema_name)
