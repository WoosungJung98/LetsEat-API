DROP TABLE IF EXISTS {schema_name}.business;

CREATE TABLE {schema_name}.business (
  business_id CHAR(22) PRIMARY KEY NOT NULL,
  business_name VARCHAR(255) NOT null,
  address VARCHAR(255) NOT null,
  city VARCHAR(255) NOT null,
  state CHAR(2),
  postal_code VARCHAR(255),
  latitude double precision not null,
  longitude double precision not null,
  stars real not null,
  review_count int not null,
  is_open boolean not null,
  attributes json,
  categories varchar(255)[] not null,
  hours json  
);

COMMENT ON COLUMN {schema_name}.business.business_id IS '22 character unique string business id';
COMMENT ON COLUMN {schema_name}.business.business_name IS 'the business name';
COMMENT ON COLUMN {schema_name}.business.address IS 'the full address of the business';
COMMENT ON COLUMN {schema_name}.business.city IS 'the city';
COMMENT ON COLUMN {schema_name}.business.state IS '2 character state code, if applicable';
COMMENT ON COLUMN {schema_name}.business.postal_code IS 'the postal code';
COMMENT ON COLUMN {schema_name}.business.latitude IS 'latitude';
COMMENT ON COLUMN {schema_name}.business.longitude IS 'longitude';
COMMENT ON COLUMN {schema_name}.business.stars IS 'star rating, rounded to half-stars';
COMMENT ON COLUMN {schema_name}.business.review_count IS 'number of reviews';
COMMENT ON COLUMN {schema_name}.business.is_open IS '0 or 1 for closed or open, respectively';
COMMENT ON COLUMN {schema_name}.business.attributes IS 'business attributes to values';
COMMENT ON COLUMN {schema_name}.business.categories IS 'an array of strings of business categories';
COMMENT ON COLUMN {schema_name}.business.hours IS 'an object of key day to value hours, hours are using a 24hr clock';
