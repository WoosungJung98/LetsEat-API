import sys
import os
sys.path.append(os.getcwd())

import argparse

from main.uploaders.common.db import UploaderDB

from main.uploaders.faceyelp.faceyelp import FaceYelpUploader


def start(schema_name):
  print("FaceYelp Uploads Start", schema_name)
  db = UploaderDB()
  uploader = FaceYelpUploader(db)
  uploader.upload(schema_name)
  db.close()


if __name__ == '__main__':
  argparser = argparse.ArgumentParser(description=__doc__)
  argparser.add_argument(
      dest='schema_name',
      metavar='schema_name',
      default=None,
      help='Schema Name')
  args = argparser.parse_args()

  schema_name = args.schema_name
  start(schema_name)
