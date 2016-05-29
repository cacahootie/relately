SELECT
    {% if query.columns == '*' %}
        *
    {% else %}
	   {{ query.columns|sql_entities|join(',') }}
    {% endif %}
FROM
	{{ query.target }}
{% if query.where %}
    WHERE
    {% for condition in query.where %}
        {{ condition.left_operand|sql_entities }} {{ condition.operator }} %s
    {% endfor %}
{% endif %}