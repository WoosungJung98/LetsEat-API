from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time
import ujson
from psycopg2.extras import execute_values

class UploadPhoto(BaseTask):
    def __init__(self, conn, schema_name, sql_path, file_path):
        super().__init__(conn, schema_name, sql_path, file_path)
    
    def execute(self):
        print("\n====================Start Uploading Photo====================\n")
        start_time = time.time()

        INSERT_LIMIT = 1000
        column_names = ["photo_id","business_id", "caption", "label"]
        f = open(f"{self.file_path}/json_datasets/photos.json", "r")
        photo_list = []
        for line in f:
            if len(photo_list) == INSERT_LIMIT:
                print(f"Insert {INSERT_LIMIT} photos")
                execute_values(
                self.cursor,
                f"INSERT INTO {self.schema_name}.photo ({', '.join(column_names)}) VALUES %s ON CONFLICT DO NOTHING",
                photo_list)
                photo_list.clear()
            loaded_line = ujson.loads(line)
            processed_line = []
            for col in column_names:
                dat = loaded_line[col]
                processed_line.append(dat)
            photo_list.append(tuple(processed_line))

        f.close()
        if len(photo_list) > 0:
            print(f"Insert {len(photo_list)} photos")
            execute_values(
                self.cursor,
                f"INSERT INTO {self.schema_name}.photo ({', '.join(column_names)}) VALUES %s ON CONFLICT DO NOTHING",
                photo_list)

        end_time = time.time()
        print(f"Photo Uploading time: {end_time-start_time:.2f}secs\n")
        print("====================Finished Uploading Photo====================\n")

        print("\n====================Start Indexing Photo====================\n")
        start_time = time.time()
        query = load_sql(os.path.join(self.sql_path, "add_index", "index_photo.sql"),
                        schema_name=self.schema_name)
        self.cursor.execute(query)
        end_time = time.time()
        print(f"Photo Indexing time: {end_time-start_time:.2f}secs\n")
        print("\n====================Finished Indexing Photo====================\n")
