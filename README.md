# relately
rest interface for postgresql select queries.

# Use
This is a standard flask/wsgi app, so the general aspects of running in dev mode
and deploying behind gunicorn/uwsgi and nginx should go without saying.  There's
a file in the project root, `run.py` which will run a simple development version,
and a file `relately-server` which is a CLI script intended to be used for
general development _outside_ this project.

`relately-server -p 8008 -d relately -u relately --password plaintextreally`

# API
Currently the server supports one method, `select` in either GET or POST.

## Get
`/select/<schema>/<entity>` :: `{"results":[[],[]]}`

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

# Testing
This package is covered by a test suite which is intended to be run by green,
nose or some other similar tool that will auto-detect testing files.  The tests
do depend on the sql in `test/test_data` having been run to set up the world
and join_test schema.  Currently, the package has 100% test coverage (except for
some debugging logging lines...).
