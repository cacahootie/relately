ALTER TABLE {{ parent.objid }}
DROP COLUMN {{ name }}
{% if if_exists %}
	IF EXISTS
{% endif %}