DROP TABLE IF EXISTS {schema_name}.photo;

CREATE TABLE {schema_name}.photo (
  photo_id  CHAR(22) PRIMARY KEY NOT NULL,
  business_id CHAR(22) NOT NULL,
  caption VARCHAR(255), 
  label VARCHAR(255)
);

COMMENT ON COLUMN {schema_name}.photo.photo_id IS '22 character unique string photo id';
COMMENT ON COLUMN {schema_name}.photo.business_id IS '22 character string business id associated with the photo';
COMMENT ON COLUMN {schema_name}.photo.caption IS 'caption of the photo';
COMMENT ON COLUMN {schema_name}.photo.label IS 'label of the photo';
