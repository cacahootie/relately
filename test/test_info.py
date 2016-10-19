
import json
import os.path
import unittest

import psycopg2
from jsonschema import validate

from relately.select import Select

from . import RelatelyTest

here = os.path.dirname(os.path.abspath(__file__))

class TestQuery(RelatelyTest):

    with open(os.path.join(here, 'test_data', 'json_schema.json')) as f:
        json_schema = json.load(f)

    def test_fields_appear(self):
        r = self.engine.json_schema(
            'http://local-relately:8000/json_schema/world/cities',
            'world',
            'cities'
        )
        fields = set(r['properties'].keys())
        expected = set(('countrycode', 'district', 'id', 'name', 'population'))
        self.assertEqual(fields, expected)

    def test_valid_schema(self):
        r = self.engine.json_schema(
            'http://local-relately:8000/json_schema/world/cities',
            'world',
            'cities'
        )
        validate(r, self.json_schema)
