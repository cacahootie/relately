
from jinja2 import Template

class Entity(object):
	"""
	Base class for postgres relational entities such as databases,
	tables, views, etc...

	"""
	create_template = Template("CREATE {{ entity_type }} {{ name }}")
	drop_template = Template("""
		DROP {{ entity_type }}
		{% if if_exists %}
			IF EXISTS
		{% endif %}
		{{ name }}
	""")

	def __init__(self, name, create=False):
		self.name = name

	@property
	def create_sql(self):
		return self.create_template.render(
			entity_type=self.entity_type, name=self.name)

	@property
	def drop_sql(self, if_exists=False):
		return self.drop_template.render(
			entity_type=self.entity_type,
			name=self.name,
			if_exists=if_exists
		)

class Schema(Entity):
	entity_type = "schema"

class Table(Entity):
	pass

class View(Entity):
	pass
