INSERT INTO {schema_name}.user_name_cnt_map (user_name, cnt)
SELECT u.user_name, count(*)
FROM faceyelp.user u
GROUP BY u.user_name;
