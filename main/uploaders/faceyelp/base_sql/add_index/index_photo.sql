DROP INDEX IF EXISTS {schema_name}.idx_photo_on_business_id;

CREATE INDEX idx_photo_on_business_id
ON {schema_name}.photo (business_id);
