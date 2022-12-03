DROP TABLE IF EXISTS {schema_name}.friend_request;

CREATE TABLE {schema_name}.friend_request (
  friend_request_id SERIAL PRIMARY KEY NOT NULL,
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  accepted_at TIMESTAMP,
  ignored_at TIMESTAMP
);

DROP INDEX IF EXISTS {schema_name}.uniq_active_friend_request_constraint;
CREATE UNIQUE INDEX uniq_active_friend_request_constraint ON {schema_name}.friend_request (user_id, friend_id)
WHERE accepted_at IS NULL AND ignored_at IS NULL;

COMMENT ON COLUMN {schema_name}.friend_request.friend_request_id IS 'auto incrementing primary key for friend request';
COMMENT ON COLUMN {schema_name}.friend_request.user_id IS 'user_id for the user initiating the friend request';
COMMENT ON COLUMN {schema_name}.friend_request.friend_id IS 'user_id for the user receiving the friend request';
COMMENT ON COLUMN {schema_name}.friend_request.created_at IS 'timestamp of when the friend request was initiated';
COMMENT ON COLUMN {schema_name}.friend_request.accepted_at IS 'timestamp of when the friend request was accepted';
COMMENT ON COLUMN {schema_name}.friend_request.ignored_at IS 'timestamp of when the friend request was ignored';
