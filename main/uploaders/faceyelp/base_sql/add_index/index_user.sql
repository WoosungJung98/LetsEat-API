DROP INDEX IF EXISTS {schema_name}.idx_user_on_user_id_email;

CREATE UNIQUE INDEX idx_user_on_user_id_email
ON {schema_name}.user (user_id, email);
