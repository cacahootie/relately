
def Info(engine, schema, view):
    sql = engine.jenv.get_template('info.sql').render()
    return engine.execute(sql, {
        "schema": schema,
        "view": view
    })

_pg_to_json_datatype = {
    "bigint": "integer",
    "bool": "boolean",
    "double precision": "number",
    "integer": "integer"
}

def _process_field(field_info):
    return field_info['column_name'], {
        "type": _pg_to_json_datatype.get(field_info['data_type'], "string")
    }

def _process_required(view_info):
    return [ x for x in view_info if x['is_nullable'] == 'NO' ]

def JsonSchema(engine, url, schema, view):
    info = Info(engine, schema, view)
    jschema = {
        "id": url,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "relately json schema for {}.{}".format(schema, view),
        "type": "object",
        "properties": dict( _process_field(x) for x in info )
    }
    required = _process_required(info)
    if required:
        jschema['required'] = required
    return jschema
