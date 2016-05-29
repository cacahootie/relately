{% macro where_condition(condition) %}
    {{ condition.left_operand|sql_entities }} {{ condition.operator }} %s
{% endmacro %}

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
        {% if condition.left_operand %}
            {{ where_condition(condition) }}
            {% if not loop.last %}
                AND
            {% endif %}
        {% endif %}
    {% endfor %}
{% elif query.any %}
    WHERE
    {% for condition in query.any %}
        {% if condition.left_operand %}
            {{ where_condition(condition) }}
            {% if not loop.last %}
                OR
            {% endif %}
        {% endif %}
    {% endfor %}
{% endif %}