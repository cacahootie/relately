
def aggregate_right_operand(query):
    kws = ('all', 'any', 'none', 'having_all', 'having_any', 'having_none')
    subcount, subvals = 0, []
    for kw in kws:
        try:
            params = []
            for x in query[kw]:
                params.append(x['right_operand'])
                x['right_operand'] = '%({})s'.format(subcount)
                subcount += 1
        except KeyError:
            continue
        subvals += params
    return query, subvals


def Select(engine, query, mogrify=False):
    query, params = aggregate_right_operand(query)
    fil = lambda x: True if x[0] is not None else False
    where = (
        (query.get('all'), "AND"),
        (query.get('any'), "OR"),
        (query.get('none'),"AND",True)
    )
    query['_where'] = filter(fil, where)
    having = (
        (query.get('having_all'), "AND"),
        (query.get('having_any'), "OR"),
        (query.get('having_none'),"AND",True)
    )
    query['_having'] = filter(fil, having)
    sql = engine.jenv.get_template('select.sql').render(query=query)
    if mogrify:
        return engine.mogrify(sql, params)
    return engine.execute(sql, params)
