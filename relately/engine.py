
from functools import partial

import psycopg2
import psycopg2.extras

import entities

class Engine(object):
    """Encapsulate access to a database."""

    def __init__(self):
        """Establish the database connection."""
        self.conn = psycopg2.connect(self.conn_string)

    def execute(self,stmt,params=None):
        """Execute the statement in a transaction, parameters optional."""
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
                args = (stmt,) if params is None else (stmt,params)
                try:
                    c.execute(*args)
                except:
                    print self.mogrify(*args)
                    raise

                try:
                    return list(c) if c.rowcount != -1 else None
                except psycopg2.ProgrammingError:
                    print self.mogrify(*args)
                    raise

    def mogrify(self,stmt,params=None):
        """Combines statement and params to string for human use."""
        with self.conn as conn:
            with conn.cursor() as c:
                return c.mogrify(stmt,params)

    @property
    def conn_string(self):
        return 'dbname=relately user=relately'

    def create_entity(self, entity_type, name, *args, **kwargs):
        e = getattr(entities, entity_type)(name, *args, **kwargs)
        self.execute(e.create_sql())
        return e

    def drop_entity(
            self, entity_type, p1, p2=None, if_exists=False, cascade=False):

        if p2 is None:
            e = getattr(entities, entity_type)(p1)
        else:
            e = getattr(entities, entity_type)(p1, p2)
        self.execute(e.drop_sql(if_exists, cascade))

    _etypes = ('schema', 'table', 'view', 'column')
    _create_func_set = set('create_'+x for x in _etypes)
    _drop_func_set = set('drop_'+x for x in _etypes)
    def __getattr__(self, attr):
        if attr in self._create_func_set:
            return partial(self.create_entity, attr.replace('create_',''))
        elif attr in self._drop_func_set:
            return partial(self.drop_entity, attr.replace('drop_',''))
        raise AttributeError(
            type(self).__name__ +  " object has no attribute: " + attr
        )
