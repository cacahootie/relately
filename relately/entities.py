
from jinja2 import Environment, FileSystemLoader, Template

jenv = Environment(loader=FileSystemLoader('./templates'))

def _quote_wrap(s):
	return '"' + s.replace('"',r'\"') + '"'

class Entity(object):
	"""
	Base class for postgres relational entities such as schemata,
	tables, views, etc...

	"""

	def __init__(self, name):
		self.parent = None
		self.name = name

	@property
	def objid(self):
		return self.name

	@property
	def entity_type(self):
		return type(self).__name__

	def create_sql(self):
		return jenv.get_template("create/{}.sql".format(self.entity_type)).render(
			entity_type=self.entity_type,
			name=self.name,
			objid=self.objid,
			parent=self.parent
		)

	def drop_sql(self, if_exists=False, cascade=False):
		return jenv.get_template("drop/{}.sql".format(self.entity_type)).render(
			entity_type=self.entity_type,
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
	
class schema(Entity): pass
class table(ChildEntity): pass
class view(ChildEntity): pass
class column(ChildEntity): pass
