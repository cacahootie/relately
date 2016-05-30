{% macro where_condition(condition) %}
    {{ condition.left_operand|sql_entities }} {{ condition.operator }} %s
{% endmacro %}

{% macro join_condition(condition) %}
    {{ condition.left_operand|sql_entities }}
    {{ condition.operator }}
    {{ condition.right_operand|sql_entities }}
{% endmacro %}

{% macro where_clause(clause, connector, negate=False) %}
    {% for condition in clause %}
        {% if negate %}
            NOT
        {% endif %}
        {% if condition.left_operand %}
            {{ where_condition(condition) }}
            {% if not loop.last %}
                {{ connector }}
            {% endif %}
        {% endif %}
    {% endfor %}
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
    {% if query.join.outer %}
        {{ query.join.outer|valid_joins }} JOIN
    {% else %}
        INNER JOIN     
    {% endif %}
    {{ query.join.target|sql_entities }}
    {% if query.join.on and query.join.on != "natural" %}
        ON {{ join_condition(query.join.on) }}
    {% elif query.join.using %}
        USING ({{ query.join.using|sql_entities }})
    {% endif %}
{% endif %}

{% if query.all or query.any or query.none %}
    WHERE
{% endif%}
{% for clause in query._where %}
    ({{ where_clause(*clause) }})
    {% if not loop.last %}
        AND
    {% endif %}
{% endfor %}

{% if query.group_by %}
    GROUP BY {{ query.group_by|sql_entities|join(', ') }}
{% endif %}

{% if query.having_all or query.having_any or query.having_none %}
    HAVING
{% endif %}
{% for clause in query._having %}
    ({{ where_clause(*clause) }})
    {% if not loop.last %}
        AND
    {% endif %}
{% endfor %}