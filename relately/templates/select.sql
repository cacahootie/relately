SELECT
	{% for column in query.columns %}
		{{ column }}{% if not loop.last %},{% endif %}
	{% endfor %}
FROM
	{{ query.target }}
