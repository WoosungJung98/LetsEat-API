from main.uploaders.common.base_uploader import BaseUploader
from main.uploaders.faceyelp.subtasks.init_schema import InitSchema
from main.uploaders.faceyelp.subtasks.base_table import BaseTable
from main.uploaders.faceyelp.subtasks.upload_business import UploadBusiness
import time


class FaceYelpUploader(BaseUploader):
  def __init__(self, db):
    super().__init__(db)

    self.sql_path = "./main/uploaders/faceyelp/base_sql"
    self.file_path = "./main/uploaders/faceyelp/files"

  def upload(self, schema_name):
    start_time = time.time()

    InitSchema(self.conn, schema_name, self.sql_path, self.file_path).execute()
    BaseTable(self.conn, schema_name, self.sql_path, self.file_path).execute()

    UploadBusiness(self.conn, schema_name, self.sql_path, self.file_path).execute()

    end_time = time.time()

    print(f"Total time: {end_time-start_time:.2f}secs")
