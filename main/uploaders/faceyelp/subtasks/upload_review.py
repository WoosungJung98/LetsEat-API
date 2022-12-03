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
        print("\n====================Start Uploading Review====================\n")
        start_time = time.time()

        INSERT_LIMIT = 5000
        column_names = ["review_id", "user_id", "business_id", "stars", 
                        "body", "useful", "funny", "cool", "created_at", "updated_at"]

        f = open(f"{self.file_path}/json_datasets/yelp_academic_dataset_review.json", "r")
        review_list = []
        for line in f:
            if len(review_list) == INSERT_LIMIT:
                print(f"Insert {INSERT_LIMIT} reviews")
                execute_values(
                    self.cursor,
                    f"INSERT INTO {self.schema_name}.review ({', '.join(column_names)}) VALUES %s",
                    review_list)
                review_list.clear()
            loaded_line = ujson.loads(line)
            processed_line = []
            for col in column_names:
                match col:
                    case "created_at":
                        dat = loaded_line["date"]
                    case "updated_at":
                        dat = loaded_line["date"]
                    case "body":
                        dat = loaded_line["text"]
                    case other:
                        dat = loaded_line[col]
                processed_line.append(dat)
            review_list.append(tuple(processed_line))
        f.close()

        if len(review_list) > 0:
            print(f"Insert {len(review_list)} reviews")
            execute_values(
                self.cursor,
                f"INSERT INTO {self.schema_name}.review ({', '.join(column_names)}) VALUES %s",
                review_list)

        end_time = time.time()
        print(f"Review Uploading time: {end_time-start_time:.2f}secs\n")
        print("====================Finished Uploading Review====================\n")

        print("\n====================Start Indexing Review====================\n")
        start_time = time.time()
        query = load_sql(os.path.join(self.sql_path, "add_index", "index_review.sql"),
                         schema_name=self.schema_name)
        self.cursor.execute(query)
        end_time = time.time()
        print(f"Review Indexing time: {end_time-start_time:.2f}secs\n")
        print("\n====================Finished Indexing Review====================\n")
