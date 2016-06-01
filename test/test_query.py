
import unittest

import psycopg2

from relately.select import Select

from . import RelatelyTest


class TestQuery(RelatelyTest):

    def test_star_from_table(self):
        r = self.engine.select({
            "columns":'*',
            "target":"world.city"
        })
        self.assertEqual(len(r), 4079)
        self.assertEqual(len(r[0]), 5)

    def test_bad_column(self):
        with self.assertRaises(ValueError):
            self.engine.select({
                "columns":("name;DROP TABLE WORLD.city;",),
                "target":"world.city"
            })

    def test_bad_table(self):
        with self.assertRaises(ValueError):
            self.engine.select({
                "columns":"*",
                "target":"world.city;DROP TABLE WORLD.city;"
            })

    def test_columns_from_table(self):
        r = self.engine.select({
            "columns":('name','countrycode'),
            "target":"world.city"
        })
        self.assertEqual(len(r), 4079)
        self.assertEqual(len(r[0]), 2)

    def test_column_from_table(self):
        r = self.engine.select({
            "columns":('name',),
            "target":"world.city"
        })
        self.assertEqual(len(r), 4079)
        self.assertEqual(len(r[0]), 1)

    def test_star_from_tables(self):
        r = self.engine.select({
            "columns":'*',
            "target":("join_test.t1", "join_test.t2")
        })
        self.assertEqual(len(r), 9)
        self.assertEqual(len(r[0]), 3)

    def test_where(self):
        r = self.engine.select({
            "columns":('name',),
            "target":"world.city",
            "all":[
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "ARG"
                }
            ]
        })
        self.assertEqual(len(r), 57)

    def test_all(self):
        r = self.engine.select({
            "columns":('name',),
            "target":"world.city",
            "all":[
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "ARG"
                },
                {
                    "left_operand": "name",
                    "operator": "=",
                    "right_operand": "Quilmes"
                }
            ]
        })
        self.assertEqual(len(r), 1)

    def test_any(self):
        r = self.engine.select({
            "columns":('name',),
            "target":"world.city",
            "any":[
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "ARG"
                },
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "BRA"
                }
            ]
        })
        self.assertEqual(len(r), 307)

    def test_any_none(self):
        r = self.engine.select({
            "columns":('name',),
            "target":"world.city",
            "any":[
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "ARG"
                },
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "BRA"
                }
            ],
            "none":[
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "ARG"
                }
            ]
        })
        self.assertEqual(len(r), 250)

    def test_none(self):
        r = self.engine.select({
            "columns":('name',),
            "target":"world.city",
            "none":[
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "ARG"
                },
                {
                    "left_operand": "countrycode",
                    "operator": "=",
                    "right_operand": "BRA"
                }
            ]
        })
        self.assertEqual(len(r), 3772)

    def test_nonexistent_column(self):
        with self.assertRaises(psycopg2.ProgrammingError):
            self.engine.select({
                "columns":('name','barleycorn'),
                "target":"world.city"
            })

    def test_cross_join(self):
        r = self.engine.select({
            "columns":"*",
            "target":"join_test.t1",
            "join":{
                "outer":"cross",
                "target":"join_test.t2"
            }
        })
        self.assertEqual(len(r), 9)
        self.assertEqual(len(r[0]), 3)

    def test_inner_join_on(self):
        r = self.engine.select({
            "columns":"*",
            "target":"join_test.t1",
            "join":{
                "target":"join_test.t2",
                "on": {
                    "left_operand": "t1.num",
                    "operator": "=",
                    "right_operand": "t2.num"
                }
            }
        })
        self.assertEqual(len(r), 2)
        self.assertEqual(len(r[0]), 3)

    def test_inner_join_using(self):
        r = self.engine.select({
            "columns":"*",
            "target":"join_test.t1",
            "join":{
                "target":"join_test.t2",
                "using": "num"
            }
        })
        self.assertEqual(len(r), 2)
        self.assertEqual(len(r[0]), 3)

    def test_natural_inner_join(self):
        r = self.engine.select({
            "columns":"*",
            "target":"join_test.t1",
            "join":{
                "target":"join_test.t2",
                "on": "natural"
            }
        })
        self.assertEqual(len(r), 2)
        self.assertEqual(len(r[0]), 3)

    def test_bobbytables_join(self):
        with self.assertRaises(ValueError):
            self.engine.select({
                "columns":"*",
                "target":"join_test.t1",
                "join":{
                    "outer":"LEFT; DROP join_test.t1;",
                    "target":"join_test.t2",
                    "on": {
                        "left_operand": "t1.num",
                        "operator": "=",
                        "right_operand": "t2.num"
                    }
                }
            })

    def test_left_join_on(self):
        r = self.engine.select({
            "columns":"*",
            "target":"join_test.t1",
            "join":{
                "outer":"left",
                "target":"join_test.t2",
                "on": {
                    "left_operand": "t1.num",
                    "operator": "=",
                    "right_operand": "t2.num"
                }
            }
        })
        self.assertEqual(len(r), 3)
        self.assertEqual(len(r[0]), 3)

    def test_left_join_using(self):
        r = self.engine.select({
            "columns":"*",
            "target":"join_test.t1",
            "join":{
                "outer":"left",
                "target":"join_test.t2",
                "using": "num"
            }
        })
        self.assertEqual(len(r), 3)
        self.assertEqual(len(r[0]), 3)

    def test_full_join_on(self):
        r = self.engine.select({
            "columns":"*",
            "target":"join_test.t1",
            "join":{
                "outer":"full",
                "target":"join_test.t2",
                "on": {
                    "left_operand": "t1.num",
                    "operator": "=",
                    "right_operand": "t2.num"
                }
            }
        })
        self.assertEqual(len(r), 4)
        self.assertEqual(len(r[0]), 3)

    def test_func(self):
        r = self.engine.select({
            "columns":("max|num",),
            "target":"join_test.t1"
        })
        self.assertEqual(r[0]['max'], 3)

    def test_group_by(self):
        r = self.engine.select({
            "columns":("max|num",),
            "target":"join_test.t1",
            "group_by":("name",)
        })
        self.assertEqual(len(r), 3)

    def test_having(self):
        r = self.engine.select({
            "columns":("name", "max|num"),
            "target":"join_test.t1",
            "group_by":("name",),
            "having_all":({
                "left_operand": "sum|num",
                "operator": ">",
                "right_operand": 1
            },)
        })
        self.assertEqual(len(r), 2)

    def test_having_all_none(self):
        r = self.engine.select({
            "columns":("name", "max|num"),
            "target":"join_test.t1",
            "group_by":("name",),
            "having_all":({
                "left_operand": "sum|num",
                "operator": ">",
                "right_operand": 1
            },),
            "having_none":({
                "left_operand": "sum|num",
                "operator": "<",
                "right_operand": 3
            },)
        })
        self.assertEqual(len(r), 1)

    def test_having_bobbytables(self):
        with self.assertRaises(psycopg2.DataError):
            r = self.engine.select({
                "columns":("name", "max|num"),
                "target":"join_test.t1",
                "group_by":("name",),
                "having_all":({
                    "left_operand": "sum|num",
                    "operator": ">",
                    "right_operand": "noodle;DROP SCHEMA join_test;"
                },)
            })

    def test_json(self):
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
        r = self.engine.select(jstr)
        self.assertEqual(len(r), 57)
