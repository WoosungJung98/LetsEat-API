from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time


class BaseTable(BaseTask):
  def __init__(self, conn, schema_name, sql_path, file_path):
    super().__init__(conn, schema_name, sql_path, file_path)

  def execute(self):
    print("\n====================Start Making All Tables====================\n")
    tables_to_create = [
        #"business",
        "review",
        "user",
        "friends",
    ]
    for tablename in tables_to_create:
      start_time = time.time()
      print(f"Start making {tablename} table!")
      query = load_sql(os.path.join(self.sql_path, "base_table", f"{tablename}_table.sql"),
                       schema_name=self.schema_name)
      self.cursor.execute(query)
      print(f"Finished making {tablename} table!")
      end_time = time.time()
      print(f"{tablename} table Making time: {end_time-start_time:.2f}secs\n")
    print("====================Finished Making All Tables====================\n")
