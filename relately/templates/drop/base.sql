DROP {{ entity_type }}
{% if if_exists %}
	IF EXISTS
{% endif %}
{{ objid }}
{% if cascade %}
	CASCADE
{% endif %}
