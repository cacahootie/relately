DROP {{ entity.entity_type|sql_entities }}
{% if args.if_exists %}
	IF EXISTS
{% endif %}
{{ entity.objid }}
{% if args.cascade %}
	CASCADE
{% endif %}
