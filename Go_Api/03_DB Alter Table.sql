SELECT setval('histories_id_seq', (SELECT max(id)+1 FROM public.histories));


ALTER TABLE histories
ADD responce_json json NULL;

UPDATE histories
SET responce_json = to_json(responce::text)

ALTER TABLE histories
DROP COLUMN responce;

ALTER TABLE histories
RENAME COLUMN responce_json to responce;