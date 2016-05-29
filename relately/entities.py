
def quote_wrap(s):
	return '"' + s + '"'

class Entity(object):
	"""
	Base class for postgres relational entities such as schemata,
	tables, views, etc...

	"""

	def __init__(self, engine, name):
		self.engine = engine
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

	@staticmethod
	def _process_args(argnames, args, kwargs): # Intentionally not expanded!
		kwargs.update(zip(argnames, args))
		if not set(kwargs.keys()).issubset(argnames):
			raise ValueError(kwargs.keys())
		return kwargs

	def get_sql(self, action, args=None):
		return self.engine.jenv.get_template(self._get_template_name(action)
			).render(
				entity=self,
				args=args
			)

	def create(self):
		self.engine.execute(self.get_sql('create'))
		return self

	drop_args = ('if_exists', 'cascade')
	def drop(self, *args, **kwargs):
		args = self._process_args(self.drop_args, args, kwargs)
		self.engine.execute(self.get_sql('drop', args))
		return None

class ChildEntity(Entity):
	"""Base class for relational entities that are bound to a parent."""

	def __init__(self, engine, parent, name):		
		Entity.__init__(self, engine, name)
		self.parent = parent

	@property
	def objid(self):
		return '.'.join(
			(quote_wrap(self.parent.name), quote_wrap(self.name))
		)
	
class schema(Entity): pass
class table(ChildEntity): pass
class view(ChildEntity): pass
class column(ChildEntity): pass
