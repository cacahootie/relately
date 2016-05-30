
import unittest

import relately.engine as engine

class RelatelyTest(unittest.TestCase):

    def setUp(self):
        "Instantiate a test instance of the engine"
        self.engine = engine.Engine()
