
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

    def create_schema(self, name):
        s = entities.Schema(name)
        self.execute(s.create_sql)
        return s

    def drop_schema(self, name, if_exists=False):
        s = entities.Schema(name)
        self.execute(s.drop_sql)
