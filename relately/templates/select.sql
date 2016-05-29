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
{% if query.all or query.any or query.none %}
    WHERE
{% endif%}
{% if query.all %}
    {% for condition in query.all %}
        {% if condition.left_operand %}
            {{ where_condition(condition) }}
            {% if not loop.last %}
                AND
            {% endif %}
        {% endif %}
    {% endfor %}
{% elif query.any %}
    {% for condition in query.any %}
        {% if condition.left_operand %}
            {{ where_condition(condition) }}
            {% if not loop.last %}
                OR
            {% endif %}
        {% endif %}
    {% endfor %}
{% elif query.none %}
    {% for condition in query.none %}
        NOT 
        {% if condition.left_operand %}
            {{ where_condition(condition) }}
            {% if not loop.last %}
                AND
            {% endif %}
        {% endif %}
    {% endfor %}
{% endif %}