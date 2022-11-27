from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time
import ujson
from psycopg2.extras import execute_values

class UploadReview(BaseTask):
    def __init__(self, conn, schema_name, sql_path, file_path):
        super().__init__(conn, schema_name, sql_path, file_path)
    
    def execute(self):
        print("\n====================Start Uploading Reviews====================\n")
        start_time = time.time()

        INSERT_LIMIT = 5000
        column_names = ["review_id","user_id", "business_id", "stars", 
                        "date", "text", "useful", "funny", "cool"]
        f = open(f"{self.file_path}/json_datasets/yelp_academic_dataset_review.json", "r")
        reviews_list = []
        processed_line = []
        for line in f:
            #if len(reviews_list) == INSERT_LIMIT:
                #print("insert")
                #execute_values(
                #self.cursor,
                #f"INSERT INTO {self.schema_name}.review ({', '.join(column_names)}) VALUES %s ON CONFLICT DO NOTHING",
                #reviews_list)
                #reviews_list.clear()
            loaded_line = ujson.loads(line)
            processed_line = []
            for col in column_names:
                dat = loaded_line[col]
                processed_line.append(dat)
            reviews_list.append(tuple(processed_line))

        f.close()
        #if len(reviews_list) > 0:
            #execute_values(
                #self.cursor,
                #f"INSERT INTO {self.schema_name}.review ({', '.join(column_names)}) VALUES %s",
                #reviews_list)

        end_time = time.time()
        print(f"User Uploading time: {end_time-start_time:.2f}secs\n")
        print("====================Finished Uploading Reviews====================\n")



     