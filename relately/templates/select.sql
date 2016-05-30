{% macro where_condition(condition) %}
    {{ condition.left_operand|sql_entities }} {{ condition.operator }} %s
{% endmacro %}

{% macro join_condition(condition) %}
    {{ condition.left_operand|sql_entities }}
    {{ condition.operator }}
    {{ condition.right_operand|sql_entities }}
{% endmacro %}

SELECT
    {% if query.columns == '*' %}
        *
    {% else %}
	   {{ query.columns|sql_entities|join(', ') }}
    {% endif %}
FROM
    {% if query.target is string %}
        {{ query.target|sql_entities }}
    {% else %}
	   {{ query.target|sql_entities|join(', ') }}
    {% endif %}

{% if query.join %}
    {% if query.join.on == "natural" %}
        NATURAL
    {% endif %}
    INNER JOIN {{ query.join.target|sql_entities }}
    {% if query.join.on and query.join.on != "natural" %}
        ON
        {{ join_condition(query.join.on) }}
    {% elif query.join.using %}
        USING ({{ query.join.using|sql_entities }})
    {% endif %}
{% elif query.cross_join %}
    CROSS JOIN {{ query.cross_join.target|sql_entities }}
{% endif %}

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