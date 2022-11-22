DROP TABLE IF EXISTS {schema_name}.user_name_cnt_map;

CREATE TABLE {schema_name}.user_name_cnt_map (
  user_name VARCHAR(255) PRIMARY KEY NOT NULL,
  cnt INT NOT NULL
);

COMMENT ON COLUMN {schema_name}.user_name_cnt_map.user_name IS 'the users first and last name';
COMMENT ON COLUMN {schema_name}.user_name_cnt_map.cnt IS 'the number of users associated with user_name';
