
from jinja2 import Template

def _quote_wrap(s):
	return '"' + s + '"'

class Entity(object):
	"""
	Base class for postgres relational entities such as databases,
	tables, views, etc...

	"""
	create_template_string = "CREATE {{ entity_type }} {{ objid }}"
	drop_template_string = """
		DROP {{ entity_type }}
		{% if if_exists %}
			IF EXISTS
		{% endif %}
		{{ objid }}
		{% if cascade %}
			CASCADE
		{% endif %}
	"""
	
	def __init__(self, name):
		self.parent = None
		self.name = name

	@property
	def objid(self):
		return self.name

	def create_sql(self):
		return self.create_template.render(
			entity_type=type(self).__name__,
			name=self.name,
			objid=self.objid,
			parent=self.parent)

	def drop_sql(self, if_exists=False, cascade=False):
		return self.drop_template.render(
			entity_type=type(self).__name__,
			name=self.name,
			objid=self.objid,
			parent=self.parent,
			if_exists=if_exists,
			cascade=cascade
		)

class ChildEntity(Entity):
	"""Base class for relational entities that are bound to a parent."""

	def __init__(self, parent, name):		
		Entity.__init__(self, name)
		self.parent = parent

	@property
	def objid(self):
		return '.'.join(
			(_quote_wrap(self.parent.name), _quote_wrap(self.name))
		)
	
class schema(Entity):
	create_template = Template(Entity.create_template_string)
	drop_template = Template(Entity.drop_template_string)

class table(ChildEntity):
	create_template = Template(Entity.create_template_string + "()")
	drop_template = Template(Entity.drop_template_string)

class view(ChildEntity):
	pass

class column(ChildEntity):
	_alter_table = "ALTER TABLE {{ parent.objid }} "
	create_template_string = _alter_table + " ADD COLUMN {{ name }} TEXT"
	drop_template_string = _alter_table + """
		DROP COLUMN {{ name }}
		{% if if_exists %}
			IF EXISTS
		{% endif %}
	"""
	create_template = Template(create_template_string)
	drop_template = Template(drop_template_string)
