ALTER TABLE {{ entity.parent.objid }}
DROP COLUMN {{ entity.name }}
{% if args.if_exists %}
	IF EXISTS
{% endif %}