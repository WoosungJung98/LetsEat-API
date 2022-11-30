DROP TABLE IF EXISTS {schema_name}.city;

CREATE TABLE {schema_name}.city(
  city_id SERIAL PRIMARY KEY NOT NULL,
  state CHAR(22) NOT NULL,
  city_name CHAR(22) NOT NULL,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL
);

COMMENT ON COLUMN {schema_name}.city.city_id IS 'autoincrementing id for city';
COMMENT ON COLUMN {schema_name}.city.state IS '22 character unique string of state that the city is located in';
COMMENT ON COLUMN {schema_name}.city.city_name IS '22 character string of city name';
COMMENT ON COLUMN {schema_name}.city.latitude IS 'latitude';
COMMENT ON COLUMN {schema_name}.city.longitude IS 'longitude';
