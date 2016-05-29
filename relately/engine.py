
from functools import partial

import psycopg2
import psycopg2.extras

import entities

class Engine(object):

    def __init__(self):
        self.conn = psycopg2.connect(self.conn_string)

    def execute(self,stmt,params=None):
        """Execute the statement in a transaction, parameters optional."""
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
                args = (stmt,) if params is None else (stmt,params)
                #print self.mogrify(*args)
                try:
                    c.execute(*args)
                except psycopg2.IntegrityError:
                    raise errors.IntegrityError
                except psycopg2.DataError:
                    print self.mogrify(*args)
                    raise
                except psycopg2.ProgrammingError:
                    #print self.mogrify(*args)
                    raise

                try:
                    return list(c)
                except psycopg2.ProgrammingError:
                    return None

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

    _create_func_set = set('create_'+x for x in ('schema', 'table', 'view'))
    _drop_func_set = set('drop_'+x for x in ('schema', 'table', 'view'))
    def __getattr__(self, attr):
        if attr in self._create_func_set:
            return partial(self.create_entity, attr.replace('create_',''))
        elif attr in self._drop_func_set:
            return partial(self.drop_entity, attr.replace('drop_',''))
