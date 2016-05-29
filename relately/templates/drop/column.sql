ALTER TABLE {{ entity.parent.objid }}
DROP COLUMN {{ entity.name|sql_entities }}
{% if args.if_exists %}
	IF EXISTS
{% endif %}