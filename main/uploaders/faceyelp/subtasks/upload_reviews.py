from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time
import ujson
from psycopg2.extras import execute_values

class UploadReviews(BaseTask):
    def __init__(self, conn, schema_name, sql_path, file_path):
        super().__init__(conn, schema_name, sql_path, file_path)
    
    def execute(self):
        print("\n====================Start Uploading Reviews====================\n")
        start_time = time.time()

        INSERT_LIMIT = 1000
        column_names = ["photo_id","business_id", "caption", "label"]
        f = open(f"{self.file_path}/json_datasets/photos.json", "r")
        photos_list = []
        processed_line = []
        for line in f:
            if len(photos_list) == INSERT_LIMIT:
                print("insert")
                execute_values(
                self.cursor,
                f"INSERT INTO {self.schema_name}.photos ({', '.join(column_names)}) VALUES %s ON CONFLICT DO NOTHING",
                photos_list)
                photos_list.clear()
            loaded_line = ujson.loads(line)
            processed_line = []
            for col in column_names:
                dat = loaded_line[col]
                processed_line.append(dat)
            photos_list.append(tuple(processed_line))

        f.close()
        if len(photos_list) > 0:
            execute_values(
                self.cursor,
                f"INSERT INTO {self.schema_name}.photos ({', '.join(column_names)}) VALUES %s",
                photos_list)

        end_time = time.time()
        print(f"User Uploading time: {end_time-start_time:.2f}secs\n")
        print("====================Finished Uploading Photos====================\n")