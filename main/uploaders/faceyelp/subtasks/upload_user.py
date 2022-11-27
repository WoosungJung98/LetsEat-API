from main.uploaders.faceyelp.subtasks.base_task import BaseTask
from main.uploaders.common.query import load_sql
import os
import time
import ujson
from psycopg2.extras import execute_values
import random

class UploadUser(BaseTask):
    def __init__(self, conn, schema_name, sql_path, file_path):
        super().__init__(conn, schema_name, sql_path, file_path)
    
    def execute(self):
        print("\n====================Start Uploading User====================\n")
        start_time = time.time()

        INSERT_LIMIT_USER = 1000
        INSERT_LIMIT_FRIEND = 10000
        column_names = ["user_id","user_name","email","profile_photo","avatar_num",
                        "password_digest","review_count","useful","funny","cool",
                        "created_at","updated_at"]
        f = open(f"{self.file_path}/json_datasets/yelp_academic_dataset_user.json", "r")
        user_list = []
        processed_line = []
        for line in f:
            if len(user_list) == INSERT_LIMIT_USER:
                print(f"Insert {INSERT_LIMIT_USER} users")
                execute_values(
                    self.cursor,
                    f"INSERT INTO {self.schema_name}.user ({', '.join(column_names)}) VALUES %s",
                    user_list)
                user_list.clear()
            loaded_line = ujson.loads(line)
            user_id = loaded_line["user_id"]
            processed_line = []
            for col in column_names:
                match col:
                    case "user_name":
                        dat = loaded_line["name"]
                    case "created_at":
                        dat = loaded_line["yelping_since"] 
                    case "email":
                        dat = f"{user_id}@gmail.com"
                    case "profile_photo":
                        dat = None
                    case "avatar_num":
                        dat = random.randint(1, 24)
                    case "password_digest":
                        dat = None
                    case "updated_at":
                        dat = loaded_line["yelping_since"]
                    case other:
                        dat = loaded_line[col]
                processed_line.append(dat)
            user_list.append(tuple(processed_line))
            friends = loaded_line["friends"]
            friends = friends.split(", ")
            cols = ["user_id", "friend_id"]
            friend_list = []
            for friend in friends:
                if len(friend_list) == INSERT_LIMIT_FRIEND:
                    # print(f"Insert {INSERT_LIMIT_FRIEND} friends for {user_id}")
                    execute_values(
                        self.cursor,
                        f"INSERT INTO {self.schema_name}.friend ({', '.join(cols)}) VALUES %s",
                        friend_list)
                    friend_list.clear()
                if len(friend) == 22:
                    friend_list.append((user_id, friend))
            if len(friend_list) > 0:
                # print(f"Insert {len(friend_list)} friends for {user_id}")
                execute_values(
                    self.cursor,
                    f"INSERT INTO {self.schema_name}.friend ({', '.join(cols)}) VALUES %s",
                    friend_list)
        f.close()
        if len(user_list) > 0:
            execute_values(
                self.cursor,
                f"INSERT INTO {self.schema_name}.user ({', '.join(column_names)}) VALUES %s",
                user_list)

        end_time = time.time()
        print(f"User Uploading time: {end_time-start_time:.2f}secs\n")
        print("====================Finished Uploading User====================\n")

        print("\n====================Start Indexing User====================\n")
        start_time = time.time()
        query = load_sql(os.path.join(self.sql_path, "add_index", "index_user.sql"),
                         schema_name=self.schema_name)
        self.cursor.execute(query)
        end_time = time.time()
        print(f"User Indexing time: {end_time-start_time:.2f}secs\n")
        print("\n====================Finished Indexing User====================\n")
