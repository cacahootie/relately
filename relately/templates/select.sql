SELECT
	{{ query.columns|join(',') }}
FROM
	{{ query.target }}
