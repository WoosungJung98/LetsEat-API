DROP TABLE IF EXISTS {schema_name}.friends;

CREATE TABLE {schema_name}.friends (
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT null,
  PRIMARY KEY (user_id, friend_id)
);

COMMENT ON COLUMN {schema_name}.friends.user_id IS '22 character unique string user id';
COMMENT ON COLUMN {schema_name}.friends.friend_id IS '22 character unique string of user who is friends with the user id';

