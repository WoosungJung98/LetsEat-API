from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time

class ExtractUserNameCntMap(BaseTask):
    def __init__(self, conn, schema_name, sql_path, file_path):
        super().__init__(conn, schema_name, sql_path, file_path)
    
    def execute(self):
        print("\n====================Start Extracting User Name Count Map====================\n")
        start_time = time.time()
        query = load_sql(os.path.join(self.sql_path, "extract_data", "make_user_name_cnt_map.sql"),
                         schema_name=self.schema_name)
        self.cursor.execute(query)
        end_time = time.time()
        print(f"User Name Count Map Extraction time: {end_time-start_time:.2f}secs\n")
        print("====================Finished Extracting User Name Count Map====================\n")

        print("\n====================Start Indexing User Name Count Map====================\n")
        start_time = time.time()
        query = load_sql(os.path.join(self.sql_path, "add_index", "index_user_name_cnt_map.sql"),
                         schema_name=self.schema_name)
        self.cursor.execute(query)
        end_time = time.time()
        print(f"User Name Count Map Indexing time: {end_time-start_time:.2f}secs\n")
        print("\n====================Finished Indexing User Name Count Map====================\n")
