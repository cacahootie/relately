
import unittest
import json

from relately.server import app

class ServerTest(unittest.TestCase):

    def setUp(self):
        "Instantiate a test instance of the engine"
        app.config['DEBUG'] = True
        with app.test_client() as c:
            self.c = c

    def test_request(self):
        jstr = """{
            "columns":["name"],
            "target":"world.city",
            "all":[
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "ARG"
                }
            ]
        }"""
        r = self.c.post('/select', data=jstr)
        r = json.loads(r.data)["results"]
        self.assertEqual(len(r), 57)

    def test_request_mogrify(self):
        jstr = """{
            "columns":["name"],
            "target":"world.city",
            "all":[
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "ARG"
                }
            ]
        }"""
        r = self.c.post('/select?mogrify=True', data=jstr)
        r = r.data
        print r

    def test_get_request(self):
        r = self.c.get('/select/join_test/t1')
        r = json.loads(r.data)["results"]
        self.assertEqual(len(r), 3)