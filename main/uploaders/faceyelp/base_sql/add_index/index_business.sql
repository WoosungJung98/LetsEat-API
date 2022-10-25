-- SUPERUSER PERMISSION REQUIRED
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS earthdistance cascade;

DROP INDEX IF EXISTS {schema_name}.idx_business_on_business_name_lower;
DROP INDEX IF EXISTS {schema_name}.idx_business_on_latlon_earthdistance;

CREATE INDEX idx_business_on_business_name_lower
ON {schema_name}.business USING gin(lower(business_name) gin_trgm_ops);

CREATE INDEX idx_business_on_latlon_earthdistance
ON {schema_name}.business USING gist(ll_to_earth(latitude, longitude));
