
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
		self.engine.drop_schema("test_create_schema",if_exists=True, cascade=True)
		s = self.engine.create_schema("test_create_schema")
		r = self.engine.execute(
			"select schema_name from information_schema.schemata")
		self.assertTrue(
			'test_create_schema' in set(x['schema_name'] for x in r))
		self.engine.drop_schema("test_create_schema")

	def test_create_table(self):
		self.engine.drop_schema("test_create_table",if_exists=True, cascade=True)
		s = self.engine.create_schema("test_create_table")
		t = self.engine.create_table(s,"test_table")
		r = self.engine.execute("""
			SELECT table_name FROM information_schema.tables 
			WHERE table_schema = 'test_create_table'
		""")
		self.assertTrue(
			'test_table' in set(x['table_name'] for x in r))
		self.engine.drop_table(s,"test_table")
		self.engine.drop_schema("test_create_table")

def getTests(cls):
    return unittest.TestLoader().loadTestsFromTestCase(cls)
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(getTests(TestDDL))
    return suite

if __name__ == '__main__':
    unittest.main()