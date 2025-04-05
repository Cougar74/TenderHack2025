CREATE VIEW сategories_by_date as
	with data_responce_and_rating_to_interaction_result as (
		SELECT 
			  c.name as classification_name
			, CASE 
				WHEN responce is null 
					THEN 'No responce'
				WHEN rating is null 
					THEN 'No rating'
				ELSE 'Rating - ' ||  rating
			  END as interaction_result
			, cast(date_time_create as date) as date_create
			
		FROM public.histories h
		inner join  public.classifications c
			ON c.id = h.classification_id
	), group_interaction_result as
	(
		SELECT
			  classification_name
			, interaction_result
			, date_create
			, count(*) as count
		FROM data_responce_and_rating_to_interaction_result
		group by classification_name, interaction_result, date_create
	)
	SELECT
		*
	FROM group_interaction_result
	order by date_create, classification_name