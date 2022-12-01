DROP TABLE IF EXISTS {schema_name}.meal_request;

CREATE TABLE {schema_name}.meal_request (
  meal_request_id SERIAL PRIMARY KEY NOT NULL,
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT NULL,
  restaurant_id CHAR(22) NOT NULL,
  meal_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  accepted_at TIMESTAMP,
  ignored_at TIMESTAMP
);

DROP INDEX IF EXISTS {schema_name}.uniq_active_meal_request_constraint;
CREATE UNIQUE INDEX uniq_active_meal_request_constraint ON {schema_name}.meal_request (user_id, friend_id, restaurant_id, meal_at)
WHERE accepted_at IS NULL AND ignored_at IS NULL;

COMMENT ON COLUMN {schema_name}.meal_request.meal_request_id IS 'auto incrementing primary key for meal request';
COMMENT ON COLUMN {schema_name}.meal_request.user_id IS 'user_id for the user initiating the meal request';
COMMENT ON COLUMN {schema_name}.meal_request.friend_id IS 'user_id for the user receiving the meal request';
COMMENT ON COLUMN {schema_name}.meal_request.restaurant_id IS 'id of the restaurant for which the meal request is being sent';
COMMENT ON COLUMN {schema_name}.meal_request.meal_at IS 'timestamp of when the meal will occur';
COMMENT ON COLUMN {schema_name}.meal_request.created_at IS 'timestamp of when the meal request was initiated';
COMMENT ON COLUMN {schema_name}.meal_request.accepted_at IS 'timestamp of when the meal request was accepted';
COMMENT ON COLUMN {schema_name}.meal_request.ignored_at IS 'timestamp of when the meal request was ignored';
