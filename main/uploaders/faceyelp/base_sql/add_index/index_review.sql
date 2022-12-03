DROP INDEX IF EXISTS {schema_name}.idx_review_on_business_id_created_at;
DROP INDEX IF EXISTS {schema_name}.idx_review_on_business_id_stars_created_at;

CREATE INDEX idx_review_on_business_id_created_at
ON {schema_name}.review (business_id, created_at);

CREATE INDEX idx_review_on_business_id_stars_created_at
ON {schema_name}.review (business_id, stars, created_at);
