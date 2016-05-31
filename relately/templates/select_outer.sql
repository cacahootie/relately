
SELECT to_json(t) FROM
    (
        {% include 'select.sql' %}
    ) t