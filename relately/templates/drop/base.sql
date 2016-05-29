DROP {{ entity.entity_type }}
{% if args.if_exists %}
	IF EXISTS
{% endif %}
{{ entity.objid }}
{% if args.cascade %}
	CASCADE
{% endif %}
