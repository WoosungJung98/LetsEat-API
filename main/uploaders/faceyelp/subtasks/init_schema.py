from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time


class InitSchema(BaseTask):
  def __init__(self, conn, schema_name, sql_path, file_path):
    super().__init__(conn, schema_name, sql_path, file_path)

  def execute(self):
    print(f"\n====================Start Making {self.schema_name} Schema====================\n")
    start_time = time.time()
    query = load_sql(os.path.join(self.sql_path, "init_schema.sql"),
                     schema_name=self.schema_name)
    self.cursor.execute(query)
    end_time = time.time()
    print(f"Schema Making time: {end_time-start_time:.2f}secs\n")
    print("====================Finished Making Schema====================\n")
