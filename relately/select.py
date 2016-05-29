
def Select(engine, query, mogrify=False):
    sql = engine.jenv.get_template('select.sql').render(query=query)
    if mogrify:
        return engine.mogrify(sql)
    params = None
    if 'where' in query:
        params = [x['right_operand'] for x in query['where']]
    return engine.execute(sql, params)
