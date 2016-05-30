# relately
rest interface for postgresql select queries.

# Use
This is a standard flask/wsgi app, so the general aspects of running in dev mode
and deploying behind gunicorn/uwsgi and nginx should go without saying.  There's
a file in the project root, `run.py` which will run a simple development version.

# API
Currently the server supports one method, `select` in either GET or POST.

## Get
`/select/<schema>/<entity>` :: `{"results":[[],[]]}`

## Post
`/select` with a json body of a query:

```javascript
{
    "columns":["name"],
    "target":"world.city",
    "all":[
        {
            "left_operand": "countrycode",
            "operator": "=",
            "right_operand": "ARG"
        }
    ]
}
```

# Testing
This package is covered by a test suite which is intended to be run by green,
nose or some other similar tool that will auto-detect testing files.  The tests
do depend on the sql in `test/test_data` having been run to set up the world
and join_test schema.  Currently, the package has 100% test coverage (except for
some debugging logging lines...).
