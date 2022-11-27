DROP TABLE IF EXISTS {schema_name}.friend;

CREATE TABLE {schema_name}.friend (
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT NULL,
  viewed_at TIMESTAMP,
  PRIMARY KEY (user_id, friend_id)
);

COMMENT ON COLUMN {schema_name}.friend.user_id IS '22 character unique string user id';
COMMENT ON COLUMN {schema_name}.friend.friend_id IS '22 character unique string of user who is friends with the user id';
