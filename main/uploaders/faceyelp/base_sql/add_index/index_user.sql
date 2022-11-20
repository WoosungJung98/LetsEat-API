-- SUPERUSER PERMISSION REQUIRED
CREATE EXTENSION IF NOT EXISTS pg_trgm;

DROP INDEX IF EXISTS {schema_name}.idx_user_on_user_id_email;
DROP INDEX IF EXISTS {schema_name}.idx_user_on_user_name_lower;

CREATE UNIQUE INDEX idx_user_on_user_id_email
ON {schema_name}.user (user_id, email);

CREATE INDEX idx_user_on_user_name_lower
ON {schema_name}.user USING gin(lower(user_name) gin_trgm_ops);
