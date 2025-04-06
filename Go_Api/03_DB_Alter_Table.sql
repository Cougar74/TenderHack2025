SELECT setval('histories_id_seq', (SELECT max(id) + 1 FROM public.histories));


ALTER TABLE histories
ADD responce_json json NULL;

UPDATE histories
SET responce_json = to_json(responce::text);

ALTER TABLE histories
DROP COLUMN responce;

ALTER TABLE histories
RENAME COLUMN responce_json to responce;



delete FROM public.histories
Where date_time_create < '2025-03-01 00:00:00';


with t1 as (
	SELECT
		   user_uuid as old_uuid
		 , cast(date_time_create as date) as date_create
		 , gen_random_uuid() as new_uuid
		
	FROM public.histories
	GROUP BY user_uuid, cast(date_time_create as date)
)
update public.histories
	SET user_uuid = t1.new_uuid
FROM t1
Where     user_uuid = t1.old_uuid
	  and cast(date_time_create as date) = t1.date_create