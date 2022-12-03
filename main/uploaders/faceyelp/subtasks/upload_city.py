from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time
import ujson
from psycopg2.extras import execute_values

class UploadCity(BaseTask):
    def __init__(self, conn, schema_name, sql_path, file_path):
        super().__init__(conn, schema_name, sql_path, file_path)
    
    def execute(self):
        print("\n====================Start Uploading Cities====================\n")
        start_time = time.time()
        INSERT_LIMIT = 10
        column_names = ["state","city_name", "latitude", "longitude"]
        f = open(f"{self.file_path}/json_datasets/city_coordinates.json", "r")
        city_list = []
        processed_line = []
        for line in f:
            if len(city_list) == INSERT_LIMIT:
                execute_values(
                self.cursor,
                f"INSERT INTO {self.schema_name}.city ({', '.join(column_names)}) VALUES %s ON CONFLICT DO NOTHING",
                city_list)
                city_list.clear()
            loaded_line = ujson.loads(line)
            processed_line = []
            print(processed_line)
            for col in column_names:
                dat = loaded_line[col]
                processed_line.append(dat)
            city_list.append(tuple(processed_line))
        if len(city_list) > 0:
            print(f"Insert {len(city_list)} city")
            execute_values(
                self.cursor,
                f"INSERT INTO {self.schema_name}.city ({', '.join(column_names)}) VALUES %s ON CONFLICT DO NOTHING",
                city_list)
        f.close()

        end_time = time.time()
        print(f"User Uploading time: {end_time-start_time:.2f}secs\n")
        print("====================Finished Uploading City Coordinates====================\n")


        