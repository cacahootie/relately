
from jinja2 import Environment, FileSystemLoader, Template

jenv = Environment(loader=FileSystemLoader('./templates'))

def _quote_wrap(s):
	return '"' + s + '"'

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

	def _get_template_name(self, action):
		return "{}/{}.sql".format(action, self.entity_type)

	def create_sql(self):
		return jenv.get_template(self._get_template_name('create')
			).render(entity=self)

	def drop_sql(self, *args, **kwargs):
		argnames = ('if_exists','cascade')
		kwargs.update(zip(argnames, args))
		if not set(kwargs.keys()).issubset(argnames):
			raise ValueError(kwargs.keys())
		return jenv.get_template(self._get_template_name('drop')
			).render(
				entity=self,
				args=kwargs
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
