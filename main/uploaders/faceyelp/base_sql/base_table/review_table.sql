DROP TABLE IF EXISTS {schema_name}.review;

CREATE TABLE {schema_name}.review (
  review_id CHAR(22) PRIMARY KEY NOT NULL,
  user_id CHAR(22) NOT NULL,
  business_id CHAR(22) NOT NULL,
  stars INT NOT NULL,
  body TEXT,
  useful INT NOT NULL,
  funny INT NOT NULL,
  cool INT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

COMMENT ON COLUMN {schema_name}.review.review_id IS '22 character unique review id';
COMMENT ON COLUMN {schema_name}.review.user_id IS '22 character unique user id, maps to the user in user.json';
COMMENT ON COLUMN {schema_name}.review.business_id IS '22 character business id, maps to business in business.json';
COMMENT ON COLUMN {schema_name}.review.stars is 'star rating';
COMMENT ON COLUMN {schema_name}.review.body is 'the text of review itself';
COMMENT ON COLUMN {schema_name}.review.useful is 'number of useful votes received';
COMMENT ON COLUMN {schema_name}.review.funny is 'number of funny votes received';
COMMENT ON COLUMN {schema_name}.review.cool is 'number of cool votes received';
COMMENT ON COLUMN {schema_name}.review.created_at is 'time when review was written';
COMMENT ON COLUMN {schema_name}.review.updated_at is 'time when review was updated';
