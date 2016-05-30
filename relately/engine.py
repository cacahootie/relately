
from functools import partial
import os
import string

from jinja2 import Environment, FileSystemLoader
import psycopg2
import psycopg2.extras
import sqlparse

import select


# Controls logging of SQL queries to stdout
DEBUG = bool(os.environ.get('DEBUG'))
LOGALL = bool(os.environ.get('LOGALL'))

_valid_chars = string.ascii_letters + string.digits + '_-'
_valid_joins = ('left', 'right', 'full', 'cross')

def quote_wrap(s):
    return '"' + s + '"'

def _allowed_chars(name):
    if not set(name).issubset(_valid_chars):
        raise ValueError(str(list(set(name) - set(_valid_chars)))
            + ' not valid characters')
    return name

def _sql_entity(name):
    if '|' in name:
        fname, ftarget = name.split('|')
        return "{}({})".format(_sql_entity(fname), _sql_entity(ftarget))
    if '.' in name:
        p = name.split('.')
        return '.'.join(quote_wrap(_allowed_chars(x)) for x in p)
    else:
        return _allowed_chars(name)

def _sql_entities(entities):
    if isinstance(entities, basestring):
        return _sql_entity(entities)
    return [_sql_entity(x) for x in entities]

def _valid_join(join):
    if join not in _valid_joins:
        raise ValueError("Invalid join: " + join)
    return join


class Engine(object):
    """Encapsulate access to a database."""

    def __init__(self):
        """Establish the database connection and jinja environment."""
        self.jenv = Environment(loader=FileSystemLoader('./templates'))
        self.jenv.filters['sql_entities'] = _sql_entities
        self.jenv.filters['valid_joins'] = _valid_join
        self.conn = psycopg2.connect(self.conn_string)

    def execute(self,stmt,params=None):
        """Execute the statement in a transaction, parameters optional."""
        with self.conn as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as c:
                args = (stmt,) if params is None else (stmt,params)
                try:
                    c.execute(*args)
                    if LOGALL: self.messageify(stmt, params)
                except Exception as e:
                    if DEBUG: self.messageify(stmt, params, e)
                    raise

                try:
                    return list(c) if c.rowcount != -1 else None
                except psycopg2.ProgrammingError as e:
                    if DEBUG: self.messageify(stmt, params, e)
                    raise

    def messageify(self, stmt, params=None, error=None):
        print self.jenv.get_template('sys/sql_error.txt').render(
            error = error,
            sql = self.mogrify(stmt, params)
        )

    def mogrify(self, stmt, params=None):
        """Combines statement and params to string for human use."""
        with self.conn as conn:
            with conn.cursor() as c:
                return sqlparse.format(
                    c.mogrify(stmt,params), reindent=True, keyword_case='upper')

    @property
    def conn_string(self):
        return 'dbname=relately user=relately'

    def select(self, query, mogrify=False):
        return select.Select(self, query, mogrify)
