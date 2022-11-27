-- SUPERUSER PERMISSION REQUIRED
CREATE EXTENSION IF NOT EXISTS pg_trgm;

DROP INDEX IF EXISTS {schema_name}.idx_user_name_cnt_map_on_user_name_lower;

CREATE INDEX idx_user_name_cnt_map_on_user_name_lower
ON {schema_name}.user_name_cnt_map USING gin(lower(user_name) gin_trgm_ops);
