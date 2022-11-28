DROP TABLE IF EXISTS {schema_name}.cities;

CREATE TABLE {schema_name}.cities (
  state CHAR(22) PRIMARY KEY NOT NULL,
  city CHAR(22) NOT NULL,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL
);

COMMENT ON COLUMN {schema_name}.cities.state IS '22 character unique string of state that the city is located in';
COMMENT ON COLUMN {schema_name}.cities.city IS '22 character string of city name';
COMMENT ON COLUMN {schema_name}.cities.latitude IS 'latitude';
COMMENT ON COLUMN {schema_name}.cities.longitude IS 'longitude';
