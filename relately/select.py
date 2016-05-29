
def Select(engine, query, mogrify=False):
    sql = engine.jenv.get_template('select.sql').render(query=query)
    if mogrify:
        return engine.mogrify(sql)
    return engine.execute(sql)
