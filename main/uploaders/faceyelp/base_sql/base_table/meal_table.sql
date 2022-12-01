DROP TABLE IF EXISTS {schema_name}.meal;

CREATE TABLE {schema_name}.meal (
  meal_id SERIAL PRIMARY KEY NOT NULL,
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT NULL,
  restaurant_id CHAR(22) NOT NULL,
  meal_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL
);

DROP INDEX IF EXISTS {schema_name}.uniq_meal_constraint;
CREATE UNIQUE INDEX uniq_meal_constraint ON {schema_name}.meal (user_id, friend_id, restaurant_id, meal_at);

COMMENT ON COLUMN {schema_name}.meal.meal_id IS 'auto incrementing primary key for meal';
COMMENT ON COLUMN {schema_name}.meal.user_id IS 'user_id for the meal inviter';
COMMENT ON COLUMN {schema_name}.meal.friend_id IS 'user_id for the meal invitee';
COMMENT ON COLUMN {schema_name}.meal.restaurant_id IS 'id of the restaurant for the meal';
COMMENT ON COLUMN {schema_name}.meal.meal_at IS 'timestamp of when the meal will occur';
COMMENT ON COLUMN {schema_name}.meal.created_at IS 'timestamp of when the meal request was initiated';
