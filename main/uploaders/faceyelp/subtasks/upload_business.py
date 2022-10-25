from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time
import ujson
from psycopg2.extras import execute_values


class UploadBusiness(BaseTask):
  def __init__(self, conn, schema_name, sql_path, file_path):
    super().__init__(conn, schema_name, sql_path, file_path)

  def execute(self):
    print("\n====================Start Uploading Business====================\n")
    start_time = time.time()

    INSERT_LIMIT = 1000
    column_names = ["business_id","business_name","address","city","state","postal_code",
                    "latitude","longitude","stars","review_count","is_open","attributes","categories","hours"]

    f = open(f"{self.file_path}/json_datasets/yelp_academic_dataset_business.json", "r")
    business_list = []
    for line in f:
      if len(business_list) == INSERT_LIMIT:
        execute_values(
          self.cursor,
          f"INSERT INTO {self.schema_name}.business ({', '.join(column_names)}) VALUES %s",
          business_list)
        business_list.clear()
      loaded_line = ujson.loads(line)
      processed_line = []
      for col in column_names:
        match col:
          case "business_name":
            dat = loaded_line["name"]
          case "state":
            dat = loaded_line[col] if len(loaded_line[col]) == 2 else None
          case "is_open":
            dat = bool(loaded_line[col])
          case "categories":
            dat = loaded_line[col].split(', ') if loaded_line[col] else []
          case "attributes" | "hours":
            dat = ujson.dumps(loaded_line[col])
          case other:
            dat = loaded_line[col]
        processed_line.append(dat)
      business_list.append(tuple(processed_line))
    f.close()

    if len(business_list) > 0:
      execute_values(
        self.cursor,
        f"INSERT INTO {self.schema_name}.business ({', '.join(column_names)}) VALUES %s",
        business_list)

    end_time = time.time()
    print(f"Business Uploading time: {end_time-start_time:.2f}secs\n")
    print("====================Finished Uploading Business====================\n")

    print("\n====================Start Indexing Business====================\n")
    start_time = time.time()
    query = load_sql(os.path.join(self.sql_path, "add_index", "index_business.sql"),
                     schema_name=self.schema_name)
    self.cursor.execute(query)
    end_time = time.time()
    print(f"Business Indexing time: {end_time-start_time:.2f}secs\n")
    print("\n====================Finished Indexing Business====================\n")
