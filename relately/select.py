
def Select(engine, query, mogrify=False):
    sql = engine.jenv.get_template('select.sql').render(query=query)
    if mogrify:
        return engine.mogrify(sql)
    params = None
    if 'where' in query:
        params = [x['right_operand'] for x in query['where'] or query]
    if 'any' in query:
        params = [x['right_operand'] for x in query['any'] or query]
    return engine.execute(sql, params)
