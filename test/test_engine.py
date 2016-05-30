from . import RelatelyTest


class TestEngine(RelatelyTest):

    def test_execute(self):
        "Make sure we can execute a text-only query"
        r = self.engine.execute("select version()")
        self.assertTrue(
            r[0]['version'].startswith('PostgreSQL'))