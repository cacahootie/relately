
import unittest

import engine

class RelatelyTest(unittest.TestCase):

	def setUp(self):
		"Instantiate a test instance of the engine"
		self.engine = engine.Engine()

class TestEngine(RelatelyTest):

	def test_execute(self):
		"Make sure we can execute a text-only query"
		r = self.engine.execute("select version()")
		self.assertTrue(
			r[0]['version'].startswith('PostgreSQL'))

class TestDDL(RelatelyTest):

	def test_create_schema(self):
		self.engine.drop_schema("ddl_test",if_exists=True)
		db = self.engine.create_schema("ddl_test")
		r = self.engine.execute(
			"select schema_name from information_schema.schemata")
		self.assertTrue(
			'ddl_test' in set(x['schema_name'] for x in r))

def getTests(cls):
    return unittest.TestLoader().loadTestsFromTestCase(cls)
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(getTests(TestDDL))
    return suite

if __name__ == '__main__':
    unittest.main()