# relately
rest interface for postgresql select queries.

# Use
This is a standard flask/wsgi app, so the general aspects of running in dev mode
and deploying behind gunicorn/uwsgi and nginx should go without saying.  There's
a file in the project root, `run.py` which will run a simple development version,
and a file `relately-server` which is a CLI script intended to be used for
general development _outside_ this project.

If you have a postgres database `relately` and access as a superuser on your
current account you can run relately with just:

`relately-server`

which will run on port 8008 by default.

If you need to specify the connection details and/or port, you may do so as such:

`relately-server -p 8008 -d relately -u relately --password plaintextreally`

Obviously it's preferred to have something more sophisticated than a plain text
password.  Also, if you're going to expose this publicly, the database user should
have limited permissions (i.e. use on the schema it needs to see and select on the
tables/views it needs), and in any more critical environment it should probably be
a read-only slave database for safety purposes.

# API
Currently the server supports one method, `select` in either GET or POST.  relately
uses the built-in json serialization in postgresql, so be cognizant of default json
serialization for custom or complex types.

## Get
`/select/<schema>/<entity>` :: `{"results":[{},{}]}`

## Post
`/select` with a json body of a query:

```javascript
{
    "columns":["name", "max|num"],
    "target":"join_test.t1",
    "group_by":["name"],
    "having_all":[{
        "left_operand": "sum|num",
        "operator": ">",
        "right_operand": 1
    }],
    "having_none":[{
        "left_operand": "sum|num",
        "operator": "<",
        "right_operand": 3
    }]
}
```
or 
```javascript
{
    "columns":"*",
    "target":"join_test.t1",
    "join":{
        "outer":"left",
        "target":"join_test.t2",
        "using": "num"
    }
}
```
You may also add the query string parameter `?mogrify=True` which will return
the compiled SQL rather than executing the query.

Currently, relately is very rude about headers.  It neither looks at nor writes
them, so expect json in and json out for now.

# Testing
This package is covered by a test suite which is intended to be run by green,
nose or some other similar tool that will auto-detect testing files.  The tests
do depend on the sql in `test/test_data` having been run to set up the world
and join_test schema.  Currently, the package has 100% test coverage (except for
some debugging logging lines...).  To run the tests, you should install the test
runner of your choice globablly using pip, i.e. `sudo pip install green`.
